import urllib.request, sys, re, os

base = "https://raw.githubusercontent.com/LeandroMontanari/python3-curso-em-video/master/Mundo%2001/Exerc%C3%ADcios%20Corrigidos"
outdir = "/workspaces/Python-Curso-em-Video/Lista de Exercícios Mundo 1"
os.makedirs(outdir, exist_ok=True)
not_found = []
for i in range(1, 101):
    num = f"{i:03d}"
    url = f"{base}/Exerc%C3%ADcio%20{num}.py"
    sys.stderr.write(f"Fetching {url}\n")
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = r.read().decode('utf-8', errors='replace')
    except Exception as e:
        sys.stderr.write(f"WARNING: no content for {num}: {e}\n")
        path = os.path.join(outdir, f"Ex{num}.py")
        with open(path, 'w', encoding='utf-8') as f:
            f.write('"""Enunciado não encontrado no repositório fonte."""\n')
        not_found.append(path)
        continue
    m = re.search(r'"""(.*?)"""', data, re.DOTALL)
    path = os.path.join(outdir, f"Ex{num}.py")
    if not m:
        sys.stderr.write(f"WARNING: docstring not found in source for {num}\n")
        with open(path, 'w', encoding='utf-8') as f:
            f.write('"""Enunciado não encontrado no arquivo fonte."""\n')
        not_found.append(path)
    else:
        enun = m.group(1).strip()
        with open(path, 'w', encoding='utf-8') as f:
            f.write('"""' + enun + '\n"""\n')
        sys.stderr.write(f"Wrote {path}\n")
if not_found:
    sys.stderr.write('\nFiles with missing enunciado:\n')
    for p in not_found:
        sys.stderr.write(p + '\n')
print('Done')
