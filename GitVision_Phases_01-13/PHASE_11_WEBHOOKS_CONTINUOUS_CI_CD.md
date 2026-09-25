You are working on GitVision, an AI-powered GitHub repository intelligence platform.

============================================================
PHASE 11 — GITHUB WEBHOOKS, CONTINUOUS INTELLIGENCE & CI/CD
============================================================

GOAL

Transform GitVision from primarily on-demand repository analysis
into a continuously updating repository intelligence platform.

GitVision should be able to receive GitHub events, safely process them,
create/update repository snapshots, run appropriate incremental analysis,
and update:

- repository metrics
- architecture
- security
- dependencies
- documentation
- AI context
- artifacts
- history
- reports

This phase must build on all previous phases.

============================================================
EXISTING SYSTEMS — DO NOT REBUILD
============================================================

GitVision already has:

- GitHub OAuth
- GitHub repository access
- Repository Workspace
- Repository Snapshots
- Analysis Runs
- Analysis Stages
- Repository ingestion
- Architecture Intelligence
- Security 2.0
- Documentation Engine
- Artifact Generation
- AI Chat
- OpenRouter abstraction
- Observability
- Background jobs
- SARIF support
- Dependency analysis
- OSV
- Profile Intelligence

Reuse these systems.

Do NOT create parallel implementations.

============================================================
1. CONTINUOUS INTELLIGENCE ARCHITECTURE
============================================================

Implement:

GitHub
  ↓
Webhook Gateway
  ↓
Signature Verification
  ↓
Event Normalization
  ↓
Event Deduplication
  ↓
Repository Resolution
  ↓
Change Classification
  ↓
Analysis Planner
  ↓
Job Queue
  ↓
Incremental Analysis
  ↓
Snapshot
  ↓
Security / Architecture / Docs / Metrics
  ↓
Artifact Refresh
  ↓
Workspace

============================================================
2. WEBHOOK RECEIVER
============================================================

Create a dedicated webhook endpoint.

Follow the existing routing conventions.

Example:

POST /api/webhooks/github

The endpoint should:

1. receive raw request body
2. verify GitHub signature
3. identify event type
4. identify delivery ID
5. normalize event
6. persist event safely
7. acknowledge quickly
8. enqueue processing

Do NOT perform expensive analysis synchronously inside the webhook request.

============================================================
3. GITHUB SIGNATURE VERIFICATION
============================================================

Verify:

X-Hub-Signature-256

using the configured webhook secret.

Use constant-time comparison.

Never accept webhook events without valid signature verification.

Do not log:

webhook secret
raw authorization headers
full payload if it contains sensitive repository information

============================================================
4. WEBHOOK SECRET MANAGEMENT
============================================================

Webhook secrets must be:

- server-side only
- encrypted/securely stored where persisted
- never returned to frontend
- never logged

Support environment configuration for development.

Production should use secure secret storage where available.

============================================================
5. RAW BODY REQUIREMENT
============================================================

GitHub signature verification requires the exact raw request body.

Ensure middleware does not mutate the payload before verification.

If the current Express/application middleware parses JSON globally,
configure webhook route handling appropriately.

============================================================
6. WEBHOOK DELIVERY MODEL
============================================================

Create:

GitHubWebhookEvent

Suggested fields:

- id
- deliveryId
- eventType
- action
- repositoryId
- installationId where applicable
- senderId
- payloadHash
- receivedAt
- verifiedAt
- processingStatus
- processingStartedAt
- processingCompletedAt
- errorCode
- errorMessage
- retryCount

Do NOT persist unnecessary full payload indefinitely.

============================================================
7. WEBHOOK DELIVERY DEDUPLICATION
============================================================

GitHub provides a delivery identifier.

Use:

deliveryId

as an idempotency key.

The same webhook must not create duplicate:

snapshots
analysis runs
security scans
artifact generations

If the delivery already exists:

return successful acknowledgement
without repeating processing.

============================================================
8. EVENT TYPES
============================================================

Initial support:

push
pull_request
pull_request_review
release
create
delete

Optional where useful:

workflow_run
repository

Do not implement every GitHub event.

Focus on repository intelligence.

============================================================
9. PUSH EVENT
============================================================

On push:

identify:

repository
branch/ref
before SHA
after SHA
commits
added files
modified files
removed files

Create an analysis plan.

Do not automatically run every expensive analyzer for every push.

============================================================
10. PULL REQUEST EVENT
============================================================

Support:

opened
synchronize
reopened
closed

For synchronize:

analyze changed files.

For opened:

run appropriate PR analysis.

