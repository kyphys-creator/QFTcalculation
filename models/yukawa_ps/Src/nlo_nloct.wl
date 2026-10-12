(* ::Package:: *)

(* ::Title:: *)
(*Step (5), 2 of 3: UV counterterms with the unpatched FeynArts and NLOCT (WriteCT)*)


(* ::Text:: *)
(*Unpatched FeynArts 3.12 + NLOCT 1.02 (from the FeynRules folder), in a kernel without FeynRules:*)
(*WriteCT computes the UV counterterms of Src/generated/PsYukawa_ren with on-shell conditions for the*)
(*masses and the fields and MS-bar for yps and lamphi (NLOCT's default), and the R2 vertices (phi phi, phi psibar psi,*)
(*phi^4: fermion loops), and writes Src/generated/PsYukawa_CT.nlo.  (NLOCT's MSbar -> True option is not used: in the*)
(*phi^3 note it returned a two-point counterterm without the factor -I; nlo_ufo.wl builds the MS-bar UFO from the poles.)*)
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
WriteCT[FileNameJoin[{Directory[], "PsYukawa_ren", "PsYukawa_ren"}], "Lorentz", Output -> "PsYukawa_CT"];
Print["written: ", FileNames["PsYukawa_CT.nlo"]];


(* ::Subsubsection:: *)
(*Inspect: the start of generated/PsYukawa_CT.nlo*)


If[$Notebooks,
  StringTake[Import[FileNameJoin[{Directory[], "PsYukawa_CT.nlo"}], "Text"], UpTo[3000]]
]
