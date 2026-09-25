import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Let's inspect lines 960 to 990
for i in range(960, min(1000, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
