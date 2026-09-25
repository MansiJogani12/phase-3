You are continuing development of the EXISTING GitVision application.

IMPORTANT:
DO NOT rebuild GitVision.

DO NOT remove or break any existing functionality.

Existing functionality includes:

PHASE 1:
- OpenRouter AI provider
- AI provider abstraction
- configurable model
- streaming chatbot
- repository context engine
- file retrieval
- conversation persistence
- AI telemetry
- prompt injection protection

PHASE 2:
- Repository Workspace
- Repository snapshots
- Analysis runs
- Analysis stages
- Analysis history
- Workspace chat
- Notes
- Workspace authorization
- snapshot comparison foundation
- audit events

PHASE 3:
- GitHub OAuth
- GitHub account connection
- repository selector
- repository search/filter/sort
- public repository access
- private repository access checks
- organization repository support
- repository synchronization
- GitHub API telemetry
- GitHub rate-limit handling
- workspace creation from repository selector

Existing GitVision features must continue working:

- repository dashboard
- directory
- file map
- timeline
- issues
- insights
- security
- contributors
- deployments
- hotspots
- OSV scanning
- bulk scanning
- reports
- dependency visualization
- architecture visualization
- FastClone

============================================================
PHASE 4
UNIVERSAL REPOSITORY INGESTION + ZIP UPLOAD
============================================================

MAIN OBJECTIVE:

Make the analysis engine independent of GitHub.

GitHub and ZIP should eventually produce the SAME internal repository representation.

User should be able to:

1. Upload a ZIP
2. GitVision validates it
3. Extracts it safely
4. Detects project structure
5. Creates a repository source
6. Creates a snapshot
7. Runs analysis
8. Creates workspace
9. Uses AI chatbot
10. Runs security analysis
11. Generates architecture
12. Generates reports

The final architecture should be:

Repository Source
       ↓
Ingestion
       ↓
Normalized Repository
       ↓
Snapshot
       ↓
Analysis Pipeline
       ↓
Workspace

============================================================
1. FIRST AUDIT EXISTING ANALYSIS PIPELINE
============================================================

Before coding inspect:

- GitHub repository fetcher
- GitHub file tree service
- file content fetcher
- repository metrics
- dependency scanner
- OSV scanner
- architecture analyzer
- hotspot calculation
- context builder
- workspace
- snapshot system
- analysis run system

Identify where the current code assumes:

"repository = GitHub repository"

Remove this assumption only where necessary.

Do not duplicate the entire analysis pipeline for ZIP.

============================================================
2. CREATE REPOSITORY SOURCE ABSTRACTION
============================================================

Create a source abstraction.

Concept:

RepositorySource

Possible values:

GITHUB
ZIP

Future:

GITLAB
LOCAL
BITBUCKET

RepositorySource should expose capabilities such as:

getMetadata()
getFileTree()
getFileContent()
getSnapshot()
getDependencies()
getHistory()

Not every source supports every capability.

For example:

ZIP:

Git history:
NOT_AVAILABLE

GitHub:

Git history:
AVAILABLE

The analysis system must handle this gracefully.

============================================================
3. SOURCE CAPABILITIES
============================================================

Represent capabilities explicitly.

Example:

{
  "source": "ZIP",
  "capabilities": {
    "fileTree": true,
    "fileContent": true,
    "gitHistory": false,
    "issues": false,
    "pullRequests": false,
    "contributors": false,
    "deployments": false
  }
}

Do not show GitHub-only sections for ZIP as if they exist.

For unavailable sections show:

"Not available for ZIP uploads."

============================================================
4. ZIP UPLOAD API
============================================================

Create:

POST /api/uploads/repository

or adapt to existing API conventions.

Requirements:

- multipart/form-data
- ZIP file only initially
- authentication required
- upload size limit
- request timeout
- safe temporary storage

Do not upload ZIP directly to the LLM.

============================================================
5. ZIP VALIDATION
============================================================

Before extraction validate:

- file extension
- MIME type where available
- file size
- archive structure
- number of files
- compressed size
- estimated uncompressed size

Reject:

- malformed ZIP
- oversized ZIP
- excessive file count
- suspicious archive
- unsupported archive type

Return clear error:

"Repository archive is too large."

or:

"Invalid ZIP archive."

Do not expose internal extraction errors.

