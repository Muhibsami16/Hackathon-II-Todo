---
id: 1
title: Update constitution
stage: constitution
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: sp.constitution
labels: ["constitution", "setup", "todo-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
tests:
---

## Prompt

Project: Todo Full-Stack Web Application (Next.js + FastAPI + SQLModel + Neon + Better Auth + JWT)

Core principles:
- Spec-driven and agentic development only (Spec-Kit Plus + Claude Code workflow)
- No manual coding by the developer (all implementation generated through agents)
- Clear separation of concerns between frontend, backend, authentication, and database layers
- Security-first design (JWT-based stateless authentication and strict user isolation)
- Production-ready API and frontend structure

Key standards:
- All backend endpoints must strictly follow the defined REST API contract
- All data access must be implemented using SQLModel ORM only
- All database operations must persist to Neon Serverless PostgreSQL
- All authenticated API requests must include a valid JWT in the Authorization header
- JWT verification must be enforced on every protected route in FastAPI
- User identity must be derived only from verified JWT claims (not from client input)
- Every task operation must be filtered and validated by the authenticated user ID
- Frontend API client must automatically attach JWT tokens to every request
- Better Auth must be configured to issue JWT tokens via its official JWT plugin
- Environment-based configuration must be used for all secrets and connection strings

Constraints:
- Frontend framework: Next.js 16+ using App Router
- Backend framework: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication library: Better Auth (frontend) with JWT integration
- Backend authentication mechanism: shared-secret JWT verification
- No session-based authentication between frontend and backend
- No direct database access from the frontend
- All features must be implemented only through the defined Agentic Dev Stack workflow:
  Write spec → Generate plan → Break into tasks → Implement via Claude Code

Success criteria:
- All listed task CRUD and completion endpoints are implemented and reachable
- All endpoints require a valid JWT and return 401 for unauthenticated requests
- Each user can only access and modify their own tasks
- JWT signature and expiry are correctly verified by the FastAPI backend
- Frontend can successfully authenticate, obtain a JWT, and call protected APIs
- Task data is persisted and retrieved correctly from Neon PostgreSQL
- The full workflow demonstrates spec-driven development with reproducible prompts and iterations

## Response snapshot

Created a new constitution file that incorporates all the specified principles, standards, constraints, and success criteria for the Todo Full-Stack Web Application project. The constitution enforces spec-driven and agentic development only, clear separation of concerns, security-first design with JWT authentication, production-ready structure, agentic development compliance, and technology stack adherence.

## Outcome

- ✅ Impact: Updated constitution file with project-specific principles
- 🧪 Tests: No automated tests for constitution file
- 📁 Files: Modified .specify/memory/constitution.md
- 🔁 Next prompts: Continue with spec, plan, and task generation
- 🧠 Reflection: Constitution now properly defines the agentic development workflow requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin spec generation for the todo application