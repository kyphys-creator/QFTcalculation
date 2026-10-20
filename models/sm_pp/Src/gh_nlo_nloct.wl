(* ::Package:: *)

(* ::Title:: *)
(*Step (2b), 2 of 3: UV counterterms and R2 vertices of QCDH.fr with the unpatched FeynArts and NLOCT (WriteCT)*)


(* ::Text:: *)
(*Research note models/sm_pp, step (2b), as the QCD note's nlo_nloct.wl (QCDOnly; no heavy quark, so no zero-momentum*)
(*subtraction): -> generated/QCDH_CT.nlo.  Runs in a kernel without FeynRules.*)
(*Batch:  wolframscript -file gh_nlo_nloct.wl*)


srcDirGN$ = DirectoryName[$InputFileName];
SetDirectory[FileNameJoin[{srcDirGN$, "generated"}]];
Get["FeynArts`"];
Get[FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules", "NLOCT.m"}]];
t0GN$ = AbsoluteTime[];
(* the generic model is FeynRules' own QCDH_ren.gen (Lorentz.gen has no H G G G structure) *)
WriteCT[FileNameJoin[{Directory[], "QCDH_ren", "QCDH_ren"}], FileNameJoin[{Directory[], "QCDH_ren", "QCDH_ren"}], Output -> "QCDH_CT",
  QCDOnly -> True];
Print["written: ", FileNames["QCDH_CT.nlo"], " in ", Round[AbsoluteTime[] - t0GN$], " s"];
