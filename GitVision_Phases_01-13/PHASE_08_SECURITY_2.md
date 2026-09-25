# Phase 8 — GitVision Security 2.0

Ab security layer ko **OSV dependency scanner** se full **Repository Security Intelligence Platform** mein upgrade karenge.

Existing OSV scanner ko touch karke replace nahi karna — usko Security 2.0 ke ek component ke roop mein integrate karna hai.

Main goals:

* Dependency vulnerabilities
* Secret detection
* SAST-lite
* License intelligence
* SBOM
* Container scanning
* IaC scanning
* SARIF
* Security evidence
* Security diff between snapshots
* Finding lifecycle
* Remediation workflow
* Security dashboard
* AI security explanation

Copy-paste prompt:

```text id="phase8-gitvision-security"
You are working on GitVision, an AI-powered GitHub repository intelligence platform.

============================================================
PHASE 8 — SECURITY 2.0
============================================================

GOAL

Upgrade GitVision's existing OSV dependency vulnerability scanner into
a comprehensive, evidence-based Repository Security Intelligence system.

Existing security functionality MUST remain functional.

Do NOT replace the existing OSV scanner.

Instead, build a unified Security 2.0 layer around it.

Security 2.0 should eventually provide:

1. Dependency vulnerability scanning
2. Secret detection
3. SAST-lite/static security analysis
4. License intelligence
5. SBOM generation
6. Container image/config scanning where statically possible
7. Infrastructure-as-Code scanning
8. SARIF import/export
9. Security findings lifecycle
10. Security snapshot history
11. Security diff
12. Remediation tracking
13. Security dashboard
14. Security evidence
15. AI security explanations
16. Security integration with repository architecture
17. Security integration with documentation
18. Security integration with reports

All findings must be evidence-backed.

Never turn an AI suggestion into a confirmed vulnerability.

============================================================
1. EXISTING SECURITY FUNCTIONALITY
============================================================

GitVision already has:

- OSV scanning
- custom repository scan
- package.json dependency parsing
- OSV.dev integration
- bulk repository scanning
- vulnerability details
- dependency findings
- repository security UI
- secret detection/redaction used for AI
- security data associated with repository analysis

DO NOT rebuild these.

First inspect and reuse:

- OSV service
- scanner routes
- scanner UI
- vulnerability models
- repository analysis
- dependency parser
- secret redaction
- workspace
- snapshots
- analysis runs
- reports

============================================================
2. SECURITY ARCHITECTURE
============================================================

Build:

Repository Snapshot
       ↓
Security Analysis
       │
       ├── Dependency Scanner
       │       └── OSV
       │
       ├── Secret Scanner
       │
       ├── SAST-lite
       │
       ├── License Analyzer
       │
       ├── SBOM Generator
       │
       ├── IaC Scanner
       │
       └── Container Config Scanner
                 ↓
          Finding Normalization
                 ↓
          Security Findings
                 ↓
       Security Risk Aggregation
                 ↓
        Security Dashboard
                 ↓
       Snapshot Security Diff
                 ↓
          Remediation Workflow
                 ↓
             Reports / AI
```

============================================================
3. SECURITY PROVIDER ABSTRACTION
================================

Create an extensible scanner interface.

Example:

SecurityScanner

DependencyScanner
SecretScanner
SASTScanner
LicenseScanner
IaCScanner
ContainerScanner

Each scanner should return normalized findings.

Example:

{
scanner: "osv",
type: "DEPENDENCY",
severity: "HIGH",
title: "...",
package: "...",
file: "...",
evidence: "...",
remediation: "...",
references: [...]
}

Do not make the UI depend directly on one scanner's raw response format.

============================================================
4. FINDING MODEL
================

Create/reuse a normalized SecurityFinding model.

Suggested fields:

* id
* repositoryId
* snapshotId
* analysisRunId
* scanner
* type
* category
* severity
* confidence
* status
* title
* description
* packageName
* packageVersion
* fixedVersion
* filePath
* startLine
* endLine
* ruleId
* cve
* cwe
* osvId
* license
* evidence
* remediation
* references
* fingerprint
* metadata
* createdAt
* updatedAt

Categories:

