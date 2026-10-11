(* ::Package:: *)

(* ::Title:: *)
(*Step (4): one-loop phi phi -> phi phi of phi^3 + phi^4 in d = 4 with the unpatched FeynArts 3.12 and FormCalc 9.10*)


(* ::Text:: *)
(*FormCalc 9.10 (research note models/phi34, step (4)); independent of FeynCalc.  Run in its own kernel: the*)
(*patched (FeynCalc) and unpatched FeynArts must not be loaded together.*)
(**)
(*CalcFeynAmp gives the amplitude M (default PreFactor -I (2 Pi)^-4) in terms of LoopTools'*)
(*functions B0i, C0i, D0i, whose normalization (2 Pi mu)^(4 - D)/(I Pi^2) int d^D q makes LoopTools'*)
(*Delta the note's DeltaUV.  The truncated amplitude (no tadpoles, no external-leg corrections) is*)
(*  (a) compared symbolically with the note's Eq. (9) (eq:M1);*)
(*  (b) evaluated with LoopTools (MathLink) at Delta = 0, mu = m = g = lambda = 1, i.e. in MS-bar: the MS-bar*)
(*      counterterms of Eq. (5), -sum_x [g^2 deltam/(x - m^2)^2 + 2 g deltag/(x - m^2)] - deltalambda, cancel*)
(*      exactly the Delta-dependence, which is checked by evaluating at Delta = 1 as well;*)
(*and written to Src/results/scat_formcalc.csv.*)
(**)
(*Usage:  wolframscript -file scat_formcalc.wl      (run run_model_check.sh first)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file scat_formcalc.wl  (in its own kernel: the patched FeynArts of FeynCalc must not be loaded).  Interactive:  ~/hep/bin/wopen scat_formcalc.wl  (in its own kernel: the patched FeynArts of FeynCalc must not be loaded), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


Get["FeynArts`"];
Get["FormCalc`"];

srcDirFC4$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelFC4$ = FileNameJoin[{srcDirFC4$, "generated", "Phi34_FA", "Phi34_FA"}];   (* FeynRules output, unpatched *)
workDirFC4$ = CreateDirectory[];
SetDirectory[workDirFC4$];   (* FormCalc writes its FORM files here *)


(* ::Section:: *)
(*(a) amplitude*)


diagsFC4$ = InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}],
   {S[1], S[1]} -> {S[1], S[1]}, InsertionLevel -> {Particles}, Model -> modelFC4$, GenericModel -> modelFC4$];
ampFC4$ = CalcFeynAmp[CreateFeynAmp[diagsFC4$], Dimension -> D];
exprFC4$ = Plus @@ ampFC4$;   (* Amp[process][part1, part2, ...] -> part1 + part2 + ... *)
Print["(a) number of diagrams: ", Length[CreateFeynAmp[diagsFC4$]]];
Print["(a) FormCalc amplitude: ", InputForm[exprFC4$]];
(* canonical names, valid for equal masses m and p_i^2 = m^2; Den[x, m^2] = 1/(x - m^2) *)
canonFC4$ = {D0i[dd0, m^2, m^2, m^2, m^2, a_, b_, m^2, m^2, m^2, m^2] :> d0[Sort[{a, b}]],
   C0i[cc0, m^2, m^2, x_, m^2, m^2, m^2] :> c0[x], C0i[cc0, m^2, x_, m^2, m^2, m^2, m^2] :> c0[x],
   C0i[cc0, x_, m^2, m^2, m^2, m^2, m^2] :> c0[x], B0i[bb0, x_, m^2, m^2] :> b0[x], A0i[aa0, m^2] :> a0, A0[m^2] :> a0, Den[x_, y_] :> 1/(x - y)};
handFC4$ = 1/(4 Pi)^2 (gphi^4 (d0[Sort[{S, T}]] + d0[Sort[{S, U}]] + d0[Sort[{T, U}]] +
      Sum[2 c0[x]/(x - m^2) + b0[x]/(2 (x - m^2)^2), {x, {S, T, U}}]) +
    gphi^2 lamphi Sum[2 c0[x] + (b0[x] + 2 b0[m^2])/(x - m^2) + a0/(2 (x - m^2)^2), {x, {S, T, U}}] +
    lamphi^2/2 Sum[b0[x], {x, {S, T, U}}]);
Print["(a) M (FormCalc) - Eq. (9) (eq:M1) = ", Simplify[(exprFC4$ /. canonFC4$) - handFC4$], "  (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: the 42 diagrams (unpatched FeynArts)*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diagsFC4$, ColumnsXRows -> {6, 7}, Numbering -> Simple, DisplayFunction -> Identity]]
]


(* ::Subsubsection:: *)
(*Inspect: the FormCalc amplitude collected by integral (LoopTools' B0i, C0i, D0i renamed)*)


If[$Notebooks,
  Collect[exprFC4$ /. canonFC4$, {gphi, lamphi}, Simplify] // TraditionalForm
]


(* ::Section:: *)
(*(b) numerical values with LoopTools*)


Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetMudim[1];
pointsFC4$ = Flatten[Table[Module[{ss = rs^2, p2}, p2 = ss/4 - 1;
     {rs, ct, ss, -2 p2 (1 - ct), -2 p2 (1 + ct)}], {rs, {5/2, 5, 10}}, {ct, {3/10, 9/10}}], 1];
valueFC4$[{rs_, ct_, ss_, tt_, uu_}] := exprFC4$ /. {S -> N[ss], T -> N[tt], U -> N[uu], m -> 1, gphi -> 1, lamphi -> 1} /.
   Den[x_, y_] :> 1/(x - y);
SetDelta[0];
rowsFC4$ = Join[#, {valueFC4$[#]}] & /@ pointsFC4$;
SetDelta[1];
(* Delta-dependence of M (g = lambda = m = 1): sum_x [g^2 (g^2 + lambda m^2)/(2 (x - m^2)^2) + 3 g^2 lambda/(x - m^2)]/(4 Pi)^2
   + 3 lambda^2/(2 (4 Pi)^2), removed by the counterterms of Eq. (5) *)
deltaDepFC4$ = (valueFC4$[#] - rowsFC4$[[First[Position[pointsFC4$, #]][[1]], 6]] -
      Sum[(2/(2 (x - 1)^2) + 3/(x - 1))/(4 Pi)^2, {x, #[[3 ;; 5]]}] - 3/(2 (4 Pi)^2)) & /@ pointsFC4$;
SetDelta[0];
Print["(b) M(Delta = 1) - M(Delta = 0) - (Delta coefficient of the counterterms) = ", Chop[N[deltaDepFC4$], 10^-15], "  (expect 0)"];
Print["(b) M1 (FormCalc + LoopTools, MS-bar) = ", rowsFC4$[[All, 6]]];


(* ::Subsubsection:: *)
(*Inspect: the values at the six points and the Delta check*)


If[$Notebooks,
  TableForm[MapThread[{N[#1[[1]]], N[#1[[2]]], NumberForm[#1[[6]], 12], ScientificForm[Chop[N[#2], 10^-15], 2]} &, {rowsFC4$, deltaDepFC4$}], TableHeadings -> {None, {"sqrt(s)", "cos", "M1 (MS-bar)", "Delta check"}}]
]


resultsDirFC4$ = FileNameJoin[{srcDirFC4$, "results"}];
Quiet[CreateDirectory[resultsDirFC4$]];
numStrFC4$[x_] := ToString[CForm[N[x]]];
csvLinesFC4$ = Prepend[
   StringRiffle[numStrFC4$ /@ {#[[1]], #[[2]], #[[3]], #[[4]], #[[5]], Re[#[[6]]], Im[#[[6]]]}, ","] & /@ rowsFC4$,
   "sqrts,costheta,s,t,u,re_formcalc,im_formcalc"];
Export[FileNameJoin[{resultsDirFC4$, "scat_formcalc.csv"}], StringRiffle[csvLinesFC4$, "\n"] <> "\n", "Text"];
Print["(b) wrote ", Length[rowsFC4$], " rows to results/scat_formcalc.csv"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


ResetDirectory[];
DeleteDirectory[workDirFC4$, DeleteContents -> True];
