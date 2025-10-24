import unittest
from datetime import datetime
from assistant.core import ContextManager, generate_ai_response

class TestContextManager(unittest.TestCase):

    def setUp(self):
        self.ctx = ContextManager(max_tokens=50)

    def test_add_prompt_and_auto_ai_response(self):
        self.ctx.add_prompt("Discuss project timeline")
        self.assertEqual(len(self.ctx.memory), 1)
        self.assertIn("Discuss project timeline", self.ctx.memory[0]['prompt'])
        self.assertTrue(isinstance(self.ctx.memory[0]['response'], str))

    def test_undo_empty_stack(self):
        # Undo with empty stack should not fail
        self.ctx.undo()
        self.assertEqual(len(self.ctx.stack.items), 0)

    def test_undo_response(self):
        self.ctx.add_prompt("Set next steps")
        self.assertEqual(len(self.ctx.memory), 1)
        self.ctx.undo()
        # The last prompt should now be finalized (per current terminal logic)
        self.assertTrue(self.ctx.memory[-1]['finalized'])

    def test_finalize_empty(self):
        # Finalize with no prompts should not fail
        self.ctx.finalize()

    def test_finalize_prompt(self):
        self.ctx.add_prompt("Plan sprint")
        self.ctx.finalize()
        self.assertTrue(self.ctx.memory[-1]['finalized'])

    def test_history_output(self):
        self.ctx.add_prompt("Update on blockers")
        # Capture printed history
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.ctx.history()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Update on blockers", output)

    def test_context_limit(self):
        # Add multiple prompts to exceed token limit
        self.ctx.add_prompt("This is prompt one with several words")
        self.ctx.add_prompt("This is prompt two with several more words to overflow")
        # Total memory should be <= max_tokens logic
        total_tokens = sum(len(p['prompt'].split()) + len(p['response'].split()) for p in self.ctx.memory)
        self.assertLessEqual(total_tokens, self.ctx.max_tokens)


if __name__ == "__main__":
    unittest.main()
