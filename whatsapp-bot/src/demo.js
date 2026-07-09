// ============================================================
// MODO DEMO EN EL NAVEGADOR
// Una pantalla tipo WhatsApp en http://localhost:3000/demo
// para probar el asistente sin conectar Meta. Usa el mismo
// cerebro que el bot real (prompt.js + claude.js).
//
// En producción, apagalo poniendo DEMO_ENABLED=false para que
// nadie con la URL pueda usar tu crédito de IA.
// ============================================================

import { pensarRespuesta } from "./claude.js";

const MAX_MENSAJES = 30;
const BOT_NAME = process.env.BOT_NAME || "ASISTIX";

export function montarDemo(app) {
  if (process.env.DEMO_ENABLED === "false") return;

  app.get("/demo", (_req, res) => {
    res.type("html").send(PAGINA_DEMO);
  });

  // El navegador manda el historial completo en cada mensaje,
  // así el servidor no tiene que guardar nada.
  app.post("/demo/message", async (req, res) => {
    const historial = Array.isArray(req.body?.historial) ? req.body.historial : [];
    const valido =
      historial.length > 0 &&
      historial.length <= MAX_MENSAJES &&
      historial.every(
        (m) =>
          (m.role === "user" || m.role === "assistant") &&
          typeof m.content === "string" &&
          m.content.length <= 2000
      );
    if (!valido) {
      return res.status(400).json({ error: "Historial inválido o demasiado largo. Refrescá la página." });
    }

    try {
      const respuesta = await pensarRespuesta(historial);
      res.json({ respuesta });
    } catch (err) {
      console.error("Error en la demo:", err.message);
      res.status(500).json({ error: "No pude responder. Revisá la ANTHROPIC_API_KEY y los logs del servidor." });
    }
  });

  console.log("🧪 Demo activada: abrí /demo en el navegador para chatear con el bot");
}

const PAGINA_DEMO = /* html */ `<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Demo — ${BOT_NAME}</title>
<style>
  * { box-sizing: border-box; margin: 0; }
  body { font-family: -apple-system, "Segoe UI", Roboto, sans-serif; background: #0b141a; height: 100dvh; display: flex; flex-direction: column; }
  header { background: #1f2c33; color: #e9edef; padding: 12px 16px; display: flex; align-items: center; gap: 12px; }
  header .avatar { width: 40px; height: 40px; border-radius: 50%; background: #00a884; display: grid; place-items: center; font-size: 20px; }
  header small { color: #8696a0; display: block; }
  #chat { flex: 1; overflow-y: auto; padding: 16px 12px; display: flex; flex-direction: column; gap: 6px; }
  .burbuja { max-width: 80%; padding: 8px 12px; border-radius: 8px; color: #e9edef; white-space: pre-wrap; line-height: 1.35; font-size: 15px; }
  .bot { background: #1f2c33; align-self: flex-start; border-top-left-radius: 0; }
  .yo { background: #005c4b; align-self: flex-end; border-top-right-radius: 0; }
  .escribiendo { color: #8696a0; font-style: italic; }
  form { display: flex; gap: 8px; padding: 10px 12px; background: #1f2c33; }
  input { flex: 1; border: 0; border-radius: 20px; padding: 12px 16px; font-size: 15px; background: #2a3942; color: #e9edef; outline: none; }
  button { border: 0; border-radius: 50%; width: 46px; height: 46px; background: #00a884; color: #fff; font-size: 18px; cursor: pointer; }
  button:disabled { opacity: .5; }
</style>
</head>
<body>
<header>
  <div class="avatar">🤖</div>
  <div><strong>${BOT_NAME}</strong> <small>demo — así lo vería tu cliente en WhatsApp</small></div>
</header>
<div id="chat"></div>
<form id="form">
  <input id="input" placeholder="Escribí como si fueras un cliente…" autocomplete="off" autofocus>
  <button id="btn" type="submit">➤</button>
</form>
<script>
const chat = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("input");
const btn = document.getElementById("btn");
const historial = [];

function burbuja(texto, clase) {
  const div = document.createElement("div");
  div.className = "burbuja " + clase;
  div.textContent = texto;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const texto = input.value.trim();
  if (!texto) return;
  input.value = "";
  btn.disabled = true;

  burbuja(texto, "yo");
  historial.push({ role: "user", content: texto });
  const espera = burbuja("escribiendo…", "bot escribiendo");

  try {
    const res = await fetch("/demo/message", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ historial }),
    });
    const data = await res.json();
    espera.remove();
    if (data.respuesta) {
      historial.push({ role: "assistant", content: data.respuesta });
      burbuja(data.respuesta, "bot");
    } else {
      historial.pop();
      burbuja("⚠️ " + (data.error || "Error desconocido"), "bot");
    }
  } catch {
    espera.remove();
    historial.pop();
    burbuja("⚠️ No pude conectar con el servidor", "bot");
  }
  btn.disabled = false;
  input.focus();
});
</script>
</body>
</html>`;
