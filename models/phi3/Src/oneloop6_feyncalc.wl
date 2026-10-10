(* ::Package:: *)

(* ::Title:: *)
(*Step (4): one-loop check in d = 6 (FeynCalc in D = 6 - 2 Epsilon, dimension shift to Package-X and LoopTools)*)


(* ::Text:: *)
(*The FeynArts amplitudes are the same as in d = 4 (the diagrams do not depend on D),*)
(*  A_n = I Pi^2 (gphi^n / S) PaVe,   S = 2, 2, 1,*)
(*but the PaVe functions are now read in D = 6 - 2 Epsilon.  The note's V_n is*)
(*V_n = A_n/(2 Pi)^D = (gphi^n / S) I_N.*)
(*(a) diagrams and amplitudes (as in oneloop4_feyncalc.wl).*)
(*(b) FeynCalc's Feynman parametrization (FCFeynmanParametrize with D -> 6 - 2 Epsilon) of the*)
(*    scalar integrals I_1, I_2, I_3, compared numerically with the note's general formula*)
(*    (App. C); the UV poles of V_n (Table 2), the MS-bar counterterms divided by DeltaUV*)
(*    (Eq. (8)), beta(g) from g_0 = mu^Epsilon (g + deltag)(1 + deltaZ)^(-3/2) (Eq. (14)), and the*)
(*    MS-bar finite part of the tadpole integral.*)
(*(c) Package-X and LoopTools through the dimension shift (note, App. H)*)
(*      PaVe^(D+2) = -2 Pi PaVe_00^(D)        (FeynCalc normalization, d^D q/(I Pi^2)),*)
(*    i.e. the D = 6 - 2 Epsilon scalar integrals are -2 Pi times the g^{mu nu} coefficients*)
(*    A00, B00, C00 in D = 4 - 2 Epsilon, which Package-X and LoopTools can evaluate.*)
(*    The poles are compared with (b).  The MS-bar finite parts X_N defined by*)
(*      mu^(2 Epsilon) I_N = I/(4 Pi)^3 [c_N DeltaUV + X_N],   X_N = A0^(6), B0^(6), C0^(6),*)
(*    are compared with closed forms and written to Src/results/oneloop6_mathematica.csv*)
(*    (m = mu = 1).  Note: LoopTools 2.16 on this Mac returns wrong C0 below threshold (d = 4*)
(*    check), and its C00 is built from C0; its C00 values are kept in the CSV as a record.*)
(**)
(*Usage:  wolframscript -file oneloop6_feyncalc.wl      (run generate_Phi3.wl first)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop6_feyncalc.wl.  Interactive:  ~/hep/bin/wopen oneloop6_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];

srcDirOL6$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Section:: *)
(*patched copy of the FeynRules-generated FeynArts model*)


modelTmpDirOL6$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOL6$, "generated", "Phi3_FA"}], FileNameJoin[{modelTmpDirOL6$, "Phi3_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOL6$, "Phi3_FA"}], Quiet -> True];
modelOL6$ = FileNameJoin[{modelTmpDirOL6$, "Phi3_FA", "Phi3_FA"}];
insertOL6$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles},
   Model -> modelOL6$, GenericModel -> modelOL6$];


(* ::Section:: *)
(*(a) diagrams and amplitudes*)


diagTadOL6$ = insertOL6$[CreateTopologies[1, 1 -> 0], {S[1]} -> {}];
diagSEOL6$  = insertOL6$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {S[1]} -> {S[1]}];
diagVtxOL6$ = insertOL6$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}],
   {S[1]} -> {S[1], S[1]}];


(* ::Subsubsection:: *)
(*Inspect: the three diagrams (tadpole, self-energy, triangle)*)


If[$Notebooks,
  Row[Flatten[Show[#, ImageSize -> 180] & /@ Render[Paint[#, ColumnsXRows -> 1, Numbering -> Simple, DisplayFunction -> Identity]] & /@ {diagTadOL6$, diagSEOL6$, diagVtxOL6$}], "    "]
]


ampOL6$[diags_, in_, out_] := FCE[TID[FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1],
     IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q}, ChangeDimension -> D,
     List -> False, SMP -> False, DropSumOver -> True], q, ToPaVe -> True]];

ampTadOL6$ = ampOL6$[diagTadOL6$, {p}, {}];
ampSEOL6$  = ampOL6$[diagSEOL6$, {p}, {p}];
ampVtxOL6$ = ampOL6$[diagVtxOL6$, {p}, {k1, k2}];
c0OL6$ = First[Cases[ampVtxOL6$, _C0, Infinity]];
Print["(a) number of diagrams (expect 1, 1, 1): ",
  Length /@ {CreateFeynAmp[diagTadOL6$], CreateFeynAmp[diagSEOL6$], CreateFeynAmp[diagVtxOL6$]}];
