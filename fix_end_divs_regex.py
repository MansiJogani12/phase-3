import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

content = re.sub(
    r'\s*<\/div>\s*\);\s*\};',
    '\n                </div>\n            </div>\n        </div>\n    );\n};',
    content
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)

print('Successfully added missing 2 closing divs using regex!')
