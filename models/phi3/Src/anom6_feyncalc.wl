(* ::Package:: *)

(* ::Title:: *)
(*Step (10): d = 6 renormalized two- and three-point functions at several mu (field anomalous dimension)*)


(* ::Text:: *)
(*field anomalous dimension (research note, step (10)).*)
(**)
(*The FeynArts self-energy and vertex amplitudes are read in D = 6 - 2 Epsilon through the dimension shift*)
(*PaVe^(D+2) = -2 Pi PaVe_00^(D) (as in oneloop6_feyncalc.wl), and the MS-bar finite parts*)
(*  B0^(6)(p^2) and C0^(6)(p1^2, p2^2, p3^2)     (note, Eqs. (11)-(12): V_2 = I g^2 B0^(6)/(2K), V_3 = I g^3 C0^(6)/K)*)
(*are evaluated with Package-X and LoopTools at m = 1 and mu = 1, 1/2, 2 -> Src/results/anom6_feyncalc.csv.*)
(*LoopTools' C00 inherits its C0 error below threshold (note, step (3)); its C0^(6) values are written as a record only.*)
(**)
(*Usage:  wolframscript -file anom6_feyncalc.wl      (run generate_Phi3.wl first)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file anom6_feyncalc.wl.  Interactive:  ~/hep/bin/wopen anom6_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];

srcDirA6$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

modelTmpDirA6$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirA6$, "generated", "Phi3_FA"}], FileNameJoin[{modelTmpDirA6$, "Phi3_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirA6$, "Phi3_FA"}], Quiet -> True];
modelA6$ = FileNameJoin[{modelTmpDirA6$, "Phi3_FA", "Phi3_FA"}];
insertA6$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelA6$, GenericModel -> modelA6$];

(* ::Section:: *)
(*(a) self-energy and vertex amplitudes*)


diagSEA6$  = insertA6$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {S[1]} -> {S[1]}];
diagVtxA6$ = insertA6$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], {S[1]} -> {S[1], S[1]}];


(* ::Subsubsection:: *)
(*Inspect: the self-energy and vertex diagrams*)


If[$Notebooks,
  Row[Flatten[Show[#, ImageSize -> 200] & /@ Render[Paint[#, ColumnsXRows -> 1, Numbering -> Simple, DisplayFunction -> Identity]] & /@ {diagSEA6$, diagVtxA6$}], "    "]
]


ampA6$[diags_, in_, out_] := FCE[TID[FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1],
     IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q}, ChangeDimension -> D,
     List -> False, SMP -> False, DropSumOver -> True], q, ToPaVe -> True]];
ampSEA6$  = ampA6$[diagSEA6$, {p}, {p}];
ampVtxA6$ = ampA6$[diagVtxA6$, {p}, {k1, k2}];
Print["(a) self-energy and vertex amplitudes (expect I Pi^2 gphi^2/2 B0, I Pi^2 gphi^3 C0): ",
  InputForm /@ {ampSEA6$, ampVtxA6$}];


(* ::Section:: *)
(*(b) the MS-bar finite parts B0^(6), C0^(6) and their mu-dependence*)


kA6$ = (4 Pi)^3;
shiftA6$ = {B0[s_, a_, b_] :> -2 Pi PaVe[0, 0, {s}, {a, b}],
   C0[s1_, s2_, s3_, a_, b_, c_] :> -2 Pi PaVe[0, 0, {s1, s2, s3}, {a, b, c}]};
msbarSeriesA6$[expr_] := Module[{s = Series[expr, {Epsilon, 0, 0}]},
   {SeriesCoefficient[s, -1], SeriesCoefficient[s, 0] - SeriesCoefficient[s, -1] (Log[4 Pi] - EulerGamma)}];
(* V_n = A_n/(2 Pi)^D with D = 6 - 2 Epsilon; {1/Epsilon coefficient, MS-bar finite part} *)
msbar6A6$[ampValue_] := msbarSeriesA6$[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^6];
normA6$ = {I gphi^2/(2 kA6$), I gphi^3/kA6$};      (* V_2^R = norm_1 B0^(6), V_3^R = norm_2 C0^(6) *)
logRulesA6$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};

