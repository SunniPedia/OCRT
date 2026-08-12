import fitz
import easyocr
import os
import re

PDF_PATH = "ihya-ul-uloom.pdf"
OUTPUT_FILE = "full_book_text.txt"

print("Loading models...")

# ১. বাংলা রিডার
reader_bn = easyocr.Reader(['bn', 'en'], gpu=False)
# ২. আরবি রিডার (আলাদা)
reader_ar = easyocr.Reader(['ar', 'en'], gpu=False)

# আরবি আছে কিনা চেক করার জন্য
arabic_pattern = re.compile(r'[\u0600-\u06FF]')

doc = fitz.open(PDF_PATH)

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

for i in range(doc.page_count):
    print(f"--> {i+1}/{doc.page_count} No Page processing...")
    page = doc[i]
    pix = page.get_pixmap(dpi=350)
    img_path = f"/tmp/page_{i+1}.png"
    pix.save(img_path)

    # বাংলা + ইংরেজি পড়া (detail=1 দিলে position সহ পাওয়া যায়)
    bn_results = reader_bn.readtext(img_path, detail=1)
    ar_results = reader_ar.readtext(img_path, detail=1)

    all_boxes = []

    for box, text, conf in bn_results:
        # y position = box[0][1]
        y = box[0][1]
        all_boxes.append((y, text.strip(), conf, 'bn'))

    for box, text, conf in ar_results:
        # শুধু আরবি টেক্সট গুলোই নেবো, বাংলা ডুপ্লিকেট বাদ যাবে
        if arabic_pattern.search(text):
            y = box[0][1]
            all_boxes.append((y, text.strip(), conf, 'ar'))

    # y অনুযায়ী উপর থেকে নিচে সাজানো, তাহলে লেখা উল্টা পাল্টা হবে না
    all_boxes.sort(key=lambda x: x[0])

    # একসাথে জোড়া লাগানো
    final_text_lines = []
    for y, text, conf, lang in all_boxes:
        if text and len(text) > 1:
            final_text_lines.append(text)

    page_text = "\n".join(final_text_lines)

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n\n========== {i+1} No Page ==========\n\n")
        f.write(page_text)

print(f"\nAlhamdulillah! Done! Arabic + Bengali saved in {OUTPUT_FILE}")
