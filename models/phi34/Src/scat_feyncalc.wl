(* ::Package:: *)

(* ::Title:: *)
(*Step (4): one-loop phi phi -> phi phi of phi^3 + phi^4 in d = 4 (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/phi34, step (4).  (a) FeynArts diagrams from Src/generated/Phi34_FA: one loop, 2 -> 2, without tadpoles (cancelled by Y) and without external-leg corrections (truncated amplitude): 42 diagrams = 12 1PI (3 fish, 6 lambda g^2 triangles, 3 boxes) + 24 vertex corrections (4 per vertex, 2 vertices, 3 channels) + 6 self-energy insertions (2 per channel).  With PreFactor -> 1 the sum of diagrams is A = i M (2 Pi)^D, i.e. M = -I A/(2 Pi)^D.  The amplitude is compared symbolically with the note's Eq. (9) (eq:M1),*)
(*    M1 (4 Pi)^2 = g^4 [ sum D0 + sum_x ( 2 C0(x)/(x - m^2) + B0(x)/(2 (x - m^2)^2) ) ]*)
(*                + g^2 lambda sum_x [ 2 C0(x) + (B0(x) + 2 B0(m^2))/(x - m^2) + A0/(2 (x - m^2)^2) ] + lambda^2/2 sum_x B0(x),*)
(*using FeynCalc's normalization (int d^D q = I Pi^2 PaVe).  For equal masses and p_i^2 = m^2, D0 depends only on its two invariants (symmetrically), C0 only on the off-shell invariant.*)
(*(b) UV poles (Package-X) and the MS-bar counterterms of Eq. (5) on the tree diagrams, M_CT = -sum_x [g^2 deltam/(x - m^2)^2 + 2 g deltag/(x - m^2)] - deltalambda.*)
(*(c) the MS-bar amplitude M1 at the comparison points (m = g = lambda = mu = 1) with Package-X (A0, B0 analytic, C0 and D0 from Package-X's numerical ScalarC0 and ScalarD0) and with LoopTools (LToolsEvaluate), written to Src/results/scat_feyncalc.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file scat_feyncalc.wl  (run run_model_check.sh first); only the lines starting with (a), (b), (c) are printed.  Interactive:  open this file in Mathematica 14.2.1 (~/hep/bin/wopen scat_feyncalc.wl) and evaluate the cells in order with Shift+Return.  The cells under the "Inspect" headings are wrapped in If[$Notebooks, ...]: in the notebook (also with "Run All Code") they show the intermediate objects (diagrams, amplitudes of single diagrams, poles, numbers) without changing anything, and wolframscript skips them.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];


srcDirS4$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Text:: *)
(*A patched copy of the FeynRules-generated FeynArts model (FeynCalc's FeynArts needs FAPatch).*)


modelTmpDirS4$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirS4$, "generated", "Phi34_FA"}], FileNameJoin[{modelTmpDirS4$, "Phi34_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirS4$, "Phi34_FA"}], Quiet -> True];
modelS4$ = FileNameJoin[{modelTmpDirS4$, "Phi34_FA", "Phi34_FA"}];


(* ::Section:: *)
(*(a) Diagrams and amplitude*)


diagsS4$ = InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}],
   {S[1], S[1]} -> {S[1], S[1]}, InsertionLevel -> {Particles}, Model -> modelS4$, GenericModel -> modelS4$];
Print["(a) number of diagrams (expect 42: 12 1PI, 24 vertex corrections, 6 self-energy insertions): ", Length[CreateFeynAmp[diagsS4$]]];


(* ::Subsubsection:: *)
(*Inspect: the 42 diagrams*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diagsS4$, ColumnsXRows -> {6, 7}, Numbering -> Simple, DisplayFunction -> Identity]]
]


(* ::Text:: *)
(*The amplitude: FeynArts -> FeynCalc, tensor reduction (TID) to Passarino-Veltman functions, and the kinematics.*)


FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, m, m, m, m];
ampS4$ = FCE[FeynAmpDenominatorExplicit[TID[FCFAConvert[CreateFeynAmp[diagsS4$, Truncated -> True, PreFactor -> 1],
      IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {k1, k2}, LoopMomenta -> {q}, ChangeDimension -> D,
      List -> False, SMP -> False, DropSumOver -> True], q, ToPaVe -> True]]] /. (-3 m^2 + s + t + u) -> m^2;
(* SetMandelstam leaves k2^2 as s + t + u - 3 m^2, which is m^2 on shell (s + t + u = 4 m^2) *)


(* ::Subsubsection:: *)
(*Inspect: each diagram before and after the tensor reduction*)


