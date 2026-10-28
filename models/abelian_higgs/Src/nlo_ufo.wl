(* ::Package:: *)

(* ::Title:: *)
(*Step (5): the UFO with NLOCT's UV and R2 counterterm vertices for MadLoop (Feynman gauge)*)


(* ::Text:: *)
(*FeynRules: read Src/generated/AbelianHiggs_CT.nlo (nlo_nloct.wl) and write Src/generated/AbelianHiggs_NLO_UFO*)
(*(overwritten) with NLOCT's UV vertices (on-shell masses and fields, MS-bar e) and R2 vertices.  NLOCT's one-point R2*)
(*vertex of h is left out: MadLoop has no tadpole diagrams (and the UFO has no one-point vertices).  FeynmanGauge = True*)
(*(set in AbelianHiggs.fr) makes the UFO declare gauge = [0, 1].*)
(*Batch: wolframscript -file nlo_ufo.wl  (in a fresh kernel, after nlo_nloct.wl)*)


srcDirNU$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNU$];
LoadModel["AbelianHiggs.fr"];
SetDirectory[FileNameJoin[{srcDirNU$, "generated"}]];
Get["AbelianHiggs_CT.nlo"];
r2NU$ = Select[R2$vertlist, Length[#[[1]]] > 1 &];
Print["R2 vertices: ", Length[R2$vertlist], " (one-point vertices left out: ", Length[R2$vertlist] - Length[r2NU$],
  ");  UV vertices: ", Length[UV$vertlist], ";  perturbed orders: ", FR$InteractionOrderPerturbativeExpansion];
If[DirectoryQ["AbelianHiggs_NLO_UFO"], DeleteDirectory["AbelianHiggs_NLO_UFO", DeleteContents -> True]];
WriteUFO[LAH, UVCounterterms -> UV$vertlist, R2Vertices -> r2NU$, Output -> "AbelianHiggs_NLO_UFO"];
Print["written: ", FileNames["AbelianHiggs_NLO_UFO"]];
