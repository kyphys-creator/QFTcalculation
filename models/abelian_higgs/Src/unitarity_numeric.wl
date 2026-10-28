(* ::Package:: *)

(* ::Title:: *)
(*Step (9): tree-level s-wave partial waves of the coupled channels A_L A_L, h h (C even) and A_L h (C odd)*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (9); no FeynCalc.  Reads results/unitarity_amps.m (the longitudinal tree*)
(*amplitudes M(s, c) of unitarity_feyncalc.wl).  The s wave*)
(*    a0_ij = N_i N_j kappa_ij/(32 pi) Integral_{-1}^{1} dc M_ij(s, c),  kappa = 2 sqrt(p_i p_f)/sqrt(s),*)
(*N = 1/sqrt 2 for A_L A_L and h h, 1 for A_L h; unitarity of the coupled channels requires |Re a| <= 1/2 for every*)
(*eigenvalue a.  A_L h has C = -1 and does not mix with A_L A_L, h h.*)
(*  (a) the limit s -> infinity: the lam part (1/(16 pi))(-3 lam, lam; lam, -3 lam) and -lam/(8 pi), eigenvalues*)
(*      -lam/(4 pi), -lam/(8 pi), -lam/(8 pi), so lam <= 2 pi, MH <= sqrt(4 pi) v; and the e^2 ln s of the vector*)
(*      exchange in the t and u channels (forward peak): d a0/d ln s -> -e^2/(8 pi) for A_L A_L -> h h and A_L h;*)
(*  (b) the eigenvalues at the benchmark (e = 1/2, MA = 1, MH = 5/2) and at MH = 6.5 for sqrt(s) up to 10^4.  For*)
(*      MH > 2 MA the u-channel A of A_L h -> A_L h can be on shell inside the physical region (u runs from 2 MA^2 +*)
(*      2 MH^2 - s to (MH^2 - MA^2)^2/s), so only sqrt(s) > (MH^2 - MA^2)/MA (and > 2 MH) is used;*)
(*  (c) the largest MH/MA with all |Re a| <= 1/2 for e = 1/2 and e = 1/10, against sqrt(4 pi)/e;*)
(*  results/unitarity_tree.csv, results/unitarity_bound.csv, results/unitarity_curves.csv (e = 1/10, MH = 32.5).*)
(*Batch: wolframscript -file unitarity_numeric.wl*)


srcDirUN$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirUN$ = FileNameJoin[{srcDirUN$, "results"}];
$NumberMarks = False;
cell$[y_] := If[StringQ[y], y, ToString[CForm[Chop[N[y, 16], 10^-30]]]];
amps$ = Association[Get[FileNameJoin[{resDirUN$, "unitarity_amps.m"}]]];
lamOf$ = ee^2 MH^2/(2 MA^2);

pmom$[m1_, m2_] := Sqrt[(s - (m1 + m2)^2) (s - (m1 - m2)^2)]/(2 Sqrt[s]);
kap$ = <|"LL" -> 2 pmom$[MA, MA]/Sqrt[s], "LLhh" -> 2 Sqrt[pmom$[MA, MA] pmom$[MH, MH]]/Sqrt[s],
    "hh" -> 2 pmom$[MH, MH]/Sqrt[s], "Lh" -> 2 pmom$[MA, MH]/Sqrt[s]|>;
nn$ = <|"LL" -> 1/2, "LLhh" -> 1/2, "hh" -> 1/2, "Lh" -> 1|>;
(* numerical partial wave at exact parameters *)
a0$[proc_, vals_] := Module[{m = amps$[proc] /. vals, k = N[kap$[proc] /. vals, 40]},
   nn$[proc] k/(32 Pi) NIntegrate[m, {c, -1, 1}, WorkingPrecision -> 40, PrecisionGoal -> 20, AccuracyGoal -> 25,
     MaxRecursion -> 30]];
eigs$[vals_] := Module[{a11 = a0$["LL", vals], a12 = a0$["LLhh", vals], a22 = a0$["hh", vals], a33 = a0$["Lh", vals]},
   Join[Sort[Eigenvalues[{{a11, a12}, {a12, a22}}]], {a33}, {a11, a12, a22}]];


(* ::Section:: *)
(*(a) the high-energy limit*)


limLam$ = {-6, 2, -6, -2} lamOf$;      (* lam parts of the fixed-c limits (unitarity_feyncalc.wl (c)) *)
mLam$ = 1/(16 Pi) {{nn$["LL"] limLam$[[1]] 2, nn$["LLhh"] limLam$[[2]] 2}, {nn$["LLhh"] limLam$[[2]] 2, nn$["hh"] limLam$[[3]] 2}};
Print["(a) lam part of the C-even s-wave matrix: ", mLam$ /. lamOf$ -> lam, ";  eigenvalues ", Eigenvalues[mLam$ /. lamOf$ -> lam],
  ";  A_L h: ", nn$["Lh"] limLam$[[4]] 2/(32 Pi) /. lamOf$ -> lam];
