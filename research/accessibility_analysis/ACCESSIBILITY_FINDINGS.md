# Accessibility Analysis: Anthropic Design System

**Date:** October 31, 2025
**Analyst:** Alden Weaver
**Tools:** Manual contrast calculation, WCAG 2.1 standards

## Executive Summary

During implementation of Anthropic's design system for this portfolio, **critical accessibility issues were discovered in Anthropic's primary accent color (Clay #d97757)**. The color fails WCAG 2.1 Level AA contrast requirements when used on light backgrounds.

## Findings

### ❌ CRITICAL: Clay Accent Color Fails WCAG Standards

**Issue:** Anthropic's primary accent color (Clay #d97757) does not meet WCAG 2.1 Level AA contrast requirements for normal text.

**Test Results:**

| Color Combination | Contrast Ratio | WCAG Result | Status |
|-------------------|----------------|-------------|--------|
| Clay on Ivory (#d97757 on #faf9f5) | **2.96:1** | FAIL | ❌ |
| Clay on White (#d97757 on #ffffff) | **3.12:1** | AA Large Only | ⚠️ |
| Cloud Medium on Ivory (#b0aea5 on #faf9f5) | **2.11:1** | FAIL | ❌ |

**WCAG Requirements:**
- Normal text: 4.5:1 minimum (AA), 7:1 (AAA)
- Large text (18pt+ or 14pt+ bold): 3:1 minimum

**Impact:**
- Clay can ONLY be used for large text (18pt+) or decorative elements
- Cannot be used for body text, small headings, or critical UI text
- Affects users with:
  - Low vision
  - Color blindness
  - Older adults with age-related vision decline
  - Anyone using screens in bright lighting conditions

### ✅ PASS: Core Text Colors Meet Standards

**Test Results:**

| Color Combination | Contrast Ratio | WCAG Level | Status |
|-------------------|----------------|------------|--------|
| Slate on Ivory (#141413 on #faf9f5) | **17.50:1** | AAA | ✅ |
| Slate on White (#141413 on #ffffff) | **18.43:1** | AAA | ✅ |
| Slate Light on Ivory (#5e5d59 on #faf9f5) | **6.26:1** | AA | ✅ |
| Ivory on Slate (#faf9f5 on #141413) | **17.50:1** | AAA | ✅ |
| Ivory on Slate Medium (#faf9f5 on #3d3d3a) | **10.34:1** | AAA | ✅ |

**Good News:** Anthropic's core text colors (Slate/Ivory) are excellent and exceed AAA standards.

## Comparison: Original vs Anthropic Colors

### Original Portfolio Colors (Before Redesign)

The accessibility report from the docs clone showed:
- Primary (#0E0E0E) on Light Background: **19.30:1** - WCAG AAA ✅
- Tan (#D4A27F) on Dark Background: **8.62:1** - WCAG AAA ✅

### Anthropic Colors (After Redesign)

- Slate (#141413) on Ivory (#faf9f5): **17.50:1** - WCAG AAA ✅
- **Clay (#d97757) on Ivory (#faf9f5): 2.96:1 - FAILS WCAG** ❌

**Key Insight:** While both color systems use warm tones, the original tan (#D4A27F) was lighter and passed accessibility standards, while Anthropic's Clay (#d97757) is too similar in luminance to the background.

## How We Mitigated This in the Portfolio

### Safe Uses of Clay:
1. **Buttons** - Large clickable areas with sufficient size
2. **Large headings** - 24px+ font size where 3:1 ratio is acceptable
3. **Borders and accents** - Decorative elements that don't convey critical information
4. **Hover states** - Secondary indicators, not primary information

### Avoided Uses:
1. ❌ Body text
2. ❌ Small labels or descriptions
3. ❌ Critical links without underlines
4. ❌ Icon-only buttons without labels

### Example Fix:

**Before (Accessibility Issue):**
```tsx
<p className="text-clay">
  Click here to learn more about our features
</p>
```
Contrast: 2.96:1 - FAILS

**After (Accessible):**
```tsx
<p className="text-slate-light">
  Click here to learn more about our features
</p>
```
Contrast: 6.26:1 - PASSES AA

## Documentation Clone Accessibility Findings

### Original Finding: 77 Missing Alt Texts

From `/Users/alden/dev/claude_docs_clone_mintlify/docs/ACCESSIBILITY_REPORT.md`:

**Issue:** 77 images across official Claude Documentation had empty alt attributes (`alt=""`).

**Affected Files:**
- `ticket-routing.mdx` - 1 diagram
- `claude-for-sheets.mdx` - 3 screenshots
- `implement-tool-use.mdx` - 1 diagram
- `prompt-improver.mdx` - 1 screenshot
- `develop-tests.mdx` - 1 diagram
- `website-wizard.mdx` - 70 code examples

**Verification:** Confirmed on live site at https://anthropic.mintlify.app/

**Impact:**
- Screen reader users hear "image" with no description
- Missing context for diagrams and UI instructions
- WCAG 2.1 Level A violation (1.1.1 Non-text Content)

**Fix Applied:** Added descriptive alt text to all 77 images in the clone.

## Recommendations for Anthropic

### Immediate Actions

1. **Accent Color Adjustment**
   - Darken Clay to achieve 4.5:1 contrast ratio
   - Suggested: #b85a31 (Clay Dark) achieves 4.52:1 on Ivory
   - OR: Only use current Clay for large text (18pt+)

2. **Add Alt Text to Documentation**
   - 77 images need descriptive alt attributes
   - Implement in CI/CD: `mint a11y` checks before deploy
   - Establish content guidelines requiring alt text

3. **Design System Documentation**
   - Document which colors are safe for body text
   - Provide contrast-passing alternatives
   - Add accessibility annotations to design tokens

### Long-term Solutions

1. **Automated Testing**
   - Add contrast checking to component library
   - Automated a11y tests in CI/CD pipeline
   - Regular audits using axe-core or similar tools

2. **Design System Updates**
   - Create accessible color palettes with guaranteed contrast
   - Provide "text-safe" and "accent-only" color designations
   - Document approved color combinations

## Testing Methodology

### Tools Used:
- Custom JavaScript contrast calculator
- WCAG 2.1 standards reference
- Manual testing against production sites

### Calculation:
```javascript
// Luminance calculation per WCAG formula
function getLuminance(r, g, b) {
  const [rs, gs, bs] = [r, g, b].map(c => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

// Contrast ratio per WCAG formula
contrastRatio = (lighter + 0.05) / (darker + 0.05)
```

### Standards Applied:
- WCAG 2.1 Level AA (minimum): 4.5:1 for normal text
- WCAG 2.1 Level AA Large: 3:1 for 18pt+ or 14pt+ bold
- WCAG 2.1 Level AAA: 7:1 for normal text

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Anthropic Design System](https://anthropic.com) (extracted from production site)

## Conclusion

This analysis reveals that even major companies like Anthropic can have accessibility gaps in their design systems. The findings demonstrate:

1. **Color accessibility requires testing**, not assumptions
2. **Brand colors may not be universally usable** - some are accent-only
3. **Documentation accessibility** (alt text) is often overlooked
4. **Technical writing expertise** includes identifying and documenting these issues

Both findings have been addressed in this portfolio clone and documented here for Anthropic's benefit.

---

**Note:** This report is provided constructively to help improve accessibility for all Claude users. All testing was performed on publicly accessible design assets and documentation.
