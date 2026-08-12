# Pillow 10 এর Bug Fix - EasyOCR এর জন্য
from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

import fitz
import easyocr
import os
import re

PDF_PATH = "ihya-ul-uloom.pdf"
OUTPUT_FILE = "full_book_text.txt"

print("Loading models...")

# আলাদা Reader
reader_bn = easyocr.Reader(['bn', 'en'], gpu=False)
reader_ar = easyocr.Reader(['ar', 'en'], gpu=False)

arabic_pattern = re.compile(r'[\u0600-\u06FF]')

doc = fitz.open(PDF_PATH)

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

for i in range(doc.page_count):
    print(f"--> {i+1}/{doc.page_count} No Page...")
    page = doc[i]
    pix = page.get_pixmap(dpi=320)
    img_path = f"/tmp/page_{i+1}.png"
    pix.save(img_path)

    bn_results = reader_bn.readtext(img_path, detail=1, paragraph=False)
    ar_results = reader_ar.readtext(img_path, detail=1, paragraph=False)

    all_boxes = []
    for box, text, conf in bn_results:
        if conf > 0.3:
            y = box[0][1]
            all_boxes.append((y, text.strip()))

    for box, text, conf in ar_results:
        if conf > 0.3 and arabic_pattern.search(text):
            y = box[0][1]
            all_boxes.append((y, text.strip()))

    # উপর থেকে নিচে সাজানো
    all_boxes.sort(key=lambda x: x[0])

    # ডুপ্লিকেট বাদ দেওয়া
    seen = set()
    final_lines = []
    for y, t in all_boxes:
        if t not in seen:
            final_lines.append(t)
            seen.add(t)

    page_text = "\n".join(final_lines)

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n\n========== {i+1} No Page ==========\n\n")
        f.write(page_text)

print(f"\nDone! Saved to {OUTPUT_FILE}")
