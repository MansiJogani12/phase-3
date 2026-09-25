You are working on GitVision, an AI-powered GitHub repository intelligence platform.

IMPORTANT:
GitVision already has substantial functionality implemented.

DO NOT rebuild or replace existing functionality.

Existing functionality includes:

1. GitHub OAuth/login
2. GitHub authenticated API access
3. Public GitHub repository analysis
4. Private repository access where GitHub permissions allow it
5. Repository workspace
6. Repository snapshots
7. Analysis runs/stages
8. AI repository chatbot
9. OpenRouter/provider abstraction
10. Repository context/retrieval
11. OSV vulnerability scanning
12. Deep repository insights
13. Hotspot analysis
14. Timeline/issues/contributors/deployments
15. Architecture/dependency analysis
16. ZIP repository ingestion
17. Repository file tree/file viewer
18. Security/redaction protections
19. Report generation
20. FastClone
21. Existing dashboard/repository UI

Read the existing codebase first.

Understand the current architecture, database schema, API conventions, authentication system, GitHub client, repository models, workspace system, analysis pipeline, UI components, styling system, and background-job architecture before modifying anything.

This phase must EXTEND the current architecture rather than create a parallel implementation.

==================================================
PHASE 5
GITHUB PROFILE INTELLIGENCE
==================================================

GOAL

Build a dedicated GitHub Profile Analysis system inside GitVision.

A user should be able to enter or select a GitHub username/account and get a structured profile intelligence dashboard based on data GitHub actually exposes.

The feature must support:

- public GitHub profile analysis
- authenticated GitHub profile analysis
- accessible private repositories
- organization repositories where permissions allow
- repository-level aggregation
- profile snapshots
- profile history
- repository activity metrics
- language distribution
- stars/forks aggregation
- documentation indicators
- repository health indicators
- security aggregation
- architecture aggregation where repository analysis exists
- AI-generated factual profile summaries
- links from profile repositories into existing GitVision workspaces
- historical profile comparison

DO NOT create subjective developer/career rankings.

Do not label someone as:

- best developer
- worst developer
- expert
- poor developer
- senior/junior
- highly skilled
- low skilled
- employable/not employable
- top developer

Instead, report measurable facts.

==================================================
1. FIRST: AUDIT THE EXISTING SYSTEM
==================================================

Before coding:

Inspect:

- GitHub OAuth implementation
- GitHub API client
- GitHub account/user model
- repository model
- repository access/authorization
- repository workspace
- repository snapshot
- analysis runs
- analysis stages
- existing repository metrics
- existing security scanner
- architecture analyzer
- existing reports
- existing AI provider
- existing frontend routing
- existing navigation/header
- existing design system
- database migrations
- background job/queue system if present
- caching system if present

Identify reusable services.

Do not duplicate:

- GitHub API clients
- authentication
- repository fetching
- repository analysis
- OSV scanning
- architecture analysis
- AI provider
- authorization
- workspace creation

Reuse existing implementations.

If an existing model already represents a GitHub repository, use it.

==================================================
2. PROFILE ARCHITECTURE
==================================================

Implement the following conceptual pipeline:

GitHub Profile
      ↓
Profile Snapshot
      ↓
Accessible Repositories
      ↓
Repository Metadata
      ↓
Existing Repository Analysis
      ↓
Profile Aggregation
      ↓
Profile Dashboard
      ↓
AI Profile Summary
      ↓
Profile Report / History

The profile system must not duplicate repository intelligence.

For example:

Profile
  └── Repository A
       └── existing Repository Workspace
            └── RepositorySnapshot
                 └── AnalysisRun

Profile
  └── Repository B
       └── existing Repository Workspace
            └── RepositorySnapshot

The profile layer should aggregate existing repository intelligence wherever possible.

==================================================
3. DATABASE MODEL
==================================================

Design database changes according to the existing ORM/schema conventions.

Introduce profile-specific persistence only where necessary.

Suggested entities:

GitHubProfile
ProfileSnapshot
ProfileRepository
ProfileAnalysisRun
ProfileMetrics
ProfileRepositoryMetrics
ProfileReport

Adapt names to the existing codebase conventions.

--------------------------------------------------
GitHubProfile
--------------------------------------------------

Possible fields:

