import codecs
import re

raw_files = """
📄 gitforme-main/gitforme/tailwind.config.js	JavaScript	17 LOC	0.3 KB
📄 gitforme-main/gitforme/postcss.config.js	JavaScript	6 LOC	0.1 KB
📄 gitforme-main/gitforme/vite.config.js	JavaScript	20 LOC	0.5 KB
📄 gitforme-main/gitforme/eslint.config.js	JavaScript	28 LOC	0.7 KB
📄 gitforme-main/gitforme/Loaders/SkeletonLoader.jsx	JavaScript (React)	11 LOC	0.7 KB
📄 gitforme-main/gitforme/src/App.jsx	JavaScript (React)	54 LOC	2.1 KB
📄 gitforme-main/gitforme/src/main.jsx	JavaScript (React)	27 LOC	0.9 KB
📄 gitforme-main/gitforme/src/context/AuthContext.jsx	JavaScript (React)	182 LOC	7.6 KB
📄 gitforme-main/gitforme/src/PageContent/LandingPageContent.jsx	JavaScript (React)	253 LOC	13.1 KB
📄 gitforme-main/gitforme/src/PageContent/FileContentModal.jsx	JavaScript (React)	49 LOC	2.9 KB
📄 gitforme-main/gitforme/src/PageContent/AppHeader.jsx	JavaScript (React)	202 LOC	15.0 KB
📄 gitforme-main/gitforme/src/cards/RepoHeaderCard.jsx	JavaScript (React)	67 LOC	6.2 KB
📄 gitforme-main/gitforme/src/cards/FeatureCard.jsx	JavaScript (React)	16 LOC	0.7 KB
📄 gitforme-main/gitforme/src/cards/GoodFirstIssues.jsx	JavaScript (React)	20 LOC	1.0 KB
📄 gitforme-main/gitforme/src/cards/StepCard.jsx	JavaScript (React)	18 LOC	0.7 KB
📄 gitforme-main/gitforme/src/cards/AccordionCard.jsx	JavaScript (React)	18 LOC	1.3 KB
📄 gitforme-main/gitforme/src/api/axiosConfig.js	JavaScript	62 LOC	2.1 KB
📄 gitforme-main/gitforme/src/components/Iconsfile.jsx	JavaScript (React)	83 LOC	5.8 KB
📄 gitforme-main/gitforme/src/components/FileHistoryPanel.jsx	JavaScript (React)	37 LOC	2.2 KB
📄 gitforme-main/gitforme/src/components/GitHistoryTimeline.jsx	JavaScript (React)	77 LOC	3.0 KB
📄 gitforme-main/gitforme/src/components/ContributorList.jsx	JavaScript (React)	18 LOC	1.0 KB
📄 gitforme-main/gitforme/src/components/VulnerabilityScanPage.jsx	JavaScript (React)	118 LOC	5.8 KB
📄 gitforme-main/gitforme/src/components/ReportModal.jsx	JavaScript (React)	37 LOC	2.6 KB
📄 gitforme-main/gitforme/src/components/RepoDetailView.jsx	JavaScript (React)	467 LOC	26.4 KB
📄 gitforme-main/gitforme/src/components/gitformeUi.jsx	JavaScript (React)	276 LOC	12.1 KB
📄 gitforme-main/gitforme/src/components/InsightsView.jsx	JavaScript (React)	28 LOC	1.5 KB
📄 gitforme-main/gitforme/src/components/DependencyDashboard.jsx	JavaScript (React)	65 LOC	4.0 KB
📄 gitforme-main/gitforme/src/components/ProtectedRoute.jsx	JavaScript (React)	15 LOC	0.5 KB
📄 gitforme-main/gitforme/src/components/FeatureStoryModal.jsx	JavaScript (React)	88 LOC	4.8 KB
📄 gitforme-main/gitforme/src/components/VulnerabilityScanner.jsx	JavaScript (React)	299 LOC	20.6 KB
📄 gitforme-main/gitforme/src/components/RepoIssues.jsx	JavaScript (React)	29 LOC	2.5 KB
📄 gitforme-main/gitforme/src/components/Chatbot.jsx	JavaScript (React)	530 LOC	17.9 KB
📄 gitforme-main/gitforme/src/components/DirectoryStructure.jsx	JavaScript (React)	91 LOC	4.8 KB
📄 gitforme-main/gitforme/src/components/FileGraph.jsx	JavaScript (React)	168 LOC	10.8 KB
📄 gitforme-main/gitforme/src/components/DomainShiftBanner.jsx	JavaScript (React)	47 LOC	1.8 KB
📄 gitforme-main/gitforme/src/components/Badges.jsx	JavaScript (React)	18 LOC	0.6 KB
📄 gitforme-main/gitforme/pages/RepoPage.jsx	JavaScript (React)	55 LOC	1.9 KB
📄 gitforme-main/gitforme/pages/gitpage.jsx	JavaScript (React)	51 LOC	1.7 KB
📄 gitforme-main/vscode/src/api.ts	TypeScript	46 LOC	1.8 KB
📄 gitforme-main/vscode/src/extension.ts	TypeScript	58 LOC	2.4 KB
📄 gitforme-main/vscode/media/sidebar.js	JavaScript	21 LOC	0.9 KB
📄 gitforme-main/llm-server/app.py	Python	318 LOC	16.1 KB
📄 gitforme-main/server/index.js	JavaScript	102 LOC	3.9 KB
📄 gitforme-main/server/config/envconfig.js	JavaScript	22 LOC	0.9 KB
📄 gitforme-main/server/models/UserModel.js	JavaScript	16 LOC	0.7 KB
📄 gitforme-main/server/Controllers/AuthController.js	JavaScript	110 LOC	5.4 KB
📄 gitforme-main/server/Controllers/StatsController.js	JavaScript	31 LOC	1.3 KB
📄 gitforme-main/server/Controllers/InsightController.js	JavaScript	148 LOC	8.2 KB
📄 gitforme-main/server/Controllers/GithubController.js	JavaScript	411 LOC	18.2 KB
📄 gitforme-main/server/scripts/swaggerGen.js	JavaScript	16 LOC	0.6 KB
📄 gitforme-main/server/scripts/export-yaml.js	JavaScript	10 LOC	0.4 KB
📄 gitforme-main/server/api/osvApi.js	JavaScript	39 LOC	1.6 KB
📄 gitforme-main/server/api/githubApi.js	JavaScript	58 LOC	1.8 KB
📄 gitforme-main/server/Routes/RepoRoutes.js	JavaScript	209 LOC	6.6 KB
📄 gitforme-main/server/Routes/AuthRoute.js	JavaScript	64 LOC	1.8 KB
📄 gitforme-main/server/Routes/StatsRoute.js	JavaScript	15 LOC	0.4 KB
📄 gitforme-main/server/Middlewares/AuthMiddleware.js	JavaScript	43 LOC	2.3 KB
📄 gitforme-main/server/util/RediaClient.js	JavaScript	53 LOC	2.0 KB
📄 gitforme-main/server/util/RediaClient.test.js	JavaScript	16 LOC	0.8 KB
📄 gitforme-main/server/util/githubApi.js	JavaScript	30 LOC	1.1 KB
📄 gitforme-main/server/util/SecretToken.js	JavaScript	6 LOC	0.2 KB
📄 gitforme-main/.gitignore	Plain Text	14 LOC	0.2 KB
📄 gitforme-main/README.md	Markdown	179 LOC	8.6 KB
📄 gitforme-main/package-lock.json	JSON	264 LOC	8.5 KB
📄 gitforme-main/docker-compose.yml	YAML	23 LOC	0.4 KB
📄 gitforme-main/OPTIMIZATION_SUMMARY.md	Markdown	165 LOC	6.2 KB
📄 gitforme-main/SECURITY_SUMMARY.md	Markdown	61 LOC	2.8 KB
📄 gitforme-main/PERFORMANCE_IMPROVEMENTS.md	Markdown	96 LOC	5.0 KB
📄 gitforme-main/package.json	JSON	7 LOC	0.1 KB
📄 gitforme-main/LICENSE	Plain Text	17 LOC	1.0 KB
📄 gitforme-main/gitforme/index.html	HTML	49 LOC	1.6 KB
📄 gitforme-main/gitforme/.gitignore	Plain Text	24 LOC	0.3 KB
📄 gitforme-main/gitforme/README.md	Markdown	7 LOC	0.8 KB
📄 gitforme-main/gitforme/.env.development	Plain Text	1 LOC	0.0 KB
📄 gitforme-main/gitforme/staticwebapp.config.json	JSON	13 LOC	0.3 KB
📄 gitforme-main/gitforme/package-lock.json	JSON	10552 LOC	375.3 KB
📄 gitforme-main/gitforme/vercel.json	JSON	8 LOC	0.1 KB
📄 gitforme-main/gitforme/package.json	JSON	58 LOC	1.6 KB
📄 gitforme-main/gitforme/public/ads.txt	Plain Text	1 LOC	0.1 KB
📄 gitforme-main/gitforme/src/index.css	CSS	3 LOC	0.1 KB
📄 gitforme-main/gitforme/src/App.css	CSS	0 LOC	0.0 KB
📄 gitforme-main/vscode/README.md	Markdown	20 LOC	0.8 KB
📄 gitforme-main/vscode/package-lock.json	JSON	602 LOC	21.3 KB
📄 gitforme-main/vscode/tsconfig.json	JSON	14 LOC	0.3 KB
📄 gitforme-main/vscode/package.json	JSON	49 LOC	1.0 KB
📄 gitforme-main/llm-server/requirements.txt	Plain Text	13 LOC	0.2 KB
📄 gitforme-main/llm-server/Dockerfile	Plain Text	8 LOC	0.3 KB
📄 gitforme-main/server/Dockerfile	Plain Text	9 LOC	0.3 KB
📄 gitforme-main/server/.env.production	Plain Text	10 LOC	0.4 KB
📄 gitforme-main/server/.env.development	Plain Text	13 LOC	0.5 KB
📄 gitforme-main/server/package-lock.json	JSON	2338 LOC	84.8 KB
📄 gitforme-main/server/.dockerignore	Plain Text	6 LOC	0.1 KB
📄 gitforme-main/server/package.json	JSON	30 LOC	0.8 KB
📄 gitforme-main/server/docs/api-docs.yaml	YAML	368 LOC	10.6 KB
📄 gitforme-main/server/docs/swagger.json	JSON	564 LOC	14.9 KB
📄 gitforme-main/.github/workflows/azure-static-web-apps-thankful-dune-02c682800.yml	YAML	49 LOC	1.8 KB
📄 gitforme-main/.github/workflows/main_gfmb.yml	YAML	56 LOC	1.6 KB
📄 gitforme-main/.github/ISSUE_TEMPLATE/feature_request.md	Markdown	15 LOC	0.6 KB
📄 gitforme-main/.github/ISSUE_TEMPLATE/bug_report.md	Markdown	30 LOC	0.8 KB
📄 gitforme-main/docs/pull_request_template.md	Markdown	22 LOC	0.8 KB
"""

rows = []
for line in raw_files.strip().split('\n'):
    parts = line.split('\t')
    if len(parts) == 4:
        name, lang, loc, size = parts
        rows.append(f'''                                          <tr className="hover:bg-gray-50">
                                              <td className="p-3 font-mono">{name}</td>
                                              <td className="p-3">{lang}</td>
                                              <td className="p-3 text-red-500 font-bold">{loc}</td>
                                              <td className="p-3 text-gray-500">{size}</td>
                                          </tr>''')

new_tbody = '<tbody className="divide-y divide-gray-200">\n' + '\n'.join(rows) + '\n                                      </tbody>'

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    content = f.read()

# Replace the old tbody with the new one
content = re.sub(r'<tbody className="divide-y divide-gray-200">.*?</tbody>', new_tbody, content, flags=re.DOTALL)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)
print("Updated table")