DEPENDENCY
SECRET
SAST
LICENSE
IAC
CONTAINER
CONFIGURATION

============================================================
5. FINDING STATUS
=================

Support lifecycle:

OPEN
ACKNOWLEDGED
IN_PROGRESS
RESOLVED
FALSE_POSITIVE
IGNORED

Do not permanently delete findings when a new scan no longer detects them.

Historical state matters.

============================================================
6. FINDING FINGERPRINT
======================

Create stable fingerprints.

Example inputs:

scanner
ruleId
filePath
packageName
normalized evidence

A finding should remain recognizable across snapshots even if:

* line numbers move
* unrelated files change

Avoid using only line number as identity.

============================================================
7. SECURITY SNAPSHOTS
=====================

Security analysis must be snapshot-aware.

Example:

Snapshot A:
8 vulnerabilities

Snapshot B:
5 vulnerabilities

Diff:

Resolved:
CVE-X

New:
CVE-Y

Changed:
CVE-Z severity

Never mix findings from different snapshots.

============================================================
8. DEPENDENCY SCANNING
======================

Reuse existing OSV implementation.

Expand dependency support where current repository parsers already allow it.

Possible ecosystems:

npm
PyPI
Maven
Gradle
Go
Cargo
NuGet
RubyGems
Composer

Do not implement unsupported ecosystems by pretending detection works.

If a package manager is unsupported:

"Dependency analysis unavailable for this ecosystem."

Do not report zero vulnerabilities.

============================================================
9. DIRECT VS TRANSITIVE DEPENDENCIES
====================================

Where lockfile/package metadata allows:

classify:

DIRECT
TRANSITIVE

Example:

express
Direct

some-package
Transitive

Only claim transitive relationships when the lockfile/resolution data supports them.

============================================================
10. DEPENDENCY FINDING
======================

Display:

Package
Installed version
Severity
Vulnerability
Fixed version
Ecosystem
Manifest
Lockfile
OSV ID
CVE
Affected range
Evidence

Actions:

[View Dependency]
[View Source]
[Open OSV]
[Mark Acknowledged]

============================================================
11. SECRET DETECTION
====================

Implement a dedicated static secret scanner.

Detect common secret categories:

* API keys
* access tokens
* private keys
* cloud credentials
* database credentials
* OAuth secrets
* JWT-like secrets
* webhook secrets
* authentication tokens

Use a combination of:

* high-confidence patterns
* entropy analysis
* contextual detection

Do NOT treat every high-entropy string as a confirmed secret.

Each finding should have:

secret type
file
line
masked evidence
confidence
reason

============================================================
12. SECRET REDACTION
====================

Critical.

Never display the full secret.

Example:

BAD:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

GOOD:

OPENAI_API_KEY=sk-••••••••••••••••

Store only what is necessary.

Prefer storing:

* fingerprint
* masked value
* location
* secret type

Avoid storing raw secret values.

============================================================
13. SECRET SCANNING SOURCES
===========================

Scan:

* source files
* config files
* .env files
* YAML
* JSON
* TOML
* XML
* shell scripts
* CI/CD files

Respect existing ignore rules.

Do not scan:

.git internals unless explicitly supported
node_modules
build output
binary files
large generated files

============================================================
14. GIT HISTORY SECRET SCANNING
===============================

If Git history is already available and safely accessible:

support optional historical secret scanning.

This must be explicit because it can be expensive.

Show:

Current tree
Git history

Do not expose deleted secrets.

Mask all values.

============================================================
15. SECRET FALSE POSITIVES
==========================

Support:

FALSE_POSITIVE

with optional reason.

Example:

"Example placeholder key used in test fixture."

Do not silently suppress repeated findings.

============================================================
16. SAST-LITE
=============

Build a lightweight static security analyzer.

Do NOT attempt to become a complete commercial SAST engine in this phase.

Focus on high-confidence patterns.

Examples:

* command injection patterns
* SQL injection patterns
* unsafe eval
* shell execution with user input
* dangerous deserialization patterns
* path traversal patterns
* insecure HTTP usage
* weak cryptographic usage
* hardcoded credentials
* unsafe file operations
* SSRF-like patterns where confidently detectable
* insecure CORS configuration where detectable

