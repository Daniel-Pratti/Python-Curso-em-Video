#!/usr/bin/env python3
from pathlib import Path
import re

BASE = Path('/workspaces/Python-Curso-em-Video')
SRC_DIRS = [BASE / 'Lista de Exercícios Mundo 1', BASE / 'Lista de Exercícios Mundo 1, 2 e 3']
TARGET_DIR = BASE / 'Curso em Video - Python'
TARGET_DIR.mkdir(parents=True, exist_ok=True)

def extract_enunciado(text):
    m = re.match(r"\s*(?:[ruRU]{0,2})?([\"']{3})(.*?)\1", text, re.S)
    if m:
        doc = m.group(2).strip()
        if doc and 'Enunciado não encontrado' not in doc:
            return doc
    # leading comment block
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
        cand = '\n'.join(comment_lines).strip()
        if 'Enunciado não encontrado' not in cand:
            return cand
    # first non-empty lines as last resort
    nonempty = [l for l in lines if l.strip()]
    cand = '\n'.join(nonempty[:8]).strip() if nonempty else ''
    if cand and 'Enunciado não encontrado' not in cand:
        return cand
    return ''

for i in range(1, 116):
    name = f'Ex{i:03}.py'
    chosen = ''
    chosen_src = None
    for d in SRC_DIRS:
        p = d / name
        if p.exists():
            text = p.read_text(encoding='utf-8')
            enu = extract_enunciado(text)
            if enu:
                chosen = enu
                chosen_src = p
                break
            # keep a non-empty even if might be fallback
            if not chosen and text.strip():
                # attempt to use any docstring/comment even if possibly fallback
                m = re.match(r"\s*(?:[ruRU]{0,2})?([\"']{3})(.*?)\1", text, re.S)
                if m:
                    chosen = m.group(2).strip()
                    chosen_src = p
    target = TARGET_DIR / name
    if chosen:
        content = '"""' + '\n' + chosen.strip() + '\n"""\n'
    else:
        content = '"""Enunciado não encontrado nas pastas fonte."""\n'
    target.write_text(content, encoding='utf-8')
    # small progress print
    print('Wrote', target)

print('Done. Wrote files to', TARGET_DIR)
