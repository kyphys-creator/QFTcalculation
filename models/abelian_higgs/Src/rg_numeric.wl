(* ::Package:: *)

(* ::Title:: *)
(*Step (6): the beta functions from the mu dependence of physical quantities, and RG-consistency of the pole masses and the width*)


(* ::Text:: *)
(*Reads results/oneloop_sigma.m (step (3)) and results/nlo_width_sigma.m (step (5)); no FeynCalc.*)
(*  (a) symbolic: the MS-bar finite parts depend on mu only through A0fin = m^2 (1 - ln m^2 + ln mu^2) and*)
(*      B0fin = ... + ln mu^2.  mu independence of M_h,p^2 = MH^2 - Re Sigma^H(MH^2), M_A,p^2 = MA^2 - Re Sigma_T(MA^2) and*)
(*      of Gamma = Gamma_0(e) (1 + delta_OS) requires  dMH^2/dln mu = d Sigma^H/dln mu,  dMA^2/dln mu = d Sigma_T/dln mu,*)
(*      2 beta_e/e = -d delta_OS/dln mu.  With MH^2 = 2 m^2, MA^2 = e^2 m^2/lam this gives beta_e, beta_m2, beta_lam,*)
(*      compared with Eq. (rge) for general xi;*)
(*  (b) numbers: the MS-bar parameters run from mu = 1 (benchmark) to mu = 1/2, 2, 4 with the one-loop equations*)
(*      (NDSolve, 30 digits); the pole masses and Gamma_NLO computed at each mu (Package-X, xi = 1) change only at the*)
(*      two-loop level, while the same quantities without running change at the one-loop level;*)
(*  (c) results/rg_numeric.csv.*)
(*Batch: wolframscript -file rg_numeric.wl*)


srcDirRG$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirRG$ = FileNameJoin[{srcDirRG$, "results"}];
$NumberMarks = False;
KK = 16 Pi^2;
plain$[x_] := x /. {s_Symbol /; SymbolName[s] === "A0" :> A0, s_Symbol /; SymbolName[s] === "B0" :> B0,
    s_Symbol /; SymbolName[s] === "C0" :> C0};
sig$ = Association[Map[plain$, Get[FileNameJoin[{resDirRG$, "oneloop_sigma.m"}]]]];
ff$ = Association[Map[plain$, Get[FileNameJoin[{resDirRG$, "nlo_width_sigma.m"}]]]];

toE$ = v -> MA/e;
kSigH$ = (Total[sig$["H"][[1]]] + Total[sig$["H"][[2]]]) /. toE$;
kSigT$ = (Total[sig$["T2"][[1]]] + Total[sig$["T2"][[2]]]) /. toE$;
derivP2$[x_] := D[x /. B0[p2, a_, b_] :> bfun[p2, a, b], p2] /. {Derivative[1, 0, 0][bfun][pp_, a_, b_] :> B0p[pp, a, b],
    bfun[pp_, a_, b_] :> B0[pp, a, b]};
lamE$ = e^2 MH^2/(2 MA^2);
kcA$ = 3 e^2 - xi e^2/2 - 3 lamE$ - 3 e^4/(2 lamE$);
tree$ = 2 e MA;
kFgR$ = ff$["Fg1PI"] + ff$["FgTad"] + kcA$ tree$/ep -
   1/2 ((derivP2$[kSigH$] /. p2 -> MH^2) + (3 - xi) e^2/ep + 2 ((derivP2$[kSigT$] /. p2 -> MA^2) - e^2/(3 ep))) tree$;
kFb$ = ff$["Fb1PI"] + ff$["FbTad"];
sG$ = 3 - MH^2/MA^2 + MH^4/(4 MA^4);
sB$ = MH^2 (MH^2 - 4 MA^2) (MH^2 - 2 MA^2)/(8 MA^4);

(* finite parts with explicit mu: A0fin = m^2 (1 - Log[m^2] + L), B0fin = b0r + L, L = ln mu^2 *)
finMu$[x_] := Module[{y = x /. A0[m2_] :> If[PossibleZeroQ[m2], 0, m2/ep + m2 (1 - Log[m2] + L)] /.
       B0[pp_, a_, b_] :> 1/ep + b0r[pp, a, b] + L /. C0[c__] :> c0r[c] /. B0p[c__] :> b0pr[c] /. D -> 4 - 2 ep},
   SeriesCoefficient[Series[y, {ep, 0, 0}], 0]];


