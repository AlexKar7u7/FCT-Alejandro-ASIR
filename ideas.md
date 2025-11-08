# Styling & Component Ideas for FCT-Alejandro-ASIR

This document collects the styling, component-structure, accessibility, and progressive-enhancement ideas we discussed. It's intended as a living reference when you implement CSS changes, component refactors, or small JS enhancements (HTMX/Alpine).

## Top-level goals

- Make styles predictable and maintainable.
- Keep templates small, reusable, and fast.
- Improve accessibility, responsiveness, and performance.
- Make future design/system changes low-cost.

## 1) CSS architecture and organization

- Adopt a light architecture: BEM or ITCSS (or a hybrid).
  - BEM maps well to partial templates (`.card`, `.card__title`, `.card--highlight`).
  - ITCSS (layered approach) helps scale: settings → tools → generic → components → utilities.

- Use CSS custom properties for theme primitives:
  - colors, spacing scale, breakpoints, font sizes, radii, z-index scale.
  - Example variables: `--color-primary`, `--space-1`, `--text-base`.

- Split CSS into logical files:
  - `settings.css` (variables, breakpoints)
  - `base.css` (normalize, body, typography)
  - `layout.css` (grid, container, site header/footer)
  - `components/*.css` (navbar.css, card.css, comment.css, forms.css)
  - `utilities.css` (helpers like `.u-hidden`, `.sr-only`, `.mt-1`)

- Static structure suggestion:
```
static/
  css/
    settings.css
    base.css
    layout.css
    components/
      navbar.css
      card.css
      comment.css
    utilities.css
  js/
  images/
```

- Consider Sass/SCSS if you want nesting, partials, and variables at scale. Plain CSS variables are fine if you want no build step.

## 2) Componentization (Django templates + CSS)

- Convert repeated markup into small included templates in `templates/blog/components/`:
  - `navbar.html` — site header
  - `card.html` — article/tema preview
  - `comment.html` — single comment + reply loop
  - `pagination.html` — pagination controls
  - `form_field.html` — consistent field rendering

- Prefer passing minimal context to includes: `{% include 'blog/components/card.html' with articulo=articulo %}`
- Use Django inclusion tags for server-side logic that prepares data for complex components (e.g., annotated vote counts).
- Keep components "dumb": prepare data in views (annotate, select_related) and pass ready-to-render context.

## 3) Naming conventions & class strategy

- Use BEM-like classes:
  - Block: `.card`
  - Element: `.card__title`
  - Modifier: `.card--featured`

- Use utility prefix: `.u-hidden`, `.u-mt-1`
- State classes: `.is-active`, `.is-disabled`

## 4) Responsive layout & breakpoints

- Define breakpoints as CSS variables:
  - `--bp-sm: 576px; --bp-md: 768px; --bp-lg: 992px; --bp-xl: 1200px`
- Adopt mobile-first: base styles for small screens, `@media (min-width: var(--bp-md))` for larger.
- Navbar: collapse to hamburger or stack vertically on small screens.

## 5) Typography & spacing

- Establish a type scale and spacing scale via variables.
- Use consistent line-height and max-width for article content for readability.
- Prefer component-level spacing over ad-hoc margins everywhere.

## 6) Forms and accessibility UX

- Visible focus states (use `:focus-visible`).
- Link error messages to fields with `aria-describedby`.
- Keep labels visible (avoid placeholders as labels).
- Provide `.sr-only` utility for screen-reader-only text.
- Make sure interactive elements are keyboard-focusable.

## 7) Comments & threaded replies component

- Render a single comment with an include and have it recursively include replies (with indentation).
- Limit visual nesting (e.g., collapse after 3 levels to "view conversation").
- Use inline reply forms that toggle with minimal JS (HTMX/Alpine).
- Hook JS using `data-` attributes (e.g., `data-comment-id`).

## 8) Cards, lists, and detail pages

- Standardize `card.html` structure: title, meta, excerpt, optional image, actions.
- Use modifiers for context: `.card--compact`, `.card--full`.
- Use a fixed aspect-ratio container for images to prevent layout shift.
- Use server-side truncated excerpts for stable layout.

