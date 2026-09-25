# Phase 9 — Artifact Intelligence & Generation Suite

Ab GitVision ke analysis engines ka output **actual professional deliverables** mein convert karna hai.

Phase 6 se documentation, Phase 7 se architecture, aur Phase 8 se security data already available hai. Is phase mein unko dobara generate nahi karna — **un sab ko consume karke unified Artifact system banana hai.**

Goal:

```text
Repository Snapshot
       │
       ├── Documentation
       ├── Architecture
       ├── Security
       ├── Git History
       ├── Metrics
       └── Profile Intelligence
               │
               ↓
        Artifact Intelligence
               │
       ┌───────┼────────┐
       ↓       ↓        ↓
     Docs     Reports   Presentations
       │       │        │
       ↓       ↓        ↓
     README    PDF       PPTX
     SRS       Report    Executive Deck
     PRD       Security  Architecture Deck
     ADR       Audit     Project Overview
```

## Copy-paste prompt

```text id="phase9-artifact-generation"
You are working on GitVision, an AI-powered GitHub repository intelligence platform.

============================================================
PHASE 9 — ARTIFACT INTELLIGENCE & GENERATION SUITE
============================================================

GOAL

Build a production-quality Artifact Intelligence and Generation
system on top of GitVision's existing repository analysis engines.

GitVision already has:

- Repository Workspace
- Repository Snapshots
- Analysis Runs
- AI Chat
- OpenRouter provider abstraction
- GitHub integration
- ZIP ingestion
- GitHub Profile Intelligence
- Documentation Engine
- Architecture Intelligence
- Security 2.0
- Dependency analysis
- Git history
- Metrics
- Repository reports

DO NOT rebuild these systems.

This phase consumes their structured outputs and turns them into
professional artifacts.

============================================================
1. ARTIFACT TYPES
============================================================

Support:

DOCUMENTATION

- README
- PROJECT_OVERVIEW
- DEVELOPER_GUIDE
- USER_GUIDE
- SETUP_GUIDE
- API_DOCUMENTATION
- ARCHITECTURE_DOCUMENTATION
- SECURITY_DOCUMENTATION
- DEPLOYMENT_GUIDE
- TESTING_GUIDE
- CONTRIBUTING_GUIDE
- DATABASE_DOCUMENTATION
- TROUBLESHOOTING

ENGINEERING

- SRS
- PRD
- ADR
- TECHNICAL_DESIGN
- ARCHITECTURE_REPORT
- SECURITY_REPORT
- DEPENDENCY_REPORT
- CODEBASE_REPORT
- CHANGELOG
- RELEASE_NOTES

BUSINESS / EXECUTIVE

- EXECUTIVE_SUMMARY
- PROJECT_HEALTH_REPORT
- ENGINEERING_SUMMARY
- SECURITY_EXECUTIVE_REPORT
- ARCHITECTURE_EXECUTIVE_REPORT

PRESENTATIONS

- PROJECT_OVERVIEW_DECK
- ARCHITECTURE_DECK
- SECURITY_DECK
- ENGINEERING_DECK
- EXECUTIVE_DECK

EXPORT FORMATS

- Markdown
- HTML
- PDF
- PPTX
- JSON where useful

Do not generate every artifact from scratch.

Use structured source data wherever possible.

============================================================
2. ARTIFACT ARCHITECTURE
============================================================

Create:

Artifact
ArtifactVersion
ArtifactSection
ArtifactSource
ArtifactGenerationRun

Architecture:

Workspace
   │
   └── Artifact
          │
          ├── ArtifactVersion
          │
          ├── ArtifactSection
          │
          ├── ArtifactSource
          │
          └── ArtifactGenerationRun

============================================================
3. ARTIFACT MODEL
============================================================

Suggested Artifact fields:

- id
- workspaceId
- repositoryId
- snapshotId
- type
- title
- description
- status
- format
- currentVersionId
- createdBy
- createdAt
- updatedAt

Status:

DRAFT
GENERATING
READY
FAILED
ARCHIVED

============================================================
4. ARTIFACT VERSION
============================================================

ArtifactVersion:

- id
- artifactId
- snapshotId
- version
- content
- structuredContent
- format
- generationRunId
- createdBy
- createdAt

Never overwrite historical versions.

If a new snapshot generates a new artifact:

create a new version.

============================================================
5. ARTIFACT SOURCE
============================================================

Every generated artifact should retain provenance.

ArtifactSource:

- artifactVersionId
- sourceType
- sourceId
- repositoryPath
- startLine
- endLine
- snapshotId
- evidence
- confidence

Possible source types:

FILE
DOCUMENTATION
ARCHITECTURE
SECURITY_FINDING
DEPENDENCY
GIT_HISTORY
METRIC
PROFILE
AI_GENERATED

Prefer actual repository evidence.

============================================================
6. PROVENANCE
============================================================

Reuse Phase 6 provenance model.

Possible states:

VERIFIED
INFERRED
GENERATED
UNKNOWN

Example:

Verified:

"package.json contains express 5.0.0."

Inferred:

"The repository appears to use a layered service architecture."

Generated:

"Suggested future architecture improvement."

Unknown:

"Production deployment configuration was not found."

Do not silently convert unknown information into facts.

============================================================
7. SNAPSHOT AWARENESS
============================================================

Artifacts must always be associated with a snapshot.

Example:

Architecture Report
Snapshot:
abc123

Security Report
Snapshot:
abc123

SRS
Snapshot:
abc123

If repository changes:

Snapshot:
def456

Generate a new artifact version.

Never mix data from different snapshots without explicitly indicating it.

============================================================
8. ARTIFACT CENTER
============================================================

Create a central UI:

Workspace
  → Artifacts

Tabs/categories:

All
Documentation
Engineering
Security
Business
Presentations

Each artifact card:

Title
Type
Snapshot
Version
Last generated
Status

Actions:

Open
Edit
Regenerate
Duplicate
Compare
Export
Archive

============================================================
9. ARTIFACT SEARCH
============================================================

Support search:

artifact title
type
snapshot
content

Filters:

type
status
format
snapshot
created by
date

============================================================
10. ARTIFACT GENERATION FLOW
============================================================

User:

[Generate Artifact]

Select:

Artifact Type
Snapshot
Format
Audience
Detail Level

Example:

Artifact:
Architecture Report

Snapshot:
Latest

Audience:
Engineering

Detail:
Detailed

Format:
PDF

Then:

Analyze Sources
      ↓
Build Artifact Plan
      ↓
Collect Evidence
      ↓
Generate Structured Content
      ↓
Validate
      ↓
Render
      ↓
Store Artifact
      ↓
Ready
```

