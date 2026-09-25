You are working on GitVision, an AI-powered GitHub repository intelligence platform.

============================================================
PHASE 12 — TEAMS, ORGANIZATIONS, RBAC & COLLABORATION
============================================================

GOAL

Transform GitVision from a primarily individual-user platform into
a secure multi-user organization and team platform.

Users should be able to:

- create organizations
- invite members
- create teams
- assign team members
- manage workspace access
- manage repository access
- control security/architecture/documentation visibility
- collaborate on conversations
- collaborate on notes
- collaborate on artifacts
- review analysis history
- audit organization activity

The system must support strict tenant isolation.

============================================================
EXISTING SYSTEMS — DO NOT REBUILD
============================================================

GitVision already has:

- GitHub OAuth
- GitHub repository access
- Repository Workspace
- Repository Snapshots
- Analysis Runs
- Continuous Analysis
- Architecture Intelligence
- Security 2.0
- Documentation Engine
- Artifact Generation
- AI Chat
- GitHub Webhooks
- CI/SARIF
- Observability
- Audit infrastructure
- repository access controls

Reuse these.

Do not create parallel repository/workspace/security systems.

============================================================
1. MULTI-TENANT MODEL
============================================================

Introduce:

Organization

OrganizationMember

Team

TeamMember

WorkspaceMember

RepositoryAccess

Do not assume:

User = Organization

A user can belong to:

Organization A
Organization B

and also retain personal GitVision workspaces.

============================================================
2. PERSONAL WORKSPACE COMPATIBILITY
============================================================

Existing personal workspaces must continue working.

Example:

User
 ├── Personal Workspace
 └── Organization Workspace

Do not force existing users to migrate manually.

============================================================
3. ORGANIZATION MODEL
============================================================

Create:

Organization

Suggested fields:

- id
- name
- slug
- description
- avatarUrl
- createdBy
- createdAt
- updatedAt
- status

Status:

ACTIVE
SUSPENDED
ARCHIVED

Slug must be unique.

============================================================
4. ORGANIZATION MEMBERS
============================================================

Create:

OrganizationMember

Fields:

- id
- organizationId
- userId
- role
- status
- invitedBy
- joinedAt
- createdAt
- updatedAt

Statuses:

INVITED
ACTIVE
SUSPENDED
REMOVED

============================================================
5. ORGANIZATION ROLES
============================================================

Initial roles:

OWNER
ADMIN
MEMBER
VIEWER

Do not create dozens of roles.

============================================================
6. OWNER
============================================================

Owner can:

- manage organization
- manage billing placeholder
- manage members
- manage teams
- manage workspaces
- manage integrations
- manage organization settings
- transfer ownership
- delete/archive organization

Only explicit owner permissions.

============================================================
7. ADMIN
============================================================

Admin can:

- manage members
- manage teams
- manage workspaces
- manage repositories
- configure continuous analysis
- manage integrations
- inspect audit logs

Admin must not automatically become owner.

============================================================
8. MEMBER
============================================================

Member can:

- access assigned workspaces
- use repository intelligence
- run permitted analyses
- chat with repositories
- create notes
- create artifacts if allowed

Member cannot:

- manage organization members
- modify organization security settings
- transfer ownership

============================================================
9. VIEWER
============================================================

Viewer:

- read assigned repositories/workspaces
- view reports
- view architecture
- view security results
- view documentation

Viewer cannot:

- modify settings
- trigger destructive operations
- manage members

============================================================
10. PERMISSION SYSTEM
============================================================

Do not scatter role checks throughout controllers.

Create centralized authorization:

AuthorizationService

Example:

can(user, action, resource)

Actions:

VIEW_ORGANIZATION
MANAGE_ORGANIZATION
INVITE_MEMBER
REMOVE_MEMBER
MANAGE_TEAM
VIEW_WORKSPACE
EDIT_WORKSPACE
RUN_ANALYSIS
VIEW_SECURITY
MANAGE_SECURITY
VIEW_ARTIFACT
CREATE_ARTIFACT
EDIT_ARTIFACT
DELETE_ARTIFACT
VIEW_AUDIT_LOG
MANAGE_INTEGRATION

============================================================
11. RBAC + RESOURCE PERMISSIONS
============================================================

Organization role alone should not determine every resource.

Example:

User can be:

Organization MEMBER

but only have access to:

Workspace A

and not:

Workspace B

Therefore support:

Organization role
+
Workspace membership
+
Team membership
+
Repository access

============================================================
12. WORKSPACE MEMBERS
============================================================

Extend existing Workspace.

Create:

WorkspaceMember

Fields:

- workspaceId
- userId
- role
- invitedBy
- status
- createdAt

Roles:

OWNER
EDITOR
VIEWER

Do not duplicate OrganizationMember.

============================================================
13. WORKSPACE ACCESS
============================================================

Workspace owner:

full workspace management

Editor:

