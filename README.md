# OpenAgent Studio

Open-source, local-first AI agent workflow orchestration for small teams.

> **Status: early MVP.** This project currently provides a deterministic workflow engine, approval gates, audit events, a CLI demo and automated tests. It does **not** yet include live LLM integrations, a web dashboard, or production authentication.

## Why

Run repeatable multi-step workflows with named agents, explicit approvals and an inspectable event trail. Start locally without API keys or paid infrastructure.

## Quick start

Requires Python 3.10+; no third-party dependencies.

```bash
python -m openagent demo
python -m unittest discover -s tests -v
```

The demo prints the gate and then automatically simulates approval; it is not interactive. For an explicit command-line decision, use the JSON runner below.

## Concepts

- **Workflow**: ordered steps with an agent, action and input.
- **Agent**: a named executor registered for a particular task.
- **Approval gate**: a human decision required before a marked step runs.
- **Audit log**: timestamped workflow transitions and results.
- **Fail closed**: unregistered agents and denied approvals never execute.

## Safety

No credentials are required for the demo. Do not commit secrets, customer records, or private business data. The current engine is an educational prototype, not a secure multi-tenant execution environment. Review all third-party integrations before enabling external actions.

## Roadmap

1. Workflow JSON schema and persistence
2. Web UI for tasks, approvals and audit logs
3. Pluggable model providers with explicit cost limits
4. Sandboxed connectors and scoped credentials
5. Durable queues, retries, roles and authentication

See [CONTRIBUTING.md](CONTRIBUTING.md) to help.

## License

MIT — see [LICENSE](LICENSE).

## Run your own JSON workflow

```sh
python -m openagent run examples/workflow.json
# Exits 3 at the approval gate, with only ungated results.
python -m openagent run examples/workflow.json --approve
# Exits 0 after explicitly approving all gates in this invocation.
```

The JSON runner performs real local `trim`, `uppercase`, and `word_count` operations. Each step has `action`, `text`, and optional boolean `requires_approval`. It rejects unknown fields/actions and never executes arbitrary code. Steps are independent; results are ordered rather than automatically passed to later steps. Output is JSON for inspection or redirection to a local file. Exit 2 indicates invalid input.

Re-running starts a new in-memory workflow; there is no persistence, retry, identity verification or remote publishing. `--approve` approves all gates for that invocation. The Python API is trusted local code: callers can mutate workflow state, so approval gates are not a security boundary against hostile callers. Use only synthetic/local non-sensitive inputs.
