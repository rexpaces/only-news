import { MongoClient, ServerApiVersion } from "mongodb";

export async function onRequestGet(context) {
  const { MONGODB_URI, MONGODB_DATABASE } = context.env;

  if (!MONGODB_URI) {
    return new Response(JSON.stringify({ error: "Missing MONGODB_URI" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }

  const { searchParams } = new URL(context.request.url);
  const category = searchParams.get("category");
  const page = Math.max(1, parseInt(searchParams.get("page") || "1"));
  const limit = Math.min(50, Math.max(1, parseInt(searchParams.get("limit") || "30")));
  const skip = (page - 1) * limit;

  const client = new MongoClient(MONGODB_URI, {
    serverApi: {
      version: ServerApiVersion.v1,
      deprecationErrors: true,
    },
    connectTimeoutMS: 10000,
    serverSelectionTimeoutMS: 10000,
    socketTimeoutMS: 15000,
  });

  try {
    await client.connect();

    const col = client.db(MONGODB_DATABASE || "only_news").collection("news");

    const filter = {};
    if (category) filter.category = category;

    const docs = await col
      .find(filter, { projection: { url_hash: 0 } })
      .sort({ published_at: -1 })
      .skip(skip)
      .limit(limit)
      .toArray();

    const articles = docs.map((doc) => ({
      ...doc,
      _id: doc._id?.toString(),
    }));

    return new Response(JSON.stringify({ articles }), {
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "public, max-age=300",
      },
    });
  } catch (err) {
    console.error("Worker error:", err?.message ?? err);
    return new Response(
      JSON.stringify({ error: "Database error", detail: err?.message }),
      {
        status: 502,
        headers: { "Content-Type": "application/json" },
      }
    );
  } finally {
    await client.close().catch(() => {});
  }
}
