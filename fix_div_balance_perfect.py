import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# Replace after })()} with the exact required 3 closing divs
old_block = '''                            })()}

                        </div>

                {/* Right Side Column (Context Builder & Accordions) '''

new_block = '''                            })()}

                        </div>
                    </div>
                </div>

                {/* Right Side Column (Context Builder & Accordions) '''

if old_block in content:
    content = content.replace(old_block, new_block)
    with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
        f.write(content)
    print('Replaced closing block successfully!')
else:
    print('Pattern not matched!')
