# Berea Consulting — sitio web

Sitio estático con la página de inicio y seis páginas de servicio. Cada página tiene
su propia dirección y es un archivo HTML real, así que puedes abrirla directamente,
recargarla o compartirla y se verá con su propio título, descripción e imagen.

| Página | Dirección | Estado |
|---|---|---|
| Inicio | `/` | Referencia aprobada |
| Selección y Hunting | `/servicios/seleccion-y-hunting/` | Referencia aprobada |
| Evaluación de Talento | `/servicios/evaluacion-de-talento/` | Referencia aprobada |
| Relaciones Laborales | `/servicios/relaciones-laborales/` | Propuesta para revisar |
| Auditoría de RR. HH. | `/servicios/auditoria-rrhh/` | Propuesta para revisar |
| Recupero de Subsidios | `/servicios/recupero-de-subsidios/` | Propuesta para revisar |
| People Analytics | `/servicios/people-analytics/` | Propuesta para revisar |

La página `/revision/` reúne todos los enlaces con su estado para revisarlos.
No aparece en el menú y los buscadores no la indexan.

## Ver el sitio en tu computadora

Necesitas Python 3; no hay que instalar nada más.

```
python server.py
```

Abre http://localhost:8000. Para usar otro puerto: `python server.py 8080`.

## Editar

- **Textos** (títulos, servicios, pasos, entregables, contacto): edita `contenido.json`
  y luego ejecuta `python build.py`. Así se regeneran todas las páginas en `web/`.
  No edites a mano los `index.html`, porque se sobrescriben.
- **Diseño** (colores, tamaños, márgenes): `web/styles.css`. Los colores están al inicio
  del archivo como variables (`--navy`, `--turq`…).
- **Fotos**: reemplaza los archivos en `web/assets/` manteniendo el nombre
  (`foto-0.jpg` … `foto-7.jpg`). En `contenido.json`, cada servicio indica qué foto
  usa (`"foto": 1`) y su texto alternativo (`"foto_alt"`).
- **Logo, favicon e imágenes para redes**: si cambias el logo o las fotos, ejecuta
  `pip install pillow` y luego `python scripts/generar_imagenes.py`. El favicon es un
  recorte del símbolo del logo original (no se redibuja).
- **Contacto**: el correo y WhatsApp están en `"sitio"` dentro de `contenido.json`.
- **Dominio**: `"url"` en `contenido.json` (lo usan los metadatos sociales y el
  sitemap). Hoy es `https://bereaconsulting.net`.

## Estructura

```
contenido.json        textos de todas las páginas (aquí se edita el contenido)
build.py              genera las páginas HTML dentro de web/
server.py             servidor local para revisar
scripts/              generación de favicon e imágenes sociales
referencias/          diseños aprobados (no se publican)
web/                  lo que se publica
  index.html          inicio
  servicios/<slug>/   una carpeta con index.html por servicio
  404.html            página para direcciones inexistentes
  revision/           índice interno de revisión
  styles.css          estilos
  app.js              menú móvil y submenú (el sitio funciona también sin JavaScript)
  assets/             logo, fotos, portada, tipografías, imágenes sociales
  _redirects, _headers, sitemap.xml, robots.txt, favicon
```

Las tipografías (DM Sans y Source Serif 4, licencia OFL) están incluidas en
`web/assets/fonts/`, así que no dependen de Google Fonts.

## Publicar

Hay que publicar solo la carpeta `web/`. Todavía no se ha publicado nada.

- **Netlify**: conecta el repositorio. `netlify.toml` ya indica la carpeta `web`.
- **Cloudflare Pages**: sin comando de compilación y con `web` como directorio de salida.
- **Cualquier otro hosting estático**: sube el contenido de `web/`.

Como cada página existe como archivo, las direcciones directas funcionan sin reglas
especiales. `_redirects` envía `/servicios/` a la sección de servicios del inicio y
las direcciones desconocidas muestran `404.html`. Si publicas en otro dominio,
actualiza `"url"` en `contenido.json` y ejecuta `python build.py`.

El sitio no tiene formulario ni backend: los botones abren WhatsApp
(+51 974 813 983) o el correo (info@bereaconsulting.net).
