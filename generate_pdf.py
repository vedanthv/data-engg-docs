from playwright.sync_api import sync_playwright
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os

BASE_URL = "https://vedanthv.github.io/data-engg-docs/"
SECTION_PREFIX = BASE_URL + "databricks/"
OUTPUT_PDF = "databricks.pdf"

# Helper: create a title page using Playwright (HTML -> PDF)
def create_title_page(page, filename="title.pdf"):
    html = """
    <html>
      <head>
        <meta charset="utf-8">
      </head>
      <body style="display:flex; justify-content:center; align-items:center; height:100vh; font-size:48px; font-family:sans-serif;">
        📘 Databricks Deep Dive 🚀 ✅
      </body>
    </html>
    """
    tmp_html = "title.html"
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)

    page.goto("file://" + os.path.abspath(tmp_html), wait_until="networkidle")
    page.pdf(
        path=filename,
        format="A4",
        print_background=True,
        margin={"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"},
    )
    os.remove(tmp_html)
    return filename

# Helper: add page numbers (monochrome, but safe everywhere)
def add_page_numbers(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages, start=1):
        # Use a simple text watermark with PyPDF2
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfbase import pdfmetrics

        width, height = A4
        tmp = f"num_{page_num}.pdf"
        c = canvas.Canvas(tmp, pagesize=A4)
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, 15, f"Page {page_num} ✅")  # add emoji check
        c.save()

        overlay = PdfReader(tmp)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)
        os.remove(tmp)

    with open(output_pdf, "wb") as f:
        writer.write(f)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Step 1: Load homepage
    page.goto(BASE_URL, wait_until="networkidle")

    # Step 2: Collect all nav links
    all_links = page.eval_on_selector_all("nav a", "els => els.map(el => el.href)")

    # Step 3: Keep only Databricks section
    section_links = [l for l in all_links if l.startswith(SECTION_PREFIX)]
    section_links = list(dict.fromkeys(section_links))  # deduplicate

    print("Databricks links found:", section_links)

    pdf_files = []

    # Step 4: Title page via Playwright
    topics_pdf = create_title_page(page, "title.pdf")
    pdf_files.append(topics_pdf)

    # Step 5: Visit each link and save as PDF with margins
    for i, link in enumerate(section_links, start=1):
        page.goto(link, wait_until="networkidle")
        filename = f"databricks_{i}.pdf"
        page.pdf(
            path=filename,
            format="A4",
            print_background=True,
            margin={"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"},
        )
        pdf_files.append(filename)
        print(f"Saved {filename} from {link}")

    browser.close()

# Step 6: Merge PDFs
print("Merging PDFs...")
merger = PdfMerger()
for pdf in pdf_files:
    merger.append(pdf)
merger.write(OUTPUT_PDF)
merger.close()

# Cleanup intermediate PDFs
for pdf in pdf_files:
    os.remove(pdf)

# Step 7: Add page numbers
print("Adding page numbers...")
final_output = "databricks_docs_numbered.pdf"
add_page_numbers(OUTPUT_PDF, final_output)
os.remove(OUTPUT_PDF)

print(f"✅ Final combined PDF with emojis saved as {final_output}")
