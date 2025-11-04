#!/usr/bin/env python3
from pathlib import Path
import re
import json
import urllib.request
import urllib.parse
import difflib

BASE = Path('/workspaces/Python-Curso-em-Video')
LOCAL_DIR = BASE / 'Curso em Video - Python'
REMOTE_BASE = 'https://raw.githubusercontent.com/andreinaoliveira/Exercicios-Python/master/Exercicios'
OUT = BASE / 'scripts' / 'verify_report.json'

def extract_enunciado(text):
    m = re.match(r"\s*(?:[ruRU]{0,2})?([\"']{3})(.*?)\1", text, re.S)
    if m:
        doc = m.group(2).strip()
        if doc:
            return doc
    # leading comments
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

report = {'checked': [], 'mismatches': []}

for i in range(1, 116):
    name = f'Ex{i:03}.py'
    local_path = LOCAL_DIR / name
    remote_name = urllib.parse.quote(name)
    remote_url = REMOTE_BASE + '/' + remote_name
    local_text = ''
    remote_text = ''
    local_exists = local_path.exists()
    remote_ok = True
    try:
        with local_path.open('r', encoding='utf-8') as f:
            local_text = f.read()
    except Exception as e:
        local_text = ''
    try:
        with urllib.request.urlopen(remote_url) as r:
            remote_bytes = r.read()
            remote_text = remote_bytes.decode('utf-8')
    except Exception as e:
        remote_ok = False
        remote_text = ''
    local_enu = extract_enunciado(local_text) if local_text else ''
    remote_enu = extract_enunciado(remote_text) if remote_text else ''
    equal = False
    if remote_ok:
        # normalize whitespace for comparison
        def norm(s):
            return '\n'.join([ln.rstrip() for ln in s.strip().splitlines()])
        equal = (norm(local_enu) == norm(remote_enu))
    else:
        equal = False
    entry = {'name': name, 'local_exists': local_exists, 'remote_ok': remote_ok, 'equal': equal}
    report['checked'].append(entry)
    if not equal:
        # produce small diff of enunciados (line-level)
        ld = local_enu.splitlines()
        rd = remote_enu.splitlines()
        diff = '\n'.join(difflib.unified_diff(rd, ld, fromfile='remote/'+name, tofile='local/'+name, lineterm=''))
        report['mismatches'].append({'name': name, 'diff': diff, 'remote_enunciado': remote_enu, 'local_enunciado': local_enu, 'remote_ok': remote_ok})

OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('Done. Checked 115 files, mismatches:', len(report['mismatches']))