For closed:

capture merge/close state.

If merged:

update repository history and metrics.

============================================================
11. PULL REQUEST REVIEW
============================================================

Optionally record review events.

Do not automatically generate review comments in this phase.

Use review events for:

history
activity
analysis context

============================================================
12. RELEASE EVENT
============================================================

On release:

capture:

tag
release name
release timestamp
release status

Generate release-related analysis where appropriate.

If release notes generation already exists:

allow continuous release artifact refresh.

============================================================
13. CREATE/DELETE EVENTS
============================================================

Use branch/tag create/delete events to update repository history.

Do not trigger expensive full analysis unless required.

============================================================
14. EVENT NORMALIZATION
============================================================

Create:

NormalizedGitHubEvent

Example:

{
  eventType: "push",
  repositoryId: "...",
  ref: "refs/heads/main",
  beforeSha: "...",
  afterSha: "...",
  changedFiles: [],
  senderId: "...",
  deliveryId: "..."
}

All downstream logic should consume normalized events.

Do not couple the analysis planner directly to raw GitHub payloads.

============================================================
15. REPOSITORY RESOLUTION
============================================================

Resolve repository using stable GitHub identity:

githubRepositoryId

Do NOT identify repositories only by:

owner/name

Owner/name can change.

Use the stable GitHub repository ID as the primary identity.

============================================================
16. WORKSPACE RESOLUTION
============================================================

Find the GitVision workspace associated with the repository.

If repository has no active workspace:

do not automatically create an unrestricted workspace unless product
configuration explicitly enables it.

Record:

NO_WORKSPACE

and safely ignore or queue the event for later association.

============================================================
17. REPOSITORY ACCESS
============================================================

Before processing private repository events:

verify repository/workspace association.

Do not use webhook events as a way to bypass normal GitHub authorization.

If the GitHub token/App installation no longer has access:

mark event:

ACCESS_UNAVAILABLE

Do not fetch private source.

============================================================
18. CHANGE CLASSIFICATION
============================================================

Classify changed files.

Categories:

SOURCE
TEST
CONFIG
DEPENDENCY
SECURITY
DOCUMENTATION
INFRASTRUCTURE
CI
BUILD
GENERATED
UNKNOWN

Example:

package-lock.json

→ DEPENDENCY

.github/workflows/deploy.yml

→ CI

src/auth.ts

→ SOURCE

README.md

→ DOCUMENTATION

============================================================
19. ANALYSIS PLANNER
============================================================

Create:

ContinuousAnalysisPlanner

Input:

NormalizedGitHubEvent
ChangedFiles
PreviousSnapshot

Output:

AnalysisPlan

Example:

{
  "snapshot": true,
  "security": true,
  "architecture": true,
  "documentation": false,
  "dependency": true,
  "profile": false,
  "artifacts": false
}

============================================================
20. CHANGE-BASED ANALYSIS
============================================================

Do not run everything for every push.

Example:

README-only change:

Documentation:
yes

Security:
no

Architecture:
no

Dependency:
no

Source change:

Architecture:
yes

Security:
yes

Documentation:
maybe

Dependency:
no

package-lock change:

Dependency:
yes

Security:
yes

SBOM:
yes

============================================================
21. DEPENDENCY CHANGE
============================================================

Trigger dependency analysis when:

package.json
package-lock.json
yarn.lock
pnpm-lock.yaml
requirements.txt
poetry.lock
Pipfile.lock
go.mod
go.sum
Cargo.toml
Cargo.lock
pom.xml
gradle files
etc.

only for supported ecosystems.

Reuse existing dependency parser.

============================================================
22. SECURITY TRIGGERS
============================================================

Run security analysis when changed files include:

source
dependencies
config
CI
IaC
Docker
environment files

Do not scan binary/generated files unnecessarily.

============================================================
23. SECRET SCANNING
============================================================

For push:

scan changed files.

If historical scanning is configured:

use existing explicit historical scanner.

Never send raw secrets externally.

Never expose detected secrets in webhook logs.

============================================================
24. ARCHITECTURE TRIGGERS
============================================================

Architecture analysis should run when:

source files change
imports change
configuration affecting architecture changes
dependencies change
service boundaries change

Avoid full architecture rebuild when only:

README
docs
images

change.

============================================================
25. DOCUMENTATION TRIGGERS
============================================================

Trigger documentation refresh when:

public API changes
README changes
source architecture changes
configuration changes
database schema changes
deployment configuration changes

Do not regenerate all documentation for every commit.

============================================================
26. ARTIFACT TRIGGERS
============================================================

