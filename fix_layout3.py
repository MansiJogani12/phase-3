import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

content = content.replace(
    '<div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">',
    '<div className="mt-8 flex flex-col gap-8">'
)

content = content.replace(
    '<div className="lg:col-span-2">',
    '<div className="w-full">'
)

content = content.replace(
    '<div className="lg:col-span-1 flex flex-col gap-8">',
    '<div className="w-full flex flex-col gap-8 mt-8">'
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Fixed layout to be bottom again')
