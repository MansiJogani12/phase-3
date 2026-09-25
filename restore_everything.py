import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# ADD THE TABS TO THE TAB BAR
tab_buttons = '''
                                  <TabButton name="security" label="Security" icon="🛡️" />
                                  <TabButton name="explanation" label="Explanation" />
                                  <TabButton name="generated_tests" label="Generated Tests" />
                                  <TabButton name="refactored_code" label="Refactored Code" />
                                  <TabButton name="improvements" label="Improvements" />
'''
content = re.sub(r'<TabButton name="security" label="Security" icon="🛡️" />', tab_buttons.strip(), content)

# ADD THE PROJECT STATS AND FILE TABLE
table_ui = '''
            {/* --- PROJECT STATS & FILE TABLE --- */}
            <div className="bg-white border-[3px] border-black rounded-2xl shadow-[8px_8px_0px_rgba(0,0,0,1)] p-4 md:p-8 mt-8 mb-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div className="border-[3px] border-black p-4 rounded-xl bg-pink-50 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                        <p className="text-pink-600 font-bold text-xs uppercase tracking-wider mb-2 flex items-center gap-2"><span>📁</span> Total Source Files</p>
                        <p className="text-4xl font-black text-pink-600">{totalFiles}</p>
                    </div>
                    <div className="border-[3px] border-black p-4 rounded-xl bg-yellow-50 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                        <p className="text-yellow-600 font-bold text-xs uppercase tracking-wider mb-2 flex items-center gap-2"><span>📊</span> Lines of Code (LOC)</p>
                        <p className="text-4xl font-black text-yellow-600">~{estimatedLoc.toLocaleString()}</p>
                    </div>
                    <div className="border-[3px] border-black p-4 rounded-xl bg-purple-50 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                        <p className="text-purple-600 font-bold text-xs uppercase tracking-wider mb-2 flex items-center gap-2"><span>🎨</span> Detected Languages</p>
                        <div className="flex flex-wrap gap-2 mt-2">
                            {(detectedLanguages.length > 0 ? detectedLanguages : ['Unknown']).map(lang => (
                                <span key={lang} className="bg-white border-2 border-black rounded-full px-3 py-1 text-xs font-bold shadow-[2px_2px_0px_rgba(0,0,0,1)]">⚡ {lang}</span>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="border-[3px] border-black rounded-xl overflow-hidden shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                    <div className="bg-gray-100 p-4 border-b-[3px] border-black font-bold flex flex-wrap justify-between items-center gap-4">
                        <span className="flex items-center gap-2 text-lg"><span>📄</span> Extracted Project Source Files ({totalFiles})</span>
                        <div className="relative w-full md:w-auto">
                            <input type="text" placeholder="Search files..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="border-2 border-black rounded-lg px-4 py-2 text-sm font-bold w-full md:w-72 shadow-[2px_2px_0px_rgba(0,0,0,1)] focus:outline-none focus:translate-x-[2px] focus:translate-y-[2px] focus:shadow-none transition-all" />
                        </div>
                    </div>
                    <div className="max-h-[500px] overflow-y-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-gray-50 border-b-[3px] border-black sticky top-0 z-10">
                                <tr>
                                    <th className="p-4 font-black">Relative File Path</th>
                                    <th className="p-4 font-black">Language</th>
                                    <th className="p-4 font-black">Lines of Code</th>
                                    <th className="p-4 font-black">File Size</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y-2 divide-black">
                                {flatTree && Array.isArray(flatTree) && flatTree.filter(f => {
                                    try { return !searchQuery || (f && f.path && typeof f.path === 'string' && f.path.toLowerCase().includes(searchQuery.toLowerCase())); } catch (e) { return false; }
                                }).slice(0, 500).map((file, idx) => (
                                    <tr key={idx} className="hover:bg-amber-50 transition-colors">
                                        <td className="p-4 font-mono font-bold text-gray-700 flex items-center gap-2"><span>📄</span> {file && file.path ? file.path : 'Unknown'}</td>
                                        <td className="p-4 font-bold">{(file && file.path && typeof file.path === 'string' && file.path.includes('.')) ? extToLang[file.path.split('.').pop().toLowerCase()] || 'Unknown' : 'Unknown'}</td>
                                        <td className="p-4 text-red-600 font-black">~{file && !isNaN(file.size) ? (file.size / 30).toFixed(0) : 0} LOC</td>
                                        <td className="p-4 text-gray-600 font-bold">{file && !isNaN(file.size) ? (file.size / 1024).toFixed(2) : 0} KB</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
'''
content = content.replace(
    '<RepoHeaderCard {...{ username, reponame, repoData, deployments, onFastClone: handleFastClone, onGenerateReport: handleGenerateReport, isReportLoading, onAiChatClick: () => setIsChatOpen(true) }} />',
    '<RepoHeaderCard {...{ username, reponame, repoData, deployments, onFastClone: handleFastClone, onGenerateReport: handleGenerateReport, isReportLoading, onAiChatClick: () => setIsChatOpen(true) }} />\n' + table_ui
)


# FIX LAYOUT ISSUE
# Make it flex-col instead of grid so the file map can expand fully without being squished on the left
content = content.replace(
    '<div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">',
    '<div className="mt-8 flex flex-col gap-8">'
)
content = content.replace(
    '<div className="lg:col-span-2">',
    '<div className="w-full">'
)
content = content.replace(
    '<div className="lg:col-span-1 flex flex-col gap-8">',
    '<div className="w-full grid grid-cols-1 md:grid-cols-2 gap-8">'
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Restored EVERYTHING!')