Print["(a) A_n - I Pi^2 gphi^n/S PaVe (expect 0, 0, 0): ", Simplify /@ {ampTadOL6$ - I Pi^2 gphi/2 A0[m^2],
   ampSEOL6$ - I Pi^2 gphi^2/2 B0[SPD[p], m^2, m^2], ampVtxOL6$ - I Pi^2 gphi^3 c0OL6$}];


(* ::Subsubsection:: *)
(*Inspect: each amplitude after the tensor reduction (the PaVe functions are now read in D = 6 - 2 Epsilon)*)


If[$Notebooks,
  TableForm[{{"tadpole", TraditionalForm[ampTadOL6$]}, {"self-energy", TraditionalForm[ampSEOL6$]}, {"triangle", TraditionalForm[ampVtxOL6$]}}]
]


(* ::Section:: *)
(*(b) Feynman parametrization in D = 6 - 2 Epsilon*)


kOL6$ = (4 Pi)^3;
dimOL6$ = 6 - 2 Epsilon;
invRulesOL6$ = {SPD[p, p] -> psq, SPD[k1, k1] -> p1sq, SPD[k2, k2] -> p2sq, SPD[k1, k2] -> (p3sq - p1sq - p2sq)/2};
scalarIntsOL6$ = {FAD[{q, m}], FAD[{q, m}, {q + p, m}], FAD[{q, m}, {q + k1, m}, {q + k1 + k2, m}]};
(* the note's q_j for I_1, I_2, I_3 (Eq. (3)), as coefficient vectors over a momentum basis with
   Gram matrix gramOL6$: I_2 has q = {0, p}, I_3 has q = {0, k1, k1 + k2} *)
