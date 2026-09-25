You are continuing development of the EXISTING GitVision application.

IMPORTANT:
DO NOT rebuild GitVision.

DO NOT remove or break:

- GitHub OAuth
- Repository dashboard
- Repository analysis
- Workspace
- Analysis history
- Repository snapshots
- AI chatbot
- OpenRouter
- Existing reports
- OSV scanner
- Bulk scanner
- Architecture/dependency visualization
- FastClone
- Timeline
- Issues
- Contributors
- Deployments
- Hotspots

Phase 1 implemented the AI/provider/context foundation.

Phase 2 implemented:

- Repository Workspace
- Repository snapshots
- Analysis runs
- Analysis stages
- Analysis history
- Workspace chat
- Notes
- Workspace authorization
- Basic snapshot comparison
- Audit event foundation

Now implement:

============================================================
PHASE 3
GITHUB ACCOUNT + REPOSITORY SELECTOR +
PRIVATE REPOSITORY ACCESS
============================================================

MAIN OBJECTIVE:

When a user connects GitHub, GitVision should be able to show the repositories that the authenticated user is actually allowed to access.

User flow:

Login with GitHub
      ↓
GitHub Account
      ↓
"Repositories"
      ↓
Search / Filter / Sort
      ↓
Select Repository
      ↓
Permission Check
      ↓
Open/Create Workspace
      ↓
Analyze

The system must correctly handle:

PUBLIC repositories
PRIVATE repositories
ORGANIZATION repositories
repositories the user does not have permission to access

Never bypass GitHub permissions.

============================================================
1. FIRST AUDIT EXISTING GITHUB OAUTH
============================================================

Inspect the existing GitHub OAuth implementation.

Find:

- OAuth routes
- callback
- token handling
- user creation/login
- GitHub API client
- session/JWT mechanism
- existing scopes
- existing user model

DO NOT create a second authentication system.

Reuse the existing login flow.

If the existing OAuth implementation is insufficient for repository access, extend it safely.

============================================================
2. SEPARATE LOGIN FROM REPOSITORY ACCESS
============================================================

Architect the system so:

GitHub OAuth
    =
User identity/login

GitHub repository authorization
    =
Permission to access repositories

Do not assume:

"User logged into GitHub"
means
"user can access every repository."

Repository access must be verified through GitHub.

============================================================
3. GITHUB ACCOUNT MODEL
============================================================

Create or extend:

GitHubAccount

Suggested fields:

id
user_id
github_user_id
github_username
github_email
avatar_url
access_status
connected_at
last_synced_at
updated_at

Do not store raw GitHub tokens in plaintext.

If tokens must be persisted, use secure encrypted storage appropriate for the application's deployment.

Do not log tokens.

Do not return tokens to frontend.

============================================================
4. TOKEN SECURITY
============================================================

IMPORTANT:

Never:

- put GitHub access token in frontend state
- return token in API response
- log Authorization header
- store token in localStorage
- expose token through React
- send token to LLM
- include token in error messages

Create a GitHub API abstraction:

GitHubClient

The backend obtains credentials internally.

============================================================
5. REPOSITORY LIST API
============================================================

Create a backend endpoint using existing route conventions.

Example:

GET /api/github/repositories

Support pagination.

Response should include safe repository metadata:

id
name
full_name
owner
description
private
fork
archived
language
stars
forks
default_branch
updated_at
html_url
permissions
organization

DO NOT return access tokens.

============================================================
6. FETCH ALL ACCESSIBLE REPOSITORIES
============================================================

Do not assume the GitHub profile page contains the complete repository list.

Use GitHub's authenticated repository API.

Implement pagination.

For example:

page=1
per_page=100

then continue until all requested pages are processed.

Do not load an unlimited number of repositories into memory.

Support server-side pagination where possible.

============================================================
7. REPOSITORY SELECTOR UI
============================================================

Create:

"Your Repositories"

Example:

Repositories
────────────────────────────

Search repositories...

[All] [Public] [Private] [Organizations]

27 repositories

