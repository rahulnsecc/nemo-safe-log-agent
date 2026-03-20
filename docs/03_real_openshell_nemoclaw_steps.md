# Real OpenShell / NemoClaw steps

This section gives you the practical path from this teaching demo to the real NVIDIA stack.

## Phase 1 — Learn with the local repo first

Do not start with full OpenShell + NemoClaw on day one.
First understand:
- why external runtime policy matters
- how allow / deny rules affect agent behavior
- what your evaluation matrix should measure

## Phase 2 — Install OpenShell CLI

Official quickstart shows two install paths:

```bash
curl -LsSf https://raw.githubusercontent.com/NVIDIA/OpenShell/main/install.sh | sh
# or
uv tool install -U openshell
```

Then:

```bash
openshell --help
```

## Phase 3 — Create your first sandbox

Follow the OpenShell quickstart and tutorials to create a first sandbox and inspect policy behavior.

## Phase 4 — Install NemoClaw on a clean OpenClaw setup

NemoClaw quickstart currently notes that it requires a **fresh installation of OpenClaw**. Use the official docs rather than guessing commands, because this is still early and moving quickly.

## Phase 5 — Re-run the same comparison in the real stack

Once you are comfortable, re-create this same demo idea in the real product flow:

- allowed workspace logs
- denied secrets path
- allowed inference endpoint
- denied random egress
- audit review

## Phase 6 — Upgrade the model path

Start with Groq for simplicity.
Then optionally move to:
- Nemotron via hosted provider
- NVIDIA NIM for optimized serving
- NeMo only if you later want model customization, training, or structured enterprise deployment work

## Phase 7 — Keep the same evaluation matrix

Do not lose the educational value when moving to the real stack.
Your evaluation matrix should still answer:
- does the task succeed?
- does the agent leak secrets?
- does the agent reach unauthorized destinations?
- do you get usable audit evidence?
