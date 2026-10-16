(* ::Package:: *)

(* ::Title:: *)
(*Step (5): step-(4) interferences converted to MadLoop's conventions (alpha_s^(n_l), four-dimensional spin sums, mu_R)*)


(* ::Text:: *)
(*Research note models/qcd, step (5).  Input: results/scat_mathematica.csv (K W of step (4) in CDR, MS-bar with n_f = 6,*)
(*pole mass, mu = m = 1, SU(3), g = 1) and work/scat/{A,B}/tree.m (Born and colour correlations in D dims).*)
(*For mu = lambda m (L = ln lambda^2), at a fixed value of the coupling (MadLoop takes aS of the param_card as alpha_s(mu_R)):*)
(*  - every loop integral scales as (mu^2)^eps; the only pure pole that does not is the MS-bar coupling counterterm,*)
(*    2 delta_g B(D)/K = -beta0^(6) B(D)/(K eps) (the field counterterms cancel against the residues), so*)
(*      K W(lambda) = K W(1) + L [K W_{-1} + beta0^(6) B4] + (L^2/2) K W_{-2}            (eps^0; poles: (lambda^2)^eps);*)
(*  - alpha_s^(6) = alpha_s^(5) [1 + (g^2/K)(4/3) T_F L] (Eq. (os)) multiplies the Born (~ g^4) by 1 + (g^2/K)(8/3) T_F L,*)
(*    i.e. adds (8/3) T_F L B4 to K (2 Re W) and (4/3) T_F L B4 to K W  (then d(K W)/dL = beta0^(5) B4 + infrared terms);*)
(*  - four-dimensional external states: the finite remainder K W - Z1 (x) B(D) is the same in CDR and with four-dimensional*)
(*    spin sums, and Z1 (x) B(4) has no eps^0 term, so  K W^(4)_fin = K W_fin - [Z1(lambda) (x) B(D)]_{eps^0}; the poles are*)
(*    Z1(lambda) (x) B(4) (Eq. (irpole) with mu -> lambda m and the four-dimensional Born and colour correlations).*)
(*Writes results/madloop_pred.csv: process, lambda, Re K W^(4) (finite), Re of the 1/eps and 1/eps^2 coefficients, B4.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file madloop_predict.wl  (after run_scat_check.sh).  Interactive:  ~/hep/bin/wopen madloop_predict.wl, then "Run All Code".*)


(* ::Section:: *)
(*Setup*)


srcDirMP$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
ep = Epsilon; sun = {CF -> 4/3, CA -> 3};
sv = 10; tv = -3; uv = 2 - sv - tv; m = 1; TF = 1/2; nl = 5; b06 = 11 - 2/3 6;
csv = Import[FileNameJoin[{srcDirMP$, "results", "scat_mathematica.csv"}], "CSV", HeaderLines -> 1];
kw[p_, k_] := First[Cases[csv, {p, k, re_, im_, __} :> re + I im]];
tree[p_] := Get[FileNameJoin[{srcDirMP$, "work", "scat", p, "tree.m"}]];


If[$Notebooks,
  {kw["A", 0], tree["A"][[1]]}
]


(* ::Section:: *)
(*predictions*)


predict[p_, lam_] := Module[{born, cc, w0, wm, bD, b4, c, L = Log[lam^2], lnS, lt, lu, beta, bb, bcoth, ci, gam, z1, w, conv, p1, p2},
   {born, cc, w0, wm} = tree[p];
   bD = born /. sun /. D -> 4 - 2 ep; b4 = bD /. ep -> 0;
   c[i_, j_] := cc[Sort[{i, j}]] /. sun /. D -> 4 - 2 ep;
   beta = Sqrt[1 - 4 m^2/sv]; bb = Log[(1 + beta)/(1 - beta)];
   bcoth = (sv - 2 m^2)/(sv beta) (bb - I Pi);
   lnS = Log[lam^2/sv] + I Pi; lt = Log[lam m/(m^2 - tv)]; lu = Log[lam m/(m^2 - uv)];
   {ci, gam} = If[p === "A", {4/3, -3 (4/3)}, {3, -(11 - 2/3 nl)}];
   (* Z1 (x) B, both light partons alike: -2 C_i/eps^2 + (1/eps)[2 lnS <T1.T2> + gamma_i B - 2 bcoth <T3.T4> - 2 C_F B + 2 sum <TI.Tj> ln] *)
   z1[bf_, cf_] := -2 ci bf/ep^2 + (2 lnS cf[1, 2] + gam bf - 2 bcoth cf[3, 4] - 2 (4/3) bf + 2 (cf[1, 3] lt + cf[1, 4] lu + cf[2, 3] lu + cf[2, 4] lt))/ep;
   w = kw[p, 0] + L (kw[p, -1] + b06 b4) + L^2/2 kw[p, -2] + 4/3 TF L b4;
   conv = Coefficient[Normal[Series[z1[bD, c], {ep, 0, 0}]], ep, 0];
   p2 = Coefficient[z1[b4, c[##] /. ep -> 0 &], ep, -2]; p1 = Coefficient[z1[b4, c[##] /. ep -> 0 &], ep, -1];
   N[{p, lam, Re[w - conv], Re[p1], Re[p2], b4}, 17]];
rows = Flatten[Table[predict[p, lam], {p, {"A", "B"}}, {lam, {1, 2, 1/2}}], 1];
Do[Print["(a) ", r[[1]], " lambda = ", r[[2]], ":  Re K W^(4) finite = ", r[[3]], ",  1/eps: ", r[[4]], ",  1/eps^2: ", r[[5]], ",  B4 = ", r[[6]]], {r, rows}];


If[$Notebooks,
  TableForm[N[rows, 12], TableHeadings -> {None, {"process", "lambda", "Re KW4 fin", "1/eps", "1/eps^2", "B4"}}]
]


Export[FileNameJoin[{srcDirMP$, "results", "madloop_pred.csv"}],
  StringRiffle[Prepend[StringRiffle[ToString[CForm[#]] & /@ #, ","] & /@ rows, "process,lambda,re_KW4_fin,re_KW4_m1,re_KW4_m2,born4"], "\n"] <> "\n", "Text"];
Print["(b) wrote results/madloop_pred.csv"];
