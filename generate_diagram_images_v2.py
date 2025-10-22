#!/usr/bin/env python3
"""
Generate business model diagram images using Google Gemini Flash Image 2.5
Based on NEW.json style specifications: minimal line-art diagrams with dark background
Version 2.0 - Refined style with sophisticated visual structures
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

# Style constants from NEW.json
STYLE_CONSTANTS = {
    "background": "#0F1115",  # Very dark blue-black
    "base_color": "#E8E8E8",  # Light gray
    "muted_color": "#6A6F78",  # Medium gray
    "accent_color": "#19E58F",  # Bright green
    "base_stroke": "3px",
    "accent_stroke": "4px",
    "resolution": "2048x1152",
    "aspect_ratio": "16:9",
}

# Visual structure mappings with detailed specifications from NEW.json
VISUAL_STRUCTURE_MAP = {
    "Add-On": {
        "structure": "hub_with_addons",
        "description": "Solid core block at center with detachable modules around it",
        "core": {
            "shape": "large hollow rounded rectangle",
            "stroke": "base",
            "placement": "center",
        },
        "modules": [
            {"name": "baggage", "icon": "briefcase", "placement": "ring_top_left"},
            {"name": "meals", "icon": "tray", "placement": "ring_top_right"},
            {"name": "priority", "icon": "arrow_up", "placement": "ring_right"},
            {"name": "insurance", "icon": "shield", "placement": "ring_bottom_right"},
            {"name": "seat", "icon": "seat_icon", "placement": "ring_bottom_left"},
            {"name": "wifi", "icon": "wifi_signal", "placement": "ring_left"},
        ],
        "arrows": "accent arrows from core to each module showing upsell paths",
        "emphasis": "accent color only on paid modules and revenue arrows",
    },
    "Affiliation": {
        "structure": "two_sided_market",
        "description": "Left and right groups feed a central platform with cross-arrows",
        "core": {
            "shape": "central platform rectangle",
            "stroke": "base",
            "placement": "center",
        },
        "sides": {
            "left": "company/merchant icon",
            "right": "customer icons (3-4 small circles)",
        },
        "arrows": "bidirectional arrows with accent on commission flow",
        "emphasis": "accent color on commission percentage and affiliate relationship",
    },
    "Aikido": {
        "structure": "venn_focus",
        "description": "Two opposing circles with narrow almond-shaped focus highlighted",
        "circles": [
            {"label": "traditional approach", "position": "left", "stroke": "base"},
            {"label": "aikido approach", "position": "right", "stroke": "base"},
        ],
        "overlap": {
            "shape": "almond intersection",
            "highlight": "accent",
            "meaning": "differentiation zone",
        },
        "arrows": "opposing arrows showing contrasting strategies",
        "emphasis": "accent only on the differentiation overlap area",
    },
    "Auction": {
        "structure": "layered_stack",
        "description": "Ascending price bars showing bid progression",
        "layers": [
            {"level": "starting_price", "height": "short", "stroke": "muted"},
            {"level": "bid_1", "height": "medium", "stroke": "base"},
            {"level": "bid_2", "height": "tall", "stroke": "base"},
            {"level": "final_price", "height": "tallest", "stroke": "accent"},
        ],
        "icons": ["gavel symbol at top", "upward arrow showing progression"],
        "emphasis": "accent color only on highest bid and gavel",
    },
    "Barter": {
        "structure": "funnel_bottleneck",
        "description": "Bidirectional exchange flow between two parties",
        "sides": {
            "left": {"shape": "rounded rectangle", "label": "Party A"},
            "right": {"shape": "rounded rectangle", "label": "Party B"},
        },
        "exchange": {
            "arrows": "bidirectional arrows crossing in center",
            "symbols": ["goods icon top", "services icon bottom"],
        },
        "emphasis": "accent color on the exchange arrows and center crossing point",
    },
}


def create_refined_prompt(model_name, how_it_works, visual_config):
    """
    Create a sophisticated image generation prompt based on NEW.json specifications.

    Args:
        model_name: Name of the business model
        how_it_works: Description of how the model works
        visual_config: Visual structure configuration dict

    Returns:
        Detailed prompt string optimized for minimal line-art style
    """

    # Extract core concept (first sentence)
    core_concept = (
        how_it_works.split(".")[0] if "." in how_it_works else how_it_works[:150]
    )

    # Build sophisticated prompt
    prompt = f"""Create a minimal vector line-art diagram for the '{model_name}' business model.

CANVAS & BACKGROUND:
- Background color: very dark blue-black #{STYLE_CONSTANTS["background"][1:]}
- Resolution: {STYLE_CONSTANTS["resolution"]} pixels
- Aspect ratio: {STYLE_CONSTANTS["aspect_ratio"]}
- Padding: 8% margin on all sides
- Generous negative space

COLOR PALETTE (use sparingly):
- Base stroke color: light gray #{STYLE_CONSTANTS["base_color"][1:]} for neutral elements
- Muted color: medium gray #{STYLE_CONSTANTS["muted_color"][1:]} for secondary elements
- Accent color: bright green #{STYLE_CONSTANTS["accent_color"][1:]} ONLY for the key revenue mechanism

