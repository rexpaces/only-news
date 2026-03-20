import express from "express";
import { MongoClient } from "mongodb";
import { config } from "dotenv";

config({ path: ".env.local" });

const MONGODB_URI = process.env.MONGODB_URI_LOCAL || "mongodb://localhost:27017";
const DB_NAME = (process.env.MONGODB_DATABASE || "only_news") + "_local";
const PORT = 3001;

const client = new MongoClient(MONGODB_URI);
await client.connect();
const col = client.db(DB_NAME).collection("news");
console.log(`Connected to local MongoDB — db: ${DB_NAME}`);

const app = express();

app.get("/api/news", async (req, res) => {
  try {
    const { category } = req.query;
    const page = Math.max(1, parseInt(req.query.page || "1"));
    const limit = Math.min(50, Math.max(1, parseInt(req.query.limit || "30")));
    const skip = (page - 1) * limit;

    const filter = {};
    if (category) filter.category = category;

    const articles = await col
      .find(filter, { projection: { url_hash: 0, synced: 0 } })
      .sort({ published_at: -1 })
      .skip(skip)
      .limit(limit)
      .toArray();

    res.json({ articles });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Database error" });
  }
});

app.listen(PORT, () => {
  console.log(`Dev API running at http://localhost:${PORT}`);
});
