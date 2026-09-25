You are continuing development of the EXISTING GitVision application.

IMPORTANT:
Do NOT rebuild GitVision from scratch.

Phase 1 has already implemented the foundation for:

- OpenRouter AI provider
- AI provider abstraction
- configurable AI model
- streaming chatbot
- repository-aware context retrieval
- repository/file context selection
- conversation persistence
- AI request telemetry
- GitHub error handling
- prompt-injection protection
- repository isolation
- GitHub repository normalization
- repository context/cache foundation

Now implement PHASE 2:

============================================================
PHASE 2
REPOSITORY WORKSPACE + ANALYSIS HISTORY + SNAPSHOTS
============================================================

MAIN OBJECTIVE:

Turn each analyzed repository into a persistent GitVision workspace.

User flow:

GitHub URL
    ↓
Repository Analysis
    ↓
"Open Workspace"
    ↓
Repository Workspace
    ├── Overview
    ├── AI Chat
    ├── Analysis History
    ├── Notes
    ├── Security
    ├── Architecture
    ├── Reports
    └── Repository Information

Every workspace must belong to exactly one repository.

A user must NEVER see another user's private repository data.

============================================================
0. FIRST AUDIT EXISTING PHASE 1
============================================================

Before coding:

Inspect the Phase 1 implementation.

Identify:

- repository model
- user model
- conversation model
- message model
- AI request model
- repository cache
- context service
- GitHub API service
- authentication
- existing dashboard routes
- existing report routes
- existing scanner routes
- existing architecture routes

Do not create duplicate models/services.

Reuse existing implementations.

If an equivalent entity already exists, extend it.

Do not destroy existing data.

Use database migrations.

============================================================
1. WORKSPACE CONCEPT
============================================================

Create the concept of a Repository Workspace.

A workspace represents the user's persistent working area around a repository.

Conceptually:

Workspace
    ↓
Repository
    ↓
Snapshots
    ↓
Analysis Runs
    ↓
Conversations
    ↓
Notes
    ↓
Reports / Artifacts

For Phase 2:

Workspace should support:

- repository identity
- owner/user
- latest analysis
- analysis history
- conversations
- notes
- repository status
- last synchronized time
- current snapshot

Future phases will add:

- generated PDF
- PPT
- SRS
- PRD
- documentation
- diagrams
- artifact history

Do NOT fully implement those future artifact generators yet.

============================================================
2. DATABASE MODEL
============================================================

Extend the database with appropriate models.

Suggested entities:

User
Repository
Workspace
RepositorySnapshot
AnalysisRun
AnalysisStage
Conversation
Message
Note

AIRequest should continue to exist from Phase 1.

============================================================
3. WORKSPACE MODEL
============================================================

Suggested:

Workspace

id
user_id
repository_id
name
description
created_at
updated_at
last_opened_at
is_archived

Constraints:

One user should not accidentally create duplicate active workspaces for the same repository unless the product explicitly supports multiple workspaces.

Use a unique constraint where appropriate.

Example:

(user_id, repository_id)

If the existing product architecture requires team workspaces later, design carefully so this can evolve into:

Organization
    ↓
Workspace
    ↓
Repository

but do not implement full organizations yet.

============================================================
4. REPOSITORY SNAPSHOTS
============================================================

This is a critical part of Phase 2.

An analysis must represent a specific version/state of a repository.

Create:

RepositorySnapshot

Fields:

id
repository_id
source
branch
commit_sha
snapshot_hash
created_at
file_count
total_loc
languages
metadata_json
status

source can currently be:

GITHUB

Future:

ZIP
GITLAB
LOCAL

Example:

Repository:

github:herin7/gitforme

Snapshot:

branch = main
commit_sha = abc123...
snapshot_hash = ...

The snapshot is the basis for analysis.

This allows future functionality:

"What changed since the previous scan?"

============================================================
5. ANALYSIS RUN
============================================================

Create a persistent analysis run entity.

Example:

AnalysisRun

id
workspace_id
repository_snapshot_id
triggered_by_user_id
status
started_at
completed_at
duration_ms
analysis_version
error_code
error_message
created_at

Statuses:

QUEUED
RUNNING
COMPLETED
FAILED
CANCELLED

Do not store sensitive error information in user-visible fields.

============================================================
6. ANALYSIS STAGES
============================================================

A repository analysis consists of multiple stages.

Create:

AnalysisStage

id
analysis_run_id
stage_name
status
started_at
completed_at
duration_ms
items_processed
error_code
metadata_json

Possible stages:

REPOSITORY_METADATA
FILE_TREE
SOURCE_FILES
DEPENDENCIES
GIT_HISTORY
ISSUES
PULL_REQUESTS
CONTRIBUTORS
DEPLOYMENTS
HOTSPOTS
SECURITY
ARCHITECTURE
CONTEXT_INDEX
FINALIZATION

Use the stages that match the existing implementation.

Do not run stages that already have equivalent results unnecessarily.

============================================================
7. ANALYSIS HISTORY
============================================================

Add a Repository History page.

Example:

/repositories/:repositoryId/history

or follow existing routing conventions.

Show:

Analysis #12
Status: Completed
Commit: a81f3d2
Branch: main
Started: ...
Duration: ...
Triggered by: user
Results: ...

Analysis #11
Status: Completed
Commit: 91abc22
...

Each analysis should be selectable.

User should be able to open an old analysis.

============================================================
8. HISTORY DETAIL
============================================================

When user opens an analysis:

Show:

Repository
Snapshot
Commit SHA
Branch
Created time
Duration
Analysis version
Status

Then sections:

Overview
Code Metrics
Architecture
Dependencies
Security
Hotspots
Git Activity
Contributors
AI Context

If an existing analysis result already exists, reuse it.

Do not rerun analysis just because the user opened history.

============================================================
9. CURRENT VS HISTORICAL DATA
============================================================

This is extremely important.

Do not accidentally show current repository data while user is viewing an old analysis.

For historical analysis:

Use the associated RepositorySnapshot and analysis results.

Example:

User opens analysis from:

2026-08-01
commit abc123

Then:

Architecture
Security
Dependencies
Hotspots
Metrics

must represent that analysis where possible.

Do not silently replace it with today's values.

============================================================
10. ANALYSIS DIFF FOUNDATION
============================================================

Do not build a full visual diff system yet.

But create backend support for:

compare(snapshotA, snapshotB)

The comparison should eventually support:

- files added
- files removed
- files changed
- dependencies added
- dependencies removed
- vulnerabilities added
- vulnerabilities resolved
- architecture changes
- hotspot changes
- LOC changes
- language changes

For Phase 2:

Implement basic repository snapshot comparison.

At minimum support:

files added
files removed
files changed
LOC difference
dependency difference where existing data allows

Return structured JSON.

Example:

{
  "files": {
    "added": [],
    "removed": [],
    "modified": []
  },
  "metrics": {
    "locBefore": 10000,
    "locAfter": 10500,
    "locDelta": 500
  }
}

============================================================
11. WORKSPACE UI
============================================================

Create a dedicated workspace layout.

Suggested:

--------------------------------------------------
GitVision
--------------------------------------------------

Repository:
herin7/gitforme

[Overview] [Chat] [Architecture] [Security]
[History] [Reports] [Notes]

--------------------------------------------------
Main Content
--------------------------------------------------

The workspace should feel separate from the normal repository dashboard.

Do not create an entirely different design system.

Reuse existing GitVision components/styles.

============================================================
12. WORKSPACE OVERVIEW
============================================================

Create:

Workspace Overview

Display:

Repository name
Description
Visibility
Language
Stars
Forks
Default branch
Latest commit
Last analysis
Analysis status

Metrics:

Files
LOC
Dependencies
Vulnerabilities
Contributors
Open Issues
Pull Requests

Existing data should be reused.

Add:

"Open AI Chat"

"Run Analysis"

"View History"

buttons where appropriate.

============================================================
13. REPOSITORY STATUS
============================================================

Show current analysis state.

Examples:

Ready
Analyzing
Syncing
Failed
Outdated

If repository data has not been synchronized recently, indicate that.

Do not pretend stale data is current.

Example:

"Last analyzed 2 hours ago"

============================================================
14. ANALYSIS BUTTON
============================================================

Add:

"Analyze Repository"

or reuse existing "Cook" behavior.

Clicking it should create an AnalysisRun.

Flow:

POST /api/workspaces/:workspaceId/analyses

    ↓

create AnalysisRun
    ↓
QUEUED
    ↓
RUNNING
    ↓
analysis stages
    ↓
COMPLETED
    ↓
workspace latest_analysis updated

Do not block the HTTP request for a long repository analysis.

Use the existing job/background infrastructure if Phase 1 has one.

If no queue exists yet, introduce a clean abstraction:

AnalysisJobRunner

Future Phase can replace implementation with Redis/BullMQ/etc.

============================================================
15. JOB STATUS API
============================================================

Create:

GET /api/analyses/:analysisId

Return:

id
status
progress
currentStage
startedAt
completedAt
duration
error

Example:

{
  "status": "RUNNING",
  "progress": 62,
  "currentStage": "ARCHITECTURE"
}

Progress does not need to be mathematically exact.

It should be based on completed stages.

============================================================
16. REAL-TIME ANALYSIS PROGRESS
============================================================

If the current frontend/backend supports WebSocket/SSE, use it.

Otherwise implement polling first.

Frontend should show:

Analyzing repository...

[██████████------] 62%

Current stage:
Architecture analysis

Then:

✓ Metadata
✓ File tree
✓ Dependencies
✓ Git history
→ Architecture
○ Security

Do not make the UI fake progress.

Progress must reflect actual stages.

============================================================
17. NOTES
============================================================

Add repository-specific notes.

User should be able to write:

"Need to refactor authentication."

"Ask backend team about deployment."

"Review this dependency."

Notes belong to:

workspace

Suggested model:

Note

id
workspace_id
user_id
title
content
created_at
updated_at
deleted_at

Support:

Create
Edit
Delete
List

Do not mix notes into AI chat messages.

============================================================
18. CHAT INSIDE WORKSPACE
============================================================

Move/reuse the Phase 1 chatbot inside the workspace.

Example:

/workspace/:workspaceId/chat

or nested workspace route.

Chat must automatically know:

Current repository
Current workspace
Current snapshot/analysis where appropriate

The user should not have to paste the GitHub URL again.

============================================================
19. CHAT + SNAPSHOT
============================================================

When chatting against the latest analysis:

Use latest completed snapshot.

When user opens an historical analysis and clicks:

"Ask AI about this analysis"

the conversation should use that analysis/snapshot context.

This enables:

"What was the architecture like at this commit?"

Future Phase can add full historical chat.

Phase 2 should establish the correct IDs/context.

============================================================
20. CONVERSATION ISOLATION
============================================================

Strictly enforce:

User A
  └── Workspace A
       └── Repository A
            └── Conversations

User B must not access them.

Backend authorization must happen on EVERY workspace-related endpoint.

Never rely only on frontend hiding.

============================================================
21. AUTHORIZATION
============================================================

For every workspace route:

1. Authenticate user.
2. Find workspace.
3. Verify workspace belongs to user.
4. Verify repository relationship.
5. Only then perform action.

Do not trust:

workspaceId
repositoryId
conversationId

provided by frontend.

Validate ownership server-side.

============================================================
22. WORKSPACE ROUTES
============================================================

Adapt to the existing API style.

Suggested endpoints:

POST
/api/workspaces

GET
/api/workspaces

GET
/api/workspaces/:workspaceId

PATCH
/api/workspaces/:workspaceId

DELETE
/api/workspaces/:workspaceId

GET
/api/workspaces/:workspaceId/history

POST
/api/workspaces/:workspaceId/analyses

GET
/api/workspaces/:workspaceId/analyses

GET
/api/analyses/:analysisId

GET
/api/analyses/:analysisId/stages

GET
/api/workspaces/:workspaceId/notes

POST
/api/workspaces/:workspaceId/notes

PATCH
/api/workspaces/:workspaceId/notes/:noteId

DELETE
/api/workspaces/:workspaceId/notes/:noteId

Use existing route naming conventions if they differ.

============================================================
23. REPOSITORY PAGE BUTTON
============================================================

On the existing repository dashboard add:

[ Open Workspace ]

When clicked:

If workspace exists:
    open existing workspace

If workspace does not exist:
    create workspace
    open workspace

Do not create duplicate workspaces.

============================================================
24. REPOSITORY LIST
============================================================

If the current GitHub repository page/list already exists:

Add:

Open Workspace

to each repository.

Future Phase will build the full repository selector.

Do not rebuild that page now.

============================================================
25. REPORT FOUNDATION
============================================================

Existing Generate Report functionality must continue working.

Associate generated reports with:

workspace
analysis_run
repository_snapshot

This is important.

Example:

Report:
Repository Analysis Report

Generated from:
Analysis #14

Commit:
abc123

Future PDFs/PPTs will use the same architecture.

============================================================
26. ARTIFACT MODEL FOUNDATION
============================================================

Do not implement all artifact generation yet.

But create a generic artifact model if appropriate.

Example:

Artifact

id
workspace_id
analysis_run_id
type
name
status
storage_key
mime_type
created_by
created_at
metadata_json

Types can eventually include:

REPORT
PDF
PPT
SRS
PRD
README
API_DOC
ARCHITECTURE_DIAGRAM
SECURITY_REPORT

