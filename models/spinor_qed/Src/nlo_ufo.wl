(* ::Package:: *)

(* ::Title:: *)
(*Step (5), 3 of 3: UFOs with counterterm and R2 vertices (MS-bar charge and alpha(0)) for MadLoop*)


(* ::Text:: *)
(*FeynRules: read Src/generated/SpinorQED_CT.nlo, compare NLOCT's counterterms and R2 vertices with the note (Eqs. (6), (10)*)
(*and the R2 paragraph of App. D), and write two UFOs (overwritten):*)
(*  Src/generated/SpinorQED_NLO_MS_UFO  NLOCT's counterterms: fields and masses on shell, the charge ee MS-bar*)
(*                                      (MadLoop then gives the S-matrix element with e(mu) and the pole masses);*)
(*  Src/generated/SpinorQED_NLO_a0_UFO  the same with ee = e_OS of the Thomson limit (alpha(0)): the charge*)
(*                                      counterterm gets -Pi^R(0)/2 = (2/3)(e^2/K) sum_f ln(mu^2/m_f^2) (Eq. (10)),*)
(*                                      i.e. both f fbar A vertices get -I ee gamma^mu times this.*)
(*Both carry NLOCT's R2 vertices (MadLoop builds the numerators in four dimensions; R2 restores the rational terms).*)
(*Hand values (1/FR$Eps = Delta; NLOCT sets its infrared marker FR$IR -> 1, so 1/FR$Eps is DeltaUV + DeltaIR where*)
(*an infrared pole occurs), Feynman gauge, K = (4 Pi)^2, Q = -1 (tree vertex -I ee gamma^mu):*)
(*  deltaZpsi = -(e^2/K) [3 Delta + 4 + 3 ln(mu^2/m^2)]   (DeltaUV + 2 DeltaIR, Eq. (10)),*)
(*  deltam    = -(e^2/K) m [3 Delta + 4 + 3 ln(mu^2/m^2)]  (m_bare = m_pole + deltam),*)
(*  deltaZA   = -Pi(0) = -(4/3)(e^2/K) sum_f [Delta + ln(mu^2/m_f^2)],   deltaee/ee = (4/3)(e^2/K) Delta (MS-bar),*)
(*with NLOCT's vertex forms  psibar psi: I [deltaZpsi (pslash - m) - deltam],  A A: I deltaZA (k^mu k^nu - k^2 g^mu nu),*)
(*psibar psi A: -I ee gamma^mu (deltaee/ee + deltaZpsi + deltaZA/2);  R2 (App. D, paragraph on R2):*)
(*  psibar psi: I (e^2/K)(2m - pslash),  A A: -I (e^2/(4 Pi^2)) sum_f (m_f^2 - k^2/6) g^mu nu,  psibar psi A: I e^3/(8 Pi^2) gamma^mu.*)
(*FeynmanGauge = True writes gauge = [0, 1]; MadGraph needs Feynman gauge for loops.*)
(**)
(*Usage:  wolframscript -file nlo_ufo.wl     (after nlo_nloct.wl)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file nlo_ufo.wl  (in a fresh kernel).  Interactive:  ~/hep/bin/wopen nlo_ufo.wl  (in a fresh kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


srcDirNU$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Section:: *)
(*FeynRules, the model and the NLOCT counterterms*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNU$];
LoadModel["SpinorQED.fr"];
SetDirectory[FileNameJoin[{srcDirNU$, "generated"}]];
Get["SpinorQED_CT.nlo"];
R2$vertlist = DeleteCases[R2$vertlist, Last[{}]];
Print["perturbed orders: ", FR$InteractionOrderPerturbativeExpansion, ";  R2 vertices: ", Length[R2$vertlist],
  ";  UV vertices: ", Length[UV$vertlist]];
Print["vertex legs: R2 ", R2$vertlist[[All, 1, All, 1]], ";  UV ", UV$vertlist[[All, 1, All, 1]]];


(* ::Section:: *)
(*R2 vertices against the hand values*)


(* the spin structures: ProjP + ProjM = 1, pslash ProjP + pslash ProjM = pslash *)
spNU$ = {TensDot[SlashedP[k_], ProjP][a_, b_] :> SlashedP[k, a, b]/2 + slash5[k, a, b]/2,
   TensDot[SlashedP[k_], ProjM][a_, b_] :> SlashedP[k, a, b]/2 - slash5[k, a, b]/2,
   TensDot[Ga[mu_], ProjP][a_, b_] :> Ga[mu, a, b]/2 + ga5[mu, a, b]/2,
   TensDot[Ga[mu_], ProjM][a_, b_] :> Ga[mu, a, b]/2 - ga5[mu, a, b]/2,
   ProjP[a_, b_] :> IndexDelta[a, b]/2 + Ga[5, a, b]/2, ProjM[a_, b_] :> IndexDelta[a, b]/2 - Ga[5, a, b]/2};
pickNU$[list_, legs_] := Expand[First[Cases[list, {legs, v_} :> v]] /. IPL[_] -> 1 /. spNU$];
s12$ = Sequence[Index[Spin, Ext[1]], Index[Spin, Ext[2]]];
kNU$ = (4 Pi)^2;
handR2$ = <|
   "elec" -> I ee^2/kNU$ (2 Me IndexDelta[s12$] - SlashedP[2, s12$]),
   "muon" -> I ee^2/kNU$ (2 MMU IndexDelta[s12$] - SlashedP[2, s12$]),
   "AA" -> -I ee^2/(4 Pi^2) (Me^2 + MMU^2 - SP[2, 2]/3) ME[Index[Lorentz, Ext[1]], Index[Lorentz, Ext[2]]],
   "elecA" -> I ee^3/(8 Pi^2) Ga[Index[Lorentz, Ext[3]], s12$],
   "muonA" -> I ee^3/(8 Pi^2) Ga[Index[Lorentz, Ext[3]], s12$]|>;
legsNU$ = <|"elec" -> {{elecbar, 1}, {elec, 2}}, "muon" -> {{muonbar, 1}, {muon, 2}}, "AA" -> {{A, 1}, {A, 2}},
   "elecA" -> {{elecbar, 1}, {elec, 2}, {A, 3}}, "muonA" -> {{muonbar, 1}, {muon, 2}, {A, 3}}|>;
Do[Print["R2 ", k, ": NLOCT - hand = ", Simplify[pickNU$[R2$vertlist, legsNU$[k]] - handR2$[k]], "  (expect 0)"], {k, Keys[handR2$]}];
Print["R2 A A A A (NLOCT; used in step (10)): ", InputForm[pickNU$[R2$vertlist, {{A, 1}, {A, 2}, {A, 3}, {A, 4}}]]];


(* ::Section:: *)
(*UV counterterms against the hand values*)


lgNU$[m_] := 2 Log[FR$MU/m];   (* ln(mu^2/m^2) *)
dZpsiNU$[m_] := -ee^2/kNU$ (3/FR$Eps + 4 + 3 lgNU$[m]);
dmNU$[m_] := -ee^2/kNU$ m (3/FR$Eps + 4 + 3 lgNU$[m]);
dZANU$ = -4/3 ee^2/kNU$ (2/FR$Eps + lgNU$[Me] + lgNU$[MMU]);
deeNU$ = 4/3 ee^2/kNU$/FR$Eps;   (* deltaee/ee, MS-bar *)
handUV$ = <|
   "elec" -> I (dZpsiNU$[Me] (SlashedP[2, s12$] - Me IndexDelta[s12$]) - dmNU$[Me] IndexDelta[s12$]),
   "muon" -> I (dZpsiNU$[MMU] (SlashedP[2, s12$] - MMU IndexDelta[s12$]) - dmNU$[MMU] IndexDelta[s12$]),
   "AA" -> I dZANU$ (FV[2, Index[Lorentz, Ext[1]]] FV[2, Index[Lorentz, Ext[2]]] - SP[2, 2] ME[Index[Lorentz, Ext[1]], Index[Lorentz, Ext[2]]]),
   "elecA" -> -I ee (deeNU$ + dZpsiNU$[Me] + dZANU$/2) Ga[Index[Lorentz, Ext[3]], s12$],
   "muonA" -> -I ee (deeNU$ + dZpsiNU$[MMU] + dZANU$/2) Ga[Index[Lorentz, Ext[3]], s12$]|>;
posNU$ = {Me -> 1, MMU -> 17/10, FR$MU -> 1};
Do[Module[{d = pickNU$[UV$vertlist, legsNU$[k]] - handUV$[k]},
    Print["UV ", k, ": NLOCT - hand = ", Simplify[d /. If[a_, b_, c_] :> c, Assumptions -> {Me > 0, MMU > 0, FR$MU > 0}],
      "  (expect 0;  the If[m == 0, ...] branches are taken for m != 0)"]], {k, Keys[handUV$]}];


(* ::Subsubsection:: *)
(*Inspect: NLOCT's vertices*)


If[$Notebooks,
  TableForm[Join[{#, "R2", TraditionalForm[pickNU$[R2$vertlist, legsNU$[#]]]} & /@ Keys[legsNU$],
    {#, "UV", TraditionalForm[pickNU$[UV$vertlist, legsNU$[#]] /. If[a_, b_, c_] :> c]} & /@ Keys[legsNU$]]]
]


(* ::Section:: *)
(*UFO outputs*)


FeynmanGauge = True;
uvMSNU$ = UV$vertlist;
(* alpha(0): ee = e_OS, deltaee -> deltaee - Pi^R(0)/2 ee, -Pi^R(0)/2 = (2/3)(ee^2/K)[ln(mu^2/Me^2) + ln(mu^2/MMU^2)];
   the f fbar A counterterm is -I ee gamma^mu deltaee/ee + ..., so it gets -I ee gamma^mu (-Pi^R(0)/2) *)
(* each term carries NLOCT's label of the particles in the loop, IPL[...], which WriteUFO turns into loop_particles:
   the logarithms come from the e and the mu loops of the photon self-energy *)
shiftA0$ = -I ee 2/3 ee^2/kNU$ (lgNU$[Me] IPL[{elec}] + lgNU$[MMU] IPL[{muon}]) Ga[Index[Lorentz, Ext[3]], Index[Spin, Ext[1]], Index[Spin, Ext[2]]];
uvA0NU$ = If[MemberQ[{legsNU$["elecA"], legsNU$["muonA"]}, #[[1]]], {#[[1]], #[[2]] + shiftA0$}, #] & /@ UV$vertlist;
Print["alpha(0) shift of the f fbar A counterterms: ", InputForm[shiftA0$]];
Print["IPL labels in the UV vertices: ", Union[Cases[UV$vertlist, _IPL, Infinity]]];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"SpinorQED_NLO_MS_UFO", "SpinorQED_NLO_a0_UFO"}];
WriteUFO[LSpinorQED, UVCounterterms -> uvMSNU$, R2Vertices -> R2$vertlist, Output -> "SpinorQED_NLO_MS_UFO"];
WriteUFO[LSpinorQED, UVCounterterms -> uvA0NU$, R2Vertices -> R2$vertlist, Output -> "SpinorQED_NLO_a0_UFO"];
(* MadGraph's UFO-to-Fortran converter writes decimal numbers with 7 significant digits (-0.08333333333333333 becomes
   -8.333333D-02), while it keeps integer ratios exact.  WriteUFO writes some rational coefficients (here -1/12, -1/24,
   -1/4) as decimals, so they are turned back into ratios, (-1./12.) etc. *)
exactUFO$[file_] := Module[{txt = Import[file, "Text"], new},
   new = StringReplace[txt, RegularExpression["(?<![\\w.])(\\d+\\.\\d{7,})"] :>
       Module[{r = Rationalize[ToExpression["$1"], 10^-15]},
         If[Head[r] === Rational, "(" <> ToString[Numerator[r]] <> "./" <> ToString[Denominator[r]] <> ".)", "$1"]]];
   Export[file, new, "Text"];
   Length[StringCases[txt, RegularExpression["(?<![\\w.])\\d+\\.\\d{7,}"]]]];
Do[Print["decimal coefficients made exact in ", u, ": ",
    exactUFO$[FileNameJoin[{Directory[], u, #}]] & /@ {"couplings.py", "CT_couplings.py"}], {u, {"SpinorQED_NLO_MS_UFO", "SpinorQED_NLO_a0_UFO"}}];
Print["written: ", FileNames["SpinorQED_NLO_*_UFO"]];
