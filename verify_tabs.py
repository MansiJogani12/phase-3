import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

tabs = ['directory', 'graph', 'timeline', 'issues', 'insights', 'security', 'explanation', 'generated_tests', 'refactored_code', 'improvements']
for t in tabs:
    print(f'Tab "{t}":', f'name="{t}"' in content)

print('handleGenerateAi present:', 'handleGenerateAi' in content)
