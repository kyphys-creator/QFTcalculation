(* ::Package:: *)

(* ::Title:: *)
(*Step (6), 1 of 3: on-shell renormalization of Phi3 with FeynRules + NLOCT*)


(* ::Text:: *)
(*FeynRules + NLOCT: OnShellRenormalization[LPhi3] adds the counterterm Lagrangian*)
(*  phi -> (1 + deltaZ/2) phi,  m -> m + deltam,  gphi -> gphi + deltag   (first order in FR$CT),*)
(*which is written as a FeynArts model, Src/generated/Phi3_ren/ (overwritten).*)
(*FlavorExpand -> True makes FeynRules write FR$ClassesTranslation = {phi -> S[1]}; without it the*)
(*translation is empty and NLOCT sets deltaZ of phi to zero in the phi-phi vertex (it does not*)
(*recognize S[1] as phi), leaving deltaZ undetermined.*)
(*Needs the local patch of FeynRules/Core/Loop.m (see ~/hep/README.md): unpatched,*)
(*OnShellRenormalization aborts for a model without any field mixing.*)
(**)
(*Usage:  wolframscript -file nlo_renormalize.wl     (then nlo_nloct.wl and nlo_ufo.wl;*)
(*        generate_Phi3_NLO.sh runs all three)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file nlo_renormalize.wl  (in a fresh kernel).  Interactive:  ~/hep/bin/wopen nlo_renormalize.wl  (in a fresh kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


srcDirNR$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

(* ::Section:: *)
(*FeynRules and the model*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNR$];
LoadModel["Phi3.fr"];


(* ::Section:: *)
(*on-shell renormalization with NLOCT (needs the local Core/Loop.m patch)*)


lagRenNR$ = OnShellRenormalization[LPhi3];
Print["renormalized Lagrangian: ", InputForm[lagRenNR$]];


(* ::Subsubsection:: *)
(*Inspect: the counterterm Lagrangian (the part of first order in FR$CT)*)


If[$Notebooks,
  Coefficient[Expand[lagRenNR$], FR$CT] // TraditionalForm
]


(* ::Section:: *)
(*the renormalized model as a FeynArts model, generated/Phi3_ren*)


Quiet[CreateDirectory[FileNameJoin[{srcDirNR$, "generated"}]]];
SetDirectory[FileNameJoin[{srcDirNR$, "generated"}]];
If[DirectoryQ["Phi3_ren"], DeleteDirectory["Phi3_ren", DeleteContents -> True]];
WriteFeynArtsOutput[lagRenNR$, Output -> "Phi3_ren", GenericFile -> False, FlavorExpand -> True];
Print["written: ", FileNames["*", "Phi3_ren"]];