Only implement rules with reliable evidence.

============================================================
17. SAST RULE ENGINE
====================

Create:

SecurityRule

Fields:

* ruleId
* category
* severity
* languages
* description
* detection
* remediation
* references

Example:

RULE:
JS-EVAL-001

Title:
Dynamic code execution

Severity:
HIGH

Evidence:
eval(...) at file.ts:42

Remediation:
Avoid dynamic code execution with untrusted input.

============================================================
18. SAST LANGUAGE ADAPTERS
==========================

Use an extensible architecture.

Example:

SASTEngine
├── JavaScriptRules
├── TypeScriptRules
├── PythonRules
├── JavaRules
└── GenericRules

Do not implement every language immediately.

Only claim supported rules.

============================================================
19. SAST EVIDENCE
=================

Every SAST finding must include:

* file
* line
* rule
* matched pattern
* surrounding context if safe
* confidence
* remediation

Do not send sensitive source context to the frontend unnecessarily.

============================================================
20. SAST FALSE POSITIVE CONTROL
===============================

Support:

* false positive
* ignore rule
* ignore file
* suppression metadata

Do not silently suppress findings.

============================================================
21. LICENSE INTELLIGENCE
========================

Detect:

* repository license
* dependency licenses
* unknown licenses
* license conflicts where reliable
* copyleft licenses
* permissive licenses
* proprietary/restricted licenses

Possible categories:

MIT
Apache-2.0
BSD
ISC
GPL
LGPL
AGPL
MPL
Unknown
Other

Do not make legal conclusions.

Use wording:

"License requires review."

not:

"This license is illegal."

============================================================
22. LICENSE SOURCES
===================

Detect license information from:

* package metadata
* lockfiles
* LICENSE files
* package manager metadata
* dependency metadata where available

For dependencies with unknown license:

Unknown

Do not guess.

============================================================
23. LICENSE DASHBOARD
=====================

Show:

License
Dependency count
Direct dependencies
Transitive dependencies
Unknown licenses
License categories

Example:

MIT:
42 dependencies

Apache-2.0:
8

Unknown:
3

============================================================
24. SBOM
========

Generate Software Bill of Materials.

Support at least one standard first.

Prefer:

CycloneDX

Optionally:

SPDX

SBOM should include:

* package name
* version
* ecosystem
* dependency relationship
* license
* source
* repository
* snapshot

SBOM must be reproducible from a snapshot.

============================================================
25. SBOM EXPORT
===============

Support:

Download SBOM

Formats:

CycloneDX JSON

If SPDX is implemented:

SPDX JSON

Do not fabricate package metadata.

============================================================
26. SBOM UI
===========

Security → SBOM

Display:

Total components
Direct dependencies
Transitive dependencies
Licenses
Vulnerable components

Actions:

[Download CycloneDX]

[View Components]

============================================================
27. IAC SECURITY
================

Implement lightweight IaC scanning where static patterns are reliable.

Potential files:

Terraform
Docker Compose
Kubernetes YAML
GitHub Actions
CloudFormation

Rules can detect examples such as:

* publicly exposed storage
* privileged containers
* dangerous permissions
* plaintext credentials
* overly broad IAM-like permissions
* unencrypted storage where explicit config indicates it
* public network exposure

Only create rules with strong evidence.

============================================================
28. GITHUB ACTIONS SECURITY
===========================

Analyze workflow files.

Potential findings:

* unpinned third-party actions
* overly broad permissions
* secrets passed into unsafe contexts
* pull_request_target risks where applicable
* untrusted input interpolation
* dangerous shell usage

Every finding must include workflow path and line.

============================================================
29. CONTAINER CONFIGURATION
===========================

Analyze Dockerfiles statically.

Detect:

* running as root
* secrets in ENV/ARG
* unpinned base image where relevant
* package manager cache issues where relevant
* curl | shell patterns
* privileged configuration

Do not execute Dockerfiles.

============================================================
30. CONTAINER IMAGE SCANNING
============================

Do NOT implement live registry/image execution in this phase unless an existing safe integration already exists.

Focus on:

Dockerfile
docker-compose
container configuration

If image scanning is later added:

