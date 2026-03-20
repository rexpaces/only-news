import NewsCard from "./NewsCard";

export default function NewsList({ news, loading, hasMore, onLoadMore }) {
  if (!loading && news.length === 0) {
    return <p className="empty">No news found.</p>;
  }

  return (
    <section className="news-section">
      <div className="news-list">
        {news.map((item) => (
          <NewsCard key={item._id} item={item} />
        ))}
      </div>
      {loading && <p className="status-msg">Loading...</p>}
      {!loading && hasMore && (
        <button className="load-more" onClick={onLoadMore}>
          Load more
        </button>
      )}
      {!loading && !hasMore && news.length > 0 && (
        <p className="status-msg">All caught up.</p>
      )}
    </section>
  );
}
