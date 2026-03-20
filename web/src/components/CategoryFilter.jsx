export default function CategoryFilter({ categories, active, onChange }) {
  return (
    <nav className="category-filter" aria-label="Filter by category">
      {categories.map((cat) => (
        <button
          key={cat}
          className={`cat-btn${active === cat ? " active" : ""}`}
          onClick={() => onChange(cat)}
          aria-pressed={active === cat}
        >
          {cat}
        </button>
      ))}
    </nav>
  );
}