modify workspace content
run analysis
create/edit notes
create artifacts

Viewer:

read-only

============================================================
14. TEAM MODEL
============================================================

Create:

Team

Fields:

- id
- organizationId
- name
- slug
- description
- createdBy
- createdAt
- updatedAt

Unique within organization.

============================================================
15. TEAM MEMBERS
============================================================

Create:

TeamMember

Fields:

- teamId
- userId
- role
- joinedAt

Initial team roles:

LEAD
MEMBER

Do not create unnecessary hierarchy.

============================================================
16. TEAM ACCESS
============================================================

A team can be assigned to:

workspace
repository

Prefer workspace-level access.

Example:

Engineering Team
  ↓
Backend Workspace
  ↓
GitVision repositories

============================================================
17. TEAM INHERITANCE
============================================================

Access can be inherited:

Organization
 ↓
Team
 ↓
Workspace
 ↓
Repository

But never allow inheritance to bypass explicit restrictions.

Document precedence.

============================================================
18. ACCESS RESOLUTION
============================================================

Create:

AccessResolver

Input:

user
resource
action

Output:

ALLOW
DENY

Optionally:

reason

Example:

ALLOW
reason:
"Workspace membership"

or:

DENY
reason:
"No workspace access"

Do not expose sensitive authorization internals to users.

============================================================
19. DENY BY DEFAULT
============================================================

If access cannot be established:

DENY.

Never:

"probably allowed"

Never fall back to organization membership for private workspace access
unless policy explicitly says so.

============================================================
20. REPOSITORY ACCESS
============================================================

Existing repository access must be extended.

A repository can belong to:

personal workspace
organization workspace

Access must respect:

GitHub access
+
GitVision workspace access

Both are required for private source operations.

============================================================
21. GITHUB PERMISSION VS GITVISION PERMISSION
============================================================

Keep separate.

GitHub determines whether GitVision can fetch repository data.

GitVision determines whether a user can see/use that repository inside
the GitVision organization.

Do not assume GitHub membership automatically grants GitVision access.

============================================================
22. PRIVATE REPOSITORY ISOLATION
============================================================

Critical requirement:

User A must never access User B's private repository data.

Test:

repository metadata
source files
snapshots
security findings
architecture
documentation
chat
messages
artifacts
notes
AI context
logs

============================================================
23. TENANT ISOLATION
============================================================

Every tenant-scoped query must include authorization context.

Do not rely only on:

frontend filtering
hidden UI elements
route naming

Backend authorization is mandatory.

============================================================
24. DATABASE ISOLATION
============================================================

All organization-owned entities should contain or be resolvable to:

organizationId

Examples:

Workspace
Repository access
Conversation
Artifact
Security data
Notes
Audit events

Avoid ambiguous ownership.

============================================================
25. OWNERSHIP MODEL
============================================================

Define clearly:

User-owned

versus

Organization-owned

Example:

Personal Workspace:
ownerUserId

Organization Workspace:
organizationId

Do not create contradictory ownership fields.

============================================================
26. MIGRATION STRATEGY
============================================================

Existing records must migrate safely.

Existing users:

retain ownership.

Existing repositories:

retain current access behavior.

Existing conversations:

remain accessible to their current owner.

Do not silently expose existing data to organization members.

============================================================
27. ORGANIZATION CREATION
============================================================

UI:

Create Organization

Fields:

Organization name
Slug

After creation:

creator becomes OWNER.

============================================================
28. ORGANIZATION SWITCHER
============================================================

Header/sidebar should support:

Personal
Organization A
Organization B

Current organization/workspace context must be explicit.

Avoid accidental operations against the wrong organization.

============================================================
29. WORKSPACE SWITCHER
============================================================

Within organization:

Workspace A
Workspace B
Workspace C

Show workspace access clearly.

============================================================
30. ORGANIZATION DASHBOARD
============================================================

Create:

Organization Overview

Show:

Members
Teams
Workspaces
Repositories
Recent analyses
Security findings
Architecture changes
Recent activity

Do not create subjective organization health scores.

============================================================
31. MEMBER MANAGEMENT
============================================================

Organization Admin/Owner can:

invite
remove
suspend
restore
change role

Do not allow owner removal without ownership transfer.

============================================================
32. INVITATION MODEL
============================================================

Create:

OrganizationInvitation

Fields:

- id
- organizationId
- email
- role
- tokenHash
- invitedBy
- expiresAt
- acceptedAt
- revokedAt
- createdAt

Store only secure token representation.

Do not store raw invitation token if avoidable.

============================================================
33. INVITATION SECURITY
============================================================

Invitation tokens:

- random
- high entropy
- single-use
- expiring
- revocable

Never log raw invitation tokens.

============================================================
34. INVITATION FLOW
============================================================

Admin:

Invite user

↓
Invitation created

↓
User receives invitation

↓
User authenticates

↓
Accept

↓
OrganizationMember created

Invitation becomes:

