import unittest
from openagent import Engine, Step, Workflow, WorkflowError


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.engine = Engine()
        self.engine.register("echo", self.echo)

    def echo(self, action, payload):
        self.calls.append((action, payload))
        return payload

    def test_simple(self):
        wf = Workflow("simple", [Step("echo", "send", {"x": 1})])
        self.engine.run(wf)
        self.assertEqual(wf.status, "completed")
        self.assertEqual(wf.results, [{"x": 1}])

    def test_gate(self):
        wf = Workflow("gate", [Step("echo", "send", {}, True)])
        self.engine.run(wf)
        self.assertEqual(wf.status, "awaiting_approval")
        self.assertFalse(self.calls)
        self.engine.decide(wf, True)
        self.assertEqual(wf.status, "completed")
        self.assertEqual(len(self.calls), 1)

    def test_denied(self):
        wf = Workflow("denied", [Step("echo", "send", {}, True)])
        self.engine.run(wf)
        self.engine.decide(wf, False)
        self.assertEqual(wf.status, "denied")
        self.assertFalse(self.calls)

    def test_unknown_agent(self):
        wf = Workflow("bad", [Step("missing", "send")])
        with self.assertRaises(WorkflowError):
            self.engine.run(wf)
        self.assertEqual(wf.status, "failed")

    def test_multiple_gates(self):
        wf = Workflow("two", [
            Step("echo", "a", {}, True),
            Step("echo", "b", {}, True),
        ])
        self.engine.run(wf)
        self.engine.decide(wf, True)
        self.assertEqual(wf.status, "awaiting_approval")
        self.assertEqual(len(self.calls), 1)
        self.engine.decide(wf, True)
        self.assertEqual(wf.status, "completed")
        self.assertEqual(len(self.calls), 2)


if __name__ == "__main__":
    unittest.main()
