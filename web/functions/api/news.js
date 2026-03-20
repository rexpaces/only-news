import { MongoClient, ServerApiVersion } from "mongodb";

let client;

async function getCollection(uri, dbName) {
  if (!client) {
    client = new MongoClient(uri, {
      serverApi: {
        version: ServerApiVersion.v1,
        strict: true,
        deprecationErrors: true,
      },
    });
  }
  await client.connect();
  return client.db(dbName).collection("news");
}

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

  try {
    const col = await getCollection(MONGODB_URI, MONGODB_DATABASE || "only_news");

    const filter = {};
    if (category) filter.category = category;

    const articles = await col
      .find(filter, { projection: { url_hash: 0 } })
      .sort({ published_at: -1 })
      .skip(skip)
      .limit(limit)
      .toArray();

    return new Response(JSON.stringify({ articles }), {
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "public, max-age=300",
      },
    });
  } catch (err) {
    console.error(err);
    return new Response(JSON.stringify({ error: "Database error" }), {
      status: 502,
      headers: { "Content-Type": "application/json" },
    });
  }
}
