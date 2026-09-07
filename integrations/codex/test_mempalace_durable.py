import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import mempalace_durable as durable


class DurableCheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.project = self.root / 'labs-wiki'
        self.project.mkdir()
        (self.project / 'report.md').write_text('Verified evidence')
        self.state = self.root / 'checkpoints'
        self.patches = [patch.object(durable, 'PROJECT', self.project), patch.object(durable, 'STATE', self.state)]
        for p in self.patches:
            p.start()
        self.payload = {'project': 'labs-wiki', 'items': [
            {'kind': 'result', 'state': 'tested', 'summary': 'Regression checks passed; deployment remains unverified.', 'evidence': ['report.md']}
        ]}
        self.session = 'session-123'

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        self.temp.cleanup()

    def test_stage_and_save_deduplicate_and_preserve_certainty(self):
        first = durable.stage(self.payload, self.session)
        self.assertEqual(durable.stage(self.payload, self.session), first)
        save = Mock(return_value={'success': True, 'drawer_id': 'drawer-1'})
        self.assertEqual(durable.flush(self.session, save), 1)
        self.assertEqual(durable.flush(self.session, save), 0)
        durable.stage(self.payload, self.session)
        self.assertEqual(durable.flush(self.session, save), 0)
        save.assert_called_once()
        record = json.loads(save.call_args.args[0])
        self.assertEqual(record['checkpoint'], self.payload)
        self.assertEqual(record['session_id'], self.session)
        self.assertIn('captured', record)
        changed = copy.deepcopy(self.payload)
        changed['items'][0]['state'] = 'deployed'
        durable.stage(changed, self.session)
        self.assertEqual(durable.flush(self.session, save), 1)

    def test_writer_failure_retains_checkpoint_for_retry(self):
        durable.stage(self.payload, self.session)
        with self.assertRaises(ValueError):
            durable.flush(self.session, lambda content: {'success': False})
        self.assertEqual(len(list(durable.session_dir(self.session).glob('*.json'))), 1)
        self.assertEqual(durable.flush(self.session, lambda content: {'success': True}), 1)

    def test_rejects_sensitive_unscoped_and_unsupported_data_before_staging(self):
        for summary in ('Authorization: Bearer dummy-token', 'The api_key=super-private-value was configured.', 'password: private-value'):
            bad = copy.deepcopy(self.payload)
            bad['items'][0]['summary'] = summary
            with self.assertRaises(ValueError):
                durable.stage(bad, self.session)
        for ref in ('../report.md', '/etc/passwd', 'missing.md'):
            bad = copy.deepcopy(self.payload)
            bad['items'][0]['evidence'] = [ref]
            with self.assertRaises(ValueError):
                durable.stage(bad, self.session)
        for change in ({'project': 'other'}, {'items': []}, {'transcript': 'unapproved'}):
            with self.assertRaises(ValueError):
                durable.stage({**self.payload, **change}, self.session)
        self.assertFalse(self.state.exists())

    def test_rejects_tampered_envelope_without_calling_writer(self):
        durable.stage(self.payload, self.session)
        path = next(durable.session_dir(self.session).glob('*.json'))
        record = json.loads(path.read_text())
        record['raw_log'] = 'unapproved data'
        path.write_text(json.dumps(record))
        save = Mock()
        with self.assertRaises(ValueError):
            durable.flush(self.session, save)
        save.assert_not_called()

    def test_scope_passthrough_and_precompact_without_transcript_reads(self):
        start = {'hook_event_name': 'SessionStart', 'session_id': self.session, 'cwd': str(self.project)}
        self.assertIn('authorized', durable.hook(start)['hookSpecificOutput']['additionalContext'])
        with patch.object(durable, 'flush', return_value=1) as flush:
            self.assertIn('saved 1', durable.hook({**start, 'hook_event_name': 'PreCompact'})['systemMessage'])
            flush.assert_called_once_with(self.session)
        with patch('subprocess.run', return_value=Mock(returncode=0, stdout='{}')) as run:
            self.assertEqual(durable.hook({**start, 'cwd': str(self.root), 'hook_event_name': 'Stop'}), {})
            self.assertIn('stop', run.call_args.args[0])
        durable.stage(self.payload, self.session)
        with patch.object(durable, 'flush', return_value=0) as flush:
            durable.hook({**start, 'cwd': str(self.root), 'hook_event_name': 'Stop'})
            flush.assert_called_once()

    def test_private_state_and_input_bounds(self):
        with self.assertRaises(ValueError):
            durable.read_json(io.StringIO('x' * (durable.LIMIT + 1)))
        with self.assertRaises(ValueError):
            durable.session_dir('../escape')
        durable.stage(self.payload, self.session)
        self.assertEqual(self.state.stat().st_mode & 0o777, 0o700)
        self.assertEqual(next(durable.session_dir(self.session).glob('*.json')).stat().st_mode & 0o777, 0o600)


if __name__ == '__main__':
    unittest.main()