For Phase 2, existing reports can optionally be associated with this model.

Do not force a risky migration if the current report system is already structured differently.

============================================================
27. DELETE WORKSPACE / HISTORY
============================================================

User must be able to delete their workspace/history.

Implement safe deletion.

Important:

Deleting workspace must not accidentally delete:

- shared repository metadata
- another user's data
- GitHub repository
- GitHub files

Only GitVision's stored data should be deleted.

Define cascade relationships carefully.

If artifacts exist, clean them up.

============================================================
28. SOFT DELETE
============================================================

Prefer soft deletion where appropriate.

Example:

deleted_at

for:

Workspace
Note
Conversation
possibly AnalysisRun

However:

Do not overcomplicate the database.

Permanent deletion can be added later.

============================================================
29. AUDIT EVENTS FOUNDATION
============================================================

Create an audit event abstraction.

Examples:

WORKSPACE_CREATED
WORKSPACE_OPENED
ANALYSIS_STARTED
ANALYSIS_COMPLETED
ANALYSIS_FAILED
NOTE_CREATED
NOTE_UPDATED
NOTE_DELETED
CONVERSATION_CREATED
WORKSPACE_DELETED
REPORT_GENERATED

Suggested:

AuditEvent

id
user_id
workspace_id
repository_id
event_type
metadata_json
created_at

This will become the enterprise audit log in a later phase.

Do not expose sensitive information in metadata.

============================================================
30. ANALYSIS VERSIONING
============================================================

Every analysis should store:

analysis_version

Example:

2026.1

or an internal semantic version.

When the analysis algorithm changes:

2026.2

Historical results must remain understandable.

Do not overwrite old results blindly.

============================================================
31. DATA RETENTION
============================================================

Add configuration for retention.

Do not automatically delete user data in Phase 2 unless the existing product already has such behavior.

Prepare configuration:

ANALYSIS_RETENTION_DAYS=
CHAT_RETENTION_DAYS=
ARTIFACT_RETENTION_DAYS=

If unset:

No automatic deletion.

Future enterprise settings can control this.

============================================================
32. PERFORMANCE
============================================================

Do not make workspace loading execute expensive analysis.

Workspace GET should be fast.

Bad:

GET /workspace
    ↓
clone repository
    ↓
scan all files
    ↓
analyze architecture
    ↓
return response

Correct:

GET /workspace
    ↓
return stored workspace/latest analysis metadata

Analysis happens separately.

============================================================
33. CACHE STRATEGY
============================================================

Reuse Phase 1 repository cache.

Workspace should point to stored analysis data.

Do not duplicate all repository files into every workspace.

Repository data:

Repository
    ↓
Snapshots
    ↓
Analysis Runs
    ↓
Workspace references latest analysis

This avoids unnecessary duplication.

============================================================
34. DATABASE INDEXES
============================================================

Add indexes for common access patterns:

workspace.user_id
workspace.repository_id
workspace.updated_at

repository_snapshot.repository_id
repository_snapshot.commit_sha
repository_snapshot.created_at

analysis_run.workspace_id
analysis_run.repository_snapshot_id
analysis_run.status
analysis_run.created_at

analysis_stage.analysis_run_id

conversation.workspace_id
conversation.repository_id

message.conversation_id
message.created_at

note.workspace_id
note.created_at

Audit indexes:

user_id
workspace_id
event_type
created_at

Use indexes based on the actual database.

============================================================
35. FRONTEND ROUTING
============================================================

Add workspace route.

Example:

/workspace/:workspaceId

Suggested nested pages:

/workspace/:workspaceId
/workspace/:workspaceId/chat
/workspace/:workspaceId/history
/workspace/:workspaceId/architecture
/workspace/:workspaceId/security
/workspace/:workspaceId/reports
/workspace/:workspaceId/notes

If the existing router supports nested layouts, use it.

============================================================
36. BREADCRUMBS
============================================================

Workspace should have:

GitVision
→ Repositories
→ herin7/gitforme
→ Workspace

This should make navigation clear.

============================================================
37. LOADING / EMPTY / ERROR STATES
============================================================

Implement proper states.

Workspace loading:

Loading workspace...

No analysis:

"This repository has not been analyzed yet."

Failed analysis:

"Analysis failed."

[Retry]

No notes:

"No notes yet."

No history:

"No completed analyses yet."

Do not show blank screens.

============================================================
38. SECURITY
============================================================

Important:

A repository workspace may eventually contain private source code.

Therefore:

