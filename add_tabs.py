import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

tabs_to_add = '''<TabButton name="security" label="Security" icon="🛡️" />
                            <TabButton name="explanation" label="Explanation" />
                            <TabButton name="generated_tests" label="Generated Tests" />
                            <TabButton name="refactored_code" label="Refactored Code" />
                            <TabButton name="improvements" label="Improvements" />'''

content = re.sub(
    r'<TabButton name="security"[^>]+>',
    tabs_to_add,
    content
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Added tabs back')
