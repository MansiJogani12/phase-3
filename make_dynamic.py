import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

dynamic_logic = '''
    // --- DYNAMIC CODEORACLE COMPUTATIONS ---
    const totalFiles = flatTree ? flatTree.length : 0;
    
    // Calculate languages from file extensions
    const extMap = {};
    if (flatTree) {
        flatTree.forEach(node => {
            if (node.type === 'blob' && node.name.includes('.')) {
                const ext = node.name.split('.').pop().toLowerCase();
                extMap[ext] = (extMap[ext] || 0) + 1;
            }
        });
    }
    const extToLang = {
        'js': 'JavaScript', 'jsx': 'React', 'ts': 'TypeScript', 'tsx': 'React TS',
        'py': 'Python', 'html': 'HTML', 'css': 'CSS', 'json': 'JSON', 'md': 'Markdown',
        'yml': 'YAML', 'yaml': 'YAML', 'java': 'Java', 'cpp': 'C++', 'c': 'C', 'go': 'Go',
        'rs': 'Rust', 'rb': 'Ruby', 'php': 'PHP'
    };
    const detectedLanguages = Object.keys(extMap)
        .map(ext => extToLang[ext] || ext.toUpperCase())
        .filter((v, i, a) => a.indexOf(v) === i)
        .slice(0, 10); // top 10

    // Fake LOC for now, or just multiply files by 150
    const estimatedLoc = totalFiles * 150;
    
    // ---------------------------------------
'''

# Insert dynamic logic near the top of the component
content = re.sub(r'(const RepoDetailView = \(\{.*?\}\) => \{)', r'\1\n' + dynamic_logic, content, flags=re.DOTALL)

# Now replace the hardcoded stats in the header
content = content.replace('>100<', '>{totalFiles}<')
content = content.replace('>21,247<', '>{estimatedLoc.toLocaleString()}<')

# Replace the hardcoded map with the dynamic one
content = re.sub(
    r"\{?\['CSS', 'HTML', 'JSON', 'JavaScript', 'React', 'Markdown', 'Python', 'TypeScript', 'YAML'\]\}?\.map",
    "{detectedLanguages.length > 0 ? detectedLanguages : ['Unknown']}.map",
    content
)

# Replace the title "Extracted Project Source Files (100)"
content = re.sub(
    r'📄 Extracted Project Source Files \(\d+\)',
    '📄 Extracted Project Source Files ({totalFiles})',
    content
)

# Now replace the <tbody> with a dynamic map of flatTree
dynamic_tbody = '''
<tbody className="divide-y divide-gray-200">
    {flatTree && flatTree.slice(0, 100).map((file, idx) => (
        <tr key={idx} className="hover:bg-gray-50">
            <td className="p-3 font-mono">📄 {file.path}</td>
            <td className="p-3">{file.name.includes('.') ? extToLang[file.name.split('.').pop().toLowerCase()] || 'Unknown' : 'Unknown'}</td>
            <td className="p-3 text-red-500 font-bold">~{(file.size / 30).toFixed(0)} LOC</td>
            <td className="p-3 text-gray-500">{(file.size / 1024).toFixed(2)} KB</td>
        </tr>
    ))}
</tbody>
'''

content = re.sub(r'<tbody className="divide-y divide-gray-200">.*?</tbody>', dynamic_tbody, content, flags=re.DOTALL)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print("Made stats dynamic")
