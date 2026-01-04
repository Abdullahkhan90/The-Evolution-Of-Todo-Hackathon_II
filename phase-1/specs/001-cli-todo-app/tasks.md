---

description: "Task list for CLI Todo Application implementation"
---

# Tasks: CLI Todo Application

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/ directory
- [X] T002 [P] Create models directory: src/models/
- [X] T003 [P] Create services directory: src/services/
- [X] T004 [P] Create ui directory: src/ui/
- [X] T005 [P] Create utils directory: src/utils/
- [X] T006 [P] Create tests directory: tests/
- [X] T007 [P] Create tests/unit directory: tests/unit/
- [X] T008 [P] Create tests/integration directory: tests/integration/
- [X] T009 [P] Create tests/contract directory: tests/contract/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T010 Create Task model in src/models/task.py with id, title, description, completed attributes
- [X] T011 Create ID generation utility in src/utils/helpers.py for auto-incrementing integers
- [X] T012 Create TaskManager service in src/services/task_manager.py with in-memory storage
- [X] T013 Implement Task validation in src/models/task.py (title length, etc.)
- [X] T014 Implement basic CRUD operations in TaskManager (add, get, update, delete, list)
- [X] T015 Implement error handling utilities in src/utils/helpers.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks with title and optional description

**Independent Test**: The feature can be fully tested by running the CLI app, entering the add task command with a title and description, and verifying that the task appears in the list with a unique ID and "incomplete" status.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US1] Unit test for Task model validation in tests/unit/test_task.py
- [ ] T017 [P] [US1] Unit test for TaskManager add_task functionality in tests/unit/test_task_manager.py

### Implementation for User Story 1

- [X] T018 [US1] Implement add_task command in src/ui/cli.py
- [X] T019 [US1] Connect add_task command to TaskManager service in src/main.py
- [X] T020 [US1] Implement command parsing for add command in src/ui/cli.py
- [X] T021 [US1] Add error handling for empty title in src/services/task_manager.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P2)

**Goal**: Enable users to see all their tasks with ID, title, description, and completion status

**Independent Test**: The feature can be tested by adding tasks to the system and then using the view command to verify that all tasks are displayed correctly with their details.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T022 [P] [US2] Unit test for TaskManager get_all_tasks functionality in tests/unit/test_task_manager.py

### Implementation for User Story 2

- [X] T023 [US2] Implement list command in src/ui/cli.py
- [X] T024 [US2] Connect list command to TaskManager service in src/main.py
- [X] T025 [US2] Implement formatted display of tasks with status indicators in src/ui/cli.py
- [X] T026 [US2] Handle empty list case with appropriate message in src/ui/cli.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Task as Complete (Priority: P3)

**Goal**: Enable users to mark tasks as complete after finishing them

**Independent Test**: The feature can be tested by adding a task, using the mark complete command with its ID, and verifying that the task's status has changed to complete.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T027 [P] [US3] Unit test for TaskManager mark_task_complete functionality in tests/unit/test_task_manager.py

### Implementation for User Story 3

- [X] T028 [US3] Implement complete command in src/ui/cli.py
- [X] T029 [US3] Connect complete command to TaskManager service in src/main.py
- [X] T030 [US3] Add error handling for invalid task IDs in src/services/task_manager.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task Details (Priority: P4)

**Goal**: Enable users to modify existing task's title or description

**Independent Test**: The feature can be tested by adding a task, updating its details, and verifying that the changes are reflected in the system.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US4] Unit test for TaskManager update_task functionality in tests/unit/test_task_manager.py

### Implementation for User Story 4

- [X] T032 [US4] Implement update command in src/ui/cli.py
- [X] T033 [US4] Connect update command to TaskManager service in src/main.py
- [X] T034 [US4] Add validation for update command parameters in src/services/task_manager.py

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Task (Priority: P5)

**Goal**: Enable users to remove tasks from their list

**Independent Test**: The feature can be tested by adding a task, deleting it, and verifying that it no longer appears in the task list.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T035 [P] [US5] Unit test for TaskManager delete_task functionality in tests/unit/test_task_manager.py

### Implementation for User Story 5

- [X] T036 [US5] Implement delete command in src/ui/cli.py
- [X] T037 [US5] Connect delete command to TaskManager service in src/main.py
- [X] T038 [US5] Add error handling for delete operations in src/services/task_manager.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: CLI Interface & Main Loop

**Goal**: Complete the command-line interface and main application loop

- [X] T039 Implement main application loop in src/main.py
- [X] T040 Implement command routing for all commands in src/ui/cli.py
- [X] T041 Implement help command in src/ui/cli.py
- [X] T042 Implement quit/exit command in src/ui/cli.py
- [X] T043 Add comprehensive error handling for CLI commands in src/ui/cli.py

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T044 Documentation updates in README.md
- [X] T045 Code cleanup and refactoring
- [X] T046 [P] Additional unit tests in tests/unit/
- [X] T047 Security hardening
- [X] T048 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **CLI Interface (Phase 8)**: Depends on all user story implementations
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

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
Task: "Unit test for Task model validation in tests/unit/test_task.py"
Task: "Unit test for TaskManager add_task functionality in tests/unit/test_task_manager.py"

# Launch implementation tasks:
Task: "Implement add_task command in src/ui/cli.py"
Task: "Connect add_task command to TaskManager service in src/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 8: CLI Interface & Main Loop
5. **STOP and VALIDATE**: Test User Story 1 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
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