You are working on GitVision, an AI-powered GitHub repository intelligence platform.

============================================================
PHASE 10 — OBSERVABILITY, ADMIN INTELLIGENCE & PRODUCTION OPERATIONS
============================================================

GOAL

Build a production-grade observability and operational intelligence
layer for GitVision.

GitVision already contains:

- AI Chat
- OpenRouter provider abstraction
- GitHub OAuth
- GitHub repository access
- Repository Workspace
- Repository Snapshots
- Analysis Runs
- Background analysis
- ZIP ingestion
- GitHub Profile Intelligence
- Documentation Engine
- Architecture Intelligence
- Security 2.0
- Artifact Generation
- PDF/PPTX generation
- OSV integration
- Dependency analysis
- Repository metrics

DO NOT rebuild any of these.

This phase focuses on observing and operating the GitVision platform itself.

The system must make it possible to answer:

1. Is GitVision healthy?
2. Which APIs are slow?
3. Which services are failing?
4. Which GitHub APIs are hitting rate limits?
5. Which AI requests are slow?
6. How many tokens are being consumed?
7. What is estimated AI usage/cost?
8. Which analysis jobs are stuck?
9. Which scanners are failing?
10. Which repositories generate the most workload?
11. Which users/workspaces consume the most resources?
12. Are queues healthy?
13. Are databases healthy?
14. Are external services healthy?
15. Can an administrator diagnose failures without reading raw logs?

============================================================
1. OBSERVABILITY ARCHITECTURE
============================================================

Create a centralized observability layer.

Architecture:

Frontend
   │
Backend API
   │
Services
   │
Workers
   │
External APIs
   │
   └──────────────┐
                  ↓
           Observability SDK
                  │
        ┌─────────┼─────────┐
        ↓         ↓         ↓
       Logs     Metrics    Traces
        │         │         │
        └─────────┼─────────┘
                  ↓
        Error Tracking / Storage
                  ↓
           Admin Dashboard

Use the project's existing infrastructure where possible.

Do not introduce unnecessary infrastructure if equivalent tooling
already exists.

============================================================
2. OBSERVABILITY PRINCIPLES
============================================================

Every important request/job should have:

requestId
traceId where supported
userId where safe
workspaceId where safe
repositoryId where safe
operation
duration
status

Never log:

OAuth tokens
API keys
Authorization headers
raw secrets
private repository source
passwords
raw LLM prompts containing secrets

============================================================
3. CORRELATION ID
============================================================

Every incoming API request gets a request ID.

Example:

x-request-id

If the client sends a valid request ID:

reuse it safely.

Otherwise:

generate one.

Propagate request ID through:

API
services
database operations where useful
background jobs
external API calls
LLM calls

Example:

Request
  ↓
requestId=abc123
  ↓
GitHub API
  ↓
Analysis Job
  ↓
OSV
  ↓
LLM
  ↓
Artifact generation

This should allow an administrator to trace one operation.

============================================================
4. STRUCTURED LOGGING
============================================================

Implement structured JSON logs.

Example:

{
  "timestamp": "...",
  "level": "info",
  "service": "api",
  "operation": "repository.analysis",
  "requestId": "...",
  "workspaceId": "...",
  "repositoryId": "...",
  "durationMs": 823,
  "status": "success"
}

Do not use uncontrolled console logging throughout the application.

Create a consistent logger abstraction.

============================================================
5. LOG LEVELS
============================================================

Support:

DEBUG
INFO
WARN
ERROR

Production default:

INFO

Development can use:

DEBUG

Never log sensitive payloads simply because DEBUG is enabled.

============================================================
6. LOG REDACTION
============================================================

Create centralized redaction.

Redact:

Authorization
Bearer tokens
GitHub OAuth tokens
OpenRouter keys
API keys
passwords
private keys
detected secrets

Example:

Authorization: Bearer [REDACTED]

Never rely on individual developers remembering to redact fields.

============================================================
7. REQUEST METRICS
============================================================

Track API:

request count
success count
error count
duration
status code

Dimensions:

route
method
status class

Avoid high-cardinality metrics such as raw URLs containing IDs.

Normalize:

/api/repositories/:id

instead of:

/api/repositories/123456

============================================================
8. API LATENCY
============================================================

Track:

p50
p75
p90
p95
p99

for important API endpoints.

Example:

Repository page
Chat
Security scan
Architecture analysis
Documentation generation
Artifact generation
GitHub repository listing

Do not calculate misleading latency from incomplete data.

============================================================
9. API ERROR METRICS
============================================================

Track:

2xx
3xx
4xx
5xx

Break down 4xx where useful:

401
403
404
409
429

Track 5xx separately.

============================================================
10. SLOW REQUEST DETECTION
============================================================

Configure thresholds.

Example:

API > 2 seconds

mark as slow.

Do not hardcode one threshold for every endpoint.

Allow operation-specific thresholds.

============================================================
11. DATABASE OBSERVABILITY
============================================================

Track:

query count
query duration
transaction duration
connection pool usage
connection failures
timeouts
deadlocks where available
slow queries

Never log full SQL containing secrets or private data.

For slow query diagnostics:

record normalized query signature where possible.

============================================================
12. DATABASE HEALTH
============================================================

Create readiness/health checks.

Check:

database connectivity
migration state
connection pool

Health endpoint:

/health

Readiness:

/ready

Separate:

Liveness

from:

Readiness

============================================================
13. EXTERNAL SERVICE OBSERVABILITY
============================================================

Track external services:

GitHub
OSV
OpenRouter
storage
email if applicable
future integrations

For each:

request count
success
failure
latency
timeouts
rate limits

============================================================
14. GITHUB API METRICS
============================================================

Track:

endpoint category
latency
status
rate-limit information
retries
pagination
failures

Examples:

repository metadata
tree
contents
commits
issues
pull requests
deployments
contributors
profile

Do not store access tokens.

============================================================
15. GITHUB RATE LIMIT DASHBOARD
============================================================

Admin should see:

Current remaining
Limit
Reset time
Recent rate-limit events

Break down by authenticated GitHub connection where appropriate,
without exposing tokens.

If multiple GitHub identities are supported, isolate metrics safely.

============================================================
16. OSV OBSERVABILITY
============================================================

Track:

OSV requests
latency
success
errors
timeouts
retries
cache hit
cache miss

Example:

OSV:

Requests: 421
Cache hit: 78%
p95: 420ms
Failures: 3

============================================================
17. LLM OBSERVABILITY
============================================================

This is a critical area.

Track each AI request:

provider
model
operation
requestId
workspaceId
repositoryId
conversationId where safe
latency
time to first token
input tokens
output tokens
total tokens
status
retry count
fallback
estimated cost if available

Do not store full prompts/responses by default.

============================================================
18. LLM TIME TO FIRST TOKEN
============================================================

For streaming chat track:

TTFT

Time to first token.

Also track:

total generation time
stream completion time

Example:

TTFT:
620ms

Total:
4.8s

============================================================
19. LLM TOKEN USAGE
============================================================

Track:

input tokens
output tokens
total tokens

If provider does not return exact usage:

mark:

ESTIMATED

Never represent estimates as exact.

============================================================
20. AI COST ESTIMATION
============================================================

Create provider/model pricing configuration.

Example:

LLMModelPricing

- provider
- model
- inputPricePerMillion
- outputPricePerMillion
- effectiveFrom

Calculate:

estimatedInputCost
estimatedOutputCost
estimatedTotalCost

Important:

Label as:

Estimated

Do not claim billing accuracy unless provider billing data is directly
available.

============================================================
21. FREE MODEL HANDLING
============================================================

For free models:

cost should be represented appropriately.

Do not fabricate monetary cost.

Possible:

cost = 0
pricingType = FREE

If actual provider limits apply:

track usage separately.

============================================================
22. AI USAGE DASHBOARD
============================================================

Admin dashboard:

AI Usage

Requests
Tokens
Estimated Cost
Average Latency
p95 Latency
TTFT
Failures
Retries
Fallbacks

Breakdowns:

By model
By provider
By operation
By workspace
By repository

Be careful with high-cardinality data.

============================================================
23. AI OPERATION TYPES
============================================================

Normalize operations:

CHAT
REPOSITORY_SUMMARY
DOCUMENTATION
ARCHITECTURE
SECURITY
PROFILE_ANALYSIS
ARTIFACT_GENERATION
ARTIFACT_REGENERATION
SECTION_REGENERATION

============================================================
24. AI FAILURE TRACKING
============================================================

Track:

timeout
rate limit
provider error
invalid response
schema validation
content filter where applicable
context overflow
network error

Do not store sensitive provider payloads.

============================================================
25. AI RETRIES
============================================================

Track:

attempt number
retry reason
final status

Example:

attempt 1:
timeout

attempt 2:
success

Do not blindly retry every error.

Respect provider limits.

============================================================
26. AI FALLBACK
============================================================

If provider abstraction supports fallback:

track:

primary provider
primary model
fallback provider
fallback model
reason

Do not silently hide fallback behavior from admin diagnostics.

============================================================
27. CONTEXT WINDOW OBSERVABILITY
============================================================

Track context statistics:

estimated input tokens
retrieved files
retrieved chunks
context mode
truncated
summarized

Example:

Context:
78 files
42,300 tokens
truncated: false

This helps diagnose bad AI answers.

============================================================
28. REPOSITORY ANALYSIS METRICS
============================================================

Track analysis operations:

analysis type
repository
snapshot
duration
files processed
files skipped
errors
partial status

Types:

INGESTION
ARCHITECTURE
SECURITY
DOCUMENTATION
PROFILE
ARTIFACT

============================================================
29. ANALYSIS STAGE METRICS
============================================================

Existing AnalysisStage system should emit metrics.

For each stage:

queuedAt
startedAt
completedAt
duration
status
retryCount

Calculate:

queue delay
execution time

============================================================
30. JOB QUEUE OBSERVABILITY
============================================================

Track:

queue depth
active jobs
completed jobs
failed jobs
retrying jobs
stalled jobs
average wait
average duration

Queues may include:

repository analysis
security
architecture
documentation
artifacts

Adapt to existing queue infrastructure.

============================================================
31. STALLED JOB DETECTION
============================================================

Detect jobs that exceed expected execution time.

Example:

Architecture job expected:
<10 min

Running:
42 min

Mark:

STALLED_SUSPECTED

Do not automatically terminate jobs without safe worker semantics.

============================================================
32. JOB RETRY
============================================================

Track:

attempts
max attempts
last error
next retry

Use exponential backoff where appropriate.

Avoid retry storms.

============================================================
33. CACHE OBSERVABILITY
============================================================

Track:

cache hit
cache miss
cache set
cache invalidation
cache errors

Important caches:

GitHub
OSV
architecture
documentation
security
LLM/context
artifact source data

============================================================
34. CACHE HIT RATE
============================================================

Expose:

Hit rate
Miss rate
Evictions

Example:

GitHub cache:
84%

OSV:
78%

Do not create misleading global cache statistics when caches behave
differently.

============================================================
35. STORAGE OBSERVABILITY
============================================================

Track:

artifact storage
ZIP uploads
generated files

Metrics:

object count
storage bytes
upload duration
download duration
failures

Do not expose private object paths.

============================================================
36. ZIP/UPLOAD OBSERVABILITY
============================================================

Track:

upload count
size
extraction duration
files extracted
files skipped
validation failures
zip bomb rejection
path traversal rejection

Never log archive contents.

============================================================
37. SECURITY SCANNER OBSERVABILITY
============================================================

Track each scanner:

OSV
Secrets
SAST
License
IaC
Container
SBOM

Metrics:

duration
files scanned
findings
errors
partial status
cache

Do not log actual secrets.

============================================================
38. DOCUMENTATION OBSERVABILITY
============================================================

Track:

documentation generation
sections
LLM calls
validation failures
rendering time
source count

Example:

README:
2.3s

Architecture docs:
8.1s

Full documentation:
42s

============================================================
39. ARTIFACT OBSERVABILITY
============================================================

Track:

artifact generation
PDF render
PPTX render
HTML render
Markdown render

Metrics:

duration
size
failure
retry

Separate:

LLM generation time

from:

rendering time.

============================================================
40. ERROR TRACKING
============================================================

Integrate an error tracking abstraction.

Possible provider:

Sentry

or an existing equivalent.

Capture:

exception
stack trace
requestId
operation
environment
release/version
safe context

Never attach:

tokens
secrets
private source

============================================================
41. ERROR GROUPING
============================================================

Group errors by:

exception type
normalized message
stack location

Avoid creating thousands of unique error groups because IDs are embedded
in error messages.

============================================================
42. ERROR DASHBOARD
============================================================

Show:

Errors today
Errors this week
New errors
Resolved errors
Top error groups
Affected endpoints
Affected jobs

Filters:

service
environment
release
operation

============================================================
43. RELEASE TRACKING
============================================================

