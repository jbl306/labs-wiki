#!/home/jbl/.local/share/pipx/venvs/mempalace/bin/python
"""Selective Labs Wiki checkpoints; other sessions retain native MemPalace hooks."""

import fcntl
import hashlib
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path('/home/jbl/projects/labs-wiki')
STATE = Path.home() / '.mempalace' / 'codex_checkpoints'
NATIVE = '/home/jbl/.local/bin/mempalace'
LIMIT = 16_384
EVENTS = {'SessionStart': 'session-start', 'Stop': 'stop', 'PreCompact': 'precompact'}
SENSITIVE = re.compile(
    r'(?i)(?:bearer\s+\S+|-----BEGIN .*PRIVATE KEY|'
    r'(?:password|passwd|secret|token|api[_-]?key|authorization|cookie)\s*[=:]\s*\S+|'
    r'\b(?:sk-[a-zA-Z0-9_-]{16,}|gh[pousr]_[a-zA-Z0-9]{16,}|github_pat_\w+)|'
    r'https?://[^\s/]+:[^\s/]+@)'
)


def read_json(stream):
    text = stream.read(LIMIT + 1)
    if len(text) > LIMIT:
        raise ValueError('checkpoint exceeds size limit')
    return json.loads(text)


def private_dir(path):
    path.mkdir(mode=0o700, exist_ok=True)
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError('checkpoint directory must be private and owned by the current user')


def sync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def session_dir(session):
    if not isinstance(session, str) or not re.fullmatch(r'[a-zA-Z0-9_-]{1,128}', session):
        raise ValueError('a valid Codex session ID is required')
    return STATE / hashlib.sha256(session.encode()).hexdigest()


def validate(payload):
    if not isinstance(payload, dict) or set(payload) != {'project', 'items'} or payload['project'] != 'labs-wiki':
        raise ValueError('only Labs Wiki checkpoints are authorized')
    items = payload['items']
    if not isinstance(items, list) or not 1 <= len(items) <= 8:
        raise ValueError('checkpoint needs 1-8 durable items')
    for item in items:
        if not isinstance(item, dict) or set(item) != {'kind', 'state', 'summary', 'evidence'}:
            raise ValueError('invalid checkpoint item fields')
        if item['kind'] not in ('decision', 'result', 'blocker') or item['state'] not in (
            'planned', 'implemented', 'tested', 'deployed', 'unresolved'
        ):
            raise ValueError('invalid checkpoint kind or state')
        summary = item['summary']
        if not isinstance(summary, str) or not 15 <= len(summary.strip()) <= 800 or any(ord(c) < 32 for c in summary):
            raise ValueError('summary must be a compact single-line fact')
        evidence = item['evidence']
        if not isinstance(evidence, list) or not 1 <= len(evidence) <= 4:
            raise ValueError('each item needs 1-4 project file references')
        for ref in evidence:
            if not isinstance(ref, str) or len(ref) > 240:
                raise ValueError('invalid evidence reference')
            path = Path(ref)
            resolved = (PROJECT / path).resolve()
            if (path.is_absolute() or '..' in path.parts or
                not resolved.is_relative_to(PROJECT.resolve()) or not resolved.is_file() or
                any(part.startswith('.') for part in path.parts) or
                resolved.suffix.lower() in ('.log', '.db', '.sqlite', '.sqlite3', '.jsonl') or
                re.search(r'(?i)(?:auth|credential|secret|history|\.env)', ref)):
                raise ValueError('evidence must reference a non-sensitive project file')
    if SENSITIVE.search(json.dumps(payload)):
        raise ValueError('potential credential detected; checkpoint rejected')
    return payload


def stage(payload, session):
    payload = validate(payload)
    directory = session_dir(session)
    if not STATE.parent.is_dir():
        raise ValueError('MemPalace is not initialized')
    private_dir(STATE)
    private_dir(directory)
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    key = hashlib.sha256(canonical.encode()).hexdigest()
    target = directory / f'{key}.json'
    if not target.exists() and not target.with_suffix('.saved').exists():
        record = {'session_id': session, 'captured': datetime.now(timezone.utc).isoformat(), 'checkpoint': payload}
        # Publish a complete checkpoint atomically; hooks never see a partial JSON file.
        import tempfile
        fd, temporary = tempfile.mkstemp(dir=directory)
        try:
            with os.fdopen(fd, 'w') as handle:
                json.dump(record, handle, sort_keys=True, ensure_ascii=False)
                handle.flush()
                os.fsync(handle.fileno())
            try:
                os.link(temporary, target)
            except FileExistsError:
                pass
            sync_dir(directory)
        finally:
            Path(temporary).unlink(missing_ok=True)
    return {'staged': True, 'checkpoint_id': key}


def native_save(content):
    # Respect the installed hook routing policy, including required-daemon failures.
    from mempalace import hooks_cli
    if not hooks_cli._palace_root_exists() or not hooks_cli.MempalaceConfig().hooks_auto_save:
        raise ValueError('native memory capture is disabled')
    routing = hooks_cli._compute_hook_write_routing()
    if routing.blocked or routing.use_daemon:
        raise ValueError('checkpoint pending: native direct writer is unavailable under the hook routing policy')
    from mempalace.mcp_server import tool_add_drawer
    return tool_add_drawer(wing='labs_wiki', room='session-checkpoints', content=content, added_by='codex')


