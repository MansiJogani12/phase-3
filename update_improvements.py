import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

improvements_ui = '''
                            {activeTab === 'improvements' && (
                                <div className="p-4 md:p-8 border-[3px] border-black rounded-2xl bg-white shadow-[8px_8px_0px_rgba(0,0,0,1)] overflow-y-auto">
                                  <div className="mb-8">
                                      <h2 className="text-2xl font-black text-gray-900 flex items-center gap-2">
                                          <span className="text-pink-500">✨</span> Project Improvements & Recommendations
                                      </h2>
                                      <p className="text-gray-600 mt-2 text-sm md:text-base">Evidence-backed architecture, code quality, and testing recommendations derived from deterministic local analysis.</p>
                                      
                                      <div className="flex gap-4 mt-4">
                                          <button className="bg-purple-600 text-white font-bold py-2 px-6 rounded-full border-2 border-black shadow-[4px_4px_0px_rgba(0,0,0,1)] hover:bg-purple-700 hover:-translate-y-0.5 transition-all">✨ Generate AI Recommendations</button>
                                          <button className="bg-white text-black font-bold py-2 px-6 rounded-full border-2 border-black shadow-[4px_4px_0px_rgba(0,0,0,1)] hover:bg-gray-50 hover:-translate-y-0.5 transition-all flex items-center gap-2">↻ Refresh</button>
                                      </div>
                                  </div>

                                  <div className="border-[3px] border-purple-500 bg-purple-50 rounded-xl p-6 mb-8 relative shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                      <div className="absolute top-0 left-0 w-full h-1 bg-purple-500 rounded-t-lg"></div>
                                      <h3 className="text-purple-700 font-bold mb-2 flex items-center gap-2">
                                          <span>⚡</span> AI Architecture Advisory Summary:
                                      </h3>
                                      <p className="text-purple-900 text-sm">
                                          The project exhibits a high concentration of oversized functions across multiple components, significantly impacting code quality (35%). Refactoring these large functions into smaller, manageable units will improve maintainability and code quality.
                                      </p>
                                  </div>

                                  <div className="mb-8">
                                      <h3 className="font-bold text-lg mb-4 flex items-center gap-2 text-gray-800">
                                          <span>⚡</span> Project Health Score (Deterministic Calculation)
                                      </h3>
                                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                          <div className="border-[3px] border-black p-4 rounded-xl bg-white shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                              <p className="text-pink-600 font-bold text-xs uppercase tracking-wider mb-1">OVERALL HEALTH</p>
                                              <p className="text-3xl font-black text-pink-600">54%</p>
                                          </div>
                                          <div className="border-[3px] border-black p-4 rounded-xl bg-white shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                              <p className="text-orange-500 font-bold text-xs uppercase tracking-wider mb-1">CODE QUALITY</p>
                                              <p className="text-3xl font-black text-orange-500">35%</p>
                                          </div>
                                          <div className="border-[3px] border-black p-4 rounded-xl bg-white shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                              <p className="text-green-500 font-bold text-xs uppercase tracking-wider mb-1">ARCHITECTURE</p>
                                              <p className="text-3xl font-black text-green-500">84%</p>
                                          </div>
                                          <div className="border-[3px] border-black p-4 rounded-xl bg-purple-50 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                              <p className="text-purple-600 font-bold text-xs uppercase tracking-wider mb-1">TEST HEALTH</p>
                                              <p className="text-2xl font-black text-purple-600">Not Measured</p>
                                          </div>
                                      </div>
                                  </div>

                                  <div className="border-[3px] border-green-500 bg-green-50 rounded-xl p-6 mb-8 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                      <h3 className="text-green-800 font-bold mb-4 flex items-center gap-2">
                                          <span>✅</span> What's Already Done Well (3 Verified Items)
                                      </h3>
                                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                          <div className="bg-white border-2 border-green-400 rounded-lg p-3 shadow-sm">
                                              <p className="font-bold text-green-700 text-sm mb-1">✔ Static AST Indexed</p>
                                              <p className="text-xs text-green-600 leading-tight">61 source files with 5,489 lines of code parsed without AI token cost.</p>
                                          </div>
                                          <div className="bg-white border-2 border-green-400 rounded-lg p-3 shadow-sm">
                                              <p className="font-bold text-green-700 text-sm mb-1">✔ Clean Syntax</p>
                                              <p className="text-xs text-green-600 leading-tight">100% of analyzed codebase files have valid, parseable syntax.</p>
                                          </div>
                                          <div className="bg-white border-2 border-green-400 rounded-lg p-3 shadow-sm">
                                              <p className="font-bold text-green-700 text-sm mb-1">✔ Architecture Graph Analyzed</p>
                                              <p className="text-xs text-green-600 leading-tight">61 modules connected via 69 verified dependency edges.</p>
                                          </div>
                                      </div>
                                  </div>

                                  <div className="mb-8">
                                      <div className="flex justify-between items-center mb-6">
                                          <h3 className="font-bold text-lg flex items-center gap-2 text-gray-800">
                                              <span className="text-pink-500">🔥</span> Prioritized Recommendations (1)
                                          </h3>
                                          <div className="flex gap-2 bg-gray-100 p-1 rounded-full border-2 border-black">
                                              <button className="px-3 py-1 bg-white border-2 border-black rounded-full text-xs font-bold shadow-[2px_2px_0px_rgba(0,0,0,1)]">All (30)</button>
                                              <button className="px-3 py-1 text-gray-500 hover:text-black text-xs font-bold">High (18)</button>
                                              <button className="px-3 py-1 text-gray-500 hover:text-black text-xs font-bold">Medium (17)</button>
                                              <button className="px-3 py-1 bg-cyan-100 text-cyan-800 border-2 border-cyan-300 rounded-full text-xs font-bold shadow-[2px_2px_0px_rgba(0,0,0,1)]">Low (2)</button>
                                          </div>
                                      </div>

                                      <div className="border-[3px] border-black rounded-xl p-6 bg-white shadow-[6px_6px_0px_rgba(0,0,0,1)]">
                                          <div className="flex justify-between items-start mb-4">
                                              <div className="flex items-center gap-3">
                                                  <span className="bg-cyan-100 text-cyan-800 border-2 border-cyan-500 rounded-full px-3 py-0.5 text-xs font-bold">LOW</span>
                                                  <span className="bg-gray-100 text-gray-600 border border-gray-300 rounded text-[10px] px-2 font-mono uppercase tracking-wider">UNUSED_IMPORTS</span>
                                                  <h4 className="font-black text-lg">Remove unused imports in `gitforme-main/llm-server/app.py`</h4>
                                              </div>
                                              <span className="text-xs text-gray-400 font-mono">Source: static_analysis</span>
                                          </div>
                                          <p className="text-sm text-gray-600 mb-6">Unused imports detected: np, requests</p>
                                          
                                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                                              <div className="bg-orange-50 border-2 border-orange-200 rounded-lg p-4">
                                                  <h5 className="font-bold text-orange-700 text-sm mb-2 flex items-center gap-1">💡 Why It Matters:</h5>
                                                  <p className="text-orange-900 text-xs">Unused imports clutter module namespace and can introduce unnecessary startup import overhead.</p>
                                              </div>
                                              <div className="bg-green-50 border-2 border-green-200 rounded-lg p-4">
                                                  <h5 className="font-bold text-green-700 text-sm mb-2 flex items-center gap-1">🛠️ Suggested Action:</h5>
                                                  <p className="text-green-900 text-xs">Clean up unused import headers.</p>
                                              </div>
                                          </div>

                                          <div className="flex justify-between items-center border-t-2 border-gray-100 pt-4">
                                              <div className="flex items-center gap-2">
                                                  <span className="text-xs text-gray-500 font-bold">Affected Files:</span>
                                                  <span className="bg-gray-100 border border-gray-300 rounded px-3 py-1 text-xs font-mono">📄 gitforme-main/llm-server/app.py</span>
                                              </div>
                                              <button className="text-xs font-bold flex items-center gap-1 border-2 border-black rounded-lg px-3 py-1.5 hover:bg-gray-50">Hide Evidence <span>▲</span></button>
                                          </div>
                                          
                                          <div className="mt-4 bg-gray-50 border-2 border-gray-200 rounded-lg p-4">
                                              <h6 className="font-bold text-sm mb-3 flex items-center gap-2">🔍 Traceable Evidence Metrics:</h6>
                                              <div className="flex justify-between items-center text-xs font-mono text-pink-600 bg-white p-2 border border-gray-200 rounded">
                                                  <span>File: gitforme-main/llm-server/app.py</span>
                                                  <span className="text-blue-600">Metric: unused_imports = Unused imports detected: np, requests</span>
                                              </div>
                                              <p className="text-xs text-gray-500 mt-2 font-mono">Unused imports detected: np, requests</p>
                                          </div>
                                      </div>
                                  </div>
                                </div>
                            )}
'''

# Use regex to replace the existing improvements tab
content = re.sub(
    r'\{activeTab === \'improvements\' && \([\s\S]*?\}\s*\)',
    improvements_ui.strip() + '\n',
    content,
    count=1
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print('Updated Improvements UI')
