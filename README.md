# Spec-Driven Development with Docusaurus

A technical book about building books, demonstrating Spec-Driven Development (SDD) principles.

## Overview

This repository contains the source code and content for the "Spec-Driven Development with Docusaurus" book. The project is structured using Docusaurus v3 and follows a rigorous "Spec-First" workflow.

## Quickstart

### Prerequisites
- Node.js v18+
- Git

### Installation

```bash
npm install
```

### Local Development

```bash
npm start
```
Opens http://localhost:3000

### Build & Validation

```bash
npm run build
```
Checks for broken links and generates static artifacts in `build/`.

## Project Structure

- `docs/`: Book chapters (Markdown/MDX)
- `src/`: Custom React components and styles
- `static/`: Static assets (images, diagrams)
- `.github/workflows/`: CI/CD pipeline definitions
- `specs/`: Project specifications and plans (SDD artifacts)

## Deployment

This project is automatically deployed to GitHub Pages via GitHub Actions on every push to the `main` branch.

## License

MIT