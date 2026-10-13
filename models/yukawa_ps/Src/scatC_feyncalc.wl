(* ::Package:: *)

(* ::Title:: *)
(*Step (12): one-loop psi psibar -> psi psibar with FeynArts + FeynCalc (pseudoscalar Yukawa + phi^4)*)


(* ::Text:: *)
(*Research note models/yukawa_ps, step (12).  psi(p1) psibar(p2) -> psi(p3) psibar(p4), truncated one-loop amplitudes*)
(*(tadpoles and external self-energies excluded), MS-bar, NDR.  Expected diagrams: phi self-energies on the s- and t-channel*)
(*phi (the fermion loop and the phi loop of the quartic vertex: 2 + 2), vertex corrections (4), boxes (4) = 12.*)
(*The amplitude is a sum of products of two spinor chains; each class is projected on four spinor structures by the*)
(*spin sum (traces):*)
(*    P(class, k) = sum_spins M_class (P_k)^*,  P_k = S55, T55, S11, T11,*)
(*    S55 = (vbar2 g5 u1)(ubar3 g5 v4), T55 = (ubar3 g5 u1)(vbar2 g5 v4), S11 = (vbar2 u1)(ubar3 v4), T11 = (ubar3 u1)(vbar2 v4),*)
(*and the MS-bar values at two points (LoopTools) are written to results/scatC_feyncalc.csv; scatC_numeric.py computes the*)
(*same projections from the hand formulas (explicit helicity spinors, COLLIER) and compares.  Classes: "se" (squared phi*)
(*propagator), "vertex" (three loop propagators), "boxT" (chains ubar3 .. u1, vbar2 .. v4), "boxS" (chains vbar2 .. u1, ubar3 .. v4).*)
(*Also: the tree spin sum against Eq. (11), and the 1/eps poles of the vertex class against the counterterm 2 deltay/y x tree.*)
(*Normalization as in scat_feyncalc.wl: PreFactor -> -I, A = (2 Pi)^D M, (4 Pi)^2 M = A/Pi^2 at D = 4.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file scatC_feyncalc.wl  (run generate_PsYukawa.wl first).  Interactive:  ~/hep/bin/wopen scatC_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
FCSetDiracGammaScheme["NDR"];
SetOptions[DiracSimplify, ToDiracGamma67 -> False, DiracSubstitute67 -> True];

srcDirCC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

modelTmpDirCC$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirCC$, "generated", "PsYukawa_FA"}], FileNameJoin[{modelTmpDirCC$, "PsYukawa_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirCC$, "PsYukawa_FA"}], Quiet -> True];
modelCC$ = FileNameJoin[{modelTmpDirCC$, "PsYukawa_FA", "PsYukawa_FA"}];
diagC$ = InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], {F[1], -F[1]} -> {F[1], -F[1]},
   InsertionLevel -> {Particles}, Model -> modelCC$, GenericModel -> modelCC$];
diagC0$ = InsertFields[CreateTopologies[0, 2 -> 2], {F[1], -F[1]} -> {F[1], -F[1]},
   InsertionLevel -> {Particles}, Model -> modelCC$, GenericModel -> modelCC$];


(* ::Subsubsection:: *)
(*Inspect: the one-loop diagrams*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diagC$, ColumnsXRows -> {4, 3}, Numbering -> Simple, DisplayFunction -> Identity]]
]


convCC$[diags_] := FCFAConvert[CreateFeynAmp[diags, PreFactor -> -I] /. M$FACouplings, IncomingMomenta -> {p1, p2},
    OutgoingMomenta -> {p3, p4}, LoopMomenta -> {q}, ChangeDimension -> D, List -> True, SMP -> False,
    DropSumOver -> True] /. {DiracGamma[6] -> (1 + DiracGamma[5])/2, DiracGamma[7] -> (1 - DiracGamma[5])/2};
rawC$ = convCC$[diagC$];
treeC$ = Total[convCC$[diagC0$]];
Print["number of one-loop diagrams (expect 12): ", Length[rawC$], ";  tree diagrams: ", Length[convCC$[diagC0$]]];

loopProps$[x_] := Max[Length /@ Cases[FCI[x], FeynAmpDenominator[a__] /; ! FreeQ[{a}, q], Infinity]];
tChainQ$[x_] := ! FreeQ[FCI[x], Spinor[Momentum[p3, ___], ___] . ___ . Spinor[Momentum[p1, ___], ___]];
(* by the number of loop propagators: 1 (phi loop of the quartic vertex) or 2 (fermion loop) = phi self-energy, 3 = vertex, 4 = box *)
classOf$[x_] := Switch[loopProps$[x], 4, If[tChainQ$[x], "boxT", "boxS"], 3, "vertex", _, "se"];
classesC$ = classOf$ /@ rawC$;
Print["classes of the diagrams: ", classesC$];


(* ::Section:: *)
(*Kinematics, reduction and the projections*)


FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -p3, -p4, Mpsi, Mpsi, Mpsi, Mpsi, Dimension -> D];
onShellC$ = {u -> 4 Mpsi^2 - s - t};
(* traces first, then the tensor reduction of the scalar integrands (much faster than reducing the spinor chains) *)
spinSumCC$[x_] := DiracSimplify[FermionSpinSum[x, ExtraFactor -> 1] /. DiracTrace[a___] :> DiracTrace[a, DiracTraceEvaluate -> True]];
reduceCC$[x_] := FCE[FeynAmpDenominatorExplicit[TID[x, q, ToPaVe -> True]]];
sp$[p_] := Spinor[Momentum[p, D], Mpsi, 1];
spm$[p_] := Spinor[-Momentum[p, D], Mpsi, 1];
(* the conjugated test structures P_k^*: (ubar3 G u1)^* = ubar1 Gbar u3, Gbar(g5) = -g5, Gbar(1) = 1 *)
conjP$ = <|"S55" -> (spm$[p4] . (-GA5) . sp$[p3]) (sp$[p1] . (-GA5) . spm$[p2]),
   "T55" -> (sp$[p1] . (-GA5) . sp$[p3]) (spm$[p4] . (-GA5) . spm$[p2]),
   "S11" -> (spm$[p4] . sp$[p3]) (sp$[p1] . spm$[p2]),
   "T11" -> (sp$[p1] . sp$[p3]) (spm$[p4] . spm$[p2])|>;
projOf$[amp_, k_] := Module[{x = DiracSimplify[FCI[amp]] conjP$[k]},
   x = spinSumCC$[x];
   x = If[FreeQ[x, q], FCE[FeynAmpDenominatorExplicit[x]], reduceCC$[x]];
   FCE[Expand[x /. onShellC$]]];
tStartCC$ = AbsoluteTime[];
classSum$[c_] := Total[Pick[rawC$, classesC$, c]];
projC$ = Association[Table[(Print["projecting ", c, " on ", k, " (", Round[AbsoluteTime[] - tStartCC$], " s)"];
     {c, k} -> projOf$[classSum$[c], k]), {c, {"se", "vertex", "boxT", "boxS"}}, {k, Keys[conjP$]}]];
projTree$ = Association[Table[k -> projOf$[treeC$, k], {k, Keys[conjP$]}]];


(* ::Text:: *)
(*Tree: sum_spins |M0|^2 against Eq. (11): 4 y^4 [s^2/(s-m^2)^2 + t^2/(t-m^2)^2 + s t/((s-m^2)(t-m^2))] (the tree with*)
(*PreFactor -I is (2 Pi)^D... no: at tree level CreateFeynAmp gives M itself up to the factor -I i = 1).*)


treeSq$ = Module[{x = DiracSimplify[FCI[treeC$]] ComplexConjugate[DiracSimplify[FCI[treeC$]]]},
   FCE[Simplify[FeynAmpDenominatorExplicit[spinSumCC$[x]] /. onShellC$ /. D -> 4]]];
treeRef$ = 4 yps^4 (s^2/(s - mphi^2)^2 + t^2/(t - mphi^2)^2 + s t/((s - mphi^2) (t - mphi^2)));
Print["tree: sum|M0|^2 - Eq. (11) = ", Simplify[(treeSq$ - treeRef$) /. onShellC$], "  (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: the projections of each class (PaVe functions)*)


If[$Notebooks, TableForm[KeyValueMap[{#1, Short[#2, 3]} &, projC$]]]


(* ::Section:: *)
(*UV poles of the vertex class against the MS-bar counterterm*)


(* ::Text:: *)
(*The phi self-energy poles cancel against delta_phi, delta_m (internal line), the vertex poles against the two Yukawa*)
(*counterterms per channel, 2 deltay/y times the tree, deltay = y^3/(4 Pi)^2 /eps; the boxes are finite.  Check on the*)
(*projections: pole of (4 Pi)^2 P(vertex, k) = -2 y^2 (4 Pi)^2 deltay/y ... i.e. -(2 y^2) times P(tree, k) per unit 1/eps.*)


(* UV parts of the PaVe functions (PaVeUVPart: B0 -> 2/(4 - D), ...), with D = 4 - 2 Epsilon; A = (2 Pi)^D M *)
poleCC$[x_] := SeriesCoefficient[(PaVeUVPart[FCI[x]] /. D -> 4 - 2 Epsilon)/(2 Pi)^4, {Epsilon, 0, -1}] (4 Pi)^2;
Do[Module[{pv = Simplify[poleCC$[projC$[{"vertex", k}]] /. onShellC$], pb = Simplify[poleCC$[projC$[{"boxT", k}] + projC$[{"boxS", k}]]]},
   Print["pole of (4 Pi)^2 P(vertex, ", k, ") + 2 y^2 P(tree, ", k, ") = ",
     Simplify[(pv + 2 yps^2 projTree$[k]) /. onShellC$ /. D -> 4], " (expect 0);  boxes: ", pb, " (expect 0)"]],
  {k, Keys[conjP$]}];


(* ::Section:: *)
(*MS-bar values at two points (LoopTools)*)


msbarCC$[0] = 0;
msbarCC$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)];
numArgsCC$[x_] := FCI[x] /. (h : A0 | B0 | C0 | D0)[args__] :> h @@ N[{args}] /. PaVe[i__, a_List, b_List] :> PaVe[i, N[a], N[b]];
ltCC$[0] = 0.;
ltCC$[x_] := Chop[N[msbarCC$[Quiet[LToolsEvaluate[numArgsCC$[x] /. D -> 4 - 2 Epsilon], LToolsEvaluate::tens]]], 10^-15];
coupCC$ = {mphi -> 1, Mpsi -> 7/10, yps -> 1, lamphi -> 1};
pointsCC$ = {{5, 3/10}, {5/2, -6/10}};
rowsCC$ = Flatten[Table[Module[{rs = pt[[1]], c = pt[[2]], ss, tt, val},
     ss = rs^2; tt = -2 (ss/4 - (7/10)^2) (1 - c);
     val = ltCC$[(4 Pi)^2 projC$[{cl, k}] /. coupCC$ /. {s -> ss, t -> tt, u -> 4 (7/10)^2 - ss - tt}];
     {rs, c, cl, k, val}], {pt, pointsCC$}, {cl, {"se", "vertex", "boxT", "boxS"}}, {k, Keys[conjP$]}], 2];
treeRowsCC$ = Flatten[Table[Module[{ss = pt[[1]]^2, tt},
     tt = -2 (ss/4 - (7/10)^2) (1 - pt[[2]]);
     {pt[[1]], pt[[2]], "tree", k, N[projTree$[k] /. coupCC$ /. {s -> ss, t -> tt, u -> 4 (7/10)^2 - ss - tt} /. D -> 4]}],
    {pt, pointsCC$}, {k, Keys[conjP$]}], 1];

resultsDirCC$ = FileNameJoin[{srcDirCC$, "results"}];
Quiet[CreateDirectory[resultsDirCC$]];
lineCC$[r_] := StringRiffle[{ToString[CForm[N[r[[1]]]]], ToString[CForm[N[r[[2]]]]], r[[3]], r[[4]],
     ToString[CForm[Re[r[[5]]]]], ToString[CForm[Im[r[[5]]]]]}, ","];
Export[FileNameJoin[{resultsDirCC$, "scatC_feyncalc.csv"}],
  StringRiffle[Prepend[lineCC$ /@ Join[treeRowsCC$, rowsCC$], "sqrts,costheta,class,structure,re,im"], "\n"] <> "\n", "Text"];
Print["wrote ", Length[rowsCC$] + Length[treeRowsCC$], " rows to results/scatC_feyncalc.csv ((4 Pi)^2 x projection, MS-bar, mu = 1)"];


(* ::Subsubsection:: *)
(*Inspect: the values*)


If[$Notebooks, TableForm[Join[treeRowsCC$, rowsCC$]]]


(* ::Section:: *)
(*Cleanup*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirCC$, DeleteContents -> True];
