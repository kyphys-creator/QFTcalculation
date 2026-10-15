(* ::Package:: *)

(* ::Title:: *)
(*Step (8): heavy-quark pair production through the photon at O(alpha_s) from the optical theorem (AMFlow 2.0)*)


(* ::Text:: *)
(*Research note models/qcd, step (8).  Reads the photon self-energy of the t loop (one loop, its m-derivative and two loops, in terms of the*)
(*masters of k1m and k2m) from results/ee_optical_reduction.m (ee_optical.wl).  At s = 4 m^2/(1 - beta^2), m = 1, the masters are evaluated*)
(*with AMFlow 2.0 (Feynman prescription +i0, 25 digits, up to eps^2), and*)
(*    Pi^(2)_tot = Pi^(2) + delta_m dPi^(1)/dm,   delta_m = -C_F (D-1)(D-2) A0(m^2)/(2 (D-3) m)  (per a = g^2/K; m_bare = m + delta_m),*)
(*    Delta^(1)(beta) = Im Pi^(2)_tot/(4 C_F Im Pi^(1))*)
(*is compared with the closed form (Eq. (rmass); Hoang and Teubner, Eqs. (49), (50) of hep-ph/9707496):*)
(*    Delta^(1) = r1/r0, r0 = beta (3 - beta^2)/2, p = (1 - beta)/(1 + beta),*)
(*    r1 = (3 - beta^2)/2 B - (1 - beta)/16 (33 - 39 beta - 17 beta^2 + 7 beta^3) ln p + 3/8 beta (5 - 3 beta^2),*)
(*    B = (1 + beta^2)[2 ln(1-p) ln p + ln(1+p) ln p + 2 Li2(p) + Li2(p^2)] - 2 beta [2 ln(1-p) + ln(1+p)].*)
(*The imaginary part of the 1/eps pole of Pi^(2)_tot must vanish (finiteness of the cross section).  -> results/ee_amflow.csv*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file ee_amflow.wl  (after ee_optical.wl; about 10 minutes).  Interactive:  ~/hep/bin/wopen ee_amflow.wl, then "Run All Code".  AMFlow is loaded in a kernel of its own.*)


(* ::Section:: *)
(*Setup*)


srcDirAF$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
workAF$ = FileNameJoin[{srcDirAF$, "work", "ee_amflow"}];
Quiet[CreateDirectory[workAF$, CreateIntermediateDirectories -> True]];     (* AMFlow's cache is kept between runs *)
redAF$ = Get[FileNameJoin[{srcDirAF$, "results", "ee_optical_reduction.m"}]];
ep = Epsilon;
mastersAF$ = Union[Cases[{redAF$["A1t"], redAF$["dA1t"], redAF$["A2t"]}, _GLI, Infinity]];
Print["(a) masters: ", mastersAF$];
SetDirectory[workAF$];
Get[FileNameJoin[{$HomeDirectory, "hep", "AMFlow-2.0", "AMFlow.m"}]];
CacheDirectory[key_] := FileNameJoin[{workAF$, "cache", ToString[AMFlowInfo["Family"], InputForm] <> "_" <> key}];
SetReductionOptions["IBPReducer" -> "Kira"];
SetAMFOptions["DESolver" -> "MMA"];
SetGlobalOptions["SilentMode" -> True];
famAF$["k2m"] := (AMFlowInfo["Family"] = k2m; AMFlowInfo["Loop"] = {l1, l2}; AMFlowInfo["Leg"] = {q}; AMFlowInfo["Conservation"] = {};
   AMFlowInfo["Replacement"] = {q^2 -> s}; AMFlowInfo["Propagator"] = {l1^2 - msq, l2^2 - msq, (l1 - q)^2 - msq, (l2 - q)^2 - msq, (l1 - l2)^2});
famAF$["k1m"] := (AMFlowInfo["Family"] = k1m; AMFlowInfo["Loop"] = {l1}; AMFlowInfo["Leg"] = {q}; AMFlowInfo["Conservation"] = {};
   AMFlowInfo["Replacement"] = {q^2 -> s}; AMFlowInfo["Propagator"] = {l1^2 - msq, (l1 - q)^2 - msq});
orderAF$ = <|"k2m" -> 6, "k1m" -> 4|>;     (* up to eps^2 *)
loopsAF$ = <|"k2m" -> 2, "k1m" -> 1|>;
betasAF$ = {1/10, 3/10, 1/2, 7/10, 9/10};


(* ::Section:: *)
(*(a) the masters with AMFlow*)


(* SolveIntegrals may return more integrals than asked for: match the results by their labels j[family, indices] *)
solveAF$[s0_] := Module[{res = {}, sel, out},
   Do[famAF$[f]; AMFlowInfo["Numeric"] = {s -> s0, msq -> 1}; AMFlowInfo["NThread"] = 4;
    sel = Select[mastersAF$, #[[1]] === f &];
    out = SolveIntegrals[j[Symbol[f], Sequence @@ #[[2]]] & /@ sel, 25, orderAF$[f]];
    res = Join[res, (# -> E^(loopsAF$[f] ep EulerGamma) (j[Symbol[f], Sequence @@ #[[2]]] /. out)) & /@ sel],
    {f, {"k2m", "k1m"}}];
   res /. sym_Symbol /; SymbolName[sym] === "eps" :> ep];
timeAF$ = AbsoluteTime[];
valuesAF$ = Association[Table[b -> solveAF$[4/(1 - b^2)], {b, betasAF$}]];
ResetDirectory[];
Put[valuesAF$, FileNameJoin[{workAF$, "amflow_values.m"}]];
Print["(a) AMFlow done for beta = ", betasAF$, " in ", Round[AbsoluteTime[] - timeAF$], " s"];


(* ::Section:: *)
(*(b) Delta^(1)(beta)*)


serAF$[x_] := Normal[Series[x, {ep, 0, 0}]];
htAF$[b_] := Module[{p = (1 - b)/(1 + b), bb},
   bb = (1 + b^2) (2 Log[1 - p] Log[p] + Log[1 + p] Log[p] + 2 PolyLog[2, p] + PolyLog[2, p^2]) - 2 b (2 Log[1 - p] + Log[1 + p]);
   ((3 - b^2)/2 bb - (1 - b)/16 (33 - 39 b - 17 b^2 + 7 b^3) Log[p] + 3/8 b (5 - 3 b^2))/(b (3 - b^2)/2)];
rowsAF$ = Table[Module[{s0 = 4/(1 - b^2), v = valuesAF$[b], sub, p1, dp1, p2, dm, tot, im1, d1},
    sub[x_] := x /. v /. {qq -> s0, mt -> 1, gS -> 1, D -> 4 - 2 ep};
    p1 = sub[CA redAF$["A1t"] I/(I (D - 1) qq)];
    dp1 = sub[CA redAF$["dA1t"] I/(I (D - 1) qq)];
    p2 = sub[redAF$["A2t"] (I)^2/(I (D - 1) qq)];
    dm = sub[-CF (D - 1) (D - 2) GLI["k1m", {1, 0}]/(2 (D - 3))];
    tot = serAF$[p2 + dm dp1] /. {CA -> 3, CF -> 4/3};
    im1 = Im[Coefficient[serAF$[p1] /. CA -> 3, ep, 0]];
    d1 = Im[Coefficient[tot, ep, 0]]/(4 (4/3) im1);
    {b, N[d1, 20], N[htAF$[b], 20], Abs[Im[Coefficient[tot, ep, -1]]], Abs[Coefficient[tot, ep, -2]], N[im1/(-(4/3) 3 (4/9) Pi b (3 - b^2)/2), 20]}],
   {b, betasAF$}];
accAF$[x_] := If[x == 0, "< 10^" <> ToString[-Round[Accuracy[x]]], ToString[ScientificForm[N[x, 3]]]];
Do[Print["(b) beta = ", N[r[[1]]], ":  Delta^(1) = ", InputForm[N[r[[2]], 16]], ",  closed form ", InputForm[N[r[[3]], 16]], ",  |difference| ",
   accAF$[Abs[r[[2]] - r[[3]]]], ";  |Im eps^-1|, |eps^-2| of Pi^(2)_tot: ", accAF$[r[[4]]], ", ", accAF$[r[[5]]],
   ";  Im Pi^(1)/(-(4/3) N Q^2 pi r0) = ", InputForm[N[r[[6]], 12]]], {r, rowsAF$}];


(* ::Subsubsection:: *)
(*Inspect: Delta^(1)(beta) against the closed form*)


If[$Notebooks, Show[Plot[htAF$[b], {b, 0.05, 0.99}, PlotRange -> {0, 12}], ListPlot[rowsAF$[[All, {1, 2}]], PlotStyle -> Red]]]


(* ::Section:: *)
(*Results*)


Export[FileNameJoin[{srcDirAF$, "results", "ee_amflow.csv"}],
  StringRiffle[Prepend[StringRiffle[ToString[CForm[N[#]]] & /@ #, ","] & /@ rowsAF$, "beta,delta1_amflow,delta1_closed,abs_im_pole1,abs_pole2,im_pi1_over_lo"], "\n"] <> "\n", "Text"];
Print["(c) wrote results/ee_amflow.csv"];
