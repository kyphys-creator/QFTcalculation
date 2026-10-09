(* ::Package:: *)

(* oneloop4_feyncalc.wl -- one-loop check in d = 4 (research note, step (3)).

   (a) FeynArts diagrams (tadpole, self-energy, triangle) from Src/generated/Phi3_FA, reduced by
       FeynCalc (TID -> PaVe).  With PreFactor -> 1 the Feynman rules predict
         A_n = I Pi^2 (gphi^n / S) PaVe,   S = 2, 2, 1,
       where FeynCalc's PaVe functions are defined by Integrate[d^D q ...] = I Pi^2 PaVe.
       The note's V_n (measure d^D q/(2 Pi)^D) is V_n = A_n/(2 Pi)^D.
   (b) UV poles with Package-X (FeynHelpers): coefficient of 1/Epsilon of V_n, and the MS
       counterterms of Eq. (7): deltaZ = I d(V2pole)/d(p^2), deltam = -I V2pole(p^2 = 0).
   (c) finite parts of A0, B0 and C0 in LoopTools' convention (Delta = 0, mu = 1) from Package-X
       (PaXEvaluate) and LoopTools (LToolsEvaluate), written to Src/results/oneloop4_mathematica.csv.
       Note: LoopTools 2.16 built on this Mac returns wrong C0 below threshold with p^2 != 0
       (see oneloop4_numeric.py); its C0 values are kept in the CSV as a record.
       FeynCalc's normalization is B0(FC) = 1/Epsilon - EulerGamma - Log[Pi] + B0(LoopTools), and
       likewise A0(FC) = m^2 (1/Epsilon - EulerGamma - Log[Pi]) + A0(LoopTools); C0 is finite.

   Usage:  wolframscript -file oneloop4_feyncalc.wl      (run generate_Phi3.wl first) *)

$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];

srcDirOL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

(* ---------- patched copy of the FeynRules-generated FeynArts model ---------- *)
modelTmpDirOL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOL$, "generated", "Phi3_FA"}], FileNameJoin[{modelTmpDirOL$, "Phi3_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOL$, "Phi3_FA"}], Quiet -> True];
modelOL$ = FileNameJoin[{modelTmpDirOL$, "Phi3_FA", "Phi3_FA"}];
insertOL$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles},
   Model -> modelOL$, GenericModel -> modelOL$];

(* ---------- (a) diagrams and amplitudes ---------- *)
diagTadOL$ = insertOL$[CreateTopologies[1, 1 -> 0], {S[1]} -> {}];
diagSEOL$  = insertOL$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {S[1]} -> {S[1]}];
diagVtxOL$ = insertOL$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}],
   {S[1]} -> {S[1], S[1]}];

ampOL$[diags_, in_, out_] := FCE[TID[FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1],
     IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q}, ChangeDimension -> D,
     List -> False, SMP -> False, DropSumOver -> True], q, ToPaVe -> True]];

ampTadOL$ = ampOL$[diagTadOL$, {p}, {}];
ampSEOL$  = ampOL$[diagSEOL$, {p}, {p}];
ampVtxOL$ = ampOL$[diagVtxOL$, {p}, {k1, k2}];

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

(* ---------- (b) UV poles and MS counterterms ---------- *)
poleOL$[amp_] := Simplify[SeriesCoefficient[PaXEvaluate[amp], {Epsilon, 0, -1}]/(2 Pi)^4];
v1Pole$ = poleOL$[ampTadOL$];
v2Pole$ = poleOL$[ampSEOL$ /. SPD[p] -> pp] /. pp -> psq;
v3Pole$ = poleOL$[ampVtxOL$];
Print["(b) 1/eps coefficient of V1 = ", InputForm[v1Pole$], "   note: I gphi m^2/(2 (4 Pi)^2) -> ",
  Simplify[v1Pole$ - I gphi m^2/(2 (4 Pi)^2)] === 0];
Print["(b) 1/eps coefficient of V2 = ", InputForm[v2Pole$], "   note: I gphi^2/(2 (4 Pi)^2) -> ",
  Simplify[v2Pole$ - I gphi^2/(2 (4 Pi)^2)] === 0];
Print["(b) 1/eps coefficient of V3 = ", InputForm[v3Pole$], "   note: 0 -> ", v3Pole$ === 0];
Print["(b) MS counterterms x eps: deltaZ = ", Simplify[I D[v2Pole$, psq]],
  ",  deltam = ", InputForm[Simplify[-I (v2Pole$ /. psq -> 0)]], "   note: 0 and gphi^2/(2 (4 Pi)^2)"];

(* ---------- (c) finite parts in LoopTools' convention (m = mu = 1) ---------- *)
toLTOL$[fcValue_, mass2_] := Chop[N[SeriesCoefficient[fcValue, {Epsilon, 0, 0}] + mass2 (EulerGamma + Log[Pi]), 20]];
pxB0$[s_] := toLTOL$[PaXEvaluate[B0[s, 1, 1]] /. ScaleMu -> 1, 1];
ltB0$[s_] := Chop[(LToolsEvaluate[B0[s, 1, 1]] /. Epsilon -> Infinity) + EulerGamma + Log[Pi]];
(* For C0, FeynHelpers' PaXEvaluate[..., PaXC0Expand -> True] returns a ConditionalExpression that is
   Undefined below threshold, so Package-X's own numerical ScalarC0 (loaded by FeynHelpers) is used. *)
PaXEvaluate[B0[2, 1, 1]];   (* makes sure Package-X (context X`) is loaded *)
pxC0$[a_, b_, c_] := Chop[N[X`ScalarC0[a, b, c, 1, 1, 1], 20], 10^-18];
ltC0$[a_, b_, c_] := Chop[LToolsEvaluate[C0[a, b, c, 1, 1, 1]]];

rowsOL$ = {{"A0", 1, 0, 0, toLTOL$[PaXEvaluate[A0[1]] /. ScaleMu -> 1, 1],
    Chop[(LToolsEvaluate[A0[1]] /. Epsilon -> Infinity) + EulerGamma + Log[Pi]]}};
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

LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirOL$, DeleteContents -> True];
