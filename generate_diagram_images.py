#!/usr/bin/env python3
"""
Generate business model diagram images using Google Gemini Flash Image 2.5
Creates minimalist, geometric diagrams on dark charcoal background
"""

import os
import csv
import json
import time
from google import genai
from google.genai import types

# API Configuration
GEMINI_API_KEY = "AIzaSyAcSvcL9TpZ3_2Q00srcEBvkC-veQ0COr0"
MODEL_NAME = "gemini-2.5-flash-image"

# File paths
CSV_PATH = "Context/IMAGES FOR PFD/60 Buisness Models (ENGLISH) - Models.csv"
OUTPUT_DIR = "newImagesForEBOOK"

# Models to generate (1-5 for now)
MODELS_TO_GENERATE = range(1, 6)

# Visual structure mappings for different business models
VISUAL_STRUCTURE_MAP = {
    "Add-On": {
        "type": "core_with_satellites",
        "shapes": [
            "central circle for core product",
            "6-8 smaller rectangles around it for add-ons",
        ],
        "icons": ["price tag in center", "plus symbols on connections"],
        "arrows": ["lines connecting core to add-ons"],
        "labels": [
            "Core Product (center)",
            "Add-On options (periphery)",
            "$ symbols showing price increase",
        ],
        "highlights": ["core in white", "add-ons in cyan"],
    },
    "Affiliation": {
        "type": "flow_diagram",
        "shapes": ["three connected nodes: company, affiliate, customer"],
        "icons": ["handshake symbol", "percentage symbol for commission"],
        "arrows": ["arrows showing referral flow and payment flow"],
        "labels": ["Company", "Affiliate", "Customer", "Commission %"],
        "highlights": ["commission flow in cyan"],
    },
    "Aikido": {
        "type": "venn_overlap",
        "shapes": ["two opposing circles/rectangles", "highlighted intersection area"],
        "icons": ["opposing arrows", "contrast symbol"],
        "arrows": ["arrows showing opposite strategies"],
        "labels": ["Traditional Approach", "Aikido Approach", "Differentiation"],
        "highlights": ["differentiation zone in cyan"],
    },
    "Auction": {
        "type": "layered_progression",
        "shapes": ["ascending price bars or steps", "gavel icon"],
        "icons": ["gavel symbol", "upward arrow"],
        "arrows": ["upward progression arrows"],
        "labels": ["Starting Price", "Bid 1", "Bid 2", "Final Price"],
        "highlights": ["highest bid in cyan"],
    },
    "Barter": {
        "type": "flow_diagram",
        "shapes": ["two boxes with bidirectional arrows between them"],
        "icons": ["exchange symbol", "goods/services icons"],
        "arrows": ["bidirectional arrows showing exchange"],
        "labels": ["Party A", "Party B", "Goods/Services"],
        "highlights": ["exchange arrows in cyan"],
    },
}


def create_business_model_prompt(model_name, how_it_works, visual_structure_config):
    """
    Create a detailed image generation prompt for a business model diagram.

    Args:
        model_name: Name of the business model
        how_it_works: Description of how the model works
        visual_structure_config: Visual structure configuration dict

    Returns:
        Detailed prompt string for image generation
    """

    # Extract core concept from how_it_works (first sentence)
    core_concept = (
        how_it_works.split(".")[0] if "." in how_it_works else how_it_works[:150]
    )

    # Build the prompt
    prompt = f"""Create a minimalist business diagram for the '{model_name}' business model.

STYLE REQUIREMENTS:
- Background: dark charcoal gray (#2a2a2a)
- Primary color: white (#ffffff)
- Accent color: cyan/teal (#00d9b5)
- Secondary color: medium gray (#666666)
- Aesthetic: minimalist, geometric, professional, clean lines, generous whitespace
- NO PHOTOGRAPHS, NO REALISTIC IMAGES, NO 3D RENDERS
- Pure geometric shapes and simple icons only

CONTENT:
Core Concept: {core_concept}

VISUAL STRUCTURE: {visual_structure_config["type"]}

ELEMENTS TO INCLUDE:
Shapes: {", ".join(visual_structure_config["shapes"])}
Icons: {", ".join(visual_structure_config["icons"])}
Arrows: {", ".join(visual_structure_config["arrows"])}
Labels: {", ".join(visual_structure_config["labels"])}
Highlights: {", ".join(visual_structure_config["highlights"])}

TEXT REQUIREMENTS:
- ALL TEXT MUST BE IN ENGLISH
- Use clear, readable sans-serif font
- Text labels should be minimal and strategic
- Main title '{model_name}' at top in white
- Label text in white or cyan for emphasis

COMPOSITION:
- Centered layout with generous whitespace
- Clear visual hierarchy
- Professional business presentation style
- Clean geometric forms
- Minimalist and modern aesthetic

Create a professional business diagram that visually explains the {model_name} model concept using only geometric shapes, simple icons, and minimal text labels."""

    return prompt


