"""Genera las páginas HTML del sitio a partir de contenido.json.

Uso:  python build.py
Escribe en web/: index.html, servicios/<slug>/index.html, 404.html,
revision/index.html, sitemap.xml y robots.txt. Solo usa la biblioteca estándar.
"""
import json
from datetime import date
from html import escape as e
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent
WEB = RAIZ / "web"
DATOS = json.loads((RAIZ / "contenido.json").read_text(encoding="utf-8"))
SITIO = DATOS["sitio"]
INICIO = DATOS["inicio"]
SERVICIOS = DATOS["servicios"]
VERSION = date.today().strftime("%Y%m%d")

# Íconos de línea (24×24, trazo fino), basados en Lucide (licencia ISC).
ICONOS = {
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "file-text": '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "file-search": '<path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M4.27 21a2 2 0 0 0 1.73 1H18a2 2 0 0 0 2-2V7l-5-5H6a2 2 0 0 0-2 2v3"/><path d="m9 18-1.5-1.5"/><circle cx="5" cy="14" r="3"/>',
    "messages": '<path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2z"/><path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/>',
    "list-checks": '<path d="m3 17 2 2 4-4"/><path d="m3 7 2 2 4-4"/><path d="M13 6h8"/><path d="M13 12h8"/><path d="M13 18h8"/>',
    "arrows": '<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/>',
    "folder": '<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "dashboard": '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
    "workflow": '<rect width="8" height="8" x="3" y="3" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><rect width="8" height="8" x="13" y="13" rx="2"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/>',
    "route": '<circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>',
    "trending": '<path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/>',
    "clipboard": '<rect width="8" height="4" x="8" y="2" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "chat": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-left": '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
}


def icono(nombre, clase="icon"):
    return (f'<svg class="{clase}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
            f'{ICONOS[nombre]}</svg>')


FLECHA = icono("arrow-right", "icon arrow")


def url_servicio(s):
    return f"/servicios/{s['slug']}/"


def whatsapp(tema=""):
    texto = f"Hola Berea, quisiera información sobre {tema or 'sus servicios'}."
    return f"https://wa.me/{SITIO['whatsapp']}?text={quote(texto)}"


def enlace_wa(tema, contenido, clase):
    return (f'<a class="{clase}" href="{e(whatsapp(tema))}" target="_blank" rel="noopener">'
            f'{contenido}<span class="sr-only"> (abre WhatsApp)</span></a>')


def foto(n, alt, clase="", ancho=None, prioridad=False, cargar="lazy"):
    w, h = (768, 512) if n < 4 else (752, 464)
    extra = ' fetchpriority="high"' if prioridad else f' loading="{cargar}"'
    return (f'<img class="{clase}" src="/assets/foto-{n}.jpg" alt="{e(alt)}" '
            f'width="{w}" height="{h}" decoding="async"{extra}>')


LOGO = ('<img class="logo" src="/assets/logo.png" alt="Berea Consulting" '
        'width="2044" height="682">')


ACTUAL = ' aria-current="page"'


def cabecera(actual=None, ancla_contacto="#contacto"):
    menu = "".join(
        f'<li><a href="{url_servicio(s)}"{ACTUAL if s is actual else ""}>{e(s["titulo_corto"])}</a></li>'
        for s in SERVICIOS)
    activo = ' class="is-active"' if actual else ""
    return f'''<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="Berea Consulting, ir al inicio">{LOGO}</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu">
      <span class="menu-bars" aria-hidden="true"></span><span class="menu-label">Menú</span>
    </button>
    <nav class="site-nav" id="menu" aria-label="Principal">
      <ul class="nav-list">
        <li class="has-sub">
          <button class="sub-toggle" type="button" aria-expanded="false" aria-controls="submenu"{activo}>Servicios {icono("chevron", "icon chevron")}</button>
          <ul class="submenu" id="submenu">{menu}<li class="submenu-all"><a href="/#servicios">Ver todos los servicios</a></li></ul>
        </li>
        <li><a href="/#enfoque">Nuestro enfoque</a></li>
        <li><a href="{ancla_contacto}">Contacto</a></li>
      </ul>
      {enlace_wa(actual["titulo"] if actual else "", f"Conversemos {FLECHA}", "button button-small nav-cta")}
    </nav>
  </div>
</header>'''


