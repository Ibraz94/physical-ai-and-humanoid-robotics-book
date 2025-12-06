# Quickstart: Physical AI Course Development

**Feature Branch**: `002-physical-ai-course`

## Prerequisites
- Node.js v18+
- Git
- **Optional**: Installed ROS 2 Jazzy (for verifying code snippets locally)

## Theme Development
The futuristic theme is controlled via `src/css/custom.css`.

1.  **Start Dev Server**:
    ```bash
    npm start
    ```
2.  **Verify Theme**:
    *   Check that `dark` mode is default.
    *   Verify primary color is "Neon Cyan" (or defined futuristic hue).
    *   Ensure cards have "glassmorphism" effects.

## Content Creation
To add a new chapter:

1.  Create file: `docs/module-X/0X-topic.mdx`
2.  Add Frontmatter:
    ```yaml
    ---
    title: My Topic
    sidebar_label: My Topic
    description: Learn about X
    ---
    ```
3.  **Validation**: Ensure ≥3 code blocks are included.
    ```python
    # Example Snippet 1
    import rclpy
    ...
    ```

## Resource Curation
To update the Essential Resources list:

1.  Edit `data/resources.json`.
2.  Add entry following the schema in `data-model.md`.
3.  Verify homepage renders the new card.
