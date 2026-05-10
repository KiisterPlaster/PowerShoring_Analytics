# Antigravity Kit Architecture

Version: 2026.03.21.2
Status: Expanded swarm-ready agent platform.

## Overview
- Total Agents: 56
- Total Skills: 1408
- Total Workflows: 13

## Core Directories
- .agent/agents/: specialist and swarm agents
- .agent/skills/: progressive-disclosure capability modules
- .agent/workflows/: task workflows and slash-command playbooks
- .agent/registry/: generated inventory (agent-registry.yaml, skill-registry.yaml)

## Design Principles (from agente1MI + agente50 + modelos)
- Dynamic swarm runtime over static mass files.
- DAG-oriented orchestration with parallel execution paths.
- Agent lifecycle management: creation, specialization, evaluation, and retirement.
- Evolution and economy layers for adaptive agent allocation.
- Shared memory and observability as first-class platform concerns.

## Practical Scale Strategy
- Keep agent templates as reusable files.
- Instantiate runtime agents on demand via scheduler/factory.
- Use registries to map capabilities and route tasks.
