(* SM + real scalar dark matter -> UFO (unitary gauge) and CalcHEP files, into ../out/model.
   FeynRules 2.3.49 with the local patch of environment/files/FeynRules.m.patch. *)
here = DirectoryName[$InputFileName];
outDir = FileNameJoin[{ParentDirectory[here], "out", "model"}];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath]; Get["FeynRules`"];
LoadModel["Models/SM/SM.fr", FileNameJoin[{here, "SingletDM.fr"}]];
FeynmanGauge = False;                                 (* SM.fr sets it to True when loaded *)
Quiet[CreateDirectory[outDir, CreateIntermediateDirectories -> True]]; SetDirectory[outDir];
lag = LSM + LDM;
Print["sdm vertices: ", InputForm[FeynmanRules[LDM, ScreenOutput -> False]]];
WriteUFO[lag, Output -> "SM_SingletDM_UFO"];
WriteCHOutput[lag, Output -> "SM_SingletDM_CH"];
Print["FeynRules messages: ", Length[$MessageList]];
