#!/usr/bin/env python3
"""
Regenerate Crowdfunding image with updated metaphor
Removes cathedral/church elements, uses collective building metaphor instead
"""

import os
import json
from google import genai
from google.genai import types

# API Configuration
GEMINI_API_KEY = "AIzaSyAcSvcL9TpZ3_2Q00srcEBvkC-veQ0COr0"
MODEL_NAME = "gemini-2.5-flash-image"

# File paths
OUTPUT_DIR = "newImagesForEBOOK"
STYLE_JSON = "Context/IMAGES FOR PFD/ImageStyle.json"

# Load style specifications
with open(STYLE_JSON, "r") as f:
    style_data = json.load(f)
    CANVAS = style_data["canvas"]
    PALETTE = style_data["palette"]
    STYLE = style_data["style"]
    TEXT_POLICY = style_data["text_policy"]

# Updated Crowdfunding concept - NO cathedral/church elements
CROWDFUNDING_CONCEPT = {
    "name": "Crowdfunding",
    "essence": "Many small contributions manifest a singular vision",
    "metaphor": "The Collective Assembly",
    "scene": "A large ambitious project (represented as a modern geometric structure or product) rises in the center—half-complete, showing its framework. Around its base, hundreds of tiny human figures form a circle, each person holding or offering a small glowing cube, coin, or brick representing their contribution. As these contributions connect with the central project, they solidify and add to its construction. Streams of light flow from each contributor toward the center, converging like tributaries. A progress indicator (simple bar or circular gauge) shows the funding goal at 75% completion. Small reward icons or tokens float back down to contributors as acknowledgment. The scene suggests democratic creation, collective power, and shared vision—but uses modern, secular imagery of community building, NOT religious architecture.",
    "perspective": "wide-angle view showing the crowd below and the growing project above, emphasizing collective action",
}


def create_prompt(concept, canvas, palette, style, text_policy):
    """Create prompt for Crowdfunding image without religious imagery."""

    name = concept["name"]
    essence = concept["essence"]
    metaphor = concept["metaphor"]
    scene = concept["scene"]
    perspective = concept["perspective"]

    prompt = f"""Create an editorial magazine cover illustration for "{name}" business model.

CORE CONCEPT: {essence}
VISUAL METAPHOR: {metaphor}

SCENE DESCRIPTION:
{scene}

PERSPECTIVE: {perspective}

CRITICAL: NO cathedral, NO church, NO religious architecture, NO religious symbols. Use modern, secular, community-building imagery only. Think startup, product, modern project, NOT religious structures.

CANVAS & FORMAT:
- Aspect ratio: {canvas["aspect_ratio"]} square ({canvas["resolution"]})
- Background: Pure white #{canvas["background_hex"][1:]}
- Padding: {canvas["padding_pct"]}% margins

COLOR PALETTE:
- Primary: Black #{palette["primary_hex"][1:]} for main elements
- Accent: Golden yellow #{palette["accent_hex"][1:]} for 2-3 focal points only
- Neutral: Light grey #{palette["neutral_hex"][1:]} for shadows

RENDERING STYLE:
- {style["rendering"]["texture"]} with {style["rendering"]["finish"]} finish
- {style["rendering"]["lighting"]}
- NO drop shadows, NO gradients
- Flat vector illustration

HALFTONE (sparingly):
- {style["halftone"]["pattern_type"]}, {style["halftone"]["dot_min_px"]}-{style["halftone"]["dot_max_px"]}px
- {style["halftone"]["angle_deg"]}° angle, {style["halftone"]["density"]} density
- Apply ONLY to {", ".join(style["halftone"]["placement"])}

LINE WORK:
- {style["lines"]["weight_px"]}px {style["lines"]["style"]} strokes
- {style["lines"]["corner_type"]} corners

COMPOSITION:
- {style["composition"]["layout"]}
- {style["composition"]["balance"]}
- {style["composition"]["spacing_pct"]}% spacing

TEXT POLICY - CRITICAL:
✗ NO titles, subtitles, or watermarks
✗ NO text on background
✓ Maximum {text_policy["max_characters_total"]} characters total (prefer ZERO)
✓ Text ONLY on tiny labels if essential
✓ Prefer pure visual communication

REQUIREMENTS:
1. White background, black primary, golden accents on key points only
2. Square 1:1 format
3. NO religious imagery (no cathedrals, churches, crosses, steeples)
4. Use modern, secular project/product/startup imagery
5. Show collective community action, many people contributing
6. Progress indicator showing 75% funded
7. Contributions flowing from crowd to central project
8. Rewards/tokens flowing back to contributors
9. NO titles or watermarks
10. Clean vector style - The Economist aesthetic

VALIDATION:
□ NO cathedral or church elements present?
□ Modern, secular imagery used?
□ White background, black primary elements?
□ Golden accents on 2-3 focal points only?
□ NO titles, subtitles, watermarks?
□ Square 1:1 aspect ratio?
□ Visual metaphor clear without text?

OUTPUT:
Sophisticated editorial illustration showing collective crowdfunding through modern, secular imagery of community building and shared vision. NO religious architecture."""

    return prompt


def generate_image(prompt, output_path):
    """Generate and save image."""

    print(f"\n{'=' * 70}")
    print(f"REGENERATING: Crowdfunding (NO cathedral elements)")
    print(f"{'=' * 70}")
    print(f"Prompt length: {len(prompt)} characters")

    client = genai.Client(api_key=GEMINI_API_KEY)

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="1:1"),
            ),
        )

        if not response.candidates or not response.candidates[0].content.parts:
            print(f"❌ No image generated")
            return False

        image_data = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                break

        if not image_data:
            print(f"❌ No image data found")
            return False

        filename = "crowdfunding.png"
        filepath = os.path.join(output_path, filename)

        with open(filepath, "wb") as f:
            f.write(image_data)

        file_size = len(image_data) / 1024
        print(f"✅ Successfully regenerated: {filename} ({file_size:.0f} KB)")
        print(f"✓ NO cathedral elements")
        print(f"✓ Modern, secular imagery")
        print(f"✓ Community building metaphor")
        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main execution."""

    print("\n" + "=" * 70)
    print("  REGENERATE CROWDFUNDING IMAGE")
    print("  Remove Cathedral | Modern Secular Imagery")
    print("=" * 70)
    print()

    prompt = create_prompt(CROWDFUNDING_CONCEPT, CANVAS, PALETTE, STYLE, TEXT_POLICY)
    success = generate_image(prompt, OUTPUT_DIR)

    if success:
        print("\n✅ Crowdfunding image regenerated successfully")
        print("   - NO cathedral or church elements")
        print("   - Modern community building metaphor")
        print("   - Secular, contemporary imagery")
    else:
        print("\n❌ Failed to regenerate image")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
