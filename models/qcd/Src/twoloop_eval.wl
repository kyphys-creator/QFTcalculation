(* ::Package:: *)

(* ::Title:: *)
(*Step (7): the masters (exact and AMFlow 2.0), Z_3 and Z~_3 at two loops in the Landau gauge, beta_1*)


(* ::Text:: *)
(*Research note models/qcd, step (7).  Reads K Pi^(2)/a^2, K Pitilde^(2)/a^2 (bare, Landau gauge) in terms of the two masters from*)
(*results/twoloop_reduction.m (twoloop_feyncalc.wl).  At -q^2 = mu^2 (all logarithms 0), with J = E^(eps EulerGamma) int d^Dl/(i Pi^(D/2))*)
(*per loop (Minkowski propagators 1/(l^2 + i0)):*)
(*  bubble^2  J[k2, {1,1,1,1,0}] = E^(2 eps EulerGamma) G(1,1)^2,*)
(*  sunset    J[k2, {1,0,0,1,1}] = -E^(2 eps EulerGamma) G(1,1) G(eps,1)      (the l1 bubble inside gives (-l2^2)^(-eps) G(1,1)),*)
(*  G(a,b) = Gamma(a+b-D/2) Gamma(D/2-a) Gamma(D/2-b)/(Gamma(a) Gamma(b) Gamma(D-a-b))  (App. G).*)
(*(a) the masters exactly against AMFlow 2.0 (30 digits, up to eps^2) at q^2 = -1.*)
(*(b) Z_3, Z~_3 from the finiteness of Z_3 (1 - Pi) and Z~_3 (1 + Pitilde) with Pi = a Z_alpha Pi^(1) + a^2 Pi^(2) (bare coupling in terms of the*)
(*    renormalized one, Z_alpha = 1 - beta_0 a/eps; Pi^(1), Pitilde^(1) of Eq. (5) at xi = 0, exact in D); the double poles against the RG*)
(*    prediction z_1 (z_1 - beta_0)/2; beta_1 = 4 z~_21 + 2 z_21 from Z_alpha = 1/(Z~_3^2 Z_3); gamma = -z_1 a - 2 z_21 a^2; the finite parts*)
(*    of the renormalized two-loop functions at mu^2 = -q^2.  -> results/twoloop_z.csv, results/twoloop_masters.csv*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file twoloop_eval.wl  (after twoloop_feyncalc.wl; about 2 minutes).  Interactive:  ~/hep/bin/wopen twoloop_eval.wl, then "Run All Code"; the cells under "Inspect" headings run only in the notebook.  AMFlow is loaded in a kernel of its own (not together with FeynCalc).*)


(* ::Section:: *)
(*Setup*)


srcDirTE$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
workTE$ = FileNameJoin[{srcDirTE$, "work", "twoloop_amflow"}];
If[DirectoryQ[workTE$], DeleteDirectory[workTE$, DeleteContents -> True]];
CreateDirectory[workTE$, CreateIntermediateDirectories -> True];
redTE$ = Get[FileNameJoin[{srcDirTE$, "results", "twoloop_reduction.m"}]];
ep = Epsilon;
gTE$[a_, b_] := Gamma[a + b - D/2] Gamma[D/2 - a] Gamma[D/2 - b]/(Gamma[a] Gamma[b] Gamma[D - a - b]);
exactTE$ = {GLI["k2", {1, 1, 1, 1, 0}] -> E^(2 ep EulerGamma) gTE$[1, 1]^2, GLI["k2", {1, 0, 0, 1, 1}] -> -E^(2 ep EulerGamma) gTE$[1, 1] gTE$[ep, 1]} /. D -> 4 - 2 ep;
serTE$[x_, n_] := Normal[Series[x, {ep, 0, n}]];
Print["(a) masters of the reduction: ", Union[Cases[Values[redTE$], _GLI, Infinity]]];


(* ::Section:: *)
(*(a) the masters: exact against AMFlow*)


