# KORMAN — Tracker del proyecto
*Qué hicimos, qué estamos haciendo, qué sigue.*
*Última actualización: 19/06/2026*

---

## ESTADO ACTUAL: FASE 1 — FUNDAMENTOS

Estamos construyendo la base de marketing de KORMAN desde cero:
identidad visual, contenido estratégico e infraestructura de comunicación.

---

## ✅ HECHO

### Investigación y estrategia
- [x] **Contexto de empresa documentado** — product-marketing.md con toda la info confirmada con el dueño
- [x] **Análisis de competencia** — scraping real con Firecrawl de Printmax, BestLabels, MercadoLibre. Identificados mínimos, precios y debilidades de cada uno.
- [x] **Perfiles YAML de competidores** — Printmax, BestLabels, China. Fuente de verdad centralizada.

### Identidad visual
- [x] **Logo/emblema KORMAN aprobado (foto de perfil)** — emblema hexagonal estilo "casa": hexágono negro, techo dorado, **K** grande blanca, **aguja plateada** atravesando en diagonal con ojo e hilo. Archivo oficial: `assets/korman-logo-oficial.jpg` (= `assets/korman-instagram-profile.jpg`). Versión elegida: hilo plata. *Tentativo — se puede revisar el color del hilo más adelante.*
- [x] **Logo KORMAN wordmark** — wordmark puro, BricolageGrotesque Bold, negro/blanco, sin ícono (uso secundario)
- [x] **5 versiones del logo** — horizontal blanco, horizontal negro, avatar IG, watermarks transparentes
- [x] **Filosofía visual "Hilo Nocturno"** — oscuro, dorado, patrones de tejido, editorial
- [x] **4 posts Instagram generados** (1080×1080, 300dpi):
  - Post 01: "Tu marca, bordada."
  - Post 02: "Sin mínimos altos."
  - Post 03: "Cada punto, tu marca." (proceso)
  - Post 04: Local vs China (contraste)

### Contenido y copy
- [x] **10 captions de Instagram listos** con hashtags (batch-01-diferenciadores.md)
- [x] **8 templates de WhatsApp** para convertir consultas en pedidos
- [x] **Página de comparación** "KORMAN vs Importar desde China" (copy completo)
- [x] **Calendario de publicación** — 4 semanas, 2-3 posts/semana

### Skills y herramientas instaladas
- [x] Firecrawl (key: fc-ac31b92675104b058d606ba05a30977a) — verificada y funcionando
- [x] canvas-design, theme-factory, image-enhancer, brand-guidelines (de awesome-claude-skills)
- [x] Scripts Python reutilizables para generar posts y logos

---

## 🔄 EN PROGRESO

- [ ] **Procesar fotos de etiquetas** — remover fondos, mejorar calidad → guardar en `assets/fotos-procesadas/`
- [ ] **Incorporar fotos a posts v4** — reemplazar placeholders con las 8 mejores fotos procesadas
- [ ] **Fotos del taller y máquinas** → Tommy las pasa después

---

## 📋 PRÓXIMO — FASE 1 (completar fundamentos)

### Esta semana
- [ ] **Tommy decide qué etiqueta va en cada post** → Claude incorpora la foto real al post v4
- [ ] **6 posts visuales restantes** del batch (educativo tipos de tejido, regalos/bebé, urgencia/temporada, antes/después, prueba social con clientes, objeción precio)
- [ ] **Fotos del taller y máquinas suizas** → Tommy las pasa cuando pueda

### Perfil de Instagram — ✅ CONFIGURADO (19/06/2026)
- [x] **Foto de perfil** — emblema oficial (casa negra, techo dorado, K blanca, aguja plata)
- [x] **Nombre** — KORMAN Etiquetas
- [x] **Bio** — "Tu marca, bordada con calidad profesional / 46 años de oficio / WhatsApp 👇"
- [x] **Categoría** — Textile Company
- [x] **Cuenta profesional** activada
- [x] **Link de WhatsApp con mensaje automático** — `https://wa.me/5491144756233?text=Hola+quiero+informacion+de+las+etiquetas` (link largo; se puede acortar más adelante con acortar.link cuando se quiera ver más prolijo)

