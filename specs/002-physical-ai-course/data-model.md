# Data Model: Physical AI & Humanoid Robotics Course

**Feature Branch**: `002-physical-ai-course`

## Conceptual Entities

### 1. Course Module
Top-level structural unit.

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | e.g., `module-01` |
| `title` | String | Display title (e.g., "Foundations") |
| `description` | String | Short summary for homepage card |
| `simulator` | Enum | `None` \| `Isaac` \| `Gazebo` \| `Webots` |
| `chapters` | Array | List of Chapter IDs |

### 2. Course Chapter (`docs/**/*.mdx`)
Individual lesson content.

| Frontmatter Field | Type | Description |
|-------------------|------|-------------|
| `title` | String | Lesson title |
| `learning_objectives` | List<String> | What the learner will achieve |
| `code_snippets` | Integer | Count (Must be >= 3) |
| `difficulty` | Enum | `Beginner` \| `Intermediate` \| `Advanced` |

### 3. Curated Resource (`data/resources.json`)
External learning material validated via MCP.

| Field | Type | Description |
|-------|------|-------------|
| `title` | String | Title of book/paper/course |
| `author` | String | Author or Organization |
| `type` | Enum | `Book` \| `Paper` \| `Official Doc` \| `Video` |
| `url` | String | Validated external link |
| `category` | Enum | `Physical AI` \| `ROS 2` \| `Simulators` |
| `year` | String | Publication year (preference for >2022) |

## Content Hierarchy (Sidebar)

Defined in `sidebars.js`:

*   **Module 1: Foundations of Physical AI & ROS 2**
    *   Intro to Embodied Intelligence
    *   Setting up ROS 2 Jazzy
    *   Nodes, Topics, and Python Clients
    *   Control Theory for Humanoids (Code-First)
*   **Module 2: High-Fidelity Simulation (Isaac Sim)**
    *   Isaac Sim Architecture & USD
    *   Importing URDFs to Isaac
    *   Synthetic Data Generation
    *   Reinforcement Learning with Isaac Gym
*   **Module 3: Open-Source Simulation (Gazebo)**
    *   Gazebo (Ignition) Fundamentals
    *   World Building & Physics Plugins
    *   Sensor Simulation (Lidar/Camera)
    *   Nav2 Integration in Gazebo
*   **Module 4: Rapid Prototyping (Webots)**
    *   Webots Supervisor API
    *   Cross-Compilation for Real Hardware
    *   Soft Robotics Simulation
    *   Sim-to-Real Transfer Strategies
