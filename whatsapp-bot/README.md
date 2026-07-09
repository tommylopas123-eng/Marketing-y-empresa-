# 🤖 Bot de WhatsApp con IA — Guía completa de conexión

Asistente virtual estilo "HUERTIX": atiende consultas por WhatsApp usando
la **Cloud API oficial de Meta** + la **API de Claude** (Anthropic).

## Cómo funciona (el circuito completo)

```
 Cliente                Meta                  TU SERVIDOR                Anthropic
   │                     │                        │                         │
   │ escribe por WhatsApp│                        │                         │
   ├────────────────────►│  POST /webhook         │                         │
   │                     ├───────────────────────►│ arma historial +        │
   │                     │                        │ system prompt           │
   │                     │                        ├────────────────────────►│
   │                     │                        │      responde la IA     │
   │                     │                        │◄────────────────────────┤
   │                     │  POST /messages        │                         │
   │   recibe respuesta  │◄───────────────────────┤                         │
   │◄────────────────────┤                        │                         │
```

Archivos del proyecto:

| Archivo | Qué hace |
|---|---|
| `src/server.js` | El servidor: recibe mensajes de Meta y coordina todo |
| `src/whatsapp.js` | Envía las respuestas por la Cloud API de Meta |
| `src/claude.js` | Le pide la respuesta a la IA |
| `src/prompt.js` | La personalidad y las reglas del asistente (editá esto) |
| `src/demo.js` | Demo en el navegador (`/demo`) para probar sin WhatsApp |
| `src/chat-local.js` | Demo en la terminal (`npm run chat`) |
| `.env.example` | Plantilla de las claves que necesitás |

---

## PARTE 0 — Probar el bot YA, sin trámite de Meta (5 min)

No hace falta tener WhatsApp conectado para ver al asistente funcionando.
Lo único que necesitás es la API key de Claude (paso 3):

```bash
cd whatsapp-bot
npm install
cp .env.example .env      # → pegá tu ANTHROPIC_API_KEY en .env
npm start
```

Abrí **http://localhost:3000/demo** en el navegador: es una pantalla tipo
WhatsApp donde chateás con el bot como si fueras un cliente. Usa exactamente
el mismo cerebro que el bot real (`src/prompt.js`), así que sirve para
ajustar la personalidad antes de conectar nada.

También podés chatear desde la terminal con `npm run chat`.

> ⚠️ Cuando el servidor esté publicado en internet (Railway), poné
> `DEMO_ENABLED=false` en las variables para que nadie con la URL
> gaste tu crédito de IA.

---

## PARTE 1 — Conseguir las credenciales de WhatsApp (30-45 min)

### Paso 1: Crear la app en Meta

