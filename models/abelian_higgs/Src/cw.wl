(* ::Package:: *)

(* ::Title:: *)
(*Step (8): the Coleman-Weinberg mechanism in the abelian Higgs model with m^2 = 0*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (8); no FeynCalc.  m^2 = 0, V0 = lam phi^4/4, field-dependent masses*)
(*mh2 = 3 lam phi^2, mG2 = lam phi^2, mA2 = e^2 phi^2; V1 of Eq. (V1) (step (7)) in Landau, background R_xi and Fermi*)
(*gauges.  Counting lam ~ e^4/K.*)
(*  (a) leading order V_LO = (phi^4/4)[lam + (3 e^4/K)(ln(e^2 phi^2/mu^2) - 5/6)]: the minimum ln(e^2 v^2/mu^2) =*)
(*      1/3 - K lam/(3 e^4), MH^2 = V''(v) = 6 e^4 v^2/K, MH^2/MA^2 = 3 e^2/(8 pi^2), V(v) = -MH^2 v^2/16; v is*)
(*      mu-independent with beta_lam = 6 e^4/K; V1 - (gauge part) = O(lam^2) in Landau gauge;*)
(*  (b) the scheme of Coleman and Weinberg (lam_CW = d^4V/dphi^4 at phi = M): the constant -25/6, lam_CW = 6 lam +*)
(*      (18 e^4/K)(ln(e^2 M^2/mu^2) + 10/3), and lam_CW = (33/(8 pi^2)) e^4 at M = <phi>;*)
(*  (c) every mass is k_i phi^2, so the one-loop V is exactly (phi^4/4)[Lambda + beta ln phi^2] with beta = sum n_i k_i^2/K*)
(*      and MH^2/MA^2 = 2 beta/e^2 = (6 e^2/K)[1 + (10 lam^2 + 2 s xi e^2 lam)/(3 e^4)], s = 0 (Landau), +1 (background*)
(*      R_xi), -1 (Fermi); checked against the full one-loop potential minimized numerically for e = 1/2 ... 1/32 with*)
(*      lam = e^4/K, mu = 1 (leading-order minimum at e v = 1): the gauge dependence +-(2/3) xi e^2/K is NLO;*)
(*  (d) the mu dependence: (e, lam, phi) of (c) at e = 1/2 run with the one-loop RGEs (Landau gamma) from mu0 = 1 to*)
(*      mu = 2^k; the minimum and the curvature in the mu0 normalization are mu-independent up to two-loop terms, and*)
(*      without running v grows like mu;*)
(*  results/cw_ratio.csv, results/cw_mu.csv, results/cw_points.csv (V at sample points for cw_tools.py).*)
(*Batch: wolframscript -file cw.wl*)


srcDirCW$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirCW$ = FileNameJoin[{srcDirCW$, "results"}];
$NumberMarks = False;
KK = 16 Pi^2;
cell$[y_] := If[StringQ[y], y, ToString[CForm[Chop[N[y, 16], 10^-30]]]];
pos$ = lam > 0 && e > 0 && mu > 0 && phi > 0 && xi > 0;
mh2 = 3 lam phi^2; mG2 = lam phi^2; mA2 = e^2 phi^2;
V0 = lam phi^4/4;
f$[y_] := y^2 (Log[y/mu^2] - 3/2)/(4 KK);
fV$[y_] := 3 y^2 (Log[y/mu^2] - 5/6)/(4 KK);
mp$ = (mG2 + Sqrt[mG2^2 - 4 xi mA2 mG2])/2; mm$ = (mG2 - Sqrt[mG2^2 - 4 xi mA2 mG2])/2;
V1L = f$[mh2] + fV$[mA2] + f$[mG2];
V1B = f$[mh2] + fV$[mA2] + f$[mG2 + xi mA2] - f$[xi mA2];
V1F = f$[mh2] + fV$[mA2] + f$[mp$] + f$[mm$];


(* ::Section:: *)
(*(a) leading order*)


