#!/usr/bin/env python3
from pathlib import Path
import urllib.request, json
from urllib.parse import urlsplit, urlunsplit, quote, unquote
BASE = Path('/workspaces/Python-Curso-em-Video')
LOCAL_DIR = BASE / 'Curso em Video - Python'
API_URL = 'https://api.github.com/repos/andreinaoliveira/Exercicios-Python/contents/Exercicios'
OUT = BASE / 'scripts' / 'byte_compare_all_report.json'

with urllib.request.urlopen(API_URL) as r:
    data = json.loads(r.read().decode('utf-8'))
mapping = {}
import re
for item in data:
    name = item.get('name','')
    m = re.match(r"^(\d{3})\s*-\s*(.*)$", name)
    if m:
        mapping[m.group(1)] = item.get('download_url')
report = {'equal': [], 'different': [], 'missing_local': [], 'no_remote': []}
for i in range(1,116):
    key = f'{i:03}'
    name = f'Ex{i:03}.py'
    lp = LOCAL_DIR / name
    remote = mapping.get(key)
    if not remote:
        report['no_remote'].append(name)
        continue
    try:
        parts = urlsplit(remote)
        raw_path = unquote(parts.path)
        path = quote(raw_path)
        safe_url = urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))
        with urllib.request.urlopen(safe_url) as r:
            remote_bytes = r.read()
    except Exception as e:
        report.setdefault('remote_errors', []).append({'name': name, 'error': str(e), 'remote': remote})
        continue
    if not lp.exists():
        report['missing_local'].append(name)
        continue
    local_bytes = lp.read_bytes()
    if local_bytes == remote_bytes:
        report['equal'].append(name)
    else:
        report['different'].append(name)

OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('done. equal:', len(report['equal']), 'different:', len(report['different']), 'missing_local:', len(report['missing_local']), 'no_remote:', len(report['no_remote']))
