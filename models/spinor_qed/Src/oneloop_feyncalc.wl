(* ::Package:: *)

(* ::Title:: *)
(*Step (3): one-loop 1PI functions of spinor QED in a general covariant gauge (FeynArts + FeynCalc, Package-X, LoopTools)*)


(* ::Text:: *)
(*Research note models/spinor_qed, step (3).*)
(*(a) FeynArts 1PI diagrams from Src/generated/SpinorQED_FA with GaugeRules -> {} (keeps the gauge parameter xi = GaugeXi[A]):*)
(*    photon 1-point (2: e and mu loops, must vanish), photon 2-point (2), electron and muon self-energies (1 each),*)
(*    e e gamma vertex (1), photon 3-point (4 = 2 orientations x 2 flavours, sum must vanish: Furry),*)
(*    photon 4-point (12 = 6 orderings x 2 flavours, the UV pole of the sum must vanish).  With PreFactor -> 1 the*)
(*    amplitude is A = (2 Pi)^D V (V = the 1PI function with the i's of the Feynman rules) and FeynCalc's TID writes*)
(*    A = I Pi^2 X with X built from PaVe functions.  The note, Eq. (5) (eq:V), predicts*)
(*      photon:  V = i Pi^{mu nu},   X = K Pi^{mu nu} = (q^2 g - q q) e^2 2/((D-1) q^2) [2 (D-2) A0 - (4 m^2 + (D-2) q^2) B0]*)
(*      fermion: V = -i Sigma,       X = -K Sigma = -e^2 [xi (D-2) pslash B1(p^2; m^2, 0) + (D-1+xi) m B0(p^2; m^2, 0)]*)
(*      vertex:  V = i e Q Lambda,   X = -e K Lambda   (Q = -1);  on shell ubar Lambda u = ubar [g F1 + i s q/(2m) F2] u*)
(*    (K = (4 Pi)^2).  TID writes the doubled photon propagator of the xi part of Sigma as C0(0, p^2, p^2; 0, 0, m^2);*)
(*    the note's IBP relation (App. D) J12 = [(D-2) A0 - (D-3)(m^2+p^2) B0]/(m^2-p^2)^2 replaces it, and is checked*)
(*    separately (pole and finite part) with Package-X and LoopTools.*)
(*(b) UV poles and the MS-bar counterterms of Eq. (6) (eq:ct); delta1 = delta2 (the vertex pole at zero external momenta).*)
(*(c) Ward identities: transversality of Pi; the Ward-Takahashi identity q.Lambda(p+q, p) = Sigma(p) - Sigma(p+q) at the*)
(*    integrand level for any xi (the Dirac identity of App. C) and integrated in Feynman gauge at off-shell points;*)
(*    the on-shell vertex does not depend on xi; R_f F1^R(0) = 1 (App. F) with the O(eps) x IR-pole terms.*)
(*(d) MS-bar finite parts (and the IR poles) at e = 1, m_e = mu = 1, m_mu = 1.7 from Package-X and LoopTools*)
(*    -> results/oneloop_mathematica.csv (oneloop_numeric.py compares them with COLLIER and the Feynman-parameter*)
(*    integrals of the note).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_feyncalc.wl  (run generate_SpinorQED.wl first).  Interactive:  ~/hep/bin/wopen oneloop_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirOL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

modelTmpDirOL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOL$, "generated", "SpinorQED_FA"}], FileNameJoin[{modelTmpDirOL$, "SpinorQED_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOL$, "SpinorQED_FA"}], Quiet -> True];
modelOL$ = FileNameJoin[{modelTmpDirOL$, "SpinorQED_FA", "SpinorQED_FA"}];
insertOL$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles},
   Model -> modelOL$, GenericModel -> modelOL$];
xiOL$ = GaugeXi[A];
KK = (4 Pi)^2;


(* ::Section:: *)
(*(a) diagrams*)


diag1$ = insertOL$[CreateTopologies[1, 1 -> 0], {V[1]} -> {}];
diagPi$ = insertOL$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {V[1]} -> {V[1]}];
diagSe$ = insertOL$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {F[1]} -> {F[1]}];
diagSm$ = insertOL$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {F[2]} -> {F[2]}];
diagV$ = insertOL$[CreateTopologies[1, 2 -> 1, ExcludeTopologies -> {Tadpoles, WFCorrections}], {F[1], V[1]} -> {F[1]}];
diag3$ = insertOL$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], {V[1]} -> {V[1], V[1]}];
diag4$ = insertOL$[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections, Reducible}],
   {V[1], V[1]} -> {V[1], V[1]}];