qVecOL6$ = {{{}}, {{0}, {1}}, {{0, 0}, {1, 0}, {1, 1}}};
gramOL6$ = {{{}}, {{psq}}, {{p1sq, (p3sq - p1sq - p2sq)/2}, {(p3sq - p1sq - p2sq)/2, p2sq}}};
(* FCFeynmanParametrize with the "Textbook" prefactor gives int d^D q/(2 Pi)^D of the integrand,
   i.e. the note's I_N, as {integrand, prefactor, Feynman parameters} *)
paramOL6$ = FCE[FCFeynmanParametrize[#, {q}, Names -> x, FCReplaceD -> {D -> dimOL6$},
      FeynmanIntegralPrefactor -> "Textbook"]] /. invRulesOL6$ & /@ scalarIntsOL6$;
(* on the simplex sum x_j = 1, eliminating x[1] *)
onSimplexOL6$[n_, expr_] := If[n == 1, expr, expr /. x[1] -> 1 - Sum[x[j], {j, 2, n}]];
integrandOL6$[n_] := onSimplexOL6$[n, paramOL6$[[n, 1]] paramOL6$[[n, 2]]];
simplexIntegrateOL6$[n_, expr_] := Switch[n,
   1, expr,
   2, Integrate[expr, {x[2], 0, 1}],
   3, Integrate[expr, {x[2], 0, 1}, {x[3], 0, 1 - x[2]}]];
(* the note's general formula, Eq. (4): I_N = I (-1)^N Gamma(N - D/2)/(4 Pi)^(D/2) int dF Delta^(D/2 - N) *)
(* Delta = m^2 - sum_j x_j q_j^2 + (sum_j x_j q_j)^2 *)
noteDeltaOL6$[1] = m^2;
noteDeltaOL6$[n_] := Module[{qv = qVecOL6$[[n]], g = gramOL6$[[n]], qsum},
   qsum = Sum[x[j] qv[[j]], {j, 1, n}];
   onSimplexOL6$[n, Expand[m^2 - Sum[x[j] qv[[j]] . g . qv[[j]], {j, 1, n}] + qsum . g . qsum]]];
noteIntegrandOL6$[n_] := I (-1)^n Gamma[n - dimOL6$/2]/(4 Pi)^(dimOL6$/2) noteDeltaOL6$[n]^(dimOL6$/2 - n);
SeedRandom[6];
checkPointOL6$ := Join[{Epsilon -> 1/7, m -> 13/10, psq -> RandomInteger[{-30, 30}]/7,
    p1sq -> RandomInteger[{-30, 30}]/7, p2sq -> RandomInteger[{-30, 30}]/7, p3sq -> RandomInteger[{-30, 30}]/7},
   {x[2] -> 1/5, x[3] -> 1/3}];
Print["(b) FCFeynmanParametrize / note's Eq. (4) at random points (expect 1): ",
  Table[Chop[N[(integrandOL6$[n]/noteIntegrandOL6$[n]) /. #, 30], 10^-25] & /@ Table[checkPointOL6$, {3}], {n, 3}]];


(* ::Subsubsection:: *)
(*Inspect: the Feynman-parameter integrands of I_1, I_2, I_3 in D = 6 - 2 Epsilon (x[1] eliminated)*)


If[$Notebooks,
  TableForm[{{"I_1", TraditionalForm[integrandOL6$[1]]}, {"I_2", TraditionalForm[integrandOL6$[2]]}, {"I_3", TraditionalForm[integrandOL6$[3]]}}]
]


(* UV poles of I_N: the 1/Epsilon coefficient is a polynomial in the x_j *)
iPoleOL6$[n_] := Simplify[simplexIntegrateOL6$[n, Expand[SeriesCoefficient[integrandOL6$[n], {Epsilon, 0, -1}]]]];
{i1PoleOL6$, i2PoleOL6$, i3PoleOL6$} = iPoleOL6$ /@ {1, 2, 3};
Print["(b) 1/eps coefficients of I_1, I_2, I_3 = ", InputForm /@ {i1PoleOL6$, i2PoleOL6$, i3PoleOL6$}];
Print["(b)   Table 2, d = 6 column -> ", Simplify[{i1PoleOL6$ + I m^4/(2 kOL6$), i2PoleOL6$ + I (m^2 - psq/6)/kOL6$,
     i3PoleOL6$ + I/(2 kOL6$)}] === {0, 0, 0}];
(* V_n = gphi^n I_N / S; MS-bar counterterms delta = c DeltaUV with the c fixed by the poles (App. D) *)
{v1PoleOL6$, v2PoleOL6$, v3PoleOL6$} = {gphi/2 i1PoleOL6$, gphi^2/2 i2PoleOL6$, gphi^3 i3PoleOL6$};
cZOL6$ = Simplify[I D[v2PoleOL6$, psq]];
cmOL6$ = Simplify[-I (v2PoleOL6$ /. psq -> 0)];
cgOL6$ = Simplify[-I v3PoleOL6$];
Print["(b) MS-bar counterterms / DeltaUV: deltaZ = ", InputForm[cZOL6$], ", deltam = ", InputForm[cmOL6$],
  ", deltag = ", InputForm[cgOL6$]];
Print["(b)   Eq. (8) -> ", Simplify[{cZOL6$ + gphi^2/(12 kOL6$), cmOL6$ + gphi^2 m^2/(2 kOL6$), cgOL6$ + gphi^3/(2 kOL6$)}] === {0, 0, 0}];
(* beta from the mu-independence of g_0 = mu^Epsilon f(g), f = g + deltag - 3/2 g deltaZ (one loop) *)
fOL6$ = gphi + (cgOL6$ - 3/2 gphi cZOL6$) deltaUV;
betaEpsOL6$ = Normal[Series[-Epsilon fOL6$/D[fOL6$, gphi], {gphi, 0, 3}]];
betaOL6$ = Simplify[SeriesCoefficient[betaEpsOL6$ /. deltaUV -> 1/Epsilon - EulerGamma + Log[4 Pi], {Epsilon, 0, 0}]];
Print["(b) beta_eps = ", InputForm[Simplify[betaEpsOL6$]], ";  beta(Epsilon -> 0) = ", InputForm[betaOL6$],
  "   Eq. (14) -> ", Simplify[betaOL6$ + 3 gphi^3/(4 kOL6$)] === 0];
(* MS-bar finite part of the tadpole integral: mu^(2 Epsilon) I_1 = I/K [c_1 DeltaUV + A0^(6)] *)
msbarSeriesOL6$[expr_] := Module[{s = Series[expr, {Epsilon, 0, 0}]},
   {SeriesCoefficient[s, -1], SeriesCoefficient[s, 0] - SeriesCoefficient[s, -1] (Log[4 Pi] - EulerGamma)}];
a06ParamOL6$ = Simplify[msbarSeriesOL6$[mu^(2 Epsilon) integrandOL6$[1]][[2]]/(I/kOL6$), m > 0 && mu > 0];
Print["(b) MS-bar A0^(6) from the parametrization = ", InputForm[a06ParamOL6$],
  "   note: -(m^4/2)(3/2 - Log[m^2/mu^2]) -> ", Simplify[PowerExpand[a06ParamOL6$ + m^4/2 (3/2 - Log[m^2/mu^2])]] === 0];


(* ::Subsubsection:: *)
(*Inspect: the 1/eps coefficients of I_1, I_2, I_3 and the MS-bar counterterms divided by DeltaUV*)


If[$Notebooks,
  TableForm[{{"I_1", TraditionalForm[i1PoleOL6$]}, {"I_2", TraditionalForm[i2PoleOL6$]}, {"I_3", TraditionalForm[i3PoleOL6$]}, {"deltaZ", TraditionalForm[cZOL6$]}, {"deltam", TraditionalForm[cmOL6$]}, {"deltag", TraditionalForm[cgOL6$]}}]
]


(* ::Subsubsection:: *)
(*Inspect: beta in D dimensions and at Epsilon -> 0*)


If[$Notebooks,
  TableForm[{{"beta_eps", TraditionalForm[Simplify[betaEpsOL6$]]}, {"beta", TraditionalForm[betaOL6$]}}]
]


(* ::Section:: *)
(*(c) Package-X and LoopTools through the dimension shift*)


shiftOL6$ = {A0[a_] :> -2 Pi PaVe[0, 0, {}, {a}], B0[s_, a_, b_] :> -2 Pi PaVe[0, 0, {s}, {a, b}],
   C0[s1_, s2_, s3_, a_, b_, c_] :> -2 Pi PaVe[0, 0, {s1, s2, s3}, {a, b, c}]};
(* V_n = A_n/(2 Pi)^D with D = 6 - 2 Epsilon; returns {1/Epsilon coefficient, MS-bar finite part} of V_n *)
msbar6OL6$[ampValue_] := msbarSeriesOL6$[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^6];
normOL6$ = {I gphi/(2 kOL6$), I gphi^2/(2 kOL6$), I gphi^3/kOL6$};   (* V_n^R = norm_n X_N, Eq. (11) of the note *)
logRulesOL6$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};

pxTadOL6$ = msbar6OL6$[PaXEvaluate[ampTadOL6$ /. shiftOL6$]];
pxSEOL6$  = msbar6OL6$[PaXEvaluate[ampSEOL6$ /. shiftOL6$ /. SPD[p] -> psq]];
pxVtxOL6$ = msbar6OL6$[PaXEvaluate[ampVtxOL6$ /. shiftOL6$]];
Print["(c) Package-X poles of V_1, V_2, V_3 minus (b) (expect 0, 0, 0): ",
  Simplify[{pxTadOL6$[[1]] - v1PoleOL6$, pxSEOL6$[[1]] - v2PoleOL6$, pxVtxOL6$[[1]] - v3PoleOL6$}]];
a06PXOL6$ = Simplify[pxTadOL6$[[2]]/normOL6$[[1]] /. ScaleMu -> mu, m > 0 && mu > 0];
Print["(c) Package-X A0^(6) - (b) = ", Simplify[PowerExpand[a06PXOL6$ - a06ParamOL6$]], "  (expect 0)"];
(* B0^(6) against the closed form of App. H, B0^(6) = -m^2 + p^2/9 + (m^2/3) Log[m^2/mu^2]
   - (2/3)(m^2 - p^2/4) B0, with the d = 4 MS-bar B0 also from Package-X *)
b06PXOL6$ = Simplify[pxSEOL6$[[2]]/normOL6$[[2]] /. ScaleMu -> mu, m > 0 && mu > 0];
b04PXOL6$ = Module[{s = Series[(2 Pi)^(2 Epsilon) PaXEvaluate[I Pi^2 gphi^2/2 B0[psq, m^2, m^2]]/(2 Pi)^4, {Epsilon, 0, 0}]},
   Simplify[(SeriesCoefficient[s, 0] - SeriesCoefficient[s, -1] (Log[4 Pi] - EulerGamma))/(I gphi^2/(2 (4 Pi)^2)) /. ScaleMu -> mu, m > 0 && mu > 0]];
Print["(c) Package-X B0^(6) - closed form (App. H) = ",
  Simplify[PowerExpand[b06PXOL6$ - (-m^2 + psq/9 + m^2/3 Log[m^2/mu^2] - 2/3 (m^2 - psq/4) b04PXOL6$)]], "  (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: the MS-bar A0^(6) and B0^(6) from Package-X through the dimension shift*)


If[$Notebooks,
  TableForm[{{"A0^(6)", TraditionalForm[a06PXOL6$]}, {"B0^(6)(p^2 = psq)", TraditionalForm[b06PXOL6$]}}]
]


(* numerical values at m = mu = 1 *)
PaXEvaluate[B0[2, 1, 1]];   (* makes sure Package-X (context X`) is loaded *)
(* Package-X's ScalarC0 takes masses, FeynCalc's C0 squared masses *)
c0ToPXOL6$ = C0[s1_, s2_, s3_, a_, b_, c_] :> X`ScalarC0[s1, s2, s3, Sqrt[a], Sqrt[b], Sqrt[c]];
vtxAtOL6$[s1_, s2_, s3_] := ampVtxOL6$ /. {SPD[k1, k1] -> s1, SPD[k2, k2] -> s2, SPD[k1, k2] -> (s3 - s1 - s2)/2} /. m -> 1;
pxXOL6$[n_, amp_] := Chop[N[Simplify[msbar6OL6$[PaXEvaluate[amp /. shiftOL6$]][[2]]/normOL6$[[n]] /. ScaleMu -> 1 /. logRulesOL6$] /. c0ToPXOL6$, 20], 10^-18];
(* LoopTools' C00 at exactly zero external momenta comes back Indeterminate; it is recorded as NaN *)
ltXOL6$[n_, amp_] := Module[{v = Chop[msbar6OL6$[LToolsEvaluate[amp /. shiftOL6$]][[2]]/normOL6$[[n]]]},
   If[NumericQ[v], v, Indeterminate]];

rowsOL6$ = {{"A06", 1, 0, 0, pxXOL6$[1, ampTadOL6$ /. m -> 1], ltXOL6$[1, ampTadOL6$ /. m -> 1]}};
Do[AppendTo[rowsOL6$, {"B06", s, 1, 1, pxXOL6$[2, ampSEOL6$ /. {SPD[p] -> s, m -> 1}],
    ltXOL6$[2, ampSEOL6$ /. {SPD[p] -> N[s], m -> 1}]}],
  {s, {-10, -5, -1, 0, 1, 2, 3, 39/10, 4, 41/10, 5, 8, 12, 20, 30}}];
Do[AppendTo[rowsOL6$, {"C06", Sequence @@ inv, pxXOL6$[3, vtxAtOL6$ @@ inv], ltXOL6$[3, vtxAtOL6$ @@ (N /@ inv)]}],
  {inv, {{0, 0, 0}, {1, 1, 1}, {1, 1, 7/2}, {1, 1, 5}, {1, 1, 10}}}];

resultsDirOL6$ = FileNameJoin[{srcDirOL6$, "results"}];
Quiet[CreateDirectory[resultsDirOL6$]];
numStrOL6$[x_] := If[x === Indeterminate, "nan", ToString[CForm[N[x]]]];   (* machine-precision decimal *)
csvLinesOL6$ = Prepend[
   StringRiffle[Join[{#[[1]]}, numStrOL6$ /@ {#[[2]], #[[3]], #[[4]], Re[#[[5]]], Im[#[[5]]], Re[#[[6]]], Im[#[[6]]]}], ","] & /@ rowsOL6$,
   "func,arg1,arg2,arg3,re_packagex,im_packagex,re_looptools,im_looptools"];
Export[FileNameJoin[{resultsDirOL6$, "oneloop6_mathematica.csv"}], StringRiffle[csvLinesOL6$, "\n"] <> "\n", "Text"];
Print["(c) wrote ", Length[rowsOL6$], " rows to results/oneloop6_mathematica.csv"];
Print["(c) max |Package-X - LoopTools| for A0^(6), B0^(6) = ", Max[Abs[#[[5]] - #[[6]]] & /@ Select[rowsOL6$, #[[1]] =!= "C06" &]]];
Print["(c) |Package-X - LoopTools| for C0^(6) rows = ", Abs[#[[5]] - #[[6]]] & /@ Select[rowsOL6$, #[[1]] === "C06" &],
  "  (Indeterminate: LoopTools has no value)"];


(* ::Subsubsection:: *)
(*Inspect: the values (LoopTools C00 inherits its C0 error below threshold)*)


If[$Notebooks,
  TableForm[{#[[1]], N[#[[2]]], N[#[[3]]], N[#[[4]]], NumberForm[#[[5]], 12], If[#[[6]] === Indeterminate, "NaN", NumberForm[#[[6]], 12]]} & /@ rowsOL6$, TableHeadings -> {None, {"func", "arg1", "arg2", "arg3", "Package-X", "LoopTools"}}]
]


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirOL6$, DeleteContents -> True];
