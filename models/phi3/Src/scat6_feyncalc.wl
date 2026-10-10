(* ::Package:: *)

(* ::Title:: *)
(*Step (8): one-loop phi phi -> phi phi in d = 6 (dimension shift, Package-X and LoopTools)*)


(* ::Text:: *)
(*(a) The FeynArts amplitude is the same as in d = 4 (12 diagrams, scat4_feyncalc.wl):*)
(*      A = I Pi^2 g^4 [ D0(s,t) + D0(s,u) + D0(t,u) + sum_x ( 2 C0(x)/(x - m^2) + B0(x)/(2 (x - m^2)^2) ) ],*)
(*    with the PaVe functions now read in D = 6 - 2 Epsilon; M = -I A/(2 Pi)^D.*)
(*(b) Through the dimension shift PaVe^(D+2) = -2 Pi PaVe_00^(D) (note, App. H), Package-X evaluates the*)
(*    D = 6 - 2 Epsilon functions as -2 Pi times D00, C00, B00 in D = 4 - 2 Epsilon.  The MS-bar*)
(*    counterterms of Eq. (8) enter the tree-like diagrams: on each internal line g^2 (deltaZ x - deltam)/(x - m^2)^2*)
(*    and at each of the two vertices -g deltag/(x - m^2).  The poles cancel, and the MS-bar amplitude equals*)
(*      M1 = g^4/(4 Pi)^3 [ sum D0^(6) + sum_x ( 2 C0^(6)(x)/(x - m^2) + B0^(6)(x)/(2 (x - m^2)^2) ) ]   (Eq. (22) (eq:M6))*)
(*    with the d = 6 MS-bar finite parts X_N of Eq. (12) (D0^(6) = int dF/Delta for the finite box).*)
(*(c) M1 at the six points of step (5) for mu = 1, 1/2, 2 (m = g = 1) with Package-X (D0, C0 from its*)
(*    numerical functions) and LoopTools -> Src/results/scat6_feyncalc.csv.*)
(**)
(*Usage:  wolframscript -file scat6_feyncalc.wl      (run generate_Phi3.wl first)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file scat6_feyncalc.wl.  Interactive:  ~/hep/bin/wopen scat6_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];

srcDirS6$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Section:: *)
(*patched copy of the FeynRules-generated FeynArts model*)


modelTmpDirS6$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirS6$, "generated", "Phi3_FA"}], FileNameJoin[{modelTmpDirS6$, "Phi3_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirS6$, "Phi3_FA"}], Quiet -> True];
modelS6$ = FileNameJoin[{modelTmpDirS6$, "Phi3_FA", "Phi3_FA"}];


(* ::Section:: *)
(*(a) diagrams and amplitude*)


diagsS6$ = InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}],
   {S[1], S[1]} -> {S[1], S[1]}, InsertionLevel -> {Particles}, Model -> modelS6$, GenericModel -> modelS6$];
Print["(a) number of diagrams (expect 12): ", Length[CreateFeynAmp[diagsS6$]]];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, m, m, m, m];
ampS6$ = FCE[FeynAmpDenominatorExplicit[TID[FCFAConvert[CreateFeynAmp[diagsS6$, Truncated -> True, PreFactor -> 1],
      IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {k1, k2}, LoopMomenta -> {q}, ChangeDimension -> D,
      List -> False, SMP -> False, DropSumOver -> True], q, ToPaVe -> True]]] /. (-3 m^2 + s + t + u) -> m^2;
canonS6$ = {D0[m^2, m^2, m^2, m^2, a_, b_, m^2, m^2, m^2, m^2] :> d0[Sort[{a, b}]],
   C0[m^2, m^2, x_, m^2, m^2, m^2] :> c0[x], C0[m^2, x_, m^2, m^2, m^2, m^2] :> c0[x],
   C0[x_, m^2, m^2, m^2, m^2, m^2] :> c0[x], B0[x_, m^2, m^2] :> b0[x]};
handS6$ = I Pi^2 gphi^4 (d0[Sort[{s, t}]] + d0[Sort[{s, u}]] + d0[Sort[{t, u}]] +
    Sum[2 c0[x]/(x - m^2) + b0[x]/(2 (x - m^2)^2), {x, {s, t, u}}]);
Print["(a) A - I Pi^2 g^4 [same form as Eq. (17)] = ", Simplify[(ampS6$ /. canonS6$) - handS6$], "  (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: the 12 diagrams (the same as in d = 4)*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diagsS6$, ColumnsXRows -> {4, 3}, Numbering -> Simple, DisplayFunction -> Identity]]
]


(* ::Subsubsection:: *)
(*Inspect: the amplitude collected by integral (PaVe functions read in D = 6 - 2 Epsilon)*)


If[$Notebooks,
  Collect[ampS6$ /. canonS6$, {_d0, _c0, _b0}, Simplify] // TraditionalForm
]


(* ::Section:: *)
(*(b) dimension shift, poles, MS-bar counterterms*)


k6S6$ = (4 Pi)^3;
dUVS6$ = 1/Epsilon - EulerGamma + Log[4 Pi];
shiftS6$ = {d0[{a_, b_}] :> -2 Pi PaVe[0, 0, {m^2, m^2, m^2, m^2, a, b}, {m^2, m^2, m^2, m^2}],
   c0[x_] :> -2 Pi PaVe[0, 0, {m^2, m^2, x}, {m^2, m^2, m^2}], b0[x_] :> -2 Pi PaVe[0, 0, {x}, {m^2, m^2}]};
(* M = -I A/(2 Pi)^D, D = 6 - 2 Epsilon *)
mBareS6$[ampValue_] := (2 Pi)^(2 Epsilon) (-I) ampValue/(2 Pi)^6;
(* Eq. (8): deltaZ = -g^2 DeltaUV/(12 K), deltam = -g^2 m^2 DeltaUV/(2 K), deltag = -g^3 DeltaUV/(2 K) *)
{dZS6$, dmS6$, dgS6$} = {-gphi^2/(12 k6S6$), -gphi^2 m^2/(2 k6S6$), -gphi^3/(2 k6S6$)} dUVS6$;
mCTS6$ = Sum[gphi^2 (dZS6$ x - dmS6$)/(x - m^2)^2 - 2 gphi dgS6$/(x - m^2), {x, {s, t, u}}];
paxS6$ = PaXEvaluate[(ampS6$ /. canonS6$) /. shiftS6$];
serS6$ = Series[mBareS6$[paxS6$] + mCTS6$, {Epsilon, 0, 0}];
Print["(b) 1/eps coefficient of M (bare) = ", InputForm[Simplify[SeriesCoefficient[Series[mBareS6$[paxS6$], {Epsilon, 0, 0}], -1]]]];
Print["(b) 1/eps coefficient of M + M_CT = ", Simplify[SeriesCoefficient[serS6$, -1]], "  (expect 0)"];
mMSS6$ = SeriesCoefficient[serS6$, 0] /. ScaleMu -> mu;
(* X_N of a D = 6 - 2 Epsilon PaVe function: mu^(2 Epsilon) I_N = I/K [c DeltaUV + X], I_N = I Pi^2 PaVe/(2 Pi)^D *)
xNS6$[pave_] := Module[{v = Series[(2 Pi)^(2 Epsilon) I Pi^2 (-2 Pi) PaXEvaluate[pave]/(2 Pi)^6, {Epsilon, 0, 0}]},
   (SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma))/(I/k6S6$) /. ScaleMu -> mu];
formulaS6$ = gphi^4/k6S6$ (Sum[xNS6$[PaVe[0, 0, {m^2, m^2, m^2, m^2, Sequence @@ pr}, {m^2, m^2, m^2, m^2}]],
      {pr, {{s, t}, {s, u}, {t, u}}}] +
    Sum[2 xNS6$[PaVe[0, 0, {m^2, m^2, x}, {m^2, m^2, m^2}]]/(x - m^2) + xNS6$[PaVe[0, 0, {x}, {m^2, m^2}]]/(2 (x - m^2)^2),
     {x, {s, t, u}}]);
logRulesS6$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
Print["(b) MS-bar M - Eq. (22) (eq:M6) with the X_N of Eq. (12) = ", Simplify[(mMSS6$ - formulaS6$) /. logRulesS6$], "  (expect 0)"];
(* the tadpole-free check of the B0^(6) closed form of Eq. (13) is in oneloop6_feyncalc.wl *)


(* ::Subsubsection:: *)
(*Inspect: the counterterms of Eq. (8) and their insertion into the tree diagrams*)


If[$Notebooks,
  TableForm[{{"deltaZ", TraditionalForm[dZS6$]}, {"deltam", TraditionalForm[dmS6$]}, {"deltag", TraditionalForm[dgS6$]}, {"M_CT", TraditionalForm[mCTS6$]}}]
]


(* ::Subsubsection:: *)
(*Inspect: Eq. (22) written with the X_N of Eq. (12)*)


If[$Notebooks,
  formulaS6$ // Short[#, 6] &
]


(* ::Section:: *)
(*(c) numerical values*)


pointsS6$ = Flatten[Table[Module[{ss = rs^2, p2}, p2 = ss/4 - 1;
     {rs, ct, ss, -2 p2 (1 - ct), -2 p2 (1 + ct)}], {rs, {5/2, 5, 10}}, {ct, {3/10, 9/10}}], 1];
musS6$ = {1, 1/2, 2};
PaXEvaluate[B0[2, 1, 1]];   (* makes sure Package-X (context X`) is loaded *)
numRulesS6$ = {D0[a_, b_, c_, d_, e_, f_, ms__] :> X`ScalarD0[N[a], N[b], N[c], N[d], N[e], N[f], 1., 1., 1., 1.],
   C0[a_, b_, c_, ms__] :> X`ScalarC0[N[a], N[b], N[c], 1., 1., 1.]};
pxS6$[{rs_, ct_, ss_, tt_, uu_}, muv_] := Chop[N[(mMSS6$ /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1, mu -> muv})
      /. logRulesS6$ /. numRulesS6$], 10^-18];
(* LoopTools: the same MS-bar procedure on LToolsEvaluate's output; LToolsSetMudim is mu^2 *)
ltS6$[{rs_, ct_, ss_, tt_, uu_}, muv_] := Module[{a, v},
   a = ((ampS6$ /. canonS6$) /. shiftS6$) /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1};
   v = LToolsEvaluate[a, LToolsSetMudim -> muv^2];
   Chop[SeriesCoefficient[mBareS6$[v] + (mCTS6$ /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1}), {Epsilon, 0, 0}]
     /. {Log[4 Pi] -> 2 Log[2] + Log[Pi]}]];
(* a check of the mu convention: B00 at mu^2 = 4 minus mu^2 = 1 is -(m^2 - p^2/6)/2 Log[4]... from LoopTools *)
Print["(c) LoopTools B00(p^2 = 2): mudim 4 minus mudim 1 = ",
  Chop[N[LToolsEvaluate[PaVe[0, 0, {2}, {1, 1}], LToolsSetMudim -> 4] - LToolsEvaluate[PaVe[0, 0, {2}, {1, 1}], LToolsSetMudim -> 1]]],
  "  expect (6 m^2 - p^2)/12 Log[4] = ", N[(6 - 2)/12 Log[4]]];
rowsS6$ = Flatten[Table[Join[pt, {muv, pxS6$[pt, muv], ltS6$[pt, muv]}], {muv, musS6$}, {pt, pointsS6$}], 1];

resultsDirS6$ = FileNameJoin[{srcDirS6$, "results"}];
Quiet[CreateDirectory[resultsDirS6$]];
numStrS6$[x_] := ToString[CForm[N[x]]];
csvLinesS6$ = Prepend[
   StringRiffle[numStrS6$ /@ {#[[1]], #[[2]], #[[6]], #[[3]], #[[4]], #[[5]], Re[#[[7]]], Im[#[[7]]], Re[#[[8]]], Im[#[[8]]]}, ","] & /@ rowsS6$,
   "sqrts,costheta,mu,s,t,u,re_packagex,im_packagex,re_looptools,im_looptools"];
Export[FileNameJoin[{resultsDirS6$, "scat6_feyncalc.csv"}], StringRiffle[csvLinesS6$, "\n"] <> "\n", "Text"];
Print["(c) wrote ", Length[rowsS6$], " rows to results/scat6_feyncalc.csv"];
Print["(c) M1 at mu = 1 (Package-X) = ", Select[rowsS6$, #[[6]] == 1 &][[All, 7]]];
Print["(c) M1 at mu = 1 (LoopTools) = ", Select[rowsS6$, #[[6]] == 1 &][[All, 8]]];


(* ::Subsubsection:: *)
(*Inspect: the values at the six points for mu = 1, 1/2, 2*)


If[$Notebooks,
  TableForm[{N[#[[1]]], N[#[[2]]], N[#[[6]]], NumberForm[#[[7]], 10], NumberForm[#[[8]], 10]} & /@ rowsS6$, TableHeadings -> {None, {"sqrt(s)", "cos", "mu", "M1 (Package-X)", "M1 (LoopTools)"}}]
]


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirS6$, DeleteContents -> True];
