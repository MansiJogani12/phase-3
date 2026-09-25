import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# Replace the 3 closing divs right before Right Side Column with 2 closing divs
old_closing = '''                            })()}

                        </div>
                    </div>
                </div>

                {/* Right Side Column (Context Builder & Accordions) */}'''

new_closing = '''                            })()}

                        </div>
                    </div>

                {/* Right Side Column (Context Builder & Accordions) */}'''

if old_closing in content:
    content = content.replace(old_closing, new_closing)
    with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
        f.write(content)
    print('Fixed adjacent JSX closing tags successfully!')
else:
    print('Old closing pattern not matched exactly!')
