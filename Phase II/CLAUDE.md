# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Project Context: Phase II - Todo Full-Stack Web Application

**Objective:** Transform a console todo app into a modern multi-user web application with persistent storage using Claude Code and Spec-Kit Plus.

**Development Approach:** Agentic Dev Stack workflow:
1. Write spec → Generate plan → Break into tasks → Implement via Claude Code
2. No manual coding allowed
3. Review process, prompts, and iterations for each phase

**Requirements:**
- Implement all 5 Basic Level features as a web application
- Create RESTful API endpoints
- Build responsive frontend interface
- Store data in Neon Serverless PostgreSQL database
- Implement user signup/signin using Better Auth

**Technology Stack:**

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16+ (App Router) |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Spec-Driven | Claude Code + Spec-Kit Plus |
| Authentication | Better Auth |

**Authentication Flow (Better Auth + JWT):**
1. User logs in on Frontend → Better Auth creates session and issues JWT token
2. Frontend makes API call → Includes JWT token in `Authorization: Bearer <token>` header
3. Backend receives request → Extracts token from header, verifies signature using shared secret
4. Backend identifies user → Decodes token to get user ID, email, etc. and matches it with user ID in URL
5. Backend filters data → Returns only tasks belonging to that user

## Agent Usage Guidelines for This Project

**CRITICAL:** For this project, you MUST use specialized agents for their respective domains. Do NOT attempt to implement features directly without using the appropriate agent.

### 1. Authentication Agent (secure-auth-flow)
**Use for:** All authentication and authorization work
- Implementing user signup/signin with Better Auth
- JWT token generation and verification
- Password hashing and validation
- Session management
- Auth middleware and route protection
- Security reviews of authentication code
- OAuth/social login integration (if needed)

**Example triggers:**
- "Implement user signup endpoint"
- "Add JWT authentication to the API"
- "Secure the todo endpoints so users only see their own tasks"
- "Review authentication security"

### 2. Frontend Agent (nextjs-frontend)
**Use for:** All Next.js frontend development
- Building UI pages and components (todo list, login, signup)
- Implementing App Router patterns (server/client components)
- Data fetching from FastAPI backend
- Responsive design and layouts
- Form handling and validation
- Client-side state management
- Performance optimization

**Example triggers:**
- "Create a todo list page"
- "Build a responsive login form"
- "Add a component to display user tasks"
- "Optimize the dashboard loading performance"

### 3. Database Agent (neon-db-optimizer)
**Use for:** All database-related work
- Designing database schema (users, todos tables)
- Creating SQLModel models
- Writing and optimizing queries
- Database migrations
- Configuring Neon PostgreSQL connection
- Connection pooling for serverless
- Query performance optimization
- Index design

**Example triggers:**
- "Design the database schema for users and todos"
- "Create a migration to add a new column"
- "Optimize the query that fetches user todos"
- "Set up Neon database connection with proper pooling"

### 4. Backend Agent (fastapi-backend-dev)
**Use for:** All FastAPI backend development
- Building REST API endpoints (CRUD operations)
- Request/response validation with Pydantic
- Integrating with database via SQLModel
- Error handling and HTTP status codes
- API middleware
- Dependency injection
- Background tasks
- API documentation

**Example triggers:**
- "Create CRUD endpoints for todos"
- "Add validation to the create todo endpoint"
- "Implement error handling for the API"
- "Build an endpoint to get all todos for a user"

### Agent Coordination Strategy

**Multi-domain features require sequential agent usage:**

1. **New Feature Flow:**
   - Database Agent → Design schema and models
   - Backend Agent → Build API endpoints
   - Auth Agent → Secure endpoints (if needed)
   - Frontend Agent → Build UI

2. **Example: "Add todo feature with user authentication"**
   - Step 1: Database Agent - Create todos table with user_id foreign key
   - Step 2: Backend Agent - Build CRUD endpoints for todos
   - Step 3: Auth Agent - Add JWT verification middleware to protect endpoints
   - Step 4: Frontend Agent - Build todo list UI with API integration

