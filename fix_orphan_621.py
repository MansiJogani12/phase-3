import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    lines = f.readlines()

new_lines = []
for idx, l in enumerate(lines, 1):
    # Remove lines 619-621 which are orphan closing tags
    if idx in [619, 620, 621]:
        continue
    new_lines.append(l)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.writelines(new_lines)

print('Successfully deleted orphan closing tags on lines 619-621!')
