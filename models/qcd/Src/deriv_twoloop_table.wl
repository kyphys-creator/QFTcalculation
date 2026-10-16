(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: the two-loop class tables, the counterterm rows, z_22, z_21, beta_1 and the finite parts*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices.  Reads results/twoloop_perdiag.m (deriv_twoloop_perdiag.wl; its sum equals*)
(*results/twoloop_reduction.m).  Each diagram: K^2 Pi^(2)/g^4 = b J_bub2 + s J_sun/(-q^2) (bare, Landau gauge, mu^2 = -q^2).*)
(*  app:rg 「図の組ごとの値と z_21、z~_21（式 (z2)）。」, tab:twoloopclass, tab:twoloopclassgh:*)
(*  (1) the class sums equal the b, s of the tables, exactly in eps; every diagram is used once;*)
(*  (2) the 1/eps^3 cancels in every class; the 1/eps^2, 1/eps entries of the tables;*)
(*  (3) the counterterm rows, z_22, z_21, z~_22, z~_21, beta_1 of Eq. (z2) / Eq. (zalpha); the "-1/2" relation of the double poles;*)
(*  (4) 「繰り込んだ有限部分。」: the eps^0 parts and the renormalized finite parts (against results/twoloop_z.csv), and the numbers quoted*)
(*      in the text (J_bub2, J_sun to higher order, the inserted one-loop coefficients, b_{-1} = -s_{-2}/4).*)
(*Reads results/twoloop_perdiag.m, results/twoloop_z.csv.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_twoloop_table.txt.*)
(*Usage (from Src/): wolframscript -file deriv_twoloop_table.wl   (about 5 s)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_twoloop_table.wl.  Interactive:  ~/hep/bin/wopen deriv_twoloop_table.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


srcDirZ1$ = Which[StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName], $Notebooks, NotebookDirectory[], True, Directory[]];
dat = Get[FileNameJoin[{srcDirZ1$, "results", "twoloop_perdiag.m"}]];
vg = #["value"] & /@ dat["gluon"]; vc = #["value"] & /@ dat["ghost"];
Print["diagrams: gluon ", Length[vg], ", ghost ", Length[vc]];
bsOf[x_] := {Coefficient[x, GLI["k2", {1, 1, 1, 1, 0}]], -qq Coefficient[x, GLI["k2", {1, 0, 0, 1, 1}]]} /. D -> 4 - 2 ep;


(* ::Section:: *)
(*the table: {name, diagram numbers (FeynArts order), colour, b, s, {eps^-2, eps^-1}}*)


cF = CF TF nf; cA = CA TF nf;
tabG = {
  {"(a) g loop + g, c loop insertion", {16, 17}, CA^2, 0, (26 - 37 ep + 14 ep^2) (8 - 17 ep - 4 ep^2 + 8 ep^3)/(4 ep (1 + ep) (3 - 2 ep)), {13/3, 817/72}},
  {"c loop + c self-energy", {13, 14}, CA^2, 0, (1 - ep)/(2 ep), {1/8, 11/16}},
  {"(b) gluons only", {10}, CA^2, -(46 - 124 ep - 128 ep^2 + 333 ep^3 - 142 ep^4)/(32 ep (3 - 2 ep)),
      (46 - 143 ep - 65 ep^2 + 447 ep^3 - 402 ep^4 + 112 ep^5)/(8 ep^2 (3 - 2 ep)), {1, 29/6}},
  {"(d) ghost loop (rung 1, triangles 2)", {5, 8, 9}, CA^2, -(2 + 11 ep - 14 ep^2)/(32 ep (3 - 2 ep)), (2 - 2 ep - 3 ep^2 + 4 ep^3)/(8 ep^2 (3 - 2 ep)), {-1/12, -107/576}},
  {"(e)(f) four-gluon vertex", {2, 3, 19, 23}, CA^2, -3 (5 - 3 ep)^2/32, -3 (15 - 72 ep + 74 ep^2 - 22 ep^3)/(8 ep), {-15/4, -573/64}},
  {"(a) g loop + q loop insertion", {15}, cA, 0, -4 (1 - ep) (8 - 17 ep - 4 ep^2 + 8 ep^3)/(ep (1 + ep) (3 - 2 ep)), {-8/3, -73/9}},
  {"quark triangles", {6, 7}, cA, 2 (1 - ep) (5 - 7 ep)/(3 - 2 ep), -4 (1 - ep) (5 - 12 ep + 8 ep^2)/(ep (3 - 2 ep)), {5/3, 23/18}},
  {"(c) quark loop, C_A part", {4}, cA, -2 (1 - ep) (2 - ep + 2 ep^2)/(ep (3 - 2 ep)), 8 (1 - ep) (1 - 2 ep) (2 - 2 ep + ep^2)/(ep^2 (3 - 2 ep)), {0, 1}},
  {"(c) quark loop, C_F part", {4}, cF, 4 (1 - ep) (2 - ep + 2 ep^2)/(ep (3 - 2 ep)), -16 (1 - ep) (1 - 2 ep) (2 - 2 ep + ep^2)/(ep^2 (3 - 2 ep)), {0, -2}},
  {"q loop + q self-energy", {11, 12}, cF, 0, 0, {0, 0}},
  {"scaleless", {1, 18, 20, 21, 22}, CA^2, 0, 0, {0, 0}}};
