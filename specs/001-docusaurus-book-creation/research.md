# Research & Decisions: AI/Spec-Driven Book Creation

**Feature Branch**: `001-docusaurus-book-creation`  
**Date**: 2025-12-06

## Critical Decisions

### 1. Documentation Framework
- **Decision**: Docusaurus v3 (Classic Preset)
- **Rationale**: Matches user constraints for a React-based, versioned, and structured documentation site. The Classic preset includes essential plugins (docs, blog, pages) and theming out-of-the-box.
- **Alternatives Considered**:
    - *MkDocs*: Simpler but less extensible than Docusaurus for React integration.
    - *Astro Docs*: Newer, but Docusaurus is more established for "docs-as-code".
    - *GitBook*: Proprietary/hosted versions less flexible for custom CI/CD pipelines.

### 2. Deployment Strategy
- **Decision**: GitHub Pages via GitHub Actions (deploying to `main` branch context)
- **Rationale**: "Spec-Driven" principles favor automated, reproducible builds. GitHub Pages is free for public repositories and integrates natively with Actions.
- **Constraint Check**: User explicitly requested deployment artifacts be served from `main` (e.g., via root or /docs configuration) rather than the traditional `gh-pages` orphan branch.
- **Alternatives Considered**:
    - *Netlify/Vercel*: Excellent but user specifically requested GitHub Pages.
    - *Manual Upload*: Violated "Workflow Automation" principle.

### 3. Search Functionality
- **Decision**: None (Navigation Only)
- **Rationale**: explicit user clarification to rely on sidebar navigation. Simplifies the "reproducibility" aspect for the book's readers as it avoids setting up external search indices like Algolia.
- **Alternatives Considered**:
    - *Local Search Plugin*: Good option but user chose "No Search".
    - *Algolia*: Requires external credentials, complicating the "from scratch" user journey.

### 4. Diagramming Tooling
- **Decision**: Standard PNG/SVG images in `/static/img` + Mermaid for code-based diagrams
- **Rationale**: SVG provides scalability for architecture diagrams; Mermaid allows version-controllable diagrams directly in Markdown.
- **Alternatives Considered**:
    - *Excalidraw*: Good for sketching, can export to SVG.

### 5. Validation & Quality
- **Decision**: Automated CI Pipeline (Build + Link Check)
- **Rationale**: Enforces "Technical Accuracy". A broken link or failed build blocks deployment.
- **Tooling**: `docusaurus-plugin-broken-links` (native) or external `markdown-link-check`.

## Technical Architecture

### Project Layout
```text
my-docusaurus-book/
├── docs/                  # Book Chapters (Markdown/MDX)
│   ├── 01-intro.md
│   ├── ...
│   └── 12-conclusion.md
├── src/
│   ├── components/        # Custom React components
│   └── css/               # Custom styling
├── static/
│   └── img/               # Diagrams and screenshots
├── docusaurus.config.js   # Main configuration
├── sidebars.js            # Sidebar navigation structure
├── package.json           # Dependencies
└── .github/
    └── workflows/
        └── deploy.yml     # CI/CD Pipeline
```

### Deployment Flow
1.  **Push** to `main` branch.
2.  **GitHub Action** triggers:
    *   Checkout code.
    *   Install dependencies (`npm ci`).
    *   Build project (`npm run build`).
    *   Validate links.
3.  **Deploy**: Upload build artifacts to GitHub Pages environment.

## Open Questions & Riskiest Assumptions
- *None remaining after clarification session.*
