(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: the seven terms of O_4 integrated over the BPST instanton*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices.  app:inst 「大きい質量の展開。」 (N2b): the seven terms of the FHSS O_4 (the*)
(*note's Omega form) integrated over the BPST background (isospin 1/2, rho = 1, g = 1, regular gauge), compared one by one with the*)
(*reductions of the text: T1 -> -(8P-4R)/21, T2 -> (8/7)(R-P), T3 -> 32P/35, T4 -> 16R/35, T5 -> (48/35)(P-R), T6 -> (64/105)(P-R),*)
(*T7 -> (44/105) R, with int P = 288 int f^8, int R = -96 int f^8, int f^8 d^4x = pi^2/42; the sum gives A_4 = 17/735.*)
(*Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_inst_a4_bpst.txt.*)
(*Usage (from Src/): wolframscript -file deriv_inst_a4_bpst.wl   (a few seconds)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_inst_a4_bpst.wl.  Interactive:  ~/hep/bin/wopen deriv_inst_a4_bpst.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


sig = PauliMatrix /@ {1, 2, 3}; T = sig/2; eps3 = LeviCivitaTensor[3];
eta[a_, m_, n_] := Which[m <= 3 && n <= 3, eps3[[a, m, n]], n == 4 && m <= 3, KroneckerDelta[a, m], m == 4 && n <= 3, -KroneckerDelta[a, n], True, 0];
X = {x1, x2, x3, x4}; r2 = X . X;
A = Table[Sum[2 eta[a, m, n] X[[n]]/(r2 + 1) T[[a]], {a, 3}, {n, 4}], {m, 4}];
G = Table[Simplify[D[A[[n]], X[[m]]] - D[A[[m]], X[[n]]] - I (A[[m]] . A[[n]] - A[[n]] . A[[m]])], {m, 4}, {n, 4}];
Om = -I G;


(* ::Subsubsection:: *)
(*Inspect: the field strength G_12 of BPST (regular gauge, rho = 1)*)


If[$Notebooks,
  MatrixForm[G[[1, 2]]]
]


Dad[m_, M_] := D[M, X[[m]]] - I (A[[m]] . M - M . A[[m]]);
DOm = Table[Simplify[Dad[k, Om[[m, n]]]], {k, 4}, {m, 4}, {n, 4}];
DDOm = Table[Simplify[Dad[k, DOm[[l, m, n]]]], {k, 4}, {l, 4}, {m, 4}, {n, 4}];
onAxis[f_] := f /. {x1 -> r, x2 -> 0, x3 -> 0, x4 -> 0};
radInt[f_] := Integrate[2 Pi^2 r^3 Simplify[onAxis[f]], {r, 0, Infinity}];
sym[f_] := Simplify[onAxis[f] - (f /. {x1 -> r/2, x2 -> r/2, x3 -> r/2, x4 -> r/2})] === 0;
R4 = Range[4];

(* ::Section:: *)
(*the seven terms of O_4 (Omega form)*)


terms = {
  Sum[Tr[Om[[k, l]] . Om[[l, m]] . Om[[m, n]] . Om[[n, k]]], {k, R4}, {l, R4}, {m, R4}, {n, R4}],
  Sum[Tr[DDOm[[k, l, m, n]] . DDOm[[l, k, m, n]]], {k, R4}, {l, R4}, {m, R4}, {n, R4}],
  Sum[Tr[Om[[k, l]] . Om[[l, k]] . Om[[m, n]] . Om[[n, m]]], {k, R4}, {l, R4}, {m, R4}, {n, R4}],
  Sum[Tr[Om[[k, l]] . Om[[l, m]] . Om[[k, n]] . Om[[n, m]]], {k, R4}, {l, R4}, {m, R4}, {n, R4}],
  Sum[Tr[Om[[k, l]] . DOm[[m, l, n]] . DOm[[m, n, k]]], {k, R4}, {l, R4}, {m, R4}, {n, R4}],
  Sum[Tr[Om[[k, l]] . DOm[[l, m, n]] . DOm[[k, n, m]]], {k, R4}, {l, R4}, {m, R4}, {n, R4}],
  Sum[Tr[Om[[k, l]] . Om[[m, n]] . Om[[l, k]] . Om[[n, m]]], {k, R4}, {l, R4}, {m, R4}, {n, R4}]};

(* ::Section:: *)
(*the integrals and the reductions of the text*)


coef = {-1/21, 1/70, 2/35, 4/35, 6/35, 8/105, 11/420};
f8 = Pi^2/42; P = 288 f8; R = -96 f8;
pred = {-(8 P - 4 R)/21, 8/7 (R - P), 32/35 P, 16/35 R, 48/35 (P - R), 64/105 (P - R), 44/105 R};
vals = Table[coef[[i]] radInt[Simplify[terms[[i]]]], {i, 7}];


(* ::Subsubsection:: *)
(*Inspect: the seven integrals*)


If[$Notebooks,
  vals
]


Do[Print["T", i, ": int = ", vals[[i]], " (density spherically symmetric: ", sym[Simplify[terms[[i]]]], ");  reduction gives ", pred[[i]], ";  equal: ", Simplify[vals[[i]] - pred[[i]]] === 0], {i, 7}];
Print["sum = ", Simplify[Total[vals]], " = (48 P + 8 R)/35 = ", Simplify[(48 P + 8 R)/35], ";  A_4 = sum/(24 * 16 pi^2) = ", Simplify[Total[vals]/(24*16 Pi^2)], " (17/735 = ", 17/735, ")"];