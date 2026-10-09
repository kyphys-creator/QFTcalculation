(* FeynCalc 10.2.1 + FeynHelpers 2: the same B0 through LoopTools and Package-X *)
$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];
Print["FeynCalc ", $FeynCalcVersion];
lt = LToolsEvaluate[B0[s, m^2, m^2], InitialSubstitutions -> {s -> 2., m -> 1.}];
Print["LToolsEvaluate B0(2;1,1) = ", ToString[lt, InputForm]];
px = PaXEvaluate[B0[s, m^2, m^2]] /. {s -> 2, m -> 1, ScaleMu -> 1};
Print["PaXEvaluate   B0(2;1,1) = ", ToString[px, InputForm], "  = 1/Epsilon + ", N[px - 1/Epsilon, 16]];
LToolsUnLoadLibrary[];
