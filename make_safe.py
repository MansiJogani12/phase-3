import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# Make the dynamic block completely crash-proof
safe_dynamic = '''
    // --- DYNAMIC CODEORACLE COMPUTATIONS ---
    let totalFiles = 0;
    let detectedLanguages = [];
    let estimatedLoc = 0;
    const extToLang = {
        'js': 'JavaScript', 'jsx': 'React', 'ts': 'TypeScript', 'tsx': 'React TS',
        'py': 'Python', 'html': 'HTML', 'css': 'CSS', 'json': 'JSON', 'md': 'Markdown',
        'yml': 'YAML', 'yaml': 'YAML', 'java': 'Java', 'cpp': 'C++', 'c': 'C', 'go': 'Go',
        'rs': 'Rust', 'rb': 'Ruby', 'php': 'PHP'
    };

    try {
        if (flatTree && Array.isArray(flatTree)) {
            totalFiles = flatTree.length;
            estimatedLoc = totalFiles * 150;

            const extMap = {};
            flatTree.forEach(node => {
                if (node && node.type === 'blob' && node.name && typeof node.name === 'string' && node.name.includes('.')) {
                    const ext = node.name.split('.').pop().toLowerCase();
                    extMap[ext] = (extMap[ext] || 0) + 1;
                }
            });

            detectedLanguages = Object.keys(extMap)
                .map(ext => extToLang[ext] || ext.toUpperCase())
                .filter((v, i, a) => a.indexOf(v) === i)
                .slice(0, 10);
        }
    } catch (err) {
        console.error("Error computing dynamic stats", err);
    }
'''

content = re.sub(
    r'// --- DYNAMIC CODEORACLE COMPUTATIONS ---.*?// ---------------------------------------',
    safe_dynamic,
    content,
    flags=re.DOTALL
)

# And make the map crash-proof
safe_tbody = '''<tbody className="divide-y divide-gray-200">
    {flatTree && Array.isArray(flatTree) && flatTree.filter(f => {
        try { return !searchQuery || (f && f.path && typeof f.path === 'string' && f.path.toLowerCase().includes(searchQuery.toLowerCase())); } catch (e) { return false; }
    }).slice(0, 100).map((file, idx) => (
        <tr key={idx} className="hover:bg-gray-50">
            <td className="p-3 font-mono">📄 {file && file.path ? file.path : 'Unknown'}</td>
            <td className="p-3">{(file && file.name && typeof file.name === 'string' && file.name.includes('.')) ? extToLang[file.name.split('.').pop().toLowerCase()] || 'Unknown' : 'Unknown'}</td>
            <td className="p-3 text-red-500 font-bold">~{file && !isNaN(file.size) ? (file.size / 30).toFixed(0) : 0} LOC</td>
            <td className="p-3 text-gray-500">{file && !isNaN(file.size) ? (file.size / 1024).toFixed(2) : 0} KB</td>
        </tr>
    ))}
</tbody>'''

content = re.sub(r'<tbody className="divide-y divide-gray-200">.*?</tbody>', safe_tbody, content, flags=re.DOTALL)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print("Made safe")
