(* ::Package:: *)

(* ::Title:: *)
(*Step (16): the master integrals with AMFlow 2.0 (Kira 3.1) and the finiteness of the two-loop self-energy*)


(* ::Text:: *)
(*Reads Shat in terms of the master integrals from Src/results/twoloop4_reduction.m (twoloop4_feyncalc.wl) and evaluates the masters with AMFlow 2.0 (auxiliary mass flow, IBP reduction with Kira 3.1, Mathematica's differential equation solver), with 30 digits and up to eps^2 (the third argument of SolveIntegrals counts the orders from eps^(-2L) of an L-loop family), at s = p^2 = -1, 1, 5, 12 (m = mu-bar = 1): below the thresholds, on shell, between the two- and three-particle thresholds s = 4 and 9, and above both.  AMFlow's integrals are J = Integrate[Product[d^Dq/(I Pi^(D/2))] Product[1/(q_i^2 - m^2 + I0)^nu_i]] (D = 4 - 2 eps).*)
(*(a) The masters at each point, converted to the normalization of TSIL's "bold" integrals (Euclidean, measure E^(eps EulerGamma) d^Dq_E/Pi^(D/2) per loop; J_TSIL = (-1)^(Sum nu) E^(L eps EulerGamma) J for L loops), written as Laurent coefficients to Src/results/twoloop4_amflow.csv for twoloop4_numeric.py.*)
(*(b) The Laurent expansion of Shat: the coefficients of eps^-2 and eps^-1 must vanish, i.e. the insertion of the one-loop MS-bar mass counterterm alone makes the two-loop self-energy finite.  The finite part Sigma^(2)/(g^4/(16 Pi^2)^2) is written to Src/results/twoloop4_sigma.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file twoloop4_amflow.wl  (after twoloop4_feyncalc.wl; about 5 minutes).  Interactive:  ~/hep/bin/wopen twoloop4_amflow.wl, then "Run All Code"; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).  AMFlow is loaded in a kernel of its own (not together with FeynCalc).*)


(* ::Section:: *)
(*Setup*)


srcDirAM$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
workAM$ = FileNameJoin[{srcDirAM$, "work", "twoloop4_amflow"}];
If[DirectoryQ[workAM$], DeleteDirectory[workAM$, DeleteContents -> True]];
CreateDirectory[workAM$, CreateIntermediateDirectories -> True];
SetDirectory[workAM$];
Get[FileNameJoin[{$HomeDirectory, "hep", "AMFlow-2.0", "AMFlow.m"}]];
(* AMFlow puts its cache next to the running file ($InputFileName in batch, NotebookFileName[] in a notebook, which
   fails when cells are evaluated without the notebook); keep it in the working directory instead *)
CacheDirectory[key_] := FileNameJoin[{workAM$, "cache", ToString[AMFlowInfo["Family"], InputForm] <> "_" <> key}];
SetReductionOptions["IBPReducer" -> "Kira"];
(* the Mathematica solver: with the default C++ solver (WSTP link), two of three runs hung in a parallel subkernel on a
   small one-loop subsystem *)
SetAMFOptions["DESolver" -> "MMA"];
SetGlobalOptions["SilentMode" -> True];

shatAM$ = Get[FileNameJoin[{srcDirAM$, "results", "twoloop4_reduction.m"}]];
mastersAM$ = Union[Cases[shatAM$, _GLI, Infinity]];
Print["(a) masters of Shat: ", mastersAM$];
pointsAM$ = {-1, 1, 5, 12};
precAM$ = 30;
(* SolveIntegrals' third argument counts the orders from eps^(-2L) of an L-loop family: 2L + 2 gives eps^2 *)
epsOrderAM$ = <|"se2" -> 6, "se1" -> 4|>;


(* ::Section:: *)
(*(a) the master integrals with AMFlow*)


famInfoAM$["se2"] := (AMFlowInfo["Family"] = se2; AMFlowInfo["Loop"] = {q1, q2}; AMFlowInfo["Leg"] = {p};
   AMFlowInfo["Conservation"] = {}; AMFlowInfo["Replacement"] = {p^2 -> s};
   AMFlowInfo["Propagator"] = {q1^2 - msq, (q1 - p)^2 - msq, q2^2 - msq, (q2 - p)^2 - msq, (q1 - q2)^2 - msq});
famInfoAM$["se1"] := (AMFlowInfo["Family"] = se1; AMFlowInfo["Loop"] = {q1}; AMFlowInfo["Leg"] = {p};
   AMFlowInfo["Conservation"] = {}; AMFlowInfo["Replacement"] = {p^2 -> s};
   AMFlowInfo["Propagator"] = {q1^2 - msq, (q1 - p)^2 - msq});
toJAM$[GLI[f_, n_]] := j[Symbol[f], Sequence @@ n];

solveAM$[s0_] := Module[{res = {}},
   Do[
    famInfoAM$[f];
    AMFlowInfo["Numeric"] = {s -> s0, msq -> 1};
    AMFlowInfo["NThread"] = 4;
    res = Join[res, SolveIntegrals[toJAM$ /@ Select[mastersAM$, #[[1]] === f &], precAM$, epsOrderAM$[f]]],
    {f, {"se2", "se1"}}];
   res];
valuesAM$ = AssociationMap[solveAM$, pointsAM$];
Put[valuesAM$, FileNameJoin[{workAM$, "amflow_values.m"}]];        (* the raw results, for re-assembling without AMFlow *)
Print["(a) AMFlow done for s = ", pointsAM$];


(* ::Subsubsection:: *)
(*Inspect: the kite M = J[se2,11111] at the four points*)


If[$Notebooks, Grid[Prepend[Table[{s0, j[se2, 1, 1, 1, 1, 1] /. valuesAM$[s0]}, {s0, pointsAM$}], {"s", "J[se2,11111]"}], Frame -> All]]


(* TSIL normalization: (-1)^(Sum nu) E^(L eps EulerGamma) J *)
loopsAM$[GLI[f_, _]] := If[f === "se2", 2, 1];
tsilAM$[g : GLI[f_, n_], s0_] := (-1)^Total[n] E^(loopsAM$[g] eps EulerGamma) (toJAM$[g] /. valuesAM$[s0]);
coeffAM$[expr_, k_] := SeriesCoefficient[expr, {eps, 0, k}];
fmtAM$[v_] := If[v == 0, "0", ToString[CForm[N[v, 25]]]];
writeCSVAM$[file_, header_, rows_] := Export[file, StringRiffle[Prepend[StringRiffle[#, ","] & /@ rows, StringRiffle[header, ","]], "\n"] <> "\n", "Text"];
rowsAM$ = Flatten[Table[
    With[{ser = Normal[Series[tsilAM$[g, s0], {eps, 0, 1}]]},
     Table[{ToString[s0], g[[1]] <> StringJoin[ToString /@ g[[2]]], ToString[k], fmtAM$[Re[coeffAM$[ser, k]]], fmtAM$[Im[coeffAM$[ser, k]]]}, {k, -2, 1}]],
    {s0, pointsAM$}, {g, mastersAM$}], 2];
writeCSVAM$[FileNameJoin[{srcDirAM$, "results", "twoloop4_amflow.csv"}], {"s", "integral", "eps_power", "re", "im"}, rowsAM$];
Print["(a) wrote Src/results/twoloop4_amflow.csv (", Length[rowsAM$], " rows)"];


(* ::Section:: *)
(*(b) the Laurent expansion of Shat*)


(* Laurent coefficients of Shat as explicit sums: (exact coefficient of each master, expanded in eps) x (AMFlow's
   30-digit expansion of the master), so that a vanishing pole coefficient carries the number of digits to which it
   vanishes *)
shatSeriesAM$[s0_] := Module[{expr = shatAM$ /. {m -> 1, pp -> s0}, terms},
   terms = Table[{CoefficientList[Normal[Series[Coefficient[expr, g] eps^2, {eps, 0, 4}]], eps],
      CoefficientList[Normal[(toJAM$[g] /. valuesAM$[s0])] eps^2 // Expand, eps]}, {g, mastersAM$}];
   (* element i of either list is the coefficient of eps^(i-3); the eps^(k-3) coefficient of the product, k = 1, 2, 3 *)
   Table[Total[Table[With[{c = N[t[[1]], 40], v = t[[2]]},
       Sum[If[1 <= k + 3 - i <= Length[v], c[[i]] v[[k + 3 - i]], 0], {i, 1, Length[c]}]], {t, terms}]],
    {k, 1, 3}]];
shatAllAM$ = AssociationMap[shatSeriesAM$, pointsAM$];
(* a vanishing coefficient comes out as 0 with the number of digits to which it vanishes (its accuracy) *)
zeroAM$[c_] := If[c == 0, "0 to " <> ToString[Round[Accuracy[c]]] <> " digits", ToString[ScientificForm[N[Abs[c], 3]]]];
Do[Print["(b) s = ", s0, ": Shat eps^-2 ", zeroAM$[shatAllAM$[s0][[1]]], ", eps^-1 ", zeroAM$[shatAllAM$[s0][[2]]],
   " (expect 0);  finite part ", N[shatAllAM$[s0][[3]], 18]], {s0, pointsAM$}];
writeCSVAM$[FileNameJoin[{srcDirAM$, "results", "twoloop4_sigma.csv"}], {"s", "re_finite", "im_finite", "accuracy_eps_m2", "accuracy_eps_m1"},
  Table[{ToString[s0], fmtAM$[Re[shatAllAM$[s0][[3]]]], fmtAM$[Im[shatAllAM$[s0][[3]]]],
    ToString[Round[Accuracy[shatAllAM$[s0][[1]]]]], ToString[Round[Accuracy[shatAllAM$[s0][[2]]]]]}, {s0, pointsAM$}]];
Print["(b) wrote Src/results/twoloop4_sigma.csv"];


(* ::Subsubsection:: *)
(*Inspect: the Laurent coefficients of Shat*)


If[$Notebooks, Grid[Prepend[Table[Prepend[N[shatAllAM$[s0], 12], s0], {s0, pointsAM$}], {"s", "eps^-2", "eps^-1", "eps^0"}], Frame -> All]]


ResetDirectory[];
