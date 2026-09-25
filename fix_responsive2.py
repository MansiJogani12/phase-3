import codecs
import re

# FIX MODAL WITH PORTAL
with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\PageContent\FileContentModal.jsx', 'r', 'utf-8') as f:
    content = f.read()

if 'createPortal' not in content:
    content = content.replace('import React from \'react\';', 'import React from \'react\';\nimport { createPortal } from \'react-dom\';')
    
    # Wrap return in createPortal
    content = re.sub(
        r'(return \(\s*)(<div className="fixed inset-0)',
        r'\1createPortal(\2',
        content
    )
    
    # Close portal at the end
    content = content.replace(');', ', document.body);', 1)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\PageContent\FileContentModal.jsx', 'w', 'utf-8') as f:
    f.write(content)

# FIX APPHEADER RESPONSIVENESS MORE AGGRESSIVELY
with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\PageContent\AppHeader.jsx', 'r', 'utf-8') as f:
    header = f.read()

header = header.replace(
    '<div className="hidden lg:flex-grow lg:flex gap-2 min-w-[300px] flex-1">',
    '<div className="hidden lg:flex-grow lg:flex gap-2 min-w-[300px] flex-1 xl:flex-none xl:w-1/3">'
)

header = header.replace(
    '<div className="hidden lg:flex lg:flex-wrap lg:items-center lg:justify-end lg:gap-3 flex-1">',
    '<div className="hidden lg:flex lg:flex-wrap lg:items-center lg:justify-end lg:gap-3 w-full xl:w-auto mt-4 xl:mt-0">'
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\PageContent\AppHeader.jsx', 'w', 'utf-8') as f:
    f.write(header)

print('Fixed modal and header')