============================================================
11. STRUCTURED GENERATION
=========================

Do not ask the LLM to directly produce a giant PDF.

Use:

LLM
↓
Structured JSON
↓
Validation
↓
Renderer
↓
PDF/PPTX/HTML

Example:

{
"title": "...",
"sections": [
{
"title": "...",
"paragraphs": [],
"tables": [],
"sources": []
}
]
}

This makes rendering deterministic.

============================================================
12. ARTIFACT PLANNER
====================

Create an ArtifactPlanner.

Input:

artifactType
snapshot
audience
detailLevel

Output:

sections
requiredEvidence
optionalEvidence
sourceRequirements

Example SRS:

1. Introduction
2. Scope
3. System Overview
4. Functional Requirements
5. Non-Functional Requirements
6. External Interfaces
7. Data Requirements
8. Security Requirements
9. Constraints
10. Assumptions
11. Acceptance Criteria

The planner should be deterministic.

============================================================
13. EVIDENCE COLLECTOR
======================

Create:

ArtifactEvidenceCollector

It should retrieve:

documentation
architecture
security
dependencies
metrics
git history
files
README
API information
configuration

Only retrieve what the artifact needs.

Do not send the entire repository blindly to the LLM.

============================================================
14. CONTEXT BUDGET
==================

Artifact generation must respect LLM context limits.

