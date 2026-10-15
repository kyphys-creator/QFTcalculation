(* ::Package:: *)

(* ::Title:: *)
(*Step (9): the real-emission master integrals (three-body cut integrals) with AMFlow 2.0*)


(* ::Text:: *)
(*Research note models/qcd, step (9).  For one family chosen by hq_reduce.wl, evaluates its representative masters (work/hq/unique_<chan>.m)*)
(*at the given values of s (m = 1) with AMFlow, the propagators 1, 2, 3 cut (AMFlowInfo["Cut"]): AMFlow's normalization of a cut*)
(*integral is the standard phase space prod d^(D-1)k/((2 pi)^(D-1) 2E) (2 pi)^D delta^D, checked against the exact D-dimensional two-body*)
(*(massive) and three-body (massless) volumes (App. L).  20 digits, up to eps^2 (the coefficients have up to 1/eps^2 poles; at large s*)
(*they cancel strongly, so the digits are needed).  The value at each s is written to work/hq/amflow/<family>_s<s>.m and skipped if it*)
(*exists.  Usage: wolframscript -file hq_amflow.wl chan family s1,s2,...   (family = index in families_<chan>.m; 1-5 minutes per point)*)


srcDirHA$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
Get[FileNameJoin[{srcDirHA$, "hq_pfrac.wl"}]];
{chanHA$, fiHA$, sStrHA$} = If[$Notebooks, {"qq", "1", "16/3"}, $ScriptCommandLine[[2 ;; 4]]];
fiHA$ = ToExpression[fiHA$]; svalsHA$ = ToExpression /@ StringSplit[sStrHA$, ","];
skeyHA$[x_] := StringReplace[ToString[x, InputForm], "/" -> "o"];
workHA$ = FileNameJoin[{srcDirHA$, "work", "hq"}];
famsHA$ = Get[FileNameJoin[{workHA$, "families_" <> chanHA$ <> ".m"}]];
nameHA$ = "R" <> chanHA$ <> ToString[fiHA$];
mastersHA$ = Select[Values[Get[FileNameJoin[{workHA$, "unique_" <> chanHA$ <> ".m"}]]["rep"]], #[[1]] === nameHA$ &];
dirHA$ = FileNameJoin[{workHA$, "amflow", nameHA$}];
Quiet[CreateDirectory[dirHA$, CreateIntermediateDirectories -> True]];
SetDirectory[dirHA$];
Get[FileNameJoin[{$HomeDirectory, "hep", "AMFlow-2.0", "AMFlow.m"}]];
CacheDirectory[key_] := FileNameJoin[{dirHA$, "cache", ToString[AMFlowInfo["Family"], InputForm] <> "_" <> key}];   (* not Src/cache *)
SetReductionOptions["IBPReducer" -> "Kira"];
SetAMFOptions["DESolver" -> "MMA"];
SetGlobalOptions["SilentMode" -> True];
famHA$ = Symbol[nameHA$];
AMFlowInfo["Family"] = famHA$;
AMFlowInfo["Loop"] = {k1, k2};
AMFlowInfo["Leg"] = {p1, p2};
AMFlowInfo["Conservation"] = {};
AMFlowInfo["Replacement"] = {p1^2 -> 0, p2^2 -> 0, (p1 + p2)^2 -> s};
AMFlowInfo["Propagator"] = Join[{k1^2 - msq, k2^2 - msq, (p1 + p2 - k1 - k2)^2}, (#[[1]]^2 - (#[[2]] /. mt2 -> msq)) & /@ (momPF /@ famsHA$[[fiHA$]])];
AMFlowInfo["NThread"] = 3;
AMFlowInfo["Prescription"] = {0, 0};
AMFlowInfo["Cut"] = {1, 1, 1, 0, 0, 0, 0};
Print[nameHA$, ": ", Length[mastersHA$], " representative masters"];
Do[Module[{t0 = AbsoluteTime[], sol, out, f = FileNameJoin[{workHA$, "amflow", nameHA$ <> "_s" <> skeyHA$[s0] <> ".m"}]},
    If[FileExistsQ[f], Continue[]];
    AMFlowInfo["Numeric"] = {s -> s0, msq -> 1};
    sol = SolveIntegrals[j[famHA$, Sequence @@ #[[2]]] & /@ mastersHA$, 20, 6];
    out = (# -> (j[famHA$, Sequence @@ #[[2]]] /. sol)) & /@ mastersHA$;
    (* AMFlow returns its own symbol eps *)
    out = out /. sym_Symbol /; SymbolName[sym] === "eps" :> ep;
    Put[out, f];
    Print[nameHA$, " s = ", s0, ": ", Round[AbsoluteTime[] - t0], " s"]], {s0, svalsHA$}];
ResetDirectory[];