┌─────────────────────────────┐
│ gitforme                    │
│ JavaScript                  │
│ ★ 382   Forks 76            │
│ Public                      │
│                             │
│ [Open Workspace]            │
└─────────────────────────────┘

Each repository should have:

- name
- owner
- description
- visibility
- language
- stars
- forks
- updated time
- archived indicator
- access indicator

============================================================
8. SEARCH
============================================================

Repository selector should support:

Search by:

- repository name
- owner
- description

Search should be case-insensitive.

For many repositories, use debounced search.

Do not fetch every repository repeatedly on every keystroke.

============================================================
9. FILTERS
============================================================

Support:

All
Public
Private
Organization
Forks
Archived

Optional:

Recently updated

Language

Do not overcomplicate Phase 3.

============================================================
10. SORTING
============================================================

Support:

Recently updated
Name
Stars

Default:

Recently updated

Use server-side sorting where practical.

============================================================
11. REPOSITORY PERMISSION DATA
============================================================

For each repository, determine whether the authenticated user has the required access.

Where available, represent:

admin
push
pull

Example:

permissions:
{
  admin: false,
  push: true,
  pull: true
}

Do not expose unnecessary GitHub permission internals to users.

Instead show:

Can analyze
Read access
No access
Access required

============================================================
12. PUBLIC REPOSITORY FLOW
============================================================

Public repository:

User selects repository.

Flow:

Repository
    ↓
Permission check
    ↓
Accessible
    ↓
Create/open workspace
    ↓
Analyze

Public repositories should remain analyzable without unnecessary authorization barriers.

============================================================
13. PRIVATE REPOSITORY FLOW
============================================================

Private repository:

User selects repository.

If GitHub confirms access:

Private
✓ Access available

Allow:

Open Workspace
Analyze

If user does NOT have access:

Show:

"GitVision cannot access this private repository with your current GitHub permissions."

Then provide an appropriate GitHub authorization/access path.

Do NOT pretend GitVision can scan the repository before GitHub grants access.

============================================================
14. IMPORTANT: OWNER APPROVAL FLOW
============================================================

The product may eventually support:

"Request access from repository owner."

Do NOT implement a fake approval system where GitVision claims that an arbitrary repository owner can simply approve access.

GitHub permissions must remain authoritative.

If implementing a request feature:

Request
    ↓
GitVision records request
    ↓
Owner/admin receives request
    ↓
Actual GitHub permission/App installation
    ↓
GitVision verifies access
    ↓
Scan allowed

For Phase 3, implement only the foundation unless the existing GitHub integration already supports a real approval mechanism.

============================================================
15. GITHUB APP COMPATIBILITY
============================================================

Architect the system so GitHub App can later become the preferred repository-access mechanism.

Current architecture may use OAuth.

Future:

GitHub OAuth
    =
Login

GitHub App
    =
Repository access
Webhooks
Organization installation
Private repo access

Do not build a completely separate GitHub App system unless explicitly required for this phase.

Create an abstraction such as:

RepositoryAccessProvider

Implement:

GitHubOAuthAccessProvider

Future:

GitHubAppAccessProvider

============================================================
16. ORGANIZATION REPOSITORIES
============================================================

Support repositories owned by organizations where the authenticated user has access.

Display:

Owner:
my-org

Repository:
backend-service

Visibility:
Private

Organization repositories may have organization policies.

If access is blocked:

Show a clear message.

Do not bypass organization restrictions.

============================================================
17. ARCHIVED REPOSITORIES
============================================================

Archived repositories can be displayed.

Show:

Archived

Do not automatically prevent analysis unless GitHub permissions/API behavior requires it.

============================================================
18. FORKS
============================================================

Display fork status.

Example:

Fork of:
owner/original-repository

Allow analysis if accessible.

Do not accidentally treat a fork as the original repository.

Repository identity must include:

GitHub repository ID

not just:

owner/name

============================================================
19. GITHUB REPOSITORY MODEL
============================================================

Extend the existing Repository model.

Suggested fields:

id
github_repo_id
provider
owner_login
owner_type
name
full_name
html_url
description
visibility
private
fork
archived
default_branch
language
stars
forks
watchers
license
github_created_at
github_updated_at
github_pushed_at
last_synced_at

provider:

GITHUB

Future:

GITLAB

============================================================
20. REPOSITORY IDENTITY
============================================================

Use GitHub's stable repository ID as the external identity where available.

Do not rely only on:

owner/name

because repositories can be renamed.

Support:

github_repo_id

plus current:

owner/name

============================================================
21. USER ↔ REPOSITORY RELATIONSHIP
============================================================

Do not create a permanent relationship saying:

User owns repository.

Instead represent access appropriately.

Possible:

RepositoryAccess

id
user_id
repository_id
access_type
source
verified_at
expires_at

access_type:

READ
WRITE
ADMIN

source:

OAUTH
GITHUB_APP

Future organization/team access can be added.

============================================================
22. ACCESS CACHE
============================================================

Do not call GitHub for permission checking on every UI action.

Cache repository access information for a reasonable period.

However:

Before starting a private repository analysis, verify access again when appropriate.

Security-sensitive operations should not trust stale cache indefinitely.

============================================================
23. OPEN WORKSPACE FROM REPOSITORY SELECTOR
============================================================

When user clicks:

Open Workspace

backend should:

1. authenticate user
2. find GitHub account
3. verify repository access
4. find repository
5. create/update repository record
6. find workspace
7. create workspace if needed
8. return workspace

Frontend navigates to:

/workspace/:workspaceId

Do not create duplicate workspaces.

============================================================
24. ANALYZE BUTTON
============================================================

Repository selector may have:

[Open Workspace]

Inside workspace:

[Analyze Repository]

Do not trigger an expensive analysis just because the user opened the repository list.

============================================================
25. PRIVATE REPOSITORY DATA SECURITY
============================================================

Private repository source code is sensitive.

Never:

- send private repository data to frontend unnecessarily
- put private code in logs
- include private source code in analytics
- send source code to unrelated third-party APIs
- store raw GitHub token with repository records
- expose repository context across users

The OpenRouter provider must receive only the context necessary for the AI request.

============================================================
26. REPOSITORY SYNC
============================================================

Create a repository synchronization concept.

Example:

POST /api/repositories/:repositoryId/sync

Flow:

GitHub
   ↓
Permission check
   ↓
Fetch metadata
   ↓
Fetch tree
   ↓
Fetch required content
   ↓
Create RepositorySnapshot
   ↓
Analysis can run

Do not automatically perform expensive full analysis during a simple metadata sync.

============================================================
27. SYNC STATUS
============================================================

Repository should expose:

last_synced_at
sync_status

Statuses:

IDLE
SYNCING
COMPLETED
FAILED

UI:

Last synced:
5 minutes ago

or:

Syncing repository...

============================================================
28. RATE LIMIT HANDLING
============================================================

GitHub API has rate limits.

Implement a centralized GitHub API wrapper that tracks:

endpoint
status
latency
remaining rate limit
reset time

Do not duplicate rate-limit logic across services.

When rate limit is low:

show a meaningful error.

Example:

"GitHub API rate limit is temporarily exhausted. Try again after 14:20 UTC."

Do not expose raw API response.

============================================================
29. GITHUB API RETRIES
============================================================

Retry only appropriate failures.

Examples:

Retry:
temporary 5xx
network timeout

Do not blindly retry:

401
403 permission denied
404 repository unavailable

Use bounded retries.

Avoid request storms.

============================================================
30. REPOSITORY LIST CACHE
============================================================

Cache repository list where appropriate.

Store:

github_account.last_repo_sync

Repository metadata can be refreshed.

User should have:

Refresh repositories

button.

Do not fetch all repositories every page load if cache is still valid.

============================================================
31. FRONTEND ACCOUNT PAGE
============================================================

Create:

/github

or equivalent existing route:

GitHub Account

Display:

GitHub username
Avatar
Connection status
Last synchronized
Repository count

Buttons:

[Refresh Repositories]
[Disconnect GitHub]

Do not show access token.

