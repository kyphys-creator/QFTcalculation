(* ::Package:: *)

(* ::Title:: *)
(*Step (8'): the masters of the vacuum family v2 (all masses M = 1) with AMFlow 2.0*)


(* ::Text:: *)
(*v2 = {l1^2 - 1, l2^2 - 1, (l1 - l2)^2 - 1}; masters v2[1,1,1] (sunset) and v2[1,1,0] (tadpole^2), int d^Dl/(i Pi^(D/2)) per loop*)
(*(no E^(eps EulerGamma), as AMFlow), 30 digits, eps^-2 ... eps^2.  The tadpole^2 is compared with Gamma(-1+eps)^2.*)
(*AMFlow runs in a kernel of its own (not with FeynCalc).  Output: results/twoloop_lambda_masters.m.*)
(*Batch: wolframscript -file twoloop_lambda_masters.wl*)


srcDir$ = DirectoryName[$InputFileName];
work$ = FileNameJoin[{srcDir$, "work", "twoloop_lambda_amflow"}];
If[DirectoryQ[work$], DeleteDirectory[work$, DeleteContents -> True]];
CreateDirectory[work$, CreateIntermediateDirectories -> True];
SetDirectory[work$];
Get[FileNameJoin[{$HomeDirectory, "hep", "AMFlow-2.0", "AMFlow.m"}]];
SetReductionOptions["IBPReducer" -> "Kira"];
SetAMFOptions["DESolver" -> "MMA"];
SetGlobalOptions["SilentMode" -> True];
(* AMFlow keeps its cache next to the script: put it under work/ *)
SetAMFOptions["CacheName" -> FileNameJoin[{"work", "twoloop_lambda_amflow", "cache"}]];
AMFlowInfo["Family"] = v2; AMFlowInfo["Loop"] = {l1, l2}; AMFlowInfo["Leg"] = {}; AMFlowInfo["Conservation"] = {};
AMFlowInfo["Replacement"] = {}; AMFlowInfo["Propagator"] = {l1^2 - msq, l2^2 - msq, (l1 - l2)^2 - msq};
AMFlowInfo["Numeric"] = {msq -> 1}; AMFlowInfo["NThread"] = 4;
res$ = SolveIntegrals[{j[v2, 1, 1, 1], j[v2, 1, 1, 0]}, 30, 6] /. s_Symbol /; SymbolName[s] === "eps" :> ep;
ResetDirectory[];
sun$ = j[v2, 1, 1, 1] /. res$; t2$ = j[v2, 1, 1, 0] /. res$;
exT2$ = Normal[Series[Gamma[-1 + ep]^2, {ep, 0, 2}]];
Print["v2[1,1,1] = ", N[Expand[sun$], 20]];
Print["v2[1,1,0] - Gamma(-1+eps)^2 (eps^-2 ... eps^2): ", Table[N[Coefficient[Expand[t2$ - exT2$], ep, k], 30], {k, -2, 2}]];
Put[<|"sunset" -> sun$, "tadpole2" -> t2$|>, FileNameJoin[{srcDir$, "results", "twoloop_lambda_masters.m"}]];
