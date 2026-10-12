(* ::Package:: *)

(* ::Title:: *)
(*Step (5), 1 of 3: on-shell renormalization of PsYukawa with FeynRules + NLOCT*)


(* ::Text:: *)
(*FeynRules + NLOCT: OnShellRenormalization[LPsYukawa] adds the counterterm Lagrangian*)
(*  phi -> (1 + deltaZphi/2) phi,  psi -> (1 + deltaZpsi/2) psi,  mphi -> mphi + deltamphi,  Mpsi -> Mpsi + deltaMpsi,*)
(*  yps -> yps + deltayps,  lamphi -> lamphi + deltalamphi   (first order in FR$CT),*)
(*which is written as a FeynArts model, Src/generated/PsYukawa_ren/ (overwritten).*)
(*FlavorExpand -> True makes FeynRules write FR$ClassesTranslation (see the phi^3 + phi^4 note); without it NLOCT does*)
(*not recognize the fields.  Needs the local patch of FeynRules/Core/Loop.m (~/hep/README.md): unpatched,*)
(*OnShellRenormalization aborts for a model without any field mixing.*)
(**)
(*Usage:  wolframscript -file nlo_renormalize.wl     (then nlo_nloct.wl and nlo_ufo.wl; generate_PsYukawa_NLO.sh runs all three)*)


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
LoadModel["PsYukawa.fr"];


(* ::Section:: *)
(*on-shell renormalization with NLOCT (needs the local Core/Loop.m patch)*)


lagRenNR$ = OnShellRenormalization[LPsYukawa];
Print["renormalized Lagrangian: ", InputForm[lagRenNR$]];


(* ::Subsubsection:: *)
(*Inspect: the counterterm Lagrangian (the part of first order in FR$CT)*)


If[$Notebooks,
  Coefficient[Expand[lagRenNR$], FR$CT] // TraditionalForm
]


(* ::Section:: *)
(*the renormalized model as a FeynArts model, generated/PsYukawa_ren*)


Quiet[CreateDirectory[FileNameJoin[{srcDirNR$, "generated"}]]];
SetDirectory[FileNameJoin[{srcDirNR$, "generated"}]];
If[DirectoryQ["PsYukawa_ren"], DeleteDirectory["PsYukawa_ren", DeleteContents -> True]];
WriteFeynArtsOutput[lagRenNR$, Output -> "PsYukawa_ren", GenericFile -> False, FlavorExpand -> True];
Print["written: ", FileNames["*", "PsYukawa_ren"]];
