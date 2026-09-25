import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

start_idx = content.find('{/* --- NEW CODEORACLE TOP HEADER --- */}')
end_idx = content.find('<div className="bg-white border-2 border-black rounded-xl shadow-[8px_8px_0px_rgba(0,0,0,1)] flex flex-col min-h-[800px] overflow-hidden">')

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

content = content.replace('<div className="mt-8 flex flex-col gap-8">', '<div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">')
content = content.replace('<div className="w-full">', '<div className="lg:col-span-2">', 1)
content = content.replace('<div className="w-full flex flex-col gap-8 mt-8">', '<div className="lg:col-span-1 flex flex-col gap-8">')

# Restore tabs wrapping
content = content.replace('flex flex-col min-h-[800px] overflow-hidden', 'h-full flex flex-col overflow-hidden')
content = content.replace('flex-wrap', 'overflow-x-auto flex-nowrap hide-scrollbar')

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Done')
