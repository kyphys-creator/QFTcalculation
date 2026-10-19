(* ::Package:: *)

(* ::Title:: *)
(*Step (2) of the NLO note: the same massless fermion pair with a photon mass*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (2), the independent check.  The radiated boson gets a mass lambda (w = lambda^2/M^2); the*)
(*fermions stay massless.  Then the soft and the collinear regions are both cut off by lambda, and the real emission and the*)
(*virtual correction are separately finite in 4 dimensions; their sum must tend to (alpha C/(2 pi)) 3/2 as w -> 0.*)
(*  Virtual: the vertex with the massive boson (Feynman gauge; the U(1) part, so the boson's own longitudinal part does not*)
(*        couple to the conserved current) and the on-shell field constant delta Z = Sigma_V(0) of the massless fermion,*)
(*        Sigma(p) = pslash Sigma_V(p^2).  FeynCalc's TID to PaVe functions and Package-X (FeynHelpers' PaXEvaluate)*)
(*        for their analytic forms; the UV poles cancel between the two (the Ward identity).*)
(*  Real: sum|M_R|^2 of Z -> f fbar gamma(lambda) in 4 dimensions (polarization sums -g: the k k/lambda^2 part vanishes on the*)
(*        conserved current), integrated over the Dalitz region of masses (0, 0, lambda) with NIntegrate,*)
(*          Gamma_R/Gamma_0 = (alpha C/(2 pi)) (1/2) int dy13 dy23 r,   r = M^2 sum|M_R|^2/(e^2 Q^2 sum|M_0|^2),*)
(*        y13 = (p1 + p3)^2/M^2 in [w, 1], y23 between w + (1 - y13) w/y13 and w + 1 - y13.*)
(*The real part of the analytic virtual correction is written in closed form, and its w -> 0 form*)
(*(alpha C/(2 pi)) (-ln^2 w - 3 ln w - 7/2 + pi^2/3) is taken from it; Gamma_R must then tend to (alpha C/(2 pi))*)
(*(ln^2 w + 3 ln w + 5 - pi^2/3).  Writes results/ir_photonmass.csv.*)
(*Batch:  wolframscript -file ir_photonmass.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirPM$ = DirectoryName[$InputFileName];
resDirPM$ = FileNameJoin[{srcDirPM$, "results"}];

(* ::Section:: *)
(*Virtual correction with the boson mass*)

FCClearScalarProducts[];
ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[p1, p2] = MM/2;
amp0PM$ = Spinor[Momentum[p1, D], 0].GAD[mu].Spinor[-Momentum[p2, D], 0];
bornPM$ = Simplify[Contract[(FermionSpinSum[amp0PM$ ComplexConjugate[amp0PM$ /. mu -> nu]] /.
        DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]) (-MTD[mu, nu])]];
vtxPM$ = Spinor[Momentum[p1, D], 0].GAD[rho].(GSD[p1] - GSD[q]).GAD[mu].(-GSD[p2] - GSD[q]).GAD[rho].Spinor[-Momentum[p2, D], 0] *
   FAD[{q, la}, q - p1, q + p2];
xPM$ = FermionSpinSum[vtxPM$ ComplexConjugate[amp0PM$ /. mu -> nu]];
xPM$ = Contract[(xPM$ /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]) (-MTD[mu, nu])];
tVtx$ = Simplify[TID[xPM$, q, ToPaVe -> True]];
Print["vertex, TID: ", tVtx$];
(* F = M1/M0 = (e^2 Q^2/(16 pi^2)) [TID/(i pi^2)]/sum|M0|^2  (the factors as in ir_massless_feyncalc.wl) *)
fVtx$ = PaXEvaluate[tVtx$/(I Pi^2)/bornPM$, PaXC0Expand -> True];

(* the self-energy: -i Sigma = (-i e Q)^2 i (-i) mu^(2 eps) int d^Dq/(2 pi)^D gamma^rho (pslash - qslash) gamma_rho/((p - q)^2 (q^2 - lambda^2)),
   so Sigma = (e^2 Q^2/(16 pi^2)) TID/(i pi^2);  Sigma_V = tr(pslash Sigma)/(4 p^2), then p^2 -> 0 *)
