// Berea Consulting — mejoras progresivas de navegación.
// El contenido está en el HTML; sin JavaScript la web sigue funcionando.
(function () {
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

  var year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();
