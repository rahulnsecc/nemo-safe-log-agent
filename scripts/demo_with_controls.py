import sys, os; sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.agent import DemoAgent
from app.runtime import GuardedRuntime

result = DemoAgent(GuardedRuntime()).run_demo(guarded=True)
print(result)
print("Audit saved to output/audit.json")
