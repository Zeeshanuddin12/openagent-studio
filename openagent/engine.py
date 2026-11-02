"""Dependency-free, local workflow engine with explicit approval gates."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable


class WorkflowError(Exception):
    pass


@dataclass(frozen=True)
class Step:
    agent: str
    action: str
    payload: dict[str, Any] = field(default_factory=dict)
    requires_approval: bool = False


@dataclass
class Workflow:
    name: str
    steps: list[Step]
    cursor: int = 0
    status: str = "pending"
    results: list[Any] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)

    def log(self, event: str, **details: Any) -> None:
        self.events.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event, **details,
        })


class Engine:
    def __init__(self) -> None:
        self.agents: dict[str, Callable[[str, dict[str, Any]], Any]] = {}

    def register(self, name: str, handler: Callable[[str, dict[str, Any]], Any]) -> None:
        if not name or name in self.agents:
            raise WorkflowError("Agent name must be unique and nonempty")
        self.agents[name] = handler

    def run(self, workflow: Workflow) -> Workflow:
        if workflow.status in {"completed", "denied", "failed"}:
            raise WorkflowError("Workflow is terminal")
        if workflow.status == "awaiting_approval":
            raise WorkflowError("Approval required")
        approved_step = workflow.cursor if workflow.status == "approved" else None
        workflow.status = "running"
        while workflow.cursor < len(workflow.steps):
            step = workflow.steps[workflow.cursor]
            if step.agent not in self.agents:
                workflow.status = "failed"
                workflow.log("failed", reason="unknown_agent", agent=step.agent)
                raise WorkflowError(f"Unknown agent: {step.agent}")
            if step.requires_approval and workflow.cursor != approved_step:
                workflow.status = "awaiting_approval"
                workflow.log("approval_requested", step=workflow.cursor)
                return workflow
            try:
                result = self.agents[step.agent](step.action, dict(step.payload))
            except Exception as exc:
                workflow.status = "failed"
                workflow.log("failed", step=workflow.cursor, reason=type(exc).__name__)
                raise WorkflowError("Agent execution failed") from exc
            workflow.results.append(result)
            workflow.log("step_completed", step=workflow.cursor, agent=step.agent)
            workflow.cursor += 1
            approved_step = None
        workflow.status = "completed"
        workflow.log("completed", total_steps=len(workflow.steps))
        return workflow

    def decide(self, workflow: Workflow, approve: bool) -> Workflow:
        if workflow.status != "awaiting_approval":
            raise WorkflowError("No approval is pending")
        if not approve:
            workflow.status = "denied"
            workflow.log("approval_denied", step=workflow.cursor)
            return workflow
        workflow.status = "approved"
        workflow.log("approval_granted", step=workflow.cursor)
        return self.run(workflow)
