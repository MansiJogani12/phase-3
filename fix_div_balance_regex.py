import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

content = re.sub(
    r'(\}\)\(\)\}\s*<\/div>)(\s*\{\/\* Right Side Column)',
    r'\1\n                    </div>\n                </div>\2',
    content
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)

print('Regex injected missing closing divs!')
