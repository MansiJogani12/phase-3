You are working on GitVision, an AI-powered GitHub repository intelligence
platform.

============================================================
PHASE 13 — ENTERPRISE SECURITY, SCALE & PRODUCTION HARDENING
============================================================

GOAL

Harden GitVision for serious production and enterprise workloads.

This phase should improve:

- security
- tenant isolation
- identity
- secrets management
- encryption
- compliance foundations
- data retention
- disaster recovery
- database reliability
- queue reliability
- horizontal scaling
- worker scaling
- observability
- abuse protection
- production deployment
- operational recovery

GitVision already contains the product functionality from Phases 1–12.

Do NOT rebuild those systems.

This phase is primarily about making the existing system:

secure
reliable
scalable
observable
recoverable
operationally mature

============================================================
EXISTING SYSTEMS — PRESERVE
============================================================

Existing:

- AI Chat
- OpenRouter abstraction
- Repository Workspace
- Repository Snapshots
- GitHub OAuth
- GitHub App foundation
- ZIP ingestion
- GitHub ingestion
- Profile Intelligence
- Documentation Engine
- Architecture Intelligence
- Security 2.0
- SBOM
- SARIF
- Artifact Engine
- PDF/PPT generation
- Webhooks
- Continuous Analysis
- CI integration
- Organizations
- Teams
- RBAC
- Audit Logs
- Admin Dashboard
- Observability

must remain functional.

Do not replace working implementations simply for architectural purity.

============================================================
1. SECURITY ARCHITECTURE REVIEW
============================================================

Before implementing changes:

audit the entire system.

Review:

authentication
authorization
OAuth
GitHub tokens
GitHub App credentials
webhooks
repository ingestion
ZIP uploads
AI prompts
AI outputs
LLM provider calls
artifact exports
file viewer
search
vector indexes
queues
background workers
admin APIs
organization APIs
audit logs
storage
database
cache

Produce:

SECURITY_ARCHITECTURE.md

Document:

threat
risk
mitigation
remaining limitation

Do not invent compliance certifications.

============================================================
2. THREAT MODEL
============================================================

Document threats:

- account takeover
- stolen OAuth credential
- stolen GitHub token
- stolen GitHub App credential
- webhook spoofing
- replay
- IDOR
- cross-tenant access
- malicious repository
- malicious ZIP
- prompt injection
- malicious artifact content
- SSRF
- path traversal
- archive bombs
- oversized files
- queue abuse
- LLM abuse
- data exfiltration
- secret leakage
- log leakage
- database compromise
- storage compromise
- admin compromise
- denial of service

Map each to mitigation.

============================================================
3. SECURITY PRINCIPLE
============================================================

Assume:

Repository content is untrusted.

GitHub metadata is untrusted.

Commit messages are untrusted.

README files are untrusted.

Source comments are untrusted.

Webhook payloads are untrusted.

AI output is untrusted.

Never treat repository content as executable instructions.

============================================================
4. ZERO TRUST RESOURCE ACCESS
============================================================

Every protected resource must verify authorization.

Examples:

repository
workspace
organization
snapshot
file
analysis
security finding
artifact
conversation
note
audit event

Resource ID alone must never grant access.

============================================================
5. CENTRAL AUTHORIZATION
============================================================

Ensure all major API routes use centralized:

AuthorizationService

Do not duplicate inconsistent permission logic.

Audit for:

controllers
services
background workers
exports
download endpoints
search
AI retrieval

============================================================
6. BACKGROUND JOB AUTHORIZATION
============================================================

Every queued job must contain scope:

organizationId
workspaceId
repositoryId
snapshotId
analysisRunId

Workers must validate resource ownership/scope before processing.

Do not trust stale job authorization forever.

============================================================
7. ENCRYPTION AT REST
============================================================

Identify sensitive fields:

GitHub OAuth credentials
GitHub App credentials
integration secrets
webhook secrets
API credentials
invitation tokens
repository connection secrets

Encrypt sensitive credentials at rest.

Never store credentials as ordinary plaintext columns.

============================================================
8. KEY MANAGEMENT ABSTRACTION
============================================================

Create:

SecretStore

Interface:

encrypt()
decrypt()
rotate()
delete()

Development:

environment-based implementation

Production:

KMS/secret-manager compatible implementation

Do not hard-code cloud provider APIs throughout application code.

============================================================
9. KEY ROTATION
============================================================

Design for credential rotation.

Support:

old key
new key
re-encryption

without requiring full application downtime.

============================================================
10. APPLICATION SECRETS
============================================================

Move production secrets toward secret-manager compatible configuration.

Examples:

DATABASE_URL
OPENROUTER_API_KEY
GITHUB_APP_PRIVATE_KEY
GITHUB_WEBHOOK_SECRET
SESSION_SECRET

Never commit production secrets.

============================================================
11. SECRET SCANNING
============================================================

Run repository secret detection before external AI calls.

Existing Phase 8 scanner should be reused.

If secret detected:

redact before:

LLM prompt
logs
telemetry
artifact
export

============================================================
12. AI DATA POLICY
============================================================

Create explicit AI data handling policy.

For every LLM request track internally:

provider
model
operation
repository
workspace
organization
data classification

Do not store raw prompts/responses by default.

============================================================
13. PRIVATE REPOSITORY PROTECTION
============================================================

For private repositories:

do not send source to arbitrary external providers unless:

provider is configured
policy permits it
user/org settings permit it

Create foundation:

AIDataPolicy

Example:

PRIVATE_REPO:
allowedProviders:
  - configured-provider

PUBLIC_REPO:
allowedProviders:
  - configured-provider

Do not silently send enterprise source to unapproved models.

============================================================
14. AI PROVIDER ALLOWLIST
============================================================

