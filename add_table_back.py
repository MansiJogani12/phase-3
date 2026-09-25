import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# Add searchQuery back if I removed it (Wait, I might have kept it. Let's check if it exists)
if 'const [searchQuery, setSearchQuery]' not in content:
    content = content.replace(
        'const [isHistoryLoading, setIsHistoryLoading] = useState(false);',
        'const [isHistoryLoading, setIsHistoryLoading] = useState(false);\n    const [searchQuery, setSearchQuery] = useState("");'
    )

table_ui = '''
                          {/* --- PROJECT STATS & FILE TABLE --- */}
                          <div className="bg-white border-2 border-black rounded-xl shadow-[8px_8px_0px_rgba(0,0,0,1)] p-6 mt-8">
                              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                                  <div className="border-2 border-black p-4 rounded-xl bg-pink-50">
                                      <p className="text-pink-600 font-bold text-sm uppercase">📁 Total Source Files</p>
                                      <p className="text-4xl font-black mt-2 text-pink-600">{totalFiles}</p>
                                  </div>
                                  <div className="border-2 border-black p-4 rounded-xl bg-yellow-50">
                                      <p className="text-yellow-600 font-bold text-sm uppercase">📊 Lines of Code (LOC)</p>
                                      <p className="text-4xl font-black mt-2 text-yellow-600">~{estimatedLoc.toLocaleString()}</p>
                                  </div>
                                  <div className="border-2 border-black p-4 rounded-xl bg-purple-50">
                                      <p className="text-purple-600 font-bold text-sm uppercase">🎨 Detected Languages</p>
                                      <div className="flex flex-wrap gap-2 mt-2">
                                          {(detectedLanguages.length > 0 ? detectedLanguages : ['Unknown']).map(lang => (
                                              <span key={lang} className="bg-white border border-black rounded-full px-3 py-1 text-xs font-bold shadow-[1px_1px_0px_rgba(0,0,0,1)]">⚡ {lang}</span>
                                          ))}
                                      </div>
                                  </div>
                              </div>

                              <div className="border-2 border-black rounded-xl overflow-hidden">
                                  <div className="bg-gray-100 p-3 border-b-2 border-black font-bold flex justify-between items-center gap-2">
                                      <span className="flex items-center gap-2">📄 Extracted Project Source Files ({totalFiles})</span>
                                      <div className="relative">
                                          <input type="text" placeholder="Search files..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="border-2 border-black rounded-lg px-3 py-1.5 text-sm font-normal w-64 shadow-[2px_2px_0px_rgba(0,0,0,1)] focus:outline-none focus:translate-x-[2px] focus:translate-y-[2px] focus:shadow-none transition-all" />
                                          <svg className="w-4 h-4 absolute right-3 top-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                                      </div>
                                  </div>
                                  <div className="max-h-[500px] overflow-y-auto">
                                      <table className="w-full text-left text-sm">
                                          <thead className="bg-gray-50 border-b-2 border-black sticky top-0 z-10">
                                              <tr>
                                                  <th className="p-3 font-bold">Relative File Path</th>
                                                  <th className="p-3 font-bold">Language</th>
                                                  <th className="p-3 font-bold">Lines of Code</th>
                                                  <th className="p-3 font-bold">File Size</th>
                                              </tr>
                                          </thead>
                                          <tbody className="divide-y divide-gray-200">
                                              {flatTree && Array.isArray(flatTree) && flatTree.filter(f => {
                                                  try { return !searchQuery || (f && f.path && typeof f.path === 'string' && f.path.toLowerCase().includes(searchQuery.toLowerCase())); } catch (e) { return false; }
                                              }).slice(0, 500).map((file, idx) => (
                                                  <tr key={idx} className="hover:bg-gray-50">
                                                      <td className="p-3 font-mono">📄 {file && file.path ? file.path : 'Unknown'}</td>
                                                      <td className="p-3">{(file && file.name && typeof file.name === 'string' && file.name.includes('.')) ? extToLang[file.name.split('.').pop().toLowerCase()] || 'Unknown' : 'Unknown'}</td>
                                                      <td className="p-3 text-red-500 font-bold">~{file && !isNaN(file.size) ? (file.size / 30).toFixed(0) : 0} LOC</td>
                                                      <td className="p-3 text-gray-500">{file && !isNaN(file.size) ? (file.size / 1024).toFixed(2) : 0} KB</td>
                                                  </tr>
                                              ))}
                                          </tbody>
                                      </table>
                                  </div>
                              </div>
                          </div>
                          {/* -------------------------------------- */}
'''

# We will inject this right before `<div className="w-full flex flex-col gap-8 mt-8">`
# Which is where the LLM Context Builder begins.
content = content.replace(
    '<div className="w-full flex flex-col gap-8 mt-8">',
    table_ui + '\n                          <div className="w-full flex flex-col gap-8 mt-8">'
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Added table back')
