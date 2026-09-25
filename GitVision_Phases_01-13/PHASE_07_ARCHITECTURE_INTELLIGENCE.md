You are working on GitVision, an AI-powered GitHub repository intelligence platform.

============================================================
PHASE 7 — ADVANCED ARCHITECTURE INTELLIGENCE
============================================================

GOAL

Upgrade GitVision's existing architecture/dependency analysis into a
production-grade Architecture Intelligence Engine.

The existing GitVision architecture functionality must remain intact.

DO NOT rewrite it from scratch.

Extend the current architecture analyzer, graph engine, visualization,
repository snapshot system, dependency analysis, file index, AI context
system, reports, and workspace UI.

The goal is to answer questions such as:

- What are the major components of this repository?
- How does data move through the system?
- Which modules are central?
- Which modules have high fan-in/fan-out?
- Where are the strongest coupling points?
- Are there circular dependencies?
- Which components are architectural boundaries?
- Which files are change-impact hotspots?
- What would be affected if a specific file/module changes?
- How did architecture change between two snapshots?
- Which dependencies are internal vs external?
- Which modules communicate across architectural boundaries?
- Which areas have unusually high complexity/coupling?
- Which parts of the system are entrypoints?
- Which external systems does the repository depend on?
- Which architectural risks are supported by actual graph evidence?

The system must remain evidence-based.

Do not invent architecture.

============================================================
1. EXISTING ARCHITECTURE FUNCTIONALITY
============================================================

GitVision already has architecture/dependency analysis.

Existing capabilities include concepts such as:

- Overview
- Components
- Dependencies
- Files
- Overview visualization
- Grouped visualization
- Detailed visualization
- Structure visualization
- Zoom
- Fit
- Center
- Reset
- Mermaid export
- SVG export
- PNG export
- Internal dependencies
- External dependencies
- Dependency categories
- LOC
- File count
- Language distribution
- Components
- Data flow
- Centrality
- Fan-in
- Fan-out
- Architecture risks

DO NOT remove these.

DO NOT replace the current UI with a completely unrelated system.

Build on top of it.

============================================================
2. FIRST: AUDIT THE CURRENT IMPLEMENTATION
============================================================

Before changing code inspect:

- architecture analyzer
- dependency parser
- file index
- symbol index
- repository snapshot
- language detection
- framework detection
- graph data structures
- component detection
- centrality calculation
- fan-in/fan-out calculation
- visualization components
- Mermaid generation
- SVG/PNG export
- architecture API endpoints
- repository workspace
- snapshot comparison
- AI context builder
- report generator
- database schema
- background jobs
- caching

Identify:

- what already exists
- what can be reused
- what is incomplete
- what is currently heuristic
- what is deterministic
- where architecture results are persisted

Do not create duplicate architecture services.

============================================================
3. ARCHITECTURE INTELLIGENCE MODEL
============================================================

Use this conceptual pipeline:

Repository Snapshot
       ↓
File Index
       ↓
Symbol / Import / Export Analysis
       ↓
Dependency Extraction
       ↓
Framework Detection
       ↓
Module / Component Detection
       ↓
Graph Construction
       ↓
Graph Algorithms
       ↓
Architecture Classification
       ↓
Risk Detection
       ↓
Change Impact Analysis
       ↓
Architecture Visualization
       ↓
AI Explanation

The architecture graph must be snapshot-specific.

Never mix files/dependencies from different snapshots.

============================================================
4. ARCHITECTURE GRAPH
============================================================

Represent architecture as a graph.

Nodes:

- repository
- application
- component
- module
- directory
- file
- symbol
- external package
- external service
- database
- queue
- API
- entrypoint

Edges:

- imports
- requires
- calls where detectable
- exports
- contains
- depends_on
- communicates_with
- reads
- writes
- routes_to
- invokes
- configured_by

Not every edge type will be available for every language.

Do not pretend an import edge is a runtime call edge.

Clearly distinguish:

STATIC DEPENDENCY

from:

INFERRED RUNTIME RELATIONSHIP

============================================================
5. EDGE CONFIDENCE
============================================================

Every non-trivial architecture relationship should have provenance.

