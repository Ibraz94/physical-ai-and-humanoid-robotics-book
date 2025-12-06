<!--
Sync Impact Report:
- Version change: 1.1.0 -> 1.2.0
- List of modified principles: II. Educational Integrity (Renamed from Technical Accuracy), IV. Developer-Centric Documentation (Renamed from Developer-Centric Clarity), VI. Web Ergonomics (New Principle)
- Added sections: None
- Removed sections: None
- Templates requiring updates: None (Templates are generic)
- Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Course published via Docusaurus + GitHub Pages Constitution

## Core Principles

### I. Spec-First & Modular Design
Course structure, chapters, and web-site layout must be defined and approved before content creation begins. This ensures a coherent learning path and prevents "scope creep" or disorganized modules. The design must be modular to allow independent updates.

### II. Educational Integrity
Course content (books, references, exercises) must be curated via verified sources. All technical claims and educational resources must be cross-referenced with authoritative materials. Agents must leverage available MCP servers to search and suggest the "best" AI-course books & resources, which must then be manually reviewed for suitability.

### III. Transparency and Traceability
All included course materials and references must be clearly documented, including source, edition, and license. Users must be able to trace every piece of knowledge back to its origin.

### IV. Developer-Centric Documentation
Content is structured and styled for readability by developers, educators, and technical learners. Avoid academic jargon where simple technical terms suffice. Focus on actionable learning outcomes and reproducible exercises.

### V. Reproducible Content Pipeline
We enforce reproducibility using Spec-Kit Plus and MCP-server integration. The process of fetching, validating, and integrating course material must be automated and version-controlled.

### VI. Web Ergonomics
The home page and navigation UX must be designed for clarity. Discoverability of course modules, lessons, and resources is paramount. The site must be responsive and clean.

## Project Standards & Constraints

### Standards
- **Resource Verification**: Course resources (books, papers, tutorials) must be hand-verified: metadata (title, author, edition, publication date, license) included.
- **Citation Format**: Inline hyperlinks + metadata (author, year, title, publisher) in a reference list (or footnote) — minimally license-compliant if content is non-public domain.
- **Module Structure**: For each course module: provide learning objectives, required resources, optional resources, estimated time-to-complete, prerequisites (if any).
- **Style**: Modular, navigable, and consistent with Docusaurus/MDX practices; code examples or sample diagrams when relevant.
- **Home Page**: Highlights course overview, module list, quick start guide, and resource repository; must be responsive and clean.

### Constraints
- **Format**: Standard Docusaurus v3 project structure.
- **Deployment**: GitHub Pages via automated CI/CD (GitHub Actions).
- **Structure**: Course content must be organized into modules — minimum 6, maximum 15 modules.
- **Resources**: For each module: at least 1 required resource (book or paper), up to 3 optional resources. Resources must be licensed appropriately (open license, or permissible for educational reference).
- **Dependencies**: All content (text, metadata, links) must be stored in Git repository; no external closed-source dependencies required for core course content.
- **Licensing**: Course content must avoid reliance on proprietary/unlicensed material for core learning (optional resources may reference commercial books if licensing allows referencing).

## Success Criteria & Definition of Done

- **Deployment**: Course homepage deployed successfully — shows course title, short description, module listing, quick start instructions, resource link database.
- **Accessibility**: All modules accessible through site navigation with clearly labeled resources, learning objectives, and resource metadata.
- **Content Quality**: Resource database (fetched via MCP-server then reviewed) contains at least 12 distinct, high-quality AI course resources (books/papers/tutorials) relevant to the course focus.
- **Usability**: Users (educators or learners) can clone the repo and navigate modules locally or via GitHub Pages without missing files or broken links.
- **Validation**: The entire site passes link-checks, build validation, and renders correctly on deployment.
- **Compliance**: All resource references are traceable (metadata + link) and license-compliant.

## Governance

Constitution supersedes all other practices. Amendments require documentation, approval, and a migration plan.

- **Resource Review**: All additions of new course resources must go through a “resource review” step: verify license, metadata, relevance, and record source details in a resource registry.
- **Versioning**: Version control and changelog maintained — major updates to modules or resources versioned (e.g. v1.0, v1.1).
- **Community**: Community contributions allowed via pull requests — any added modules, resources, or homepage changes must comply with core principles and standards.
- **Maintenance**: Periodic review cycles (every 6 months) to refresh resource list, remove obsolete links, and update deprecated references.

**Version**: 1.2.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06