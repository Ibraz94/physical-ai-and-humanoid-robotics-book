---

description: "Task list template for feature implementation"
---

# Tasks: Physical AI & Humanoid Robotics Course

**Input**: Design documents from `/specs/002-physical-ai-course/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Root**: `.`
- **Docs**: `docs/`
- **Data**: `data/`
- **Config**: `docusaurus.config.ts`, `sidebars.ts`
- **Styles**: `src/css/custom.css`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 [P] Create `data/` directory for resource metadata
- [ ] T002 [P] Create module directory structure in `docs/` (module-01-foundations, module-02-isaac-sim, etc.)
- [ ] T003 [P] Create `src/components/Homepage/` directory for new components

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Configure `sidebars.ts` to define the 4-module hierarchy per data-model.md
- [ ] T005 Update `docusaurus.config.ts` (if needed) to support new sidebars or plugins
- [ ] T006 Initialize `data/resources.json` with an empty array schema

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Course Foundation & Theme (Priority: P1) 🎯 MVP

**Goal**: Access a Docusaurus-powered course site with a futuristic, responsive theme.

**Independent Test**: Deploy the site; verify the homepage loads with the futuristic theme, and the navigation sidebar correctly displays the 4-module hierarchy.

### Implementation for User Story 1

- [ ] T007 [US1] Implement futuristic theme variables (Neon Cyan, Dark Mode defaults) in `src/css/custom.css`
- [ ] T008 [US1] Create `ModuleCards` component in `src/components/Homepage/ModuleCards.tsx`
- [ ] T009 [US1] Update `src/pages/index.tsx` to use the new futuristic Hero and ModuleCards
- [ ] T010 [US1] Verify responsive layout on mobile viewport

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Module 1 Content & Code-Driven Learning (Priority: P2)

**Goal**: Read Module 1 chapters containing runnable code snippets (Python/ROS 2) instead of diagrams.

**Independent Test**: Open a Module 1 chapter; copy a code snippet; verify it is syntactically correct.

### Implementation for User Story 2

- [ ] T011 [P] [US2] Create `docs/module-01-foundations/01-intro.mdx` with Learning Objectives and 3+ Python snippets
- [ ] T012 [P] [US2] Create `docs/module-01-foundations/02-setup-ros2.mdx` with ROS 2 Jazzy setup commands
- [ ] T013 [P] [US2] Create `docs/module-01-foundations/03-nodes-topics.mdx` with Python Node examples
- [ ] T014 [P] [US2] Create `docs/module-01-foundations/04-control-theory.mdx` with Code-First control loops
- [ ] T015 [P] [US2] Create placeholders for Modules 2, 3, 4 (`01-intro.mdx` in each folder) to ensure navigation works

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Automated Resource Curation (Priority: P3)

**Goal**: See a curated list of high-quality AI/robotics resources on the homepage.

**Independent Test**: Verify the "Essential AI Resources" section exists and contains valid links.

### Implementation for User Story 3

- [ ] T016 [US3] Populate `data/resources.json` with at least 12 high-quality entries (Book/Paper/Doc) validated via MCP
- [ ] T017 [US3] Create `ResourceList` component in `src/components/Homepage/ResourceList.tsx` to render JSON data
- [ ] T018 [US3] Add `ResourceList` to `src/pages/index.tsx`
- [ ] T019 [US3] Verify external links in `data/resources.json` are reachable (manual or script check)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T020 [P] Add "glassmorphism" effects to cards in `src/css/custom.css`
- [ ] T021 [P] Ensure code blocks have high contrast in the new dark theme
- [ ] T022 Run `npm run build` to verify all new pages and components build successfully

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent

### Parallel Opportunities

- Tasks T011-T015 (Content) can run in parallel with T007-T010 (Theme)
- Tasks T016 (Data Entry) can run in parallel with any implementation task

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Verify futuristic homepage and module navigation.

### Incremental Delivery

1. Complete Setup + Foundational
2. Add User Story 1 → Deploy Theme & Skeleton
3. Add User Story 2 → Deploy Module 1 Content
4. Add User Story 3 → Deploy Resource Directory
