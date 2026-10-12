(* ::Package:: *)

(* ::Title:: *)
(*Step (3): one-loop 1PI functions of the pseudoscalar Yukawa + phi^4 model in d = 4 (FeynArts + FeynCalc, Package-X, LoopTools)*)


(* ::Text:: *)
(*Research note models/yukawa_ps, step (3).*)
(*(a) FeynArts 1PI diagrams from Src/generated/PsYukawa_FA: phi 1-point (1 diagram) and phi 3-point (2 fermion triangles),*)
(*    which must vanish by the trace (parity), V_phi (2), V_psi (1),*)
(*    V_y (1), V_4 (9 = 3 lambda^2 bubbles + 6 fermion boxes).  Traces and gamma5 in NDR, tensor reduction by TID to the*)
(*    scalar functions A0, B0, C0, D0.  With PreFactor -> 1 the note, Eq. (4) (eq:V), predicts A = (2 Pi)^D V, i.e. with*)
(*    FeynCalc's Integrate[d^D q ...] = I Pi^2 PaVe (q = loop momentum):*)
(*      A_phi = I Pi^2 [2 y^2 (p^2 B0(p^2; M^2, M^2) - 2 A0(M^2)) + lambda/2 A0(m^2)],*)
(*      A_psi = I Pi^2 y^2 [-pslash B1(p^2; M^2, m^2) - M B0(p^2; M^2, m^2)],*)
(*      A_y   = Pi^2 y^3 [-B0(p'^2; M^2, m^2) - M kslash C0 - k^2 C1 + kslash pslash C2] gamma5,*)
(*              C_i = C_i(k^2, p'^2, p^2; M^2, M^2, m^2)   (fermion in p, phi in k, fermion out p' = p + k),*)
(*      A_4   = I Pi^2 [lambda^2/2 sum_x B0(x; m^2, m^2) - 2 y^4 sum_(x,x') F(x, x')],   Eq. (7) (eq:box), on shell.*)
(*    Also the algebraic identity behind Eq. (7): the box trace T as a quadratic polynomial in the denominators.*)
(*(b) UV poles (Package-X) and the MS-bar counterterms of Eq. (5) (eq:ct).*)
(*(c) MS-bar finite parts at m = mu = 1, M = 0.7, y = lambda = 1: the brackets*)
(*      b_phi = (4 Pi)^2 V_phi / I,   b_psi^V = (4 Pi)^2 [V_psi]_pslash / I = -y^2 B1,   b_psi^S = (4 Pi)^2 [V_psi]_1 / I = -y^2 M B0,*)
(*      b_y^X = (4 Pi)^2 [V_y]_X for X = gamma5, kslash gamma5, pslash gamma5, kslash pslash gamma5*)
(*            = -y^3 (B0 + k^2 C1), -y^3 M C0, 0, y^3 C2,*)
(*      b_4 = (4 Pi)^2 V_4 / I*)
(*    from Package-X and LoopTools, written to Src/results/oneloop_mathematica.csv (oneloop_numeric.py compares them*)
(*    with COLLIER).*)
(*The gamma5-scheme comparison (BMHV vs NDR) is in oneloop_bmhv.wl.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_feyncalc.wl  (run generate_PsYukawa.wl first).  Interactive:  ~/hep/bin/wopen oneloop_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
FCSetDiracGammaScheme["NDR"];
(* keep gamma5 explicit: DiracSimplify writes odd gamma5 chains with the chiral projectors GA[6], GA[7] by default *)
SetOptions[DiracSimplify, ToDiracGamma67 -> False, DiracSubstitute67 -> True];

srcDirOL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

modelTmpDirOL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOL$, "generated", "PsYukawa_FA"}], FileNameJoin[{modelTmpDirOL$, "PsYukawa_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOL$, "PsYukawa_FA"}], Quiet -> True];
modelOL$ = FileNameJoin[{modelTmpDirOL$, "PsYukawa_FA", "PsYukawa_FA"}];
insertOL$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles},
   Model -> modelOL$, GenericModel -> modelOL$];


(* ::Section:: *)
(*(a) diagrams and amplitudes*)


diag1$ = insertOL$[CreateTopologies[1, 1 -> 0], {S[1]} -> {}];
diag3$ = insertOL$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], {S[1]} -> {S[1], S[1]}];
diagPhi$ = insertOL$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {S[1]} -> {S[1]}];
diagPsi$ = insertOL$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {F[1]} -> {F[1]}];
diagY$ = insertOL$[CreateTopologies[1, 2 -> 1, ExcludeTopologies -> {Tadpoles, WFCorrections}], {F[1], S[1]} -> {F[1]}];
diag4$ = insertOL$[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections, Reducible}],
   {S[1], S[1]} -> {S[1], S[1]}];