Use:

* summaries
* structured metrics
* relevant file snippets
* architecture graph summaries
* security findings
* documentation artifacts

Do not send huge repositories wholesale unless explicitly required.

============================================================
15. SRS GENERATOR
=================

Implement Software Requirements Specification generation.

Sections:

1. Document Control
2. Introduction
3. Purpose
4. Scope
5. Definitions
6. System Overview
7. Stakeholders where evidence exists
8. Functional Requirements
9. Non-Functional Requirements
10. External Interfaces
11. Data Requirements
12. Security Requirements
13. Performance Requirements
14. Constraints
15. Assumptions
16. Dependencies
17. Acceptance Criteria
18. Open Questions

Important:

Distinguish:

Observed Existing Behavior

from:

Proposed Requirement

Do not invent product requirements.

For missing requirements:

"Not established from repository evidence."

============================================================
16. PRD GENERATOR
=================

Generate Product Requirements Document.

Sections:

* Problem
* Product Context
* Current System
* Users/personas where known
* User workflows
* Functional capabilities
* Non-functional requirements
* Success metrics
* Constraints
* Dependencies
* Risks
* Open Questions
* Future opportunities

Critical:

Do not fabricate users, business metrics, revenue,
market data, or customer research.

Clearly mark:

Observed
Inferred
Proposed

============================================================
17. ARCHITECTURE REPORT
=======================

Consume Phase 7.

Sections:

* Executive Summary
* Repository Overview
* Technology Stack
* Component Architecture
* Dependency Graph
* Data Flow
* Entry Points
* External Integrations
* Central Components
* Coupling
* Circular Dependencies
* Architecture Risks
* Change Impact
* Architecture History
* Recommendations

Use actual architecture evidence.

============================================================
18. SECURITY REPORT
===================

Consume Phase 8.

Sections:

* Security Overview
* Dependency Vulnerabilities
* Secrets
* SAST
* License Intelligence
* IaC
* Container Configuration
* SBOM Summary
* Security Changes
* Open Findings
* Resolved Findings
* Remediation

Never include raw secrets.

Use masked evidence.

============================================================
19. CODEBASE REPORT
===================

Generate:

* repository overview
* language distribution
* LOC
* file count
* directory structure
* hotspots
* contributors
* commits
* issues
* PR metrics
* architecture
* dependencies
* security
* documentation
* deployment information

Clearly identify missing data.

============================================================
20. EXECUTIVE REPORT
====================

Executive report should summarize the repository without overwhelming
the reader with implementation details.

Sections:

* Project Overview
* Technology
* Architecture Summary
* Development Activity
* Security Summary
* Key Dependencies
* Documentation Status
* Operational/Deployment Signals
* Open Risks
* Recommended Areas for Review

Do not provide subjective overall rankings.

Use factual language.

============================================================
21. CHANGELOG
=============

Consume Git history.

Generate changelog from commits/releases.

Group changes:

Added
Changed
Fixed
Security
Documentation
Infrastructure

Do not blindly classify arbitrary commits.

Where commit intent is unclear:

"Other changes"

============================================================
22. RELEASE NOTES
=================

Generate release notes between:

snapshot A
and
snapshot B

Include:

New
Changed
Fixed
Security
Breaking changes where evidence supports them

Never claim a breaking change without evidence.

============================================================
23. ADR GENERATOR
=================

Generate Architecture Decision Records.

Important distinction:

Historical ADR:

based on actual repository evidence.

Proposed ADR:

AI/user suggestion for future change.

Never present a proposed decision as historical fact.

ADR format:

Title
Status
Context
Decision
Alternatives
Consequences
Evidence
Date

============================================================
24. TECHNICAL DESIGN DOCUMENT
=============================

Generate detailed technical design.

Sections:

* Problem
* Existing Architecture
* Proposed Change
* Components
* Data Flow
* API Changes
* Database Changes
* Security
* Failure Modes
* Observability
* Migration
* Rollback
* Testing

When generated from existing code:

clearly separate existing and proposed.

============================================================
25. README GENERATION
=====================

Reuse Phase 6 documentation engine.

Artifact layer should add:

* versioning
* export
* editing
* provenance
* snapshot association

Do not create a second README generator.

============================================================
26. DOCUMENTATION REUSE
=======================

Phase 6 already generates documentation artifacts.

Artifact Center must reference them.

Avoid duplicate content.

Architecture:

DocumentationArtifact
↓
Artifact Composer
↓
PDF / HTML / PPTX

============================================================
27. PDF ENGINE
==============

Implement deterministic PDF rendering.

Recommended:

reportlab

or the existing project PDF library if already present.

PDF should support:

* title page
* table of contents
* headings
* paragraphs
* tables
* code blocks
* diagrams
* architecture images
* security findings
* page numbers
* headers/footers
* source references

Avoid huge unbroken pages.

============================================================
28. PDF DESIGN
==============

Professional layout.

Include:

GitVision
Repository
Snapshot
Generated date

Example:

GitVision
Architecture Report

Repository:
owner/repository

Snapshot:
abc123

Generated:
2026-09-25

Do not hardcode dates.

============================================================
29. TABLE OF CONTENTS
=====================

PDF documents should support TOC where practical.

Heading hierarchy:

H1
H2
H3

Use stable section anchors.

============================================================
30. DIAGRAMS IN PDF
===================

Consume Phase 7 architecture exports.

Possible:

* system overview
* component graph
* dependency graph
* data flow
* security architecture

Use SVG/PNG where required by PDF renderer.

Do not generate fake diagrams.

============================================================
31. PPTX ENGINE
===============

Implement PowerPoint generation.

Recommended:

python-pptx

or existing project tooling if already available.

Create reusable slide templates.

============================================================
32. PRESENTATION TYPES
======================

PROJECT_OVERVIEW_DECK

Slides:

1. Title
2. Project Overview
3. Technology Stack
4. Architecture
5. Key Components
6. Development Activity
7. Security
8. Dependencies
9. Risks / Open Questions
10. Summary

============================================================
33. ARCHITECTURE DECK
=====================

Slides:

1. Title
2. System Overview
3. Technology Stack
4. Component Architecture
5. Dependency Graph
6. Data Flow
7. Central Components
8. Architecture Risks
9. Change Impact
10. Summary

============================================================
34. SECURITY DECK
=================

Slides:

1. Security Overview
2. Dependency Vulnerabilities
3. Secret Findings
4. SAST
5. License/Supply Chain
6. IaC/Container
7. Security Changes
8. Remediation
9. Open Questions
10. Summary

Never display raw secrets.

============================================================
35. EXECUTIVE DECK
==================

Keep it concise.

Slides:

1. Project
2. System
3. Architecture
4. Development Activity
5. Security
6. Dependencies
7. Documentation
8. Risks
9. Key Observations
10. Next Areas for Review

No subjective "best/worst" ranking.

============================================================
36. SLIDE DATA MODEL
====================

Represent slides structurally.

Example:

{
"title": "...",
"layout": "TITLE_AND_CONTENT",
"content": [],
"sources": []
}

Layouts:

TITLE
TITLE_AND_CONTENT
TWO_COLUMN
METRIC_GRID
TABLE
DIAGRAM
TIMELINE
SECTION
SUMMARY

============================================================
37. PPTX VALIDATION
===================

Validate:

* no overflowing text
* no empty slides
* no broken images
* no missing titles
* no giant tables
* valid PPTX
* consistent slide dimensions

For large datasets:

summarize instead of creating unreadable tables.

============================================================
38. ARTIFACT EDITOR
===================

Allow users to edit generated artifacts.

Features:

* edit title
* edit sections
* regenerate section
* regenerate artifact
* save version
* compare versions
* revert to previous version

Do not destroy previous versions.

============================================================
39. SECTION REGENERATION
========================

Allow:

"Regenerate this section"

Only send the relevant section context to the LLM.

Do not regenerate the entire artifact unnecessarily.

