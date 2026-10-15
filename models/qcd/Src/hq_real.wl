(* ::Package:: *)

(* ::Title:: *)
(*Step (9): D-dimensional squared real-emission matrix elements, diagram pair by diagram pair (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/qcd, step (9).  "qq": u(p1) ubar(p2) -> t(k1) tbar(k2) g(k3) (5 diagrams), "gg": g(p1) g(p2) -> t tbar g (16), "qg":*)
(*u(p1) g(p2) -> t tbar u(k3) (5).  Sums (not averages) over spins, polarizations and colours in D dimensions, Feynman gauge.  Polarizations:*)
(*-g for the single external gluon of qq and qg (the Ward identity holds when every other coloured particle is a quark); for gg the two*)
(*incoming gluons are summed over their physical polarizations with light-cone tensors -g + (p n + n p)/(p.n) (reference n = the other*)
(*incoming momentum, so p.n = s/2), and then -g suffices for the outgoing gluon.  For each pair (i <= j) of diagrams the polarization tensors*)
(*are contracted inside the Dirac trace before it is evaluated (evaluating the trace with six open indices first was 10-100 times slower and*)
(*the whole squared amplitude at once did not finish), and i != j gives 2 Re.  On the cut (k3 = p1 + p2 - k1 - k2) the result is a rational*)
(*function of x1 = -2 p1.k1, x2 = -2 p2.k1, x3 = -2 p2.k2, x4 = -2 p1.k2, s, D.  At D = 4 it is compared with MadGraph5 (hq_me_mg5.py).*)
(*Writes work/hq/pairs_<chan>/p_i_j.m and work/hq/real_<chan>.m.  Usage: wolframscript -file hq_real.wl chan [from to]  (pair indices*)
(*(i - 1) n + j; run_hq_check.sh splits gg over several processes); with no pair range it also sums the pairs and compares with MadGraph5.*)


(* ::Text:: *)
(*How to run.  Batch: as above (qq, qg: about 1 minute; gg: about 1 hour on 6 cores).  Interactive: ~/hep/bin/wopen hq_real.wl; the notebook runs qq.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirHR$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
argsHR$ = If[$Notebooks, {"qq"}, Rest[$ScriptCommandLine]];
chanHR$ = First[argsHR$];
workHR$ = FileNameJoin[{srcDirHR$, "work", "hq"}];
Quiet[CreateDirectory[FileNameJoin[{workHR$, "pairs_" <> chanHR$}], CreateIntermediateDirectories -> True]];
modelTmpHR$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirHR$, "generated", "QCD_FA"}], FileNameJoin[{modelTmpHR$, "QCD_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpHR$, "QCD_FA"}], Quiet -> True];
modelFileHR$ = FileNameJoin[{modelTmpHR$, "QCD_FA", "QCD_FA"}];
TF = 1/2;


(* ::Section:: *)
(*Diagrams and amplitudes*)


{inHR$, outHR$} = Switch[chanHR$,
   "qq", {{F[2], -F[2]}, {F[7], -F[7], V[2]}},
   "gg", {{V[2], V[2]}, {F[7], -F[7], V[2]}},
   "qg", {{F[2], V[2]}, {F[7], -F[7], F[2]}}];
diagsHR$ = InsertFields[CreateTopologies[0, 2 -> 3], inHR$ -> outHR$, InsertionLevel -> {Particles}, Model -> modelFileHR$,
   GenericModel -> modelFileHR$, ExcludeParticles -> {V[1], F[1]}];


(* ::Subsubsection:: *)
(*Inspect: the diagrams*)


If[$Notebooks, Show[#, ImageSize -> 520] & /@ Render[Paint[diagsHR$, ColumnsXRows -> {5, 1}, Numbering -> Simple, DisplayFunction -> Identity]]]


ampsHR$ = FCFAConvert[CreateFeynAmp[diagsHR$, GaugeRules -> {}] /. M$FACouplings,
    IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {k1, k2, k3}, ChangeDimension -> D, List -> True, SMP -> False,
    UndoChiralSplittings -> True, DropSumOver -> True] /.
   {SMP["g_s"] -> gS, FCGV["GS"] -> gS, FCGV["MT"] -> mt, SMP["m_t"] -> mt, GaugeXi[V[2, ___]] -> 1, GaugeXi[G] -> 1};
Print["(a) ", chanHR$, ": ", Length[ampsHR$], " diagrams (expect 5, 16, 5 for qq, gg, qg)"];
polsHR$ = Switch[chanHR$, "qq", {k3}, "gg", {p1, p2, k3}, "qg", {p2}];
openHR$[x_, idx_] := Fold[ReplaceAll[#1, {Momentum[Polarization[#2[[1]], _], dim___] :> LorentzIndex[#2[[2]], dim]}] &, x, Transpose[{polsHR$, idx}]];
muHR$ = Table[Symbol["mu" <> ToString[i]], {i, Length[polsHR$]}]; nuHR$ = Table[Symbol["nu" <> ToString[i]], {i, Length[polsHR$]}];
dAxHR$[a_, b_, k_, n_] := -MTD[a, b] + (FVD[k, a] FVD[n, b] + FVD[n, a] FVD[k, b])/SPD[k, n];
polTHR$ = Switch[chanHR$, "qq", -MTD[mu1, nu1], "gg", dAxHR$[mu1, nu1, p1, p2] dAxHR$[mu2, nu2, p2, p1] (-MTD[mu3, nu3]), "qg", -MTD[mu1, nu1]];
FCClearScalarProducts[];
SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[k1, k1] = mt^2; SPD[k2, k2] = mt^2; SPD[k3, k3] = 0; SPD[p1, p2] = s/2;
cutRulesHR$ = {SPD[p1, k1] -> -x1/2, SPD[p2, k1] -> -x2/2, SPD[p2, k2] -> -x3/2, SPD[p1, k2] -> -x4/2,
   SPD[k1, k2] -> -(s + 2 mt^2 + x1 + x2 + x3 + x4)/2};


(* ::Section:: *)
(*(b) pairs of diagrams*)


ndHR$ = Length[ampsHR$];
pairsHR$ = Flatten[Table[{i, j}, {i, ndHR$}, {j, i, ndHR$}], 1];
If[Length[argsHR$] >= 3, With[{a = ToExpression[argsHR$[[2]]], b = ToExpression[argsHR$[[3]]]},
   pairsHR$ = Select[pairsHR$, a <= (#[[1]] - 1) ndHR$ + #[[2]] <= b &]]];
If[Length[argsHR$] >= 4 && argsHR$[[4]] === "rev", pairsHR$ = Reverse[pairsHR$]];
pairHR$[pr_] := Module[{a = openHR$[FCI[ampsHR$[[pr[[1]]]]], muHR$], b = openHR$[ComplexConjugate[FCI[ampsHR$[[pr[[2]]]]]], nuHR$], sq},
   sq = FermionSpinSum[Contract[a b polTHR$], ExtraFactor -> 1];
   sq = DiracSimplify[sq /. DiracTrace[y_] :> DiracTrace[DiracSimplify[y], DiracTraceEvaluate -> True]];
   sq = SUNSimplify[Contract[sq], SUNNToCACF -> True] /. SUNN -> CA;
   sq = FeynAmpDenominatorExplicit[sq] /. Momentum[k3, dim___] :> Momentum[p1, dim] + Momentum[p2, dim] - Momentum[k1, dim] - Momentum[k2, dim];
   sq = Together[FCE[ExpandScalarProduct[sq]] /. cutRulesHR$];
   If[!FreeQ[sq, SPD | Pair], Print["   scalar products left in pair ", pr]];
   If[pr[[1]] != pr[[2]], sq + (sq /. Complex[re_, im_] :> Complex[re, -im]), sq]];
Do[Module[{f = FileNameJoin[{workHR$, "pairs_" <> chanHR$, "p_" <> ToString[pr[[1]]] <> "_" <> ToString[pr[[2]]] <> ".m"}], t0 = AbsoluteTime[]},
   If[!FileExistsQ[f], Put[pairHR$[pr], f]; Print["(b) pair ", pr, ": ", Round[AbsoluteTime[] - t0], " s"]]], {pr, pairsHR$}];


(* ::Section:: *)
(*(c) the sum and the check against MadGraph5 at D = 4*)


If[Length[argsHR$] < 3,
  Module[{fs = FileNames["p_*.m", FileNameJoin[{workHR$, "pairs_" <> chanHR$}]], tot, rows, avg, dev},
   tot = Together[Total[Get /@ fs]];
   Print["(c) ", chanHR$, ": ", Length[fs], " pairs (expect ", ndHR$ (ndHR$ + 1)/2, "); explicit I left: ", !FreeQ[tot, Complex]];
   Put[tot, FileNameJoin[{workHR$, "real_" <> chanHR$ <> ".m"}]];
   rows = Select[Import[FileNameJoin[{srcDirHR$, "results", "hq_me_mg5.csv"}], "CSV"], #[[1]] == chanHR$ &];
   avg = <|"qq" -> 36, "gg" -> 256, "qg" -> 96|>[chanHR$];
   (* evaluated with 40 digits: in machine precision the rational function of gg loses up to 4 digits *)
   dev = Table[Abs[(tot /. {D -> 4, gS -> 1, mt -> 1, CA -> 3, CF -> 4/3} /. SetPrecision[{s -> rw[[2]], x1 -> rw[[3]], x2 -> rw[[4]], x3 -> rw[[5]], x4 -> rw[[6]]}, 40])/avg/rw[[7]] - 1],
     {rw, rows}];
   Print["(c) ", chanHR$, ": D = 4 against MadGraph5 at ", Length[dev], " points, max |ratio - 1| = ", N[Max[dev], 3], "  (expect ~1e-14)"]]];
Quiet[DeleteDirectory[modelTmpHR$, DeleteContents -> True]];
