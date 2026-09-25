import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

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
    // ---------------------------------------
'''

if '// --- DYNAMIC CODEORACLE COMPUTATIONS ---' not in content:
    content = re.sub(r'(const RepoDetailView = \(\{.*?\}\) => \{)', r'\1\n' + safe_dynamic, content, flags=re.DOTALL)
else:
    # already there, just replace it
    content = re.sub(r'// --- DYNAMIC CODEORACLE COMPUTATIONS ---.*?// ---------------------------------------', safe_dynamic, content, flags=re.DOTALL)


with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Injected missing variables')
