---

description: "Task list for CLI Todo App - Organization & Usability Enhancements implementation"
---

# Tasks: CLI Todo App - Organization & Usability Enhancements

**Input**: Design documents from `/specs/002-todo-enhancements/`
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

- [X] T010 Extend Task model in src/models/task.py with priority, tags, due_date attributes
- [X] T011 Update Task validation in src/models/task.py for new fields (priority, tags, due_date)
- [X] T012 Update TaskManager service in src/services/task_manager.py to handle new fields
- [X] T013 Implement search functionality in src/services/task_manager.py
- [X] T014 Implement filter functionality in src/services/task_manager.py
- [X] T015 Implement sort functionality in src/services/task_manager.py
- [X] T016 Create command parsing utilities in src/utils/helpers.py for optional flags
- [X] T017 Create validation utilities in src/utils/helpers.py for new fields

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task with Priority, Tags, and Due Date (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks with additional organizational features like priority, tags, and due date using enhanced "add" command with optional flags.

**Independent Test**: The feature can be fully tested by running the CLI app, entering the enhanced add command with priority, tags, and due date flags, and verifying that the task is created with all specified attributes while maintaining the original behavior when flags are omitted.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US1] Unit test for Task model validation of new fields in tests/unit/test_task.py
- [ ] T019 [P] [US1] Unit test for TaskManager add_task functionality with new fields in tests/unit/test_task_manager.py

### Implementation for User Story 1

- [X] T020 [US1] Implement enhanced add command in src/ui/cli.py with support for --priority, --tags, --due flags
- [X] T021 [US1] Connect enhanced add command to TaskManager service in src/main.py
- [X] T022 [US1] Implement command parsing for optional flags in src/ui/cli.py
- [X] T023 [US1] Add validation for new field inputs in src/services/task_manager.py
- [X] T024 [US1] Ensure backward compatibility with original add command syntax in src/ui/cli.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Enhanced Task List (Priority: P2)

**Goal**: Enable users to see all their tasks with the new organizational information displayed, showing priority indicators, tags, and due dates when present, while maintaining the original formatting for tasks without these attributes.

**Independent Test**: The feature can be tested by adding tasks with various combinations of priority, tags, and due dates, then using the list command to verify that the new information is displayed appropriately.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T025 [P] [US2] Unit test for TaskManager get_all_tasks functionality with enhanced display in tests/unit/test_task_manager.py

### Implementation for User Story 2

- [X] T026 [US2] Implement enhanced list command in src/ui/cli.py with conditional display of new fields
- [X] T027 [US2] Connect enhanced list command to TaskManager service in src/main.py
- [X] T028 [US2] Implement formatted display of tasks with priority, tags, due_date indicators in src/ui/cli.py
- [X] T029 [US2] Handle backward compatibility by keeping original format when no new fields in src/ui/cli.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Search Tasks by Keyword (Priority: P3)

**Goal**: Enable users to find specific tasks by searching for keywords across title, description, and tags using the new "search" command.

**Independent Test**: The feature can be tested by adding multiple tasks with different content, then using the search command to verify that matching tasks are returned.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T030 [P] [US3] Unit test for TaskManager search functionality in tests/unit/test_task_manager.py

### Implementation for User Story 3

- [X] T031 [US3] Implement search command in src/ui/cli.py
- [X] T032 [US3] Connect search command to TaskManager service in src/main.py
- [X] T033 [US3] Implement search algorithm that searches across title, description, and tags in src/services/task_manager.py
- [X] T034 [US3] Format search results in the same list format as regular list command in src/ui/cli.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Filter Tasks (Priority: P4)

**Goal**: Enable users to view tasks that match specific criteria using the new "filter" command with various options to narrow down the task list.

**Independent Test**: The feature can be tested by adding tasks with various attributes, then using the filter command with different criteria to verify that only matching tasks are displayed.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T035 [P] [US4] Unit test for TaskManager filter functionality in tests/unit/test_task_manager.py

### Implementation for User Story 4

- [X] T036 [US4] Implement filter command in src/ui/cli.py
- [X] T037 [US4] Connect filter command to TaskManager service in src/main.py
- [X] T038 [US4] Implement filter algorithms for status, priority, tags, and due date in src/services/task_manager.py
- [X] T039 [US4] Handle multiple filter conditions with AND logic in src/services/task_manager.py

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Sort Tasks (Priority: P5)

**Goal**: Enable users to view tasks in a specific order using the new "sort" command with different criteria to organize the task list.

**Independent Test**: The feature can be tested by adding tasks with various attributes, then using the sort command with different criteria to verify that tasks are displayed in the correct order.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T040 [P] [US5] Unit test for TaskManager sort functionality in tests/unit/test_task_manager.py

### Implementation for User Story 5

- [X] T041 [US5] Implement sort command in src/ui/cli.py
- [X] T042 [US5] Connect sort command to TaskManager service in src/main.py
- [X] T043 [US5] Implement sort algorithms for priority, due date, and alphabetical in src/services/task_manager.py
- [X] T044 [US5] Handle persistent sorting until changed by user in src/services/task_manager.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Update Command Enhancement

**Goal**: Enhance the update command to accept optional priority, tags, and due date parameters while maintaining backward compatibility.

- [X] T045 Implement enhanced update command in src/ui/cli.py with support for --priority, --tags, --due flags
- [X] T046 Connect enhanced update command to TaskManager service in src/main.py
- [X] T047 Add validation for new field inputs in update command in src/services/task_manager.py
- [X] T048 Ensure backward compatibility with original update command syntax in src/ui/cli.py

---

## Phase 9: CLI Interface & Main Loop

**Goal**: Complete the command-line interface and main application loop with all new functionality.

- [X] T049 Implement main application loop in src/main.py with all new commands
- [X] T050 Implement command routing for all commands in src/ui/cli.py
- [X] T051 Implement help command with new options in src/ui/cli.py
- [X] T052 Implement quit/exit command in src/ui/cli.py
- [X] T053 Add comprehensive error handling for CLI commands in src/ui/cli.py

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T054 Documentation updates in README.md
- [X] T055 Code cleanup and refactoring
- [X] T056 [P] Additional unit tests in tests/unit/
- [X] T057 Security hardening
- [X] T058 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Update Command Enhancement (Phase 8)**: Depends on User Story 1 completion
- **CLI Interface (Phase 9)**: Depends on all user story implementations
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
Task: "Unit test for Task model validation of new fields in tests/unit/test_task.py"
Task: "Unit test for TaskManager add_task functionality with new fields in tests/unit/test_task_manager.py"

# Launch implementation tasks:
Task: "Implement enhanced add command in src/ui/cli.py with support for --priority, --tags, --due flags"
Task: "Connect enhanced add command to TaskManager service in src/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 9: CLI Interface & Main Loop
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