(* ::Subsubsection:: *)
(*Inspect: the 1PI diagrams (photon 1-point, photon 2-point, e and mu self-energies, vertex, photon 3-point, photon 4-point)*)


If[$Notebooks,
  {Show[#, ImageSize -> 360] & /@ Render[Paint[diag1$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 360] & /@ Render[Paint[diagPi$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 180] & /@ Render[Paint[diagSe$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 180] & /@ Render[Paint[diagSm$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 180] & /@ Render[Paint[diagV$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 560] & /@ Render[Paint[diag3$, ColumnsXRows -> {4, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 560] & /@ Render[Paint[diag4$, ColumnsXRows -> {4, 3}, Numbering -> Simple, DisplayFunction -> Identity]]}
]


Print["(a) number of 1PI diagrams (expect 2, 2, 1, 1, 1, 4, 12): ",
  Length[CreateFeynAmp[#]] & /@ {diag1$, diagPi$, diagSe$, diagSm$, diagV$, diag3$, diag4$}];


(* ::Section:: *)
(*(a) amplitudes*)


(* ::Text:: *)
(*M$FACouplings (gc1, gc2 -> -EL) is applied by hand, FCGV["EL"] -> EL.  CreateFeynAmp's GaugeRules -> {} keeps*)
(*GaugeXi[A] in the photon propagator.  rawOL$ keeps the unreduced integrand; reduceOL$ applies TID.*)


rawOL$[diags_, in_, out_, lor_] := FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
   IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {l}, LorentzIndexNames -> lor, ChangeDimension -> D,
   List -> False, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI // MomentumExpand // ReplaceAll[#, FCGV["EL"] -> EL] &;
reduceOL$[x_] := FCE[DiracSimplify[FeynAmpDenominatorExplicit[TID[DiracSimplify[x], l, ToPaVe -> True]]]];
(* IBP relation for the doubled massless propagator (note App. D), in FeynCalc's PaVe notation *)
ibpOL$ = {PaVe[0, {0, pp_, pp_}, {0, 0, m2_}] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2,
   C0[0, pp_, pp_, 0, 0, m2_] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2};
canonB$ = {B0[x_, 0, m2_] :> B0[x, m2, 0]};
diffOL$[a_, h_] := Simplify[FCE[DiracSimplify[PaVeReduce[FCI[a - h]] /. canonB$]]];

FCClearScalarProducts[];
raw1$ = rawOL$[diag1$, {q}, {}, {mu}];
amp1$ = reduceOL$[raw1$];

ScalarProduct[q, q] = qq;
rawPi$ = rawOL$[diagPi$, {q}, {q}, {mu, nu}];
ampPi$ = reduceOL$[rawPi$];
FCClearScalarProducts[];
ScalarProduct[p, p] = pp;
rawSe$ = rawOL$[diagSe$, {p}, {p}, {mu}];
ampSe$ = reduceOL$[rawSe$] /. ibpOL$ /. SPD[p, p] -> pp;
rawSm$ = rawOL$[diagSm$, {p}, {p}, {mu}];
ampSm$ = reduceOL$[rawSm$] /. ibpOL$ /. SPD[p, p] -> pp;
FCClearScalarProducts[];


(* ::Subsubsection:: *)
(*Inspect: the reduced photon and fermion two-point amplitudes*)


If[$Notebooks,
  TableForm[{{"photon 1-point", TraditionalForm[amp1$]}, {"photon 2-point A", TraditionalForm[Collect[ampPi$, {Me, MMU}]]},
    {"electron A (after IBP)", TraditionalForm[ampSe$]}}]
]


(* ::Text:: *)
(*Comparison with Eq. (5) times (2 Pi)^D:  A = I Pi^2 X.  Pi_f is summed over f = e, mu.  The fermion momentum p is*)
(*incoming; FeynArts writes the e-propagator mass as Me (MMU for the muon).*)


xPi$[m_] := EL^2 2/((D - 1) qq) (2 (D - 2) A0[m^2] - (4 m^2 + (D - 2) qq) B0[qq, m^2, m^2]);
handPi$ = I Pi^2 (qq MTD[mu, nu] - FVD[q, mu] FVD[q, nu]) (xPi$[Me] + xPi$[MMU]);
handS$[m_] := -I Pi^2 EL^2 (xiOL$ (D - 2) GSD[p] PaVe[1, {pp}, {m^2, 0}] + (D - 1 + xiOL$) m B0[pp, m^2, 0]);
Print["(a) photon 1-point function (expect 0): ", amp1$];
ScalarProduct[p, p] = pp;
Print["(a) A_photon - I Pi^2 (q^2 g - q q) sum_f X_Pi_f, Eq. (5) = ", diffOL$[ampPi$, handPi$], "  (expect 0)"];
Print["(a) A_e - Eq. (5) Sigma (general xi) = ", diffOL$[ampSe$, handS$[Me]], ",  A_mu - Eq. (5) = ", diffOL$[ampSm$, handS$[MMU]], "  (expect 0, 0)"];
FCClearScalarProducts[];


(* ::Text:: *)
(*The vertex: electron in p, photon in q (index mu), electron out p1 = p + q.  ScalarProducts on shell: p^2 = p1^2 = m^2,*)
(*p.p1 = m^2 - q^2/2.  Between on-shell spinors the result is ubar(p1) [g^mu G1 + p^mu Gp + p1^mu Gp1] u(p).*)


rawV$ = rawOL$[diagV$, {p, q}, {p1}, {mu}] /. Momentum[q, D] -> Momentum[p1, D] - Momentum[p, D];
FCClearScalarProducts[];
ScalarProduct[p, p] = Me^2; ScalarProduct[p1, p1] = Me^2; ScalarProduct[p, p1] = Me^2 - qq/2;
chainV$ = SpinorUBarD[p1, Me] . rawV$ . SpinorUD[p, Me];
ampVos$ = FCE[DiracSimplify[TID[DiracSimplify[chainV$], l, ToPaVe -> True]]];
xVos$ = Expand[ampVos$/(I Pi^2) /. {Spinor[Momentum[p1, D], Me, 1] . GAD[mu] . Spinor[Momentum[p, D], Me, 1] -> sG,
      Spinor[Momentum[p1, D], Me, 1] . Spinor[Momentum[p, D], Me, 1] -> sOne}];
gV1$ = Coefficient[xVos$, sG]; gVp$ = Coefficient[Coefficient[xVos$, sOne], FVD[p, mu]];
gVp1$ = Coefficient[Coefficient[xVos$, sOne], FVD[p1, mu]];
Print["(a) on-shell vertex: decomposition complete (expect 0): ",
  Simplify[xVos$ - gV1$ sG - sOne (gVp$ FVD[p, mu] + gVp1$ FVD[p1, mu])],
  ";  q^mu term Gp1 - Gp (expect 0): ", Simplify[PaVeReduce[gVp1$ - gVp$]], ";  d/dxi (expect 0): ", Simplify[D[xVos$, xiOL$]]];
(* Lambda = -X/(e K) with e = EL;  (p + p1)^mu coefficient G2 = Gp;  F2 = -2 m G2, F1 = G1 + 2 m G2 *)
f1PV$ = Simplify[PaVeReduce[-(gV1$ + 2 Me gVp$)/EL]];       (* = K F1^Lambda / 1 *)
f2PV$ = Simplify[PaVeReduce[-(-2 Me gVp$)/EL]];             (* = K F2 *)
f1note$ = EL^2 (2 (D - 2) A0[Me^2] + 4 (2 Me^2 - qq) B0[Me^2, Me^2, 0] - (8 Me^2 + (D - 7) qq) B0[qq, Me^2, Me^2] +
      2 (2 Me^2 - qq) (4 Me^2 - qq) C0[Me^2, Me^2, qq, Me^2, 0, Me^2])/(4 Me^2 - qq);
f2note$ = -2 Me EL^2 ((D - 2) A0[Me^2]/(4 Me^3 - Me qq) - 4 Me B0[Me^2, Me^2, 0]/(4 Me^2 - qq) - 2 (D - 5) Me B0[qq, Me^2, Me^2]/(4 Me^2 - qq));
Print["(a) K F1^Lambda (D dims) - its PaVe form (App. H) = ", Simplify[PaVeReduce[f1PV$ - f1note$] /. canonB$],
  ",  K F2 - its PaVe form = ", Simplify[PaVeReduce[f2PV$ - f2note$] /. canonB$], "  (expect 0, 0)"];


(* ::Subsubsection:: *)
(*Inspect: the on-shell form factors (PaVe form, D dimensions)*)


If[$Notebooks,
  TableForm[{{"K F1^Lambda", TraditionalForm[f1PV$]}, {"K F2", TraditionalForm[f2PV$]}}]
]


(* ::Text:: *)
(*Photon 3-point (Furry): the sum of the four triangles vanishes.  Photon in q1 = k1 + k2 (index mu), out k1 (nu), k2 (rho).*)


FCClearScalarProducts[];
raw3$ = rawOL$[diag3$, {q1}, {k1, k2}, {mu, nu, rho}] /. Momentum[q1, D] -> Momentum[k1, D] + Momentum[k2, D];
ScalarProduct[k1, k1] = s1; ScalarProduct[k2, k2] = s2; ScalarProduct[k1, k2] = (s3 - s1 - s2)/2;
amp3$ = Simplify[PaVeOrder[PaVeReduce[reduceOL$[raw3$]]]];
FCClearScalarProducts[];
Print["(a) photon 3-point function, sum of the 4 triangles (Furry, expect 0): ", amp3$];


(* ::Text:: *)
(*Photon 4-point: the UV pole is independent of the external momenta, so it is taken at zero external momenta (vacuum*)
(*integrals, IR finite because the fermions are massive).  Each diagram has a pole; the sum per flavour must not.*)


raw4$ = FCFAConvert[CreateFeynAmp[diag4$, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
    IncomingMomenta -> {k1, k2}, OutgoingMomenta -> {k3, k4}, LoopMomenta -> {l}, LorentzIndexNames -> {mu, nu, rho, si},
    ChangeDimension -> D, List -> True, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI // MomentumExpand //
   ReplaceAll[#, FCGV["EL"] -> EL] &;
zeroMom4$ = {Momentum[k1, D] -> 0, Momentum[k2, D] -> 0, Momentum[k3, D] -> 0, Momentum[k4, D] -> 0};
uv4$ = Simplify[PaVeUVPart[reduceOL$[#], Prefactor -> 1] /. D -> 4 - 2 eps] & /@ (MomentumExpand[#] /. zeroMom4$ & /@ raw4$);
uv4$ = Normal[Series[# eps, {eps, 0, 0}]] & /@ uv4$;
Print["(a) photon 4-point: UV pole (eps x A/(I Pi^2)) of diagram 1 = ", Simplify[uv4$[[1]]/(I Pi^2)]];
Print["(a) number of diagrams with a non-zero UV pole: ", Count[uv4$, x_ /; Simplify[x] =!= 0],
  ";  sum over the 6 e diagrams, the 6 mu diagrams (expect 0, 0): ",
  Simplify[Total[Select[Transpose[{uv4$, raw4$}], FreeQ[#[[2]], MMU] &][[All, 1]]]],
  ", ", Simplify[Total[Select[Transpose[{uv4$, raw4$}], ! FreeQ[#[[2]], MMU] &][[All, 1]]]]];


(* ::Section:: *)
(*(b) UV poles and MS-bar counterterms*)


(* ::Text:: *)
(*Pole of V = A/(2 Pi)^D: the 1/eps coefficient of A/(I Pi^2) (UV parts, PaVeUVPart; after the IBP relation every*)
(*remaining function is UV divergent only).  Counterterms, Eq. (6):  Pi - delta3 finite -> delta3 = pole(Pi);*)
(*Sigma = pslash a + m b,  delta2 = pole(a), delta2 + deltam = -pole(b);  vertex at zero external momenta: Lambda_div =*)
(*c gamma^mu, delta1 = -c.*)


uvOL$[x_] := Module[{y = PaVeUVPart[x, Prefactor -> 1] /. D -> 4 - 2 eps}, Simplify[Normal[Series[y eps, {eps, 0, 0}]]]];
poleXPi$ = uvOL$[Coefficient[Expand[ampPi$/(I Pi^2)] /. MTD[mu, nu] -> gmn, gmn]/qq];    (* K Pi pole *)
delta3$ = Simplify[poleXPi$/KK];
FCClearScalarProducts[]; ScalarProduct[p, p] = pp;
xSe$ = Expand[FCI[DiracSimplify[ampSe$]/(I Pi^2)]];
aSe$ = Coefficient[xSe$, DiracGamma[Momentum[p, D], D]]; bSe$ = Simplify[(xSe$ - aSe$ DiracGamma[Momentum[p, D], D])/Me];
(* Sigma = -X/K *)
delta2$ = Simplify[-uvOL$[aSe$]/KK]; deltam$ = Simplify[-(-uvOL$[bSe$]/KK) - delta2$];
FCClearScalarProducts[];
rawV0$ = rawV$ /. {Momentum[p, D] -> 0, Momentum[p1, D] -> 0};
xV0$ = Expand[FCI[DiracSimplify[reduceOL$[rawV0$]]]/(I Pi^2)];
Print["(b) vertex at zero external momenta is proportional to gamma^mu (expect True): ",
  FreeQ[Simplify[xV0$ - Coefficient[xV0$, DiracGamma[LorentzIndex[mu, D], D]] DiracGamma[LorentzIndex[mu, D], D]], DiracGamma]];
cV$ = Simplify[-uvOL$[Coefficient[xV0$, DiracGamma[LorentzIndex[mu, D], D]]]/(EL KK)];      (* Lambda = -X/(e K) *)
delta1$ = -cV$;
Print["(b) MS-bar counterterms / DeltaUV: delta3, delta2, deltam, delta1 = ", InputForm[{delta3$, delta2$, deltam$, delta1$}]];
Print["(b) minus the note, Eq. (6) (N_f = 2): ", Simplify[{delta3$, delta2$, deltam$, delta1$} -
     {-8 EL^2/(3 KK), -xiOL$ EL^2/KK, -3 EL^2/KK, -xiOL$ EL^2/KK}], "  (expect {0, 0, 0, 0});  delta1 - delta2 = ",
  Simplify[delta1$ - delta2$], ",  Z_e: delta_e = -delta3/2 = ", Simplify[-delta3$/2]];


(* ::Section:: *)
(*(c) Ward identities*)


(* ::Text:: *)
(*Transversality: q_mu X^{mu nu} = 0.  Ward-Takahashi at the integrand level: with S(k) = (kslash + m)/(k^2 - m^2),*)
(*(bslash + m)(bslash - aslash)(aslash + m) = (b^2 - m^2)(aslash + m) - (a^2 - m^2)(bslash + m), i.e.*)
(*S(b) (bslash - aslash) S(a) = S(a) - S(b) (App. C); the photon propagator D_{nu rho}(l) is a spectator, so this proves*)
(*q.Lambda = Sigma(p) - Sigma(p') for every xi.  Integrated: Feynman gauge, off-shell p^2, p'^2, q^2.*)


FCClearScalarProducts[]; ScalarProduct[q, q] = qq;
Print["(c) q_mu X^{mu nu} of the photon 2-point function (expect 0): ",
  Simplify[PaVeReduce[Contract[FVD[q, mu] ampPi$]]]];
FCClearScalarProducts[];
Print["(c) Dirac identity behind Ward-Takahashi, (b+m)(b-a)(a+m) - [(b^2-m^2)(a+m) - (a^2-m^2)(b+m)] = ",
  Simplify[ExpandScalarProduct[DiracSimplify[(GSD[b] + Me) . (GSD[b] - GSD[a]) . (GSD[a] + Me) -
       ((SPD[b, b] - Me^2) (GSD[a] + Me) - (SPD[a, a] - Me^2) (GSD[b] + Me))]]], "  (expect 0)"];
(* integrated, Feynman gauge: q.Lambda vs Sigma(p) - Sigma(p1), off shell; X_V = -e K Lambda, X_S = -K Sigma *)
FCClearScalarProducts[];
ScalarProduct[p, p] = pA; ScalarProduct[p1, p1] = pB; ScalarProduct[p, p1] = (pA + pB - qq)/2;
wtL$ = FCE[DiracSimplify[TID[DiracSimplify[Contract[(FVD[p1, mu] - FVD[p, mu]) (rawV$ /. xiOL$ -> 1)]], l, ToPaVe -> True]]];
sigOf$[mom_, mm2_] := handS$[Me] /. {GSD[p] -> GSD[mom], pp -> mm2} /. xiOL$ -> 1;
(* X_V(q.Lambda) = -e K q.Lambda = -e K [Sigma(p) - Sigma(p1)] = e [X_S(p) - X_S(p1)]   (X_S = -K Sigma) *)
wtDiff$ = Simplify[DiracSimplify[DiracOrder[PaVeReduce[wtL$/(I Pi^2) - EL (sigOf$[p, pA] - sigOf$[p1, pB])/(I Pi^2)] /. canonB$, {p, p1}]]];
Print["(c) Ward-Takahashi integrated (Feynman gauge, off shell): X(q.Lambda) - e [X(Sigma(p)) - X(Sigma(p'))] = ", wtDiff$, "  (expect 0)"];
FCClearScalarProducts[];


(* ::Section:: *)
(*(d) MS-bar finite parts and IR poles at e = 1, m_e = mu = 1, m_mu = 1.7*)


(* ::Text:: *)
(*Conversion to the note's MS-bar values (as in the earlier notes): V = A/(2 Pi)^D; the eps^0 coefficient of*)
(*(2 Pi)^(2 eps) A/(2 Pi)^4 minus its 1/eps coefficient times (Log[4 Pi] - EulerGamma).  The same convention applies to*)
(*the IR poles (DeltaIR = 1/eps - gamma_E + ln 4 pi).  msbarOL$ returns {pole, finite}.  The brackets are K/e^2 times the*)
(*note's Pi^R, Sigma_V, Sigma_S (MS-bar finite, counterterms subtracted), K F1^Lambda (total 1/eps coefficient and*)
(*finite part, UV and IR together), K F2.*)


msbarOL$[x_ /; PossibleZeroQ[x]] := {0, 0};     (* e.g. Sigma_V at xi = 0 *)
msbarOL$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   {SeriesCoefficient[v, -1], SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)}];
logRulesOL$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
PaXEvaluate[B0[2, 1, 1]];   (* loads Package-X *)
pxOL$[x_] := Chop[N[Simplify[msbarOL$[I Pi^2 Quiet[PaXEvaluate[x /. D -> 4 - 2 Epsilon], PaXEvaluate::tens] /. ScaleMu -> 1] KK/I /. logRulesOL$], 20], 10^-14];
ltOL$[x_] := Chop[N[msbarOL$[I Pi^2 Quiet[LToolsEvaluate[x /. D -> 4 - 2 Epsilon], LToolsEvaluate::tens]] KK/I], 10^-14];
coup$ = {EL -> 1, Me -> 1, MMU -> 17/10};
(* brackets as PaVe expressions in D dims (functions of the kinematic variable), from the FeynCalc amplitudes above *)
FCClearScalarProducts[];
bPi$[m_] := Coefficient[Expand[ampPi$/(I Pi^2)] /. MTD[mu, nu] -> gmn, gmn]/qq /. If[m === Me, MMU -> 0, Me -> 0] /.
   {A0[0] -> 0, B0[x_, 0, 0] -> 0};                                  (* K Pi_f / e^2 for one flavour *)
sigStruct$[amp_, m_] := Module[{x = Expand[FCI[amp/(I Pi^2)]], g = DiracGamma[Momentum[p, D], D], a},
   a = Coefficient[x, g]; {-a, -Simplify[(x - a g)/m]}];               (* K Sigma_V, K Sigma_S *)
{bSVe$, bSSe$} = sigStruct$[ampSe$, Me];
{bSVm$, bSSm$} = sigStruct$[ampSm$, MMU];
rowsOL$ = {};
addRow$[name_, a1_, a2_, x_, ct_] := Module[{px = pxOL$[x], lt = ltOL$[x]},
   AppendTo[rowsOL$, {name, a1, a2, px[[1]] - ct, px[[2]], lt[[1]] - ct, lt[[2]]}]];
(* photon: subtract delta3 per flavour (pole -4/3) -> pole column 0 *)
Do[addRow$["Pi_e", x, 0, bPi$[Me] /. coup$ /. qq -> x, -4/3];
   addRow$["Pi_mu", x, 0, bPi$[MMU] /. coup$ /. qq -> x, -4/3], {x, {-5, -1, 1/2, 2, 39/10, 6, 20}}];
Do[addRow$["SigV_e", x, xi, bSVe$ /. coup$ /. {pp -> x, xiOL$ -> xi}, -xi];
   addRow$["SigS_e", x, xi, bSSe$ /. coup$ /. {pp -> x, xiOL$ -> xi}, 3 + xi];
   addRow$["SigV_mu", x, xi, bSVm$ /. coup$ /. {pp -> x, xiOL$ -> xi}, -xi];
   addRow$["SigS_mu", x, xi, bSSm$ /. coup$ /. {pp -> x, xiOL$ -> xi}, 3 + xi],
  {x, {-5, 1/2, 2, 4, 10}}, {xi, {0, 1, 3}}];
(* vertex: total pole (UV + IR) kept, no counterterm *)
Do[addRow$["F1", x, 0, f1PV$ /. coup$ /. qq -> x, 0];
   addRow$["F2", x, 0, f2PV$ /. coup$ /. qq -> x, 0], {x, {-5, -1, 1/2, 2, 39/10, 6, 10}}];


(* ::Text:: *)
(*q^2 = 0: LoopTools returns Indeterminate for the IR-divergent C0(m^2, m^2, 0; m^2, 0, m^2); Package-X only.*)


With[{px0 = pxOL$[f1PV$ /. coup$ /. qq -> 0], px2 = pxOL$[f2PV$ /. coup$ /. qq -> 0]},
  AppendTo[rowsOL$, {"F1", 0, 0, px0[[1]], px0[[2]], Indeterminate, Indeterminate}];
  AppendTo[rowsOL$, {"F2", 0, 0, px2[[1]], px2[[2]], Indeterminate, Indeterminate}];
  Print["(d) Package-X at q^2 = 0: K F1^Lambda(0) {pole, finite} = ", px0, " (expect {3, 4} at m = mu: xi DUV + (3-xi) DIR + 4),  K F2(0) = ", px2, " (expect {0, 2}: alpha/2pi)"]];


(* ::Text:: *)
(*The IBP relation for the doubled massless propagator, checked numerically (pole and finite part) at p^2 = 1/2, 3, -2.*)


Do[Module[{lhs = PaVe[0, {0, x, x}, {0, 0, 1}], rhs},
    rhs = PaVe[0, {0, x, x}, {0, 0, 1}] /. ibpOL$;
    Print["(d) IBP for C0(0, p^2, p^2; 0, 0, m^2) at p^2 = ", x, ": Package-X lhs, rhs = ", pxOL$[lhs], ", ", pxOL$[rhs],
      ";  LoopTools lhs = ", ltOL$[lhs]]], {x, {1/2, 3, -2}}];


(* ::Text:: *)
(*Residue and the Ward identity R_f F1^R(0) = 1 (App. F).  R - 1 = Sigma_V + 2 m^2 (Sigma_V' + Sigma_S') at p^2 = m^2, minus*)
(*delta2; the derivative is taken in D dimensions (FeynCalc writes DB0, DB1), so that the O(eps) parts of (D-2) and*)
(*(D-1+xi) multiply the IR poles.  DB0/DB1 at threshold from LoopTools (Package-X leaves them unevaluated).  The note:*)
(*R - 1 = -(e^2/K)[(3 - xi) DeltaIR + 4 + 3 ln(mu^2/m^2)],  F1^R(0) - 1 = (e^2/K)[(3 - xi) DeltaIR + 4 - 3 ln(m^2/mu^2)].*)


{sVD$, sSD$} = {xiOL$ (D - 2) PaVe[1, {pp}, {Me^2, 0}], (D - 1 + xiOL$) B0[pp, Me^2, 0]};      (* K Sigma_V, K Sigma_S over e^2 *)
rMinus1$ = (sVD$ /. pp -> Me^2) + 2 Me^2 (xiOL$ (D - 2) DB1[Me^2, Me^2, 0] + (D - 1 + xiOL$) DB0[Me^2, Me^2, 0]);
Print["(d) K(R - 1)/e^2 in D dims, before subtracting delta2: ", InputForm[rMinus1$]];
Do[Module[{r = ltOL$[rMinus1$ /. coup$ /. xiOL$ -> xi] + {xi, 0}, f = pxOL$[f1PV$ /. coup$ /. qq -> 0] + {-xi, 0}},
    Print["(d) xi = ", xi, ":  K(R-1) {IR pole, finite} = ", r, " (expect {", -(3 - xi), ", -4});  K(F1^R(0)-1) = ", f,
      " (expect {", 3 - xi, ", 4});  sum = ", Chop[r + f]]], {xi, {0, 1, 3}}];
Do[Module[{r = ltOL$[rMinus1$ /. {Me -> mv, xiOL$ -> xi} /. coup$] + {xi, 0}},
    AppendTo[rowsOL$, {If[mv == 1, "R_e", "R_mu"], mv, xi, Indeterminate, Indeterminate, r[[1]], r[[2]]}]],
  {mv, {1, 17/10}}, {xi, {0, 1, 3}}];


(* ::Text:: *)
(*The pole mass: Sigma_V + Sigma_S at p^2 = m^2 does not depend on xi (Package-X, mu = 1).*)


Do[Print["(d) K(Sigma_V + Sigma_S)(m^2)/e^2 at m = ", N[mv], ", xi = 0, 1, 3: ",
    Table[Last[pxOL$[(sVD$ + sSD$) /. pp -> mv^2 /. Me -> mv /. xiOL$ -> xi]], {xi, {0, 1, 3}}],
    "  (expect 4 - 3 ln m^2 = ", N[4 - 3 Log[mv^2], 16], ")"], {mv, {1, 17/10}}];


(* ::Subsubsection:: *)
(*Inspect: the brackets from Package-X and LoopTools*)


If[$Notebooks,
  TableForm[{#[[1]], N[#[[2]]], N[#[[3]]], NumberForm[#[[4]], 10], NumberForm[#[[5]], 12], NumberForm[#[[6]], 10], NumberForm[#[[7]], 12]} & /@ rowsOL$,
    TableHeadings -> {None, {"func", "arg", "xi", "PX pole", "PX finite", "LT pole", "LT finite"}}]
]


resultsDirOL$ = FileNameJoin[{srcDirOL$, "results"}];
Quiet[CreateDirectory[resultsDirOL$]];
numStrOL$[x_] := If[x === Indeterminate, "nan", ToString[CForm[N[x]]]];
cplxOL$[x_] := If[x === Indeterminate, {"nan", "nan"}, {numStrOL$[Re[x]], numStrOL$[Im[x]]}];
csvLinesOL$ = Prepend[
   StringRiffle[Join[{#[[1]], numStrOL$[#[[2]]], numStrOL$[#[[3]]]}, Flatten[cplxOL$ /@ #[[4 ;; 7]]]], ","] & /@ rowsOL$,
   "func,arg,xi,re_pole_px,im_pole_px,re_px,im_px,re_pole_lt,im_pole_lt,re_lt,im_lt"];
Export[FileNameJoin[{resultsDirOL$, "oneloop_mathematica.csv"}], StringRiffle[csvLinesOL$, "\n"] <> "\n", "Text"];
Print["(d) wrote ", Length[rowsOL$], " rows to results/oneloop_mathematica.csv"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirOL$, DeleteContents -> True];