GitVision should identify application release/version.

Record:

version
commit SHA
environment
deployment timestamp

Errors and metrics should be attributable to a release.

============================================================
44. DEPLOYMENT HEALTH
============================================================

Track:

current version
previous version
deployment time
deployment status

After deployment:

monitor:

5xx
latency
error rate
job failures

Do not automatically rollback unless existing infrastructure explicitly
supports safe rollback.

============================================================
45. ENVIRONMENTS
============================================================

Support:

development
staging
production

Metrics must be separated.

Never mix staging traffic into production dashboards.

============================================================
46. ADMIN DASHBOARD
============================================================

Create:

Admin
  ├── Overview
  ├── API
  ├── AI
  ├── Jobs
  ├── GitHub
  ├── Security
  ├── Errors
  ├── Database
  ├── Storage
  └── System Health

============================================================
47. ADMIN OVERVIEW
============================================================

Show:

System Health

API:
Healthy

Database:
Healthy

Queue:
Healthy

GitHub:
Healthy

OSV:
Healthy

LLM:
Healthy

Storage:
Healthy

Then:

Requests
Errors
Active Jobs
AI Usage
Latency
Rate Limits

============================================================
48. HEALTH STATUS
============================================================

Statuses:

HEALTHY
DEGRADED
UNAVAILABLE
UNKNOWN

Do not claim HEALTHY if a dependency has not been checked.

============================================================
49. SERVICE HEALTH
============================================================

Create service health cards:

API
Database
Queue
GitHub
OSV
LLM
Storage

Each:

status
last checked
latency
recent failures

============================================================
50. HEALTH CHECKS
============================================================

Health checks should be lightweight.

Liveness:

application process is alive.

Readiness:

application can serve traffic.

Dependency health:

checked separately.

Do not make liveness dependent on GitHub/LLM.

============================================================
51. API DASHBOARD
============================================================

Display:

Requests/min
Error rate
p50
p95
p99
5xx
4xx
Slow endpoints

Table:

Endpoint
Requests
p95
Errors
Error Rate

============================================================
52. AI DASHBOARD
============================================================

Display:

Requests
Tokens
Estimated Cost
p95
TTFT
Failures
Retry rate
Fallback rate

Table:

Model
Requests
Tokens
Latency
Failures
Estimated Cost

============================================================
53. JOB DASHBOARD
============================================================

Display:

Queued
Running
Completed
Failed
Retrying
Stalled

Table:

Job
Repository
Stage
Duration
Status
Attempts

============================================================
54. GITHUB DASHBOARD
============================================================

Display:

API calls
Rate limit remaining
Rate limit resets
Errors
429s
Latency

Top endpoint categories.

============================================================
55. ERROR DASHBOARD
============================================================

Display:

Error groups
Occurrences
Last seen
Affected operations
Release

Allow:

View details

but never expose sensitive request content.

============================================================
56. REPOSITORY WORKLOAD
============================================================

Admin can see aggregate workload:

Most analyzed repositories
Most expensive AI operations
Largest repositories
Longest analysis jobs

Do not expose private repository source.

Repository names should only be visible to authorized administrators.

============================================================
57. USER WORKLOAD
============================================================

If product policy allows admin usage analytics:

show aggregate:

requests
AI usage
analysis runs
artifact generations

Do not expose private content.

Respect workspace/user privacy boundaries.

============================================================
58. USAGE QUOTAS
============================================================

Create foundation for future quotas.

Track:

AI requests
analysis runs
storage
artifact generation

Do not enforce commercial billing limits in this phase unless already
required by the existing product.

============================================================
59. RATE LIMITING
============================================================

Add application-level rate limiting where appropriate.

Protect:

login
chat
scan
artifact generation
upload

Use different limits by operation.

Do not rate-limit normal read APIs so aggressively that UI breaks.

============================================================
60. RATE LIMIT OBSERVABILITY
============================================================

Track:

requests rejected
limit
window
operation

Do not store sensitive client information unnecessarily.

============================================================
61. AUDIT EVENTS
============================================================

Reuse existing audit foundation.

Track important admin/system events:

login
logout
repository access
scan
artifact generation
security finding update
configuration change
admin access

Never log raw credentials.

============================================================
62. ADMIN AUTHORIZATION
============================================================

Admin dashboard must not be available to normal users.

Use the existing authorization system.

