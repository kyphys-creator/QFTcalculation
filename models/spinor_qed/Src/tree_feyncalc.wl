(* ::Package:: *)

(* ::Title:: *)
(*Step (2): tree-level amplitudes and spin sums with FeynArts + FeynCalc (spinor QED with e and mu)*)


(* ::Text:: *)
(*Research note models/spinor_qed, step (2): compare with Eq. (11) (eq:Mtree) and Eq. (12) (eq:sumtree).*)
(*  (A) e-(p1) e+(p2) -> mu-(k1) mu+(k2):   M = e^2/s [vbar(p2) g^nu u(p1)] [ubar(k1) g_nu v(k2)]*)
(*  (B) e-(p1) e+(p2) -> e-(k1) e+(k2):     M = e^2 { [ub(k1) g u(p1)][vb(p2) g v(k2)]/t - [ub(k1) g v(k2)][vb(p2) g u(p1)]/s }*)
(*  (C) e-(p1) gamma(p2) -> e-(k1) gamma(k2)  (the note's p, k, p', k'):*)
(*      M = -e^2 eps*_mu(k2) eps_nu(p2) ubar(k1) [g^mu (p1+p2+m) g^nu/(s-m^2) + g^nu (p1-k2+m) g^mu/(u-m^2)] u(p1)*)
(*  (D) e-(p1) e+(p2) -> gamma(k1) gamma(k2):*)
(*      M = -e^2 eps*_mu(k1) eps*_nu(k2) vbar(p2) [g^nu (p1-k1+m) g^mu/(t-m^2) + g^mu (p1-k2+m) g^nu/(u-m^2)] u(p1)*)
(*Mandelstam variables s = (p1+p2)^2, t = (p1-k1)^2, u = (p1-k2)^2.  sum|M|^2 is the sum (not the average) over the*)
(*spins and photon polarizations.  Besides the spin sums, the script checks the gauge structure at tree level:*)
(*  - (A), (B): the (1 - xi) k k/k^2 part of the photon propagator drops out (the amplitude does not depend on xi);*)
(*  - (C), (D): replacing a photon polarization by its momentum gives 0 (Ward identity, note App. G), so that the*)
(*    polarization sum may be replaced by -g;  the amplitude-level comparison uses the physical (transverse) sum with an*)
(*    auxiliary light-like vector, which is positive definite.*)
(*Uses the FeynArts model in Src/generated/SpinorQED_FA (run generate_SpinorQED.wl first); a copy is patched with*)
(*FAPatch in a temporary directory.  FeynRules wrote the charge ee as FeynArts' EL (M$FACouplings: gc1 -> -EL).*)
(*Model symbols: EL = e, Me = m_e, MMU = m_mu.  CreateFeynAmp's GaugeRules -> {} keeps GaugeXi[A] (its default sets it to 1).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file tree_feyncalc.wl.  Interactive:  ~/hep/bin/wopen tree_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;


srcDirTree$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Text:: *)
(*A patched copy of the FeynRules-generated FeynArts model.*)


modelTmpDirTree$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTree$, "generated", "SpinorQED_FA"}], FileNameJoin[{modelTmpDirTree$, "SpinorQED_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirTree$, "SpinorQED_FA"}], Quiet -> True];
modelFileTree$ = FileNameJoin[{modelTmpDirTree$, "SpinorQED_FA", "SpinorQED_FA"}];


(* ::Text:: *)
(*Helpers.  M$FACouplings (gc1 -> -EL, gc2 -> -EL) must be applied by hand; FCFAConvert writes EL as FCGV["EL"].*)
(*Field codes: F[1] = e-, -F[1] = e+, F[2] = mu-, -F[2] = mu+, V[1] = photon.  Numerical check point (also evaluated in*)
(*tree_sigma.py): sqrt(s) = 5, cos(theta) = 0.3, m_e = 1, m_mu = 1.7, e = 1, with theta the angle of k1 to p1 in the CM frame.*)


diagramsTree$[in_, out_] := InsertFields[CreateTopologies[0, 2 -> 2], in -> out,
   InsertionLevel -> {Particles}, Model -> modelFileTree$, GenericModel -> modelFileTree$];
amplitudesTree$[diags_] := FCFAConvert[CreateFeynAmp[diags, GaugeRules -> {}] /. M$FACouplings,
   IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {k1, k2}, ChangeDimension -> 4, List -> True, SMP -> False,
   UndoChiralSplittings -> True, DropSumOver -> True] /. FCGV["EL"] -> EL;
xiTree$ = GaugeXi[A];
spinSumTree$[amp_] := Simplify[DiracSimplify[FermionSpinSum[amp ComplexConjugate[amp]]]];
(* physical polarization sums with the other photon's momentum as the auxiliary light-like vector *)
polSumTree$[x_, {k_, n_}] := DoPolarizationSums[x, k, n];
numTree$ = {EL -> 1, Me -> 1, MMU -> 17/10};
vb$[q_, mass_] := Spinor[-Momentum[q], mass, 1];  ub$[q_, mass_] := Spinor[Momentum[q], mass, 1];
vv$[q_, mass_] := Spinor[-Momentum[q], mass, 1];  uu$[q_, mass_] := Spinor[Momentum[q], mass, 1];
epsIn$[k_, mu_] := Pair[LorentzIndex[mu], Momentum[Polarization[k, I]]];
epsOut$[k_, mu_] := Pair[LorentzIndex[mu], Momentum[Polarization[k, -I]]];


(* ::Section:: *)
(*(A)  e+ e- -> mu+ mu-*)


diagsA$ = diagramsTree$[{F[1], -F[1]}, {F[2], -F[2]}];


(* ::Subsubsection:: *)
(*Inspect: the diagram (s-channel photon)*)


If[$Notebooks,
  Show[#, ImageSize -> 260] & /@ Render[Paint[diagsA$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampA$ = amplitudesTree$[diagsA$];
Print["(A) number of diagrams (expect 1): ", Length[ampA$]];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, Me, Me, MMU, MMU];
mA$ = FeynAmpDenominatorExplicit[Total[ampA$]];
Print["(A) d M/d xi after the Dirac equation (expect 0): ", Simplify[DiracSimplify[D[mA$, xiTree$]]]];
mA$ = mA$ /. xiTree$ -> 1;
mAnote$ = EL^2/s vb$[p2, Me] . GA[nu] . uu$[p1, Me] ub$[k1, MMU] . GA[nu] . vv$[k2, MMU];
Print["(A) sum_spins |M(FC) - M(note)|^2 = ", Simplify[spinSumTree$[mA$ - mAnote$] /. u -> 2 Me^2 + 2 MMU^2 - s - t],
  ",  sum_spins |M(FC) + M(note)|^2 = ", Simplify[spinSumTree$[mA$ + mAnote$] /. u -> 2 Me^2 + 2 MMU^2 - s - t],
  "   (expect one of them 0)"];
sqA$ = spinSumTree$[mA$];
sqAnote$ = 8 EL^4/s^2 ((t - Me^2 - MMU^2)^2 + (u - Me^2 - MMU^2)^2 + 2 s (Me^2 + MMU^2));
Print["(A) sum|M|^2(FeynCalc) - Eq. (12) = ", Simplify[(sqA$ - sqAnote$) /. u -> 2 Me^2 + 2 MMU^2 - s - t], "   (expect 0)"];


(* ::Section:: *)
(*(B)  e+ e- -> e+ e-  (Bhabha)*)


diagsB$ = diagramsTree$[{F[1], -F[1]}, {F[1], -F[1]}];


(* ::Subsubsection:: *)
(*Inspect: the two diagrams (s and t channel photon)*)


If[$Notebooks,
  Show[#, ImageSize -> 320] & /@ Render[Paint[diagsB$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampB$ = amplitudesTree$[diagsB$];
Print["(B) number of diagrams (expect 2): ", Length[ampB$]];


(* ::Subsubsection:: *)
(*Inspect: the amplitude of each diagram (note the relative sign)*)


If[$Notebooks,
  TableForm[Transpose[{Range[Length[ampB$]], TraditionalForm[FCE[#]] & /@ ampB$}], TableHeadings -> {None, {"diagram", "M"}}]
]


FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, Me, Me, Me, Me];
mB$ = FeynAmpDenominatorExplicit[Total[ampB$]];
Print["(B) d M/d xi after the Dirac equation (expect 0): ", Simplify[DiracSimplify[D[mB$, xiTree$]]]];
mB$ = mB$ /. xiTree$ -> 1;
mBnote$ = EL^2 (ub$[k1, Me] . GA[nu] . uu$[p1, Me] vb$[p2, Me] . GA[nu] . vv$[k2, Me]/t -
     ub$[k1, Me] . GA[nu] . vv$[k2, Me] vb$[p2, Me] . GA[nu] . uu$[p1, Me]/s);


(* ::Text:: *)
(*The overall sign of a fermionic amplitude is a convention (the order of the external fermion operators); only the*)
(*relative sign of the two diagrams is physical.  Both M(FC) - M(note) and M(FC) + M(note) are printed (also in (A),*)
(*(C), (D)): one of them must vanish.*)


dmB$ = Simplify[spinSumTree$[mB$ - mBnote$] /. u -> 4 Me^2 - s - t];
spB$ = Simplify[spinSumTree$[mB$ + mBnote$] /. u -> 4 Me^2 - s - t];
Print["(B) sum_spins |M(FC) - M(note)|^2 = ", dmB$, ",  sum_spins |M(FC) + M(note)|^2 = ", spB$,
  "   (expect one of them 0)"];
sqB$ = spinSumTree$[mB$];
sqBnote$ = 8 EL^4 (((s - 2 Me^2)^2 + (u - 2 Me^2)^2 + 4 Me^2 t)/t^2 + ((t - 2 Me^2)^2 + (u - 2 Me^2)^2 + 4 Me^2 s)/s^2 +
     2 (u - 2 Me^2) (u - 6 Me^2)/(s t));
Print["(B) sum|M|^2(FeynCalc) - Eq. (12) = ", Simplify[(sqB$ - sqBnote$) /. u -> 4 Me^2 - s - t], "   (expect 0)"];


(* ::Section:: *)
(*(C)  e- gamma -> e- gamma  (Compton)*)


diagsC$ = diagramsTree$[{F[1], V[1]}, {F[1], V[1]}];


(* ::Subsubsection:: *)
(*Inspect: the two diagrams (s and u channel electron)*)


If[$Notebooks,
  Show[#, ImageSize -> 320] & /@ Render[Paint[diagsC$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampC$ = amplitudesTree$[diagsC$];
Print["(C) number of diagrams (expect 2): ", Length[ampC$]];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, Me, 0, Me, 0];
mC$ = FeynAmpDenominatorExplicit[Total[ampC$]];


(* ::Text:: *)
(*Ward identity: the amplitude with eps(p2) -> p2 (or eps*(k2) -> k2) vanishes between on-shell spinors.  FeynCalc does*)
(*not reduce the Dirac chains to 0 by itself (it would need momentum conservation inside the chains), so the check is*)
(*done on sum_spins sum_pol |M(eps -> k)|^2 with the physical sum over the other photon, which is positive definite and*)
(*vanishes only if the amplitude vanishes for every spin and polarization.*)


wardSq$[x_, {k_, n_}] := Simplify[polSumTree$[FermionSpinSum[x ComplexConjugate[x]] // DiracSimplify, {k, n}]];
wardC$ = {wardSq$[mC$ /. Momentum[Polarization[p2, I]] -> Momentum[p2], {k2, p2}] /. t -> 2 Me^2 - s - u,
   wardSq$[mC$ /. Momentum[Polarization[k2, -I]] -> Momentum[k2], {p2, k2}] /. t -> 2 Me^2 - s - u} // Simplify;
Print["(C) Ward identity: sum|M(eps(p2) -> p2)|^2, sum|M(eps*(k2) -> k2)|^2 = ", wardC$, "   (expect {0, 0})"];
mCnote$ = -EL^2 epsOut$[k2, mu] epsIn$[p2, nu] ub$[k1, Me] . (GA[mu] . (GS[p1 + p2] + Me) . GA[nu]/(s - Me^2) +
      GA[nu] . (GS[p1 - k2] + Me) . GA[mu]/(u - Me^2)) . uu$[p1, Me];
physC$[x_] := Simplify[polSumTree$[polSumTree$[FermionSpinSum[x ComplexConjugate[x]] // DiracSimplify, {p2, k2}], {k2, p2}] /.
    t -> 2 Me^2 - s - u];
dmC$ = physC$[mC$ - mCnote$]; spC$ = physC$[mC$ + mCnote$];
Print["(C) physical sum |M(FC) - M(note)|^2 = ", dmC$, ",  |M(FC) + M(note)|^2 = ", spC$, "   (expect one of them 0)"];
sqC$ = Simplify[DoPolarizationSums[DoPolarizationSums[spinSumTree$[mC$], p2, 0], k2, 0]];
sqCnote$ = 8 EL^4 (-(u - Me^2)/(s - Me^2) - (s - Me^2)/(u - Me^2) + 4 Me^2 (1/(s - Me^2) + 1/(u - Me^2)) +
     4 Me^4 (1/(s - Me^2) + 1/(u - Me^2))^2);
Print["(C) sum|M|^2(FeynCalc, -g) - Eq. (12) = ", Simplify[(sqC$ - sqCnote$) /. t -> 2 Me^2 - s - u], "   (expect 0)"];
Print["(C) sum|M|^2(FeynCalc, physical) - Eq. (12) = ", Simplify[physC$[mC$] - (sqCnote$ /. t -> 2 Me^2 - s - u)], "   (expect 0)"];


(* ::Section:: *)
(*(D)  e+ e- -> gamma gamma*)


diagsD$ = diagramsTree$[{F[1], -F[1]}, {V[1], V[1]}];


(* ::Subsubsection:: *)
(*Inspect: the two diagrams (t and u channel electron)*)


If[$Notebooks,
  Show[#, ImageSize -> 320] & /@ Render[Paint[diagsD$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampD$ = amplitudesTree$[diagsD$];
Print["(D) number of diagrams (expect 2): ", Length[ampD$]];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, Me, Me, 0, 0];
mD$ = FeynAmpDenominatorExplicit[Total[ampD$]];
wardD$ = {wardSq$[mD$ /. Momentum[Polarization[k1, -I]] -> Momentum[k1], {k2, k1}] /. s -> 2 Me^2 - t - u,
   wardSq$[mD$ /. Momentum[Polarization[k2, -I]] -> Momentum[k2], {k1, k2}] /. s -> 2 Me^2 - t - u} // Simplify;
Print["(D) Ward identity: sum|M(eps*(k1) -> k1)|^2, sum|M(eps*(k2) -> k2)|^2 = ", wardD$, "   (expect {0, 0})"];
mDnote$ = -EL^2 epsOut$[k1, mu] epsOut$[k2, nu] vb$[p2, Me] . (GA[nu] . (GS[p1 - k1] + Me) . GA[mu]/(t - Me^2) +
      GA[mu] . (GS[p1 - k2] + Me) . GA[nu]/(u - Me^2)) . uu$[p1, Me];
physD$[x_] := Simplify[polSumTree$[polSumTree$[FermionSpinSum[x ComplexConjugate[x]] // DiracSimplify, {k1, k2}], {k2, k1}] /.
    s -> 2 Me^2 - t - u];
dmD$ = physD$[mD$ - mDnote$]; spD$ = physD$[mD$ + mDnote$];
Print["(D) physical sum |M(FC) - M(note)|^2 = ", dmD$, ",  |M(FC) + M(note)|^2 = ", spD$, "   (expect one of them 0)"];
sqD$ = Simplify[DoPolarizationSums[DoPolarizationSums[spinSumTree$[mD$], k1, 0], k2, 0]];
sqDnote$ = 8 EL^4 ((u - Me^2)/(t - Me^2) + (t - Me^2)/(u - Me^2) - 4 Me^2 (1/(t - Me^2) + 1/(u - Me^2)) -
     4 Me^4 (1/(t - Me^2) + 1/(u - Me^2))^2);
Print["(D) sum|M|^2(FeynCalc, -g) - Eq. (12) = ", Simplify[(sqD$ - sqDnote$) /. s -> 2 Me^2 - t - u], "   (expect 0)"];
Print["(D) sum|M|^2(FeynCalc, physical) - Eq. (12) = ", Simplify[physD$[mD$] - (sqDnote$ /. s -> 2 Me^2 - t - u)], "   (expect 0)"];
Print["(D) crossing: sum|M_D|^2 + sum|M_C|^2(s -> t) = ", Simplify[sqDnote$ + (sqCnote$ /. s -> t)], "   (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: the four spin sums from FeynCalc*)


If[$Notebooks,
  TableForm[{{"A", Factor[sqA$ /. u -> 2 Me^2 + 2 MMU^2 - s - t]}, {"B", Factor[sqB$ /. u -> 4 Me^2 - s - t]},
    {"C", Factor[sqC$ /. t -> 2 Me^2 - s - u]}, {"D", Factor[sqD$ /. s -> 2 Me^2 - t - u]}}] // TraditionalForm
]


(* ::Section:: *)
(*Numbers at the check point*)


(* ::Text:: *)
(*sqrt(s) = 5, cos(theta) = 0.3, m_e = 1, m_mu = 1.7, e = 1.  CM kinematics, theta = angle of k1 to p1:*)
(*(A) E = sqrt(s)/2, p = sqrt(E^2 - m_e^2), k = sqrt(E^2 - m_mu^2), t = m_e^2 + m_mu^2 - 2 (E^2 - p k c), u = ... + p k c;*)
(*(B) t = -2 p^2 (1 - c), u = -2 p^2 (1 + c);*)
(*(C) p = (s - m^2)/(2 sqrt(s)), E_e = (s + m^2)/(2 sqrt(s)), u = m^2 - 2 p (E_e + p c)  (k2 is opposite to k1);*)
(*(D) E = sqrt(s)/2, p = sqrt(E^2 - m^2), t = m^2 - 2 E (E - p c), u = m^2 - 2 E (E + p c).*)


With[{sv = 25, c = 3/10, me = 1, mm = 17/10},
  Module[{e = Sqrt[sv]/2, pA, kA, tA, uA, pB, pC, eC, uC, pD, tD, uD, pr},
    pA = Sqrt[e^2 - me^2]; kA = Sqrt[e^2 - mm^2];
    tA = me^2 + mm^2 - 2 (e^2 - pA kA c); uA = me^2 + mm^2 - 2 (e^2 + pA kA c);
    pB = Sqrt[e^2 - me^2];
    pC = (sv - me^2)/(2 Sqrt[sv]); eC = (sv + me^2)/(2 Sqrt[sv]); uC = me^2 - 2 pC (eC + pC c);
    pD = Sqrt[e^2 - me^2]; tD = me^2 - 2 e (e - pD c); uD = me^2 - 2 e (e + pD c);
    pr[lab_, x_] := Print[lab, " sum|M|^2 at the check point: ", ToString[NumberForm[N[x /. numTree$, 20], 16], OutputForm]];
    pr["(A)", sqA$ /. {s -> sv, t -> tA, u -> uA}];
    pr["(B)", sqB$ /. {s -> sv, t -> -2 pB^2 (1 - c), u -> -2 pB^2 (1 + c)}];
    pr["(C)", (sqC$ /. t -> 2 Me^2 - s - u) /. {s -> sv, u -> uC}];
    pr["(D)", (sqD$ /. s -> 2 Me^2 - t - u) /. {t -> tD, u -> uD}]]];
