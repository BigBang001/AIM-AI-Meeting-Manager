def generate_recap(self):
    """Generate a simple dynamic recap from finalized prompts and responses."""
    recap_entries = []
    for e in self.memory.to_list():
        if e['finalized']:
            responses = " / ".join(e['responses']) if e['responses'] else "No response"
            recap_entries.append(f"{e['prompt']} → {responses}")
    return recap_entries
