(* ::Package:: *)

(* ::Title:: *)
(*Step (8): the anomalous magnetic moment with FeynArts + FeynCalc (projectors, Package-X, LoopTools)*)


(* ::Text:: *)
(*Research note models/spinor_qed, step (8), Eqs. (eq:proj), (eq:g2vp), App. g2.  e = 1, m_e = 1, m_mu = 1.7.*)
(*(a) The on-shell vertex of both flavours (FeynArts, general xi) projected on its two form factors: with P = p + p', q = p' - p,*)
(*    Lambda^mu = gamma^mu G1 + P^mu G2 between on-shell spinors (F1 = G1 + 2 m G2, F2 = -2 m G2), the traces*)
(*      T_gamma = tr[(p'slash + m) Lambda^mu (pslash + m) gamma_mu],   T_P = tr[(p'slash + m) Lambda^mu (pslash + m) P_mu]*)
(*    are a 2 x 2 linear system in (G1, G2) whose matrix is computed here from the traces of the basis (D dimensions) and*)
(*    compared with the note; its determinant 4 (D-2) q^2 (4m^2 - q^2)^2 vanishes at q^2 = 0, so F2(0) is the limit q^2 -> 0.*)
(*    Checks: F2 and F1 do not depend on xi; they equal the PaVe forms of steps (3) and (4) (App. vertex, scat_feyncalc.wl);*)
(*    K F2(0)/e^2 = 2, i.e. F2(0) = alpha/(2 pi) for both flavours; the closed form from Package-X.*)
(*(b) The vacuum polarization of one flavour subtracted at q^2 = 0, Pibar_f(t) = Pi_f^R(t) - Pi_f^R(0) (the alpha(0) scheme),*)
(*    from the FeynArts photon two-point function: Package-X closed form against the Feynman-parameter integral*)
(*    (pi/alpha) Pibar = 2 int_0^1 dz z(1-z) ln(1 - z(1-z) t/m^2); values at the quadrature nodes of g2_numeric.py*)
(*    (work/g2_nodes.txt, m = 1) from Package-X (exact rational t, 30 digits) and LoopTools (machine precision, only for*)
(*    |t| >= 0.05 m^2, where the 1/t terms of the PaVe form do not cancel badly) -> results/g2_feyncalc_pibar.csv.*)
(*(c) K F2(q^2)/e^2 of e and mu at the points of step (3) from Package-X and LoopTools -> results/g2_feyncalc_f2.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file g2_feyncalc.wl  (after g2_numeric.py --nodes; run_g2_check.sh does both).  Interactive:  ~/hep/bin/wopen g2_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirG2$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirG2$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirG2$, "generated", "SpinorQED_FA"}], FileNameJoin[{modelTmpDirG2$, "SpinorQED_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirG2$, "SpinorQED_FA"}], Quiet -> True];
modelG2$ = FileNameJoin[{modelTmpDirG2$, "SpinorQED_FA", "SpinorQED_FA"}];
insertG2$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelG2$, GenericModel -> modelG2$];
xiG2$ = GaugeXi[A];
KK = (4 Pi)^2;


(* ::Section:: *)
(*(a) The vertex and its projection on F1, F2*)


diagVeG2$ = insertG2$[CreateTopologies[1, 2 -> 1, ExcludeTopologies -> {Tadpoles, WFCorrections}], {F[1], V[1]} -> {F[1]}];
diagVmG2$ = insertG2$[CreateTopologies[1, 2 -> 1, ExcludeTopologies -> {Tadpoles, WFCorrections}], {F[2], V[1]} -> {F[2]}];


(* ::Subsubsection:: *)
(*Inspect: the one-loop vertex of e and of mu*)


If[$Notebooks,
  {Show[#, ImageSize -> 180] & /@ Render[Paint[diagVeG2$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 180] & /@ Render[Paint[diagVmG2$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]]}
]


(* ::Text:: *)
(*The amplitude A = I Pi^2 X with X = -e K Lambda (oneloop_feyncalc.wl): incoming fermion p, photon q (index mu), outgoing*)
(*fermion p1 = p + q.  The traces are taken on the integrand, then TID.  m is the mass of the flavour (Me or MMU).*)


rawVG2$[diags_] := FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
     IncomingMomenta -> {p, q}, OutgoingMomenta -> {p1}, LoopMomenta -> {l}, LorentzIndexNames -> {mu}, ChangeDimension -> D,
     List -> False, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI // MomentumExpand //
   ReplaceAll[#, FCGV["EL"] -> EL] & // ReplaceAll[#, Momentum[q, D] -> Momentum[p1, D] - Momentum[p, D]] &;
setKinG2$[m_] := (FCClearScalarProducts[]; ScalarProduct[p, p] = m^2; ScalarProduct[p1, p1] = m^2; ScalarProduct[p, p1] = m^2 - qq/2);
traceG2$[left_, x_, proj_] := DiracSimplify[DiracTrace[left . x . proj], DiracTraceEvaluate -> True];
(* the two projections of a vertex expression x (with the open index mu), m the mass *)
projG2$[x_, m_] := {traceG2$[GSD[p1] + m, x, (GSD[p] + m) . GAD[mu]],
   Contract[traceG2$[GSD[p1] + m, x, GSD[p] + m] (FVD[p, mu] + FVD[p1, mu])]};
(* the matrix of the projections of the basis {gamma^mu, P^mu} *)
matG2$[m_] := Module[{b1 = projG2$[GAD[mu], m], b2 = projG2$[FVD[p, mu] + FVD[p1, mu], m]},
   Simplify[ExpandScalarProduct[Contract[Transpose[{b1, b2}]]]]];
setKinG2$[mG];
Print["(a) projection matrix {{T_gamma(gamma), T_gamma(P)}, {T_P(gamma), T_P(P)}} = ", InputForm[matG2$[mG]]];
Print["(a) minus the note {{8m^2 + 2(D-2)q^2, 4m(4m^2-q^2)}, {4m(4m^2-q^2), 2(4m^2-q^2)^2}} = ",
  Simplify[matG2$[mG] - {{8 mG^2 + 2 (D - 2) qq, 4 mG (4 mG^2 - qq)}, {4 mG (4 mG^2 - qq), 2 (4 mG^2 - qq)^2}}],
  ";  determinant = ", Factor[Det[matG2$[mG]]]];
FCClearScalarProducts[];
formG2$[diags_, m_] := Module[{raw = rawVG2$[diags], t, mat, g},
   setKinG2$[m];
   t = FCE[PaVeReduce[FeynAmpDenominatorExplicit[TID[#, l, ToPaVe -> True]]]] & /@ projG2$[raw, m];
   mat = matG2$[m];
   g = LinearSolve[mat, t/(I Pi^2)];                (* {G1, G2} of X *)
   FCClearScalarProducts[];
   {-(g[[1]] + 2 m g[[2]])/EL, 2 m g[[2]]/EL}];      (* {K F1^Lambda, K F2}, e^2 inside (Lambda = -X/(e K)) *)
{f1eG2$, f2eG2$} = formG2$[diagVeG2$, Me];
{f1mG2$, f2mG2$} = formG2$[diagVmG2$, MMU];


(* ::Subsubsection:: *)
(*Inspect: K F2 of the electron from the projection (PaVe form, D dimensions)*)


If[$Notebooks, TraditionalForm[Simplify[f2eG2$]]]


(* ::Text:: *)
(*The note's PaVe forms (App. vertex, as in oneloop_feyncalc.wl and scat_feyncalc.wl).*)


f1noteG2$[m_, q2_] := EL^2 (2 (D - 2) A0[m^2] + 4 (2 m^2 - q2) B0[m^2, m^2, 0] - (8 m^2 + (D - 7) q2) B0[q2, m^2, m^2] +
      2 (2 m^2 - q2) (4 m^2 - q2) C0[m^2, m^2, q2, m^2, 0, m^2])/(4 m^2 - q2);
f2noteG2$[m_, q2_] := -2 m EL^2 ((D - 2) A0[m^2]/(4 m^3 - m q2) - 4 m B0[m^2, m^2, 0]/(4 m^2 - q2) - 2 (D - 5) m B0[q2, m^2, m^2]/(4 m^2 - q2));
canonG2$ = {B0[x_, 0, m2_] :> B0[x, m2, 0]};
Print["(a) d/dxi of K F1, K F2 (e, mu; expect 0): ", Simplify[D[{f1eG2$, f2eG2$, f1mG2$, f2mG2$}, xiG2$]]];
Print["(a) projection minus the note's PaVe form, K F1 and K F2 for e and mu (expect 0): ",
  Simplify[PaVeReduce[{f1eG2$ - f1noteG2$[Me, qq], f2eG2$ - f2noteG2$[Me, qq], f1mG2$ - f1noteG2$[MMU, qq], f2mG2$ - f2noteG2$[MMU, qq]}] /. canonG2$]];
(* F2 is UV and IR finite: the note's finite form K F2/e^2 = -4 m^2 [B0(q^2) - B0(0) - 2]/(4 m^2 - q^2) *)
f2finG2$[m_, q2_] := -4 m^2 (B0[q2, m^2, m^2] - B0[0, m^2, m^2] - 2)/(4 m^2 - q2);
PaXEvaluate[B0[2, 1, 1]];   (* loads Package-X *)
pxF2G2$[m_] := Simplify[PaXEvaluate[f2finG2$[m, qq]] /. ScaleMu -> 1, {qq < 0, m > 0}];
Print["(a) Package-X K F2(q^2)/e^2 for q^2 < 0: ", InputForm[pxF2G2$[mG]]];
Print["(a) K F2(0)/e^2 = lim_{q^2 -> 0} (expect 2, i.e. F2(0) = alpha/(2 pi)): electron ", Limit[pxF2G2$[1], qq -> 0, Direction -> "FromBelow"],
  ",  muon ", Limit[pxF2G2$[17/10], qq -> 0, Direction -> "FromBelow"], ",  symbolic m ", Limit[pxF2G2$[mG], qq -> 0, Direction -> "FromBelow"]];


(* ::Section:: *)
(*(b) The subtracted vacuum polarization at the quadrature nodes*)


diagPiG2$ = insertG2$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {V[1]} -> {V[1]}];
FCClearScalarProducts[];
ScalarProduct[q, q] = qq;
ampPiG2$ = FCE[DiracSimplify[FeynAmpDenominatorExplicit[TID[DiracSimplify[FCFAConvert[
        CreateFeynAmp[diagPiG2$, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
        IncomingMomenta -> {q}, OutgoingMomenta -> {q}, LoopMomenta -> {l}, LorentzIndexNames -> {mu, nu}, ChangeDimension -> D,
        List -> False, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI // ReplaceAll[#, FCGV["EL"] -> EL] &],
      l, ToPaVe -> True]]]];
FCClearScalarProducts[];
(* K Pi_f/e^2 of the electron loop (m_e = 1), the MS-bar finite part at mu = 1 *)
bPiG2$ = Coefficient[Expand[ampPiG2$/(I Pi^2)] /. MTD[mu, nu] -> gmn, gmn]/qq /. MMU -> 0 /. {A0[0] -> 0, B0[x_, 0, 0] -> 0} /. {EL -> 1, Me -> 1};
msbarG2$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   {SeriesCoefficient[v, -1], SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)}];
logRulesG2$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
pxPiFinG2$ = Simplify[msbarG2$[I Pi^2 Quiet[PaXEvaluate[bPiG2$ /. D -> 4 - 2 Epsilon], PaXEvaluate::tens] KK/I][[2]] /. ScaleMu -> 1 /. logRulesG2$, qq < 0];
pxPi0G2$ = Limit[pxPiFinG2$, qq -> 0, Direction -> "FromBelow"];
Print["(b) K Pi^R(0)/e^2 (Package-X limit) = ", pxPi0G2$, "  (expect -(4/3) B0(0; 1, 1) = 0 at m = mu = 1)"];
(* (pi/alpha) Pibar = (K/(4 e^2)) Pibar *)
pibarPXG2$ = Function[{tt}, Evaluate[(pxPiFinG2$ - pxPi0G2$)/4 /. qq -> tt]];
pibarFPG2$[t_?NumericQ] := 2 NIntegrate[z (1 - z) Log[1 - z (1 - z) t], {z, 0, 1}, WorkingPrecision -> 30, PrecisionGoal -> 25];
Print["(b) Package-X closed form minus the Feynman-parameter integral at t = -1/100, -1, -37/2, -10^4: ",
  N[pibarPXG2$[#] - pibarFPG2$[#] & /@ {-1/100, -1, -37/2, -10^4}, 5]];
nodesFileG2$ = FileNameJoin[{srcDirG2$, "work", "g2_nodes.txt"}];
nodesG2$ = ToExpression[StringReplace[#, {"e" -> "*^"}]] & /@ StringSplit[ReadString[nodesFileG2$]];
tsLtG2$ = 1/20;    (* LoopTools only for |t| >= 0.05 *)
ltPibarG2$[t_] := If[Abs[t] < tsLtG2$, Indeterminate,
   (Chop[N[msbarG2$[I Pi^2 Quiet[LToolsEvaluate[bPiG2$ /. qq -> t /. D -> 4 - 2 Epsilon], LToolsEvaluate::tens] KK/I]], 10^-14][[2]] -
      N[pxPi0G2$])/4];
rowsPibarG2$ = Table[With[{tr = Rationalize[t, 0]}, {t, N[pibarPXG2$[tr], 30], ltPibarG2$[tr]}], {t, nodesG2$}];   (* exact t: FeynCalc's Collect2 fails on machine numbers *)
Print["(b) ", Length[rowsPibarG2$], " nodes; max |Package-X - LoopTools| where LoopTools is used: ",
  ScientificForm[Max[Abs[#[[2]] - #[[3]]] & /@ Select[rowsPibarG2$, NumericQ[#[[3]]] &]], 2]];


(* ::Subsubsection:: *)
(*Inspect: Pibar at the first nodes*)


If[$Notebooks, TableForm[N[rowsPibarG2$[[;; 12]], 16], TableHeadings -> {None, {"t", "Package-X (pi/alpha) Pibar", "LoopTools"}}]]


resultsDirG2$ = FileNameJoin[{srcDirG2$, "results"}];
Quiet[CreateDirectory[resultsDirG2$]];
strG2$[x_] := If[x === Indeterminate, "nan", ToString[CForm[N[x, 20]]]];
Export[FileNameJoin[{resultsDirG2$, "g2_feyncalc_pibar.csv"}],
  StringRiffle[Prepend[StringRiffle[strG2$ /@ #, ","] & /@ rowsPibarG2$, "t,pibar_px,pibar_lt"], "\n"] <> "\n", "Text"];
Print["(b) wrote results/g2_feyncalc_pibar.csv ((pi/alpha) Pibar, m = 1)"];


(* ::Section:: *)
(*(c) K F2(q^2)/e^2 at the points of step (3)*)


rowsF2G2$ = Flatten[Table[Module[{x = f2finG2$[mv, q2], px, lt},
     px = If[q2 == 0, Limit[pxF2G2$[mv], qq -> 0, Direction -> "FromBelow"], PaXEvaluate[x] /. ScaleMu -> 1];
     lt = LToolsEvaluate[x];
     {If[mv == 1, "F2_e", "F2_mu"], q2, N[px, 20], lt}],
    {mv, {1, 17/10}}, {q2, {-5, -1, 0, 1/2, 2, 39/10, 6, 10}}], 1];
Print["(c) K F2/e^2: max |Package-X - LoopTools| = ", ScientificForm[Max[Abs[#[[3]] - #[[4]]] & /@ rowsF2G2$], 2],
  ";  at q^2 = 0: ", Select[rowsF2G2$, #[[2]] == 0 &][[All, {1, 3, 4}]]];
cplxG2$[x_] := {strG2$[Re[x]], strG2$[Im[x]]};
Export[FileNameJoin[{resultsDirG2$, "g2_feyncalc_f2.csv"}],
  StringRiffle[Prepend[StringRiffle[Join[{#[[1]], strG2$[#[[2]]]}, cplxG2$[#[[3]]], cplxG2$[#[[4]]]], ","] & /@ rowsF2G2$,
     "func,q2,re_px,im_px,re_lt,im_lt"], "\n"] <> "\n", "Text"];
Print["(c) wrote results/g2_feyncalc_f2.csv"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirG2$, DeleteContents -> True];
