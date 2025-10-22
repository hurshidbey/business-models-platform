# 60 Business Models Image Generator

Generate infographic images for 60 business models using Google Gemini API (Imagen).

## Setup

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Get Gemini API Key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create or select a project
   - Generate an API key

3. **Set up environment variables:**
   ```bash
   export GEMINI_API_KEY='your-api-key-here'
   ```
   
   Or create a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

## Usage

### Test API Connection
```bash
python3 test_gemini.py
```

### Generate Images
```bash
# Generate images for business models 1-10
python3 generate_images.py
```

## Project Structure

```
60 Business/
├── Context/
│   └── 60 Buisness Models (ENGLISH) - Models.csv  # Source data
├── images/                                          # Generated images
├── IMAGE JSON TEMPLATE.json                        # Visual style template
├── generate_images.py                              # Main generator script
├── test_gemini.py                                  # API test script
├── requirements.txt                                # Python dependencies
├── CLAUDE.md                                       # Claude Code guidance
└── README.md                                       # This file
```

## Visual Style

All generated images follow a consistent style:
- **Colors:** Black (#000000), White (#FFFFFF), Yellow (#FFD42A) only
- **Layout:** Horizontal left-to-right flow diagram
- **Style:** Minimalist line art with geometric shapes
- **Format:** 16:9 aspect ratio (wide format)

## Business Models (60 Total)

1. Add-On
2. Affiliation
3. Aikido
... (see CLAUDE.md for full list)

## Notes

- Images are generated using Gemini's Imagen model (nano-banana: gemini-2.5-flash-image)
- Rate limiting: 5 seconds between requests
- Output format: PNG, 16:9 aspect ratio (1344x768 pixels)
- Naming convention: `{id:02d}-{model-name}.png` (English) or `{id:02d}-{model-name}-uz.png` (Uzbek)

## Important: Language Instructions Best Practice

**When generating images in non-English languages (like Uzbek):**
- ✅ **DO:** Write all instructions and prompts in English
- ✅ **DO:** Request the model to generate text/labels in the target language
- ❌ **DON'T:** Write the instructions themselves in the target language

**Why?** LLMs like Gemini perform significantly better with English instructions. The model can still generate text in any language you request - you just need to specify it in the prompt.

**Example:**
```python
# ❌ BAD - Instructions in Uzbek
prompt = "Qora, oq va sariq ranglardan foydalaning..."

# ✅ GOOD - Instructions in English, requesting Uzbek output
prompt = "Use only black, white, and yellow colors... CRITICAL: ALL TEXT AND LABELS MUST BE IN UZBEK LANGUAGE!"
```