## 9) Interactivity: JS choices

- For small interactions use HTMX or Alpine.js:
  - HTMX: server-rendered fragments, progressive enhancement.
  - Alpine: tiny reactive layer for client state.
- Example: voting endpoint returns updated button + count fragment; HTMX swaps it in.
- Keep JS unobtrusive: server-side first, enhance afterward.

## 10) Performance & asset pipeline

- Serve minified CSS in production. Options:
  - Add a small build step: PostCSS + cssnano (if you want optimization).
  - Use WhiteNoise + `ManifestStaticFilesStorage` for cache-busting.
- Optimize images (WebP where possible, `loading="lazy"`).

## 11) Theme, color, and contrast

- Small palette: primary, secondary, neutral, success, danger.
- Ensure WCAG contrast (4.5:1 for normal text).
- Optional dark mode via CSS variables toggled with `.dark` on `<body>`.

## 12) SEO & meta components

- Add `templates/components/meta.html` include for canonical, description, OG, and Twitter cards.
- Use it in article/detail templates and ensure each page sets title/description context.

## 13) Template performance & caching

- Cache repeating, infrequently-changing components (menu, sidebar lists) with template fragment cache.
- Use `{% include %}` for small bits, but use view-side annotation to avoid heavy template logic.

## 14) Design system & living docs

- Add a one-page style guide (`/styleguide/`) showcasing components:
  - Buttons, forms, cards, navbar, comment styles, utilities
- Keep `settings.css` as the single source of theme variables.

## 15) Quick wins (no build step)

1. Consolidate component CSS under `static/css/components/`.
2. Add `static/css/settings.css` with variables and replace hard-coded colors in existing CSS.
3. Add visible focus styles and `.sr-only` utility.
4. Make `.card` responsive and add fixed aspect container for images.
5. Convert vote button to HTMX endpoint returning a small fragment (button + count).
6. Create `templates/blog/components/meta.html` to centralize meta tags.

## 16) Progressive enhancement with HTMX (recommended)

- Replace full-page posts for comments/votes with HTMX endpoints returning updated partials.
- Benefits: minimal JS, server-rendered HTML, faster dev loop.

## 17) Accessibility checklist (component-focused)

- All images have `alt` (or empty alt if decorative).
- Logical focus order.
- Buttons/links have discernible text.
- Error messages are linked to fields (`aria-describedby`).
- Color contrast meets WCAG.

## 18) Example snippets (conceptual)

- A few variables to start in `settings.css`:
```
:root {
  --color-primary: #0d6efd;
  --bg: #fff;
  --text: #111;
  --radius: 8px;
  --gap: 1rem;
  --bp-md: 768px;
}
```

- A simple BEM card markup (`templates/blog/components/card.html`):
```html
<article class="card card--compact">
  <h3 class="card__title">{{ articulo.titulo }}</h3>
  <p class="card__meta">By {{ articulo.autor.username }} • {{ articulo.fecha_publicacion|date:"SHORT_DATE_FORMAT" }}</p>
  <p class="card__excerpt">{{ articulo.excerpt }}</p>
</article>
```

## 19) Tools & libraries to consider

- CSS: Sass/SCSS, PostCSS, Autoprefixer, cssnano
- UI frameworks: Tailwind CSS (utility-first) or Bootstrap (component-ready)
- Tiny JS: HTMX, Alpine.js
- Forms: `django-crispy-forms` (if you want quick form theming)
- Static serving: `whitenoise` for simple deployments
- Image handling: `django-imagekit` or on-deploy optimization

## 20) Next steps I can help with
- Draft `static/css/settings.css` and a scaffold for `card.css` and `comment.css` to match `templates/blog/components/`.
- Create a small HTMX-enabled fragment for voting/comments (view + template examples).
- Produce a one-page style guide under `templates/styleguide.html` showcasing components.

## Assumptions
- You prefer server-rendered HTML and minimal JS enhancement.
- The repo should keep a minimal/no-build approach unless you request a build pipeline.

---

If you want any of the quick wins implemented as a small PR or patch (CSS scaffold, HTMX fragment, or styleguide), tell me which one and I'll prepare the changes. No code has been modified in the repository yet.
