(* ::Package:: *)

(* ::Title:: *)
(*Step (2): tree-level amplitudes and spin sums with FeynArts + FeynCalc (pseudoscalar Yukawa + phi^4)*)


(* ::Text:: *)
(*Research note models/yukawa_ps, step (2): compare with Eq. (11) (eq:Mtree) and with the psi psi -> psi psi formula of Sec. 5 (eq:MtreeD).*)
(*  (A) phi(p1) phi(p2) -> phi(k1) phi(k2):          M = -lambda*)
(*  (B) psi(p1) psibar(p2) -> phi(k1) phi(k2):       M = y^2 vbar(p2) [k1slash/(t-M^2) + k2slash/(u-M^2)] u(p1),*)
(*                                                   sum|M|^2 = 2 y^4 [(t-M^2)(u-M^2) - m^4] (t-u)^2 / ((t-M^2)^2 (u-M^2)^2)*)
(*  (C) psi(p1) psibar(p2) -> psi(p3) psibar(p4):    sum|M|^2 = 4 y^4 [s^2/(s-m^2)^2 + t^2/(t-m^2)^2 + s t/((s-m^2)(t-m^2))]*)
(*  (D) psi(p1) psi(p2) -> psi(p3) psi(p4):          sum|M|^2 = 4 y^4 [t^2/(t-m^2)^2 + u^2/(u-m^2)^2 + t u/((t-m^2)(u-m^2))]*)
(*sum|M|^2 is the sum (not the average) over the spins of the external fermions.  Mandelstam variables: s = (p1+p2)^2,*)
(*t = (p1-k1)^2 or (p1-p3)^2, u = (p1-k2)^2 or (p1-p4)^2.  Uses the FeynArts model in Src/generated/PsYukawa_FA (run*)
(*generate_PsYukawa.wl first); a copy is patched with FAPatch in a temporary directory.  FeynArts' default PreFactor -I*)
(*turns the sum of diagrams (i M) into M itself.  Model symbols: yps = y, lamphi = lambda, mphi = m, Mpsi = M.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file tree_feyncalc.wl.  Interactive:  ~/hep/bin/wopen tree_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
FCSetDiracGammaScheme["NDR"];


srcDirTree$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Text:: *)
(*A patched copy of the FeynRules-generated FeynArts model.*)


modelTmpDirTree$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTree$, "generated", "PsYukawa_FA"}], FileNameJoin[{modelTmpDirTree$, "PsYukawa_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirTree$, "PsYukawa_FA"}], Quiet -> True];
modelFileTree$ = FileNameJoin[{modelTmpDirTree$, "PsYukawa_FA", "PsYukawa_FA"}];


(* ::Text:: *)
(*Helpers.  The FeynArts model writes the Yukawa vertex with the chiral couplings gc2L, gc2R, and the replacement list*)
(*M$FACouplings = {gc2L -> -yps, gc2R -> yps} (written by FeynRules into PsYukawa_FA.mod, defined once the model is loaded)*)
(*must be applied by hand: FeynCalc does not do it.  Then gc2L omega_- + gc2R omega_+ = yps gamma5, and UndoChiralSplittings*)
(*recombines the projectors.  Numerical check point (also evaluated in tree_sigma.py): sqrt(s) = 5, cos(theta) = 0.3,*)
(*m = 1, M = 0.7, y = lambda = 1.*)


diagramsTree$[in_, out_] := InsertFields[CreateTopologies[0, 2 -> 2], in -> out,
   InsertionLevel -> {Particles}, Model -> modelFileTree$, GenericModel -> modelFileTree$];
amplitudesTree$[diags_, outMom_] := FCFAConvert[CreateFeynAmp[diags] /. M$FACouplings, IncomingMomenta -> {p1, p2},
   OutgoingMomenta -> outMom, ChangeDimension -> 4, List -> True, SMP -> False, UndoChiralSplittings -> True,
   DropSumOver -> True];
spinSumTree$[amp_] := Simplify[DiracSimplify[FermionSpinSum[amp ComplexConjugate[amp]]]];
numTree$ = {yps -> 1, lamphi -> 1, mphi -> 1, Mpsi -> 7/10};


(* ::Section:: *)
(*(A)  phi phi -> phi phi*)


diagsA$ = diagramsTree$[{S[1], S[1]}, {S[1], S[1]}];


(* ::Subsubsection:: *)
(*Inspect: the diagram (contact term only, no phi^3)*)


If[$Notebooks,
  Show[#, ImageSize -> 260] & /@ Render[Paint[diagsA$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampA$ = amplitudesTree$[diagsA$, {k1, k2}];
Print["(A) number of diagrams (expect 1): ", Length[ampA$]];
Print["(A) M(FeynCalc) - M(note) = ", Simplify[Total[ampA$] - (-lamphi)], "   (expect 0)"];


(* ::Section:: *)
(*(B)  psi psibar -> phi phi*)


diagsB$ = diagramsTree$[{F[1], -F[1]}, {S[1], S[1]}];


(* ::Subsubsection:: *)
(*Inspect: the two diagrams (t and u channel fermion exchange; no s channel)*)


If[$Notebooks,
  Show[#, ImageSize -> 320] & /@ Render[Paint[diagsB$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampB$ = amplitudesTree$[diagsB$, {k1, k2}];
Print["(B) number of diagrams (expect 2): ", Length[ampB$]];


(* ::Subsubsection:: *)
(*Inspect: the amplitude of each diagram*)


If[$Notebooks,
  TableForm[Transpose[{Range[Length[ampB$]], TraditionalForm[FCE[#]] & /@ ampB$}], TableHeadings -> {None, {"diagram", "M"}}]
]


FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, Mpsi, Mpsi, mphi, mphi];
mB$ = FeynAmpDenominatorExplicit[Total[ampB$]];
mBnote$ = yps^2 Spinor[-Momentum[p2], Mpsi] . (GS[k1]/(t - Mpsi^2) + GS[k2]/(u - Mpsi^2)) . Spinor[Momentum[p1], Mpsi];


(* ::Text:: *)
(*Amplitude-level comparison: sum over spins of |M(FeynCalc) - M(note)|^2 vanishes only if the two amplitudes agree for every*)
(*spin configuration (including the overall sign).  Then the spin sum itself against Eq. (11).*)


diffB$ = Simplify[spinSumTree$[mB$ - mBnote$] /. u -> 2 Mpsi^2 + 2 mphi^2 - s - t];
Print["(B) sum_spins |M(FeynCalc) - M(note)|^2 = ", diffB$, "   (expect 0)"];
sqB$ = spinSumTree$[mB$];
sqBnote$ = 2 yps^4 ((t - Mpsi^2) (u - Mpsi^2) - mphi^4) (t - u)^2/((t - Mpsi^2)^2 (u - Mpsi^2)^2);
Print["(B) sum|M|^2(FeynCalc) - Eq. (11) = ", Simplify[(sqB$ - sqBnote$) /. u -> 2 Mpsi^2 + 2 mphi^2 - s - t], "   (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: the spin sum from FeynCalc and the note's formula*)


If[$Notebooks,
  {Factor[sqB$ /. u -> 2 Mpsi^2 + 2 mphi^2 - s - t], Factor[sqBnote$ /. u -> 2 Mpsi^2 + 2 mphi^2 - s - t]} // TraditionalForm
]


(* ::Section:: *)
(*(C)  psi psibar -> psi psibar*)


diagsC$ = diagramsTree$[{F[1], -F[1]}, {F[1], -F[1]}];


(* ::Subsubsection:: *)
(*Inspect: the two diagrams (s and t channel phi exchange)*)


If[$Notebooks,
  Show[#, ImageSize -> 320] & /@ Render[Paint[diagsC$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampC$ = amplitudesTree$[diagsC$, {p3, p4}];
Print["(C) number of diagrams (expect 2): ", Length[ampC$]];


(* ::Subsubsection:: *)
(*Inspect: the amplitude of each diagram (note the relative sign)*)


If[$Notebooks,
  TableForm[Transpose[{Range[Length[ampC$]], TraditionalForm[FCE[#]] & /@ ampC$}], TableHeadings -> {None, {"diagram", "M"}}]
]


FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -p3, -p4, Mpsi, Mpsi, Mpsi, Mpsi];
sqC$ = spinSumTree$[FeynAmpDenominatorExplicit[Total[ampC$]]];
sqCnote$ = 4 yps^4 (s^2/(s - mphi^2)^2 + t^2/(t - mphi^2)^2 + s t/((s - mphi^2) (t - mphi^2)));
Print["(C) sum|M|^2(FeynCalc) - Eq. (11) = ", Simplify[(sqC$ - sqCnote$) /. u -> 4 Mpsi^2 - s - t], "   (expect 0)"];


(* ::Section:: *)
(*(D)  psi psi -> psi psi*)


diagsD$ = diagramsTree$[{F[1], F[1]}, {F[1], F[1]}];


(* ::Subsubsection:: *)
(*Inspect: the two diagrams (t and u channel phi exchange)*)


If[$Notebooks,
  Show[#, ImageSize -> 320] & /@ Render[Paint[diagsD$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampD$ = amplitudesTree$[diagsD$, {p3, p4}];
Print["(D) number of diagrams (expect 2): ", Length[ampD$]];
sqD$ = spinSumTree$[FeynAmpDenominatorExplicit[Total[ampD$]]];
sqDnote$ = 4 yps^4 (t^2/(t - mphi^2)^2 + u^2/(u - mphi^2)^2 + t u/((t - mphi^2) (u - mphi^2)));
Print["(D) sum|M|^2(FeynCalc) - Sec. 5 formula = ", Simplify[(sqD$ - sqDnote$) /. u -> 4 Mpsi^2 - s - t], "   (expect 0)"];


(* ::Section:: *)
(*Numbers at the check point*)


(* ::Text:: *)
(*sqrt(s) = 5, cos(theta) = 0.3, m = 1, M = 0.7, y = lambda = 1.  (B): E = sqrt(s)/2, |p| = sqrt(E^2 - M^2), |k| = sqrt(E^2 - m^2),*)
(*t = M^2 + m^2 - 2 (E^2 - |p||k| cos), u = M^2 + m^2 - 2 (E^2 + |p||k| cos).  (C), (D): t = -2 p^2 (1 - cos), u = -2 p^2 (1 + cos).*)


With[{sv = 25, c = 3/10, mv = 1, Mv = 7/10},
  Module[{e = Sqrt[sv]/2, pB, kB, tB, uB, p2, tC, uC},
    pB = Sqrt[e^2 - Mv^2]; kB = Sqrt[e^2 - mv^2];
    tB = Mv^2 + mv^2 - 2 (e^2 - pB kB c); uB = Mv^2 + mv^2 - 2 (e^2 + pB kB c);
    p2 = sv/4 - Mv^2; tC = -2 p2 (1 - c); uC = -2 p2 (1 + c);
    Print["(B) sum|M|^2 at the check point: ", ToString[NumberForm[N[sqB$ /. {s -> sv, t -> tB, u -> uB} /. numTree$, 20], 16], OutputForm]];
    Print["(C) sum|M|^2 at the check point: ", ToString[NumberForm[N[sqC$ /. {s -> sv, t -> tC, u -> uC} /. numTree$, 20], 16], OutputForm]];
    Print["(D) sum|M|^2 at the check point: ", ToString[NumberForm[N[sqD$ /. {s -> sv, t -> tC, u -> uC} /. numTree$, 20], 16], OutputForm]]]];


(* ::Section:: *)
(*Cleanup*)


DeleteDirectory[modelTmpDirTree$, DeleteContents -> True];
