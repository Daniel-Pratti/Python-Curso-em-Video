import os, re, json, urllib.request, urllib.parse, sys

repo_api = "https://api.github.com/repos/andreinaoliveira/Exercicios-Python/contents/Exercicios"
raw_base = 'https://raw.githubusercontent.com/andreinaoliveira/Exercicios-Python/master/Exercicios/'
local_dir = "/workspaces/Python-Curso-em-Video/Lista de Exercícios Mundo 1"
start, end = 36, 115
os.makedirs(local_dir, exist_ok=True)

# fetch repo index
print('Fetching repo index...')
with urllib.request.urlopen(repo_api, timeout=15) as r:
    idx = json.load(r)
num_to_name = {}
for e in idx:
    name = e.get('name','')
    m = re.match(r"\s*(\d{1,3})\b", name)
    if m:
        num_to_name[int(m.group(1))] = name

missing_pre = []
for i in range(start, end+1):
    local = os.path.join(local_dir, f"Ex{i:03d}.py")
    if not os.path.exists(local):
        missing_pre.append(i)

print(f'Local files missing entirely: {missing_pre}')

updated = []
not_found = []
for i in range(start, end+1):
    local = os.path.join(local_dir, f"Ex{i:03d}.py")
    # read local
    local_text = ''
    if os.path.exists(local):
        with open(local, 'r', encoding='utf-8') as f:
            local_text = f.read()
    # detect fallback or empty docstring
    mloc = re.search(r'"""(.*?)"""', local_text, re.DOTALL)
    local_enun = mloc.group(1).strip() if mloc else None
    if local_enun and 'Enunciado não encontrado' not in local_enun:
        # ok
        continue
    # need to fetch remote
    name = num_to_name.get(i)
    if not name:
        not_found.append((i, 'no-name-in-index'))
        continue
    url = raw_base + urllib.parse.quote(name)
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = r.read().decode('utf-8', errors='replace')
    except Exception as e:
        not_found.append((i, f'fetch-failed:{e}'))
        continue
    # try triple quote
    m = re.search(r'"""(.*?)"""', data, re.DOTALL)
    enun = None
    if m:
        enun = m.group(1).strip()
    else:
        # try consecutive top comments starting with #
        lines = data.splitlines()
        comment_lines = []
        for ln in lines:
            s = ln.strip()
            if s.startswith('#'):
                comment_lines.append(s.lstrip('#').strip())
            elif s == '':
                # allow one blank between comments
                if comment_lines:
                    comment_lines.append('')
                else:
                    continue
            else:
                # stop when code starts
                if comment_lines:
                    break
                else:
                    # maybe a plain text header (no comment), collect first 6 lines
                    break
        if comment_lines and any(l.strip() for l in comment_lines):
            enun = '\n'.join(comment_lines).strip()
        else:
            # fallback: take first 8 non-empty lines from file if they look like description
            nonempty = [ln for ln in lines if ln.strip()][:8]
            if nonempty:
                enun = '\n'.join(nonempty).strip()
    if not enun:
        not_found.append((i, 'no-enunciado-found'))
        continue
    # write local file with docstring enun
    try:
        with open(local, 'w', encoding='utf-8') as f:
            f.write('"""' + enun + '\n"""\n')
        updated.append(i)
        print(f'Updated Ex{i:03d}.py')
    except Exception as e:
        not_found.append((i, 'write-failed:'+str(e)))

# write report
rep = {'updated': updated, 'not_found': not_found}
with open('/workspaces/Python-Curso-em-Video/scripts/fill_missing_enunciados_report.json','w',encoding='utf-8') as fh:
    json.dump(rep, fh, ensure_ascii=False, indent=2)
print('Done. report saved to scripts/fill_missing_enunciados_report.json')
