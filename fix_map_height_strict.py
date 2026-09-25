import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# Change the wrapper of the tab content to a strict height so FileGraph can fill it
content = content.replace(
    'className="flex-grow overflow-y-auto p-4 min-h-[800px] h-full bg-white flex flex-col"',
    'className="flex-grow overflow-y-auto p-4 h-[800px] bg-white flex flex-col"'
)

# And on the root container, just to be safe
content = content.replace(
    '<div className="bg-white border-2 border-black rounded-xl shadow-[8px_8px_0px_rgba(0,0,0,1)] min-h-[800px] flex flex-col overflow-hidden">',
    '<div className="bg-white border-2 border-black rounded-xl shadow-[8px_8px_0px_rgba(0,0,0,1)] h-[850px] flex flex-col overflow-hidden">'
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Fixed map height strictly')