If admin role does not exist yet:

introduce a minimal safe admin capability.

Do NOT build full RBAC in this phase.

Keep architecture compatible with Phase 12 RBAC.

============================================================
63. ADMIN IDOR PROTECTION
============================================================

Test:

normal user cannot access admin APIs
normal user cannot query admin metrics
normal user cannot access private diagnostic information

============================================================
64. OBSERVABILITY API
============================================================

Create APIs following existing conventions.

Potential:

GET /api/admin/health

GET /api/admin/metrics/overview

GET /api/admin/metrics/api

GET /api/admin/metrics/ai

GET /api/admin/metrics/jobs

GET /api/admin/metrics/github

GET /api/admin/metrics/errors

GET /api/admin/metrics/storage

GET /api/admin/operations

GET /api/admin/errors/:id

Adapt to the existing routing architecture.

============================================================
65. METRIC STORAGE
============================================================

Choose appropriate storage.

Do not put every high-frequency metric event into a normal relational
table indefinitely.

Prefer:

time-series metrics system

or

aggregated metric tables

or

existing monitoring infrastructure.

Detailed event data can use relational storage selectively.

============================================================
66. HIGH-CARDINALITY PROTECTION
============================================================

Never use:

raw repository URL
raw user ID
raw request ID
raw file path

as unbounded metric labels.

Use logs/traces for high-cardinality investigation.

Metrics should use controlled dimensions.

============================================================
67. RETENTION
============================================================

Define retention policies.

Example:

Detailed request logs:
short retention

Aggregated metrics:
longer retention

Error events:
medium retention

AI usage aggregates:
longer retention

Make retention configurable.

============================================================
68. PRIVACY
============================================================

Observability must not become a data exfiltration path.

Never collect:

private source code by default
full chat transcripts by default
raw prompts
raw responses
secrets
OAuth tokens

If debugging requires payload capture:

make it explicit, restricted, redacted, and configurable.

Default:

OFF.

============================================================
69. AI DEBUG MODE
============================================================

Do NOT enable full prompt/response logging in production by default.

If a future debug mode is introduced:

- admin-only
- explicit
- time-limited
- redacted
- audited

Do not implement broad raw prompt logging now.

============================================================
70. OPEN TELEMETRY
============================================================

If practical with the existing stack, add OpenTelemetry.

Trace:

HTTP
database
GitHub
OSV
LLM
queue jobs

Example:

HTTP request
   ↓
repository service
   ↓
GitHub
   ↓
analysis job
   ↓
OSV
   ↓
LLM

All should share trace context where supported.

If full OpenTelemetry is not practical in the current stack,
create a compatible tracing abstraction instead of invasive rewrites.

============================================================
71. PROMETHEUS / METRICS
============================================================

If compatible with the deployment environment:

expose Prometheus-compatible metrics.

Potential:

/metrics

Protect the endpoint.

Do not expose sensitive labels.

============================================================
72. DASHBOARD DATA
============================================================

Admin dashboard should not directly query raw logs for every page load.

Use:

aggregations
caching
time windows

Default:

last 24 hours

Options:

1h
6h
24h
7d
30d

============================================================
73. TIME SERIES
============================================================

Charts:

API request rate
error rate
latency
AI usage
job throughput
queue depth
GitHub API usage
OSV latency

Use consistent time buckets.

============================================================
74. ALERTING FOUNDATION
============================================================

Create alert rules.

Examples:

5xx rate above threshold
queue backlog above threshold
LLM failure rate high
GitHub rate limit low
database unavailable
OSV unavailable
storage failures
job stall rate high

Alerts should be configurable.

============================================================
75. ALERT MODEL
============================================================

Potential:

AlertRule

- id
- name
- metric
- condition
- threshold
- window
- severity
- enabled
- cooldown

AlertEvent

- ruleId
- triggeredAt
- resolvedAt
- status

============================================================
76. ALERT SEVERITY
============================================================

Use:

INFO
WARNING
CRITICAL

Severity should reflect operational urgency based on deterministic
configuration.

============================================================
77. ALERT FATIGUE
============================================================

Implement:

cooldown
deduplication
grouping

Do not send hundreds of repeated alerts for one outage.

============================================================
78. ALERT UI
============================================================

Admin:

Alerts

Active
Resolved
Muted

Example:

CRITICAL
Database unavailable

WARNING
GitHub rate limit below configured threshold

