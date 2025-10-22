#!/usr/bin/env python3
"""
Generate data.js file from CSV for the website
"""

import csv
import json

CSV_FILE = "Context/60 Buisness Models (ENGLISH) - Models.csv"
OUTPUT_FILE = "website/js/data.js"


def clean_text(text):
    """Clean and escape text for JavaScript"""
    if not text:
        return ""
    # Escape quotes and newlines
    text = text.replace('"', '\\"').replace("\n", " ")
    return text.strip()


def generate_js_data():
    """Generate JavaScript data file from CSV"""
    models = []

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            model = {
                "id": idx,
                "name": clean_text(row["Business Model"]),
                "image": f"{idx:02d}-{row['Business Model'].lower().replace(' ', '-')}.png",
                "howItWorks": clean_text(row["How it works?"]),
                "origin": clean_text(row["Where it Comes from?"]),
                "examples": clean_text(row["Examples"]),
                "whoFor": clean_text(row["Who is it for?"]),
            }
            models.append(model)

    # Generate JavaScript file
    js_content = """// 60 Business Models Data
// Auto-generated from CSV file

const businessModels = """

    js_content += json.dumps(models, indent=2, ensure_ascii=False)
    js_content += """;

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = businessModels;
}
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"✓ Generated {OUTPUT_FILE}")
    print(f"✓ Total models: {len(models)}")


if __name__ == "__main__":
    generate_js_data()
