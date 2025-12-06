# Data Model: AI/Spec-Driven Book Creation

**Feature Branch**: `001-docusaurus-book-creation`

## Conceptual Entities

### 1. Book Configuration (`docusaurus.config.js`)
The central source of truth for site metadata.

| Field | Type | Description |
|-------|------|-------------|
| `title` | String | Book Title |
| `url` | String | Production URL (GitHub Pages) |
| `baseUrl` | String | Path prefix (usually `/repo-name/`) |
| `onBrokenLinks` | String | 'throw' (Enforces validation) |
| `presets` | Array | `['classic', ...]` configuration |
| `themeConfig` | Object | Navbar, Footer, Color Mode |

### 2. Chapter (`docs/*.md`)
Represents a single unit of content.

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | String | Unique identifier (filename slug) |
| `title` | String | Chapter Title (Frontmatter) |
| `sidebar_position` | Integer | Ordering in the book |
| `description` | String | SEO description |
| `body` | Markdown | The technical content |

### 3. Asset (`static/img/*`)
Binary or vector resources referenced by Chapters.

| Attribute | Type | Description |
|-----------|------|-------------|
| `path` | String | Relative path (e.g., `/img/arch.png`) |
| `alt` | String | Accessibility text |

## Content Hierarchy (Sidebar)

The book follows a linear progression defined in `sidebars.js`:

1.  **Part I: Foundations**
    *   Chapter 1: Introduction & Philosophy
    *   Chapter 2: Tooling Setup (Prerequisites)
2.  **Part II: Building the Engine**
    *   Chapter 3: Initializing Docusaurus
    *   Chapter 4: Configuring the Spec-Kit
    *   Chapter 5: The CI/CD Pipeline
3.  **Part III: Authoring & Automation**
    *   Chapter 6: Writing Spec-Driven Content
    *   Chapter 7: Diagramming as Code
    *   Chapter 8: Automated Validation
4.  **Part IV: Publishing & Maintenance**
    *   Chapter 9: Deployment to GitHub Pages
    *   Chapter 10: Versioning & Maintenance