============================================================
40. ARTIFACT DIFF
=================

Compare versions.

Show:

Added
Removed
Changed

For Markdown/text:

line/section diff.

For structured documents:

section-level diff.

============================================================
41. ARTIFACT COMMENTS / NOTES
=============================

If workspace notes infrastructure already exists:

allow artifact notes.

Examples:

"Need product team confirmation."

"Deployment section needs update."

Do not build a complete collaboration system yet.

============================================================
42. ARTIFACT GENERATION JOBS
============================

Large artifact generation must be asynchronous.

Pipeline:

PLAN
↓
COLLECT_EVIDENCE
↓
GENERATE
↓
VALIDATE
↓
RENDER
↓
STORE
↓
READY

Each stage must be retryable.

============================================================
43. GENERATION STATUS
=====================

UI:

Generating Architecture Report

✓ Collecting architecture
✓ Collecting dependencies
✓ Collecting security
● Generating content
○ Validating
○ Rendering PDF

Do not fake progress.

============================================================
44. FAILURE HANDLING
====================

If PDF rendering fails:

artifact status:
FAILED

Store:

error stage
safe error message
generation run

Do not lose generated structured content if available.

============================================================
45. ARTIFACT VALIDATION
=======================

Validate generated content before rendering.

Checks:

* required sections exist
* no unresolved placeholders
* no raw secrets
* source references valid
* snapshot exists
* unsupported claims flagged
* JSON schema valid

============================================================
46. HALLUCINATION VALIDATION
============================

For factual statements:

prefer source-backed evidence.

Potential validation:

claim
↓
source reference
↓
source exists
↓
source matches claim

If validation fails:

mark:

UNVERIFIED

Do not silently publish as verified.

============================================================
47. PLACEHOLDER DETECTION
=========================

Reject or flag:

TODO
TBD
INSERT HERE <unknown>
[PLACEHOLDER]

unless the artifact intentionally contains an Open Questions section.

============================================================
48. SOURCE REFERENCES
=====================

Artifact should optionally display:

Source:

src/server/index.js:42-57

Architecture:

Component: API Gateway

Security:

OSV-XXXX

Git:

commit abc123

Make references clickable where UI supports it.

============================================================
49. ARTIFACT QUALITY METADATA
=============================

Store:

generationModel
provider
generationTime
snapshot
artifactVersion
sourceCount
validationStatus

Do not expose internal provider secrets.

============================================================
50. MODEL/PROVIDER
==================

Use existing Phase 1 provider abstraction.

Do NOT directly call OpenRouter from artifact code.

Use:

LLMProvider

This allows future providers.

============================================================
51. AI COST CONTROL
===================

Avoid unnecessary LLM calls.

Use deterministic composition when possible.

For example:

Repository metrics:
use actual metrics.

Dependency table:
use structured dependency data.

Security findings:
use SecurityFinding.

Only use LLM for:

* narrative synthesis
* interpretation
* structured prose
* summaries
* proposed explanations

============================================================
52. PRIVATE REPOSITORY SECURITY
===============================

Artifact generation inherits workspace authorization.

Users must not be able to:

* access another user's artifact
* access another user's source
* download another user's PDF
* download another user's PPTX
* access private repository content through artifact IDs

Prevent IDOR.

============================================================
53. ARTIFACT DOWNLOAD SECURITY
==============================

Downloads must verify:

user
workspace
repository
artifact

Do not expose predictable file paths.

Use secure artifact storage abstraction.

============================================================
54. STORAGE
===========

Use existing storage abstraction if available.

Possible:

local development storage
object storage production

Store:

structured artifact
rendered PDF
PPTX
HTML

Do not store secrets.

============================================================
55. ARTIFACT FILE NAMES
=======================

Safe filename:

gitvision-owner-repo-architecture-report-v2.pdf

Sanitize:

slashes
special characters
control characters
path traversal

Never allow user-controlled path traversal.

============================================================
56. EXPORT API
==============

Adapt to existing API architecture.

