(* ::Package:: *)

(* ::Title:: *)
(*Step (4), 1 of 3: the renormalized Lagrangian of the note's model for NLOCT (Feynman gauge)*)


(* ::Text:: *)
(*FeynRules + NLOCT: OnShellRenormalization[LAH] adds the counterterm Lagrangian (field constants FR$deltaZ, parameter*)
(*constants FR$delta for the external parameters ee, MA, MH, the tadpole constant FR$deltat[H]) at first order in*)
(*FR$CT.  xiA is set to 1 first (NLOCT and MadLoop work in Feynman gauge; otherwise NLOCT also renormalizes xiA).  As in*)
(*the SM note, FR$deltat[H] is set to 0: its one-point vertex has no generic coupling in FeynArts' Lorentz.gen and the*)
(*model would not load.  The result is written as a FeynArts model, Src/generated/AbelianHiggs_ren/ (overwritten), for*)
(*nlo_nloct.wl.  Needs the local patch of FeynRules/Core/Loop.m (~/hep/README.md).*)
(*Batch: wolframscript -file nlo_renormalize.wl  (in a fresh kernel)*)


srcDirNR$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNR$];
LoadModel["AbelianHiggs.fr"];

t0NR$ = AbsoluteTime[];
lagRenNR$ = OnShellRenormalization[LAH /. xiA -> 1];
lagRenNR$ = lagRenNR$ /. FR$deltat[_] -> 0;
Put[Coefficient[Expand[lagRenNR$], FR$CT], FileNameJoin[{srcDirNR$, "generated", "AbelianHiggs_ctlag.m"}]];
(* the constants (FR$delta[{ee}], FR$delta[{MA}], FR$delta[{MH}], FR$deltaZ[{A, A}], FR$deltaZ[{H, H}], FR$deltaZ[{G0, G0}],
   FR$deltaZ[{G0, H}], FR$deltaZ[{H, G0}]) are listed by nlo_compare.wl from that file *)
Print["renormalized: ", Round[AbsoluteTime[] - t0NR$], " s;  counterterm Lagrangian with ",
  Length[Expand[Coefficient[Expand[lagRenNR$], FR$CT]]], " terms written to generated/AbelianHiggs_ctlag.m"];

SetDirectory[FileNameJoin[{srcDirNR$, "generated"}]];
If[DirectoryQ["AbelianHiggs_ren"], DeleteDirectory["AbelianHiggs_ren", DeleteContents -> True]];
WriteFeynArtsOutput[lagRenNR$, Output -> "AbelianHiggs_ren", GenericFile -> False, FlavorExpand -> True];
Print["written: ", FileNames["*", "AbelianHiggs_ren"]];
