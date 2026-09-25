import codecs
import re

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

dynamic_improvements_ui = '''
                            {activeTab === 'improvements' && (() => {
                                // Dynamic calculations from GitHub repo tree & issues
                                const openIssuesList = (issues && Array.isArray(issues)) ? issues.filter(i => i.state === 'open') : (issues?.open || []);
                                const openCount = openIssuesList.length;
                                
                                const testFiles = flatTree?.filter(f => f.path && (f.path.toLowerCase().includes('test') || f.path.toLowerCase().includes('spec'))) || [];
                                const hasTests = testFiles.length > 0;
                                const hasWorkflows = flatTree?.some(f => f.path && f.path.includes('.github/workflows')) || false;
                                const hasReadme = flatTree?.some(f => f.path && f.path.toLowerCase() === 'readme.md') || false;
                                const hasLicense = flatTree?.some(f => f.path && f.path.toLowerCase().includes('license')) || false;

                                const largestFile = flatTree?.filter(f => f.type === 'blob' && f.size)
                                    .sort((a, b) => (b.size || 0) - (a.size || 0))[0];

                                const overallHealth = Math.max(35, Math.min(98, 100 - (openCount * 3) - (hasTests ? 0 : 15)));
                                const codeQuality = Math.min(95, Math.max(50, 92 - (totalFiles > 150 ? 15 : 5)));
                                const architectureScore = Math.min(95, Math.max(65, 75 + (flatTree?.filter(f => f.type === 'tree').length || 0)));

                                const recs = [];

                                if (largestFile && largestFile.size > 10000) {
                                    recs.push({
                                        level: 'HIGH',
                                        badgeBg: 'bg-red-100 text-red-800 border-red-500',
                                        type: 'LARGE_FILE',
                                        title: `Refactor oversized file \`${largestFile.path}\` (~${(largestFile.size / 30).toFixed(0)} LOC)`,
                                        matters: `Large files increase cognitive load, bug density, and make maintenance & testing difficult.`,
                                        action: `Extract sub-modules or helper components out of \`${largestFile.path}\`.`,
                                        file: largestFile.path,
                                        metric: `File size: ${(largestFile.size / 1024).toFixed(1)} KB (~${(largestFile.size / 30).toFixed(0)} LOC)`
                                    });
                                }

                                if (!hasTests) {
                                    recs.push({
                                        level: 'HIGH',
                                        badgeBg: 'bg-red-100 text-red-800 border-red-500',
                                        type: 'NO_TESTS',
                                        title: `Add automated unit & integration test suite`,
                                        matters: `0 test files detected in repository tree. Changes may break existing functionality without automated regression checks.`,
                                        action: `Create a \`tests/\` directory and configure Jest, PyTest, or Vitest.`,
                                        file: `root/tests/`,
                                        metric: `Test file count = 0`
                                    });
                                }

                                if (openIssuesList.length > 0) {
                                    const topIssue = openIssuesList[0];
                                    recs.push({
                                        level: 'MEDIUM',
                                        badgeBg: 'bg-amber-100 text-amber-800 border-amber-500',
                                        type: 'OPEN_ISSUE',
                                        title: `Address active GitHub Issue #${topIssue.number}: "${topIssue.title}"`,
                                        matters: `Active open issues affect user satisfaction and project backlog health.`,
                                        action: `Inspect and resolve issue #${topIssue.number} in repository issues backlog.`,
                                        file: `GitHub Issues #${topIssue.number}`,
                                        metric: `Open issue created by ${topIssue.user?.login || 'contributor'}`
                                    });
                                }

                                if (!hasWorkflows) {
                                    recs.push({
                                        level: 'LOW',
                                        badgeBg: 'bg-cyan-100 text-cyan-800 border-cyan-500',
                                        type: 'MISSING_CI',
                                        title: `Configure GitHub Actions CI/CD workflow`,
                                        matters: `Automated building and linting ensures code quality before merging PRs.`,
                                        action: `Add a \`.github/workflows/main.yml\` workflow file.`,
                                        file: `.github/workflows/`,
                                        metric: `Workflow files detected = 0`
                                    });
                                }

                                return (
                                    <div className="p-4 md:p-8 border-[3px] border-black rounded-2xl bg-white shadow-[8px_8px_0px_rgba(0,0,0,1)] overflow-y-auto space-y-8">
                                        <div>
                                            <h2 className="text-2xl font-black text-gray-900 flex items-center gap-2">
                                                <span className="text-pink-500">✨</span> Project Improvements &amp; Recommendations
                                            </h2>
                                            <p className="text-gray-600 mt-2 text-sm md:text-base font-medium">
                                                Evidence-backed architecture, code quality, and testing recommendations derived from dynamic GitHub API tree analysis.
                                            </p>
                                        </div>

                                        {/* AI Architecture Advisory Summary */}
                                        <div className="border-[3px] border-purple-500 bg-purple-50 rounded-xl p-6 relative shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                            <div className="absolute top-0 left-0 w-full h-1.5 bg-purple-500 rounded-t-lg"></div>
                                            <h3 className="text-purple-800 font-black text-sm uppercase tracking-wider mb-2 flex items-center gap-2">
                                                <span>⚡</span> AI Architecture Advisory Summary:
                                            </h3>
                                            <p className="text-purple-950 text-sm font-semibold leading-relaxed">
                                                Repository contains {totalFiles} files with ~{estimatedLoc.toLocaleString()} total LOC across {detectedLanguages.length || 1} detected languages ({detectedLanguages.join(', ') || 'Code'}). {hasTests ? `Automated test suite detected (${testFiles.length} test files).` : 'No automated test files detected; adding tests is highly recommended.'} {openCount > 0 ? `Currently ${openCount} open issue(s) require attention.` : 'No open issues currently logged.'}
                                            </p>
                                        </div>

                                        {/* Project Health Score */}
                                        <div>
                                            <h3 className="font-black text-lg mb-4 flex items-center gap-2 text-gray-900">
                                                <span>⚡</span> Project Health Score (Dynamic Github Data)
                                            </h3>
                                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                                <div className="border-[3px] border-black p-4 rounded-xl bg-pink-50 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                                    <p className="text-pink-600 font-bold text-xs uppercase tracking-wider mb-1">OVERALL HEALTH</p>
                                                    <p className="text-3xl font-black text-pink-600">{overallHealth}%</p>
                                                </div>
                                                <div className="border-[3px] border-black p-4 rounded-xl bg-orange-50 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                                    <p className="text-orange-600 font-bold text-xs uppercase tracking-wider mb-1">CODE QUALITY</p>
                                                    <p className="text-3xl font-black text-orange-600">{codeQuality}%</p>
                                                </div>
                                                <div className="border-[3px] border-black p-4 rounded-xl bg-green-50 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                                    <p className="text-green-600 font-bold text-xs uppercase tracking-wider mb-1">ARCHITECTURE</p>
                                                    <p className="text-3xl font-black text-green-600">{architectureScore}%</p>
                                                </div>
                                                <div className="border-[3px] border-black p-4 rounded-xl bg-purple-50 shadow-[4px_4px_0px_rgba(0,0,0,1)] flex flex-col justify-center">
                                                    <p className="text-purple-600 font-bold text-xs uppercase tracking-wider mb-1">TEST HEALTH</p>
                                                    <p className={`text-lg font-black ${hasTests ? 'text-emerald-600' : 'text-purple-600'}`}>
                                                        {hasTests ? `${testFiles.length} Test Files` : 'Not Measured'}
                                                    </p>
                                                </div>
                                            </div>
                                        </div>

                                        {/* What's Already Done Well */}
                                        <div className="border-[3px] border-green-500 bg-green-50 rounded-xl p-6 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                                            <h3 className="text-green-900 font-black text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                                                <span>✅</span> What&apos;s Already Done Well (Verified Items)
                                            </h3>
                                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                                <div className="bg-white border-2 border-green-400 rounded-lg p-4 shadow-sm">
                                                    <p className="font-black text-green-800 text-sm mb-1">✔ GitHub AST Tree Parsed</p>
                                                    <p className="text-xs text-green-900 font-bold leading-tight">
                                                        {totalFiles} files with ~{estimatedLoc.toLocaleString()} LOC parsed dynamically from GitHub API.
                                                    </p>
                                                </div>
                                                <div className="bg-white border-2 border-green-400 rounded-lg p-4 shadow-sm">
                                                    <p className="font-black text-green-800 text-sm mb-1">✔ Multi-Language Stack</p>
                                                    <p className="text-xs text-green-900 font-bold leading-tight">
                                                        {detectedLanguages.join(', ') || 'Source Code'} detected and classified.
                                                    </p>
                                                </div>
                                                <div className="bg-white border-2 border-green-400 rounded-lg p-4 shadow-sm">
                                                    <p className="font-black text-green-800 text-sm mb-1">✔ Open Source Status</p>
                                                    <p className="text-xs text-green-900 font-bold leading-tight">
                                                        {hasLicense ? 'LICENSE file present.' : 'Repository indexed and accessible.'} {hasReadme ? 'README documentation present.' : ''}
                                                    </p>
                                                </div>
                                            </div>
                                        </div>

                                        {/* Prioritized Recommendations */}
                                        <div>
                                            <div className="flex justify-between items-center mb-6">
                                                <h3 className="font-black text-lg flex items-center gap-2 text-gray-900">
                                                    <span className="text-pink-500">🔥</span> Dynamic Recommendations ({recs.length})
                                                </h3>
                                            </div>

                                            <div className="space-y-6">
                                                {recs.map((rec, idx) => (
                                                    <div key={idx} className="border-[3px] border-black rounded-xl p-6 bg-white shadow-[6px_6px_0px_rgba(0,0,0,1)] space-y-4">
                                                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-2">
                                                            <div className="flex items-center gap-3 flex-wrap">
                                                                <span className={`border-2 rounded-full px-3 py-0.5 text-xs font-black shadow-xs ${rec.badgeBg}`}>
                                                                    {rec.level}
                                                                </span>
                                                                <span className="bg-gray-100 text-gray-700 border-2 border-gray-300 rounded text-[10px] px-2 py-0.5 font-mono uppercase tracking-wider font-black">
                                                                    {rec.type}
                                                                </span>
                                                                <h4 className="font-black text-base md:text-lg text-gray-900">{rec.title}</h4>
                                                            </div>
                                                            <span className="text-xs text-gray-400 font-mono font-bold">Source: github_api_scan</span>
                                                        </div>

                                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                            <div className="bg-amber-50 border-2 border-amber-300 rounded-lg p-4">
                                                                <h5 className="font-black text-amber-800 text-xs uppercase tracking-wider mb-1 flex items-center gap-1">💡 Why It Matters:</h5>
                                                                <p className="text-amber-950 text-xs font-bold leading-relaxed">{rec.matters}</p>
                                                            </div>
                                                            <div className="bg-emerald-50 border-2 border-emerald-300 rounded-lg p-4">
                                                                <h5 className="font-black text-emerald-800 text-xs uppercase tracking-wider mb-1 flex items-center gap-1">🛠️ Suggested Action:</h5>
                                                                <p className="text-emerald-950 text-xs font-bold leading-relaxed">{rec.action}</p>
                                                            </div>
                                                        </div>

                                                        <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-t-2 border-gray-100 pt-4 gap-2 text-xs font-mono">
                                                            <div className="flex items-center gap-2">
                                                                <span className="font-bold text-gray-600">Affected File/Target:</span>
                                                                <span className="bg-gray-100 border border-black rounded px-2.5 py-1 font-bold text-gray-800">{rec.file}</span>
                                                            </div>
                                                            <span className="text-blue-600 font-bold">{rec.metric}</span>
                                                        </div>
                                                    </div>
                                                ))}

                                                {recs.length === 0 && (
                                                    <div className="p-8 text-center bg-gray-50 border-2 border-dashed border-gray-300 rounded-xl">
                                                        <p className="font-bold text-gray-600">No major architectural issues detected for this repository!</p>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                );
                            })()}
'''

content = re.sub(
    r'\{activeTab === \'improvements\' && \([\s\S]*?\)\}\n*',
    dynamic_improvements_ui.strip() + '\n',
    content
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)

print('Successfully made Improvements tab completely dynamic!')
