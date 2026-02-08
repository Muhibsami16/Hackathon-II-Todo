---
id: 1
title: Update constitution for Phase III AI Chatbot project
stage: constitution
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: Phase III AI Chatbot
branch: 001-frontend-app
user: user
command: /sp.constitution
labels: [constitution, phase-iii, chatbot, mcp]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - E:\HACKATHON-II\Phase III\.specify\memory\constitution.md
tests:
 - None
---

## Prompt

/sp.constitution

Project: Phase III – AI Chatbot & MCP Integration for Todo Application

Core principles:
- Agent-first, tool-only task management via MCP
- Stateless chat processing with database-backed context
- Strict JWT-based user isolation
- Spec-driven, agentic development workflow

Key standards:
- All task operations must be executed only through MCP tools (Official MCP SDK)
- FastAPI chat endpoint must not directly modify tasks
- OpenAI Agents SDK must be used for agent logic and tool invocation
- Conversation history must be reconstructed from the database on every request
- All messages and tool calls must be persisted
- User identity must come only from verified JWT claims

Constraints:
- Frontend: OpenAI ChatKit
- Backend: FastAPI
- AI: OpenAI Agents SDK
- MCP: Official MCP SDK
- ORM: SQLModel
- Database: Neon PostgreSQL
- Auth: Better Auth + JWT
- Endpoint: POST /api/{user_id}/chat
- Server must be stateless between requests

Success criteria:
- Users can manage todos via natural language
- Agent correctly invokes MCP tools for all basic operations
- Conversation resumes correctly after restart
- All actions are scoped to the authenticated user

## Response snapshot

Updated the project constitution to version 2.0.0 with new principles for the Phase III AI Chatbot & MCP Integration project. The constitution now reflects the agent-first, tool-only approach with MCP SDK integration, stateless chat processing, strict JWT user isolation, and the mandated technology stack.

## Outcome

- ✅ Impact: Completely replaced previous todo app constitution with Phase III AI Chatbot principles
- 🧪 Tests: None required for constitution update
- 🗁 Files: Updated .specify/memory/constitution.md with new content
- 🔄 Next prompts: None - constitution update complete
- 🧠 Reflection: Successfully transitioned from todo app to AI chatbot project constitution with proper version increment and comprehensive principle coverage

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A