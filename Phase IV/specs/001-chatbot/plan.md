# Implementation Plan: Phase III AI Chatbot & MCP Integration for Todo Application

**Branch**: `001-chatbot` | **Date**: 2026-02-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build agent-driven stateless chat with frontend integration and MCP tools. The project will extend the existing FastAPI backend with MCP server integration, OpenAI Agents SDK, and conversation persistence using Neon PostgreSQL. The frontend ChatKit interface will connect to the chat endpoint for natural language todo management.

## Technical Context

**Language/Version**: Python 3.11 (FastAPI backend)
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Better Auth
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server (serverless deployment)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: <200ms p95 response time for chat endpoint
**Constraints**: <100MB memory per request, stateless processing
**Scale/Scope**: Support 1000 concurrent users with conversation persistence

## Constitution Check

*Complies with all constitution principles:*

- ✅ **Agent-First, Tool-Only Task Management via MCP**: All task operations must be executed exclusively through MCP tools using the Official MCP SDK
- ✅ **Stateless Chat Processing with Database-Backed Context**: All chat processing must be stateless between requests with conversation history reconstructed from database
- ✅ **Strict JWT-Based User Isolation**: User identity must come only from verified JWT claims with all operations scoped to authenticated user ID
- ✅ **Spec-Driven, Agentic Development Workflow**: All development follows Spec-Kit Plus + Claude Code workflow
- ✅ **Official MCP SDK and OpenAI Agents SDK Integration**: MCP tool operations must use Official MCP SDK and agent logic must use OpenAI Agents SDK
- ✅ **Conversation Persistence and Reconstruction**: All messages and tool calls must be persisted with full context for conversation reconstruction

## Project Structure

### Documentation (this feature)

```text
specs/001-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── spec.md             # Feature specification
├── research.md         # Phase 0 output (/sp.plan command)
├── data-model.md       # Phase 1 output (/sp.plan command)
├── quickstart.md       # Phase 1 output (/sp.plan command)
├── contracts/          # Phase 1 output (/sp.plan command)
└── tasks.md            # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/         # SQLModel database models (user, todo, conversation, message, toolcall)
│   ├── services/       # Business logic services
│   ├── api/            # FastAPI endpoints and routers
│   └── middleware/     # JWT auth, error handling, security headers
└── tests/              # pytest test files

frontend/
├── src/
│   ├── components/     # React/Next.js components
│   ├── pages/          # Next.js App Router pages
│   └── services/       # API client services
└── tests/              # Frontend tests
```

**Structure Decision**: Web application structure with separate backend (FastAPI) and frontend (Next.js) services, matching existing codebase architecture.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| MCP Server Integration | Required for agent-first, tool-only architecture per constitution | Direct database access would violate constitution principles |
| OpenAI Agents SDK | Required for agent logic and tool invocation per constitution | Custom agent implementation would violate constitution principles |
| Conversation Persistence | Required for stateless chat processing with context reconstruction | In-memory state would violate stateless processing requirement |

## Phase 0: Outline & Research

### Research Findings

Based on existing codebase analysis and feature requirements:

**Decision**: Extend existing FastAPI backend with MCP server integration
**Rationale**: Leverages existing authentication, database models, and API structure while adding MCP layer for agent-first architecture
**Alternatives considered**:
- Separate MCP service: Rejected due to added complexity and latency
- Direct database access: Rejected due to constitution violation

**Decision**: Use OpenAI Agents SDK for agent logic
**Rationale**: Constitution mandates OpenAI Agents SDK for tool invocation and agent logic
**Alternatives considered**:
- Custom agent implementation: Rejected due to constitution violation
- Alternative AI frameworks: Rejected due to constitution violation

**Decision**: Implement conversation persistence with message and tool call tracking
**Rationale**: Required for stateless chat processing with context reconstruction
**Alternatives considered**:
- In-memory storage: Rejected due to stateless processing requirement
- Session-based storage: Rejected due to stateless processing requirement

## Phase 1: Design & Contracts

### Data Model Design

Based on existing user and todo models, we need to add:

**Conversation Model**:
- id: primary key
- user_id: foreign key to User
- created_at: timestamp
- updated_at: timestamp

**Message Model**:
- id: primary key
- conversation_id: foreign key to Conversation
- content: text
- role: "user" | "assistant" | "system"
- tool_call_id: foreign key to ToolCall (nullable)
- created_at: timestamp

**ToolCall Model**:
- id: primary key
- conversation_id: foreign key to Conversation
- tool_name: string
- parameters: JSON
- result: JSON
- status: "pending" | "success" | "failed"
- created_at: timestamp

### API Contracts

**POST /api/{user_id}/chat**: Chat endpoint for natural language interaction
- Request: {"messages": [{"role": "user", "content": "string"}]}
- Response: {"messages": [{"role": "string", "content": "string"}], "tool_calls": [{"id": "string", "name": "string", "parameters": "object", "result": "object", "status": "string"}]}

**MCP Tools**:
- add_task: Add a new todo task
- list_tasks: List all tasks for user
- update_task: Update an existing task
- complete_task: Mark task as complete
- delete_task: Delete a task

### Quickstart Integration

**Backend Setup**:
1. Install required dependencies: openai, mcp, mcp-server-fastapi
2. Configure MCP server with FastAPI integration
3. Implement tool mapping between MCP and existing services
4. Add conversation persistence to existing models

**Frontend Integration**:
1. Install OpenAI ChatKit component
2. Configure API client with JWT authentication
3. Connect ChatKit to /api/{user_id}/chat endpoint
4. Implement message streaming and tool call handling

## Phase 2: Implementation Tasks

Based on the research and design, here are the key implementation tasks:

1. Add Conversation, Message, and ToolCall models to database
2. Implement MCP server with add/list/update/complete/delete task tools
3. Enforce JWT user scope in all MCP tools
4. Integrate OpenAI Agents SDK with MCP tool mapping
5. Implement POST /api/{user_id}/chat endpoint with history loading and response generation
6. Connect ChatKit frontend to chat endpoint
7. Validate stateless flow and conversation persistence

## Constitution Check (Post-Design)

*Re-validated after Phase 1 design:*

- ✅ All task operations flow through MCP tools only
- ✅ Stateless chat processing with database-backed context
- ✅ Strict JWT user isolation enforced
- ✅ Spec-driven agentic development workflow followed
- ✅ Official MCP SDK and OpenAI Agents SDK integration implemented
- ✅ Conversation persistence and reconstruction supported

## Success Criteria Alignment

**SC-001**: Users can successfully add tasks through natural language commands in under 30 seconds
- **Implementation**: MCP add_task tool with natural language parsing

**SC-002**: System correctly processes and responds to task management commands with 95% accuracy
- **Implementation**: OpenAI Agents SDK with tool mapping and error handling

**SC-003**: Conversation context is maintained across multiple turns with 100% accuracy
- **Implementation**: Message persistence and conversation reconstruction

**SC-004**: All chat messages and tool calls are persisted to database within 100ms
- **Implementation**: Optimized database operations and indexing

**SC-005**: System maintains 99.9% uptime for chat endpoint
- **Implementation**: Stateless architecture with graceful degradation

**SC-006**: User data isolation is enforced with 100% accuracy
- **Implementation**: JWT-based user scoping in all operations

**SC-007**: Chat interface loads within 2 seconds and responds within 1 second
- **Implementation**: Optimized frontend with efficient API calls

## Next Steps

This plan provides the foundation for implementing the Phase III AI Chatbot & MCP Integration. The next step would be to generate detailed implementation tasks using `/sp.tasks` command, followed by agent-based implementation of each component.