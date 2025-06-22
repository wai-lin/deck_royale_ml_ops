import type { HonoRequest } from "hono";

export function logRequestDetails(req: HonoRequest) {
  const headers = Object.fromEntries(req.raw.headers);

  console.log("\nRequest Details:", new Date().toISOString());
  console.log(`Received request: ${req.method} ${req.url}`);
  console.log("Headers:", JSON.stringify(headers, null, 2));
  console.log("==========================================");
}

export async function logResponseDetails(res: Response) {
  const headers = Object.fromEntries(res.headers);

  console.log("Response Details:", new Date().toISOString());
  console.log(`Status: ${res.status} ${res.statusText}`);
  console.log(`Response URL: ${res.url}`);
  console.log("Headers:", JSON.stringify(headers, null, 2));

  const clonedRes = res.clone();
  try {
    const text = await clonedRes.text();
    console.log("Body", text.slice(0, 100)); // log first 100 chars
  } catch (err) {
    console.log("Body: <unable to read body>", err);
  }

  console.log("==========================================");
  console.log("==========================================");
  console.log("==========================================");
}

const apiKeys = [
  process.env.API_KEY_1 ?? "",
  process.env.API_KEY_2 ?? "",
  process.env.API_KEY_3 ?? "",
];
/**
 * Rotates API keys by shifting the first key to the end of the list.
 * @returns a rotated API key from the list of available keys
 */
export function rotateApiKeys(): string {
  const key = apiKeys.shift();
  if (key) {
    apiKeys.push(key);
    return key;
  } else {
    throw new Error("No API keys available");
  }
}
