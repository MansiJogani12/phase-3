import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    lines = f.readlines()

stack = []
in_string = False
string_char = ''

for line_idx, line in enumerate(lines, 1):
    i = 0
    while i < len(line):
        char = line[i]
        # skip inline comments //
        if not in_string and char == '/' and i + 1 < len(line) and line[i+1] == '/':
            break
        if char in ['"', "'", '`'] and not in_string:
            in_string = True
            string_char = char
        elif char == string_char and in_string:
            if i > 0 and line[i-1] == '\\':
                pass
            else:
                in_string = False
                string_char = ''
        elif not in_string:
            if char in ['{', '(', '[']:
                stack.append((char, line_idx, i+1))
            elif char in ['}', ')', ']']:
                if not stack:
                    print(f"UNMATCHED CLOSING '{char}' at line {line_idx}:{i+1}")
                else:
                    top, l, c = stack.pop()
                    pair = {'}': '{', ')': '(', ']': '['}
                    if top != pair[char]:
                        print(f"MISMATCHED '{char}' at line {line_idx}:{i+1}, opened with '{top}' at line {l}:{c}")
        i += 1

print(f"Parsing complete. Remaining unclosed brackets: {len(stack)}")
for item in stack:
    print(f"Unclosed '{item[0]}' from line {item[1]}:{item[2]}")
