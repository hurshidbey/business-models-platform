# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project consists of two main components:
1. **Image Generation System**: Generates 60 editorial minimalist illustrations for business models using Google Gemini API
2. **Static Website**: Displays all 60 business models with their images and detailed information

**Core Data Source**: `Context/60 Buisness Models (ENGLISH) - Models.csv`

## Project Structure

```
60 Business/
├── Context/
│   ├── 60 Buisness Models (ENGLISH) - Models.csv  # Source data
│   ├── Fonts/                                      # Nohemi font family (9 weights)
│   └── images/                                     # Generated images (60 PNG files)
├── website/
│   ├── index.html                                  # Homepage grid
│   ├── model.html                                  # Detail page template
│   ├── css/
│   │   ├── style.css                              # Main stylesheet
│   │   └── fonts/                                 # Nohemi fonts (copied)
│   ├── js/
│   │   ├── data.js                                # Business models data (auto-generated)
│   │   └── main.js                                # Dynamic content loader
│   └── images/                                    # Business model images (copied)
├── generate_images.py                             # Main image generator
├── generate_data_js.py                            # CSV → data.js converter
├── IMAGE JSON TEMPLATE.json                       # Visual style template
└── requirements.txt                               # Python dependencies
```

## Common Commands

### Image Generation

```bash
# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set API key
export GEMINI_API_KEY='your-api-key-here'

# Generate all 60 images (range 1-61)
python3 generate_images.py

# Generate Uzbek language images
python3 generate_images_uzbek.py

# Test single model
python3 generate_editorial_style.py
```

### Website Development

```bash
# Regenerate website data from CSV
python3 generate_data_js.py

# Open website locally
open website/index.html

# Copy fonts to website (if needed)
cp Context/Fonts/*.ttf website/css/fonts/

# Copy images to website (if needed)
cp Context/images/*.png website/images/
```

## Architecture & Key Concepts

### 1. Image Generation Pipeline

**Flow**: CSV → Python Script → JSON Template → Gemini API → PNG Images

**Critical API Details**:
- **Package**: `google-genai` (NOT `google-generativeai`)
- **Model**: `gemini-2.5-flash-image` (nicknamed "nano-banana")
- **API Pattern**:
  ```python
  from google import genai
  from google.genai import types
  
  client = genai.Client(api_key=GEMINI_API_KEY)
  response = client.models.generate_content(
      model="gemini-2.5-flash-image",
      contents=[prompt],
      config=types.GenerateContentConfig(
          image_config=types.ImageConfig(aspect_ratio="16:9")
      )
  )
  ```

**Prompt Engineering Strategy**:
- Loads style specifications from `IMAGE JSON TEMPLATE.json`
- Injects business model details (name, how it works) into template
- Enforces NO TEXT policy in prompts
- Uses Editorial Minimalist Illustration style
- 16:9 aspect ratio enforced via API config

**Important Language Best Practice**:
- ✅ **Always write prompts in English** (better LLM performance)
- ✅ Request specific language output when needed (e.g., "ALL TEXT IN UZBEK")
- ❌ Never write the instructions themselves in non-English languages

### 2. Website Architecture

**Type**: Pure static HTML/CSS/JavaScript (no frameworks)

**Data Flow**:
1. CSV → `generate_data_js.py` → `website/js/data.js` (JSON array)
2. Browser loads `index.html` → `main.js` reads `data.js` → Renders cards
3. Click card → Navigate to `model.html?id=X` → `main.js` loads specific model

**Key Design Patterns**:
- **Single Data Source**: `data.js` contains all 60 models as JavaScript array
- **URL Routing**: Query parameter (`?id=1` to `?id=60`) for model details
- **Dynamic Content**: JavaScript populates HTML templates from `data.js`
- **Responsive Grid**: CSS Grid with auto-fill for adaptive columns
- **Image Lazy Loading**: `loading="lazy"` attribute for performance

**CSS Architecture**:
- CSS Custom Properties (`:root`) for design tokens
- Beige color scheme: `--beige-bg: #F4E8D8`
- Typography: Nohemi font family (9 weights loaded via @font-face)
- Mobile-first responsive breakpoints: 768px, 480px

### 3. Visual Style Specifications

**Images Generated Follow**:
- **Style**: Editorial Minimalist Illustration
- **Aspect Ratio**: 16:9 (1344x768 pixels)
- **Color Palette**:
  - Primary: #D44C4C (red), #1E2B47 (navy), #8AB2B8 (teal)
  - Secondary: #E8E8E8, #F2F0EC, #B5B5B5 (grays)
  - Accent: #FFFFFF, #000000
