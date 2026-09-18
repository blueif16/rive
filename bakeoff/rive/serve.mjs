// Static server that behaves like a real CDN (brotli / gzip by negotiation) and
// records exactly how many bytes every request actually put on the wire. The
// page-weight numbers in NOTES.md come from build/weight.json, not from a
// guess at compression ratios.
//
//   node serve.mjs 8099          # serve, log to build/weight.json
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import zlib from "node:zlib";

const ROOT = path.dirname(new URL(import.meta.url).pathname);
const PORT = Number(process.argv[2] || 8099);
const LOG = path.join(ROOT, "build", "weight.json");

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".wasm": "application/wasm",
  ".riv": "application/octet-stream",
  ".png": "image/png",
  ".json": "application/json"
};
const COMPRESSIBLE = new Set([".html", ".js", ".riv", ".json", ".wasm"]);

const hits = [];

http
  .createServer((req, res) => {
    const url = decodeURIComponent(req.url.split("?")[0]);
    let file = path.join(ROOT, url === "/" ? "index.html" : url);
    if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
      res.writeHead(404).end("not found");
      return;
    }
    const ext = path.extname(file);
    const raw = fs.readFileSync(file);
    const accept = req.headers["accept-encoding"] || "";

    let body = raw;
    let enc = null;
    if (COMPRESSIBLE.has(ext)) {
      if (/\bbr\b/.test(accept)) {
        enc = "br";
        body = zlib.brotliCompressSync(raw, {
          params: { [zlib.constants.BROTLI_PARAM_QUALITY]: 11 }
        });
      } else if (/\bgzip\b/.test(accept)) {
        enc = "gzip";
        body = zlib.gzipSync(raw, { level: 9 });
      }
    }

    hits.push({ url, raw: raw.length, sent: body.length, encoding: enc || "identity" });
    fs.writeFileSync(LOG, JSON.stringify(hits, null, 1));

    res.writeHead(200, {
      "content-type": TYPES[ext] || "application/octet-stream",
      "content-length": body.length,
      ...(enc ? { "content-encoding": enc } : {}),
      "cache-control": "no-store"
    });
    res.end(body);
  })
  .listen(PORT, () => console.log(`serving ${ROOT} on http://localhost:${PORT}`));
