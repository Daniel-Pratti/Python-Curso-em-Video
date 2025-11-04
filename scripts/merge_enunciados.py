#!/usr/bin/env python3
import re
from pathlib import Path

BASE = Path('/workspaces/Python-Curso-em-Video')
DIRS = [BASE / 'Lista de Exercícios Mundo 1', BASE / 'Lista de Exercícios Mundo 1, 2 e 3']
OUT = BASE / 'Lista_Unificada_Ex001-Ex100.md'

def extract_enunciado(text):
    # try triple-quoted docstring at top
    m = re.match(r"\s*(?:[ruRU]{0,2})?([\"']{3})(.*?)\1", text, re.S)
    if m:
        doc = m.group(2).strip()
        if doc:
            return doc
    # fallback: leading comments (lines starting with #) or first non-empty lines until blank
    lines = text.lstrip().splitlines()
    comment_lines = []
    for ln in lines[:20]:
        if ln.strip().startswith('#'):
            comment_lines.append(ln.strip().lstrip('#').strip())
        elif ln.strip() == '':
            if comment_lines:
                break
        else:
            # first block of non-empty non-comment lines (could be code) -> collect first 5 lines
            break
    if comment_lines:
        return '\n'.join(comment_lines).strip()
    # last resort: first 6 non-empty lines
    nonempty = [l for l in lines if l.strip()]
    return '\n'.join(nonempty[:6]).strip() if nonempty else ''

results = {}
missing = []

with OUT.open('w', encoding='utf-8') as out:
    out.write('# Lista Unificada de Enunciados — Ex001 a Ex100\n\n')
    for i in range(1, 101):
        name = f'Ex{i:03}.py'
        chosen = None
        chosen_src = None
        contents = None
        for d in DIRS:
            p = d / name
            if p.exists():
                text = p.read_text(encoding='utf-8')
                enu = extract_enunciado(text)
                # treat fallback markers as empty
                if enu and 'Enunciado não encontrado' not in enu:
                    chosen = enu
                    chosen_src = str(p.relative_to(BASE))
                    contents = text
                    break
                # otherwise keep as potential if none other
                if not chosen:
                    potential = enu
                    potential_src = str(p.relative_to(BASE))
        if not chosen:
            # if we had a potential without the specific fallback phrase, use it
            if 'potential' in locals() and potential and 'Enunciado não encontrado' not in potential:
                chosen = potential
                chosen_src = potential_src
            else:
                chosen = ''
        results[name] = {'enunciado': chosen, 'source': chosen_src}
        out.write(f'## {name}\n\n')
        if chosen:
            out.write(chosen + '\n\n')
        else:
            out.write('_Enunciado não encontrado nas duas pastas._\n\n')
            missing.append(name)

# write a small report
rep = BASE / 'scripts' / 'merge_report.json'
import json
rep.write_text(json.dumps({'total':100,'missing':missing,'count_missing':len(missing)}, ensure_ascii=False, indent=2), encoding='utf-8')
print('Wrote', OUT, 'missing:', len(missing))

