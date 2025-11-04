#!/usr/bin/env python3
from pathlib import Path
import json
import urllib.request
from urllib.parse import urlsplit, urlunsplit, quote

BASE = Path('/workspaces/Python-Curso-em-Video')
LOCAL_DIR = BASE / 'Curso em Video - Python'
LOCAL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_IN = BASE / 'scripts' / 'verify_report_v2.json'
OUT = BASE / 'scripts' / 'sync_report.json'

report = {'updated': [], 'failed': []}

data = json.loads(REPORT_IN.read_text(encoding='utf-8'))
for m in data.get('mismatches', []):
    name = m['name']
    remote_url = m.get('remote_url')
    if not remote_url:
        report['failed'].append({'name': name, 'reason': 'no remote_url'})
        continue
    try:
        parts = urlsplit(remote_url)
        # some download_url values may already contain percent-encodings; normalize by unquoting then quoting
        from urllib.parse import unquote
        raw_path = unquote(parts.path)
        path = quote(raw_path)
        safe_url = urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))
        with urllib.request.urlopen(safe_url) as r:
            content = r.read()
        target = LOCAL_DIR / name
        # ensure parent exists
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        report['updated'].append(name)
        print('Wrote', target)
    except Exception as e:
        report['failed'].append({'name': name, 'reason': str(e), 'remote_url': remote_url})

OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('Done. updated:', len(report['updated']), 'failed:', len(report['failed']))
