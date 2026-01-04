# Implementation Plan: CLI Todo App - Organization & Usability Enhancements

**Branch**: `002-todo-enhancements` | **Date**: 2025-12-28 | **Spec**: [spec link](./spec.md)
**Input**: Feature specification from `/specs/002-todo-enhancements/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of intermediate-level organization and usability enhancements for the CLI Todo Application. This includes adding optional priority, tags, and due date fields to tasks, enhancing the list output to show these fields when present, and introducing new commands for search, filter, and sort functionality. The implementation maintains 100% backward compatibility with the Basic Level (Phase I) functionality.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Built-in Python modules only (no external dependencies beyond what's in standard library)
**Storage**: In-memory only (list of Task objects) - consistent with Basic Level
**Testing**: pytest for unit and integration tests
**Target Platform**: Cross-platform (Windows, macOS, Linux) console application
**Project Type**: Single project CLI application
**Performance Goals**: Instantaneous operations (sub-100ms for all operations) since using in-memory storage
**Constraints**: 
- No external dependencies beyond Python 3.13+ standard library
- CLI interface only
- In-memory storage only
- 100% backward compatibility with Basic Level commands
- New fields must be optional when using old commands
- New functionality must be additive only
**Scale/Scope**: Single user, single session application with up to 1000 tasks in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-driven, Agentic Development: All features derive from specifications in spec.md
- ✅ Strict Non-breaking Progression: All Basic Level functionality preserved with identical syntax and output
- ✅ Clean, Modular, Extensible Architecture: Will follow clean architecture principles with separation of concerns
- ✅ Focus Progression: DevX → UserX → Intelligence → Production: Starting with developer and user experience
- ✅ Traceable Evaluation Process: Following spec-driven development with full traceability
- ✅ Universal Architecture Rules: Using Python 3.13+, UV, and standard project structure

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-enhancements/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py              # Main entry point with CLI loop
├── models/
│   └── task.py          # Enhanced Task class definition with priority, tags, due_date
├── services/
│   └── task_manager.py  # CRUD operations for tasks with new fields support
├── ui/
│   └── cli.py           # CLI interface functions with enhanced command parsing
└── utils/
    └── helpers.py       # Utility functions (validation, parsing, etc.)
```

### Tests

```text
tests/
├── unit/
│   ├── test_task.py     # Task model tests
│   └── test_task_manager.py  # Task manager service tests
├── integration/
│   └── test_cli_flow.py # CLI interaction tests
└── contract/
    └── test_api_contract.py  # API contract tests
```

**Structure Decision**: Single project structure selected as per constitution. The application follows a clean architecture with separation of concerns: models for data, services for business logic, UI for presentation, and utils for helpers. Enhanced to support new organizational features while maintaining backward compatibility.

## Key Technical Decisions

### 1. Task Model Extension
- **Decision**: Extend existing Task class with optional fields (priority, tags, due_date)
- **Rationale**: Maintains backward compatibility while adding new functionality
- **Alternatives considered**: 
  - Separate task classes: Would complicate the architecture
  - Database migration: Not applicable for in-memory storage
- **Selected**: Extend existing Task class with optional fields

### 2. Priority Representation
- **Decision**: Use string enum with values "high", "medium", "low" (case-insensitive)
- **Rationale**: More user-friendly than numeric values, clear semantics
- **Alternatives considered**:
  - Integer values (1, 2, 3): Less intuitive for users
  - Single letters (h, m, l): Concise but potentially confusing
- **Selected**: String values "high", "medium", "low" with aliases (h, m, l)

### 3. Tags Storage
- **Decision**: Store as list[str] to allow multiple tags per task
- **Rationale**: Enables multiple categorization of tasks, maintains order if needed
- **Alternatives considered**:
  - Set[str]: Would prevent duplicates but lose order
  - Single string with delimiter: Less structured
- **Selected**: List[str] for flexibility