Organization administrators should eventually be able to configure:

allowed AI providers
allowed models

For this phase implement the backend policy foundation.

Do not trust frontend model selection.

============================================================
15. OPENROUTER POLICY
============================================================

OpenRouter remains supported through existing provider abstraction.

Do not bypass:

LLMProvider

for direct model calls.

All providers must use common security/telemetry policies.

============================================================
16. PROMPT INJECTION DEFENSE
============================================================

Continue existing defenses.

Treat repository text as data.

Prompt structure:

SYSTEM INSTRUCTIONS
↓
TASK
↓
TRUSTED APPLICATION CONTEXT
↓
UNTRUSTED REPOSITORY CONTENT

Never allow repository content to redefine system instructions.

============================================================
17. TOOL CALL SECURITY
============================================================

If AI tools exist:

every tool must have:

explicit schema
authorization
input validation
resource scoping
timeout
rate limit

AI must not be able to:

delete repositories
change permissions
retrieve arbitrary users' data
access secrets

without explicit controlled application action.

============================================================
18. SSRF PROTECTION
============================================================

Audit all server-side URL fetching.

Potential sources:

GitHub URLs
external documentation
webhook payload URLs
artifact references

Block:

localhost
127.0.0.1
private IP ranges
link-local
metadata endpoints

unless explicitly required and safely controlled.

============================================================
19. URL ALLOWLIST
============================================================

Where possible:

allow only known provider domains.

Example:

github.com
api.github.com

Do not blindly fetch arbitrary URLs from repository files.

============================================================
20. ZIP SECURITY
============================================================

Reuse Phase 4 ZIP safeguards.

Verify:

path traversal
absolute paths
symlinks
archive bombs
compression ratio
max files
max uncompressed size
max file size

before extraction.

============================================================
21. ZIP SYMLINK SECURITY
============================================================

Do not allow extracted symlinks to escape extraction root.

Validate resolved path.

============================================================
22. FILE SYSTEM ISOLATION
============================================================

Repository extraction must happen in isolated temporary directories.

Cleanup after analysis.

Never extract user ZIPs into shared persistent application directories.

============================================================
23. NO CODE EXECUTION
============================================================

Default repository processing must never execute:

npm install
npm scripts
pip install
setup.py
Makefile
Docker
Terraform apply
GitHub Actions
binaries

Static analysis only.

============================================================
24. RESOURCE LIMITS
============================================================

Apply limits to:

ZIP
repository files
single file size
total repository size
dependency count
architecture graph size
documentation context
LLM tokens
analysis runtime
artifact generation
queue jobs

============================================================
25. LLM TOKEN LIMITS
============================================================

Existing context engine must enforce:

maximum input tokens
maximum output tokens
maximum files
maximum chunk count

Never allow user/repository content to bypass token budget.

============================================================
26. AI REQUEST RATE LIMITING
============================================================

Rate limit:

chat
context generation
artifact generation
documentation generation
AI reports

by:

user
workspace
organization

where appropriate.

============================================================
27. AI COST LIMITS
============================================================

Organization-level limits:

daily AI requests
monthly token budget
artifact generation count

Do not implement billing yet.

These are protection limits.

============================================================
28. COST EXCEEDED BEHAVIOR
============================================================

If limit exceeded:

reject new expensive AI operation

but allow:

read-only access
security viewing
existing artifacts
normal repository browsing

Do not lock the entire organization.

============================================================
29. DATABASE SECURITY
============================================================

Audit:

ORM queries
raw SQL
joins
tenant filters
authorization filters

Ensure organization/workspace scope cannot be accidentally omitted.

============================================================
30. DATABASE CONSTRAINTS
============================================================

Use database constraints where possible.

Examples:

foreign keys
unique constraints
not-null
check constraints

Do not rely only on application validation.

============================================================
31. DATABASE CONNECTION POOL
============================================================

Configure safe pool limits.

Prevent one worker or request class from exhausting database
connections.

============================================================
32. DATABASE TRANSACTIONS
============================================================

Use transactions for:

membership changes
ownership transfer
security finding lifecycle
artifact version creation
snapshot creation
analysis state transitions

where consistency requires it.

============================================================
33. MIGRATION SAFETY
============================================================

Production migrations should:

avoid destructive operations by default
support rollback where practical
be tested on representative schema
avoid long table locks

Never drop production data as part of normal deployment.

============================================================
34. DATABASE BACKUPS
============================================================

Document backup strategy.

Minimum:

automated database backups
retention
restore procedure

Do not claim backups exist until actually configured.

============================================================
35. RESTORE TESTING
============================================================

A backup is not enough.

Create documented restore test.

Verify:

database restored
application connects
authorization remains intact
repository metadata remains consistent
snapshots remain readable

============================================================
36. DISASTER RECOVERY
============================================================

Document:

RPO
RTO

Do not invent numeric guarantees.

Set initial target values only if infrastructure can actually meet them.

============================================================
37. STORAGE DURABILITY
============================================================

Repository uploads/artifacts/snapshots stored in object storage where
appropriate.

Create:

StorageProvider

Interface:

put()
get()
delete()
exists()
stream()

============================================================
38. STORAGE SECURITY
============================================================

Private repository artifacts:

private by default.

Do not expose raw object storage URLs publicly.

Use:

short-lived signed URLs

where direct download is required.

============================================================
39. SIGNED URL SECURITY
============================================================

Signed URLs should:

expire quickly
be scoped
not expose credentials

Every generation requires authorization first.

============================================================
40. STORAGE TENANT ISOLATION
============================================================

Object keys should contain safe tenant scope.

Example:

organizations/{organizationId}/workspaces/{workspaceId}/...

Do not use user-controlled paths directly.

============================================================
41. LOG SECURITY
============================================================

Continue Phase 10 redaction.

Never log:

OAuth tokens
GitHub App private keys
webhook secrets
API keys
raw secrets
session cookies
authorization headers

============================================================
42. LOG DATA MINIMIZATION
============================================================

Avoid logging full:

LLM prompts
LLM responses
repository source
webhook payloads

unless explicitly required for controlled debugging.

============================================================
43. STRUCTURED LOGGING
============================================================

Every important request:

requestId
organizationId
workspaceId
repositoryId
userId
route
status
duration

Use IDs only.

Never use raw sensitive content.

============================================================
44. CORRELATION IDs
============================================================

Support:

requestId
traceId
analysisRunId
jobId
webhookDeliveryId

This should make one analysis traceable across services.

============================================================
45. DISTRIBUTED TRACING
============================================================

If Phase 10 OpenTelemetry exists:

extend it.

Trace:

HTTP
DB
queue
GitHub
OSV
LLM
storage
analysis stages

Do not record secrets in spans.

============================================================
46. METRICS CARDINALITY
============================================================

Do not use:

repository name
file path
user email

as unlimited metric labels.

Use bounded identifiers or sampling.

============================================================
47. ALERTING
============================================================

Production alerts for:

database failure
queue backlog
worker crash
high error rate
webhook failures
GitHub API failures
LLM provider failures
storage failure
disk exhaustion
memory exhaustion

Use Phase 10 alert foundation.

============================================================
48. HEALTH ENDPOINTS
============================================================

Implement:

/health
/readiness

Health:

application alive

Readiness:

dependencies available enough to serve traffic.

Do not expose sensitive diagnostics publicly.

============================================================
49. DEPENDENCY HEALTH
============================================================

Readiness may consider:

database
queue
storage

But avoid making optional integrations make the whole application
unavailable.

Example:

OpenRouter unavailable

should not make repository browsing unavailable.

============================================================
50. GRACEFUL SHUTDOWN
============================================================

On SIGTERM:

stop accepting new work
finish active requests where practical
stop queue consumers
finish/acknowledge safe jobs
close database connections
close storage connections

Respect configurable shutdown timeout.

============================================================
51. WORKER SCALING
============================================================

Separate worker types logically:

web/API
analysis
security
documentation
artifact

Do not require every process to execute every workload.

============================================================
52. HORIZONTAL SCALING
============================================================

Application instances must be stateless where possible.

Do not store critical session/work state only in local memory.

Use:

database
Redis
object storage

where appropriate.

============================================================
53. SESSION STORAGE
============================================================

If server-side sessions exist:

do not store them only in process memory when multiple instances run.

Use shared secure session storage.

============================================================
54. CACHE
============================================================

If Redis exists:

centralize cache.

If cache unavailable:

application should degrade gracefully where possible.

Never use cache as source of truth for permissions.

============================================================
55. QUEUE SCALING
============================================================

Support multiple workers consuming safely.

Jobs must be:

idempotent
retryable
observable

============================================================
56. JOB LEASES
============================================================

If supported by queue:

use visibility timeout/lease.

Stuck jobs should become retryable.

============================================================
57. JOB DUPLICATION
============================================================

Workers may execute a job more than once under failure.

Therefore every critical operation must remain idempotent.

Especially:

snapshot creation
security findings
artifact versions
webhook processing

============================================================
58. ANALYSIS LOCKING
============================================================

Prevent duplicate expensive analyses for same:

repository
commit
analysis profile

Use:

unique DB constraint
distributed lock
or deterministic job ID

preferably more than one defense.

============================================================
59. RATE LIMITING ARCHITECTURE
============================================================

Implement distributed rate limiting where multiple application
instances exist.

Do not rely only on process-local counters.

============================================================
60. ABUSE PROTECTION
============================================================

Protect endpoints:

login
invitation
chat
artifact generation
ZIP upload
repository analysis
webhook

against:

burst abuse
large payloads
repeated expensive requests

============================================================
61. LOGIN PROTECTION
============================================================

GitHub OAuth is the primary identity mechanism.

Still protect callback endpoints from:

CSRF
state mismatch
replay

Reuse secure OAuth state implementation.

============================================================
62. COOKIE SECURITY
============================================================

If cookies are used:

Secure
HttpOnly
SameSite

according to deployment requirements.

Do not expose session cookies to JavaScript unnecessarily.

============================================================
63. CSRF
============================================================

Audit state-changing browser requests.

OAuth state alone is not a universal CSRF solution.

Use appropriate CSRF protections depending on auth architecture.

============================================================
64. CORS
============================================================

Production CORS must use explicit allowed origins.

Do not use:

Access-Control-Allow-Origin: *

for authenticated APIs.

============================================================
65. SECURITY HEADERS
============================================================

Configure appropriate headers:

CSP
HSTS
X-Content-Type-Options
Referrer-Policy
Frame restrictions

Do not introduce CSP that breaks the application without testing.

============================================================
66. CONTENT SECURITY POLICY
============================================================

Start with report-only if necessary.

Then enforce once verified.

Do not allow arbitrary inline scripts unnecessarily.

============================================================
67. FILE DOWNLOAD SECURITY
============================================================

Generated:

PDF
PPTX
JSON
SARIF
Markdown

must use correct content types.

Prevent content sniffing.

============================================================
68. HTML ARTIFACT SECURITY
============================================================

Generated HTML documentation may contain repository-controlled content.

Sanitize HTML.

Do not allow repository source to inject arbitrary scripts.

============================================================
69. MARKDOWN RENDERING SECURITY
============================================================

Sanitize unsafe HTML.

Protect against:

script injection
javascript URLs
unsafe embeds

============================================================
70. PDF SECURITY
============================================================

PDF renderer must treat source content as data.

Avoid unsafe external resource fetching.

