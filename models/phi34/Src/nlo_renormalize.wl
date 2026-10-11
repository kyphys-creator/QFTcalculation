(* ::Package:: *)

(* ::Title:: *)
(*Step (5), 1 of 3: on-shell renormalization of Phi34 with FeynRules + NLOCT*)


(* ::Text:: *)
(*FeynRules + NLOCT: OnShellRenormalization[LPhi34] adds the counterterm Lagrangian*)
(*  phi -> (1 + deltaZ/2) phi,  m -> m + deltam,  gphi -> gphi + deltag,  lamphi -> lamphi + deltalambda*)
(*  (first order in FR$CT),*)
(*which is written as a FeynArts model, Src/generated/Phi34_ren/ (overwritten).*)
(*FlavorExpand -> True makes FeynRules write FR$ClassesTranslation = {phi -> S[1]}; without it the*)
(*translation is empty and NLOCT sets deltaZ of phi to zero in the phi-phi vertex (it does not*)
(*recognize S[1] as phi), leaving deltaZ undetermined.*)
(*Needs the local patch of FeynRules/Core/Loop.m (see ~/hep/README.md): unpatched,*)
(*OnShellRenormalization aborts for a model without any field mixing.*)
(**)
(*Usage:  wolframscript -file nlo_renormalize.wl     (then nlo_nloct.wl and nlo_ufo.wl;*)
(*        generate_Phi34_NLO.sh runs all three)*)


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
LoadModel["Phi34.fr"];


(* ::Section:: *)
(*on-shell renormalization with NLOCT (needs the local Core/Loop.m patch)*)


lagRenNR$ = OnShellRenormalization[LPhi34];
Print["renormalized Lagrangian: ", InputForm[lagRenNR$]];


(* ::Subsubsection:: *)
(*Inspect: the counterterm Lagrangian (the part of first order in FR$CT)*)


If[$Notebooks,
  Coefficient[Expand[lagRenNR$], FR$CT] // TraditionalForm
]


(* ::Section:: *)
(*the renormalized model as a FeynArts model, generated/Phi34_ren*)


Quiet[CreateDirectory[FileNameJoin[{srcDirNR$, "generated"}]]];
SetDirectory[FileNameJoin[{srcDirNR$, "generated"}]];
If[DirectoryQ["Phi34_ren"], DeleteDirectory["Phi34_ren", DeleteContents -> True]];
WriteFeynArtsOutput[lagRenNR$, Output -> "Phi34_ren", GenericFile -> False, FlavorExpand -> True];
Print["written: ", FileNames["*", "Phi34_ren"]];