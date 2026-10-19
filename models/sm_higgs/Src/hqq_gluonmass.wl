(* ::Package:: *)

(* ::Title:: *)
(*Step (3) of the Higgs note: the same massless H -> q qbar with a gluon mass*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (3), the independent check; the scalar-current version of the NLO note's ir_photonmass.wl.*)
(*The radiated boson gets a mass lambda (w = lambda^2/M^2; the abelian part, alpha C = alpha_s C_F), the quarks stay massless.*)
(*The soft and the collinear regions are both cut off by lambda, so the real emission and the virtual correction are separately*)
(*infrared finite in 4 dimensions; the UV pole stays in dimensional regularization and is removed by the MS-bar Yukawa*)
(*counterterm, as in hqq_massless_feyncalc.wl.  As w -> 0 the sum must tend to (alpha C/(2 pi)) (17/2 + 3 ln(mu^2/M^2)).*)
(*  Virtual: the scalar vertex with the massive boson (Feynman gauge) and the on-shell field constant delta Z = Sigma_V(0) of the*)
(*        massless quark, Sigma(p) = pslash Sigma_V(p^2) (both legs: 2 delta Z in the width); FeynCalc's TID and Package-X;*)
(*        the UV pole of vertex + 2 delta Z must equal the MS-bar one, +3 in units of alpha C/(2 pi) (2 dy/y = -3/eps there), and the*)
(*        finite part is taken with ScaleMu^2 = pi e^gamma mu^2 (the MS-bar scale of FeynCalc's normalization).*)
(*  Real: sum|M_R|^2 of H -> q qbar g(lambda) in 4 dimensions (the k k/lambda^2 part of the polarization sum vanishes on the*)
(*        conserved colour current), integrated over the Dalitz region of masses (0, 0, lambda) with NIntegrate,*)
(*          Gamma_R/Gamma_0 = (alpha C/(2 pi)) (1/2) int dy13 dy23 r,   r = M^2 sum|M_R|^2/(e^2 Q^2 sum|M_0|^2).*)
(*Writes results/hqq_gluonmass.csv.  Batch:  wolframscript -file hqq_gluonmass.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirGM$ = DirectoryName[$InputFileName];
resDirGM$ = FileNameJoin[{srcDirGM$, "results"}];

(* ::Section:: *)
(*Virtual correction with the boson mass*)

FCClearScalarProducts[];
ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[p1, p2] = MM/2;
amp0GM$ = Spinor[Momentum[p1, D], 0].Spinor[-Momentum[p2, D], 0];
bornGM$ = Simplify[FermionSpinSum[amp0GM$ ComplexConjugate[amp0GM$]] /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]];
vtxGM$ = Spinor[Momentum[p1, D], 0].GAD[rho].(GSD[p1] - GSD[q]).(-GSD[p2] - GSD[q]).GAD[rho].Spinor[-Momentum[p2, D], 0] *
   FAD[{q, la}, q - p1, q + p2];
xGM$ = FermionSpinSum[vtxGM$ ComplexConjugate[amp0GM$]];
xGM$ = Contract[xGM$ /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]];
tVtx$ = Simplify[TID[xGM$, q, ToPaVe -> True]];
Print["vertex, TID: ", tVtx$];
fVtx$ = PaXEvaluate[tVtx$/(I Pi^2)/bornGM$, PaXC0Expand -> True];

FCClearScalarProducts[];
ScalarProduct[p, p] = pp;
seGM$ = GAD[rho].(GSD[p] - GSD[q]).GAD[rho] FAD[{q, la}, q - p];
tSE$ = Simplify[TID[seGM$, q, ToPaVe -> True]];
sigV$ = Simplify[DiracTrace[GSD[p].tSE$, DiracTraceEvaluate -> True]/(4 pp)/(I Pi^2)];
sigV0$ = Simplify[Limit[PaXEvaluate[sigV$], pp -> 0], la > 0 && ScaleMu > 0];
Print["Sigma_V(0)/(e^2 Q^2/(16 pi^2)) = ", sigV0$];
(* Gamma_V/Gamma_0 = 2 Re F + 2 delta Z + 2 dy/y; in units of alpha C/(2 pi) = e^2 Q^2/(8 pi^2): Re fVtx + sigV0 - 3/eps *)
vSum$ = fVtx$ + sigV0$;
vPole$ = Simplify[Coefficient[Expand[Normal[Series[vSum$ /. D -> 4 - 2 Epsilon, {Epsilon, 0, 0}]]], Epsilon, -1]];
Print["UV pole of vertex + delta Z: ", vPole$, "   (expect 3: removed by the MS-bar 2 dy/y = -3/eps)"];
vFin$ = Normal[Series[vSum$ /. D -> 4 - 2 Epsilon, {Epsilon, 0, 0}]] /. Epsilon -> Infinity;
(* MS-bar: ScaleMu^2 = pi e^gamma mu^2; mu^2 = wmu M^2 *)
vFin$ = vFin$ /. ScaleMu -> Sqrt[Pi Exp[EulerGamma] wmu MM] /. {la -> Sqrt[w MM]};
vFin$ = Simplify[vFin$ /. MM -> 1];
Print["  the renormalized virtual depends on M only through w and mu^2/M^2: ", FreeQ[vFin$, MM]];
gammaV$[wv_, wm_] := Re[N[vFin$ /. {w -> wv, wmu -> wm}, 30]];

(* ::Section:: *)
(*Real emission of the massive boson in 4 dimensions*)

FCClearScalarProducts[];
ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[p3, p3] = MM w;
ScalarProduct[p1, p3] = MM (y13 - w)/2; ScalarProduct[p2, p3] = MM (y23 - w)/2; ScalarProduct[p1, p2] = MM (1 + w - y13 - y23)/2;
ampRGM$ = Spinor[Momentum[p1], 0].(GA[rho].(GS[p1] + GS[p3])/(MM y13) - (GS[p2] + GS[p3]).GA[rho]/(MM y23)).Spinor[-Momentum[p2], 0];
xR$ = FermionSpinSum[ampRGM$ ComplexConjugate[ampRGM$ /. {rho -> sig}]];
xR$ = Contract[(xR$ /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]) (-MT[rho, sig])];
rGM$ = Simplify[MM xR$/(2 MM)];
Print["r(w) = M^2 sum|M_R|^2/(e^2 Q^2 sum|M_0|^2): ", rGM$];
Print["  at w = 0 it is the d = 4 form of hqq_massless_feyncalc.wl, 2 (1 + y12^2)/(y13 y23): ",
  Simplify[(rGM$ /. w -> 0) - 2 (1 + (1 - y13 - y23)^2)/(y13 y23)] === 0];
rFun$ = Function[{wv, a, b}, Evaluate[rGM$ /. {w -> wv, y13 -> a, y23 -> b}]];
gammaR$[wv_] := Module[{L = Log[1/wv]},
   (1/2) NIntegrate[Module[{a = wv Exp[u L], lo, hi},
       lo = wv + (1 - a) wv/a; hi = wv + 1 - a;
       rFun$[wv, a, lo Exp[v Log[hi/lo]]] a L lo Exp[v Log[hi/lo]] Log[hi/lo]],
     {u, 0, 1}, {v, 0, 1}, WorkingPrecision -> 30, PrecisionGoal -> 13, MaxRecursion -> 30,
     Method -> {"GlobalAdaptive", "MaxErrorIncreases" -> 20000}]];

(* ::Section:: *)
(*The sum as w -> 0*)

fmtF$[v_] := ToString[NumberForm[N[v, 16], 16]];
fmtE$[v_] := ToString[NumberForm[N[v], 3, NumberFormat -> (If[#3 === "", #1, #1 <> "e" <> #3] &), ExponentFunction -> (# &)]];
rowsGM$ = Flatten[Table[Module[{gr = gammaR$[wv]}, Table[Module[{gv = gammaV$[wv, wm], want = 17/2 + 3 Log[wm]},
       Print["w = ", fmtE$[wv], ", mu^2/M^2 = ", N[wm], ":  Gamma_V/(Gamma_0 alpha C/(2 pi)) = ", fmtF$[gv], ",  Gamma_R = ", fmtF$[gr],
        ",  sum - (17/2 + 3 ln(mu^2/M^2)) = ", fmtE$[gv + gr - want]];
       {N[wv], N[wm], N[gv, 16], N[gr, 16], N[gv + gr - want, 6]}], {wm, {1, 4}}]], {wv, {10^-4, 10^-6, 10^-8, 10^-10}}], 1];
Export[FileNameJoin[{resDirGM$, "hqq_gluonmass.csv"}], Prepend[rowsGM$,
   {"w", "mu2_over_M2", "virtual_over_aC2pi", "real_over_aC2pi", "sum_minus_expected"}], "CSV"];
Print["written: results/hqq_gluonmass.csv"];
