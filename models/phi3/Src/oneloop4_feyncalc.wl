(* ::Package:: *)

(* ::Title:: *)
(*Step (3): one-loop check in d = 4 (FeynArts + FeynCalc, Package-X, LoopTools)*)


(* ::Text:: *)
(*(a) FeynArts diagrams (tadpole, self-energy, triangle) from Src/generated/Phi3_FA, reduced by*)
(*    FeynCalc (TID -> PaVe).  With PreFactor -> 1 the Feynman rules predict*)
(*      A_n = I Pi^2 (gphi^n / S) PaVe,   S = 2, 2, 1,*)
(*    where FeynCalc's PaVe functions are defined by Integrate[d^D q ...] = I Pi^2 PaVe.*)
(*    The note's V_n (measure d^D q/(2 Pi)^D) is V_n = A_n/(2 Pi)^D.*)
(*(b) UV poles with Package-X (FeynHelpers): coefficient of 1/Epsilon of V_n, and the MS-bar*)
(*    counterterms of Eq. (7), delta = (1/Epsilon coefficient) x DeltaUV with*)
(*    DeltaUV = 1/Epsilon - EulerGamma + Log[4 Pi]:*)
(*    deltaZ = I d(V2pole)/d(p^2) DeltaUV, deltam = -I V2pole(p^2 = 0) DeltaUV.*)
(*(c) MS-bar finite parts (m = mu = 1).  The renormalized V_n^R (loop + MS-bar counterterm,*)
(*    Epsilon -> 0) is computed from the FeynCalc amplitudes, with the PaVe functions evaluated by*)
(*    Package-X (PaXEvaluate) and by LoopTools (LToolsEvaluate).  Dividing by the factors of*)
(*    Eq. (9) of the note, V_1^R = I g A0/(2 (4 Pi)^2), V_2^R = I g^2 B0/(2 (4 Pi)^2),*)
(*    V_3^R = I g^3 C0/(4 Pi)^2, gives the MS-bar A0, B0 and C0 (the same as LoopTools' Delta = 0*)
(*    values), written to Src/results/oneloop4_mathematica.csv.*)
(*    FeynCalc's PaVe functions are normalized by d^D q/(I Pi^2), so their Epsilon^0 parts alone*)
(*    are off by -EulerGamma - Log[Pi]: B0(FC) = 1/Epsilon - EulerGamma - Log[Pi] + B0(MS-bar).*)
(*    The (2 Pi)^(2 Epsilon) of the measure d^D q/(2 Pi)^D and the MS-bar subtraction remove this.*)
(*    Note: LoopTools 2.16 built on this Mac returns wrong C0 below threshold with p^2 != 0*)
(*    (see oneloop4_numeric.py); its C0 values are kept in the CSV as a record.*)
(**)
(*Usage:  wolframscript -file oneloop4_feyncalc.wl      (run generate_Phi3.wl first)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop4_feyncalc.wl.  Interactive:  ~/hep/bin/wopen oneloop4_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];

srcDirOL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Section:: *)
(*patched copy of the FeynRules-generated FeynArts model*)


modelTmpDirOL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOL$, "generated", "Phi3_FA"}], FileNameJoin[{modelTmpDirOL$, "Phi3_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOL$, "Phi3_FA"}], Quiet -> True];
modelOL$ = FileNameJoin[{modelTmpDirOL$, "Phi3_FA", "Phi3_FA"}];
insertOL$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles},
   Model -> modelOL$, GenericModel -> modelOL$];


(* ::Section:: *)
(*(a) diagrams and amplitudes*)


diagTadOL$ = insertOL$[CreateTopologies[1, 1 -> 0], {S[1]} -> {}];
diagSEOL$  = insertOL$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {S[1]} -> {S[1]}];
diagVtxOL$ = insertOL$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}],
   {S[1]} -> {S[1], S[1]}];


(* ::Subsubsection:: *)
(*Inspect: the three diagrams (tadpole, self-energy, triangle)*)


