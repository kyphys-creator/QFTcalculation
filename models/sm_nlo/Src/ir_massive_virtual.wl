(* ::Package:: *)

(* ::Title:: *)
(*Step (3) of the NLO note: the virtual correction and the soft real emission for massive emitters*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (3).  The abelian part of the radiation (alpha C = alpha_s C_F for the gluon, alpha Q^2 for the*)
(*photon), written as Gamma^(1)/Gamma_0 = (alpha C/pi) K.  Two decays:*)
(*  Z(k) -> Q(p1) Qbar(p2) with the currents gamma^mu (V) and gamma^mu gamma5 (A) separately (mass m, M^2 = k^2; they do not*)
(*      interfere in the width), and t(p) -> b(p1) W+(k) with gamma^mu P_L.*)
(*Virtual: the vertex with the gluon in Feynman gauge, d dimensions, TID to PaVe functions, Package-X (FeynHelpers' PaXEvaluate)*)
(*      for their analytic forms; the on-shell field constants delta Z = Sigma_V(m^2) + 2 m^2 (Sigma_V' + Sigma_S')(m^2) of each*)
(*      massive leg computed here the same way (the p^2 derivative taken on the integrand).  Package-X returns the full Laurent*)
(*      series of FeynCalc's normalization, (2 pi mu)^(4 - D)/(i pi^2) int d^Dq, so its ScaleMu^2 is 4 pi^2 mu^2 and gamma_E is*)
(*      explicit; UV and IR poles share one eps.  The virtual pole must equal the soft pole of Eq. (softpole), the UV poles cancel.*)
(*Soft: the eikonal factor of Eq. (eikonal) integrated in d dimensions over gluon energies E < Delta E in the rest frame of the*)
(*      decaying particle:  K_S = -(1/(4 eps)) (4 pi mu^2/Delta E^2)^eps/Gamma(1 - eps) Sigma(eps),  Sigma = 2 A12 - A11 - A22,*)
(*      A_ij = int_{-1}^{1} dc (1 - c^2)^(-eps) (p_i.p_j)/((E_i - pvec_i.n)(E_j - pvec_j.n)).  K_V + K_S must have no pole and no mu.*)
(*Writes results/ir_massive_vs.csv: K_V + K_S (finite, mu-free) for the channels at Delta E = delta E_max, and the virtual alone*)
(*(MadLoop's normalization: (4 pi)^eps/Gamma(1 - eps) stripped, mu_R) at the point of the CKM note's MadLoop check.*)
(*Batch:  wolframscript -file ir_massive_virtual.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
$MaxExtraPrecision = 500;
t0MV$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0MV$], " s] ", s];
srcDirMV$ = DirectoryName[$InputFileName];
resDirMV$ = FileNameJoin[{srcDirMV$, "results"}];
Quiet[CreateDirectory[resDirMV$]];
noCond$[x_] := x /. ConditionalExpression[a_, _] :> a;
laurent$[x_] := Normal[Series[noCond$[x] /. D -> 4 - 2 Epsilon, {Epsilon, 0, 0}]];
trEval$[x_] := x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];

(* ::Section:: *)
(*On-shell field constant of a massive quark (in units of g^2 C/(16 pi^2))*)

FCClearScalarProducts[];
numSE$ = GAD[rho].(GSD[p] - GSD[q] + mq).GAD[rho];
intV$ = DiracTrace[GSD[p].numSE$, DiracTraceEvaluate -> True]/(4 SPD[p, p]) FAD[q, {q - p, mq}];
intS$ = DiracTrace[numSE$, DiracTraceEvaluate -> True]/(4 mq) FAD[q, {q - p, mq}];
ddp2$[f_] := Contract[FVD[p, al] FourDivergence[f, FVD[p, al]]]/(2 SPD[p, p]);
dIntV$ = ddp2$[intV$]; dIntS$ = ddp2$[intS$];
ScalarProduct[p, p] = mq^2;
dZq$ = Simplify[laurent$[PaXEvaluate[TID[intV$ + 2 mq^2 (dIntV$ + dIntS$), q, ToPaVe -> True]/(I Pi^2)]], mq > 0 && ScaleMu > 0];
Print["delta Z/(g^2 C/(16 pi^2)) = ", dZq$];
Print["  minus -(3 (1/eps - gamma_E + ln(4 pi mu^2/m^2)) + 4) (expect 0): ",
  Simplify[dZq$ + 3 (1/Epsilon - EulerGamma + Log[ScaleMu^2/(Pi mq^2)]) + 4, mq > 0 && ScaleMu > 0]];
dZof$[mv_] := dZq$ /. mq -> mv;

(* ::Section:: *)
(*Virtual correction of Z -> Q Qbar (V and A)*)

FCClearScalarProducts[];
ScalarProduct[p1, p1] = m^2; ScalarProduct[p2, p2] = m^2; ScalarProduct[p1, p2] = (MM - 2 m^2)/2;
polZ$ = -MTD[mu, nu] + FVD[p1 + p2, mu] FVD[p1 + p2, nu]/MM;
amp0Z$[gam_] := Spinor[Momentum[p1, D], m].GAD[mu].gam.Spinor[-Momentum[p2, D], m];
bornZ$[gam_] := Simplify[Contract[trEval$[FermionSpinSum[amp0Z$[gam] ComplexConjugate[amp0Z$[gam] /. mu -> nu]]] polZ$]];
vtxZ$[gam_] := Spinor[Momentum[p1, D], m].GAD[rho].(GSD[p1] - GSD[q] + m).GAD[mu].gam.(-GSD[p2] - GSD[q] + m).GAD[rho].
     Spinor[-Momentum[p2, D], m] FAD[q, {q - p1, m}, {q + p2, m}];
(* K_V = 2 Re(M0^* M1)/|M0|^2/(alpha C/pi): M1/M0 = (g^2 C/(16 pi^2)) [TID/(i pi^2)]/sum|M0|^2, so the vertex gives (1/2) Re[TID/(i pi^2)/born],
   the two field constants 2 (delta Z/2) each, in units of alpha C/pi: (1/2) delta Z/(g^2 C/(16 pi^2)) x 2/... = delta Z_unit/2 *)
kVZ$ = Association[Table[gam -> Module[{x},
      x = FermionSpinSum[vtxZ$[gam] ComplexConjugate[amp0Z$[gam] /. mu -> nu]];
      x = Contract[trEval$[x] polZ$];
      x = TID[x, q, ToPaVe -> True];
      laurent$[PaXEvaluate[(1/2) x/(I Pi^2)/bornZ$[gam], PaXC0Expand -> True]] + dZof$[m]/2], {gam, {1, GA5}}]];
bornZv$ = <|1 -> bornZ$[1], GA5 -> bornZ$[GA5]|>;
tick$["Z virtual"];
Print["Born (d dimensions): V ", bornZv$[1], ",  A ", bornZv$[GA5]];
(* the soft pole of Eq. (softpole), in units of alpha C/pi: -1 + (1 + b^2)/(2 b) ln((1 + b)/(1 - b)) *)
toBeta$ = {m -> Sqrt[MM (1 - b^2)/4]};
softPoleZ$ = -1 + (1 + b^2)/(2 b) Log[(1 + b)/(1 - b)];
Do[Module[{pole = Coefficient[Expand[kVZ$[gam]], Epsilon, -1]},
    Print["Z, ", If[gam === 1, "V", "A"], ": Re(1/eps coefficient) minus the soft pole (expect 0): ",
     FullSimplify[Re[pole /. toBeta$] - softPoleZ$, 0 < b < 1 && MM > 0], ";  at b = 0.3, 0.9, 0.999: ",
     N[Table[Re[pole /. {m -> 1, MM -> 4/(1 - bv^2)}] - (softPoleZ$ /. b -> bv), {bv, {3/10, 9/10, 999/1000}}], 20]]],
  {gam, {1, GA5}}];

(* ::Section:: *)
(*Virtual correction of t -> b W+ (gamma^mu P_L = (V - A)/2)*)

FCClearScalarProducts[];
ScalarProduct[pt, pt] = mt^2; ScalarProduct[p1, p1] = mb^2; ScalarProduct[pt, p1] = (mt^2 + mb^2 - MW^2)/2;
polW$ = -MTD[mu, nu] + FVD[pt - p1, mu] FVD[pt - p1, nu]/MW^2;
amp0t$[gam_] := Spinor[Momentum[p1, D], mb].GAD[mu].gam.Spinor[Momentum[pt, D], mt];
bornT$[gam_] := Simplify[Contract[trEval$[FermionSpinSum[amp0t$[gam] ComplexConjugate[amp0t$[gam] /. mu -> nu]]] polW$]];
vtxT$[gam_] := Spinor[Momentum[p1, D], mb].GAD[rho].(GSD[p1] - GSD[q] + mb).GAD[mu].gam.(GSD[pt] - GSD[q] + mt).GAD[rho].
     Spinor[Momentum[pt, D], mt] FAD[q, {q - p1, mb}, {q - pt, mt}];
tidT$[gam_] := Module[{x},
   x = FermionSpinSum[vtxT$[gam] ComplexConjugate[amp0t$[gam] /. mu -> nu]];
   x = Contract[trEval$[x] polW$];
   TID[x, q, ToPaVe -> True]];
(* P_L: sum|M0|^2 = (B_V + B_A)/4 and 2 Re(M0^* M1) = (T_V + T_A)/4 (the V-A cross terms vanish with the symmetric polarization sum) *)
kVT$ = laurent$[PaXEvaluate[(1/2) (tidT$[1] + tidT$[GA5])/(I Pi^2)/(bornT$[1] + bornT$[GA5]), PaXC0Expand -> True]] +
   (dZof$[mt] + dZof$[mb])/4;
tick$["t virtual"];
Print["Born t -> b W+ (d dimensions, V + A): ", Simplify[bornT$[1] + bornT$[GA5]]];
(* the soft pole for the pair t, b: v = sqrt(1 - mt^2 mb^2/(pt.p1)^2) *)
vT$ = Sqrt[1 - mt^2 mb^2/((mt^2 + mb^2 - MW^2)/2)^2];
softPoleT$ = -1 - Log[(1 - vT$)/(1 + vT$)]/(2 vT$);
poleT$ = Coefficient[Expand[kVT$], Epsilon, -1];
Print["t -> b W+: 1/eps coefficient minus the soft pole at three mass points (expect 0): ",
  N[(poleT$ - softPoleT$) /. # & /@ {{mt -> 17257/100, mb -> 478/100, MW -> 803692/10000}, {mt -> 1, mb -> 1/10, MW -> 1/2},
      {mt -> 1, mb -> 3/10, MW -> 1/5}}, 20]];

(* ::Section:: *)
(*Soft real emission in d dimensions*)

(* the angular integrals to O(eps): A = A0 - eps A1 with A1 = int dc ln(1 - c^2) (...) *)
nint$[f_] := NIntegrate[f[x], {x, -1, 0, 1}, WorkingPrecision -> 40, PrecisionGoal -> 25, MaxRecursion -> 40];
angZ$[bv_] := Module[{f12 = Function[x, (1 + bv^2)/((1 - bv x) (1 + bv x))], f11 = Function[x, (1 - bv^2)/(1 - bv x)^2]},
   {2 nint$[f12] - 2 nint$[f11], 2 nint$[Log[1 - #^2] f12[#] &] - 2 nint$[Log[1 - #^2] f11[#] &]}];
angT$[bv_] := Module[{ftb = Function[x, 1/(1 - bv x)], fbb = Function[x, (1 - bv^2)/(1 - bv x)^2]},
   {2 nint$[ftb] - 2 - nint$[fbb], 2 nint$[Log[1 - #^2] ftb[#] &] - (4 Log[2] - 4) - nint$[Log[1 - #^2] fbb[#] &]}];
Print["the leading angular sums against their closed forms (expect 0): Z ",
  N[angZ$[3/10][[1]] - (2 (1 + 9/100)/(3/10) Log[13/7] - 4), 20], ",  t ",
  N[angT$[3/10][[1]] - (2/(3/10) Log[13/7] - 2 - 2), 20]];
(* K_S = -Sigma0/(4 eps) - (Sigma0 l - Sigma1)/4,  l = ln(4 pi mu^2/Delta E^2) - gamma_E = ln(ScaleMu^2/(pi Delta E^2)) - gamma_E *)
kS$[{s0_, s1_}, dE_] := -s0/(4 Epsilon) - (s0 (Log[ScaleMu^2/(Pi dE^2)] - EulerGamma) - s1)/4;
(* the soft pole of Z: -Sigma0/4 must equal minus the virtual pole *)
Print["Z: -Sigma0/4 + soft pole at b = 0.3 (expect 0): ", N[-angZ$[3/10][[1]]/4 + (softPoleZ$ /. b -> 3/10), 20]];

(* ::Section:: *)
(*K_V + K_S for the channels*)

(* the pole masses of nlo_inputs.py (PDG 2024) *)
massesMV$ = {"MZ" -> 911876/10000, "MW" -> 803692/10000, "MT" -> 17257/100, "MB" -> 478/100, "MC" -> 167/100,
   "MTA" -> 177693/100000, "MMU" -> 1056584/10000000};
mass$[k_] := k /. massesMV$;
deltas$ = {10^-4, 10^-5, 10^-6, 10^-7, 10^-8};
(* Z channels: name, m, M; the tests: massless limit (m/M = 1e-3, 1e-5) and threshold (b = 0.05, 0.01) *)
chanZ$ = {{"Z_b", mass$["MB"], mass$["MZ"]}, {"Z_c", mass$["MC"], mass$["MZ"]}, {"Z_ta", mass$["MTA"], mass$["MZ"]},
   {"Z_mu", mass$["MMU"], mass$["MZ"]}, {"Z_m1e-3", 1/1000, 1}, {"Z_m1e-5", 1/100000, 1},
   {"Z_b0.05", Sqrt[1 - (5/100)^2]/2, 1}, {"Z_b0.01", Sqrt[1 - (1/100)^2]/2, 1}};
vsZ$[gam_, mv_, Mv_, dl_] := Module[{bv = Sqrt[1 - 4 mv^2/Mv^2], emax = (Mv^2 - 4 mv^2)/(2 Mv), tot},
   tot = kVZ$[gam] + kS$[angZ$[bv], dl emax];
   tot = tot /. {m -> mv, MM -> Mv^2};
   {N[Re[Coefficient[tot, Epsilon, -1]], 20], N[Re[(tot /. Epsilon -> Infinity) /. ScaleMu -> 7], 25],
    N[Re[(tot /. Epsilon -> Infinity) /. ScaleMu -> 300], 25]}];
(* t channels: name, mt, mb, MW; the test: mb, MW -> 0 *)
chanT$ = {{"t_bW", mass$["MT"], mass$["MB"], mass$["MW"]}, {"t_mb1e-3_MW1e-3", 1, 1/1000, 1/1000}, {"t_mb1e-4_MW1e-4", 1, 1/10000, 1/10000}};
vsT$[mtv_, mbv_, mwv_, dl_] := Module[{eb = (mtv^2 + mbv^2 - mwv^2)/(2 mtv), pb, emax = (mtv^2 - (mbv + mwv)^2)/(2 mtv), tot},
   pb = Sqrt[eb^2 - mbv^2];
   tot = kVT$ + kS$[angT$[pb/eb], dl emax];
   tot = tot /. {mt -> mtv, mb -> mbv, MW -> mwv};
   {N[Re[Coefficient[tot, Epsilon, -1]], 20], N[Re[(tot /. Epsilon -> Infinity) /. ScaleMu -> 7], 25],
    N[Re[(tot /. Epsilon -> Infinity) /. ScaleMu -> 300], 25]}];
tick$["soft"];
rowsMV$ = {};
Do[Do[Module[{r = vsZ$[gam, c[[2]], c[[3]], dl]},
     If[dl == deltas$[[1]], Print[c[[1]], " ", If[gam === 1, "V", "A"], ": pole of K_V + K_S ", CForm[N[r[[1]], 3]],
       ",  mu = 7 minus mu = 300: ", CForm[N[r[[2]] - r[[3]], 3]], ";  K_V + K_S at delta = 1e-4: ", CForm[N[r[[2]], 12]]]];
     AppendTo[rowsMV$, {c[[1]] <> If[gam === 1, "_V", "_A"], N[dl], ToString[CForm[N[r[[2]], 20]]]}]], {gam, {1, GA5}}, {dl, deltas$}],
  {c, chanZ$}];
Do[Do[Module[{r = vsT$[c[[2]], c[[3]], c[[4]], dl]},
    If[dl == deltas$[[1]], Print[c[[1]], ": pole of K_V + K_S ", CForm[N[r[[1]], 3]], ",  mu = 7 minus mu = 300: ",
      CForm[N[r[[2]] - r[[3]], 3]], ";  K_V + K_S at delta = 1e-4: ", CForm[N[r[[2]], 12]]]];
    AppendTo[rowsMV$, {c[[1]], N[dl], ToString[CForm[N[r[[2]], 20]]]}]], {dl, deltas$}], {c, chanT$}];
Export[FileNameJoin[{resDirMV$, "ir_massive_vs.csv"}], Prepend[rowsMV$, {"channel", "delta", "KV_plus_KS"}], "CSV"];

(* ::Section:: *)
(*The virtual alone in MadLoop's normalization at the CKM note's MadLoop point*)

tick$["channels"];
(* strip (4 pi)^eps Gamma(1 + eps): ScaleMu^2 -> pi e^gamma_E mu_R^2 removes gamma_E and ln(4 pi) with the poles *)
msML$[x_, muR_] := Module[{y = Expand[x /. ScaleMu -> Sqrt[Pi Exp[EulerGamma]] muR]},
   {Coefficient[y, Epsilon, -1], y /. Epsilon -> Infinity}];
pointML$ = {"MZ" -> 91, "MW" -> 80, "MT" -> 165, "MB" -> 286/100};
mlRows$ = {};
Do[Module[{mz = "MZ" /. pointML$, mw = "MW" /. pointML$, mbv = "MB" /. pointML$, mtv = "MT" /. pointML$, s2, vb, ab, bV, bA, z, t},
   s2 = 1 - mw^2/mz^2; vb = -1/2 + 2/3 s2; ab = -1/2;
   bV = bornZv$[1] /. {D -> 4, m -> mbv, MM -> mz^2}; bA = bornZv$[GA5] /. {D -> 4, m -> mbv, MM -> mz^2};
   z = (vb^2 bV msML$[kVZ$[1], muR] + ab^2 bA msML$[kVZ$[GA5], muR])/(vb^2 bV + ab^2 bA) /. {m -> mbv, MM -> mz^2};
   t = msML$[kVT$, muR] /. {mt -> mtv, mb -> mbv, MW -> mw};
   Print["MadLoop point, mu_R = ", muR, ":  Z -> b bbar  K_V pole ", N[Re[z[[1]]], 15], ", finite ", N[Re[z[[2]]], 15],
    ";  t -> b W+  pole ", N[Re[t[[1]]], 15], ", finite ", N[Re[t[[2]]], 15]];
   AppendTo[mlRows$, {"z_bb", muR, ToString[CForm[N[Re[z[[1]]], 20]]], ToString[CForm[N[Re[z[[2]]], 20]]]}];
   AppendTo[mlRows$, {"t_bw", muR, ToString[CForm[N[Re[t[[1]]], 20]]], ToString[CForm[N[Re[t[[2]]], 20]]]}]], {muR, {91, 500}}];
Export[FileNameJoin[{resDirMV$, "ir_massive_virtual_ml.csv"}], Prepend[mlRows$, {"process", "mu_R", "KV_pole", "KV_finite"}], "CSV"];
Print["written: results/ir_massive_vs.csv, results/ir_massive_virtual_ml.csv"];
