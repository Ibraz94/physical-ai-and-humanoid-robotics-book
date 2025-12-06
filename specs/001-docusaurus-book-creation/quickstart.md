# Quickstart: Docusaurus Book Project

**Feature Branch**: `001-docusaurus-book-creation`

## Prerequisites
- Node.js v18+ (`node -v`)
- Git (`git --version`)
- A GitHub Account

## Setup Instructions

1.  **Clone the Repository**
    ```bash
    git clone <repo-url>
    cd <repo-name>
    ```

2.  **Install Dependencies**
    ```bash
    npm install
    ```

3.  **Run Local Development Server**
    ```bash
    npm start
    ```
    *   Opens http://localhost:3000

## Verification Steps

1.  **Build Check**
    Run the production build command to ensure no errors:
    ```bash
    npm run build
    ```
    *   *Expectation*: Output directory `build/` is created without error.

2.  **Link Validation**
    (Assuming plugin is configured)
    ```bash
    npm run docusaurus check-broken-links
    # OR
    npm run build # (config: onBrokenLinks: 'throw')
    ```

## Deployment Simulation

1.  Commit changes to `main`.
2.  Push to GitHub.
3.  Navigate to "Actions" tab in GitHub repository.
4.  Verify "Deploy to GitHub Pages" workflow succeeds.
