import argparse
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, LEGAL, LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


PAGE_SIZES = {
    "A4": A4,
    "LETTER": LETTER,
    "LEGAL": LEGAL,
}


def parse_hex_color(value: str, fallback: str) -> colors.HexColor:
    try:
        return colors.HexColor(value)
    except Exception:
        return colors.HexColor(fallback)


def build_styles(theme: dict) -> dict:
    primary = parse_hex_color(theme.get("primary_color", "#17324d"), "#17324d")
    accent = parse_hex_color(theme.get("accent_color", "#e9f0f7"), "#e9f0f7")
    text = parse_hex_color(theme.get("text_color", "#222222"), "#222222")

    base = getSampleStyleSheet()
    return {
        "primary": primary,
        "accent": accent,
        "text": text,
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=text,
            spaceAfter=6,
        ),
        "section_title": ParagraphStyle(
            "SectionTitle",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=primary,
            spaceBefore=6,
            spaceAfter=8,
        ),
        "kv_label": ParagraphStyle(
            "KVLabel",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=14,
            textColor=primary,
        ),
        "kv_value": ParagraphStyle(
            "KVValue",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=text,
        ),
        "header_title": ParagraphStyle(
            "HeaderTitle",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=20,
            textColor=primary,
            alignment=TA_LEFT,
        ),
        "header_subtitle": ParagraphStyle(
            "HeaderSubtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=12,
            textColor=text,
            alignment=TA_LEFT,
        ),
        "header_right": ParagraphStyle(
            "HeaderRight",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            textColor=primary,
            alignment=TA_RIGHT,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=text,
            alignment=TA_RIGHT,
        ),
    }


def draw_header_footer(canvas, doc, payload, styles):
    canvas.saveState()
    width, height = doc.pagesize
    left = doc.leftMargin
    right = width - doc.rightMargin

    header = payload.get("header", {})
    footer = payload.get("footer", {})

    canvas.setStrokeColor(styles["primary"])
    canvas.setLineWidth(0.75)
    canvas.line(left, height - 22 * mm, right, height - 22 * mm)

    title = header.get("title", payload.get("document", {}).get("title", "PDF Document"))
    subtitle = header.get("subtitle", "")
    right_text = header.get("right_text", "")

    canvas.setFont("Helvetica-Bold", 16)
    canvas.setFillColor(styles["primary"])
    canvas.drawString(left, height - 15 * mm, title)

    if subtitle:
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(styles["text"])
        canvas.drawString(left, height - 19.5 * mm, subtitle)

    if right_text:
        canvas.setFont("Helvetica-Bold", 9)
        canvas.setFillColor(styles["primary"])
        canvas.drawRightString(right, height - 15 * mm, right_text)

    footer_text = footer.get("text", "")
    page_number = f"Page {canvas.getPageNumber()}"
    canvas.setStrokeColor(styles["accent"])
    canvas.line(left, 15 * mm, right, 15 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(styles["text"])
    if footer_text:
        canvas.drawString(left, 10 * mm, footer_text)
    canvas.drawRightString(right, 10 * mm, page_number)
    canvas.restoreState()


def build_key_value_section(section, styles):
    rows = []
    for item in section.get("items", []):
        label = Paragraph(str(item.get("label", "")), styles["kv_label"])
        value = Paragraph(str(item.get("value", "")), styles["kv_value"])
        rows.append([label, value])

    if not rows:
        return []

    table = Table(rows, colWidths=[55 * mm, 110 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("LINEBELOW", (0, 0), (-1, -1), 0.25, styles["accent"]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return [table, Spacer(1, 8)]


def build_paragraph_section(section, styles):
    text = str(section.get("text", ""))
    if not text:
        return []
    return [Paragraph(text, styles["body"]), Spacer(1, 8)]


def build_bullets_section(section, styles):
    items = []
    for raw in section.get("items", []):
        items.append(ListItem(Paragraph(str(raw), styles["body"])))

    if not items:
        return []

    bullets = ListFlowable(items, bulletType="bullet", start="circle", leftIndent=18)
    return [bullets, Spacer(1, 8)]


def build_table_section(section, styles):
    columns = section.get("columns", [])
    rows = section.get("rows", [])
    if not columns or not rows:
        return []

    headers = [Paragraph(str(col.get("header", "")), styles["kv_label"]) for col in columns]
    table_rows = [headers]
    for row in rows:
        table_rows.append(
            [Paragraph(str(row.get(col.get("key", ""), "")), styles["body"]) for col in columns]
        )

    col_widths = [col.get("width", 100) for col in columns]
    table = Table(table_rows, colWidths=col_widths, hAlign="LEFT", repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), styles["accent"]),
                ("TEXTCOLOR", (0, 0), (-1, 0), styles["primary"]),
                ("GRID", (0, 0), (-1, -1), 0.25, styles["accent"]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return [table, Spacer(1, 10)]


def build_story(payload, styles):
    story = [Spacer(1, 28 * mm)]
    for section in payload.get("sections", []):
        section_type = section.get("type", "").lower()
        title = section.get("title")
        if title:
            story.append(Paragraph(str(title), styles["section_title"]))

        if section_type == "key_value":
            story.extend(build_key_value_section(section, styles))
        elif section_type == "paragraph":
            story.extend(build_paragraph_section(section, styles))
        elif section_type == "bullets":
            story.extend(build_bullets_section(section, styles))
        elif section_type == "table":
            story.extend(build_table_section(section, styles))
        elif section_type == "spacer":
            story.append(Spacer(1, float(section.get("height", 12))))
        elif section_type == "page_break":
            story.append(PageBreak())
        else:
            story.append(Paragraph(f"Unsupported section type: {section_type}", styles["body"]))
            story.append(Spacer(1, 8))
    return story


def generate_pdf(payload: dict, output_path: Path):
    document = payload.get("document", {})
    page_size_name = str(document.get("page_size", "A4")).upper()
    page_size = PAGE_SIZES.get(page_size_name, A4)
    styles = build_styles(payload.get("theme", {}))

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=page_size,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=24 * mm,
        bottomMargin=22 * mm,
        title=document.get("title", "PDF Document"),
        author=document.get("author", ""),
    )

    story = build_story(payload, styles)
    doc.build(
        story,
        onFirstPage=lambda canvas, current_doc: draw_header_footer(
            canvas, current_doc, payload, styles
        ),
        onLaterPages=lambda canvas, current_doc: draw_header_footer(
            canvas, current_doc, payload, styles
        ),
    )


def main():
    parser = argparse.ArgumentParser(description="Generate a PDF from a JSON definition.")
    parser.add_argument("--input", required=True, help="Path to the input JSON file.")
    parser.add_argument(
        "--output",
        help="Path to the output PDF. If omitted, the JSON document filename is used.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    with input_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    output = args.output or payload.get("document", {}).get("filename") or "output.pdf"
    output_path = Path(output)
    generate_pdf(payload, output_path)
    print(f"Created PDF: {output_path.resolve()}")


if __name__ == "__main__":
    main()
