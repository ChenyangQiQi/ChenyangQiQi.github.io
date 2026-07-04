// ---- dark mode ----
(function () {
  const btn = document.getElementById('themeToggle');
  const root = document.documentElement;
  let saved = null;
  try { saved = localStorage.getItem('theme'); } catch (e) {}
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  apply(saved || (prefersDark ? 'dark' : 'light'));
  if (btn) btn.addEventListener('click', function () {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    apply(next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });
  function apply(theme) {
    root.setAttribute('data-theme', theme);
    if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
  }
})();

// ---- footer year ----
(function () {
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
