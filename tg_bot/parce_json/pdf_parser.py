import fitz


def extract_text_without_headers_footers(pdf_path, header_margin=50, footer_margin=50):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        page_rect = page.rect
        width, height = page_rect.width, page_rect.height
        header_zone = fitz.Rect(0, 0, width, header_margin)
        footer_zone = fitz.Rect(0, height - footer_margin, width, height)
        blocks = page.get_text("blocks")
        for block in blocks:
            x0, y0, x1, y1, block_text, block_no, block_type = block
            block_rect = fitz.Rect(x0, y0, x1, y1)
            if not (header_zone.intersects(block_rect) or footer_zone.intersects(block_rect)):
                text += block_text + "\n"

    return text


pdf_path = "tk.pdf"
text = extract_text_without_headers_footers(pdf_path)
with open("output_no_headers_footers.txt", "w", encoding="utf-8") as f:
    f.write(text)
print("Текст без колонтитулов сохранён в output_no_headers_footers.txt")