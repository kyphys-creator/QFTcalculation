# QFTcalculation

場の量子論の摂動計算（主に1ループ、一部は2ループ）を、自分で組んだツール群で行い、独立な方法で検算して研究ノートにまとめるリポジトリ。

ツールの本体はリポジトリの外（`~/hep`、`~/Library/Wolfram/Applications`、conda 環境 `qft`）にある。ここに置くのは、環境の構築記録とその試験、模型ごとの計算スクリプトと研究ノートである。

## 構成

```
environment/
  environment.tex, .pdf   環境の構築記録：導入したツール、この環境に固有の問題と対処、検証、使い方
  tests/                  環境の試験（run_all.sh）。lhc/ は LHC の道具、eftdm/ は EFT・暗黒物質の道具、geant4/ は Geant4 の照合
  interactive/            スクリプトをセルごとに実行できる形にする道具と、その検証（README.md）
  files/                  ツールへの局所パッチ、入口ファイル、ラッパー
loop_tools_review/        ループ計算のツールの比較レビュー（環境はこの推奨に沿って組んだ）
models/<模型>/
  Src/                    計算スクリプト（.wl、.py、.f90）と検算の実行スクリプト run_*_check.sh
    generated/            FeynRules・NLOCT が書き出した模型（FeynArts の模型、UFO、対抗項）
    results/              検算の数値（CSV）
  ResearchNote/note.pdf   導出、結果、検算の記録
  figs/                   ノートの図
models/backup_20261009/   旧環境から退避した自作の FeynRules・FeynArts の模型（README.md）
simulation/<流れ>/         模型（.fr）から検出器の模擬と表示までの一連の流れ（FeynRules → MG5 → Pythia 8 → Geant4 → Qt）と、その検算
```

## 環境

詳しくは [environment/environment.pdf](environment/environment.pdf) を参照。

| 分野 | ツール | 記録 |
|---|---|---|
| 振幅の代数・図の生成 | FeynCalc 10.2.1、FeynArts 3.12、FeynHelpers 2、FormCalc 9.10、FORM 5.0.2 | 第3節 |
| 1ループ積分 | LoopTools 2.16、COLLIER 1.2.10、Package-X 2.1.1 | 第3節 |
| 模型の作成 | FeynRules 2.3.49 + NLOCT（局所パッチ2つ） | 第3節 |
| 自動の NLO・事象の生成 | MG5_aMC@NLO 3.8.1（MadLoop、HEPTools） | 第3節 |
| 有限温度・相転移・重力波 | DRalgo、Matchete、PT2GWFinder、FindBounce、CosmoTransitions、PhaseTracer2、BSMPT、TransitionListener、WallGo | 第7節 |
| 2ループ | Kira 3.1、FIRE 7.1、AMFlow 2.0、pySecDec 1.6.6、feyntrop 1.1.0、TSIL 1.46 | 第8節 |
| LHC の現象論 | LHAPDF 6.5.5、Pythia 8.317、Delphes 3.5.1、ROOT 6.32.14、MadAnalysis5 1.11.0、pyhf、SModelS 3.2.1、HiggsTools 1.3 | 第9節 |
| EFT・暗黒物質 | wilson、DsixTools 2.1、DirectDM、MadDM 3.3、micrOMEGAs 7.1.10 | 第10節 |
| 物質中の輸送・検出器の模擬 | Geant4 11.4.3（マルチスレッド、Qt 6、13組のデータ）、geant4_pybind 0.1.3 | 第11節 |

計算機は2台ある。1ループの中核、熱的な道具、2ループの道具は Apple M3 の Mac（`~` は `/Users/koichiro`）に入れた。LHC と EFT・暗黒物質の道具、Geant4 は Mac Studio（`~` は `/Users/koichiromacstudio`）に入れた。

## 模型のノート

