# Research & Decisions: Physical AI & Humanoid Robotics Course

**Feature Branch**: `002-physical-ai-course`  
**Date**: 2025-12-06

## Critical Decisions

### 1. Course Structure (4 Modules)
- **Decision**: 
    - **Module 1**: Foundations of Physical AI & ROS 2 (Jazzy)
    - **Module 2**: High-Fidelity Simulation with Isaac Sim
    - **Module 3**: Open-Source Simulation with Gazebo (Ignition)
    - **Module 4**: Rapid Prototyping with Webots & Sim-to-Real Transfer
- **Rationale**: Dedicating a full module to each simulator (Modules 2, 3, 4) minimizes context switching and allows deep dives into the specific strengths of each tool (Isaac for visual AI, Gazebo for ROS integration, Webots for ease of use). Module 1 provides the necessary shared ROS 2 and theoretical foundation.
- **Alternatives Considered**:
    - *Parallel Chapters*: integrating all sims in every chapter would confuse learners with constant syntax switching.
    - *Topic-Based*: teaching "Navigation" across 3 sims simultaneously is too fragmented.

### 2. Simulation Tools
- **Decision**: Cover Isaac Sim, Gazebo, AND Webots.
- **Rationale**: Explicit user requirement. Each has a unique place in the modern robotics stack (Industry/NVIDIA, Research/Open Source, Education/Prototyping).
- **Constraint**: All examples must target **ROS 2 Jazzy Jalisco**.

### 3. Code-First Content Strategy
- **Decision**: Replace diagrams with ≥3 runnable code snippets per chapter.
- **Primary Language**: Python (accessible, standard for AI/ROS 2 high-level logic).
- **Rationale**: "Physical AI" is best learned by doing. Visuals are replaced by reproducible code that generates the visual/behavioral result in the simulator.

### 4. Theming & UX
- **Decision**: Custom "Futuristic" theme using Docusaurus Infima overrides.
- **Attributes**: Dark mode default, neon accents (cyan/magenta), clean sans-serif typography.
- **Rationale**: Matches the "Physical AI / Humanoid" aesthetic. Infima overrides ensure compatibility with Docusaurus upgrades unlike a full fork.

### 5. Resource Curation (MCP)
- **Decision**: Automated fetching + Human verification.
- **Source**: Official docs (NVIDIA, ROS.org, Cyberbotics) and seminal papers/books.
- **Integration**: "Essential AI Resources" list on Homepage and "Further Reading" at end of each module.

## Open Questions
- *None. Clarification session resolved distribution (Jazzy), language (Python), and structure (Module-based).*

## Technical Architecture

### Project Layout (Additions to Docusaurus)
```text
docs/
├── module-01-foundations/
├── module-02-isaac-sim/
├── module-03-gazebo/
└── module-04-webots/
src/
├── css/
│   └── custom.css       # Futuristic theme overrides
├── components/
│   └── Homepage/        # Hero, Module Cards, Resource List
static/
│   └── img/             # Hero assets only (no diagram files)
data/
│   └── resources.json   # MCP-curated resource list
```
