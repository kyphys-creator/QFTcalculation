(* ::Package:: *)

(* ::Title:: *)
(*Step (6), 2 of 3: UV counterterms and R2 vertices of the Standard Model with the unpatched FeynArts and NLOCT (WriteCT)*)


(* ::Text:: *)
(*Unpatched FeynArts 3.12 + NLOCT 1.02 (from the FeynRules folder), in a kernel without FeynRules, with FeynRules' generic*)
(*model LorentzTadpole.gen (Lorentz.gen plus the one-point scalar coupling of the tadpole counterterm): WriteCT computes the*)
(*R2 vertices (Feynman gauge) and the UV counterterms of Src/generated/SM_ren (nlo_renormalize.wl) for the full one-loop*)
(*corrections (QCD and electroweak): on-shell conditions for the masses and the fields (NLOCT's default; infrared poles*)
(*are marked with FR$IR and then FR$IR -> 1), the tadpole counterterm cancelling the tadpoles, and the charge (aEWM1) and*)
(*aS in MS-bar.  The four-scalar counterterms are left out (Exclude4ScalarsCT -> True).  Long renormalization constants are*)
(*written as parameters FR$CTparam (CTparameters -> True).  Writes Src/generated/SM_CT.nlo.*)
(*Research note models/sm, step (6).*)
(**)
(*Usage:  wolframscript -file nlo_nloct.wl     (after nlo_renormalize.wl)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file nlo_nloct.wl  (in a fresh kernel without FeynRules).  Interactive:  ~/hep/bin/wopen nlo_nloct.wl  (in a fresh kernel without FeynRules), then "Run All Code".*)


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
(* the tadpole counterterm is a one-point vertex C[S[1]], which FeynArts' Lorentz.gen has no generic coupling for (the model
   then fails to initialize and nothing is inserted); FeynRules ships LorentzTadpole.gen, Lorentz.gen plus that coupling *)
genNC$ = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules", "Interfaces", "FeynArts", "LorentzTadpole"}];
(* CTparameters -> True: the renormalization constants longer than 200 leaves become named parameters (FR$CTparam, written
   to the UFO's CT_parameters.py); without it the UV vertices are so long that WriteUFO did not finish in 45 minutes *)
WriteCT[FileNameJoin[{Directory[], "SM_ren", "SM_ren"}], genNC$, Output -> "SM_CT", Exclude4ScalarsCT -> True, CTparameters -> True];
Print["written: ", FileNames["SM_CT.nlo"], " in ", Round[AbsoluteTime[] - t0NC$], " s"];
