import codecs
import time

path = r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx'

with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

# Touch the file by appending a space and saving
with codecs.open(path, 'w', 'utf-8') as f:
    f.write(content)

print('Touched RepoDetailView.jsx to trigger Vite cache refresh!')