If[$Notebooks,
  ampListS4$ = FCFAConvert[CreateFeynAmp[diagsS4$, Truncated -> True, PreFactor -> 1], IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {k1, k2}, LoopMomenta -> {q}, ChangeDimension -> D, List -> True, SMP -> False, DropSumOver -> True];
  Grid[Prepend[Table[{i, TraditionalForm[FCE[ampListS4$[[i]]]], TraditionalForm[FCE[FeynAmpDenominatorExplicit[TID[ampListS4$[[i]], q, ToPaVe -> True]]] /. (-3 m^2 + s + t + u) -> m^2]}, {i, Length[ampListS4$]}], {"diagram", "integrand", "after TID"}], Frame -> All, Alignment -> Left]
]


(* ::Text:: *)
(*Canonical names, valid for equal masses m and p_i^2 = m^2, and the hand-calculated form (Eq. (9) times I Pi^2 (4 Pi)^2/(4 Pi)^2).*)


canonS4$ = {D0[m^2, m^2, m^2, m^2, a_, b_, m^2, m^2, m^2, m^2] :> d0[Sort[{a, b}]],
   C0[m^2, m^2, x_, m^2, m^2, m^2] :> c0[x], C0[m^2, x_, m^2, m^2, m^2, m^2] :> c0[x],
   C0[x_, m^2, m^2, m^2, m^2, m^2] :> c0[x], B0[x_, m^2, m^2] :> b0[x], A0[m^2] :> a0};
handS4$ = I Pi^2 (gphi^4 (d0[Sort[{s, t}]] + d0[Sort[{s, u}]] + d0[Sort[{t, u}]] +
      Sum[2 c0[x]/(x - m^2) + b0[x]/(2 (x - m^2)^2), {x, {s, t, u}}]) +
    gphi^2 lamphi Sum[2 c0[x] + (b0[x] + 2 b0[m^2])/(x - m^2) + a0/(2 (x - m^2)^2), {x, {s, t, u}}] +
    lamphi^2/2 Sum[b0[x], {x, {s, t, u}}]);
