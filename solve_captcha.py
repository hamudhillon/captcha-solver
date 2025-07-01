import base64
import sys
import io
import time
from PIL import Image, ImageFilter
import pytesseract
from PIL.Image import Resampling

# Configure Tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust path if needed

def preprocess_image(base64_data):
    image_data = base64.b64decode(base64_data)
    image = Image.open(io.BytesIO(image_data)).convert("L")  # Grayscale

    # Resize early (preserves more detail)
    image = image.resize((image.width * 3, image.height * 3), Resampling.LANCZOS)

    # Use a softer binarization
    image = image.point(lambda x: 0 if x < 180 else 255, mode='1')

    # Slightly sharpen
    image = image.filter(ImageFilter.SHARPEN)

    return image

def solve_captcha(base64_data, max_retries=3, delay_sec=1):
    for attempt in range(1, max_retries + 1):
        try:
            image = preprocess_image(base64_data)

            # Save for debugging
            image.save(f"captcha_attempt_{attempt}.png")

            # OCR
            text = pytesseract.image_to_string(
                image,
                config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789=@'
            ).strip().replace(" ", "").replace("\n", "")

            if text:
                return text
            else:
                print(f"⚠️ Attempt {attempt} failed, empty result. Retrying...")
                time.sleep(delay_sec)

        except Exception as e:
            return f"ERROR: {e}"

    return ""  # Return empty if all retries fail

if __name__ == "__main__":
    base64_input = sys.stdin.read().strip()
    result = solve_captcha(base64_input)
    print(result)
