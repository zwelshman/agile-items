# Agile Refinery

**Transform rough ideas into polished, actionable agile work items with AI**

---

## What is Agile Refinery?

Agile Refinery is a modern web application that uses Claude AI to transform unstructured work items into professional, actionable agile descriptions. Whether you have a quick Slack message, a rough idea from a meeting, or a vague feature request, Agile Refinery will craft it into a polished work item ready for your sprint.

### What You Get

Every work item is transformed into:

| Section | Description |
|---------|-------------|
| **Title** | Concise, action-oriented (max 10 words) |
| **User Story** | "As a... I want... So that..." format |
| **Description** | Context, problem, and business value |
| **Acceptance Criteria** | 3-5 testable, specific criteria |
| **Technical Notes** | Implementation hints & considerations |
| **Definition of Done** | Complete checklist for sign-off |
| **Story Points** | Fibonacci estimate with rationale |

---

## Quick Start

### Deploy to Vercel (Recommended)

1. Fork this repository
2. Import the project in [Vercel](https://vercel.com/new)
3. Add your `ANTHROPIC_API_KEY` environment variable
4. Deploy and start refining!

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd agile-items

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local and add your ANTHROPIC_API_KEY

# Start development server
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) to see the app.

---

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom animations
- **Animations**: Framer Motion
- **UI**: Custom glassmorphism design system
- **AI**: Claude AI (claude-sonnet-4-20250514)
- **Deployment**: Vercel

---

## Example

**Input:**
```
Fix the slow dashboard
```

**Output:**

### Title
Optimize Dashboard Load Time Performance

### User Story
As a data analyst, I want the dashboard to load within 3 seconds so that I can quickly access insights without workflow interruption.

### Description
The current dashboard experiences significant load time delays, impacting user productivity and satisfaction. This optimization addresses performance bottlenecks to deliver a snappy, responsive experience that keeps users engaged.

### Acceptance Criteria
- [ ] Dashboard initial load completes within 3 seconds on standard connections
- [ ] Loading indicators display for any operation exceeding 500ms
- [ ] No visible layout shifts during data hydration
- [ ] Performance metrics logged for monitoring

### Technical Notes
- Profile current render cycle to identify bottlenecks
- Consider implementing React.memo for expensive components
- Evaluate data fetching strategy (SSR vs client-side)
- Implement virtualization for large data lists

### Definition of Done
- [ ] Code complete and reviewed
- [ ] Unit tests written and passing
- [ ] Performance benchmarks documented
- [ ] Deployed to staging
- [ ] Product owner sign-off

### Story Points
**5 points** - Moderate complexity requiring performance profiling and multiple optimization techniques.

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Yes |

Get your API key from the [Anthropic Console](https://console.anthropic.com/).

---

## Project Structure

```
agile-refinery/
├── app/
│   ├── api/
│   │   └── generate/
│   │       └── route.ts    # Claude AI integration
│   ├── globals.css         # Tailwind & custom styles
│   ├── layout.tsx          # Root layout
│   └── page.tsx            # Main application
├── src/
│   └── lib/
│       └── utils.ts        # Utility functions
├── public/                 # Static assets
├── tailwind.config.ts      # Tailwind configuration
├── next.config.mjs         # Next.js configuration
├── vercel.json             # Vercel deployment config
└── package.json
```

---

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Import the project in Vercel
3. Add `ANTHROPIC_API_KEY` to environment variables
4. Deploy!

### Other Platforms

The app is a standard Next.js application and can be deployed to any platform that supports Node.js:

- **Railway**: `railway up`
- **Render**: Connect your Git repository
- **Docker**: Use `next build && next start`

---

## License

MIT License - feel free to use this project for personal or commercial purposes.

---

**Built with Next.js and Claude AI**
