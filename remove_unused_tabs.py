import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# 1. Remove tab buttons for generated_tests and refactored_code
content = content.replace('<TabButton name="generated_tests" label="Generated Tests" />\n', '')
content = content.replace('<TabButton name="generated_tests" label="Generated Tests" />', '')
content = content.replace('<TabButton name="refactored_code" label="Refactored Code" />\n', '')
content = content.replace('<TabButton name="refactored_code" label="Refactored Code" />', '')

# 2. Remove the JSX rendering blocks for generated_tests and refactored_code
content = re.sub(r'\{activeTab === \'generated_tests\' && \([\s\S]*?\)\}\n*', '', content)
content = re.sub(r'\{activeTab === \'refactored_code\' && \([\s\S]*?\)\}\n*', '', content)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)

print('Removed Generated Tests & Refactored Code tabs from RepoDetailView.jsx')