Print["(a) |a| = 1/2: lam = ", Solve[lam/(4 Pi) == 1/2, lam], ",  MH/MA = sqrt(2 lam)/e = sqrt(4 pi)/e = ", N[Sqrt[4 Pi]/ee /. ee -> 1/2, 8],
  " (e = 1/2)"];
(* d a0/d ln s at large s from two energies *)
Module[{v1 = {ee -> 1/2, MA -> 1, MH -> 5/2, s -> 10^8}, v2 = {ee -> 1/2, MA -> 1, MH -> 5/2, s -> 10^10}, d},
  d = Table[(a0$[p, v2] - a0$[p, v1])/Log[100], {p, {"LL", "LLhh", "hh", "Lh"}}];
  Print["(a) d a0/d ln s between sqrt(s) = 10^4 and 10^5 (benchmark), in units of e^2/(8 pi): ", N[d/(1/4/(8 Pi)), 6],
   "  (expect 0, -1, 0, -1)"]];


(* ::Section:: *)
(*(b) eigenvalues at finite energy*)


rsList$ = <|5/2 -> {10, 30, 100, 300, 1000, 10^4}, 13/2 -> {50, 100, 300, 1000, 10^4}|>;
treeRows$ = Flatten[Table[Module[{vals = {ee -> 1/2, MA -> 1, MH -> mh, s -> rs^2}, ev, lv},
     ev = eigs$[vals]; lv = lamOf$ /. vals;
     Print["(b) MH = ", mh, ", sqrt(s) = ", rs, ": C-even eigenvalues ", N[ev[[1 ;; 2]], 8], ", A_L h ", N[ev[[3]], 8],
       ";  (a11, a12, a22) = ", N[ev[[4 ;; 6]], 6], ";  lam limits -lam/(4 pi) = ", N[-lv/(4 Pi), 6], ", -lam/(8 pi) = ", N[-lv/(8 Pi), 6]];
     Join[{mh, rs}, ev]], {mh, {5/2, 13/2}}, {rs, rsList$[mh]}], 1];
Export[FileNameJoin[{resDirUN$, "unitarity_tree.csv"}],
  Map[cell$, Prepend[treeRows$, {"MH", "sqrt_s", "eig_even_1", "eig_even_2", "a_Lh", "a11", "a12", "a22"}], {2}], "CSV"];

(* curves for the figure: e = 1/10, MH = 32.5 MA (the same lam = 5.28 as MH = 6.5 at e = 1/2), sqrt(s) = 1100 ... 10^6 *)
curveRows$ = Table[Module[{vals = {ee -> 1/10, MA -> 1, MH -> 65/2, s -> 10^(2 x)}, ev},
    ev = eigs$[vals]; Join[{N[10^x]}, ev]], {x, Log10[1100], 6, 1/20}];
Export[FileNameJoin[{resDirUN$, "unitarity_curves.csv"}],
  Map[cell$, Prepend[curveRows$, {"sqrt_s", "eig_even_1", "eig_even_2", "a_Lh", "a11", "a12", "a22"}], {2}], "CSV"];


(* ::Section:: *)
(*(c) the largest MH/MA with |Re a| <= 1/2*)


maxAbs$[ev_, mh_?NumericQ, rs_] := Quiet[Max[Abs[Re[eigs$[{ee -> ev, MA -> 1, MH -> mh, s -> rs^2}][[1 ;; 3]]]]], NIntegrate::precw];
boundRows$ = Flatten[Table[Module[{mhc, ref = N[Sqrt[4 Pi]/ev, 10]},
     mhc = mh /. FindRoot[maxAbs$[ev, SetPrecision[mh, 40], rs] - 1/2, {mh, 0.8 ref, 1.25 ref}, Method -> "Brent",
         WorkingPrecision -> 30, AccuracyGoal -> 10, PrecisionGoal -> 10];
     Print["(c) e = ", ev, ", sqrt(s) = ", rs, ": largest MH/MA = ", N[mhc, 8], "  (sqrt(4 pi)/e = ", ref, ", ratio ", N[mhc/ref, 6], ")"];
     {ev, rs, mhc, ref}], {ev, {1/2, 1/10}}, {rs, If[ev == 1/2, {100, 300, 1000, 10^4, 10^5}, {3000, 10^4, 10^5}]}], 1];
Export[FileNameJoin[{resDirUN$, "unitarity_bound.csv"}],
  Map[cell$, Prepend[boundRows$, {"e", "sqrt_s", "MH_over_MA_max", "sqrt4pi_over_e"}], {2}], "CSV"];
Print["(c) written results/unitarity_tree.csv, results/unitarity_curves.csv, results/unitarity_bound.csv"];
