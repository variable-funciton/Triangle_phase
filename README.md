# 三角関数の動くグラフ（数学IB 後期）

Streamlit Community Cloud で公開する、三角関数の学習用 Web アプリです。

## ページ構成

| ページ | 内容 | 関連課題 |
|---|---|---|
| 三角比・三角関数の公式まとめ | 有名角の度数法・弧度法と sin/cos/tan の値（単位円の図）、ラジアンと扇形、三角比の定義・相互関係・角の変換・グラフの性質、正弦定理・余弦定理（三角形と外接円の図）、加法定理と派生公式、公式を数値で確かめる | 後期課題1〜3・7・8 |
| 一般形 `y = A sin B(x − t) + β` | 振幅・周期・平行移動を 4 つのスライダーで操作。①重ねて比較 ②段階的に変形 ③アニメーション（ブラウザ側で再生） | 後期課題4・5・6 |
| sin と cos の位相差 | `sin(x − t)` と `cos x` を重ねて π/2 の位相差と周期性を確認（旧 `traingle_sincos_phase`） | 後期課題3・4・5 |
| テントマップの変換と合成 | `y = a f(b(x−p)) + q` の拡大・縮小・平行移動・反転（旧 `Expand_transform`）、HTML/PDF 保存、合成関数 f(g(x)) と g(f(x))、f の n 回合成、蜘蛛の巣図 | 後期課題5・12 |
| 三角関数の合成 | `a sin x + b cos x = R sin(x+α) = R cos(x+β)`。点 (a, b) と角 α、2 つの波の和、回転するベクトルのアニメーション、sin 形と cos 形、区間での最大・最小 | 後期課題8 |
| 積和・和積の公式 | 加法定理からの導き方、15° の倍数の角で厳密に確かめる、うなりのグラフ、類題 | 後期課題7・8 |
| 三角関数の足し合わせ（フーリエ級数） | 矩形波・のこぎり波・三角波・半波／全波整流を sin, cos の和で近づける。項を足していくアニメーション、スペクトル、自分で係数を決めて波を作る（微分積分なしの入門） | 後期課題4・5（応用） |
| 斜方投射 | 初速度と角度を変えて投げるアニメーション、5 つの角度の同時比較、飛距離 L(θ) のグラフ、2倍角の公式で 45° が最大になることの説明 | 後期課題7（応用） |
| モンキーハンティング | (a, b) を狙って投げると同時に B を自由落下させるアニメーション、½gt² のずれの可視化、当たる条件 v₀ > √(g(a²+b²)/2b) のグラフ、狙いのずれ・放す時刻のずれで外れる様子 | 後期課題1〜3（応用） |
| バネの単振動と波 | 等速円運動の影としての単振動、動摩擦（振幅が等差数列で減り止まる）・速さに比例する抵抗（等比数列）のアニメーション、横波・縦波の伝わり方、縦波の横波表示 | 後期課題1〜5・9・10（応用） |

## ファイル構成

```
streamlit_app.py      エントリーポイント（ページ一覧はここで管理）
views/                各ページ
  home.py
  basics.py           三角比・三角関数の公式まとめ
  general_form.py
  phase_shift.py
  tent_map.py         テントマップの変換と合成
  synthesis.py        三角関数の合成
  product_sum.py      積和・和積の公式
  fourier.py          三角関数の足し合わせ（フーリエ級数）
  projectile.py       斜方投射
  monkey.py           モンキーハンティング
  spring.py           バネの単振動と波
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
```

## ページの追加方法

1. `views/` に新しいファイル（例: `unit_circle.py`）を作る
2. `streamlit_app.py` の `PAGES` に `st.Page("views/unit_circle.py", title="…")` を 1 行追加する

`st.set_page_config` は `streamlit_app.py` で一度だけ呼ぶので、各ページでは呼ばないこと。
