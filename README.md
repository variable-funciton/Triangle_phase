# 三角関数の動くグラフ（数学IB 後期）

Streamlit Community Cloud で公開する、三角関数の学習用 Web アプリです。

## ページ構成

| ページ | 内容 | 関連課題 |
|---|---|---|
| 三角比・三角関数の公式まとめ | 有名角の度数法・弧度法と sin/cos/tan の値（単位円の図）、ラジアンと扇形、三角比の定義・相互関係・角の変換・グラフの性質、正弦定理・余弦定理（三角形と外接円の図）、加法定理と派生公式、公式を数値で確かめる | 後期課題1〜3・7・8 |
| 一般形 `y = A sin B(x − α) + β` | 「表示の設定」（基本の関数・角度の単位・α の入れ方）と「パラメータ」（A, B, α, β のスライダー）を別の囲みに分け、スライダーを動かすとグラフと式が連続的に変わる（ブラウザ側で描画）。式を大きく表示、①重ねて比較（キーポイントと矢印・Bx − α の形との比較は任意）②段階的に変形 | 後期課題4・5・6 |
| sin と cos の位相差 | `sin(x − t)` と `cos x` を重ねて π/2 の位相差と周期性を確認（旧 `traingle_sincos_phase`） | 後期課題3・4・5 |
| テントマップの変換と合成 | `y = a f(b(x−p)) + q` の拡大・縮小・平行移動・反転（旧 `Expand_transform`）、HTML/PDF 保存、合成関数 f(g(x)) と g(f(x))、f の n 回合成、蜘蛛の巣図 | 後期課題5・12 |
| 加法定理とその証明 | sin・cos・tan の加法定理、単位円上の 2 点の距離（回転）による cos(α − β) の証明（α, β を動かせる図）、余弦定理による別証明、残りの公式の導き方、sin 75° = sin(45° + 30°) などの例題 | 後期課題7 |
| 三角関数の合成 | `a sin x + b cos x = R sin(x+α) = R cos(x+β)`。点 (a, b) と角 α、2 つの波の和、回転するベクトルのアニメーション、sin 形と cos 形、区間での最大・最小 | 後期課題8 |
| 積和・和積の公式 | 加法定理からの導き方、15° の倍数の角で厳密に確かめる、うなりのグラフ、類題 | 後期課題7・8 |
| 三角関数の足し合わせ（フーリエ級数） | 矩形波・のこぎり波・三角波・半波／全波整流を sin, cos の和で近づける。項を足していくアニメーション、スペクトル、自分で係数を決めて波を作る（微分積分なしの入門） | 後期課題4・5（応用） |
| 斜方投射 | 初速度と角度を変えて投げるアニメーション、5 つの角度の同時比較、飛距離 L(θ) のグラフ、2倍角の公式で 45° が最大になることの説明、詳しい解説（運動の分解・軌跡の式・最高点・よくある間違い・練習問題） | 後期課題7（応用） |
| モンキーハンティング | (a, b) を狙って投げると同時に B を自由落下させるアニメーション、½gt² のずれの可視化、当たる条件 v₀ > √(g(a²+b²)/2b) のグラフ、狙いのずれ・放す時刻のずれで外れる様子、詳しい解説（三角比・重ね合わせ・相対運動・当たる条件・練習問題） | 後期課題1〜3（応用） |
| バネの単振動と波 | 等速円運動の影としての単振動、動摩擦（振幅が等差数列で減り止まる）・速さに比例する抵抗（等比数列）のアニメーション、横波・縦波の伝わり方、縦波の横波表示、詳しい解説（円運動の影から ω = √(k/m)・エネルギー・摩擦で等差数列になる理由・波の式・練習問題） | 後期課題1〜5・9・10（応用） |
| 媒介変数表示とリサージュ図形 | `x = A sin(at + δ), y = B sin bt` の軌跡。a, b, δ, A, B を連続的に変えるスライダー、点を動かす・δ を変化させるアニメーション、x(t)・y(t) の波形の投影、a : b と辺に接する回数、a = b のときの位相差の読み取り、よく出る形のボタン | 後期課題4〜7（応用） |
| 逆三角関数と主値 | arcsin・arccos・arctan を元の関数の y = x に関する折り返しとして表示、主値の範囲の色づけ、対応する点 P(θ, k)・Q(k, θ)、制限しないで折り返すと関数にならない様子、三角方程式の解（範囲を選んで一覧）と一般解 | 後期課題3・6（発展） |
| 接線の傾きと cos x | sin x（cos x）上を動く点の接線と傾きの三角形、傾きを点 (a, m) としてためると cos x（−sin x）が現れるアニメーション、割線 PQ から h → 0 で接線に近づける、有名角での傾きの表 | 発展（微分の入り口） |
| テイラー展開（多項式で近似） | x₀ と次数 n のスライダー、次数を上げる・x₀ を動かすアニメーション、展開した式（有名角ではぴったりの値、文字のままの形、小数の係数の形）、誤差 0.01 未満の範囲 | 発展（微分の入り口） |
| 【学科共通】観覧車の高さ | h = h₀ − r cos(2πt/T) のアニメーション、一般形との対応、高さ H 以上にいる時間（三角不等式） | 後期課題4〜6 |
| 【学科共通】季節の変化 | 札幌・東京・那覇の月平均気温（気象庁平年値 1991〜2020）に sin を手で合わせる・最小二乗（合成の公式）で答え、緯度と昼の長さ | 後期課題4〜6・8 |
| 【機械】クランク機構 | ピストン位置 x = r cos θ + √(l² − r² sin² θ)（余弦定理）、単振動との比較、連接棒の傾き（正弦定理） | 後期課題1〜3 |
| 【機械】回転と弧度法 | 転がる車輪（弧の長さ rθ）、rpm と角速度・周速、歯車（歯数比）、ベルト車 | 後期課題1（弧度法） |
| 【機械】斜面と力の分解 | mg sin θ・mg cos θ の分解図、すべり出す条件 tan θ > μ（摩擦角）、すべるアニメーション | 後期課題1〜3 |
| 【電気】交流と三角関数 | 50/60 Hz、回転ベクトル、実効値（v² の平均と 2 倍角の公式）、電流の位相 | 後期課題4〜7 |
| 【電気】三相交流 | 120° ずれた 3 相と和が 0（加法定理）、ベクトルをつなげる図、ずれを変えると 0 でなくなる、線間電圧 √3 倍 | 後期課題7・8 |
| 【電気】交流の電力と力率 | p = vi を積和の公式で変形、平均電力 VI cos φ、電力がもどる部分の色分け | 後期課題7・8 |
| 【化学】分子の形と結合角 | 結合角と結合距離から原子間距離（余弦定理）、代表的な分子、メタンの正四面体を立方体で（3D） | 後期課題1〜3 |
| 【化学】X 線回折 | 原子の面と X 線の道のりの差 2d sin θ、2 つの反射波の和、N 枚の面での強さと角度 | 後期課題1〜3・8 |
| 【都市】日影と建物の間隔 | 南中高度 90° − φ + δ、影の長さ H / tan h、建物の間隔、1 日の日影曲線 | 後期課題1〜3 |
| 【都市】測量 | 仰角で高さ（tan）、川幅（正弦定理）、トラバース測量（方位角と Δx = L cos a、Δy = L sin a、閉合誤差） | 後期課題1〜3 |
| 【都市】勾配の表し方 | %・‰・寸勾配・比と tan θ、角度とパーセントが比例しないこと、斜距離と水平距離 | 後期課題1〜3 |