ACCEPTED

============================================================
35. EXISTING ACCOUNT
============================================================

If invited email belongs to existing GitHub user:

attach organization membership.

Do not create duplicate user accounts.

============================================================
36. INVITE NON-REGISTERED USER
============================================================

Allow invitation before account exists.

After signup:

resolve invitation.

Do not automatically grant unrelated organization access.

============================================================
37. INVITATION EXPIRATION
============================================================

Expired invitation:

cannot be accepted.

Allow admin to:

revoke
resend

============================================================
38. TEAM MANAGEMENT UI
============================================================

Organization:

Teams

Create:

Engineering
Security
Frontend
Backend
Platform

Team page:

Members
Workspaces
Repositories
Settings

============================================================
39. TEAM ASSIGNMENT
============================================================

Admin can:

add member
remove member
assign workspace
remove workspace access

Keep operations auditable.

============================================================
40. TEAM-BASED WORKSPACE ACCESS
============================================================

Example:

Backend Team

→ Backend Workspace

All active team members inherit:

VIEW/EDIT

according to team policy.

============================================================
41. TEAM ACCESS LEVEL
============================================================

Team workspace assignment should support:

VIEW
EDIT

Do not create more than necessary.

============================================================
42. DIRECT VS TEAM ACCESS
============================================================

User may have:

direct access
team access

Effective permission should be computed.

If any valid path grants access:

ALLOW

unless explicit deny policy is introduced.

Do not introduce DENY rules in initial version unless required.

This keeps authorization understandable.

============================================================
43. ACCESS UI
============================================================

Workspace:

Access

Show:

People
Teams

Example:

People:

Alice — Editor
Bob — Viewer

Teams:

Backend — Editor
Security — Viewer

============================================================
44. ACCESS AUDIT
============================================================

Track:

member invited
member accepted
member removed
role changed
team created
team member added
workspace shared
workspace access removed
repository access changed

============================================================
45. SECURITY FINDINGS ACCESS
============================================================

Security findings are sensitive.

Workspace permission required.

Viewer:
read

Editor:
read

Admin:
read/manage according to policy

Do not expose private security findings to organization members
without workspace/repository access.

============================================================
46. SECRET FINDINGS
============================================================

Secret findings require extra protection.

Even users with repository access should only see:

location
type
masked representation
status

Never display full secret value.

============================================================
47. AI CHAT ACCESS
============================================================

Chat must inherit repository/workspace authorization.

Before loading context:

authorize user.

Before loading message history:

authorize conversation.

Before retrieving files:

authorize repository.

============================================================
48. AI DATA ISOLATION
============================================================

Critical:

User A conversation must not influence User B's repository context.

Do not share:

conversation memory
embeddings
retrieval indexes
cached context
LLM prompt cache

across unauthorized tenants.

============================================================
49. VECTOR/SEARCH ISOLATION
============================================================

If pgvector/FTS/search indexes exist:

every query must be tenant-scoped.

Example:

organizationId
workspaceId
repositoryId
snapshotId

Use multiple isolation dimensions where appropriate.

============================================================
50. ARTIFACT COLLABORATION
============================================================

Artifacts should support:

owner
workspace
createdBy
updatedBy

Workspace members with permission can view.

Editors can modify where permitted.

============================================================
51. ARTIFACT EDIT LOCKING
============================================================

Do not implement complex real-time collaboration yet.

Use optimistic concurrency.

Artifact version:

versionNumber

updatedAt

If stale edit:

return conflict.

============================================================
52. ARTIFACT VERSION HISTORY
============================================================

Existing ArtifactVersion remains.

Add:

createdBy
changeReason

Allow:

compare versions
restore version

Restore creates a new version.

Do not delete historical versions.

============================================================
53. NOTES COLLABORATION
============================================================

Notes should support:

author
workspace
visibility

Initial visibility:

WORKSPACE

Optionally:

PRIVATE

if existing architecture supports it.

Do not expose private notes to workspace members.

============================================================
54. CONVERSATIONS
============================================================

Repository conversations should have:

workspaceId
repositoryId
createdBy

Access follows workspace/repository authorization.

============================================================
55. CONVERSATION SHARING
============================================================

Support:

private conversation
workspace conversation

Do not make all historical chats automatically visible to teammates.

Default:

PRIVATE

Allow explicit:

Share with workspace

============================================================
56. SHARED AI CONTEXT
============================================================

Shared conversations should still use:

authorized repository
authorized snapshot

Never use another member's private repository.

============================================================
57. ANALYSIS RUN ACCESS
============================================================

Analysis runs are workspace-scoped.

View access:

VIEWER+

Trigger access:

EDITOR+

Manage:

ADMIN/OWNER

Use centralized authorization.

============================================================
58. CONTINUOUS ANALYSIS PERMISSIONS
============================================================

Only authorized users can enable/disable continuous analysis.

Recommended:

OWNER
ADMIN

