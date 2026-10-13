(* ::Package:: *)

(* ::Title:: *)
(*Step (7): the mu-dependence of the one-loop functions and of the e+ e- -> mu+ mu- interference (FeynArts + FeynCalc, Package-X, LoopTools)*)


(* ::Text:: *)
(*Research note models/spinor_qed, step (7).  At fixed parameters (e, m_f, xi) an MS-bar quantity depends on mu only through*)
(*ln mu^2.  The RG coefficients of Eq. (rge) are read from the slopes mu d/dmu of the renormalized functions (K/e^2 units,*)
(*K = (4 Pi)^2, N_f = 2), from the RG equations of the two-point functions at one loop:*)
(*  K Pi_f^R:                  -8/3 per flavour  (sum -2 gamma_A K/e^2)  -> gamma_A = (4 N_f/3) e^2/K = beta_e/e;*)
(*  K Sigma_V^R:               -2 xi             (= -2 gamma_psi K/e^2)  -> gamma_psi = xi e^2/K;*)
(*  K Sigma_S^R:               2 (3 + xi)        (= (2 gamma_psi - gamma_m/m) K/e^2) -> gamma_m = -6 m e^2/K;*)
(*  K (Sigma_V + Sigma_S)(m^2): 6, any xi        (= -gamma_m K/(m e^2): the pole mass does not run);*)
(*  K (R_f - 1) - delta2:      -6, any xi        (UV part -2 gamma_psi, IR part -2 (3 - xi) with the IR pole -(3 - xi)).*)
(*(a) 1PI functions from FeynArts (as in oneloop_feyncalc.wl); slopes symbolically with Package-X (symbolic ScaleMu).  The*)
(*    residue needs B0', B1' at threshold, which Package-X does not evaluate; they are written with the exact D-dimensional*)
(*    relations  B0(m^2; m^2, 0) = (D-2) A0(m^2)/(2 (D-3) m^2),  B0'(m^2; m^2, 0) = -(D-2) A0(m^2)/(4 (D-3) m^4),*)
(*    B1' = -A0/(2 m^4) + B0/(2 m^2) - B0'  (note App. F; UV and IR poles are both 1/eps in dimensional regularization),*)
(*    checked against LoopTools' DB0, DB1.*)
(*(b) the 1PI brackets at the points of rg_collier.f90 for mu = 1/2, 1, 2 from Package-X (ScaleMu) and LoopTools*)
(*    (option LToolsSetMudim of LToolsEvaluate, reset to 1 at every call otherwise) -> results/rg_feyncalc_onepi.csv*)
(*    (counterterms subtracted from the pole column).*)
(*(c) K W of e+ e- -> mu+ mu- (Feynman gauge, CDR, the classes of scat_feyncalc.wl, step (4)) at the nine points of step (4)*)
(*    for mu = 1/2, 1, 2 with LoopTools (Package-X has no four-point functions) -> results/rg_feyncalc.csv.  Prediction:*)
(*    d(K W)/d ln mu^2 = P - (8/3) B(4), P the IR pole of K W (all poles carry mu^(2 eps)), -(8/3) B(4) = -(K/e^3) beta_e B(4).*)
(*e = 1, m_e = 1, m_mu = 1.7.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file rg_feyncalc.wl  (run generate_SpinorQED.wl first).  Interactive:  ~/hep/bin/wopen rg_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirRG$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirRG$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirRG$, "generated", "SpinorQED_FA"}], FileNameJoin[{modelTmpDirRG$, "SpinorQED_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirRG$, "SpinorQED_FA"}], Quiet -> True];
modelRG$ = FileNameJoin[{modelTmpDirRG$, "SpinorQED_FA", "SpinorQED_FA"}];
insertRG$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelRG$, GenericModel -> modelRG$];
xiRG$ = GaugeXi[A];
KK = (4 Pi)^2;
musRG$ = {1/2, 1, 2};


(* ::Section:: *)
(*(a) 1PI functions and their symbolic mu-dependence*)


diagPiRG$ = insertRG$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {V[1]} -> {V[1]}];
diagSeRG$ = insertRG$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {F[1]} -> {F[1]}];
diagSmRG$ = insertRG$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {F[2]} -> {F[2]}];


(* ::Subsubsection:: *)
(*Inspect: the photon and fermion two-point diagrams*)


