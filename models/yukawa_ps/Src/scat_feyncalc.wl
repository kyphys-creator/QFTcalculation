(* ::Package:: *)

(* ::Title:: *)
(*Step (4): one-loop phi phi -> phi phi and psi psibar -> phi phi with FeynArts + FeynCalc (pseudoscalar Yukawa + phi^4)*)


(* ::Text:: *)
(*Research note models/yukawa_ps, step (4).  Truncated amplitudes (no external-leg corrections), MS-bar.*)
(*(a) phi phi -> phi phi: the FeynArts one-loop diagrams (tadpoles and external self-energies excluded, reducible ones*)
(*    allowed: expect 9 = 3 phi bubbles + 6 fermion boxes, since there is no phi^3) give Eq. (13) (eq:M1).*)
(*(b) psi(p1) psibar(p2) -> phi(k1) phi(k2): 11 diagrams = lambda triangle (1), fermion triangles on an s-channel phi (2,*)
(*    zero by the trace), vertex corrections (4), boxes (2), internal fermion self-energies (2).  With the Dirac equation*)
(*    and k2 = p1 + p2 - k1 every amplitude reduces to two spinor structures,*)
(*        (4 Pi)^2 M = a vbar(p2) u(p1) + b vbar(p2) k1slash u(p1),*)
(*    and each class is compared with the hand formulas of the note (eq:M1B, App. scat): coefficients a, b in terms of*)
(*    B0, B1, C0, C1, C2, D0, D1, D2, D3 (reduced to scalar functions with PaVeReduce, as TID does).*)
(*(c) UV poles of (b): they cancel against the MS-bar counterterm diagrams built from Eq. (5) (eq:ct).*)
(*(d) a, b (MS-bar) at m = mu = 1, M = 0.7, y = lambda = 1 and sqrt(s) = 2.5, 5, 10, cos(theta) = 0.3, 0.9 from Package-X*)
(*    and LoopTools, and M1 of (a) at the same points -> Src/results/scat_feyncalc.csv.*)
(*Normalization: FCFAConvert with PreFactor -> -I and FeynCalc's int d^D q gives A = (2 Pi)^D M, so (4 Pi)^2 M = A / Pi^2 at*)
(*D = 4 (the MS-bar finite part is taken as in oneloop_feyncalc.wl).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file scat_feyncalc.wl  (run generate_PsYukawa.wl first).  Interactive:  ~/hep/bin/wopen scat_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
FCSetDiracGammaScheme["NDR"];
SetOptions[DiracSimplify, ToDiracGamma67 -> False, DiracSubstitute67 -> True];

srcDirSC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

modelTmpDirSC$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirSC$, "generated", "PsYukawa_FA"}], FileNameJoin[{modelTmpDirSC$, "PsYukawa_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirSC$, "PsYukawa_FA"}], Quiet -> True];
modelSC$ = FileNameJoin[{modelTmpDirSC$, "PsYukawa_FA", "PsYukawa_FA"}];
insertSC$[proc_] := InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], proc,
   InsertionLevel -> {Particles}, Model -> modelSC$, GenericModel -> modelSC$];
convSC$[diags_] := FCFAConvert[CreateFeynAmp[diags, PreFactor -> -I] /. M$FACouplings, IncomingMomenta -> {p1, p2},
    OutgoingMomenta -> {k1, k2}, LoopMomenta -> {q}, ChangeDimension -> D, List -> True, SMP -> False,
    DropSumOver -> True] /. {DiracGamma[6] -> (1 + DiracGamma[5])/2, DiracGamma[7] -> (1 - DiracGamma[5])/2};
reduceSC$[x_] := FCE[FeynAmpDenominatorExplicit[TID[DiracSimplify[x], q, ToPaVe -> True]]];


(* ::Section:: *)
(*(a) phi phi -> phi phi*)


diagA$ = insertSC$[{S[1], S[1]} -> {S[1], S[1]}];


(* ::Subsubsection:: *)
(*Inspect: the diagrams of phi phi -> phi phi*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diagA$, ColumnsXRows -> {5, 2}, Numbering -> Simple, DisplayFunction -> Identity]]
]


FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, mphi, mphi, mphi, mphi];
ampA$ = Total[reduceSC$ /@ convSC$[diagA$]];
FCClearScalarProducts[];
onShellA$ = {u -> 4 mphi^2 - s - t};
canonA$ = {D0[mphi^2, mphi^2, mphi^2, mphi^2, a_, b_, Mpsi^2, Mpsi^2, Mpsi^2, Mpsi^2] :> d0M[Sort[{a, b}]],
   C0[mphi^2, mphi^2, x_, Mpsi^2, Mpsi^2, Mpsi^2] :> c0M[x], C0[mphi^2, x_, mphi^2, Mpsi^2, Mpsi^2, Mpsi^2] :> c0M[x],
   C0[x_, mphi^2, mphi^2, Mpsi^2, Mpsi^2, Mpsi^2] :> c0M[x], B0[x_, Mpsi^2, Mpsi^2] :> b0M[x], B0[x_, mphi^2, mphi^2] :> b0m[x]};
boxFA$[x_, xp_] := (2 mphi^4 - x xp) d0M[Sort[{x, xp}]] + 2 (b0M[x] + b0M[xp]) + 2 (x - 2 mphi^2) c0M[x] + 2 (xp - 2 mphi^2) c0M[xp];
(* PreFactor -I: the sum of the diagrams is (2 Pi)^D M = Pi^2 times the bracket of Eq. (13) *)
handA$ = Pi^2 (lamphi^2/2 (b0m[s] + b0m[t] + b0m[u]) - 2 yps^4 (boxFA$[s, t] + boxFA$[t, u] + boxFA$[u, s]));
Print["(a) phi phi -> phi phi: number of diagrams (expect 9): ", Length[CreateFeynAmp[diagA$]],
  ";  (2 Pi)^D M1 - Pi^2 (4 Pi)^2 M1(Eq. (13)) = ",
  Simplify[((ampA$ /. onShellA$ /. canonA$) - (handA$ /. onShellA$)) /. d0M[l_List] :> d0M[Sort[l]]], "  (expect 0)"];


(* ::Section:: *)
(*(b) psi psibar -> phi phi*)


diagB$ = insertSC$[{F[1], -F[1]} -> {S[1], S[1]}];


(* ::Subsubsection:: *)
(*Inspect: the 11 diagrams (1 lambda triangle, 2-3 fermion triangles, 4-7 vertex corrections, 8-9 boxes, 10-11 self-energies)*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diagB$, ColumnsXRows -> {4, 3}, Numbering -> Simple, DisplayFunction -> Identity]]
]


rawB$ = convSC$[diagB$];
Print["(b) psi psibar -> phi phi: number of diagrams (expect 11): ", Length[rawB$]];


(* ::Text:: *)
(*Classes, checked from the integrands: a DiracTrace (fermion triangle), the coupling lamphi (lambda triangle), four loop*)
(*propagators (box), a squared tree propagator (self-energy), otherwise a vertex correction.*)


loopProps$[x_] := Max[Length /@ Cases[FCI[x], FeynAmpDenominator[a__] /; ! FreeQ[{a}, q], Infinity]];
classOf$[x_] := Which[! FreeQ[x, DiracTrace], "ftri", ! FreeQ[x, lamphi], "ltri", loopProps$[x] == 4, "box",
   Count[FCI[x], FeynAmpDenominator[a_, a_], Infinity] > 0, "se", True, "vertex"];
classesB$ = classOf$ /@ rawB$;
Print["(b) classes of the diagrams: ", classesB$];


(* ::Text:: *)
(*Kinematics (D-dimensional external momenta) and the reduction to the basis vbar u, vbar k1slash u.*)


FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, Mpsi, Mpsi, mphi, mphi, Dimension -> D];
onShellB$ = {u -> 2 Mpsi^2 + 2 mphi^2 - s - t};
vu$ = Spinor[-Momentum[p2, D], Mpsi, 1] . Spinor[Momentum[p1, D], Mpsi, 1];
vku$ = Spinor[-Momentum[p2, D], Mpsi, 1] . GSD[k1] . Spinor[Momentum[p1, D], Mpsi, 1];
toBasis$[x_] := Module[{y = FCReplaceMomenta[FCI[x], {k2 -> p1 + p2 - k1}], c1, c2, rest},
   y = DiracSimplify[DiracOrder[DiracSimplify[y], {p2, k1, p1}]];
   y = Expand[FCE[y]] /. {FCE[vu$] -> sVU, FCE[vku$] -> sVKU};
   c1 = Coefficient[y, sVU]; c2 = Coefficient[y, sVKU]; rest = Simplify[y - c1 sVU - c2 sVKU];
   If[rest =!= 0, Print["(b) WARNING: structure outside the basis: ", rest]];
   {c1, c2}];
