import "dotenv/config";
import { serve } from "@hono/node-server";
import { Hono, type HonoRequest } from "hono";
import { cors } from "hono/cors";
import { logRequestDetails, logResponseDetails, rotateApiKeys } from "./utils.js";

const TARGET_API = "https://api.clashroyale.com";

const API_KEY = process.env.API_KEY;
if (!API_KEY) {
  console.error("API_KEY is not set in the environment variables.");
  process.exit(1);
}

let allowedOrigins: string | string[] = process.env.ALLOWED_ORIGINS ?? "";
allowedOrigins = allowedOrigins
  .split(",")
  .map((origin) => origin.trim())
  .filter((origin) => origin !== "");

const app = new Hono();

app.use(
  "*",
  cors({
    origin: allowedOrigins,
  }),
  async (c, next) => {
    const token = c.req.raw.headers.get("x-api-key");
    if (token !== API_KEY) return c.text("Unauthorized!", 401);
    return await next();
  }
);

app.get("/health", (c) => {
  return c.json({ status: "ok" });
});

app.get("*", async (c) => {
  logRequestDetails(c.req);

  const path = c.req.path;
  const method = c.req.method;
  const apiKey = rotateApiKeys()

  const response = await fetch(`${TARGET_API}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${apiKey}`,
    },
  });

  logResponseDetails(response);

  const allowedMethods = "GET, POST, PUT, DELETE, OPTIONS";
  const resp = response.clone();
  const newHeaders = new Headers(resp.headers);

  newHeaders.delete("Content-Encoding"); // Remove compression header
  newHeaders.set("Access-Control-Allow-Origin", "*"); // Optional: CORS header
  newHeaders.set("Access-Control-Allow-Methods", allowedMethods);
  newHeaders.set("Access-Control-Allow-Headers", "Authorization, Content-Type");

  return new Response(resp.body, {
    status: resp.status,
    statusText: resp.statusText,
    headers: newHeaders,
  });
});

serve(
  {
    fetch: app.fetch,
    port: 3001,
  },
  (info) => {
    console.log(`Server is running on http://localhost:${info.port}`);
  }
);