def flush(session, save=native_save):
    directory = session_dir(session)
    if not directory.exists():
        return 0
    private_dir(STATE)
    private_dir(directory)
    saved = 0
    with (STATE / 'save.lock').open('a') as lock:
        os.chmod(lock.name, 0o600)
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in sorted(directory.glob('*.json')):
            if path.is_symlink():
                raise ValueError('checkpoint must be a regular owned file')
            with path.open() as handle:
                record = read_json(handle)
            if not isinstance(record, dict) or set(record) != {'session_id', 'captured', 'checkpoint'}:
                raise ValueError('invalid checkpoint envelope')
            if record.get('session_id') != session:
                raise ValueError('checkpoint session mismatch')
            if not isinstance(record['captured'], str) or len(record['captured']) > 40:
                raise ValueError('invalid capture timestamp')
            datetime.fromisoformat(record['captured'])
            payload = validate(record['checkpoint'])
            key = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            if path.stem != key:
                raise ValueError('checkpoint digest mismatch')
            receipt = path.with_suffix('.saved')
            if not receipt.exists():
                content = json.dumps(record, sort_keys=True, ensure_ascii=False)
                result = save(content)
                if not isinstance(result, dict) or result.get('success') is not True:
                    raise ValueError('MemPalace did not confirm the checkpoint; retained for retry')
                with receipt.open('x') as handle:
                    os.chmod(receipt, 0o600)
                    json.dump({'drawer_id': result.get('drawer_id')}, handle)
                    handle.flush()
                    os.fsync(handle.fileno())
                saved += 1
                sync_dir(directory)
            path.unlink()
            sync_dir(directory)
    return saved


def hook(event):
    name = event.get('hook_event_name')
    if name not in EVENTS:
        return {}
    session = event.get('session_id', '')
    directory = session_dir(session)
    cwd = Path(event.get('cwd') or '.').resolve()
    scoped = cwd.is_relative_to(PROJECT.resolve()) or directory.exists()
    if not scoped:
        # Delegate unchanged installed behavior without reading the transcript here.
        import subprocess
        result = subprocess.run([NATIVE, 'hook', 'run', '--hook', EVENTS[name], '--harness', 'codex'],
                                input=json.dumps(event), text=True, capture_output=True, timeout=110)
        if result.returncode:
            raise ValueError('native MemPalace hook failed')
        return json.loads(result.stdout or '{}')
    if name == 'SessionStart':
        return {'hookSpecificOutput': {'hookEventName': name, 'additionalContext': (
            'Labs Wiki durable checkpoint capture is authorized. Follow the Labs Wiki session memory '
            'section in ~/.codex/AGENTS.md. Stage concise evidence-backed checkpoints at meaningful '
            f'milestones and before your final response. Session ID: {session}. '
            'Routine conversation needs no checkpoint. Stop/PreCompact save staged items automatically.'
        )}}
    count = flush(session)
    return {'systemMessage': f'MemPalace saved {count} durable Labs Wiki checkpoint(s).'} if count else {}


def main():
    if sys.argv[1:2] == ['--mcp']:
        # Extend the installed server in its own process: it owns the palace lock.
        from mempalace import mcp_server as server
        name = 'mempalace_durable_hook'
        server.TOOLS[name] = {
            'description': 'Run the authorized selective Labs Wiki checkpoint hook; accepts Codex lifecycle metadata only.',
            'input_schema': {'type': 'object', 'properties': {'event': {'type': 'object'}}, 'required': ['event']},
            'handler': safe_hook,
        }
        # Preserve native read-only, writer-lock, and vector-write admission gates.
        for gate in ('_MUTATING_TOOLS', '_VECTOR_WRITE_TOOLS', '_READ_ONLY_REFUSED_TOOLS'):
            setattr(server, gate, getattr(server, gate) | {name})
        del sys.argv[1]
        server.main()
        return 0
    exit_code = 0
    try:
        if sys.argv[1:] == ['--stage']:
            result = stage(read_json(sys.stdin), os.environ.get('CODEX_THREAD_ID', ''))
        elif sys.argv[1:] == ['--flush']:
            result = {'saved': flush(os.environ.get('CODEX_THREAD_ID', ''))}
        else:
            result = hook(read_json(sys.stdin))
    except Exception:
        # Errors must never echo submitted content or credentials into the chat/logs.
        result = {'systemMessage': 'MemPalace durable checkpoint failed; pending data was retained. Check schema, private state directory, and native writer availability.'}
        if sys.argv[1:]:
            exit_code = 1
    # The native MCP module redirects Python stdout; hooks_cli preserves the real descriptor.
    from mempalace.hooks_cli import _output
    _output(result)
    return exit_code


def safe_hook(event):
    try:
        return hook(event)
    except Exception:
        return {'systemMessage': 'MemPalace durable checkpoint failed; pending data retained for retry.'}


if __name__ == '__main__':
    raise SystemExit(main())
