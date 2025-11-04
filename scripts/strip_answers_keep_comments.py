#!/usr/bin/env python3
from pathlib import Path
import re
BASE = Path('/workspaces/Python-Curso-em-Video')
TARGET = BASE / 'Curso em Video - Python'
REPORT = BASE / 'scripts' / 'strip_comments_report.json'

RESULT = {'updated': [], 'kept_docstring': [], 'no_enunciado': []}

def extract_leading_docstring(text):
    m = re.match(r"\s*(?:[ruRU]{0,2})?([\"']{3})(.*?)\1", text, re.S)
    if m:
        return m.group(2).strip()
    return ''

for i in range(1, 116):
    name = f'Ex{i:03}.py'
    p = TARGET / name
    if not p.exists():
        RESULT.setdefault('missing', []).append(name)
        continue
    text = p.read_text(encoding='utf-8')
    lines = text.splitlines()
    # collect leading comment block
    collected = []
    started = False
    for ln in lines:
        if ln.lstrip().startswith('#'):
            collected.append(ln)
            started = True
        else:
            # blank lines allowed inside block if already started
            if ln.strip() == '' and started:
                collected.append(ln)
                continue
            # if not started and blank line, skip
            if not started and ln.strip() == '':
                continue
            break
    if collected:
        # strip leading # and whitespace
        cleaned = []
        for c in collected:
            if c.lstrip().startswith('#'):
                # remove first # only
                idx = c.find('#')
                cleaned.append(c[idx+1:].rstrip())
            else:
                cleaned.append(c.rstrip())
        enu = '\n'.join([l.strip() for l in cleaned]).strip()
        if not enu:
            # fallback to existing docstring
            doc = extract_leading_docstring(text)
            if doc:
                content = '"""\n' + doc + '\n"""\n'
                p.write_text(content, encoding='utf-8')
                RESULT['kept_docstring'].append(name)
            else:
                p.write_text('"""Enunciado não encontrado."""\n', encoding='utf-8')
                RESULT['no_enunciado'].append(name)
        else:
            content = '"""\n' + enu + '\n"""\n'
            p.write_text(content, encoding='utf-8')
            RESULT['updated'].append(name)
    else:
        # no leading comments: try docstring
        doc = extract_leading_docstring(text)
        if doc:
            content = '"""\n' + doc + '\n"""\n'
            p.write_text(content, encoding='utf-8')
            RESULT['kept_docstring'].append(name)
        else:
            p.write_text('"""Enunciado não encontrado."""\n', encoding='utf-8')
            RESULT['no_enunciado'].append(name)

import json
REPORT.write_text(json.dumps(RESULT, ensure_ascii=False, indent=2), encoding='utf-8')
print('Done. updated:', len(RESULT['updated']), 'kept_docstring:', len(RESULT['kept_docstring']), 'no_enunciado:', len(RESULT['no_enunciado']))