学科別の応用ページには、それぞれ「🔗 参考リンク・関連ページ」（公的機関・辞典・大学や高専の講義資料へのリンクと、このアプリの関連ページ）を付けている。

## 演習（各単元の練習問題）

「応用数学ラボ」（applied-mathematics リポジトリ）と同じしくみの演習ページを、各単元の最後に置いている。

| ページ | 問題の型（基本 / 標準） | ファイル |
|---|---|---|
| 演習（基礎） | 度数法⇔弧度法、有名角の値、扇形、相互関係 / 負の角の値、正弦定理、余弦定理、加法定理、2倍角 | `exercises/basics.py` |
| 演習（グラフ） | 周期、最大値・最小値、三角方程式、角の変換 / 平行移動の量、グラフから式（図あり）、三角不等式 | `exercises/graph.py` |
| 演習（変換と合成） | 合成関数の値、漸化式 / 変換したグラフの頂点、合成のくり返し | `exercises/transform.py` |
| 演習（加法定理の応用） | 加法定理の公式、加法定理で値（sin 75° = sin(45° + 30°) など分け方つき）、合成、積和、和積 / 加法定理で値（分け方も考える・tan・弧度法）、加法定理（三角比の値から）、合成と最大・最小、区間での最大・最小、積和・和積で値 | `exercises/addition.py` |
| 演習（物理への応用） | 飛距離、滞空時間、単振動の周期、波、リサージュ / 最高点、モンキーハンティング | `exercises/physics.py` |
| 演習（学科別の応用） | 【共通】【機械】【電気】【化学】【都市】の 16 の型（学科でしぼれる） | `exercises/applied.py` |
| 演習（発展） | 逆三角関数の値、接線の傾き、テイラー展開の係数 / arcsin(sin θ)、テイラー展開で近似値 | `exercises/advanced.py` |

- 難易度と問題の型を選び、4 択で解く。答えを選ぶと正誤と、誤答なら間違えやすい点（`why`）が出る。ヒントは 1 段ずつ。
- 「セット番号」が同じなら同じ問題が出る。「同じ型でもう一問」で数値だけを変えた類題になる。
- 表示中の問題を LaTeX 一式（`数学IB演習.tex` / `数学IB演習-Ans.tex` + `problems.tex` / `answers.tex`）の zip でダウンロードできる。
  年度・科目名・クラスの行は `exercises/core.py` の `NENDO`・`SUBJECT`・`CLASS_LINE` で変える。
- 学生用 PDF（問題 → 解答・解説）はサーバーで uplatex + dvipdfmx を使って作る。`packages.txt` に日本語 LaTeX を入れてある
  （初回のデプロイは数分長くかかる）。LaTeX がない環境では、代わりに印刷用ページ（.html）を出す。