Example:

{
  "type": "IMPORTS",
  "source": "src/api/user.ts",
  "target": "src/services/userService.ts",
  "confidence": "VERIFIED",
  "evidence": "import statement"
}

Possible confidence:

VERIFIED
INFERRED
HEURISTIC

Use VERIFIED whenever static source evidence directly supports the relationship.

============================================================
6. FILE-LEVEL DEPENDENCY GRAPH
============================================================

Build/extend a file dependency graph.

For each file:

- imports
- imported by
- exports
- imported symbols where available
- file size
- LOC
- language
- directory
- component
- test relationship
- entrypoint relationship

Store normalized paths.

Handle:

- relative imports
- aliases
- package imports
- index/barrel files
- extension resolution
- generated files
- ignored files

Reuse language-specific parsers where they already exist.

============================================================
7. SYMBOL-LEVEL ANALYSIS
============================================================

Where reliable parser support exists, identify:

- functions
- classes
- methods
- interfaces
- types
- exported symbols
- imported symbols

Do not require symbol-level analysis for every language.

If unsupported:

mark symbol data unavailable.

Do not fabricate symbols.

============================================================
8. COMPONENT DETECTION
============================================================

Extend existing component detection.

Components can be based on:

- directory boundaries
- package boundaries
- import clusters
- framework conventions
- configuration
- naming patterns
- dependency communities
- explicit monorepo packages

Example:

src/
  auth/
  users/
  billing/
  payments/

could produce:

Auth
Users
Billing
Payments

But this is a detected grouping, not necessarily an officially declared architecture.

Label appropriately:

"Detected component"

rather than:

"Official architecture component"

============================================================
9. COMPONENT CLASSIFICATION
============================================================

Where evidence allows, classify components:

- API
- UI
- service
- domain
- database
- infrastructure
- configuration
- authentication
- messaging
- integration
- worker
- CLI
- testing
- utility
- unknown

Classification must be evidence-backed.

Example:

A directory containing Express route definitions can be classified as:

API

with evidence.

If classification is uncertain:

Unknown

============================================================
10. ENTRYPOINT DETECTION
============================================================

Detect likely application entrypoints.

Possible evidence:

package.json main
package.json bin
scripts
index files
server startup files
main functions
CLI definitions
framework configuration
Docker CMD/ENTRYPOINT
worker startup
GitHub Actions entrypoints

For each entrypoint:

- path
- type
- framework
- confidence
- evidence

Example:

server/index.js
Type: HTTP Server Entry Point
Confidence: VERIFIED

============================================================
11. DATA FLOW
============================================================

Extend existing data-flow analysis.

Represent:

User/API Request
    ↓
Router
    ↓
Controller
    ↓
Service
    ↓
Repository/DAO
    ↓
Database

Where evidence exists.

Other flows:

Event
 ↓
Queue
 ↓
Worker
 ↓
Service

HTTP API
 ↓
External Service
 ↓
Response

Do not infer runtime execution merely from imports.

Clearly distinguish:

Detected static relationship

from:

Detected/inferred flow

============================================================
12. EXTERNAL DEPENDENCIES
============================================================

Categorize external dependencies.

Examples:

Database
Authentication
Cloud
Payments
Email
Messaging
Storage
Analytics
AI/LLM
Monitoring
Testing
Build
Framework
Utility

For every external dependency:

- package
- version if available
- category
- files using it
- component using it
- direct/transitive if detectable

Reuse dependency information from existing scanner.

============================================================
13. EXTERNAL SERVICES
============================================================

Detect configured external services from evidence such as:

- environment variables
- SDK usage
- configuration
- URLs
- Docker Compose
- infrastructure configuration

Examples:

PostgreSQL
Redis
S3
GitHub
Stripe
OpenAI
OpenRouter
SendGrid

Do not claim a service merely because a generic package exists.

Example:

Installing an AWS SDK does not prove that S3 is actually used.

Require usage/configuration evidence.

============================================================
14. DATABASE DETECTION
============================================================

Detect database systems where evidence exists.

Possible:

PostgreSQL
MySQL
MongoDB
Redis
SQLite
DynamoDB
etc.