### Configurar Instagram API (pasos para Tommy)
- [ ] **Paso 1:** Convertir @kormanetiquetas a cuenta Business en la app de Instagram (Configuración → Cuenta → Cambiar a cuenta profesional → Empresa)
- [ ] **Paso 2:** Crear una Página de Facebook y vincularla a la cuenta de Instagram
- [ ] **Paso 3:** Entrar a developers.facebook.com → Crear app → Tipo "Business" → Agregar producto "Instagram Graph API"
- [ ] **Paso 4:** Generar token de acceso y pasárselo a Claude
- [ ] **Paso 5:** Claude programa y publica los posts automáticamente desde ahí
- *TikTok API no disponible para cuentas chicas — publicar manualmente por ahora*

### Política de precios (confirmado, no cambiar)
- ❌ **Nunca publicar precio** — varía siempre por diseño, tejido, tamaño, terminación y cantidad
- ✅ Toda consulta de precio → derivar al WhatsApp a cotizar individualmente

### Cuando tengamos testimonios
- [ ] **Post de prueba social** con citas de clientes
- [ ] **Stories highlight** de marcas que confiaron en KORMAN

---

## 🗓️ FASE 2 — CRECIMIENTO (próximas semanas)

### Instagram
- [ ] Definir frecuencia de publicación (recomendación: 4-5 posts/semana)
- [ ] Crear plantilla de Stories (encuestas, "antes/después", "¿sabías que?")
- [ ] Plan de Reels — guion y estructura para videos del proceso
- [ ] Estrategia de hashtags por tipo de post
- [ ] Responder comentarios y DMs con los templates de WA

### Contenido SEO
- [ ] Publicar página "KORMAN vs Importar desde China"
- [ ] Segunda página de comparación: "KORMAN vs etiquetas genéricas"
- [ ] Blog/nota: "Cómo elegir la etiqueta para tu marca de ropa"
- [ ] Guía: "Tipos de etiquetas tejidas — cuál es la indicada para tu proyecto"

### Captación de clientes
- [ ] Definir estrategia de outreach: DMs a emprendedoras de ropa en IG
- [ ] Identificar 50 cuentas de marcas de ropa emprendedoras en CABA para contactar
- [ ] Script de DM frío para presentar KORMAN
- [ ] Seguimiento de las consultas abiertas

---

## 🔮 FASE 3 — ESCALADO (1-2 meses)

- [ ] **Web propia** — landing page con portfolio, formulario de cotización, página de comparación
- [ ] **Google Business Profile** — aparecer en búsquedas locales de CABA
- [ ] **WhatsApp Business API** — respuestas automáticas fuera de horario
- [ ] **Portfolio digital** — catálogo de trabajos reales por tipo y calidad
- [ ] **Estrategia de reseñas** — Google, Instagram, testimonios en web
- [ ] **Ads de Instagram** — cuando el contenido orgánico esté funcionando

---

## MÉTRICAS A SEGUIR

| Métrica | Ahora | Meta 3 meses |
|---------|-------|--------------|
| Seguidores IG | ~521 | 1.500+ |
| Engagement rate | Bajo | 4%+ |
| Consultas WA/semana | [confirmar] | 10+ |
| Clientes nuevos/mes | [confirmar] | 5+ marcas |
| Conversión consulta→pedido | [confirmar] | 40%+ |

---

## REGLAS DE TRABAJO (cómo nos manejamos)

- **Tommy decide, Claude ejecuta** — Claude propone y produce, Tommy y el papá aprueban y actúan.
- **Todo se sube al branch** `claude/fervent-lamport-qsc9um` → PR #2 en GitHub.
- **Al arrancar un chat nuevo:** leer `KORMAN-CONTEXTO-EMPRESA.md` + este archivo.
- **Datos que requieren acción humana** se marcan como `[pendiente]` o `[confirmar]`.
- **Firecrawl key:** `fc-ac31b92675104b058d606ba05a30977a`
- **Branch activo:** `claude/fervent-lamport-qsc9um`
- **PR activo:** https://github.com/tommylopas123-eng/Marketing-y-empresa-/pull/2

---

## LOG DE SESIONES

### Sesión 1 — 19/06/2026
- Creado contexto de empresa y análisis de competencia con Firecrawl
- Generados perfiles YAML de competidores
- Escritos 10 captions de Instagram + 8 templates de WhatsApp
- Creada página de comparación vs China
- Instaladas 4 skills de diseño (awesome-claude-skills)
- Generados 4 posts visuales Instagram
- Diseñado y aprobado logo KORMAN v2 (wordmark puro)
- Confirmados datos de empresa con el dueño: 46 años, maquinaria suiza, tipos de tejido, plazos, clientes autorizados
- Creados documentos de contexto y tracker (este archivo)