- 問題を増やすときは、`exercises/*.py` に生成関数（`random.Random` を受け取り `Problem` を返す）を書いて `REGISTRY` に登録する。
  誤答は典型的な間違いから作り、`why` にその誤答を選んだときの指摘を書く。`python -m tests.test_exercises` で全部の型を確かめられる。

## ファイル構成

```
streamlit_app.py      エントリーポイント（ページ一覧はここで管理）
views/                各ページ
  home.py
  basics.py           三角比・三角関数の公式まとめ
  general_form.py     一般形（画面は assets/general_form.html をブラウザで動かす）
  phase_shift.py
  tent_map.py         テントマップの変換と合成
  addition_theorem.py 加法定理とその証明
  synthesis.py        三角関数の合成
  product_sum.py      積和・和積の公式
  fourier.py          三角関数の足し合わせ（フーリエ級数）
  projectile.py       斜方投射
  monkey.py           モンキーハンティング
  spring.py           バネの単振動と波
  lissajous.py        媒介変数表示とリサージュ図形
  inverse_trig.py     逆三角関数と主値
  tangent_slope.py    接線の傾きと cos x
  taylor.py           テイラー展開
  ferris.py / seasons.py                        学科共通の応用
  crank.py / rotation.py / incline.py           機械系
  ac.py / three_phase.py / ac_power.py          電気系
  molecule.py / bragg.py                        化学系
  shadow.py / survey.py / slope.py              都市系
explain/              物理のページの「詳しい解説」タブ（projectile.py・monkey.py・spring.py）
assets/               ブラウザ側で動く画面（スライダーを動かすとグラフが連続的に変わるページ）
  common.css / common_core.js / common_ui.js   共通の見た目・計算・部品
  <名前>.html / <名前>_core.js                  各ページの画面と計算（ページのファイル名と同じ名前）
exercises/            演習（core.py：画面・LaTeX・PDF、fig.py：図、各単元の問題生成）
utils/                共通部品
  formulas.py         公式の一覧（表示用 LaTeX と数値確認用の関数）・三角形の計算
  angles.py           π の分数・度数の表示（π/2, −3π/4, 90° など）
  trig.py             y = A f(B(x − t)) + β の計算（Streamlit に依存しない）
  tent.py             テントマップ・台形関数の変換と合成
  exact.py            1, √2, √3, √6 を使った厳密計算（15° の倍数の sin・cos）
  synthesis.py        三角関数の合成の計算（R, α, β, 区間の最大・最小）
  fourier.py          フーリエ級数の係数と部分和
  projectile.py       斜方投射の計算（滞空時間・最高点・飛距離）
  monkey.py           モンキーハンティングの計算（命中判定・最小の初速度）
  oscillation.py      単振動（摩擦・抵抗あり）と波の計算
  widget.py           assets/ の画面をページに埋め込む
  plotting.py         Plotly 描画の共通部品
tests/test_utils.py   計算部分のテスト
requirements.txt / packages.txt（日本語フォント、PDF 保存用の Chromium）
```

## 公開手順（Streamlit Community Cloud）

1. このリポジトリを GitHub に push する
2. https://share.streamlit.io で **Create app** → リポジトリ `Triangle_phase`、ブランチ `main`
3. **Main file path** に `streamlit_app.py` を指定して Deploy

## ローカルでの確認

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
python -m tests.test_utils       # 計算部分のテスト
python -m tests.test_synthesis   # 合成・積和和積のテスト
python -m tests.test_projectile  # 斜方投射のテスト
python -m tests.test_monkey      # モンキーハンティングのテスト
python -m tests.test_tent        # テントマップのテスト
python -m tests.test_fourier     # フーリエ級数のテスト
python -m tests.test_oscillation # 単振動と波のテスト
python -m tests.test_formulas    # 公式まとめのテスト
node tests/test_general_form_js.js  # 一般形ページ（JavaScript）のテスト
node tests/test_widgets_js.js       # 逆三角関数・接線・テイラー・リサージュ（JavaScript）のテスト
node tests/test_applied_js.js       # 学科別の応用ページ（JavaScript）のテスト
python -m tests.test_exercises      # 演習の問題生成のテスト
```

## ページの追加方法

1. `views/` に新しいファイル（例: `unit_circle.py`）を作る
2. `streamlit_app.py` の `PAGES` に `st.Page("views/unit_circle.py", title="…")` を 1 行追加する

`st.set_page_config` は `streamlit_app.py` で一度だけ呼ぶので、各ページでは呼ばないこと。

スライダーをドラッグしている間もグラフを動かしたいページは、`assets/<名前>.html`（と `<名前>_core.js`）を作り、
ページからは `from utils.widget import render` → `render("<名前>", height=…)` で埋め込む。
HTML の中の `/*__CSS__*/`・`/*__COMMON__*/`・`/*__CORE__*/` が共通部品と計算のファイルに置きかわる。
Plotly.js と KaTeX は cdn.jsdelivr.net から読み込む。