vLO = phi^4/4 (lam + 3 e^4/KK (Log[e^2 phi^2/mu^2] - 5/6));
lamStar$ = lam /. First[Solve[D[vLO, phi] == 0, lam]] /. phi -> v;
Print["(a) minimum: lam = ", InputForm[Simplify[lamStar$]], ",  i.e. ln(e^2 v^2/mu^2) = 1/3 - K lam/(3 e^4): ",
  Simplify[lamStar$ - (-3 e^4/KK (Log[e^2 v^2/mu^2] - 1/3))] == 0];
mh2LO$ = Simplify[D[vLO, {phi, 2}] /. phi -> v /. lam -> lamStar$, v > 0 && e > 0 && mu > 0];
Print["(a) MH^2 = V''(v) = ", mh2LO$, ";  MH^2/MA^2 - 3 e^2/(8 pi^2) = ", Simplify[mh2LO$/(e^2 v^2) - 3 e^2/(8 Pi^2)]];
Print["(a) V(v) + MH^2 v^2/16 = ", Simplify[(vLO /. phi -> v /. lam -> lamStar$) + mh2LO$ v^2/16, v > 0 && e > 0 && mu > 0]];
Print["(a) d/d ln mu [ln(e^2 v^2/mu^2) + K lam/(3 e^4)] with d lam/d ln mu = 6 e^4/K (e fixed): ",
  Simplify[mu D[Log[e^2 v^2/mu^2], mu] + KK/(3 e^4) 6 e^4/KK]];
Print["(a) Landau V1 minus the gauge-field part: ", InputForm[Simplify[V1L - fV$[mA2]]], "  (order lam^2)"];
Print["(a) background R_xi and Fermi minus Landau, xi part of sum n m^4: ",
  Factor[Expand[(mG2 + xi mA2)^2 - (xi mA2)^2 - mG2^2]], ", ", Factor[Expand[mp$^2 + mm$^2 - mG2^2]], "  (order xi e^2 lam)"];


(* ::Section:: *)
(*(b) the Coleman-Weinberg scheme*)


vCW = lc phi^4/24 + 3 e^4/(64 Pi^2) phi^4 (Log[phi^2/M^2] - 25/6);
Print["(b) d^4 V_CW/dphi^4 at phi = M: ", Simplify[D[vCW, {phi, 4}] /. phi -> M, M > 0], "  (= lam_CW: the loop part vanishes)"];
lcSol$ = lc /. First[Solve[Simplify[PowerExpand[vCW - vLO]] == 0, lc]];
Print["(b) lam_CW = ", InputForm[Simplify[PowerExpand[lcSol$]]], ";  minus 6 lam + (18 e^4/K)(ln(e^2 M^2/mu^2) + 10/3): ",
  Simplify[PowerExpand[lcSol$ - (6 lam + 18 e^4/KK (Log[e^2 M^2/mu^2] + 10/3))]]];
lcAtMin$ = lc /. First[Solve[(D[vCW, phi] /. phi -> M) == 0, lc]];
Print["(b) minimum at phi = M: lam_CW = ", lcAtMin$, " = (33/(8 pi^2)) e^4: ", Simplify[lcAtMin$ - 33 e^4/(8 Pi^2)] == 0,
  ";  MH^2/MA^2 = ", Simplify[(D[vCW, {phi, 2}] /. phi -> M /. lc -> lcAtMin$)/(e^2 M^2), M > 0]];


(* ::Section:: *)
(*(c) the full one-loop minimum for small e*)


bench$[ev_] := {e -> ev, lam -> ev^4/KK, mu -> 1};
minCW[v1_, ev_, xv_] := Module[{dv, p0, vals = bench$[ev]},
   dv = (D[V0 + v1, phi] /. vals /. xi -> xv);
   p0 = p /. FindRoot[Re[N[dv /. phi -> SetPrecision[p, 60], 60]], {p, 1/(2 ev), 2/ev}, Method -> "Brent",
       WorkingPrecision -> 40, AccuracyGoal -> 30, PrecisionGoal -> 30];
   {p0, Re[N[(D[V0 + v1, {phi, 2}] /. vals /. xi -> xv) /. phi -> SetPrecision[p0, 60], 40]]}];
