<!--
Sync Impact Report:
- Version change: 1.0.0 -> 1.1.0
- List of modified principles: II. Technical Accuracy (Added MCP server requirement)
- Added sections: None
- Removed sections: None
- Templates requiring updates: None
- Follow-up TODOs: None
-->

# AI/Spec-Driven Book Creation using Docusaurus Constitution

## Core Principles

### I. Spec-First Development
Book structure, chapters, and workflows must be defined and approved before content creation begins. This ensures a coherent narrative arc and prevents "content drift" where chapters diverge from the central theme. Changes to the structure require a spec update.

### II. Technical Accuracy
All technical explanations, especially those related to Docusaurus, GitHub Pages, and documentation tooling, must be validated against official sources. Agents must leverage available MCP servers to retrieve and verify authoritative information directly from official documentation before generation. We do not publish unverified claims. If an official source contradicts a common practice, we follow the official source or explicitly explain the deviation.

### III. Developer-Centric Clarity
Content is optimized for software engineers and technical writers. Avoid fluff; focus on actionable, precise instructions. Use standard industry terminology correctly. Assume a reader who values their time and seeks specific technical outcomes.

### IV. Workflow Automation
We enforce reproducibility using Spec-Kit Plus automation primitives. Manual, undocumented steps are prohibited for build and deployment processes. The book creation process itself should serve as an example of the automation principles it teaches.

### V. Version-Controlled Knowledge
All content, including text, diagrams, and code examples, must be traceable and diff-friendly in Git repositories. We treat documentation as code. 'Binary blobs' for text content are forbidden; use Markdown.

## Project Standards & Constraints

### Standards
- **Validation**: All instructions must be cross-referenced with official Docusaurus v3, GitHub, and GitHub Actions documentation.
- **Code Examples**: Must be runnable and tested within a minimal Docusaurus setup.
- **Style**: Concise, modular, and suitable for static documentation platforms (e.g., avoiding "click here" links, using semantic structure).
- **Citations**: Use inline hyperlinks to primary sources (official docs preferred).
- **Visuals**: Visual architecture diagrams must be included where relevant (generated or referenced). Minimum of 3 diagrams (PNG/SVG) required for the book.

### Constraints
- **Format**: Standard Docusaurus v3 project structure.
- **Deployment**: GitHub Pages via automated CI/CD (GitHub Actions).
- **Scope**: 8–12 chapters, each 600–1200 words.
- **Visibility**: Repository must be public.
- **Pipeline**: A working deployment pipeline on push is mandatory.

## Success Criteria & Definition of Done

- **Build Success**: Book builds successfully locally and via GitHub Actions without warnings or errors.
- **Live Deployment**: GitHub Pages deployment URL is live, stable, and matches the specification.
- **Verification**: All instructions are confirmed by official docs or verified examples.
- **Tooling**: Spec-Kit Plus is used to generate, validate, and maintain the project structure.
- **Value**: Content is assessed as clear, accurate, and useful for developers building documentation pipelines.

## Governance

Constitution supersedes all other practices. Amendments require documentation, approval, and a migration plan.

All Pull Requests and reviews must verify compliance with these principles. Complexity in the workflow or content must be justified against the principle of Developer-Centric Clarity.

**Version**: 1.1.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