FCClearScalarProducts[];
ScalarProduct[p, p] = pp;
sePM$ = GAD[rho].(GSD[p] - GSD[q]).GAD[rho] FAD[{q, la}, q - p];
tSE$ = Simplify[TID[sePM$, q, ToPaVe -> True]];
Print["self-energy, TID: ", tSE$];
sigV$ = Simplify[DiracTrace[GSD[p].tSE$, DiracTraceEvaluate -> True]/(4 pp)/(I Pi^2)];
sigVPX$ = PaXEvaluate[sigV$];
sigV0$ = Simplify[Limit[sigVPX$, pp -> 0], la > 0 && ScaleMu > 0];
Print["Sigma_V(0)/(e^2 Q^2/(16 pi^2)) = ", sigV0$];
(* Gamma_V/Gamma_0 = 2 Re F + 2 delta Z, delta Z = Sigma_V(0); in units of alpha C/(2 pi) = e^2 Q^2/(8 pi^2) *)
vSum$ = fVtx$ + sigV0$;
vPole$ = Simplify[Coefficient[Expand[Normal[Series[vSum$ /. D -> 4 - 2 Epsilon, {Epsilon, 0, 0}]]], Epsilon, -1]];
Print["UV pole of vertex + delta Z (expect 0): ", vPole$];
vFin$ = Normal[Series[vSum$ /. D -> 4 - 2 Epsilon, {Epsilon, 0, 0}]] /. Epsilon -> Infinity;
vFin$ = vFin$ /. {MM -> 1, la -> Sqrt[w], ScaleMu -> 1};
Print["  the scale mu drops out: ", FreeQ[vFin$, ScaleMu]];
gammaV$[wv_] := Re[N[vFin$ /. w -> wv, 30]];
(* the real part in closed form (s = M^2 + i0: Log[-w] = Log[w] + i pi; only Log[-w]^2 enters, so the sign of i pi drops out) *)
reV$ = FullSimplify[ComplexExpand[Re[vFin$ /. Log[-w] -> Log[w] + I Pi]], 0 < w < 1];
Print["Re(virtual)/(alpha C/(2 pi)) = ", reV$];
Print["  minus the numerical value at w = 1e-4 (expect 0): ", ToString[N[(reV$ /. w -> 10^-4) - gammaV$[10^-4], 20], InputForm]];
(* w -> 0: Re Li2(1 + w) -> Li2(1) = pi^2/6 *)
vLead$ = Simplify[Normal[Series[reV$ /. Re[PolyLog[2, 1 + w]] -> Pi^2/6, {w, 0, 0}, Assumptions -> 0 < w < 1]], 0 < w < 1];
Print["  its w -> 0 form: ", vLead$, ";  minus (-ln^2 w - 3 ln w - 7/2 + pi^2/3) (expect 0): ",
  Simplify[vLead$ - (-Log[w]^2 - 3 Log[w] - 7/2 + Pi^2/3)]];

(* ::Section:: *)
(*Real emission of the massive boson in 4 dimensions*)

FCClearScalarProducts[];
ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[p3, p3] = MM w;
ScalarProduct[p1, p3] = MM (y13 - w)/2; ScalarProduct[p2, p3] = MM (y23 - w)/2; ScalarProduct[p1, p2] = MM (1 + w - y13 - y23)/2;
ampRPM$ = Spinor[Momentum[p1], 0].(GA[rho].(GS[p1] + GS[p3]).GA[mu]/(MM y13) -
      GA[mu].(GS[p2] + GS[p3]).GA[rho]/(MM y23)).Spinor[-Momentum[p2], 0];
xR$ = FermionSpinSum[ampRPM$ ComplexConjugate[ampRPM$ /. {mu -> nu, rho -> sig}]];
xR$ = Contract[(xR$ /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]) (-MT[mu, nu]) (-MT[rho, sig])];
rPM$ = Simplify[MM xR$/(4 MM)];
Print["r(w) = M^2 sum|M_R|^2/(e^2 Q^2 sum|M_0|^2): ", rPM$];
Print["  at w = 0 it is the d = 4 form of ir_massless_feyncalc.wl: ",
  Simplify[(rPM$ /. w -> 0) - 2 ((1 - y23)^2 + (1 - y13)^2)/(y13 y23)] === 0];
rFun$ = Function[{wv, a, b}, Evaluate[rPM$ /. {w -> wv, y13 -> a, y23 -> b}]];
(* logarithmic variables: y13 = w (1/w)^u, y23 = lo (hi/lo)^v *)
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
rowsPM$ = Table[Module[{gv = gammaV$[wv], gr = gammaR$[wv], lw = Log[wv]},
    Print["w = ", fmtE$[wv], ":  Gamma_V/(Gamma_0 alpha C/(2 pi)) = ", fmtF$[gv], ",  Gamma_R = ", fmtF$[gr],
     ",  sum - 3/2 = ", fmtE$[gv + gr - 3/2]];
    Print["          minus the leading terms: virtual ", fmtE$[gv - (-lw^2 - 3 lw - 7/2 + Pi^2/3)],
     ",  real ", fmtE$[gr - (lw^2 + 3 lw + 5 - Pi^2/3)]];
    {N[wv], N[gv, 16], N[gr, 16], N[gv + gr - 3/2, 6], N[gv - (-lw^2 - 3 lw - 7/2 + Pi^2/3), 6],
     N[gr - (lw^2 + 3 lw + 5 - Pi^2/3), 6]}], {wv, {10^-4, 10^-6, 10^-8, 10^-10}}];
Export[FileNameJoin[{resDirPM$, "ir_photonmass.csv"}], Prepend[rowsPM$,
   {"w", "virtual_over_aC2pi", "real_over_aC2pi", "sum_minus_3_2", "virtual_minus_leading", "real_minus_leading"}], "CSV"];
Print["written: results/ir_photonmass.csv"];
