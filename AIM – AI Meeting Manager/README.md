# AIM: AI Meeting Manager

**AIM** is a terminal and web-based AI meeting assistant that helps you manage meeting prompts, automatically generates professional AI responses, and maintains a context-aware memory of conversations. It simulates real AI behavior with token-limited memory, undo/redo features, and a recap of finalized discussions.

---

## Features

### Terminal Mode

* Add meeting prompts and receive automated AI suggestions.
* Undo the last AI response.
* Finalize prompts to lock their responses.
* View the full history of prompt-response pairs.
* Context-aware token memory: older prompts are automatically removed when the token limit is exceeded.

### Web App Mode

* Modern, responsive UI with dark/light theme toggle (sun/moon icon).
* Context memory bar showing token usage.
* Sections for **Active**, **Finalized**, and **Pinned** prompts.
* Buttons for **Add Prompt**, **Undo**, **Finalize**, and **Pin**.
* Dynamic recap section for reviewing finalized prompts.
* Token-limited context with automatic removal of oldest unpinned prompts.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/aim-ai-meeting-manager.git
cd aim-ai-meeting-manager
```

2. Create and activate a Python virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Terminal Usage

Run the terminal assistant:

```bash
python core.py
```

### Commands

| Command    | Description                                                         |
| ---------- | ------------------------------------------------------------------- |
| `ADD`      | Add a new meeting prompt. The program will prompt you for the text. |
| `UNDO`     | Undo the last AI response.                                          |
| `FINALIZE` | Finalize the last active prompt and lock its response.              |
| `HISTORY`  | Display all prompt-response pairs.                                  |
| `EXIT`     | Exit the terminal assistant.                                        |

**Example Terminal Session:**

```
Enter command: ADD
Your prompt: Project X update
✅ Added: Project X update
🤖 AI: I've noted your update. We'll reflect that in the meeting summary.

Enter command: HISTORY
🕓 --- HISTORY ---
1. 🟡 Project X update → I've noted your update. We'll reflect that in the meeting summary.

Enter command: FINALIZE
✅ Finalized: Project X update → I've noted your update. We'll reflect that in the meeting summary
```

---

## Web App Usage

1. Start the Flask server:

```bash
python main.py
```

2. Open your browser at:

```
http://127.0.0.1:5000/
```

3. Features:

* Add prompts using the input box.
* Undo the latest AI response.
* Finalize prompts.
* Pin prompts to prevent automatic removal.
* Toggle dark/light mode using the sun/moon button.
* See **Active**, **Finalized**, and **Pinned** prompts in separate sections.
* Context memory bar shows token usage out of the maximum.

---

## Project Structure

```
aim-ai-meeting-manager/
├─ assistant/
│  ├─ __init__.py
│  ├─ core.py          # Core logic for terminal & web modes
├─ web_ui/
│  ├─ index.html       # Web interface
│  ├─ app.js           # JS interactions
│  ├─ style.css        # Styling, dark/light mode
├─ main.py             # Flask server
├─ tests/
│  ├─ test_context_manager.py  # Unit tests for context logic
├─ README.md
├─ requirements.txt
```

---

## Testing

Run unit tests to validate context manager behavior:

```bash
python -m unittest discover tests
```

Test scenarios include:

* Adding prompts and automatic AI responses.
* Undoing the latest AI response.
* Finalizing prompts.
* Token-based context limit enforcement.
* Edge cases like empty memory or empty undo stack.

---

## Notes

* Token counting is based on **words**, mimicking real AI context limitations.
* Undo removes the latest AI response and may remove the prompt if no responses remain.
* Finalized prompts are locked and cannot be undone.
* Pinned prompts are protected from automatic removal.

---

## Future Enhancements

* Multi-user support with separate context queues.
* AI learning from user input for better suggestions.
* Integration with Google Calendar or meeting platforms.
* Improved UI with real-time animations and notifications.

---