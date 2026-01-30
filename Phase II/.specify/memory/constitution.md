<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: None (completely new constitution for this project)
Added sections: All sections (new project constitution)
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending review
Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-Driven and Agentic Development Only
All development must follow the Spec-Kit Plus + Claude Code workflow exclusively. No manual coding by developers is allowed - all implementation must be generated through specialized agents following the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code.

### Clear Separation of Concerns
Maintain strict separation between frontend, backend, authentication, and database layers. Frontend (Next.js) and backend (FastAPI) must be separate services with well-defined API contracts. Each layer has its dedicated technology stack and responsibilities without cross-contamination.

### Security-First Design with JWT Authentication
Implement security-first design with JWT-based stateless authentication and strict user isolation. All API endpoints must require valid JWT tokens, user data must be isolated by user ID, and authentication must follow the Better Auth + FastAPI JWT verification pattern.

### Production-Ready API and Frontend Structure
All implementations must follow production-ready patterns including proper error handling, validation, logging, and performance considerations. APIs must follow RESTful conventions, and frontend must be responsive and accessible.

### Agentic Development Compliance
All features must be implemented only through the defined Agentic Dev Stack workflow. Manual coding is prohibited. Every change must go through the spec → plan → tasks → implement pipeline using specialized agents (auth, frontend, backend, database).

### Technology Stack Adherence
Strict adherence to the mandated technology stack: Next.js 16+ (App Router) for frontend, Python FastAPI for backend, SQLModel for ORM, Neon Serverless PostgreSQL for database, and Better Auth with JWT for authentication.

## Key Standards

All backend endpoints must strictly follow the defined REST API contract with proper HTTP methods and status codes. All data access must be implemented using SQLModel ORM only, with all database operations persisting to Neon Serverless PostgreSQL. All authenticated API requests must include a valid JWT in the Authorization header, with JWT verification enforced on every protected route in FastAPI. User identity must be derived only from verified JWT claims, not from client input. Every task operation must be filtered and validated by the authenticated user ID. Frontend API client must automatically attach JWT tokens to every request. Better Auth must be configured to issue JWT tokens via its official JWT plugin. Environment-based configuration must be used for all secrets and connection strings.

## Constraints

Frontend framework: Next.js 16+ using App Router. Backend framework: Python FastAPI. ORM: SQLModel. Database: Neon Serverless PostgreSQL. Authentication library: Better Auth (frontend) with JWT integration. Backend authentication mechanism: shared-secret JWT verification. No session-based authentication between frontend and backend. No direct database access from the frontend. No manual coding - all implementation must be agent-driven.

## Success Criteria

All task CRUD and completion endpoints are implemented and reachable. All endpoints require a valid JWT and return 401 for unauthenticated requests. Each user can only access and modify their own tasks. JWT signature and expiry are correctly verified by the FastAPI backend. Frontend can successfully authenticate, obtain a JWT, and call protected APIs. Task data is persisted and retrieved correctly from Neon PostgreSQL. The full workflow demonstrates spec-driven development with reproducible prompts and iterations.

## Governance

This constitution governs all development activities for the Todo Full-Stack Web Application project. All development must comply with these principles and standards. Amendments require explicit documentation of changes and approval from project stakeholders. All pull requests and reviews must verify compliance with these principles. The agentic development workflow (spec → plan → tasks → implement) is mandatory for all changes. Use CLAUDE.md for runtime development guidance and agent selection.

**Version**: 1.1.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-01-30