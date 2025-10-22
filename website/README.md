# 60 Business Models Website

A clean, minimalist website showcasing 60 different business models with editorial minimalist illustrations.

## Design Specifications

- **Background**: Warm beige (#F4E8D8)
- **Typography**: Nohemi font family (all weights included)
- **Layout**: Responsive grid layout (3-4 columns on desktop, 1-2 on mobile)
- **Images**: 16:9 editorial minimalist illustrations
- **Style**: Clean, magazine-like aesthetic

## File Structure

```
website/
├── index.html              # Homepage with grid of all 60 models
├── model.html              # Detail page template for individual models
├── css/
│   ├── style.css          # Main stylesheet
│   └── fonts/             # Nohemi font files (9 weights)
├── js/
│   ├── data.js            # All 60 business models data
│   └── main.js            # Main JavaScript for dynamic content
├── images/                # 60 business model images (16:9 format)
└── README.md              # This file
```

## Features

### Homepage (index.html)
- Grid display of all 60 business models
- Each card shows:
  - Business model illustration
  - Model number
  - Model name
  - Brief description (first 150 characters)
- Click any card to view full details
- Fully responsive design

### Detail Page (model.html)
- Large hero image (16:9 format)
- Complete information:
  - How it works
  - Where it comes from (historical origin)
  - Examples (real-world companies)
  - Who is it for (target audience/use cases)
- Navigation:
  - Previous/Next model buttons
  - Back to all models link
- Dynamic URL routing (?id=1-60)

## How to Use

1. **Open the website**: Simply open `index.html` in any modern web browser
2. **Browse models**: Scroll through the grid to see all 60 business models
3. **View details**: Click any model card to see complete information
4. **Navigate**: Use Previous/Next buttons to browse through models sequentially

## Technical Details

- **Pure HTML/CSS/JavaScript** - No frameworks required
- **Responsive Design** - Mobile-friendly with breakpoints at 768px and 480px
- **Dynamic Content** - JavaScript loads content from data.js
- **Lazy Loading** - Images load as needed for better performance
- **Clean URLs** - Model pages use query parameters (?id=X)

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Data Source

All business model information is sourced from:
`Context/60 Buisness Models (ENGLISH) - Models.csv`

Images generated using:
- Google Gemini API (gemini-2.5-flash-image model)
- Editorial Minimalist Illustration style
- 16:9 aspect ratio (1344x768 pixels)
- NO TEXT policy (pure visual storytelling)

## Customization

### To update business model data:
1. Edit `Context/60 Buisness Models (ENGLISH) - Models.csv`
2. Run `python3 generate_data_js.py` to regenerate `js/data.js`

### To change colors:
Edit CSS variables in `css/style.css`:
```css
:root {
  --beige-bg: #F4E8D8;
  --black: #1A1A1A;
  /* etc. */
}
```

### To change typography:
Replace font files in `css/fonts/` and update `@font-face` declarations in `css/style.css`

## Performance

- Optimized CSS with minimal specificity
- Lazy loading for images
- Minimal JavaScript (no heavy frameworks)
- Total page weight: ~50KB (without images)
- Images: ~1.5MB each (PNG format)

## Future Enhancements

Potential additions:
- Search functionality
- Filter by category/industry
- Favorites/bookmarking
- Print-friendly views
- Social sharing buttons
- Multi-language support

---

**Built with**: HTML5, CSS3, Vanilla JavaScript  
**Design**: Editorial Minimalist Style  
**Font**: Nohemi (9 weights)  
**Year**: 2025