def contacto(titulo, acento, texto, tema="", boton="Contactar a Berea"):
    titulo_html = e(titulo) + (f' <em>{e(acento)}</em>' if acento else "")
    return f'''<section class="contact" id="contacto" aria-labelledby="contacto-titulo">
  <div class="wrap contact-inner">
    <div class="contact-copy">
      <p class="eyebrow eyebrow-line">Hablemos de tu próximo paso</p>
      <h2 id="contacto-titulo">{titulo_html}</h2>
      <p class="contact-text">{e(texto)}</p>
    </div>
    <div class="contact-actions">
      {enlace_wa(tema, f"{icono('chat')} {e(boton)} {FLECHA}", "button")}
      <a class="contact-link" href="mailto:{SITIO["email"]}">{icono("mail")} {SITIO["email"]}</a>
      <a class="contact-link" href="{e(whatsapp(tema))}" target="_blank" rel="noopener">{icono("chat")} WhatsApp {SITIO["whatsapp_visible"]}<span class="sr-only"> (abre WhatsApp)</span></a>
    </div>
  </div>
</section>'''


def pie(servicio=False):
    lista = "".join(f'<li><a href="{url_servicio(s)}">{e(s["titulo_corto"])}</a></li>' for s in SERVICIOS)
    volver = (f'<a class="back-link" href="/#servicios">{icono("arrow-left")} Volver a servicios</a>'
              if servicio else "")
    return f'''<footer class="site-footer">
  <div class="wrap footer-inner">
    <div class="footer-brand">
      <a class="brand" href="/" aria-label="Berea Consulting, ir al inicio">{LOGO}</a>
      <p class="footer-motto">{e(SITIO["lema"])}</p>
    </div>
    <nav class="footer-col" aria-label="Servicios">
      <p class="footer-title">Servicios</p>
      <ul>{lista}</ul>
    </nav>
    <div class="footer-col">
      <p class="footer-title">Contacto</p>
      <ul>
        <li><a href="mailto:{SITIO["email"]}">{SITIO["email"]}</a></li>
        <li><a href="{e(whatsapp())}" target="_blank" rel="noopener">WhatsApp {SITIO["whatsapp_visible"]}<span class="sr-only"> (abre WhatsApp)</span></a></li>
        <li><a href="/#enfoque">Nuestro enfoque</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <small>© <span data-year>{date.today().year}</span> Berea Consulting</small>
    {volver}
  </div>
</footer>'''


def documento(titulo, descripcion, ruta, imagen, cuerpo, actual=None, indexar=True, cuerpo_clase=""):
    url = SITIO["url"] + ruta
    img = SITIO["url"] + imagen
    robots = "" if indexar else '\n<meta name="robots" content="noindex, nofollow">'
    canon = f'\n<link rel="canonical" href="{url}">' if indexar else ""
    datos = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": SITIO["nombre"],
        "url": SITIO["url"] + "/",
        "logo": SITIO["url"] + "/assets/logo.png",
        "email": SITIO["email"],
        "telephone": SITIO["whatsapp_visible"].replace(" ", ""),
    }
    precarga = ('\n<link rel="preload" href="/assets/fonts/source-serif-4.woff2" as="font" type="font/woff2" crossorigin>'
                if cuerpo_clase != "page-home" else "")
    ld = (f'\n<script type="application/ld+json">{json.dumps(datos, ensure_ascii=False)}</script>'
          if ruta == "/" else "")
    return f'''<!doctype html>
<html lang="es" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descripcion)}">{robots}{canon}
<meta name="theme-color" content="#183750">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_PE">
<meta property="og:site_name" content="Berea Consulting">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Logo de Berea Consulting junto a una fotografía del servicio">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(titulo)}">
<meta name="twitter:description" content="{e(descripcion)}">
<meta name="twitter:image" content="{img}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/dm-sans.woff2" as="font" type="font/woff2" crossorigin>{precarga}
<link rel="stylesheet" href="/styles.css?v={VERSION}">
<script>document.documentElement.classList.remove('no-js');document.documentElement.classList.add('js')</script>{ld}
</head>
<body class="{cuerpo_clase}">
<a class="skip-link" href="#contenido">Ir al contenido</a>
{cabecera(actual, "#contacto" if indexar else "/#contacto")}
<main id="contenido" tabindex="-1">
{cuerpo}
</main>
{pie(servicio=actual is not None)}
<script src="/app.js?v={VERSION}" defer></script>
</body>
</html>
'''


def items_iconos(items, clase):
    return "".join(
        f'<li class="{clase}">{icono(ic)}<div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>'
        for t, d, ic in items)