Sources:

- ORM configuration
- connection code
- migrations
- Docker Compose
- environment variables
- drivers
- schema files

Display:

Database
Evidence
Used by components

Never expose credentials.

============================================================
15. DEPENDENCY CATEGORIES
============================================================

Improve current dependency categorization.

At minimum:

Runtime
Framework
Database
Authentication
Cloud
Storage
Messaging
Testing
Build
Linting
Formatting
Observability
AI/LLM
Security
Developer tooling
Unknown

Allow multiple categories when appropriate.

============================================================
16. GRAPH ALGORITHMS
============================================================

Implement/reuse deterministic graph analysis.

Metrics:

- fan-in
- fan-out
- in-degree
- out-degree
- PageRank or similar centrality
- betweenness centrality where practical
- closeness where useful
- connected components
- strongly connected components
- dependency depth
- graph density

Do not expose every mathematical metric by default.

Surface useful interpretations.

Example:

High fan-in:
"Many modules depend on this module."

High fan-out:
"This module depends on many modules."

High betweenness:
"This module sits between multiple dependency paths."

Do not automatically call such modules "bad."

============================================================
17. CIRCULAR DEPENDENCIES
============================================================

Detect cycles.

Example:

A → B
B → C
C → A

Display:

Circular dependency detected.

Cycle:
A → B → C → A

Provide:

- files
- components
- cycle length
- source evidence

Allow filtering:

File-level cycles
Component-level cycles

Do not count normal bidirectional relationships as a cycle unless graph traversal confirms it.

============================================================
18. ARCHITECTURAL BOUNDARIES
============================================================

Detect potential boundaries.

Examples:

UI
 ↓
API
 ↓
Service
 ↓
Repository
 ↓
Database

Flag cross-boundary dependencies.

Example:

UI → Database

If the repository architecture appears to have a service layer between them, this can be surfaced as:

"Detected direct dependency crossing the inferred service boundary."

Do not state that it violates a formal architecture unless the repository explicitly defines that architecture.

Use wording:

Potential boundary crossing

============================================================
19. COUPLING ANALYSIS
============================================================

Calculate:

- afferent coupling
- efferent coupling
- instability where meaningful
- component dependency count
- cross-component edge count
- dependency concentration

For component C:

Ca = incoming dependencies

Ce = outgoing dependencies

Instability:

I = Ce / (Ca + Ce)

Handle zero denominator.

Do not use mathematical metrics as a subjective quality score.

Explain what the metric means.

============================================================
20. CHANGE IMPACT ANALYSIS
============================================================

Build:

"What could be affected if this file/component changes?"

For selected node:

Direct dependents
Indirect dependents
Dependent components
Potentially affected entrypoints
Potentially affected tests
External integrations

Example:

Selected:
src/auth/authService.ts

Direct dependents:
- userController.ts
- sessionController.ts

Indirect dependents:
- apiRouter.ts

Affected components:
- Authentication
- API

The result should be graph-based.

Clearly label:

Potential impact

not:

Guaranteed runtime impact

============================================================
21. CHANGE IMPACT BY SNAPSHOT
============================================================

If GitVision has two snapshots:

Snapshot A
Snapshot B

Calculate:

Added nodes
Removed nodes
Changed dependencies
New cycles
Removed cycles
Changed centrality
Changed component boundaries
Changed external dependencies

Example:

Architecture Changes

+ PaymentService component
+ Redis dependency

Removed:
LegacyAuth

Dependency changes:
A → B added
C → D removed

Do not infer why a change happened unless Git history supports it.

============================================================
22. HOTSPOT + ARCHITECTURE CORRELATION
============================================================

Integrate existing code hotspot metrics.

For each architecture component:

- commit churn
- file count
- LOC
- dependency count
- centrality
- security findings
- recent changes

Identify evidence-backed combinations.

Example:

"Authentication component has high recent file churn and 14 incoming dependencies."

This is a factual correlation.

Do NOT automatically say:

"Authentication architecture is poor."

============================================================
23. ARCHITECTURE RISK ENGINE
============================================================

Create deterministic risk rules.

Examples:

