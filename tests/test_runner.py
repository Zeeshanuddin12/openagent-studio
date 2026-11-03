import unittest
from openagent.runner import execute
from openagent import Engine, Step, Workflow, WorkflowError

class RunnerTests(unittest.TestCase):
    def test_gate_and_real_operations(self):
        data={"name":"test", "steps":[{"action":"trim","text":"  hi  "},{"action":"word_count","text":"hello world","requires_approval":True}]}
        blocked=execute(data)
        self.assertEqual(blocked["results"],["hi"])
        self.assertEqual(blocked["status"],"awaiting_approval")
        approved=execute(data,True)
        self.assertEqual(approved["results"],["hi",2])
        self.assertEqual(approved["status"],"completed")
    def test_invalid_schema_and_no_arbitrary_execution(self):
        for step in [{"action":"shell","text":"echo hi"},{"action":"trim","text":"x","requires_approval":"false"},{"action":"trim","text":1},{"action":"trim","text":"x","unknown":True}]:
            with self.subTest(step=step), self.assertRaises(ValueError):execute({"name":"test","steps":[step]})
    def test_failed_handler_cannot_resume(self):
        engine=Engine()
        def fail(action,payload):raise RuntimeError("private context")
        engine.register("fail",fail)
        wf=Workflow("failure",[Step("fail","run")])
        with self.assertRaises(WorkflowError):engine.run(wf)
        self.assertEqual(wf.status,"failed")
        self.assertNotIn("private context",str(wf.events))
        with self.assertRaises(WorkflowError):engine.run(wf)
    def test_completed_cannot_replay(self):
        engine=Engine();calls=[]
        engine.register("echo",lambda a,p:calls.append(a))
        wf=Workflow("once",[Step("echo","run")]);engine.run(wf)
        with self.assertRaises(WorkflowError):engine.run(wf)
        self.assertEqual(calls,["run"])
