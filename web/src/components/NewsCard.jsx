export default function NewsCard({ item }) {
  return (
    <article className="news-card">
      <div className="card-meta">
        <span className="badge badge-category">{item.category}</span>
        {item.region && item.region !== "Global" && (
          <span className="badge badge-region">{item.region}</span>
        )}
        <span className="card-source">{item.source}</span>
        <span className="card-date">{formatDate(item.published_at)}</span>
      </div>
      <a
        href={item.url}
        target="_blank"
        rel="noopener noreferrer"
        className="card-title"
      >
        {item.title}
      </a>
      {item.description && (
        <p className="card-desc">{item.description}</p>
      )}
    </article>
  );
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  try {
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  } catch {
    return "";
  }
}