INFO
Artifact queue above normal volume

============================================================
79. SYSTEM DIAGNOSTICS
============================================================

Create a diagnostic endpoint/service.

Example:

System Diagnostics

Application:
OK

Database:
OK

Queue:
OK

GitHub:
DEGRADED

OSV:
OK

LLM:
OK

Storage:
OK

Version:
...

Environment:
production

============================================================
80. DIAGNOSTIC SNAPSHOT
============================================================

Allow admin to generate a safe diagnostic snapshot.

Include:

version
environment
health
metrics summary
queue summary
dependency health
recent error counts

Exclude:

tokens
secrets
private source
raw prompts

============================================================
81. MAINTENANCE MODE FOUNDATION
============================================================

If useful for current architecture, create a maintenance state.

Possible:

NORMAL
MAINTENANCE
DEGRADED

Do not implement a complex maintenance scheduler.

============================================================
82. FEATURE FLAGS
============================================================

Introduce lightweight feature flag abstraction if one does not exist.

Potential future flags:

securityScannerV2
artifactGeneration
profileAnalysis
newLLMProvider

Flags should be server-controlled.

Do not expose secret configuration to frontend.

============================================================
83. CONFIGURATION VALIDATION
============================================================

At application startup validate required configuration.

Examples:

database
GitHub OAuth
OpenRouter
storage
queue

Errors should be clear.

Never print secret values.

============================================================
84. STARTUP DIAGNOSTICS
============================================================

Startup log:

GitVision starting

Version:
...

Environment:
production

Database:
connected

Queue:
connected

Observability:
enabled

Do not log credentials.

============================================================
85. GRACEFUL SHUTDOWN
============================================================

Implement safe shutdown where architecture allows.

On SIGTERM:

stop accepting new work
finish safe requests
stop workers
close queue
close database
flush telemetry
exit

Avoid abruptly killing analysis jobs.

============================================================
86. JOB CANCELLATION
============================================================

Where safe, support cancellation.

Example:

admin/user cancels long artifact generation.

Job state:

CANCEL_REQUESTED
CANCELLED

Do not kill arbitrary processes because repository code must never
be executed.

============================================================
87. OBSERVABILITY OF CANCELLATION
============================================================

Track:

who cancelled
job
reason
timestamp

============================================================
88. TESTING
============================================================

Add tests for:

REQUEST IDs
structured logging
redaction
API metrics
latency
error metrics
database health
queue health
GitHub metrics
OSV metrics
LLM metrics
token tracking
cost estimation
AI retries
AI fallback
cache metrics
artifact metrics
security scanner metrics
admin authorization
IDOR
health endpoint
readiness endpoint
metrics endpoint
alert triggering
alert cooldown
diagnostic snapshot
retention
high-cardinality protection
graceful shutdown

============================================================
89. SECURITY TESTS
============================================================

Explicitly verify observability never exposes:

GitHub OAuth token
OpenRouter API key
Authorization header
detected secret
private source
raw AI prompt
raw AI response

Test logs.

Test metrics.

Test traces.

Test error tracking.

Test admin APIs.

============================================================
90. PERFORMANCE
============================================================

Observability itself must not materially slow GitVision.

Avoid:

synchronous heavy logging
large payload serialization
full prompt capture
per-request database writes for every metric

Prefer:

buffers
aggregation
async telemetry
sampling

where appropriate.

============================================================
91. TRACE SAMPLING
============================================================

Support configurable sampling.

Example:

production:
10%

errors:
100%

slow requests:
100%

Do not sample away critical error diagnostics.

============================================================
92. METRIC AGGREGATION
============================================================

Use pre-aggregation where appropriate.

Example:

Instead of storing every API latency forever:

aggregate by:

route
status
time bucket

Retain detailed traces separately according to retention policy.

============================================================
93. ADMIN UX
============================================================

Create:

Admin Dashboard

Header:

System Status
Environment
Version
Last Updated

Cards:

API
Database
Queue
GitHub
OSV
LLM
Storage

Then:

Request Metrics
AI Usage
Job Metrics
Errors
Alerts

============================================================
94. ADMIN API DETAIL
============================================================

Admin can inspect an operation.

Example:

Request ID:
abc123

Operation:
security.scan

Duration:
12.4s

Status:
success

Stages:

GitHub:
1.2s

OSV:
2.8s

Secret Scanner:
1.1s

SAST:
4.3s

