// Berea Consulting — mejoras progresivas de navegación.
// El contenido está en el HTML; sin JavaScript la web sigue funcionando.
(function () {
  // Al entrar a una página (por ejemplo, un servicio) se empieza siempre arriba.
  // Se respeta la posición al volver atrás y cuando el enlace apunta a una sección (#).
  var navEntry = window.performance && performance.getEntriesByType ? performance.getEntriesByType('navigation')[0] : null;
  if (!location.hash && !(navEntry && navEntry.type === 'back_forward')) {
    var userMoved = false;
    ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (t) {
      window.addEventListener(t, function () { userMoved = true; }, { once: true, passive: true });
    });
    var toTop = function () {
      if (userMoved) return;
      try { window.scrollTo({ top: 0, left: 0, behavior: 'instant' }); } catch (e) { window.scrollTo(0, 0); }
      if (window.self !== window.top) document.documentElement.scrollIntoView({ block: 'start' });
    };
    toTop();
    window.addEventListener('load', toTop);
    [80, 300, 700].forEach(function (ms) { setTimeout(toTop, ms); });
  }

  var header = document.querySelector('.site-header');
  var nav = document.getElementById('menu');
  var menuBtn = document.querySelector('.menu-toggle');
  var sub = document.querySelector('.has-sub');
  var subBtn = sub && sub.querySelector('.sub-toggle');

  function setMenu(open) {
    if (!menuBtn) return;
    menuBtn.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    if (!open) setSub(false);
  }
  function setSub(open) {
    if (!subBtn) return;
    subBtn.setAttribute('aria-expanded', String(open));
    sub.classList.toggle('is-open', open);
  }

  menuBtn && menuBtn.addEventListener('click', function () {
    setMenu(menuBtn.getAttribute('aria-expanded') !== 'true');
  });
  subBtn && subBtn.addEventListener('click', function () {
    setSub(subBtn.getAttribute('aria-expanded') !== 'true');
  });

  // Cerrar con Escape y devolver el foco al botón que abrió el menú.
  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape') return;
    if (sub && sub.classList.contains('is-open')) { setSub(false); subBtn.focus(); }
    else if (nav.classList.contains('is-open')) { setMenu(false); menuBtn.focus(); }
  });

  // Cerrar al hacer clic fuera o al salir del submenú con el teclado.
  document.addEventListener('click', function (ev) {
    if (sub && !sub.contains(ev.target)) setSub(false);
    if (!header.contains(ev.target)) setMenu(false);
  });
  sub && sub.addEventListener('focusout', function (ev) {
    if (ev.relatedTarget && !sub.contains(ev.relatedTarget)) setSub(false);
  });

  // Los enlaces a secciones de la misma página cierran el menú móvil.
  nav.addEventListener('click', function (ev) {
    var a = ev.target.closest('a');
    if (a && a.hash && a.pathname === location.pathname) setMenu(false);
  });

  // Borde inferior de la cabecera al desplazarse.
  var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Aparición suave de secciones al desplazarse. Solo se ocultan elementos que
  // todavía no están en pantalla, así que nada visible desaparece al cargar.
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce && 'IntersectionObserver' in window) {
    var grupos = [
      '.section-head', '.features-section > .wrap > h2', '.uses-copy > h2', '.uses-plain > .wrap > h2',
      '.section-tint > .wrap > .eyebrow', '.section-tint > .wrap > h2', '.deliverables-row > .wrap > :not(ul)',
      '.deliverables-copy > *', '.card', '.pillar', '.feature', '.use', '.steps > li',
      '.deliverable-row > li', '.aside-note', '.contact-copy', '.contact-actions', '.uses-media', '.deliverables-media'
    ];
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    var limite = window.innerHeight * 0.92;
    document.querySelectorAll(grupos.join(',')).forEach(function (el) {
      if (el.getBoundingClientRect().top < limite) return;
      var hermanos = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.style.setProperty('--d', Math.min(hermanos, 5) * 0.09 + 's');
      el.classList.add('reveal');
      io.observe(el);
    });
  }

  var year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();
