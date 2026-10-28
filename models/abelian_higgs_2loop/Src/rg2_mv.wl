(* ::Package:: *)

(* ::Title:: *)
(*Step (2): two-loop renormalization group and the Landau-gauge effective potential (abelian Higgs model)*)


(* ::Text:: *)
(*Research note models/abelian_higgs_2loop, step (2).  V = V0 + V1/K + V2/K^2 (K = 16 pi^2, Landau gauge, MS-bar),*)
(*V0 = Lam - m2 phi^2/2 + lam phi^4/4 (Lam: the field-independent vacuum energy), and the RG equation*)
(*    [Q d/dQ + beta_lam d/dlam + beta_e d/de + beta_m2 d/dm2 + beta_Lam d/dLam - gamma phi d/dphi] V = 0.*)
(*  (a) The general two-loop formulas of Machacek-Vaughn with the corrections of Luo, Wang, Xiao (hep-ph/0211440,*)
(*      Eqs. (22), (23), (30), (38), (44); real scalars, -L = lam_abcd phi^4/4!, D phi = (d - i g theta A) phi),*)
(*      implemented with explicit tensors; m2 and Lam through a non-propagating dummy scalar (their Eq. (21)):*)
(*      lam_{ab dd} = 2 m2_ab (V = m2_ab phi_a phi_b/2), lam_{dddd} = 24 Lam.  Abelian group, no Yukawa couplings,*)
(*      fermions only through kappa S2(F), xi = 0.*)
(*  (b) Check of the implementation: the Standard Model Higgs doublet with U(1)_Y only (g = 0, Yukawa = 0, n_g = 3,*)
(*      kappa S2(F) = 5) against Luo-Xiao (hep-ph/0207271, Eqs. (9)-(12); lam_LX = 2 lam, g1^2 = 5/3 g'^2).*)
(*  (c) The model: one complex scalar of charge 1 (two real scalars), beta functions and the Landau-gauge gamma.*)
(*  (d) Pole consistency: the MS-bar counterterms of V0 at order 1/K^2 built from the RG functions must cancel the*)
(*      1/eps^2 and 1/eps poles of the two-loop diagrams plus the one-loop counterterm insertions (step (1),*)
(*      "poles" in results/v2_landau.m).*)
(*  (e) RG invariance: Q dV/dQ = O(1/K^3) with V2 of results/v2_landau.m, Q^2 dA(x)/dQ^2 = -x,*)
(*      Q^2 dI(x,y,z)/dQ^2 = A(x) + A(y) + A(z) - x - y - z.*)
(*  (f) results/rg2.m (the RG functions) and results/rg2_beta.csv (their coefficients, for rg2_numeric.py).*)
(*Batch: wolframscript -file rg2_mv.wl*)


(* ::Section:: *)
(*Setup*)


srcDirRG$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirRG$ = FileNameJoin[{srcDirRG$, "results"}];


(* ::Section:: *)
(*(a) The general two-loop formulas*)


(* lamT: quartic tensor on the indices 1..n (physical) and n+1 (dummy); th: list of generators (zero on the dummy);
   internal sums run over the physical scalars only.  Returns the tensors beta^I, beta^II as functions of four external
   indices, the matrices gamma^I, gamma^II (xi = 0), and the gauge-coupling coefficients. *)
perms4RG$ = Permutations[Range[4]];
rgGeneral[lamT_, th_List, g_, kS2F_] := Module[
  {nAll, ph, lm, c2, s2s, ac, nA, lam2S, sym, legs, L2, LS, A4, L3, L2S, L2g, LSS, Al, Abl, AS, b1, b2, g1, g2},
  nAll = Range[Length[lamT]];
  ph = Most[nAll];
  nA = Length[th];
  lm[a_, b_, c_, d_] := lamT[[a, b, c, d]];
  c2 = Total[#.# & /@ th];                                          (* C2(S)_ab *)
  s2s = Tr[th[[1]].th[[1]]];                                        (* S2(S), one abelian generator *)
  ac[aa_, bb_] := th[[aa]].th[[bb]] + th[[bb]].th[[aa]];             (* {theta^A, theta^B} *)
  lam2S = Table[1/6 Sum[lm[a, c, d, e] lm[b, c, d, e], {c, ph}, {d, ph}, {e, ph}], {a, nAll}, {b, nAll}];
  sym[f_, ext_] := Sum[f @@ ext[[p]], {p, perms4RG$}];               (* sum over the 24 permutations *)
  legs[mat_, t_, {a_, b_, c_, d_}] := Sum[mat[[a, e]] t[e, b, c, d] + mat[[b, e]] t[a, e, c, d] +
      mat[[c, e]] t[a, b, e, d] + mat[[d, e]] t[a, b, c, e], {e, nAll}];
  (* the invariants of Eqs. (39)-(61) *)
  L2[x__] := 1/8 sym[Sum[lm[#1, #2, e, f] lm[e, f, #3, #4], {e, ph}, {f, ph}] &, {x}];
  A4[x__] := 1/8 sym[Sum[ac[aa, bb][[#1, #2]] ac[aa, bb][[#3, #4]], {aa, nA}, {bb, nA}] &, {x}];
  L3[x__] := 1/4 sym[Sum[lm[#1, #2, e, f] lm[#3, e, gg, h] lm[#4, f, gg, h], {e, ph}, {f, ph}, {gg, ph}, {h, ph}] &, {x}];
  L2S[x__] := 1/8 sym[Sum[c2[[f, gg]] lm[#1, #2, e, f] lm[#3, #4, e, gg], {e, ph}, {f, ph}, {gg, ph}] &, {x}];
  L2g[x__] := 1/8 sym[Sum[lm[#1, #2, e, f] lm[#3, #4, gg, h] th[[aa, e, gg]] th[[aa, f, h]],
       {aa, nA}, {e, ph}, {f, ph}, {gg, ph}, {h, ph}] &, {x}];
  Al[x__] := 1/4 sym[Sum[lm[#1, #2, e, f] ac[aa, bb][[e, f]] ac[aa, bb][[#3, #4]], {aa, nA}, {bb, nA}, {e, ph}, {f, ph}] &, {x}];
  Abl[x__] := 1/4 sym[Sum[lm[#1, #2, e, f] ac[aa, bb][[#3, e]] ac[aa, bb][[#4, f]], {aa, nA}, {bb, nA}, {e, ph}, {f, ph}] &, {x}];
  LS[x__] := legs[c2, lm, {x}];                                     (* sum_i C2(i) lam_abcd *)
  LSS[x__] := legs[c2.c2, lm, {x}];
  AS[x__] := legs[c2, A4, {x}];
  (* Eq. (38) and Eq. (44) with C2(G) = 0, no Yukawa couplings *)
  b1[x__] := L2[x] - 3 g^2 LS[x] + 3 g^4 A4[x];
  b2[x__] := 1/2 legs[lam2S, lm, {x}] - L3[x] + g^2 (2 L2S[x] - 6 L2g[x]) -
    g^4 ((-10/3 kS2F - 11/12 s2s) LS[x] - 3/2 LSS[x] - 5/2 Al[x] - 1/2 Abl[x]) +
    g^6 ((-32/3 kS2F - 7/3 s2s) A4[x] - 15/2 AS[x]);
  (* Eqs. (22), (23) at xi = 0 *)
  g1 = -3 g^2 c2;
  g2 = -g^4 (-10/3 kS2F - 11/12 s2s) c2 + 1/2 lam2S + 3/2 g^4 c2.c2;
  <|"b1" -> b1, "b2" -> b2, "gamma1" -> g1, "gamma2" -> g2, "C2S" -> c2, "S2S" -> s2s|>];


(* the O(N)-symmetric quartic V = lam/4 (phi.phi)^2 - m2/2 phi.phi + Lam on n real scalars plus the dummy *)
quarticRG$[n_, lam_, m2_, lamV_] := Module[{t, d = n + 1, dl},
   dl[i_, j_] := If[i <= n && j <= n && i == j, 1, 0];
   t = Table[2 lam (dl[a, b] dl[c, d2] + dl[a, c] dl[b, d2] + dl[a, d2] dl[b, c]), {a, d}, {b, d}, {c, d}, {d2, d}];
   (* lam_{ab dd} = 2 m2_ab with m2_ab = -m2 delta_ab, in all index positions *)
   Do[If[Count[{a, b, c, d2}, d] == 2,
     Module[{ph = Select[{a, b, c, d2}, # <= n &]}, t[[a, b, c, d2]] = 2 (-m2) dl @@ ph]],
    {a, d}, {b, d}, {c, d}, {d2, d}];
   t[[d, d, d, d]] = 24 lamV;
   t];
(* generator of a complex scalar of charge q on (Re, Im), embedded with zeros *)
blockRG$ = {{0, -I}, {I, 0}};


(* ::Section:: *)
(*(b) Check of the implementation: the Standard Model with U(1)_Y only*)


Module[{n = 4, d = 5, lamT, th, rg, bl1, bl2, bm1, bm2, exp},
  lamT = quarticRG$[n, lam, m2, Lam];
  th = {1/2 ArrayFlatten[{{blockRG$, 0, 0}, {0, blockRG$, 0}, {0, 0, {{0}}}}]};
  rg = rgGeneral[lamT, th, gp, 5];                     (* kappa S2(F) = 1/2 * 10 (three generations) *)
  bl1 = Expand[rg["b1"][1, 1, 1, 1]/6]; bl2 = Expand[rg["b2"][1, 1, 1, 1]/6];
  bm1 = Expand[-rg["b1"][1, 1, d, d]/2]; bm2 = Expand[-rg["b2"][1, 1, d, d]/2];
  (* Luo-Xiao, U(1)_Y part, converted to V = lam (H^+H)^2 - m2 H^+H and g' *)
  exp = {24 lam^2 - 3 gp^2 lam + 3/8 gp^4,
     -312 lam^3 + 36 gp^2 lam^2 + 629/24 gp^4 lam - 379/48 gp^6,
     m2 (12 lam - 3/2 gp^2),
     m2 (-60 lam^2 + 24 gp^2 lam + 557/48 gp^4)};
  Print["(b) SM, U(1)_Y only: beta_lam^(1), beta_lam^(2), beta_m2^(1), beta_m2^(2) = ", {bl1, bl2, bm1, bm2}];
  Print["(b) minus Luo-Xiao (expect {0, 0, 0, 0}): ", Expand[{bl1, bl2, bm1, bm2} - exp]]];


(* ::Section:: *)
(*(c) The abelian Higgs model*)


rgAH$ = Module[{n = 2, d = 3, lamT, th, rg, b1, b2, sym},
   lamT = quarticRG$[n, lam, m2, Lam];
   th = {ArrayFlatten[{{blockRG$, 0}, {0, {{0}}}}]};
   rg = rgGeneral[lamT, th, el, 0];
   b1 = rg["b1"]; b2 = rg["b2"];
   (* the beta tensors keep the O(2)-symmetric form *)
   sym = Expand[{b1[1, 1, 2, 2] - b1[1, 1, 1, 1]/3, b2[1, 1, 2, 2] - b2[1, 1, 1, 1]/3, b1[1, 2, 2, 2], b2[1, 2, 2, 2],
      b1[1, 1, d, d] - b1[2, 2, d, d], b2[1, 1, d, d] - b2[2, 2, d, d], b1[1, 2, d, d], b2[1, 2, d, d]}];
   Print["(c) O(2) structure of the beta tensors (expect zeros): ", sym];
   Print["(c) C2(S), S2(S) = ", {rg["C2S"][[1, 1]], rg["S2S"]}];
   <|"lam" -> {b1[1, 1, 1, 1]/6, b2[1, 1, 1, 1]/6},
     "m2" -> {-b1[1, 1, d, d]/2, -b2[1, 1, d, d]/2},
     "Lam" -> {b1[d, d, d, d]/24, b2[d, d, d, d]/24},
     (* Eq. (30): C2(G) = S2(F) = 0, C2(S) = 1, S2(S) = 2 *)
     "el" -> {el^3/6 rg["S2S"], el^5 2 rg["C2S"][[1, 1]] rg["S2S"]},
     "gamma" -> {rg["gamma1"][[1, 1]], rg["gamma2"][[1, 1]]}|>];
rgAH$ = Map[Factor@*Expand, rgAH$, {2}];
Do[Print["(c) beta_", k, " (one loop, two loops) = ", InputForm[rgAH$[k]]], {k, {"lam", "m2", "el", "Lam"}}];
Print["(c) gamma (Landau gauge; one loop, two loops) = ", InputForm[rgAH$["gamma"]]];


(* ::Section:: *)
(*(d) Pole consistency*)


(* The bare V0 = mu^(-2 eps) [R - M phi^2/2 + L phi^4/4], with R = mu^(2 eps) Lam0, M = m0^2 Z, L = mu^(-2 eps) lam0 Z^2.
   Writing ln L = ln lam + l1/eps + l2/eps^2, ln M = ln m2 + n1/eps + n2/eps^2, R = Lam + c1/eps + c2/eps^2 and using
   d phi/d ln mu = -gamma phi, rho = 2 (lam), 1 (e), 0 (m2), the mu-independence gives at L loops
     (2 L) l1 = beta_lam/lam - 4 gamma,  (2 L) n1 = beta_m2/m2 - 2 gamma,  (2 L) c1 = beta_Lam,
   and at two loops  4 l2 = beta^(1).d l1^(1),  4 n2 = beta^(1).d n1^(1),  4 c2 = beta^(1).d c1^(1). *)
Module[{bLam, bEl, bM, bL, gm, l1, n1, c1, d1, l2, n2, c2, ct2, pred, poles},
  {bL, bM, bEl, bLam, gm} = rgAH$ /@ {"lam", "m2", "el", "Lam", "gamma"};
  l1 = Table[(bL[[k]]/lam - 4 gm[[k]])/(2 k), {k, 2}];
  n1 = Table[(bM[[k]]/m2 - 2 gm[[k]])/(2 k), {k, 2}];
  c1 = Table[bLam[[k]]/(2 k), {k, 2}];
  d1[f_] := bL[[1]] D[f, lam] + bEl[[1]] D[f, el] + bM[[1]] D[f, m2];
  {l2, n2, c2} = d1 /@ {l1[[1]], n1[[1]], c1[[1]]}/4;
  (* the order-1/K^2 counterterms of V0; the loops must give minus these *)
  ct2 = (c1[[2]]/eps + c2/eps^2) - phi^2/2 m2 (n1[[2]]/eps + (n2 + n1[[1]]^2/2)/eps^2) +
    phi^4/4 lam (l1[[2]]/eps + (l2 + l1[[1]]^2/2)/eps^2);
  pred = Expand[{Coefficient[-ct2, eps, -2], Coefficient[-ct2, eps, -1]}];
  poles = "poles" /. Get[FileNameJoin[{resDirRG$, "v2_landau.m"}]];
  Print["(d) predicted poles 1/eps^2, 1/eps: ", InputForm[Collect[pred, phi, Factor]]];
  Print["(d) predicted - diagrams (step (1)) (expect {0, 0}): ", Expand[pred - poles]];
  (* the reverse: two-loop RG functions read off from the 1/eps poles of the diagrams *)
  Print["(d) from the 1/eps poles: beta_lam^(2) - 4 lam gamma^(2) = ",
   InputForm[Factor[-4 4 Coefficient[poles[[2]], phi, 4]]], ",  beta_m2^(2) - 2 m2 gamma^(2) = ",
   InputForm[Factor[4 2 Coefficient[poles[[2]], phi, 2]]], ",  beta_Lam^(2) = ",
   InputForm[Factor[-4 Coefficient[poles[[2]], phi, 0]]]]];


(* ::Section:: *)
(*(e) RG invariance of V0 + V1/K + V2/K^2*)


Module[{v2f, masses, v0, v1, pars, b, gm, dOp, qD, ord1, ord2, toSym},
  {v2f, masses} = {"V2", "masses"} /. Get[FileNameJoin[{resDirRG$, "v2_landau.m"}]];
  v0 = Lam - m2 phi^2/2 + lam phi^4/4;
  (* V1 = (1/4) sum n x^2 (ln x - c) = (1/4)[xh A(xh) - xh^2/2 + xg A(xg) - xg^2/2 + 3 xa A(xa) + xa^2/2] *)
  v1 = 1/4 (xh A[xh] - xh^2/2 + xg A[xg] - xg^2/2 + 3 xa A[xa] + xa^2/2) /. masses;
  pars = {lam, el, m2, Lam};
  b = Transpose[rgAH$ /@ {"lam", "el", "m2", "Lam"}];               (* b[[k]]: k-loop betas *)
  gm = rgAH$["gamma"];
  Derivative[1][A] = (A[#]/# + 1) &;                                (* dA/dx = ln x *)
  dOp[k_, f_] := b[[k]].(D[f, #] & /@ pars) - gm[[k]] phi D[f, phi];
  (* Q d/dQ = 2 Q^2 d/dQ^2 on the explicit Q dependence *)
  qD[f_] := 2 D[f /. {A[x_] :> A[x] - t x, II[x_, y_, z_] :> II[x, y, z] + t (A[x] + A[y] + A[z] - x - y - z)} /.
        A[0] -> 0, t] /. t -> 0;
  toSym[e_] := Together[e /. masses /. {A[-m2 + 3 lam phi^2] -> ah, A[-m2 + lam phi^2] -> ag, A[el^2 phi^2] -> aa}];
  ord1 = toSym[qD[v1] + dOp[1, v0]];
  ord2 = toSym[qD[v2f] + dOp[1, v1] + dOp[2, v0]];
  Print["(e) Q dV/dQ at order 1/K (expect 0): ", ord1];
  Print["(e) Q dV/dQ at order 1/K^2 (expect 0): ", ord2];
  Print["(e) the same with gamma^(2) left out (expect nonzero): ",
   Factor[toSym[qD[v2f] + dOp[1, v1] + b[[2]].(D[v0, #] & /@ pars)]]]];


(* ::Section:: *)
(*(f) Output*)


Put[rgAH$, FileNameJoin[{resDirRG$, "rg2.m"}]];
Export[FileNameJoin[{resDirRG$, "rg2_beta.csv"}],
  Prepend[Flatten[Table[
     {k, l, Sequence @@ #1, ToString[InputForm[#2]]} & @@@
      CoefficientRules[rgAH$[k][[l]], {lam, el, m2}], {k, {"lam", "el", "m2", "Lam", "gamma"}}, {l, 2}], 2],
   {"function", "loops", "power_lam", "power_e", "power_m2", "coefficient"}], "CSV"];
Print["(f) written results/rg2.m and results/rg2_beta.csv"];
