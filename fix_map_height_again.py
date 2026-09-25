import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# Fix the map height issue again
content = content.replace(
    '<div className="bg-white border-2 border-black rounded-xl shadow-[8px_8px_0px_rgba(0,0,0,1)] h-full flex flex-col overflow-hidden">',
    '<div className="bg-white border-[3px] border-black rounded-2xl shadow-[8px_8px_0px_rgba(0,0,0,1)] h-[850px] flex flex-col overflow-hidden">'
)

content = content.replace(
    '<div className="flex-grow overflow-y-auto p-4 min-h-[40rem] bg-white">',
    '<div className="flex-grow overflow-y-auto p-0 h-[800px] bg-white flex flex-col">'
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Fixed Map Height')
