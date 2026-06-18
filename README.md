# Backend Engineering Masterclass

30-day backend engineering curriculum. Principal-engineer depth. One topic per day, 8 interactive visuals each.

## Live now: Week 1 — Networking & APIs
- Day 01: HTTP Deep Dive
- Day 02: TCP/IP & Sockets
- Day 03: DNS & Service Discovery
- Day 04: REST API Design at Scale
- Day 05: Load Balancing Strategies
- Day 06: API Gateway Patterns
- Day 07: gRPC & Protocol Buffers

## Deploy to Vercel

### Option A: Drag and drop (fastest)
1. Go to [vercel.com/new](https://vercel.com/new)
2. Drag this entire folder onto the page
3. Done — Vercel detects static HTML automatically

### Option B: GitHub + Vercel (best for adding new days)
1. Create a new GitHub repo and push this folder
2. Go to [vercel.com/new](https://vercel.com/new), import the repo
3. Framework: **Other** (static HTML, no build step needed)
4. Root directory: `/` (leave as-is)
5. Deploy — every push to main auto-deploys

### Option C: Vercel CLI
```bash
npm i -g vercel
cd masterclass
vercel
```

## Adding new days (Week 2+)
1. Add `dayNN/index.html` to the project
2. Add a rewrite entry to `vercel.json`:
   ```json
   { "source": "/day08", "destination": "/day08/index.html" }
   ```
3. Update the landing `index.html` — change the card from `.locked` to `.live` and add `href="/day08"`
4. Push to GitHub — Vercel deploys automatically

## Project structure
```
masterclass/
├── index.html        ← landing page (curriculum grid)
├── vercel.json       ← routing + headers
├── README.md
├── day01/
│   └── index.html   ← HTTP Deep Dive
├── day02/
│   └── index.html   ← TCP/IP & Sockets
...
└── day07/
    └── index.html   ← gRPC & Protocol Buffers
```
