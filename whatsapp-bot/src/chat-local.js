// ============================================================
// MODO DEMO EN TERMINAL
// Chateá con el asistente sin tener WhatsApp conectado.
// Usa exactamente el mismo cerebro (prompt.js + claude.js)
// que el bot real; lo único que cambia es que en vez de
// WhatsApp, escribís acá.
//
//   npm run chat
// ============================================================

import "dotenv/config";
import readline from "node:readline/promises";
import { pensarRespuesta } from "./claude.js";

if (!process.env.ANTHROPIC_API_KEY) {
  console.error("⚠️  Falta ANTHROPIC_API_KEY en el archivo .env");
  console.error("   (se consigue en platform.claude.com — es lo único que necesitás para la demo)");
  process.exit(1);
}

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const historial = [];

console.log("💬 Demo del asistente — escribí como si fueras un cliente (Ctrl+C para salir)\n");

while (true) {
  const texto = (await rl.question("Vos: ")).trim();
  if (!texto) continue;

  historial.push({ role: "user", content: texto });
  try {
    const respuesta = await pensarRespuesta(historial);
    historial.push({ role: "assistant", content: respuesta });
    console.log(`\n🤖 Bot: ${respuesta}\n`);
  } catch (err) {
    historial.pop();
    console.error(`\n❌ ${err.message}\n`);
  }
}