Existing artifacts should NOT automatically regenerate every time.

Use artifact policies.

Example:

Security Report:
refresh on security changes

Architecture Report:
refresh on architecture changes

README:
refresh on documentation changes

Executive Report:
refresh only when explicitly configured

============================================================
27. ARTIFACT REFRESH POLICY
============================================================

Add:

ArtifactRefreshPolicy

Fields:

- artifactType
- enabled
- triggerTypes
- autoRegenerate
- maxFrequency

Default:

autoRegenerate = false

unless explicitly enabled.

This prevents unexpected AI costs.

============================================================
28. AI COST PROTECTION
============================================================

Continuous analysis must not unexpectedly generate huge LLM bills.

Default automatic webhook processing:

NO unnecessary LLM calls.

Prefer:

deterministic analysis
structured metrics
existing summaries
cached context

Only invoke AI when:

required
explicitly configured
or an artifact policy requires it.

============================================================
29. DEBOUNCING
============================================================

Multiple commits may arrive rapidly.

Example:

10 pushes in 2 minutes.

Do not start 10 full analyses.

Implement event/job debouncing.

Possible strategy:

wait configurable period
coalesce compatible push events
analyze latest SHA

Example:

push A
push B
push C

→ one analysis for C

Keep historical GitHub events for audit/history.

============================================================
30. DEBOUNCE CONFIGURATION
============================================================

Example:

continuousAnalysis:
  enabled: true
  debounceSeconds: 30

Do not hardcode if configuration system already exists.

============================================================
31. COALESCING SAFETY
============================================================

Never coalesce events across:

different repositories
different branches when branch-specific state matters
different workspaces

Only coalesce compatible events.

============================================================
32. BRANCH HANDLING
============================================================

Repository snapshots should record:

branch
commit SHA
parent SHA

Default continuous analysis branch:

default branch

PR analysis:

PR head SHA

Do not accidentally replace main branch snapshot with a PR snapshot.

============================================================
33. SNAPSHOT TYPES
============================================================

Support distinction:

DEFAULT_BRANCH
BRANCH
PULL_REQUEST
TAG
RELEASE

This must remain compatible with existing RepositorySnapshot.

============================================================
34. PR SNAPSHOT
============================================================

For pull requests:

create analysis context:

base SHA
head SHA

Example:

PR #42

Base:
main@abc123

Head:
feature@def456

Changed files:

...

Do not treat a PR snapshot as the main branch snapshot.

============================================================
35. PR SECURITY ANALYSIS
============================================================

Run incremental security checks on PR changes.

Show:

New findings
Resolved findings
Unchanged findings

relative to PR base.

Do not automatically block the PR in this phase.

============================================================
36. PR ARCHITECTURE DIFF
============================================================

Use Phase 7 architecture diff.

Show:

new dependency
removed dependency
new component
changed component
new cycle
changed coupling

Only report changes supported by analysis.

============================================================
37. PR DOCUMENTATION IMPACT
============================================================

Detect:

API changes
configuration changes
public component changes

Then identify documentation that may be stale.

Do not automatically rewrite docs unless configured.

============================================================
38. CONTINUOUS SNAPSHOT CREATION
============================================================

After successful event processing:

create RepositorySnapshot.

Snapshot should include:

commit SHA
branch
source
analysis status
timestamp

Do not create duplicate snapshot for same:

repository
branch
commit SHA
snapshot type

============================================================
39. SNAPSHOT IDEMPOTENCY
============================================================

Unique identity:

repositoryId
commitSha
branch
snapshotType

If already analyzed:

reuse.

============================================================
40. PARTIAL SNAPSHOT
============================================================

If some analysis stages fail:

snapshot can still exist.

Example:

Security:
success

Architecture:
success

Documentation:
failed

Snapshot status:

PARTIAL

Do not delete successful analysis.

============================================================
41. ANALYSIS RUN
============================================================

Reuse existing AnalysisRun.

Store:

trigger:

MANUAL
WEBHOOK
PR
RELEASE
CI

eventId

snapshotId

commitSha

branch

============================================================
42. ANALYSIS STAGES
============================================================

Stages may include:

INGESTION
CHANGE_DETECTION
DEPENDENCY
SECURITY
ARCHITECTURE
DOCUMENTATION
METRICS
ARTIFACT_REFRESH

Each:

queued
running
completed
failed
skipped

============================================================
43. SKIPPED STAGES
============================================================

If a stage is not required:

status:

SKIPPED

Reason:

"No dependency files changed."

This is important for diagnostics.