Possible:

POST /api/workspaces/:workspaceId/artifacts

GET /api/workspaces/:workspaceId/artifacts

GET /api/artifacts/:artifactId

POST /api/artifacts/:artifactId/generate

POST /api/artifacts/:artifactId/regenerate

POST /api/artifacts/:artifactId/sections/:sectionId/regenerate

POST /api/artifacts/:artifactId/export

GET /api/artifacts/:artifactId/versions

GET /api/artifacts/:artifactId/versions/:versionId

POST /api/artifacts/:artifactId/compare

Do not blindly copy these paths if the existing routing conventions differ.

============================================================
57. ARTIFACT CENTER UI
======================

Workspace:

Overview
Directory
Architecture
Security
Documentation
History
Artifacts
Chat

Artifacts page:

[+ Generate Artifact]

Cards:

Architecture Report
Security Report
SRS
PRD
README
Executive Summary
Project Deck

Each card:

Status
Snapshot
Version
Updated
Formats

============================================================
58. GENERATE ARTIFACT MODAL
===========================

Step 1:

Select Artifact

Step 2:

Select Snapshot

Step 3:

Audience

Developer
Engineering
Management
Security
Customer
General

Step 4:

Detail

Brief
Standard
Detailed

Step 5:

Format

Markdown
HTML
PDF
PPTX

Step 6:

Generate

============================================================
59. AUDIENCE ADAPTATION
=======================

Same repository data can produce different artifacts.

Developer:

technical detail

Executive:

high-level summary

Security:

findings/remediation

Customer:

capabilities and architecture overview

Never expose sensitive internal details to a customer-oriented artifact
unless explicitly included.

============================================================
60. DATA CLASSIFICATION
=======================

Before generating an artifact, classify content:

PUBLIC
INTERNAL
SENSITIVE

Security findings and private source are sensitive.

Artifact generation should respect workspace visibility.

Do not create a public artifact automatically from a private repository.

============================================================
61. PUBLIC SHARING
==================

DO NOT implement public artifact sharing in this phase.

Keep artifacts private to authorized workspace users.

Future phase can add:

share links
expiration
password protection
public artifacts

============================================================
62. ARTIFACT TEMPLATE SYSTEM
============================

Create reusable templates.

Example:

SRS template
Security report template
Architecture report template
Executive report template
Deck template

Templates should define:

sections
ordering
required fields
rendering hints

============================================================
63. TEMPLATE VERSIONING
=======================

Store:

templateVersion

If template changes:

old artifacts remain reproducible.

============================================================
64. REPORT REPRODUCIBILITY
==========================

Artifact must record:

repository
snapshot
artifact type
template version
generation model
generation timestamp
source references

This allows users to understand how the artifact was produced.

============================================================
65. PROFILE ARTIFACTS
=====================

Consume Phase 5 GitHub Profile Intelligence.

Support:

PROFILE_REPORT
PROFILE_EXECUTIVE_SUMMARY

Possible content:

public profile information
repository portfolio
language distribution
activity
documentation signals
security signals
architecture summaries

Do not invent unavailable profile information.

============================================================
66. REPOSITORY COMPARISON ARTIFACTS
===================================

If existing snapshot comparison supports it:

generate:

Change Report

Sections:

Code changes
Architecture changes
Security changes
Dependencies
Documentation
Git activity

Only compare snapshots belonging to the same repository.

============================================================
67. ARTIFACT CHAT
=================

Existing repository chat should be able to answer:

"Summarize this report."

"Why is this section saying that?"

"Show the source."

"Regenerate the security section."

"What changed from the previous version?"

Artifact chat must remain evidence-based.

============================================================
68. MARKDOWN EXPORT
===================

Markdown should preserve:

headings
tables
links
source references
code blocks
diagrams where possible

============================================================
69. HTML EXPORT
===============

HTML should support:

responsive layout
table of contents
syntax highlighting where relevant
architecture diagrams
security tables
source links

Do not allow unsafe generated HTML/JS execution.

Sanitize output.