Print["(a) PaVe functions in the amplitude: ", Union[Cases[ampS4$, _D0 | _C0 | _B0 | _A0, Infinity] /. canonS4$]];
Print["(a) A - I Pi^2 (4 Pi)^2 [Eq. (9) (eq:M1)] = ", Simplify[(ampS4$ /. canonS4$) - handS4$], "  (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: the amplitude collected by integral*)


If[$Notebooks,
  Collect[ampS4$ /. canonS4$, {gphi, lamphi}, Simplify] // TraditionalForm
]


(* ::Section:: *)
(*(b) UV poles and the MS-bar counterterm*)


(* ::Text:: *)
(*M = -I A/(2 Pi)^D with D = 4 - 2 Epsilon; the poles come from A0 and B0 only (C0 and D0 are finite in d = 4).*)


mBareS4$[ampValue_] := (2 Pi)^(2 Epsilon) (-I) ampValue/(2 Pi)^4;
dUVS4$ = 1/Epsilon - EulerGamma + Log[4 Pi];
ctS4$ = {(gphi^2 + lamphi m^2)/(2 (4 Pi)^2), 3 gphi lamphi/(2 (4 Pi)^2), 3 lamphi^2/(2 (4 Pi)^2)} dUVS4$;   (* deltam, deltag, deltalambda, Eq. (5) *)
mCTS4$ = -Sum[gphi^2 ctS4$[[1]]/(x - m^2)^2 + 2 gphi ctS4$[[2]]/(x - m^2), {x, {s, t, u}}] - ctS4$[[3]];
paxS4$ = PaXEvaluate[ampS4$ /. canonS4$ /. {b0[x_] :> B0[x, m^2, m^2], a0 -> A0[m^2]}];   (* c0, d0 are finite *)
poleS4$ = Simplify[SeriesCoefficient[mBareS4$[paxS4$], {Epsilon, 0, -1}]];
Print["(b) 1/eps coefficient of M (bare) = ", InputForm[poleS4$]];
Print["(b) 1/eps coefficient of M + M_CT = ", Simplify[poleS4$ + SeriesCoefficient[mCTS4$, {Epsilon, 0, -1}]], "  (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: the pole of the bare amplitude and of the counterterm*)


If[$Notebooks,
  {poleS4$, SeriesCoefficient[mCTS4$, {Epsilon, 0, -1}]} // TraditionalForm
]


(* ::Text:: *)
(*The MS-bar amplitude in terms of the MS-bar A0 and B0 of Eq. (6), compared with Eq. (9).*)


mMSS4$ = Simplify[SeriesCoefficient[mBareS4$[paxS4$] + mCTS4$, {Epsilon, 0, 0}] /. ScaleMu -> mu];
b0MSS4$[x_] := Module[{v = Series[(2 Pi)^(2 Epsilon) PaXEvaluate[I Pi^2 gphi^2/2 B0[x, m^2, m^2]]/(2 Pi)^4, {Epsilon, 0, 0}]},
   (SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma))/(I gphi^2/(2 (4 Pi)^2)) /. ScaleMu -> mu];
a0MSS4$ = m^2 (1 - Log[m^2/mu^2]);
handMSS4$ = 1/(4 Pi)^2 (gphi^4 (d0[Sort[{s, t}]] + d0[Sort[{s, u}]] + d0[Sort[{t, u}]] +
      Sum[2 c0[x]/(x - m^2) + b0MSS4$[x]/(2 (x - m^2)^2), {x, {s, t, u}}]) +
    gphi^2 lamphi Sum[2 c0[x] + (b0MSS4$[x] + 2 b0MSS4$[m^2])/(x - m^2) + a0MSS4$/(2 (x - m^2)^2), {x, {s, t, u}}] +
    lamphi^2/2 Sum[b0MSS4$[x], {x, {s, t, u}}]);
Print["(b) MS-bar M - Eq. (9) (eq:M1) with the MS-bar A0, B0 = ",
  Simplify[PowerExpand[mMSS4$ - handMSS4$ /. {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]}]], "  (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: the MS-bar amplitude*)


If[$Notebooks,
  mMSS4$ // Short[#, 8] &
]


(* ::Section:: *)
(*(c) Numerical values*)


(* ::Text:: *)
(*The six points sqrt(s) = 2.5, 5, 10 (m = 1) and cos(theta) = 0.3, 0.9; Package-X's numerical functions take masses (FeynCalc: squared masses) and machine numbers.*)


pointsS4$ = Flatten[Table[Module[{ss = rs^2, p2}, p2 = ss/4 - 1;
     {rs, ct, ss, -2 p2 (1 - ct), -2 p2 (1 + ct)}], {rs, {5/2, 5, 10}}, {ct, {3/10, 9/10}}], 1];
PaXEvaluate[B0[2, 1, 1]];   (* makes sure Package-X (context X`) is loaded *)
numRulesPXS4$ = {d0[{a_, b_}] :> X`ScalarD0[1., 1., 1., 1., N[a], N[b], 1., 1., 1., 1.],
   c0[x_] :> X`ScalarC0[1., 1., N[x], 1., 1., 1.]};
pxS4$[{rs_, ct_, ss_, tt_, uu_}] := Module[{v},
   v = mMSS4$ /. {s -> ss, t -> tt, u -> uu, m -> 1, mu -> 1, gphi -> 1, lamphi -> 1};
   Chop[N[v /. numRulesPXS4$], 10^-18]];
(* the kinematics are passed as exact rationals: with machine-number prefactors in front of B0,
   LToolsEvaluate wrongly warns that the input contains tensor integrals (::tens) *)
ltS4$[{rs_, ct_, ss_, tt_, uu_}] := Module[{v},
   v = Quiet[LToolsEvaluate[ampS4$ /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1, lamphi -> 1}], LToolsEvaluate::tens];
   Chop[SeriesCoefficient[mBareS4$[v] + (mCTS4$ /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1, lamphi -> 1}), {Epsilon, 0, 0}]]];
rowsS4$ = Join[#, {pxS4$[#], ltS4$[#]}] & /@ pointsS4$;


resultsDirS4$ = FileNameJoin[{srcDirS4$, "results"}];
Quiet[CreateDirectory[resultsDirS4$]];
numStrS4$[x_] := ToString[CForm[N[x]]];
csvLinesS4$ = Prepend[
   StringRiffle[numStrS4$ /@ {#[[1]], #[[2]], #[[3]], #[[4]], #[[5]], Re[#[[6]]], Im[#[[6]]], Re[#[[7]]], Im[#[[7]]]}, ","] & /@ rowsS4$,
   "sqrts,costheta,s,t,u,re_packagex,im_packagex,re_looptools,im_looptools"];
Export[FileNameJoin[{resultsDirS4$, "scat_feyncalc.csv"}], StringRiffle[csvLinesS4$, "\n"] <> "\n", "Text"];
Print["(c) wrote ", Length[rowsS4$], " rows to results/scat_feyncalc.csv"];
Print["(c) M1 (Package-X) = ", rowsS4$[[All, 6]]];
Print["(c) M1 (LoopTools) = ", rowsS4$[[All, 7]]];


(* ::Subsubsection:: *)
(*Inspect: the numbers*)


If[$Notebooks,
  TableForm[{N[#[[1]]], N[#[[2]]], NumberForm[#[[6]], 10], NumberForm[#[[7]], 10], ScientificForm[Abs[#[[6]] - #[[7]]]/Abs[#[[7]]], 2]} & /@ rowsS4$, TableHeadings -> {None, {"sqrt(s)", "cos", "M1 (Package-X)", "M1 (LoopTools)", "rel. diff."}}]
]


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it unloads LoopTools and removes the temporary model copy.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirS4$, DeleteContents -> True];
