(* ::Package:: *)

(* ::Title:: *)
(*Step (6) of the Higgs note: the FeynArts model and the UFO of SM_CKM.fr with the heavy-top operator of HggEFT.fr*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (6).  LoadModel["SM_CKM.fr", "HggEFT.fr"]: the note's model file (unchanged) and the*)
(*operator -(1/4) cHgg (H/vev) G G.  Writes, as generate_SM_CKM.wl:*)
(*  Src/generated/FeynmanRules_HggEFT.m    the vertices of the operator (H g g, H g g g, H g g g g)*)
(*  Src/generated/SM_CKM_HEFT_UFO/          UFO for MadGraph (Feynman gauge)*)
(*  Src/generated/SM_CKM_HEFT_FA/           FeynArts model (GaugeXi kept)*)
(*and checks that the SM vertices are those of step (1) (generated/FeynmanRules_SM_CKM.m).*)
(*Batch:  wolframscript -file generate_HggEFT.wl*)


srcDirGN$ = DirectoryName[$InputFileName];
outDirGN$ = FileNameJoin[{srcDirGN$, "generated"}];

$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirGN$];
LoadModel["SM_CKM.fr", "HggEFT.fr"];

verticesGN$ = FeynmanRules[LSM, ScreenOutput -> False];
smVerticesGN$ = Get[FileNameJoin[{outDirGN$, "FeynmanRules_SM_CKM.m"}]];
Print["SM vertex classes: ", Length[verticesGN$], ";  identical to step (1): ", verticesGN$ === smVerticesGN$];
effGN$ = FeynmanRules[LHgg, ScreenOutput -> False];
Print["operator vertices: ", Length[effGN$], " (", (Sort[#[[1]][[All, 1]]] &) /@ effGN$, ")"];
Print["H g g vertex: ", InputForm[Select[effGN$, Length[#[[1]]] == 3 &][[1, 2]]]];

Quiet[CreateDirectory[outDirGN$]];
SetDirectory[outDirGN$];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"SM_CKM_HEFT_FA", "SM_CKM_HEFT_UFO"}];
Put[effGN$, "FeynmanRules_HggEFT.m"];
WriteUFO[LSM + LHgg, Output -> "SM_CKM_HEFT_UFO"];
ParallelEvaluate[Off[Simplify::time]];
WriteFeynArtsOutput[LSM + LHgg, Output -> "SM_CKM_HEFT_FA", GenericFile -> True];
modFileGN$ = FileNameJoin[{outDirGN$, "SM_CKM_HEFT_FA", "SM_CKM_HEFT_FA.mod"}];
Export[modFileGN$, StringReplace[Import[modFileGN$, "Text"], {
    RegularExpression["\\bxiZ\\b"] -> "GaugeXi[Z]", RegularExpression["\\bxiW\\b"] -> "GaugeXi[W]",
    RegularExpression["\\bxiA\\b"] -> "GaugeXi[A]", RegularExpression["\\bxiG\\b"] -> "GaugeXi[G]"}], "Text"];
Print["written: generated/FeynmanRules_HggEFT.m, SM_CKM_HEFT_UFO, SM_CKM_HEFT_FA"];
