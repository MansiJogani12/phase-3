import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# Let's check for any unterminated string literals or unmatched braces
stack = []
in_string = False
string_char = ''
lines = content.split('\n')

for line_idx, line in enumerate(lines, 1):
    for col_idx, char in enumerate(line, 1):
        if char in ['"', "'", '`'] and not in_string:
            in_string = True
            string_char = char
        elif char == string_char and in_string:
            # check backslash escape
            if col_idx > 1 and line[col_idx-2] == '\\':
                pass
            else:
                in_string = False
                string_char = ''
        elif not in_string:
            if char in ['{', '(', '[']:
                stack.append((char, line_idx, col_idx))
            elif char in ['}', ')', ']']:
                if not stack:
                    print(f"Unmatched closing '{char}' at line {line_idx}:{col_idx}")
                else:
                    top, l, c = stack.pop()
                    pair = {'}': '{', ')': '(', ']': '['}
                    if top != pair[char]:
                        print(f"Mismatched '{char}' at line {line_idx}:{col_idx}, opened with '{top}' at line {l}:{c}")

print(f"Parsing complete. Remaining unclosed brackets: {len(stack)}")
for item in stack:
    print(f"Unclosed '{item[0]}' from line {item[1]}:{item[2]}")
