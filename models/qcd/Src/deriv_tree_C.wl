(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: g g -> g g colour projections of the Feynman-rule diagrams (FeynCalc)*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices (FeynCalc 10.2.1).*)
(*  app:tree 「(C) gg -> gg。」 (T3): the four Feynman-rule diagrams of the note (amplitude as in tree_feyncalc.wl) projected onto*)
(*  c_s = f^{abe} f^{cde}, c_t = f^{ace} f^{bde} for general SU(N), with the CM linear polarizations of the text, symbolic in c = cos(theta)*)
(*  (s = 4, E = 1): M = -g^2 (c_s X + c_t Y) with the table of X, Y; the colour matrix; the polarization sum of X^2 + Y^2 + XY.*)
(*Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_tree_C.txt.*)
(*Usage (from Src/): wolframscript -file deriv_tree_C.wl   (about 5 s)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_tree_C.wl.  Interactive:  ~/hep/bin/wopen deriv_tree_C.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
Get["FeynCalc`"];
$FCAdvice = False;

(* ::Section:: *)
(*kinematics, polarizations and the Feynman-rule amplitude*)


sn = Sqrt[1 - c^2];
vec = <|p1 -> {1, 0, 0, 1}, p2 -> {1, 0, 0, -1}, k1 -> {1, sn, 0, c}, k2 -> {1, -sn, 0, -c}|>;
xh = {0, 1, 0, 0}; yh = {0, 0, 1, 0}; th = {0, c, 0, -sn};
mink[a_, b_] := a[[1]] b[[1]] - a[[2 ;;]] . b[[2 ;;]];
setVecs[pols_] := Module[{all = Join[Normal[vec], {e1 -> pols[[1]], e2 -> pols[[2]], e3 -> pols[[3]], e4 -> pols[[4]]}]},
   FCClearScalarProducts[];
   Do[ScalarProduct[a[[1]], b[[1]]] = Simplify[mink[a[[2]], b[[2]]]], {a, all}, {b, all}]];
(* the note's diagrams (Fig. rules), incoming momenta p1, p2, -k1, -k2, polarizations e1..e4 (from tree_feyncalc.wl) *)
v3[{m1_, q1_}, {m2_, q2_}, {m3_, q3_}] := MT[m1, m2] FV[q1 - q2, m3] + MT[m2, m3] FV[q2 - q3, m1] + MT[m3, m1] FV[q3 - q1, m2];
pc = Contract[ExpandScalarProduct[#]] &;
sp[a_, b_] := Pair[Momentum[a], Momentum[b]];
f4[a_, b_, cc_, d_] := SUNF[SUNIndex[a], SUNIndex[b], SUNIndex[ee]] SUNF[SUNIndex[cc], SUNIndex[d], SUNIndex[ee]];
amp[] := Module[{lorS, lorT, lorU, s = 4, t = -2 (1 - c), u = -2 (1 + c)},
   lorS = pc[FV[e1, mu] FV[e2, nu] v3[{mu, p1}, {nu, p2}, {al, -p1 - p2}] v3[{al, p1 + p2}, {ro, -k1}, {si, -k2}] FV[e3, ro] FV[e4, si]];
   lorT = pc[FV[e1, mu] FV[e3, ro] v3[{mu, p1}, {ro, -k1}, {al, k1 - p1}] v3[{al, p1 - k1}, {nu, p2}, {si, -k2}] FV[e2, nu] FV[e4, si]];
   lorU = pc[FV[e1, mu] FV[e4, si] v3[{mu, p1}, {si, -k2}, {al, k2 - p1}] v3[{al, p1 - k2}, {nu, p2}, {ro, -k1}] FV[e2, nu] FV[e3, ro]];
   -1/s f4[a1, a2, a3, a4] lorS - 1/t f4[a1, a3, a2, a4] lorT - 1/u f4[a1, a4, a2, a3] lorU -
    (f4[a1, a2, a3, a4] pc[sp[e1, e3] sp[e2, e4] - sp[e1, e4] sp[e2, e3]] + f4[a1, a3, a2, a4] pc[sp[e1, e2] sp[e3, e4] - sp[e1, e4] sp[e2, e3]] +
      f4[a1, a4, a2, a3] pc[sp[e1, e2] sp[e3, e4] - sp[e1, e3] sp[e2, e4]])];


(* ::Subsubsection:: *)
(*Inspect: the amplitude for the polarizations x x y y (before the colour projection)*)


If[$Notebooks,
  setVecs[{xh, xh, yh, yh}]; Simplify[amp[]]
]


(* ::Section:: *)
(*colour projections*)


cS = SUNF[SUNIndex[a1], SUNIndex[a2], SUNIndex[hh]] SUNF[SUNIndex[a3], SUNIndex[a4], SUNIndex[hh]];
cT = SUNF[SUNIndex[a1], SUNIndex[a3], SUNIndex[hh]] SUNF[SUNIndex[a2], SUNIndex[a4], SUNIndex[hh]];
proj[x_, cc_] := Simplify[SUNSimplify[Expand[x cc], SUNNToCACF -> True] /. SUNN -> CA];
cS2 = cS /. hh -> hh2; cT2 = cT /. hh -> hh2;
gram = {{proj[cS, cS2], proj[cS, cT2]}, {proj[cT, cS2], proj[cT, cT2]}};
Print["colour matrix in (c_s, c_t) / (CA^2 dA): ", Simplify[gram/(CA^2 (CA^2 - 1)) /. CF -> (CA^2 - 1)/(2 CA)], "   (expect {{1, 1/2}, {1/2, 1}})"];


(* ::Subsubsection:: *)
(*Inspect: the colour matrix (SUNN = C_A)*)


If[$Notebooks,
  MatrixForm[gram]
]


(* ::Section:: *)
(*the 16 polarization configurations*)


expect = <|"xxxx" -> {(3 + c^2)/(1 + c), -2 (3 + c^2)/(1 - c^2)}, "yyyy" -> {(3 + c^2)/(1 + c), -2 (3 + c^2)/(1 - c^2)},
   "xxyy" -> {1 - c, -2}, "yyxx" -> {1 - c, -2}, "xyxy" -> {2, -4/(1 - c)}, "yxyx" -> {2, -4/(1 - c)},
   "xyyx" -> {-2 (1 - c)/(1 + c), 4/(1 + c)}, "yxxy" -> {-2 (1 - c)/(1 + c), 4/(1 + c)}|>;
pv = {<|"x" -> xh, "y" -> yh|>, <|"x" -> xh, "y" -> yh|>, <|"x" -> th, "y" -> yh|>, <|"x" -> th, "y" -> yh|>};
tot = 0; allok = True;
Do[
  Module[{cfg = StringJoin[cf], m, pr, xy, ok},
   setVecs[Table[pv[[i]][cf[[i]]], {i, 4}]];
   m = amp[];
   pr = {proj[m, cS], proj[m, cT]};
   xy = -Simplify[LinearSolve[gram, pr] /. CF -> (CA^2 - 1)/(2 CA)];   (* M = -(c_s X + c_t Y), g = 1 *)
   ok = If[OddQ[Count[cf, "y"]], Simplify[xy] === {0, 0}, Simplify[xy - expect[cfg]] === {0, 0}];
   allok = allok && ok;
   tot += xy[[1]]^2 + xy[[2]]^2 + xy[[1]] xy[[2]];
   Print[cfg, ": (X, Y) = ", Simplify[xy], If[ok, "   OK", "   FAIL"]]],
  {cf, Tuples[{"x", "y"}, 4]}];
Print["sum over polarizations of X^2+Y^2+XY - 4(3+c^2)^3/(1-c^2)^2 = ", Simplify[tot - 4 (3 + c^2)^3/(1 - c^2)^2], "   (expect 0)"];
Print["all configurations OK: ", allok];


(* ::Subsubsection:: *)
(*Inspect: the polarization sum of X^2 + Y^2 + XY*)


If[$Notebooks,
  Simplify[tot]
]
