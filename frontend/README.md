# Daily AI Newsletter - Professional Frontend

A sophisticated, enterprise-grade web application for managing and showcasing daily AI newsletters. Built with cutting-edge web technologies and refined design aesthetics.

## Design Philosophy

This frontend embodies a **refined minimalism** aesthetic combined with data-forward UX patterns:

- **Typography**: Playfair Display (elegant headers) + Poppins (clean body) + JetBrains Mono (code)
- **Color Palette**: Deep slate backgrounds with cyan accents, cream text for contrast
- **Interactions**: Subtle animations, smooth transitions, purposeful hover states
- **Spatial Design**: Generous whitespace with strategic information density

The interface prioritizes content (the newsletter) while providing powerful administrative capabilities.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **UI Library**: React 18 with TypeScript
- **Styling**: Tailwind CSS 3 with custom design tokens
- **Markdown**: React Markdown with GitHub Flavored Markdown support
- **Animations**: Framer Motion (optional advanced animations)
- **State Management**: Zustand (lightweight, optional)
- **Icons**: Lucide React
- **Date Handling**: date-fns
- **API Client**: Axios

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout with metadata
│   ├── page.tsx             # Dashboard page
│   └── globals.css          # Global styles and design tokens
├── components/
│   ├── Sidebar.tsx          # Navigation sidebar
│   ├── Header.tsx           # Top header with controls
│   ├── StatsCard.tsx        # Statistics cards
│   ├── NewsletterViewer.tsx # Newsletter display with markdown
│   └── Archive.tsx          # Newsletter archive and search
├── lib/
│   └── hooks/
│       └── useNewsletter.ts # Newsletter data hook
├── public/                  # Static assets
├── next.config.js           # Next.js configuration
├── tailwind.config.ts       # Tailwind theme configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies
```

## Setup & Installation

### Prerequisites

- Node.js 18+ and npm/yarn
- Python backend (for API integration)

### Installation

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env.local
   ```

   Configure in `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000) in your browser.

4. **Build for production**
   ```bash
   npm run build
   npm run start
   ```

## Features

### Dashboard
- **Latest Newsletter Display**: Beautiful markdown rendering with syntax highlighting
- **Quick Stats**: Article, paper, and post counts at a glance
- **View Modes**: Toggle between rendered preview and raw markdown
- **Download Options**: Export as Markdown, Text, or PDF

### Navigation
- **Responsive Sidebar**: Collapsible navigation with sub-menus
- **Sticky Header**: View tabs (Latest, Stats, Archive) always accessible
- **Mobile-Friendly**: Full responsive design for all screen sizes

### Archive & Search
- **Browsable History**: All past newsletters with metadata
- **Advanced Search**: Filter by date or content
- **Theme Tags**: Visual indicators of newsletter themes
- **Quick Access**: Download previous newsletters easily

### Notifications
- **Real-time Updates**: Bell icon with unread notification count
- **Newsletter Status**: Generation completion notifications
- **Source Alerts**: New content availability alerts

### Design System

#### Colors
- **Primary**: Slate (`#1a1f36`) - Dark, refined backgrounds
- **Accents**: Cyan (`#06b6d4`), Teal (`#14b8a6`), Gold (`#f59e0b`), Rose (`#f43f5e`)
- **Text**: Cream (`#f8f7f3`) - High contrast, easy on eyes

#### Typography
- **Display Font**: Playfair Display - Elegant, distinctive
- **Body Font**: Poppins - Clean, readable
- **Mono Font**: JetBrains Mono - Code and technical content

#### Spacing
- Base unit: 0.25rem (4px)
- Generous use of whitespace for premium feel
- Consistent padding and margins throughout

#### Animations
- **Fade In**: 0.6s ease-in-out on page load
- **Slide Up**: 0.5s ease-out for content reveals
- **Hover States**: Smooth 0.3s transitions for interactivity
- **Micro-interactions**: Subtle pulse and glow effects on hover

## API Integration

The frontend expects the Python backend to provide these endpoints:

### GET `/api/newsletter/latest`
Returns the latest generated newsletter:
```json
{
  "id": "newsletter-2024-03-14",
  "date": "2024-03-14T07:00:00Z",
  "content": "# Daily AI Newsletter\n...",
  "metadata": {
    "articles": 12,
    "papers": 8,
    "posts": 6,
    "themes": ["Agentic AI", "Multimodal Models"]
  }
}
```

### GET `/api/newsletter/archive?page=1&limit=20`
Returns paginated newsletter archive:
```json
{
  "newsletters": [...],
  "total": 365,
  "page": 1,
  "limit": 20
}
```

### POST `/api/newsletter/generate`
Triggers manual newsletter generation:
```json
{
  "status": "processing",
  "id": "job-12345"
}
```

### POST `/api/newsletter/schedule`
Configures generation schedule:
```json
{
  "enabled": true,
  "time": "07:00",
  "timezone": "UTC"
}
```

## Customization

### Colors
Edit `tailwind.config.ts`:
```typescript
colors: {
  slate: { /* slate colors */ },
  accent: {
    cyan: '#06b6d4',
    teal: '#14b8a6',
    gold: '#f59e0b',
    rose: '#f43f5e',
  }
}
```

### Fonts
Update `globals.css` Google Fonts imports:
```css
@import url('https://fonts.googleapis.com/css2?family=...');
```

### Spacing
Modify Tailwind theme in `tailwind.config.ts`:
```typescript
spacing: {
  /* custom values */
}
```

## Performance Optimizations

- **Code Splitting**: Next.js automatic route-based code splitting
- **Image Optimization**: Next.js Image component for responsive images
- **CSS-in-JS**: Minimal runtime overhead with Tailwind
- **Lazy Loading**: Components loaded on-demand
- **API Caching**: Implement caching headers for archive data

## Accessibility

- WCAG 2.1 Level AA compliance
- Semantic HTML structure
- ARIA labels for interactive elements
- Keyboard navigation support
- High contrast color scheme
- Reduced motion support (respects `prefers-reduced-motion`)

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome Mobile)

## Development

### Type Checking
```bash
npm run type-check
```

### Linting (optional - add ESLint)
```bash
npm run lint
```

### Build Analysis (optional)
```bash
npm run build -- --analyze
```

## Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "start"]
```

### Manual Deployment
```bash
npm run build
npm run start
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `NODE_ENV` | Environment | `development` |

## Future Enhancements

- [ ] Dark/Light mode toggle
- [ ] User authentication and multi-user support
- [ ] Advanced analytics dashboard
- [ ] Email subscription integration
- [ ] PDF export with custom branding
- [ ] Real-time collaboration features
- [ ] Advanced markdown editor
- [ ] Theme customization panel
- [ ] API rate limiting visualization
- [ ] Source management interface

## Performance Metrics

Target metrics for production:
- **Lighthouse Score**: 90+ (Performance)
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **Time to Interactive**: < 3.5s

## Troubleshooting

### API Connection Issues
Check `NEXT_PUBLIC_API_URL` in `.env.local` matches your backend:
```bash
curl http://localhost:8000/api/newsletter/latest
```

### Styling Issues
Clear Next.js cache:
```bash
rm -rf .next
npm run dev
```

### Import Errors
Verify `tsconfig.json` paths configuration is correct.

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check existing GitHub issues
2. Review the main project README.md
3. Examine component docstrings and type definitions
4. Check the CLAUDE.md specification

## Contributing

1. Create a feature branch
2. Make changes with atomic commits
3. Test responsively on multiple devices
4. Submit pull request with clear description

---

Built with care for businesses who value beautiful, functional interfaces.
