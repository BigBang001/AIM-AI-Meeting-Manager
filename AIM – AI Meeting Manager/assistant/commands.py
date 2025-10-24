from .core import ContextManager

# Initialize context with window size 5
context = ContextManager(max_context_pairs=5)

def handle_prompt(text):
    context.add_prompt(text)
    return "Prompt added & AI response generated!"

def handle_undo():
    res = context.undo_response()
    return f"Undone: {res}" if res else "No response to undo!"

def handle_finalize():
    context.finalize_prompt()
    return "Prompt finalized!"

def handle_pin(index):
    context.pin_prompt(index)
    return f"Pinned prompt {index}"
