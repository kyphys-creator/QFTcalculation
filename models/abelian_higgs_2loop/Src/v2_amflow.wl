(* ::Package:: *)

(* ::Title:: *)
(*Step (1): the vacuum sunrise with AMFlow 2.0 (abelian Higgs model, two-loop effective potential)*)


(* ::Text:: *)
(*Research note models/abelian_higgs_2loop, step (1); an independent evaluation of the masters of V2.  For the benchmark*)
(*couplings (e = 1/2, lam = 25/32, m2 = 25/8, Q = 1) and the background fields phi = 2 (the tree minimum, xg = 0) and*)
(*phi = 3, the vacuum sunrises with the squared masses needed in V2 (from {0, xh, xg, xa}) are computed with AMFlow 2.0*)
(*(auxiliary mass flow, IBP with Kira 3.1), 30 digits, eps^-2 ... eps^0:*)
(*    J = Integrate[d^Dq1 d^Dq2/(I Pi^(D/2))^2 1/((q1^2 - x)(q2^2 - y)((q1 + q2)^2 - z))],*)
(*converted to TSIL's bold form s = (-1)^3 E^(2 eps EulerGamma) J (Euclidean, MS-bar measure, Q = 1), and*)
(*    I(x,y,z) = s|eps^0 - Aeps(x) - Aeps(y) - Aeps(z),   Aeps(x) = x (-1 - z2/2 + L - L^2/2),  L = ln x;*)
(*the 1/eps^2 and 1/eps coefficients are checked against -(x+y+z)/2 and A(x)+A(y)+A(z) - (x+y+z)/2.*)
(*Writes results/v2_amflow.csv (x, y, z, I).  Batch: wolframscript -file v2_amflow.wl (AMFlow in a kernel of its own).*)


srcDirAV$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
workAV$ = FileNameJoin[{srcDirAV$, "work", "v2_amflow"}];
If[DirectoryQ[workAV$], DeleteDirectory[workAV$, DeleteContents -> True]];
CreateDirectory[workAV$, CreateIntermediateDirectories -> True];
SetDirectory[workAV$];
Get[FileNameJoin[{$HomeDirectory, "hep", "AMFlow-2.0", "AMFlow.m"}]];
CacheDirectory[key_] := FileNameJoin[{workAV$, "cache", ToString[AMFlowInfo["Family"], InputForm] <> "_" <> key}];
SetReductionOptions["IBPReducer" -> "Kira"];
SetAMFOptions["DESolver" -> "MMA"];
SetGlobalOptions["SilentMode" -> True];


(* the squared masses at the two background fields *)
massesAV$[phi_] := With[{lam = 25/32, m2 = 25/8, e = 1/2}, {-m2 + 3 lam phi^2, -m2 + lam phi^2, e^2 phi^2}];
triplesAV$[phi_] := Module[{xh, xg, xa},
   {xh, xg, xa} = massesAV$[phi];
   Union[Sort /@ {{xh, xh, xh}, {xh, xg, xg}, {xa, xg, xh}, {0, xg, xh}, {xa, xa, xh}, {0, xa, xh}, {0, 0, xh}}]];
triplesAll$ = Union[Join[triplesAV$[2], triplesAV$[3]]];
Print["(a) sunrises to evaluate: ", triplesAll$];

aAV$[x_] := If[x == 0, 0, x (Log[x] - 1)];
aepsAV$[x_] := If[x == 0, 0, x (-1 - Pi^2/12 + Log[x] - Log[x]^2/2)];
rowsAV$ = {};
Do[Module[{x, y, z, jv, s, c},
    {x, y, z} = t;
    AMFlowInfo["Family"] = sun; AMFlowInfo["Loop"] = {q1, q2}; AMFlowInfo["Leg"] = {};
    AMFlowInfo["Conservation"] = {}; AMFlowInfo["Replacement"] = {};
    AMFlowInfo["Propagator"] = {q1^2 - mx, q2^2 - my, (q1 + q2)^2 - mz};
    AMFlowInfo["Numeric"] = {mx -> x, my -> y, mz -> z};
    AMFlowInfo["NThread"] = 4;
    jv = j[sun, 1, 1, 1] /. SolveIntegrals[{j[sun, 1, 1, 1]}, 30, 4];   (* j is AMFlow's global head *)
    s = Normal[Series[-Exp[2 eps EulerGamma] jv, {eps, 0, 0}]];
    c = Table[Coefficient[s, eps, k], {k, -2, 0}];
    Print["(a) {x,y,z} = ", N[t, 8], ":  eps^-2 - expected ", N[c[[1]] + (x + y + z)/2, 3], ",  eps^-1 - expected ",
     N[c[[2]] - (aAV$[x] + aAV$[y] + aAV$[z] - (x + y + z)/2), 3]];
    AppendTo[rowsAV$, {x, y, z, c[[3]] - aepsAV$[x] - aepsAV$[y] - aepsAV$[z]}]],
  {t, triplesAll$}];
Export[FileNameJoin[{srcDirAV$, "results", "v2_amflow.csv"}],
  Prepend[{ToString[CForm[N[#1, 17]]], ToString[CForm[N[#2, 17]]], ToString[CForm[N[#3, 17]]],
      ToString[NumberForm[N[#4, 25], 25, ExponentFunction -> (Null &)]]} & @@@ rowsAV$, {"x", "y", "z", "I"}], "CSV"];
Print["(a) written results/v2_amflow.csv"];
