from fastapi import FastAPI
from app.agent import DemoAgent
from app.runtime import GuardedRuntime, UnsafeRuntime

app = FastAPI(title="OpenShell/NemoClaw Demo")


@app.get("/")
def root() -> dict:
    return {"status": "ok", "message": "OpenShell/NemoClaw comparison demo"}


@app.post("/demo/guarded")
def guarded_demo() -> dict:
    agent = DemoAgent(GuardedRuntime())
    result = agent.run_demo(guarded=True)
    return result.__dict__


@app.post("/demo/unguarded")
def unguarded_demo() -> dict:
    agent = DemoAgent(UnsafeRuntime())
    result = agent.run_demo(guarded=False)
    return result.__dict__
