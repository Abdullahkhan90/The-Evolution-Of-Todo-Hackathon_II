# Tasks: CLI Todo App - Intelligent Features

**Input**: Design documents from `/specs/003-intelligent-todo-features/`
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

- [X] T001 Install dateparser library for natural language date parsing
- [X] T002 [P] Update Task model in src/models/task.py with recurrence and datetime due_date fields
- [X] T003 [P] Update Task validation in src/models/task.py for new fields
- [X] T004 [P] Create date parsing utilities in src/utils/helpers.py
- [X] T005 [P] Update TaskManager service in src/services/task_manager.py to handle new fields

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Implement recurring task functionality in src/services/task_manager.py
- [X] T007 Implement natural language date parsing in src/utils/helpers.py
- [X] T008 Implement reminder system logic in src/services/task_manager.py
- [X] T009 Update CLI interface in src/ui/cli.py to support new features
- [X] T010 Update main application loop in src/main.py to integrate new features

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Recurring Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks that repeat regularly (e.g., weekly team meeting, monthly report) using the enhanced "add" command with a recurring pattern flag.

**Independent Test**: The feature can be fully tested by running the CLI app, entering the enhanced add command with a recurring pattern flag (e.g., --recurring weekly), completing the task, and verifying that a new instance of the task is automatically created with an updated due date.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T011 [P] [US1] Unit test for Task model validation of recurrence field in tests/unit/test_task.py
- [ ] T012 [P] [US1] Unit test for TaskManager recurring task functionality in tests/unit/test_task_manager.py

### Implementation for User Story 1

- [X] T013 [US1] Implement recurring task creation in src/ui/cli.py with --recurring flag support
- [X] T014 [US1] Connect recurring task creation to TaskManager service in src/main.py
- [X] T015 [US1] Implement recurrence pattern validation in src/utils/helpers.py
- [X] T016 [US1] Add recurrence handling to complete command in src/services/task_manager.py
- [X] T017 [US1] Ensure backward compatibility with original add command syntax in src/ui/cli.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Natural Language Date Input (Priority: P2)

**Goal**: Enable users to set due dates using natural language phrases (e.g., "tomorrow at 3pm", "next Monday morning") with the enhanced "add" or "update" command.

**Independent Test**: The feature can be tested by running the CLI app, entering commands with natural language dates (e.g., --due "tomorrow at 5pm"), and verifying that the system correctly parses and sets the due date/time.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Unit test for natural language date parsing in tests/unit/test_utils.py

### Implementation for User Story 2

- [X] T019 [US2] Implement natural language date parsing in src/utils/helpers.py
- [X] T020 [US2] Connect date parsing to add/update commands in src/ui/cli.py
- [X] T021 [US2] Update TaskManager to handle datetime objects for due dates in src/services/task_manager.py
- [X] T022 [US2] Add validation for parsed datetime objects in src/utils/helpers.py
- [X] T023 [US2] Ensure backward compatibility with original date handling in src/ui/cli.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - View Upcoming Due Tasks (Priority: P3)

**Goal**: Enable users to see tasks that are due soon or overdue with notifications displayed on application startup.

**Independent Test**: The feature can be tested by creating tasks with various due dates (some in the future, some in the past), starting the application, and verifying that appropriate reminders are displayed for upcoming and overdue tasks.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T024 [P] [US3] Unit test for reminder system in tests/unit/test_task_manager.py

### Implementation for User Story 3

- [X] T025 [US3] Implement startup reminder logic in src/main.py
- [X] T026 [US3] Create function to identify upcoming tasks in src/services/task_manager.py
- [X] T027 [US3] Create function to identify overdue tasks in src/services/task_manager.py
- [X] T028 [US3] Format reminder messages for console display in src/ui/cli.py
- [X] T029 [US3] Integrate reminder system with main application loop in src/main.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Enhanced Task List View (Priority: P4)

**Goal**: Enable users to see all their tasks with enhanced organizational information displayed, including recurrence patterns and detailed due dates/times.

**Independent Test**: The feature can be tested by adding tasks with various recurrence patterns and detailed due dates, then using the list command to verify that the new information is displayed appropriately.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T030 [P] [US4] Unit test for enhanced list display in tests/unit/test_cli.py

### Implementation for User Story 4

- [X] T031 [US4] Update list command to show recurrence patterns in src/ui/cli.py
- [X] T032 [US4] Update list command to show detailed due date/time in src/ui/cli.py
- [X] T033 [US4] Implement conditional display logic for new fields in src/ui/cli.py
- [X] T034 [US4] Maintain backward compatibility for tasks without new fields in src/ui/cli.py
- [X] T035 [US4] Update help command to show new options in src/ui/cli.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Integration & Polish

**Purpose**: Cross-cutting concerns that affect multiple user stories

- [X] T036 Update command parsing to handle new optional flags in src/ui/cli.py
- [X] T037 Add comprehensive error handling for new features in src/ui/cli.py
- [X] T038 Update documentation in README.md with new features
- [X] T039 [P] Add additional unit tests for edge cases in tests/unit/
- [X] T040 Run integration tests to verify all features work together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Integration & Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

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
Task: "Unit test for Task model validation of recurrence field in tests/unit/test_task.py"
Task: "Unit test for TaskManager recurring task functionality in tests/unit/test_task_manager.py"

# Launch implementation tasks:
Task: "Implement recurring task creation in src/ui/cli.py with --recurring flag support"
Task: "Connect recurring task creation to TaskManager service in src/main.py"
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

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
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