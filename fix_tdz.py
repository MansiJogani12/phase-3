import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# 1. Remove the old dynamic block at the top
content = re.sub(r'// --- DYNAMIC CODEORACLE COMPUTATIONS ---.*?// ---------------------------------------', '', content, flags=re.DOTALL)

# 2. Re-inject it AFTER the useState hooks (right before `useEffect(() => {`)
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
                if (node && node.type === 'blob' && node.path && typeof node.path === 'string' && node.path.includes('.')) {
                    const ext = node.path.split('.').pop().toLowerCase();
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
    // ---------------------------------------
'''

content = content.replace('useEffect(() => {', safe_dynamic + '\n    useEffect(() => {', 1)

# 3. Fix the table to use path instead of name
content = content.replace(
    '''{(file && file.name && typeof file.name === 'string' && file.name.includes('.')) ? extToLang[file.name.split('.').pop().toLowerCase()] || 'Unknown' : 'Unknown'}''',
    '''{(file && file.path && typeof file.path === 'string' && file.path.includes('.')) ? extToLang[file.path.split('.').pop().toLowerCase()] || 'Unknown' : 'Unknown'}'''
)


with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Moved logic below state variables')
