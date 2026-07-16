const BREVO_API = "https://api.brevo.com/v3";

function cors(origin) {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin"
  };
}

function json(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...cors(origin) }
  });
}

function validEmail(value) {
  return typeof value === "string" && value.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

async function brevo(path, apiKey, body) {
  return fetch(`${BREVO_API}${path}`, {
    method: "POST",
    headers: {
      accept: "application/json",
      "api-key": apiKey,
      "content-type": "application/json"
    },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(15000)
  });
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowed = origin === env.ALLOWED_ORIGIN;

    if (request.method === "OPTIONS") {
      return allowed ? new Response(null, { status: 204, headers: cors(origin) }) : new Response(null, { status: 403 });
    }
    if (request.method !== "POST" || new URL(request.url).pathname !== "/suscribir") {
      return json({ ok: false, error: "not_found" }, 404, allowed ? origin : env.ALLOWED_ORIGIN);
    }
    if (!allowed) return json({ ok: false, error: "origin_not_allowed" }, 403, env.ALLOWED_ORIGIN);
    if (!env.BREVO_API_KEY) return json({ ok: false, error: "service_not_configured" }, 503, origin);

    let payload;
    try {
      payload = await request.json();
    } catch {
      return json({ ok: false, error: "invalid_json" }, 400, origin);
    }

    // Campo señuelo: los visitantes reales nunca deben completarlo.
    if (payload.website) return json({ ok: true }, 200, origin);
    const email = String(payload.email || "").trim().toLowerCase();
    if (!validEmail(email)) return json({ ok: false, error: "invalid_email" }, 400, origin);
    if (payload.privacyAccepted !== true) return json({ ok: false, error: "privacy_required" }, 400, origin);

    const contactPayload = {
      email,
      updateEnabled: true
    };
    if (payload.promoAccepted === true) contactPayload.listIds = [Number(env.BREVO_LIST_ID)];
    let contact;
    try {
      contact = await brevo("/contacts", env.BREVO_API_KEY, contactPayload);
    } catch (error) {
      console.error("Brevo contact timeout", error?.message || error);
      return json({ ok: false, error: "contact_timeout" }, 504, origin);
    }
    if (!contact.ok) {
      const detail = await contact.text();
      console.error("Brevo contact error", contact.status, detail);
      return json({ ok: false, error: "contact_failed" }, 502, origin);
    }

    let message;
    try {
      message = await brevo("/smtp/email", env.BREVO_API_KEY, {
        templateId: Number(env.BREVO_TEMPLATE_ID),
        to: [{ email }],
        params: { DOWNLOAD_PAGE: "https://viajescasal-sketch.github.io/elkitdelviajero/guias/" },
        tags: ["kit-viajero", "guias"]
      });
    } catch (error) {
      console.error("Brevo email timeout", error?.message || error);
      return json({ ok: false, error: "email_timeout" }, 504, origin);
    }
    if (!message.ok) {
      const detail = await message.text();
      console.error("Brevo email error", message.status, detail);
      return json({ ok: false, error: "email_failed" }, 502, origin);
    }

    return json({ ok: true }, 201, origin);
  }
};
