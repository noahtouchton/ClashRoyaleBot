import cv2
import pyautogui
import numpy as np
import pygetwindow as gw

def show_pixel_color_clash_royale():
    # Find the Clash Royale/BlueStacks window
    window = None
    for w in gw.getAllWindows():
        if "Blue" in w.title:   # Match "BlueStacks" window
            window = w
            break

    if window is None:
        print("❌ Clash Royale window not found!")
        return

    # Print the window size for scaling purposes
    print(f"📏 Window Size: Width = {window.width}, Height = {window.height}")

    cv2.namedWindow("Clash Royale Live")
    frame_holder = {"frame": None}

    # Mouse callback to show color + coords
    def mouse_event(event, x, y, flags, param):
        frame = frame_holder["frame"]
        if frame is not None and event == cv2.EVENT_MOUSEMOVE:
            if 0 <= y < frame.shape[0] and 0 <= x < frame.shape[1]:
                b, g, r = frame[y, x]
                print(f"Position: ({x}, {y}) | Color (BGR): ({b}, {g}, {r})")

    cv2.setMouseCallback("Clash Royale Live", mouse_event)

    while True:
        # Update window position each frame
        left, top, width, height = window.left, window.top, window.width, window.height

        # Screenshot only the window region
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        frame_holder["frame"] = frame
        cv2.imshow("Clash Royale Live", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):   # Quit if 'q'
            break
        if key == ord('y'):   # Stop completely if 'y'
            print("🛑 Stopped because 'y' was pressed.")
            break

    cv2.destroyAllWindows()

show_pixel_color_clash_royale()
yyy