can configure organization-level defaults.

Workspace:

OWNER
EDITOR if policy allows

can configure repository automation.

============================================================
59. WEBHOOK ACCESS
============================================================

Webhook configuration is sensitive.

Only:

OWNER
ADMIN

can manage webhook/GitHub App integration.

Normal members cannot retrieve webhook secrets.

============================================================
60. GITHUB INTEGRATION ACCESS
============================================================

Only authorized organization admins should manage:

GitHub App installation
OAuth organization connection
repository synchronization policies

Do not allow ordinary members to replace organization credentials.

============================================================
61. GITHUB APP OWNERSHIP
============================================================

If Phase 11 GitHub App foundation exists:

associate installation with:

organization

not individual member.

Example:

Organization
  ↓
GitHub Installation
  ↓
Repositories
  ↓
Workspaces

============================================================
62. DISCONNECT GITHUB
============================================================

Do not let one normal member disconnect an organization's GitHub
integration.

Owner/Admin only.

Before disconnect:

show impact.

Do not immediately delete historical analysis.

Mark integration:

DISCONNECTED

============================================================
63. ORGANIZATION REPOSITORY DIRECTORY
============================================================

Organization:

Repositories

Show:

Name
Visibility
Workspace
Default branch
Last analysis
Security state
Continuous analysis

Do not expose repositories to users without access.

============================================================
64. REPOSITORY ASSIGNMENT
============================================================

Admin can assign repository to workspace.

Do not duplicate repository records.

Existing repository identity remains stable.

============================================================
65. ONE REPOSITORY, MULTIPLE WORKSPACES
============================================================

Decide and document whether repository can be linked to multiple
workspaces.

Prefer:

one canonical repository record

multiple scoped workspace relationships

if product architecture requires it.

Do not duplicate source ingestion unnecessarily.

============================================================
66. REPOSITORY ACCESS TABLE
============================================================

Implement clear relationship:

Repository
Workspace
Organization

Example:

Repository A
belongs to Organization X
linked to Workspace Backend

Repository B
belongs to Organization X
linked to Workspace Security

============================================================
67. CROSS-WORKSPACE ACCESS
============================================================

Do not allow members to access another workspace's repository simply
because both are inside the same organization.

Organization membership is not equivalent to workspace membership.

============================================================
68. ORGANIZATION SECURITY SETTINGS
============================================================

Create foundation for:

OrganizationSecuritySettings

Possible settings:

require2FA
allowExternalInvites
defaultMemberRole
defaultWorkspaceVisibility
defaultAnalysisPolicy

Only implement settings actually supported by application.

Do not fake enforcement.

============================================================
69. EXTERNAL INVITATIONS
============================================================

If:

allowExternalInvites = false

users outside configured organization domain may be rejected.

But do not infer corporate domains without explicit configuration.

============================================================
70. DOMAIN VERIFICATION
============================================================

Do not implement full enterprise domain verification unless necessary.

Prepare model/interface for future:

VerifiedDomain

but do not pretend domain ownership is verified.

============================================================
71. ORGANIZATION AUDIT LOG
============================================================

Create organization-scoped audit view.

Filters:

actor
action
resource
date
team
workspace

Examples:

Alice invited Bob
Alice changed Bob role
Bob created artifact
Charlie enabled continuous analysis

============================================================
72. AUDIT LOG SECURITY
============================================================

Audit logs should not contain:

passwords
OAuth tokens
GitHub installation tokens
webhook secrets
invitation tokens
raw secrets
full private source

Use redacted metadata.

============================================================
73. ADMIN DASHBOARD
============================================================

Extend Phase 10 admin dashboard with organization metrics.

Show:

organizations
active members
active workspaces
repositories
analysis runs
failed analyses
security findings
webhook health

Do not expose tenant data across organizations accidentally.

============================================================
74. ORGANIZATION METRICS
============================================================

Organization users should only see aggregate metrics for organizations
they are authorized to view.

Examples:

repositories analyzed
analysis runs
open security findings
recent architecture changes

No subjective score.

============================================================
75. USAGE METRICS
============================================================

Track organization-level:

analysis count
AI request count
token usage
artifact generation count
storage usage
webhook events

Reuse Phase 10 telemetry.

============================================================
76. COST VISIBILITY
============================================================

Organization admins may view:

AI requests
estimated token usage
estimated model cost

Do not expose provider secrets.

Do not claim billing-grade accuracy if costs are estimates.

============================================================
77. RATE LIMITING
============================================================

Prepare organization-scoped rate limits.

Examples:

analysis jobs
AI requests
artifact generations
repository imports

Avoid allowing one organization to consume all system resources.

============================================================
78. FAIR QUEUE USAGE
============================================================

If queue system supports it:

introduce organization-aware fairness.

Do not allow a single tenant to monopolize workers.

============================================================
79. STORAGE QUOTAS
============================================================

Prepare quota model:

OrganizationQuota

Potential dimensions:

repository storage
snapshot storage
artifact storage
analysis retention

Do not delete data automatically without explicit retention policy.

============================================================
80. QUOTA ENFORCEMENT
============================================================

If quota exceeded:

new operation should return clear error.

Existing data remains accessible.

Do not silently delete old snapshots.

============================================================
81. ORGANIZATION DELETION
============================================================

Owner-only.

Prefer:

ARCHIVED

first.

Hard deletion should require explicit confirmation.

Do not immediately destroy historical data.

============================================================
82. OWNERSHIP TRANSFER
============================================================

Owner can transfer ownership.

Requirements:

new owner must be active member.

Old owner becomes:

ADMIN

unless explicit removal selected.

Audit event required.

============================================================
83. LAST OWNER PROTECTION
============================================================

Cannot:

remove last owner
downgrade last owner
leave organization as last owner

without ownership transfer.

============================================================
84. MEMBER REMOVAL
============================================================

When member removed:

revoke:

organization access
team access
workspace access inherited through organization
organization conversations
organization artifacts

But preserve authored historical records where required.

Example:

Artifact created by removed user:

createdBy remains user ID

User display may show:

Former Member

============================================================
85. DATA RETENTION
============================================================

Do not delete historical authorship automatically when member leaves.

Use soft identity references.

============================================================
86. TEAM REMOVAL
============================================================

Deleting a team:

removes team-based access

does not delete:

users
workspaces
repositories
artifacts

Audit the operation.

============================================================
87. WORKSPACE TRANSFER
============================================================

Workspace owner/admin should be able to transfer ownership.

Validate recipient access.

Audit event.

============================================================
88. ROLE CHANGE
============================================================

Every role change:

oldRole
newRole
actor
target
timestamp

must be auditable.

============================================================
89. API DESIGN
============================================================

Implement clean APIs.

Examples:

POST   /api/organizations
GET    /api/organizations
GET    /api/organizations/:id
PATCH  /api/organizations/:id

GET    /api/organizations/:id/members
POST   /api/organizations/:id/invitations
PATCH  /api/organizations/:id/members/:memberId
DELETE /api/organizations/:id/members/:memberId

GET    /api/organizations/:id/teams
POST   /api/organizations/:id/teams
PATCH  /api/teams/:id
DELETE /api/teams/:id

GET    /api/workspaces/:id/members
POST   /api/workspaces/:id/members
DELETE /api/workspaces/:id/members/:memberId

Use existing API conventions.

============================================================
90. DO NOT TRUST CLIENT ROLE
============================================================

Never accept:

role=ADMIN

from frontend as proof.

Resolve role server-side.

============================================================
91. AUTHORIZATION MIDDLEWARE
============================================================

Add reusable middleware/helper:

requireOrganizationAccess
requireWorkspaceAccess
requireRepositoryAccess
requirePermission

Avoid repeating authorization logic.

============================================================
92. DATABASE CONSTRAINTS
============================================================

Add uniqueness constraints.

Examples:

organization.slug

organizationMember:

organizationId + userId

team:

organizationId + slug

teamMember:

teamId + userId

workspaceMember:

workspaceId + userId

============================================================
93. SOFT DELETE
============================================================

For membership/removal:

prefer status fields over destructive deletion where history matters.

============================================================
94. UI — ORGANIZATION SWITCHER
============================================================

Header:

Personal
Organization A
Organization B

Current context must be visually obvious.

============================================================
95. UI — ORGANIZATION SETTINGS
============================================================

Tabs:

General
Members
Teams
Workspaces
Repositories
Security
Integrations
Audit Log

Only render tabs user is authorized to access.

Backend must still enforce.

============================================================
96. UI — MEMBERS
============================================================

Table:

User
Role
Status
Teams
Joined
Actions

Actions depend on permissions.

============================================================
97. UI — TEAMS
============================================================

Cards/table:

Team
Members
Workspaces
Repositories
Actions

============================================================
98. UI — WORKSPACE ACCESS
============================================================

Workspace settings:

Members
Teams

Allow:

Add member
Add team
Change role
Remove access

============================================================
99. UI — REPOSITORY ACCESS
============================================================

Repository page:

Organization
Workspace
Access

Display:

GitHub access
GitVision access

Keep them conceptually separate.

============================================================
100. UI — AUDIT LOG
============================================================

Table:

Time
Actor
Action
Resource
Result

Example:

2026-09-25 14:20
Alice
Changed member role
Bob
SUCCESS

============================================================
101. SHARED ARTIFACTS
============================================================

Artifact Center should have filters:

My Artifacts
Workspace Artifacts

if workspace access allows.

Do not automatically show organization-wide artifacts unless shared.

============================================================
102. SHARED DOCUMENTATION
============================================================

Documentation generated for workspace can be visible to workspace
members according to permissions.

Historical versions remain immutable.

============================================================
103. SHARED SECURITY
============================================================

