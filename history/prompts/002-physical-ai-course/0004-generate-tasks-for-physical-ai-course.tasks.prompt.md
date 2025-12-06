---
id: 0004
title: Generate Tasks for Physical AI Course
stage: tasks
date: 2025-12-06
surface: agent
model: gemini-2.0-flash-exp
feature: 002-physical-ai-course
branch: 002-physical-ai-course
user: user
command: /sp.tasks
labels: ["tasks", "planning", "physical-ai"]
links:
  spec: specs/002-physical-ai-course/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-physical-ai-course/tasks.md
tests:
  - none
---

## Prompt

/sp.tasks

## Response snapshot

Generated `tasks.md` with 22 tasks across 6 phases.
- Phase 1: Setup (3 tasks)
- Phase 2: Foundational (3 tasks)
- Phase 3: US1 Theme/Home (4 tasks)
- Phase 4: US2 Module 1 Content (5 tasks)
- Phase 5: US3 Resources (4 tasks)
- Phase 6: Polish (3 tasks)

## Outcome

- ✅ Impact: Actionable roadmap defined for course implementation.
- 🧪 Tests: None included.
- 📁 Files: 1 file created.
- 🔁 Next prompts: /sp.check or start implementation.
- 🧠 Reflection: Tasks focus heavily on content structure and theming, which are the core differentiators for this feature.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None
