import pygetwindow as gw
import pyautogui
import cv2
import numpy as np

# Find Bluestacks window
# window = gw.getWindowsWithTitle("BlueStacks")[0]
#
# # Get window bounds
# left, top, width, height = window.left, window.top, window.width, window.height
#
# # Screenshot only that region
# screenshot = pyautogui.screenshot(region=(left, top, width, height))
# screenshot.save("bluestacks.png")

#temporarily change these to the size of the test image which may be different then the given screen size


img = cv2.imread("test_image.png")

height, width, _ = img.shape
print(height, width)
img_copy = img.copy()

x_start, x_end = 365, 405
y_start, y_end = 118, 135
print(f"({x_start}, {y_start}, {x_end}, {y_end})")

cv2.rectangle(img_copy, (x_start, y_start), (x_end, y_end), (255,20,147), 2)

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.6
thickness = 2
text_size, _ = cv2.getTextSize("elixer bar", font, font_scale, thickness)

text_x = x_start
text_y = y_start - 10 if y_start - 10 > y_end - 10 else y_end

label = "elixer bar"
cv2.putText(img_copy, label, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)

cv2.imwrite("timer_image.png", img_copy)