HIGH_FAN_OUT

HIGH_FAN_IN

CIRCULAR_DEPENDENCY

HIGH_COMPONENT_COUPLING

DIRECT_DATABASE_ACCESS_FROM_UI

HIGH_CROSS_BOUNDARY_DEPENDENCY

ORPHAN_MODULE

LARGE_CENTRAL_MODULE

EXCESSIVE_EXTERNAL_DEPENDENCIES

SINGLE_ENTRYPOINT_CONCENTRATION

DUPLICATE_INTEGRATION

ARCHITECTURE_CHANGE_SPIKE

Each risk must contain:

- rule
- severity
- evidence
- affected nodes
- explanation
- source files
- snapshot

Example:

Risk:
Circular Dependency

Severity:
Medium

Evidence:
A → B → C → A

Affected:
3 components

============================================================
24. RISK SEVERITY
============================================================

Severity should represent structural significance, not business certainty.

Possible:

INFO
LOW
MEDIUM
HIGH

Do not call an architecture issue "critical" unless the existing product has a documented deterministic rule supporting that classification.

Every severity rule should be documented.

============================================================
25. ARCHITECTURE RECOMMENDATIONS
============================================================

Provide recommendations based on detected evidence.

Example:

Observed:
Component A depends directly on 11 modules.

Recommendation:
"Consider evaluating whether the responsibilities of Component A can be split."

Observed:
Circular dependency between A/B/C.

Recommendation:
"Review the dependency direction between these components."

Recommendations must be:

- evidence-backed
- optional
- clearly marked as recommendations

Do not present architectural opinions as facts.

============================================================
26. ARCHITECTURE EXPLORER
============================================================

Extend the existing architecture UI.

Suggested tabs:

Overview
Components
Dependencies
Data Flow
Files
Risks
Impact
History
External Systems

============================================================
27. ARCHITECTURE OVERVIEW
============================================================

Display:

Components
Files
LOC
Internal dependencies
External dependencies
Languages
Entrypoints
External services
Databases
Queues
Architecture risks

Use existing cards and styling.

============================================================
28. COMPONENT VIEW
============================================================

For each component:

Name

Type

Files

LOC

Incoming dependencies

Outgoing dependencies

Centrality

Fan-in

Fan-out

Recent churn

Security findings

Related external dependencies

Entrypoints

Tests

Actions:

[Explore]
[Impact]
[Source]

============================================================
29. DEPENDENCY VIEW
============================================================

Support filters:

Internal
External
Component
File
Runtime
Build
Database
AI
Cloud
Security

Search:

module/file/package

Clicking an edge should show evidence.

Example:

src/auth/authService.ts
  imports
src/db/userRepository.ts

Source:
authService.ts:12

============================================================
30. DATA FLOW VIEW
============================================================

Create a simplified architecture flow.

Example:

Request
 ↓
Router
 ↓
Controller
 ↓
Service
 ↓
Repository
 ↓
Database

Allow:

Overview
Detailed

Do not clutter the diagram with hundreds of nodes.

For large repositories:

collapse components by default.

============================================================
31. ARCHITECTURE GRAPH UX
============================================================

Existing controls must remain:

Zoom
Fit
Center
Reset
Download Mermaid
Download SVG
Download PNG

Add:

Search
Filter
Hide external dependencies
Group by component
Show labels
Show risks
Highlight impact
Highlight cycles

When selecting a node:

show a side panel.

============================================================
32. NODE DETAILS
============================================================

Node details should contain:

Name

Type

Path

Component

LOC

Language

Fan-in

Fan-out

Centrality

Dependencies

Dependents

Security findings

Recent churn

Tests

Source

Architecture risks

Change impact

============================================================
33. LARGE REPOSITORY PERFORMANCE
============================================================

Architecture graphs can become huge.

Implement:

- graph aggregation
- lazy loading
- component-level default view
- virtualized lists
- capped visualization nodes
- server-side filtering where useful
- cached graph analysis

Do not render 20,000 file nodes simultaneously.

For huge repositories:

Show:

"Showing component-level architecture."

Allow drilling into:

Component → files → symbols

============================================================
34. GRAPH CACHING
============================================================