### 4. Command Parsing Strategy
- **Decision**: Enhance existing parser to support optional flags (--priority, --tags, --due) while maintaining simple syntax
- **Rationale**: Preserves backward compatibility while enabling new functionality
- **Alternatives considered**:
  - Separate command parsers: Would increase complexity
  - Require new syntax for all commands: Would break compatibility
- **Selected**: Flexible parser that supports both old and new syntax

### 5. Date Format
- **Decision**: Use ISO 8601 format (YYYY-MM-DD) for due dates
- **Rationale**: Standard format, unambiguous, easily sortable
- **Alternatives considered**:
  - Natural language parsing: More user-friendly but complex
  - Different formats: Would create inconsistency
- **Selected**: ISO 8601 format for consistency and simplicity

### 6. List Output Enhancement
- **Decision**: Show new fields only when present, maintain original format otherwise
- **Rationale**: Preserves familiar output while adding value when applicable
- **Alternatives considered**:
  - Always show placeholders: Would clutter output
  - Completely new format: Would break user expectations
- **Selected**: Conditional display based on field presence

### 7. Filtering Implementation
- **Decision**: In-memory filtering applied to current task list
- **Rationale**: Simple implementation that works with existing in-memory storage
- **Alternatives considered**:
  - Pre-computed indexes: More complex, unnecessary for in-memory
  - Database-style queries: Overkill for this phase
- **Selected**: Runtime filtering of in-memory list

## Implementation Phases

### Phase 1: Task Model Extension
1. Extend Task class with optional priority, tags, and due_date fields
2. Update validation logic for new fields
3. Write unit tests for enhanced Task model

### Phase 2: Task Manager Service Enhancement
1. Update TaskManager to handle new fields in CRUD operations
2. Implement search functionality across title, description, and tags
3. Implement filter functionality for various criteria
4. Implement sort functionality for different criteria
5. Write unit tests for enhanced TaskManager

### Phase 3: CLI Interface Enhancement
1. Enhance command parser to support optional flags (--priority, --tags, --due)
2. Implement new commands (search, filter, sort)
3. Update list command to show enhanced output when applicable
4. Update help command to show new options
5. Write integration tests for CLI flows

### Phase 4: Quality Assurance & Documentation
1. Complete test coverage for all new features
2. Verify backward compatibility with Basic Level functionality
3. Update documentation and quickstart guide
4. Run regression tests to ensure no breaking changes

## Quality & Validation Strategy

### Unit Test Coverage Plan
- Task model: 100% coverage of new field validation and accessors
- TaskManager: Full coverage of new search, filter, and sort operations
- CLI interface: Coverage of new command parsing and handling

### Manual Validation Checklist
- [ ] Add task with priority works (new syntax)
- [ ] Add task with tags works (new syntax)
- [ ] Add task with due date works (new syntax)
- [ ] Add task with old syntax still works (backward compatibility)
- [ ] List shows new fields when present
- [ ] List shows original format when no new fields
- [ ] Search finds tasks by title, description, and tags
- [ ] Filter works by priority, tags, status, and due date
- [ ] Sort works by priority, due date, and title
- [ ] All Basic Level commands work identically to before

### Acceptance Criteria Verification
- [ ] SC-001: All 5 Basic Level features remain 100% unchanged in syntax, behavior, and output
- [ ] SC-002: Users can add tasks with priority, tags, and due date using optional flags
- [ ] SC-003: Users can see enhanced information (priority, tags, due date) in the list output when present
- [ ] SC-004: Users can search tasks by keyword across title, description, and tags
- [ ] SC-005: Users can filter tasks by priority, tags, due date, and completion status
- [ ] SC-006: Users can sort tasks by priority, due date, and title
- [ ] SC-007: New fields (priority, tags, due_date) are optional when using old commands
- [ ] SC-008: When old commands are used, new fields default to None/empty
- [ ] SC-009: List output enhanced to show new fields (but only if present), without breaking old formatting
- [ ] SC-010: Search, filter, and sort commands are new and separate from existing functionality

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |