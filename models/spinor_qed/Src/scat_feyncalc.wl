(* ::Package:: *)

(* ::Title:: *)
(*Step (4): one-loop e+ e- -> mu+ mu- with FeynArts + FeynCalc (spinor QED, general covariant gauge)*)


(* ::Text:: *)
(*Research note models/spinor_qed, step (4).  e-(p1) e+(p2) -> mu-(k1) mu+(k2), s = (p1+p2)^2, t = (p1-k1)^2, u = (p1-k2)^2,*)
(*m = m_e, M = m_mu.  The quantity is the interference with the tree, W = sum_spins M0^* M1, in CDR (Dirac algebra and spin*)
(*sums in D dimensions; the Born is B(D) = sum |M0|^2 = B(4) + (D-4) 4 e^4).  K = (4 Pi)^2.  The note's formulas:*)
(*  vacuum polarization:  W_VP = Pi_f(s) B(D)  (Eq. (5));*)
(*  vertices:             W_Lambda_f = F1^Lambda_f(s) B(D) + F2^f(s) Z_f,  Z_e = (e^4/s^2) 4 s ((D-2) s + 4 M^2),*)
(*                        Z_mu = (e^4/s^2) 4 s ((D-2) s + 4 m^2)  (App. H);*)
(*  boxes:                W_box = (e^6/(K s)) [N(s, t) - N(s, u)]  (Eq. (15)), N = sum over the monomials of the numerator*)
(*                        polynomial (Table 2) times the integrals of App. H; the crossed box is minus the direct box with t <-> u.*)
(*(a) FeynArts: 1 tree diagram, 6 one-loop diagrams (2 vertices, 2 boxes, 2 vacuum-polarization loops).*)
(*(b) the box numerator: the trace equals the polynomial of Table 2 in the denominators (symbolically); crossed = -direct(t <-> u).*)
(*(c) each diagram equals its hand formula at three exact rational points (coefficient by coefficient of the PaVe functions).*)
(*(d) gauge parameter: d/dxi of the on-shell vertices is 0, that of each box is not, that of the sum of the boxes is 0.*)
(*(e) UV: the sum of the diagrams and the MS-bar counterterms (-delta3 + 2 delta1) B(D) has no UV pole.*)
(*(f) LoopTools numbers at physical points (Feynman gauge): the classes VP (with delta3), Lambda_e and Lambda_mu (with delta1*)
(*    and R_f - 1), box, and their sum; the IR pole of the sum against the eikonal formula, Eq. (16).*)
(*    -> results/scat_mathematica.csv*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file scat_feyncalc.wl  (run generate_SpinorQED.wl first).  Interactive:  ~/hep/bin/wopen scat_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirSC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirSC$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirSC$, "generated", "SpinorQED_FA"}], FileNameJoin[{modelTmpDirSC$, "SpinorQED_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirSC$, "SpinorQED_FA"}], Quiet -> True];
modelSC$ = FileNameJoin[{modelTmpDirSC$, "SpinorQED_FA", "SpinorQED_FA"}];
KK = (4 Pi)^2;
xiSC$ = GaugeXi[A];


(* ::Section:: *)
(*(a) diagrams*)


diag0$ = InsertFields[CreateTopologies[0, 2 -> 2], {F[1], -F[1]} -> {F[2], -F[2]}, InsertionLevel -> {Particles},
   Model -> modelSC$, GenericModel -> modelSC$];
diag1$ = InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], {F[1], -F[1]} -> {F[2], -F[2]},
   InsertionLevel -> {Particles}, Model -> modelSC$, GenericModel -> modelSC$];


(* ::Subsubsection:: *)
(*Inspect: the tree and the six one-loop diagrams (external self-energies are left to the residues R_f)*)


If[$Notebooks,
  {Show[#, ImageSize -> 200] & /@ Render[Paint[diag0$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 560] & /@ Render[Paint[diag1$, ColumnsXRows -> {3, 2}, Numbering -> Simple, DisplayFunction -> Identity]]}
]


Print["(a) number of diagrams: tree (expect 1) ", Length[CreateFeynAmp[diag0$]], ", one loop (expect 6) ", Length[CreateFeynAmp[diag1$]]];
convSC$[d_] := FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {p1, p2},
   OutgoingMomenta -> {k1, k2}, LoopMomenta -> {l}, ChangeDimension -> D, List -> True, SMP -> False, DropSumOver -> True,
   UndoChiralSplittings -> True] /. FCGV["EL"] -> EL;
amp0$ = convSC$[diag0$];
amp1$ = convSC$[diag1$];
(* identify the classes by content: a closed loop (DiracTrace) with an e or mu; a vertex: the loop momentum on one line only *)
chainWith$[a_, sp_] := Select[Cases[FCI[a], HoldPattern[Dot[x__]] /; ! FreeQ[{x}, Spinor], Infinity], ! FreeQ[#, sp] &];
classOf$[a_] := Which[
   ! FreeQ[a, DiracTrace], If[FreeQ[Cases[a, DiracTrace[x_] :> x, Infinity], Me], "VPmu", "VPe"],
   ! FreeQ[chainWith$[a, Momentum[p1, D]], l] && ! FreeQ[chainWith$[a, Momentum[k1, D]], l], "box",
   ! FreeQ[chainWith$[a, Momentum[p1, D]], l], "Ve",
   True, "Vmu"];
classes$ = classOf$ /@ amp1$;
Print["(a) diagram classes: ", classes$];


(* ::Section:: *)
(*(b) the box numerator in the denominators (Table 2)*)


(* ::Text:: *)
(*Direct box: ubar(k1) g^nu S(k1-l) g^rho v(k2) x vbar(p2) g_rho S(p1-l) g_nu u(p1) / (D0 D1 D2 D3), D0 = l^2, D1 = (l-p1)^2 - m^2,*)
(*D2 = (l-k1)^2 - M^2, D3 = (l-p1-p2)^2.  Its interference with the tree has the numerator N = tr_mu tr_e (App. H); with*)
(*2 l.p1 = D0 - D1, 2 l.k1 = D0 - D2, 2 l.(p1+p2) = D0 - D3 + s it is a quadratic polynomial in the D_i.  tau = m^2 + M^2 - t.*)


tableSC$[m_, M_, s_, t_] := Module[{tau = m^2 + M^2 - t, sig = m^2 + M^2},
   {{{0, 0, 0, 0}, 4 tau (sig s - s^2 - s tau + 2 tau^2) + 3/2 D s^2 tau},
    {{1, 0, 0, 0}, 4 tau (sig + s - tau) - D s tau}, {{0, 0, 0, 1}, 4 tau (sig + s - tau) - D s tau},
    {{0, 1, 0, 0}, 2 (2 sig s - 2 s^2 - 4 M^2 tau - 3 s tau + 4 tau^2) + D/2 s (3 s + 2 tau)},
    {{0, 0, 1, 0}, 2 (2 sig s - 2 s^2 - 4 m^2 tau - 3 s tau + 4 tau^2) + D/2 s (3 s + 2 tau)},
    {{2, 0, 0, 0}, (3 D/2 - 4) tau}, {{0, 0, 0, 2}, (3 D/2 - 4) tau},
    {{0, 2, 0, 0}, (D - 2) s}, {{0, 0, 2, 0}, (D - 2) s},
    {{1, 1, 0, 0}, 2 (2 s + tau) - D/2 (3 s + 2 tau)}, {{1, 0, 1, 0}, 2 (2 s + tau) - D/2 (3 s + 2 tau)},
    {{0, 1, 0, 1}, 2 (2 s + tau) - D/2 (3 s + 2 tau)}, {{0, 0, 1, 1}, 2 (2 s + tau) - D/2 (3 s + 2 tau)},
    {{1, 0, 0, 1}, -4 (2 s - tau) + D (3 s - tau)}, {{0, 1, 1, 0}, -4 (s + tau) + D (s + 2 tau)}}];
polySC$[m_, M_, s_, t_] := 4 Total[(d0^#[[1, 1]] d1^#[[1, 2]] d2^#[[1, 3]] d3^#[[1, 4]]) #[[2]] & /@ tableSC$[m, M, s, t]];
FCClearScalarProducts[];
SPD[p1, p1] = mS^2; SPD[p2, p2] = mS^2; SPD[k1, k1] = MS^2;
SPD[p1, p2] = (sS - 2 mS^2)/2; SPD[p1, k1] = (mS^2 + MS^2 - tS)/2; SPD[p2, k1] = (mS^2 + MS^2 - uS)/2;
traceNum$[trm_, tre_] := Module[{x = Contract[DiracSimplify[trm] DiracSimplify[tre]] // ExpandScalarProduct // FCI // Expand},
   x /. {Pair[Momentum[l, D], Momentum[l, D]] -> ll, Pair[Momentum[l, D], Momentum[p1, D]] -> lp1,
     Pair[Momentum[l, D], Momentum[p2, D]] -> lp2, Pair[Momentum[k1, D], Momentum[l, D]] -> lk1}];
k2v$ = p1 + p2 - k1;
trE$ = DiracTrace[(GSD[p2] - mS) . GAD[rho] . (GSD[p1] - GSD[l] + mS) . GAD[nu] . (GSD[p1] + mS) . GAD[al]];
numA$ = traceNum$[DiracTrace[(GSD[k1] + MS) . GAD[nu] . (GSD[k1] - GSD[l] + MS) . GAD[rho] . (GSD[k2v$] - MS) . GAD[al]], trE$];
numB$ = traceNum$[DiracTrace[(GSD[k1] + MS) . GAD[rho] . (GSD[l] - GSD[k2v$] + MS) . GAD[nu] . (GSD[k2v$] - MS) . GAD[al]], trE$];
uSub$ = uS -> 2 mS^2 + 2 MS^2 - sS - tS;
polyA$ = Expand[numA$ /. {ll -> d0, lp1 -> (d0 - d1)/2, lk1 -> (d0 - d2)/2, lp2 -> (d1 - d3 + sS)/2} /. uSub$];
(* crossed box: D2' = (l-k2)^2 - M^2, i.e. 2 l.k2 = d0 - d2 *)
polyB$ = Expand[numB$ /. {ll -> d0, lp1 -> (d0 - d1)/2, lp2 -> (d1 - d3 + sS)/2, lk1 -> (d0 - d1)/2 + (d1 - d3 + sS)/2 - (d0 - d2)/2} /. uSub$];
Print["(b) trace numerator of the direct box minus Table 2 (expect 0): ", Simplify[polyA$ - polySC$[mS, MS, sS, tS]]];
Print["(b) crossed box numerator + direct(t <-> u) (expect 0): ",
  Simplify[polyB$ + (polySC$[mS, MS, sS, tS] /. tS -> 2 mS^2 + 2 MS^2 - sS - tS)]];
FCClearScalarProducts[];


(* ::Text:: *)
(*The integrals of the monomials (App. H), LoopTools conventions, (K/i) mu^(2 eps) int d^Dl/(2 Pi)^D.  The squared*)
(*denominators leave a rank-1 triangle, written with C1, C2.*)


integralSC$[m_, M_, s_, t_] := Module[{mm = m^2, MM = M^2, c1, c2},
   c1[a_, b_, c_, x_, y_, z_] := PaVe[1, {a, b, c}, {x, y, z}]; c2[a_, b_, c_, x_, y_, z_] := PaVe[2, {a, b, c}, {x, y, z}];
   {{0, 0, 0, 0} -> D0[mm, mm, MM, MM, s, t, 0, mm, 0, MM],
    {1, 0, 0, 0} -> C0[mm, MM, t, mm, 0, MM], {0, 1, 0, 0} -> C0[MM, MM, s, 0, MM, 0],
    {0, 0, 1, 0} -> C0[mm, mm, s, 0, mm, 0], {0, 0, 0, 1} -> C0[mm, t, MM, 0, mm, MM],
    {1, 1, 0, 0} -> B0[MM, MM, 0], {1, 0, 1, 0} -> B0[mm, mm, 0], {1, 0, 0, 1} -> B0[t, mm, MM],
    {0, 1, 1, 0} -> B0[s, 0, 0], {0, 1, 0, 1} -> B0[MM, 0, MM], {0, 0, 1, 1} -> B0[mm, 0, mm],
    {2, 0, 0, 0} -> B0[MM, MM, 0] + 2 mm C0[mm, MM, t, mm, 0, MM] - (s - 2 mm) c1[mm, MM, t, mm, 0, MM] - (MM - mm - t) c2[mm, MM, t, mm, 0, MM],
    {0, 2, 0, 0} -> B0[MM, MM, 0] + (mm + MM - t) c1[MM, MM, s, 0, MM, 0] + s c2[MM, MM, s, 0, MM, 0],
    {0, 0, 2, 0} -> B0[mm, mm, 0] + (mm + MM - t) c1[mm, mm, s, 0, mm, 0] + s c2[mm, mm, s, 0, mm, 0],
    {0, 0, 0, 2} -> B0[t, mm, MM] + s (C0[mm, t, MM, 0, mm, MM] + c1[mm, t, MM, 0, mm, MM] + c2[mm, t, MM, 0, mm, MM])}];
calN$[m_, M_, s_, t_] := Total[4 #[[2]] (#[[1]] /. integralSC$[m, M, s, t]) & /@ tableSC$[m, M, s, t]];


(* ::Section:: *)
(*(c) each diagram against its hand formula at exact rational points*)


setKin$[mv_, Mv_, sv_, tv_] := Module[{uv = 2 mv^2 + 2 Mv^2 - sv - tv},
   FCClearScalarProducts[];
   SPD[p1, p1] = mv^2; SPD[p2, p2] = mv^2; SPD[k1, k1] = Mv^2; SPD[k2, k2] = Mv^2;
   SPD[p1, p2] = (sv - 2 mv^2)/2; SPD[k1, k2] = (sv - 2 Mv^2)/2;
   SPD[p1, k1] = (mv^2 + Mv^2 - tv)/2; SPD[p2, k2] = (mv^2 + Mv^2 - tv)/2;
   SPD[p1, k2] = (mv^2 + Mv^2 - uv)/2; SPD[p2, k1] = (mv^2 + Mv^2 - uv)/2];
tree$[mv_, Mv_] := FeynAmpDenominatorExplicit[amp0$[[1]] /. xiSC$ -> 1 /. {Me -> mv, MMU -> Mv}] // Contract // DiracSimplify;
interfSC$[m0_, a_] := Module[{x},
   x = FermionSpinSum[ComplexConjugate[m0] a, ExtraFactor -> 1] // DiracSimplify // Contract;
   x = TID[x, l, ToPaVe -> True] // FCE;
   FeynAmpDenominatorExplicit[PaVeReduce[x]] // FCI // ExpandScalarProduct // FCE];
canonSC$[x_] := Expand[FCI[PaVeReduce[FCI[x]]]] /. PaVe[0, {a_}, {0, b_}] :> PaVe[0, {a}, {b, 0}];
xPiSC$[m_, sv_] := EL^2/KK 2/((D - 1) sv) (2 (D - 2) A0[m^2] - (4 m^2 + (D - 2) sv) B0[sv, m^2, m^2]);
f1SC$[m_, q2_] := EL^2/KK (2 (D - 2) A0[m^2] + 4 (2 m^2 - q2) B0[m^2, m^2, 0] - (8 m^2 + (D - 7) q2) B0[q2, m^2, m^2] +
      2 (2 m^2 - q2) (4 m^2 - q2) C0[m^2, m^2, q2, m^2, 0, m^2])/(4 m^2 - q2);
f2SC$[m_, q2_] := -2 m EL^2/KK ((D - 2) A0[m^2]/(4 m^3 - m q2) - 4 m B0[m^2, m^2, 0]/(4 m^2 - q2) - 2 (D - 5) m B0[q2, m^2, m^2]/(4 m^2 - q2));
handSC$[cls_, mv_, Mv_, sv_, tv_, bornD_] := Module[{uv = 2 mv^2 + 2 Mv^2 - sv - tv},
   Switch[cls,
     "VPe", bornD xPiSC$[mv, sv], "VPmu", bornD xPiSC$[Mv, sv],
     "Ve", bornD f1SC$[mv, sv] + EL^4/sv^2 4 sv ((D - 2) sv + 4 Mv^2) f2SC$[mv, sv],
     "Vmu", bornD f1SC$[Mv, sv] + EL^4/sv^2 4 sv ((D - 2) sv + 4 mv^2) f2SC$[Mv, sv],
     "boxA", EL^6/(KK sv) calN$[mv, Mv, sv, tv], "boxB", -EL^6/(KK sv) calN$[mv, Mv, sv, uv]]];
pointsSC$ = {{1, 17/10, 25, -6}, {1, 17/10, 16, -3}, {1, 17/10, 30, -1/2}};
Do[Module[{mv, Mv, sv, tv, m0, born, w, diffs},
    {mv, Mv, sv, tv} = pt; setKin$[mv, Mv, sv, tv];
    m0 = tree$[mv, Mv];
    born = Simplify[FermionSpinSum[ComplexConjugate[m0] m0] // DiracSimplify // Contract];
    w = interfSC$[m0, # /. xiSC$ -> 1 /. {Me -> mv, MMU -> Mv}] & /@ amp1$;
    diffs = MapThread[If[#1 === "box",
         Min[Length[Cases[{Simplify[canonSC$[#2 - handSC$["boxA", mv, Mv, sv, tv, born]]]}, Except[0]]],
             Length[Cases[{Simplify[canonSC$[#2 - handSC$["boxB", mv, Mv, sv, tv, born]]]}, Except[0]]]],
         Simplify[canonSC$[#2 - handSC$[#1, mv, Mv, sv, tv, born]]]] &, {classes$, w}];
    Print["(c) (s, t) = ", {sv, tv}, ": B(D)/e^4 = ", born/EL^4, " (expect ", Simplify[4/sv^2 (4 (mv^2 + Mv^2)^2 + (D - 2) sv^2 - 8 (mv^2 + Mv^2) tv + 4 sv tv + 4 tv^2)],
      "); diagram - hand formula (boxes: 0 if it matches the direct or the crossed box): ", diffs]], {pt, pointsSC$}];


(* ::Section:: *)
(*(d) gauge parameter*)


(* ::Text:: *)
(*The xi-part of a photon attached to an on-shell line cancels the neighbouring propagator (App. C); in a vertex this*)
(*leaves a scaleless integral, in a box an integral proportional to the Born that cancels between the direct and the*)
(*crossed box (App. H).*)


Module[{mv = 1, Mv = 17/10, sv = 25, tv = -6, m0, dxi},
  setKin$[mv, Mv, sv, tv]; m0 = tree$[mv, Mv];
  dxi = interfSC$[m0, D[# /. {Me -> mv, MMU -> Mv}, xiSC$]] & /@ amp1$;
  Print["(d) d/dxi per diagram (", classes$, "): ", If[PossibleZeroQ[Simplify[#]], 0, "non-zero"] & /@ dxi];
  Print["(d) d/dxi of the sum of the two boxes (expect 0): ", Simplify[PaVeReduce[Total[Pick[dxi, classes$, "box"]]]]]];


(* ::Section:: *)
(*(e) UV poles*)


(* ::Text:: *)
(*Counterterms (Eq. (6)): the photon insertion gives -delta3 M0, the two vertex insertions delta1 M0 each, so their*)
(*interference is (-delta3 + 2 delta1) B(D), with delta3 = -(8/3) e^2/K DeltaUV and delta1 = -xi e^2/K DeltaUV (xi = 1 here).*)


Do[Module[{mv, Mv, sv, tv, m0, born, w, uvLoop, ct},
    {mv, Mv, sv, tv} = pt; setKin$[mv, Mv, sv, tv]; m0 = tree$[mv, Mv];
    born = Simplify[FermionSpinSum[ComplexConjugate[m0] m0] // DiracSimplify // Contract];
    w = Total[interfSC$[m0, # /. xiSC$ -> 1 /. {Me -> mv, MMU -> Mv}] & /@ amp1$];
    uvLoop = Simplify[Normal[Series[(PaVeUVPart[FCI[w], Prefactor -> 1] /. D -> 4 - 2 eps) eps, {eps, 0, 0}]]];
    ct = (8/3 - 2) EL^2/KK born /. D -> 4;
    Print["(e) (s, t) = ", {sv, tv}, ": UV pole of the loops + counterterms (expect 0): ", Simplify[uvLoop + ct]]], {pt, pointsSC$}];


(* ::Section:: *)
(*(f) LoopTools numbers at physical points and the IR pole*)


(* ::Text:: *)
(*Classes (Feynman gauge), given as K W/e^6 at e = 1, i.e. {1/eps coefficient, MS-bar finite part} of K W:*)
(*  VP = W_VPe + W_VPmu - delta3 B;  Le = W_Ve + delta1 B + (R_e - 1) B;  Lmu likewise;  box = W_boxA + W_boxB;  total.*)
(*R_f - 1 = Sigma_V + 2 m^2 (Sigma_V' + Sigma_S') - delta2 is the D-dimensional expression of step (3) with LoopTools' DB0, DB1.*)
(*A counterterm c DeltaUV times the D-dimensional Born has the pole c B(4) and the finite part c (-8 e^4) (from*)
(*B(D) = B(4) - 8 eps e^4); delta1 - delta2 = 0, so only -delta3 B = (8/3)(e^2/K) DeltaUV B is added explicitly.*)
(*The IR pole of the total is compared with Eq. (16): K W_IR/e^6 = 2 B(4) [f_IR(s; m) + f_IR(s; M) + G(t) - G(u)], with*)
(*f_IR(s; m) = ((s - 2 m^2)/(s beta)) [ln((1+beta)/(1-beta)) - i Pi] - 1 above threshold (App. H) and G by numerical integration.*)


msbarSC$[x_ /; PossibleZeroQ[x]] := {0, 0};
msbarSC$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   {SeriesCoefficient[v, -1], SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)}];
(* x = (1/K) sum c PaVe (the normalization of W): ltSC$ returns {pole, finite} of K x *)
ltSC$[x_] := Chop[N[msbarSC$[I Pi^2 Quiet[LToolsEvaluate[KK x /. D -> 4 - 2 Epsilon], LToolsEvaluate::tens]] KK/I], 10^-12];
rMinus1SC$[m_] := EL^2/KK ((D - 2) PaVe[1, {m^2}, {m^2, 0}] + 2 m^2 ((D - 2) DB1[m^2, m^2, 0] + D DB0[m^2, m^2, 0]));   (* xi = 1, before -delta2 *)
fIR$[m_, sv_] := Module[{b = Sqrt[1 - 4 m^2/sv]}, (sv - 2 m^2)/(sv b) (Log[(1 + b)/(1 - b)] - I Pi) - 1];
gIR$[m_, M_, x_] := (m^2 + M^2 - x) NIntegrate[1/(w m^2 + (1 - w) M^2 - x w (1 - w)), {w, 0, 1}, WorkingPrecision -> 30];
rowsSC$ = {};
(* physical points with rational (s, t) (so that FeynCalc works with exact numbers): sqrt(s) = 4, 6, 10 and three t each *)
physPts$ = {{16, -6}, {16, -3}, {16, -1}, {36, -20}, {36, -8}, {36, -1}, {100, -70}, {100, -30}, {100, -5}};
Do[Module[{mv = 1, Mv = 17/10, rs, c, sv, tv, uv, e, p, k, m0, born, born4, w, vals, tot, irPred, ctVP},
    {sv, tv} = pt; rs = Sqrt[sv]; e = rs/2; p = Sqrt[e^2 - mv^2]; k = Sqrt[e^2 - Mv^2];
    c = (tv - mv^2 - Mv^2 + 2 e^2)/(2 p k); uv = 2 mv^2 + 2 Mv^2 - sv - tv;
    setKin$[mv, Mv, sv, tv]; m0 = tree$[mv, Mv];
    born = Simplify[FermionSpinSum[ComplexConjugate[m0] m0] // DiracSimplify // Contract];
    born4 = N[born /. D -> 4 /. EL -> 1];
    w = interfSC$[m0, # /. xiSC$ -> 1 /. {Me -> mv, MMU -> Mv}] & /@ amp1$;
    ctVP = 8/3 {born4, -8};
    vals = <|"VP" -> ltSC$[(Total[Pick[w, classes$, "VPe"]] + Total[Pick[w, classes$, "VPmu"]]) /. EL -> 1] + ctVP,
       "Le" -> ltSC$[(Total[Pick[w, classes$, "Ve"]] + rMinus1SC$[mv] born) /. EL -> 1],
       "Lmu" -> ltSC$[(Total[Pick[w, classes$, "Vmu"]] + rMinus1SC$[Mv] born) /. EL -> 1],
       "box" -> ltSC$[Total[Pick[w, classes$, "box"]] /. EL -> 1]|>;
    tot = Total[Values[vals]];
    irPred = 2 born4 (fIR$[mv, sv] + fIR$[Mv, sv] + gIR$[mv, Mv, tv] - gIR$[mv, Mv, uv]);
    KeyValueMap[AppendTo[rowsSC$, {#1, N[rs], N[c], N[sv], N[tv], #2[[1]], #2[[2]]}] &, vals];
    AppendTo[rowsSC$, {"total", N[rs], N[c], N[sv], N[tv], tot[[1]], tot[[2]]}];
    Print["(f) sqrt(s) = ", rs, ", t = ", tv, " (cos = ", N[c], "):  K W_total/e^6 pole = ", tot[[1]], ",  Eq. (16) = ", N[irPred, 16],
      ",  finite = ", tot[[2]]]], {pt, physPts$}];


(* ::Subsubsection:: *)
(*Inspect: the classes at the physical points*)


If[$Notebooks,
  TableForm[rowsSC$, TableHeadings -> {None, {"class", "sqrt s", "cos", "s", "t", "pole", "finite"}}]
]


resultsDirSC$ = FileNameJoin[{srcDirSC$, "results"}];
Quiet[CreateDirectory[resultsDirSC$]];
strSC$[x_] := ToString[CForm[N[x]]];
Export[FileNameJoin[{resultsDirSC$, "scat_mathematica.csv"}],
  StringRiffle[Prepend[StringRiffle[{#[[1]], strSC$[#[[2]]], strSC$[#[[3]]], strSC$[#[[4]]], strSC$[#[[5]]],
        strSC$[Re[#[[6]]]], strSC$[Im[#[[6]]]], strSC$[Re[#[[7]]]], strSC$[Im[#[[7]]]]}, ","] & /@ rowsSC$,
     "class,rs,cos,s,t,re_pole,im_pole,re_fin,im_fin"], "\n"] <> "\n", "Text"];
Print["(f) wrote ", Length[rowsSC$], " rows to results/scat_mathematica.csv (K W/e^6 at e = 1)"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirSC$, DeleteContents -> True];
