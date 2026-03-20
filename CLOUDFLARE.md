# Deploying to Cloudflare

## Prerequisites

- [Node.js](https://nodejs.org) installed
- A [Cloudflare account](https://dash.cloudflare.com/sign-up) (free)
- Your MongoDB Atlas connection string (the `mongodb+srv://...` one)

---

## 1. Install Wrangler and log in

```bash
npm install -g wrangler
wrangler login --no-browser
```

---

## 2. Set your MongoDB connection string as a secret

```bash
cd web
wrangler secret put MONGODB_URI
```

When prompted, paste your full connection string with your real password:

```
mongodb+srv://vmvini:<your_password>@cluster0.qsuqzb6.mongodb.net/?appName=Cluster0
```

---

## 3. Allow Cloudflare IPs in Atlas

By default Atlas blocks all connections. You need to allow Cloudflare's outbound IPs.

The simplest option for a personal project:

1. In Atlas, go to **Security → Network Access**
2. Click **Add IP Address**
3. Click **Allow Access from Anywhere** (`0.0.0.0/0`)
4. Click **Confirm**

> If you want stricter access, Cloudflare publishes their IP ranges at
> https://www.cloudflare.com/ips/ — you can add each range instead.

---

## 4. Build and deploy

```bash
cd web
npm install
npm run build
wrangler pages deploy dist --project-name only-news
```

On first deploy, Wrangler creates the project on Cloudflare Pages.
Your site will be live at:

```
https://only-news.pages.dev
```

---

## 5. Subsequent deploys

```bash
npm run build
wrangler pages deploy dist --project-name only-news
```

---

## Environment variables reference

| Secret | Value |
|---|---|
| `MONGODB_URI` | Your full `mongodb+srv://...` connection string |

The `MONGODB_DATABASE` variable defaults to `only_news` and is already set in `wrangler.toml`.