(* (4 Pi)^2 M = A / Pi^2 *)
abB$ = Table[toBasis$[reduceSC$[rawB$[[i]]]]/Pi^2, {i, Length[rawB$]}];
abClass$[c_] := Total[Pick[abB$, classesB$, c]];
FCClearScalarProducts[];


(* ::Subsubsection:: *)
(*Inspect: (a, b) per diagram*)


If[$Notebooks,
  TableForm[Transpose[{Range[Length[abB$]], classesB$, TraditionalForm[Simplify[# /. onShellB$]] & /@ abB$}]]
]


(* ::Text:: *)
(*The hand formulas (note eq:M1B; each a, b already multiplied by (4 Pi)^2).  B(x) = B(x; M^2, m^2); vertex C's:*)
(*C(m^2, x, M^2; M^2, M^2, m^2) at the psi(p1) end, C(m^2, M^2, x; M^2, M^2, m^2) at the psibar(p2) end; box D's:*)
(*D(M^2, m^2, m^2, M^2, x, s; m^2, M^2, M^2, M^2), Cs = C(M^2, s, M^2; m^2, M^2, M^2), C0M = C0(m^2, m^2, s; M^2, M^2, M^2);*)
(*lambda triangle C1(M^2, M^2, s; m^2, M^2, m^2).  The u-channel pieces follow from t -> u and vbar k2slash u = -vbar k1slash u.*)


bF$[i_, x_] := PaVe[i, {x}, {Mpsi^2, mphi^2}];
cV1$[i_, x_] := PaVe[i, {mphi^2, x, Mpsi^2}, {Mpsi^2, Mpsi^2, mphi^2}];
cV2$[i_, x_] := PaVe[i, {mphi^2, Mpsi^2, x}, {Mpsi^2, Mpsi^2, mphi^2}];
dB$[i_, x_] := PaVe[i, {Mpsi^2, mphi^2, mphi^2, Mpsi^2, x, s}, {mphi^2, Mpsi^2, Mpsi^2, Mpsi^2}];
cS$[i_] := PaVe[i, {Mpsi^2, s, Mpsi^2}, {mphi^2, Mpsi^2, Mpsi^2}];
c0Ms$ = PaVe[0, {mphi^2, mphi^2, s}, {Mpsi^2, Mpsi^2, Mpsi^2}];
handSE$[x_, sg_] := {yps^4 Mpsi (bF$[0, x] + bF$[1, x])/(x - Mpsi^2),
   sg yps^4 ((x + Mpsi^2) bF$[1, x] + 2 Mpsi^2 bF$[0, x])/(x - Mpsi^2)^2};
handV1$[x_, sg_] := Module[{al = bF$[0, x] + mphi^2 cV1$[1, x], be = Mpsi (cV1$[0, x] + cV1$[2, x])},
   {-yps^4 be, -sg yps^4 (al + 2 Mpsi be)/(x - Mpsi^2)}];
handV2$[x_, sg_] := Module[{al = bF$[0, Mpsi^2] + mphi^2 cV2$[1, x]},
   {-yps^4 Mpsi (cV2$[0, x] + cV2$[2, x]), -sg yps^4 (al + 2 Mpsi^2 cV2$[0, x] + (x + Mpsi^2) cV2$[2, x])/(x - Mpsi^2)}];
handBox$[x_, sg_] := {-yps^4 Mpsi ((x - Mpsi^2) (dB$[1, x] + dB$[2, x] + dB$[3, x]) - (cS$[1] + cS$[2])),
   sg yps^4 (mphi^2 dB$[0, x] + c0Ms$ + (x - Mpsi^2) dB$[2, x])};
handLtri$ = {lamphi yps^2 Mpsi PaVe[1, {Mpsi^2, Mpsi^2, s}, {mphi^2, Mpsi^2, mphi^2}], 0};
handClass$ = <|"ltri" -> handLtri$, "ftri" -> {0, 0}, "se" -> handSE$[t, 1] + handSE$[u, -1],
   "vertex" -> handV1$[t, 1] + handV2$[t, 1] + handV1$[u, -1] + handV2$[u, -1], "box" -> handBox$[t, 1] + handBox$[u, -1]|>;

cmpSC$[fc_, hand_] := (Simplify[PaVeOrder[FCE[PaVeReduce[FCI[#], PaVeAutoReduce -> True]]] /. onShellB$] & /@ ((fc - hand) /. onShellB$));
Do[Print["(b) ", c, ": (a, b)(FeynCalc) - hand = ", cmpSC$[abClass$[c], handClass$[c]], "  (expect {0, 0})"],
  {c, {"ltri", "ftri", "se", "vertex", "box"}}];


(* ::Section:: *)
(*(c) UV poles of psi psibar -> phi phi and the MS-bar counterterms*)


(* ::Text:: *)
(*Counterterm diagrams (Eq. (5) with DeltaUV -> 1/eps): the two Yukawa vertices give (2 deltay / y) times the tree,*)
(*the internal-line insertion i(deltapsi Pslash - deltaM) gives -y^2 vbar g5 (P + M)(deltapsi P - deltaM)(P + M) g5 u / (P^2 - M^2)^2.*)


ctSC$ = {deltapsi -> -yps^2/(2 (4 Pi)^2), deltaM -> -yps^2 Mpsi/(4 Pi)^2, deltay -> yps^3/(4 Pi)^2};
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, Mpsi, Mpsi, mphi, mphi, Dimension -> D];
treeB$ = yps^2 Spinor[-Momentum[p2, D], Mpsi, 1] . (GA5 . (GSD[p1 - k1] + Mpsi) . GA5/(t - Mpsi^2) +
      GA5 . (GSD[p1 - k2] + Mpsi) . GA5/(u - Mpsi^2)) . Spinor[Momentum[p1, D], Mpsi, 1];
ctSEchain$[P_, x_] := -yps^2 Spinor[-Momentum[p2, D], Mpsi, 1] . GA5 . (GSD[P] + Mpsi) . (deltapsi GSD[P] - deltaM) .
     (GSD[P] + Mpsi) . GA5 . Spinor[Momentum[p1, D], Mpsi, 1]/(x - Mpsi^2)^2;
abTree$ = toBasis$[treeB$];
abCT$ = (4 Pi)^2 (2 deltay/yps abTree$ + toBasis$[ctSEchain$[p1 - k1, t]] + toBasis$[ctSEchain$[p1 - k2, u]]) /. ctSC$;
FCClearScalarProducts[];
poleSC$[x_] := SeriesCoefficient[PaXEvaluate[x Pi^2]/(2 Pi)^4, {Epsilon, 0, -1}] (4 Pi)^2;   (* pole of (4 Pi)^2 M *)
abLoop$ = Total[abB$];
poleLoop$ = Simplify[poleSC$ /@ (abLoop$ /. onShellB$)];
Print["(b) tree: (a, b) = ", Simplify[abTree$ /. onShellB$], "  (expect {0, y^2 [1/(t-M^2) - 1/(u-M^2)]})"];
Print["(c) 1/eps coefficient of (4 Pi)^2 M (loops) = ", InputForm[Simplify[poleLoop$ /. onShellB$]]];
Print["(c) loops + counterterms (expect {0, 0}): ", Simplify[(poleLoop$ + abCT$) /. onShellB$]];


(* ::Subsubsection:: *)
(*Inspect: the poles of each class*)


If[$Notebooks,
  TableForm[{#, TraditionalForm[Simplify[poleSC$ /@ (abClass$[#] /. onShellB$)]]} & /@ {"ltri", "ftri", "se", "vertex", "box"}]
]


(* ::Section:: *)
(*(d) MS-bar values at the comparison points*)


msbarSC$[0] = 0;
msbarSC$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)];
logRulesSC$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
PaXEvaluate[B0[2, 1, 1]];
numPXSC$ = {C0[a_, b_, c_, m0_, m1_, m2_] :> X`ScalarC0[N[a], N[b], N[c], Sqrt[N[m0]], Sqrt[N[m1]], Sqrt[N[m2]]],
   D0[a_, b_, c_, d_, e_, f_, m0_, m1_, m2_, m3_] :> X`ScalarD0[N[a], N[b], N[c], N[d], N[e], N[f], Sqrt[N[m0]], Sqrt[N[m1]], Sqrt[N[m2]], Sqrt[N[m3]]]};
(* x = (4 Pi)^2 M coefficient = A/Pi^2: the MS-bar value is (4 Pi)^2 msbar[A] with A = Pi^2 x *)
pxSC$[0] = 0.; ltSC$[0] = 0.;
pxSC$[x_] := Chop[N[Simplify[(4 Pi)^2 msbarSC$[Quiet[PaXEvaluate[Pi^2 x /. numPXSC$], PaXEvaluate::tens] /. ScaleMu -> 1] /. logRulesSC$], 20], 10^-14];
(* LToolsEvaluate needs machine numbers as arguments; N acts only on the arguments, so that D-dependent coefficients
   such as (D-2)/(D-2) still cancel exactly *)
numArgsSC$[x_] := FCI[x] /. (h : A0 | B0 | C0 | D0)[args__] :> h @@ N[{args}] /. PaVe[i__, a_List, b_List] :> PaVe[i, N[a], N[b]];
ltSC$[x_] := Chop[N[(4 Pi)^2 msbarSC$[Quiet[LToolsEvaluate[numArgsSC$[Pi^2 x] /. D -> 4 - 2 Epsilon], LToolsEvaluate::tens]]], 10^-14];
coupSC$ = {mphi -> 1, Mpsi -> 7/10, yps -> 1, lamphi -> 1};
pointsSC$ = Flatten[Table[Module[{ss = rs^2, e = rs/2, pB, kB, tB, p2A, tA},
     pB = Sqrt[e^2 - (7/10)^2]; kB = Sqrt[e^2 - 1]; tB = (7/10)^2 + 1 - 2 (e^2 - pB kB c);
     p2A = ss/4 - 1; tA = -2 p2A (1 - c);
     {rs, c, ss, tB, tA}], {rs, {5/2, 5, 10}}, {c, {3/10, 9/10}}], 1];
abLoopNum$ = abLoop$ /. coupSC$;
mAnum$ = ampA$/Pi^2 /. coupSC$;   (* (4 Pi)^2 M1 of phi phi -> phi phi *)
nonNum$[x_] := Select[Union[Cases[FCI[x], _PaVe | _A0 | _B0 | _C0 | _D0, Infinity]], ! NumericQ[Total[Flatten[List @@ #]] /. PaVe -> List] &];
rowsSC$ = Table[Module[{rs = pt[[1]], c = pt[[2]], ss = pt[[3]], tB = pt[[4]], tA = pt[[5]], ab, mA},
    ab = abLoopNum$ /. {s -> ss, t -> tB, u -> 2 (7/10)^2 + 2 - ss - tB};
    mA = mAnum$ /. {s -> ss, t -> tA, u -> 4 - ss - tA};
    If[nonNum$[{ab, mA}] =!= {}, Print["(d) WARNING: non-numerical loop functions: ", InputForm[nonNum$[{ab, mA}]]]];
    {rs, c, ss, tB, tA, pxSC$[ab[[1]]], pxSC$[ab[[2]]], ltSC$[ab[[1]]], ltSC$[ab[[2]]], pxSC$[mA], ltSC$[mA]}], {pt, pointsSC$}];

resultsDirSC$ = FileNameJoin[{srcDirSC$, "results"}];
Quiet[CreateDirectory[resultsDirSC$]];
numStrSC$[x_] := ToString[CForm[N[x]]];
csvLinesSC$ = Prepend[StringRiffle[numStrSC$ /@ Flatten[{#[[1 ;; 5]], ReIm /@ #[[6 ;; 11]]}], ","] & /@ rowsSC$,
   "sqrts,costheta,s,t_B,t_A,re_a_px,im_a_px,re_b_px,im_b_px,re_a_lt,im_a_lt,re_b_lt,im_b_lt,re_mA_px,im_mA_px,re_mA_lt,im_mA_lt"];
Export[FileNameJoin[{resultsDirSC$, "scat_feyncalc.csv"}], StringRiffle[csvLinesSC$, "\n"] <> "\n", "Text"];
Print["(d) wrote ", Length[rowsSC$], " rows to results/scat_feyncalc.csv"];


(* ::Subsubsection:: *)
(*Inspect: the values*)


If[$Notebooks,
  TableForm[rowsSC$ /. x_Real :> NumberForm[x, 10], TableHeadings -> {None, {"sqrt(s)", "cos", "s", "t_B", "t_A", "a PX", "b PX", "a LT", "b LT", "M1 PX", "M1 LT"}}]
]


(* ::Section:: *)
(*Cleanup*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirSC$, DeleteContents -> True];