If[$Notebooks,
  {Show[#, ImageSize -> 360] & /@ Render[Paint[diagPiRG$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 180] & /@ Render[Paint[diagSeRG$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 180] & /@ Render[Paint[diagSmRG$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]]}
]


(* ::Text:: *)
(*Amplitudes as in oneloop_feyncalc.wl: A = I Pi^2 X, X = K Pi^{mu nu} for the photon and X = -K Sigma for the fermions; the*)
(*doubled massless propagator of the xi part of Sigma is reduced by the IBP relation of App. D.*)


rawRG$[diags_, in_, out_, lor_] := FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
   IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {l}, LorentzIndexNames -> lor, ChangeDimension -> D,
   List -> False, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI // MomentumExpand // ReplaceAll[#, FCGV["EL"] -> EL] &;
reduceRG$[x_] := FCE[DiracSimplify[FeynAmpDenominatorExplicit[TID[DiracSimplify[x], l, ToPaVe -> True]]]];
ibpRG$ = {PaVe[0, {0, pp_, pp_}, {0, 0, m2_}] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2,
   C0[0, pp_, pp_, 0, 0, m2_] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2};
FCClearScalarProducts[];
ScalarProduct[q, q] = qq;
ampPiRG$ = reduceRG$[rawRG$[diagPiRG$, {q}, {q}, {mu, nu}]];
FCClearScalarProducts[];
ScalarProduct[p, p] = pp;
ampSeRG$ = reduceRG$[rawRG$[diagSeRG$, {p}, {p}, {mu}]] /. ibpRG$ /. SPD[p, p] -> pp;
ampSmRG$ = reduceRG$[rawRG$[diagSmRG$, {p}, {p}, {mu}]] /. ibpRG$ /. SPD[p, p] -> pp;
(* brackets with e = 1: K Pi_f for one flavour; K Sigma_V, K Sigma_S *)
bPiRG$[m_] := Coefficient[Expand[ampPiRG$/(I Pi^2)] /. MTD[mu, nu] -> gmn, gmn]/qq /. If[m === Me, MMU -> 0, Me -> 0] /.
   {A0[0] -> 0, B0[x_, 0, 0] -> 0} /. EL -> 1;
sigStructRG$[amp_, m_] := Module[{x = Expand[FCI[amp/(I Pi^2)]], g = DiracGamma[Momentum[p, D], D], a},
   a = Coefficient[x, g]; {-a, -Simplify[(x - a g)/m]} /. EL -> 1];
{bSVeRG$, bSSeRG$} = sigStructRG$[ampSeRG$, Me];
{bSVmRG$, bSSmRG$} = sigStructRG$[ampSmRG$, MMU];
FCClearScalarProducts[];
(* The IBP form has (m^2 - p^2)^(-2) terms that cancel only after reduction, so p^2 = m^2 cannot be substituted directly.
   The brackets equal Eq. (5) (checked here as in oneloop_feyncalc.wl), which is used from now on. *)
canonBRG$ = {B0[x_, 0, m2_] :> B0[x, m2, 0]};
handSVRG$[m_] := xiRG$ (D - 2) PaVe[1, {pp}, {m^2, 0}];
handSSRG$[m_] := (D - 1 + xiRG$) B0[pp, m^2, 0];
Print["(a) FeynCalc K Sigma_V, K Sigma_S minus Eq. (5), e and mu (expect 0): ",
  Simplify[PaVeReduce[{bSVeRG$ - handSVRG$[Me], bSSeRG$ - handSSRG$[Me], bSVmRG$ - handSVRG$[MMU], bSSmRG$ - handSSRG$[MMU]}] /. canonBRG$]];
{bSVeRG$, bSSeRG$, bSVmRG$, bSSmRG$} = {handSVRG$[Me], handSSRG$[Me], handSVRG$[MMU], handSSRG$[MMU]};
(* K (R - 1) before -delta2: Sigma_V + 2 m^2 (Sigma_V' + Sigma_S') at p^2 = m^2 with the D-dimensional coefficients (App. F) *)
rDBRG$[m_] := xiRG$ (D - 2) PaVe[1, {m^2}, {m^2, 0}] + 2 m^2 (xiRG$ (D - 2) DB1[m^2, m^2, 0] + (D - 1 + xiRG$) DB0[m^2, m^2, 0]);
relRG$ = {DB0[m2_, m2_, 0] :> -(D - 2) A0[m2]/(4 (D - 3) m2^2),
   DB1[m2_, m2_, 0] :> -A0[m2]/(2 m2^2) + (D - 2) A0[m2]/(2 (D - 3) m2^2)};
rA0RG$[m_] := rDBRG$[m] /. relRG$;


(* ::Subsubsection:: *)
(*Inspect: the brackets (PaVe form, D dimensions)*)


If[$Notebooks,
  TableForm[{{"K Pi_e", TraditionalForm[bPiRG$[Me]]}, {"K Sigma_V (e)", TraditionalForm[bSVeRG$]}, {"K Sigma_S (e)", TraditionalForm[bSSeRG$]},
    {"K (R_e - 1), A0 form", TraditionalForm[Simplify[rA0RG$[Me]]]}}]
]


(* ::Text:: *)
(*MS-bar values as in oneloop_feyncalc.wl (pole, finite part of K/e^2 times the function); ScaleMu is kept symbolic for the*)
(*slopes.  slopeRG$ returns {pole, mu d(finite)/dmu}.*)


msbarRG$[x_ /; PossibleZeroQ[x]] := {0, 0};
msbarRG$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   {SeriesCoefficient[v, -1], SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)}];
logRulesRG$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
PaXEvaluate[B0[2, 1, 1]];   (* loads Package-X *)
pxSymRG$[x_] := msbarRG$[I Pi^2 Quiet[PaXEvaluate[x /. D -> 4 - 2 Epsilon], PaXEvaluate::tens] KK/I] /. logRulesRG$;
slopeRG$[x_] := Module[{v = pxSymRG$[x]}, Simplify[{v[[1]], ScaleMu D[v[[2]], ScaleMu]}, ScaleMu > 0]];
symRG$ = <|
   "Pi_e(q^2)" -> {slopeRG$[bPiRG$[Me]], {-4/3, -8/3}},
   "Pi_mu(q^2)" -> {slopeRG$[bPiRG$[MMU]], {-4/3, -8/3}},
   "Sigma_V(p^2), e" -> {slopeRG$[bSVeRG$], {-xiRG$, -2 xiRG$}},
   "Sigma_S(p^2), e" -> {slopeRG$[bSSeRG$], {3 + xiRG$, 2 (3 + xiRG$)}},
   "Sigma_V(p^2), mu" -> {slopeRG$[bSVmRG$], {-xiRG$, -2 xiRG$}},
   "Sigma_S(p^2), mu" -> {slopeRG$[bSSmRG$], {3 + xiRG$, 2 (3 + xiRG$)}},
   "(Sigma_V + Sigma_S)(m_e^2)" -> {slopeRG$[(bSVeRG$ + bSSeRG$) /. pp -> Me^2], {3, 6}},
   "(Sigma_V + Sigma_S)(m_mu^2)" -> {slopeRG$[(bSVmRG$ + bSSmRG$) /. pp -> MMU^2], {3, 6}},
   "R_e - 1 (before -delta2)" -> {slopeRG$[rA0RG$[Me]], {-3, -6}},
   "R_mu - 1 (before -delta2)" -> {slopeRG$[rA0RG$[MMU]], {-3, -6}}|>;
