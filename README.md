# OpenShell + NemoClaw Feature Demonstration Project

This project is a **simple, production-style demo** designed to show **exactly why OpenShell and NemoClaw matter**:

- **Without governance**: the agent can complete the task, but it can also read secrets and exfiltrate data.
- **With governance**: the agent still completes the useful task, but external policy blocks unauthorized file access and network egress.

## What this project demonstrates

1. **Sandbox / policy behavior** using a local guarded runtime that mirrors OpenShell concepts.
2. **Comparison mode**: run the same agent in unguarded and guarded modes.
3. **Evaluation matrix**: score usefulness, secret leakage prevention, unauthorized network blocking, and audit coverage.
4. **Groq API integration** so you can use a free model path for learning.
5. **Cloud Run deployment** for a clean demo endpoint.

## Project idea

**Secure Log Analysis Agent**

The agent reads application logs, summarizes incidents, writes a report, then attempts two unsafe actions:
- read `data/secrets/credentials.txt`
- call `https://evil.example.com/upload`

In **unguarded mode**, both unsafe actions succeed.
In **guarded mode**, policy blocks them and writes an audit trail.

---

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Add environment variables

```bash
cp .env.example .env
```

Set your Groq key in `.env`:

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

If you do not set a Groq key, the demo still works with a fallback summary.

### 3. Run the two comparison demos

```bash
python scripts/demo_without_controls.py
python scripts/demo_with_controls.py
```

### 4. Generate the evaluation matrix

```bash
python scripts/run_evals.py
```

Outputs:
- `output/report.md`
- `output/audit.json`
- `output/evaluation_matrix.csv`
- `output/evaluation_matrix.md`

### 5. Run the API

```bash
uvicorn app.main:app --reload --port 8080
```

Then open:
- `http://127.0.0.1:8080/docs`

Routes:
- `POST /demo/unguarded`
- `POST /demo/guarded`

---

## Exact demo flow you should present

### Demo A — Without OpenShell-style external governance

Run:

```bash
python scripts/demo_without_controls.py
```

Show that:
- the agent reads logs
- writes the report
- **reads the secret file**
- **calls an unauthorized external URL**

Message: the agent is useful, but unsafe.

### Demo B — With OpenShell-style governance

Run:

```bash
python scripts/demo_with_controls.py
```

Show that:
- the agent still reads logs
- still writes the report
- **cannot read the secret file**
- **cannot call the unauthorized URL**
- every action is written to `output/audit.json`

Message: same useful task, much better trust and control.

### Demo C — Evaluation matrix

Run:

```bash
python scripts/run_evals.py
```

Show the matrix side by side.

---

## How this maps to real OpenShell and NemoClaw

This repo uses a **local teaching runtime** so you can learn the security model even if you are not yet running the full OpenShell / NemoClaw stack.

Map it like this:

- `GuardedRuntime` → OpenShell sandbox + policy engine
- `policy.yaml` → declarative runtime policy
- `audit.json` → allow / deny audit trail
- Groq model call → external inference provider
- Later swap Groq for Nemotron or NIM if you want a more NVIDIA-native stack

Use the docs in `docs/` for the step-by-step real-product mapping.

---

## Deploy to Cloud Run

```bash
bash cloudrun/deploy.sh YOUR_PROJECT_ID us-central1 openshell-nemoclaw-demo
```

---

## Best order to learn

1. Understand the architecture in `docs/01_architecture_and_mapping.md`
2. Run the local comparison demos
3. Review `output/audit.json`
4. Generate and study the evaluation matrix
5. Read `docs/03_real_openshell_nemoclaw_steps.md`
6. Deploy the API

---

## What to say in an interview or demo

> I built a controlled agent demo that shows the difference between agent capability and runtime trust. In the unguarded setup the agent completes the task but can also access secrets and exfiltrate data. In the guarded setup, the same task still succeeds, but external policy blocks unauthorized file and network actions and records a full audit trail. That is the core value proposition of OpenShell and NemoClaw.
