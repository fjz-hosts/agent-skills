# PyGUIAuto Reference

Complete reference for PyGUIAuto library functions and common automation patterns.

## Installation

```bash
pip install pyautogui
```

## Core Functions

### Mouse Control

#### `pyautogui.click(x=None, y=None, button='left', clicks=1, interval=0.0)`
Click at specified coordinates.

**Parameters:**
- `x`, `y`: Screen coordinates (pixels from top-left)
- `button`: 'left', 'right', or 'middle'
- `clicks`: Number of clicks (1 for single, 2 for double)
- `interval`: Delay between clicks in seconds

**Examples:**
```python
pyautogui.click(100, 200)  # Left click at (100, 200)
pyautogui.click(100, 200, button='right')  # Right click
pyautogui.click(100, 200, clicks=2)  # Double click
```

#### `pyautogui.moveTo(x, y, duration=0.0)`
Move mouse to coordinates.

**Parameters:**
- `x`, `y`: Target coordinates
- `duration`: Movement duration in seconds (0 for instant)

#### `pyautogui.dragTo(x, y, duration=0.0, button='left')`
Drag mouse while holding button.

#### `pyautogui.scroll(clicks, x=None, y=None)`
Scroll mouse wheel.

**Parameters:**
- `clicks`: Positive scrolls up, negative scrolls down
- `x`, `y`: Position to scroll at (optional)

### Keyboard Control

#### `pyautogui.write(text, interval=0.0)`
Type text character by character.

**Parameters:**
- `text`: String to type
- `interval`: Delay between characters in seconds

**Examples:**
```python
pyautogui.write("Hello World")
pyautogui.write("Hello", interval=0.1)  # Slower typing
```

#### `pyautogui.press(key)`
Press a single key.

**Common keys:**
- Letters: 'a', 'b', 'c', etc.
- Numbers: '0', '1', '2', etc.
- Special: 'enter', 'tab', 'space', 'backspace', 'delete', 'esc'
- Arrow keys: 'up', 'down', 'left', 'right'
- Function keys: 'f1', 'f2', ..., 'f12'

**Examples:**
```python
pyautogui.press('enter')
pyautogui.press('tab')
pyautogui.press('f5')
```

#### `pyautogui.hotkey(*keys)`
Press key combination simultaneously.

**Parameters:**
- `*keys`: Variable number of keys to press together

**Examples:**
```python
pyautogui.hotkey('ctrl', 'c')  # Copy
pyautogui.hotkey('ctrl', 'v')  # Paste
pyautogui.hotkey('ctrl', 's')  # Save
pyautogui.hotkey('alt', 'tab')  # Switch windows
pyautogui.hotkey('ctrl', 'shift', 'esc')  # Task Manager
```

### Screen Information

#### `pyautogui.size()`
Get screen dimensions.

**Returns:** (width, height) tuple

**Example:**
```python
width, height = pyautogui.size()
print(f"Screen size: {width}x{height}")
```

#### `pyautogui.position()`
Get current mouse position.

**Returns:** (x, y) tuple

**Example:**
```python
x, y = pyautogui.position()
print(f"Mouse at: ({x}, {y})")
```

### Image Recognition

#### `pyautogui.locateOnScreen(image, confidence=0.9)`
Find image on screen.

**Parameters:**
- `image`: Path to image file
- `confidence`: Match confidence threshold (0.0 to 1.0)

**Returns:** Box object or None if not found

**Example:**
```python
location = pyautogui.locateOnScreen('button.png', confidence=0.8)
if location:
    center = pyautogui.center(location)
    pyautogui.click(center)
```

#### `pyautogui.locateCenterOnScreen(image, confidence=0.9)`
Find image and return center coordinates.

**Returns:** (x, y) tuple or None

### Safety Features

#### `pyautogui.FAILSAFE = True`
Enable failsafe (move mouse to corner to abort)

#### `pyautogui.PAUSE = 0.1`
Set delay between PyGUIAuto calls (seconds)

## Common Automation Patterns

### Pattern 1: Open Application and Type

```python
import subprocess
import pyautogui
import time

subprocess.Popen(['notepad.exe'])
time.sleep(1)  # Wait for app to load
pyautogui.write("Hello World")
```

### Pattern 2: Fill Form Fields

```python
import pyautogui

pyautogui.click(100, 200)  # Click first field
pyautogui.write("John Doe")
pyautogui.press('tab')  # Move to next field
pyautogui.write("john@example.com")
pyautogui.press('tab')
pyautogui.write("123-456-7890")
```

### Pattern 3: Menu Navigation

```python
import pyautogui

pyautogui.hotkey('alt', 'f')  # Open File menu
time.sleep(0.2)
pyautogui.press('s')  # Select Save
```

### Pattern 4: Image-Based Automation

```python
import pyautogui

submit_button = pyautogui.locateCenterOnScreen('submit.png', confidence=0.8)
if submit_button:
    pyautogui.click(submit_button)
else:
    print("Button not found")
```

## Key Names Reference

### Modifier Keys
- `ctrl`, `alt`, `shift`, `win` (Windows key), `cmd` (Mac)

### Special Keys
- `enter`, `return`, `tab`, `space`, `backspace`, `delete`, `esc`
- `insert`, `home`, `end`, `pageup`, `pagedown`
- `up`, `down`, `left`, `right`
- `capslock`, `numlock`, `scrolllock`
- `printscreen`, `pause`, `menu`

### Function Keys
- `f1` through `f12`

### Numpad Keys
- `num0` through `num9`
- `numlock`, `numdivide`, `nummultiply`, `numminus`, `numplus`, `numenter`, `numperiod`

## Error Handling

```python
import pyautogui

try:
    pyautogui.click(100, 200)
except pyautogui.FailSafeException:
    print("Failsafe triggered - mouse moved to corner")
except Exception as e:
    print(f"Error: {e}")
```

## Best Practices

1. **Add delays** between operations to allow UI to respond
2. **Use failsafe** to prevent runaway automation
3. **Test coordinates** with `pyautogui.position()` before automation
4. **Handle exceptions** gracefully
5. **Use image recognition** when coordinates might change
6. **Set appropriate confidence** for image matching (0.7-0.9 typically)

## Troubleshooting

### PyGUIAuto not responding
- Check if application is in focus
- Add delays between operations
- Verify coordinates are correct

### Image recognition failing
- Lower confidence threshold
- Ensure screenshot matches actual screen resolution
- Use partial images for better matching

### Mouse movements too fast
- Increase duration in `moveTo()`
- Set `pyautogui.PAUSE` to add delays
