(* ::Package:: *)

(* ::Title:: *)
(*Step (6), 1 of 3: on-shell renormalization of the Standard Model with FeynRules + NLOCT*)


(* ::Text:: *)
(*FeynRules + NLOCT: OnShellRenormalization[LSM] adds the counterterm Lagrangian (first order in FR$CT) of the*)
(*Standard Model of Src/SM.fr with the CKM matrix set to 1 (DiagonalCKM.rst):*)
(*  fields   phi -> (1 + deltaZ/2) phi for every physical field, with the A-Z mixing constants (FlavorMixing -> {{A, Z}});*)
(*  masses   M -> M + deltaM for all masses; SM.fr's FR$LoopSwitches = {{Gf, MW}} makes MW external and Gf internal,*)
(*           FR$RmDblExt sets the Yukawa masses ym_f equal to the masses (one parameter per fermion);*)
(*  charge   aEWM1 -> aEWM1 + delta aEWM1 (NLOCT then fixes it in MS-bar; alpha(0) is set in nlo_ufo.wl).*)
(*The four-scalar counterterms are left out (Exclude4ScalarsCT -> True; they do not enter e+ e- -> mu+ mu- at one loop).*)
(*The result is written as a FeynArts model, Src/generated/SM_ren/ (overwritten).  Research note models/sm, step (6).*)
(*FlavorExpand -> True makes FeynRules write FR$ClassesTranslation; without it NLOCT does not recognize the fields.*)
(**)
(*Usage:  wolframscript -file nlo_renormalize.wl     (then nlo_nloct.wl and nlo_ufo.wl; generate_SM_NLO.sh runs all three)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file nlo_renormalize.wl  (in a fresh kernel).  Interactive:  ~/hep/bin/wopen nlo_renormalize.wl  (in a fresh kernel), then "Run All Code".*)


(* ::Section:: *)
(*Setup*)


srcDirNR$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Section:: *)
(*FeynRules and the model*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNR$];
LoadModel["SM.fr"];
LoadRestriction[FileNameJoin[{srcDirNR$, "DiagonalCKM.rst"}]];


(* ::Section:: *)
(*on-shell renormalization with NLOCT*)


t0NR$ = AbsoluteTime[];
lagRenNR$ = OnShellRenormalization[LSM, FlavorMixing -> {{A, Z}}, Exclude4ScalarsCT -> True];
Print["renormalized Lagrangian in ", Round[AbsoluteTime[] - t0NR$], " s: ", Length[lagRenNR$], " terms;  counterterm symbols: ",
  Union[Cases[lagRenNR$, FR$deltaZ[__] | FR$delta[__], Infinity]]];


(* ::Section:: *)
(*the renormalized model as a FeynArts model, generated/SM_ren*)


Quiet[CreateDirectory[FileNameJoin[{srcDirNR$, "generated"}]]];
SetDirectory[FileNameJoin[{srcDirNR$, "generated"}]];
If[DirectoryQ["SM_ren"], DeleteDirectory["SM_ren", DeleteContents -> True]];
t1NR$ = AbsoluteTime[];
WriteFeynArtsOutput[lagRenNR$, Output -> "SM_ren", GenericFile -> False, FlavorExpand -> True];
Print["written: ", FileNames["*", "SM_ren"], " in ", Round[AbsoluteTime[] - t1NR$], " s"];