SetDirectory[workTE$];
Get[FileNameJoin[{$HomeDirectory, "hep", "AMFlow-2.0", "AMFlow.m"}]];
CacheDirectory[key_] := FileNameJoin[{workTE$, "cache", ToString[AMFlowInfo["Family"], InputForm] <> "_" <> key}];
SetReductionOptions["IBPReducer" -> "Kira"];
SetAMFOptions["DESolver" -> "MMA"];
SetGlobalOptions["SilentMode" -> True];
AMFlowInfo["Family"] = k2; AMFlowInfo["Loop"] = {l1, l2}; AMFlowInfo["Leg"] = {q}; AMFlowInfo["Conservation"] = {};
AMFlowInfo["Replacement"] = {q^2 -> s}; AMFlowInfo["Propagator"] = {l1^2, l2^2, (l1 - q)^2, (l2 - q)^2, (l1 - l2)^2};
AMFlowInfo["Numeric"] = {s -> -1}; AMFlowInfo["NThread"] = 4;
(* AMFlow writes the regulator as its own symbol eps *)
amfTE$ = SolveIntegrals[{j[k2, 1, 1, 1, 1, 0], j[k2, 1, 0, 0, 1, 1]}, 30, 6] /. s_Symbol /; SymbolName[s] === "eps" :> ep;
ResetDirectory[];
(* AMFlow's J has no E^(eps EulerGamma) per loop *)
amfValTE$ = {GLI["k2", {1, 1, 1, 1, 0}] -> E^(2 ep EulerGamma) (j[k2, 1, 1, 1, 1, 0] /. amfTE$), GLI["k2", {1, 0, 0, 1, 1}] -> E^(2 ep EulerGamma) (j[k2, 1, 0, 0, 1, 1] /. amfTE$)};
mastersTE$ = Table[With[{ex = serTE$[g /. exactTE$, 2], am = serTE$[g /. amfValTE$, 2]},
    {g, Table[N[Coefficient[ex, ep, k], 20], {k, -2, 2}], Max[Abs[Table[N[Coefficient[ex - am, ep, k], 30], {k, -2, 2}]]]}], {g, {GLI["k2", {1, 1, 1, 1, 0}], GLI["k2", {1, 0, 0, 1, 1}]}}];
(* the AMFlow values carry about 30 digits: an exact zero difference is printed as its accuracy *)
Do[Print["(a) ", m[[1]], ": eps^-2..eps^2 = ", InputForm[N[Rationalize[m[[2]], 10^-15], 15]], ";  max |exact - AMFlow| < 10^", -Round[Accuracy[m[[3]]]]], {m, mastersTE$}];


(* ::Subsubsection:: *)
(*Inspect: the masters in closed form (eps expansion)*)


If[$Notebooks, TableForm[{#, Collect[FullSimplify[serTE$[# /. exactTE$, 1]], ep]} & /@ {GLI["k2", {1, 1, 1, 1, 0}], GLI["k2", {1, 0, 0, 1, 1}]}]]


(* ::Section:: *)
(*(b) Z_3, Z~_3 and beta_1*)


pi2TE$ = redTE$["Pi2"] /. qq -> -1 /. exactTE$ /. D -> 4 - 2 ep;
pt2TE$ = redTE$["Pitilde2"] /. qq -> -1 /. exactTE$ /. D -> 4 - 2 ep;
pi1TE$ = ((CA/2 ((3 D - 2)/(D - 1) + (2 D - 7) - (D - 4)/4) - 2 TF nf (D - 2)/(D - 1)) E^(ep EulerGamma) gTE$[1, 1]) /. D -> 4 - 2 ep;
pt1TE$ = (-CA (1/2 + (D - 3)/4) E^(ep EulerGamma) gTE$[1, 1]) /. D -> 4 - 2 ep;
b0TE$ = 11/3 CA - 4/3 TF nf;
lauTE$[x_] := Module[{s = serTE$[x, 0]}, Table[Expand[FullSimplify[Coefficient[s, ep, k] /. PolyGamma[2, n_] :> FunctionExpand[PolyGamma[2, n]]]], {k, -2, 0}]];
z31TE$ = lauTE$[pi1TE$][[2]]; zt31TE$ = -lauTE$[pt1TE$][[2]];
pi2LTE$ = lauTE$[pi2TE$]; pt2LTE$ = lauTE$[pt2TE$];
Print["(b) bare K^2 Pi^(2)/g^4 (mu^2 = -q^2), {1/eps^2, 1/eps, 1}: ", InputForm[pi2LTE$]];
Print["(b) bare K^2 Pitilde^(2)/g^4: ", InputForm[pt2LTE$]];
(* Z_3 (1 - Pi) and Z~_3 (1 + Pitilde) finite order by order *)
z32TE$ = lauTE$[(z31TE$/ep - b0TE$/ep) pi1TE$ + pi2TE$];
zt32TE$ = -lauTE$[(zt31TE$/ep - b0TE$/ep) pt1TE$ + pt2TE$];
Print["(b) one loop: z_31 = ", z31TE$, ",  z~_31 = ", zt31TE$, "  (expect 13/6 C_A - 4/3 T_F n_f, 3/4 C_A: Eq. (7) at xi = 0)"];
Print["(b) Z_3 at two loops {1/eps^2, 1/eps} = ", InputForm[z32TE$[[{1, 2}]]], ";  double pole - z_31 (z_31 - beta_0)/2 = ", Expand[z32TE$[[1]] - z31TE$ (z31TE$ - b0TE$)/2]];
Print["(b) Z~_3 at two loops {1/eps^2, 1/eps} = ", InputForm[zt32TE$[[{1, 2}]]], ";  double pole - z~_31 (z~_31 - beta_0)/2 = ", Expand[zt32TE$[[1]] - zt31TE$ (zt31TE$ - b0TE$)/2]];
b1TE$ = Expand[4 zt32TE$[[2]] + 2 z32TE$[[2]]];
Print["(b) beta_1 = 4 z~_321 + 2 z_321 = ", b1TE$, ";  minus Caswell-Jones 34/3 C_A^2 - 4 C_F T_F n_f - 20/3 C_A T_F n_f = ",
  Simplify[b1TE$ - (34/3 CA^2 - 4 CF TF nf - 20/3 CA TF nf)]];
gA2TE$ = Expand[-2 z32TE$[[2]]]; gC2TE$ = Expand[-2 zt32TE$[[2]]];
Print["(b) two-loop anomalous dimensions (a^2 = (g^2/K)^2 units, Landau gauge): gamma_A^(2) = ", gA2TE$, ",  gamma_c^(2) = ", gC2TE$];
(* the renormalized two-loop functions at mu^2 = -q^2 (finite parts) *)
pi2RTE$ = Expand[lauTE$[(z31TE$/ep - b0TE$/ep) pi1TE$ + pi2TE$][[3]]];
pt2RTE$ = Expand[lauTE$[(zt31TE$/ep - b0TE$/ep) pt1TE$ + pt2TE$][[3]]];
Print["(b) renormalized K^2 Pi^R(2)/g^4 at mu^2 = -q^2: ", InputForm[pi2RTE$], " = ", N[pi2RTE$ /. {CA -> 3, CF -> 4/3, TF -> 1/2, nf -> 6}], " (SU(3), n_f = 6)"];
Print["(b) renormalized K^2 Pitilde^R(2)/g^4 at mu^2 = -q^2: ", InputForm[pt2RTE$], " = ", N[pt2RTE$ /. {CA -> 3, CF -> 4/3, TF -> 1/2, nf -> 6}]];


(* ::Subsubsection:: *)
(*Inspect: Z_3, Z~_3, Z_alpha to two loops*)


If[$Notebooks,
  TableForm[{{"Z_3", 1 + z31TE$ a/ep + (z32TE$[[1]]/ep^2 + z32TE$[[2]]/ep) a^2}, {"Z~_3", 1 + zt31TE$ a/ep + (zt32TE$[[1]]/ep^2 + zt32TE$[[2]]/ep) a^2},
    {"Z_alpha = 1/(Z~_3^2 Z_3)", Collect[Normal[Series[1/((1 + zt31TE$ a/ep + (zt32TE$[[1]]/ep^2 + zt32TE$[[2]]/ep) a^2)^2 (1 + z31TE$ a/ep + (z32TE$[[1]]/ep^2 + z32TE$[[2]]/ep) a^2)), {a, 0, 2}]], a, Simplify]}}]
]


(* ::Section:: *)
(*Results*)


strTE$[x_] := ToString[CForm[N[x, 17]]];
coefTE$[x_] := {Coefficient[x, CA^2], Coefficient[x, CF TF nf], Coefficient[x, CA TF nf]};
rowsTE$ = {
   Join[{"z3_double"}, coefTE$[z32TE$[[1]]]], Join[{"z3_single"}, coefTE$[z32TE$[[2]]]],
   Join[{"zt3_double"}, coefTE$[zt32TE$[[1]]]], Join[{"zt3_single"}, coefTE$[zt32TE$[[2]]]],
   Join[{"gamma_A2"}, coefTE$[gA2TE$]], Join[{"gamma_c2"}, coefTE$[gC2TE$]], Join[{"beta1"}, coefTE$[b1TE$]],
   Join[{"PiR2_finite"}, coefTE$[pi2RTE$]], Join[{"PitildeR2_finite"}, coefTE$[pt2RTE$]]};
Export[FileNameJoin[{srcDirTE$, "results", "twoloop_z.csv"}],
  StringRiffle[Prepend[StringRiffle[Join[{#[[1]]}, ToString[InputForm[#]] & /@ #[[2 ;;]], strTE$ /@ #[[2 ;;]]], ","] & /@ rowsTE$,
    "quantity,CA2,CFTFnf,CATFnf,CA2_num,CFTFnf_num,CATFnf_num"], "\n"] <> "\n", "Text"];
Export[FileNameJoin[{srcDirTE$, "results", "twoloop_masters.csv"}],
  StringRiffle[Prepend[StringRiffle[Join[{ToString[#[[1, 2]], InputForm]}, strTE$ /@ #[[2]], {strTE$[#[[3]]]}], ";"] & /@ mastersTE$,
    "master;eps-2;eps-1;eps0;eps1;eps2;max_abs_exact_minus_amflow"], "\n"] <> "\n", "Text"];
Print["(c) wrote results/twoloop_z.csv, results/twoloop_masters.csv"];
