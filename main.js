// Mobile menu
(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();

// Background: sample paths of a self-exciting jump process (Hawkes-style),
// a nod to the cyber-contagion and credit-loss models of the research.
(function () {
  var svgs = document.querySelectorAll('svg.paths');
  if (!svgs.length) return;
  var NS = 'http://www.w3.org/2000/svg';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function rng(seed) {
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function gauss(r) { var u = r() || 1e-9, v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }

  svgs.forEach(function (svg, k) {
    var W = 1200, H = 300, N = 240, n = +(svg.dataset.n || 6);
    var animate = svg.dataset.animate === 'true' && !reduce;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('preserveAspectRatio', 'none');
    var r = rng(20240917 + k);
    for (var i = 0; i < n; i++) {
      var y = H * 0.82, lam = 0.012, pts = [], jumps = [];
      for (var s = 0; s <= N; s++) {
        var x = s / N * W;
        y -= 0.35 + gauss(r) * 3.2 * 0.6;          // drift + diffusion (upwards = rising losses)
        if (r() < lam) {                             // jump; excitation raises the intensity
          var J = 10 + r() * 26, y0 = y; y -= J; lam += 0.05; jumps.push([x, y0, y]);
        }
        lam = 0.012 + (lam - 0.012) * 0.93;          // exponential decay of excitation
        y = Math.max(8, Math.min(H - 4, y));
        pts.push(x.toFixed(1) + ',' + y.toFixed(1));
      }
      var p = document.createElementNS(NS, 'polyline');
      p.setAttribute('points', pts.join(' '));
      p.setAttribute('class', 'p ' + (i === 0 ? 'lead' : 'c' + ((i - 1) % 4)));
      svg.appendChild(p);
      if (i === 0) {
        jumps.forEach(function (j) {
          var c = document.createElementNS(NS, 'line');
          c.setAttribute('x1', j[0]); c.setAttribute('x2', j[0]);
          c.setAttribute('y1', Math.min(H - 4, j[1])); c.setAttribute('y2', Math.max(8, j[2]));
          c.setAttribute('class', 'jump');
          svg.appendChild(c);
        });
      }
      if (animate) {
        var L = p.getTotalLength ? p.getTotalLength() : 3000;
        p.style.strokeDasharray = L; p.style.strokeDashoffset = L;
        p.animate([{ strokeDashoffset: L }, { strokeDashoffset: 0 }],
          { duration: 2200 + i * 180, delay: i * 90, easing: 'cubic-bezier(.3,.6,.2,1)', fill: 'forwards' });
      }
    }
    if (animate) {
      svg.querySelectorAll('.jump').forEach(function (c) {
        c.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 400, delay: 2100, fill: 'both' });
      });
    }
  });
})();

// Topic filters (publications, talks)
(function () {
  var bar = document.querySelector('.filters');
  if (!bar) return;
  var buttons = bar.querySelectorAll('button');
  bar.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    var f = b.dataset.f;
    buttons.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    document.querySelectorAll('[data-topics]').forEach(function (li) {
      li.classList.toggle('hidden', f !== 'all' && (' ' + li.dataset.topics + ' ').indexOf(' ' + f + ' ') < 0);
    });
    document.querySelectorAll('main section').forEach(function (sec) {
      var items = sec.querySelectorAll('[data-topics]');
      if (!items.length) return;
      sec.classList.toggle('hidden', !sec.querySelector('[data-topics]:not(.hidden)'));
    });
  });
})();