- id
- githubUserId
- username
- login
- name
- avatarUrl
- bio
- company
- location
- blog
- email if GitHub exposes it and policy permits storage
- followers
- following
- publicRepositoryCount
- profileUrl
- createdAt
- updatedAt

Do not store information unnecessarily.

Respect GitHub privacy and application requirements.

--------------------------------------------------
ProfileSnapshot
--------------------------------------------------

Purpose:

Preserve the state of the profile at a point in time.

Possible fields:

- id
- profileId
- capturedAt
- source
- repositoryCount
- accessibleRepositoryCount
- publicRepositoryCount
- privateRepositoryCount if authorized
- totalStars
- totalForks
- activeRepositoryCount
- staleRepositoryCount
- archivedRepositoryCount
- languageDistribution
- metricsJson if existing schema uses JSON
- status

A snapshot must be immutable after completion wherever possible.

--------------------------------------------------
ProfileRepository
--------------------------------------------------

Represents repository membership/access at a profile snapshot.

Possible fields:

- id
- profileSnapshotId
- repositoryId
- githubRepositoryId
- ownerLogin
- name
- fullName
- visibility
- isPrivate
- isFork
- isArchived
- language
- stars
- forks
- openIssues
- createdAt
- updatedAt
- pushedAt
- defaultBranch
- snapshot metadata

Prefer references to the existing Repository entity instead of duplicating repository data.

--------------------------------------------------
ProfileAnalysisRun
--------------------------------------------------

Track profile analysis separately from repository analysis.

Possible stages:

- FETCH_PROFILE
- FETCH_REPOSITORIES
- NORMALIZE_REPOSITORIES
- CALCULATE_METRICS
- LOAD_REPOSITORY_ANALYSES
- AGGREGATE_SECURITY
- AGGREGATE_ARCHITECTURE
- GENERATE_AI_SUMMARY
- BUILD_REPORT
- COMPLETE

Each stage should have:

- status
- startedAt
- completedAt
- error
- metadata

Reuse the existing AnalysisRun/AnalysisStage infrastructure if it already supports this cleanly.

Do not create redundant job infrastructure.

==================================================
4. PROFILE DATA SOURCE
==================================================

Use official GitHub APIs through the existing GitHub client.

Do not scrape GitHub HTML for core profile data.

Support:

- public profile
- authenticated user
- accessible repositories
- organization repositories when permissions allow
- private repositories when authorized

Respect GitHub permissions.

Never assume that because a repository exists, the current user can inspect its contents.

The authoritative source of repository access is GitHub authorization.

==================================================
5. PAGINATION
==================================================

GitHub repository lists can be large.

Implement robust pagination.

Do not assume:

"first 30 repositories = complete profile"

Support:

- page size
- cursor/page pagination according to the current API implementation
- continuation
- large repository counts
- rate-limit awareness

The final profile aggregation must represent all repositories that were actually fetched.

If fetching is incomplete, explicitly mark the analysis as partial.

Never silently present partial data as complete.

==================================================
6. PUBLIC PROFILE ANALYSIS
==================================================

For a public username, retrieve available public profile information.

Display, where available:

- username
- display name
- avatar
- bio
- company
- location
- website/blog
- followers
- following
- public repositories
- public repository metadata

Then calculate:

- total stars received across analyzed repositories
- total forks
- language distribution
- repository activity
- archived repository count
- fork count
- stale repositories
- recently updated repositories
- repository age distribution
- repository visibility
- documentation indicators
- release/tag information where available
- issue/PR information where available
- repository health indicators

Do not treat unavailable information as zero.

Example:

BAD:
PRs = 0

when GitHub data was not fetched.

GOOD:
PR data = "Not available"

==================================================
7. AUTHENTICATED PROFILE ANALYSIS
==================================================

If the user is logged in with GitHub:

Use their authenticated GitHub token through the existing secure backend integration.

Analyze repositories they are actually authorized to access.

This may include:

- public repositories
- private repositories
- organization repositories
- repositories where they have collaborator access

Only analyze repositories GitHub says the user can access.

Do not bypass permissions.

Do not infer organization access.

Do not expose private repository data to another user.

==================================================
8. SECURITY / TOKEN RULES
==================================================

Critical.

Never send GitHub OAuth tokens to:

- frontend
- browser localStorage
- AI model
- OpenRouter
- logs
- analytics
- error messages

