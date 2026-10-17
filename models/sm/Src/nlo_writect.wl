(* ::Package:: *)

(* ::Title:: *)
(*Step (9b), 2 of 3: NLOCT's R2 vertices (and on-shell UV counterterms) of the note's model*)


(* ::Text:: *)
(*Unpatched FeynArts 3.12 + NLOCT 1.02 in a kernel without FeynRules: WriteCT computes the one-loop UV counterterms of*)
(*Src/generated/SM_ren (NLOCT's on-shell conditions) and the R2 vertices in Feynman gauge, at order QED (electroweak),*)
(*and writes Src/generated/SM_CT.nlo (not in git) and its R2 vertices to Src/generated/SM_R2.m.  nlo_ufo.wl uses the R2*)
(*vertices, nlo_dz.wl NLOCT's on-shell field constants from its UV vertices; the UV counterterms of the FJ scheme are the note's own.  Batch: wolframscript -file nlo_writect.wl  (after nlo_renormalize.wl; long)*)


srcDirNC$ = DirectoryName[$InputFileName];
SetDirectory[FileNameJoin[{srcDirNC$, "generated"}]];
Get["FeynArts`"];
Get[FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules", "NLOCT.m"}]];
t0NC$ = AbsoluteTime[];
WriteCT[FileNameJoin[{Directory[], "SM_ren", "SM_ren"}], "Lorentz", Output -> "SM_CT"];
Print["written: ", FileNames["SM_CT.nlo"], ";  ", Round[AbsoluteTime[] - t0NC$], " s"];
(* SM_CT.nlo is about 90 MB (the on-shell UV vertices) and is not kept in git; the R2 vertices go to SM_R2.m *)
Get["SM_CT.nlo"];
Put[DeleteCases[R2$vertlist, Last[{}]], "SM_R2.m"];
Print["written: SM_R2.m (", Length[DeleteCases[R2$vertlist, Last[{}]]], " R2 vertices)"];
