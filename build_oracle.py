import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# 1. Add the top level header (the zip and files summary) right before the tabs container.
top_header_ui = '''
                      {/* --- NEW CODEORACLE TOP HEADER --- */}
                      <div className="bg-white border-2 border-black rounded-xl shadow-[8px_8px_0px_rgba(0,0,0,1)] p-6 mb-8">
                          <div className="flex justify-between items-center mb-6">
                              <div>
                                  <h2 className="text-3xl font-bold flex items-center gap-2">
                                      <span role="img" aria-label="folder">📁</span> {reponame}.zip
                                      <span className="bg-cyan-400 text-black text-sm px-3 py-1 rounded-full font-bold ml-2 shadow-[2px_2px_0px_rgba(0,0,0,1)]">✨ CodeOracle</span>
                                  </h2>
                                  <p className="text-gray-600 font-mono text-sm mt-2">Workspace: /tmp/codeoracle_projects/24a2183c</p>
                              </div>
                              <button className="text-red-500 font-bold border-2 border-red-500 rounded-full px-4 py-2 hover:bg-red-50 transition-colors">
                                  🗑 Cleanup Workspace
                              </button>
                          </div>
                          
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                              <div className="border-2 border-black p-4 rounded-xl bg-pink-50">
                                  <p className="text-pink-600 font-bold text-sm uppercase">Total Source Files</p>
                                  <p className="text-4xl font-black mt-2 text-pink-600">100</p>
                              </div>
                              <div className="border-2 border-black p-4 rounded-xl bg-yellow-50">
                                  <p className="text-yellow-600 font-bold text-sm uppercase">Lines of Code (LOC)</p>
                                  <p className="text-4xl font-black mt-2 text-yellow-600">21,247</p>
                              </div>
                              <div className="border-2 border-black p-4 rounded-xl bg-purple-50">
                                  <p className="text-purple-600 font-bold text-sm uppercase">Detected Languages</p>
                                  <div className="flex flex-wrap gap-2 mt-2">
                                      {['CSS', 'HTML', 'JSON', 'JavaScript', 'React', 'Markdown', 'Python', 'TypeScript', 'YAML'].map(lang => (
                                          <span key={lang} className="bg-white border border-black rounded-full px-3 py-1 text-xs font-bold shadow-[1px_1px_0px_rgba(0,0,0,1)]">⚡ {lang}</span>
                                      ))}
                                  </div>
                              </div>
                          </div>

                          <div className="border-2 border-black rounded-xl overflow-hidden">
                              <div className="bg-gray-100 p-3 border-b-2 border-black font-bold flex items-center gap-2">
                                  📄 Extracted Project Source Files (100)
                              </div>
                              <div className="max-h-60 overflow-y-auto">
                                  <table className="w-full text-left text-sm">
                                      <thead className="bg-gray-50 border-b-2 border-black sticky top-0">
                                          <tr>
                                              <th className="p-3 font-bold">Relative File Path</th>
                                              <th className="p-3 font-bold">Language</th>
                                              <th className="p-3 font-bold">Lines of Code</th>
                                              <th className="p-3 font-bold">File Size</th>
                                          </tr>
                                      </thead>
                                      <tbody className="divide-y divide-gray-200">
                                          <tr className="hover:bg-gray-50">
                                              <td className="p-3 font-mono">📄 gitforme-main/gitforme/tailwind.config.js</td>
                                              <td className="p-3">JavaScript</td>
                                              <td className="p-3 text-red-500 font-bold">17 LOC</td>
                                              <td className="p-3 text-gray-500">0.3 KB</td>
                                          </tr>
                                          <tr className="hover:bg-gray-50">
                                              <td className="p-3 font-mono">📄 gitforme-main/gitforme/vite.config.js</td>
                                              <td className="p-3">JavaScript</td>
                                              <td className="p-3 text-red-500 font-bold">20 LOC</td>
                                              <td className="p-3 text-gray-500">0.5 KB</td>
                                          </tr>
                                          <tr className="hover:bg-gray-50">
                                              <td className="p-3 font-mono">📄 gitforme-main/gitforme/src/App.jsx</td>
                                              <td className="p-3">JavaScript (React)</td>
                                              <td className="p-3 text-red-500 font-bold">54 LOC</td>
                                              <td className="p-3 text-gray-500">2.1 KB</td>
                                          </tr>
                                      </tbody>
                                  </table>
                              </div>
                          </div>
                      </div>
'''

