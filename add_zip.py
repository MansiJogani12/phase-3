import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\PageContent\AppHeader.jsx', 'r', 'utf-8') as f:
    content = f.read()

btn_to_add = '''
                            <label className="bg-white hover:bg-gray-50 text-black px-4 py-2 rounded-lg font-bold border-2 border-black transition-colors flex items-center gap-2 cursor-pointer shadow-[2px_2px_0px_rgba(0,0,0,1)]">
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
                                ZIP Upload
                                <input type="file" className="hidden" accept=".zip" onChange={(e) => alert('ZIP parsing engine starting (Phase 4 integration pending)')} />
                            </label>
'''
content = content.replace(
    '''<button 
                                onClick={oncook}''',
    btn_to_add + '''\n                            <button 
                                onClick={oncook}'''
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\PageContent\AppHeader.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Updated AppHeader')