Never include Authorization headers in logs.

Profile analysis must preserve existing repository-level authorization.

A user must never be able to request:

GET /profile/someone-private-repo

and receive private repository data merely by knowing its name.

Every repository access must pass existing authorization checks.

==================================================
9. PROFILE METRICS
==================================================

Implement factual aggregate metrics.

Examples:

--------------------------------------------------
Repository metrics
--------------------------------------------------

- total repositories
- public repositories
- private repositories when authorized
- fork count
- archived repositories
- active repositories
- stale repositories
- recently created repositories
- recently updated repositories

Define activity windows explicitly.

For example:

Active:
repository updated within configurable N days.

Stale:
repository has not been updated for configurable N days.

Do not hardcode ambiguous language without documenting the threshold.

Make thresholds configurable.

Example:

PROFILE_ACTIVE_DAYS=90
PROFILE_STALE_DAYS=180

--------------------------------------------------
Stars / forks
--------------------------------------------------

Calculate:

- total stars
- median stars
- average stars
- total forks
- repositories receiving stars
- repositories receiving forks

Be explicit whether forked repositories are included.

Prefer excluding fork repositories from original-project portfolio aggregates unless there is a clear reason otherwise.

Document the calculation.

--------------------------------------------------
Languages
--------------------------------------------------

Calculate language distribution from available repository language data.

Support:

- language by repository count
- language by bytes if GitHub provides reliable data
- primary language distribution

Example:

JavaScript: 38%
TypeScript: 27%
Python: 21%
Other: 14%

Do not invent language percentages.

==================================================
10. ACTIVITY ANALYSIS
==================================================

Calculate descriptive activity metrics where data exists.

Possible metrics:

- repositories updated in last 30 days
- repositories updated in last 90 days
- repositories updated in last 180 days
- stale repositories
- commits over time
- PR activity
- issue activity
- release activity
- repository creation trend

For commit/PR/issue metrics:

Use actual fetched GitHub data.

If the API does not provide sufficient historical information, report the limitation.

Do not fake contribution graph numbers.

==================================================
11. PR / ISSUE ANALYSIS
==================================================

Where accessible, calculate:

- total PRs analyzed
- merged PRs
- closed-unmerged PRs
- open PRs
- merge rate
- average PR merge time
- median PR merge time
- total issues
- open issues
- closed issues
- issue closure time where data supports it

Always show the population/time period.

Example:

"PR merge rate: 84%, based on 50 analyzed closed PRs."

Not:

"Merge rate: 84%"

without context.

Avoid interpreting these metrics as developer quality.

==================================================
12. DOCUMENTATION ANALYSIS
==================================================

Aggregate existing repository information.

For each repository detect:

- README exists
- README size
- documentation directory
- API documentation
- setup instructions
- contribution guide
- license
- changelog
- examples

Possible aggregate metrics:

- repositories with README
- repositories without README
- repositories with license
- repositories with contribution guide
- repositories with documentation directory

Use existing repository ingestion/file analysis where available.

Do not perform expensive full analysis for every repository merely to render the profile.

==================================================
13. SECURITY AGGREGATION
==================================================

Reuse existing GitVision security analysis.

Do not create a second vulnerability scanner.

If a repository already has:

- OSV results
- secret findings
- dependency findings

aggregate them into profile-level metrics.

Example:

Security Overview

Repositories analyzed: 12
Repositories with dependency findings: 3
Total vulnerability findings: 7
Repositories requiring review: 2

Every finding must link back to the repository/workspace.

Do not claim that unscanned repositories are secure.

Correct:

"Security analysis available for 8 of 20 repositories."

Not:

"Profile security: clean"

when 12 repositories were never scanned.

==================================================
14. ARCHITECTURE AGGREGATION
==================================================

Reuse existing architecture analysis.

For repositories with architecture analysis available, aggregate:

- languages
- LOC
- file count
- component count
- internal dependencies
- external dependencies
- architecture risks
- central files
- dependency categories

Show:

"Architecture analysis available for X repositories."

Do not imply that all repositories have been analyzed.

Allow clicking into the existing repository architecture workspace.

==================================================
15. REPOSITORY HEALTH
==================================================

Create factual repository health indicators.

Possible indicators:

- README present
- license present
- recent activity
- archived status
- dependency vulnerabilities
- open issue count
- release activity
- test presence
- documentation presence
- CI configuration presence
- package manager
- framework
- language

Do not collapse these into a subjective "Developer Score".

Prefer:

Repository Health Signals

with individual evidence-backed indicators.

==================================================
16. PROFILE DASHBOARD
==================================================

Create a dedicated route.

Suggested:

/profile/:username

or

/profile/:username/analysis

If the existing router has a better convention, follow it.

Suggested layout:

--------------------------------------------------

PROFILE ANALYSIS

@username

[avatar]

Name
Bio
Website
Company
Location

Followers
Following
Repositories
Stars Received
Forks

[Refresh Profile]
[Analyze Profile]
[Compare History]

--------------------------------------------------

Overview
Repositories
Languages
Activity
Security
Architecture
Reports
History

--------------------------------------------------

OVERVIEW

Profile summary

Repository count
Active repositories
Stale repositories
Archived repositories
Stars
Forks

--------------------------------------------------

LANGUAGES

Language distribution visualization

--------------------------------------------------

ACTIVITY

30 days
90 days
180 days
1 year

Repository activity timeline

--------------------------------------------------

REPOSITORIES

Search
Filter
Sort

Columns:

Repository
Visibility
Language
Stars
Forks
Updated
Activity
Security
Docs
Workspace

--------------------------------------------------

SECURITY

Repositories analyzed
Repositories with findings
Total findings
Severity distribution

--------------------------------------------------

ARCHITECTURE

Repositories analyzed
Total LOC
Components
Dependencies

--------------------------------------------------

AI SUMMARY

Factual AI-generated summary based only on analyzed profile data.

--------------------------------------------------

HISTORY

Previous profile snapshots

--------------------------------------------------

17. REPOSITORY TABLE
==================================================

Build a useful repository explorer.

Support:

Search:
- repository name

Filter:
- public/private
- archived
- fork
- language
- active/stale
- security findings
- documentation status
- analyzed/not analyzed

Sort:
- stars
- forks
- updated
- created
- name
- activity

Each repository should provide:

[Open Workspace]

If workspace does not exist:

[Analyze Repository]

Do not automatically run expensive deep analysis for every repository when the profile page loads.

==================================================
18. PROFILE ANALYSIS STRATEGY
==================================================

Profile analysis should have two levels.

LEVEL 1:
LIGHTWEIGHT PROFILE ANALYSIS

Fetch:

- profile
- repository metadata
- languages
- stars
- forks
- dates
- visibility
- archive status
- basic metadata

Fast.

LEVEL 2:
DEEP PROFILE ANALYSIS

Optional explicit operation:

"Analyze Profile"

This can queue repository-level analysis.

Allow configurable limits.

Example:

Analyze:
[All repositories]
[Active repositories]
[Selected repositories]

If repository count is very large, process asynchronously.

Show:

Queued
Running
Completed
Failed
Skipped

Never freeze the browser waiting for dozens/hundreds of GitHub API requests.

==================================================
19. BACKGROUND JOBS
==================================================

Reuse the existing job/queue architecture.

If no queue exists, introduce a minimal background processing layer consistent with the existing stack.

Profile jobs should be:

- asynchronous
- retryable
- idempotent
- resumable
- rate-limit aware

Avoid duplicate analysis.

Example idempotency key:

profileId + profileSnapshotId + repositoryId + analysisType

A failed repository should not invalidate the entire profile analysis.

==================================================
20. RATE LIMIT HANDLING
==================================================

GitHub API rate limits are critical.

Before large analysis:

Check available rate limit where possible.

Handle:

- 403
- rate limit exhaustion
- secondary rate limits
- temporary GitHub failures
- network errors

Implement:

- retry with backoff
- Retry-After handling when available
- partial analysis state
- user-visible explanation

Example:

"Profile analysis completed partially because GitHub API rate limits were reached. 83 of 104 repositories were processed."

Do not silently omit repositories.

==================================================
21. PROFILE SNAPSHOTS
==================================================

Every completed profile analysis should create a snapshot.

Example:

Snapshot
Sep 25, 2026
104 repositories
8,420 stars
1,203 forks

Snapshot
Aug 10, 2026
98 repositories
7,920 stars
1,080 forks

Allow:

[View Snapshot]
[Compare]

