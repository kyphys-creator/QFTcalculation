(* ::Package:: *)

(* ::Title:: *)
(*Step (3): one-loop 1PI functions of phi^3 + phi^4 in d = 4 (FeynArts + FeynCalc, Package-X, LoopTools)*)


(* ::Text:: *)
(*Research note models/phi34, step (3).*)
(*(a) FeynArts 1PI diagrams from Src/generated/Phi34_FA: V1 (1 diagram), V2 (2), V3 (4), V4 (12, one-particle*)
(*    reducible topologies excluded), reduced by FeynCalc (TID -> PaVe).  With PreFactor -> 1 the note, Eq. (4),*)
(*    predicts A_n = (2 Pi)^D V_n, i.e. with FeynCalc's Integrate[d^D q ...] = I Pi^2 PaVe:*)
(*      A1 = I Pi^2 g/2 A0,   A2 = I Pi^2 [g^2/2 B0(p^2) + lambda/2 A0],*)
(*      A3 = I Pi^2 [g^3 C0 + g lambda/2 (B0(p^2) + B0(k1^2) + B0(k2^2))],*)
(*      A4 = I Pi^2 [lambda^2/2 sum_x B0(x) + 2 lambda g^2 sum_x C0(m^2, m^2, x) + g^4 sum D0]   (on shell, x = s, t, u).*)
(*(b) UV poles (Package-X) and the MS-bar counterterms of Eq. (5): deltaZ = I d(V2pole)/d(p^2), deltam = -I V2pole(0),*)
(*    deltag = -I V3pole, deltalambda = -I V4pole (all times DeltaUV).*)
(*(c) MS-bar finite parts at m = mu = g = lambda = 1: the bracket b_n = (4 Pi)^2 V_n^R / I of Eq. (6) at a few*)
(*    points, from Package-X (A0, B0 analytic, C0 and D0 from ScalarC0, ScalarD0) and from LoopTools, written to*)
(*    Src/results/oneloop_mathematica.csv; oneloop_numeric.py compares them with COLLIER.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_feyncalc.wl  (run generate_Phi34.wl first).  Interactive:  ~/hep/bin/wopen oneloop_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];

srcDirOL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

modelTmpDirOL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOL$, "generated", "Phi34_FA"}], FileNameJoin[{modelTmpDirOL$, "Phi34_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOL$, "Phi34_FA"}], Quiet -> True];
modelOL$ = FileNameJoin[{modelTmpDirOL$, "Phi34_FA", "Phi34_FA"}];
insertOL$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles},
   Model -> modelOL$, GenericModel -> modelOL$];


(* ::Section:: *)
(*(a) diagrams and amplitudes*)


diag1$ = insertOL$[CreateTopologies[1, 1 -> 0], {S[1]} -> {}];
diag2$ = insertOL$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {S[1]} -> {S[1]}];
diag3$ = insertOL$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], {S[1]} -> {S[1], S[1]}];
diag4$ = insertOL$[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections, Reducible}],
   {S[1], S[1]} -> {S[1], S[1]}];
