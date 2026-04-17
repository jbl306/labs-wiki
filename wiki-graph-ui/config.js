// Runtime config. Rewritten by nginx entrypoint so a single image can point at
// different API origins per environment.
window.__WIKI_GRAPH_CONFIG = {
  apiBase: "__API_BASE__"
};