============================================================
70. PDF SECURITY
================

PDF must not contain:

raw secrets
OAuth tokens
API keys
internal auth headers

Validate before rendering.

============================================================
71. PPT SECURITY
================

Same rule.

Never put raw secret values into slides.

============================================================
72. LARGE REPORT HANDLING
=========================

For very large repositories:

avoid generating 500-page reports by default.

Use:

summary
appendix
top findings
top components
representative files

Allow detailed artifacts separately.

============================================================
73. APPENDICES
==============

Detailed artifacts may include appendices:

* dependency inventory
* security findings
* file inventory
* architecture nodes
* source references
* methodology
* limitations

============================================================
74. METHODOLOGY SECTION
=======================

Reports should explain:

Snapshot analyzed
Analysis engines
Scanner versions
Known limitations
Partial scans
Generated sections

This improves transparency.

============================================================
75. NO FABRICATED BUSINESS INFORMATION
======================================

Never invent:

customers
revenue
market size
business KPIs
users
SLAs
product strategy
company goals

unless explicitly present in repository/workspace data.

============================================================
76. NO FABRICATED REQUIREMENTS
==============================

For SRS/PRD:

distinguish:

Observed
Inferred
Proposed

Example:

Observed:
"Authentication uses GitHub OAuth."

Proposed:
"System should support SSO."

Never present the second as an existing capability.

============================================================
77. TESTING
===========

Add tests for:

Artifact creation
Artifact versioning
Snapshot association
Authorization
IDOR protection
Evidence collection
Structured LLM output
Schema validation
Source references
README generation
SRS
PRD
Architecture report
Security report
Executive report
PDF generation
PPTX generation
Markdown export
HTML sanitization
Artifact diff
Section regeneration
Failed generation
Retry
Large artifacts
Secret redaction
Private repository isolation

============================================================
78. PDF TESTING
===============

Verify:

* PDF opens
* page count > 0
* headings render
* tables render
* diagrams render
* no blank pages
* no broken characters
* metadata exists

============================================================
79. PPTX TESTING
================

Verify:

* PPTX opens
* slide count expected
* titles exist
* no empty slides
* no broken images
* text does not overflow where detectable

============================================================
80. ARTIFACT GENERATION SECURITY
================================

Generated content is untrusted.

Sanitize:

HTML
Markdown where rendered
file names
links
embedded images

Do not execute generated scripts.

Do not permit generated HTML to access application credentials.

============================================================
81. PERFORMANCE
===============

Use caching for:

documentation
architecture
security
metrics

Do not rerun full repository analysis just to generate a PDF.

Artifact generation should consume existing analysis results.

============================================================
82. FAILURE ISOLATION
=====================

If:

architecture data unavailable

the architecture section should say:

"Architecture analysis unavailable for this snapshot."

Do not fail the entire executive report unnecessarily.

Same for:

security
profile
documentation
deployment

============================================================
83. ARTIFACT GENERATION AUDIT
=============================

Record:

artifact generated
artifact regenerated
artifact exported
artifact archived

Include:

user
workspace
artifact
timestamp

Do not log sensitive artifact content.

============================================================
84. DATABASE INDEXES
====================

Index:

workspaceId
repositoryId
snapshotId
artifactType
status
createdAt
updatedAt

ArtifactVersion:

artifactId
snapshotId
version

ArtifactSource:

artifactVersionId

============================================================
85. FINAL UI
============

Workspace navigation should become:

Overview
Directory
Architecture
Security
Documentation
History
Artifacts
Chat

Artifacts becomes the central place for generated deliverables.

============================================================
86. PHASE 9 DEFINITION OF DONE
==============================

[ ] Artifact model exists

[ ] Artifact versioning exists

[ ] Artifact source/provenance exists

[ ] Artifact generation runs exist

[ ] Artifact Center exists

[ ] Artifact search/filter exists

[ ] Snapshot association works

[ ] Documentation artifacts integrate

[ ] Architecture artifacts integrate

[ ] Security artifacts integrate

