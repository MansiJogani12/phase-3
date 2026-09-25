import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    lines = f.readlines()

open_divs = []
for idx, line in enumerate(lines, 1):
    div_opens = line.count('<div')
    div_closes = line.count('</div>')
    for _ in range(div_opens):
        open_divs.append(idx)
    for _ in range(div_closes):
        if open_divs:
            open_divs.pop()
        else:
            print(f"Extra closing </div> at line {idx}")

print(f"Unclosed divs remaining at end: {len(open_divs)}")
for d in open_divs:
    print(f"Opened at line {d}: {lines[d-1].strip()[:60]}")
