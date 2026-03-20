# Architecture and mapping to OpenShell / NemoClaw

## The core idea

OpenShell is the governance layer between the agent and infrastructure. NemoClaw packages OpenClaw with OpenShell and model configuration so always-on assistants can run more safely.

## This project's architecture

```text
User / Evaluator
    ↓
Demo Agent
    ↓
Runtime Layer
  ├─ UnsafeRuntime (no controls)
  └─ GuardedRuntime (policy + audit)
    ↓
Filesystem / Network / Model API
```

## Mapping to the NVIDIA stack

### In this repo
- `DemoAgent`: your claw / assistant logic
- `GuardedRuntime`: stand-in for OpenShell runtime enforcement
- `config/policy.yaml`: stand-in for sandbox policy
- `output/audit.json`: stand-in for allow / deny audit trail
- Groq inference: practical free inference path

### In the real stack
- **OpenShell**: isolated runtime, policy engine, privacy routing
- **NemoClaw**: OpenClaw plugin / reference stack that installs and configures OpenShell plus model plumbing
- **Nemotron / NIM / NeMo**:
  - Nemotron = model family
  - NIM = optimized inference serving path
  - NeMo = framework to build / customize / deploy models

## Why the comparison matters

A lot of teams prove only that the agent can do a task.
This project proves a more useful claim:

> the agent can do the task **and** the runtime can still prevent unsafe behavior.
