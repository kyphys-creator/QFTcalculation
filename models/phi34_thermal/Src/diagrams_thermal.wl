(* ::Package:: *)

(* ::Title:: *)
(*The Feynman diagrams that the finite-temperature calculations evaluate*)


(* ::Text:: *)
(*Research note models/phi34_thermal.  Draws, with FeynArts and the FeynArts model of the zero-temperature note (FeynRules output in ../../phi34/Src/generated/Phi34_FA, unpatched FeynArts), the diagrams behind the finite-temperature formulas, and writes them to ../figs/diagrams/*.png, which the evaluating scripts show in their Inspect cells before they evaluate anything.*)
(*(a) One-loop 1PI diagrams of the 1-, 2-, 3- and 4-point functions (1, 2, 4, 12 diagrams).  With the hard (nonzero Matsubara) modes in the loop they give the one-loop matching of the 3D EFT (DRalgo, Matchotter: dralgo_check.wl, matchotter_check.wl, nonpert_single.py); summed with zero external momenta they are the field derivatives of the one-loop thermal potential, Eq. (12).*)
(*(b) Two-loop 1PI diagrams of the 1- and 2-point functions (3 and 9 diagrams): the NLO (two-loop) terms of the 3D tadpole and mass (DRalgo at NLO, Gould 2021 Eqs. (2.21), (2.22): dralgo_check.wl (c), (d), nonpert_single.py).*)
(*(c) Vacuum diagrams: the one-loop vacuum loop with the field-dependent mass M^2(phi) is the one-loop potential, Eq. (12) (thermal_single.py; drawn by hand, since FeynArts inserts no loop without vertices); of the two-loop vacuum diagrams (3), the figure eight with one zero-mode loop and one hard loop is the first ring (daisy) term, which the daisy sum in Eq. (13) resums.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file diagrams_thermal.wl  (in its own kernel; unpatched FeynArts); only the lines starting with (a), (b), (c) are printed.  Interactive:  ~/hep/bin/wopen diagrams_thermal.wl, then "Run All Code"; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


Get["FeynArts`"];
srcDirDG$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelDG$ = FileNameJoin[{srcDirDG$, "..", "..", "phi34", "Src", "generated", "Phi34_FA", "Phi34_FA"}];
outDirDG$ = FileNameJoin[{srcDirDG$, "..", "figs", "diagrams"}];
Quiet[CreateDirectory[outDirDG$]];
insertDG$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelDG$, GenericModel -> modelDG$];
(* all diagrams of a list of insertions as one column of drawings, 130 points per diagram column (at least 280) *)
drawDG$[diags_List, cols_List] := Column[Flatten[MapThread[
     Function[{d, c}, Show[#, ImageSize -> Max[280, 130 c[[1]]]] & /@ Render[Paint[d, ColumnsXRows -> c, Numbering -> Simple, DisplayFunction -> Identity]]],
     {diags, cols}]], Spacings -> 1];
saveDG$[name_, expr_] := Export[FileNameJoin[{outDirDG$, name <> ".png"}], Rasterize[expr, ImageResolution -> 110]];


(* ::Section:: *)
(*(a) one-loop 1PI diagrams of the 1- to 4-point functions*)


oneLoopDG$ = {
   insertDG$[CreateTopologies[1, 1 -> 0], {S[1]} -> {}],
   insertDG$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Reducible}], {S[1]} -> {S[1]}],
   insertDG$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Reducible}], {S[1]} -> {S[1], S[1]}],
   insertDG$[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Reducible}], {S[1], S[1]} -> {S[1], S[1]}]};
Print["(a) one-loop 1PI diagrams of the 1-, 2-, 3-, 4-point functions (expect 1, 2, 4, 12): ",
  Length[CreateFeynAmp[#]] & /@ oneLoopDG$];
saveDG$["oneloop", drawDG$[oneLoopDG$, {{1, 1}, {2, 1}, {4, 1}, {4, 3}}]];


(* ::Subsubsection:: *)
(*Inspect: the one-loop diagrams of the matching*)


If[$Notebooks, drawDG$[oneLoopDG$, {{1, 1}, {2, 1}, {4, 1}, {4, 3}}]]


(* ::Section:: *)
(*(b) two-loop 1PI diagrams of the 1- and 2-point functions*)


twoLoopDG$ = {
   insertDG$[CreateTopologies[2, 1 -> 0, ExcludeTopologies -> {Reducible}], {S[1]} -> {}],
   insertDG$[CreateTopologies[2, 1 -> 1, ExcludeTopologies -> {Reducible}], {S[1]} -> {S[1]}]};
Print["(b) two-loop 1PI diagrams of the 1-, 2-point functions (expect 3, 9): ", Length[CreateFeynAmp[#]] & /@ twoLoopDG$];
saveDG$["twoloop", drawDG$[twoLoopDG$, {{3, 1}, {5, 2}}]];


(* ::Subsubsection:: *)
(*Inspect: the two-loop diagrams of the NLO tadpole and mass*)


If[$Notebooks, drawDG$[twoLoopDG$, {{3, 1}, {5, 2}}]]


(* ::Section:: *)
(*(c) vacuum diagrams: the one-loop potential and the first ring (daisy) term*)


vac2DG$ = insertDG$[CreateTopologies[2, 0 -> 0], {} -> {}];
Print["(c) two-loop vacuum diagrams (expect 3: figure eight, sunset, dumbbell): ", Length[CreateFeynAmp[vac2DG$]]];
(* the one-loop vacuum loop, drawn by hand: no vertex, the propagator carries M^2(phi) + Pi (zero mode) or M^2(phi) *)
vac1DG$ = Graphics[{Dashed, Thick, Circle[{0, 0}, 1], Text[Style["\!\(\*SuperscriptBox[\(M\), \(2\)]\)(\[Phi])", 14], {0, -1.35}],
    Text[Style["one-loop vacuum loop", 12], {0, 1.45}]}, PlotRange -> {{-2, 2}, {-1.7, 1.7}}, ImageSize -> 200];
vacuumDG$ = Column[{vac1DG$, Show[First[Render[Paint[vac2DG$, ColumnsXRows -> {3, 1}, Numbering -> Simple, DisplayFunction -> Identity]]],
     ImageSize -> 480]}, Spacings -> 1];
saveDG$["vacuum", vacuumDG$];
Print["(c) wrote ../figs/diagrams/oneloop.png, twoloop.png, vacuum.png"];


(* ::Subsubsection:: *)
(*Inspect: the vacuum diagrams*)


If[$Notebooks, vacuumDG$]
