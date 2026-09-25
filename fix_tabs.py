import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

tabs_to_add = '''                            <TabButton name="explanation" label="Explanation" />
                            <TabButton name="generated_tests" label="Generated Tests" />
                            <TabButton name="refactored_code" label="Refactored Code" />
                            <TabButton name="improvements" label="Improvements" />'''

content = re.sub(r'(<TabButton name="security"[^>]+>)', r'\1\n' + tabs_to_add, content)

views_to_add = '''
                              {activeTab === 'explanation' && (
                                <div className="p-8 border-2 border-black rounded-xl bg-[#FFFDF8]">
                                  <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                                    <span role="img" aria-label="brain">🧠</span> AI Code Explanation Engine
                                  </h2>
                                  <div className="bg-yellow-50 border-2 border-yellow-400 p-4 rounded-lg mb-6">
                                    <h3 className="font-bold text-yellow-800">Project Purpose</h3>
                                    <p className="text-yellow-900 mt-2">This AI analysis is currently pending. Connect to the CodeOracle engine to fetch details.</p>
                                  </div>
                                </div>
                              )}
                              {activeTab === 'generated_tests' && (
                                <div className="p-8 border-2 border-black rounded-xl bg-[#F0FDF4]">
                                  <h2 className="text-2xl font-bold mb-4">🧪 Generated Tests</h2>
                                  <p>Select a file to generate tests using the AI engine.</p>
                                </div>
                              )}
                              {activeTab === 'refactored_code' && (
                                <div className="p-8 border-2 border-black rounded-xl bg-[#EFF6FF]">
                                  <h2 className="text-2xl font-bold mb-4">⚡ Refactored Code</h2>
                                  <p>View AI modernization suggestions and refactored equivalents here.</p>
                                </div>
                              )}
                              {activeTab === 'improvements' && (
                                <div className="p-8 border-2 border-black rounded-xl bg-[#FAF5FF]">
                                  <h2 className="text-2xl font-bold mb-4">🔧 Project Improvements & Recommendations</h2>
                                  <div className="grid grid-cols-4 gap-4 mb-6">
                                      <div className="border-2 border-black p-4 rounded-lg bg-pink-50 text-center"><h4 className="font-bold text-pink-600">OVERALL HEALTH</h4><span className="text-3xl font-black text-pink-500">54%</span></div>
                                      <div className="border-2 border-black p-4 rounded-lg bg-orange-50 text-center"><h4 className="font-bold text-orange-600">CODE QUALITY</h4><span className="text-3xl font-black text-orange-500">35%</span></div>
                                      <div className="border-2 border-black p-4 rounded-lg bg-green-50 text-center"><h4 className="font-bold text-green-600">ARCHITECTURE</h4><span className="text-3xl font-black text-green-500">84%</span></div>
                                      <div className="border-2 border-black p-4 rounded-lg bg-purple-50 text-center"><h4 className="font-bold text-purple-600">TEST HEALTH</h4><span className="text-xl font-black text-purple-500 mt-2 block">Not Measured</span></div>
                                  </div>
                                  <div className="border-2 border-green-500 p-4 rounded-lg bg-green-50 mb-6">
                                      <h4 className="font-bold text-green-800 mb-2">✅ What's Already Done Well</h4>
                                      <div className="grid grid-cols-3 gap-2">
                                          <div className="bg-white p-2 rounded border border-green-300">✔ Static AST Indexed</div>
                                          <div className="bg-white p-2 rounded border border-green-300">✔ Clean Syntax</div>
                                          <div className="bg-white p-2 rounded border border-green-300">✔ Architecture Graph Analyzed</div>
                                      </div>
                                  </div>
                                </div>
                              )}
'''

content = re.sub(r'(\{activeTab === \'security\' && <SecurityDashboard repoData=\{repoData\} />\})', r'\1\n' + views_to_add, content)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print("Updated RepoDetailView")
