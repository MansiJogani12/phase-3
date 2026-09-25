import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    lines = f.readlines()

# Line 979 is index 978 in zero-indexed list
# We remove index 978 (extra closing div before Right Side Column)
# And we remove the extra closing divs at the end of return statement
new_lines = []
for idx, l in enumerate(lines):
    # Skip extra </div> right before Right Side Column (line 979)
    if idx == 978 and '</div>' in l:
        continue
    # Skip extra </div> at lines 1022 & 1023
    if idx in [1021, 1022] and '</div>' in l:
        continue
    new_lines.append(l)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.writelines(new_lines)

print('Removed exact extra closing divs!')
