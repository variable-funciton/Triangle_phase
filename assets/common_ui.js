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


  /**
   * パラメータのスライダーをまとめて作る。
   *   defs: [{key, label, sub, min, max, step, btn, fmt(v) → 表示文字列, snap(v) → v}]
   *   S[key] に値を入れ、onChange(key) を呼ぶ。戻り値 {sync()}（S の値をスライダーに反映）
   */
  function params(container, defs, S, onChange) {
    var root = typeof container === "string" ? $(container) : container;
    root.innerHTML = defs.map(function (d) {
      var id = "p-" + d.key;
      return '<div class="prm"><div class="top"><span class="name">' + d.label + (d.sub ? "<small>" + d.sub + "</small>" : "") +
        '</span><span class="val" id="v-' + d.key + '"></span></div><div class="row">' +
        '<button class="step-btn" data-for="' + id + '" data-d="-1">−</button>' +
        '<input type="range" id="' + id + '" min="' + d.min + '" max="' + d.max + '" step="' + (d.step || 0.01) + '">' +
        '<button class="step-btn" data-for="' + id + '" data-d="1">＋</button></div></div>';
    }).join("");
    function show(d) { var el = $("v-" + d.key); if (el) el.textContent = d.fmt ? d.fmt(S[d.key]) : String(S[d.key]); }
    defs.forEach(function (d) {
      bindRange("p-" + d.key, function (v) {
        if (d.snap) v = d.snap(v);
        S[d.key] = v; show(d); onChange(d.key);
      }, d.btn);
    });
    return {
      sync: function () { defs.forEach(function (d) { var el = $("p-" + d.key); if (el) el.value = S[d.key]; show(d); }); },
      show: function () { defs.forEach(show); },
    };
  }

  /** π/12 などの倍数の近くなら、その倍数にぴったりそろえる関数を返す */
  function snapTo(q, tol) { return function (v) { var r = Math.round(v / q) * q; return Math.abs(v - r) < (tol || 0.006) ? r : v; }; }

  /** チェックボックスを作る。defs: [{key, label}]。S.show[key] と結ぶ */
  function checks(container, defs, S, onChange) {
    var root = typeof container === "string" ? $(container) : container;
    root.innerHTML = defs.map(function (d) { return '<label><input type="checkbox" data-chk="' + d.key + '"> ' + d.label + "</label>"; }).join("");
    root.querySelectorAll("[data-chk]").forEach(function (c) {
      c.checked = !!S.show[c.dataset.chk];
      c.addEventListener("change", function () { S.show[c.dataset.chk] = c.checked; onChange(c.dataset.chk); });
    });
  }

  /** メトリクス（小さいカード）を並べる。items: [[ラベル, 値(HTML)]] */
  function metrics(container, items) {
    var root = typeof container === "string" ? $(container) : container;
    root.innerHTML = items.map(function (m) { return '<div class="metric"><div class="ml">' + m[0] + '</div><div class="mv">' + m[1] + "</div></div>"; }).join("");
  }

  /** タブ（.tabs の button[data-tab]）と、id="tab-<名前>" の中身を切りかえる */
  function tabs(S, key, onChange) {
    function sync() {
      document.querySelectorAll(".tabs button[data-tab]").forEach(function (b) {
        var on = b.dataset.tab === S[key];
        b.classList.toggle("on", on);
        var pane = $("tab-" + b.dataset.tab); if (pane) pane.hidden = !on;
      });
    }
    document.querySelectorAll(".tabs button[data-tab]").forEach(function (b) {
      b.addEventListener("click", function () { S[key] = b.dataset.tab; sync(); onChange(); });
    });
    sync();
    return sync;
  }

  /** 円の点列（中心 cx, cy、半径 r） */
  function circle(cx, cy, r, n) {
    n = n || 120; var xs = [], ys = [];
    for (var i = 0; i <= n; i++) { var a = 2 * Math.PI * i / n; xs.push(cx + r * Math.cos(a)); ys.push(cy + r * Math.sin(a)); }
    return { x: xs, y: ys };
  }

  /**
   * 矢印（データ座標）from → to を L.annotations に追加。text があれば矢印の先に書く。
   * （Plotly の注釈の文字は矢印の根元に付くので、文字は別の注釈にする）
   */
  function arrow(L, from, to, color, text, opt) {
    opt = opt || {};
    L.annotations.push({ x: to[0], y: to[1], ax: from[0], ay: from[1], xref: opt.xref || "x", yref: opt.yref || "y",
      axref: opt.xref || "x", ayref: opt.yref || "y", showarrow: true, arrowhead: 2, arrowsize: 1.1, arrowwidth: opt.width || 2.2,
      arrowcolor: color, text: "" });
    if (text) {
      var dx = to[0] - from[0], dy = to[1] - from[1], len = Math.hypot(dx, dy) || 1;
      L.annotations.push({ x: to[0], y: to[1], xref: opt.xref || "x", yref: opt.yref || "y", text: text, showarrow: false,
        xshift: 14 * dx / len, yshift: 12 * dy / len, xanchor: dx > 0.2 * len ? "left" : dx < -0.2 * len ? "right" : "center",
        yanchor: dy > 0.2 * len ? "bottom" : dy < -0.2 * len ? "top" : "middle", font: { color: color, size: opt.size || 13 } });
    }
  }

  root.UI = {
    $: $, ready: ready, tex: tex, store: store, bindSegs: bindSegs, syncSegs: syncSegs, bindRange: bindRange,
    Player: Player, throttle: throttle, axis: axis, layout: layout, CONFIG: CONFIG, lineTrace: lineTrace, pointTrace: pointTrace,
    params: params, snapTo: snapTo, checks: checks, metrics: metrics, tabs: tabs, circle: circle, arrow: arrow,
  };
})(this);