tabC = {
  {"(g) g, c loop insertion", {5, 7}, CA^2, 0, -(1 - ep) (26 - 37 ep + 14 ep^2)/(8 ep (1 + ep)), {-13/16, -5/2}},
  {"c self-energy on the ghost line", {6}, CA^2, 0, -(3 - 2 ep)^2 (1 - 2 ep)/(8 ep), {-9/32, -57/64}},
  {"(h) three-gluon vertex", {3}, CA^2, (3 - 2 ep) (4 - 3 ep - 6 ep^2)/(64 ep), -(3 - 2 ep) (1 - 2 ep) (4 - 5 ep)/(16 ep^2), {0, -63/128}},
  {"two gluons on the ghost line", {2}, CA^2, -(2 - 11 ep + 12 ep^2 - 4 ep^3)/(64 ep), (1 - 2 ep) (2 - 12 ep + 13 ep^2 - 4 ep^3)/(16 ep^2), {0, -3/128}},
  {"(g) q loop insertion", {4}, cA, 0, 2 (1 - ep)^2/(ep (1 + ep)), {1/2, 7/4}},
  {"scaleless", {1}, CA^2, 0, 0, {0, 0}}};


(* ::Section:: *)
(*the masters and the check of the rows*)


(* colour projection of a class sum *)
colPart[x_, col_] := Which[col === CA^2, Coefficient[x, CA, 2] CA^2 /. {CF -> 0, nf -> 0},
   col === cA, Coefficient[Expand[x], CA TF nf] cA, col === cF, Coefficient[Expand[x], CF TF nf] cF];
(* the masters at mu^2 = -q^2 (= 1) *)
gF[a_, b_] := Gamma[a + b - DD/2] Gamma[DD/2 - a] Gamma[DD/2 - b]/(Gamma[a] Gamma[b] Gamma[DD - a - b]);
jb = E^(2 ep EulerGamma) gF[1, 1]^2 /. DD -> 4 - 2 ep; jsh = -E^(2 ep EulerGamma) gF[1, 1] gF[ep, 1] /. DD -> 4 - 2 ep;
jbS = Normal[Series[jb, {ep, 0, 2}]]; jsS = Normal[Series[jsh, {ep, 0, 3}]];


(* ::Subsubsection:: *)
(*Inspect: the masters J_bub2 and J_sun/(-q^2) at -q^2 = mu^2 = 1*)


If[$Notebooks,
  {jbS, jsS}
]


Print["J_bub2 = ", InputForm[Table[Coefficient[jbS, ep, k], {k, -2, 1}]], ";  J_sun/(-q^2) = ", InputForm[Table[Coefficient[jsS, ep, k], {k, -1, 2}]]];
lau[b_, s_] := Module[{ser = Normal[Series[b jb + s jsh, {ep, 0, 0}]]}, Table[FullSimplify[Coefficient[ser, ep, k]], {k, -3, 0}]];