============================================================
44. WEBHOOK PROCESSING QUEUE
============================================================

Webhook endpoint should enqueue:

WebhookProcessingJob

Worker then:

verify persisted event
resolve repository
build analysis plan
enqueue analysis

Do not do expensive work in HTTP request.

============================================================
45. QUEUE IDEMPOTENCY
============================================================

Use deterministic job keys.

Example:

repositoryId
commitSha
analysisType

Prevent duplicate jobs.

Reuse Phase 10 observability.

============================================================
46. RETRIES
============================================================

Retry transient failures:

GitHub timeout
OSV timeout
LLM temporary error
storage transient error

Do not retry:

invalid signature
invalid repository
permission denied
malformed event

Use exponential backoff.

============================================================
47. DEAD LETTER
============================================================

If a webhook repeatedly fails:

move to:

DEAD_LETTER

Admin should be able to inspect:

event ID
type
repository
error
attempt count

Do not expose raw sensitive payloads.

============================================================
48. WEBHOOK REPLAY
============================================================

Admin should be able to safely replay a failed event.

Replay must remain idempotent.

Do not allow arbitrary users to replay events.

============================================================
49. WEBHOOK HISTORY UI
============================================================

Admin:

Webhooks

Columns:

Delivery
Event
Repository
Received
Status
Duration
Retries

Statuses:

RECEIVED
PROCESSING
PROCESSED
IGNORED
FAILED
DEAD_LETTER

============================================================
50. CONTINUOUS ANALYSIS UI
============================================================

Repository Workspace:

Continuous Analysis

Status:

Enabled

Last event:
2 minutes ago

Last analyzed:
commit abc123

Next:
none

Configuration:

Enable automatic analysis
Debounce
Default branch
Security
Architecture
Documentation
Artifact refresh

============================================================
51. REPOSITORY SYNC STATUS
============================================================

Display:

Last GitHub event
Last snapshot
Last successful analysis
Last failed analysis
Current commit

Example:

GitHub:
Connected

Last Push:
2m ago

Last Analysis:
3m ago

Status:
Healthy

============================================================
52. ANALYSIS HISTORY
============================================================

History should distinguish:

Manual
Webhook
Pull Request
Release
CI

Example:

Commit abc123
Trigger: Webhook
Status: Completed
Duration: 42s

============================================================
53. CONTINUOUS SECURITY
============================================================

When continuous analysis detects a new security finding:

add it to existing SecurityFinding.

Use fingerprinting.

Do not create duplicates.

Security diff should show:

NEW

and previous snapshot comparison.

============================================================
54. CONTINUOUS ARCHITECTURE
============================================================

When architecture changes:

create new architecture analysis associated with snapshot.

Phase 7 architecture history should update automatically.

============================================================
55. CONTINUOUS DOCUMENTATION
============================================================

When documentation-triggering source changes:

mark affected documentation as:

STALE

if auto-regeneration is disabled.

This is important.

Do not silently regenerate.

Example:

Architecture Documentation

Status:
STALE

Reason:
3 architecture files changed.

Action:

[Regenerate]

============================================================
56. ARTIFACT STALENESS
============================================================

Artifact should have:

snapshotId

When repository advances:

older artifact becomes:

OUTDATED

unless it is historical.

Do not overwrite historical artifacts.

============================================================
57. STALE ARTIFACT UI
============================================================

Show:

Architecture Report
Snapshot:
abc123

Current repository:
def456

Status:
OUTDATED

[Generate New Version]

============================================================
58. CI/CD INTEGRATION
============================================================

Implement CI-compatible interfaces.

Primary initial mechanism:

SARIF

GitVision should be able to produce SARIF that external CI systems
can consume.

Do not implement deep vendor-specific CI integration first.

============================================================
59. GITHUB ACTIONS FOUNDATION
============================================================

Provide documentation and configuration for:

GitVision CI analysis

Possible workflow:

checkout
 ↓
GitVision CLI/API
 ↓
analysis
 ↓
SARIF
 ↓
upload-artifact / code scanning integration

Do not require repository code execution beyond what the existing
GitHub Actions runner naturally performs.

============================================================
60. GITVISION CLI FOUNDATION
============================================================

If the architecture supports a CLI:

create foundation for:

gitvision analyze
gitvision security
gitvision architecture
gitvision sbom

Do not build a huge CLI.

Minimum useful interface:

analyze repository
output SARIF
output JSON
return appropriate exit code

============================================================
61. CI EXIT CODES
============================================================

Define deterministic exit behavior.

Example:

0:
analysis completed and no configured blocking findings