============================================================
71. PPT SECURITY
============================================================

Same principle.

Do not embed arbitrary remote executable content.

============================================================
72. EXPORT ACCESS
============================================================

Every export:

authorize
generate
store
download

must respect tenant/workspace permissions.

============================================================
73. AUDIT LOG HARDENING
============================================================

Audit logs:

append-only
tenant-scoped
tamper-resistant where infrastructure supports it

Do not expose raw database mutation controls.

============================================================
74. AUDIT RETENTION
============================================================

Create configurable retention.

Example:

organization audit retention

Do not silently delete security-critical audit events.

============================================================
75. SECURITY EVENT MODEL
============================================================

Normalize security events:

AUTH_FAILURE
AUTHZ_DENIED
TOKEN_ROTATED
MEMBER_ROLE_CHANGED
INTEGRATION_CHANGED
WEBHOOK_SECRET_CHANGED
EXPORT_CREATED
CREDENTIAL_REVOKED

============================================================
76. CREDENTIAL REVOCATION
============================================================

Support revocation for:

GitHub OAuth
GitHub App integration
webhook credentials
organization invitations

Do not keep using revoked credentials.

============================================================
77. TOKEN ROTATION
============================================================

If GitHub credentials are rotated:

new credential should be used for new operations.

Existing credential should be safely invalidated.

============================================================
78. OAUTH TOKEN STORAGE
============================================================

Do not expose GitHub OAuth access tokens to:

frontend
logs
AI
artifacts

Only backend integration layer may access them.

============================================================
79. GITHUB APP PRIVATE KEY
============================================================

Never store in frontend.

Never include in API responses.

Never log.

Prefer secret manager in production.

============================================================
80. WEBHOOK SECRET ROTATION
============================================================

Support rotation without downtime where possible.

Potential:

active secret
previous secret during transition

but minimize transition period.

============================================================
81. ENTERPRISE SSO FOUNDATION
============================================================

Prepare abstraction:

IdentityProvider

Implement:

GitHub OAuth

Keep interface compatible with:

OIDC
SAML

Do not implement full SAML yet unless infrastructure already exists.

============================================================
82. OIDC FOUNDATION
============================================================

Create provider abstraction:

authorize
callback
validateIdentity
mapUser

Do not hard-code GitHub assumptions into user identity layer.

============================================================
83. SSO DOMAIN MODEL
============================================================

Prepare:

OrganizationIdentityProvider

Fields:

organizationId
providerType
issuer
clientId
enabled
configurationReference

Never store client secrets plaintext.

============================================================
84. SAML
============================================================

Do not implement a fragile custom SAML system merely for completeness.

If not already supported:

create interface/documentation only.

Production SAML should use a vetted library/provider.

============================================================
85. SCIM FOUNDATION
============================================================

Prepare future:

SCIMUser
SCIMGroup

Do not implement complete SCIM provisioning in this phase.

============================================================
86. USER LIFECYCLE
============================================================

Enterprise identity should eventually support:

joiner
mover
leaver

For now ensure organization membership can be centrally revoked.

============================================================
87. MFA
============================================================

Do not implement custom MFA cryptography.

If GitHub is the identity provider:

document dependence on GitHub account security.

Enterprise SSO/MFA belongs to identity provider integration.

============================================================
88. COMPLIANCE FOUNDATION
============================================================

Create documentation for:

data categories
data retention
access control
audit
encryption
backup
incident response

Do NOT claim:

SOC 2
ISO 27001
HIPAA
GDPR certification/compliance

unless actually validated.

============================================================
89. DATA CLASSIFICATION
============================================================

Define:

PUBLIC
INTERNAL
CONFIDENTIAL
SECRET

Examples:

Public repository:
PUBLIC/INTERNAL

Private source:
CONFIDENTIAL

Credentials:
SECRET

============================================================
90. DATA HANDLING MATRIX
============================================================

For each classification define:

logging
LLM usage
storage
export
retention

Document it.

============================================================
91. DATA RETENTION ENGINE
============================================================

Create configurable retention policies.

Resources:

webhook events
analysis runs
snapshots
artifacts
audit logs
temporary uploads
logs

Do not delete data without policy + authorization.

============================================================
92. TEMP FILE CLEANUP
============================================================

ZIP/temp extraction must have:

TTL
startup cleanup
failed-job cleanup

Do not let temporary files grow indefinitely.

============================================================
93. ORPHAN CLEANUP
============================================================

Detect:

orphaned snapshots
orphaned artifacts
orphaned uploads
failed temporary files

Cleanup must be safe and auditable.

============================================================
94. STORAGE GARBAGE COLLECTION
============================================================

Do not delete object storage files merely because database records are
temporarily missing.

Use:

mark
verify
grace period
delete

to avoid accidental data loss.

============================================================
95. INCIDENT RESPONSE FOUNDATION
============================================================

Create:

docs/incident-response.md

Include:

credential leak
tenant isolation incident
database outage
storage outage
LLM provider compromise
GitHub integration compromise

============================================================
96. SECURITY INCIDENT STATES
============================================================

Support internal:

OPEN
INVESTIGATING
CONTAINED
RESOLVED

Do not expose this as a customer-facing incident platform yet.

============================================================
97. EMERGENCY CREDENTIAL REVOCATION
============================================================

Document procedure for:

revoke GitHub App credentials
rotate webhook secret
rotate application secrets
disable AI provider
disable compromised integration

============================================================
98. FEATURE KILL SWITCHES
============================================================

Use Phase 10 feature flags for emergency shutdown:

AI_CHAT_DISABLED
ZIP_UPLOAD_DISABLED
CONTINUOUS_ANALYSIS_DISABLED
WEBHOOKS_DISABLED
ARTIFACT_GENERATION_DISABLED

