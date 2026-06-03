# Design System Master File

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** Intelligent Matching Evaluation System
**Generated:** 2026-06-03 16:29:32
**Category:** Internal Evaluation Tool

---

## Global Rules

### Color Palette

| Role | Hex | CSS Variable |
|------|-----|--------------|
| Primary | `#7BA7A2` | `--color-primary` |
| Secondary | `#DCEBE8` | `--color-secondary` |
| CTA/Accent | `#4F8F83` | `--color-cta` |
| Background | `#F6F3EE` | `--color-background` |
| Surface | `#EEF4F2` | `--color-surface` |
| Soft Pink | `#F3D9D5` | `--color-soft-pink` |
| Soft Blue | `#DDEAF2` | `--color-soft-blue` |
| Text | `#253634` | `--color-text` |

**Color Notes:** Soothing pastels adapted from the reference prompt. Use sage, mist blue, blush, and warm off-white. Avoid a purple-dominant palette so the tool feels calm and operational rather than decorative.

### Typography

- **Heading Font:** Lora
- **Body Font:** Raleway
- **Mood:** calm, wellness, health, relaxing, natural, organic
- **Google Fonts:** [Lora + Raleway](https://fonts.google.com/share?selection.family=Lora:wght@400;500;600;700|Raleway:wght@300;400;500;600;700)

**CSS Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Raleway:wght@300;400;500;600;700&display=swap');
```

### Spacing Variables

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | `4px` / `0.25rem` | Tight gaps |
| `--space-sm` | `8px` / `0.5rem` | Icon gaps, inline spacing |
| `--space-md` | `16px` / `1rem` | Standard padding |
| `--space-lg` | `24px` / `1.5rem` | Section padding |
| `--space-xl` | `32px` / `2rem` | Large gaps |
| `--space-2xl` | `48px` / `3rem` | Section margins |
| `--space-3xl` | `64px` / `4rem` | Hero padding |

### Shadow Depths

| Level | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle lift |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.1)` | Cards, buttons |
| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modals, dropdowns |
| `--shadow-xl` | `0 20px 25px rgba(0,0,0,0.15)` | Hero images, featured cards |

---

## Component Specs

### Buttons

```css
/* Primary Button */
.btn-primary {
  background: #4F8F83;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 200ms ease;
  cursor: pointer;
}

.btn-primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

/* Secondary Button */
.btn-secondary {
  background: transparent;
  color: #253634;
  border: 2px solid #7BA7A2;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 200ms ease;
  cursor: pointer;
}
```

### Cards

```css
.card {
  background: #EEF4F2;
  border-radius: 8px;
  padding: 24px;
  box-shadow: var(--shadow-md);
  transition: all 200ms ease;
  cursor: pointer;
}

.card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}
```

### Inputs

```css
.input {
  padding: 12px 16px;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 200ms ease;
}

.input:focus {
  border-color: #7BA7A2;
  outline: none;
  box-shadow: 0 0 0 3px #7BA7A240;
}
```

### Modals

```css
.modal-overlay {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.modal {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: var(--shadow-xl);
  max-width: 500px;
  width: 90%;
}
```

---

## Style Guidelines

**Style:** Calming Neumorphic Evaluation Interface

**Keywords:** soothing, pastel, low-stress, neumorphic, focused, internal evaluation, audio review, feedback capture

**Best For:** internal tools, evaluation workflows, repeated review tasks, audio recommendation testing

**Key Effects:** soft inset fields, raised recommendation cards, calm focus rings, 150-250ms hover/focus transitions, clear loading states

### Page Pattern

**Pattern Name:** Single-Page Evaluation Workspace

- **Workflow Strategy:** Reduce friction for repeated text testing and feedback capture.
- **CTA Placement:** Primary action beside the text input controls, feedback actions inside each recommendation card.
- **Section Order:** 1. Text input workspace, 2. Top5 recommendation results, 3. Per-voice audio preview, 4. Per-voice rating and optional comment.

---

## Anti-Patterns (Do NOT Use)

- ❌ Flat design without depth
- ❌ Text-heavy pages
- ❌ Purple-dominant wellness palette
- ❌ Marketing landing page structure
- ❌ Hidden debug labels during internal evaluation

### Additional Forbidden Patterns

- ❌ **Emojis as icons** — Use SVG icons (Heroicons, Lucide, Simple Icons)
- ❌ **Missing cursor:pointer** — All clickable elements must have cursor:pointer
- ❌ **Layout-shifting hovers** — Avoid scale transforms that shift layout
- ❌ **Low contrast text** — Maintain 4.5:1 minimum contrast ratio
- ❌ **Instant state changes** — Always use transitions (150-300ms)
- ❌ **Invisible focus states** — Focus states must be visible for a11y

---

## Pre-Delivery Checklist

Before delivering any UI code, verify:

- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Light mode: text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard navigation
- [ ] `prefers-reduced-motion` respected
- [ ] Responsive: 375px, 768px, 1024px, 1440px
- [ ] No content hidden behind fixed navbars
- [ ] No horizontal scroll on mobile