VISUAL STRUCTURE: {visual_config["structure"]}
{visual_config["description"]}

CORE CONCEPT: {core_concept}

ELEMENTS TO DRAW:
{json.dumps(visual_config, indent=2)}

STROKE SPECIFICATIONS:
- Base stroke width: 3px (for neutral flows and shapes)
- Accent stroke width: 4px (for monetization arrows only)
- All corners: rounded
- Arrow style: simple solid lines with small triangle heads
- NO gradients, NO 3D effects, NO shadows (except subtle soft shadow if needed)

RENDERING STYLE:
- Clean vector line art only
- Flat matte finish
- No photographs, no realistic images
- No gradients or textures
- Uniform stroke widths throughout
- Consistent geometric icon language
- Thin halftone allowed sparingly if needed

TEXT & LABELS:
- NO text labels preferred
- If absolutely essential: use only 1-3 tiny minimal tags
- Keep diagram visually self-explanatory through shapes and arrows

COMPOSITION RULES:
- Single focal idea at center
- Lots of negative space around elements
- Centered symmetrical layout
- Clear visual hierarchy
- Elements should not touch edges

EMPHASIS RULE (CRITICAL):
- Use accent color #{STYLE_CONSTANTS["accent_color"][1:]} ONLY on:
  * Monetized elements (paid features, revenue streams)
  * Key mechanism arrows (pricing flows, upsell paths)
- Maximum 6-8 accent elements
- Everything else uses base color #{STYLE_CONSTANTS["base_color"][1:]}

NEGATIVE CONSTRAINTS (exclude these):
- No brand logos or watermarks
- No UI chrome or interface elements
- No photographs or people images
- No paragraphs of text or long labels
- No realistic rendering or 3D effects
- No complex gradients or textures

FINAL OUTPUT:
A clean, professional, minimalist vector diagram on dark background that instantly communicates the '{model_name}' business model concept through simple geometric shapes, strategic use of accent color, and clear directional arrows."""

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
        print(f"\n{'=' * 60}")
        print(f"Generating: {model_name}")
        print(f"{'=' * 60}")
        print(f"Prompt length: {len(prompt)} characters")
        print(
            f"Structure: {VISUAL_STRUCTURE_MAP.get(model_name, {}).get('structure', 'default')}"
        )

        # Generate image using Gemini API
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="16:9"),
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
                    print(f"   Part {i}: Text - {part.text[:80]}")
            return False

        # Save image
        filename = f"{model_name.lower().replace(' ', '-').replace('/', '-')}.png"
        filepath = os.path.join(output_path, filename)

        with open(filepath, "wb") as f:
            f.write(image_data)

        file_size = len(image_data) / 1024  # KB
        print(f"✅ Successfully generated: {filename} ({file_size:.0f} KB)")
        return True

    except Exception as e:
        print(f"❌ Error generating image for {model_name}: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main execution function."""

    print("\n" + "=" * 70)
    print("  BUSINESS MODEL DIAGRAM GENERATOR V2.0")
    print("  Minimal Line-Art Style | Google Gemini Flash Image 2.5")
    print("=" * 70)

    print(f"\nStyle Profile:")
    print(f"  Background: Dark #{STYLE_CONSTANTS['background'][1:]}")
    print(f"  Accent: Bright Green #{STYLE_CONSTANTS['accent_color'][1:]}")
    print(f"  Resolution: {STYLE_CONSTANTS['resolution']}")
    print(f"  Aesthetic: Clean vector line-art, generous negative space")
    print()

    # Initialize Gemini client
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Read CSV data
    print(f"Reading data from: {CSV_PATH}")
    models_data = []

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            models_data.append(row)

    print(f"Loaded {len(models_data)} business models\n")

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

        # Get visual structure configuration
        visual_config = VISUAL_STRUCTURE_MAP.get(
            model_name,
            {
                "structure": "hub_with_addons",
                "description": "Generic diagram with core concept and supporting elements",
                "emphasis": "accent on monetization mechanism",
            },
        )

        # Create prompt
        prompt = create_refined_prompt(model_name, how_it_works, visual_config)

        # Generate image
        success = generate_image(client, prompt, model_name, OUTPUT_DIR)

        if success:
            successful += 1
        else:
            failed += 1

        # Rate limiting: wait 5 seconds between requests
        if i < max(MODELS_TO_GENERATE):
            print("\n⏱️  Waiting 5 seconds before next request...")
            time.sleep(5)

    # Summary
    print("\n" + "=" * 70)
    print("  GENERATION SUMMARY")
    print("=" * 70)
    print(f"  Total attempted: {len(list(MODELS_TO_GENERATE))}")
    print(f"  ✅ Successful: {successful}")
    print(f"  ❌ Failed: {failed}")
    print(f"\n  Images saved to: {OUTPUT_DIR}/")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
