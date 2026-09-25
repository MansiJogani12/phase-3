import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# Replace the end of return statement to have proper 3 closing divs
old_end = '''                    </AccordionCard>
                </div>
    );
};'''

new_end = '''                    </AccordionCard>
                </div>
            </div>
        </div>
    );
};'''

if old_end in content:
    content = content.replace(old_end, new_end)
    with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
        f.write(content)
    print('Fixed end of return statement with 3 closing divs!')
else:
    print('Pattern for end of return statement not matched!')