| 模型 | 内容 | ノート |
|---|---|---|
| `phi3` | φ³ 理論（d=4, 6）：1ループと2ループの構造、繰り込み群、ユニタリー性、真空の崩壊 | [note.pdf](models/phi3/ResearchNote/note.pdf) |
| `phi34` | φ³+φ⁴ 理論：1ループの構造、ユニタリー性、偽の真空の崩壊と1ループの前因子 | [note.pdf](models/phi34/ResearchNote/note.pdf) |
| `phi34_thermal` | φ³+φ⁴ 理論の有限温度の一次相転移と重力波 | [note.pdf](models/phi34_thermal/ResearchNote/note.pdf) |
| `yukawa_ps` | 擬スカラー湯川理論：1ループの構造、γ⁵ の処方、有効ポテンシャルと真空の安定性 | [note.pdf](models/yukawa_ps/ResearchNote/note.pdf) |
| `spinor_qed` | スピノル QED（電子と μ 粒子）：g−2、光子–光子散乱、Uehling のポテンシャル、Schwinger の対生成 | [note.pdf](models/spinor_qed/ResearchNote/note.pdf) |
| `qcd` | QCD：1ループと2ループの構造、e⁺e⁻→ハドロン、重いクォークの対生成、インスタントン | [note.pdf](models/qcd/ResearchNote/note.pdf) |
| `sm` | 標準模型：MS-bar の電弱の1ループの繰り込み（V_CKM=1、FJ のタドポール、一般の R_ξ ゲージ） | [note.pdf](models/sm/ResearchNote/note.pdf) |
| `sm_ckm` | 標準模型と CKM 行列：湯川行列の MS-bar の繰り込みと世代を変える過程 | [note.pdf](models/sm_ckm/ResearchNote/note.pdf) |
| `sm_higgs` | ヒッグスの崩壊：NLO の部分幅と分岐比 | [note.pdf](models/sm_higgs/ResearchNote/note.pdf) |
| `sm_nlo` | 標準模型の NLO の物理量：実の放射を含む崩壊幅、ρ パラメータ、Z 極、m_W | [note.pdf](models/sm_nlo/ResearchNote/note.pdf) |
| `abelian_higgs` | アーベル・ヒッグス模型（U(1) のゲージ場と電荷1の複素スカラー）：一般の R_ξ ゲージの1ループの構造（FJ のタドポール、Slavnov–Taylor 恒等式、ゲージ依存の打ち消し）、繰り込み群、極質量、木の振幅と等価定理、ゲージによらない極質量、3点・4点の対抗項と NLOCT、NLO の Γ(h→AA) と MadLoop、繰り込み群の走りと自明性の限界、背景場の R_ξ と Fermi ゲージの有効ポテンシャルと Nielsen 恒等式（真空期待値の走りと SSV の γ̂）、Coleman–Weinberg の機構（M_h²/M_A²=3e²/8π²、繰り込み群による改良）、摂動のユニタリー性（A_LA_L、hh、A_Lh の部分波、λ≤2π と1ループの補正）。現在は手順 (9) まで | [note.pdf](models/abelian_higgs/ResearchNote/note.pdf) |

どのノートも、おおむね「目的と問い」「設定」「結果」「検算の計画」「検算」「議論と今後」の順に書き、導出は付録に置く。

## シミュレーションの流れ

| 流れ | 内容 | 説明 |
|---|---|---|
| `stable_lepton` | SM + 安定なベクトル的荷電レプトン（500 GeV）：pp → lv⁺lv⁻ を Pythia 8 と簡略化した円筒の検出器（Geant4）に通し、Qt で表示する。Si のエネルギー損失、飛跡の曲率、飛行時間と質量を自前の計算と照合する | [README.md](simulation/stable_lepton/README.md) |

## 使い方

### 環境の試験

ツールを更新したら、環境の試験をすべて実行し直す。結果は `environment/tests/out/log.txt` に書かれる。

```bash
environment/tests/run_all.sh --no-mg5
```

オプションなしで実行すると、10項目すべての試験を行う（MadGraph の試験を含む）。`--no-mg5` は MadGraph の試験を飛ばす。ほかに次のオプションで照合を加えられる。

| オプション | 照合する道具 | 時間の目安 |
|---|---|---|
| `--thermal` | 熱的な道具 | 約50分 |
| `--twoloop` | 2ループの道具 | 約12分 |
| `--lhc` | LHC の道具（6段階） | 約1.5時間、出力は 10 GB を超える |
| `--eftdm` | EFT・暗黒物質の道具 | 約5分 |
| `--geant4` | Geant4（配布の例を参照の出力と、G4NDL・G4TENDL をデータのファイルと、geant4_pybind を C++ と） | 約35秒 |

