export default function Header({ dark, onToggleDark }) {
  return (
    <header className="header">
      <div className="header-inner">
        <span className="logo">Only News</span>
        <span className="tagline">World news, no noise</span>
        <button className="theme-toggle" onClick={onToggleDark} aria-label="Toggle dark mode">
          {dark ? "☀︎" : "☾"}
        </button>
      </div>
    </header>
  );
}
