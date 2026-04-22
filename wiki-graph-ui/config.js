// Runtime config. Rewritten by nginx entrypoint so a single image can point at
// different API origins per environment.
window.__WIKI_GRAPH_CONFIG = {
  apiBase: "__API_BASE__",
  // Renderer: "webgl" (custom WebGL2 with glow shader, default) or
  // "canvas" (R1-R19 fallback). Override via ?renderer=canvas in URL or
  // by editing this file.
  renderer: "webgl"
};
