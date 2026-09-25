import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# 1. Add searchQuery state
content = content.replace(
    'const [isHistoryLoading, setIsHistoryLoading] = useState(false);',
    'const [isHistoryLoading, setIsHistoryLoading] = useState(false);\n    const [searchQuery, setSearchQuery] = useState("");'
)

# 2. Fix the name.includes bug in the header stats loop
content = content.replace(
    "if (node.type === 'blob' && node.name.includes('.')) {",
    "if (node.type === 'blob' && node?.name?.includes('.')) {"
)

# 3. Hook up the search input to the state
content = content.replace(
    '<input type="text" placeholder="Search files..." className="border-2 border-black rounded-lg px-3 py-1.5 text-sm font-normal w-64 shadow-[2px_2px_0px_rgba(0,0,0,1)] focus:outline-none focus:translate-x-[2px] focus:translate-y-[2px] focus:shadow-none transition-all" />',
    '<input type="text" placeholder="Search files..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="border-2 border-black rounded-lg px-3 py-1.5 text-sm font-normal w-64 shadow-[2px_2px_0px_rgba(0,0,0,1)] focus:outline-none focus:translate-x-[2px] focus:translate-y-[2px] focus:shadow-none transition-all" />'
)

# 4. Filter the table map
old_map = '{flatTree && flatTree.slice(0, 100).map((file, idx) => ('
new_map = '{flatTree && flatTree.filter(f => !searchQuery || f.path?.toLowerCase().includes(searchQuery.toLowerCase())).slice(0, 100).map((file, idx) => ('
content = content.replace(old_map, new_map)

# 5. Fix the name.includes bug in the table rendering
content = content.replace(
    "{file.name.includes('.') ? extToLang[file.name.split('.').pop().toLowerCase()] || 'Unknown' : 'Unknown'}",
    "{file?.name?.includes('.') ? extToLang[file.name.split('.').pop().toLowerCase()] || 'Unknown' : 'Unknown'}"
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Fixed search and crash')