[ ] Git history artifacts integrate

[ ] Profile artifacts integrate

[ ] SRS generation works

[ ] PRD generation works

[ ] ADR generation works

[ ] Technical design works

[ ] Architecture report works

[ ] Security report works

[ ] Codebase report works

[ ] Executive report works

[ ] Changelog works

[ ] Release notes work

[ ] README integrates with Phase 6

[ ] Markdown export works

[ ] HTML export works

[ ] PDF export works

[ ] PPTX export works

[ ] Artifact editing works

[ ] Artifact versioning works

[ ] Artifact diff works

[ ] Section regeneration works

[ ] Evidence/provenance works

[ ] Hallucination validation works

[ ] Secret redaction works

[ ] Private workspace isolation works

[ ] Artifact downloads are authorized

[ ] Background generation works

[ ] Retry works

[ ] Failure states work

[ ] Existing GitVision functionality remains intact

[ ] All tests pass

============================================================
87. DO NOT IMPLEMENT IN THIS PHASE
==================================

Do NOT implement:

* public artifact sharing
* public report URLs
* team collaboration
* comments/review workflows
* RBAC
* SSO
* billing
* Slack
* Teams
* webhooks
* CI/CD
* automated PR creation
* automatic code modification
* live deployment
* full observability platform

Those belong to later phases.

============================================================
88. FINAL VERIFICATION
======================

Run:

1. Existing test suite
2. Artifact tests
3. SRS generation
4. PRD generation
5. Architecture report
6. Security report
7. Executive report
8. Markdown export
9. HTML export
10. PDF generation
11. PPTX generation
12. Artifact versioning
13. Artifact diff
14. Section regeneration
15. Authorization tests
16. Secret redaction tests
17. Large repository test
18. Failed generation test
19. Snapshot comparison
20. Existing chatbot test

At completion report:

A. Files created
B. Files modified
C. Database migrations
D. Artifact models
E. Generation pipelines
F. Templates
G. API endpoints
H. UI components
I. PDF implementation
J. PPTX implementation
K. Tests
L. Known limitations
M. Manual verification
N. Architectural decisions

Do not rewrite unrelated systems.

Do not remove existing features.

Prefer incremental implementation.

````

## Phase 9 ke baad GitVision ka flow

```text
                 GITVISION
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
   Documentation Architecture  Security
        │            │            │
        └────────────┼────────────┘
                     ↓
              Evidence Layer
                     ↓
            Artifact Intelligence
                     │
       ┌─────────────┼──────────────┐
       ↓             ↓              ↓
   Documents       Reports      Presentations
       │             │              │
       ├─ README     ├─ SRS        ├─ PPTX
       ├─ Guide      ├─ PRD        ├─ Architecture
       ├─ API Docs   ├─ Security   ├─ Security
       ├─ ADR        ├─ Codebase   └─ Executive
       └─ Changelog  └─ Executive
                     │
                     ↓
               Artifact Center
````

### Important architectural principle

**LLM ≠ document renderer.**

LLM sirf structured content/evidence-backed narrative banayega:

```text
LLM
 ↓
Structured Artifact JSON
 ↓
Validation
 ↓
Deterministic Renderer
 ↓
PDF / PPTX / HTML / Markdown
```

Isse generated reports consistent rahenge aur same repository snapshot se PDF aur PPTX banane ke liye repository ko dobara analyze nahi karna padega.

### Roadmap

```text
Phase 1   AI Foundation                    ✅
Phase 2   Repository Workspace             ✅
Phase 3   GitHub Access                    ✅
Phase 4   Universal Ingestion + ZIP        ✅
Phase 5   GitHub Profile Intelligence      ✅
Phase 6   AI Documentation Engine          ✅
Phase 7   Advanced Architecture            ✅
Phase 8   Security 2.0                    ✅
Phase 9   Artifact Generation             ← NOW
Phase 10  Observability + Admin
Phase 11  Webhooks + CI/CD
Phase 12  Teams + RBAC
Phase 13  Enterprise + Scale
```