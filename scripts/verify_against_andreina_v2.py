#!/usr/bin/env python3
from pathlib import Path
import re
import json
import urllib.request
import difflib

BASE = Path('/workspaces/Python-Curso-em-Video')
LOCAL_DIR = BASE / 'Curso em Video - Python'
API_URL = 'https://api.github.com/repos/andreinaoliveira/Exercicios-Python/contents/Exercicios'
OUT = BASE / 'scripts' / 'verify_report_v2.json'

def extract_enunciado(text):
    m = re.match(r"\s*(?:[ruRU]{0,2})?([\"']{3})(.*?)\1", text, re.S)
    if m:
        doc = m.group(2).strip()
        if doc:
            return doc
    lines = text.lstrip().splitlines()
    comment_lines = []
    for ln in lines[:30]:
        if ln.strip().startswith('#'):
            comment_lines.append(ln.strip().lstrip('#').strip())
        elif ln.strip() == '':
            if comment_lines:
                break
        else:
            break
    if comment_lines:
        return '\n'.join(comment_lines).strip()
    nonempty = [l for l in lines if l.strip()]
    return '\n'.join(nonempty[:8]).strip() if nonempty else ''

# fetch listing via API
try:
    with urllib.request.urlopen(API_URL) as r:
        data = json.loads(r.read().decode('utf-8'))
except Exception as e:
    print('Failed to fetch API listing:', e)
    raise

# build map from number (001..115) to download_url
mapping = {}
import re
for item in data:
    name = item.get('name','')
    m = re.match(r"^(\d{3})\s*-\s*(.*)$", name)
    if m:
        num = m.group(1)
        mapping[num] = item.get('download_url')

report = {'checked': [], 'mismatches': []}
for i in range(1, 116):
    key = f'{i:03}'
    name = f'Ex{i:03}.py'
    local_path = LOCAL_DIR / name
    local_text = ''
    if local_path.exists():
        local_text = local_path.read_text(encoding='utf-8')
    remote_url = mapping.get(key)
    remote_text = ''
    remote_ok = True
    if remote_url:
        try:
            # some download_url values contain spaces; percent-encode path part
            from urllib.parse import urlsplit, urlunsplit, quote
            parts = urlsplit(remote_url)
            path = quote(parts.path)
            safe_url = urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))
            with urllib.request.urlopen(safe_url) as r:
                remote_text = r.read().decode('utf-8')
        except Exception as e:
            remote_ok = False
    else:
        remote_ok = False
    local_enu = extract_enunciado(local_text) if local_text else ''
    remote_enu = extract_enunciado(remote_text) if remote_text else ''
    def norm(s):
        return '\n'.join([ln.rstrip() for ln in s.strip().splitlines()])
    equal = False
    if remote_ok:
        equal = (norm(local_enu) == norm(remote_enu))
    report['checked'].append({'name': name, 'local_exists': local_path.exists(), 'remote_ok': remote_ok, 'equal': equal, 'remote_url': remote_url})
    if not equal:
        diff = '\n'.join(difflib.unified_diff(remote_enu.splitlines(), local_enu.splitlines(), fromfile='remote/'+name, tofile='local/'+name, lineterm=''))
        report['mismatches'].append({'name': name, 'diff': diff, 'remote_enunciado': remote_enu, 'local_enunciado': local_enu, 'remote_url': remote_url})

OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('Done v2. Checked', len(report['checked']), 'mismatches:', len(report['mismatches']))
