import mss
import mouse
import keyboard
import pyautogui
import pyperclip
import pytesseract
import tkinter as tk
from PIL import Image
from pathlib import Path
from plyer import notification

pyperclip.determine_clipboard()

# captchar config
loop_interval_ms = 100

# captchar states
enabled = False
pressed = False
end_coords = None
start_coords = None
retain_lines = True

# config overlay
root = tk.Tk()
root.overrideredirect(True)
root.attributes('-alpha', 0.3)
root.attributes('-topmost', True)
root.config(bg='cyan')
root.withdraw()

def toggle_enabled(with_lines: bool) -> None:
    global enabled, pressed, end_coords, start_coords, retain_lines
    
    # toggle
    pressed = False
    end_coords = None
    start_coords = None
    enabled = not enabled
    retain_lines = with_lines
    
    # hide overlay when disabling
    root.withdraw()

    # indicate toggle
    notification.notify(
        title='Captchar',
        message=f"Ready to capture ({'with lines' if with_lines else 'without lines'})." if enabled else "Capture was cancelled.",
        timeout=0
    )

def toggle_enabled_lines() -> None:
    toggle_enabled(True)

def toggle_enabled_no_lines() -> None:
    toggle_enabled(False)

def terminate():
    notification.notify(
        title='Captchar',
        message=f'Captchar is now terminated.',
        timeout=0
    )
    root.after(0, root.destroy)

def get_screen_info(start: tuple[int, int], end: tuple[int, int]) -> dict[str, int] | None:
    endx, endy = end
    startx, starty = start

    # get the screen info
    top = min(starty, endy)
    left = min(startx, endx)
    width = abs(endx - startx)
    height = abs(endy - starty)

    # do nothing if width or height is zero
    if width == 0 or height == 0:
        return
    
    return {'top': top, 'left': left, 'width': width, 'height': height}

def show_overlay(start: tuple[int, int], end: tuple[int, int]) -> None:
    screen_info = get_screen_info(start, end)

    if not screen_info:
        return
    
    screen_left = screen_info["left"]
    screen_top = screen_info["top"]
    screen_width = screen_info["width"]
    screen_height = screen_info["height"]
    
    root.deiconify()
    root.geometry(f'{screen_width}x{screen_height}+{screen_left}+{screen_top}')

def capture(start: tuple[int, int], end: tuple[int, int]) -> None:
    screen_info = get_screen_info(start, end)

    if not screen_info:
        return

    with mss.mss() as screen:
        # capture the screen with the specified screen info
        image = screen.grab(screen_info)
        image_filename = Path(__file__).parent / 'latest.png'
        mss.tools.to_png(image.rgb, image.size, output=image_filename)

        # point to the tesseract executable's path
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        # extract text from the captured image
        text = pytesseract.image_to_string(Image.open(image_filename))
        text_splitted = text.split('\n')

        # copy the extracted text to the clipboard with/without retained lines
        pyperclip.copy(f'{"\n" if retain_lines else " "}'.join(line.strip() for line in text_splitted if line.strip()))

        # notify extraction success
        notification.notify(
            title='Captchar',
            message=f'Text copied.',
            timeout=0
        )
        
        # cleanup: remove the captured image from the filesystem
        image_filename.unlink(missing_ok=True)

def loop():
    global pressed, start_coords, end_coords, enabled

    # only process mouse events if enabled
    if not enabled:
        root.withdraw()
        root.after(loop_interval_ms, loop)
        return

    coords = pyautogui.position()
    pressing = mouse.is_pressed(button='left')

    if pressing and pressed:
        show_overlay(start_coords, coords)
    else:
        root.withdraw()
    
    if pressing:
        if not pressed:
            pressed = True
            start_coords = coords
    else:
        if pressed:
            pressed = False
            end_coords = coords
            enabled = False
            capture(start_coords, end_coords)

    root.after(loop_interval_ms, loop)

# config hotkeys
keyboard.add_hotkey('ctrl+alt+l', toggle_enabled_lines)
keyboard.add_hotkey('ctrl+alt+x', toggle_enabled_no_lines)
keyboard.add_hotkey('ctrl+alt+d', terminate)

# initial run
loop()

# notify
notification.notify(
    title='Captchar',
    message=f'Captchar is now running.',
    timeout=0
)

# run main loop
root.mainloop()