1. Entrá a **[developers.facebook.com](https://developers.facebook.com)** e iniciá
   sesión con tu Facebook.
2. **My Apps → Create App**.
3. Elegí tipo **Business** y ponele nombre (ej: "Bot Mi Negocio").
4. Te va a pedir asociar un **portfolio de Meta Business**
   ([business.facebook.com](https://business.facebook.com)) — si no tenés, crealo ahí
   mismo con los datos de tu negocio. Es gratis.

### Paso 2: Activar WhatsApp en la app

1. En el panel de tu app: **Add Product → WhatsApp → Set up**.
2. Entrá a **WhatsApp → API Setup**. Ahí Meta te regala:
   - Un **número de prueba** gratuito para desarrollar
   - Un **token temporal** (dura 24 hs, sirve para probar)
   - El **Phone number ID** (un ID numérico largo — copialo)
3. En "To", agregá TU número personal como destinatario de prueba
   (te llega un código por WhatsApp para confirmarlo).

> 💡 Con el número de prueba podés desarrollar todo gratis. El número real
> se conecta recién al final (Parte 4).

### Paso 3: Conseguir la clave de la IA

1. Entrá a **[platform.claude.com](https://platform.claude.com)** y creá una cuenta.
2. Cargá crédito (con USD 5 tenés para ~2 meses de un bot chico).
3. **API Keys → Create Key** y copiá la clave (empieza con `sk-ant-...`).

---

## PARTE 2 — Levantar el servidor (15 min)

### Paso 4: Configurar y correr localmente

```bash
cd whatsapp-bot
npm install
cp .env.example .env
# → abrí .env y pegá: el token, el Phone number ID y la API key
npm start
```

Tenés que ver: `Servidor escuchando en el puerto 3000`.

### Paso 5: Hacer visible tu servidor desde internet

Meta necesita una URL **https pública** para mandarte los mensajes. Para
probar desde tu compu, abrí un túnel en otra terminal:

```bash
npx localtunnel --port 3000
# te da una URL tipo: https://algo-random.loca.lt
```

(Alternativa: [ngrok](https://ngrok.com), gratis para desarrollo.)

Para producción esto no hace falta: Railway te da la URL pública directa
(Parte 4).

### Paso 6: Conectar el webhook en Meta

1. En el panel de tu app: **WhatsApp → Configuration → Webhook → Edit**.
2. **Callback URL**: tu URL pública + `/webhook`
   (ej: `https://algo-random.loca.lt/webhook`)
3. **Verify token**: exactamente lo que pusiste en
   `WHATSAPP_VERIFY_TOKEN` en tu `.env`.
4. Click en **Verify and save** → en tu terminal tiene que aparecer
   `✅ Webhook verificado por Meta`.
5. En **Webhook fields**, suscribite al campo **`messages`** (Subscribe).

### Paso 7: ¡Probarlo! 🎉

Mandale un WhatsApp desde tu celular al **número de prueba**
(figura en API Setup). El bot tiene que:

1. Marcar tu mensaje como leído (tildes azules)
2. Responderte como el asistente en unos segundos

Si no responde, mirá la terminal del servidor: los errores de token vencido
o de API key aparecen ahí.

---

## PARTE 3 — Personalizarlo para tu negocio (10 min)

Abrí **`src/prompt.js`** y completá:

- Nombre del bot y del negocio (o seteá `BOT_NAME` y `BUSINESS_NAME` en `.env`)
- Qué vendés, horarios, zonas, precios orientativos
- Qué datos tiene que juntar antes de derivar a un humano

Todo el comportamiento del bot sale de ese archivo. Cambiás el texto,
reiniciás el servidor y ya habla distinto.

---

## PARTE 4 — Pasarlo a producción (cuando ya funciona)

### Paso 8: Token permanente

El token de API Setup vence a las 24 hs. Para el definitivo:

1. En [business.facebook.com](https://business.facebook.com) →
   **Configuración del negocio → Usuarios → Usuarios del sistema → Agregar**.
2. Creá un usuario del sistema (rol Admin), asignale tu app con permisos
   completos.
3. **Generar token** → tildá `whatsapp_business_messaging` y
   `whatsapp_business_management` → duración **nunca vence**.
4. Ese token va en `WHATSAPP_TOKEN` en producción.

### Paso 9: Subir el servidor a Railway (~USD 5/mes)

1. Subí este repo a GitHub (ya está 😉).
2. En [railway.app](https://railway.app): **New Project → Deploy from GitHub repo**.
3. Seteá **Root Directory** = `whatsapp-bot`.
4. En **Variables**, cargá las mismas del `.env` (token permanente, IDs, API key).
5. En **Settings → Networking → Generate Domain** te da la URL pública.
6. Volvé al paso 6 y actualizá la Callback URL del webhook con esa URL
   (`https://tu-app.up.railway.app/webhook`).

### Paso 10: Conectar tu número real

1. En **WhatsApp → API Setup → Add phone number**: cargá el número del
   negocio (no puede estar activo en la app común de WhatsApp — si lo está,
   primero eliminá esa cuenta desde la app).
2. Verificalo por SMS o llamada.
3. Registrá el número y usá su nuevo **Phone number ID** en las variables.
4. Completá la **verificación del negocio** en Meta Business
   (Configuración → Centro de seguridad → Iniciar verificación): subís
   documentación del negocio. Es gratis y desbloquea más volumen de
   mensajes. El tilde verde (cuenta oficial) se solicita después desde
   el WhatsApp Manager.

---

## Costos reales (julio 2026)

| Ítem | Costo |
|---|---|
| Meta — responder consultas entrantes | **Gratis** hasta el 30/9/2026; desde octubre 2026 se cobra por mensaje (tarifa similar a "utility", Meta la publica antes del 1/9/2026) |
| Meta — mensajes que inicia la empresa (plantillas) | Argentina: ~USD 0,12 marketing / ~USD 0,058 utility |
| IA (Claude Haiku, ~1.000 mensajes/mes) | USD 3-5/mes |
| Railway | USD 5/mes |
| **Total típico** | **~USD 8-10/mes** |

## Plan a futuro: automatizaciones con n8n

Cuando el bot esté vendido/funcionando y quieras sumarle automatizaciones
(guardar leads en Google Sheets, avisar al vendedor, agendar reuniones),
el camino es n8n self-hosted (gratis, ~USD 5-10/mes de hosting):

- El trámite de Meta y el prompt que armes acá **se reutilizan tal cual**:
  en n8n apuntás el mismo webhook de Meta al nodo "WhatsApp Trigger"
  y pegás el contenido de `src/prompt.js` en el nodo "AI Agent".
- Este bot puede convivir con n8n: una opción común es que el bot siga
  respondiendo y solo llame a n8n (por webhook) cuando junta los datos
  de un lead, para que n8n dispare las automatizaciones.

## Seguridad

- El `.env` con tus claves **nunca** se sube al repo (ya está en `.gitignore`).
- Si un token o API key se te filtra, revocalo y generá uno nuevo
  (Meta Business → usuarios del sistema / platform.claude.com → API Keys).