DB:
0.8s

Do not expose sensitive payloads.

============================================================
95. REQUEST DETAIL
============================================================

Show:

timestamp
requestId
traceId
route
method
status
duration
service
release
safe metadata

Never:

request body
Authorization
raw source

unless explicitly safe.

============================================================
96. AI REQUEST DETAIL
============================================================

Show:

requestId
operation
provider
model
TTFT
duration
input tokens
output tokens
estimated cost
retry
fallback
status

Do not show raw prompt/response.

============================================================
97. JOB DETAIL
============================================================

Show:

job ID
type
repository
snapshot
stage
queued
started
finished
duration
attempts
status
safe error

============================================================
98. RELEASE COMPARISON
============================================================

Allow:

Current release
Previous release

Compare:

error rate
latency
5xx
job failures
LLM failures

This should be descriptive.

Do not automatically declare a release "bad" without evidence.

============================================================
99. PRODUCTION READINESS
============================================================

Add checks for:

configuration
database
queue
storage
external services
migrations
observability

Example:

Production Readiness

Database:
PASS

Migrations:
PASS

Queue:
PASS

Storage:
PASS

GitHub:
PASS

LLM:
PASS

Telemetry:
PASS

============================================================
100. DOCUMENTATION
============================================================

Add:

docs/observability.md

Include:

architecture
metrics
logs
traces
health endpoints
admin dashboard
retention
redaction
alerts
troubleshooting

Also document:

what is intentionally NOT logged.

============================================================
101. DEFINITION OF DONE
============================================================

[ ] Structured logger exists

[ ] Request IDs exist

[ ] Correlation works across jobs

[ ] Log redaction works

[ ] API metrics work

[ ] API latency metrics work

[ ] p50/p95/p99 available

[ ] Database health works

[ ] Queue metrics work

[ ] Job metrics work

[ ] GitHub metrics work

[ ] GitHub rate-limit visibility works

[ ] OSV metrics work

[ ] LLM metrics work

[ ] LLM TTFT works for streaming

[ ] Token usage tracked

[ ] Estimated AI cost tracked

[ ] Free model usage represented correctly

[ ] Retry tracking works

[ ] Fallback tracking works

[ ] Cache metrics work

[ ] Storage metrics work

[ ] Security scanner metrics work

[ ] Documentation metrics work

[ ] Artifact metrics work

[ ] Error tracking works

[ ] Release tracking works

[ ] Health endpoint works

[ ] Readiness endpoint works

[ ] Admin dashboard exists

[ ] Admin API authorization works

[ ] IDOR tests pass

[ ] Alerting foundation exists

[ ] Alert deduplication works

[ ] Diagnostic snapshot works

[ ] Graceful shutdown works

[ ] Observability does not expose secrets

[ ] High-cardinality labels are controlled

[ ] Retention configuration exists

[ ] Existing features continue working

[ ] Existing tests pass

============================================================
102. DO NOT IMPLEMENT IN THIS PHASE
============================================================

Do NOT implement:

- full enterprise RBAC
- SSO/SAML
- billing
- public dashboards
- customer-facing analytics
- Slack notifications
- Teams notifications
- GitHub webhooks
- CI/CD automation
- automated PR creation
- autonomous remediation
- arbitrary repository execution
- full APM replacement if existing infrastructure already exists

Those belong to later phases.

============================================================
103. FINAL VERIFICATION
============================================================

Run:

1. Existing test suite
2. Observability tests
3. Request ID test
4. Log redaction test
5. API metrics test
6. DB health test
7. Queue test
8. GitHub metrics test
9. OSV metrics test
10. LLM telemetry test
11. Token usage test
12. Cost estimation test
13. Error tracking test
14. Admin authorization test
15. IDOR test
16. Health test
17. Readiness test
18. Alert test
19. Diagnostic snapshot test
20. Graceful shutdown test
21. Secret exposure test
22. Private repository isolation test
23. Large workload test

At completion report:

A. Files created
B. Files modified
C. Database migrations
D. Observability abstractions
E. Metrics
F. Logs
G. Traces
H. Admin APIs
I. Admin UI
J. Health checks
K. Alerts
L. Error tracking
M. AI telemetry
N. Tests
O. Known limitations
P. Manual verification
Q. Architectural decisions

Do not rewrite unrelated code.

Do not remove existing functionality.

Prefer incremental, composable changes.