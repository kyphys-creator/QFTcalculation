(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: D-dimensional Dirac algebra of e+e- -> hadrons at NLO*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices (FeynCalc 10.2.1).*)
(*  The contraction identities used in the text; app:tree 「(D) e+e- -> q qbar g。」 and app:ee 「実の補正。」 (E4, E1): the hadronic*)
(*  tensor of gamma* -> q qbar g in D dimensions (t11, t22 and the cross traces), -g H_3/(-g H_2/s) in y13, y23 and at D = 4 in x1, x2;*)
(*  app:ee 「仮想の補正。」 (E2): the vertex numerator trace T = tr[N^mu p2 gamma_mu p1] in the hand form, the pieces of the text, the*)
(*  gauge-part identities with on-shell spinors, and TID: T/(D1 D2 D3) -> 2(D-2) s [(D-7) B0 - 2 s C0], the gauge part scaleless.*)
(*Each line prints OK (0) or the residual.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_ee_feyncalc.txt.*)
(*Usage (from Src/): wolframscript -file deriv_ee_feyncalc.wl   (a few seconds)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_ee_feyncalc.wl.  Interactive:  ~/hep/bin/wopen deriv_ee_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
Get["FeynCalc`"];
$FCAdvice = False;
chk[name_, expr_] := Print[name, ": ", If[TrueQ[Simplify[expr] === 0], "OK (0)", Simplify[expr]]];


(* ::Section:: *)
(*D-dimensional identities used in the text*)


FCClearScalarProducts[];
chk["id1 g^al a g^mu b g_al = -2 b g^mu a + (4-D) a g^mu b",
  DiracSimplify[GAD[al].GSD[a].GAD[mu].GSD[b].GAD[al] - (-2 GSD[b].GAD[mu].GSD[a] + (4 - D) GSD[a].GAD[mu].GSD[b])]];
chk["id2 g^mu a b g_mu = 4 a.b - (4-D) a b",
  DiracSimplify[GAD[mu].GSD[a].GSD[b].GAD[mu] - (4 SPD[a, b] - (4 - D) GSD[a].GSD[b])]];
chk["id3 g^mu a g_mu = -(D-2) a", DiracSimplify[GAD[mu].GSD[a].GAD[mu] + (D - 2) GSD[a]]];


(* ::Section:: *)
(*E4/E1: hadronic tensor of gamma* -> q(k1) qbar(k2) g(k3), D dims*)


FCClearScalarProducts[];
SPD[k1, k1] = 0; SPD[k2, k2] = 0; SPD[k3, k3] = 0;
SPD[k1, k2] = s12/2; SPD[k1, k3] = s13/2; SPD[k2, k3] = s23/2;
sRule = s12 -> s - s13 - s23;
P13 = k1 + k3; P23 = k2 + k3;
tr4[a_, b_, c_, d_] := DiracSimplify[DiracTrace[GSD[a].GSD[b].GSD[c].GSD[d]]];
(* |Gamma1|^2, |Gamma2|^2 with g_{mu mu'} g_{nu nu'} *)
t11 = DiracSimplify[DiracTrace[GSD[k1].GAD[nu].GSD[P13].GAD[mu].GSD[k2].GAD[mu].GSD[P13].GAD[nu]]];
t22 = DiracSimplify[DiracTrace[GSD[k1].GAD[mu].GSD[P23].GAD[nu].GSD[k2].GAD[nu].GSD[P23].GAD[mu]]];
x12 = DiracSimplify[DiracTrace[GSD[k1].GAD[nu].GSD[P13].GAD[mu].GSD[k2].GAD[nu].GSD[P23].GAD[mu]]];
x21 = DiracSimplify[DiracTrace[GSD[k1].GAD[mu].GSD[P23].GAD[nu].GSD[k2].GAD[mu].GSD[P13].GAD[nu]]];
chk["tr[k1 P13 k2 P13] = 2 s13 s23", tr4[k1, P13, k2, P13] - 2 s13 s23];
chk["tr[k1 P23 k2 P23] = 2 s13 s23", tr4[k1, P23, k2, P23] - 2 s13 s23];
chk["t11 = (D-2)^2 2 s13 s23", t11 - (D - 2)^2 2 s13 s23];
chk["t22 = (D-2)^2 2 s13 s23", t22 - (D - 2)^2 2 s13 s23];
chk["P13.P23 = s/2", (ExpandScalarProduct[SPD[k1 + k3, k2 + k3]] /. sRule) - s/2];
chk["tr[k1 k2 P13 P23] = 2 s s12", (tr4[k1, k2, P13, P23] /. sRule) - 2 s s12 /. sRule];
chk["tr[k1 P13 k2 P23] = 2 s13 s23", (tr4[k1, P13, k2, P23] /. sRule) - 2 s13 s23];
chk["tr[k1 P13] = 2 s13", DiracSimplify[DiracTrace[GSD[k1].GSD[P13]]] - 2 s13];
chk["cross trace X (intermediate form)",
  ExpandScalarProduct[(x12 - (-8 SPD[P13, P23] DiracSimplify[DiracTrace[GSD[k1].GSD[k2]]] + 2 (4 - D) tr4[k1, k2, P13, P23]
     + 4 (4 - D) SPD[k2, P23] DiracSimplify[DiracTrace[GSD[k1].GSD[P13]]] - (4 - D)^2 tr4[k1, P13, k2, P23]))] /. sRule];
chk["cross trace X = -4(D-2) s s12 - 2(D-4)(D-2) s13 s23", (x12 - (-4 (D - 2) s s12 - 2 (D - 4) (D - 2) s13 s23)) /. sRule];
chk["second cross trace equals the first (real)", (x21 - x12) /. sRule];
h3 = t11/s13^2 + t22/s23^2 - (x12 + x21)/(s13 s23);
h3hand = (D - 2) (2 (D - 2) (s13/s23 + s23/s13) + 8 s s12/(s13 s23) + 4 (D - 4));
chk["-g H3/(g^2 C_F d_F) = (D-2)[2(D-2)(s13/s23+s23/s13) + 8 s s12/(s13 s23) + 4(D-4)]", (h3 - h3hand) /. sRule];
h2 = -DiracSimplify[DiracTrace[GSD[k1].GAD[mu].GSD[k2].GAD[mu]]] /. sRule /. s12 -> s;
FCClearScalarProducts[]; SPD[k1, k1] = 0; SPD[k2, k2] = 0; SPD[k1, k2] = s/2;
h2 = -DiracSimplify[DiracTrace[GSD[k1].GAD[mu].GSD[k2].GAD[mu]]];
chk["-g H2/d_F = 2(D-2) s", h2 - 2 (D - 2) s];
ratio = Simplify[(h3hand/(h2/s)) /. {s13 -> s y13, s23 -> s y23, s12 -> s (1 - y13 - y23)}];


(* ::Subsubsection:: *)
(*Inspect: -g H3/(-g H2/s) in y13, y23 (D dimensions, units C_F g^2)*)


If[$Notebooks,
  ratio
]


chk["ratio = [4+(D-2)(y13^2+y23^2)+2(D-4)y13 y23-4(y13+y23)]/(y13 y23) (note app:ee)",
  ratio - (4 + (D - 2) (y13^2 + y23^2) + 2 (D - 4) y13 y23 - 4 (y13 + y23))/(y13 y23)];
chk["D=4: -gH3/(8 g^2 C_F d_F) = s13/s23+s23/s13+2 s s12/(s13 s23)", (h3hand /. D -> 4) - 8 (s13/s23 + s23/s13 + 2 s s12/(s13 s23))];
chk["D=4 bracket in x: (x1^2+x2^2)/((1-x1)(1-x2))",
  Simplify[(s13/s23 + s23/s13 + 2 s s12/(s13 s23)) /. {s23 -> s (1 - x1), s13 -> s (1 - x2), s12 -> s (x1 + x2 - 1)}] - (x1^2 + x2^2)/((1 - x1) (1 - x2))];
chk["ratio in D: = 2[x1^2+x2^2 - eps x3^2]/((1-x1)(1-x2)) (D=4-2eps; info)",
  (ratio /. {y23 -> 1 - x1, y13 -> 1 - x2} /. D -> 4 - 2 eps) - 2 (x1^2 + x2^2 - eps (2 - x1 - x2)^2)/((1 - x1) (1 - x2))];


(* ::Section:: *)
(*E2: vertex numerator trace and TID*)


FCClearScalarProducts[];
SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[p1, p2] = s/2;
aa = p1 - k; bb = p2 + k;
num = GAD[al].GSD[aa].GAD[mu].GSD[bb].GAD[al];
T = DiracSimplify[DiracTrace[num.GSD[p2].GAD[mu].GSD[p1]]] // ExpandScalarProduct // Expand;
Thand = -8 s^2 - 16 s x + 16 s y + 32 x y + (4 - D) (4 s^2 + 8 s (x - y) - 4 s K - 16 x y) + 2 (4 - D)^2 s K;
kRule = {Pair[Momentum[k, D], Momentum[p1, D]] -> x, Pair[Momentum[k, D], Momentum[p2, D]] -> y, Pair[Momentum[k, D], Momentum[k, D]] -> K};


(* ::Subsubsection:: *)
(*Inspect: the vertex numerator trace T in x = k.p1, y = k.p2, K = k^2*)


If[$Notebooks,
  Collect[Expand[FCI[T] /. kRule], {x, y, K}, Factor]
]


chk["T = tr[N^mu p2 g_mu p1] (hand form)", Expand[FCI[T] /. kRule] - Expand[Thand]];
chk["tr[b a p2 p1] = 2s^2 + 4 s (x-y) - 2 s K",
  FCI[ExpandScalarProduct[DiracSimplify[DiracTrace[GSD[bb].GSD[aa].GSD[p2].GSD[p1]]]]] /. kRule // Expand // # - (2 s^2 + 4 s (x - y) - 2 s K) &];
chk["tr[a b p2 p1] = -2 s K",
  FCI[ExpandScalarProduct[DiracSimplify[DiracTrace[GSD[aa].GSD[bb].GSD[p2].GSD[p1]]]]] /. kRule // Expand // # + 2 s K &];
chk["Born trace tr[g^mu p2 g_mu p1] = -2(D-2)s", DiracSimplify[DiracTrace[GAD[mu].GSD[p2].GAD[mu].GSD[p1]]] + 2 (D - 2) s];
(* gauge part: u(p1) kslash (p1slash - kslash) = -D2 u(p1): check (kslash(p1-k) + D2) p1slash... via traces with projectors *)
chk["gauge-part: kslash.(p1-k) = 2k.p1 - k^2 - p1slash.kslash", DiracSimplify[DiracOrder[DiracSimplify[GSD[k].GSD[p1 - k] - (2 SPD[k, p1] - SPD[k, k] - GSD[p1].GSD[k])]]] // ExpandScalarProduct];
chk["gauge-part: (p2+k).kslash = 2k.p2 + k^2 - kslash.p2slash", DiracSimplify[DiracOrder[DiracSimplify[GSD[p2 + k].GSD[k] - (2 SPD[k, p2] + SPD[k, k] - GSD[k].GSD[p2])]]] // ExpandScalarProduct];
(* with the spinors: u(p1) kslash (p1-k) = -D2 u(p1) and (p2+k) kslash v(p2) = D3 v(p2) *)
chk["ubar(p1) kslash(p1-k)slash = -D2 ubar(p1)", DiracSimplify[SpinorUBarD[p1, 0].GSD[k].GSD[p1 - k] + (SPD[k, k] - 2 SPD[k, p1]) SpinorUBarD[p1, 0]] // ExpandScalarProduct];
chk["(p2+k)slash kslash v(p2) = D3 v(p2)", DiracSimplify[GSD[p2 + k].GSD[k].SpinorVD[p2, 0] - (SPD[k, k] + 2 SPD[k, p2]) SpinorVD[p2, 0]] // ExpandScalarProduct];
(* TID: int d^Dk T/(D1 D2 D3), D1 = k^2, D2 = (k-p1)^2, D3 = (k+p2)^2 *)
SPD[p1 + p2, p1 + p2] = s;
Tint = T FAD[k, k - p1, k + p2];
tid = TID[Tint, k, ToPaVe -> True] // PaVeReduce // Simplify;
Print["TID of T/(D1 D2 D3) (FeynCalc, I Pi^2 PaVe): ", InputForm[tid]];
target = I Pi^2 2 (D - 2) s ((D - 7) B0[s, 0, 0] - 2 s C0[0, s, 0, 0, 0, 0]);
Print["TID / [I Pi^2 2(D-2) s] = ", InputForm[Simplify[tid/(I Pi^2 2 (D - 2) s)]]];


(* ::Subsubsection:: *)
(*Inspect: the reduced vertex: TID of T/(D1 D2 D3)*)


If[$Notebooks,
  tid
]


(* gauge part through TID: numerator with kslash on both ends, propagator 1/k^4 *)
numG = GSD[k].GSD[aa].GAD[mu].GSD[bb].GSD[k];
TG = DiracSimplify[DiracTrace[numG.GSD[p2].GAD[mu].GSD[p1]]] // ExpandScalarProduct // Expand;
tidG = TID[TG FAD[k, k, k - p1, k + p2], k, ToPaVe -> True] // PaVeReduce // Simplify;
Print["gauge part (k k/k^4 term) after TID: ", InputForm[tidG], "  (expect 0: scaleless)"];