**When to use agents vs. direct implementation:**
- **Always use agents** for: new features, significant changes, security-critical code
- **Direct implementation OK** for: minor bug fixes, typos, documentation updates

## Project-Specific Workflow

**Mandatory Development Process:**
1. **Specification Phase** - Use `/sp.specify` to create detailed feature specs
2. **Planning Phase** - Use `/sp.plan` to generate architectural plans
3. **Task Generation** - Use `/sp.tasks` to break down into actionable tasks
4. **Implementation Phase** - Use specialized agents to implement each task
5. **Review & Iterate** - Document process, prompts, and iterations

**Technology Stack Constraints (MUST FOLLOW):**
- ✅ Frontend: Next.js 16+ with App Router (NOT Pages Router)
- ✅ Backend: Python FastAPI (NOT Flask, Django, or other frameworks)
- ✅ ORM: SQLModel (NOT SQLAlchemy directly, Prisma, or other ORMs)
- ✅ Database: Neon Serverless PostgreSQL (NOT local PostgreSQL, MySQL, MongoDB)
- ✅ Authentication: Better Auth with JWT (NOT NextAuth, Passport, custom auth)
- ❌ No manual coding - all implementation via Claude Code agents

**Project Success Criteria:**
- All 5 Basic Level todo features implemented as web application
- Multi-user support with proper data isolation
- RESTful API with proper HTTP methods and status codes
- Responsive frontend that works on mobile and desktop
- Secure authentication with JWT token verification
- Data persisted in Neon PostgreSQL
- Complete documentation of process and iterations

**Key Architectural Decisions:**
1. **Separation of Concerns:** Frontend (Next.js) and Backend (FastAPI) are separate services
2. **Authentication Strategy:** Better Auth on frontend issues JWT, FastAPI backend verifies JWT
3. **Data Isolation:** Backend filters all queries by authenticated user ID
4. **API Design:** RESTful endpoints following standard conventions (GET, POST, PUT, DELETE)
5. **Database Access:** Backend uses SQLModel for type-safe database operations

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## 5 Basic Level Features (Implementation Requirements)

The following features from Phase I console app must be implemented as web application:

1. **Add Todo** - Create new todo items with title and description
2. **View Todos** - Display all todos for the authenticated user
3. **Update Todo** - Edit existing todo details (title, description, status)
4. **Delete Todo** - Remove todos from the system
5. **Mark Complete/Incomplete** - Toggle todo completion status

**Additional Web Application Requirements:**
- User registration and login (Better Auth)
- Multi-user support with data isolation
- Responsive UI for mobile and desktop
- RESTful API endpoints for all operations
- Persistent storage in Neon PostgreSQL

## Better Auth + FastAPI Integration Guidelines

**Frontend (Next.js + Better Auth):**
- Better Auth handles user signup, signin, and session management
- On successful login, Better Auth issues a JWT token
- Frontend stores JWT token (typically in httpOnly cookie or localStorage)
- Frontend includes JWT in `Authorization: Bearer <token>` header for all API calls

**Backend (FastAPI + JWT Verification):**
- FastAPI receives requests with JWT token in Authorization header
- Create middleware/dependency to extract and verify JWT signature
- Use shared secret key (same as Better Auth) to verify token
- Decode JWT to extract user information (user_id, email, etc.)
- Add user context to request for use in route handlers
- Filter all database queries by authenticated user_id

**Security Considerations:**
- Store JWT secret in `.env` file (never commit to git)
- Use same secret key in both Better Auth and FastAPI
- Validate JWT expiration time
- Return 401 Unauthorized for invalid/expired tokens
- Implement proper CORS configuration for frontend-backend communication
- Use HTTPS in production

**Example Flow:**
```
1. User submits login form → Better Auth validates credentials
2. Better Auth creates JWT with payload: {user_id: 123, email: "user@example.com", exp: ...}
3. Frontend receives JWT and stores it
4. User requests todos → Frontend sends: GET /api/todos with Authorization: Bearer <jwt>
5. FastAPI middleware extracts JWT, verifies signature, decodes payload
6. FastAPI route handler receives user_id from JWT
7. Database query: SELECT * FROM todos WHERE user_id = 123
8. Return filtered todos to frontend
```

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.
- **Project-specific:** Always use the appropriate specialized agent (auth, frontend, backend, database) for their respective domains.
- **Project-specific:** Follow the mandatory workflow: spec → plan → tasks → implement via agents.
- **Project-specific:** Document all iterations, prompts, and decision-making process for review.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