def pagina_inicio():
    i = INICIO
    pilares = items_iconos(i["pilares"], "pillar")
    tarjetas = "".join(f'''<li class="card">
        <a class="card-link" href="{url_servicio(s)}">
          <span class="card-media">{foto(s["foto"], "", "card-img")}</span>
          <span class="card-body">
            {icono(s["icono"])}
            <span class="card-text">
              <span class="card-title">{e(s["titulo_corto"])}</span>
              <span class="card-desc">{e(s["tarjeta"])}</span>
              <span class="card-more">Explorar servicio {FLECHA}</span>
            </span>
          </span>
        </a>
      </li>''' for s in SERVICIOS)
    enfoque = "".join(
        f'<li><span class="step-number">{n:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>'
        for n, (t, d) in enumerate(i["enfoque"], 1))
    cuerpo = f'''<section class="hero hero-home" aria-labelledby="titulo">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow eyebrow-line">{e(i["eyebrow"])}</p>
      <h1 id="titulo">{e(i["titulo"])} <em>{e(i["titulo_acento"])}</em></h1>
      <p class="lead">{e(i["lead"])}</p>
      <a class="button" href="#servicios">{e(i["boton"])} {FLECHA}</a>
    </div>
    <figure class="hero-art">
      <img src="/assets/portada-tech.png" alt="{e(i["portada_alt"])}" width="574" height="456" fetchpriority="high">
    </figure>
  </div>
</section>

<section class="pillars" aria-label="Lo que hacemos">
  <ul class="wrap pillar-list">{pilares}</ul>
</section>

<section class="section" id="servicios" aria-labelledby="servicios-titulo">
  <div class="wrap">
    <div class="section-head split">
      <div>
        <p class="eyebrow eyebrow-line">{e(i["servicios_eyebrow"])}</p>
        <h2 id="servicios-titulo">{e(i["servicios_titulo"])} <em>{e(i["servicios_acento"])}</em></h2>
      </div>
      <p class="section-intro">{e(i["servicios_intro"])}</p>
    </div>
    <ul class="cards">{tarjetas}</ul>
  </div>
</section>

<section class="section section-tint" id="enfoque" aria-labelledby="enfoque-titulo">
  <div class="wrap">
    <div class="section-head split">
      <div>
        <p class="eyebrow eyebrow-line">{e(i["enfoque_eyebrow"])}</p>
        <h2 id="enfoque-titulo">{e(i["enfoque_titulo"])}</h2>
      </div>
      <p class="section-intro">{e(i["enfoque_intro"])}</p>
    </div>
    <ol class="steps steps-3">{enfoque}</ol>
    <p class="aside-note">{e(i["complementarias"])} {enlace_wa("soluciones complementarias", f"Consulta el alcance {FLECHA}", "text-link")}</p>
  </div>
</section>

{contacto(i["contacto_titulo"], i["contacto_acento"], i["contacto_texto"])}'''
    return documento(
        "Berea Consulting | Talento, gestión laboral y People Analytics",
        SITIO["descripcion"], "/", "/assets/social/inicio.jpg", cuerpo, cuerpo_clase="page-home")


def pagina_servicio(s):
    enfoque = items_iconos(s["enfoque"], "feature")
    pasos = "".join(
        f'<li><span class="step-number">{n:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>'
        for n, (t, d) in enumerate(s["proceso"], 1))

    usos = ""
    if s.get("usos"):
        lista = items_iconos(s["usos"], "use")
        if s.get("usos_foto") is not None:
            usos = f'''<section class="uses has-photo" aria-labelledby="usos-titulo">
  <div class="uses-copy">
    <h2 id="usos-titulo">{e(s["usos_titulo"])}</h2>
    <ul class="use-list">{lista}</ul>
  </div>
  <div class="uses-media">{foto(s["usos_foto"], s["usos_foto_alt"], "media-img")}</div>
</section>'''
        else:
            usos = f'''<section class="section uses-plain" aria-labelledby="usos-titulo">
  <div class="wrap">
    <h2 id="usos-titulo">{e(s["usos_titulo"])}</h2>
    <ul class="use-list use-cols">{lista}</ul>
  </div>
</section>'''

    nota = f'<p class="note">{e(s["nota"])}</p>' if s.get("nota") else ""
    if s.get("entregables_foto") is not None:
        lista = "".join(f'<li>{icono(ic)}<span>{e(t)}</span></li>' for t, ic in s["entregables"])
        entregables = f'''<section class="deliverables has-photo" aria-labelledby="entregables-titulo">
  <div class="deliverables-media">{foto(s["entregables_foto"], s["entregables_foto_alt"], "media-img")}</div>
  <div class="deliverables-copy">
    <p class="eyebrow">Entregables</p>
    <h2 id="entregables-titulo">{e(s["entregables_titulo"])}</h2>
    <ul class="deliverable-list">{lista}</ul>
    {nota}
  </div>
</section>'''
    else:
        lista = "".join(f'<li>{icono(ic)}<span>{e(t)}</span></li>' for t, ic in s["entregables"])
        entregables = f'''<section class="section deliverables-row" aria-labelledby="entregables-titulo">
  <div class="wrap">
    <p class="eyebrow">Entregables</p>
    <h2 id="entregables-titulo">{e(s["entregables_titulo"])}</h2>
    <ul class="deliverable-row">{lista}</ul>
    {nota}
  </div>
</section>'''

    cuerpo = f'''<section class="hero hero-service" aria-labelledby="titulo">
  <div class="hero-service-media">{foto(s["foto"], s["foto_alt"], "hero-img", prioridad=True)}</div>
  <div class="wrap">
    <div class="hero-copy">
      <nav class="breadcrumb" aria-label="Ruta de navegación">
        <ol><li><a href="/">Inicio</a></li><li><a href="/#servicios">Servicios</a></li><li><span aria-current="page">{e(s["titulo"])}</span></li></ol>
      </nav>
      <h1 id="titulo">{e(s["titulo"])}</h1>
      <p class="subtitle">{e(s["frase"])}</p>
      <p class="hero-text">{e(s["descripcion"])}</p>
      {enlace_wa(s["titulo"], f"{e(s['boton'])} {FLECHA}", "button")}
    </div>
  </div>
</section>

<section class="section features-section" aria-labelledby="enfoque-titulo">
  <div class="wrap">
    <h2 id="enfoque-titulo">{e(s["enfoque_titulo"])}</h2>
    <ul class="features">{enfoque}</ul>
  </div>
</section>

{usos}

<section class="section section-tint" aria-labelledby="proceso-titulo">
  <div class="wrap">
    <p class="eyebrow">Nuestro proceso</p>
    <h2 id="proceso-titulo">{e(s["proceso_titulo"])}</h2>
    <ol class="steps">{pasos}</ol>
  </div>
</section>

{entregables}

{contacto(s["contacto_titulo"], "", s["contacto_texto"], s["titulo"], s["contacto_boton"])}'''
    return documento(
        f'{s["titulo"]} | Berea Consulting', s["descripcion"], url_servicio(s),
        f'/assets/social/{s["slug"]}.jpg', cuerpo, actual=s, cuerpo_clase="page-service")