If[$Notebooks,
  Row[Flatten[Show[#, ImageSize -> 180] & /@ Render[Paint[#, ColumnsXRows -> 1, Numbering -> Simple, DisplayFunction -> Identity]] & /@ {diagTadOL$, diagSEOL$, diagVtxOL$}], "    "]
]


ampOL$[diags_, in_, out_] := FCE[TID[FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1],
     IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q}, ChangeDimension -> D,
     List -> False, SMP -> False, DropSumOver -> True], q, ToPaVe -> True]];

ampTadOL$ = ampOL$[diagTadOL$, {p}, {}];
ampSEOL$  = ampOL$[diagSEOL$, {p}, {p}];
ampVtxOL$ = ampOL$[diagVtxOL$, {p}, {k1, k2}];


(* ::Subsubsection:: *)
(*Inspect: each amplitude before and after the tensor reduction (TID -> PaVe)*)


If[$Notebooks,
  rawOL$[diags_, in_, out_] := FCE[FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1], IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q}, ChangeDimension -> D, List -> False, SMP -> False, DropSumOver -> True]];
  Grid[Prepend[{{"tadpole", TraditionalForm[rawOL$[diagTadOL$, {p}, {}]], TraditionalForm[ampTadOL$]}, {"self-energy", TraditionalForm[rawOL$[diagSEOL$, {p}, {p}]], TraditionalForm[ampSEOL$]}, {"triangle", TraditionalForm[rawOL$[diagVtxOL$, {p}, {k1, k2}]], TraditionalForm[ampVtxOL$]}}, {"diagram", "integrand", "after TID"}], Frame -> All, Alignment -> Left]
]


Print["(a) number of diagrams (expect 1, 1, 1): ",
  Length /@ {CreateFeynAmp[diagTadOL$], CreateFeynAmp[diagSEOL$], CreateFeynAmp[diagVtxOL$]}];
Print["(a) tadpole     A1 = ", InputForm[ampTadOL$]];
Print["(a) self-energy A2 = ", InputForm[ampSEOL$]];
Print["(a) triangle    A3 = ", InputForm[ampVtxOL$]];

c0OL$ = First[Cases[ampVtxOL$, _C0, Infinity]];
Print["(a) A1 - I Pi^2 gphi/2 A0(m^2)      = ", Simplify[ampTadOL$ - I Pi^2 gphi/2 A0[m^2]], "  (expect 0)"];
Print["(a) A2 - I Pi^2 gphi^2/2 B0(p^2,m,m) = ",
  Simplify[ampSEOL$ - I Pi^2 gphi^2/2 B0[SPD[p], m^2, m^2]], "  (expect 0)"];
Print["(a) A3 - I Pi^2 gphi^3 C0           = ", Simplify[ampVtxOL$ - I Pi^2 gphi^3 c0OL$], "  (expect 0)"];


(* ::Section:: *)
(*(b) UV poles and MS-bar counterterms*)


poleOL$[amp_] := Simplify[SeriesCoefficient[PaXEvaluate[amp], {Epsilon, 0, -1}]/(2 Pi)^4];
v1Pole$ = poleOL$[ampTadOL$];
v2Pole$ = poleOL$[ampSEOL$ /. SPD[p] -> pp] /. pp -> psq;
v3Pole$ = poleOL$[ampVtxOL$];
Print["(b) 1/eps coefficient of V1 = ", InputForm[v1Pole$], "   note: I gphi m^2/(2 (4 Pi)^2) -> ",
  Simplify[v1Pole$ - I gphi m^2/(2 (4 Pi)^2)] === 0];
Print["(b) 1/eps coefficient of V2 = ", InputForm[v2Pole$], "   note: I gphi^2/(2 (4 Pi)^2) -> ",
  Simplify[v2Pole$ - I gphi^2/(2 (4 Pi)^2)] === 0];