def generate_image(client, prompt, model_name, output_path):
    """
    Generate an image using Gemini API and save it.

    Args:
        client: Gemini client instance
        prompt: Image generation prompt
        model_name: Name of the business model (for filename)
        output_path: Directory to save the image

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"Generating image for: {model_name}")
        print(f"Prompt length: {len(prompt)} characters")

        # Generate image using Gemini API
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt],
            config=types.GenerateContentConfig(
                image_config=types.ImageConfig(aspect_ratio="16:9")
            ),
        )

        # Check if image was generated
        if not response.candidates or not response.candidates[0].content.parts:
            print(f"❌ No image generated for {model_name}")
            return False

        # Extract image data using inline_data attribute
        image_data = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                break

        if not image_data:
            print(f"❌ No image data found for {model_name}")
            print(f"   Response parts: {len(response.candidates[0].content.parts)}")
            for i, part in enumerate(response.candidates[0].content.parts):
                if part.text:
                    print(f"   Part {i}: Text - {part.text[:50]}")
                else:
                    print(f"   Part {i}: {type(part)}")
            return False

        # Save image
        filename = f"{model_name.lower().replace(' ', '-').replace('/', '-')}.png"
        filepath = os.path.join(output_path, filename)

        with open(filepath, "wb") as f:
            f.write(image_data)

        print(f"✅ Successfully generated: {filename}")
        return True

    except Exception as e:
        print(f"❌ Error generating image for {model_name}: {str(e)}")
        return False


def main():
    """Main execution function."""

    print("=" * 60)
    print("Business Model Diagram Image Generator")
    print("Using Google Gemini Flash Image 2.5")
    print("=" * 60)
    print()

    # Initialize Gemini client
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Read CSV data
    print(f"Reading CSV from: {CSV_PATH}")
    models_data = []

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            models_data.append(row)

    print(f"Loaded {len(models_data)} business models")
    print()

    # Generate images for specified models
    successful = 0
    failed = 0

    for i in MODELS_TO_GENERATE:
        if i > len(models_data):
            print(
                f"⚠️  Model #{i} out of range (only {len(models_data)} models available)"
            )
            continue

        # Get model data (1-indexed)
        model_data = models_data[i - 1]
        model_name = model_data["Business Model"]
        how_it_works = model_data["How it works?"]

        print(f"\n--- Model #{i}: {model_name} ---")

        # Get visual structure configuration
        visual_config = VISUAL_STRUCTURE_MAP.get(
            model_name,
            {
                "type": "flow_diagram",
                "shapes": ["geometric shapes representing key components"],
                "icons": ["simple icons representing key concepts"],
                "arrows": ["directional arrows showing flow"],
                "labels": ["key concept labels"],
                "highlights": ["important elements in cyan"],
            },
        )

        # Create prompt
        prompt = create_business_model_prompt(model_name, how_it_works, visual_config)

        # Generate image
        success = generate_image(client, prompt, model_name, OUTPUT_DIR)

        if success:
            successful += 1
        else:
            failed += 1

        # Rate limiting: wait 5 seconds between requests
        if i < max(MODELS_TO_GENERATE):
            print("Waiting 5 seconds before next request...")
            time.sleep(5)

    # Summary
    print()
    print("=" * 60)
    print("GENERATION SUMMARY")
    print("=" * 60)
    print(f"Total attempted: {len(list(MODELS_TO_GENERATE))}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"\nImages saved to: {OUTPUT_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