Architecture analysis can be expensive.

Cache results by:

repository
snapshot
analysis version

Example key:

repositoryId:snapshotId:architecture:v2

When parser/rule version changes:

invalidate old architecture cache.

Never mix architecture results generated by incompatible analyzer versions.

============================================================
35. ANALYZER VERSIONING
============================================================

Persist:

architectureAnalyzerVersion

dependencyParserVersion

riskRulesVersion

This allows reproducibility.

Example:

Architecture Analyzer:
v2.3

Snapshot:
abc123

============================================================
36. MULTI-LANGUAGE SUPPORT
============================================================

Preserve current supported languages.

Architecture engine should be extensible.

Use parser adapters:

LanguageAdapter
  ├── JavaScriptAdapter
  ├── TypeScriptAdapter
  ├── PythonAdapter
  ├── JavaAdapter
  ├── GoAdapter
  ├── RustAdapter
  └── ...

Do not implement every language in this phase if the current engine does not support them.

Create the abstraction first.

============================================================
37. IMPORT RESOLUTION
============================================================

Improve import resolution where practical.

Support:

relative paths

aliases

index files

package exports

extensions

monorepo packages

workspace packages

Handle unresolved imports.

Store:

resolutionStatus

RESOLVED
UNRESOLVED
EXTERNAL

Do not force incorrect resolution.

============================================================
38. MONOREPO ARCHITECTURE
============================================================

Detect:

- workspace packages
- apps
- packages
- services
- shared libraries

Examples:

apps/web
apps/api
packages/ui
packages/config

Represent these as higher-level components.

Show:

App → Shared Package
API → Database
Worker → Queue

============================================================
39. TEST RELATIONSHIPS
============================================================

Detect relationships such as:

src/foo.ts
tests/foo.test.ts

Where naming/path conventions make the relationship reasonably reliable.

Show:

Tests:
foo.test.ts

Do not claim test coverage merely because a test file exists.

============================================================
40. ARCHITECTURE + SECURITY
============================================================

Integrate security findings into architecture.

Example:

Component:
Authentication

Security findings:
2 dependency vulnerabilities

Files:
authService.ts
tokenService.ts

This creates a combined architecture/security view.

Do not create a new security scanner.

============================================================
41. ARCHITECTURE + DOCUMENTATION
============================================================

Integrate with Phase 6 Documentation Engine.

Architecture page:

[Generate Architecture Documentation]

Generated documentation should link back to:

- components
- files
- diagrams
- dependencies
- risks

Documentation should use the same snapshot.

============================================================
42. ARCHITECTURE AI ASSISTANT
============================================================

Extend existing repository chatbot with architecture-aware context.

Questions:

"How does authentication work?"

"Why is this module central?"

"What depends on this service?"

"What happens if I change this file?"

"Explain the architecture."

"Where are the circular dependencies?"

"What are the external integrations?"

The AI must use actual architecture graph data.

Example context:

Selected node:
authService.ts

Dependencies:
...

Dependents:
...

Centrality:
...

Risks:
...

Source:
...

Do not allow AI to invent relationships absent from graph evidence.

============================================================
43. ARCHITECTURE EXPLANATION FORMAT
============================================================

AI architecture explanations should distinguish:

Verified:
Directly supported by graph/source.

Inferred:
Reasonable interpretation of evidence.

Unknown:
Not available.

Example:

Verified:
authController imports authService.

Inferred:
authService appears to coordinate authentication logic.

Unknown:
Whether this service is deployed independently cannot be determined from the repository.

============================================================
44. ARCHITECTURE REPORT
============================================================

Extend existing reports.

Include:

1. Architecture Overview
2. Technology Stack
3. Components
4. Dependencies
5. Data Flow
6. External Systems
7. Central Modules
8. Coupling
9. Cycles
10. Architecture Risks
11. Change Impact
12. Security Correlation
13. Architecture Changes
14. Recommendations
15. Data Limitations

All sections must be snapshot-specific.

============================================================
45. MERMAID GENERATION
============================================================

Preserve existing Mermaid export.

Improve diagrams where possible:

- component diagrams
- dependency graphs
- sequence/data-flow diagrams
- deployment-like diagrams when evidence supports them

Do not invent runtime infrastructure.

For large graphs:

generate simplified diagrams.

============================================================
46. ARCHITECTURE DIFF
============================================================

Create a dedicated architecture comparison.

Compare:

Snapshot A
vs
Snapshot B

Show:

Components:
Added
Removed
Changed

Dependencies:
Added
Removed

External services:
Added
Removed

Cycles:
Added
Resolved

Centrality:
Changed

Risk:
New
Resolved

Files:
Moved/added/removed where detectable

============================================================
47. FILE MOVE DETECTION
============================================================

Where Git history or content hashes allow:

detect likely renames/moves.

Example:

old:
src/auth/auth.js

new:
src/services/authService.js

Mark:

Likely rename/move

Do not claim certainty if Git history is unavailable.

============================================================
48. ARCHITECTURE TIMELINE
============================================================

Use existing timeline/history data.

Show major architecture events:

- new component
- removed component
- dependency spike
- external service added
- circular dependency introduced
- major file movement
- architecture risk introduced/resolved

These events should be derived from snapshot comparisons.

============================================================
49. API DESIGN
============================================================

Follow existing API conventions.

Possible endpoints:

GET /api/workspaces/:workspaceId/architecture

GET /api/workspaces/:workspaceId/architecture/components

GET /api/workspaces/:workspaceId/architecture/dependencies

GET /api/workspaces/:workspaceId/architecture/risks

GET /api/workspaces/:workspaceId/architecture/impact/:nodeId

GET /api/workspaces/:workspaceId/architecture/history

GET /api/workspaces/:workspaceId/architecture/compare

POST /api/workspaces/:workspaceId/architecture/analyze

Adapt to existing API patterns.

============================================================
50. DATABASE
============================================================

Reuse existing architecture persistence where possible.

If current storage is insufficient, introduce normalized entities such as:

ArchitectureAnalysis

ArchitectureNode

ArchitectureEdge

ArchitectureComponent

ArchitectureRisk

ArchitectureSnapshot

ArchitectureChange

But avoid unnecessary normalization if existing JSON storage is appropriate.

For large graphs, do not store enormous duplicated JSON blobs if the current DB design can be improved.

Consider:

- normalized nodes
- normalized edges
- compressed graph representation
- JSON metadata

Follow existing database conventions.

============================================================
51. AUTHORIZATION
============================================================

Architecture data follows repository/workspace permissions.

A user cannot access architecture data for a repository they cannot access.

Private repository architecture remains private.

Profile aggregation must not bypass workspace authorization.

============================================================
52. SECURITY
============================================================

Architecture source data is untrusted repository content.

Preserve:

- prompt injection protection
- secret redaction
- token protection
- path traversal protection
- ZIP safety
- authorization

Do not execute repository code to determine architecture.

Architecture analysis should be static by default.

============================================================
53. NO CODE EXECUTION
============================================================

DO NOT:

npm install

pip install

cargo build

go run

docker build

execute scripts

execute binaries

run repository applications

Architecture analysis must work statically.

If future dynamic analysis is introduced, it must be a separately isolated feature.

============================================================
54. OBSERVABILITY
============================================================

Track:

- architecture analysis duration
- parser duration
- files analyzed
- edges created
- unresolved imports
- graph size
- component count
- risk count
- cache hit/miss
- snapshot
- analyzer version
- errors

Never log:

- tokens
- secrets
- private source contents

============================================================
55. PERFORMANCE
============================================================

Test against:

Small repository
Medium repository
Large repository
Monorepo

Avoid:

- O(N²) operations where avoidable
- unnecessary repeated parsing
- repeated database writes
- rendering huge graphs
- recomputing unchanged snapshots

Use:

- graph algorithms
- batching
- indexes
- caching
- incremental analysis where possible

============================================================
56. INCREMENTAL ANALYSIS
============================================================

Where practical, compare:

previous snapshot

with:

current snapshot

Only reprocess changed files.

Reuse unchanged:

- file hashes
- parsed imports
- symbols
- dependency edges