Print["(b) 1/eps coefficient of V3 = ", InputForm[v3Pole$], "   note: 0 -> ", v3Pole$ === 0];
Print["(b) MS-bar counterterms / DeltaUV: deltaZ = ", Simplify[I D[v2Pole$, psq]],
  ",  deltam = ", InputForm[Simplify[-I (v2Pole$ /. psq -> 0)]], "   note: 0 and gphi^2/(2 (4 Pi)^2)"];


(* ::Subsubsection:: *)
(*Inspect: the 1/eps coefficients of V1, V2, V3 and the MS-bar counterterms*)


If[$Notebooks,
  TableForm[{{"V1", TraditionalForm[v1Pole$]}, {"V2", TraditionalForm[v2Pole$]}, {"V3", TraditionalForm[v3Pole$]}, {"deltaZ/DeltaUV", TraditionalForm[Simplify[I D[v2Pole$, psq]]]}, {"deltam/DeltaUV", TraditionalForm[Simplify[-I (v2Pole$ /. psq -> 0)]]}}]
]


(* ::Section:: *)
(*(c) MS-bar finite parts (m = mu = 1)*)


(* PaXEvaluate and LToolsEvaluate return FeynCalc's PaVe functions (measure d^D q/(I Pi^2), scale
   included), so the loop part of the note's V_n is (2 Pi)^(2 Epsilon) A_n/(2 Pi)^4.  The MS-bar
   counterterm is -(1/Epsilon coefficient) DeltaUV, so V_n^R is the Epsilon^0 coefficient minus the
   1/Epsilon coefficient times (Log[4 Pi] - EulerGamma). *)
msbarOL$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)];
normOL$ = {I gphi/(2 (4 Pi)^2), I gphi^2/(2 (4 Pi)^2), I gphi^3/(4 Pi)^2};   (* Eq. (9) of the note *)
(* split the logs of 2 Pi and 4 Pi so that exact zeros (e.g. B0 at p^2 = 0 for m = mu) simplify to 0
   before N[] is applied; PowerExpand is used only on logs of positive real quantities *)
logRulesOL$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};

a0MSOL$ = Simplify[msbarOL$[PaXEvaluate[ampTadOL$]]/normOL$[[1]], m > 0 && ScaleMu > 0];
b0MSOL$ = Simplify[msbarOL$[PaXEvaluate[ampSEOL$ /. SPD[p] -> pp]]/normOL$[[2]], m > 0 && ScaleMu > 0];
Print["(c) MS-bar A0 from the tadpole = ", InputForm[a0MSOL$], "   note: m^2 (1 - Log[m^2/mu^2]) -> ",
  Simplify[PowerExpand[a0MSOL$ - m^2 (1 - Log[m^2/ScaleMu^2])]] === 0];
Print["(c) MS-bar B0 from the self-energy = ", InputForm[b0MSOL$]];
b0MSZeroOL$ = Limit[b0MSOL$, pp -> 0, Assumptions -> m > 0 && ScaleMu > 0];
Print["(c) MS-bar B0 at p^2 -> 0: ", InputForm[b0MSZeroOL$], "   note: -Log[m^2/mu^2] -> ",
  Simplify[PowerExpand[b0MSZeroOL$ + Log[m^2/ScaleMu^2]]] === 0];
Print["(c) V3^R - I gphi^3 C0/(4 Pi)^2 = ", Simplify[msbarOL$[ampVtxOL$] - normOL$[[3]] c0OL$], "  (expect 0; C0 is finite)"];


(* ::Subsubsection:: *)
(*Inspect: the MS-bar A0 and B0 from the amplitudes*)


If[$Notebooks,
  TableForm[{{"A0", TraditionalForm[a0MSOL$]}, {"B0(p^2 = pp)", TraditionalForm[b0MSOL$]}, {"B0(0)", TraditionalForm[b0MSZeroOL$]}}]
]


