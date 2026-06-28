 🍛 Saffron Table — Artisan Food & Dining Website

 A fully responsive restaurant website with a functional cart system, category-based menu filtering, and smooth multi-page navigation — all built as a **single HTML file** with zero dependencies.

✨ Features

- **Multi-page SPA** — Home, Menu, About, and Contact pages with smooth JS-based switching
- **Dynamic Menu** — Filter dishes by category: Starters, Mains, Pizza, Desserts, Drinks
- **Shopping Cart Drawer** — Slide-in cart with quantity controls and live total (₹ INR)
- **LocalStorage Persistence** — Cart items saved across page refreshes
- **Order Success Modal** — Animated confirmation popup on checkout
- **Toast Notifications** — Feedback messages for add-to-cart and form actions
- **Contact Form** — Name, email, subject, and message fields with validation
- **Responsive Design** — Mobile hamburger menu, fluid grids, works on all screen sizes
- **Veg / Non-Veg Labels** — Green 🟢 / Red 🔴 indicators on every dish card
- **Scroll-aware Navbar** — Shadow effect triggers on scroll



 🛠️ Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Structure  | HTML5                               |
| Styling    | CSS3 (CSS Variables, Grid, Flexbox) |
| Logic      | Vanilla JavaScript (ES6+)           |
| Fonts      | Google Fonts — Playfair Display, DM Sans |
| Storage    | localStorage (cart persistence)     |
| Hosting    | GitHub Pages / Netlify _(recommended)_ |

🎨 Color Palette

| Name       | Hex       | Usage                        |
|------------|-----------|------------------------------|
| Burgundy   | `#5C1A1A` | Primary brand color, buttons |
| Gold       | `#E8A020` | Accents, highlights, badges  |
| Cream      | `#FDF6EC` | Page background              |
| Charcoal   | `#1C1C1C` | Body text                    |
| Sage       | `#7A8C6E` | Category labels              |



 🧠 What I Learned Building This

- Structuring a multi-page experience inside a single HTML file using JS page switching
- Managing state (cart items, quantities) with localStorage
- Building a slide-in drawer with CSS transitions and overlay logic
- Writing clean, reusable CSS using custom properties (variables)
- Making a fully responsive layout without any CSS framework


📁 Project Structure

```
saffron-table/
└── saffron-table.html   # Entire project — HTML + CSS + JS in one file
```

 🚀 Getting Started

No installs or setup needed!

1. **Clone the repo**
   ```bash
   git clone https://github.com/joshuak2005/saffron-table.git
   ```

2. **Open the file**
   ```bash
   cd saffron-table
   start saffron-table.html   # Windows
   # or just double-click the file
   ```

Runs directly in any browser. ✅

 🌍 Deployment

 GitHub Pages (Free)
1. Push the file to a GitHub repo
2. Go to **Settings → Pages**
3. Set source to `main` branch → `/ (root)`
4. Live at `https://joshuak2005.github.io/saffron-table/saffron-table.html`

 Netlify (Free)
1. Drag and drop the HTML file at [netlify.com/drop](https://app.netlify.com/drop)
2. Instant live URL — no account needed!

 📄 Pages Overview

| Page    | Description                                               |
|---------|-----------------------------------------------------------|
| Home    | Hero banner, category grid, featured dishes, testimonials |
| Menu    | Full dish listing with filter buttons by category         |
| About   | Brand story, team section, core values                    |
| Contact | Contact form + address, phone, email info                 |

 
GitHub: [@joshuak2005](https://github.com/joshuak2005)