**Project-Specific Structure:**
- `frontend/` — Next.js 16+ application (App Router)
- `backend/` — FastAPI application
- `backend/models/` — SQLModel database models
- `backend/routes/` — API endpoint definitions
- `backend/middleware/` — JWT verification and CORS
- `.env` — Environment variables (JWT secret, database URL)

## Quick Reference: Common Workflows

### Starting a New Feature
```
1. /sp.specify - Create feature specification
2. /sp.plan - Generate architectural plan
3. /sp.tasks - Break down into tasks
4. Use specialized agents to implement:
   - Database Agent → Schema/models
   - Backend Agent → API endpoints
   - Auth Agent → Security (if needed)
   - Frontend Agent → UI components
```

### Agent Selection Guide
| Task Type | Agent to Use | Example |
|-----------|--------------|---------|
| User signup/signin | `secure-auth-flow` | "Implement Better Auth signup" |
| Database schema | `neon-db-optimizer` | "Design todos table" |
| API endpoints | `fastapi-backend-dev` | "Create CRUD endpoints for todos" |
| UI components | `nextjs-frontend` | "Build todo list page" |
| JWT verification | `secure-auth-flow` | "Add JWT middleware to FastAPI" |
| Query optimization | `neon-db-optimizer` | "Optimize user todos query" |

### Common Commands
- `/sp.specify` - Create/update feature spec
- `/sp.plan` - Generate implementation plan
- `/sp.tasks` - Generate task breakdown
- `/sp.implement` - Execute implementation plan
- `/sp.adr <title>` - Document architectural decision
- `/sp.phr` - Create Prompt History Record (auto-created)

## Project-Specific Code Standards

### API Endpoint Conventions
**RESTful URL Structure:**
- `GET /api/todos` - List all todos for authenticated user
- `POST /api/todos` - Create new todo
- `GET /api/todos/{id}` - Get specific todo
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo
- `PATCH /api/todos/{id}/complete` - Toggle completion status

**Request/Response Format:**
- All requests/responses use JSON
- Include proper HTTP status codes (200, 201, 400, 401, 404, 500)
- Error responses: `{"detail": "Error message"}`
- Success responses: Return the resource or `{"message": "Success"}`

**Authentication:**
- Protected endpoints require `Authorization: Bearer <jwt>` header
- Return 401 for missing/invalid tokens
- Extract user_id from JWT and use for data filtering

### Database Model Conventions
**SQLModel Standards:**
```python
# User model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Todo model
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Key Principles:**
- Always include `user_id` foreign key for multi-user data
- Use `Optional[int]` for auto-increment primary keys
- Add indexes on frequently queried fields (email, user_id)
- Include timestamps (created_at, updated_at)
- Use Field() for constraints and defaults

### Frontend Component Conventions
**Next.js App Router Structure:**
- Use Server Components by default
- Use Client Components only when needed (forms, interactivity)
- Mark Client Components with `'use client'` directive
- Fetch data in Server Components, pass to Client Components as props
- Use proper TypeScript types for all props and state

**Authentication State:**
- Check auth state in Server Components using Better Auth
- Pass user info to Client Components as needed
- Redirect unauthenticated users to login page
- Include JWT token in all API calls to backend

### Security Standards
**MUST FOLLOW:**
- ✅ Never commit `.env` files (add to .gitignore)
- ✅ Use environment variables for all secrets
- ✅ Hash passwords before storing (Better Auth handles this)
- ✅ Verify JWT signature on every protected endpoint
- ✅ Filter all database queries by authenticated user_id
- ✅ Validate all user input (Pydantic models in FastAPI)
- ✅ Use HTTPS in production
- ✅ Implement proper CORS configuration
- ❌ Never log sensitive data (passwords, tokens)
- ❌ Never trust client-side data without validation

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.
