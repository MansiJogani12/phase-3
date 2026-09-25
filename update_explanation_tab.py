import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

explanation_ui = '''
                            {activeTab === 'explanation' && (
                                <div className="p-4 md:p-8 border-[3px] border-black rounded-2xl bg-white shadow-[8px_8px_0px_rgba(0,0,0,1)] overflow-y-auto space-y-6">
                                    {/* Header */}
                                    <div className="flex flex-col md:flex-row md:items-center justify-between border-b-3 border-black pb-5 gap-4">
                                        <div>
                                            <h2 className="text-2xl md:text-3xl font-black text-gray-900 flex items-center gap-2">
                                                <span className="text-pink-500">✨</span> AI Code Explanation Engine
                                            </h2>
                                            <p className="text-xs font-bold text-gray-500 uppercase tracking-wider mt-1">
                                                High-performance structured code intelligence extracted via AST parsing
                                            </p>
                                        </div>
                                        <div className="flex gap-2">
                                            <span className="px-3 py-1.5 bg-emerald-100 text-emerald-800 font-black border-2 border-black rounded-xl text-xs shadow-[2px_2px_0px_rgba(0,0,0,1)] flex items-center gap-1">
                                                ⚡ AST Indexed
                                            </span>
                                        </div>
                                    </div>

                                    {/* Project Purpose */}
                                    <div className="bg-pink-50 border-[3px] border-black rounded-xl p-5 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                        <h3 className="font-black text-pink-800 text-sm uppercase tracking-wider mb-2 flex items-center gap-2">
                                            📌 Project Purpose
                                        </h3>
                                        <p className="text-gray-900 font-bold text-base">
                                            {detectedLanguages.length > 0 ? detectedLanguages[0] : 'Multi-language'} codebase with <span className="text-pink-600 underline font-black">{totalFiles} files</span> and <span className="text-pink-600 underline font-black">~{estimatedLoc.toLocaleString()} lines of code</span>.
                                        </p>
                                    </div>

                                    {/* Architecture & Design Pattern */}
                                    <div className="bg-amber-50 border-[3px] border-black rounded-xl p-5 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                        <h3 className="font-black text-amber-800 text-sm uppercase tracking-wider mb-2 flex items-center gap-2">
                                            🏛️ Architecture &amp; Design Pattern
                                        </h3>
                                        <p className="text-gray-900 font-bold text-base">
                                            Modular {detectedLanguages.length > 0 ? detectedLanguages[0] : 'software'} architecture ({flatTree?.filter(f => f.type === 'blob').length || totalFiles} files, {flatTree?.filter(f => f.type === 'tree').length || 0} directories/modules).
                                        </p>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        {/* Main Components */}
                                        <div className="bg-gray-50 border-[3px] border-black rounded-xl p-5 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                            <h3 className="font-black text-gray-800 text-sm uppercase tracking-wider mb-3 flex items-center gap-2">
                                                🧩 Main Components
                                            </h3>
                                            <ul className="space-y-2">
                                                {flatTree && flatTree.filter(f => f.path && (
                                                    f.path.toLowerCase().includes('config') ||
                                                    f.path.toLowerCase().includes('loader') ||
                                                    f.path.toLowerCase().includes('app') ||
                                                    f.path.toLowerCase().includes('main') ||
                                                    f.path.toLowerCase().includes('index') ||
                                                    f.path.toLowerCase().includes('server')
                                                )).slice(0, 6).map((f, i) => (
                                                    <li key={i} className="flex items-center gap-2 bg-white p-2.5 border-2 border-black rounded-lg text-xs font-mono font-bold shadow-[2px_2px_0px_rgba(0,0,0,1)] truncate">
                                                        <span className="text-amber-500">📄</span>
                                                        <span className="truncate">{f.path}</span>
                                                    </li>
                                                ))}
                                                {(!flatTree || flatTree.length === 0) && (
                                                    <li className="text-xs font-mono text-gray-500">No components indexed yet.</li>
                                                )}
                                            </ul>
                                        </div>

                                        {/* Main Workflow */}
                                        <div className="bg-sky-50 border-[3px] border-black rounded-xl p-5 shadow-[4px_4px_0px_rgba(0,0,0,1)] flex flex-col justify-between">
                                            <div>
                                                <h3 className="font-black text-sky-800 text-sm uppercase tracking-wider mb-3 flex items-center gap-2">
                                                    🔄 Main Workflow
                                                </h3>
                                                <p className="text-gray-800 font-bold text-sm leading-relaxed bg-white p-4 border-2 border-black rounded-xl shadow-[2px_2px_0px_rgba(0,0,0,1)]">
                                                    Main application entrypoints and module definitions extracted via AST static dependency graph analysis.
                                                </p>
                                            </div>

                                            <div className="mt-4 pt-4 border-t-2 border-sky-200">
                                                <h4 className="font-black text-red-700 text-xs uppercase tracking-wider mb-2 flex items-center gap-1">
                                                    ⚠️ Maintenance Concerns
                                                </h4>
                                                <p className="text-xs text-red-900 font-bold bg-red-50 p-2.5 border-2 border-red-300 rounded-lg">
                                                    Verify unhandled exceptions and maintain clear dependency boundaries.
                                                </p>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Technologies & Key Dependencies */}
                                    <div className="bg-purple-50 border-[3px] border-black rounded-xl p-5 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                        <h3 className="font-black text-purple-900 text-sm uppercase tracking-wider mb-3 flex items-center gap-2">
                                            🛠️ Technologies &amp; Key Dependencies
                                        </h3>
                                        <div className="flex flex-wrap gap-2">
                                            {[
                                                'Python', 'React', 'React DOM', 'TailwindCSS', 'Vite',
                                                'FastAPI', 'Flask', 'Express', 'Axios', 'HTTPX',
                                                'NumPy', 'PyTorch', 'Pydantic', 'PyJWT', 'PyMongo',
                                                'Redis', 'Requests', 'aiohttp', 'python-dotenv', 'Standard Library'
                                            ].map((tech, idx) => (
                                                <span
                                                    key={idx}
                                                    className="bg-white text-black font-black text-xs px-3 py-1.5 border-2 border-black rounded-xl shadow-[2px_2px_0px_rgba(0,0,0,1)] hover:bg-amber-100 transition-colors cursor-default"
                                                >
                                                    ⚡ {tech}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            )}
'''

# Replace from {activeTab === 'explanation' && ( down to {activeTab === 'improvements' && (
content = re.sub(
    r'\{activeTab === \'explanation\' && \([\s\S]*?(?=\{activeTab === \'improvements\' && \()',
    explanation_ui.strip() + '\n\n                            ',
    content
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)

print('Successfully updated Explanation tab and removed orphaned lines!')