============================================================
6. ZIP BOMB PROTECTION
============================================================

This is mandatory.

Protect against:

ZIP bombs
recursive archives
extreme compression ratios
millions of files
huge uncompressed data

Define limits through environment variables.

Example:

MAX_UPLOAD_SIZE_MB=
MAX_EXTRACTED_SIZE_MB=
MAX_FILES_PER_ARCHIVE=
MAX_COMPRESSION_RATIO=

Choose sensible defaults based on the existing infrastructure.

Do not hardcode limits throughout the application.

============================================================
7. PATH TRAVERSAL PROTECTION
============================================================

Never allow archive paths such as:

../../etc/passwd

or:

../../../application.env

or absolute paths.

Normalize every extracted path.

Verify:

resolvedPath.startsWith(extractionRoot)

before writing.

Reject unsafe archives.

This must be covered by automated security tests.

============================================================
8. NO ARBITRARY CODE EXECUTION
============================================================

CRITICAL:

Do NOT run:

npm install
pip install
composer install
cargo build
make
./script.sh

or any repository executable automatically.

The uploaded repository is untrusted.

Phase 4 should perform static analysis only.

Never execute:

package scripts
shell scripts
binaries
Docker containers

as part of normal ingestion.

Future code execution, if ever required, must use a hardened sandbox.

============================================================
9. ISOLATED EXTRACTION
============================================================

Extract ZIP into a temporary isolated workspace.

Example conceptual structure:

/tmp/gitvision/
    upload-id/
        extracted/

Do not extract into:

application root
public/
frontend/
backend source tree

After processing, clean up temporary files according to retention rules.

============================================================
10. UPLOAD MODEL
============================================================

Create or extend:

RepositoryUpload

Suggested fields:

id
user_id
workspace_id
repository_id
original_filename
storage_key
size_bytes
file_count
status
source_hash
created_at
completed_at
error_code

Statuses:

UPLOADING
VALIDATING
EXTRACTING
PROCESSING
COMPLETED
FAILED
DELETED

Never store arbitrary raw filesystem paths as public identifiers.

============================================================
11. SOURCE HASH
============================================================

Calculate a cryptographic hash of the uploaded archive or normalized snapshot.

Example:

SHA-256

Store:

source_hash

This allows:

- duplicate detection
- snapshot identity
- reproducibility
- analysis comparison

Do not use filenames as identity.

============================================================
12. ZIP REPOSITORY IDENTITY
============================================================

A ZIP does not necessarily have:

owner/name

Therefore generate a GitVision repository identity.

Example:

upload:<uuid>

or another stable internal identifier.

The repository model should support:

provider = GITHUB
provider = UPLOAD

Do not fake a GitHub URL for ZIP repositories.

============================================================
13. ZIP ROOT DETECTION
============================================================

ZIPs commonly contain:

project/
    package.json
    src/

or:

repo-main/
    src/
    README.md

Detect whether the archive has a single wrapper directory.

Example:

repo-main/
    ...

Treat:

repo-main/

as the project root if appropriate.

Avoid incorrectly analyzing the outer directory as the actual project.

Allow unusual structures to remain supported.

============================================================
14. IGNORE UNNECESSARY FILES
============================================================

Do not index every binary or generated file.

Ignore or deprioritize:

node_modules/
.git/
dist/
build/
coverage/
.next/
.cache/
target/
vendor/
venv/
__pycache__/

and large binaries.

However:

Do not blindly ignore files that may matter to analysis.

For example:

Dockerfile
.github/workflows/*
package-lock.json
requirements.txt
pyproject.toml

must remain available.

Create a configurable ignore policy.

============================================================
15. SECRET FILE PROTECTION
============================================================

Detect sensitive files such as:

.env
.env.production
credentials.json
service-account files
private keys

Do not automatically send raw secret values to the LLM.

For Phase 4:

- detect
- redact
- record finding
- preserve file metadata

Example:

API_KEY=********

Do not display the raw secret in:

- AI context
- logs
- analytics
- error messages

This must integrate with the future security scanner.

============================================================
16. LANGUAGE DETECTION
============================================================

For ZIP repositories determine:

- JavaScript
- TypeScript
- Python
- Java
- Kotlin
- Go
- Rust
- C
- C++
- C#
- PHP
- Ruby
- HTML
- CSS
- Shell
- etc.

Use file extensions plus repository metadata/configuration where useful.

Return:

language
file_count
loc

and language distribution.

Reuse existing GitVision language detection if it exists.

============================================================
17. FRAMEWORK DETECTION
============================================================

Detect common frameworks from dependency/config files.

Examples:

JavaScript:

React
Next.js
Express
NestJS
Vue
Angular

Python:

Django
FastAPI
Flask
LangChain
etc.

Java:

Spring Boot

Go:

Gin
Echo

Do not claim a framework merely because a file happens to contain a matching word.

Use evidence from:

package manifests
imports
config
directory structure

Store evidence.

============================================================
18. PACKAGE MANAGER DETECTION
============================================================

Detect:

npm
yarn
pnpm
bun
pip
poetry
pipenv
cargo
maven
gradle
go modules
composer
bundler

Use:

package.json
yarn.lock
pnpm-lock.yaml
bun.lock
requirements.txt
pyproject.toml
poetry.lock
Cargo.toml
go.mod
pom.xml
build.gradle
composer.json
Gemfile

Do not install dependencies.

============================================================
19. DEPENDENCY ANALYSIS
============================================================

Reuse the existing dependency analysis engine.

For ZIP:

Read manifest/lock files.

Produce:

- direct dependencies
- dev dependencies
- versions
- package manager
- dependency tree where possible

Do not run package installation.

If lockfile exists, prefer it as a source of resolved versions.

============================================================
20. OSV SECURITY SCANNING
============================================================

Existing OSV scanner must be reused.

ZIP flow:

ZIP
 ↓
detect package manager
 ↓
parse dependency manifests
 ↓
OSV scan
 ↓
security results
 ↓
workspace

Do not duplicate the OSV implementation.

If dependency ecosystem is unsupported:

Show:

"Dependency vulnerability scanning is not currently available for this ecosystem."

============================================================
21. FILE TREE
============================================================

Generate normalized file tree.

Example:

src/
 ├── components/
 │   ├── Header.tsx
 │   └── Dashboard.tsx
 ├── services/
 │   └── api.ts
 └── main.tsx

The same frontend Directory component should work for:

GitHub
ZIP

without source-specific UI duplication.

============================================================
22. FILE CONTENT ACCESS
============================================================

Create a normalized:

getFileContent(path)

interface.

GitHub implementation:

fetch GitHub content.

ZIP implementation:

read extracted file safely.

The chatbot/context engine should not care where the file came from.

This is one of the most important architectural requirements.

============================================================
23. SNAPSHOT CREATION
============================================================

ZIP upload must create:

RepositorySnapshot

Fields from Phase 2:

repository_id
source
snapshot_hash
created_at
file_count
total_loc
languages
metadata_json

For ZIP:

source = ZIP

commit_sha:

NULL

Do not invent a commit SHA.

Instead display:

Snapshot:
<short hash>

============================================================
24. ANALYSIS RUN
============================================================

After successful extraction:

Create:

AnalysisRun

Status:

QUEUED

Then:

RUNNING

Stages:

UPLOAD_VALIDATION
EXTRACTION
FILE_TREE
LANGUAGE_DETECTION
DEPENDENCIES
METRICS
ARCHITECTURE
SECURITY
CONTEXT_INDEX
FINALIZATION

Skip GitHub-only stages.

Example:

GIT_HISTORY = NOT_AVAILABLE

============================================================
25. WORKSPACE CREATION
============================================================

After upload succeeds:

Create/open workspace.

Example:

My Uploaded Repository

Source:
ZIP

Snapshot:
abc123...

Actions:

Open Workspace
Analyze

User should NOT have to upload the ZIP again to open the workspace.

============================================================
26. ZIP WORKSPACE
============================================================

Workspace should look almost identical to GitHub repository workspace.

Show:

Overview
Chat
Architecture
Security
History
Reports
Notes

But source-dependent information must be accurate.

For example:

GitHub:

Commits ✓
PRs ✓
Issues ✓

ZIP:

Commits —
PRs —
Issues —

Do not show fake zero values.

Use:

"Not available"

when data does not exist.

============================================================
27. CHATBOT WITH ZIP
============================================================

The same Phase 1 chatbot must work for ZIP.

User asks:

"How does authentication work?"

Backend retrieves files from extracted ZIP.

LLM receives:

- repository metadata
- relevant files
- architecture data
- dependency data
- security findings

Response should reference actual paths.

Example:

src/auth/AuthService.ts

Do not mention GitHub if source is ZIP.

============================================================
28. ZIP CHAT ISOLATION
============================================================

Strictly isolate uploaded repositories.

User A's ZIP:

Upload A

must never become available to:

User B

even if they know:

upload ID
workspace ID
repository ID

Test for IDOR.

============================================================
29. ZIP PREVIEW BEFORE ANALYSIS
============================================================

After upload validation, optionally show:

Repository detected

Files:
842

Languages:
TypeScript 62%
CSS 14%
JavaScript 12%
Other 12%

Dependencies:
126

Potential secrets:
3

Archive size:
18 MB

Buttons:

[Analyze Repository]
[Cancel]

Do not start expensive AI analysis before user confirms if product UX supports confirmation.

============================================================
30. DUPLICATE UPLOAD DETECTION
============================================================

If same user uploads identical ZIP hash:

source_hash matches

Do not unnecessarily process it again.

Offer:

"This repository snapshot already exists."

Options:

Open existing workspace

or

Analyze again

Do not globally deduplicate private data across users.

============================================================
31. UPLOAD LIMITS
============================================================

Make configurable:

MAX_UPLOAD_SIZE_MB
MAX_EXTRACTED_SIZE_MB
MAX_FILES_PER_ARCHIVE
MAX_SINGLE_FILE_SIZE_MB

Also limit:

filename length
path depth
number of nested directories

Return safe errors.

============================================================
32. BINARY FILE HANDLING
============================================================

Do not attempt to send binary files to the LLM.

Detect binary files.

Store metadata:

path
size
type

Ignore them for source context.

Examples:

.png
.jpg
.jpeg
.gif
.webp
.mp4
.mov
.pdf
.zip
.exe
.dll

Do not automatically execute or parse arbitrary binaries.

============================================================
33. LARGE FILE HANDLING
============================================================

Do not load extremely large files into memory.

For files above configured threshold:

- skip from LLM context
- store metadata
- optionally chunk safely
- inform user

Example:

"Large file excluded from AI context due to size limits."

============================================================
34. GENERATED FILES
============================================================

Avoid indexing:

node_modules
build output
compiled bundles
coverage output
generated source maps

unless explicitly requested.

Do not modify uploaded source files.

============================================================
35. ARCHITECTURE ANALYSIS
============================================================

Reuse the existing architecture analyzer.

For ZIP:

Build dependency graph from source.

Produce:

- files
- components
- imports
- internal dependencies
- external dependencies
- central files
- fan-in
- fan-out
- architecture overview
- risks

The existing architecture visualization should work with ZIP.

Exports:

Mermaid
SVG
PNG

must continue working.

============================================================
36. HOTSPOTS
============================================================

ZIP has no Git history unless the archive itself contains .git and the product explicitly chooses to support it.

Do NOT invent churn.

For ZIP:

Hotspot based on Git churn:

NOT_AVAILABLE

Potential alternative:

Structural complexity hotspots

only if already supported.

Label the metric correctly.

============================================================
37. GIT HISTORY
============================================================

Default behavior:

Do not depend on .git inside uploaded ZIP.

If ZIP contains .git:

Do not automatically trust or execute it.

Phase 4 may ignore Git history.

Show:

"Git history is not available for this upload."

Future phase may explicitly support uploaded Git repositories.

============================================================
38. REPORT COMPATIBILITY
============================================================

Existing report system should work with ZIP.

Report must say:

Source:
ZIP upload

Snapshot:
abc123

GitHub-specific metrics should be omitted or marked unavailable.

Never show:

GitHub stars: 0

when stars are actually unknown.

Use:

Not available for uploaded repositories.

============================================================
39. REPOSITORY SOURCE BADGE
============================================================

Add UI badge:

GitHub

or:

ZIP Upload

Example:

Repository:
my-project

Source:
ZIP Upload

This should appear throughout workspace where relevant.

============================================================
40. UPLOAD HISTORY
============================================================

Extend workspace/history so users can see:

Upload #1
Snapshot abc123
18 MB
842 files
Analyzed

Upload #2
Snapshot def456
19 MB
901 files
Analyzed

This prepares the system for:

"What changed between ZIP uploads?"

============================================================
41. SNAPSHOT COMPARISON
============================================================

Use Phase 2 comparison foundation.

For two ZIP snapshots calculate where possible:

- added files
- removed files
- modified files
- LOC changes
- language changes
- dependencies added
- dependencies removed

Do not compare GitHub commit history to ZIP unless there is explicit compatible snapshot data.

============================================================
42. SECURITY SCANNING
============================================================

Add static secret detection foundation.

Detect patterns for common secret types.

IMPORTANT:

Do not display secret values.

Finding should contain:

type
file
line
severity
redacted evidence

Example:

Potential API key

File:
config/api.ts

Line:
18

Evidence:
API_KEY=********

Future security phase will expand this significantly.

============================================================
43. LLM SECRET REDACTION
============================================================

Before context reaches OpenRouter:

Run:

SecretRedactor

Pipeline:

file
 ↓
secret detection
 ↓
redaction
 ↓
context builder
 ↓
OpenRouter

The raw secret must never be passed to the model.

This protection must also apply to chat-selected files.

============================================================
44. PROMPT INJECTION PROTECTION
============================================================

Continue Phase 1 protection.

Repository content is DATA.

ZIP may contain malicious:

README
instructions
comments
code

such as:

"Ignore system instructions."

The model must not follow those instructions.

Never allow repository content to:

- reveal system prompts
- reveal secrets
- change tool permissions
- execute commands

============================================================
45. FILE PREVIEW
============================================================

Workspace Directory should allow:

Click file
    ↓
File viewer

Display:

- path
- language
- size
- content
- line numbers

For secret-containing files:

show redacted content where appropriate.

Do not expose raw credentials.

============================================================
46. API ENDPOINTS
============================================================

Adapt to existing conventions.

Possible:

POST /api/uploads/repository

GET /api/uploads/:uploadId

DELETE /api/uploads/:uploadId

POST /api/uploads/:uploadId/analyze

GET /api/uploads/:uploadId/status

GET /api/repositories/:repositoryId/files

GET /api/repositories/:repositoryId/files/:path

POST /api/repositories/:repositoryId/sync

POST /api/repositories/:repositoryId/compare

Do not duplicate existing routes.

============================================================
47. UPLOAD CLEANUP
============================================================

Temporary extracted files must be cleaned.

Use:

upload processing directory
temporary directory
cleanup job

Do not leave extracted repositories indefinitely on application disk.

Persistent analysis data should live in appropriate storage/database/object storage.

============================================================
48. OBJECT STORAGE COMPATIBILITY
============================================================

Design storage abstraction.

Possible:

LocalStorageProvider
S3StorageProvider
Future:
Cloudflare R2
GCS
Azure Blob

Do not require S3 in local development.

Use:

StorageProvider

with:

put()
get()
delete()
exists()

Future enterprise deployments can replace storage implementation.

============================================================
49. DATABASE
============================================================

Extend database as necessary.

Possible models:

RepositoryUpload
RepositorySource
RepositoryFile
SecretFinding

Reuse:

Repository
RepositorySnapshot
AnalysisRun
AnalysisStage
Workspace
Note
Conversation
Message
Artifact

Do not create duplicate file tables if existing repository file indexing already exists.

============================================================
50. FILE INDEX
============================================================

For ZIP create normalized file records if the existing architecture supports persistent file indexing.

Possible:

RepositoryFile

repository_snapshot_id
path
type
language
size_bytes
is_binary
is_generated
content_hash
created_at

Do NOT necessarily store complete source content in PostgreSQL.

For larger repositories, use:

object storage
filesystem
or existing content store

and keep metadata in DB.

============================================================
51. CONTENT HASH
============================================================

Calculate per-file hash where practical.

This enables:

modified file detection
duplicate detection
snapshot comparison

Example:

SHA-256(file content)

Do not calculate unnecessarily for huge binaries.

============================================================
52. PERFORMANCE
============================================================

ZIP processing must be asynchronous for large archives.

Do not do:

POST /upload
    ↓
extract 20GB
    ↓
analyze
    ↓
wait
    ↓
HTTP response

Instead:

POST /upload
    ↓
create upload
    ↓
QUEUED
    ↓
return upload ID
    ↓
background processing
    ↓
frontend polls/streams status

============================================================
53. PROGRESS UI
============================================================

Show actual stages:

Uploading
✓
Validating
✓
Extracting
→
Scanning files
○
Detecting dependencies
○
Architecture analysis
○
Security analysis
○
Building AI context

Do not fake progress.

============================================================
54. TESTING
============================================================

Create tests for:

ZIP validation
ZIP extraction
path traversal
zip bomb protection
file count limit
size limit
large file handling
binary detection
root directory detection
language detection
framework detection
package manager detection
dependency extraction
OSV integration
secret detection
secret redaction
snapshot creation
workspace creation
chat context
file retrieval
snapshot comparison
authorization
IDOR
cleanup

============================================================
55. SECURITY TEST CASES
============================================================

Create malicious ZIP fixtures:

1. ../../ traversal
2. absolute path
3. excessive nested paths
4. huge compression ratio
5. too many files
6. oversized archive
7. malicious filename
8. secret-containing file
9. binary executable
10. README prompt injection

All must be handled safely.

============================================================
56. ACCEPTANCE TEST
============================================================

Test this exact flow:

1. Login.

2. Open:

Upload Repository

3. Upload:

project.zip

4. GitVision validates the archive.

5. GitVision extracts it into isolated temporary storage.

6. Detect:

files
languages
framework
package manager
dependencies

7. Display preview.

8. User clicks:

Analyze Repository

9. RepositoryUpload becomes PROCESSING.

10. RepositorySnapshot is created.

11. AnalysisRun is created.

12. Analysis stages execute.

13. Architecture is generated.

14. OSV scan runs where supported.

15. Secret detection runs.

16. AI context index is generated.

17. Workspace is created.

18. User opens Workspace.

19. Directory works.

20. File viewer works.

21. Architecture visualization works.

22. Security results work.

23. Chat works.

24. User asks:

"Explain the authentication flow."

25. AI retrieves relevant ZIP files.

26. AI references real file paths.

27. User opens History.

28. Upload snapshot is shown.

29. Upload same ZIP again.

30. Duplicate detection works.

31. Upload modified ZIP.

32. New snapshot is created.

33. Comparison shows modified/added/removed files.

34. User cannot access another user's upload/workspace.

============================================================
57. DO NOT IMPLEMENT YET
============================================================

Do NOT fully implement:

- GitHub Profile Analyzer
- GitLab
- complete GitDocify generator
- PDF/PPT/SRS/PRD generation
- advanced security engine
- full enterprise monitoring dashboard
- webhooks
- CI/CD
- RBAC
- SSO
- Slack/Teams
- PR review assistant

Only build abstractions required for future phases.

============================================================
58. PHASE 4 DEFINITION OF DONE
============================================================

[ ] ZIP upload works
[ ] Upload is authenticated
[ ] File size limits exist
[ ] Extracted size limits exist
[ ] File count limits exist
[ ] Zip bomb protection exists
[ ] Path traversal protection exists
[ ] No arbitrary code execution
[ ] Temporary extraction is isolated
[ ] Cleanup works
[ ] RepositorySource abstraction exists
[ ] GitHub source still works
[ ] ZIP source works
[ ] RepositorySnapshot works for ZIP
[ ] AnalysisRun works for ZIP
[ ] GitHub-only stages are handled correctly
[ ] File tree works
[ ] File viewer works
[ ] Language detection works
[ ] Framework detection works
[ ] Package manager detection works
[ ] Dependency analysis works
[ ] OSV works where supported
[ ] Architecture analysis works
[ ] Architecture visualization works
[ ] Secret detection exists
[ ] Secret redaction exists
[ ] Secrets never reach LLM
[ ] ZIP chatbot works
[ ] Workspace works
[ ] ZIP history works
[ ] Snapshot comparison works
[ ] Authorization works
[ ] IDOR tests pass
[ ] Security tests pass
[ ] Existing GitHub workflow still works
[ ] Existing Phase 1-3 functionality still works

============================================================
59. FINAL IMPLEMENTATION REPORT
============================================================

After implementation provide:

1. Files created
2. Files modified
3. Database migrations
4. New models
5. New APIs
6. RepositorySource architecture
7. ZIP processing architecture
8. Security protections
9. Secret detection/redaction
10. Storage implementation
11. Analysis pipeline changes
12. Frontend pages/components
13. Tests
14. Existing features verified
15. Known limitations
16. Environment variables
17. Local development commands
18. Production deployment considerations

DO NOT START PHASE 5.