Security dashboard should support:

My Workspaces
Organization Workspaces

based on access.

No cross-tenant aggregation.

============================================================
104. SHARED ARCHITECTURE
============================================================

Architecture views inherit workspace permissions.

Export actions must also enforce authorization.

============================================================
105. EXPORT SECURITY
============================================================

PDF/PPT/JSON/SARIF exports can contain sensitive data.

Every export endpoint must perform authorization.

Do not create publicly accessible predictable download URLs.

============================================================
106. FILE ACCESS
============================================================

File viewer must enforce:

organization
workspace
repository

authorization.

Do not allow:

/files/:fileId

to bypass repository access.

============================================================
107. SNAPSHOT ACCESS
============================================================

Snapshot IDs are not secrets.

But knowing an ID must not grant access.

Every snapshot query requires authorization.

============================================================
108. ANALYSIS RUN ACCESS
============================================================

Same principle:

runId alone must not grant access.

============================================================
109. CONVERSATION ACCESS
============================================================

Conversation ID alone must not grant access.

Verify:

workspace
repository
conversation visibility

============================================================
110. ARTIFACT ACCESS
============================================================

Artifact ID alone must not grant access.

Check:

organization
workspace
artifact visibility

============================================================
111. IDOR TESTING
============================================================

Write tests for:

organization IDOR
workspace IDOR
repository IDOR
snapshot IDOR
analysis IDOR
artifact IDOR
conversation IDOR
security finding IDOR
file IDOR
audit log IDOR

============================================================
112. CROSS-TENANT TESTING
============================================================

Create:

Organization A
Organization B

User A
User B

Private repository A
Private repository B

Verify:

User A cannot access B
User B cannot access A

Test every major endpoint.

============================================================
113. ROLE MATRIX TESTING
============================================================

Test:

OWNER
ADMIN
MEMBER
VIEWER

against:

view
create
edit
delete
manage
export
analyze
invite
audit

Document expected behavior.

============================================================
114. TEAM PERMISSION TESTING
============================================================

Test:

User has direct workspace access

User has team workspace access

User loses team membership

User has both direct and team access

============================================================
115. MEMBER REMOVAL TEST
============================================================

After removing user:

existing session/token must not continue granting organization access.

Authorization should be evaluated against current membership.

============================================================
116. SESSION SECURITY
============================================================

If existing sessions are long-lived:

consider membership revocation behavior.

At minimum:

authorization must check current membership.

Do not rely solely on login-time role.

============================================================
117. AUDIT TESTING
============================================================

Verify audit events for:

organization creation
invitation
acceptance
role change
team change
workspace sharing
repository assignment
GitHub integration change
continuous analysis setting
ownership transfer
member removal

============================================================
118. AI PRIVACY TEST
============================================================

Critical tests:

Org A repository context

must never appear in:

Org B AI request

Org A conversation

must never be retrievable by:

Org B user

Shared context must respect authorization.

============================================================
119. CACHE ISOLATION
============================================================

Audit:

repository cache
AI context cache
architecture cache
security cache
documentation cache
artifact cache
search cache

All must include proper tenant/resource identity.

============================================================
120. BACKGROUND JOB AUTHORIZATION
============================================================

Queued jobs must store enough scope:

organizationId
workspaceId
repositoryId
userId
analysisRunId

Worker must not trust only user-supplied resource IDs.

============================================================
121. JOB OWNERSHIP
============================================================

If a user loses access after job creation:

worker must verify whether job may continue.

Do not blindly execute stale authorized jobs.

============================================================
122. WEBHOOK + ORGANIZATION
============================================================

Phase 11 webhook events should resolve:

GitHub repository
→ GitVision repository
→ Organization
→ Workspace

If workspace is no longer accessible/configured:

event may still update organization-owned automation,
but user-facing access remains protected.

============================================================
123. CONTINUOUS ANALYSIS ADMIN
============================================================

Organization admin should see:

Repositories with continuous analysis

but only repository metadata permitted by organization policy.

============================================================
124. SECURITY INCIDENT VISIBILITY
============================================================

Organization security findings should be visible only to authorized
workspace/team members.

Do not automatically notify every organization member.

Notification system belongs to a later phase.

============================================================
125. ORGANIZATION DEFAULTS
============================================================

Prepare:

OrganizationDefaults

Possible defaults:

defaultWorkspaceRole
defaultTeamAccess
defaultAnalysisPolicy
defaultArtifactPolicy

Do not override explicit workspace configuration.

============================================================
126. POLICY PRECEDENCE
============================================================

Document precedence:

system
→ organization
→ workspace
→ repository
→ user/team permissions

Where conflicts exist:

more restrictive explicit security policy should win.

Do not invent hidden precedence rules.

============================================================
127. FEATURE FLAGS
============================================================

Use Phase 10 feature flag foundation for:

organizations
teams
workspace sharing
advanced RBAC