Do not require deployment to disable dangerous subsystems.

============================================================
99. DEGRADED MODE
============================================================

GitVision should continue partial operation during dependency failures.

Example:

LLM unavailable:

repository browsing:
WORKS

security scanner:
WORKS

architecture:
WORKS

AI chat:
UNAVAILABLE

============================================================
100. GITHUB DEGRADED MODE
============================================================

GitHub API unavailable:

existing snapshots:
READABLE

historical reports:
READABLE

new sync:
QUEUED/FAILED

Do not make all existing data disappear.

============================================================
101. OSV DEGRADED MODE
============================================================

OSV unavailable:

existing findings:
READABLE

new dependency scan:
RETRY/PARTIAL

Do not mark all dependencies safe.

============================================================
102. STORAGE DEGRADED MODE
============================================================

If artifact storage unavailable:

existing metadata:
READABLE

new artifact generation:
QUEUED/FAILED

============================================================
103. LLM FAILOVER
============================================================

Provider abstraction should allow:

primary provider
fallback provider

only where policy permits.

Do not automatically send private data to an unapproved fallback provider.

============================================================
104. PROVIDER FAILURE POLICY
============================================================

For each organization:

allowed providers

must be checked before fallback.

If no allowed fallback:

fail safely.

============================================================
105. LOAD TESTING
============================================================

Create load-test scenarios:

concurrent repository browsing
concurrent chat
concurrent analysis
rapid webhook events
large ZIP uploads
artifact generation
security scanning

Measure:

latency
throughput
error rate
queue delay
database utilization

Do not invent performance claims.

============================================================
106. LARGE REPOSITORY TEST
============================================================

Test:

large file count
large dependency graph
large git history
many contributors
large documentation set

Ensure system degrades gracefully.

============================================================
107. LARGE GRAPH PROTECTION
============================================================

Architecture visualization should use:

aggregation
pagination
lazy loading

Do not send enormous graph JSON directly to browser.

============================================================
108. LARGE CHAT CONTEXT
============================================================

Use:

retrieval
chunking
token budgets
summaries

Never blindly inject entire massive repository into every request.

============================================================
109. DATABASE INDEX REVIEW
============================================================

Audit indexes for:

organizationId
workspaceId
repositoryId
snapshotId
analysisRunId
userId
createdAt

Do not add indexes blindly.

Measure query patterns.

============================================================
110. QUERY PERFORMANCE
============================================================

Identify slow queries.

Add:

pagination
selective fields
appropriate joins
indexes

Avoid N+1.

============================================================
111. API PAGINATION
============================================================

Large collections must paginate:

repositories
snapshots
analysis runs
findings
artifacts
audit logs
members
teams
webhooks

============================================================
112. API RESPONSE LIMITS
============================================================

Do not return huge:

file trees
graphs
audit logs
analysis payloads

Use pagination or summarized responses.

============================================================
113. API VERSIONING
============================================================

Prepare:

/api/v1

if current architecture permits.

Do not break existing routes unnecessarily.

Document compatibility.

============================================================
114. BACKWARD COMPATIBILITY
============================================================

Existing frontend clients should continue working.

If response shape changes:

add fields instead of removing existing ones where possible.

============================================================
115. PRODUCTION CONFIGURATION
============================================================

Separate:

development
test
staging
production

Do not use production credentials in local development.

============================================================
116. CONFIG VALIDATION
============================================================

On startup validate:

required environment variables
secret presence
URLs
database configuration
queue configuration
storage configuration

Fail fast for missing critical secrets.

============================================================
117. SAFE STARTUP
============================================================

Do not print secret values when configuration fails.

Example:

ERROR:
OPENROUTER_API_KEY is missing

Never:

ERROR:
OPENROUTER_API_KEY=sk-...

============================================================
118. DEPLOYMENT STRATEGY
============================================================

Document:

build
migration
deploy
health check
rollback

Avoid schema/application incompatibility.

============================================================
119. ZERO-DOWNTIME MIGRATIONS
============================================================

Where possible:

expand
deploy
migrate
contract later

Do not perform destructive schema changes before all old workers are
compatible.

============================================================
120. ROLLBACK
============================================================

Document:

application rollback
migration rollback
feature flag rollback

Not every migration can be reversed.

Where irreversible:

document recovery strategy.

============================================================
121. BLUE/GREEN OR ROLLING DEPLOYMENT
============================================================

Do not require one deployment strategy.

Create deployment-compatible architecture.

Application should tolerate multiple versions during rolling deployment
where practical.

============================================================
122. WORKER VERSION COMPATIBILITY
============================================================

Queue payloads should be versioned where necessary.

Example:

analysisJobVersion

Old workers should not silently process incompatible payloads.

============================================================
123. JOB SCHEMA VERSIONING
============================================================

For important jobs:

type
version
payload

This enables future migrations.

============================================================
124. OBSERVABILITY DASHBOARD
============================================================

Production dashboard:

API
Database
Queue
Workers
GitHub
OSV
LLM
Storage
Webhooks

Metrics:

latency
error rate
throughput
queue depth
failed jobs
resource usage

============================================================
125. SERVICE LEVEL INDICATORS
============================================================

Track:

API availability
analysis success
webhook processing success
queue delay
AI availability
GitHub sync success

Do not publish SLA promises unless contractually supported.

============================================================
126. ERROR BUDGET FOUNDATION
============================================================

Prepare SLO/SLA-compatible metrics.

Do not create fake guarantees.

============================================================
127. RELEASE TRACKING
============================================================

Every production deployment should record:

version
commit SHA
deployment time

Reuse Phase 10 release tracking.

============================================================
128. BUILD ARTIFACT INTEGRITY
============================================================

Where practical:

immutable build artifacts
versioned containers
dependency lockfiles

Do not deploy untracked builds.

============================================================
129. DEPENDENCY SECURITY
============================================================

Scan application dependencies.

Use:

OSV
package ecosystem security tools

Do not automatically update dependencies without review.

============================================================
130. CONTAINER SECURITY
============================================================

If containerized:

minimal base image
non-root user
read-only filesystem where practical
drop unnecessary capabilities
no embedded secrets

============================================================
131. CONTAINER RESOURCE LIMITS
============================================================

Set:

CPU
memory
process
filesystem

limits appropriate to workload.

Do not allow repository analysis to consume entire host.

============================================================
132. WORKER SANDBOXING
============================================================

Although code execution is not allowed:

static analysis workers processing untrusted data should still be
isolated.

Use:

non-root
restricted filesystem
network restrictions where possible
resource limits

============================================================
133. NETWORK EGRESS
============================================================

Workers should only access required external services.

Example:

GitHub API
OSV
configured LLM provider
storage

Do not allow arbitrary outbound access from analysis workers if
infrastructure supports egress control.

============================================================
134. ADMIN ACCESS
============================================================

Admin APIs are high-risk.

Require:

strong authentication
authorization
audit logging

Do not expose admin endpoints publicly without protection.

============================================================
135. BREAK-GLASS ACCESS
============================================================

If emergency admin access exists:

record:

actor
reason
time
resource

Do not create invisible superuser access.

============================================================
136. SUPPORT ACCESS
============================================================

Do not create generic "support can see everything" behavior.

Any privileged access must be explicit and audited.

============================================================
137. CUSTOMER DATA ISOLATION
============================================================

Support personnel should not automatically access:

private repository source
AI conversations
secret findings

unless explicit authorized access exists.

============================================================
138. PRIVACY CONTROLS
============================================================

Organization settings should eventually control:

AI processing
retention
artifact storage
telemetry

Implement only controls actually enforceable.

============================================================
139. TELEMETRY PRIVACY
============================================================

Do not send repository source into third-party analytics systems.

Analytics events should use metadata.

============================================================
140. ERROR TRACKING PRIVACY
============================================================

Error tracking must redact:

authorization headers
tokens
repository source
secret values
private prompt content

============================================================
141. SENSITIVE URL PARAMETERS
============================================================

Do not put:

tokens
secrets
invitation tokens

in query strings.

Use headers/body.

============================================================
142. FILE PATH SECURITY
============================================================

Normalize file paths.

Prevent:

../
absolute paths
Windows traversal
null-byte tricks

Reuse existing safe path utility.

============================================================
143. COMMAND INJECTION REVIEW
============================================================

Search codebase for:

child_process
exec
spawn
shell
system

Any dynamic command execution must be reviewed.

Repository-controlled strings must never become shell commands.

============================================================
144. SQL INJECTION REVIEW
============================================================

Audit raw SQL.

Use parameterized queries.

No user/repository content directly interpolated into SQL.

============================================================
145. XSS REVIEW
============================================================

Audit:

README rendering
Markdown
commit messages
issue text
AI output
artifact HTML
repository names
file contents

Sanitize untrusted HTML.

============================================================
146. OPEN REDIRECT REVIEW
============================================================

OAuth and external redirect flows must validate destination.

Do not accept arbitrary redirect URLs.

============================================================
147. SECURITY TEST SUITE
============================================================

Create security regression suite for:

IDOR
tenant isolation
auth bypass
CSRF
CORS
XSS
SSRF
path traversal
ZIP bombs
secret leakage
prompt injection
SQL injection
command injection
webhook spoofing
replay
rate-limit bypass

============================================================
148. PENETRATION TEST PREPARATION
============================================================

Create:

docs/security-testing.md

Document testable attack surfaces.

Do not claim penetration testing has occurred unless it actually has.

============================================================
149. SECURITY CONTACT
============================================================

Create security policy foundation:

SECURITY.md

Include:

how to report vulnerabilities
what information to include
responsible disclosure guidance

Do not expose private internal infrastructure.

============================================================
150. DEPENDENCY UPDATE POLICY
============================================================

Document:

security update cadence
critical vulnerability handling
dependency review

Do not automatically merge dependency upgrades.

============================================================
151. INCIDENT LOGGING
============================================================

Critical security events should create structured audit events.

Do not log sensitive payloads.

============================================================
152. BACKUP ENCRYPTION
============================================================

Backups containing private repository data must be encrypted.

Document key ownership.

============================================================
153. BACKUP ACCESS
============================================================

Backup access must be restricted.

Do not let normal application users access database backups.

============================================================
154. RESTORE AUTHORIZATION
============================================================

Restore operations are infrastructure/admin actions.

Never expose to normal users.

============================================================
155. DATA DELETION
============================================================

Organization deletion should define:

soft delete
retention period
hard delete

Do not immediately purge data unless policy requires it.

============================================================
156. USER DATA DELETION
============================================================

If user deletion is supported:

remove active access

preserve necessary audit history

anonymize where required

do not break referential integrity.

============================================================
157. REPOSITORY DISCONNECT
============================================================

When GitHub repository access is revoked:

existing historical data policy must be explicit.

Options:

retain historical snapshot
delete source
retain metadata only

Do not silently choose destructive behavior.

============================================================
158. DATA EXPORT / PORTABILITY
============================================================

Prepare export architecture for organization-owned:

metadata
artifacts
reports
audit logs

Only authorized admins.

Do not expose credentials.

============================================================
159. ENTERPRISE POLICY ENGINE
============================================================

Create foundation:

OrganizationPolicy

Potential policies:

AI usage
allowed providers
continuous analysis
artifact generation
retention
external invitations
export permissions

Only implement enforceable policies.

