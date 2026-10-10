(* ::Package:: *)

(* ::Title:: *)
(*Step (6), 2 of 3: UV counterterms with the unpatched FeynArts and NLOCT (WriteCT)*)


(* ::Text:: *)
(*Unpatched FeynArts 3.12 + NLOCT 1.02 (from the FeynRules folder), in a kernel without FeynRules:*)
(*WriteCT computes the UV counterterms of Src/generated/Phi3_ren with on-shell conditions for the*)
(*mass and the field and MS-bar for gphi (NLOCT's default), and writes Src/generated/Phi3_CT.nlo.*)
(*The scalar theory has no R2 vertices; NLOCT then writes the malformed R2$vertlist = {Last[{}]},*)
(*which nlo_ufo.wl removes.  (NLOCT's MSbar -> True option is not used: for this model it returns*)
(*a two-point counterterm without the factor -I, so the poles do not cancel in MadLoop.)*)
(**)
(*Usage:  wolframscript -file nlo_nloct.wl     (after nlo_renormalize.wl)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file nlo_nloct.wl  (in a fresh kernel without FeynRules).  Interactive:  ~/hep/bin/wopen nlo_nloct.wl  (in a fresh kernel without FeynRules), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


srcDirNC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

(* ::Section:: *)
(*unpatched FeynArts and NLOCT: the UV counterterms (WriteCT)*)


SetDirectory[FileNameJoin[{srcDirNC$, "generated"}]];
Get["FeynArts`"];
Get[FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules", "NLOCT.m"}]];
WriteCT[FileNameJoin[{Directory[], "Phi3_ren", "Phi3_ren"}], "Lorentz", Output -> "Phi3_CT"];
Print["written: ", FileNames["Phi3_CT.nlo"]];


(* ::Subsubsection:: *)
(*Inspect: the start of generated/Phi3_CT.nlo*)


If[$Notebooks,
  StringTake[Import[FileNameJoin[{Directory[], "Phi3_CT.nlo"}], "Text"], UpTo[3000]]
]
