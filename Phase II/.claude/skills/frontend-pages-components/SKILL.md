---
name: frontend-pages-components
description: Build responsive frontend pages, reusable components, layouts, and styling. Use for UI development and design systems.
---

# Frontend Pages & Components

## Instructions

1. **Page & Layout Structure**
   - Responsive grid or flex-based layout
   - Clear page sections (header, main, footer)
   - Consistent spacing and alignment

2. **Components**
   - Reusable UI components (buttons, cards, forms)
   - Component-based structure
   - Props/variants for flexibility

3. **Styling**
   - Modern CSS (Flexbox, Grid)
   - Scalable naming (BEM / utility classes)
   - Theme variables (colors, fonts, spacing)

4. **Responsiveness**
   - Mobile-first design
   - Breakpoints for tablet & desktop
   - Fluid typography and layouts

5. **Interactions**
   - Hover & focus states
   - Basic transitions and animations
   - Accessible keyboard navigation

## Best Practices
- Keep components small and reusable
- Follow consistent design patterns
- Use semantic HTML
- Optimize for performance
- Ensure accessibility (ARIA, contrast, focus)

## Example Structure
```html
<div class="page">
  <header class="header">
    <nav class="nav">
      <a href="#" class="logo">Brand</a>
      <ul class="nav-links">
        <li><a href="#">Home</a></li>
        <li><a href="#">About</a></li>
      </ul>
    </nav>
  </header>

  <main class="content">
    <section class="card">
      <h2 class="card-title">Component Title</h2>
      <p class="card-text">Reusable component content.</p>
      <button class="btn-primary">Action</button>
    </section>
  </main>

  <footer class="footer">
    <p>© 2026</p>
  </footer>
</div>