it must use isolated external scanning infrastructure.

============================================================
31. SECURITY NORMALIZATION
==========================

Normalize all scanners into one finding schema.

Example:

{
"type": "SECRET",
"scanner": "GitVisionSecretScanner",
"severity": "HIGH",
"confidence": "HIGH",
"status": "OPEN",
"file": ".env",
"line": 4
}

or:

{
"type": "DEPENDENCY",
"scanner": "OSV",
"severity": "HIGH",
"osvId": "...",
"package": "..."
}

The UI should not need scanner-specific rendering logic for basic findings.

============================================================
32. SECURITY SEVERITY
=====================

Use:

CRITICAL
HIGH
MEDIUM
LOW
INFO

Severity must be defined by deterministic scanner rules or authoritative vulnerability metadata.

For OSV:

reuse OSV severity information where available.

For custom findings:

document the rule severity.

Do not let an LLM assign severity.

============================================================
33. CONFIDENCE
==============

Separate:

Severity

from:

Confidence

Example:

HIGH severity
LOW confidence

This is important for heuristic SAST/secret findings.

Possible confidence:

HIGH
MEDIUM
LOW

============================================================
34. SECURITY DASHBOARD
======================

Upgrade existing Security tab.

Suggested:

Security Overview

---

Security Status

Critical
High
Medium
Low

---

Findings by Type

Dependencies
Secrets
SAST
License
IaC
Container

---

Dependency Security

Vulnerable packages
Fixed versions
OSV findings

---

Secrets

Open secrets
False positives
Historical findings

---

Code Security

SAST findings

---

Supply Chain

SBOM
Licenses
Dependency health

---

Infrastructure

IaC
Docker
GitHub Actions

============================================================
35. FINDING TABLE
=================

Columns:

Severity
Type
Title
File/Package
Rule/ID
Status
Confidence
Detected
Fixed/Remediation

Filters:

Severity
Type
Status
Scanner
File
Component

Search:

package
file
CVE
OSV
rule
title

============================================================
36. FINDING DETAILS
===================

Finding page/panel:

Title

Severity

Confidence

Status

Scanner

Description

Evidence

Source

Affected package/file

References

Remediation

History

Related architecture component

Related commits

Related documentation

Actions:

[Mark Acknowledged]

[Mark Resolved]

[False Positive]

[Ignore]

============================================================
37. REMEDIATION WORKFLOW
========================

Allow users to track findings.

Example:

OPEN
↓
ACKNOWLEDGED
↓
IN_PROGRESS
↓
RESOLVED

Support:

assignee if existing team system supports it
notes
updatedAt
resolvedAt

Do not implement full enterprise assignment/RBAC yet.

============================================================
38. SECURITY DIFF
=================

Compare security snapshots.

Example:

Security Changes

New:
2 HIGH
1 MEDIUM

Resolved:
4 HIGH

Changed:
CVE-X fixed version changed

Secrets:
1 new secret

SAST:
2 new findings

Licenses:
1 dependency changed from MIT to GPL

Show:

New
Resolved
Changed
Still Open

============================================================
39. SECURITY TREND
==================

Show historical trend.

Examples:

Open findings over time
Critical/high findings over time
Dependency findings
Secret findings
SAST findings

Do not turn this into an arbitrary security score.

============================================================
40. SECURITY SCORE
==================

DO NOT create a subjective "Security Score" in this phase.

Use concrete counts and status.

If a future security score is introduced, it must have an explicit deterministic methodology and separate approval.

============================================================
41. SARIF
=========

Support SARIF 2.1.0.

Implement:

Import SARIF

Export SARIF

Normalize imported findings into SecurityFinding.

Preserve:

tool
ruleId
severity
location
message
fingerprints
help
references

This allows GitHub Actions and external scanners to integrate later.

============================================================
42. SARIF VALIDATION
====================

Validate:

schema version
runs
tool
rules
results
locations

Reject malformed input safely.

Never execute anything contained in SARIF.

============================================================
43. EXTERNAL SCANNER IMPORT
===========================

Create an abstraction:

SecurityFindingImporter

Potential future integrations:

Semgrep
Trivy
CodeQL
Grype
Snyk
etc.

