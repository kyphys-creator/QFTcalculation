(* ::Package:: *)

(* ::Title:: *)
(*Step (5), 1 of 3: on-shell renormalization of QCD with FeynRules + NLOCT*)


(* ::Text:: *)
(*FeynRules + NLOCT: OnShellRenormalization[LQCD, QCDOnly -> True, FlavorMixing -> False] adds the counterterm Lagrangian of the strong sector*)
(*(first order in FR$CT): the gluon, ghost and quark fields G -> (1 + deltaZG/2) G, ..., the heavy-quark mass*)
(*MT -> MT + deltaMT and the coupling aS -> aS + deltaaS.  The photon and the electron are not renormalized (they are*)
(*only the external probe of the note).  The result is written as a FeynArts model, Src/generated/QCD_ren/*)
(*(overwritten).  Research note models/qcd, step (5).  The gauge-fixing term is not part of the Lagrangian: NLOCT*)
(*computes the loops with the Feynman-gauge gluon propagator of FeynArts' generic model.*)
(*FlavorExpand -> True makes FeynRules write FR$ClassesTranslation; without it NLOCT does not recognize the fields.*)
(*Needs the local patch of FeynRules/Core/Loop.m (~/hep/README.md).*)
(**)
(*Usage:  wolframscript -file nlo_renormalize.wl     (then nlo_nloct.wl and nlo_ufo.wl; generate_QCD_NLO.sh runs all three)*)


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
LoadModel["QCD.fr"];


(* ::Section:: *)
(*on-shell renormalization with NLOCT (QCD only)*)


lagRenNR$ = OnShellRenormalization[LQCD, QCDOnly -> True, FlavorMixing -> False];
Print["renormalized parameters and fields: ", Union[Cases[lagRenNR$, (FR$deltaZ | FR$delta)[__], Infinity]]];


(* ::Subsubsection:: *)
(*Inspect: the counterterm Lagrangian (the part of first order in FR$CT)*)


If[$Notebooks,
  Short[Coefficient[Expand[lagRenNR$], FR$CT], 30]
]


(* ::Section:: *)
(*the renormalized model as a FeynArts model, generated/QCD_ren*)


Quiet[CreateDirectory[FileNameJoin[{srcDirNR$, "generated"}]]];
SetDirectory[FileNameJoin[{srcDirNR$, "generated"}]];
If[DirectoryQ["QCD_ren"], DeleteDirectory["QCD_ren", DeleteContents -> True]];
WriteFeynArtsOutput[lagRenNR$, Output -> "QCD_ren", GenericFile -> False, FlavorExpand -> True];
Print["written: ", FileNames["*", "QCD_ren"]];