- **NO TEXT POLICY**: Zero words, letters, or numbers in images
- **Composition**: Flat, minimalist, magazine editorial style

**Website Design**:
- **Background**: Warm beige (#F4E8D8)
- **Typography**: Nohemi (Regular 400, Medium 500, Bold 700, etc.)
- **Layout**: Clean grid, generous whitespace
- **Style**: Editorial, professional, minimalist

## Data Structure

**CSV Columns** (60 rows total):
1. `Business Model` - Name (e.g., "Add-On", "Freemium")
2. `How it works?` - Mechanism and value proposition
3. `Where it Comes from?` - Historical origin
4. `Examples` - Real-world companies
5. `Who is it for?` - Target audience/applicability

**JavaScript Data Format** (`data.js`):
```javascript
const businessModels = [
  {
    id: 1,
    name: "Add-On",
    image: "01-add-on.png",
    howItWorks: "...",
    origin: "...",
    examples: "...",
    whoFor: "..."
  },
  // ... 59 more
];
```

## Development Workflows

### Adding New Business Models
1. Update CSV file with new row(s)
2. Run `python3 generate_images.py` (adjust `MODELS_TO_GENERATE` range)
3. Run `python3 generate_data_js.py` to update website data
4. Images auto-named: `{id:02d}-{name-kebab-case}.png`

### Modifying Visual Style
1. Edit `IMAGE JSON TEMPLATE.json` style specifications
2. Regenerate images with updated template
3. JSON sections: color_palette, composition, illustration_technique, text_policy

### Website Content Updates
1. Edit CSV source data
2. Run `python3 generate_data_js.py`
3. Refresh browser (no rebuild needed)

### Changing Website Design
- **Colors**: Edit CSS custom properties in `:root` selector
- **Typography**: Replace fonts in `website/css/fonts/` and update `@font-face`
- **Layout**: Modify grid in `.models-grid` class
- **Responsive**: Adjust `@media` query breakpoints

## Image Generation Best Practices

1. **Rate Limiting**: Include 5-second delays between API requests
2. **Error Handling**: Wrap API calls in try/except, log failures
3. **Aspect Ratio**: Use `types.ImageConfig(aspect_ratio="16:9")` in config
4. **Prompt Length**: Keep prompts detailed but under ~2000 characters
5. **Batch Processing**: Generate in batches (e.g., models 1-10, 11-20) for monitoring
6. **Naming Convention**: `{id:02d}-{model-name-lowercase-hyphenated}.png`

## Important Notes

- **API Key**: Set `GEMINI_API_KEY` environment variable (never commit to git)
- **Python Environment**: Always use virtual environment (`venv/`)
- **Website Deployment**: Static files - can deploy to any web host (no server needed)
- **Browser Compatibility**: Supports all modern browsers (Chrome, Firefox, Safari)
- **Image Format**: PNG output (lossless, ~1.5MB per image)
- **Total Images**: 60 business models × 1 image each = 60 PNG files

## Complete List of 60 Business Models

1. Add-On, 2. Affiliation, 3. Aikido, 4. Auction, 5. Barter, 6. Cash Machine, 7. Cross-Selling, 8. Crowdfunding, 9. Crowdsourcing, 10. Customer Loyalty, 11. Digitalisation, 12. Direct Selling, 13. E-commerce, 14. Experience Selling, 15. Flat Rate, 16. Fractional Ownership, 17. Franchising, 18. Freemium, 19. From Push to Pull, 20. Guaranteed Availability, 21. Hidden Revenue, 22. Ingredient Branding, 23. Integrator, 24. Layer Player, 25. Leverage Customer Data, 26. Licensing, 27. Lock-In, 28. Long Tail, 29. Make More of It, 30. Mass Customisation, 31. No Frills, 32. Open Business, 33. Open Source, 34. Orchestrator, 35. Pay Per Use, 36. Pay What You Want, 37. Peer to Peer, 38. Performance-Based Contracting, 39. Razor and Blade, 40. Rent Instead of Buy, 41. Revenue Sharing, 42. Reverse Engineering, 43. Reverse Innovation, 44. Robin Hood, 45. Self-Service, 46. Shop in Shop, 47. Solution Provider, 48. Subscription, 49. Supermarket, 50. Target the Poor, 51. Trash to Cash, 52. Two-Sided Market, 53. Ultimate Luxury, 54. User Design, 55. White Label, 56. Sensor as a Service, 57. Virtualisation, 58. Object Self-Service, 59. Object as Point of Sale, 60. Prosumer
