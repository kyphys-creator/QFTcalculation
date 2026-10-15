(* ::Package:: *)

(* ::Title:: *)
(*Step (8): e+ e- -> hadrons at O(alpha_s) in D dimensions -- virtual and real corrections, their sum, the thrust distribution (FeynArts + FeynCalc, Package-X, LoopTools)*)


(* ::Text:: *)
(*Research note models/qcd, step (8).  R = sigma(e+ e- -> hadrons)/sigma(e+ e- -> mu+ mu-) for massless quarks; after the average over the*)
(*lepton directions only -g_{mu nu} H^{mu nu} of the hadronic tensor enters (current conservation), and the ratio to the D-dimensional Born*)
(*is  R/R_0 = 1 + r_V + r_R  (Eq. (rr)), a = g^2/K, MS-bar measure, mu^2 = s:*)
(*  r_V = 2 Re F^(1)(s + i0),  F^(1) = C_F a [(D-7) B0(s) - 2 s C0(s)] = -C_F a (2 - eps + 2 eps^2)/eps B0(s)  (C0 = -2 (D-3)/((D-4) s) B0, IBP),*)
(*  r_R = C_F a E^(eps gamma_E)/Gamma(1-eps) Int dy13 dy23 (y12 y13 y23)^(-eps) (-g H_3)/(-g H_2/s)   (three-body phase space / two-body, y_ij = s_ij/s).*)
(*(a) -g_{mu nu} H^{mu nu} of q qbar and q qbar g in D dimensions (FeynCalc traces; gluon polarization sum -g, allowed for one gluon and a*)
(*    colour-singlet current); D = 4 against Eq. (19) (eq:sumtree, (D)).  The Dalitz integrals are Dirichlet integrals, exact in eps.*)
(*(b) the one-loop q qbar gamma vertex from FeynArts (the gluon diagram; general xi), the interference with the tree current, TID: F^(1) in*)
(*    terms of B0 and C0, xi-independent; the IBP relation checked with Package-X; F^(1) at s = mu^2 with Package-X and LoopTools.*)
(*(c) the sum: poles cancel, R/R_0 = 1 + 3 C_F a (= 1 + alpha_s/pi in SU(3)).*)
(*(d) the thrust T = max x_i: (1/sigma_0) dsigma/dT from Eq. (19), against the closed form (eq:thrust); its integral from 2/3 to 1 - y is the*)
(*    three-jet fraction F(y) of Eq. (sigtree) (T < 1 - y is the same as s_ij > y s for all pairs).  -> results/ee_feyncalc.csv*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file ee_feyncalc.wl  (after generate_QCD.wl; about 1 minute).  Interactive:  ~/hep/bin/wopen ee_feyncalc.wl, then "Run All Code"; the cells under "Inspect" headings run only in the notebook.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirEE$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirEE$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirEE$, "generated", "QCD_FA"}], FileNameJoin[{modelTmpDirEE$, "QCD_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirEE$, "QCD_FA"}], Quiet -> True];
modelEE$ = FileNameJoin[{modelTmpDirEE$, "QCD_FA", "QCD_FA"}];
ep = Epsilon;
gEE$[a_, b_] := Gamma[a + b - D/2] Gamma[D/2 - a] Gamma[D/2 - b]/(Gamma[a] Gamma[b] Gamma[D - a - b]);


(* ::Section:: *)
(*(a) the hadronic tensors and the real correction*)


(* ::Text:: *)
(*gamma*(q) -> q(p1) qbar(p2) [g(p3)], massless, colour factor C_F N stripped; the conjugate amplitude is the reversed chain.*)


FCClearScalarProducts[];
SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[p3, p3] = 0; SPD[p1, p2] = s12/2; SPD[p1, p3] = s13/2; SPD[p2, p3] = s23/2;
curEE$ = GAD[nu].(GSD[p1] + GSD[p3]).GAD[mu]/s13 - GAD[mu].(GSD[p2] + GSD[p3]).GAD[nu]/s23;
curCEE$ = GAD[mu2].(GSD[p1] + GSD[p3]).GAD[nu2]/s13 - GAD[nu2].(GSD[p2] + GSD[p3]).GAD[mu2]/s23;
h3EE$ = Factor[Contract[DiracSimplify[DiracTrace[GSD[p1].curEE$.GSD[p2].curCEE$]] MTD[mu, mu2] MTD[nu, nu2]] /. s12 -> s - s13 - s23];
h2EE$ = Factor[-Contract[DiracSimplify[DiracTrace[GSD[p1].GAD[mu].GSD[p2].GAD[mu2]]] MTD[mu, mu2]] /. s12 -> s];
Print["(a) -g H_2/N = ", InputForm[h2EE$], ";  -g H_3/(C_F N) = ", InputForm[h3EE$]];
x3EE$ = Simplify[(h3EE$/(h2EE$/s)) /. {s13 -> s (1 - x2), s23 -> s (1 - x1)} /. D -> 4];
Print["(a) D = 4 ratio minus 8 (x1^2 + x2^2)/((1 - x1)(1 - x2)) /2 ... : ", Simplify[x3EE$ - 2 (x1^2 + x2^2)/((1 - x1) (1 - x2))], "  (expect 0: Eq. (19) (D) with C_F alpha_s/(2 pi) = 2 C_F a)"];
(* Dirichlet integrals over the simplex y12 + y13 + y23 = 1 *)
dirEE$[a_, b_, c_] := Gamma[a] Gamma[b] Gamma[c]/Gamma[a + b + c];
realEE$ = Module[{e = Expand[(h3EE$/(h2EE$/s)) /. {s13 -> y13, s23 -> y23} /. s -> 1], cr},
   cr = CoefficientRules[Expand[e y13 y23], {y13, y23}];
   E^(ep EulerGamma)/Gamma[1 - ep] Total[(#[[2]] dirEE$[#[[1, 1]] - ep, #[[1, 2]] - ep, 1 - ep]) & /@ cr] /. D -> 4 - 2 ep];
realEE$ = FullSimplify[realEE$];
realSerEE$ = Collect[FullSimplify[Normal[Series[realEE$, {ep, 0, 1}]]], ep];
Print["(a) r_R/(C_F a) exact = ", InputForm[realEE$]];
Print["(a) r_R/(C_F a) = ", InputForm[realSerEE$]];


(* ::Subsubsection:: *)
(*Inspect: the D-dimensional real matrix element and r_R*)


If[$Notebooks, TableForm[{{"-g H_3/(C_F N)", TraditionalForm[h3EE$]}, {"r_R/(C_F a)", TraditionalForm[realEE$]}}]]


(* ::Section:: *)
(*(b) the virtual correction*)


topsEE$ = CreateTopologies[1, 2 -> 1, ExcludeTopologies -> {Tadpoles, WFCorrections}];
insEE$ = InsertFields[topsEE$, {F[2], -F[2]} -> {V[1]}, InsertionLevel -> {Particles}, Model -> modelEE$, GenericModel -> modelEE$,
   ExcludeParticles -> {F[1], F[3], F[4], F[5], F[6], F[7]}];


(* ::Subsubsection:: *)
(*Inspect: the vertex diagrams (gluon and photon exchange; only the gluon one is kept)*)


If[$Notebooks, Show[#, ImageSize -> 360] & /@ Render[Paint[insEE$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]]]


ampsEE$ = FCFAConvert[CreateFeynAmp[insEE$, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
    IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {q}, LoopMomenta -> {l}, LorentzIndexNames -> {mu}, ChangeDimension -> D,
    List -> True, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI //
   ReplaceAll[#, {SMP["g_s"] -> gS, FCGV["GS"] -> gS, GaugeXi[V[2, ___]] -> xi, GaugeXi[G] -> xi, SMP["e"] -> 1, FCGV["EL"] -> 1}] &;
ampGEE$ = Select[ampsEE$, !FreeQ[#, gS] &];
Print["(b) vertex diagrams: ", Length[ampsEE$], ", with a gluon: ", Length[ampGEE$]];
FCClearScalarProducts[];
SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[p1, p2] = s/2; SPD[q, q] = s; SPD[p1, q] = s/2; SPD[p2, q] = s/2;
numEE$ = SUNSimplify[DiracSimplify[DiracTrace[GSD[p2].Total[ampGEE$].GSD[p1].GAD[mu]]], SUNNToCACF -> True] /. {SUNFDelta[__] -> 1, SUNDelta[__] -> 1, SDF[__] -> 1};
denEE$ = DiracSimplify[DiracTrace[GSD[p2].((2 I/3) GAD[mu]).GSD[p1].GAD[mu]]];
(* TID: int d^Dl -> I Pi^2 PaVe; V = A/(2 Pi)^D, g^2 int d^Dl/(2 Pi)^D -> I a J: F^(1) = (ratio)/(gS^2 Pi^2) x a in the PaVe normalization *)
fEE$ = Collect[Simplify[PaVeReduce[TID[numEE$, l, ToPaVe -> True]]/denEE$/(gS^2 Pi^2)], {PaVe[__], B0[__], C0[__]}, Simplify];
Print["(b) F^(1)/a = ", InputForm[fEE$], ";  d/dxi = ", Simplify[D[fEE$, xi]], "  (expect C_F[(D-7) B0 - 2 s C0], 0)"];
(* exact massless B0 and C0 in the MS-bar normalization (mu = 1), at s = -1 (Euclidean): B0 = E^(eps gamma) G(1,1),
   C0 = -E^(eps gamma) Gamma(1+eps) Gamma(1-eps)^2/(eps^2 Gamma(1-2eps)); checked against Package-X and LoopTools (Laurent
   coefficients), and the IBP relation C0 = -2 (D-3)/((D-4) s) B0 holds exactly between them *)
pxEE$[x_] := Normal[Series[(2 Pi)^(2 ep) Exp[-ep (Log[4 Pi] - EulerGamma)] (PaXEvaluate[x /. D -> 4 - 2 ep, PaXC0Expand -> True] /. ScaleMu -> 1), {ep, 0, 0}]];
ltEE$[x_] := Normal[Series[(2 Pi)^(2 ep) Exp[-ep (Log[4 Pi] - EulerGamma)] LToolsEvaluate[x /. D -> 4 - 2 ep, LToolsFullResult -> True], {ep, 0, 0}]];
b0xEE$ = E^(ep EulerGamma) gEE$[1, 1] /. D -> 4 - 2 ep;
c0xEE$ = -E^(ep EulerGamma) Gamma[1 + ep] Gamma[1 - ep]^2/(ep^2 Gamma[1 - 2 ep]);
devPaVeEE$ = Chop[N[Flatten[{CoefficientList[ep^2 (pxEE$[PaVe[0, {-1}, {0, 0}]] - Normal[Series[b0xEE$, {ep, 0, 0}]]), ep],
      CoefficientList[ep^2 (pxEE$[PaVe[0, {0, 0, -1}, {0, 0, 0}]] - Normal[Series[c0xEE$, {ep, 0, 0}]]), ep],
      CoefficientList[ep^2 (ltEE$[PaVe[0, {-1}, {0, 0}]] - Normal[Series[b0xEE$, {ep, 0, 0}]]), ep],
      CoefficientList[ep^2 (ltEE$[PaVe[0, {0, 0, -1}, {0, 0, 0}]] - Normal[Series[c0xEE$, {ep, 0, 0}]]), ep]}]], 10^-13];
Print["(b) exact B0, C0 (s = -1) minus Package-X and LoopTools, all Laurent coefficients: max ", Max[Abs[devPaVeEE$]], "  (expect ~1e-15)"];
Print["(b) IBP: C0 + 2 (D-3)/((D-4) s) B0 with the exact forms at s = -1: ", FullSimplify[c0xEE$ + 2 (D - 3)/((D - 4) (-1)) b0xEE$ /. D -> 4 - 2 ep], "  (expect 0)"];
(* exact: B0(s) = E^(eps gamma) G(1,1) (-s - i0)^(-eps), mu = 1 *)
fExactEE$ = -CF (2 - ep + 2 ep^2)/ep E^(ep EulerGamma) gEE$[1, 1] /. D -> 4 - 2 ep;    (* times (-s - i0)^(-eps) *)
fSerEE$ = Collect[FullSimplify[Normal[Series[fExactEE$, {ep, 0, 0}]]], ep];
Print["(b) F^(1)/(a C_F) at -s = mu^2 (Euclidean): ", InputForm[fSerEE$/CF]];
(* numbers at s = mu^2 = 1 (+i0): Package-X and LoopTools *)
fPXEE$ = Chop[N[pxEE$[fEE$ /. xi -> 1 /. s -> 1 /. CF -> 4/3]]];
fLTEE$ = Chop[N[ltEE$[fEE$ /. xi -> 1 /. s -> 1 /. CF -> 4/3]]];
fExNumEE$ = Chop[N[Normal[Series[fExactEE$ Exp[I Pi ep] /. CF -> 4/3, {ep, 0, 0}]]]];
Print["(b) F^(1)/a at s = mu^2 = 1 (+i0), SU(3): exact ", fExNumEE$, ";  Package-X - exact ", Chop[Expand[fPXEE$ - fExNumEE$], 10^-12],
  ";  LoopTools - exact ", Chop[Expand[fLTEE$ - fExNumEE$], 10^-12]];


(* ::Section:: *)
(*(c) the sum*)


virtEE$ = 2 fExactEE$ Cos[Pi ep]/CF;       (* (-s - i0)^(-eps) = e^(i pi eps) at s = mu^2; the Euclidean F is real for real eps *)
virtSerEE$ = Collect[FullSimplify[Normal[Series[virtEE$, {ep, 0, 0}]]], ep];
sumEE$ = FullSimplify[Normal[Series[virtEE$ + realEE$, {ep, 0, 0}]]];
Print["(c) r_V/(C_F a) = ", InputForm[virtSerEE$], ";  r_R/(C_F a) = ", InputForm[Normal[Series[realEE$, {ep, 0, 0}]]], ";  sum = ", sumEE$, "  (expect 3)"];


(* ::Section:: *)
(*(d) the thrust distribution*)


(* ::Text:: *)
(*(1/sigma_0) d sigma/dx1 dx2 = 2 C_F a f(x1, x2), f = (x1^2 + x2^2)/((1-x1)(1-x2)) (D = 4).  T = max(x1, x2, x3), x3 = 2 - x1 - x2:*)
(*T = x1 (x2 from 2 - 2T to T), T = x2 (the same by symmetry), T = x3 (x1 from 1 - T... with x1, x2 <= T).*)


fxEE$[x1_, x2_] := (x1^2 + x2^2)/((1 - x1) (1 - x2));
thrustEE$[t_] = Simplify[2 Integrate[fxEE$[t, x2], {x2, 2 - 2 t, t}, Assumptions -> 2/3 < t < 1] +
     Integrate[fxEE$[x1, 2 - t - x1], {x1, 2 - 2 t, t}, Assumptions -> 2/3 < t < 1], 2/3 < t < 1];
closedEE$[t_] := 2 (3 t^2 - 3 t + 2)/(t (1 - t)) Log[(2 t - 1)/(1 - t)] - 3 (3 t - 2) (2 - t)/(1 - t);
Print["(d) thrust: integral of Eq. (19) minus the closed form (in units of 2 C_F a = C_F alpha_s/(2 pi)): ",
  FullSimplify[thrustEE$[t] - closedEE$[t], 2/3 < t < 1], "  (expect 0);  at T = 0.9: ", N[{thrustEE$[9/10], closedEE$[9/10]}]];
(* the three-jet fraction F(y) of Eq. (sigtree): sigma_D(y)/sigma_0 = C_F alpha_s/(2 pi) F(y), s_ij > y s for all pairs <=> T < 1 - y *)
fyEE$[y_] := (3 - 6 y) Log[y/(1 - 2 y)] + 2 Log[y/(1 - y)]^2 + 5/2 - 6 y - 9/2 y^2 + 4 PolyLog[2, y/(1 - y)] - Pi^2/3;
Print["(d) Int_{2/3}^{1-y} dT (thrust) - F(y) at y = 0.1, 0.01, 0.001: ",
  Table[Chop[N[NIntegrate[closedEE$[t], {t, 2/3, 1 - y}, WorkingPrecision -> 30, PrecisionGoal -> 20] - fyEE$[y], 25]], {y, {1/10, 1/100, 1/1000}}], "  (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: the thrust distribution*)


If[$Notebooks, Plot[closedEE$[t], {t, 2/3, 0.99}, AxesLabel -> {"T", "(1/sigma0) dsigma/dT / (C_F alpha_s/2pi)"}, PlotRange -> All]]


(* ::Section:: *)
(*Results*)


strEE$[x_] := ToString[CForm[N[x, 17]]];
rowsEE$ = {{"rV_over_CFa", Sequence @@ (strEE$ /@ Table[Coefficient[virtSerEE$, ep, k], {k, -2, 0}])},
   {"rR_over_CFa", Sequence @@ (strEE$ /@ Table[Coefficient[Normal[Series[realEE$, {ep, 0, 0}]], ep, k], {k, -2, 0}])},
   {"sum_over_CFa", "0", "0", strEE$[sumEE$]},
   {"F1_px_minus_exact_re", strEE$[Max[Abs[Re[CoefficientList[Expand[ep^2 (fPXEE$ - fExNumEE$)], ep]]]]], "", ""},
   {"F1_lt_minus_exact_re", strEE$[Max[Abs[CoefficientList[Expand[ep^2 (fLTEE$ - fExNumEE$)], ep]]]], "", ""}};
Export[FileNameJoin[{srcDirEE$, "results", "ee_feyncalc.csv"}],
  StringRiffle[Prepend[StringRiffle[#, ","] & /@ rowsEE$, "quantity,eps-2,eps-1,eps0"], "\n"] <> "\n", "Text"];
Print["(e) wrote results/ee_feyncalc.csv"];


(* ::Section:: *)
(*Cleanup*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirEE$, DeleteContents -> True];
