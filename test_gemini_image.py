#!/usr/bin/env python3
"""
Test script to debug Gemini API image generation response
"""

from google import genai
from google.genai import types
import json

GEMINI_API_KEY = "AIzaSyAcSvcL9TpZ3_2Q00srcEBvkC-veQ0COr0"
MODEL_NAME = "gemini-2.5-flash-image"

# Initialize client
client = genai.Client(api_key=GEMINI_API_KEY)

# Simple test prompt
prompt = """Create a minimalist business diagram on dark charcoal background (#2a2a2a).

Draw a white circle in the center labeled 'Core Product'.
Draw 6 cyan rectangular boxes around it connected by white lines.
Label each box 'Add-On 1', 'Add-On 2', etc.
Add dollar signs showing increasing prices.

16:9 aspect ratio. Minimalist geometric style. Clean professional design."""

print("Sending request to Gemini API...")
print(f"Model: {MODEL_NAME}")
print(f"Prompt: {prompt[:100]}...")
print()

try:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt],
        config=types.GenerateContentConfig(
            image_config=types.ImageConfig(aspect_ratio="16:9")
        ),
    )

    print("Response received!")
    print(f"Type: {type(response)}")
    print(f"Has candidates: {hasattr(response, 'candidates')}")

    if hasattr(response, "candidates"):
        print(f"Number of candidates: {len(response.candidates)}")

        if response.candidates:
            candidate = response.candidates[0]
            print(f"Candidate type: {type(candidate)}")
            print(f"Has content: {hasattr(candidate, 'content')}")

            if hasattr(candidate, "content"):
                content = candidate.content
                print(f"Content type: {type(content)}")
                print(f"Has parts: {hasattr(content, 'parts')}")

                if hasattr(content, "parts"):
                    print(f"Number of parts: {len(content.parts)}")

                    for i, part in enumerate(content.parts):
                        print(f"\nPart {i}:")
                        print(f"  Type: {type(part)}")
                        print(
                            f"  Dir: {[attr for attr in dir(part) if not attr.startswith('_')]}"
                        )

                        # Check for different possible attributes
                        if hasattr(part, "image"):
                            print(f"  Has 'image' attribute: {part.image}")
                        if hasattr(part, "inline_data"):
                            print(f"  Has 'inline_data' attribute: {part.inline_data}")
                        if hasattr(part, "data"):
                            print(
                                f"  Has 'data' attribute (length): {len(part.data) if part.data else 0}"
                            )
                        if hasattr(part, "mime_type"):
                            print(f"  MIME type: {part.mime_type}")
                        if hasattr(part, "text"):
                            print(f"  Text: {part.text[:100] if part.text else None}")

    # Try to access response differently
    print("\n\nTrying alternative access methods:")
    print(
        f"Response dict keys: {response.__dict__.keys() if hasattr(response, '__dict__') else 'N/A'}"
    )

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
