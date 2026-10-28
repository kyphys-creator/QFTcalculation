(* ::Package:: *)

(* ::Title:: *)
(*Step (10): the finite-temperature phase transition of the abelian Higgs model at one loop*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (10); no FeynCalc.  V0 = -m2 phi^2/2 + lam phi^4/4, masses mh2 = -m2 + 3 lam phi^2,*)
(*mG2 = -m2 + lam phi^2, mA2 = e^2 phi^2.  One loop, MS-bar at the scale mu (zero-temperature part of Eq. (V1)) plus*)
(*(T^4/(2 pi^2)) sum n J_B(m^2/T^2).  High-temperature expansion per degree of freedom (the ln m^2 of the zero-temperature*)
(*part cancels): m^2 T^2/24 - (T/(12 pi)) (m^2)^(3/2) + (m^4/(64 pi^2)) (3/2 - L_b - c),  L_b = 2 ln(mu/T) + 2 gamma_E*)
(*- 2 ln(4 pi) (DRalgo's L_b).*)
(*  (a) the high-T series against the exact J_B; the thermal masses Pi_h = Pi_G = (lam/3 + e^2/4) T^2 (gauge independent*)
(*      also in R_xi and Fermi gauges), Pi_L = e^2 T^2/3;*)
(*  (b) the general form D (T^2 - T0^2) phi^2 - E T phi^3 + lam_T phi^4/4 of the thermal note: D = (4 lam + 3 e^2)/24,*)
(*      E = e^3/(4 pi), lam_T = lam + (3 e^4/(16 pi^2))(2/3 - L_b), T0^2 = m2/(2 D); with the longitudinal mode screened*)
(*      (Debye mass) E -> 2E/3 at leading order;*)
(*  (c) T_c and phi_c/T_c for MH = 1/2 and 1 (lam = e^3/4, e^3; e = 1/2, MA = 1, mu = 1): the general form, the full*)
(*      one-loop high-T potential (Landau gauge) without and with the daisy resummation (Arnold-Espinosa), and the*)
(*      one-loop potential with the exact J_B (interpolated; compared with CosmoTransitions in thermal_ct.py);*)
(*      (the note's benchmark MH = 5/2 has lam >> e^3: a weak transition, only the general form is given);*)
(*  (d) gauge dependence: background R_xi and Fermi gauges with the same resummation (the 3D EFT at one loop; the G*)
(*      block with mG2 + Pi_G, which is O(lam phi^2) near T_c), xi = 1, 3; at fixed lam/e^3 the change of phi_c/T_c*)
(*      from Landau gauge falls like e (next order in the high-T counting);*)
(*  results/thermal.csv, results/thermal_gauge.csv, results/thermal_curves.csv, results/thermal_jb.csv.*)
(*Batch: wolframscript -file thermal.wl*)


srcDirTH$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirTH$ = FileNameJoin[{srcDirTH$, "results"}];
$NumberMarks = False;
cell$[y_] := If[StringQ[y], y, ToString[CForm[Chop[N[y, 16], 10^-30]]]];
KK = 16 Pi^2;
lbOf$[mu_, T_] := 2 Log[mu/T] + 2 EulerGamma - 2 Log[4 Pi];
mh2 = -m2 + 3 lam phi^2; mG2 = -m2 + lam phi^2; mA2 = e^2 phi^2;
V0 = -m2 phi^2/2 + lam phi^4/4;
(* high-T contribution of one bosonic degree of freedom with constant c; cube: Re of the principal branch *)
hT$[x_, c_] := x T^2/24 - T/(12 Pi) Re[x^(3/2)] + x^2/(64 Pi^2) (3/2 - Lb - c);
hT0$[x_, c_] := x T^2/24 + x^2/(64 Pi^2) (3/2 - Lb - c);           (* without the cubic term *)
cube$[x_] := -T/(12 Pi) Re[x^(3/2)];
piS = (lam/3 + e^2/4) T^2; piL = e^2 T^2/3;
VLandau = V0 + hT$[mh2, 3/2] + hT$[mG2, 3/2] + 3 hT$[mA2, 5/6];
(* Arnold-Espinosa: the cubic terms with the thermal masses (A_T: no thermal mass at this order) *)
VDaisy = V0 + hT0$[mh2, 3/2] + hT0$[mG2, 3/2] + 3 hT0$[mA2, 5/6] + cube$[mh2 + piS] + cube$[mG2 + piS] + 2 cube$[mA2] + cube$[mA2 + piL];
(* Fermi-gauge masses of the G - A_L block as functions of the G mass^2 (tree or resummed) *)
mpOf$[x_] := (x + Sqrt[x^2 - 4 xi mA2 x])/2; mmOf$[x_] := (x - Sqrt[x^2 - 4 xi mA2 x])/2;
mp$ = mpOf$[mG2]; mm$ = mmOf$[mG2];
(* background R_xi and Fermi gauges with the same resummation (the one-loop potential of the 3D EFT in these gauges):
   the G block uses mG2 + piS; the T^2 and log terms of G, A_L and ghosts sum to those of Landau gauge in the T^2 terms *)
VBack = V0 + hT0$[mh2, 3/2] + 3 hT0$[mA2, 5/6] + hT0$[mG2 + xi mA2, 3/2] - hT0$[xi mA2, 3/2] + cube$[mh2 + piS] + 2 cube$[mA2] +
   cube$[mA2 + piL] + cube$[mG2 + piS + xi mA2] - cube$[xi mA2];
VFermi = V0 + hT0$[mh2, 3/2] + 3 hT0$[mA2, 5/6] + hT0$[mp$, 3/2] + hT0$[mm$, 3/2] + cube$[mh2 + piS] + 2 cube$[mA2] +
   cube$[mA2 + piL] + cube$[mpOf$[mG2 + piS]] + cube$[mmOf$[mG2 + piS]];
Print["(d) xi -> 0: background R_xi and Fermi minus Landau (resummed; expect 0): ",
  N[Table[(({VBack, VFermi} - VDaisy) /. {e -> 1/8, lam -> 1/2048, m2 -> 1/32, Lb -> -6, T -> 2.83, phi -> p, xi -> 10^-12}),
     {p, {1/2, 7/5}}], 3]];


(* ::Section:: *)
(*(a) the high-T series and the thermal masses*)


jbExact$[y_?NumericQ] := Re[NIntegrate[x^2 Log[1 - Exp[-Sqrt[x^2 + y + 0 I]]], {x, 0, Sqrt[Max[0, -y]], Infinity},
     WorkingPrecision -> 30, PrecisionGoal -> 20, AccuracyGoal -> 25, MaxRecursion -> 40]];
(* T^4/(2 pi^2) J_B + MS-bar zero-T part with c = 3/2, mu = T e^(gamma_E)/(4 pi) e^(Lb/2): compare per dof at T = 1, Lb = 0 *)
jbSeries$[y_] := -Pi^4/45 + Pi^2 y/12 - Pi/6 Re[y^(3/2)] - y^2/32 (Log[y/(16 Pi^2 Exp[3/2 - 2 EulerGamma])]) ;
Do[Print["(a) J_B(y) exact ", N[jbExact$[y], 12], ", high-T series ", N[jbSeries$[SetPrecision[y, 30]], 12],
   " (y = ", y, ")"], {y, {1/10, 1/2, 1, 2}}];
Print["(a) thermal masses d^2/dphi^2 of the T^2 terms at phi = 0 (h, G): ",
  Simplify[{D[(mh2 + mG2 + 3 mA2) T^2/24, {phi, 2}]}], " = 2 x ", piS, ";  the same in background R_xi and Fermi gauges: ",
  Simplify[{(mG2 + xi mA2) - xi mA2 - mG2, mp$ + mm$ - mG2}]];
(* the J_B for the exact potential: the high-T series to y^3 (real part; its y^(3/2) and y^2 ln|y| are not analytic at
   y = 0) plus an interpolated remainder, which is O(y^4) and smooth, on a grid in s = sign(y) sqrt|y| *)
jbSer$[y_] := -Pi^4/45 + Pi^2 y/12 - Pi/6 Re[y^(3/2)] - If[y == 0, 0, y^2/32 Log[Abs[y]/(16 Pi^2 Exp[3/2 - 2 EulerGamma])]] +
    Zeta[3] y^3/(384 Pi^2);
jbTab$ = Table[{sv, jbExact$[Sign[sv] sv^2]}, {sv, -3, 8, 1/40}];
jbInt$ = Interpolation[Map[{#[[1]], If[#[[1]] == 0, 0, #[[2]] - jbSer$[N[Sign[#[[1]]] #[[1]]^2, 30]]]} &, jbTab$],
   InterpolationOrder -> 5];
jb$[y_?NumericQ] := jbSer$[y] + jbInt$[Sign[y] Sqrt[Abs[y]]];
Print["(a) remainder J_B - series to y^3 at y = 0.1, 1, 4: ", N[{jbExact$[1/10] - jbSer$[0.1`30], jbExact$[1] - jbSer$[1.`30],
     jbExact$[4] - jbSer$[4.`30]}, 3]];
Print["(a) J_B interpolation check at y = -1.3, -0.003, 2*10^-4, 0.37, 11.1: ", N[{jb$[-1.3] - jbExact$[-13/10],
     jb$[-0.003] - jbExact$[-3/1000], jb$[0.0002] - jbExact$[2/10000], jb$[0.37] - jbExact$[37/100], jb$[11.1] - jbExact$[111/10]}, 3]];
Export[FileNameJoin[{resDirTH$, "thermal_jb.csv"}], Map[cell$, Prepend[N[jbTab$, 20], {"s_sign_sqrt_y", "J_B"}], {2}], "CSV"];


(* ::Section:: *)
(*(b) the general form*)


dGen = (4 lam + 3 e^2)/24; eGen = e^3/(4 Pi); lamTGen = lam + 3 e^4/(16 Pi^2) (2/3 - Lb); t0Gen = Sqrt[m2/(2 dGen)];
genGauge$ = V0 + (mh2 + mG2 + 3 mA2) T^2/24 - T/(12 Pi) 3 mA2^(3/2) + 3 mA2^2/(64 Pi^2) (3/2 - Lb - 5/6);
Print["(b) general form: D (T^2 - T0^2) phi^2 - E T phi^3 + lam_T phi^4/4 minus [V0 + T^2 terms + gauge cubic and log]: ",
  Simplify[PowerExpand[(dGen (T^2 - t0Gen^2) phi^2 - eGen T phi^3 + lamTGen phi^4/4) - (genGauge$ - (genGauge$ /. phi -> 0))],
   e > 0 && phi > 0 && m2 > 0 && lam > 0]];
Print["(b) D = ", dGen, ", E = ", eGen, ", lam_T = ", lamTGen, ", T0^2 = ", Simplify[t0Gen^2]];
(* the screened longitudinal mode at leading order: expand (mA2 + piL)^(3/2) in mA2 *)
scr$ = Normal[Series[-T/(12 Pi) (eps mA2 + piL)^(3/2), {eps, 0, 2}]] /. eps -> 1;
Print["(b) -(T/12 pi)(mA2 + Pi_L)^(3/2) = ", InputForm[Simplify[PowerExpand[scr$], T > 0 && e > 0]],
  " + ...:  E -> 2E/3, D -> D - e^3/(8 sqrt3 pi), lam_T -> lam_T - sqrt3 e^3/(8 pi)"];
tcGen$[dd_, ee_, lt_, t0_] := Sqrt[t0^2/(1 - ee^2/(lt dd))];


(* ::Section:: *)
(*(c) T_c and phi_c/T_c*)


benchTH$[mh_] := {e -> 1/2, lam -> (1/2)^2 mh^2/2, m2 -> (1/2)^2 mh^2/2 4, mu -> 1};   (* v = 2, MA = 1 *)
(* machine-precision functions of (T, phi), built once per potential and parameter set *)
vFun[v_, vals_, xv_] := vFun[v, vals, xv] = Module[{ex = v /. vals /. xi -> xv /. Lb -> lbOf$[mu /. vals, T]},
    Function[{tt, p}, Evaluate[Re[N[ex /. {T -> tt, phi -> p}]]]]];
vNum[v_, vals_, xv_, tt_?NumericQ, p_?NumericQ] := vFun[v, vals, xv][tt, p];
(* the exact one-loop potential: MS-bar zero-T part + J_B *)
vExact[vals_, tt_?NumericQ, p_?NumericQ] := Module[{ms = N[{mh2, mG2, mA2} /. vals /. phi -> p], mu0 = mu /. vals},
   N[V0 /. vals /. phi -> p] + Sum[{1, 1, 3}[[i]] (Re[If[ms[[i]] == 0, 0, ms[[i]]^2 (Log[ms[[i]]/mu0^2 + 0 I] -
              {3/2, 3/2, 5/6}[[i]])]]/(64 Pi^2) + tt^4/(2 Pi^2) jb$[ms[[i]]/tt^2]), {i, 3}]];
(* the broken minimum near pguess, and T_c from V(phi_min) = V(0) *)
pmin$[f_, tt_?NumericQ, pguess_?NumericQ] := Module[{r},
   r = Quiet[FindMinimum[f[tt, p], {p, pguess, pguess/2, 2 pguess}, AccuracyGoal -> 14, PrecisionGoal -> 12]];
   {p /. r[[2]], r[[1]] - f[tt, 0]}];
dV$[f_, tt_?NumericQ, pg_?NumericQ] := pmin$[f, tt, pg][[2]];
(* T_c: the sign change of V(phi_min) - V(0) on a grid of T around the guess, then Brent; the minimum is searched within
   a factor 2 of the guess, so that the broken minimum is followed *)
tcOf$[f_, tGuess_, pGuess_] := Module[{ts, ds, i, tc, pc},
   ts = N[tGuess] (1 + Range[-15, 15]/100); ds = dV$[f, #, N[pGuess]] & /@ ts;
   i = SelectFirst[Range[Length[ts] - 1], ds[[#]] < 0 && ds[[# + 1]] > 0 &];
   tc = tt /. FindRoot[dV$[f, tt, N[pGuess]], {tt, ts[[i]], ts[[i + 1]]}, Method -> "Brent", AccuracyGoal -> 14,
       PrecisionGoal -> 12];
   pc = pmin$[f, tc, N[pGuess]][[1]];
   {tc, pc, pc/tc}];
(* a deeper minimum below the followed one (the xi-dependent structure at small phi), at T_c *)
lowMin$[f_, tc_, pc_] := Module[{g = Table[{x, f[tc, x] - f[tc, 0]}, {x, pc/50, 0.8 pc, pc/200}], m},
   m = First[MinimalBy[g, Last]]; If[m[[2]] < -10^-10 Abs[f[tc, pc/2] - f[tc, 0]], m[[1]]/tc, 0]];
rowsTH$ = {};
Do[Module[{vals = benchTH$[mh], lt, tc0, pc0, tcL, tcD, tcDg, tcE, tcF, ltc, dd, ee},
    dd = dGen /. vals; ee = eGen /. vals;
    (* general form, lam_T at T_c by iteration *)
    tc0 = t0Gen /. vals; Do[ltc = lamTGen /. vals /. Lb -> lbOf$[1, tc0]; tc0 = tcGen$[dd, ee, ltc, t0Gen /. vals], {6}];
    pc0 = 2 ee tc0/ltc;
    tcL = tcOf$[vNum[VLandau, vals, 0, #1, #2] &, tc0, pc0];
    tcD = tcOf$[vNum[VDaisy, vals, 0, #1, #2] &, tc0, pc0];
    tcE = tcOf$[vExact[vals, #1, #2] &, tcL[[1]], tcL[[2]]];
    Print["(c) MH = ", mh, " (lam = ", lam /. vals, "): general form T_c = ", N[tc0, 10], ", phi_c/T_c = ", N[pc0/tc0, 8],
      ";  high-T one loop (Landau) ", N[tcL[[1]], 10], ", ", N[tcL[[3]], 8], ";  with daisy ", N[tcD[[1]], 10], ", ",
      N[tcD[[3]], 8], ";  exact J_B ", N[tcE[[1]], 10], ", ", N[tcE[[3]], 8]];
    AppendTo[rowsTH$, {mh, lam /. vals, N[tc0], N[pc0/tc0], tcL[[1]], tcL[[3]], tcD[[1]], tcD[[3]], tcE[[1]], tcE[[3]],
      tcE[[2]]}]], {mh, {1/2, 1}}];
Module[{vals = benchTH$[5/2], dd, ee, tc0, ltc},
  dd = dGen /. vals; ee = eGen /. vals; tc0 = t0Gen /. vals;
  Do[ltc = lamTGen /. vals /. Lb -> lbOf$[1, tc0]; tc0 = tcGen$[dd, ee, ltc, t0Gen /. vals], {6}];
  Print["(c) MH = 5/2 (the benchmark, lam = 25/32 >> e^3): general form T_c = ", N[tc0, 10], ", phi_c/T_c = ", N[2 ee/ltc, 6]]];
Export[FileNameJoin[{resDirTH$, "thermal.csv"}],
  Map[cell$, Prepend[rowsTH$, {"MH", "lam", "Tc_general", "phic_Tc_general", "Tc_highT", "phic_Tc_highT", "Tc_daisy",
      "phic_Tc_daisy", "Tc_exactJB", "phic_Tc_exactJB", "phic_exactJB"}], {2}], "CSV"];

(* curves for the figure: V(phi, T_c) - V(0, T_c) for MH = 1/2, normalized by T_c^4 *)
Module[{vals = benchTH$[1/2], tcs, rows},
  tcs = {rowsTH$[[1, 5]], rowsTH$[[1, 7]], rowsTH$[[1, 9]]};
  rows = Table[Join[{x}, {(vNum[VLandau, vals, 0, tcs[[1]], x tcs[[1]]] - vNum[VLandau, vals, 0, tcs[[1]], 0])/tcs[[1]]^4,
       (vNum[VDaisy, vals, 0, tcs[[2]], x tcs[[2]]] - vNum[VDaisy, vals, 0, tcs[[2]], 0])/tcs[[2]]^4,
       (vExact[vals, tcs[[3]], x tcs[[3]]] - vExact[vals, tcs[[3]], 0])/tcs[[3]]^4}], {x, 0, 1, 1/200}];
  Export[FileNameJoin[{resDirTH$, "thermal_curves.csv"}],
   Map[cell$, Prepend[rows, {"phi_over_Tc", "highT_Landau", "daisy_Landau", "exactJB_Landau"}], {2}], "CSV"]];


(* ::Section:: *)
(*(d) gauge dependence*)


(* scan: lam = r e^3 with r = 1/4, MA = 1 (v = 1/e), mu = 1; Landau, background R_xi (1, 3), Fermi (1, 3) *)
gaugeRows$ = {};
Do[Module[{vals = {e -> ev, lam -> ev^3/4, m2 -> ev^3/4/ev^2, mu -> 1}, dd, ee, ltc, tc0, pc0, res, land},
    dd = dGen /. vals; ee = eGen /. vals; tc0 = t0Gen /. vals;
    Do[ltc = lamTGen /. vals /. Lb -> lbOf$[1, tc0]; tc0 = tcGen$[dd, ee, ltc, t0Gen /. vals], {6}];
    pc0 = 2 ee tc0/ltc;
    land = tcOf$[vNum[VDaisy, vals, 0, #1, #2] &, tc0, pc0];       (* the guess for the other gauges *)
    res = Table[Module[{f = vNum[g[[2]], vals, g[[3]], #1, #2] &, r},
        r = tcOf$[f, land[[1]], land[[2]]];
        {g[[1]], g[[3]], r[[1]], r[[3]], lowMin$[f, r[[1]], r[[2]]]}], {g, {{"Landau", VDaisy, 0}, {"background R_xi", VBack, 1}, {"background R_xi", VBack, 3},
         {"Fermi", VFermi, 1}, {"Fermi", VFermi, 3}}}];
    Do[Print["(d) e = ", ev, " (lam = e^3/4): ", r[[1]], " xi = ", r[[2]], ": T_c = ", N[r[[3]], 10], ", phi_c/T_c = ", N[r[[4]], 8],
       ";  relative to Landau - 1: T_c ", N[r[[3]]/res[[1, 3]] - 1, 4], ", phi_c/T_c ", N[r[[4]]/res[[1, 4]] - 1, 4],
       If[r[[5]] > 0, ";  a deeper minimum at phi/T_c = " <> ToString[NumberForm[r[[5]], 3]], ""]], {r, res}];
    gaugeRows$ = Join[gaugeRows$, Map[Join[{ev, pc0/tc0}, #] &, res]]], {ev, {1/2, 1/4, 1/8, 1/16, 1/32}}];
Export[FileNameJoin[{resDirTH$, "thermal_gauge.csv"}],
  Map[cell$, Prepend[gaugeRows$, {"e", "phic_Tc_general", "gauge", "xi", "Tc", "phic_Tc", "deeper_min_phi_over_Tc"}], {2}], "CSV"];
Print["(d) written results/thermal.csv, results/thermal_gauge.csv, results/thermal_curves.csv, results/thermal_jb.csv"];
