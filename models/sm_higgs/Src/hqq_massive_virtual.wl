(* ::Package:: *)

(* ::Title:: *)
(*Step (4) of the Higgs note: the virtual correction and the soft emission of H -> Q Qbar with massive quarks*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (4); the scalar-current version of the NLO note's ir_massive_virtual.wl (step (3)).*)
(*H(k) -> Q(p1) Qbar(p2), mass m, M^2 = k^2, the abelian part of the radiation (alpha C = alpha_s C_F, or alpha Q^2 for the*)
(*photon), written as Gamma^(1)/Gamma_0 = (alpha C/pi) K with Gamma_0 = N_c y^2 M beta^3/(16 pi) in the scheme of y.*)
(*Virtual: the scalar vertex with the gluon in Feynman gauge, d dimensions, TID and Package-X; the on-shell field constants*)
(*      delta Z = Sigma_V(m^2) + 2 m^2 (Sigma_V' + Sigma_S')(m^2) of both legs (as the NLO note); and the counterterm of the*)
(*      Yukawa coupling, 2 dy/y, in two schemes:*)
(*        MS-bar (the note's):  dy/y = -3 (alpha C/(4 pi)) (1/eps - gamma_E + ln 4 pi),*)
(*        on shell (the pole Yukawa coupling sqrt(2) m/v): dy/y = dm/m = -(alpha C/(4 pi)) [3 (1/eps - gamma_E + ln(4 pi mu^2/m^2)) + 4].*)
(*      Package-X in FeynCalc's normalization (ScaleMu^2 = 4 pi^2 mu^2, gamma_E explicit); UV and IR poles share one eps.  The*)
(*      UV pole cancels with either counterterm, the IR pole must equal the soft one, -1 + (1 + b^2)/(2 b) ln((1 + b)/(1 - b)).*)
(*Soft: the eikonal factor integrated in d dimensions over E < Delta E in the H rest frame (the same as for the Z: it does not*)
(*      depend on the current), K_S = -(1/(4 eps)) (4 pi mu^2/Delta E^2)^eps/Gamma(1 - eps) Sigma(eps).*)
(*Writes results/hqq_massive_vs.csv (K_V + K_S at Delta E = delta E_max, on-shell scheme: finite and mu-free; the MS-bar scheme*)
(*at mu = M is checked to differ by 2 + (3/2) ln(M^2/m^2)) and results/hqq_massive_virtual_ml.csv (the MS-bar virtual alone in*)
(*MadLoop's normalization at the point of the CKM note's MadLoop checks).  Batch:  wolframscript -file hqq_massive_virtual.wl*)


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
(*On-shell field constant of a massive quark (in units of g^2 C/(16 pi^2)), as the NLO note*)

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

(* ::Section:: *)
(*Virtual correction of H -> Q Qbar*)

FCClearScalarProducts[];
ScalarProduct[p1, p1] = m^2; ScalarProduct[p2, p2] = m^2; ScalarProduct[p1, p2] = (MM - 2 m^2)/2;
amp0H$ = Spinor[Momentum[p1, D], m].Spinor[-Momentum[p2, D], m];
bornH$ = Simplify[trEval$[FermionSpinSum[amp0H$ ComplexConjugate[amp0H$]]]];
Print["Born (d dimensions, coupling and colour stripped): ", bornH$, "   (expect 2 (M^2 - 4 m^2))"];
vtxH$ = Spinor[Momentum[p1, D], m].GAD[rho].(GSD[p1] - GSD[q] + m).(-GSD[p2] - GSD[q] + m).GAD[rho].
    Spinor[-Momentum[p2, D], m] FAD[q, {q - p1, m}, {q + p2, m}];
xH$ = Contract[trEval$[FermionSpinSum[vtxH$ ComplexConjugate[amp0H$]]]];
tidH$ = TID[xH$, q, ToPaVe -> True];
(* in units of alpha C/pi: the vertex (1/2) Re[TID/(i pi^2)/born], the two field constants delta Z_unit/2, the counterterm *)
kVertZ$ = laurent$[PaXEvaluate[(1/2) tidH$/(I Pi^2)/bornH$, PaXC0Expand -> True]] + (dZq$ /. mq -> m)/2;
ctMS$ = -(3/2) (1/Epsilon - EulerGamma + Log[4 Pi]);
ctOS$ = -(1/2) (3 (1/Epsilon - EulerGamma + Log[ScaleMu^2/(Pi m^2)]) + 4);
kV$ = <|"MS" -> kVertZ$ + ctMS$, "OS" -> kVertZ$ + ctOS$|>;
tick$["H virtual"];
toBeta$ = {m -> Sqrt[MM (1 - b^2)/4]};
softPole$ = -1 + (1 + b^2)/(2 b) Log[(1 + b)/(1 - b)];
Print["UV: the pole of vertex + field constants without the counterterm minus the soft pole at b = 0.3, 0.9 (expect +3/2): ",
  N[Table[Re[Coefficient[Expand[kVertZ$], Epsilon, -1] /. {m -> 1, MM -> 4/(1 - bv^2)}] - (softPole$ /. b -> bv), {bv, {3/10, 9/10}}], 20]];
Do[Module[{pole = Coefficient[Expand[kV$[s]], Epsilon, -1]},
   Print[s, ": Re(1/eps coefficient of K_V) minus the soft pole (expect 0): ", FullSimplify[Re[pole /. toBeta$] - softPole$, 0 < b < 1 && MM > 0],
    ";  at b = 0.3, 0.9, 0.999: ", N[Table[Re[pole /. {m -> 1, MM -> 4/(1 - bv^2)}] - (softPole$ /. b -> bv), {bv, {3/10, 9/10, 999/1000}}], 20]]],
  {s, {"MS", "OS"}}];

(* ::Section:: *)
(*Soft real emission in d dimensions (the same eikonal integrals as for the Z)*)

nint$[f_] := NIntegrate[f[x], {x, -1, 0, 1}, WorkingPrecision -> 40, PrecisionGoal -> 25, MaxRecursion -> 40];
ang$[bv_] := Module[{f12 = Function[x, (1 + bv^2)/((1 - bv x) (1 + bv x))], f11 = Function[x, (1 - bv^2)/(1 - bv x)^2]},
   {2 nint$[f12] - 2 nint$[f11], 2 nint$[Log[1 - #^2] f12[#] &] - 2 nint$[Log[1 - #^2] f11[#] &]}];
kS$[{s0_, s1_}, dE_] := -s0/(4 Epsilon) - (s0 (Log[ScaleMu^2/(Pi dE^2)] - EulerGamma) - s1)/4;
Print["-Sigma0/4 + soft pole at b = 0.3 (expect 0): ", N[-ang$[3/10][[1]]/4 + (softPole$ /. b -> 3/10), 20]];

(* ::Section:: *)
(*K_V + K_S for the channels*)

massesMV$ = {"MH" -> 12520/100, "MB" -> 478/100, "MC" -> 167/100, "MTA" -> 177693/100000, "MMU" -> 1056584/10000000};
mass$[k_] := k /. massesMV$;
deltas$ = {10^-4, 10^-5, 10^-6, 10^-7, 10^-8};
(* name, m, M; the tests: the massless limit (m/M = 1e-3, 1e-5) and the threshold (b = 0.05, 0.01) *)
chan$ = {{"H_b", mass$["MB"], mass$["MH"]}, {"H_c", mass$["MC"], mass$["MH"]}, {"H_ta", mass$["MTA"], mass$["MH"]},
   {"H_mu", mass$["MMU"], mass$["MH"]}, {"H_m1e-3", 1/1000, 1}, {"H_m1e-5", 1/100000, 1},
   {"H_b0.05", Sqrt[1 - (5/100)^2]/2, 1}, {"H_b0.01", Sqrt[1 - (1/100)^2]/2, 1}};
vs$[s_, mv_, Mv_, dl_, muList_] := Module[{bv = Sqrt[1 - 4 mv^2/Mv^2], emax = (Mv^2 - 4 mv^2)/(2 Mv), tot},
   tot = (kV$[s] + kS$[ang$[bv], dl emax]) /. {m -> mv, MM -> Mv^2};
   Join[{N[Re[Coefficient[tot, Epsilon, -1]], 20]}, N[Re[(tot /. Epsilon -> Infinity) /. ScaleMu -> 2 Pi #], 25] & /@ muList]];
tick$["soft"];
rowsMV$ = {};
Do[Module[{mv = c[[2]], Mv = c[[3]]},
   Do[Module[{os = vs$["OS", mv, Mv, dl, {7, 300}], ms = vs$["MS", mv, Mv, dl, {Mv}]},
      If[dl == deltas$[[1]],
       Print[c[[1]], ": pole of K_V + K_S: OS ", CForm[N[os[[1]], 3]], ", MS ", CForm[N[ms[[1]], 3]],
        ";  OS mu = 7 minus mu = 300: ", CForm[N[os[[2]] - os[[3]], 3]], ";  K_V + K_S at delta = 1e-4: OS ", CForm[N[os[[2]], 12]],
        ";  MS(mu = M) - OS - (2 + (3/2) ln(M^2/m^2)): ", CForm[N[ms[[2]] - os[[2]] - (2 + 3/2 Log[Mv^2/mv^2]), 3]]]];
      AppendTo[rowsMV$, {c[[1]], N[dl], ToString[CForm[N[os[[2]], 20]]]}]], {dl, deltas$}]], {c, chan$}];
Export[FileNameJoin[{resDirMV$, "hqq_massive_vs.csv"}], Prepend[rowsMV$, {"channel", "delta", "KV_plus_KS_OS"}], "CSV"];

(* ::Section:: *)
(*The MS-bar virtual alone in MadLoop's normalization at the CKM note's MadLoop point*)

tick$["channels"];
(* strip (4 pi)^eps Gamma(1 + eps): ScaleMu^2 -> pi e^gamma_E mu_R^2 removes gamma_E and ln(4 pi) with the poles; the MS-bar
   counterterm's -gamma_E + ln 4 pi go with it *)
msML$[x_, muR_] := Module[{y = Expand[x /. ScaleMu -> Sqrt[Pi Exp[EulerGamma]] muR]},
   {Coefficient[y, Epsilon, -1], y /. Epsilon -> Infinity}];
(* in this normalization the MS-bar counterterm is the pure pole -(3/2)/eps: its -gamma_E + ln 4 pi belong to the stripped
   (4 pi)^eps e^(-gamma eps), which the substitution of ScaleMu removes from the loop functions only *)
kVml$ = kVertZ$ - (3/2)/Epsilon;
mlRows$ = {};
(* the same K (abelian) for the photonic part of the leptons in step (5): tau, mu at the point's masses *)
Do[Module[{z = msML$[kVml$, muR] /. {m -> c[[2]], MM -> 125^2}},
   Print["MadLoop point (M_H = 125, m = ", N[c[[2]]], "), mu_R = ", muR, ":  ", c[[1]], "  K_V (MS-bar) pole ", N[Re[z[[1]]], 15],
    ", finite ", N[Re[z[[2]]], 15]];
   AppendTo[mlRows$, {c[[1]], muR, ToString[CForm[N[Re[z[[1]]], 20]]], ToString[CForm[N[Re[z[[2]]], 20]]]}]],
  {c, {{"h_bb", 286/100}, {"h_tata", 1746/1000}, {"h_mumu", 1027/10000}}}, {muR, {125, 500}}];
Export[FileNameJoin[{resDirMV$, "hqq_massive_virtual_ml.csv"}], Prepend[mlRows$, {"process", "mu_R", "KV_pole", "KV_finite"}], "CSV"];
Print["written: results/hqq_massive_vs.csv, results/hqq_massive_virtual_ml.csv"];