- authorization checks server-side
- no repository data in client logs
- no secrets in application logs
- no GitHub tokens in database
- no cross-user context retrieval
- no cross-workspace chat retrieval
- validate all IDs
- validate note content length
- validate chat input length
- rate limit expensive operations

============================================================
39. TESTING
============================================================

Create tests for:

WORKSPACE

1. create workspace
2. open workspace
3. duplicate workspace prevention
4. unauthorized workspace access
5. workspace deletion

SNAPSHOT

6. create snapshot
7. snapshot linked to repository
8. historical snapshot retrieval
9. snapshot isolation

ANALYSIS

10. create analysis run
11. stage tracking
12. successful completion
13. failed analysis
14. retry

HISTORY

15. latest analysis
16. historical analysis
17. historical data doesn't use latest snapshot accidentally

CHAT

18. workspace chat
19. conversation isolation
20. repository isolation
21. historical analysis context

NOTES

22. create note
23. update note
24. delete note
25. unauthorized note access

AUTH

26. user A cannot access user B workspace

============================================================
40. ACCEPTANCE TEST
============================================================

Perform this exact test:

1. Login to GitVision.

2. Open:

https://github.com/herin7/gitforme

3. Existing repository dashboard works.

4. Click:

Open Workspace

5. Workspace is created.

6. Workspace displays:

Repository
Latest Analysis
Metrics
Last Updated
Navigation

7. Click:

Analyze Repository

8. AnalysisRun is created.

9. UI shows real analysis progress.

10. Analysis completes.

11. History shows:

Analysis #1
Commit SHA
Date
Duration
Status

12. Run analysis again after repository changes/sync.

13. History now shows:

Analysis #1
Analysis #2

14. Open Analysis #1.

15. Historical information corresponds to Analysis #1.

16. Open Chat.

17. Ask:

"What changed between this analysis and the current repository?"

If comparison data is available, show the factual changes.

18. Create a note:

"Review authentication before next release."

19. Note appears in Notes.

20. Refresh.

21. Workspace, history, chat and note remain.

22. Log out.

23. Another account cannot access the workspace.

24. Existing GitVision features continue working.

============================================================
41. UI QUALITY
============================================================

The workspace should look like a serious developer tool.

Avoid:

- excessive animations
- unnecessary gradients
- huge cards
- dashboard clutter
- fake metrics
- placeholder data

Prefer:

- clean developer-tool UI
- clear hierarchy
- compact cards
- useful empty states
- responsive layout
- clear status indicators
- consistent GitVision design

Reuse existing UI components.

============================================================
42. DO NOT IMPLEMENT YET
============================================================

Do NOT implement the following fully in Phase 2:

- GitHub profile analyzer
- full private repository approval workflow
- ZIP upload
- GitLab
- full enterprise RBAC
- SSO
- Slack
- Teams
- CI/CD integration
- complete observability dashboard
- PDF generator
- PPT generator
- SRS generator
- PRD generator
- complete GitDocify-like documentation engine
- automatic GitHub webhooks
- PR review bot

Only create clean foundations/interfaces where required.

============================================================
43. PHASE 2 DEFINITION OF DONE
============================================================

Phase 2 is complete only when:

[ ] Repository Workspace exists
[ ] Open Workspace button exists
[ ] Workspace persistence works
[ ] Repository snapshots exist
[ ] Commit SHA is stored
[ ] AnalysisRun exists
[ ] Analysis stages are tracked
[ ] Analysis history page works
[ ] Historical analysis can be opened
[ ] Latest analysis is clearly identified
[ ] Basic snapshot comparison exists
[ ] Workspace chat uses correct repository
[ ] Historical analysis context is isolated
[ ] Notes work
[ ] Workspace authorization works
[ ] User isolation works
[ ] Existing reports are associated with analysis where practical
[ ] Artifact model foundation exists if compatible
[ ] Audit event foundation exists
[ ] Workspace deletion works safely
[ ] Database indexes added
[ ] Tests added
[ ] Existing Phase 1 functionality still works
[ ] Existing GitVision features still work

============================================================
44. FINAL IMPLEMENTATION REPORT
============================================================

After implementation, report:

1. Files created
2. Files modified
3. Database migrations
4. New models
5. New API endpoints
6. New frontend routes
7. New frontend components
8. Analysis pipeline changes
9. Snapshot implementation
10. History implementation
11. Notes implementation
12. Authorization implementation
13. Tests added
14. Existing features verified
15. Known limitations
16. Commands to run migrations
17. Commands to start the application
18. Any recommended Phase 3 prerequisites

DO NOT START PHASE 3.