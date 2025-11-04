import urllib.request, json, re, os, sys, urllib.parse

api_url = "https://api.github.com/repos/andreinaoliveira/Exercicios-Python/contents/Exercicios"
outdir = "/workspaces/Python-Curso-em-Video/Lista de Exercícios Mundo 1"
os.makedirs(outdir, exist_ok=True)

print('Fetching repository index...')
with urllib.request.urlopen(api_url, timeout=15) as r:
    idx = json.load(r)

num_to_name = {}
for entry in idx:
    name = entry.get('name','')
    m = re.match(r"\s*(\d{1,3})\b", name)
    if not m:
        continue
    num = int(m.group(1))
    num_to_name[num] = name

start, end = 36, 115
updated = []
failed = []
for i in range(start, end+1):
    name = num_to_name.get(i)
    if not name:
        print(f'No file name found in repo index for {i:03d}')
        failed.append((i, 'not-in-index'))
        continue
    raw_base = 'https://raw.githubusercontent.com/andreinaoliveira/Exercicios-Python/master/Exercicios/'
    encoded_name = urllib.parse.quote(name)
    url = raw_base + encoded_name
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = r.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f'Failed fetching {url}: {e}', file=sys.stderr)
        failed.append((i, str(e)))
        continue
    m = re.search(r'"""(.*?)"""', data, re.DOTALL)
    enun = m.group(1).strip() if m else None
    path = os.path.join(outdir, f"Ex{i:03d}.py")
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('"""' + (enun or 'Enunciado não encontrado no arquivo fonte.') + '\n"""\n')
        updated.append(i)
        print(f'Wrote {path}')
    except Exception as e:
        print(f'Failed writing {path}: {e}', file=sys.stderr)
        failed.append((i, 'write-failed:'+str(e)))

print('\nSummary:')
print(f'  Updated: {len(updated)}')
print(f'  Failed: {len(failed)}')
if failed:
    print('Failed list (first 20):', failed[:20])
with open('/workspaces/Python-Curso-em-Video/scripts/fetch_andreina_036_115_report.json','w',encoding='utf-8') as fh:
    json.dump({'updated':updated,'failed':failed}, fh, ensure_ascii=False, indent=2)
print('Report written to scripts/fetch_andreina_036_115_report.json')
