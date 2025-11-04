#!/usr/bin/env python3
from pathlib import Path
import json
import urllib.request
from urllib.parse import urlsplit, urlunsplit, quote, unquote
BASE = Path('/workspaces/Python-Curso-em-Video')
LOCAL_DIR = BASE / 'Curso em Video - Python'
SYNC = BASE / 'scripts' / 'sync_report.json'
VREP = BASE / 'scripts' / 'verify_report_v2.json'

sync = json.loads(SYNC.read_text(encoding='utf-8'))
vre = json.loads(VREP.read_text(encoding='utf-8'))
map_remote = {m['name']: m.get('remote_url') for m in vre.get('mismatches', [])}

results = {'equal_bytes': [], 'diff_bytes': [], 'no_remote': []}
for name in sync.get('updated', []):
    localp = LOCAL_DIR / name
    remote_url = map_remote.get(name)
    if not remote_url:
        results['no_remote'].append(name)
        continue
    parts = urlsplit(remote_url)
    raw_path = unquote(parts.path)
    path = quote(raw_path)
    safe_url = urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))
    try:
        with urllib.request.urlopen(safe_url) as r:
            remote_bytes = r.read()
        local_bytes = localp.read_bytes()
        if remote_bytes == local_bytes:
            results['equal_bytes'].append(name)
        else:
            results['diff_bytes'].append(name)
    except Exception as e:
        results.setdefault('errors', []).append({'name': name, 'error': str(e)})

print('equal:', len(results['equal_bytes']), 'diff:', len(results['diff_bytes']), 'no_remote:', len(results['no_remote']))
Path('/workspaces/Python-Curso-em-Video/scripts/check_updates_report.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