Do not implement an overly complex incremental engine if existing infrastructure does not support it cleanly.

A stable architecture should remain extensible for future incremental analysis.

============================================================
57. TESTING
============================================================

Add tests for:

GRAPH

- node creation
- edge creation
- import resolution
- unresolved imports
- external dependencies
- components

ALGORITHMS

- fan-in
- fan-out
- centrality
- cycles
- connected components
- coupling
- impact

COMPONENTS

- component detection
- monorepo detection
- boundary detection

RISKS

- circular dependency
- high fan-out
- high coupling
- boundary crossing
- orphan modules

SNAPSHOTS

- architecture snapshot
- architecture diff
- added component
- removed component
- changed dependency
- resolved cycle

SECURITY

- private repository isolation
- secret redaction
- prompt injection

PERFORMANCE

- large graph
- large repository
- monorepo

UI

- graph filtering
- node selection
- impact view
- risk panel
- architecture history

============================================================
58. EXAMPLE TEST REPOSITORY
============================================================

Create fixtures representing:

A:

UI
 ↓
API
 ↓
Service
 ↓
Repository
 ↓
Database

B:

A → B
B → C
C → A

C:

UI → Database

D:

High fan-out service

E:

Monorepo:

apps/web
apps/api
packages/shared

Verify architecture analysis produces expected relationships.

============================================================
59. ARCHITECTURE RISK LANGUAGE
============================================================

Use careful language.

Good:

"Detected circular dependency."

"Component A has 17 outgoing dependencies."

"Potential boundary crossing detected."

"Module X is highly central in the dependency graph."

Bad:

"This architecture is terrible."

"This codebase is badly designed."

"This developer doesn't understand architecture."

"This system will definitely fail."

Architecture intelligence should describe evidence, not judge people.

============================================================
60. FRONTEND INFORMATION ARCHITECTURE
============================================================

Suggested:

Architecture
│
├── Overview
├── Components
├── Dependencies
├── Data Flow
├── Files
├── Risks
├── Impact
└── History

Top actions:

[Analyze]
[Compare Snapshots]
[Generate Docs]
[Export]

============================================================
61. ARCHITECTURE OVERVIEW CARDS
============================================================

Display:

Files
LOC
Components
Internal Dependencies
External Dependencies
Entrypoints
External Services
Databases
Cycles
Risks

Clicking a card should filter the architecture explorer.

============================================================
62. COMPONENT EXPLORER
============================================================

Table:

Component
Type
Files
LOC
Fan-in
Fan-out
Centrality
Dependencies
Risks

Search/filter:

Type
Risk
Language
High fan-out
High fan-in
Recently changed

============================================================
63. RISK EXPLORER
============================================================

Table:

Risk
Severity
Component
Evidence
Snapshot
Status

Filters:

Severity
Rule
Component
New
Resolved

Each risk:

[View Evidence]

============================================================
64. IMPACT EXPLORER
============================================================

User selects:

file/component/symbol

Then display:

Direct dependents
Indirect dependents
Affected components
Affected entrypoints
Related tests
External integrations

Use graph traversal.

Allow:

1 hop
2 hops
All reachable

Default to 2 hops for large graphs.

============================================================
65. ARCHITECTURE HISTORY
============================================================

Display snapshot timeline.

Example:

Sep 25
Architecture:
12 components
101 internal dependencies

Sep 18
Architecture:
11 components
96 internal dependencies

Change:

+ Payment component
+ Redis dependency
+ 5 internal edges

============================================================
66. EXPORTS
============================================================

Preserve existing:

Mermaid
SVG
PNG

Add where useful:

JSON architecture graph

JSON should include:

nodes
edges
components
risks
metadata
snapshot
analyzer version

Do not expose private data through unauthenticated export endpoints.

============================================================
67. AI ARCHITECTURE REPORT
============================================================

AI-generated architecture report should be grounded in:

- architecture graph
- components
- dependencies
- centrality
- risks
- data flow
- external services
- snapshot comparison

It must not fabricate:

- runtime behavior
- deployment topology
- business logic
- performance characteristics
- organizational ownership

============================================================
68. DOCUMENTATION INTEGRATION
============================================================