Do not implement all integrations now.

The architecture should make them possible later.

============================================================
44. SECURITY + ARCHITECTURE
===========================

Integrate Phase 7 architecture.

For each finding where possible:

repository
component
file
dependency
architecture node

Example:

Finding:
SQL injection

Component:
User API

File:
userController.ts

This allows:

Security → Architecture

============================================================
45. SECURITY + DOCUMENTATION
============================

Integrate Phase 6 Documentation Engine.

Security documentation should include:

* confirmed findings
* dependency vulnerabilities
* security configuration
* authentication architecture
* secrets handling
* known risks
* remediation status

AI suggestions must be clearly separated from confirmed findings.

============================================================
46. SECURITY + CHAT
===================

Existing AI repository chatbot should understand security context.

Questions:

"Which dependencies are vulnerable?"

"Show me all high severity findings."

"Why was this flagged?"

"How can I remediate this vulnerability?"

"Which component contains the finding?"

"What changed since the last security scan?"

The AI must cite evidence.

For a dependency vulnerability:

Package
Version
OSV ID
Affected range
Fixed version
Manifest

For SAST:

Rule
File
Line
Evidence

============================================================
47. SECURITY AI SAFETY
======================

AI must never:

* invent vulnerabilities
* invent CVEs
* invent package versions
* invent fixes
* claim a finding is resolved without scan evidence
* expose secrets
* reveal private credentials

AI-generated remediation must be labeled:

"Suggested remediation"

not:

"Confirmed fix"

============================================================
48. SECRET-SAFE AI CONTEXT
==========================

Before security findings reach the LLM:

redact:

raw secrets
tokens
credentials
private keys

For secret findings send:

type
masked value
file
line
fingerprint

Never raw secret value.

============================================================
49. SECURITY ANALYSIS PIPELINE
==============================

Implement:

FETCH SNAPSHOT
↓
DEPENDENCY SCAN
↓
SECRET SCAN
↓
SAST
↓
LICENSE
↓
IAC
↓
CONTAINER CONFIG
↓
SBOM
↓
NORMALIZE
↓
DEDUPLICATE
↓
FINGERPRINT
↓
SECURITY DIFF
↓
STORE
↓
REPORT

Stages must be independently retryable.

============================================================
50. BACKGROUND JOBS
===================

Security analysis can be expensive.

Use existing job system.

Stages:

DEPENDENCY
SECRET
SAST
LICENSE
IAC
CONTAINER
SBOM
AGGREGATION

Show progress:

Dependency ✓
Secrets ✓
SAST running...
License queued
SBOM queued

One scanner failure should not invalidate every other result.

============================================================
51. IDEMPOTENCY
===============

Security analysis must be idempotent.

Key:

repositoryId
snapshotId
scanner
scannerVersion

Do not duplicate findings if the same scan is rerun.

============================================================
52. SCANNER VERSIONING
======================

Persist:

scannerVersion

Examples:

OSV adapter v2
Secret scanner v1
SAST rules v1
License analyzer v1

When rule versions change:

old findings remain historical.

New scan uses new rules.

============================================================
53. PERFORMANCE
===============

Security analysis must support large repositories.

Optimize:

* file filtering
* binary detection
* generated file exclusion
* parallel scanners where safe
* caching
* incremental scans
* batch DB writes

Never load an entire huge repository into memory unnecessarily.

============================================================
54. INCREMENTAL SECURITY SCANNING
=================================

When snapshot B differs from snapshot A:

identify changed files.

Where safe:

rerun file-based scanners only for changed files.

Dependency scanner should rerun when:

manifest/lockfile changes

Architecture/security config scanners should rerun when relevant files change.

Do not implement unsafe incremental shortcuts.

============================================================
55. SECURITY CACHE
==================

Cache results by:

repository
snapshot
scanner
scannerVersion

Example:

repo123:snapshot456:sast:v1

============================================================
56. IGNORE RULES
================

Support project-level security configuration.

Example:

.gitvision/security.yml

Possible:

ignored rules
ignored paths
severity overrides where allowed
scanner configuration

But:

severity overrides must be auditable.

Do not allow users to silently convert a CRITICAL vulnerability to INFO without recording it.