Existing users should remain unaffected if feature is disabled.

============================================================
128. OBSERVABILITY
============================================================

Extend Phase 10 metrics:

organization.created
member.invited
member.joined
member.removed
team.created
workspace.shared
repository.assigned
authorization.denied
authorization.allowed
cross_tenant_access_attempt
invitation.expired

Track latency for authorization where practical.

============================================================
129. SECURITY ALERTS
============================================================

Do not build notification channels yet.

But record security-sensitive events:

repeated authorization failures
suspicious cross-tenant access attempts
large invitation activity
permission changes

Admin observability can surface them.

============================================================
130. RATE LIMITING
============================================================

Rate-limit:

invitation creation
organization creation
team creation
membership modifications
authorization-sensitive endpoints

Avoid abuse.

============================================================
131. API ERROR SEMANTICS
============================================================

Use consistent:

401:
unauthenticated

403:
authenticated but unauthorized

404:
resource not visible / intentionally hidden where appropriate

409:
membership/conflict

422:
validation

Do not leak whether a private resource exists when policy requires
resource hiding.

============================================================
132. FRONTEND SECURITY
============================================================

UI should hide unavailable actions.

But this is convenience only.

Backend remains authoritative.

============================================================
133. ORGANIZATION CONTEXT
============================================================

Frontend should not assume:

currentOrgId

is trusted.

Every backend request must authorize the actual resource.

============================================================
134. URL SECURITY
============================================================

Routes such as:

/org/:orgId
/workspace/:workspaceId
/repository/:repositoryId

must verify authorization server-side.

============================================================
135. SEARCH SECURITY
============================================================

Global search must only return resources the current user can access.

Do not filter after fetching an unrestricted dataset if possible.

Prefer authorization-aware queries.

============================================================
136. LIST API SECURITY
============================================================

Repository/workspace/member listing endpoints must be scoped.

Do not:

fetch everything
then filter in frontend.

============================================================
137. PAGINATION
============================================================

Organization members
teams
repositories
audit events

must support pagination.

Do not load thousands of records into memory.

============================================================
138. SORT/FILTER
============================================================

Support server-side:

search
status
role
team
workspace

where useful.

============================================================
139. ORGANIZATION ANALYTICS
============================================================

Provide descriptive metrics:

repositories
active workspaces
analysis runs
security findings
artifact count

Do not generate subjective organizational quality scores.

============================================================
140. NO EMPLOYEE RANKING
============================================================

Do NOT implement:

developer ranking
employee productivity score
"best engineer"
"worst engineer"
team ranking

GitVision should provide repository intelligence, not employee
performance surveillance.

============================================================
141. NO SUBJECTIVE TEAM SCORE
============================================================

Do not create:

team health score
developer score
engineering ranking

Use objective metrics instead.

============================================================
142. DATA EXPORT
============================================================

Organization admins may export authorized:

audit logs
repository metadata
security findings
architecture data
artifacts

Exports must obey permissions.

============================================================
143. EXPORT AUDIT
============================================================

Every sensitive export:

actor
resource
format
timestamp

must be logged.

============================================================
144. ORGANIZATION IMPORT
============================================================

Do not build bulk migration/import in this phase.

============================================================
145. BILLING FOUNDATION
============================================================

Do not implement actual billing.

Only prepare optional:

planId
usage counters

if existing architecture requires them.

Do not block core functionality behind fake billing logic.

============================================================
146. API DOCUMENTATION
============================================================

Document:

organization endpoints
team endpoints
membership endpoints
workspace sharing
authorization rules
invitation lifecycle

============================================================
147. SECURITY DOCUMENTATION
============================================================

Create:

docs/rbac.md
docs/multi-tenancy.md
docs/organization-security.md

Document:

tenant isolation
authorization
roles
permissions
data ownership
session behavior
cache isolation

============================================================
148. MIGRATIONS
============================================================

Create safe database migrations.

Must include:

Organization
OrganizationMember
OrganizationInvitation
Team
TeamMember
WorkspaceMember
RepositoryAccess / relationships
Organization settings if required
Audit extensions

Add indexes for:

organizationId
userId
workspaceId
repositoryId
teamId

============================================================
149. BACKWARD COMPATIBILITY
============================================================

Existing:

GitHub login
repo URL analysis
ZIP upload
chat
security
architecture
docs
artifacts
continuous analysis

must continue working.

No forced organization signup for existing personal users.

============================================================
150. TEST MATRIX
============================================================

Run:

1. Existing test suite

2. Organization creation
3. Organization switch
4. Member invite
5. Invite accept
6. Invite expire
7. Invite revoke
8. Role change
9. Member removal
10. Owner transfer

11. Team creation
12. Team membership
13. Team workspace access
14. Direct workspace access
15. Combined direct/team access
16. Team removal

17. Workspace authorization
18. Repository authorization
19. Snapshot authorization
20. Security authorization
21. Artifact authorization
22. Conversation authorization