def pagina_404():
    cuerpo = '''<section class="section notfound">
  <div class="wrap">
    <p class="eyebrow">Error 404</p>
    <h1>No encontramos esta página.</h1>
    <p class="lead">Es posible que la dirección haya cambiado. Puedes volver al inicio o revisar nuestros servicios.</p>
    <p class="notfound-actions"><a class="button" href="/">Volver al inicio</a> <a class="text-link" href="/#servicios">Ver servicios</a></p>
  </div>
</section>'''
    return documento("Página no encontrada | Berea Consulting", SITIO["descripcion"], "/404.html",
                     "/assets/social/inicio.jpg", cuerpo, indexar=False, cuerpo_clase="page-404")


def pagina_revision():
    filas = [("Inicio", "/", "aprobada", "referencias/inicio.png")]
    for s in SERVICIOS:
        ref = {"seleccion-y-hunting": "referencias/seleccion.png",
               "evaluacion-de-talento": "referencias/evaluacion.png"}.get(s["slug"], "—")
        filas.append((s["titulo"], url_servicio(s), s["estado"], ref))
    lista = "".join(
        f'<tr><td><a href="{u}">{e(t)}</a></td><td><code>{u}</code></td>'
        f'<td><span class="tag tag-{est}">{"Referencia aprobada" if est == "aprobada" else "Propuesta para revisar"}</span></td>'
        f'<td>{e(r)}</td></tr>' for t, u, est, r in filas)
    cuerpo = f'''<section class="section review">
  <div class="wrap">
    <p class="eyebrow">Uso interno · no indexada</p>
    <h1>Revisión de páginas</h1>
    <p class="lead">Abre cada página para revisarla. Las marcadas como propuesta siguen la línea de las referencias aprobadas y esperan tus comentarios.</p>
    <div class="table-scroll"><table>
      <thead><tr><th scope="col">Página</th><th scope="col">Dirección</th><th scope="col">Estado</th><th scope="col">Referencia</th></tr></thead>
      <tbody>{lista}</tbody>
    </table></div>
    <p class="note">Para cambiar textos edita <code>contenido.json</code> y ejecuta <code>python build.py</code>.</p>
  </div>
</section>'''
    return documento("Revisión de páginas | Berea Consulting", "Listado interno de páginas para revisión.",
                     "/revision/", "/assets/social/inicio.jpg", cuerpo, indexar=False, cuerpo_clase="page-review")


def escribir(ruta, contenido):
    destino = WEB / ruta
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8")
    print("  ", destino.relative_to(RAIZ))


def main():
    print("Generando páginas:")
    escribir("index.html", pagina_inicio())
    for s in SERVICIOS:
        escribir(f"servicios/{s['slug']}/index.html", pagina_servicio(s))
    escribir("404.html", pagina_404())
    escribir("revision/index.html", pagina_revision())
    urls = ["/"] + [url_servicio(s) for s in SERVICIOS]
    escribir("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
             + "".join(f"  <url><loc>{SITIO['url']}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    escribir("robots.txt", f"User-agent: *\nDisallow: /revision/\n\nSitemap: {SITIO['url']}/sitemap.xml\n")


if __name__ == "__main__":
    main()