Print["(a) number of 1PI diagrams (expect 1, 2, 1, 1, 9; phi 3-point: 2): ",
  Length[CreateFeynAmp[#]] & /@ {diag1$, diagPhi$, diagPsi$, diagY$, diag4$, diag3$}];


(* ::Subsubsection:: *)
(*Inspect: the 1PI diagrams (phi 1-point, phi 3-point, V_phi, V_psi, V_y, V_4)*)


If[$Notebooks,
  {Show[#, ImageSize -> 180] & /@ Render[Paint[diag1$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 360] & /@ Render[Paint[diag3$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 360] & /@ Render[Paint[diagPhi$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 180] & /@ Render[Paint[diagPsi$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 180] & /@ Render[Paint[diagY$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 560] & /@ Render[Paint[diag4$, ColumnsXRows -> {5, 2}, Numbering -> Simple, DisplayFunction -> Identity]]}
]


(* ::Text:: *)
(*The FeynArts couplings gc2L, gc2R are replaced by M$FACouplings (FeynCalc does not do it, see step (2)), and the chiral*)
(*projectors omega_+ = GA[6], omega_- = GA[7] are written as (1 +- gamma5)/2, so that yps omega_+ - yps omega_- = yps gamma5*)
(*(with DiracSimplify's defaults an open fermion line would come back in terms of the projectors; see the SetOptions*)
(*above).  FeynArts' closed fermion loops come with the factor -1 and a DiracTrace.  rawOL$ keeps the unreduced integrand (used again in (d)); reduceOL$ reduces it.  V_4 is on*)
(*shell, so comparisons use u = 4 m^2 - s - t (onShellOL$).*)


rawOL$[diags_, in_, out_] := FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1] /. M$FACouplings,
   IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q}, ChangeDimension -> D,
   List -> False, SMP -> False, DropSumOver -> True] /. {DiracGamma[6] -> (1 + DiracGamma[5])/2, DiracGamma[7] -> (1 - DiracGamma[5])/2};
onShellOL$ = {u -> 4 mphi^2 - s - t};
reduceOL$[x_] := FCE[FeynAmpDenominatorExplicit[TID[DiracSimplify[x], q, ToPaVe -> True]]];

FCClearScalarProducts[];
raw1$ = rawOL$[diag1$, {p}, {}];
raw3$ = rawOL$[diag3$, {k1 + k2}, {k1, k2}];
rawPhi$ = rawOL$[diagPhi$, {p}, {p}];
rawPsi$ = rawOL$[diagPsi$, {p}, {p}];
rawY$ = rawOL$[diagY$, {p, k}, {p + k}];
amp1$ = reduceOL$[raw1$];
amp3$ = reduceOL$[raw3$];
ampPhi$ = reduceOL$[rawPhi$] /. SPD[p] -> pp;
ampPsi$ = reduceOL$[rawPsi$] /. SPD[p] -> pp;
(* V_y: fermion in p, phi in k, fermion out p' = p + k;  p^2 = pp, k^2 = kk, p'^2 = ppr *)
ScalarProduct[p, p] = pp; ScalarProduct[k, k] = kk; ScalarProduct[p, k] = (ppr - pp - kk)/2;
ampY$ = DiracOrder[DiracSimplify[reduceOL$[rawY$]], {k, p}] // FCE;
FCClearScalarProducts[];
(* V_4 on shell *)
SetMandelstam[s, t, u, p1, p2, -k1, -k2, mphi, mphi, mphi, mphi];
raw4$ = rawOL$[diag4$, {p1, p2}, {k1, k2}];
amp4$ = reduceOL$[raw4$];
FCClearScalarProducts[];


(* ::Subsubsection:: *)
(*Inspect: the reduced amplitudes*)


If[$Notebooks,
  TableForm[{{"phi 1-point", TraditionalForm[amp1$]}, {"A_phi", TraditionalForm[ampPhi$]}, {"A_psi", TraditionalForm[ampPsi$]},
    {"A_y", TraditionalForm[ampY$]}, {"A_4", TraditionalForm[Collect[amp4$, {yps, lamphi}]]}}]
]


(* ::Text:: *)
(*Comparison with the note, Eq. (4) times (2 Pi)^D.  The hand expressions with B1, C1, C2 are reduced to scalar functions*)
(*with PaVeReduce, as FeynCalc's TID does.  V_4: canonical names on shell (internal M for the fermion functions).*)


handPhi$ = I Pi^2 (2 yps^2 (pp B0[pp, Mpsi^2, Mpsi^2] - 2 A0[Mpsi^2]) + lamphi/2 A0[mphi^2]);
handPsi$ = I Pi^2 yps^2 (-GSD[p] PaVe[1, {pp}, {Mpsi^2, mphi^2}] - Mpsi B0[pp, Mpsi^2, mphi^2]);
cArgsOL$ = Sequence[{kk, ppr, pp}, {Mpsi^2, Mpsi^2, mphi^2}];
handY$ = Pi^2 yps^3 (-B0[ppr, Mpsi^2, mphi^2] GA5 - Mpsi GSD[k] . GA5 PaVe[0, cArgsOL$] - kk PaVe[1, cArgsOL$] GA5 +
     GSD[k] . GSD[p] . GA5 PaVe[2, cArgsOL$]);
diffOL$[a_, h_] := Simplify[PaVeOrder[FCE[DiracSimplify[PaVeReduce[FCI[a - h]]]]]];
canon4$ = {D0[mphi^2, mphi^2, mphi^2, mphi^2, a_, b_, Mpsi^2, Mpsi^2, Mpsi^2, Mpsi^2] :> d0M[Sort[{a, b}]],
   C0[mphi^2, mphi^2, x_, Mpsi^2, Mpsi^2, Mpsi^2] :> c0M[x], C0[mphi^2, x_, mphi^2, Mpsi^2, Mpsi^2, Mpsi^2] :> c0M[x],
   C0[x_, mphi^2, mphi^2, Mpsi^2, Mpsi^2, Mpsi^2] :> c0M[x], B0[x_, Mpsi^2, Mpsi^2] :> b0M[x], B0[x_, mphi^2, mphi^2] :> b0m[x]};
boxF$[x_, xp_] := (2 mphi^4 - x xp) d0M[Sort[{x, xp}]] + 2 (b0M[x] + b0M[xp]) + 2 (x - 2 mphi^2) c0M[x] + 2 (xp - 2 mphi^2) c0M[xp];
hand4$ = I Pi^2 (lamphi^2/2 (b0m[s] + b0m[t] + b0m[u]) - 2 yps^4 (boxF$[s, t] + boxF$[t, u] + boxF$[u, s]));
Print["(a) phi 1-point function (expect 0): ", amp1$, ";  phi 3-point function, two fermion triangles (expect 0): ", amp3$];
Print["(a) A_phi - I Pi^2 [2 y^2 (p^2 B0 - 2 A0(M^2)) + lambda/2 A0(m^2)] = ", diffOL$[ampPhi$, handPhi$], "  (expect 0)"];
Print["(a) A_psi - I Pi^2 y^2 [-pslash B1 - M B0] = ", diffOL$[ampPsi$, handPsi$], "  (expect 0)"];
Print["(a) A_y - Pi^2 y^3 [-B0 - M kslash C0 - k^2 C1 + kslash pslash C2] gamma5 = ", diffOL$[ampY$, handY$], "  (expect 0)"];
Print["(a) PaVe functions in A_4 (on shell): ", Union[Cases[amp4$ /. onShellOL$, _D0 | _C0 | _B0 | _A0, Infinity] /. canon4$]];
Print["(a) A_4 - I Pi^2 [lambda^2/2 sum B0 - 2 y^4 sum F] (Eq. (7)) = ", Simplify[((amp4$ /. onShellOL$ /. canon4$) - (hand4$ /. onShellOL$)) /. d0M[l_List] :> d0M[Sort[l]]], "  (expect 0)"];


(* ::Text:: *)
(*The identity behind Eq. (7) (App. D): T = tr[(M - k1)(M + k2)(M - k3)(M + k4)] written with D_i = k_i^2 - M^2 and*)
(*s_ij = (k_i - k_j)^2, for general (off-shell) momenta k_i = q + r_i.*)


Module[{kv = {q, q + r1, q + r1 + r2, q + r1 + r2 + r3}, dd, ss, tr, mine},
  dd[i_] := ExpandScalarProduct[SPD[kv[[i]], kv[[i]]]] - Mpsi^2;
  ss[i_, j_] := ExpandScalarProduct[SPD[kv[[i]] - kv[[j]], kv[[i]] - kv[[j]]]];
  tr = ExpandScalarProduct[DiracSimplify[DiracTrace[(Mpsi - GSD[kv[[1]]]) . (Mpsi + GSD[kv[[2]]]) . (Mpsi - GSD[kv[[3]]]) . (Mpsi + GSD[kv[[4]]])]]];
  mine = (ss[1, 2] ss[3, 4] + ss[2, 3] ss[1, 4] - ss[1, 3] ss[2, 4]) + 2 (dd[1] dd[3] + dd[2] dd[4]) +
    (ss[2, 4] - ss[2, 3] - ss[3, 4]) dd[1] + (ss[1, 3] - ss[3, 4] - ss[1, 4]) dd[2] +
    (ss[2, 4] - ss[1, 4] - ss[1, 2]) dd[3] + (ss[1, 3] - ss[1, 2] - ss[2, 3]) dd[4];
  Print["(a) box trace minus its form in the denominators (App. D) = ", Simplify[Expand[tr - mine]], "  (expect 0)"]];


(* ::Section:: *)
(*(b) UV poles and MS-bar counterterms*)


(* ::Text:: *)
(*Pole of V = A/(2 Pi)^D: the 1/eps coefficient of PaXEvaluate[A]/(2 Pi)^4.  V_psi and V_y are split into their Dirac*)
(*structures first: V_psi = a pslash + b, V_y = sum_X c_X X with X in {gamma5, kslash gamma5, pslash gamma5, kslash pslash gamma5}.*)
(*Counterterms from Eq. (4): deltaphi = I d(Pphi)/d(p^2), deltam = -I Pphi(0), deltapsi = I a, deltaM = -I b, deltay = -c_gamma5,*)
(*deltalambda = -I P4 (all times DeltaUV).*)


poleOL$[amp_] := Simplify[SeriesCoefficient[PaXEvaluate[amp], {Epsilon, 0, -1}]/(2 Pi)^4];
structPsi$[amp_] := Module[{x = Expand[FCI[amp]], g = DiracGamma[Momentum[p, D], D], a},
   a = Coefficient[x, g]; {FCE[a], FCE[Simplify[x - a g]]}];
basisY$ = {GA5, GSD[k] . GA5, GSD[p] . GA5, GSD[k] . GSD[p] . GA5};
structY$[amp_] := Module[{x = Expand[DiracOrder[DiracSimplify[FCI[amp]], {k, p}]], syms = {sY1, sYk, sYp, sYkp}, rules, y},
   rules = Thread[FCI /@ Reverse[basisY$] -> Reverse[syms]];
   y = Expand[x /. rules];
   If[! FreeQ[y, DiracGamma], Print["(b) WARNING: unmatched Dirac structure in V_y: ", y]];
   FCE[Coefficient[y, #]] & /@ syms];

pPhi$ = poleOL$[ampPhi$];
{aPsi$, bPsi$} = poleOL$ /@ structPsi$[ampPsi$];
cY$ = poleOL$ /@ structY$[ampY$];
p4$ = Simplify[poleOL$[amp4$ /. onShellOL$ /. canon4$ /. {c0M[_] -> 0, d0M[_] -> 0, b0M[x_] :> B0[x, Mpsi^2, Mpsi^2], b0m[x_] :> B0[x, mphi^2, mphi^2]}]];
Print["(b) 1/eps coefficients: V_phi = ", InputForm[pPhi$], ",  V_psi = ", InputForm[{aPsi$, bPsi$}], " (pslash, 1),  V_y = ",
  InputForm[cY$], " (gamma5, k gamma5, p gamma5, k p gamma5),  V_4 = ", InputForm[p4$]];
ct$ = Simplify[{I D[pPhi$, pp], -I (pPhi$ /. pp -> 0), I aPsi$, -I bPsi$, -cY$[[1]], -I p4$}];
Print["(b) MS-bar counterterms / DeltaUV: deltaphi, deltam, deltapsi, deltaM, deltay, deltalambda = ", InputForm[ct$]];
Print["(b) minus the note, Eq. (5): ", Simplify[ct$ - {-2 yps^2, lamphi mphi^2/2 - 4 yps^2 Mpsi^2, -yps^2/2, -yps^2 Mpsi, yps^3,
      3 lamphi^2/2 - 24 yps^4}/(4 Pi)^2], "  (expect {0, 0, 0, 0, 0, 0});  other V_y structures UV finite: ", Simplify[Rest[cY$]]];


(* ::Subsubsection:: *)
(*Inspect: the poles and the counterterms*)


If[$Notebooks,
  TableForm[{{"V_phi pole", TraditionalForm[pPhi$]}, {"V_psi pole (pslash, 1)", TraditionalForm[{aPsi$, bPsi$}]},
    {"V_y pole (gamma5, k gamma5, p gamma5, k p gamma5)", TraditionalForm[cY$]}, {"V_4 pole", TraditionalForm[p4$]},
    {"{deltaphi, deltam, deltapsi, deltaM, deltay, deltalambda}/DeltaUV", TraditionalForm[ct$]}}]
]


(* ::Section:: *)
(*(c) MS-bar finite parts at m = mu = 1, M = 0.7, y = lambda = 1*)


(* V^R = epsilon^0 coefficient of (2 Pi)^(2 eps) A/(2 Pi)^4 minus its 1/eps coefficient times (Log[4 Pi] - EulerGamma)
   (loop + MS-bar counterterm, as in the phi^3 note). *)
msbarOL$[0] = 0;   (* a Dirac structure that is absent (V_y's pslash gamma5) *)
msbarOL$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)];
logRulesOL$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
PaXEvaluate[B0[2, 1, 1]];   (* loads Package-X (context X`) *)
(* Package-X's ScalarC0, ScalarD0 take masses, not squared masses; arguments in the LoopTools order *)
numPX$ = {C0[a_, b_, c_, m0_, m1_, m2_] :> X`ScalarC0[N[a], N[b], N[c], Sqrt[N[m0]], Sqrt[N[m1]], Sqrt[N[m2]]],
   D0[a_, b_, c_, d_, e_, f_, m0_, m1_, m2_, m3_] :> X`ScalarD0[N[a], N[b], N[c], N[d], N[e], N[f], Sqrt[N[m0]], Sqrt[N[m1]], Sqrt[N[m2]], Sqrt[N[m3]]]};
pxOL$[0, _] = 0.;
pxOL$[ampNum_, fac_] := Chop[N[Simplify[fac msbarOL$[Quiet[PaXEvaluate[ampNum /. numPX$], PaXEvaluate::tens] /. ScaleMu -> 1] /. logRulesOL$], 20], 10^-14];
(* LToolsEvaluate returns each scalar function as F^fin + Res/Epsilon in FeynCalc's normalization, so msbarOL$ applies
   as for Package-X.  The TID coefficients c(D) may depend on D: with D = 4 - 2 Epsilon the eps^0 term of c(D) F contains
   the rational term -2 c'(4) Res, which a plain D -> 4 would miss. *)
ltOL$[0, _] = 0.;
ltOL$[ampNum_, fac_] := Chop[N[fac msbarOL$[Quiet[LToolsEvaluate[ampNum /. D -> 4 - 2 Epsilon], LToolsEvaluate::tens]]], 10^-14];
coup$ = {mphi -> 1, Mpsi -> 7/10, yps -> 1, lamphi -> 1};
facI$ = (4 Pi)^2/I;  facR$ = (4 Pi)^2;

rowsOL$ = {};
addRow$[name_, args_, a_, fac_] := AppendTo[rowsOL$, {name, Sequence @@ args, pxOL$[a, fac], ltOL$[a, fac]}];
Do[addRow$["Vphi", {x, 0, 0}, ampPhi$ /. coup$ /. pp -> x, facI$], {x, {-5, 0, 1, 2, 5, 10}}];
psiStruct$ = structPsi$[ampPsi$];
Do[addRow$["Vpsi_V", {x, 0, 0}, psiStruct$[[1]] /. coup$ /. pp -> x, facI$];
   addRow$["Vpsi_S", {x, 0, 0}, psiStruct$[[2]] /. coup$ /. pp -> x, facI$], {x, {-5, 1/4, 49/100, 1, 4, 10}}];
yStruct$ = structY$[ampY$];
Do[With[{rule = {pp -> pt[[1]], kk -> pt[[2]], ppr -> pt[[3]]}},
    MapThread[addRow$[#1, pt, #2 /. coup$ /. rule, facR$] &, {{"Vy_1", "Vy_k", "Vy_p", "Vy_kp"}, yStruct$}]],
  {pt, {{49/100, 1, 49/100}, {49/100, -2, 49/100}, {49/100, 5, 49/100}, {-1, -2, -3}, {1, 1/2, 4}, {3/10, 0, 2}}}];
Do[With[{ss = rs^2, tt = -2 (rs^2/4 - 1) (1 - c), uu = -2 (rs^2/4 - 1) (1 + c)},
    addRow$["V4", {ss, tt, 0}, amp4$ /. coup$ /. {s -> ss, t -> tt, u -> uu}, facI$]],
  {rs, {5/2, 5, 10}}, {c, {3/10, 9/10}}];

resultsDirOL$ = FileNameJoin[{srcDirOL$, "results"}];
Quiet[CreateDirectory[resultsDirOL$]];
numStrOL$[x_] := ToString[CForm[N[x]]];
csvLinesOL$ = Prepend[
   StringRiffle[Join[{#[[1]]}, numStrOL$ /@ {#[[2]], #[[3]], #[[4]], Re[#[[5]]], Im[#[[5]]], Re[#[[6]]], Im[#[[6]]]}], ","] & /@ rowsOL$,
   "func,arg1,arg2,arg3,re_packagex,im_packagex,re_looptools,im_looptools"];
Export[FileNameJoin[{resultsDirOL$, "oneloop_mathematica.csv"}], StringRiffle[csvLinesOL$, "\n"] <> "\n", "Text"];
Print["(c) wrote ", Length[rowsOL$], " rows to results/oneloop_mathematica.csv"];


(* ::Subsubsection:: *)
(*Inspect: the brackets from Package-X and LoopTools*)


If[$Notebooks,
  TableForm[{#[[1]], N[#[[2]]], N[#[[3]]], N[#[[4]]], NumberForm[#[[5]], 12], NumberForm[#[[6]], 12]} & /@ rowsOL$, TableHeadings -> {None, {"func", "arg1", "arg2", "arg3", "Package-X", "LoopTools"}}]
]


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirOL$, DeleteContents -> True];
