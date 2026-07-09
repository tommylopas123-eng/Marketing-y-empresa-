// ============================================================
// Conexión con WhatsApp (Cloud API de Meta)
// Envía mensajes de texto y marca los mensajes como leídos
// usando el Graph API oficial.
// ============================================================

const TOKEN = process.env.WHATSAPP_TOKEN;
const PHONE_NUMBER_ID = process.env.WHATSAPP_PHONE_NUMBER_ID;
const GRAPH_URL = `https://graph.facebook.com/v21.0/${PHONE_NUMBER_ID}/messages`;

async function llamarGraphApi(body) {
  const res = await fetch(GRAPH_URL, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${TOKEN}`,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const detalle = await res.text();
    throw new Error(`Error de la API de WhatsApp (${res.status}): ${detalle}`);
  }
  return res.json();
}

/** Envía un mensaje de texto al número indicado (formato internacional, ej: 5491126146803). */
export function enviarTexto(numeroDestino, texto) {
  return llamarGraphApi({
    messaging_product: "whatsapp",
    to: numeroDestino,
    type: "text",
    text: { body: texto },
  });
}

/** Marca un mensaje entrante como leído (los tildes azules del cliente). */
export function marcarLeido(messageId) {
  return llamarGraphApi({
    messaging_product: "whatsapp",
    status: "read",
    message_id: messageId,
  });
}
