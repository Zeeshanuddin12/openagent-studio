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

The demo pauses before a sensitive action and requires an explicit approval before resuming.

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