============================================================
32. DISCONNECT GITHUB
============================================================

Implement safe disconnect behavior.

Disconnecting should:

- remove/revoke stored GitHub credential where applicable
- invalidate GitHub connection
- prevent future private repository access

Do NOT automatically delete historical analyses unless product requirements explicitly say so.

Historical GitVision data can remain according to retention policy, but future GitHub sync must fail until reconnect.

============================================================
33. REPOSITORY ACCESS ERROR UX
============================================================

Create clear messages.

404:

"Repository was not found or you don't have access to it."

Private without access:

"This private repository is not accessible through your connected GitHub account."

403:

"GitHub denied access to this repository."

Rate limit:

"GitHub API rate limit reached. Please try again later."

OAuth expired:

"Your GitHub connection needs to be refreshed."

============================================================
34. URL ANALYSIS COMPATIBILITY
============================================================

Existing flow:

Paste GitHub URL
    ↓
Analyze

MUST CONTINUE WORKING.

New flow:

GitHub account
    ↓
Select repository
    ↓
Analyze

Both should resolve to the same Repository entity.

Avoid duplicate records.

============================================================
35. REPOSITORY URL NORMALIZATION
============================================================

The following should resolve to the same repository:

https://github.com/user/repo

https://github.com/user/repo/

https://github.com/user/repo.git

github.com/user/repo

Use GitHub repository ID whenever possible.

============================================================
36. SECURITY / AUTHORIZATION TESTS
============================================================

Test:

1. User A can access own workspace.
2. User B cannot access User A workspace.
3. User A cannot access User B private repository through an ID.
4. Invalid repository ID fails safely.
5. Invalid workspace ID fails safely.
6. Expired GitHub connection is handled.
7. Private repo without access is blocked.
8. Public repo works.
9. Organization repo with permission works.
10. Organization repo without permission is blocked.
11. GitHub token never appears in API response.
12. GitHub token never appears in logs.

============================================================
37. REPOSITORY SELECTOR PERFORMANCE
============================================================

The repository list should remain usable for:

10 repositories
100 repositories
500 repositories
1000+ repositories

Use:

pagination
search
server-side filtering
server-side sorting

Avoid rendering thousands of cards simultaneously.

Use virtualization if necessary.

============================================================
38. UX DETAILS
============================================================

Repository card should contain:

[icon/avatar]

repository-name

owner/name

description

language

★ stars

forks

Public / Private

Updated X days ago

[Open Workspace]

For private:

🔒 Private

For archived:

Archived

For inaccessible:

Access required

============================================================
39. GITHUB PROFILE FOUNDATION
============================================================

Prepare the architecture for a future GitHub Profile Analysis page.

Do not implement the complete profile analyzer yet.

Store enough GitHub account metadata to later support:

Profile
Repositories
Languages
Stars
Forks
Activity
Contributions
Issues
Pull Requests
Projects

Future Phase will implement:

/profile/:username/analysis

Do not scrape GitHub HTML for the core implementation.

Use official GitHub APIs wherever possible.

============================================================
40. AUDIT EVENTS
============================================================

Extend Phase 2 audit events.

Add:

GITHUB_CONNECTED
GITHUB_DISCONNECTED
REPOSITORIES_SYNC_STARTED
REPOSITORIES_SYNC_COMPLETED
REPOSITORY_OPENED
REPOSITORY_ACCESS_DENIED
PRIVATE_REPOSITORY_ANALYSIS_STARTED
PRIVATE_REPOSITORY_ANALYSIS_COMPLETED
PRIVATE_REPOSITORY_ANALYSIS_FAILED

Do not store tokens or raw source code in audit metadata.

============================================================
41. OBSERVABILITY
============================================================

For GitHub API requests, record:

request_id
user_id
repository_id if known
endpoint
method
status_code
latency_ms
rate_limit_remaining
retry_count
success
error_category
created_at

Do not log:

Authorization header
OAuth token
private source code

This telemetry will later feed the company-grade monitoring dashboard.

============================================================
42. API DESIGN
============================================================

Use existing API conventions.

Suggested:

GET /api/github/account

GET /api/github/repositories

GET /api/github/repositories/:githubRepoId

POST /api/github/repositories/sync

POST /api/github/disconnect

GET /api/repositories/:repositoryId/access

POST /api/repositories/:repositoryId/sync

POST /api/repositories/:repositoryId/workspace

Adapt names to the existing project.

Do not create duplicate endpoints if equivalents already exist.

============================================================
43. DATABASE MIGRATIONS
============================================================

Use migrations.

Possible additions:

github_accounts
repository_access
repository_syncs

Extend:

repositories
users
audit_events

Do not destroy production data.

Add proper:

foreign keys
indexes
unique constraints

============================================================
44. TESTING
============================================================

Unit tests:

- URL normalization
- repository identity
- permission mapping
- pagination
- repository filtering
- repository sorting
- access cache
- rate limit handling
- error normalization

Integration tests:

- GitHub OAuth → account
- account → repositories
- repository → workspace
- private repo → permission check
- inaccessible repo → blocked
- workspace → analysis

Security tests:

- cross-user workspace access
- cross-user repository access
- token leakage
- authorization bypass
- IDOR
- private repo data leakage

============================================================
45. ACCEPTANCE TEST
============================================================

Test exact flow:

1. User logs into GitVision using GitHub.

2. User opens:

"My Repositories"

3. GitVision fetches authenticated accessible repositories.

4. UI shows repository count.

5. User searches:

gitforme

6. Repository appears.

7. User sees:

name
description
language
stars
forks
visibility
last updated

8. User clicks:

Open Workspace

9. Existing workspace opens if it exists.

10. Otherwise workspace is created.

11. User clicks:

Analyze Repository

12. GitVision verifies repository access.

13. Analysis starts.

14. Repository snapshot is created.

15. Analysis completes.

16. Workspace shows latest analysis.

17. User logs out.

18. Another account cannot access the workspace.

19. Test a private repository the user can access.

20. Private repository is successfully analyzed.

21. Test a private repository the user cannot access.

22. GitVision blocks access with a clear message.

23. Test existing URL-based repository analysis.

24. It still works.

============================================================
46. DO NOT IMPLEMENT YET
============================================================

Do NOT fully implement:

- GitHub Profile Analyzer
- ZIP upload
- GitLab
- complete GitHub App installation UI
- organization/team management
- RBAC
- SSO
- Slack/Teams
- CI/CD
- PR review bot
- complete observability dashboard
- PDF
- PPT
- SRS
- PRD
- GitDocify-style documentation generator

Those are future phases.

============================================================
47. PHASE 3 DEFINITION OF DONE
============================================================

[ ] Existing GitHub OAuth continues working
[ ] GitHub account entity exists
[ ] Secure credential handling exists
[ ] Repository API implemented
[ ] Repository pagination works
[ ] Repository search works
[ ] Repository filters work
[ ] Repository sorting works
[ ] Public repositories work
[ ] Private repositories with access work
[ ] Private repositories without access are blocked
[ ] Organization repositories are handled
[ ] Repository identity uses GitHub ID
[ ] URL-based analysis still works
[ ] Repository selector opens workspace
[ ] Duplicate workspaces prevented
[ ] Repository synchronization exists
[ ] Sync status exists
[ ] GitHub rate limits are handled
[ ] GitHub API telemetry exists
[ ] Disconnect GitHub works
[ ] Audit events exist
[ ] Authorization tests pass
[ ] Cross-user isolation tests pass
[ ] Existing Phase 1 features work
[ ] Existing Phase 2 features work

============================================================
48. FINAL REPORT
============================================================

After implementation report:

1. Files created
2. Files modified
3. Database migrations
4. New models
5. New API endpoints
6. GitHub OAuth changes
7. Repository selector implementation
8. Permission implementation
9. Private repository behavior
10. Rate-limit handling
11. Security improvements
12. Tests
13. Existing functionality verified
14. Known limitations
15. Environment variables
16. Commands to run
17. Recommended prerequisites for Phase 4

DO NOT START PHASE 4.