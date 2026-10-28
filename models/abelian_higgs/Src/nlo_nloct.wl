(* ::Package:: *)

(* ::Title:: *)
(*Step (4), 2 of 3: UV and R2 counterterms with the unpatched FeynArts and NLOCT (WriteCT)*)


(* ::Text:: *)
(*Unpatched FeynArts 3.12 + NLOCT 1.02 (from the FeynRules folder), in a kernel without FeynRules: WriteCT computes the*)
(*UV counterterms of Src/generated/AbelianHiggs_ren (on-shell conditions for the masses and fields, NLOCT's default for*)
(*ee) and the R2 vertices, and writes Src/generated/AbelianHiggs_CT.nlo.*)
(*Batch: wolframscript -file nlo_nloct.wl  (in a fresh kernel without FeynRules, after nlo_renormalize.wl)*)


srcDirNC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
SetDirectory[FileNameJoin[{srcDirNC$, "generated"}]];
Get["FeynArts`"];
Get[FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules", "NLOCT.m"}]];
t0NC$ = AbsoluteTime[];
WriteCT[FileNameJoin[{Directory[], "AbelianHiggs_ren", "AbelianHiggs_ren"}], "Lorentz", Output -> "AbelianHiggs_CT"];
Print["written: ", FileNames["AbelianHiggs_CT.nlo"], " in ", Round[AbsoluteTime[] - t0NC$], " s"];
