(* ::Package:: *)

(* rg4_feyncalc.wl -- MS-bar one-loop phi phi -> phi phi in d = 4 at several mu, for the
   renormalization-group check (research note, step (9)).  The amplitude is built as in
   scat4_feyncalc.wl (12 diagrams, MS-bar mass counterterm on the internal lines) and evaluated with
   Package-X (D0, C0 from its numerical functions) and LoopTools at the six points of step (5) for
   mu = 1, 1/2, 2 (m = g = 1) -> Src/results/rg4_feyncalc.csv.

   Usage:  wolframscript -file rg4_feyncalc.wl      (run generate_Phi3.wl first) *)

$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];

srcDirR4$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

modelTmpDirR4$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirR4$, "generated", "Phi3_FA"}], FileNameJoin[{modelTmpDirR4$, "Phi3_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirR4$, "Phi3_FA"}], Quiet -> True];
modelR4$ = FileNameJoin[{modelTmpDirR4$, "Phi3_FA", "Phi3_FA"}];

diagsR4$ = InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}],
   {S[1], S[1]} -> {S[1], S[1]}, InsertionLevel -> {Particles}, Model -> modelR4$, GenericModel -> modelR4$];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, m, m, m, m];
ampR4$ = FCE[FeynAmpDenominatorExplicit[TID[FCFAConvert[CreateFeynAmp[diagsR4$, Truncated -> True, PreFactor -> 1],
      IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {k1, k2}, LoopMomenta -> {q}, ChangeDimension -> D,
      List -> False, SMP -> False, DropSumOver -> True], q, ToPaVe -> True]]] /. (-3 m^2 + s + t + u) -> m^2;
Print["(a) number of diagrams (expect 12): ", Length[CreateFeynAmp[diagsR4$]]];

canonR4$ = {D0[m^2, m^2, m^2, m^2, a_, b_, m^2, m^2, m^2, m^2] :> d0[Sort[{a, b}]],
   C0[m^2, m^2, x_, m^2, m^2, m^2] :> c0[x], C0[m^2, x_, m^2, m^2, m^2, m^2] :> c0[x],
   C0[x_, m^2, m^2, m^2, m^2, m^2] :> c0[x]};
(* M = -I A/(2 Pi)^D (D = 4 - 2 Epsilon) plus the MS-bar mass counterterm on the internal lines *)
mBareR4$[ampValue_] := (2 Pi)^(2 Epsilon) (-I) ampValue/(2 Pi)^4;
mCTR4$ = -gphi^2 (gphi^2 (1/Epsilon - EulerGamma + Log[4 Pi])/(2 (4 Pi)^2)) Sum[1/(x - m^2)^2, {x, {s, t, u}}];
paxR4$ = PaXEvaluate[ampR4$ /. canonR4$ /. {d0[{a_, b_}] :> D0[m^2, m^2, m^2, m^2, a, b, m^2, m^2, m^2, m^2],
       c0[x_] :> C0[m^2, m^2, x, m^2, m^2, m^2]}, PaXC0Expand -> False, PaXD0Expand -> False];
serR4$ = Series[mBareR4$[paxR4$] + mCTR4$, {Epsilon, 0, 0}];
Print["(a) 1/eps coefficient of M + M_CT = ", Simplify[SeriesCoefficient[serR4$, -1]], "  (expect 0)"];
mMSR4$ = SeriesCoefficient[serR4$, 0] /. ScaleMu -> mu;

pointsR4$ = Flatten[Table[Module[{ss = rs^2, p2}, p2 = ss/4 - 1;
     {rs, ct, ss, -2 p2 (1 - ct), -2 p2 (1 + ct)}], {rs, {5/2, 5, 10}}, {ct, {3/10, 9/10}}], 1];
PaXEvaluate[B0[2, 1, 1]];
numRulesR4$ = {D0[a_, b_, c_, d_, e_, f_, ms__] :> X`ScalarD0[N[a], N[b], N[c], N[d], N[e], N[f], 1., 1., 1., 1.],
   C0[a_, b_, c_, ms__] :> X`ScalarC0[N[a], N[b], N[c], 1., 1., 1.]};
logRulesR4$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
pxR4$[{rs_, ct_, ss_, tt_, uu_}, muv_] := Chop[N[(mMSR4$ /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1, mu -> muv})
      /. logRulesR4$ /. numRulesR4$], 10^-18];
ltR4$[{rs_, ct_, ss_, tt_, uu_}, muv_] := Module[{v},
   v = LToolsEvaluate[ampR4$ /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1}, LToolsSetMudim -> muv^2];
   Chop[SeriesCoefficient[mBareR4$[v] + (mCTR4$ /. {s -> ss, t -> tt, u -> uu, m -> 1, gphi -> 1}), {Epsilon, 0, 0}]
     /. logRulesR4$]];
rowsR4$ = Flatten[Table[Join[pt, {muv, pxR4$[pt, muv], ltR4$[pt, muv]}], {muv, {1, 1/2, 2}}, {pt, pointsR4$}], 1];

numStrR4$[x_] := ToString[CForm[N[x]]];
csvR4$ = Prepend[
   StringRiffle[numStrR4$ /@ {#[[1]], #[[2]], #[[6]], #[[3]], #[[4]], #[[5]], Re[#[[7]]], Im[#[[7]]], Re[#[[8]]], Im[#[[8]]]}, ","] & /@ rowsR4$,
   "sqrts,costheta,mu,s,t,u,re_packagex,im_packagex,re_looptools,im_looptools"];
Quiet[CreateDirectory[FileNameJoin[{srcDirR4$, "results"}]]];
Export[FileNameJoin[{srcDirR4$, "results", "rg4_feyncalc.csv"}], StringRiffle[csvR4$, "\n"] <> "\n", "Text"];
Print["(b) wrote ", Length[rowsR4$], " rows to results/rg4_feyncalc.csv"];

LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirR4$, DeleteContents -> True];
