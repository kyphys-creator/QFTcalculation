(* ::Package:: *)

(* ::Title:: *)
(*Step (1) of the Higgs note: the FeynArts model and the UFO of SM_CKM.fr*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (1).  SM_CKM.fr is the CKM note's model file, copied unchanged (models/sm_ckm/Src) as for*)
(*the NLO note (models/sm_nlo/Src).*)
(*This script writes, as the CKM note's generate_SM_CKM.wl does (the UFO first, then FeynArts; the gauge parameters of*)
(*the ghost-scalar couplings of the FeynArts model renamed GaugeXi[...]):*)
(*  Src/generated/FeynmanRules_SM_CKM.m   vertex list returned by FeynmanRules*)
(*  Src/generated/SM_CKM_UFO/             UFO for MadGraph (Feynman gauge)*)
(*  Src/generated/SM_CKM_FA/              FeynArts model (GaugeXi kept)*)
(*and checks that the vertices and the written files equal the NLO note's (models/sm_nlo/Src/generated, itself equal to the CKM*)
(*note's), apart from*)
(*the lines with the date and the folder.*)
(*Batch:  wolframscript -file generate_SM_CKM.wl*)


srcDirGN$ = DirectoryName[$InputFileName];
outDirGN$ = FileNameJoin[{srcDirGN$, "generated"}];
ckmGenDirGN$ = FileNameJoin[{ParentDirectory[srcDirGN$], "..", "sm_nlo", "Src", "generated"}];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirGN$];
LoadModel["SM_CKM.fr"];

verticesGN$ = FeynmanRules[LSM, ScreenOutput -> False];
ckmVerticesGN$ = Get[FileNameJoin[{ckmGenDirGN$, "FeynmanRules_SM_CKM.m"}]];
Print["vertex classes: ", Length[verticesGN$], " (the NLO note: ", Length[ckmVerticesGN$], ");  identical to the NLO note's list: ",
  verticesGN$ === ckmVerticesGN$];
If[verticesGN$ =!= ckmVerticesGN$,
  Module[{a = Association[(Sort[#[[1]][[All, 1]]] -> #[[2]]) & /@ verticesGN$],
      b = Association[(Sort[#[[1]][[All, 1]]] -> #[[2]]) & /@ ckmVerticesGN$], diff},
    diff = Select[Union[Keys[a], Keys[b]], ! KeyExistsQ[a, #] || ! KeyExistsQ[b, #] || Simplify[a[#] - b[#]] =!= 0 &];
    Print["   classes that differ after Simplify: ", Length[diff], " ", diff]]];

Quiet[CreateDirectory[outDirGN$]];
SetDirectory[outDirGN$];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"SM_CKM_FA", "SM_CKM_UFO"}];
Put[verticesGN$, "FeynmanRules_SM_CKM.m"];
WriteUFO[LSM, Output -> "SM_CKM_UFO"];
ParallelEvaluate[Off[Simplify::time]];
WriteFeynArtsOutput[LSM, Output -> "SM_CKM_FA", GenericFile -> True];
modFileGN$ = FileNameJoin[{outDirGN$, "SM_CKM_FA", "SM_CKM_FA.mod"}];
Export[modFileGN$, StringReplace[Import[modFileGN$, "Text"], {
    RegularExpression["\\bxiZ\\b"] -> "GaugeXi[Z]", RegularExpression["\\bxiW\\b"] -> "GaugeXi[W]",
    RegularExpression["\\bxiA\\b"] -> "GaugeXi[A]", RegularExpression["\\bxiG\\b"] -> "GaugeXi[G]"}], "Text"];

(* the written files against the NLO note's, without the lines that carry the date, the time or the folder *)
cleanGN$[file_] := Select[StringSplit[Import[file, "Text"], "\n"],
   ! StringContainsQ[#, RegularExpression["(?i)date|created|generated on|/Users/|/private/|\\d\\d:\\d\\d:\\d\\d"]] &];
filesGN$ = Join[
   FileNameJoin[{"SM_CKM_FA", #}] & /@ {"SM_CKM_FA.mod", "SM_CKM_FA.gen", "SM_CKM_FA.pars"},
   FileNameJoin[{"SM_CKM_UFO", #}] & /@ {"parameters.py", "couplings.py", "vertices.py", "lorentz.py", "particles.py",
     "coupling_orders.py", "propagators.py", "decays.py"}];
Do[Module[{a = cleanGN$[FileNameJoin[{outDirGN$, f}]], b = cleanGN$[FileNameJoin[{ckmGenDirGN$, f}]]},
   Print["   ", f, ": ", If[a === b, "identical to the NLO note's", "DIFFERENT (" <> ToString[Length[a]] <> " vs " <> ToString[Length[b]] <> " lines)"]]],
  {f, filesGN$}];
Print["written: generated/FeynmanRules_SM_CKM.m, SM_CKM_UFO, SM_CKM_FA"];