(* ::Section:: *)
(*(a) beta functions from the mu dependence*)


(* d/dln mu = 2 d/dL; real parts: L is real *)
dSigH$ = Simplify[2 D[finMu$[kSigH$ /. p2 -> MH^2]/KK, L]];
dSigT$ = Simplify[2 D[finMu$[kSigT$ /. p2 -> MA^2]/KK, L]];
dDelta$ = Simplify[2 D[finMu$[(kFgR$ + kFb$ sB$/sG$)/KK]/(e MA) + finMu$[kSigT$ /. p2 -> MA^2]/KK/MA^2, L]];
Print["(a) d Sigma^H(MH^2)/dln mu = ", Factor[dSigH$], ";  d Sigma_T(MA^2)/dln mu = ", Factor[dSigT$],
  ";  d delta_OS/dln mu = ", Factor[dDelta$], "   (all independent of xi: ", FreeQ[{dSigH$, dSigT$, dDelta$}, xi], ")"];
betaE$ = Simplify[-e dDelta$/2];
betaM2$ = Simplify[dSigH$/2] /. MH^2 -> 2 m2;     (* MH^2 = 2 m^2 *)
dlnMA2$ = dSigT$/MA^2;
betaLam$ = Simplify[lamE$ (2 betaE$/e + dSigH$/MH^2 - dlnMA2$)];
toCoup$ = {MH -> Sqrt[2 lam] MA/e};
Print["(a) beta_e = ", Simplify[betaE$], ",  minus Eq. (rge): ", Simplify[betaE$ - e^3/(3 KK)]];
Print["(a) beta_m2/m2 = ", Simplify[(dSigH$/MH^2) /. toCoup$], ",  minus Eq. (rge): ",
  Simplify[(dSigH$/MH^2 /. toCoup$) - (8 lam - 6 e^2)/KK]];
Print["(a) beta_lam = ", Simplify[betaLam$ /. toCoup$], ",  minus Eq. (rge): ",
  Simplify[(betaLam$ /. toCoup$) - (20 lam^2 - 12 e^2 lam + 6 e^4)/KK]];


(* ::Section:: *)
(*(b) RG consistency at the benchmark*)


Get["X`"];
dropEps$[r_] := r /. {sy_Symbol /; SymbolName[sy] === "Eps" :> Infinity};
(* LoopRefine needs exact arguments: the running parameters (30 digits) are turned into rationals first *)
ex$[x_] := Rationalize[SetPrecision[x, 40], 10^-35];
pxB0$[pp_, a_, b_, mu_] := N[dropEps$[LoopRefine[PVB[0, 0, ex$[pp], Sqrt[ex$[a]], Sqrt[ex$[b]]]]] /.
    {sy_Symbol /; SymbolName[sy] === "Mu" :> mu}, 40];
pxB0p$[pp_, a_, b_, mu_] := Module[{s, r},
   r = dropEps$[LoopRefine[PVB[0, 0, s, Sqrt[ex$[a]], Sqrt[ex$[b]]]]] /. {sy_Symbol /; SymbolName[sy] === "Mu" :> mu};
   N[D[r, s] /. s -> ex$[pp], 40]];
pxC0$[a1_, a2_, a3_, m1_, m2_, m3_] := N[LoopRefine[PVC[0, 0, 0, ex$[a1], ex$[a2], ex$[a3], Sqrt[ex$[m1]], Sqrt[ex$[m2]],
      Sqrt[ex$[m3]]]], 40];
(* the mu-free parts of the finite parts: b0r = B0fin(mu = 1) etc.; L = ln mu^2 *)
evalAt$[x_, vals_, mu_] := N[finMu$[x] /. vals /. L -> Log[mu^2] /. {b0r[pp_, a_, b_] :> pxB0$[pp, a, b, 1],
      b0pr[pp_, a_, b_] :> pxB0p$[pp, a, b, 1], c0r[c__] :> pxC0$[c]}, 30];

