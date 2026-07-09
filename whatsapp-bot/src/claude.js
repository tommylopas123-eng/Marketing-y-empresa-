// ============================================================
// Conexión con la IA (API de Anthropic / Claude)
// Recibe el historial de la conversación y devuelve la
// respuesta que el bot va a mandar por WhatsApp.
// ============================================================

import { SYSTEM_PROMPT } from "./prompt.js";

const API_KEY = process.env.ANTHROPIC_API_KEY;
const MODEL = process.env.CLAUDE_MODEL || "claude-haiku-4-5";

/**
 * @param {Array<{role: "user"|"assistant", content: string}>} historial
 *   Mensajes previos de la conversación, en orden.
 * @returns {Promise<string>} La respuesta del asistente.
 */
export async function pensarRespuesta(historial) {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 500,
      // El system prompt va cacheado: Anthropic cobra ~90% menos
      // por la parte de la entrada que se repite en cada mensaje.
      system: [
        {
          type: "text",
          text: SYSTEM_PROMPT,
          cache_control: { type: "ephemeral" },
        },
      ],
      messages: historial,
    }),
  });

  if (!res.ok) {
    const detalle = await res.text();
    throw new Error(`Error de la API de Claude (${res.status}): ${detalle}`);
  }

  const data = await res.json();
  return data.content
    .filter((bloque) => bloque.type === "text")
    .map((bloque) => bloque.text)
    .join("\n");
}