==================================================
22. SNAPSHOT COMPARISON
==================================================

Implement factual historical comparison.

Compare:

- repository count
- repositories added
- repositories removed
- stars change
- forks change
- active repository count
- stale repository count
- language distribution
- archived repositories
- security findings
- documentation indicators
- release activity

Example:

Since previous snapshot:

Repositories: +6
Stars: +500
Forks: +123
Active repositories: +3
Repositories with README: +4

Repository changes:

+ repo-a
+ repo-b
- old-repo

Do not produce subjective conclusions.

==================================================
23. AI PROFILE SUMMARY
==================================================

Reuse the existing OpenRouter provider abstraction.

Create a dedicated profile-summary context builder.

Do NOT send unnecessary raw repository source code.

For the profile AI summary, prefer structured data:

- profile metadata
- repository metadata
- metrics
- language distribution
- activity metrics
- documentation signals
- security findings
- architecture summaries
- historical changes

The AI should produce factual statements only.

Example:

"The profile contains 42 accessible repositories. TypeScript and Python are the two most common primary languages by repository count. 17 repositories were updated within the last 90 days."

Good.

Avoid:

"This developer is excellent."

Avoid:

"This developer is highly skilled."

Avoid:

"This is a top-tier engineer."

The AI must not invent metrics.

==================================================
24. PROMPT INJECTION DEFENSE
==================================================

Repository READMEs, source code, comments, issue descriptions and other GitHub content are untrusted input.

Profile analysis must preserve existing prompt-injection defenses.

Never allow repository content to override system instructions.

Clearly separate:

SYSTEM INSTRUCTIONS

from:

PROFILE DATA

from:

REPOSITORY CONTENT

from:

USER REQUEST

When AI summarizes repository data, treat repository text as data, not instructions.

==================================================
25. AI CONTEXT FORMAT
==================================================

Build a structured profile context.

Example:

PROFILE:
username
followers
following

REPOSITORY SUMMARY:
total
public
private
archived
forks

LANGUAGES:
...

ACTIVITY:
...

DOCUMENTATION:
...

SECURITY:
...

ARCHITECTURE:
...

HISTORY:
...

REPOSITORIES:
...

Use deterministic structured serialization.

Avoid dumping an enormous unbounded JSON object into the model.

Apply token budgeting.

==================================================
26. PROFILE REPORT
==================================================

Integrate with the existing report system.

Add a profile report type.

Suggested sections:

1. Profile Overview
2. Repository Portfolio
3. Language Distribution
4. Activity
5. Repository Health Signals
6. Documentation Signals
7. Security Summary
8. Architecture Summary
9. Historical Changes
10. AI-generated factual summary
11. Data limitations

Reports must clearly state:

- analysis date
- repositories analyzed
- repositories skipped
- data availability
- private repository scope
- partial-analysis status

Do not call the report a "developer scorecard".

==================================================
27. NAVIGATION
==================================================

Add Profile Analysis to the existing GitVision navigation.

Possible:

Dashboard
Repositories
Profile Analysis
Scanner
History

Respect the existing navigation structure.

For authenticated users:

[Analyze My GitHub Profile]

For public profiles:

[Analyze GitHub Profile]

Do not require login for public-profile metadata analysis unless existing product requirements require it.

==================================================
28. WORKSPACE INTEGRATION
==================================================

Profile repositories must integrate with the existing repository workspace.

For each repository:

If existing workspace exists:

[Open Workspace]

Otherwise:

[Analyze Repository]

When opening a workspace, preserve:

- repository identity
- snapshot
- analysis history
- security
- architecture
- chatbot
- reports

Do not create duplicate repository workspaces for the same GitHub repository.

GitHub repository ID should remain the canonical identity where possible.

==================================================
29. PROFILE CACHE
==================================================

Do not hit GitHub APIs on every page load.

Reuse existing repository caching infrastructure.

Cache:

- profile metadata
- repository metadata
- language data
- timestamps
- rate limit information where appropriate

Use TTLs appropriate to the data.

Allow:

[Refresh]

to explicitly request fresh data.

Never allow stale cache to appear as newly fetched data.

Show:

Last analyzed:
2 hours ago

==================================================
30. API DESIGN
==================================================

Follow existing API conventions.

Potential endpoints:

GET /api/profiles/:username

GET /api/profiles/:username/repositories

