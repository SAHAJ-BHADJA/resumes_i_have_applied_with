# Configurable PDF Generator

This project creates PDFs from a JSON file. It is a starter generator you can adapt to your exact requirement once you provide the final fields and layout.

## Features

- Custom title, header, subtitle, and footer
- Key/value sections
- Paragraph sections
- Bullet list sections
- Table sections
- Theme colors from JSON
- A4, Letter, and Legal page sizes

## Setup

```powershell
python -m pip install -r requirements.txt
```

## Usage

```powershell
python pdf_generator.py --input sample_data.json --output output.pdf
```

If `--output` is omitted, the generator uses the filename from the JSON file.

## JSON Structure

```json
{
  "document": {
    "title": "Project Status Report",
    "filename": "project-status-report.pdf",
    "page_size": "A4",
    "author": "Your Name"
  },
  "theme": {
    "primary_color": "#17324d",
    "accent_color": "#e9f0f7",
    "text_color": "#222222"
  },
  "header": {
    "title": "Project Status Report",
    "subtitle": "April 2026",
    "right_text": "Internal Use"
  },
  "footer": {
    "text": "Confidential"
  },
  "sections": [
    {
      "type": "key_value",
      "title": "Client Information",
      "items": [
        { "label": "Client", "value": "Northwind Traders" },
        { "label": "Manager", "value": "Ava Wilson" }
      ]
    },
    {
      "type": "paragraph",
      "title": "Summary",
      "text": "This section contains a free-form paragraph."
    },
    {
      "type": "table",
      "title": "Milestones",
      "columns": [
        { "header": "Task", "key": "task", "width": 220 },
        { "header": "Owner", "key": "owner", "width": 110 },
        { "header": "Status", "key": "status", "width": 90 }
      ],
      "rows": [
        { "task": "Design", "owner": "Mia", "status": "Done" }
      ]
    },
    {
      "type": "bullets",
      "title": "Notes",
      "items": [
        "First note",
        "Second note"
      ]
    }
  ]
}
```

## Next Step

Send your exact PDF requirement and I can convert this starter into your final generator.