gaugesCW$ = {{"Landau", V1L, 0}, {"background R_xi", V1B, 1}, {"background R_xi", V1B, 3}, {"Fermi", V1F, 1}, {"Fermi", V1F, 3}};
es$ = 2^-Range[1, 5];
(* exact one-loop ratio: V = (phi^4/4)[Lambda + beta ln phi^2], beta = (1/2) phi d(4 V/phi^4)/dphi is phi-independent,
   the minimum has V'' = 2 beta v^2 *)
betaOf$[v1_] := Simplify[PowerExpand[phi D[4 (V0 + v1)/phi^4, phi]/2], pos$];
Print["(c) beta (Landau) = ", InputForm[betaOf$[V1L]], ";  beta (background R_xi) - beta (Landau) = ",
  InputForm[Simplify[betaOf$[V1B] - betaOf$[V1L]]], ";  Fermi (numerically, xi = 1, 3; phi = 1, 3): ",
  Table[N[Re[N[(phi D[4 (V0 + V1F)/phi^4, phi]/2 - betaOf$[V1L]) /. bench$[1/2] /. {xi -> xv, phi -> SetPrecision[pv, 40]}, 40]]/
     (-2 xv (1/2)^2 (1/2)^4/KK/KK), 12], {xv, {1, 3}}, {pv, {1, 3}}], "  (in units of -2 xi e^2 lam/K)"];
Print["(c) (phi^4/4)[Lambda + beta ln phi^2]: V'(v) and V''(v)/(2 beta v^2) - 1 at v = exp(-Lambda/(2 beta) - 1/4): ",
  Module[{vv = (ph^4/4) (la + be Log[ph^2]), vm = Exp[-la/(2 be) - 1/4]},
   Simplify[PowerExpand[{D[vv, ph], D[vv, {ph, 2}]/(2 be ph^2) - 1} /. ph -> vm], be > 0]]];
sgn$ = <|"Landau" -> 0, "background R_xi" -> 1, "Fermi" -> -1|>;
exactRatio$[g_, xv_, ev_] := 6 ev^2/KK (1 + (10 (ev^4/KK)^2 + 2 sgn$[g] xv ev^2 ev^4/KK)/(3 ev^4));
ratioRows$ = Flatten[Table[Module[{m = minCW[g[[2]], ev, g[[3]]], r},
     r = m[[2]]/(ev^2 m[[1]]^2)/(6 ev^2/KK);
     {g[[1]], g[[3]], ev, ev m[[1]], m[[2]]/(ev^2 m[[1]]^2), r - 1, (r - 1) KK/ev^2, m[[2]]/(ev^2 m[[1]]^2)/exactRatio$[g[[1]], g[[3]], ev] - 1}],
    {g, gaugesCW$}, {ev, es$}], 1];
Do[Print["(c) ", r[[1]], " xi = ", r[[2]], ", e = ", r[[3]], ": e v = ", N[r[[4]], 12], ", MH^2/MA^2 = ", N[r[[5]], 10],
   ", ratio/(3 e^2/(8 pi^2)) - 1 = ", N[r[[6]], 6], "  (x K/e^2: ", N[r[[7]], 6], ");  against the exact one-loop formula: ",
   If[Abs[r[[8]]] < 10^-25, "< 10^-25", N[r[[8]], 3]]], {r, ratioRows$}];
Export[FileNameJoin[{resDirCW$, "cw_ratio.csv"}],
  Map[cell$, Prepend[ratioRows$, {"gauge", "xi", "e", "e_v", "MH2_over_MA2", "dev", "dev_K_over_e2", "minus_exact_formula"}], {2}], "CSV"];

(* sample values of V0 + V1 for the CosmoTransitions check (Landau and background R_xi, e = 1/2) *)
pts$ = Flatten[Table[{g[[1]], g[[3]], pv, N[(V0 + g[[2]]) /. bench$[1/2] /. xi -> g[[3]] /. phi -> pv, 20]},
    {g, gaugesCW$[[1 ;; 3]]}, {pv, {1/2, 1, 3/2, 2, 5/2, 3, 4}}], 1];