============================================================
57. SECURITY CONFIGURATION
==========================

Example:

security:
secretScan: true
sast: true
dependencyScan: true
licenseScan: true
iacScan: true

sast:
ignoredRules:
- JS-EXAMPLE-001

paths:
ignore:
- vendor/
- generated/

Configuration itself must be validated.

============================================================
58. SECURITY BASELINE
=====================

Support optional baseline.

Purpose:

Existing known findings should not flood every scan.

Baseline should identify:

* accepted findings
* false positives
* existing technical debt

New findings remain visible.

Baseline must be snapshot-aware.

============================================================
59. SECURITY REPORT
===================

Extend report generation.

Sections:

1. Security Overview
2. Dependency Vulnerabilities
3. Secrets
4. SAST
5. License Intelligence
6. SBOM Summary
7. IaC Findings
8. Container Configuration
9. Security Diff
10. Remediation
11. Data Limitations

Include:

analysis date
snapshot
scanner versions
files scanned
files skipped
partial scan status

============================================================
60. EXPORT
==========

Support:

SARIF
CycloneDX JSON
Markdown security report
JSON normalized findings

Do not expose secrets in exports.

============================================================
61. SECURITY API
================

Follow existing API conventions.

Possible endpoints:

GET /api/workspaces/:workspaceId/security

POST /api/workspaces/:workspaceId/security/scan

GET /api/workspaces/:workspaceId/security/findings

GET /api/security/findings/:findingId

PATCH /api/security/findings/:findingId/status

POST /api/security/sarif/import

GET /api/workspaces/:workspaceId/security/sarif

GET /api/workspaces/:workspaceId/security/sbom

GET /api/workspaces/:workspaceId/security/compare

Adapt to the existing API architecture.

============================================================
62. DATABASE
============

Reuse existing vulnerability models where appropriate.

Potential new models:

SecurityAnalysis

SecurityFinding

SecurityFindingEvent

SecurityBaseline

SecurityScanConfig

SBOMComponent

LicenseFinding

SecuritySnapshot

Avoid duplicating OSV vulnerability records.

Potential relationship:

SecurityFinding
↓
VulnerabilityReference
↓
OSV data

============================================================
63. FINDING EVENTS
==================

Track status changes.

Example:

OPEN
→ ACKNOWLEDGED
→ IN_PROGRESS
→ RESOLVED

Store:

previousStatus
newStatus
changedBy
reason
timestamp

This creates an audit trail.

============================================================
64. AUTHORIZATION
=================

Security data is sensitive.

Enforce:

workspace access
repository access
organization access

A user cannot access another user's private security findings.

SARIF/SBOM exports must use the same authorization.

============================================================
65. SECRET PRIVACY
==================

Never:

* show raw secret
* store raw secret unnecessarily
* send raw secret to AI
* include raw secret in logs
* include raw secret in reports
* include raw secret in SARIF

If a secret is detected:

display masked evidence only.

============================================================
66. SECURITY UI
===============

Security page:

---

SECURITY

Critical 0
High 4
Medium 8
Low 12

[Run Security Scan]

---

Findings

Dependencies
Secrets
SAST
License
IaC
Container

---

Security Changes

New
Resolved
Changed

---

SBOM

Components
Vulnerable Components
Licenses

---

Security History

Snapshot timeline

============================================================
67. SECURITY FINDING UX
=======================

Each finding card:

Severity
Type
Title

Affected:
file/package

Evidence:
masked/source-linked

Status:
Open

Confidence:
High

Actions:

View
Acknowledge
Resolve
False Positive

============================================================
68. SECURITY SOURCE VIEW
========================

Clicking a finding should open existing source viewer.

Highlight:

file
line
safe context

Never highlight/display raw secrets.

============================================================
69. LICENSE UX
==============

Create:

License Overview

Table:

License
Dependencies
Direct
Transitive
Unknown

Warning:

"License information could not be determined for 3 dependencies."

Do not provide legal advice.

============================================================
70. SBOM UX
===========

Display:

SBOM generated:
Snapshot abc123

Components:
184

Vulnerable:
7

Unknown licenses:
3

[Download CycloneDX]

