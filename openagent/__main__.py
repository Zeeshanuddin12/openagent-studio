"""Usage: python -m openagent demo"""
import json
import sys
from .engine import Engine, Step, Workflow


def main() -> int:
    if sys.argv[1:] != ["demo"]:
        print("Usage: python -m openagent demo")
        return 2
    engine = Engine()
    engine.register("research", lambda action, data: {
        "action": action, "brief": "Sample brief: " + data["topic"]
    })
    engine.register("publisher", lambda action, data: {
        "action": action, "status": "simulated", "text": data["text"]
    })
    workflow = Workflow("Content approval", [
        Step("research", "summarize", {"topic": "AI automation"}),
        Step("publisher", "publish", {"text": "Hello world"}, True),
    ])
    engine.run(workflow)
    print("Before approval:", workflow.status)
    engine.decide(workflow, True)
    print(json.dumps({"status": workflow.status, "results": workflow.results,
                      "events": workflow.events}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
