# MARKETER_AI

> **The Ultimate AI-Powered Marketing Platform That Crushes GoHighLevel**

Pre-equipped AI agents with 95+ marketing skills that make users say *"WTF this is too good"*

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## Vision

MARKETER_AI is an AI-powered marketing automation platform that delivers:

- **95+ Pre-loaded Marketing Skills** - Instant expertise from Skills.sh
- **CrewAI Multi-Agent Orchestration** - Autonomous marketing crews
- **AI-Generated Remotion Videos** - Custom code, not templates
- **70+ Psychology Mental Models** - Built into every agent
- **April Dunford Positioning** - Brand strategy methodology
- **BANT/MEDDIC Lead Scoring** - Automated qualification

---

## Core Differentiators vs GoHighLevel

| Feature | GoHighLevel | MARKETER_AI |
|---------|-------------|-------------|
| AI Agents | Basic chatbots | Pre-equipped crews with 95+ skills |
| Video | Templates only | AI-generated Remotion code |
| Psychology | None | 70+ mental models built-in |
| Hooks | Manual | AI-generated scroll-stoppers |
| Lead Scoring | Basic rules | AI-powered BANT/MEDDIC |
| Positioning | None | April Dunford methodology |

---

## Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **UI**: shadcn/ui + Radix UI
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **State**: TanStack React Query

### Backend
- **Database**: Supabase (Postgres + Auth + Storage)
- **Agent Engine**: CrewAI (Python)
- **Primary LLM**: Claude Opus 4
- **Multimodal**: Kimi K2.5

### Video
- **Framework**: Remotion
- **Avatars**: HeyGen API
- **Fast Gen**: InVideo API

---

## Project Structure

```
MARKETER_AI/
├── apps/
│   ├── web/                    # Next.js 14 App
│   └── video-studio/           # Remotion video generation
├── packages/
│   ├── agent-core/             # CrewAI Python engine
│   ├── skill-adapter/          # Skills.sh integration
│   ├── database/               # Supabase schema
│   └── shared/                 # Shared utilities
├── skills/                     # Marketing skills cache
└── docs/                       # Documentation
```

---

## Pre-Equipped Agent Crews

### Content Crew
- **Hook Specialist**: Creates scroll-stopping hooks (pattern interrupts, curiosity gaps)
- **Psychology Copywriter**: Applies 70+ mental models to copy
- **Platform Expert**: Optimizes for TikTok/IG/YouTube algorithms

### Video Crew
- **Video Strategy Director**: Designs retention-optimized structure
- **Remotion Code Generator**: Produces production-ready React video code
- **Caption Animator**: TikTok-style word-by-word highlighting

### Lead Gen Crew
- **Lead Qualifier**: BANT/MEDDIC scoring automation
- **Pipeline Analyst**: Deal tracking and forecasting
- **ICP Matcher**: Ideal Customer Profile scoring

### Campaign Crew
- **Brand Strategist**: April Dunford positioning methodology
- **Campaign Planner**: Multi-channel orchestration
- **Analytics Expert**: Performance optimization

---

## Key Files

- `MARKETER_AI_HANDOFF.json` - Complete project specification (25KB)
- `IMPLEMENTATION_PLAN.md` - Phased implementation roadmap
- `packages/database/migrations/` - Supabase schema

---

## Pricing Tiers

| Plan | Price | Videos/mo | Agent Sessions | Leads |
|------|-------|-----------|----------------|-------|
| Free | $0 | 3 | 10 | 100 |
| Starter | $49 | 25 | 100 | 1,000 |
| Pro | $149 | 100 | 500 | 10,000 |
| Enterprise | Custom | Unlimited | Unlimited | Unlimited |

---

## Psychology Principles (Built-In)

Every hook must include 1-2 of these triggers:

1. **Pattern Interrupt** - Break the scroll trance
2. **Curiosity Gap** - Incomplete info creates tension
3. **Value Promise** - Signal reward for watching
4. **Loss Aversion** - Losses hurt 2x more than gains
5. **Social Proof** - Tribal validation
6. **Scarcity/Urgency** - Limited = valuable

### Critical Stats
- 65%+ retention at 3 seconds = 4-7x more impressions
- 85% watch videos muted - text/captions essential
- Videos losing >35% at 3 seconds get algorithmically buried

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/0x404ethsol/Marketer_AI.git

# Install dependencies
pnpm install

# Set up environment variables
cp .env.example .env.local

# Run development server
pnpm dev
```

---

## License

MIT

---

## Contributing

This is an ambitious project. Contributions welcome!

1. Fork the repo
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

**Built with rage and persistence. Let's crush GoHighLevel.**