1:
configured blocking finding detected

2:
analysis/tool failure

Document this clearly.

Do not make all findings automatically block CI.

============================================================
62. CI POLICY
============================================================

Support configuration:

security:
  failOn:
    - CRITICAL

Optional:

HIGH

Default should be conservative.

Do not unexpectedly break existing CI.

============================================================
63. SARIF CI OUTPUT
============================================================

CI output must include:

ruleId
severity
message
location
fingerprint

No raw secrets.

============================================================
64. PR ANALYSIS API
============================================================

If existing API architecture allows:

POST /api/repositories/:id/pull-request-analysis

Input:

pullRequestNumber

or use event-triggered analysis.

Prefer event-driven processing for GitHub.

============================================================
65. CI AUTHENTICATION
============================================================

Do not expose GitVision admin secrets in repository code.

If CI requires authentication:

support scoped project/repository token architecture.

Do not use user OAuth tokens directly in public workflow configuration.

If repository-scoped tokens are not yet safe:

document the limitation and provide a server-side API mechanism.

============================================================
66. GITHUB APP FOUNDATION
============================================================

Build architecture compatible with GitHub App installation.

Models may include:

GitHubInstallation
GitHubInstallationRepository

Store:

installationId
accountId
repositoryId
permissions
createdAt
updatedAt

Do not implement full GitHub App installation UI if it is too large
for this phase.

============================================================
67. GITHUB APP VS OAUTH
============================================================

Keep separate concepts:

OAuth:
user identity and user-authorized repository access.

GitHub App:
installation-level repository automation.

Do not mix credentials.

============================================================
68. INSTALLATION ACCESS
============================================================

For webhook-driven private repository analysis:

prefer GitHub App installation credentials where available.

OAuth remains supported for existing user flows.

Do not expose installation tokens.

============================================================
69. WEBHOOK INSTALLATION EVENTS
============================================================

Where GitHub App support exists, prepare for:

installation
installation_repositories

events.

Use them to synchronize repository access.

============================================================
70. PERMISSION CHANGES
============================================================

If GitHub App installation loses repository access:

mark repository access:

REVOKED

Do not continue fetching source.

============================================================
71. WEBHOOK SECURITY
============================================================

Threat model:

spoofed event
replay
duplicate event
stolen webhook secret
malformed payload
oversized payload
DoS

Mitigations:

signature verification
delivery ID idempotency
payload limits
timeouts
rate limiting
safe parsing
queue isolation

============================================================
72. PAYLOAD LIMIT
============================================================

Set safe maximum webhook payload size.

Reject oversized requests.

Do not allocate unbounded memory.

============================================================
73. EVENT VALIDATION
============================================================

Validate required fields.

For push:

repository.id
after
ref

For pull request:

repository.id
pull_request.number
pull_request.head.sha

If invalid:

mark malformed.

============================================================
74. WEBHOOK RATE LIMITING
============================================================

Protect endpoint against abuse.

But do not accidentally block legitimate GitHub bursts.

Use:

IP/network controls where available
signature verification
delivery dedupe
queue backpressure

============================================================
75. BACKPRESSURE
============================================================

If analysis queue is overloaded:

webhook should still acknowledge valid events after durable persistence.

Do not run expensive analysis inline.

Queue state should show:

BACKLOGGED

Admin can diagnose.

============================================================
76. QUEUE PRIORITY
============================================================

Potential priorities:

P0:
manual user-triggered

P1:
PR/security

P2:
push analysis

P3:
background documentation/artifact refresh

Do not starve lower-priority jobs indefinitely.

============================================================
77. PRIORITY CONFIGURATION
============================================================

Keep queue priority configurable.

Do not hardcode business-critical priorities throughout code.

============================================================
78. CONTINUOUS ANALYSIS COST CONTROL
============================================================

Implement:

debounce
coalescing
incremental analysis
cache
artifact refresh policies
LLM call minimization

Continuous mode must be economically predictable.

============================================================
79. CONTINUOUS ANALYSIS SETTINGS
============================================================

Workspace/repository configuration:

continuousAnalysis.enabled

analyzePushes

analyzePullRequests

analyzeReleases

securityEnabled

architectureEnabled

documentationEnabled

autoRefreshArtifacts

debounceSeconds

Do not expose unsupported settings.

============================================================
80. DEFAULTS
============================================================

Recommended defaults:

continuous analysis:
disabled until explicitly enabled

push:
enabled when continuous mode enabled

PR:
enabled

security:
enabled

architecture:
enabled

documentation:
enabled but mark stale unless auto-refresh configured

