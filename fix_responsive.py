import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\PageContent\AppHeader.jsx', 'r', 'utf-8') as f:
    content = f.read()

content = content.replace(
    '<div className="flex justify-between items-center gap-4">',
    '<div className="flex flex-wrap justify-between items-center gap-4 lg:gap-6">'
)

content = content.replace(
    '<div className="hidden lg:flex-grow lg:flex gap-2">',
    '<div className="hidden lg:flex-grow lg:flex gap-2 min-w-[300px] flex-1">'
)

content = content.replace(
    '<div className="hidden lg:flex lg:items-center lg:gap-4 lg:flex-shrink-0">',
    '<div className="hidden lg:flex lg:flex-wrap lg:items-center lg:justify-end lg:gap-3 flex-1">'
)

content = content.replace(
    '<div className="container mx-auto px-4 md:px-8 py-3">',
    '<div className="w-full px-4 xl:px-8 py-3">'
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\PageContent\AppHeader.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Made AppHeader responsive')
