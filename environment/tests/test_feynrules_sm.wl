(* FeynRules 2.3.49 (+ local MatrixSymbol patch): SM -> UFO and FeynArts model files.
   Do not assign to model symbols (v is the Higgs vev in SM.fr). *)
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath]; Get["FeynRules`"];
LoadModel["Models/SM/SM.fr"];
testOutDir$ = FileNameJoin[{DirectoryName[$InputFileName], "out", "feynrules"}];
Quiet[CreateDirectory[testOutDir$, CreateIntermediateDirectories -> True]]; SetDirectory[testOutDir$];
WriteUFO[LSM];
WriteFeynArtsOutput[LSM];
Print["FeynRules messages: ", Length[$MessageList]];
