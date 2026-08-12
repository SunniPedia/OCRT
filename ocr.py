import fitz # PyMuPDF
import easyocr
import os

PDF_PATH = "ihya-ul-uloom.pdf"
OUTPUT_FILE = "full_book_text.txt"

# বাংলা + আরবি + ইংরেজি সাপোর্ট
print("Loading OCR model... (first time 2 min lagbe)")
reader = easyocr.Reader(['bn', 'ar', 'en'], gpu=False)

doc = fitz.open(PDF_PATH)
print(f"Total PDF Pages: {doc.page_count}")

# আগের ফাইল থাকলে ডিলিট
if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

full_text = ""

for i in range(doc.page_count):
    print(f"--> Processing {i+1}/{doc.page_count} No Page...")
    page = doc[i]
    # dpi 350 দিলে বাংলা লেখা সবচেয়ে ক্লিয়ার আসে
    pix = page.get_pixmap(dpi=350)
    img_path = f"/tmp/page_{i+1}.png"
    pix.save(img_path)

    # Same to Same OCR
    result = reader.readtext(img_path, detail=0, paragraph=True)
    page_text = "\n".join(result)

    # ফাইলে লেখা
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n\n========== {i+1} No Page ==========\n\n")
        f.write(page_text)

print(f"\nDone! Full book saved in {OUTPUT_FILE}")