artifacts:
manual refresh

This prevents unexpected expensive generation.

============================================================
81. ANALYSIS POLICY
============================================================

Allow a policy layer.

Example:

AnalysisPolicy

{
  security: true,
  architecture: true,
  documentation: "STALE_ONLY",
  artifacts: "MANUAL"
}

Use structured values rather than arbitrary booleans where needed.

============================================================
82. EVENT TO ANALYSIS MATRIX
============================================================

Create deterministic matrix.

Example:

PUSH source:
security ✓
architecture ✓
metrics ✓
documentation stale
artifacts unchanged

PUSH dependency:
security ✓
architecture ✓
SBOM ✓
documentation stale

PULL REQUEST:
security diff ✓
architecture diff ✓
metrics ✓

RELEASE:
release history ✓
changelog ✓
optional artifacts

============================================================
83. DOCUMENTATION STALENESS DETECTION
============================================================

Track documentation sources.

If source changes:

determine impacted documentation artifacts.

Example:

src/auth/*
changes

→ authentication documentation stale

Do not mark unrelated docs stale.

============================================================
84. ARTIFACT STALENESS DETECTION
============================================================

Track ArtifactSource.

If source evidence changes:

artifact becomes:

OUTDATED

This should be deterministic.

============================================================
85. SECURITY BASELINE + CONTINUOUS SCAN
============================================================

Existing security baseline must work with continuous scans.

New finding:

OPEN

Existing accepted finding:

still accepted

Resolved finding:

RESOLVED

Do not reset status on every scan.

============================================================
86. ARCHITECTURE HISTORY
============================================================

Every continuous architecture analysis should be associated with:

snapshot
commit
branch

Allow timeline:

commit A
commit B
commit C

with architecture changes.

============================================================
87. CHAT CONTEXT UPDATE
============================================================

When new snapshot completes:

invalidate or refresh repository AI context.

Do not continue using stale repository context silently.

Chat should know:

Current snapshot:
abc123

If historical question:

use requested snapshot.

============================================================
88. CONTEXT CACHE INVALIDATION
============================================================

Invalidate caches when:

source changes
dependency changes
architecture changes
security changes

Do not invalidate unrelated caches unnecessarily.

============================================================
89. SEARCH INDEX UPDATE
============================================================

If repository file search/index exists:

update incrementally where possible.

Changed files:
reindex

Deleted files:
remove

Unchanged files:
reuse

============================================================
90. ANALYSIS RESULT NOTIFICATION FOUNDATION
============================================================

Create internal event:

AnalysisCompleted

Payload:

repository
snapshot
analysisRun
status
newSecurityFindings
architectureChanged
documentationStale

Do not implement Slack/email notifications yet.

============================================================
91. AUDIT
============================================================

Record:

webhook received
webhook verified
analysis triggered
analysis skipped
analysis completed
artifact marked stale
artifact regenerated

Reuse Phase 10 audit infrastructure.

============================================================
92. OBSERVABILITY
============================================================

Integrate Phase 10.

Track:

webhook count
verification failures
duplicate deliveries
processing duration
queue delay
analysis duration
coalesced events
skipped stages
failed stages
dead letters

Metrics:

webhook.success
webhook.invalid_signature
webhook.duplicate
webhook.processing_duration
analysis.triggered
analysis.coalesced
analysis.failed

============================================================
93. WEBHOOK DASHBOARD
============================================================

Admin:

Webhook Events

Metrics:

Received
Verified
Failed
Duplicate
Processing
Dead Letter

Chart:

events/hour

Table:

Delivery ID
Event
Repository
Received
Status
Duration

============================================================
94. CONTINUOUS ANALYSIS DASHBOARD
============================================================

Show:

Repositories with continuous analysis enabled

Last event
Last snapshot
Last analysis
Failed analyses
Queue backlog

============================================================
95. REPOSITORY PAGE
============================================================

Add:

Continuous Analysis

Status:

ON/OFF

Last synchronized:

timestamp

Current commit:

SHA

Last analysis:

status

Settings:

[Configure]

============================================================
96. PULL REQUEST EXPERIENCE
============================================================

Workspace should support:

PR Analysis

Display:

Changed Files
Security Changes
Architecture Changes
Dependency Changes
Documentation Impact

No automatic PR comment in this phase.

============================================================
97. PR SECURITY SUMMARY
============================================================

Example:

PR #42

Security:

2 new findings
1 resolved
15 unchanged

New:

HIGH
Dependency vulnerability

MEDIUM
SAST finding

============================================================
98. PR ARCHITECTURE SUMMARY
============================================================

Example:

Architecture:

3 files changed

1 new dependency

1 component boundary changed

0 new cycles

All claims must come from architecture analysis.

============================================================
99. PR DEPENDENCY SUMMARY
============================================================

Display:

Added
Removed
Updated

Example:

Added:
package-x 1.2.0

Removed:
package-y

Updated:
package-z 2.1 → 2.2

============================================================
100. RELEASE INTELLIGENCE
============================================================

For release events:

create release snapshot

link:

tag
commit
release metadata

Generate optional:

release notes artifact

only if configured.

============================================================
101. CI RESULT INGESTION
============================================================

If practical:

support receiving external SARIF from CI.

Example:

POST /api/security/sarif

Associate with:

repository
commit
branch
PR

Normalize into existing SecurityFinding model.

Do not create a separate security system.

============================================================
102. SARIF SOURCE
============================================================

Store:

source:
EXTERNAL_CI

tool:

Semgrep
CodeQL
Trivy

if provided.

Never execute imported SARIF.

============================================================
103. CI FINDING LIFECYCLE
============================================================

External CI findings should participate in:

fingerprinting
status
snapshot
security diff

Do not duplicate GitVision-native findings unnecessarily.

============================================================
104. CLI OUTPUT
============================================================

If CLI is implemented:

support:

--format sarif
--format json

Exit codes:

0 success/no blocking findings
1 blocking findings
2 tool error

Document behavior.

============================================================
105. SECURITY OF CLI
============================================================

CLI must never print:

tokens
raw secrets

When secret findings exist:

show:

Secret detected at file:line

not secret content.

============================================================
106. TESTING — WEBHOOK
============================================================

Test:

valid signature
invalid signature
missing signature
replayed delivery
duplicate delivery
malformed payload
oversized payload
unknown event
push
PR
release
create
delete

============================================================
107. TESTING — ANALYSIS
============================================================

Test:

source change
dependency change
README-only change
CI change
IaC change
deleted file
renamed file
large push
multiple pushes
rapid pushes
coalescing
branch separation
PR snapshot
release snapshot

============================================================
108. TESTING — SECURITY
============================================================

Test:

new vulnerability
resolved vulnerability
new secret
false positive
SAST change
SBOM change

Verify no raw secret leakage.

============================================================
109. TESTING — ARCHITECTURE
============================================================

Test:

new dependency
removed dependency
new component
cycle
file rename
component boundary change

============================================================
110. TESTING — DOCUMENTATION
============================================================

Test:

source changes
documentation becomes stale
unrelated change does not stale unrelated docs
manual regeneration

============================================================
111. TESTING — ARTIFACTS
============================================================

Test:

artifact remains historical
artifact becomes outdated
auto-refresh policy
manual refresh
failed refresh
snapshot association

============================================================
112. TESTING — SECURITY
============================================================

Test:

webhook secret not logged
GitHub tokens not logged
private source not logged
raw AI context not logged

============================================================
113. TESTING — AUTHORIZATION
============================================================

Test:

user A cannot process/access user B private repository

user A cannot access user B webhook

normal user cannot access admin webhook dashboard

installation access is respected

============================================================
114. FAILURE HANDLING
============================================================

If:

GitHub unavailable

→ webhook persisted
→ analysis queued/retry

If:

OSV unavailable

→ security stage retry/partial

If:

LLM unavailable

→ deterministic analysis still completes

If:

artifact generation fails

→ repository snapshot remains valid

Never make repository ingestion dependent on successful AI generation.

============================================================
115. PARTIAL ANALYSIS
============================================================

Example:

Snapshot:
abc123

Security:
COMPLETE

Architecture:
COMPLETE

Documentation:
FAILED

Artifacts:
SKIPPED

Overall:
PARTIAL

Dashboard must explain why.

============================================================
116. SECURITY PRINCIPLE
============================================================

GitHub webhook events are untrusted external input.

Treat:

event payload
commit metadata
branch names
repository names
commit messages

as untrusted data.

Never directly execute repository content.

============================================================
117. PROMPT INJECTION
============================================================

Commit messages, README changes, source comments, and repository files
can contain prompt injection.

Webhook-triggered AI jobs must use existing Phase 1/6 prompt injection
defenses.

Do not allow repository text to override system instructions.

============================================================
118. NO AUTOMATIC CODE EXECUTION
============================================================

Webhook analysis must never execute:

npm scripts
shell scripts
Dockerfiles
Terraform
GitHub Actions
binaries
repository programs

Static analysis only.

============================================================
119. RESOURCE LIMITS
============================================================

Protect workers from malicious repositories.

Limits:

max files
max file size
max total analyzed bytes
max dependency count
max graph size
max LLM context
max analysis duration

Respect existing repository ingestion safeguards.

============================================================
120. TIMEOUTS
============================================================

Every external operation should have a timeout.

GitHub
OSV
LLM
storage
database
queue

No unbounded requests.

============================================================
121. CONTINUOUS ANALYSIS RETENTION
============================================================

Webhook events:

short/medium retention

Repository snapshots:

existing retention policy

Analysis runs:

existing retention

Do not retain every raw webhook payload forever.

============================================================
122. CONFIGURATION
============================================================

Environment/config:

GITHUB_WEBHOOK_SECRET

CONTINUOUS_ANALYSIS_ENABLED

WEBHOOK_MAX_PAYLOAD_SIZE

WEBHOOK_DEBOUNCE_SECONDS

WEBHOOK_RATE_LIMIT

ANALYSIS_JOB_TIMEOUT

Do not hardcode secrets.

============================================================
123. DOCUMENTATION
============================================================

Create:

docs/webhooks.md
docs/continuous-analysis.md
docs/ci-integration.md

Document:

setup
security
signature verification
event handling
analysis triggers
debouncing
CI
SARIF
failure recovery

============================================================
124. DEFINITION OF DONE
============================================================

[ ] GitHub webhook endpoint exists

[ ] Signature verification works

[ ] Raw body handling works

[ ] Delivery IDs are persisted

[ ] Duplicate delivery protection works

[ ] Webhook event model exists

[ ] Event normalization exists

[ ] Repository resolution works

[ ] Workspace resolution works

[ ] Access checks work

[ ] Push events work

[ ] Pull request events work

[ ] Release events work

[ ] Create/delete events work where implemented

[ ] Analysis planner exists

[ ] Change classification works

[ ] Incremental security works

[ ] Incremental architecture works

[ ] Dependency-triggered analysis works

[ ] Documentation staleness works

[ ] Artifact staleness works

[ ] Snapshot creation works

[ ] Snapshot idempotency works

[ ] PR snapshots are isolated from main

[ ] Debouncing works

[ ] Event coalescing works

[ ] Queue integration works

[ ] Retry works

[ ] Dead-letter handling works

[ ] Webhook replay works

[ ] Continuous analysis settings exist

[ ] AI cost protection exists

[ ] GitHub App compatibility foundation exists

[ ] SARIF CI integration works

[ ] CI exit-code semantics documented

[ ] Webhook dashboard exists

[ ] Continuous analysis dashboard exists

[ ] PR analysis summary exists

[ ] Phase 10 observability integration exists

[ ] Security protections exist

[ ] No arbitrary code execution

[ ] Existing GitVision features remain intact

[ ] All tests pass

============================================================
125. DO NOT IMPLEMENT IN THIS PHASE
============================================================

Do NOT implement:

- automatic PR comments
- automatic PR approvals
- automatic code fixes
- automatic commits
- autonomous remediation
- Slack integration
- Microsoft Teams integration
- email notification system
- full GitHub App installation marketplace flow
- enterprise RBAC
- SSO/SAML
- billing
- multi-organization management
- cloud deployment scanning
- runtime application execution

These belong to later phases.

============================================================
126. FINAL VERIFICATION
============================================================

Run:

1. Existing test suite
2. Webhook signature tests
3. Duplicate delivery tests
4. Push event tests
5. PR event tests
6. Release event tests
7. Event normalization tests
8. Analysis planner tests
9. Debounce tests
10. Coalescing tests
11. Snapshot tests
12. Security incremental scan
13. Architecture incremental scan
14. Documentation staleness test
15. Artifact staleness test
16. SARIF CI test
17. Queue retry test
18. Dead-letter test
19. Replay test
20. GitHub access test
21. Admin authorization test
22. Secret leakage test
23. Prompt injection test
24. Resource limit test
25. Large repository test
26. Existing chatbot test
27. Existing OSV test
28. Existing architecture test
29. Existing documentation test
30. Existing artifact generation test

At completion report:

A. Files created
B. Files modified
C. Database migrations
D. Webhook architecture
E. Event types
F. Analysis planner
G. Queue jobs
H. Snapshot behavior
I. CI/SARIF integration
J. GitHub App foundation
K. UI changes
L. API endpoints
M. Tests
N. Security controls
O. Known limitations
P. Manual verification
Q. Architectural decisions

Do not rewrite unrelated code.

Do not remove existing functionality.

Prefer incremental, composable changes.