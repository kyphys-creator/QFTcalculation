(* ::Package:: *)

(* ::Title:: *)
(*Step (5), 2 of 3: UV counterterms with the unpatched FeynArts and NLOCT (WriteCT)*)


(* ::Text:: *)
(*Unpatched FeynArts 3.12 + NLOCT 1.02 (from the FeynRules folder), in a kernel without FeynRules: WriteCT computes the*)
(*UV counterterms of Src/generated/SpinorQED_ren with on-shell conditions for the masses and the fields (NLOCT's*)
(*default; the fermion field constants carry the infrared pole, which NLOCT marks with FR$IR and then sets FR$IR -> 1)*)
(*and MS-bar for the charge ee, and the R2 vertices (photon and fermion two-point functions, the vertex, the four-photon*)
(*function), and writes Src/generated/SpinorQED_CT.nlo.  Research note models/spinor_qed, step (5).*)
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
WriteCT[FileNameJoin[{Directory[], "SpinorQED_ren", "SpinorQED_ren"}], "Lorentz", Output -> "SpinorQED_CT"];
Print["written: ", FileNames["SpinorQED_CT.nlo"]];


(* ::Subsubsection:: *)
(*Inspect: the start of generated/SpinorQED_CT.nlo*)


If[$Notebooks,
  StringTake[Import[FileNameJoin[{Directory[], "SpinorQED_CT.nlo"}], "Text"], UpTo[3000]]
]
