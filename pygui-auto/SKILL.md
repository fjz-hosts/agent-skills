---
name: pygui-auto
description: Automate computer operations using PyGUIAuto library. Use when user requests to open applications or programs, create new files on the computer, type text using keyboard simulation, fill input fields or forms, click buttons or UI elements, press keyboard shortcuts or keys, or perform any GUI automation tasks that require mouse or keyboard interaction.
---

# PyGUI Auto

Automate computer GUI operations using PyGUIAuto library for mouse and keyboard control.

## Quick Start

### Prerequisites

Install PyGUIAuto:
```bash
pip install pyautogui
```

For window activation features (recommended):
```bash
pip install pywin32 psutil
```

### Common Operations

**Open application:**
```bash
python scripts/open_application.py --app "Notepad"
python scripts/open_application.py --path "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
```

The `open_application.py` script automatically:
1. Launches the application
2. Waits for the window to load (3 seconds)
3. Searches for the window by application name
4. Activates and brings the window to front

If the window is found and activated, it displays ✅ success message. If not found, it shows ⚠️ warning.

**Type text:**
```bash
python scripts/type_text.py --text "Hello World"
```

**Press key:**
```bash
python scripts/press_key.py --key "enter"
python scripts/press_key.py --key "ctrl+c" --combo
```

**Click mouse:**
```bash
python scripts/click_mouse.py --x 100 --y 200
python scripts/click_mouse.py --x 100 --y 200 --button right
```

**Create file:**
```bash
python scripts/create_file.py --path "C:\\Users\\User\\Documents\\test.txt" --content "Hello World"
```

## Automation Patterns

### Pattern 1: Open Application and Type

```bash
python scripts/open_application.py --app "Notepad"
# Wait for app to load (add delay as needed)
python scripts/type_text.py --text "Hello World"
```

Note: The `open_application.py` script automatically verifies window activation. No manual delay needed for window detection.

### Pattern 2: Fill Form Fields

```bash
python scripts/click_mouse.py --x 100 --y 200
python scripts/type_text.py --text "John Doe"
python scripts/press_key.py --key "tab"
python scripts/type_text.py --text "john@example.com"
python scripts/press_key.py --key "tab"
python scripts/type_text.py --text "123-456-7890"
```

### Pattern 3: Keyboard Shortcuts

```bash
python scripts/press_key.py --key "ctrl+s" --combo  # Save
python scripts/press_key.py --key "ctrl+c" --combo  # Copy
python scripts/press_key.py --key "ctrl+v" --combo  # Paste
python scripts/press_key.py --key "alt+tab" --combo  # Switch windows
```

## Best Practices

1. **Add delays** between operations to allow UI to respond
2. **Test coordinates** before automation by checking mouse position
3. **Use application names** when possible instead of full paths
4. **Handle errors** gracefully - check if operations succeed
5. **Use keyboard navigation** (Tab) instead of coordinates when possible
6. **Window activation**: The `open_application.py` script automatically checks if the window is displayed and activates it. Install `pywin32` and `psutil` for full window management features

## Safety

PyGUIAuto includes failsafe: move mouse to screen corner to abort automation.

## Resources

- **[pyguiauto_reference.md](references/pyguiauto_reference.md)** - Complete API reference and advanced patterns
- **scripts/** - Pre-built automation scripts for common operations