(* one-loop running from mu = 1: t = ln mu *)
sol$ = NDSolve[{ee'[t] == ee[t]^3/(3 KK), ll'[t] == (20 ll[t]^2 - 12 ee[t]^2 ll[t] + 6 ee[t]^4)/KK,
     mm'[t] == mm[t] (8 ll[t] - 6 ee[t]^2)/KK, ee[0] == 1/2, ll[0] == 25/32, mm[0] == 25/8}, {ee, ll, mm}, {t, -1, 2},
    WorkingPrecision -> 30, PrecisionGoal -> 25, AccuracyGoal -> 25, MaxSteps -> 10^6][[1]];
paramsAt$[mu_] := Module[{t = Log[mu], ev, lv, mv},
   {ev, lv, mv} = {ee[t], ll[t], mm[t]} /. sol$;
   {e -> ev, MA -> ev Sqrt[mv/lv], MH -> Sqrt[2 mv], xi -> 1}];
poleAt$[mu_, vals_] := Module[{ma = MA /. vals, mh = MH /. vals},
   {Sqrt[mh^2 - Re[evalAt$[kSigH$ /. p2 -> MH^2, vals, mu]]/KK], Sqrt[ma^2 - Re[evalAt$[kSigT$ /. p2 -> MA^2, vals, mu]]/KK]}];
gamma0$[ev_, ma_, mh_] := Module[{x = ma^2/mh^2}, ev^2 mh^3/(32 Pi ma^2) Sqrt[1 - 4 x] (1 - 4 x + 12 x^2)];
(* NLO width at mu: e(mu), the loop parts with the running parameters, Gamma_0 with the pole masses of mu = 1 *)
deltaAt$[mu_, vals_] := Re[evalAt$[(kFgR$ + kFb$ sB$/sG$)/KK, vals, mu]]/(e MA /. vals) +
   Re[evalAt$[kSigT$ /. p2 -> MA^2, vals, mu]]/KK/(MA^2 /. vals);
p1$ = paramsAt$[1]; pole1$ = poleAt$[1, p1$];
rows$ = {};
Do[Module[{pv = paramsAt$[mu], pm, pmFixed, gam, gamFixed},
    pm = poleAt$[mu, pv];
    pmFixed = poleAt$[mu, p1$];            (* the parameters of mu = 1 used at mu: no running *)
    gam = gamma0$[e /. pv, pole1$[[2]], pole1$[[1]]] (1 + deltaAt$[mu, pv]);
    gamFixed = gamma0$[1/2, pole1$[[2]], pole1$[[1]]] (1 + deltaAt$[mu, p1$]);
    Print["(b) mu = ", mu, ": e, lam, m^2 = ", N[{e /. pv, (e^2 MH^2/(2 MA^2)) /. pv, (MH^2/2) /. pv}, 10],
      ";  M_h,p = ", N[pm[[1]], 12], ", M_A,p = ", N[pm[[2]], 12], ", Gamma_NLO = ", N[gam, 12],
      ";  without running: ", N[pmFixed[[1]], 10], ", ", N[pmFixed[[2]], 10], ", ", N[gamFixed, 10]];
    AppendTo[rows$, {mu, e /. pv, (e^2 MH^2/(2 MA^2)) /. pv, (MH^2/2) /. pv, pm[[1]], pm[[2]], gam, pmFixed[[1]], pmFixed[[2]], gamFixed}]],
  {mu, {1/2, 1, 2, 4}}];
ref$ = First[Select[rows$, #[[1]] == 1 &]];
zero$[x_] := If[x == 0, 0, N[x, 3]];
Do[Print["(b) mu = ", r[[1]], ": relative change from mu = 1 with running {M_h,p, M_A,p, Gamma} = ",
    zero$ /@ {r[[5]]/ref$[[5]] - 1, r[[6]]/ref$[[6]] - 1, r[[7]]/ref$[[7]] - 1}, ",  without running ",
    zero$ /@ {r[[8]]/ref$[[5]] - 1, r[[9]]/ref$[[6]] - 1, r[[10]]/ref$[[7]] - 1}], {r, Select[rows$, #[[1]] != 1 &]}];

Export[FileNameJoin[{resDirRG$, "rg_numeric.csv"}],
  Join[{{"mu", "e", "lam", "m2", "MH_pole", "MA_pole", "Gamma_NLO", "MH_pole_norun", "MA_pole_norun", "Gamma_norun"}},
    Map[CForm[N[#, 17]] &, rows$, {2}]], "CSV"];
Print["(c) written results/rg_numeric.csv"];
