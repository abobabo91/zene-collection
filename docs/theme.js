/* Applies the saved theme before first paint and exposes the toggle used by the nav.
   Loaded synchronously in <head> by every page. The choice lives in localStorage under
   `zene-theme` (shared by all three pages: same origin); without one, the system setting wins. */
(function () {
  var KEY = 'zene-theme', root = document.documentElement;
  function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function current() {
    var s = saved();
    if (s === 'light' || s === 'dark') return s;
    return window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function apply() {
    root.setAttribute('data-theme', current());
    window.dispatchEvent(new CustomEvent('zene-theme'));
  }
  window.zeneTheme = {
    current: current,
    toggle: function () {
      try { localStorage.setItem(KEY, current() === 'dark' ? 'light' : 'dark'); } catch (e) {}
      apply();
    }
  };
  root.setAttribute('data-theme', current());
  if (window.matchMedia) matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
    if (!saved()) apply();
  });
})();
