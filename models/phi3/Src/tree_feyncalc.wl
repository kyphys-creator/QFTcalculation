(* ::Package:: *)

(* ::Title:: *)
(*Step (2): tree-level phi phi -> phi phi with FeynArts + FeynCalc*)


(* ::Text:: *)
(*Research note, step (2): compare with Eq. (16) (eq:Mtree), M = -g^2 [1/(s-m^2)+1/(t-m^2)+1/(u-m^2)].  Uses the FeynArts model in Src/generated/Phi3_FA (run generate_Phi3.wl first).  A copy is patched with FAPatch in a temporary directory, so the committed files are not modified.  Momenta: p1 p2 -> k1 k2;  s = (p1+p2)^2, t = (p1-k1)^2, u = (p1-k2)^2.  FeynArts' default PreFactor -I turns the sum of diagrams (i M) into M itself.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file tree_feyncalc.wl.  Interactive:  ~/hep/bin/wopen tree_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];


srcDirTree$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Text:: *)
(*A patched copy of the FeynRules-generated FeynArts model.*)


modelTmpDirTree$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTree$, "generated", "Phi3_FA"}], FileNameJoin[{modelTmpDirTree$, "Phi3_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirTree$, "Phi3_FA"}], Quiet -> True];
modelFileTree$ = FileNameJoin[{modelTmpDirTree$, "Phi3_FA", "Phi3_FA"}];


(* ::Section:: *)
(*Diagrams and amplitude*)


diagsTree$ = InsertFields[CreateTopologies[0, 2 -> 2], {S[1], S[1]} -> {S[1], S[1]},
   InsertionLevel -> {Particles}, Model -> modelFileTree$, GenericModel -> modelFileTree$];


(* ::Subsubsection:: *)
(*Inspect: the three diagrams (s, t, u channels)*)


If[$Notebooks,
  Show[#, ImageSize -> 480] & /@ Render[Paint[diagsTree$, ColumnsXRows -> {3, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampTree$ = FCFAConvert[CreateFeynAmp[diagsTree$], IncomingMomenta -> {p1, p2},
   OutgoingMomenta -> {k1, k2}, ChangeDimension -> 4, List -> True, SMP -> False];
Print["number of tree diagrams (expect 3): ", Length[ampTree$]];
Print["amplitudes per diagram: ", InputForm /@ ampTree$];


(* ::Subsubsection:: *)
(*Inspect: the amplitude of each diagram*)


If[$Notebooks,
  TableForm[Transpose[{Range[Length[ampTree$]], TraditionalForm[FCE[#]] & /@ ampTree$}], TableHeadings -> {None, {"diagram", "M"}}]
]


FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, m, m, m, m];
mTreeFC$ = Simplify[FeynAmpDenominatorExplicit[Total[ampTree$]]];
Print["M (FeynCalc) = ", InputForm[mTreeFC$]];


(* ::Section:: *)
(*Comparison with the note, Eq. (16) (eq:Mtree)*)


mTreeNote$ = -gphi^2 (1/(s - m^2) + 1/(t - m^2) + 1/(u - m^2));
Print["M(FeynCalc) - M(note, Eq. 11) = ", Simplify[mTreeFC$ - mTreeNote$], "   (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: FeynCalc's sum and the note's formula*)


If[$Notebooks,
  {mTreeFC$, mTreeNote$} // TraditionalForm
]


(* ::Text:: *)
(*One numerical point for the MadGraph / Python comparison: sqrt(s) = 5, cos(theta) = 0.3, m = g = 1.*)


With[{sv = 25., mv = 1., c = 0.3},
  Module[{p2cm = sv/4 - mv^2, tv, uv},
    tv = -2 p2cm (1 - c); uv = -2 p2cm (1 + c);
    Print["M at sqrt(s)=5, cos(theta)=0.3, m=g=1: ", mTreeFC$ /. {s -> sv, t -> tv, u -> uv, m -> mv, gphi -> 1.}]]];


(* ::Section:: *)
(*Cleanup*)


DeleteDirectory[modelTmpDirTree$, DeleteContents -> True];
