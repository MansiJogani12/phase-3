import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    lines = f.readlines()

clean_lines = []
skipping = False
for l in lines:
    if '%</p>' in l:
        skipping = True
    if skipping:
        if 'Right Side Column' in l:
            skipping = False
            clean_lines.append(l)
        continue
    clean_lines.append(l)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.writelines(clean_lines)

print('Cleaned up orphan lines via line iteration!')
