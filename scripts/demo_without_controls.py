import sys, os; sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.agent import DemoAgent
from app.runtime import UnsafeRuntime

result = DemoAgent(UnsafeRuntime()).run_demo(guarded=False)
print(result)
