/*
 * wm-figure.js — drop-in embed for the Rive essay figures.
 *
 * A host page adds one element and one script tag; everything else (canvas,
 * caption, screen-reader description, styles, breakpoints, playback policy)
 * is built here.
 *
 *   <div data-wm-figure
 *        data-src="figure/world-models.riv"
 *        data-alt="…"
 *        data-caption="…"
 *        data-describe="Renderer → observations | Simulator → state | …"></div>
 *   <script src="figure/wm-figure.js" defer></script>
 *
 * House embed contract, point by point:
 *   1 responsive    three authored artboards, picked by container width, each
 *                   capped so the rendered scale stays inside 0.8–1.4
 *   2 in-viewport   IntersectionObserver play/pause, plus page visibility
 *   3 reduced motion  never plays; renders one still of the all-three-lanes beat
 *   4 accessible    figure/figcaption, canvas role=img + aria-label, and a
 *                   visually-hidden description of the three rows
 *   5 self-contained  no build step, no framework, scoped styles injected once
 *   6 weight        one runtime + one .riv per page, cached across figures
 */
(function () {
  "use strict";

  var RUNTIME_FALLBACK = "https://unpkg.com/@rive-app/canvas@2.42.2/rive.js";
  var IS_FILE = location.protocol === "file:";

  /* ---------------------------------------------------------------- bands --
   * Each artboard is authored at a fixed pixel size, so legibility is a
   * question of render scale rather than of viewport width. `cap` is the
   * widest we will draw an artboard: past it the figure stops growing and
   * sits centred, which keeps 11px letterspaced captions from ballooning.
   */
  var BANDS = [
    { until: 560, artboard: "Mobile", w: 360, h: 560, cap: 480 },
    { until: 900, artboard: "Medium", w: 700, h: 440, cap: 900 },
    { until: Infinity, artboard: "Desktop", w: 1200, h: 600, cap: 1200 }
  ];

  function bandFor(width) {
    for (var i = 0; i < BANDS.length; i++) if (width < BANDS[i].until) return BANDS[i];
    return BANDS[BANDS.length - 1];
  }

  /* --------------------------------------------------------------- styles -- */
  var CSS =
    ".wmf{margin:2.75rem 0;}" +
    ".wmf-stage{background:#F7F7FA;overflow:hidden;display:flex;justify-content:center;}" +
    ".wmf-stage canvas{display:block;width:100%;height:100%;}" +
    // 4.7% matches the left inset every artboard gives its label cards, so the
    // caption lines up with the figure's content rather than its bleed edge.
    ".wmf-cap{margin:.9rem 0 0;padding:0 4.7%;font-size:.8125rem;line-height:1.55;" +
    "color:#746E63;max-width:52rem;}" +
    ".wmf-cap b{font-weight:600;color:#3B3730;}" +
    ".wmf-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;" +
    "overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0;}";

  function injectStyles() {
    if (document.getElementById("wmf-styles")) return;
    var s = document.createElement("style");
    s.id = "wmf-styles";
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  /* -------------------------------------------------------------- runtime --
   * Loaded once per page and shared by every figure on it. Over http the
   * vendored copy is used and the wasm is pointed at its sibling; a page
   * opened straight off the disk cannot fetch either (file:// is an opaque
   * origin), so that one case falls back to the CDN.
   */
  var runtimePromise = null;

  function loadRuntime(base) {
    if (window.rive) return Promise.resolve(window.rive);
    if (runtimePromise) return runtimePromise;
    runtimePromise = new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = IS_FILE ? RUNTIME_FALLBACK : base + "rive-runtime.js";
      s.onload = function () {
        if (!window.rive) return reject(new Error("rive runtime did not load"));
        if (!IS_FILE && window.rive.RuntimeLoader) {
          window.rive.RuntimeLoader.setWasmUrl(base + "rive.wasm");
        }
        resolve(window.rive);
      };
      s.onerror = function () { reject(new Error("could not load " + s.src)); };
      document.head.appendChild(s);
    });
    return runtimePromise;
  }

  /* ------------------------------------------------------------- the file --
   * One ArrayBuffer per .riv URL. Four figures cut from the same file cost
   * exactly one download, and switching artboards at a breakpoint re-uses the
   * bytes already in memory rather than hitting the network again.
   */
  var buffers = {};

  function loadBuffer(url, inlineName) {
    if (buffers[url]) return buffers[url];
    if (IS_FILE) {
      buffers[url] = new Promise(function (resolve, reject) {
        if (window[inlineName]) return resolve(decodeBase64(window[inlineName]));
        var s = document.createElement("script");
        s.src = url.replace(/\.riv$/, "") + "-inline.js";
        s.onload = function () {
          window[inlineName]
            ? resolve(decodeBase64(window[inlineName]))
            : reject(new Error("inline .riv missing"));
        };
        s.onerror = function () { reject(new Error("could not load " + s.src)); };
        document.head.appendChild(s);
      });
    } else {
      buffers[url] = fetch(url).then(function (r) {
        if (!r.ok) throw new Error(url + " → " + r.status);
        return r.arrayBuffer();
      });
    }
    return buffers[url];
  }

  function decodeBase64(b64) {
    var bin = atob(b64), out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out.buffer;
  }

  /* --------------------------------------------------------------- figure -- */
  function Figure(host) {
    var base = (host.dataset.src || "").replace(/[^/]+$/, "");
    var src = host.dataset.src;

    var fig = document.createElement("figure");
    // Carry the host's classes over so the page keeps control of placement
    // (grid column, bleed) without knowing anything about this script.
    fig.className = ("wmf " + (host.className || "")).trim();
    var stage = document.createElement("div");
    stage.className = "wmf-stage";
    var canvas = document.createElement("canvas");
    stage.appendChild(canvas);
    fig.appendChild(stage);

    var descId = "wmf-d" + Math.random().toString(36).slice(2, 8);
    canvas.setAttribute("role", "img");
    canvas.setAttribute("aria-label", host.dataset.alt || "");
    canvas.setAttribute("aria-describedby", descId);

    // The long description is the figure's point in words: a screen-reader
    // user should not need the animation to get it.
    var sr = document.createElement("div");
    sr.className = "wmf-sr";
    sr.id = descId;
    sr.textContent = host.dataset.describe || "";
    fig.appendChild(sr);

    if (host.dataset.caption) {
      var cap = document.createElement("figcaption");
      cap.className = "wmf-cap";
      cap.innerHTML = host.dataset.caption;
      fig.appendChild(cap);
    }

    host.replaceWith(fig);

    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
    var rive = null, r = null, band = null, visible = false, ready = false;

    function size() {
      var avail = stage.parentElement.clientWidth || stage.clientWidth || 360;
      var b = bandFor(avail);
      var w = Math.max(240, Math.min(avail, b.cap));
      canvas.style.width = w + "px";
      canvas.style.height = Math.round((w * b.h) / b.w) + "px";
      stage.style.height = canvas.style.height;
      return b;
    }

    // Rive holds a wasm-side artboard instance, so changing artboard means a
    // new instance. That only happens when a resize crosses a band edge.
    function mount(b) {
      if (r) { r.cleanup(); r = null; ready = false; }
      band = b;
      loadBuffer(src, "WM_FIGURE_RIV").then(function (buffer) {
        r = new rive.Rive({
          buffer: buffer,
          canvas: canvas,
          artboard: b.artboard,
          animations: "Loop",
          autoplay: false,
          layout: new rive.Layout({ fit: rive.Fit.Contain, alignment: rive.Alignment.Center }),
          onLoad: function () {
            ready = true;
            r.resizeDrawingSurfaceToCanvas();
            still();                       // paint something before any play
            apply();
            // Let the host page reach the instance (and let the capture
            // harness seek to a named beat).
            fig.rive = r;
            fig.dispatchEvent(new CustomEvent("wm-figure:ready", {
              bubbles: true, detail: { rive: r, artboard: b.artboard }
            }));
          }
        });
      })["catch"](function (e) { fail(e); });
    }

    // Reduced motion, and the pre-roll frame in every case: one still of the
    // opening beat, where all three lanes are up together.
    function still() {
      try { r.scrub("Loop", 1.1); } catch (e) { /* rest pose is beat 1 too */ }
    }

    function apply() {
      if (!r || !ready) return;
      if (reduce.matches) { r.pause(); still(); return; }
      visible ? r.play("Loop") : r.pause();
    }

    function fail(e) {
      stage.innerHTML =
        '<p style="margin:auto;padding:1.5rem;font:14px/1.5 system-ui;color:#746E63">' +
        "This figure needs its Rive runtime. " +
        (IS_FILE ? "Opened from disk it loads that from a CDN — check the network. " : "") +
        "</p>";
      if (window.console) console.warn("[wm-figure]", e);
    }

    var io = new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      apply();
    }, { threshold: 0.12 });
    io.observe(stage);

    document.addEventListener("visibilitychange", function () {
      if (document.hidden) { if (r && ready) r.pause(); } else apply();
    });

    var mqHandler = function () { apply(); };
    reduce.addEventListener ? reduce.addEventListener("change", mqHandler)
                            : reduce.addListener(mqHandler);

    var ro = new ResizeObserver(function () {
      var b = size();
      if (!rive) return;
      if (b.artboard !== (band && band.artboard)) mount(b);
      else if (r && ready) r.resizeDrawingSurfaceToCanvas();
    });
    ro.observe(stage.parentElement || stage);

    var first = size();
    loadRuntime(base).then(function (lib) {
      rive = lib;
      mount(bandFor(stage.parentElement.clientWidth || first.w));
    })["catch"](fail);
  }

  function boot() {
    injectStyles();
    var hosts = document.querySelectorAll("[data-wm-figure]");
    for (var i = 0; i < hosts.length; i++) new Figure(hosts[i]);
  }

  document.readyState === "loading"
    ? document.addEventListener("DOMContentLoaded", boot)
    : boot();
})();