============================================================
71. SECURITY HISTORY
====================

Timeline:

Sep 25
5 open high findings

Sep 18
8 open high findings

Show:

+2 new
-5 resolved

Never imply that fewer findings automatically means the repository is "secure".

============================================================
72. SECURITY DIFF
=================

Example:

NEW

HIGH
CVE-XXXX

SECRET
.env:4

RESOLVED

HIGH
OSV-XXXX

CHANGED

Dependency:
package-a
1.2.0 → 1.3.0

============================================================
73. SECURITY DATA LIMITATIONS
=============================

Display explicit limitations.

Examples:

"Secret scanning covers the current snapshot only."

"Historical Git scanning is disabled."

"Container image vulnerabilities were not scanned."

"SAST rules support JavaScript/TypeScript/Python."

"3 files could not be parsed."

Never present partial analysis as complete.

============================================================
74. TESTING
===========

Add tests for:

OSV

* existing tests continue passing
* vulnerability normalization
* direct/transitive dependencies

SECRETS

* API key detection
* token detection
* private key detection
* false positive
* masking
* no raw secret persistence

SAST

* rule detection
* line locations
* false positive suppression
* unsupported language behavior

LICENSE

* known licenses
* unknown licenses

SBOM

* CycloneDX generation
* dependency relationships
* license metadata

IAC

* Docker
* GitHub Actions
* Terraform/Kubernetes where supported

SECURITY DIFF

* new
* resolved
* unchanged
* changed

AUTHORIZATION

* private repository
* cross-user access
* exports

AI

* evidence grounding
* secret redaction
* no fabricated CVEs
* prompt injection

PERFORMANCE

* large repository
* large lockfile
* many findings

============================================================
75. SECURITY FIXTURES
=====================

Create safe test fixtures containing fake credentials only.

Never use real credentials.

Examples:

FAKE_API_KEY
FAKE_PRIVATE_KEY
FAKE_DB_PASSWORD

Clearly mark them as test data.

============================================================
76. NO REAL SECRET COLLECTION
=============================

The scanner must never upload discovered secrets to an external service.

Do not send raw secrets to:

OpenRouter
GitHub
OSV
analytics
logging services

Only local detection metadata should leave the process where necessary.

============================================================
77. NO ARBITRARY CODE EXECUTION
===============================

Security scanning must remain static by default.

DO NOT:

npm install
pip install
cargo build
docker build
execute binaries
run repository scripts

Do not execute Terraform.

Do not execute GitHub Actions.

Do not execute Dockerfiles.

============================================================
78. OBSERVABILITY
=================

Track:

scanner duration
files scanned
files skipped
findings
cache hits
cache misses
GitHub API usage
OSV latency
scanner failures
queue duration
SBOM generation duration

Never log:

raw secrets
OAuth tokens
private source
Authorization headers

============================================================
79. PHASE 8 DEFINITION OF DONE
==============================

[ ] Existing OSV scanner remains functional

[ ] Unified SecurityFinding model exists

[ ] Security scanner abstraction exists

[ ] Dependency scanning integrated

[ ] Secret scanning works

[ ] Secret masking works

[ ] SAST-lite works

[ ] License detection works

[ ] SBOM generation works

[ ] CycloneDX export works

[ ] IaC scanning works where supported

[ ] Dockerfile static security scanning works

[ ] GitHub Actions security scanning works where supported

[ ] SARIF import works

[ ] SARIF export works

[ ] Findings have fingerprints

[ ] Finding status lifecycle works

[ ] Finding history works

[ ] Security snapshots work

[ ] Security diff works

[ ] Security history works

[ ] Security baseline works

[ ] Security dashboard works

[ ] Finding details work

[ ] Source links work

[ ] Architecture integration works

[ ] Documentation integration works

[ ] AI security chat works

[ ] AI does not invent findings

[ ] Secrets never reach AI

[ ] Secrets never appear in logs

[ ] Private security data remains isolated

[ ] Scanner versioning works

[ ] Partial analysis is represented correctly

[ ] Background jobs work

[ ] Retry/idempotency works

[ ] Existing repository security UI continues working

[ ] Existing repository scanner continues working

[ ] Existing chatbot continues working

