# INSTRUCCIONES PARA CLAUDE — LEER ANTES DE HACER CUALQUIER COSA

Este es el repositorio de marketing de **KORMAN Etiquetas Bordadas**.
Antes de responder cualquier mensaje, leer los dos archivos base:

1. `KORMAN-CONTEXTO-EMPRESA.md` — todo sobre la empresa, el producto, clientes, identidad visual, banco de fotos
2. `KORMAN-PROYECTO-TRACKER.md` — qué hicimos, qué estamos haciendo, qué sigue

---

## REGLA PRINCIPAL — DOCUMENTAR TODO

**Cada cosa que se haga en este proyecto tiene que quedar escrita en algún doc.**

Después de cada acción relevante (nuevo diseño, nueva estrategia, nueva info de la empresa, nuevo objetivo, nueva decisión):
1. Actualizar el doc correspondiente (`.md`)
2. Regenerar el PDF con `python3 generar_pdfs.py` o `python3 generar_portfolio.py`
3. Hacer commit y push al branch `claude/fervent-lamport-qsc9um`

Nunca dejar algo hecho sin documentarlo. El objetivo es que Tommy pueda abrir un chat nuevo, Claude lea estos archivos, y sepa exactamente todo lo que pasó y lo que sigue.

---

## QUIÉNES SOMOS

**Tommy** (el hijo) gestiona el marketing y trabaja con Claude.
**El papá** (el dueño) aprueba diseños y aporta datos de la empresa.
**Claude** propone, produce y ejecuta. Tommy y el papá aprueban.

---

## ARCHIVOS CLAVE

| Archivo | Para qué |
|---------|----------|
| `KORMAN-CONTEXTO-EMPRESA.md` | Fuente de verdad de la empresa. Leer siempre al arrancar. |
| `KORMAN-PROYECTO-TRACKER.md` | Estado del proyecto, tareas pendientes, log de sesiones. |
| `docs-pdf/` | Versiones PDF de todos los docs (abribles sin Word) |
| `docs-pdf/KORMAN-Portfolio-Produccion.pdf` | Todo lo producido visualmente: logos, posts, fotos |
| `posts_v4/` | Posts de Instagram más recientes (v4 — los aprobados) |
| `assets/fotos-procesadas/` | Fotos de etiquetas con fondo removido (negro, blanco, transparente) |
| `.agents/design/logo/` | Todas las versiones del logo aprobado |
| `.agents/instagram/` | Captions de Instagram listos para publicar |
| `.agents/whatsapp-templates.md` | Templates de respuesta para WhatsApp |
| `.agents/design/philosophy-korman-v3.md` | Filosofía visual "Silencio Textil" — guía de diseño |
| `generar_pdfs.py` | Regenera todos los PDFs de docs |
| `generar_portfolio.py` | Regenera el portfolio visual |

---

## REGLAS DE CONTENIDO — NUNCA OLVIDAR

- **NUNCA publicar precios** — el precio varía siempre. Toda consulta va al WhatsApp.
- La empresa se llama **KORMAN ETIQUETAS** — nunca solo "KORMAN"
- Siempre **"BORDADAS"** — nunca "TEJIDAS"
- Títulos de posts: **MAYÚSCULAS, sin puntos**
- Texto arriba, foto/etiqueta abajo en los posts
- Una sola idea por post
- WhatsApp comercial: https://wa.me/5491144756233
- Instagram: @kormanetiquetas

---

## IDENTIDAD VISUAL

- **Logo:** wordmark puro, BricolageGrotesque Bold, sin ícono
- **Paleta:** #080808 negro · #FCFAF6 blanco roto · #969490 gris cálido
- **Tipografía:** BricolageGrotesque Bold (títulos) + InstrumentSans Regular (subtítulos) + Jura Light (labels)
- **Filosofía:** "Silencio Textil" — espacio como material, museo, autoridad tipográfica. Referencia: Toteme, COS, The Row.
- **Fuentes disponibles en:** `.claude/skills/canvas-design/canvas-fonts/`

---

## BRANCH Y FLUJO DE TRABAJO

- **Branch activo:** `claude/fervent-lamport-qsc9um`
- **PR activo:** https://github.com/tommylopas123-eng/Marketing-y-empresa-/pull/2
- Siempre hacer commit + push después de cada sesión
- Los PDFs se regeneran con los scripts Python del root del repo

---

## LOG DE SESIONES (resumen)

### Sesión 1 — 19/06/2026
- Análisis de competencia con Firecrawl (Printmax, BestLabels, China)
- Perfiles YAML de competidores
- 10 captions de Instagram + 8 templates de WhatsApp
- Página de comparación KORMAN vs China
- Logo v2 aprobado (wordmark BricolageGrotesque Bold)
- 4 posts Instagram generados (v1 y v2 — rechazados)
- Instaladas skills de diseño

### Sesión 2 — 19/06/2026
- Filosofía visual "Silencio Textil" documentada
- 6 posts v4 generados y aprobados (Tafeta, Alta Definición, Triple Densidad, Texturada, 1980, 46 Años)
- Tommy mandó 37 fotos de etiquetas de referencia del taller
- 12 fotos procesadas con remoción de fondo (negro, blanco, transparente)
- Inventario completo de fotos en KORMAN-CONTEXTO-EMPRESA.md
- Todos los docs exportados a PDF
- Portfolio visual generado (logos + posts + fotos)
- Pasos de Instagram API documentados en tracker
- **Regla nueva:** todo lo que se haga se documenta en los docs y se regeneran los PDFs

---

## PRÓXIMOS PASOS (al arrancar el próximo chat)

1. Tommy confirma qué etiqueta va en cada post → incorporar foto real
2. Fotos del taller y máquinas suizas → Tommy las pasa
3. Configurar Instagram API (pasos en el tracker)
4. 6 posts adicionales del batch 2
5. Testimonios de clientes cuando estén disponibles
