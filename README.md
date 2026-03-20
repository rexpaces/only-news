# Only News

**Live demo: [https://main.only-news.pages.dev](https://main.only-news.pages.dev)**

A minimal worldwide news aggregator. No ads, no algorithms, no noise — just a clean list of the latest news with short titles and descriptions, filterable by category and region.

---

## What it does

- Displays the most recent news from sources around the world
- Covers global categories: World, Politics, Tech, Science, Sports, Business
- Covers regional news from major cities across all continents
- Users can filter by category and click any headline to open the original article

---

## Architecture

```
┌─────────────────────────────────────┐
│          LOCAL (your machine)        │
│                                      │
│  RSS Feeds → Collector (Python)      │
│       ↓                              │
│  Ollama (gemma3:12b)                 │
│  - generates short title             │
│  - generates short description       │
│  - classifies category               │
│       ↓                              │
│  Local MongoDB (buffer)              │
│       ↓ (after full run)             │
│  Sync → Remote MongoDB Atlas         │
└─────────────────────────────────────┘
                  ↑ reads
┌─────────────────────────────────────┐
│           CLOUDFLARE                 │
│                                      │
│  Pages → serves React frontend       │
│  Pages Functions → /api/news         │
│    connects to MongoDB Atlas         │
│    returns filtered, paginated news  │
└─────────────────────────────────────┘
```

### Data collection (runs locally, daily)

A Python script fetches RSS feeds from sources like BBC, Al Jazeera, The Guardian, TechCrunch, and Google News (per city). Each article is sent to a local **Ollama** instance running **gemma3:12b**, which generates a short title, a short description, and classifies the article into a category — all without any paid API.

Articles are saved to a **local MongoDB** instance as a buffer. Once the full collection run is complete, all new articles are bulk-synced to **MongoDB Atlas** (free M0 tier) in the cloud.

A daily cron job keeps the database fresh automatically.

### Website (always on)

The frontend is a React app deployed to **Cloudflare Pages** (free tier). The API is a Cloudflare Pages Function that connects directly to MongoDB Atlas using the standard MongoDB driver over TCP. No middleware, no backend server to manage.

---

## Setup

### 1. MongoDB Atlas

1. Create a free account at [cloud.mongodb.com](https://cloud.mongodb.com)
2. Create a new **M0 free cluster** (any region)
3. Go to **Database Access** → create a database user with a password
4. Go to **Network Access** → click **Add IP Address** → **Allow Access from Anywhere** (`0.0.0.0/0`)
5. Go to **Database** → click **Connect** → **Drivers** → copy your connection string:
   ```
   mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/?appName=Cluster0
   ```
6. Create a database named `only_news` with a collection named `news`
7. Add the following indexes to the `news` collection:
   - `{ url_hash: 1 }` — unique
   - `{ published_at: -1 }`
   - `{ category: 1 }`

---

### 2. Install the project

```bash
git clone <your-repo-url>
cd only-news
```

#### Python collector

```bash
cd collector
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
MONGODB_URI=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/?appName=Cluster0
MONGODB_URI_LOCAL=mongodb://localhost:27017
MONGODB_DATABASE=only_news
```

#### Web app

```bash
cd web
npm install
```

---

### 3. Run the collector

Make sure local MongoDB and Ollama are running, then:

```bash
cd collector
source .venv/bin/activate
python main.py
```

The collector will:
1. Fetch RSS feeds from all sources
2. Process each article through Ollama (title, description, category)
3. Save to local MongoDB
4. Bulk sync to MongoDB Atlas when done

#### Schedule it daily with cron

```bash
crontab -e
```

Add this line (runs every day at 6am):

```
0 6 * * * cd /path/to/only-news/collector && .venv/bin/python main.py >> /tmp/only-news.log 2>&1
```

---

### 4. Test locally

Make sure local MongoDB is running, then:

```bash
cd web
npm run dev:local
```

Open [http://localhost:5173](http://localhost:5173).

This starts:
- A local Express API server on `:3001` reading from your local MongoDB
- The Vite dev server on `:5173` proxying `/api` requests to it

---

### 5. Deploy to Cloudflare

#### Install and log in to Wrangler

```bash
npm install -g wrangler
wrangler login --no-browser
```

#### Set your MongoDB URI as a secret

```bash
cd web
wrangler pages secret put MONGODB_URI --project-name only-news
```

Paste your full Atlas connection string when prompted.

Alternatively, set it from the Cloudflare dashboard:
**Workers & Pages → only-news → Settings → Environment Variables → Add variable (Production)**

#### Build and deploy

```bash
cd web
npm run build
wrangler pages deploy
```

Your site will be live at `https://only-news.pages.dev` (or the alias Cloudflare assigns).

#### Subsequent deploys

```bash
cd web
npm run build && wrangler pages deploy
```

---

## Stack

| Layer | Technology |
|---|---|
| Data collection | Python, feedparser, Ollama (gemma3:12b) |
| Local buffer | MongoDB (local) |
| Remote database | MongoDB Atlas M0 (free) |
| Frontend | React + Vite |
| Hosting | Cloudflare Pages (free) |
| API | Cloudflare Pages Functions |
