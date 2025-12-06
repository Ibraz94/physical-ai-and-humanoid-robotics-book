---
id: 0001
title: Update Constitution for AI Course
stage: constitution
date: 2025-12-06
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: 001-docusaurus-book-creation
user: user
command: /sp.constitution
labels: ["governance", "redefinition", "ai-course"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

/sp.constitution Project: Physical AI & Humanoid Robotics Course published via Docusaurus + GitHub PagesCore principles:- Spec-first & modular design: course structure, chapters, and web-site layout defined before content creation  - Educational integrity: course content (books, references, exercises) curated via verified sources  - Transparency and traceability: all included course materials and references clearly documented (source, edition, license)  - Developer-centric documentation: content structured and styled for readability by developers, educators, and technical learners  - Reproducible content pipeline: use Spec-Kit Plus + MCP-server to fetch, validate, and integrate course material; version controlled  - Web ergonomics: home page and navigation UX designed for clarity — straightforward discoverability of course modules, lessons, resources  Key standards:- Course resources (books, papers, tutorials) must be hand-verified: metadata (title, author, edition, publication date, license) included  - Use of an “MCP-server” query tool (or equivalent) to search and suggest the “best” AI-course books & resources — results must then be manually reviewed for suitability  - Citation/reference format: inline hyperlinks + metadata (author, year, title, publisher) in a reference list (or footnote) — minimally license-compliant if content is non-public domain  - For each course module: provide learning objectives, required resources, optional resources, estimated time-to-complete, prerequisites (if any)  - Content style: modular, navigable, and consistent with Docusaurus/MDX practices; code examples or sample diagrams when relevant  - Home page design: highlights course overview, module list, quick start guide, and resource repository; must be responsive and clean  Constraints:- Course content must be organized into modules — minimum 6, maximum 15 modules  - For each module: at least 1 required resource (book or paper), up to 3 optional resources  - Resources fetched via MCP-server must be licensed appropriately (open license, or permissible for educational reference)  - Home page and navigation must render properly in Docusaurus v3 and on GitHub Pages in modern browsers  - All content (text, metadata, links) must be stored in Git repository; no external closed-source dependencies required for core course content  - Course content must avoid reliance on proprietary/unlicensed material for core learning (optional resources may reference commercial books if licensing allows referencing)  Success criteria:- Course homepage deployed successfully — shows course title, short description, module listing, quick start instructions, resource link database  - All modules accessible through site navigation with clearly labeled resources, learning objectives, and resource metadata  - Resource database (fetched via MCP-server then reviewed) contains at least 12 distinct, high-quality AI course resources (books/papers/tutorials) relevant to the course focus  - Users (educators or learners) can clone the repo and navigate modules locally or via GitHub Pages without missing files or broken links  - The entire site passes link-checks, build validation, and renders correctly on deployment  - All resource references are traceable (metadata + link) and license-compliant  Governance & Maintenance Principles:- All additions of new course resources must go through a “resource review” step: verify license, metadata, relevance, and record source details in a resource registry (e.g. a JSON or MDX manifest)  - Version control and changelog maintained — major updates to modules or resources versioned (e.g. v1.0, v1.1)  - Community contributions allowed via pull requests — any added modules, resources, or homepage changes must comply with core principles and standards  - Periodic review cycles (every 6 months) to refresh resource list, remove obsolete links, and update deprecated references

## Response snapshot

Updated Constitution to v1.2.0. Redefined project as "Physical AI & Humanoid Robotics Course". Aligned principles with educational goals (Educational Integrity, Web Ergonomics). Set specific constraints on module count (6-15) and resource licensing.

## Outcome

- ✅ Impact: Constitution completely realigned with new project definition.
- 🧪 Tests: None
- 📁 Files: 1 file updated.
- 🔁 Next prompts: /sp.specify (to define the course modules)
- 🧠 Reflection: The shift from "Book Creation" to "Course Creation" required significant renaming of principles and standards, but the underlying Docusaurus infrastructure remains relevant.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None