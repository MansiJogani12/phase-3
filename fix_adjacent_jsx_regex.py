import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# Match })() followed by closing divs right before Right Side Column
content = re.sub(
    r'(\}\)\(\)\}\s*<\/div>\s*<\/div>)\s*<\/div>(\s*\{\/\* Right Side Column)',
    r'\1\2',
    content
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)

print('Regex fixed adjacent JSX closing tags!')
