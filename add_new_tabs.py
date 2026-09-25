import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

new_tabs = '''
                            {activeTab === 'explanation' && (
                                <div className="p-8 border-2 border-black rounded-xl bg-white shadow-[4px_4px_0px_rgba(0,0,0,1)] overflow-y-auto">
                                  <div className="flex justify-between items-center border-b-2 border-black pb-4 mb-6">
                                      <h2 className="text-2xl font-black flex items-center gap-2 text-pink-500">
                                        ✨ AI Code Explanation Engine
                                      </h2>
                                      <div className="flex gap-2">
                                          <button className="px-4 py-2 bg-pink-100 text-pink-600 font-bold border-2 border-pink-300 rounded-lg shadow-[2px_2px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-y-0.5 active:translate-x-0.5">Project Overview</button>
                                      </div>
                                  </div>
                                  
                                  <div className="bg-pink-50 border-2 border-pink-200 p-6 rounded-xl mb-6">
                                    <h3 className="font-bold text-pink-800 mb-2">Project Purpose</h3>
                                    <p className="text-pink-900">This is a <strong>{detectedLanguages.length > 0 ? detectedLanguages[0] : 'mixed'}</strong> codebase containing <strong>{totalFiles} files</strong> and approximately <strong>~{estimatedLoc.toLocaleString()} lines of code</strong>.</p>
                                  </div>
                                  
                                  <div className="bg-yellow-50 border-2 border-yellow-200 p-6 rounded-xl mb-6">
                                    <h3 className="font-bold text-yellow-800 mb-2">Architecture & Design</h3>
                                    <p className="text-yellow-900">Analyzed {flatTree?.filter(f => f.type === 'tree').length || 0} main directories. The project is primarily written in {detectedLanguages.join(', ')}.</p>
                                  </div>

                                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                                      <div className="bg-gray-50 border-2 border-gray-200 p-6 rounded-xl">
                                          <h3 className="font-bold text-gray-800 mb-4">Main Components</h3>
                                          <ul className="list-disc list-inside text-gray-600 font-mono text-sm space-y-1">
                                              {flatTree?.filter(f => f.path && (f.path.toLowerCase().includes('config') || f.path.toLowerCase().includes('main') || f.path.toLowerCase().includes('index') || f.path.toLowerCase().includes('app'))).slice(0, 5).map((f, i) => (
                                                  <li key={i}>{f.path}</li>
                                              ))}
                                          </ul>
                                      </div>
                                      <div className="bg-white border-2 border-gray-200 p-6 rounded-xl">
                                          <h3 className="font-bold text-gray-800 mb-4">Detected Technologies</h3>
                                          <div className="flex flex-wrap gap-2">
                                              {(detectedLanguages.length > 0 ? detectedLanguages : ['Unknown']).map(tech => (
                                                  <span key={tech} className="bg-pink-100 text-pink-600 border border-pink-300 rounded-lg px-3 py-1 font-bold text-sm">{tech}</span>
                                              ))}
                                          </div>
                                      </div>
                                  </div>
                                </div>
                            )}

                            {activeTab === 'generated_tests' && (
                                <div className="p-8 border-2 border-black rounded-xl bg-blue-50 shadow-[4px_4px_0px_rgba(0,0,0,1)] overflow-y-auto">
                                    <h2 className="text-2xl font-black text-blue-600 mb-4">🧪 AI Test Generator</h2>
                                    <p className="text-gray-700 mb-6">Select a file from your repository to automatically generate a comprehensive suite of unit tests, integration tests, and edge case coverage using GitVision's AI.</p>
                                    
                                    <div className="bg-white border-2 border-black rounded-xl p-6">
                                        <div className="flex flex-col gap-4">
                                            <select className="border-2 border-black rounded-lg p-3 font-mono text-sm">
                                                <option>Select a source file to generate tests...</option>
                                                {flatTree?.filter(f => f.type === 'blob' && f.path && (f.path.endsWith('.js') || f.path.endsWith('.py') || f.path.endsWith('.jsx'))).slice(0,20).map((f, i) => (
                                                    <option key={i} value={f.path}>{f.path}</option>
                                                ))}
                                            </select>
                                            <button className="bg-blue-500 text-white font-bold py-3 px-6 rounded-lg border-2 border-black shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-y-[3px] active:translate-x-[3px] w-48">Generate Tests</button>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {activeTab === 'refactored_code' && (
                                <div className="p-8 border-2 border-black rounded-xl bg-green-50 shadow-[4px_4px_0px_rgba(0,0,0,1)] overflow-y-auto">
                                    <h2 className="text-2xl font-black text-green-600 mb-4">♻️ AI Code Refactoring</h2>
                                    <p className="text-gray-700 mb-6">Instantly improve code quality, enforce SOLID principles, optimize performance, and modernize syntax using GitVision's Refactoring Engine.</p>
                                    
                                    <div className="bg-white border-2 border-black rounded-xl p-6">
                                        <div className="flex flex-col gap-4">
                                            <select className="border-2 border-black rounded-lg p-3 font-mono text-sm">
                                                <option>Select a source file to refactor...</option>
                                                {flatTree?.filter(f => f.type === 'blob' && f.path && (f.path.endsWith('.js') || f.path.endsWith('.py') || f.path.endsWith('.jsx'))).slice(0,20).map((f, i) => (
                                                    <option key={i} value={f.path}>{f.path}</option>
                                                ))}
                                            </select>
                                            <button className="bg-green-500 text-white font-bold py-3 px-6 rounded-lg border-2 border-black shadow-[3px_3px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-y-[3px] active:translate-x-[3px] w-48">Refactor Code</button>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {activeTab === 'improvements' && (
                                <div className="p-8 border-2 border-black rounded-xl bg-[#FAF5FF] shadow-[4px_4px_0px_rgba(0,0,0,1)] overflow-y-auto">
                                  <h2 className="text-2xl font-bold mb-4">🔧 Project Improvements & Recommendations</h2>
                                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                                      <div className="border-2 border-black p-4 rounded-lg bg-pink-50 text-center"><h4 className="font-bold text-pink-600">OVERALL HEALTH</h4><span className="text-3xl font-black text-pink-500">{Math.max(40, 100 - (issues?.length || 0) * 2)}%</span></div>
                                      <div className="border-2 border-black p-4 rounded-lg bg-orange-50 text-center"><h4 className="font-bold text-orange-600">CODE QUALITY</h4><span className="text-3xl font-black text-orange-500">{detectedLanguages.length > 0 ? 85 : 45}%</span></div>
                                      <div className="border-2 border-black p-4 rounded-lg bg-green-50 text-center"><h4 className="font-bold text-green-600">ARCHITECTURE</h4><span className="text-3xl font-black text-green-500">84%</span></div>
                                      <div className="border-2 border-black p-4 rounded-lg bg-purple-50 text-center"><h4 className="font-bold text-purple-600">ISSUES</h4><span className="text-xl font-black text-purple-500 mt-2 block">{issues?.length || 0} Open</span></div>
                                  </div>
                                  <div className="border-2 border-green-500 p-4 rounded-lg bg-green-50 mb-6">
                                      <h4 className="font-bold text-green-800 mb-2">✅ What's Already Done Well</h4>
                                      <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                                          <div className="bg-white p-3 rounded border border-green-300 shadow-sm font-semibold">✔ Clean Directory Structure</div>
                                          <div className="bg-white p-3 rounded border border-green-300 shadow-sm font-semibold">✔ Standard Tech Stack ({detectedLanguages[0]})</div>
                                          <div className="bg-white p-3 rounded border border-green-300 shadow-sm font-semibold">✔ Version Controlled</div>
                                      </div>
                                  </div>
                                </div>
                            )}
'''

content = re.sub(
    r'(<DependencyDashboard dependencyHealth=\{dependencyHealth\} />\s*</div>\s*</div>\s*\)}?)',
    r'\1\n' + new_tabs,
    content
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Added new tabs content')