23. Cross-tenant IDOR
24. Search isolation
25. Cache isolation
26. Background job isolation
27. AI context isolation

28. Webhook organization mapping
29. Continuous analysis authorization
30. GitHub integration authorization

31. Export authorization
32. Audit logging
33. Pagination
34. Rate limiting
35. Concurrent membership changes

============================================================
151. PERFORMANCE
============================================================

Authorization should not create N+1 database queries.

Use:

indexed relationships
batched queries
request-scoped caching

But never cache authorization across users incorrectly.

============================================================
152. AUTHORIZATION CACHE
============================================================

If permission caching is used:

key must include:

userId
organizationId
resourceId
permission/version

Invalidate after:

role change
member removal
team change
workspace access change

============================================================
153. DATABASE TRANSACTION SAFETY
============================================================

Membership operations should be transactional.

Example:

role change
+
audit event

should succeed/fail consistently.

============================================================
154. CONCURRENCY
============================================================

Handle concurrent:

role changes
member removal
ownership transfer
team membership

Use optimistic locking or transactions where appropriate.

============================================================
155. AUDIT IMMUTABILITY
============================================================

Audit logs should be append-only from application perspective.

Do not provide normal UI action to edit audit events.

============================================================
156. OWNER PROTECTION
============================================================

Ownership transfer should require:

authenticated current owner
valid target member
transaction
audit event

============================================================
157. ORGANIZATION SUSPENSION
============================================================

If organization becomes:

SUSPENDED

normal member operations should be blocked.

Owner/admin should still have appropriate recovery access.

Do not delete data.

============================================================
158. USER DEACTIVATION
============================================================

If user account becomes inactive:

organization memberships should not grant active access.

Historical authored records remain.

============================================================
159. DATA MODEL SUMMARY
============================================================

Target:

User
 │
 ├── Personal Workspaces
 │
 └── OrganizationMembership
        │
        ↓
    Organization
       │
       ├── Members
       ├── Teams
       │    └── TeamMembers
       │
       ├── Workspaces
       │    └── WorkspaceMembers
       │
       ├── Repositories
       │
       ├── Security
       ├── Architecture
       ├── Documentation
       ├── Artifacts
       ├── Conversations
       └── Audit Events

============================================================
160. DEFINITION OF DONE
============================================================

[ ] Organization model exists

[ ] Organization membership exists

[ ] Owner/Admin/Member/Viewer roles exist

[ ] Personal workspaces continue working

[ ] Organization switcher exists

[ ] Workspace membership exists

[ ] Teams exist

[ ] Team membership exists

[ ] Team-based workspace access works

[ ] Direct workspace access works

[ ] Repository authorization works

[ ] GitHub authorization remains separate

[ ] Invitation flow works

[ ] Invitation expiration works

[ ] Invitation revocation works

[ ] Ownership transfer works

[ ] Last-owner protection works

[ ] Member removal works

[ ] Central authorization service exists

[ ] Backend does not trust frontend roles

[ ] Cross-tenant isolation works

[ ] IDOR tests pass

[ ] AI context isolation works

[ ] Cache isolation works

[ ] Background-job authorization works

[ ] Security finding access works

[ ] Architecture access works

[ ] Documentation access works

[ ] Artifact access works

[ ] Conversation access works

[ ] Export authorization works

[ ] Audit logs work

[ ] Organization dashboard exists

[ ] Member management UI exists

[ ] Team management UI exists

[ ] Workspace access UI exists

[ ] Organization repository directory exists

[ ] Organization usage metrics exist

[ ] Rate limiting exists where required

[ ] Existing webhook system remains compatible

[ ] Existing continuous analysis remains compatible

[ ] Existing GitHub App foundation remains compatible

[ ] Existing personal workflows remain compatible

[ ] Existing tests pass

[ ] New security tests pass

============================================================
161. DO NOT IMPLEMENT IN THIS PHASE
============================================================

Do NOT implement:

- SSO
- SAML
- SCIM
- enterprise directory sync
- advanced compliance certifications
- billing system
- subscriptions
- payment processing
- Slack
- Teams notifications
- email notification platform
- real-time collaborative editing
- public artifact sharing
- anonymous repository sharing
- employee performance scoring
- developer rankings
- automatic code modifications
- autonomous remediation

These belong to later phases.

============================================================
162. FINAL REPORT
============================================================

At completion report:

A. Files created
B. Files modified
C. Database migrations
D. Organization model
E. RBAC model
F. Permission matrix
G. Team model
H. Workspace access model
I. Invitation flow
J. Ownership transfer
K. Tenant isolation
L. API endpoints
M. UI changes
N. Audit events
O. Security controls
P. Tests
Q. Migration/backward compatibility
R. Known limitations
S. Manual verification
T. Architectural decisions

Do not rewrite unrelated code.

Do not remove existing functionality.

Prefer incremental, composable changes.