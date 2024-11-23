import easyocr

reader = easyocr.Reader(['en'])  # Replace 'en' with the appropriate language code
result = reader.readtext('cropped_image.png')

for (bbox, text, conf) in result:
    print(text)

from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import pytesseract


