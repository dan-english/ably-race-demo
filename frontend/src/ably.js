import * as Ably from "ably";

let ablyClient = null;

export function initAbly(apiKey) {
  if (!ablyClient) {
    ablyClient = new Ably.Realtime(apiKey);
  }
  return ablyClient;
}

export function getAbly() {
  if (!ablyClient) {
    throw new Error("Ably client not initialized. Call initAbly first.");
  }
  return ablyClient;
}