POST /api/profiles/:username/analyze

GET /api/profiles/:username/analysis/:runId

GET /api/profiles/:username/snapshots

GET /api/profiles/:username/snapshots/:snapshotId

GET /api/profiles/:username/compare/:snapshotA/:snapshotB

GET /api/profiles/me

POST /api/profiles/me/analyze

Adapt naming to existing API conventions.

Every endpoint must enforce authorization.

==================================================
31. ERROR STATES
==================================================

Handle:

- GitHub username does not exist
- GitHub API unavailable
- rate limit
- insufficient permission
- private repository inaccessible
- repository deleted
- repository renamed
- repository moved
- partial profile fetch
- analysis failure
- AI failure
- timeout

Example:

"Profile found, but 12 repositories could not be analyzed because the current GitHub authorization does not provide access."

Do not present inaccessible repositories as empty/zero-data repositories.

==================================================
32. PRIVACY
==================================================

Private repository data is sensitive.

Rules:

- tenant/user isolation
- workspace authorization
- encrypted credential handling
- no raw OAuth token storage in normal application logs
- no private source sent to AI unless the existing repository AI feature explicitly permits it
- no cross-user profile leakage
- no private repository names exposed through public profile endpoints
- no private security findings exposed to unauthorized users

If an authenticated user analyzes their private repositories, only that authorized user and explicitly authorized workspace members may access the result.

==================================================
33. AUDIT EVENTS
==================================================

Reuse existing audit event infrastructure.

Track important events:

- PROFILE_ANALYSIS_STARTED
- PROFILE_ANALYSIS_COMPLETED
- PROFILE_ANALYSIS_FAILED
- PROFILE_REFRESHED
- PROFILE_SNAPSHOT_CREATED
- PROFILE_REPORT_GENERATED

Do not log secrets.

==================================================
34. FRONTEND UX
==================================================

The UI should feel consistent with existing GitVision.

Avoid creating a completely different design system.

Use existing:

- cards
- tabs
- tables
- badges
- charts
- loading states
- dialogs
- typography
- spacing
- dark/light theme

Important states:

Initial:
"Enter a GitHub username"

Loading:
"Fetching profile..."

Repository loading:
"Loading repositories..."

Deep analysis:
"Analyzing repositories 24 / 104"

Partial:
"Analysis completed with 8 repositories unavailable"

Complete:
"Profile analysis completed"

==================================================
35. VISUALIZATIONS
==================================================

Use useful visualizations, not decoration.

Suggested:

1. Language distribution
2. Repository activity timeline
3. Stars/forks distribution
4. Repository age distribution
5. Security finding distribution
6. Documentation coverage
7. Snapshot comparison

Charts must have clear labels and units.

Avoid charts implying subjective quality.

==================================================
36. ACCESS CONTROL TESTING
==================================================

Test:

User A cannot access User B's private profile analysis.

User A cannot access User B's private repository analysis.

Public profile data remains public.

Authenticated private repository data requires authorization.

Organization repositories require appropriate GitHub access.

Profile workspace access follows existing workspace permissions.

==================================================
37. TESTING
==================================================

Add automated tests for:

PROFILE FETCHING

- public profile
- nonexistent username
- authenticated profile
- profile update

REPOSITORIES

- pagination
- many repositories
- private repositories
- organization repositories
- forks
- archived repositories
- renamed repositories
- deleted repositories

METRICS

- stars aggregation
- forks aggregation
- language distribution
- active/stale calculation
- documentation metrics
- security aggregation
- architecture aggregation

HISTORY

- snapshot creation
- snapshot comparison
- repository additions
- repository removals
- metric changes

SECURITY

- cross-user access
- private repo isolation
- token protection
- authorization failures

RELIABILITY

- GitHub API timeout
- rate limit
- retry
- partial analysis
- failed repository analysis

AI

- profile summary uses structured context
- no fabricated metrics
- prompt injection defense
- token budget enforcement

==================================================
38. PERFORMANCE
==================================================

Profile analysis may involve hundreds of repositories.

Avoid:

- N+1 database queries
- N+1 unnecessary GitHub API calls
- repeated repository analysis
- synchronous long-running HTTP requests

Use:

- batching
- caching
- pagination
- background jobs
- existing repository snapshots
- existing analysis results
- database indexes

