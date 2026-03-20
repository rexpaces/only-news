import { useState, useEffect, useCallback } from "react";
import Header from "./components/Header";
import CategoryFilter from "./components/CategoryFilter";
import NewsList from "./components/NewsList";

const CATEGORIES = [
  "All",
  "World",
  "Politics",
  "Tech",
  "Science",
  "Sports",
  "Business",
  "Regional",
];
const PAGE_SIZE = 30;

export default function App() {
  const [news, setNews] = useState([]);
  const [category, setCategory] = useState("All");
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [dark, setDark] = useState(
    () => localStorage.getItem("theme") === "dark" ||
      (!localStorage.getItem("theme") && window.matchMedia("(prefers-color-scheme: dark)").matches)
  );

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
    localStorage.setItem("theme", dark ? "dark" : "light");
  }, [dark]);

  const fetchNews = useCallback(async (cat, pg) => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ page: pg, limit: PAGE_SIZE });
      if (cat !== "All") params.set("category", cat);
      const res = await fetch(`/api/news?${params}`);
      if (!res.ok) throw new Error("Failed to fetch");
      const data = await res.json();
      if (pg === 1) {
        setNews(data.articles);
      } else {
        setNews((prev) => [...prev, ...data.articles]);
      }
      setHasMore(data.articles.length === PAGE_SIZE);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    setPage(1);
    fetchNews(category, 1);
  }, [category, fetchNews]);

  const loadMore = () => {
    const next = page + 1;
    setPage(next);
    fetchNews(category, next);
  };

  return (
    <div className="app">
      <Header dark={dark} onToggleDark={() => setDark((d) => !d)} />
      <main>
        <CategoryFilter
          categories={CATEGORIES}
          active={category}
          onChange={(cat) => {
            setCategory(cat);
            setPage(1);
          }}
        />
        <NewsList
          news={news}
          loading={loading}
          hasMore={hasMore}
          onLoadMore={loadMore}
        />
      </main>
    </div>
  );
}