[ ] Existing architecture analysis continues working

[ ] Existing documentation engine continues working

[ ] All tests pass

============================================================
80. DO NOT IMPLEMENT IN THIS PHASE
==================================

Do NOT implement:

* full commercial-grade SAST
* runtime application security testing
* live container registry scanning
* production cloud security scanning
* full penetration testing
* exploit execution
* automatic vulnerability exploitation
* automatic code modification
* automatic PR creation
* enterprise RBAC
* SSO/SAML
* billing
* Slack/Teams
* webhooks
* CI/CD integration beyond SARIF compatibility
* full observability platform

Those belong to later phases.

============================================================
81. FINAL VERIFICATION
======================

Before completing:

1. Run all existing tests.
2. Run all new security tests.
3. Run migration.
4. Test OSV.
5. Test fake secret detection.
6. Verify raw secret never persists.
7. Test SAST.
8. Test license detection.
9. Generate SBOM.
10. Validate CycloneDX.
11. Test SARIF import/export.
12. Test Dockerfile scanning.
13. Test GitHub Actions scanning.
14. Test security diff.
15. Test finding lifecycle.
16. Test false positives.
17. Test authorization.
18. Test private repository isolation.
19. Test AI security explanation.
20. Test prompt injection.
21. Test large repository.
22. Test partial scanner failure.
23. Verify existing GitVision functionality.

At the end report:

A. Files created
B. Files modified
C. Database migrations
D. Security models
E. Scanner modules
F. New rules
G. API endpoints
H. Frontend routes/components
I. Background jobs
J. Export formats
K. Tests
L. Known limitations
M. Manual verification
N. Architectural decisions

Do not rewrite unrelated code.

Do not remove existing functionality.

Prefer incremental, composable changes.

````

## Phase 8 ke baad Security architecture

```text
                         Security 2.0
                              │
              ┌───────────────┼────────────────┐
              │               │                │
          Dependencies      Secrets          SAST
              │               │                │
             OSV         Secret Engine     Rule Engine
              │               │                │
              └───────────────┼────────────────┘
                              │
              ┌───────────────┼────────────────┐
              │               │                │
           License           IaC            Container
              │               │                │
              └───────────────┼────────────────┘
                              ↓
                     Finding Normalizer
                              ↓
                    SecurityFinding
                              ↓
          ┌───────────────────┼───────────────────┐
          ↓                   ↓                   ↓
     Security Diff       Architecture         SBOM/SARIF
          │               Correlation              │
          ↓                   ↓                   ↓
     History             Workspace             Export
          │
          ↓
    Remediation
          │
          ↓
       AI Chat
````

### Sabse important change

Ab GitVision ka security answer sirf:

> `package-x has CVE`

nahi rahega.

It can provide:

```text
Security Finding
│
├── Type: Dependency
├── Severity: HIGH
├── Confidence: HIGH
├── Package: package-x
├── Version: 1.2.0
├── Fixed Version: 1.2.4
├── OSV: ...
├── File: package-lock.json
├── Component: Authentication
├── Snapshot: abc123
├── Status: OPEN
├── First Seen: ...
├── Last Seen: ...
└── Remediation: Upgrade to 1.2.4
```

Aur secret ke case mein:

```text
SECRET DETECTED
│
├── Type: API Credential
├── File: .env
├── Line: 4
├── Severity: HIGH
├── Confidence: HIGH
├── Value: sk-••••••••••••
└── Status: OPEN
```

Raw secret kahin expose nahi hoga.

### Roadmap

```text
Phase 1   AI Foundation                    ✅
Phase 2   Repository Workspace             ✅
Phase 3   GitHub Access                    ✅
Phase 4   Universal Ingestion + ZIP        ✅
Phase 5   GitHub Profile Intelligence      ✅
Phase 6   AI Documentation Engine          ✅
Phase 7   Advanced Architecture            ✅
Phase 8   Security 2.0                    ← NOW
Phase 9   PDF/PPT/SRS/PRD + Artifact Hub
Phase 10  Observability + Admin
Phase 11  Webhooks + CI/CD
Phase 12  Teams + RBAC
Phase 13  Enterprise + Scale
```

