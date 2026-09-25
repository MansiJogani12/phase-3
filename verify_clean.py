import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

print('Generate Tests orphan in content:', 'Generate Tests' in content)
print('Refactor Code orphan in content:', 'Refactor Code' in content)
print('Deployments button in RepoHeaderCard:', 'Deployments' in content)