pxA0$ = Chop[N[Simplify[msbarOL$[PaXEvaluate[ampTadOL$ /. m -> 1] /. ScaleMu -> 1]/normOL$[[1]] /. logRulesOL$], 20]];
ltA0$ = Chop[msbarOL$[LToolsEvaluate[ampTadOL$ /. m -> 1]]/normOL$[[1]]];
pxB0$[s_] := Chop[N[Simplify[msbarOL$[PaXEvaluate[ampSEOL$ /. {SPD[p] -> s, m -> 1}] /. ScaleMu -> 1]/normOL$[[2]] /. logRulesOL$], 20]];
ltB0$[s_] := Chop[msbarOL$[LToolsEvaluate[ampSEOL$ /. {SPD[p] -> s, m -> 1}]]/normOL$[[2]]];
(* C0 is finite, so its MS-bar value is C0 itself.  FeynHelpers' PaXEvaluate[..., PaXC0Expand -> True]
   returns a ConditionalExpression that is Undefined below threshold, so Package-X's own numerical
   ScalarC0 (loaded by FeynHelpers) is used. *)
PaXEvaluate[B0[2, 1, 1]];   (* makes sure Package-X (context X`) is loaded *)
pxC0$[a_, b_, c_] := Chop[N[X`ScalarC0[a, b, c, 1, 1, 1], 20], 10^-18];
ltC0$[a_, b_, c_] := Chop[LToolsEvaluate[C0[a, b, c, 1, 1, 1]]];

rowsOL$ = {{"A0", 1, 0, 0, pxA0$, ltA0$}};
Do[AppendTo[rowsOL$, {"B0", s, 1, 1, pxB0$[s], ltB0$[N[s]]}],
  {s, {-10, -5, -1, 0, 1, 2, 3, 39/10, 4, 41/10, 5, 8, 12, 20, 30}}];
Do[AppendTo[rowsOL$, {"C0", Sequence @@ inv, pxC0$[Sequence @@ inv], ltC0$[Sequence @@ (N /@ inv)]}],
  {inv, {{0, 0, 0}, {1, 1, 1}, {1, 1, 7/2}, {1, 1, 5}, {1, 1, 10}}}];

resultsDirOL$ = FileNameJoin[{srcDirOL$, "results"}];
Quiet[CreateDirectory[resultsDirOL$]];
numStrOL$[x_] := ToString[CForm[N[x]]];   (* machine-precision decimal, 16-17 digits *)
csvLinesOL$ = Prepend[
   StringRiffle[Join[{#[[1]]}, numStrOL$ /@ {#[[2]], #[[3]], #[[4]], Re[#[[5]]], Im[#[[5]]], Re[#[[6]]], Im[#[[6]]]}], ","] & /@ rowsOL$,
   "func,arg1,arg2,arg3,re_packagex,im_packagex,re_looptools,im_looptools"];
Export[FileNameJoin[{resultsDirOL$, "oneloop4_mathematica.csv"}], StringRiffle[csvLinesOL$, "\n"] <> "\n", "Text"];
Print["(c) wrote ", Length[rowsOL$], " rows to results/oneloop4_mathematica.csv"];
Print["(c) max |Package-X - LoopTools| for A0, B0 = ", Max[Abs[#[[5]] - #[[6]]] & /@ Select[rowsOL$, #[[1]] =!= "C0" &]]];
Print["(c) |Package-X - LoopTools| for C0 rows = ", Abs[#[[5]] - #[[6]]] & /@ Select[rowsOL$, #[[1]] === "C0" &]];


(* ::Subsubsection:: *)
(*Inspect: the values (LoopTools C0 is wrong below threshold, step (3))*)


If[$Notebooks,
  TableForm[{#[[1]], N[#[[2]]], N[#[[3]]], N[#[[4]]], NumberForm[#[[5]], 12], NumberForm[#[[6]], 12]} & /@ rowsOL$, TableHeadings -> {None, {"func", "arg1", "arg2", "arg3", "Package-X", "LoopTools"}}]
]


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirOL$, DeleteContents -> True];