(* Package-X: the finite parts as functions of mu, then numbers *)
b06PXA6$ = Simplify[msbar6A6$[PaXEvaluate[ampSEA6$ /. shiftA6$ /. SPD[p] -> psq]][[2]]/normA6$[[1]] /. ScaleMu -> mu, m > 0 && mu > 0];
Print["(b) Package-X: mu d B0^(6)/d mu = ", InputForm[Simplify[mu D[b06PXA6$, mu]]], "  (note: -2 (m^2 - p^2/6))"];
PaXEvaluate[B0[2, 1, 1]];
c0ToPXA6$ = C0[s1_, s2_, s3_, a_, b_, c_] :> X`ScalarC0[N[s1], N[s2], N[s3], Sqrt[N[a]], Sqrt[N[b]], Sqrt[N[c]]];
vtxAtA6$[s1_, s2_, s3_] := ampVtxA6$ /. {SPD[k1, k1] -> s1, SPD[k2, k2] -> s2, SPD[k1, k2] -> (s3 - s1 - s2)/2} /. m -> 1;
(* the point is substituted before PaXEvaluate: the symbolic form in psq is 0/0 at psq = 0 *)
pxB06A6$[s_, muv_] := Chop[N[msbar6A6$[PaXEvaluate[ampSEA6$ /. shiftA6$ /. {SPD[p] -> s, m -> 1}]][[2]]/normA6$[[1]]
      /. ScaleMu -> muv /. logRulesA6$, 20], 10^-18];
pxC06A6$[inv_, muv_] := Chop[N[(msbar6A6$[PaXEvaluate[vtxAtA6$ @@ inv /. shiftA6$]][[2]]/normA6$[[2]] /. ScaleMu -> muv
      /. logRulesA6$) /. c0ToPXA6$, 20], 10^-18];
Print["(b) Package-X: mu d C0^(6)/d mu at (1,1,1) (note: -1) = ",
  Chop[(pxC06A6$[{1, 1, 1}, 1 + 10^-6] - pxC06A6$[{1, 1, 1}, 1 - 10^-6])/(Log[1 + 10^-6] - Log[1 - 10^-6]), 10^-8]];


(* ::Subsubsection:: *)
(*Inspect: B0^(6) and its mu-dependence; the p^2 term of mu dB0^(6)/dmu gives gamma_phi (step (10))*)


If[$Notebooks,
  TableForm[{{"B0^(6)(p^2 = psq)", TraditionalForm[b06PXA6$]}, {"mu dB0^(6)/dmu", TraditionalForm[Simplify[mu D[b06PXA6$, mu]]]}}]
]


(* LoopTools *)
ltA6$[n_, amp_, muv_] := Module[{v = Chop[msbar6A6$[LToolsEvaluate[amp /. shiftA6$, LToolsSetMudim -> muv^2]][[2]]/normA6$[[n]]]},
   If[NumericQ[v], v, Indeterminate]];


(* ::Section:: *)
(*(c) values at mu = 1, 1/2, 2 with Package-X and LoopTools*)


p2ListA6$ = {-5, -1, 0, 1, 2, 3, 5, 8};
invListA6$ = {{0, 0, 0}, {1, 1, 1}, {1, 1, 7/2}, {1, 1, 5}};
rowsA6$ = Join[
   Flatten[Table[{"B06", s, 1, 1, muv, pxB06A6$[s, muv], ltA6$[1, ampSEA6$ /. {SPD[p] -> s, m -> 1}, muv]},
     {muv, {1, 1/2, 2}}, {s, p2ListA6$}], 1],
   Flatten[Table[{"C06", Sequence @@ inv, muv, pxC06A6$[inv, muv], ltA6$[2, vtxAtA6$ @@ inv, muv]},
     {muv, {1, 1/2, 2}}, {inv, invListA6$}], 1]];


(* ::Subsubsection:: *)
(*Inspect: the values (LoopTools C0^(6) below threshold is wrong, its mu-dependence is right)*)


If[$Notebooks,
  TableForm[{#[[1]], N[#[[2]]], N[#[[3]]], N[#[[4]]], N[#[[5]]], NumberForm[#[[6]], 10], If[#[[7]] === Indeterminate, "NaN", NumberForm[#[[7]], 10]]} & /@ rowsA6$, TableHeadings -> {None, {"X", "arg1", "arg2", "arg3", "mu", "Package-X", "LoopTools"}}]
]


numStrA6$[x_] := If[x === Indeterminate, "nan", ToString[CForm[N[x]]]];
csvA6$ = Prepend[
   StringRiffle[Join[{#[[1]]}, numStrA6$ /@ {#[[2]], #[[3]], #[[4]], #[[5]], Re[#[[6]]], Im[#[[6]]],
        If[#[[7]] === Indeterminate, Indeterminate, Re[#[[7]]]], If[#[[7]] === Indeterminate, Indeterminate, Im[#[[7]]]]}], ","] & /@ rowsA6$,
   "func,arg1,arg2,arg3,mu,re_packagex,im_packagex,re_looptools,im_looptools"];
Quiet[CreateDirectory[FileNameJoin[{srcDirA6$, "results"}]]];
Export[FileNameJoin[{srcDirA6$, "results", "anom6_feyncalc.csv"}], StringRiffle[csvA6$, "\n"] <> "\n", "Text"];
Print["(c) wrote ", Length[rowsA6$], " rows to results/anom6_feyncalc.csv"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirA6$, DeleteContents -> True];