Export[FileNameJoin[{resDirCW$, "cw_points.csv"}],
  Map[cell$, Join[{{"gauge", "xi", "phi", "V"}}, pts$, {{"min", "Landau", minCW[V1L, 1/2, 0][[1]], minCW[V1L, 1/2, 0][[2]]}}], {2}], "CSV"];


(* ::Section:: *)
(*(d) mu dependence with running couplings*)


(* one-loop RGEs, t = ln(mu/mu0): de^2/dt = 2 e^4/(3K), dlam/dt = (20 lam^2 - 12 e^2 lam + 6 e^4)/K,
   d ln phi/dt = -gamma = 3 e^2/K (Landau) *)
e0$ = 1/2; lam0$ = e0$^4/KK;
rge$ = NDSolve[{e2'[t] == 2 e2[t]^2/(3 KK), la'[t] == (20 la[t]^2 - 12 e2[t] la[t] + 6 e2[t]^2)/KK,
    lz'[t] == 3 e2[t]/KK, e2[0] == e0$^2, la[0] == lam0$, lz[0] == 0}, {e2, la, lz}, {t, -6, 6},
   WorkingPrecision -> 30, AccuracyGoal -> 25, PrecisionGoal -> 25][[1]];
vRef$ = minCW[V1L, e0$, 0][[1]];   (* mu = mu0: the same as (c) *)
muRows$ = Table[Module[{tt = k Log[2], ev, lv, z, dv, p0, curv, vals, pn, cn},
    ev = Sqrt[e2[tt] /. rge$]; lv = la[tt] /. rge$; z = Exp[lz[tt] /. rge$];   (* phi(mu) = z phi(mu0) *)
    vals = {e -> ev, lam -> lv, mu -> Exp[tt]};
    dv = D[V0 + V1L, phi] /. vals;
    p0 = p /. Quiet[FindRoot[Re[N[dv /. phi -> SetPrecision[p, 50], 50]], {p, 1/ev/4, 4/ev}, Method -> "Brent", WorkingPrecision -> 30],
        FindRoot::precw];
    curv = Re[N[(D[V0 + V1L, {phi, 2}] /. vals) /. phi -> p0, 30]];
    (* the same with the couplings frozen at mu0 *)
    pn = p /. FindRoot[Re[N[(D[V0 + V1L, phi] /. {e -> e0$, lam -> lam0$, mu -> Exp[tt]}) /. phi -> SetPrecision[p, 50], 50]],
        {p, Exp[tt]/e0$/8, 8 Exp[tt]/e0$}, Method -> "Brent", WorkingPrecision -> 30];
    cn = Re[N[(D[V0 + V1L, {phi, 2}] /. {e -> e0$, lam -> lam0$, mu -> Exp[tt]}) /. phi -> pn, 30]];
    Print["(d) mu = 2^", k, ": e = ", N[ev, 8], ", lam = ", N[lv, 8], ";  v (mu0 normalization) = ", N[p0/z, 10],
      ", ln(v/v(mu0)) = ", If[k == 0, 0, N[Log[p0/z/vRef$], 5]], " (running of mA2 in V1: (20/3)(e^2/K)(t^2 - t/6) = ",
      N[20/3 e0$^2/KK (tt^2 - tt/6), 5], ")",
      ", V''/(e^2 v^2) at mu = ", N[curv/(ev^2 p0^2), 8], ";  frozen couplings: v = ", N[pn, 8]];
    {k, ev, lv, z, p0/z, curv/(ev^2 p0^2), pn, cn/(e0$^2 pn^2)}], {k, -6, 6, 2}];
Export[FileNameJoin[{resDirCW$, "cw_mu.csv"}],
  Map[cell$, Prepend[muRows$, {"log2_mu", "e", "lam", "phi_ratio", "v_mu0norm", "MH2_over_MA2_at_mu", "v_frozen", "MH2_over_MA2_frozen"}], {2}], "CSV"];
Print["(d) written results/cw_ratio.csv, results/cw_mu.csv, results/cw_points.csv"];
