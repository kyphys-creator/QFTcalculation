(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: the D-dimensional Dirac algebra of the two-loop diagram (c)*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices (FeynCalc 10.2.1).  app:rg 「C_F T_F n_f の部分の手計算。」 (Z2): the two contraction*)
(*identities, the trace N^{alpha beta} of diagram (c) contracted with g and with k k (k = l1 - l2) in terms of D1..D5 against the text, the*)
(*shortcuts (l1-q) kslash (l2-q) = D3 (l2-q) - D4 (l1-q) and l2 kslash l1 = D1 l2 - D2 l1, the colour factor tr(T^a T^c T^b T^c)*)
(*(independent of deriv_twoloop_cftf.py).*)
(*Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_twoloop_trace.txt.*)
(*Usage (from Src/): wolframscript -file deriv_twoloop_trace.wl   (a few seconds)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_twoloop_trace.wl.  Interactive:  ~/hep/bin/wopen deriv_twoloop_trace.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
Get["FeynCalc`"]; $FCAdvice = False;
FCClearScalarProducts[];
sp = {SPD[l1, l1] -> d1, SPD[l2, l2] -> d2, SPD[q, q] -> qq, SPD[l1, q] -> (d1 + qq - d3)/2, SPD[l2, q] -> (d2 + qq - d4)/2, SPD[l1, l2] -> (d1 + d2 - d5)/2};

(* ::Section:: *)
(*the contraction identities*)


(* the identities *)
id1 = DiracSimplify[GAD[mu] . GSD[a] . GAD[al] . GSD[b] . GAD[mu] - (-2 GSD[b] . GAD[al] . GSD[a] + (4 - D) GSD[a] . GAD[al] . GSD[b])];
id2 = DiracSimplify[GAD[al] . GSD[x] . GSD[y] . GAD[al] - (4 SPD[x, y] - (4 - D) GSD[x] . GSD[y])];
Print["gamma^mu a gamma^al b gamma_mu = -2 b gamma^al a + (4-D) a gamma^al b: ", id1 === 0];
Print["gamma^al x y gamma_al = 4 x.y - (4-D) x y: ", id2 === 0];

(* ::Section:: *)
(*the trace of diagram (c)*)


(* the trace with the two internal-gluon indices contracted with g, and with k k (k = l1 - l2) *)
tr[gb_, ga_] := DiracTrace[GAD[mu] . (GSD[l1] - GSD[q]) . gb . (GSD[l2] - GSD[q]) . GAD[mu] . GSD[l2] . ga . GSD[l1]];
nF = Expand[FCE[ExpandScalarProduct[DiracSimplify[tr[GAD[al], GAD[al]] /. DiracTrace[z_] :> DiracTrace[z, DiracTraceEvaluate -> True]]]] /. sp];


(* ::Subsubsection:: *)
(*Inspect: g_ab N^ab of diagram (c) in D1..D5*)


If[$Notebooks,
  Factor[nF]
]


nL = Expand[FCE[ExpandScalarProduct[DiracSimplify[tr[GSD[l1] - GSD[l2], GSD[l1] - GSD[l2]] /. DiracTrace[z_] :> DiracTrace[z, DiracTraceEvaluate -> True]]]] /. sp];
nFtext = (D - 2) (-4 qq^2 + 2 (D - 8) qq d5 - 4 d5^2 + 4 (qq + d5) (d1 + d2 + d3 + d4) - 4 (d1 + d4) (d2 + d3) - 2 (D - 4) (d1 d4 + d2 d3));
(* k k part: tr[gamma^mu (D3 b - D4 a) gamma_mu (D1 l2 - D2 l1)] = -4(D-2)[D1 D3 b.l2 - D2 D3 b.l1 - D1 D4 a.l2 + D2 D4 a.l1] *)
bl2 = (d2 + d4 - qq)/2; bl1 = Expand[(d1 + d2 - d5)/2 - (d1 + qq - d3)/2]; al2 = Expand[(d1 + d2 - d5)/2 - (d2 + qq - d4)/2]; al1 = (d1 + d3 - qq)/2;
nLtext = -4 (D - 2) (d1 d3 bl2 - d2 d3 bl1 - d1 d4 al2 + d2 d4 al1);
Print["g_ab N^ab (FeynCalc) - text: ", Simplify[nF - nFtext]];
Print["k_a k_b N^ab (FeynCalc) - text: ", Simplify[nL - nLtext]];

(* ::Section:: *)
(*the shortcuts and the colour factor*)


(* the two shortcuts *)
Print["(l1-q) k (l2-q) = D3 (l2-q) - D4 (l1-q): ", Expand[FCE[ExpandScalarProduct[DiracOrder[DiracSimplify[DiracGammaExpand[(GSD[l1 - q]) . (GSD[l1 - l2]) . (GSD[l2 - q]) - (SPD[l1 - q, l1 - q] GSD[l2 - q] - SPD[l2 - q, l2 - q] GSD[l1 - q])]]]]]] === 0];
Print["l2 k l1 = D1 l2 - D2 l1: ", Expand[FCE[ExpandScalarProduct[DiracOrder[DiracSimplify[DiracGammaExpand[GSD[l2] . GSD[l1 - l2] . GSD[l1] - (SPD[l1, l1] GSD[l2] - SPD[l2, l2] GSD[l1])]]]]]] === 0];
(* colour: tr(T^a T^c T^b T^c) = (C_F - C_A/2) T_F delta^ab, with FeynCalc's T_F = 1/2 *)
Print["tr(T^a T^c T^b T^c) / delta^ab = ", FCE[SUNSimplify[SUNTrace[SUNT[a, c, b, c]], SUNNToCACF -> True]] /. SD[a, b] -> 1, "  (expect (C_F - C_A/2)/2)"];