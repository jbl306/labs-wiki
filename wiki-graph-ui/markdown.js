// Minimal, safe markdown -> HTML renderer for the in-graph wiki popup.
// Goals:
//   - HTML-escape everything by default (the wiki body is trusted but we
//     still don't want stray <script> from an LLM-synthesised page to fire).
//   - Support: headings (#..######), bold (**), italic (*), inline code (`),
//     fenced code blocks (```), bullet/ordered lists, blockquotes,
//     horizontal rules, links [t](u), wikilinks [[Page]], paragraphs.
//   - Strip the YAML frontmatter block if present.
//   - Emit wikilinks as <a class="wikilink" data-target="..."> so the
//     caller can intercept clicks for in-graph navigation.

export function renderMarkdown(src) {
  if (!src) return "";
  let body = String(src);

  // Strip frontmatter if present.
  if (body.startsWith("---\n")) {
    const end = body.indexOf("\n---", 4);
    if (end !== -1) body = body.slice(end + 4).replace(/^\s*\n/, "");
  }

  // Pull fenced code blocks out first so their content isn't mangled.
  const codeBlocks = [];
  body = body.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (_, lang, code) => {
    const idx = codeBlocks.push({ lang, code }) - 1;
    return `\u0000CODEBLOCK${idx}\u0000`;
  });

  const lines = body.split("\n");
  const out = [];
  let i = 0;

  function escapeHTML(s) {
    return s.replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }

  function inline(s) {
    let t = escapeHTML(s);
    // Wikilinks [[Page]] or [[Page|alias]]
    t = t.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (_, target, alias) => {
      const safeTarget = target.trim();
      const text = (alias || target).trim();
      return `<a class="wikilink" data-target="${safeTarget.replace(/"/g, "&quot;")}" href="#">${text}</a>`;
    });
    // Inline code
    t = t.replace(/`([^`]+)`/g, "<code>$1</code>");
    // Bold + italic
    t = t.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    t = t.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, "$1<em>$2</em>");
    // Links [text](url) — only http(s)/relative
    t = t.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, text, url) => {
      const safeUrl = /^(https?:\/\/|\/|#|mailto:)/.test(url) ? url : "#";
      return `<a href="${safeUrl}" target="_blank" rel="noopener noreferrer">${text}</a>`;
    });
    return t;
  }

  while (i < lines.length) {
    const line = lines[i];

    // Codeblock placeholder
    const cbm = line.match(/^\u0000CODEBLOCK(\d+)\u0000$/);
    if (cbm) {
      const { lang, code } = codeBlocks[+cbm[1]];
      out.push(`<pre><code class="lang-${escapeHTML(lang)}">${escapeHTML(code)}</code></pre>`);
      i++; continue;
    }

    // Heading
    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      const lvl = h[1].length;
      out.push(`<h${lvl}>${inline(h[2].trim())}</h${lvl}>`);
      i++; continue;
    }

    // Horizontal rule
    if (/^\s*(?:---|\*\*\*|___)\s*$/.test(line)) {
      out.push("<hr/>"); i++; continue;
    }

    // Blockquote (group consecutive)
    if (/^>\s?/.test(line)) {
      const buf = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) {
        buf.push(lines[i].replace(/^>\s?/, ""));
        i++;
      }
      out.push(`<blockquote>${inline(buf.join(" "))}</blockquote>`);
      continue;
    }

    // Unordered list
    if (/^\s*[-*+]\s+/.test(line)) {
      const buf = [];
      while (i < lines.length && /^\s*[-*+]\s+/.test(lines[i])) {
        buf.push(`<li>${inline(lines[i].replace(/^\s*[-*+]\s+/, ""))}</li>`);
        i++;
      }
      out.push(`<ul>${buf.join("")}</ul>`);
      continue;
    }

    // Ordered list
    if (/^\s*\d+\.\s+/.test(line)) {
      const buf = [];
      while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
        buf.push(`<li>${inline(lines[i].replace(/^\s*\d+\.\s+/, ""))}</li>`);
        i++;
      }
      out.push(`<ol>${buf.join("")}</ol>`);
      continue;
    }

    // Blank line
    if (!line.trim()) { i++; continue; }

    // Paragraph (collect until blank line, list, heading, or code)
    const buf = [line];
    i++;
    while (i < lines.length) {
      const ln = lines[i];
      if (!ln.trim()) break;
      if (/^(#{1,6})\s+/.test(ln)) break;
      if (/^\s*[-*+]\s+/.test(ln)) break;
      if (/^\s*\d+\.\s+/.test(ln)) break;
      if (/^>\s?/.test(ln)) break;
      if (/^\u0000CODEBLOCK\d+\u0000$/.test(ln)) break;
      buf.push(ln);
      i++;
    }
    out.push(`<p>${inline(buf.join(" "))}</p>`);
  }

  return out.join("\n");
}