KeyValueMap[Print["(a) ", #1, ":  {pole, mu d/dmu of the finite part} = ", InputForm[#2[[1]]], ",  minus the expectation ",
    InputForm[#2[[2]]], " = ", Simplify[#2[[1]] - #2[[2]]]] &, symRG$];
Print["(a) RG coefficients (e^2/K units): gamma_A = -(1/2) sum_f slope(Pi_f) = ", -(symRG$["Pi_e(q^2)"][[1, 2]] + symRG$["Pi_mu(q^2)"][[1, 2]])/2,
  ",  gamma_psi = -(1/2) slope(Sigma_V) = ", -symRG$["Sigma_V(p^2), e"][[1, 2]]/2,
  ",  gamma_m/m = 2 gamma_psi - slope(Sigma_S) = ", Simplify[-symRG$["Sigma_V(p^2), e"][[1, 2]] - symRG$["Sigma_S(p^2), e"][[1, 2]]],
  ",  from the pole mass: ", -symRG$["(Sigma_V + Sigma_S)(m_e^2)"][[1, 2]]];
Print["(a) the residue minus the note (finite part at mu, xi general): ",
  Simplify[pxSymRG$[rA0RG$[Me]][[2]] - (-4 - 3 Log[ScaleMu^2/Me^2]), {ScaleMu > 0, Me > 0}], "  (expect 0)"];


(* ::Section:: *)
(*(b) the 1PI brackets at mu = 1/2, 1, 2 with Package-X and LoopTools*)


(* ::Text:: *)
(*The points of rg_collier.f90.  Counterterms (pure poles) are subtracted from the pole column: Pi_f +4/3, Sigma_V +xi,*)
(*Sigma_S -(3 + xi), R - 1 +xi (delta2); the pole mass and the finite parts need none.  LoopTools evaluates the residue with*)
(*its DB0, DB1; Package-X with the A0 relations above.*)


coupRG$ = {Me -> 1, MMU -> 17/10};
pxNumRG$[x_, muv_] := Chop[N[msbarRG$[I Pi^2 Quiet[PaXEvaluate[x /. D -> 4 - 2 Epsilon], PaXEvaluate::tens] KK/I] /. ScaleMu -> muv /. logRulesRG$, 20], 10^-14];
ltNumRG$[x_, muv_] := Chop[N[msbarRG$[I Pi^2 Quiet[LToolsEvaluate[x /. D -> 4 - 2 Epsilon, LToolsSetMudim -> N[muv^2]], LToolsEvaluate::tens] KK/I]], 10^-14];
rowsOneRG$ = {};
addOneRG$[name_, arg_, xi_, muv_, xpx_, xlt_, ct_] := Module[{a = pxNumRG$[xpx, muv], b = ltNumRG$[xlt, muv]},
   AppendTo[rowsOneRG$, {name, arg, xi, muv, a[[1]] + ct, a[[2]], b[[1]] + ct, b[[2]]}]];
Do[
  Do[addOneRG$["Pi_e", x, 0, muv, bPiRG$[Me] /. coupRG$ /. qq -> x, bPiRG$[Me] /. coupRG$ /. qq -> x, 4/3];
     addOneRG$["Pi_mu", x, 0, muv, bPiRG$[MMU] /. coupRG$ /. qq -> x, bPiRG$[MMU] /. coupRG$ /. qq -> x, 4/3], {x, {-5, -1, 1/2, 2, 39/10, 6, 20}}];
  Do[With[{r = {pp -> x, xiRG$ -> xi}},
     addOneRG$["SigV_e", x, xi, muv, bSVeRG$ /. coupRG$ /. r, bSVeRG$ /. coupRG$ /. r, xi];
     addOneRG$["SigS_e", x, xi, muv, bSSeRG$ /. coupRG$ /. r, bSSeRG$ /. coupRG$ /. r, -(3 + xi)];
     addOneRG$["SigV_mu", x, xi, muv, bSVmRG$ /. coupRG$ /. r, bSVmRG$ /. coupRG$ /. r, xi];
     addOneRG$["SigS_mu", x, xi, muv, bSSmRG$ /. coupRG$ /. r, bSSmRG$ /. coupRG$ /. r, -(3 + xi)]], {x, {-5, 1/2, 2, 4, 10}}, {xi, {0, 1, 3}}];
  Do[With[{r = xiRG$ -> xi},
     addOneRG$["Mpole_e", 1, xi, muv, (bSVeRG$ + bSSeRG$) /. pp -> Me^2 /. coupRG$ /. r, (bSVeRG$ + bSSeRG$) /. pp -> Me^2 /. coupRG$ /. r, 0];
     addOneRG$["Mpole_mu", 17/10, xi, muv, (bSVmRG$ + bSSmRG$) /. pp -> MMU^2 /. coupRG$ /. r, (bSVmRG$ + bSSmRG$) /. pp -> MMU^2 /. coupRG$ /. r, 0];
     addOneRG$["R_e", 1, xi, muv, rA0RG$[Me] /. coupRG$ /. r, rDBRG$[Me] /. coupRG$ /. r, xi];
     addOneRG$["R_mu", 17/10, xi, muv, rA0RG$[MMU] /. coupRG$ /. r, rDBRG$[MMU] /. coupRG$ /. r, xi]], {xi, {0, 1, 3}}],
  {muv, musRG$}];
devOneRG$ = Max[Abs[Flatten[(#[[{5, 6}]] - #[[{7, 8}]]) & /@ rowsOneRG$]]];
Print["(b) ", Length[rowsOneRG$], " values: max |Package-X - LoopTools| over poles and finite parts = ", ScientificForm[devOneRG$, 2],
  "  (the residue: A0 relations against DB0, DB1)"];


(* ::Subsubsection:: *)
(*Inspect: the 1PI brackets at the three scales*)


If[$Notebooks,
  TableForm[{#[[1]], N[#[[2]]], #[[3]], N[#[[4]]], NumberForm[#[[5]], 8], NumberForm[#[[6]], 12], NumberForm[#[[8]], 12]} & /@ rowsOneRG$,
    TableHeadings -> {None, {"func", "arg", "xi", "mu", "PX pole", "PX finite", "LT finite"}}]
]


resultsDirRG$ = FileNameJoin[{srcDirRG$, "results"}];
Quiet[CreateDirectory[resultsDirRG$]];
strRG$[x_] := ToString[CForm[N[x]]];
Export[FileNameJoin[{resultsDirRG$, "rg_feyncalc_onepi.csv"}],
  StringRiffle[Prepend[StringRiffle[Join[{#[[1]], strRG$[#[[2]]], strRG$[#[[3]]], strRG$[#[[4]]]},
        Flatten[{strRG$[Re[#]], strRG$[Im[#]]} & /@ #[[5 ;; 8]]]], ","] & /@ rowsOneRG$,
     "func,arg,xi,mu,re_pole_px,im_pole_px,re_fin_px,im_fin_px,re_pole_lt,im_pole_lt,re_fin_lt,im_fin_lt"], "\n"] <> "\n", "Text"];
Print["(b) wrote results/rg_feyncalc_onepi.csv"];


(* ::Section:: *)
(*(c) K W of e+ e- -> mu+ mu- at mu = 1/2, 1, 2 (LoopTools)*)


(* ::Text:: *)
(*The amplitudes, classes, interference and residues of scat_feyncalc.wl (step (4)), Feynman gauge.*)


diag0RG$ = InsertFields[CreateTopologies[0, 2 -> 2], {F[1], -F[1]} -> {F[2], -F[2]}, InsertionLevel -> {Particles},
   Model -> modelRG$, GenericModel -> modelRG$];
diag1RG$ = InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], {F[1], -F[1]} -> {F[2], -F[2]},
   InsertionLevel -> {Particles}, Model -> modelRG$, GenericModel -> modelRG$];
convRG$[d_] := FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {p1, p2},
   OutgoingMomenta -> {k1, k2}, LoopMomenta -> {l}, ChangeDimension -> D, List -> True, SMP -> False, DropSumOver -> True,
   UndoChiralSplittings -> True] /. FCGV["EL"] -> EL;
amp0RG$ = convRG$[diag0RG$];
amp1RG$ = convRG$[diag1RG$];
chainWithRG$[a_, sp_] := Select[Cases[FCI[a], HoldPattern[Dot[x__]] /; ! FreeQ[{x}, Spinor], Infinity], ! FreeQ[#, sp] &];
classOfRG$[a_] := Which[
   ! FreeQ[a, DiracTrace], If[FreeQ[Cases[a, DiracTrace[x_] :> x, Infinity], Me], "VPmu", "VPe"],
   ! FreeQ[chainWithRG$[a, Momentum[p1, D]], l] && ! FreeQ[chainWithRG$[a, Momentum[k1, D]], l], "box",
   ! FreeQ[chainWithRG$[a, Momentum[p1, D]], l], "Ve",
   True, "Vmu"];
classesRG$ = classOfRG$ /@ amp1RG$;
Print["(c) diagram classes: ", classesRG$];
setKinRG$[mv_, Mv_, sv_, tv_] := Module[{uv = 2 mv^2 + 2 Mv^2 - sv - tv},
   FCClearScalarProducts[];
   SPD[p1, p1] = mv^2; SPD[p2, p2] = mv^2; SPD[k1, k1] = Mv^2; SPD[k2, k2] = Mv^2;
   SPD[p1, p2] = (sv - 2 mv^2)/2; SPD[k1, k2] = (sv - 2 Mv^2)/2;
   SPD[p1, k1] = (mv^2 + Mv^2 - tv)/2; SPD[p2, k2] = (mv^2 + Mv^2 - tv)/2;
   SPD[p1, k2] = (mv^2 + Mv^2 - uv)/2; SPD[p2, k1] = (mv^2 + Mv^2 - uv)/2];
treeRG$[mv_, Mv_] := FeynAmpDenominatorExplicit[amp0RG$[[1]] /. xiRG$ -> 1 /. {Me -> mv, MMU -> Mv}] // Contract // DiracSimplify;
interfRG$[m0_, a_] := Module[{x},
   x = FermionSpinSum[ComplexConjugate[m0] a, ExtraFactor -> 1] // DiracSimplify // Contract;
   x = TID[x, l, ToPaVe -> True] // FCE;
   FeynAmpDenominatorExplicit[PaVeReduce[x]] // FCI // ExpandScalarProduct // FCE];
(* x = (1/K) sum c PaVe (the normalization of W): {pole, finite} of K x at the scale mu *)
ltWRG$[x_, muv_] := Chop[N[msbarRG$[I Pi^2 Quiet[LToolsEvaluate[KK x /. D -> 4 - 2 Epsilon, LToolsSetMudim -> N[muv^2]], LToolsEvaluate::tens]] KK/I], 10^-12];
rMinus1WRG$[m_] := EL^2/KK ((D - 2) PaVe[1, {m^2}, {m^2, 0}] + 2 m^2 ((D - 2) DB1[m^2, m^2, 0] + D DB0[m^2, m^2, 0]));   (* xi = 1, before -delta2 *)
rowsWRG$ = {};
physPtsRG$ = {{16, -6}, {16, -3}, {16, -1}, {36, -20}, {36, -8}, {36, -1}, {100, -70}, {100, -30}, {100, -5}};
Do[Module[{mv = 1, Mv = 17/10, sv, tv, m0, born, born4, w, xVP, xLe, xLm, xBox},
    {sv, tv} = pt; setKinRG$[mv, Mv, sv, tv]; m0 = treeRG$[mv, Mv];
    born = Simplify[FermionSpinSum[ComplexConjugate[m0] m0] // DiracSimplify // Contract];
    born4 = N[born /. D -> 4 /. EL -> 1];
    w = interfRG$[m0, # /. xiRG$ -> 1 /. {Me -> mv, MMU -> Mv}] & /@ amp1RG$;
    xVP = (Total[Pick[w, classesRG$, "VPe"]] + Total[Pick[w, classesRG$, "VPmu"]]) /. EL -> 1;
    xLe = (Total[Pick[w, classesRG$, "Ve"]] + rMinus1WRG$[mv] born) /. EL -> 1;
    xLm = (Total[Pick[w, classesRG$, "Vmu"]] + rMinus1WRG$[Mv] born) /. EL -> 1;
    xBox = Total[Pick[w, classesRG$, "box"]] /. EL -> 1;
    Do[Module[{tot = ltWRG$[xVP, muv] + 8/3 {born4, -8} + ltWRG$[xLe, muv] + ltWRG$[xLm, muv] + ltWRG$[xBox, muv]},
        AppendTo[rowsWRG$, {sv, tv, muv, born4, tot[[1]], tot[[2]]}]], {muv, musRG$}];
    With[{r = Select[rowsWRG$, #[[1]] == sv && #[[2]] == tv &]},
      Print["(c) (s, t) = ", {sv, tv}, ":  K W pole = ", r[[2, 5]], ",  finite at mu = 1/2, 1, 2: ", r[[All, 6]],
        ";  slope d/d ln mu^2 = ", (r[[3, 6]] - r[[1, 6]])/(2 Log[4.]), ",  P - (8/3) B(4) = ", r[[2, 5]] - 8/3 born4]]], {pt, physPtsRG$}];


(* ::Subsubsection:: *)
(*Inspect: K W at the nine points and three scales*)


If[$Notebooks,
  TableForm[rowsWRG$, TableHeadings -> {None, {"s", "t", "mu", "B(4)", "pole", "finite"}}]
]


Export[FileNameJoin[{resultsDirRG$, "rg_feyncalc.csv"}],
  StringRiffle[Prepend[StringRiffle[{strRG$[#[[1]]], strRG$[#[[2]]], strRG$[#[[3]]], strRG$[#[[4]]],
        strRG$[Re[#[[5]]]], strRG$[Im[#[[5]]]], strRG$[Re[#[[6]]]], strRG$[Im[#[[6]]]]}, ","] & /@ rowsWRG$,
     "s,t,mu,born4,re_pole,im_pole,re_fin,im_fin"], "\n"] <> "\n", "Text"];
Print["(c) wrote ", Length[rowsWRG$], " rows to results/rg_feyncalc.csv (K W/e^6 at e = 1, LoopTools)"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirRG$, DeleteContents -> True];
