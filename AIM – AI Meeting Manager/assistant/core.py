from datetime import datetime
from random import choice

# --- Custom Data Structures (No Built-ins) ---
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items += [item]  # No append()

    def pop(self):
        if len(self.items) == 0:
            return None
        top = self.items[-1]
        self.items = self.items[:-1]
        return top

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items += [item]

    def dequeue(self):
        if len(self.items) == 0:
            return None
        first = self.items[0]
        self.items = self.items[1:]
        return first


# --- AI Response ---
def generate_ai_response(prompt):
    """Generate professional, human-like AI meeting responses."""
    prompt = prompt.lower()
    if "deadline" in prompt or "timeline" in prompt:
        return "Let's align on the deadlines and track milestones efficiently."
    elif "update" in prompt or "progress" in prompt:
        return "I've noted your update. We'll reflect that in the meeting summary."
    elif "blocker" in prompt or "issue" in prompt:
        return "Got it — I’ll mark that as a potential blocker for the next sprint."
    elif "task" in prompt or "next step" in prompt:
        return "Assign next tasks accordingly to ensure accountability."
    elif "review" in prompt or "action item" in prompt:
        return "Let's review the action items to ensure follow-through."
    else:
        responses = [
            "Make sure everyone is aligned.",
            "Schedule a follow-up meeting for deeper discussion.",
            "Summarize the takeaways at the end of the session."
        ]
        return choice(responses)


# --- Context Manager ---
class ContextManager:
    def __init__(self, max_tokens=50):
        self.max_tokens = max_tokens
        self.memory = []
        self.stack = Stack()
        self.total_tokens = 0

    def add_prompt(self, text):
        """Add new user prompt."""
        if not text.strip():
            print("⚠️ Please enter a valid prompt, not gibberish.")
            return
        ai_resp = generate_ai_response(text)
        tokens = len(text.split()) + len(ai_resp.split())

        # Enforce token limit
        while self.total_tokens + tokens > self.max_tokens and len(self.memory) > 0:
            removed = self.memory[0]
            removed_tokens = len(removed['prompt'].split()) + len(removed['response'].split())
            self.total_tokens -= removed_tokens
            self.memory = self.memory[1:]
            print("⚠️ Context full — oldest pair removed.")

        self.memory += [{"prompt": text, "response": ai_resp, "finalized": False}]
        self.stack.push(ai_resp)
        self.total_tokens += tokens
        print(f"✅ Added: {text}")
        print(f"🤖 AI: {ai_resp}")

    def undo(self):
        """Undo last AI response."""
        if len(self.stack.items) == 0:
            print("⚠️ No responses to undo!")
            return
        last = self.stack.pop()
        self.memory[-1]['finalized'] = True
        print(f"↩️ Undone: {last}")

    def finalize(self):
        """Finalize last active prompt."""
        if len(self.memory) == 0:
            print("⚠️ Nothing to finalize.")
            return
        latest = self.memory[-1]
        latest['finalized'] = True
        print(f"✅ Finalized: {latest['prompt']} → {latest['response']}")

    def history(self):
        """Display all prompt-response pairs."""
        if len(self.memory) == 0:
            print("No history yet.")
            return
        print("\n🕓 --- HISTORY ---")
        for i, entry in enumerate(self.memory, 1):
            status = "✔️" if entry['finalized'] else "🟡"
            print(f"{i}. {status} {entry['prompt']} → {entry['response']}")


# --- Main Terminal Mode ---
def main():
    print("\AIM - AI MEETING MANAGER (Terminal Mode)")
    print("Commands: ADD, UNDO, FINALIZE, HISTORY, EXIT\n")

    ctx = ContextManager(max_tokens=50)
    while True:
        cmd = input("Enter command: ").strip().upper()

        if cmd == "ADD":
            prompt = input("Your prompt: ").strip()
            ctx.add_prompt(prompt)
        elif cmd == "UNDO":
            ctx.undo()
        elif cmd == "FINALIZE":
            ctx.finalize()
        elif cmd == "HISTORY":
            ctx.history()
        elif cmd == "EXIT":
            print("👋 Exiting AIM Assistant. Goodbye!")
            break
        else:
            print("⚠️ Unknown command. Try ADD, UNDO, FINALIZE, HISTORY, or EXIT.")


if __name__ == "__main__":
    main()