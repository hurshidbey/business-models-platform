#!/usr/bin/env python3
"""
Generate editorial illustrations for business models - Version 2
Combines ImagineConcepts.md scene descriptions with ImageStyle.json v1.1 specifications
Enforces strict text policy: NO titles, NO watermarks, minimal text
Uses Google Gemini Flash Image 2.5
"""

import os
import json
import time
from google import genai
from google.genai import types

# API Configuration
GEMINI_API_KEY = "AIzaSyAcSvcL9TpZ3_2Q00srcEBvkC-veQ0COr0"
MODEL_NAME = "gemini-2.5-flash-image"

# File paths
OUTPUT_DIR = "newImagesForEBOOK"
STYLE_JSON = "Context/IMAGES FOR PFD/ImageStyle.json"

# Models to generate (1-10 for now)
MODELS_TO_GENERATE = range(1, 11)

# Load style specifications
with open(STYLE_JSON, "r") as f:
    style_data = json.load(f)
    CANVAS = style_data["canvas"]
    PALETTE = style_data["palette"]
    STYLE = style_data["style"]
    TEXT_POLICY = style_data["text_policy"]

# Editorial concepts for first 10 models
EDITORIAL_CONCEPTS = {
    1: {
        "name": "Add-On",
        "essence": "A stripped-down core becomes expensive through optional extras",
        "metaphor": "The Assembly Line of Desire",
        "scene": "A stark, minimalist product (a simple geometric chair or car skeleton) sits in the center, rendered in cold steel blue. Surrounding it in a perfect ring are 8-10 floating modules—plush cushions, chrome armrests, decorative panels—each glowing with warm golden light and casting soft shadows. Fine, delicate threads connect the core to each add-on, creating a web of temptation. Small price tags dangle from invisible threads above each optional module, their numbers progressively increasing. The composition suggests a spider's web of consumer desire.",
        "perspective": "slightly elevated, looking down at 30 degrees, emphasizing the radiating pattern",
    },
    2: {
        "name": "Affiliation",
        "essence": "Invisible intermediaries harvest commissions from connections",
        "metaphor": "The Network of Invisible Hands",
        "scene": "A vast constellation of glowing nodes connected by luminous threads against a deep indigo background. At the center, a bright company star. Around it, dozens of smaller affiliate satellites—blogs, websites, influencers—represented as smaller orbs of varying sizes. Some threads are dormant (pale blue), others are active (electric green), pulsing with transaction energy. Small coins flow along the active threads like trains on rails, splitting at each node with a percentage continuing to the affiliate.",
        "perspective": "three-quarter angle, as if floating in this commercial constellation",
    },
    3: {
        "name": "Aikido",
        "essence": "Using a competitor's strength against them through strategic opposition",
        "metaphor": "The Redirected Force",
        "scene": "Two massive geometric forms face each other in a tense composition. On the left, a towering, monolithic rectangle in aggressive red, pushing forward with force lines suggesting immense momentum. On the right, a smaller, elegant curved form in cool cyan, positioned at an angle that deflects the red giant's energy. The red force's momentum creates visible wind trails that curve around the blue form, redirecting into empty space. A single pivot point glows with energy, the fulcrum of the reversal.",
        "perspective": "profile view, emphasizing the deflection angle and energy transfer",
    },
    4: {
        "name": "Auction",
        "essence": "Ascending bids determine value through competitive desire",
        "metaphor": "The Ladder of Ascending Value",
        "scene": "A vertical composition showing a series of platforms rising like steps toward the sky, each platform representing a bid level. On the bottom step, multiple hands reach upward (muted grey). With each ascending level, fewer hands remain (gradually warming in color from grey to amber to gold), until at the top platform, a single golden hand triumphantly holds a glowing object. A golden gavel descends from above like a judge's decision.",
        "perspective": "low angle looking up, emphasizing the vertical journey and the apex of victory",
    },
    5: {
        "name": "Barter",
        "essence": "Direct exchange of value without monetary intermediation",
        "metaphor": "The Crossing of Reciprocal Gifts",
        "scene": "Two open hands reach toward each other from opposite sides of the frame, meeting at the center point in perfect symmetry. The left hand offers a geometric shape representing goods (a cube with product textures), the right hand offers a different form representing services (flowing ribbons of capability). As they meet, the objects begin to merge and exchange properties. No money exists in this scene, only pure exchange. Arrows of value flow bidirectionally, perfectly balanced.",
        "perspective": "eye level, straight on, emphasizing the symmetrical exchange and equality",
    },
    6: {
        "name": "Cash Machine",
        "essence": "Cash flows in before it flows out, creating financial leverage",
        "metaphor": "The Reversed Waterfall",
        "scene": "A surreal scene where water (representing cash) flows upward, defying gravity. At the bottom, multiple streams from customers converge into a central pool (the company's reserves). From this pool, a single, thinner stream flows upward toward suppliers, but significantly delayed in time. The pool in the center glows with accumulated energy, growing larger while the outward flow remains thin and slow. Clock faces float in the stream, showing the time gap between receiving and paying.",
        "perspective": "side view showing the full vertical flow, emphasizing the reversed directionality",
    },
    7: {
        "name": "Cross-Selling",
        "essence": "One purchase opens doors to many related purchases",
        "metaphor": "The Branching Tree of Needs",
        "scene": "A single strong trunk rises from the bottom (the core product), rendered in solid earth tones. From this trunk, multiple branches extend in all directions, each branch bearing different fruits—representing complementary products and services. A customer figure stands at the base, reaching up, and where their hand touches the trunk, the entire tree lights up with possibility—branches illuminate in sequence. Small price tags on golden chains dangle from each fruit. Roots visible below ground mirror the branches above.",
        "perspective": "slight low angle, looking up into the canopy of opportunities",
    },
    8: {
        "name": "Crowdfunding",
        "essence": "Many small contributions manifest a singular vision",
        "metaphor": "The Cathedral Built by Hands",
        "scene": "A magnificent structure rises in the center—half-built, transparent, showing its skeletal framework. Around its base, hundreds of tiny figures (the crowd) reach upward, each figure holding a small glowing brick, tile, or beam. As these offerings connect with the structure, they solidify and add to the growing edifice. Streams of light from each contributor converge on the central building. A progress indicator shows the funding goal, currently three-quarters full. Small reward tokens float back down to contributors.",
        "perspective": "wide-angle view showing both the multitude below and the soaring structure above",
    },
    9: {
        "name": "Crowdsourcing",
        "essence": "External minds solve internal problems for recognition and reward",
        "metaphor": "The Problem Lighthouse",
        "scene": "A tall, luminous lighthouse stands at the center, its beacon casting a wide circular beam across a dark sea. The beam is actually a question radiating outward. In the surrounding darkness, thousands of small boats (individual contributors) navigate toward the light, each carrying a different proposed solution, represented by unique geometric shapes or glowing ideas. A few boats have reached the lighthouse dock, their solutions being lifted by a crane into the tower. The sea is studded with small reward tokens.",
        "perspective": "high angle view, looking down on the lighthouse and its surrounding flotilla",
    },
    10: {
        "name": "Customer Loyalty",
        "essence": "Rewards bind customers through accumulated value and emotional connection",
        "metaphor": "The Chain of Golden Links",
        "scene": "A customer figure stands at the left, connected to a company symbol at the right by an elegant chain made of mixed materials: some links are gold (rewards), some are silver (points), some are platinum (exclusive status). With each transaction, a pulse of light along the chain adds a new link. Around the customer's feet, competitor offers lie ignored. Small benefits (free coffee, upgrades, early access) hang from the chain like charms on a bracelet. The company end of the chain has roots growing deep into the ground.",
        "perspective": "eye level, showing the full connection and emphasizing the beauty of the chain",
    },
}


