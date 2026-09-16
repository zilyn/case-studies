(function () {
  // Category filters on the front page.
  var filters = document.querySelectorAll('.filter');
  var entries = document.querySelectorAll('.entry[data-cat]');
  var empty = document.getElementById('empty');
  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var cat = btn.dataset.filter;
      var shown = 0;
      filters.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      entries.forEach(function (el) {
        var show = cat === 'all' || el.dataset.cat === cat;
        el.hidden = !show;
        if (show) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    });
  });

  // The whole card opens the case study, unless a link inside it was clicked.
  document.querySelectorAll('.entry[data-href], .fcard[data-href]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (e.target.closest('a')) return;
      window.location.href = el.dataset.href;
    });
  });

  // Highlight the section in view in the sticky page nav.
  var links = document.querySelectorAll('.subnav a');
  if (links.length && 'IntersectionObserver' in window) {
    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var obs = new IntersectionObserver(function (found) {
      found.forEach(function (en) {
        if (en.isIntersecting) {
          links.forEach(function (a) { a.classList.remove('is-here'); });
          var a = byId[en.target.id];
          if (a) a.classList.add('is-here');
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) obs.observe(el);
    });
  }

  // Theme toggle: system by default, remembered per browser once chosen.
  var toggle = document.getElementById('theme-toggle');
  if (toggle) {
    var root = document.documentElement;
    function current() {
      var set = root.getAttribute('data-theme');
      if (set) return set;
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    function label() {
      toggle.textContent = current() === 'dark' ? 'Light' : 'Dark';
    }
    toggle.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      label();
    });
    label();
  }
})();
