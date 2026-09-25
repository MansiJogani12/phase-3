import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

content = content.replace(
    '                    </AccordionCard>\n                </div>\n    );',
    '                    </AccordionCard>\n                </div>\n            </div>\n        </div>\n    );'
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)

print('Added missing 2 closing divs before ); !')
