import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# Replace the header div
old_header = '''<div className="bg-gray-100 p-3 border-b-2 border-black font-bold flex items-center gap-2">
                                  📄 Extracted Project Source Files (100)
                              </div>'''

new_header = '''<div className="bg-gray-100 p-3 border-b-2 border-black font-bold flex justify-between items-center gap-2">
                                  <span className="flex items-center gap-2">📄 Extracted Project Source Files (100)</span>
                                  <div className="relative">
                                      <input type="text" placeholder="Search files..." className="border-2 border-black rounded-lg px-3 py-1.5 text-sm font-normal w-64 shadow-[2px_2px_0px_rgba(0,0,0,1)] focus:outline-none focus:translate-x-[2px] focus:translate-y-[2px] focus:shadow-none transition-all" />
                                      <svg className="w-4 h-4 absolute right-3 top-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                                  </div>
                              </div>'''

content = content.replace(old_header, new_header)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print("Added search bar")
