import json, urllib.request, re, os, sys

api_url = "https://api.github.com/repos/andreinaoliveira/Exercicios-Python/contents/Exercicios"
outdir = "/workspaces/Python-Curso-em-Video/Lista de Exercícios Mundo 1"
os.makedirs(outdir, exist_ok=True)

print('Fetching repository index...')
with urllib.request.urlopen(api_url, timeout=15) as r:
    idx = json.load(r)

# Build map num->download_url
num_to_url = {}
for entry in idx:
    name = entry.get('name','')
    m = re.match(r"\s*(\d{1,3})\b", name)
    if not m:
        continue
    num = int(m.group(1))
    if num < 1 or num > 115:
        continue
    download_url = entry.get('download_url')
    if download_url:
        num_to_url[num] = download_url

print(f'Found {len(num_to_url)} exercicio files in repo (1..115).')

changed = []
unchanged = []
missing = []
for i in range(1, 101):
    local_path = os.path.join(outdir, f"Ex{i:03d}.py")
    repo_url = num_to_url.get(i)
    if not repo_url:
        missing.append(i)
        continue
    # fetch repo file
    try:
        with urllib.request.urlopen(repo_url, timeout=15) as r:
            data = r.read().decode('utf-8', errors='replace')
    except Exception as e:
        missing.append(i)
        print(f'Warning: could not fetch {repo_url}: {e}', file=sys.stderr)
        continue
    m = re.search(r'"""(.*?)"""', data, re.DOTALL)
    repo_enun = m.group(1).strip() if m else None
    # read local file docstring if exists
    local_enun = None
    if os.path.exists(local_path):
        try:
            with open(local_path, 'r', encoding='utf-8') as f:
                local_data = f.read()
            lm = re.search(r'"""(.*?)"""', local_data, re.DOTALL)
            local_enun = lm.group(1).strip() if lm else None
        except Exception as e:
            print(f'Warning reading {local_path}: {e}', file=sys.stderr)
    # compare
    if repo_enun is None:
        # take repo entire file first comment lines as fallback
        repo_enun = data.strip().splitlines()[0:5]
        repo_enun = '\n'.join(repo_enun)
    if local_enun == repo_enun:
        unchanged.append(i)
    else:
        # overwrite local with repo_enun as docstring
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write('"""' + (repo_enun or 'Enunciado não encontrado') + '\n"""\n')
        changed.append(i)
        print(f'Updated Ex{i:03d}.py from repo')

print('\nSummary:')
print(f'  Updated: {len(changed)} files')
print(f'  Unchanged: {len(unchanged)} files')
print(f'  Missing in repo: {len(missing)} files')
if missing:
    print('Missing numbers:', missing)

# write a small report
report = {
    'updated': changed,
    'unchanged': unchanged,
    'missing': missing,
}
with open('/workspaces/Python-Curso-em-Video/scripts/compare_and_update_report.json', 'w', encoding='utf-8') as r:
    json.dump(report, r, ensure_ascii=False, indent=2)
print('Report written to scripts/compare_and_update_report.json')
