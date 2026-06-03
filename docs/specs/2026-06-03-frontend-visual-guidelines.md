# Frontend Visual Guidelines - Voice Recommendation Evaluation

## Reference Direction

Use the user's reference prompt as visual inspiration:

> Build a calming mental health app landing page with neumorphic elements, mood tracking preview, therapy session booking, resource library, and crisis support section. Use soothing pastels.

This project is not a mental health landing page. Translate the reference into a calm internal evaluation workspace:
- soothing pastel palette
- soft neumorphic surfaces
- low-stress interaction states
- clear input and review flow
- visible recommendation metadata for evaluation

## Visual Style

Use a calming neumorphic product interface.

Recommended palette:
- `--color-background: #F6F3EE`
- `--color-surface: #EEF4F2`
- `--color-primary: #7BA7A2`
- `--color-cta: #4F8F83`
- `--color-soft-pink: #F3D9D5`
- `--color-soft-blue: #DDEAF2`
- `--color-text: #253634`
- `--color-muted: #667A76`

Avoid:
- purple-dominant wellness palettes
- dark mode as the default
- decorative hero sections
- marketing-style landing page copy
- oversized cards that reduce scan density

## Layout

The first screen should be the actual evaluation tool:
- left or top: text input and match button
- right or below: status, character count, and result area
- result cards show `Top5` recommendations after matching

Do not make a marketing landing page. The page should behave like a work surface for repeated testing.

## Recommendation Card

Each card must show:
- rank
- speaker name
- VCN
- 一级场景
- 二级场景
- 标签信息
- 性别
- 语言
- 技术标签
- audio player
- rating control
- optional comment field
- submit feedback action

Use soft raised cards with at most `8px` border radius. Use clear spacing, but keep cards dense enough for comparison.

## Interaction Rules

Follow `ui-ux-pro-max` priority rules:
- body text minimum `16px`
- normal text contrast at least `4.5:1`
- all interactive controls at least `44px` touch target
- visible focus ring
- disabled state while matching or submitting feedback
- no layout shift when loading results
- support `prefers-reduced-motion`
- hover/focus transitions `150-250ms`

## Audio And Feedback

Audio playback should be obvious and local to each card. If `audio_url` is missing, show a neutral unavailable state.

Rating should be one-tap/click, preferably segmented or star-like controls implemented with accessible buttons rather than emoji.

The comment field is optional and should not block rating submission.

