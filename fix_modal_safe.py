import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\PageContent\FileContentModal.jsx', 'r', 'utf-8') as f:
    content = f.read()

if 'import { createPortal }' not in content:
    content = "import { createPortal } from 'react-dom';\n" + content

content = content.replace(
    'return (\n        <div className="fixed',
    'return createPortal(\n        <div className="fixed'
)

content = content.replace(
    '        </div>\n    );\n};\n',
    '        </div>\n    , document.body);\n};\n'
)
content = content.replace(
    '        </div>\n    );\n}',
    '        </div>\n    , document.body);\n}'
)

# If the file still has syntax errors because of replacement mismatches, we can just regex the end
content = re.sub(r'        </div>\n    \);\n\};?$', '        </div>\n    , document.body);\n};', content, flags=re.MULTILINE)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\PageContent\FileContentModal.jsx', 'w', 'utf-8') as f:
    f.write(content)

print('Fixed FileContentModal portal safely')
