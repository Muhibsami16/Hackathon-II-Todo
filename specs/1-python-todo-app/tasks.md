---
description: "Task list for Phase I In-Memory Python Console Todo App implementation"
---

# Tasks: Phase I – In-Memory Python Console Todo App

**Input**: Design documents from `/specs/1-python-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included based on the feature specification requirements for comprehensive coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in src/todo_app/
- [ ] T002 Create tests directory structure in tests/
- [ ] T003 [P] Create __init__.py files in src/todo_app/, src/todo_app/models/, src/todo_app/services/, src/todo_app/cli/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create Todo data model in src/todo_app/models/todo.py
- [ ] T005 Create TodoList collection class in src/todo_app/models/todo.py
- [ ] T006 Create TodoService in src/todo_app/services/todo_service.py
- [ ] T007 Create CLI interface skeleton in src/todo_app/cli/cli.py
- [ ] T008 Create main application entry point in src/todo_app/main.py
- [ ] T009 Configure basic error handling and validation

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Todo Items (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo items to their list with a unique ID

**Independent Test**: Run the application and use the add command to create new todo items, verifying they appear in the list with sequential IDs

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Unit test for Todo model in tests/unit/test_todo.py
- [ ] T011 [P] [US1] Unit test for TodoService add functionality in tests/unit/test_todo_service.py
- [ ] T012 [P] [US1] Integration test for add command in tests/integration/test_cli.py

### Implementation for User Story 1

- [ ] T013 [P] [US1] Implement Todo model with id, title, completed fields in src/todo_app/models/todo.py
- [ ] T014 [P] [US1] Implement TodoList add operation in src/todo_app/models/todo.py
- [ ] T015 [US1] Implement TodoService add_todo method in src/todo_app/services/todo_service.py
- [ ] T016 [US1] Implement add command in CLI interface in src/todo_app/cli/cli.py
- [ ] T017 [US1] Add validation for empty task descriptions in src/todo_app/services/todo_service.py
- [ ] T018 [US1] Add sequential ID assignment in src/todo_app/services/todo_service.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Todo List (Priority: P1)

**Goal**: Enable users to view all their todo items with IDs, descriptions, and completion status

**Independent Test**: Run the application and use the list command to display all todo items, verifying they show with proper formatting

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T019 [P] [US2] Unit test for TodoService list functionality in tests/unit/test_todo_service.py
- [ ] T020 [P] [US2] Integration test for list command in tests/integration/test_cli.py

### Implementation for User Story 2

- [ ] T021 [P] [US2] Implement TodoList list operation in src/todo_app/models/todo.py
- [ ] T022 [US2] Implement TodoService get_all_todos method in src/todo_app/services/todo_service.py
- [ ] T023 [US2] Implement list command in CLI interface in src/todo_app/cli/cli.py
- [ ] T024 [US2] Add formatted display for todo items in src/todo_app/cli/cli.py
- [ ] T025 [US2] Handle empty list case in src/todo_app/cli/cli.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Todo Items Complete (Priority: P2)

**Goal**: Enable users to mark todo items as complete/incomplete

**Independent Test**: Run the application, add a todo item, mark it complete, then verify it shows as completed when viewing

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T026 [P] [US3] Unit test for TodoService mark complete functionality in tests/unit/test_todo_service.py
- [ ] T027 [P] [US3] Integration test for complete command in tests/integration/test_cli.py

### Implementation for User Story 3

- [ ] T028 [P] [US3] Implement TodoList update operation in src/todo_app/models/todo.py
- [ ] T029 [US3] Implement TodoService mark_complete method in src/todo_app/services/todo_service.py
- [ ] T030 [US3] Implement complete command in CLI interface in src/todo_app/cli/cli.py
- [ ] T031 [US3] Add validation for non-existent IDs in src/todo_app/services/todo_service.py
- [ ] T032 [US3] Add appropriate visual indicator for completed items in display in src/todo_app/cli/cli.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Update Todo Items (Priority: P2)

**Goal**: Enable users to update the description of existing todo items

**Independent Test**: Run the application, add a todo item, update its description, then verify the change is reflected

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T033 [P] [US4] Unit test for TodoService update functionality in tests/unit/test_todo_service.py
- [ ] T034 [P] [US4] Integration test for update command in tests/integration/test_cli.py

### Implementation for User Story 4

- [ ] T035 [US4] Implement TodoService update_todo method in src/todo_app/services/todo_service.py
- [ ] T036 [US4] Implement update command in CLI interface in src/todo_app/cli/cli.py
- [ ] T037 [US4] Add validation for empty descriptions in src/todo_app/services/todo_service.py
- [ ] T038 [US4] Add validation for non-existent IDs in src/todo_app/services/todo_service.py

---

## Phase 7: User Story 5 - Delete Todo Items (Priority: P2)

**Goal**: Enable users to delete todo items from the list

**Independent Test**: Run the application, add a todo item, delete it, then verify it no longer appears when viewing

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T039 [P] [US5] Unit test for TodoService delete functionality in tests/unit/test_todo_service.py
- [ ] T040 [P] [US5] Integration test for delete command in tests/integration/test_cli.py

### Implementation for User Story 5

- [ ] T041 [P] [US5] Implement TodoList delete operation in src/todo_app/models/todo.py
- [ ] T042 [US5] Implement TodoService delete_todo method in src/todo_app/services/todo_service.py
- [ ] T043 [US5] Implement delete command in CLI interface in src/todo_app/cli/cli.py
- [ ] T044 [US5] Add validation for non-existent IDs in src/todo_app/services/todo_service.py

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T045 [P] Add help command to CLI interface in src/todo_app/cli/cli.py
- [ ] T046 [P] Add quit command to CLI interface in src/todo_app/cli/cli.py
- [ ] T047 [P] Implement main application loop in src/todo_app/main.py
- [ ] T048 [P] Add error handling for invalid commands in src/todo_app/cli/cli.py
- [ ] T049 [P] Add error handling for invalid IDs in src/todo_app/cli/cli.py
- [ ] T050 [P] Add proper argument parsing for CLI commands in src/todo_app/cli/cli.py
- [ ] T051 [P] Add comprehensive error messages based on CLI contract in src/todo_app/cli/cli.py
- [ ] T052 [P] Add input validation for edge cases in src/todo_app/services/todo_service.py
- [ ] T053 [P] Add additional unit tests for edge cases in tests/unit/
- [ ] T054 Run quickstart validation with all implemented features

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Todo model in tests/unit/test_todo.py"
Task: "Unit test for TodoService add functionality in tests/unit/test_todo_service.py"
Task: "Integration test for add command in tests/integration/test_cli.py"

# Launch all models for User Story 1 together:
Task: "Implement Todo model with id, title, completed fields in src/todo_app/models/todo.py"
Task: "Implement TodoList add operation in src/todo_app/models/todo.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence