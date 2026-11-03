"""Run declarative JSON workflows using a closed set of local text operations."""
import json
from .engine import Engine, Step, Workflow

def load(data):
    if not isinstance(data, dict) or set(data) != {"name", "steps"}:
        raise ValueError("Workflow requires name and steps only")
    if not isinstance(data["name"], str) or not data["name"].strip():
        raise ValueError("Workflow name must be nonempty")
    if not isinstance(data["steps"], list) or not 1 <= len(data["steps"]) <= 100:
        raise ValueError("Provide 1 to 100 steps")
    steps = []
    for item in data["steps"]:
        if not isinstance(item, dict) or set(item) - {"action", "text", "requires_approval"} or not {"action", "text"} <= set(item):
            raise ValueError("Each step needs action and text, with optional requires_approval")
        if item["action"] not in ("uppercase", "word_count", "trim") or not isinstance(item["text"], str) or len(item["text"]) > 100000:
            raise ValueError("Invalid local text operation or text")
        gate = item.get("requires_approval", False)
        if type(gate) is not bool:
            raise ValueError("requires_approval must be boolean")
        steps.append(Step("text", item["action"], {"text":item["text"]}, gate))
    return Workflow(data["name"], steps)

def execute(data, approve=False):
    workflow = load(data)
    engine = Engine()
    operations = {"uppercase":str.upper, "trim":str.strip, "word_count":lambda text: len(text.split())}
    engine.register("text", lambda action, payload: operations[action](payload["text"]))
    engine.run(workflow)
    while workflow.status == "awaiting_approval" and approve:
        engine.decide(workflow, True)
    return {"name":workflow.name, "status":workflow.status, "cursor":workflow.cursor,
            "results":workflow.results, "events":workflow.events}
