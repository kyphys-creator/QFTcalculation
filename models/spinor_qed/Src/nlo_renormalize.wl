(* ::Package:: *)

(* ::Title:: *)
(*Step (5), 1 of 3: on-shell renormalization of spinor QED with FeynRules + NLOCT*)


(* ::Text:: *)
(*FeynRules + NLOCT: OnShellRenormalization[LSpinorQED] adds the counterterm Lagrangian*)
(*  A -> (1 + deltaZA/2) A,  elec -> (1 + deltaZe/2) elec,  muon -> (1 + deltaZmu/2) muon,*)
(*  Me -> Me + deltaMe,  MMU -> MMU + deltaMMU,  ee -> ee + deltaee   (first order in FR$CT),*)
(*which is written as a FeynArts model, Src/generated/SpinorQED_ren/ (overwritten).  Research note models/spinor_qed,*)
(*step (5).  The gauge-fixing term is not part of the Lagrangian: NLOCT computes the loops with the Feynman-gauge*)
(*photon propagator of FeynArts' generic model.*)
(*FlavorExpand -> True makes FeynRules write FR$ClassesTranslation; without it NLOCT does not recognize the fields.*)
(*Needs the local patch of FeynRules/Core/Loop.m (~/hep/README.md): unpatched, OnShellRenormalization aborts for a*)
(*model without any field mixing.*)
(**)
(*Usage:  wolframscript -file nlo_renormalize.wl     (then nlo_nloct.wl and nlo_ufo.wl; generate_SpinorQED_NLO.sh runs all three)*)


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
LoadModel["SpinorQED.fr"];


(* ::Section:: *)
(*on-shell renormalization with NLOCT (needs the local Core/Loop.m patch)*)


lagRenNR$ = OnShellRenormalization[LSpinorQED];
Print["renormalized Lagrangian: ", InputForm[lagRenNR$]];


(* ::Subsubsection:: *)
(*Inspect: the counterterm Lagrangian (the part of first order in FR$CT)*)


If[$Notebooks,
  Coefficient[Expand[lagRenNR$], FR$CT] // TraditionalForm
]


(* ::Section:: *)
(*the renormalized model as a FeynArts model, generated/SpinorQED_ren*)


Quiet[CreateDirectory[FileNameJoin[{srcDirNR$, "generated"}]]];
SetDirectory[FileNameJoin[{srcDirNR$, "generated"}]];
If[DirectoryQ["SpinorQED_ren"], DeleteDirectory["SpinorQED_ren", DeleteContents -> True]];
WriteFeynArtsOutput[lagRenNR$, Output -> "SpinorQED_ren", GenericFile -> False, FlavorExpand -> True];
Print["written: ", FileNames["*", "SpinorQED_ren"]];
