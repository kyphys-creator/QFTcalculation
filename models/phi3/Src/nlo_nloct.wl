(* ::Package:: *)

(* nlo_nloct.wl -- step 2 of 3 of the NLO UFO generation (research note, step (6)).
   Unpatched FeynArts 3.12 + NLOCT 1.02 (from the FeynRules folder), in a kernel without FeynRules:
   WriteCT computes the UV counterterms of Src/generated/Phi3_ren with on-shell conditions for the
   mass and the field and MS-bar for gphi (NLOCT's default), and writes Src/generated/Phi3_CT.nlo.
   The scalar theory has no R2 vertices; NLOCT then writes the malformed R2$vertlist = {Last[{}]},
   which nlo_ufo.wl removes.  (NLOCT's MSbar -> True option is not used: for this model it returns
   a two-point counterterm without the factor -I, so the poles do not cancel in MadLoop.)

   Usage:  wolframscript -file nlo_nloct.wl     (after nlo_renormalize.wl) *)

srcDirNC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
SetDirectory[FileNameJoin[{srcDirNC$, "generated"}]];
Get["FeynArts`"];
Get[FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules", "NLOCT.m"}]];
WriteCT[FileNameJoin[{Directory[], "Phi3_ren", "Phi3_ren"}], "Lorentz", Output -> "Phi3_CT"];
Print["written: ", FileNames["Phi3_CT.nlo"]];