Print["(a) number of 1PI diagrams (expect 1, 2, 4, 12): ",
  Length[CreateFeynAmp[#]] & /@ {diag1$, diag2$, diag3$, diag4$}];


(* ::Subsubsection:: *)
(*Inspect: the 1PI diagrams of V2, V3 and V4*)


If[$Notebooks,
  {Show[#, ImageSize -> 360] & /@ Render[Paint[diag2$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 560] & /@ Render[Paint[diag3$, ColumnsXRows -> {4, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 560] & /@ Render[Paint[diag4$, ColumnsXRows -> {4, 3}, Numbering -> Simple, DisplayFunction -> Identity]]}
]


ampOL$[diags_, in_, out_] := FCE[FeynAmpDenominatorExplicit[TID[FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1],
     IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q}, ChangeDimension -> D,
     List -> False, SMP -> False, DropSumOver -> True], q, ToPaVe -> True]]];

FCClearScalarProducts[];
amp1$ = ampOL$[diag1$, {p}, {}];
amp2$ = ampOL$[diag2$, {p}, {p}] /. SPD[p] -> pp;
(* V3: incoming p = k1 + k2, invariants p^2 = p3s, k1^2 = k1s, k2^2 = k2s *)
FCClearScalarProducts[];
ScalarProduct[k1, k1] = k1s; ScalarProduct[k2, k2] = k2s; ScalarProduct[k1, k2] = (p3s - k1s - k2s)/2;
amp3$ = ampOL$[diag3$, {k1 + k2}, {k1, k2}] // Simplify;
(* V4 on shell *)
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, m, m, m, m];
amp4$ = ampOL$[diag4$, {p1, p2}, {k1, k2}] /. (-3 m^2 + s + t + u) -> m^2;
FCClearScalarProducts[];


(* ::Subsubsection:: *)
(*Inspect: the four amplitudes after the tensor reduction*)


If[$Notebooks,
  TableForm[{{"A1", TraditionalForm[amp1$]}, {"A2", TraditionalForm[amp2$]}, {"A3", TraditionalForm[amp3$]}, {"A4", TraditionalForm[Collect[amp4$, {gphi, lamphi}]]}}]
]


(* ::Text:: *)
(*Comparison with the note, Eq. (4) times (2 Pi)^D.  V3: one C0 (the g^3 triangle) and three B0; V4: canonical names on shell.*)


c03$ = First[Cases[amp3$, _C0, Infinity]];
canon4$ = {D0[m^2, m^2, m^2, m^2, a_, b_, m^2, m^2, m^2, m^2] :> d0[Sort[{a, b}]],
   C0[m^2, m^2, x_, m^2, m^2, m^2] :> c0[x], C0[m^2, x_, m^2, m^2, m^2, m^2] :> c0[x],
   C0[x_, m^2, m^2, m^2, m^2, m^2] :> c0[x], B0[x_, m^2, m^2] :> b0[x]};
hand1$ = I Pi^2 gphi/2 A0[m^2];
hand2$ = I Pi^2 (gphi^2/2 B0[pp, m^2, m^2] + lamphi/2 A0[m^2]);
hand3$ = I Pi^2 (gphi^3 c03$ + gphi lamphi/2 (B0[p3s, m^2, m^2] + B0[k1s, m^2, m^2] + B0[k2s, m^2, m^2]));
hand4$ = I Pi^2 (lamphi^2/2 (b0[s] + b0[t] + b0[u]) + 2 lamphi gphi^2 (c0[s] + c0[t] + c0[u]) +
    gphi^4 (d0[Sort[{s, t}]] + d0[Sort[{s, u}]] + d0[Sort[{t, u}]]));
Print["(a) A1 - I Pi^2 g/2 A0 = ", Simplify[amp1$ - hand1$], "  (expect 0)"];
Print["(a) A2 - I Pi^2 [g^2/2 B0 + lambda/2 A0] = ", Simplify[amp2$ - hand2$], "  (expect 0)"];
Print["(a) A3 - I Pi^2 [g^3 C0 + g lambda/2 sum B0] = ", Simplify[amp3$ - hand3$], "  (expect 0);  C0 = ", InputForm[c03$]];
Print["(a) PaVe functions in A4: ", Union[Cases[amp4$, _D0 | _C0 | _B0 | _A0, Infinity] /. canon4$]];
Print["(a) A4 - I Pi^2 [lambda^2/2 sum B0 + 2 lambda g^2 sum C0 + g^4 sum D0] = ", Simplify[(amp4$ /. canon4$) - hand4$], "  (expect 0)"];


(* ::Section:: *)
(*(b) UV poles and MS-bar counterterms*)


poleOL$[amp_] := Simplify[SeriesCoefficient[PaXEvaluate[amp], {Epsilon, 0, -1}]/(2 Pi)^4];
v1Pole$ = poleOL$[amp1$];
v2Pole$ = poleOL$[amp2$];
v3Pole$ = poleOL$[amp3$ /. c03$ -> 0];                                  (* C0 is UV finite *)
v4Pole$ = poleOL$[amp4$ /. canon4$ /. {c0[_] -> 0, d0[_] -> 0, b0[x_] :> B0[x, m^2, m^2]}];   (* C0, D0 finite *)
Print["(b) 1/eps coefficients: V1 = ", InputForm[v1Pole$], ",  V2 = ", InputForm[v2Pole$], ",  V3 = ", InputForm[v3Pole$],
  ",  V4 = ", InputForm[v4Pole$]];
ct$ = {I D[v2Pole$, pp], -I (v2Pole$ /. pp -> 0), -I v3Pole$, -I v4Pole$} // Simplify;
Print["(b) MS-bar counterterms / DeltaUV: deltaZ, deltam, deltag, deltalambda = ", InputForm[ct$]];
Print["(b) minus the note, Eq. (5): ", Simplify[ct$ - {0, (gphi^2 + lamphi m^2)/(2 (4 Pi)^2), 3 gphi lamphi/(2 (4 Pi)^2),
     3 lamphi^2/(2 (4 Pi)^2)}], "  (expect {0, 0, 0, 0})"];


(* ::Subsubsection:: *)
(*Inspect: the poles and the counterterms*)


If[$Notebooks,
  TableForm[{{"V1 pole", TraditionalForm[v1Pole$]}, {"V2 pole", TraditionalForm[v2Pole$]}, {"V3 pole", TraditionalForm[v3Pole$]}, {"V4 pole", TraditionalForm[v4Pole$]}, {"{deltaZ, deltam, deltag, deltalambda}/DeltaUV", TraditionalForm[ct$]}}]
]


(* ::Section:: *)
(*(c) MS-bar finite parts at m = mu = g = lambda = 1*)


(* V_n^R = epsilon^0 coefficient of (2 Pi)^(2 eps) A_n/(2 Pi)^4 minus its 1/eps coefficient times (Log[4 Pi] - EulerGamma)
   (loop + MS-bar counterterm, as in the phi^3 note); the bracket of Eq. (6) is b_n = (4 Pi)^2 V_n^R / I. *)
msbarOL$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)];
bracketOL$[ampValue_] := (4 Pi)^2 msbarOL$[ampValue]/I;
logRulesOL$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
PaXEvaluate[B0[2, 1, 1]];   (* loads Package-X (context X`) *)
numPX$ = {C0[a_, b_, c_, __] :> X`ScalarC0[N[a], N[b], N[c], 1., 1., 1.],
   D0[a_, b_, c_, d_, e_, f_, __] :> X`ScalarD0[N[a], N[b], N[c], N[d], N[e], N[f], 1., 1., 1., 1.]};
pxOL$[ampNum_] := Chop[N[Simplify[bracketOL$[Quiet[PaXEvaluate[ampNum /. numPX$], PaXEvaluate::tens] /. ScaleMu -> 1] /. logRulesOL$], 20], 10^-14];
ltOL$[ampNum_] := Chop[bracketOL$[Quiet[LToolsEvaluate[ampNum], LToolsEvaluate::tens]], 10^-14];
coup$ = {m -> 1, gphi -> 1, lamphi -> 1};

rowsOL$ = {};
Do[With[{a = amp2$ /. coup$ /. pp -> x}, AppendTo[rowsOL$, {"V2", x, 0, 0, pxOL$[a], ltOL$[a /. pp -> N[x]]}]],
  {x, {-5, 0, 1, 2, 5, 10}}];
Do[With[{a = amp3$ /. coup$ /. {k1s -> pt[[1]], k2s -> pt[[2]], p3s -> pt[[3]]}},
    AppendTo[rowsOL$, {"V3", Sequence @@ pt, pxOL$[a], ltOL$[a /. {k1s -> N[pt[[1]]], k2s -> N[pt[[2]]], p3s -> N[pt[[3]]]}]}]],
  {pt, {{1, 1, -5}, {1, 1, -1}, {1, 1, 5}, {1, 1, 10}, {-1, -2, -3}}}];
Do[With[{ss = rs^2, tt = -2 (rs^2/4 - 1) (1 - c), uu = -2 (rs^2/4 - 1) (1 + c)},
    With[{a = amp4$ /. coup$ /. {s -> ss, t -> tt, u -> uu}}, AppendTo[rowsOL$, {"V4", ss, tt, 0, pxOL$[a], ltOL$[a]}]]],
  {rs, {5/2, 5, 10}}, {c, {3/10, 9/10}}];

resultsDirOL$ = FileNameJoin[{srcDirOL$, "results"}];
Quiet[CreateDirectory[resultsDirOL$]];
numStrOL$[x_] := ToString[CForm[N[x]]];
csvLinesOL$ = Prepend[
   StringRiffle[Join[{#[[1]]}, numStrOL$ /@ {#[[2]], #[[3]], #[[4]], Re[#[[5]]], Im[#[[5]]], Re[#[[6]]], Im[#[[6]]]}], ","] & /@ rowsOL$,
   "func,arg1,arg2,arg3,re_packagex,im_packagex,re_looptools,im_looptools"];
Export[FileNameJoin[{resultsDirOL$, "oneloop_mathematica.csv"}], StringRiffle[csvLinesOL$, "\n"] <> "\n", "Text"];
Print["(c) wrote ", Length[rowsOL$], " rows to results/oneloop_mathematica.csv;  max |Package-X - LoopTools| = ",
  Max[Abs[#[[5]] - #[[6]]] & /@ rowsOL$]];


(* ::Subsubsection:: *)
(*Inspect: the brackets b_n from Package-X and LoopTools*)


If[$Notebooks,
  TableForm[{#[[1]], N[#[[2]]], N[#[[3]]], N[#[[4]]], NumberForm[#[[5]], 12], NumberForm[#[[6]], 12]} & /@ rowsOL$, TableHeadings -> {None, {"func", "arg1", "arg2", "arg3", "Package-X", "LoopTools"}}]
]


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirOL$, DeleteContents -> True];