def create_editorial_prompt(model_number, concept, canvas, palette, style, text_policy):
    """
    Create a sophisticated prompt with strict text policy enforcement.
    """

    name = concept["name"]
    essence = concept["essence"]
    metaphor = concept["metaphor"]
    scene = concept["scene"]
    perspective = concept["perspective"]

    # Build comprehensive prompt
    prompt = f"""Create an editorial magazine cover illustration for "{name}" business model.

CORE CONCEPT: {essence}
VISUAL METAPHOR: {metaphor}

SCENE DESCRIPTION:
{scene}

PERSPECTIVE: {perspective}

CANVAS & FORMAT:
- Aspect ratio: {canvas["aspect_ratio"]} square format ({canvas["resolution"]})
- Background: Pure white #{canvas["background_hex"][1:]}
- Padding: {canvas["padding_pct"]}% margin on all sides for breathing room

COLOR PALETTE (Use strictly):
- Primary: Black #{palette["primary_hex"][1:]} for main elements, outlines, solid shapes
- Accent: Golden yellow #{palette["accent_hex"][1:]} ONLY for 2-3 key focal elements
- Neutral: Light grey #{palette["neutral_hex"][1:]} for shadows and subtle elements

RENDERING STYLE:
- {style["rendering"]["texture"]} with {style["rendering"]["finish"]} finish
- Lighting: {style["rendering"]["lighting"]} (no realistic shadows)
- Drop shadows: {"Disabled" if not style["rendering"]["drop_shadows"] else "Enabled"}
- Gradients: {"Disabled" if not style["rendering"]["gradients"] else "Enabled"}
- Pure flat vector illustration with minimal depth

HALFTONE TEXTURE (Apply sparingly):
- Pattern: {style["halftone"]["pattern_type"]}
- Dot size range: {style["halftone"]["dot_min_px"]}-{style["halftone"]["dot_max_px"]}px
- Angle: {style["halftone"]["angle_deg"]}°
- Density: {style["halftone"]["density"]}
- Tint: #{style["halftone"]["tint_hex"][1:]}
- Apply ONLY to: {", ".join(style["halftone"]["placement"])}
- Keep subtle - not a dominant visual element

LINE WORK:
- Weight: {style["lines"]["weight_px"]}px consistent throughout
- Style: {style["lines"]["style"]} strokes
- Corners: {style["lines"]["corner_type"]}
- Arrows (if needed): {style["lines"]["arrow_type"]}

COMPOSITION:
- Layout: {style["composition"]["layout"]} arrangement
- Balance: {style["composition"]["balance"]}
- Depth: {style["composition"]["object_depth"]}
- Spacing: {style["composition"]["spacing_pct"]}% between elements
- Anchor to center: {style["composition"]["central_anchor"]}

TEXT POLICY - CRITICAL:
✗ NO titles anywhere on the image
✗ NO subtitles anywhere on the image
✗ NO watermarks or signatures
✗ NO text on background
✓ Maximum {text_policy["max_characters_total"]} characters total (prefer ZERO)
✓ Text ONLY allowed: tiny labels on tokens/arrows if absolutely essential
✓ If any text: {text_policy["allowed_languages"]} only, spelled correctly, factually accurate
✓ Font: {text_policy["font_family_hint"]}, {text_policy["font_weight"]} weight
✓ PREFER pure visual communication - use symbols and metaphors instead of words

CRITICAL REQUIREMENTS:
1. White background with black primary elements
2. Golden yellow accent on 2-3 focal points ONLY
3. Halftone dots on side faces and shadows ONLY (not everywhere)
4. ZERO text preferred (max 20 chars if absolutely necessary)
5. NO titles, NO watermarks anywhere
6. Square 1:1 format ({canvas["aspect_ratio"]})
7. NO gradients, NO realistic rendering, NO photographs
8. Clean vector - think The Economist editorial style
9. Visual metaphor communicates concept without text
10. Generous white space, clean composition

VALIDATION:
□ Background is pure white?
□ Primary elements are black with golden accents on key points only?
□ Halftone used sparingly on shadows/sides only?
□ Total text is 0-20 characters (ideally zero)?
□ NO titles, subtitles, or watermarks present?
□ Any text is spelled correctly and accurate?
□ Composition is clean with {canvas["padding_pct"]}% margins?
□ Visual metaphor is clear without text?
□ Square 1:1 aspect ratio?

OUTPUT:
A sophisticated editorial illustration communicating "{name}" through pure visual metaphor, minimal/zero text, clean vector style on white background, suitable for business book chapter cover."""

    return prompt