### 模型の検算を実行し直す

各ノートの手順は `Src/run_*_check.sh` で実行し直せる。どこから起動してもよい（スクリプトが自分の場所に移る）。何を計算し、何を書き出すか、先に要るものは何かは、各スクリプトの冒頭に書いてある。`Src/generated/` の模型はリポジトリに入っている。ただし、大きな生成物は入っていないので、使う前に作り直す（下の「取り決め」）。模型を変えたら `generate_<模型>.wl` で作り直す。

```bash
models/phi3/Src/run_oneloop4_check.sh
```

### スクリプトを対話的に動かす

スクリプトは、まとめて実行することも、セルごとに実行して途中の式や図を確かめることもできる。

```bash
cd models/phi3/Src
wolframscript -file oneloop4_feyncalc.wl              # まとめて実行（Inspect セルは飛ばす）
~/hep/bin/wopen $PWD/oneloop4_feyncalc.wl             # Mathematica 14.2.1 のノートブックとして開く
~/miniforge3/envs/qft/bin/python oneloop4_numeric.py  # まとめて実行。VS Code では # %% のセルを「Run Cell」で実行
```

VS Code では、[.vscode/settings.json](.vscode/settings.json) で conda 環境 `qft` の Python を指定している。ただし、パスは M3 の Mac のもの（`/Users/koichiro/...`）である。変換と検証の道具は [environment/interactive/README.md](environment/interactive/README.md) にある。

### Mathematica でのパッケージの読み込み

```mathematica
(* FeynCalc + FeynArts（パッチ版）+ FeynHelpers *)
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
<< FeynCalc`

(* FeynArts（パッチなし）+ FormCalc。FeynCalc とは別のカーネルで *)
<< FeynArts`
<< FormCalc`

(* Package-X *)
<< X`
```

## 取り決め

- 正しさは、既知の厳密値、独立な別実装、独立な解析計算のいずれかとの数値の一致で判定する。手順ごとに、記号の計算（FeynCalc、FeynArts）、数値（LoopTools、COLLIER、Package-X）、独立な実装（MadLoop、aMC@NLO など）を突き合わせる。
- 文献の値と比べるときは、ノート自身の模型で計算した量を使う。文献の値は「参照」として示す。
- 評価する Feynman 図は、評価する前のセルで表示する。
- FeynRules、FormCalc（パッチなしの FeynArts）、NLOCT のスクリプトは、FeynCalc と同じカーネルで動かさない。
- 大きな生成物（NLOCT の出力など）は git に入れていない。スクリプトで作り直す（[.gitignore](.gitignore) に作り直し方を書いてある）。

## 注意

この環境で分かったツールの問題と、その対処は environment.pdf の第4節にまとめてある。特に次の点に注意する。

- 閾値より下で外運動量がゼロでない場合、LoopTools の `C0` は誤った値を返し、その誤りは `C00` にも及ぶ。`C0` と `C00` には Package-X か COLLIER を使う。
- √s ≫ m では、COLLIER の箱図が精度を失う。
- MadLoop は、QCD と QED の摂動しか受け付けない。
- MG5_aMC@NLO は自分のディレクトリから起動する。
- MG5_aMC@NLO は、Python 2 の形の UFO をその場で書き換える。リポジトリの UFO は、写しを読ませる。
- FeynRules は局所パッチ2つ（`FeynRules.m`、`Core/Loop.m`）を前提に動く。入れ直したら [environment/files/](environment/files/) のパッチを当て直す。
- Geant4 を使うシェルでは、先に `source ~/hep/opt/geant4env.sh` とする（Qt 6 を conda の環境 `g4` から取るため）。Python からは `~/miniforge3/envs/g4/bin/python` で geant4_pybind を使う。
- Geant4 で熱中性子を扱うときは `_HP` の物理リストを使う。HP なしのリストは、Au の熱中性子の捕獲を 51% 大きく見積もる。TENDL を使うのは `_AllHP`（`_HPT` は熱中性子の散乱を加えたもの）。
- Mac Studio（36 GB）で大きな C++ を構築するときは、並列を 6 ほどに抑え、LTO を切る。geant4_pybind を既定の LTO のまま作ったら、リンクでメモリを使い切って Mac がフリーズした。
