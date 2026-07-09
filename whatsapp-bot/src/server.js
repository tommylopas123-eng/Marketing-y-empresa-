// ============================================================
// SERVIDOR DEL BOT
// Este es el corazón del sistema. Hace de puente entre
// WhatsApp y la IA:
//
//   Cliente escribe → Meta llama a POST /webhook →
//   armamos el historial → se lo damos a Claude →
//   mandamos su respuesta de vuelta por WhatsApp.
// ============================================================

import "dotenv/config";
import express from "express";
import { pensarRespuesta } from "./claude.js";
import { enviarTexto, marcarLeido } from "./whatsapp.js";
import { montarDemo } from "./demo.js";

const app = express();
app.use(express.json());

// Demo en el navegador (/demo) para probar el bot sin conectar Meta
montarDemo(app);

const VERIFY_TOKEN = process.env.WHATSAPP_VERIFY_TOKEN;
const PORT = process.env.PORT || 3000;

// ------------------------------------------------------------
// Memoria de conversaciones.
// Guardamos el historial por número de teléfono para que el bot
// se acuerde de qué venían hablando. En producción con volumen
// conviene moverlo a una base de datos (Postgres, Redis).
// ------------------------------------------------------------
const conversaciones = new Map();
const MAX_MENSAJES_HISTORIAL = 20;

function agregarAlHistorial(numero, role, content) {
  const historial = conversaciones.get(numero) || [];
  historial.push({ role, content });
  // Recortamos para que la conversación no crezca infinito
  // (menos tokens = menos costo y más velocidad).
  while (historial.length > MAX_MENSAJES_HISTORIAL) historial.shift();
  conversaciones.set(numero, historial);
  return historial;
}

// ------------------------------------------------------------
// 1) VERIFICACIÓN DEL WEBHOOK (GET /webhook)
// Meta llama a esta ruta UNA vez, cuando configurás el webhook
// en el panel de developers.facebook.com. Manda un "desafío" y
// espera que se lo devuelvas si el token coincide.
// ------------------------------------------------------------
app.get("/webhook", (req, res) => {
  const modo = req.query["hub.mode"];
  const token = req.query["hub.verify_token"];
  const desafio = req.query["hub.challenge"];

  if (modo === "subscribe" && token === VERIFY_TOKEN) {
    console.log("✅ Webhook verificado por Meta");
    return res.status(200).send(desafio);
  }
  return res.sendStatus(403);
});

// ------------------------------------------------------------
// 2) MENSAJES ENTRANTES (POST /webhook)
// Cada vez que alguien le escribe a tu número de WhatsApp,
// Meta hace un POST acá con el contenido del mensaje.
// ------------------------------------------------------------
app.post("/webhook", (req, res) => {
  // Respondemos 200 de inmediato: si tardamos, Meta reintenta
  // y el cliente recibiría respuestas duplicadas.
  res.sendStatus(200);

  const cambio = req.body?.entry?.[0]?.changes?.[0]?.value;
  const mensaje = cambio?.messages?.[0];

  // Ignoramos todo lo que no sea un mensaje de texto entrante
  // (acuses de entrega, stickers, reacciones, etc.).
  if (!mensaje || mensaje.type !== "text") return;

  procesarMensaje(mensaje).catch((err) =>
    console.error("Error procesando mensaje:", err)
  );
});

async function procesarMensaje(mensaje) {
  const numero = mensaje.from; // ej: "5491126146803"
  const texto = mensaje.text.body;
  console.log(`📩 ${numero}: ${texto}`);

  // Tildes azules mientras "piensa"
  await marcarLeido(mensaje.id).catch(() => {});

  // Armamos el historial y le pedimos la respuesta a la IA
  const historial = agregarAlHistorial(numero, "user", texto);
  const respuesta = await pensarRespuesta(historial);
  agregarAlHistorial(numero, "assistant", respuesta);

  // Y se la mandamos al cliente por WhatsApp
  await enviarTexto(numero, respuesta);
  console.log(`🤖 ${numero}: ${respuesta}`);
}

// Ruta simple para chequear que el servidor está vivo
app.get("/", (_req, res) => res.send("Bot de WhatsApp funcionando ✅"));

app.listen(PORT, () => {
  console.log(`Servidor escuchando en el puerto ${PORT}`);
  for (const variable of [
    "WHATSAPP_TOKEN",
    "WHATSAPP_PHONE_NUMBER_ID",
    "WHATSAPP_VERIFY_TOKEN",
    "ANTHROPIC_API_KEY",
  ]) {
    if (!process.env[variable]) {
      console.warn(`⚠️  Falta la variable de entorno ${variable} (ver .env.example)`);
    }
  }
});
