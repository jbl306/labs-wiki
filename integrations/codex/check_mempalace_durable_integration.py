"""Exercise the installed native MCP transport against an isolated palace."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
import mempalace_durable as d
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    d.PROJECT=root/'labs-wiki'
    d.PROJECT.mkdir()
    (d.PROJECT/'report.md').write_text('Integration fixture')
    d.STATE=root/'checkpoints'
    session='native-integration-1'
    d.stage({'project':'labs-wiki','items':[{'kind':'result','state':'tested','summary':'Native integration fixture verifies exact checkpoint persistence.', 'evidence':['report.md']}]},session)
    program=f"""
import sys
from pathlib import Path
sys.path.insert(0, {str(Path(__file__).resolve().parent)!r})
import mempalace_durable as d
d.STATE = Path(sys.argv[1])
d.PROJECT = Path(sys.argv[2])
sys.argv = ['mempalace', '--mcp', '--palace', *sys.argv[3:]]
d.main()
"""
    event={'hook_event_name':'Stop','session_id':session,'cwd':str(d.PROJECT)}
    requests=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'durable-integration','version':'1'}}}, {'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}}]
    for id in (3,4):
        requests.append({'jsonrpc':'2.0','id':id,'method':'tools/call','params':{'name':'mempalace_durable_hook','arguments':{'event':event}}})
    proc=subprocess.run([sys.executable,'-c',program,str(d.STATE),str(d.PROJECT),str(root/'palace')],input='\n'.join(json.dumps(r) for r in requests)+'\n',capture_output=True,text=True,timeout=60)
    replies={r['id']:r for line in proc.stdout.splitlines() if (r:=json.loads(line)).get('id')}
    assert proc.returncode==0,proc.stderr[-1000:]
    assert 'mempalace_durable_hook' in {t['name'] for t in replies[2]['result']['tools']}
    result=json.loads(replies[3]['result']['content'][0]['text'])
    assert 'saved 1' in result.get('systemMessage',''),result
    assert json.loads(replies[4]['result']['content'][0]['text'])=={},replies[4]
    receipts=list(d.session_dir(session).glob('*.saved'))
    assert len(receipts)==1
    assert json.loads(receipts[0].read_text())['drawer_id']
    assert not list(d.session_dir(session).glob('*.json'))
    readonly=subprocess.run([sys.executable,'-c',program,str(d.STATE),str(d.PROJECT),str(root/'palace'),'--read-only'],input='\n'.join(json.dumps(r) for r in requests[:2])+'\n',capture_output=True,text=True,timeout=60)
    readonly_replies={r['id']:r for line in readonly.stdout.splitlines() if (r:=json.loads(line)).get('id')}
    assert readonly.returncode==0
    assert 'mempalace_durable_hook' not in {t['name'] for t in readonly_replies[2]['result']['tools']}
    print('Native MCP transport: saved, retry skipped, receipt verified, read-only gate preserved.')
