---
id: 002
title: Update Constitution with MCP Requirement
stage: constitution
date: 2025-12-06
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["governance", "mcp", "documentation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

/sp.constitution add one thing in constitution that use mcp server to follow official documentations

## Response snapshot

Updated .specify/memory/constitution.md to v1.1.0. Modified "II. Technical Accuracy" principle to explicitly require agents to leverage available MCP servers for verifying technical explanations against official documentation.

## Outcome

- ✅ Impact: Constitution updated to mandate MCP usage for verification.
- 🧪 Tests: None
- 📁 Files: 1 file updated
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: Incorporated user feedback to mandate specific tooling (MCP) for the accuracy principle.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None