============================================================
160. POLICY EVALUATION
============================================================

Create:

PolicyService

All sensitive operations can query policy.

Example:

canUseAI()
canExport()
canInviteExternal()
canEnableAutomation()

============================================================
161. POLICY AUDIT
============================================================

Policy changes must be audited.

Store:

old value
new value
actor
timestamp

Do not store secret values.

============================================================
162. DEFAULT SECURITY POSTURE
============================================================

Default:

private data protected
exports protected
AI cost limited
continuous analysis opt-in
external invitations controlled
secrets redacted
audit enabled

Do not choose convenience over tenant isolation.

============================================================
163. PERFORMANCE REGRESSION
============================================================

After adding authorization/policy checks:

measure:

API latency
repository loading
chat context retrieval
artifact loading
search
security dashboard

Optimize only based on measurements.

============================================================
164. CHAOS / FAILURE TESTING
============================================================

Test:

database unavailable
Redis unavailable
queue unavailable
GitHub unavailable
OSV unavailable
LLM unavailable
storage unavailable

Verify graceful degradation.

============================================================
165. RECOVERY TEST
============================================================

Simulate:

worker crash during analysis

Expected:

job retries safely
no duplicate snapshot
no duplicate finding
analysis state remains recoverable

============================================================
166. WEBHOOK RECOVERY TEST
============================================================

Simulate:

webhook received
worker crashes
event remains durable
event retries
analysis completes once

============================================================
167. ARTIFACT RECOVERY TEST
============================================================

Simulate:

artifact generation fails after analysis succeeds.

Expected:

analysis remains successful
artifact remains retryable
no corrupted artifact version marked complete

============================================================
168. DATABASE FAILURE TEST
============================================================

During database outage:

API should return controlled error.

No secret leakage.

No partial membership changes.

============================================================
169. SECURITY REGRESSION
============================================================

Every future feature must include:

authorization tests
tenant isolation tests
secret redaction tests

as part of CI.

============================================================
170. SECURITY CHECKLIST IN CI
============================================================

CI should validate:

dependency vulnerabilities
secret scanning
lint
tests
build
migration validation

Do not block CI on non-actionable informational warnings unless configured.

============================================================
171. PRODUCTION READINESS CHECK
============================================================

Create:

docs/production-readiness.md

Checklist:

security
database
storage
queue
observability
backup
recovery
deployment
secrets
rate limits
AI policy
GitHub integrations

============================================================
172. RUNBOOKS
============================================================

Create runbooks:

docs/runbooks/database-outage.md
docs/runbooks/queue-outage.md
docs/runbooks/github-outage.md
docs/runbooks/llm-outage.md
docs/runbooks/storage-outage.md
docs/runbooks/security-incident.md

============================================================
173. DEPLOYMENT DOCUMENTATION
============================================================

Create:

docs/deployment.md

Include:

environment variables
services
database
Redis/queue
storage
worker processes
health checks
migrations
rollback

============================================================
174. ENVIRONMENT REFERENCE
============================================================

Existing Documentation Engine should generate/update environment
reference.

Secrets must always be masked.

============================================================
175. PRODUCTION CONFIG VALIDATION
============================================================

Validate incompatible settings.

Example:

production + debug logging

should fail or warn strongly.

Example:

production + insecure local secret store

should warn/fail according to policy.

============================================================
176. DEBUG MODE
============================================================

Production must not expose:

stack traces
SQL
raw webhook payload
AI prompts
source content

============================================================
177. ERROR RESPONSES
============================================================

Production API errors:

safe
structured
non-sensitive

Example:

{
  "error": {
    "code": "RESOURCE_ACCESS_DENIED",
    "message": "You do not have access to this resource.",
    "requestId": "..."
  }
}

============================================================
178. REQUEST SIZE LIMITS
============================================================

Apply limits to:

JSON
multipart
webhooks
chat
artifact generation

Different endpoints may have different safe limits.

============================================================
179. TIMEOUT POLICY
============================================================

Centralize timeout configuration.

Do not allow individual HTTP requests to hang indefinitely.

============================================================
180. RETRY POLICY
============================================================

Centralize retry classification:

retryable:
timeout
connection reset
5xx

non-retryable:
401
403
400
validation

Avoid retry storms.

============================================================
181. CIRCUIT BREAKERS
============================================================

For unstable external services:

GitHub
OSV
LLM

consider circuit breaker behavior.

Do not repeatedly hammer failing providers.

============================================================
182. PROVIDER HEALTH
============================================================

Track:

provider availability
latency
error rate

Use for controlled failover.

============================================================
183. LLM FALLBACK SAFETY
============================================================

Fallback provider must satisfy:

organization policy
data classification
capabilities
context requirements

Never fallback blindly.

============================================================
184. MODEL CONTEXT PROTECTION
============================================================

Prevent:

context overflow
untrusted prompt escalation
secret inclusion

before provider call.

============================================================
185. AI RESPONSE VALIDATION
============================================================

Structured AI output must be validated.

Existing artifact/documentation schemas remain authoritative.

AI cannot create arbitrary database mutations.

============================================================
186. AI GENERATED CONTENT LABELING
============================================================

Where relevant, artifact metadata should record:

generatedBy:
AI

and provenance:

VERIFIED
INFERRED
GENERATED
UNKNOWN

Reuse Phase 6/9 provenance.

============================================================
187. SECURITY REPORT AI CLAIMS
============================================================

AI security explanations must reference deterministic findings.

AI cannot invent vulnerability IDs.

============================================================
188. ARCHITECTURE AI CLAIMS
============================================================

AI architecture explanations must reference architecture evidence.

No invented components.

============================================================
189. COMPLIANCE CLAIM SAFETY
============================================================

Do not let AI generate unsupported claims like:

"SOC 2 compliant"
"ISO certified"
"HIPAA compliant"

unless evidence exists.

============================================================
190. TEST COVERAGE
============================================================

Do not target arbitrary percentage as proof of security.

Prioritize:

auth
tenant isolation
data access
credentials
uploads
webhooks
AI
exports
background jobs

============================================================
191. STATIC SECURITY ANALYSIS
============================================================

Run security checks against GitVision itself.

Use existing tools where available.

Review:

dependency vulnerabilities
secrets
unsafe command execution
unsafe SQL
unsafe HTML
SSRF
auth issues

============================================================
192. SUPPLY CHAIN SECURITY
============================================================

Document:

dependency lockfiles
trusted registries
build provenance where possible
container image provenance

Do not over-engineer before product deployment needs it.

============================================================
193. BUILD SECURITY
============================================================

CI should not expose production secrets to untrusted pull requests.

Especially important for forked PRs.

============================================================
194. GITHUB ACTION SECURITY
============================================================

If GitVision provides workflow templates:

pin third-party actions to safe immutable references where practical.

Never place secrets into untrusted PR execution paths.

============================================================
195. FORK SECURITY
============================================================

Do not expose private GitVision secrets to workflows triggered by forks.

============================================================
196. PR TRUST BOUNDARY
============================================================

Treat pull request source code as untrusted.

Do not automatically execute PR code.

============================================================
197. PRODUCTION AI PROMPTS
============================================================

Version important system prompts.

Track:

promptVersion

in AI telemetry.

Do not store full sensitive prompt by default.

============================================================
198. ANALYZER VERSIONING
============================================================

Existing analysis systems should record:

analyzerVersion

Examples:

securityAnalyzerVersion
architectureAnalyzerVersion
documentationAnalyzerVersion

This allows historical reproducibility.

============================================================
199. SNAPSHOT REPRODUCIBILITY
============================================================

Historical analysis should identify:

commit SHA
analyzer version
policy version
timestamp

Do not claim exact reproducibility if external provider behavior changed.

============================================================
200. FINAL PRODUCTION VALIDATION
============================================================

Run:

1. Full existing test suite
2. Security suite
3. Tenant isolation suite
4. Load tests
5. Queue tests
6. Failure tests
7. Backup/restore test
8. Migration test
9. Storage test
10. Webhook recovery test
11. AI provider failure test
12. GitHub outage test
13. OSV outage test
14. Artifact failure test
15. Authorization regression suite
16. Secret leakage suite
17. ZIP security suite
18. SSRF suite
19. XSS suite
20. CSRF suite
21. Rate-limit tests
22. Large repository test
23. Large graph test
24. Large organization test

============================================================
201. DEFINITION OF DONE
============================================================

[ ] Security architecture review completed

[ ] Threat model documented

[ ] Central authorization verified

[ ] Tenant isolation verified

[ ] Sensitive credentials encrypted

[ ] SecretStore abstraction exists

[ ] Production secret-manager compatibility exists

[ ] Credential rotation documented

[ ] AI data policy exists

[ ] Provider allowlist foundation exists

[ ] Prompt injection defenses verified

[ ] Tool authorization verified

[ ] SSRF protections verified

[ ] ZIP protections verified

[ ] Resource limits verified

[ ] LLM token limits verified

[ ] AI rate limiting exists

[ ] AI cost protection exists

[ ] Database constraints reviewed

[ ] Database backup strategy documented

[ ] Restore procedure tested

[ ] Storage abstraction exists

[ ] Signed download URLs protected

[ ] Log redaction verified

[ ] Distributed tracing integrated where available

[ ] Health/readiness endpoints exist

[ ] Graceful shutdown exists

[ ] Horizontal scaling supported

[ ] Queue workers scale safely

[ ] Job idempotency verified

[ ] Distributed rate limiting exists where needed

[ ] CORS hardened

[ ] Security headers configured

[ ] Markdown/HTML sanitized

[ ] Export security verified

[ ] Audit logs hardened

[ ] Retention policies documented

[ ] Temporary file cleanup exists

[ ] Feature kill switches exist

[ ] Degraded modes documented

[ ] Enterprise identity abstraction exists

[ ] OIDC foundation exists

[ ] SCIM/SAML extension points documented

[ ] Compliance documentation exists

[ ] Incident response documented

[ ] Production runbooks exist

[ ] Production deployment documented

[ ] Security CI checks exist

[ ] Dependency/security scanning exists

[ ] Load tests exist

[ ] Failure recovery tests exist

[ ] Existing functionality remains intact

[ ] Full regression suite passes

============================================================
202. DO NOT IMPLEMENT
============================================================

Do NOT implement unless already required by existing architecture:

- actual billing
- payment processing
- SOC 2 certification
- ISO certification
- HIPAA certification
- custom cryptography
- custom SAML implementation
- custom MFA cryptography
- arbitrary code execution
- automatic repository modification
- automatic PR merging
- employee productivity scoring
- developer ranking
- surveillance features
- public private-repository sharing
- uncontrolled external URL fetching

============================================================
203. FINAL REPORT
============================================================

At completion report:

A. Security architecture review
B. Threat model
C. Files created
D. Files modified
E. Database migrations
F. Secret management
G. Encryption changes
H. Authorization hardening
I. Tenant isolation
J. AI privacy controls
K. SSRF/XSS/CSRF protections
L. Rate limits
M. Queue scaling
N. Database scaling
O. Storage architecture
P. Backup/restore
Q. Disaster recovery
R. Deployment hardening
S. Observability
T. Runbooks
U. Tests
V. Load-test results
W. Known limitations
X. Manual verification
Y. Production-readiness gaps

Do not rewrite unrelated code.

Do not remove existing functionality.

Prefer incremental, composable, production-safe changes.