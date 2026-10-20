(* ::Package:: *)

(* ::Title:: *)
(*Step (4b), 2 of 3: UV counterterms and R2 vertices of QCDZp.fr with the unpatched FeynArts and NLOCT (WriteCT)*)


(* ::Text:: *)
(*Research note models/sm_pp, step (4b), as the QCD note's nlo_nloct.wl (QCDOnly; no heavy quark, so no zero-momentum*)
(*subtraction): -> generated/QCDZp_CT.nlo.  Runs in a kernel without FeynRules.*)
(*Batch:  wolframscript -file zp_nlo_nloct.wl*)


srcDirZN$ = DirectoryName[$InputFileName];
SetDirectory[FileNameJoin[{srcDirZN$, "generated"}]];
Get["FeynArts`"];
Get[FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules", "NLOCT.m"}]];
t0ZN$ = AbsoluteTime[];
WriteCT[FileNameJoin[{Directory[], "QCDZp_ren", "QCDZp_ren"}], "Lorentz", Output -> "QCDZp_CT", QCDOnly -> True];
Print["written: ", FileNames["QCDZp_CT.nlo"], " in ", Round[AbsoluteTime[] - t0ZN$], " s"];
