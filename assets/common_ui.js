/*
 * ブラウザ側のページで共通に使う画面の部品（KaTeX・Plotly・ボタン・アニメーション）
 */
(function (root) {
  "use strict";

  function $(id) { return document.getElementById(id); }

  function ready() {
    if (typeof Plotly === "undefined" || typeof katex === "undefined") {
      document.body.innerHTML =
        '<div class="err">グラフの部品（Plotly.js / KaTeX）を読み込めませんでした。ネットワークを確認して、ページを再読み込みしてください。</div>';
      return false;
    }
    return true;
  }

  function tex(s, display) { return katex.renderToString(s, { throwOnError: false, displayMode: !!display }); }

  /** 状態をブラウザに保存（ページを切りかえても残る）。保存できない環境では毎回初期値 */
  function store(key, defaults) {
    var S = JSON.parse(JSON.stringify(defaults));
    try {
      var saved = JSON.parse(window.localStorage.getItem(key) || "null");
      if (saved && typeof saved === "object") {
        Object.keys(defaults).forEach(function (k) {
          if (saved[k] === undefined) return;
          if (defaults[k] && typeof defaults[k] === "object" && !Array.isArray(defaults[k])) S[k] = Object.assign({}, defaults[k], saved[k]);
          else S[k] = saved[k];
        });
      }
    } catch (e) { /* なにもしない */ }
    S.save = function () {
      try {
        var o = {}; Object.keys(defaults).forEach(function (k) { o[k] = S[k]; });
        window.localStorage.setItem(key, JSON.stringify(o));
      } catch (e) { /* なにもしない */ }
    };
    S.reset = function () { var d = JSON.parse(JSON.stringify(defaults)); Object.keys(d).forEach(function (k) { S[k] = d[k]; }); };
    return S;
  }

  /** <div class="seg" data-key="..."><button data-v="...">  を状態 S と結ぶ */
  function bindSegs(S, onChange) {
    document.querySelectorAll(".seg[data-key]").forEach(function (seg) {
      seg.addEventListener("click", function (e) {
        var b = e.target.closest("button"); if (!b) return;
        S[seg.dataset.key] = b.dataset.v;
        onChange(seg.dataset.key);
      });
    });
  }
  function syncSegs(S) {
    document.querySelectorAll(".seg[data-key]").forEach(function (seg) {
      seg.querySelectorAll("button").forEach(function (b) { b.classList.toggle("on", String(S[seg.dataset.key]) === b.dataset.v); });
    });
  }

  /** スライダー（input[type=range]）と −／＋ ボタン。onInput(数値) を呼ぶ */
  function bindRange(id, onInput, btnStep) {
    var el = $(id);
    el.addEventListener("input", function () { onInput(Number(el.value)); });
    document.querySelectorAll('.step-btn[data-for="' + id + '"]').forEach(function (b) {
      b.addEventListener("click", function () {
        var st = btnStep || Number(el.step) || 1;
        var v = Math.round((Number(el.value) + Number(b.dataset.d) * st) * 1e6) / 1e6;
        v = Math.max(Number(el.min), Math.min(Number(el.max), v));
        el.value = v; onInput(v);
      });
    });
    return el;
  }

  /**
   * アニメーション。step(dt 秒) が false を返すと止まる。button のラベルを ▶／⏸ で切りかえる
   */
  function Player(button, step, labels) {
    labels = labels || ["▶ 再生", "⏸ 停止"];
    var running = false, last = 0, self = this;
    function frame(ts) {
      if (!running) return;
      var dt = last ? Math.min(0.1, (ts - last) / 1000) : 0;
      last = ts;
      if (step(dt) === false) { self.stop(); return; }
      window.requestAnimationFrame(frame);
    }
    this.start = function () { if (running) return; running = true; last = 0; button.textContent = labels[1]; button.classList.add("on"); window.requestAnimationFrame(frame); };
    this.stop = function () { running = false; button.textContent = labels[0]; button.classList.remove("on"); };
    this.toggle = function () { if (running) self.stop(); else self.start(); };
    this.running = function () { return running; };
    button.textContent = labels[0];
    button.addEventListener("click", this.toggle);
  }

  /** 描画をまとめる（スライダーを速く動かしても 1 フレームに 1 回だけ描く） */
  function throttle(fn) {
    var pending = false;
    return function () {
      if (pending) return;
      pending = true;
      window.requestAnimationFrame(function () { pending = false; fn(); });
    };
  }

  var FONT = "Source Sans Pro, Hiragino Kaku Gothic ProN, Noto Sans JP, sans-serif";
  var GRID = "rgba(0,0,0,0.08)";

  function axis(extra) {
    return Object.assign({ zeroline: true, zerolinecolor: "black", zerolinewidth: 1.2, gridcolor: GRID, fixedrange: true }, extra || {});
  }

  function layout(extra) {
    return Object.assign({
      margin: { l: 44, r: 16, t: 30, b: 40 }, paper_bgcolor: "#fff", plot_bgcolor: "#fff",
      legend: { orientation: "h", yanchor: "bottom", y: 1.02, xanchor: "left", x: 0 },
      hovermode: "closest", uirevision: "keep", font: { family: FONT }, shapes: [], annotations: [],
    }, extra || {});
  }

  var CONFIG = { displayModeBar: false, responsive: true };

  function lineTrace(xs, ys, name, color, opt) {
    opt = opt || {};
    return Object.assign({ x: xs, y: ys, name: name, mode: "lines", type: "scatter",
      line: { color: color, width: opt.width || 2.5, dash: opt.dash || "solid" },
      hovertemplate: "(%{x:.3f}, %{y:.3f})<extra>%{fullData.name}</extra>" }, opt.extra || {});
  }

  function pointTrace(xs, ys, name, color, size, extra) {
    return Object.assign({ x: xs, y: ys, name: name, mode: "markers", type: "scatter",
      marker: { color: color, size: size || 11, line: { color: "white", width: 1.5 } },
      hovertemplate: "(%{x:.3f}, %{y:.3f})<extra>%{fullData.name}</extra>" }, extra || {});
  }

  root.UI = {
    $: $, ready: ready, tex: tex, store: store, bindSegs: bindSegs, syncSegs: syncSegs, bindRange: bindRange,
    Player: Player, throttle: throttle, axis: axis, layout: layout, CONFIG: CONFIG, lineTrace: lineTrace, pointTrace: pointTrace,
  };
})(this);
