import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    lines = f.readlines()

clean = []
for l in lines:
    if 'Generate Tests' in l or 'Refactor Code' in l or '</select>' in l:
        continue
    clean.append(l)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.writelines(clean)

print('Permanently removed all orphan Generate Tests/Refactor Code/select lines!')
