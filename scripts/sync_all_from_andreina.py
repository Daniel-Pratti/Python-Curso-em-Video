#!/usr/bin/env python3
from pathlib import Path
import urllib.request, json
from urllib.parse import urlsplit, urlunsplit, quote, unquote
BASE = Path('/workspaces/Python-Curso-em-Video')
LOCAL_DIR = BASE / 'Curso em Video - Python'
API_URL = 'https://api.github.com/repos/andreinaoliveira/Exercicios-Python/contents/Exercicios'
OUT = BASE / 'scripts' / 'sync_all_report.json'

LOCAL_DIR.mkdir(parents=True, exist_ok=True)

with urllib.request.urlopen(API_URL) as r:
    data = json.loads(r.read().decode('utf-8'))
mapping = {}
import re
for item in data:
    name = item.get('name','')
    m = re.match(r"^(\d{3})\s*-\s*(.*)$", name)
    if m:
        mapping[m.group(1)] = item.get('download_url')

report = {'updated': [], 'failed': []}
for i in range(1,116):
    key = f'{i:03}'
    name = f'Ex{i:03}.py'
    remote = mapping.get(key)
    if not remote:
        report['failed'].append({'name': name, 'reason': 'no_remote_in_api'})
        continue
    try:
        parts = urlsplit(remote)
        raw_path = unquote(parts.path)
        path = quote(raw_path)
        safe_url = urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))
        with urllib.request.urlopen(safe_url) as r:
            content = r.read()
        target = LOCAL_DIR / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        report['updated'].append(name)
    except Exception as e:
        report['failed'].append({'name': name, 'reason': str(e), 'remote': remote})

OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('Done. updated:', len(report['updated']), 'failed:', len(report['failed']))