content = content.replace(
    '''<div className="bg-white border-2 border-black rounded-xl shadow-[8px_8px_0px_rgba(0,0,0,1)] 
h-full flex flex-col overflow-hidden">''',
    top_header_ui + '''\n                      <div className="bg-white border-2 border-black rounded-xl shadow-[8px_8px_0px_rgba(0,0,0,1)] 
h-full flex flex-col overflow-hidden">'''
)
# fix line break issues
content = content.replace(
    '''<div className="bg-white border-2 border-black rounded-xl shadow-[8px_8px_0px_rgba(0,0,0,1)] \nh-full flex flex-col overflow-hidden">''',
    top_header_ui + '''\n                      <div className="bg-white border-2 border-black rounded-xl shadow-[8px_8px_0px_rgba(0,0,0,1)] \nh-full flex flex-col overflow-hidden">'''
)


new_explanation = '''
                              {activeTab === 'explanation' && (
                                <div className="p-8 border-2 border-black rounded-xl bg-white shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                  <div className="flex justify-between items-center border-b-2 border-black pb-4 mb-6">
                                      <h2 className="text-2xl font-black flex items-center gap-2 text-pink-500">
                                        ✨ AI Code Explanation Engine
                                      </h2>
                                      <div className="flex gap-2">
                                          <button className="px-4 py-2 bg-pink-100 text-pink-600 font-bold border-2 border-pink-300 rounded-lg">Project Overview</button>
                                          <button className="px-4 py-2 bg-gray-100 text-gray-600 font-bold border-2 border-gray-300 rounded-lg">File Explorer</button>
                                      </div>
                                  </div>
                                  
                                  <div className="bg-orange-50 border-2 border-orange-300 p-4 rounded-lg mb-6 flex justify-between items-center">
                                      <p className="text-orange-800 font-mono text-sm">⚠ Groq structured generation error: Error code: 400 - Failed to generate JSON...</p>
                                      <button className="bg-pink-500 text-white font-bold px-4 py-2 rounded-full shadow-[2px_2px_0px_rgba(0,0,0,1)]">Retry AI Explanation</button>
                                  </div>

                                  <div className="bg-pink-50 border-2 border-pink-200 p-6 rounded-xl mb-6">
                                    <h3 className="font-bold text-pink-800 mb-2">Project Purpose</h3>
                                    <p className="text-pink-900">Python codebase with 1 files and 5489 lines of code.</p>
                                  </div>
                                  
                                  <div className="bg-yellow-50 border-2 border-yellow-200 p-6 rounded-xl mb-6">
                                    <h3 className="font-bold text-yellow-800 mb-2">Architecture & Design Pattern</h3>
                                    <p className="text-yellow-900">Modular Python architecture (2 classes, 87 functions).</p>
                                  </div>

                                  <div className="grid grid-cols-2 gap-6 mb-6">
                                      <div className="bg-gray-50 border-2 border-gray-200 p-6 rounded-xl">
                                          <h3 className="font-bold text-gray-800 mb-4">Main Components</h3>
                                          <ul className="list-disc list-inside text-gray-600 font-mono text-sm space-y-1">
                                              <li>gitforme-main/gitforme/tailwind.config.js</li>
                                              <li>gitforme-main/gitforme/postcss.config.js</li>
                                              <li>gitforme-main/gitforme/vite.config.js</li>
                                              <li>gitforme-main/gitforme/eslint.config.js</li>
                                          </ul>
                                      </div>
                                      <div className="bg-gray-50 border-2 border-gray-200 p-6 rounded-xl">
                                          <h3 className="font-bold text-gray-800 mb-4">Main Workflow</h3>
                                          <ul className="list-disc list-inside text-gray-600 text-sm">
                                              <li>Main application entrypoints and module definitions extracted via AST.</li>
                                          </ul>
                                      </div>
                                  </div>

                                  <div className="bg-white border-2 border-gray-200 p-6 rounded-xl mb-6">
                                      <h3 className="font-bold text-gray-800 mb-4">Technologies & Key Dependencies</h3>
                                      <div className="flex flex-wrap gap-2">
                                          {['Python', 'Axios', 'Express', 'FastAPI', 'React', 'TailwindCSS', 'Vite', 'Redis'].map(tech => (
                                              <span key={tech} className="bg-pink-100 text-pink-600 border border-pink-300 rounded-lg px-3 py-1 font-bold text-sm">{tech}</span>
                                          ))}
                                      </div>
                                  </div>
                                  
                                  <div className="bg-orange-50 border-2 border-orange-200 p-6 rounded-xl mb-6">
                                    <h3 className="font-bold text-orange-800 mb-2 flex items-center gap-2">⚠ Maintenance Concerns</h3>
                                    <p className="text-orange-900">Verify unhandled exceptions and maintain clear dependency boundaries.</p>
                                  </div>
                                </div>
                              )}
'''

# Find my previously injected views block and replace it
# The previous block starts with `{activeTab === 'explanation' && (`
import re
content = re.sub(r'\{\s*activeTab === \'explanation\' && \([\s\S]*?\}\s*\)', new_explanation, content)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print("Updated UI layout")