def generate_image(client, prompt, model_name, output_path):
    """Generate image using Gemini API and save it."""
    try:
        print(f"\n{'=' * 70}")
        print(f"GENERATING: {model_name}")
        print(f"{'=' * 70}")
        print(f"Prompt length: {len(prompt)} characters")

        # Generate image with 1:1 aspect ratio
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="1:1"),
            ),
        )

        # Check response
        if not response.candidates or not response.candidates[0].content.parts:
            print(f"❌ No image generated for {model_name}")
            return False

        # Extract image data
        image_data = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                break

        if not image_data:
            print(f"❌ No image data found for {model_name}")
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
    print("  EDITORIAL BUSINESS MODEL ILLUSTRATIONS v2")
    print("  Clean Vector | NO Titles | Minimal Text")
    print("=" * 70)

    print(f"\nStyle Profile:")
    print(f"  Format: {CANVAS['aspect_ratio']} square ({CANVAS['resolution']})")
    print(f"  Background: White #{CANVAS['background_hex'][1:]}")
    print(f"  Primary: Black #{PALETTE['primary_hex'][1:]}")
    print(f"  Accent: Golden #{PALETTE['accent_hex'][1:]}")
    print(
        f"  Text Policy: {TEXT_POLICY['allowed']} (max {TEXT_POLICY['max_characters_total']} chars)"
    )
    print(f"  Titles: {'NO' if not TEXT_POLICY['titles'] else 'YES'}")
    print(f"  Watermarks: {'NO' if not TEXT_POLICY['watermarks'] else 'YES'}")
    print()

    # Initialize Gemini client
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Generate images
    successful = 0
    failed = 0

    for i in MODELS_TO_GENERATE:
        if i not in EDITORIAL_CONCEPTS:
            print(f"⚠️  Model #{i} concept not found")
            continue

        concept = EDITORIAL_CONCEPTS[i]
        model_name = concept["name"]

        # Create prompt with all specifications
        prompt = create_editorial_prompt(
            i, concept, CANVAS, PALETTE, STYLE, TEXT_POLICY
        )

        # Generate image
        success = generate_image(client, prompt, model_name, OUTPUT_DIR)

        if success:
            successful += 1
        else:
            failed += 1

        # Rate limiting
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
    print("  Format: 1:1 square, NO titles, minimal text")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
