"""Usage: python -m openagent demo | run FILE [--approve]"""
import argparse
from pathlib import Path
from .runner import execute
import json
import sys
from .engine import Engine, Step, Workflow


def main() -> int:
    if sys.argv[1:2] == ["run"]:
        parser = argparse.ArgumentParser(description="Run a JSON workflow with built-in local text operations")
        parser.add_argument("command", choices=["run"])
        parser.add_argument("file", type=Path)
        parser.add_argument("--approve", action="store_true", help="Explicitly approve all gates in this invocation")
        args = parser.parse_args()
        try:
            result = execute(json.loads(args.file.read_text()), approve=args.approve)
        except (OSError, ValueError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "completed" else 3
    if sys.argv[1:] != ["demo"]:
        print("Usage: python -m openagent demo | run FILE [--approve]")
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
