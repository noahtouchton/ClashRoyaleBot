import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import time
import pytesseract

# Reference resolution (base coords come from this)
REF_WIDTH = 506
REF_HEIGHT = 900

# Define all the box coordinates in reference resolution
# Each entry: "label": (x_start, y_start, x_end, y_end)
BOXES = {
    "timer": (430, 18, 495, 48),
    "elixer bar": (172, 870, 490, 890),
    "card 1": (117, 750, 200, 855),
    "card 2": (210, 750, 295, 855),
    "card 3": (305, 750, 390, 855),
    "card 4": (400, 750, 486, 855),
    "next": (30,840, 65, 890),
    "player tower 1": (100,560,140,577),
    "player tower 2": (365, 560, 405, 577),
    "enemy tower 1": (100, 118, 140, 135),
    "enemy tower 2": (365, 118, 405, 135)
    #add king towers
}

def scale_boxes(width, height):
    """Return scaled boxes based on the current window size."""
    x_scale = width / REF_WIDTH
    y_scale = height / REF_HEIGHT

    scaled = {}
    for label, (x1, y1, x2, y2) in BOXES.items():
        scaled[label] = (
            int(x1 * x_scale),
            int(y1 * y_scale),
            int(x2 * x_scale),
            int(y2 * y_scale)
        )
    return scaled

def draw_boxes_on_image(img, boxes):
    """Draw all boxes with labels on the image."""
    img_copy = img.copy()
    for label, (x1, y1, x2, y2) in boxes.items():
        cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Add label text
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img_copy, label, (x1, y1 - 5), font, 0.5, (255, 255, 255), 1)
    return img_copy

def extract_text(img, box_coords):
    (x1, y1, x2, y2) = box_coords
    cropped = img[y1:y2, x1:x2]

    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150,255, cv2.THRESH_BINARY_INV)[1]

    raw_text = pytesseract.image_to_string(gray, config="--psm 7 digits")
    raw_text = raw_text.strip()

    return raw_text

def find_time(img, scaled_boxes):
    raw_time_text = extract_text(img, scaled_boxes["timer"])

    # If OCR returns blank text, skip immediately
    if raw_time_text is None or raw_time_text.strip() == "":
        print("Timer OCR returned blank text this frame")
    else:
        # Remove any colon characters if present
        raw_time_text = raw_time_text.replace(":", "").strip()

        try:
            raw_time = int(raw_time_text)
            seconds = raw_time % 100
            minutes = raw_time // 100


        except (ValueError, TypeError):
            # Skip bad OCR frames
            print(f"Timer OCR failed: '{raw_time_text}'")

def check_pixel(img, pixel, desired_color, tolerance=0):
    x, y = pixel
    x = int(x)
    y = int(y)

    # Check bounds
    if not (0 <= x < img.shape[1] and 0 <= y < img.shape[0]):
        return False

    pixel_color = img[y, x]  # OpenCV uses BGR and row=y, col=x

    # Compare color with tolerance
    return all(abs(int(pc) - int(dc)) <= tolerance for pc, dc in zip(pixel_color, desired_color))


def check_if_on_menu(img, real_w, real_h, tolerance=10):
    # Reference window dimensions (base resolution)
    window_w = 501
    window_h = 865

    # Reference pixel position from base resolution
    ref_x, ref_y = 295, 698

    # Scale to current resolution
    scaled_x = real_w / window_w * ref_x
    scaled_y = real_h / window_h * ref_y

    # Reference BGR color (Clash Royale menu button?)
    ref_color = (0, 164, 255)

    return check_pixel(img, (scaled_x, scaled_y), ref_color, tolerance)




def main():
    window = gw.getWindowsWithTitle("BlueStacks")[0]

    print("Press Ctrl+C to stop...")
    while True:
        # Get window bounds
        left, top, width, height = window.left, window.top, window.width, window.height

        # Take screenshot
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        #img = cv2.imread("test_image.png")
        #height, width, _ = img.shape
        # Scale boxes to current window size
        scaled_boxes = scale_boxes(width, height)

        if not check_if_on_menu(img, width, height):

            # Draw boxes
            img_with_boxes = draw_boxes_on_image(img, scaled_boxes)

            # Save the image
            cv2.imwrite("bluestacks_debug.png", img_with_boxes)

            # Show live window (optional)
            cv2.imshow("Bluestacks Tracker", img_with_boxes)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            raw_time_text = extract_text(img, scaled_boxes["timer"])

            # If OCR returns blank text, skip immediately
            if raw_time_text is None or raw_time_text.strip() == "":
                print("Timer OCR returned blank text this frame")
            else:
                # Remove any colon characters if present
                raw_time_text = raw_time_text.replace(":", "").strip()

                try:
                    raw_time = int(raw_time_text)
                    seconds = raw_time % 100
                    minutes = raw_time // 100


                except (ValueError, TypeError):
                    # Skip bad OCR frames
                    print(f"Timer OCR failed: '{raw_time_text}'")

            # Control refresh rate (lower = faster but more CPU)
            time.sleep(0.05)
        else:
            print("In menu waiting to start...")
            time.sleep(0.1)
            cv2.destroyAllWindows()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
