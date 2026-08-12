import fitz
import pytesseract
from PIL import Image

PDF_PATH = "ihya-ul-uloom.pdf"
OUTPUT = "full_book_text.txt"

doc = fitz.open(PDF_PATH)

with open(OUTPUT, "w", encoding="utf-8") as out:
    for i in range(doc.page_count):
        print(f"Processing {i+1}/{doc.page_count}...")
        page = doc[i]
        pix = page.get_pixmap(dpi=250) # dpi 250 করলে আরো ফাস্ট হবে
        img_path = f"/tmp/p{i}.png"
        pix.save(img_path)

        # bn + ar + en একসাথে - Tesseract এ চলে!
        text = pytesseract.image_to_string(
            Image.open(img_path),
            lang='ben+ara+eng',
            config='--psm 6'
        )

        out.write(f"\n\n========== {i+1} No Page ==========\n\n")
        out.write(text)

print("Done!")