A profile page should load quickly from stored snapshot data.

The page should not trigger a complete fresh GitHub scan merely because it was opened.

==================================================
39. DATABASE INDEXES
==================================================

Add indexes appropriate for:

- githubUserId
- username
- profileId
- profileSnapshotId
- repositoryId
- githubRepositoryId
- capturedAt
- analysis status

Avoid duplicate indexes already present.

==================================================
40. DOCUMENTATION
==================================================

Update developer documentation.

Document:

- profile architecture
- GitHub API dependencies
- permission model
- profile metrics definitions
- active/stale thresholds
- snapshot behavior
- partial analysis behavior
- caching
- background processing
- rate limits
- security/privacy
- AI context rules

==================================================
41. DO NOT IMPLEMENT IN THIS PHASE
==================================================

Do NOT implement:

- GitDocify-style full documentation engine
- PDF/PPT/SRS/PRD generation beyond minimal profile report integration
- full SBOM engine
- full SAST
- full secrets platform
- GitLab integration
- GitLab profile analysis
- webhooks
- CI/CD integration
- Slack/Teams integrations
- enterprise RBAC
- SSO/SAML
- billing
- organization/team management
- full observability dashboard
- replacement of existing repository architecture engine
- replacement of existing OSV scanner

Those belong to later phases.

==================================================
42. IMPORTANT PRODUCT PRINCIPLE
==================================================

GitVision is a repository intelligence product, not a social-profile ranking engine.

The profile feature should answer:

"What repositories and technical activity are visible on this GitHub profile, and what measurable characteristics can GitVision derive from the available data?"

It should NOT answer:

"How good is this developer?"

Keep the entire implementation evidence-based and descriptive.

==================================================
43. DEFINITION OF DONE
==================================================

Phase 5 is complete only when:

[ ] Public GitHub profiles can be analyzed

[ ] Authenticated GitHub profiles can be analyzed

[ ] Accessible private repositories are supported

[ ] Organization repositories respect GitHub permissions

[ ] Repository pagination works

[ ] Profile snapshots are persisted

[ ] Profile history works

[ ] Snapshot comparison works

[ ] Repository aggregation works

[ ] Stars/forks metrics work

[ ] Language distribution works

[ ] Activity metrics work

[ ] Active/stale thresholds are documented

[ ] Documentation signals work

[ ] Existing security findings can be aggregated

[ ] Existing architecture analysis can be aggregated

[ ] Repository table supports search/filter/sort

[ ] Repository → Workspace navigation works

[ ] Missing workspace → Analyze Repository works

[ ] Profile AI summary uses structured evidence

[ ] AI cannot fabricate unavailable metrics

[ ] Prompt injection protection is preserved

[ ] GitHub tokens never reach frontend/LLM/logs

[ ] Cross-user authorization tests pass

[ ] Private repository isolation tests pass

[ ] GitHub rate-limit handling works

[ ] Partial analysis is represented correctly

[ ] Background processing works for large profiles

[ ] Profile cache works

[ ] Refresh works

[ ] Profile reports work

[ ] Audit events exist

[ ] Existing GitVision repository functionality still works

[ ] Existing scanner still works

[ ] Existing chatbot still works

[ ] Existing architecture analysis still works

[ ] Existing ZIP analysis still works

[ ] Existing OAuth still works

[ ] No major regression is introduced

==================================================
44. FINAL IMPLEMENTATION REQUIREMENT
==================================================

Before finishing:

1. Run the existing test suite.
2. Add Phase 5 tests.
3. Run database migrations.
4. Verify development database.
5. Verify production build.
6. Verify frontend routing.
7. Verify API authorization.
8. Verify GitHub pagination.
9. Verify private repository isolation.
10. Verify rate-limit behavior.
11. Verify profile snapshot creation.
12. Verify snapshot comparison.
13. Verify AI profile summary.
14. Verify existing repository features.

At the end provide:

A. Files created
B. Files modified
C. Database migrations
D. New API endpoints
E. New frontend routes/components
F. New background jobs
G. New environment variables
H. Tests added
I. Known limitations
J. Manual verification steps
K. Any architectural decisions made

Do not silently change unrelated existing behavior.

Do not remove existing functionality.

Do not rewrite the application unnecessarily.

Prefer small, composable changes that fit the current GitVision architecture.