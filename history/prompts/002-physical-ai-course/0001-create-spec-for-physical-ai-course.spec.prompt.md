---
id: 0001
title: Create Spec for Physical AI Course
stage: spec
date: 2025-12-06
surface: agent
model: gemini-2.0-flash-exp
feature: 002-physical-ai-course
branch: 002-physical-ai-course
user: user
command: /sp.specify
labels: ["spec", "physical-ai", "docusaurus", "code-driven"]
links:
  spec: specs/002-physical-ai-course/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-physical-ai-course/spec.md
  - specs/002-physical-ai-course/checklists/requirements.md
tests:
  - none
---

## Prompt

Physical AI & Humanoid Robotics Course with 4 Modules (Futuristic Theme, Code-Driven) Target audience:- Students, engineers, and educators studying Physical AI, robotics, and embodied intelligence- Developers working with ROS 2, simulation frameworks, NVIDIA Isaac, and Vision-Language-Action systems- Learners who benefit from hands-on, code-first explanationsFocus:- Build a 4-module course book inside Docusaurus v3 with a futuristic UI theme- Prioritize actionable **code snippets** instead of diagrams- Integrate high-quality AI/robotics learning resources obtained via MCP-server search- Use Module 1 (provided markdown) as the reference structure for all modules- Auto-generate a clean, futuristic Docusaurus homepage based on course metadataCourse structure:- Total modules: 4 - Each module contains 4–8 chapters - Each chapter includes: • Learning objectives • Minimum 3 code snippets (Python, ROS 2, Isaac, VLA pipelines, etc.) • Concept explanation • Practical mini-exercises - Module 1 is already provided and should be converted into structured MDX chapters- Modules 2–4 must follow the same pedagogical depth and toneSuccess criteria:- Docusaurus site builds successfully and deploys on GitHub Pages using GitHub Actions- Homepage generated from course metadata: • Course overview • Module list + summaries • Key skills learned • Essential AI learning resources (via MCP Server → validated → indexed) - MCP server search produces a curated list of AI/robotics books; results must be human-verified- Code snippets render correctly in MDX on all device sizes- The theme uses a futuristic style (dark mode, neon accents, smooth UI transitions)- Navigation is intuitive, with module → chapter paths clearly structuredConstraints:- Replace all diagram requirements with code requirements: • At least 3 **code snippets per chapter** • Code must be runnable or syntactically correct - Content type: MDX (no diagrams required)- Theme: Futuristic, cyber-neon, clean typography, minimalistic UI- MCP search requirements: • “Best AI course books” • “Top robotics and ROS 2 learning resources” • “Modern embodied AI curriculum references”- Repository must be public, fully versioned, with a changelog- All content must comply with the `/sp.constitution` (accuracy, reproducibility, official-source verification)Timeline:- MCP resource collection/verification: 48–72 hours - Final module outline: 48 hours - Writing + code example creation for Modules 2–4: 3–5 weeks - Theme + homepage design: 1 week - Final deployment: within 45 daysNot building:- Diagrams of any kind (SVG/PNG/flowcharts) — replaced by code and narrative - A commercial e-learning system - Non-technical beginner-level AI explanations - ROS hardware build guides or mechanical designs - In-depth AI ethics coverage (separate course)Homepage requirements:- Hero section with futuristic gradient, neon accent glow, and subtle animations - High-level module cards (Module 1–4) auto-generated from metadata - "Start Learning" CTA button - "Essential AI Resources" section linked to the MCP-derived resource list - Smooth scroll sections and responsive layoutAdditional requirements:- Course content must emphasize hands-on, code-first robotics and AI development - Code should follow best practices (naming, modularity, comments, safety notes) - Each module should end with a short coding challenge or scenario-based exercise

## Response snapshot

Created feature branch `002-physical-ai-course` and specification file `specs/002-physical-ai-course/spec.md`. Defined 3 key user stories: Course Foundation/Theme, Module 1 Code-Driven Content, and Automated Resource Curation.

## Outcome

- ✅ Impact: Detailed spec created for 4-module robotics course.
- 🧪 Tests: None
- 📁 Files: 2 files created
- 🔁 Next prompts: /sp.clarify
- 🧠 Reflection: Explicitly replaced diagram requirements with "code snippet" requirements per user constraint.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None