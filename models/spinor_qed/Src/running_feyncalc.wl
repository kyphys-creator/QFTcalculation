(* ::Package:: *)

(* ::Title:: *)
(*Step (9): the subtracted vacuum polarization for the running coupling (FeynArts + FeynCalc, Package-X, LoopTools)*)


(* ::Text:: *)
(*Research note models/spinor_qed, step (9), Eqs. (eq:disp), (eq:aeff), App. run.  The photon two-point function of one flavour*)
(*from FeynArts (as in oneloop_feyncalc.wl), K Pi^R/e^2 in MS-bar.  At mu = m the subtraction constant Pi^R(0) =*)
(*-(4/3) B0(0; m, m) e^2/K vanishes, so K Pi^R/e^2 = K Pibar/e^2.*)
(*(a) Package-X, symbolic mass: the expansion for small q^2, K Pibar/e^2 = -(4/15) q^2/m^2 - (1/35) q^4/m^4 + ..., and for large*)
(*    -q^2 = Q^2, K Pibar/e^2 = (4/3)[ln(Q^2/m^2) - 5/3 + 6 m^2/Q^2] + O(m^4/Q^4 ln): the constant -5/3 is what maps the*)
(*    on-shell charge at Q onto the MS-bar charge at e^(-5/6) Q.*)
(*(b) K Pibar/e^2 (complex, +i0 above threshold) at the q^2 values of work/running_q2.txt (m = 1) from Package-X (exact rational q^2,*)
(*    30 digits) and LoopTools (rational input) -> results/running_feyncalc.csv.  running_numeric.py compares them with the*)
(*    dispersion relation and uses their imaginary parts as the spectral function of the Uehling potential.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file running_feyncalc.wl  (after running_numeric.py --nodes; run_running_check.sh does both).  Interactive:  ~/hep/bin/wopen running_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirRU$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirRU$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirRU$, "generated", "SpinorQED_FA"}], FileNameJoin[{modelTmpDirRU$, "SpinorQED_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirRU$, "SpinorQED_FA"}], Quiet -> True];
modelRU$ = FileNameJoin[{modelTmpDirRU$, "SpinorQED_FA", "SpinorQED_FA"}];
KK = (4 Pi)^2;


(* ::Section:: *)
(*(a) The photon two-point function and its expansions*)


diagPiRU$ = InsertFields[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {V[1]} -> {V[1]},
   InsertionLevel -> {Particles}, Model -> modelRU$, GenericModel -> modelRU$];


(* ::Subsubsection:: *)
(*Inspect: the electron and muon loops*)


If[$Notebooks, Show[#, ImageSize -> 360] & /@ Render[Paint[diagPiRU$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]]]


FCClearScalarProducts[];
ScalarProduct[q, q] = qq;
ampPiRU$ = FCE[DiracSimplify[FeynAmpDenominatorExplicit[TID[DiracSimplify[FCFAConvert[
        CreateFeynAmp[diagPiRU$, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
        IncomingMomenta -> {q}, OutgoingMomenta -> {q}, LoopMomenta -> {l}, LorentzIndexNames -> {mu, nu}, ChangeDimension -> D,
        List -> False, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI // ReplaceAll[#, FCGV["EL"] -> EL] &],
      l, ToPaVe -> True]]]];
FCClearScalarProducts[];
(* K Pi_f/e^2 of the electron loop with mass Me (the muon loop removed) *)
bPiRU$ = Coefficient[Expand[ampPiRU$/(I Pi^2)] /. MTD[mu, nu] -> gmn, gmn]/qq /. MMU -> 0 /. {A0[0] -> 0, B0[x_, 0, 0] -> 0} /. EL -> 1;
msbarRU$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   {SeriesCoefficient[v, -1], SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)}];
logRulesRU$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
PaXEvaluate[B0[2, 1, 1]];   (* loads Package-X *)
(* the finite part for spacelike q^2 with mu = m: K Pibar/e^2 *)
pxPibarRU$ = Simplify[msbarRU$[I Pi^2 Quiet[PaXEvaluate[bPiRU$ /. D -> 4 - 2 Epsilon], PaXEvaluate::tens] KK/I][[2]] /. ScaleMu -> Me /. logRulesRU$,
   {qq < 0, Me > 0}];
Print["(a) Package-X K Pibar/e^2 (q^2 < 0, mu = m): ", InputForm[pxPibarRU$]];
Print["(a) at q^2 -> 0 (expect 0, the subtraction): ", Limit[pxPibarRU$, qq -> 0, Direction -> "FromBelow"]];
smallRU$ = Normal[Series[pxPibarRU$, {qq, 0, 2}]];
Print["(a) small q^2: ", InputForm[Expand[smallRU$]], ";  minus (-(4/15) q^2/m^2 - (1/35) q^4/m^4) = ",
  Simplify[smallRU$ - (-4/15 qq/Me^2 - 1/35 qq^2/Me^4)]];
largeRU$ = Normal[Series[pxPibarRU$ /. qq -> -QQ, {QQ, Infinity, 1}]];
Print["(a) large Q^2 = -q^2: ", InputForm[Simplify[largeRU$, {QQ > 0, Me > 0}]], ";  minus (4/3)[ln(Q^2/m^2) - 5/3 + 6 m^2/Q^2] = ",
  Simplify[largeRU$ - 4/3 (Log[QQ/Me^2] - 5/3 + 6 Me^2/QQ), {QQ > 0, Me > 0}]];


(* ::Section:: *)
(*(b) Values at the points and spectral nodes (m = mu = 1)*)


nodesRU$ = ToExpression[StringReplace[#, {"e" -> "*^"}]] & /@ StringSplit[ReadString[FileNameJoin[{srcDirRU$, "work", "running_q2.txt"}]]];
xRU$ = bPiRU$ /. Me -> 1;
pxValRU$[t_] := N[msbarRU$[I Pi^2 Quiet[PaXEvaluate[xRU$ /. qq -> t /. D -> 4 - 2 Epsilon], PaXEvaluate::tens] KK/I][[2]] /. ScaleMu -> 1 /. logRulesRU$, 30];
ltValRU$[t_] := Chop[N[msbarRU$[I Pi^2 Quiet[LToolsEvaluate[xRU$ /. qq -> t /. D -> 4 - 2 Epsilon], LToolsEvaluate::tens] KK/I]], 10^-15][[2]];
rowsRU$ = Table[With[{tr = Rationalize[t, 0]}, {t, pxValRU$[tr], ltValRU$[tr]}], {t, nodesRU$}];
Print["(b) ", Length[rowsRU$], " values; max |Package-X - LoopTools| = ", ScientificForm[Max[Abs[#[[2]] - #[[3]]] & /@ rowsRU$], 2],
  ";  q^2 = -1: ", N[Select[rowsRU$, #[[1]] == -1. &][[1, 2 ;;]], 16]];


(* ::Subsubsection:: *)
(*Inspect: the first values*)


If[$Notebooks, TableForm[N[rowsRU$[[;; 11]], 14], TableHeadings -> {None, {"q^2/m^2", "Package-X K Pibar/e^2", "LoopTools"}}]]


strRU$[x_] := ToString[CForm[N[x, 20]]];
Quiet[CreateDirectory[FileNameJoin[{srcDirRU$, "results"}]]];
Export[FileNameJoin[{srcDirRU$, "results", "running_feyncalc.csv"}],
  StringRiffle[Prepend[StringRiffle[{strRU$[#[[1]]], strRU$[Re[#[[2]]]], strRU$[Im[#[[2]]]], strRU$[Re[#[[3]]]], strRU$[Im[#[[3]]]]}, ","] & /@ rowsRU$,
     "q2,re_px,im_px,re_lt,im_lt"], "\n"] <> "\n", "Text"];
Print["(b) wrote results/running_feyncalc.csv (K Pibar/e^2, m = 1)"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirRU$, DeleteContents -> True];