chk[tab_, vals_, who_] := Module[{ok = True, sumP = 0},
  Do[Module[{x = Total[vals[[r[[2]]]]], bs, bt, st, l},
     bs = bsOf[colPart[x, r[[3]]]]; bt = r[[3]] r[[4]]; st = r[[3]] r[[5]];
     l = lau[bt, st];
     Print[StringPadRight[r[[1]], 40], " b,s exact: ", Simplify[bs - {bt, st}] === {0, 0}, ";  1/eps^3: ", l[[1]],
       ";  {1/eps^2, 1/eps} = ", InputForm[l[[{2, 3}]]], "  table: ", InputForm[r[[3]] r[[6]]], "  ", Simplify[l[[{2, 3}]] - r[[3]] r[[6]]] === {0, 0}];
     If[!(Simplify[bs - {bt, st}] === {0, 0} && Simplify[l[[{2, 3}]] - r[[3]] r[[6]]] === {0, 0} && l[[1]] === 0), ok = False];
     sumP += l], {r, tab}];
  (* every diagram is in exactly one class; colour pieces add up to the diagram *)
  Print[who, ": every diagram used once: ", Sort[Union @@ (#[[2]] & /@ tab)] === Range[Length[vals]] && Total[Length[Union[#[[2]]]] & /@ DeleteDuplicates[tab, #1[[2]] === #2[[2]] &]] === Length[vals]];
  Print[who, ": sum of the class rows minus the sum of all diagrams (b, s): ",
    Simplify[bsOf[Total[vals]] - Total[{#[[3]] #[[4]], #[[3]] #[[5]]} & /@ tab]]];
  Print[who, ": all rows OK: ", ok];
  Expand[sumP]];


(* ::Section:: *)
(*the gluon and ghost tables*)


Print["===== gluon Pi^(2)"];
sG = chk[tabG, vg, "gluon"];
Print["===== ghost Pitilde^(2)"];
sC = chk[tabC, vc, "ghost"];
Print["bare sums {1/eps^3, 1/eps^2, 1/eps, 1}:\n  gluon ", InputForm[sG], "\n  ghost ", InputForm[sC]];


(* ::Subsubsection:: *)
(*Inspect: the bare two-loop sums {1/eps^3, 1/eps^2, 1/eps, 1}: gluon, ghost*)


If[$Notebooks,
  {sG, sC}
]


(* ::Section:: *)
(*counterterm rows: (z1 - beta0)/eps Pi^(1)*)


b0 = 11/3 CA - 4/3 TF nf;
pi1 = ((7 DD^2 - 19 DD + 16)/(8 (DD - 1)) CA - 2 (DD - 2)/(DD - 1) TF nf) E^(ep EulerGamma) gF[1, 1] /. DD -> 4 - 2 ep;  (* eq:V, xi = 0 *)
pt1 = -(DD - 1)/4 CA E^(ep EulerGamma) gF[1, 1] /. DD -> 4 - 2 ep;
Print["(7D^2-19D+16)/(8(D-1)) = 1/2[(3D-2)/(D-1)+(2D-7)-(D-4)/4]: ", Simplify[(7 DD^2 - 19 DD + 16)/(8 (DD - 1)) - 1/2 ((3 DD - 2)/(DD - 1) + (2 DD - 7) - (DD - 4)/4)] === 0];
p1 = Table[Expand[FullSimplify[Coefficient[Normal[Series[pi1, {ep, 0, 1}]], ep, k]]], {k, -1, 1}];
q1 = Table[Expand[FullSimplify[Coefficient[Normal[Series[pt1, {ep, 0, 1}]], ep, k]]], {k, -1, 1}];
Print["Pi^(1) {1/eps, 1, eps} = ", InputForm[p1]];
Print["Pitilde^(1) {1/eps, 1, eps} = ", InputForm[q1]];
z1 = p1[[1]]; zt1 = -q1[[1]];
Print["z1 = ", z1, ", z~1 = ", zt1, ";  z1 - beta0 = ", Expand[z1 - b0], ", z~1 - beta0 = ", Expand[zt1 - b0]];
ctG = Expand[(z1 - b0) {p1[[1]], p1[[2]], p1[[3]]}];   (* {1/eps^2, 1/eps, eps^0} *)
ctC = Expand[(zt1 - b0) {q1[[1]], q1[[2]], q1[[3]]}];
Print["CT row gluon {1/eps^2, 1/eps} = ", InputForm[ctG[[{1, 2}]]], "   (table: -13/4 C_A^2 + 2 C_A T_F n_f, -97/24 C_A^2 + 10/3 C_A T_F n_f)  ",
  Expand[ctG[[{1, 2}]] - {-13/4 CA^2 + 2 CA TF nf, -97/24 CA^2 + 10/3 CA TF nf}] === {0, 0}];
Print["CT row ghost {1/eps^2, 1/eps} = ", InputForm[ctC[[{1, 2}]]], "   (table: 35/16 C_A^2 - C_A T_F n_f, 35/12 C_A^2 - 4/3 C_A T_F n_f)  ",
  Expand[ctC[[{1, 2}]] - {35/16 CA^2 - CA TF nf, 35/12 CA^2 - 4/3 CA TF nf}] === {0, 0}];
Print["p0 (gluon) = ", p1[[2]], "  (text: 97/36 C_A - 20/9 T_F n_f) ", Expand[p1[[2]] - (97/36 CA - 20/9 TF nf)] === 0];


(* ::Section:: *)
(*z22, z21, z~22, z~21, beta1*)


z22 = Expand[ctG[[1]] + sG[[2]]]; z21 = Expand[ctG[[2]] + sG[[3]]];
zt22 = -Expand[ctC[[1]] + sC[[2]]]; zt21 = -Expand[ctC[[2]] + sC[[3]]];
Print["z22 = ", z22, "   note: -13/8 C_A^2 + C_A T_F n_f ", Expand[z22 - (-13/8 CA^2 + CA TF nf)] === 0, ";  = z1(z1-beta0)/2: ", Expand[z22 - z1 (z1 - b0)/2] === 0];
Print["z21 = ", z21, "   note eq:z2: ", Expand[z21 - (59/16 CA^2 - 5/2 CA TF nf - 2 CF TF nf)] === 0];
Print["z~22 = ", zt22, "   note: -35/32 C_A^2 + 1/2 C_A T_F n_f ", Expand[zt22 - (-35/32 CA^2 + 1/2 CA TF nf)] === 0, ";  = z~1(z~1-beta0)/2: ", Expand[zt22 - zt1 (zt1 - b0)/2] === 0];
Print["z~21 = ", zt21, "   note eq:z2: ", Expand[zt21 - (95/96 CA^2 - 5/12 CA TF nf)] === 0];
b1 = Expand[4 zt21 + 2 z21];
Print["beta1 = 4 z~21 + 2 z21 = ", b1, "   note: ", Expand[b1 - (34/3 CA^2 - 4 CF TF nf - 20/3 CA TF nf)] === 0];
Print["beta1 pieces: 4 z~21 = ", Expand[4 zt21], ", 2 z21 = ", Expand[2 z21]];


(* ::Subsubsection:: *)
(*Inspect: z_21, z~_21 and beta_1*)


If[$Notebooks,
  {z21, zt21, b1}
]


Print["double poles: bare two-loop / counterterm insertions = -1/2:  gluon ", Expand[sG[[2]] + ctG[[1]]/2] === 0, ", ghost ", Expand[sC[[2]] + ctC[[1]]/2] === 0];
Print["CT double pole = z1 (z1 - beta0) (gluon): ", Expand[ctG[[1]] - z1 (z1 - b0)] === 0, ";  ghost CT double pole = -z~1 (z~1 - beta0): ", Expand[ctC[[1]] + zt1 (zt1 - b0)] === 0];
Print["CT single pole = (z1 - beta0) p0 : ", Expand[ctG[[2]] - (z1 - b0) p1[[2]]] === 0];


(* ::Section:: *)
(*finite parts (Z3): unchanged numbers of app:details*)


Print["J_bub2 eps^1 = ", InputForm[Coefficient[jbS, ep, 1]], ";  J_sun/(-q^2) eps^2 = ", InputForm[Coefficient[jsS, ep, 2]]];
Print["[Pi^(1)]_eps^1 = ", InputForm[p1[[3]]], ";  [Pitilde^(1)]_eps^1 = ", InputForm[q1[[3]]]];
Print["bare [Pi^(2)]_eps^0 = ", InputForm[Collect[sG[[4]], {CA, CF}, Simplify]]];
Print["bare [Pitilde^(2)]_eps^0 = ", InputForm[Collect[sC[[4]], {CA, CF}, Simplify]]];
Print["CT eps^0: gluon ", InputForm[Collect[ctG[[3]], {CA}, Simplify]], ";  ghost ", InputForm[Collect[ctC[[3]], {CA}, Simplify]]];
piR = Expand[sG[[4]] + ctG[[3]]]; ptR = Expand[sC[[4]] + ctC[[3]]];
Print["Pi^R(2) finite = ", InputForm[Collect[piR, {CA, CF}, Simplify]]];
Print["   app:details: ", Expand[piR - ((2381/96 - 3 Zeta[3]) CA^2 - (59/4 + 8 Zeta[3]) CA TF nf - (55/3 - 16 Zeta[3]) CF TF nf)] === 0,
  ";  SU(3), n_f = 6: ", N[piR /. {CA -> 3, CF -> 4/3, TF -> 1/2, nf -> 6}, 6]];
Print["Pitilde^R(2) finite = ", InputForm[Collect[ptR, {CA, CF}, Simplify]]];
Print["   app:details: ", Expand[ptR - ((-1751/192 + 15/16 Zeta[3]) CA^2 + 95/24 CA TF nf)] === 0,
  ";  SU(3), n_f = 6: ", N[ptR /. {CA -> 3, CF -> 4/3, TF -> 1/2, nf -> 6}, 6]];
csv = Import[FileNameJoin[{srcDirZ1$, "results", "twoloop_z.csv"}], "CSV"];
Print["Src/results/twoloop_z.csv rows z3_single, zt3_single: ", csv[[3]], " ", csv[[5]]];


(* ::Section:: *)
(*extra numbers quoted in the text of Z1/Z3a*)


Print["---- extra checks"];
Print["J_bub2 eps^1 = 32 - 2pi^2/3 - 14 zeta3/3: ", FullSimplify[FunctionExpand[Coefficient[jbS, ep, 1]] - (32 - 2 Pi^2/3 - 14/3 Zeta[3])] === 0];
Print["J_sun/(-q^2) eps^2 = 865/32 - 13pi^2/48 - 8 zeta3/3: ", FullSimplify[FunctionExpand[Coefficient[jsS, ep, 2]] - (865/32 - 13 Pi^2/48 - 8/3 Zeta[3])] === 0];
Print["e^(eps gE) G(1,1) = 1/eps + 2 + (4 - pi^2/12) eps: ", FullSimplify[Normal[Series[E^(ep EulerGamma) gF[1, 1] /. DD -> 4 - 2 ep, {ep, 0, 1}]] - (1/ep + 2 + (4 - Pi^2/12) ep)] === 0];
Print["-(1/2 + (D-3)/4) = -(D-1)/4: ", Simplify[-(1/2 + (DD - 3)/4) + (DD - 1)/4] === 0];
Print["[Pi^(1)]_eps^1 text: ", Expand[p1[[3]] - ((295/54 - 13 Pi^2/72) CA - (112/27 - Pi^2/9) TF nf)] === 0, ";  [Pitilde^(1)]_eps^1 text: ", Expand[q1[[3]] + (2 - Pi^2/16) CA] === 0];
Print["bare eps^0 text (gluon): ", Expand[sG[[4]] - ((9503/288 - 13 Pi^2/48 - 3 Zeta[3]) CA^2 - (755/36 - Pi^2/6 + 8 Zeta[3]) CA TF nf - (55/3 - 16 Zeta[3]) CF TF nf)] === 0];
Print["bare eps^0 text (ghost): ", Expand[sC[[4]] - (-(2871/192 - 35 Pi^2/192 - 15/16 Zeta[3]) CA^2 + (53/8 - Pi^2/12) CA TF nf)] === 0];
cAe = (26 - 37 ep + 14 ep^2)/(4 (3 - 2 ep)); cQe = -4 (1 - ep)/(3 - 2 ep);
Print["c_A(eps) = (7D^2-19D+16)/(8(D-1)): ", Simplify[cAe - ((7 DD^2 - 19 DD + 16)/(8 (DD - 1)) /. DD -> 4 - 2 ep)] === 0, ";  c_q = -2(D-2)/(D-1): ", Simplify[cQe - (-2 (DD - 2)/(DD - 1) /. DD -> 4 - 2 ep)] === 0];
oG = (8 - 17 ep - 4 ep^2 + 8 ep^3)/(ep (1 + ep)); oC = -(1 - ep) (3 - 2 ep)/(2 ep (1 + ep));
Print["insertion rows = (inserted coefficient) x (outer factor): (a) g,c ", Simplify[tabG[[1, 5]] - cAe oG] === 0, ", (a) q ", Simplify[tabG[[6, 5]] - cQe oG] === 0,
  ", (g) g,c ", Simplify[tabC[[1, 5]] - cAe oC] === 0, ", (g) q ", Simplify[tabC[[5, 5]] - cQe oC] === 0];
Print["b_{-1} = -s_{-2}/4 in every row: ", And @@ (Simplify[Limit[ep #[[4]], ep -> 0] + Limit[ep^2 #[[5]], ep -> 0]/4] === 0 & /@ Join[tabG, tabC])];