Phase 6 Documentation Engine should be able to request:

Architecture Documentation

using Phase 7 architecture results.

Architecture documentation should automatically include:

- component overview
- dependency structure
- data flow
- important modules
- architecture risks
- diagram

Source references should remain available.

============================================================
69. PROFILE INTEGRATION
============================================================

Phase 5 Profile Analysis may aggregate architecture metrics.

Examples:

Repositories with architecture analysis
Total components
Total dependencies
Architecture risks

Do not automatically deeply analyze every profile repository.

Only aggregate existing analysis.

============================================================
70. REPORT INTEGRATION
============================================================

Existing report generation should be extended, not replaced.

Allow:

[Generate Architecture Report]

Report must be linked to a repository snapshot.

============================================================
71. VERSIONING
============================================================

Architecture analysis results must record:

repository
snapshot
analyzer version
parser version
risk rules version
createdAt

This guarantees reproducibility.

============================================================
72. DATA LIMITATIONS
============================================================

Architecture UI should communicate limitations.

Examples:

"Runtime call relationships are not available from static analysis."

"Import resolution failed for 12 files."

"Symbol-level analysis is unavailable for this language."

"Architecture represents static repository evidence."

This is important.

============================================================
73. DEFINITION OF DONE
============================================================

Phase 7 is complete when:

[ ] Existing architecture UI still works

[ ] Existing Mermaid export works

[ ] Existing SVG export works

[ ] Existing PNG export works

[ ] File dependency graph is reliable

[ ] Component graph exists

[ ] External dependency graph exists

[ ] Entrypoint detection works

[ ] External service detection works where evidence exists

[ ] Database detection works where evidence exists

[ ] Fan-in works

[ ] Fan-out works

[ ] Centrality works

[ ] Cycle detection works

[ ] Component coupling metrics work

[ ] Architecture boundary detection works

[ ] Change impact analysis works

[ ] Snapshot architecture diff works

[ ] Added/removed dependencies are detected

[ ] Architecture risks are evidence-backed

[ ] Risk evidence is viewable

[ ] Hotspot correlation works

[ ] Architecture history works

[ ] Large graphs are handled efficiently

[ ] Graph caching works

[ ] Analyzer versioning exists

[ ] Architecture AI assistant is grounded

[ ] Documentation Engine integrates with architecture

[ ] Profile aggregation can consume architecture results

[ ] Architecture report works

[ ] Authorization works

[ ] Private repositories remain isolated

[ ] Prompt injection protection works

[ ] No repository code is executed

[ ] Tests pass

[ ] Existing GitVision features remain functional

============================================================
74. DO NOT IMPLEMENT IN THIS PHASE
============================================================

Do NOT implement:

- full SAST
- full SBOM
- container scanning
- IaC security scanning
- PDF/PPT generation
- SRS/PRD generation
- webhooks
- CI/CD integration
- Slack/Teams
- SSO/SAML
- enterprise RBAC
- billing
- GitLab architecture analysis
- runtime tracing
- production traffic tracing
- automatic code refactoring

Those belong to later phases.

============================================================
75. FINAL VERIFICATION
============================================================

Before finishing:

1. Run existing tests.
2. Run architecture tests.
3. Test small repository.
4. Test medium repository.
5. Test large repository.
6. Test monorepo.
7. Test circular dependencies.
8. Test unresolved imports.
9. Test external dependencies.
10. Test impact analysis.
11. Test snapshot comparison.
12. Test architecture risks.
13. Test private repository authorization.
14. Test architecture AI.
15. Test documentation integration.
16. Test graph exports.
17. Test existing repository workspace.
18. Test existing security scanner.
19. Test existing chatbot.
20. Test existing profile analysis.

At the end provide:

A. Files created
B. Files modified
C. Database migrations
D. Architecture data model
E. Graph algorithms added
F. API endpoints
G. Frontend routes/components
H. Background jobs
I. Cache strategy
J. Analyzer versioning
K. Tests added
L. Known limitations
M. Manual verification steps
N. Architectural decisions

Do not rewrite unrelated code.

Do not remove existing functionality.

Prefer incremental, composable changes.