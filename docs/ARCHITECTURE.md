# MARKETER_AI Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           MARKETER_AI                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐     │
│  │   Next.js Web   │    │  Video Studio   │    │   Supabase      │     │
│  │   (Dashboard)   │    │   (Remotion)    │    │   (Backend)     │     │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘     │
│           │                      │                      │               │
│           └──────────────────────┼──────────────────────┘               │
│                                  │                                       │
│                    ┌─────────────▼─────────────┐                        │
│                    │      API Layer            │                        │
│                    │   (Next.js API Routes)    │                        │
│                    └─────────────┬─────────────┘                        │
│                                  │                                       │
│           ┌──────────────────────┼──────────────────────┐               │
│           │                      │                      │               │
│  ┌────────▼────────┐    ┌───────▼────────┐    ┌───────▼────────┐      │
│  │  Skill Adapter  │    │   Agent Core   │    │ Video Renderer │      │
│  │  (Skills.sh)    │    │   (CrewAI)     │    │  (Remotion)    │      │
│  └────────┬────────┘    └───────┬────────┘    └───────┬────────┘      │
│           │                      │                      │               │
│           └──────────────────────┼──────────────────────┘               │
│                                  │                                       │
│                    ┌─────────────▼─────────────┐                        │
│                    │     LLM Layer             │                        │
│                    │  Claude / Kimi K2.5       │                        │
│                    └───────────────────────────┘                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Frontend (Next.js 14)

**Location:** `apps/web/`

**Key Features:**
- App Router for modern routing
- Server Components for performance
- Server Actions for mutations
- React Query for client state
- Framer Motion for animations

**UI Stack:**
- shadcn/ui components
- Tailwind CSS
- Glass morphism design

### 2. Video Studio (Remotion)

**Location:** `apps/video-studio/`

**Key Features:**
- Programmatic video generation
- React-based compositions
- Frame-accurate animations
- Multi-platform export

**Compositions:**
- TikTokAd (1080x1920, 9:16)
- InstagramReel (1080x1920, 9:16)
- YouTubeShort (1080x1920, 9:16)
- YouTubeVideo (1920x1080, 16:9)

### 3. Agent Core (CrewAI)

**Location:** `packages/agent-core/`

**Pre-Equipped Crews:**

#### Content Crew
- Hook Specialist (pattern interrupts, curiosity gaps)
- Psychology Copywriter (70+ mental models)
- Platform Expert (algorithm optimization)

#### Video Crew
- Video Strategy Director (retention optimization)
- Remotion Code Generator (React video code)
- Caption Animator (TikTok-style captions)

#### Lead Gen Crew
- Lead Qualifier (BANT/MEDDIC scoring)
- Pipeline Analyst (forecasting, velocity)
- ICP Matcher (ideal customer profiling)

#### Campaign Crew
- Brand Strategist (April Dunford positioning)
- Campaign Planner (multi-channel orchestration)
- Analytics Expert (performance optimization)

### 4. Skill Adapter

**Location:** `packages/skill-adapter/`

**Purpose:** Bridge between Skills.sh content and agent engine

**Key Skills:**
- marketing-strategy-pmm (1,163 lines)
- marketing-psychology (70+ mental models)
- ad-copy-writer (platform-specific copy)
- kinetic-video-creator (Remotion patterns)
- lead-qualifier (BANT/MEDDIC)

### 5. Database (Supabase)

**Location:** `packages/database/`

**Core Tables:**
- organizations
- users
- brands
- campaigns
- generated_videos
- agent_crews
- agent_sessions
- leads
- skills_registry
- usage_records

**Features:**
- Row Level Security
- Real-time subscriptions
- Storage for videos/assets

---

## Data Flow

### Campaign Creation Flow

```
User Input (Brief)
       │
       ▼
┌─────────────────┐
│  Campaign Crew  │
│                 │
│ 1. Brand DNA    │ ← marketing-strategy-pmm skill
│ 2. ICP          │ ← April Dunford methodology
│ 3. Positioning  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Content Crew   │
│                 │
│ 1. Hook Gen     │ ← marketing-psychology skill
│ 2. Copy Gen     │ ← ad-copy-writer skill
│ 3. Platform Opt │ ← tiktok-creator skill
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Video Crew    │
│                 │
│ 1. Structure    │ ← Retention science
│ 2. Remotion     │ ← kinetic-video-creator skill
│ 3. Captions     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Remotion Render │
│                 │
│ Generate MP4    │
└────────┬────────┘
         │
         ▼
   Supabase Storage
         │
         ▼
   User Dashboard
```

### Lead Qualification Flow

```
Lead Input
    │
    ▼
┌─────────────────┐
│  Lead Gen Crew  │
│                 │
│ 1. BANT Score   │
│    - Budget     │
│    - Authority  │
│    - Need       │
│    - Timeline   │
│                 │
│ 2. MEDDIC Score │
│    - Metrics    │
│    - Economic   │
│    - Decision   │
│    - Identify   │
│    - Champion   │
│                 │
│ 3. ICP Match    │
│    A/B/C/D fit  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Lead Score (0-100)
│ Stage Assignment │
│ Pipeline Update  │
└─────────────────┘
```

---

## Technology Decisions

### Why CrewAI?
- Native multi-agent orchestration
- Flows for complex workflows
- Built-in tool integration
- Production-ready

### Why Remotion?
- React-based (team familiarity)
- Frame-accurate animations
- Programmatic generation
- Code = reusable templates

### Why Supabase?
- Postgres (familiar, powerful)
- Built-in auth
- Real-time subscriptions
- Storage included
- Row Level Security

### Why Next.js 14?
- Server Components (performance)
- Server Actions (simplified mutations)
- App Router (modern patterns)
- Vercel deployment (seamless)

---

## Scaling Considerations

### Phase 1: MVP
- Single Vercel deployment
- Supabase free tier
- Synchronous video rendering

### Phase 2: Growth
- Vercel Pro (longer timeouts)
- Supabase Pro (more connections)
- Queue-based video rendering

### Phase 3: Scale
- Dedicated render workers
- Redis for caching
- CDN for video delivery
- Kubernetes for agent workers

---

## Security

### Authentication
- Supabase Auth (OAuth, Magic Link)
- JWT-based sessions
- Secure cookie storage

### Authorization
- Row Level Security on all tables
- Role-based access (owner, admin, member, viewer)
- Organization isolation

### Data Protection
- HTTPS everywhere
- Encrypted at rest (Supabase)
- Environment variables for secrets
- No secrets in client code
