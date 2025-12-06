# Implementation Plan: Physical AI & Humanoid Robotics Course

**Branch**: `002-physical-ai-course` | **Date**: 2025-12-06 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/002-physical-ai-course/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create a 4-module, code-driven course on Physical AI and Humanoid Robotics using Docusaurus v3. The project features a custom "futuristic" theme, integrates three major simulators (Isaac Sim, Gazebo, Webots) in dedicated modules, and uses Python/ROS 2 Jazzy for all technical examples.

## Technical Context

**Language/Version**: Node.js 18+ (Docusaurus), Python 3.10+ (Code Snippets)
**Primary Dependencies**: Docusaurus v3 (Existing), Infima (Styling), React 18
**Storage**: JSON (`data/resources.json` for curated list)
**Testing**: `npm run build` (Site), Manual Verification (Code Snippets)
**Target Platform**: GitHub Pages (Existing pipeline)
**Project Type**: Static Site / Educational Courseware
**Performance Goals**: Homepage load < 2s
**Constraints**: No diagrams (Code only), Dark/Neon Theme, ROS 2 Jazzy
**Scale/Scope**: 4 Modules, ~20-30 Chapters total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Spec-First & Modular Design**: ✅ Modules defined upfront (Foundations, Isaac, Gazebo, Webots).
- **II. Educational Integrity**: ✅ Curated resources via MCP; verified ROS 2 distro.
- **III. Transparency**: ✅ Resource metadata schema defined in data model.
- **IV. Developer-Centric**: ✅ Code-first constraint (<3 snippets/chapter) replaces diagrams.
- **VI. Web Ergonomics**: ✅ Futuristic theme focuses on readability and navigation.

## Project Structure

### Documentation (this feature)

```text
specs/002-physical-ai-course/
├── plan.md
├── research.md          # Simulator & Theme decisions
├── data-model.md        # Module/Chapter schema
├── quickstart.md        # Theme dev guide
└── tasks.md
```

### Source Code (repository root)

```text
docs/
├── module-01-foundations/
├── module-02-isaac-sim/
├── module-03-gazebo/
└── module-04-webots/
src/
├── css/
│   └── custom.css       # Futuristic overrides
├── components/
│   ├── HomepageFeatures/ # (Refactor to ModuleCards)
│   └── ResourceList/    # New component
data/
└── resources.json       # Curated DB
docusaurus.config.ts     # Config updates
sidebars.ts              # 4-Module structure
```

**Structure Decision**: Additions to existing Docusaurus root; no new repo required.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |