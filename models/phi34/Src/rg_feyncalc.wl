(* ::Package:: *)

(* ::Title:: *)
(*Step (7): the MS-bar amplitude of phi^3 + phi^4 at several mu, for the renormalization group*)


(* ::Text:: *)
(*Research note models/phi34, step (7).  The amplitude is built as in scat_feyncalc.wl (42 diagrams, MS-bar counterterms*)
(*deltam, deltag, deltalambda of Eq. (5) on the tree diagrams).  (a) diagrams and pole cancellation.  (b) the explicit*)
(*mu-dependence of the MS-bar M1 at fixed m, g, lambda (App. J):*)
(*    mu dM1/dmu = [g^4 A + 6 g^2 lambda B + g^2 lambda m^2 A + 3 lambda^2]/(4 Pi)^2,*)
(*    A = sum_x 1/(x - m^2)^2,  B = sum_x 1/(x - m^2).*)
(*(c) M1 with Package-X (C0, D0 from its numerical functions) and LoopTools at the six points of step (4) for*)
(*mu = 1, 1/2, 2 (m = g = lambda = 1) -> Src/results/rg_feyncalc.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file rg_feyncalc.wl  (run run_model_check.sh first); only the lines starting with (a), (b), (c) are printed.  Interactive:  ~/hep/bin/wopen rg_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];

srcDirRG$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

modelTmpDirRG$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirRG$, "generated", "Phi34_FA"}], FileNameJoin[{modelTmpDirRG$, "Phi34_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirRG$, "Phi34_FA"}], Quiet -> True];
modelRG$ = FileNameJoin[{modelTmpDirRG$, "Phi34_FA", "Phi34_FA"}];


(* ::Section:: *)
(*(a) diagrams, amplitude and the MS-bar counterterms*)


diagsRG$ = InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}],
   {S[1], S[1]} -> {S[1], S[1]}, InsertionLevel -> {Particles}, Model -> modelRG$, GenericModel -> modelRG$];


(* ::Subsubsection:: *)
(*Inspect: the 42 diagrams*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diagsRG$, ColumnsXRows -> {6, 7}, Numbering -> Simple, DisplayFunction -> Identity]]
]


FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, m, m, m, m];
ampRG$ = FCE[FeynAmpDenominatorExplicit[TID[FCFAConvert[CreateFeynAmp[diagsRG$, Truncated -> True, PreFactor -> 1],
      IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {k1, k2}, LoopMomenta -> {q}, ChangeDimension -> D,
      List -> False, SMP -> False, DropSumOver -> True], q, ToPaVe -> True]]] /. (-3 m^2 + s + t + u) -> m^2;
Print["(a) number of diagrams (expect 42): ", Length[CreateFeynAmp[diagsRG$]]];


(* M = -I A/(2 Pi)^D (D = 4 - 2 Epsilon) plus the MS-bar counterterms of Eq. (5) on the tree diagrams *)
canonRG$ = {D0[m^2, m^2, m^2, m^2, a_, b_, m^2, m^2, m^2, m^2] :> d0[Sort[{a, b}]],
   C0[m^2, m^2, x_, m^2, m^2, m^2] :> c0[x], C0[m^2, x_, m^2, m^2, m^2, m^2] :> c0[x],
   C0[x_, m^2, m^2, m^2, m^2, m^2] :> c0[x]};
mBareRG$[ampValue_] := (2 Pi)^(2 Epsilon) (-I) ampValue/(2 Pi)^4;
dUVRG$ = 1/Epsilon - EulerGamma + Log[4 Pi];
ctRG$ = {(gphi^2 + lamphi m^2)/(2 (4 Pi)^2), 3 gphi lamphi/(2 (4 Pi)^2), 3 lamphi^2/(2 (4 Pi)^2)} dUVRG$;
mCTRG$ = -Sum[gphi^2 ctRG$[[1]]/(x - m^2)^2 + 2 gphi ctRG$[[2]]/(x - m^2), {x, {s, t, u}}] - ctRG$[[3]];
paxRG$ = PaXEvaluate[ampRG$ /. canonRG$ /. {d0[{a_, b_}] :> D0[m^2, m^2, m^2, m^2, a, b, m^2, m^2, m^2, m^2],
       c0[x_] :> C0[m^2, m^2, x, m^2, m^2, m^2]}, PaXC0Expand -> False, PaXD0Expand -> False];
serRG$ = Series[mBareRG$[paxRG$] + mCTRG$, {Epsilon, 0, 0}];
Print["(a) 1/eps coefficient of M + M_CT = ", Simplify[SeriesCoefficient[serRG$, -1]], "  (expect 0)"];
mMSRG$ = SeriesCoefficient[serRG$, 0] /. ScaleMu -> mu;


(* ::Section:: *)
(*(b) the explicit mu-dependence of the MS-bar M1*)


(* C0 and D0 are mu-independent; mu enters through the MS-bar A0 and B0 only *)
aSumRG$ = Sum[1/(x - m^2)^2, {x, {s, t, u}}];
bSumRG$ = Sum[1/(x - m^2), {x, {s, t, u}}];
slopeRG$ = (gphi^4 aSumRG$ + 6 gphi^2 lamphi bSumRG$ + gphi^2 lamphi m^2 aSumRG$ + 3 lamphi^2)/(4 Pi)^2;
Print["(b) mu dM1/dmu - [g^4 A + 6 g^2 lambda B + g^2 lambda m^2 A + 3 lambda^2]/(4 Pi)^2 = ",
  Simplify[mu D[mMSRG$, mu] - slopeRG$], "  (expect 0)"];


(* ::Subsubsection:: *)
(*Inspect: mu dM1/dmu as computed*)


If[$Notebooks,
  Collect[Simplify[mu D[mMSRG$, mu]], {gphi, lamphi}, Simplify] // TraditionalForm
]


(* ::Section:: *)
(*(c) values at mu = 1, 1/2, 2 with Package-X and LoopTools*)


pointsRG$ = Flatten[Table[Module[{ss = rs^2, p2}, p2 = ss/4 - 1;
     {rs, ct, ss, -2 p2 (1 - ct), -2 p2 (1 + ct)}], {rs, {5/2, 5, 10}}, {ct, {3/10, 9/10}}], 1];
PaXEvaluate[B0[2, 1, 1]];
numRulesRG$ = {D0[a_, b_, c_, d_, e_, f_, ms__] :> X`ScalarD0[N[a], N[b], N[c], N[d], N[e], N[f], 1., 1., 1., 1.],
   C0[a_, b_, c_, ms__] :> X`ScalarC0[N[a], N[b], N[c], 1., 1., 1.]};
logRulesRG$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
pxRG$[{rs_, ct_, ss_, tt_, uu_}, muv_] := Chop[N[(mMSRG$ /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1, lamphi -> 1,
         mu -> muv}) /. logRulesRG$ /. numRulesRG$], 10^-18];
(* exact rational kinematics: with machine numbers LToolsEvaluate wrongly warns about tensor integrals (::tens) *)
ltRG$[{rs_, ct_, ss_, tt_, uu_}, muv_] := Module[{v},
   v = Quiet[LToolsEvaluate[ampRG$ /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1, lamphi -> 1}, LToolsSetMudim -> muv^2],
     LToolsEvaluate::tens];
   Chop[SeriesCoefficient[mBareRG$[v] + (mCTRG$ /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1, lamphi -> 1}),
       {Epsilon, 0, 0}] /. logRulesRG$]];
rowsRG$ = Flatten[Table[Join[pt, {muv, pxRG$[pt, muv], ltRG$[pt, muv]}], {muv, {1, 1/2, 2}}, {pt, pointsRG$}], 1];


(* ::Subsubsection:: *)
(*Inspect: the values at the six points for mu = 1, 1/2, 2*)


If[$Notebooks,
  TableForm[{N[#[[1]]], N[#[[2]]], N[#[[6]]], NumberForm[#[[7]], 10], NumberForm[#[[8]], 10]} & /@ rowsRG$, TableHeadings -> {None, {"sqrt(s)", "cos", "mu", "M1 (Package-X)", "M1 (LoopTools)"}}]
]


numStrRG$[x_] := ToString[CForm[N[x]]];
csvRG$ = Prepend[
   StringRiffle[numStrRG$ /@ {#[[1]], #[[2]], #[[6]], #[[3]], #[[4]], #[[5]], Re[#[[7]]], Im[#[[7]]], Re[#[[8]]], Im[#[[8]]]}, ","] & /@ rowsRG$,
   "sqrts,costheta,mu,s,t,u,re_packagex,im_packagex,re_looptools,im_looptools"];
Quiet[CreateDirectory[FileNameJoin[{srcDirRG$, "results"}]]];
Export[FileNameJoin[{srcDirRG$, "results", "rg_feyncalc.csv"}], StringRiffle[csvRG$, "\n"] <> "\n", "Text"];
Print["(c) wrote ", Length[rowsRG$], " rows to results/rg_feyncalc.csv"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirRG$, DeleteContents -> True];
