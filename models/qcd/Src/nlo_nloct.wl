(* ::Package:: *)

(* ::Title:: *)
(*Step (5), 2 of 3: UV counterterms and R2 vertices with the unpatched FeynArts and NLOCT (WriteCT)*)


(* ::Text:: *)
(*Unpatched FeynArts 3.12 + NLOCT (from the FeynRules folder), in a kernel without FeynRules: WriteCT computes, for the*)
(*QCD corrections only (QCDOnly -> True), the UV counterterms of Src/generated/QCD_ren with on-shell conditions for the*)
(*heavy-quark mass and for the fields (NLOCT's default; infrared poles are marked with FR$IR and then FR$IR -> 1), and*)
(*the strong coupling in MS-bar with the heavy quark subtracted at zero momentum: ZeroMom -> {{aS, {t, g, tbar}}} fixes the*)
(*finite part of deltaaS so that the t tbar g vertex counterterm (without the top field constants) has no finite piece,*)
(*i.e. aS = alpha_s^(n_l) of the decoupled theory (the MadGraph convention).  It also computes the R2 vertices*)
(*(Feynman gauge, 't Hooft-Veltman scheme) and writes Src/generated/QCD_CT.nlo.  Research note models/qcd, step (5).*)
(*Field codes of QCD_ren: V[1] photon, V[2] gluon, U[1] ghost, F[1] electron, F[2..6] u, c, d, s, b, F[7] t.*)
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
(*unpatched FeynArts and NLOCT: the UV counterterms and R2 vertices (WriteCT)*)


SetDirectory[FileNameJoin[{srcDirNC$, "generated"}]];
Get["FeynArts`"];
Get[FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules", "NLOCT.m"}]];
t0NC$ = AbsoluteTime[];
WriteCT[FileNameJoin[{Directory[], "QCD_ren", "QCD_ren"}], "Lorentz", Output -> "QCD_CT", QCDOnly -> True,
  ZeroMom -> {{aS, {F[7], V[2], -F[7]}}}];
Print["written: ", FileNames["QCD_CT.nlo"], " in ", Round[AbsoluteTime[] - t0NC$], " s"];


(* ::Subsubsection:: *)
(*Inspect: the start of generated/QCD_CT.nlo*)


If[$Notebooks,
  StringTake[Import[FileNameJoin[{Directory[], "QCD_CT.nlo"}], "Text"], UpTo[3000]]
]
