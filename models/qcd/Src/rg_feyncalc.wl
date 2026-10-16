(* ::Package:: *)

(* ::Title:: *)
(*Step (6): the mu-dependence of the one-loop 1PI functions and of the u ubar -> t tbar, g g -> t tbar interferences (FeynArts + FeynCalc, Package-X, LoopTools)*)


(* ::Text:: *)
(*Research note models/qcd, step (6).  At fixed (g, m, xi) an MS-bar quantity depends on mu only through ln mu^2 at one loop;*)
(*the slope mu d/dmu follows from the RG equation of the quantity (Eq. (rgslope); K/g^2 times the quantity, K = (4 Pi)^2):*)
(*  K Pi^R:   gluon + ghost loops C_A (13/3 - xi), each quark loop -(8/3) T_F   (sum -2 gamma_A; full propagator 1/(k^2 (1 - Pi)));*)
(*  K Pitilde^R: -(3 - xi) C_A/2   (2 gamma_c; full ghost propagator 1/(p^2 (1 + Pitilde)));*)
(*  K Sigma_V^R: -2 xi C_F (-2 gamma_psi);   K Sigma_S^R: 2 (3 + xi) C_F (2 gamma_psi - gamma_m/m);*)
(*  pole mass K (Sigma_V + Sigma_S)(m^2): 6 C_F for every xi (-gamma_m/m);  K (R_Q - 1) before -delta2: -6 C_F, IR pole -(3 - xi) C_F;*)
(*  K Pi_Q^R(0) (the t part of R_G): -(8/3) T_F;  decoupling: K [Pi_Q^R(k^2) - Pi_Q^R(0)] = -(4/3) T_F [k^2/(5 m^2) + 3 k^4/(140 m^4) + ...],*)
(*  independent of mu.*)
(*(a) the two-point functions from FeynArts as in oneloop_feyncalc.wl (step (3)), checked against Eq. (V); Eq. (V) is used*)
(*    from then on (the IBP form of the t self-energy has (m^2 - p^2)^-2 terms, so p^2 = m^2 cannot be substituted directly).*)
(*(b) slopes symbolically with Package-X (ScaleMu symbolic, general xi and momenta).  The residue needs B0', B1' at threshold, which*)
(*    Package-X does not evaluate; they are written with the exact D-dimensional relations to A0 (App. F of the QED note).*)
(*(c) the brackets at the points of rg_collier.f90 for mu = 1/2, 1, 2 from Package-X and LoopTools (option LToolsSetMudim of*)
(*    LToolsEvaluate; LoopTools' DB0, DB1 for the residue) -> results/rg_feyncalc_onepi.csv (expected pole subtracted).*)
(*(d) K W of (A) u ubar -> t tbar and (B) g g -> t tbar (Feynman gauge, CDR, MS-bar coupling with n_f = 6, pole mass, SU(3), g = 1)*)
(*    at s = 10, t = -3 for mu = 1/2, 1, 2 with LoopTools: the TID amplitudes of scat_feyncalc.wl (step (4), work/scat/<A,B>/tid_*.m)*)
(*    plus the counterterms and residues of scat_eval.wl, with A0, B1, DB0, DB1 from LoopTools at the same mu*)
(*    -> results/rg_feyncalc.csv.  rg_numeric.py compares with Eq. (rgW) and reads beta_0.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file rg_feyncalc.wl  (after generate_QCD.wl and run_scat_check.sh).  Interactive:  ~/hep/bin/wopen rg_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


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
CopyDirectory[FileNameJoin[{srcDirRG$, "generated", "QCD_FA"}], FileNameJoin[{modelTmpDirRG$, "QCD_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirRG$, "QCD_FA"}], Quiet -> True];
modelRG$ = FileNameJoin[{modelTmpDirRG$, "QCD_FA", "QCD_FA"}];
KK = (4 Pi)^2;
musRG$ = {1/2, 1, 2};


(* ::Text:: *)
(*Helpers as in oneloop_feyncalc.wl.  Field codes: V[2] gluon, U[1] ghost, F[2] u, F[7] t.  The coupling is renamed gS (GS is*)
(*FeynCalc's slash) and the gauge parameter of an internal gluon xi.  eta = 1 - xi.*)


insRG$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelRG$, GenericModel -> modelRG$,
   ExcludeParticles -> {V[1], F[1]}];
rawRG$[diags_, in_, out_, lor_] := FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
    IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {l}, LorentzIndexNames -> lor, ChangeDimension -> D,
    List -> True, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI // MomentumExpand //
   ReplaceAll[#, {SMP["g_s"] -> gS, FCGV["GS"] -> gS, GaugeXi[V[2, ___]] -> xi, GaugeXi[G] -> xi, FCGV["MT"] -> mt, SMP["m_t"] -> mt}] &;
redRG$[x_] := FCE[SUNSimplify[DiracSimplify[FeynAmpDenominatorExplicit[TID[SUNSimplify[DiracSimplify[x], SUNNToCACF -> True], l,
        ToPaVe -> True]]], SUNNToCACF -> True]] /. {SD[__] -> 1, SDF[__] -> 1, SUNDelta[__] -> 1, SUNFDelta[__] -> 1};
ibpRG$ = {PaVe[0, {0, qq_, qq_}, {0, 0, 0}] :> -(D - 3)/qq B0[qq, 0, 0], C0[0, qq_, qq_, 0, 0, 0] :> -(D - 3)/qq B0[qq, 0, 0],
   PaVe[0, {0, qq_, 0, qq_, qq_, qq_}, {0, 0, 0, 0}] :> (D - 3) (D - 6)/qq^2 B0[qq, 0, 0],
   C0[0, pp_, pp_, 0, 0, m2_] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2,
   PaVe[0, {0, pp_, pp_}, {0, 0, m2_}] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2,
   PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {qq_}, {ma_, mb_}] :> B0[qq, ma, mb],
   B0[qq_, 0, m2_] /; m2 =!= 0 :> B0[qq, m2, 0]};
fullRedRG$[x_] := Simplify[PaVeReduce[x] //. ibpRG$ /. {B0[0, 0, 0] -> 0, A0[0] -> 0}];


(* ::Section:: *)
(*(a) the two-point functions*)


topSERG$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];
diagGRG$ = insRG$[topSERG$, {V[2]} -> {V[2]}];
diagCRG$ = insRG$[topSERG$, {U[1]} -> {U[1]}];
diagURG$ = insRG$[topSERG$, {F[2]} -> {F[2]}];
diagTRG$ = insRG$[topSERG$, {F[7]} -> {F[7]}];


(* ::Subsubsection:: *)
(*Inspect: the two-point diagrams (gluon, ghost, u, t)*)


If[$Notebooks,
  {Show[#, ImageSize -> 600] & /@ Render[Paint[diagGRG$, ColumnsXRows -> {5, 2}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 160] & /@ Render[Paint[diagCRG$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 160] & /@ Render[Paint[diagURG$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 160] & /@ Render[Paint[diagTRG$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]]}
]


(* ::Text:: *)
(*Amplitudes A = I Pi^2 X with X = K Pi^{mu nu} (gluon), K p^2 Pitilde (ghost), -K Sigma (quarks).  The brackets b... are K/g^2*)
(*times the note's quantities in D dimensions (Eq. (V)); bPiQ is one quark flavour of mass^2 m2 (T_F x the QED vacuum polarization).*)


bPiYMRG$ = CA/2 ((3 D - 2)/(D - 1) + (2 D - 7) eta - (D - 4)/4 eta^2) B0[qq, 0, 0];
bPiQRG$[m2_] := TF 2/((D - 1) qq) (2 (D - 2) A0[m2] - (4 m2 + (D - 2) qq) B0[qq, m2, m2]) /. A0[0] -> 0;
bGhRG$ = -CA (1/2 + (D - 3) eta/4) B0[pp, 0, 0];
bSVRG$[m2_] := CF xi (D - 2) PaVe[1, {pp}, {m2, 0}];
bSSRG$[m2_] := CF (D - 1 + xi) B0[pp, m2, 0];
b1RuleRG$ = {PaVe[1, {pp_}, {m2_, 0}] /; m2 =!= 0 :> (A0[m2] - (pp + m2) B0[pp, m2, 0])/(2 pp), PaVe[1, {pp_}, {0, 0}] :> -B0[pp, 0, 0]/2};
FCClearScalarProducts[]; ScalarProduct[q, q] = qq;
piFARG$ = Simplify[Total[fullRedRG$[Contract[FCI[#] MTD[mu, nu]] /. SPD[q, q] -> qq] & /@ (redRG$ /@ (rawRG$[diagGRG$, {q}, {q}, {mu, nu}] /. xi -> 1 - eta))]/
    (I Pi^2 gS^2 (D - 1) qq)];
FCClearScalarProducts[]; ScalarProduct[p, p] = pp;
ghFARG$ = Simplify[fullRedRG$[Total[redRG$ /@ (rawRG$[diagCRG$, {p}, {p}, {mu}] /. xi -> 1 - eta)] /. SPD[p, p] -> pp]/(I Pi^2 gS^2 pp)];
sigFARG$[diag_, m_] := Module[{x = Total[redRG$ /@ rawRG$[diag, {p}, {p}, {mu}]], g = GSD[p], a},
   x = Expand[fullRedRG$[x /. SPD[p, p] -> pp]/(I Pi^2 gS^2)];
   a = Coefficient[x, g]; {-a, If[m === 0, -(x - a g), -Simplify[(x - a g)/m]]}];
{sVuFARG$, sSuFARG$} = sigFARG$[diagURG$, 0];
{sVtFARG$, sStFARG$} = sigFARG$[diagTRG$, mt];
FCClearScalarProducts[];
Print["(a) FeynArts minus Eq. (V) (gluon with n_l = 5 + t, ghost, u Sigma_V and Sigma_S, t Sigma_V and Sigma_S; expect 0): ",
  Simplify[{piFARG$ - (bPiYMRG$ + 5 bPiQRG$[0] + bPiQRG$[mt^2]), ghFARG$ - bGhRG$, sVuFARG$ - (bSVRG$[0] /. b1RuleRG$), sSuFARG$,
     sVtFARG$ - (bSVRG$[mt^2] /. b1RuleRG$), sStFARG$ - bSSRG$[mt^2]} /. TF -> 1/2]];   (* FeynCalc writes tr(T^a T^b) = delta^ab/2 *)
(* K (R_Q - 1) before -delta2: Sigma_V + 2 m^2 (Sigma_V' + Sigma_S') at p^2 = m^2 (App. F); with the exact A0 relations for Package-X *)
rDBRG$[m2_] := CF (xi (D - 2) PaVe[1, {m2}, {m2, 0}] + 2 m2 (xi (D - 2) DB1[m2, m2, 0] + (D - 1 + xi) DB0[m2, m2, 0]));
relRG$ = {DB0[m2_, m2_, 0] :> -(D - 2) A0[m2]/(4 (D - 3) m2^2), DB1[m2_, m2_, 0] :> -A0[m2]/(2 m2^2) + (D - 2) A0[m2]/(2 (D - 3) m2^2)};
rA0RG$[m2_] := rDBRG$[m2] /. relRG$;
(* K Pi_Q(0): the k^2 -> 0 limit of bPiQ (by the IBP relations of a massive bubble), the t part of R_G *)
bPiQ0RG$[m2_] := -(2/3) TF (D - 2) A0[m2]/m2;


(* ::Subsubsection:: *)
(*Inspect: the brackets (PaVe form, D dimensions)*)


If[$Notebooks,
  TableForm[{{"K Pi (gluon + ghost loops)", TraditionalForm[bPiYMRG$]}, {"K Pi (one quark of mass^2 m2)", TraditionalForm[bPiQRG$[m2]]},
    {"K Pitilde", TraditionalForm[bGhRG$]}, {"K Sigma_V, K Sigma_S", TraditionalForm[{bSVRG$[m2], bSSRG$[m2]}]},
    {"K (R_Q - 1), A0 form", TraditionalForm[Simplify[rA0RG$[m2]]]}, {"K Pi_Q(0)", TraditionalForm[bPiQ0RG$[m2]]}}]
]


(* ::Section:: *)
(*(b) symbolic slopes (Package-X)*)


(* ::Text:: *)
(*MS-bar values as in oneloop_feyncalc.wl: {pole, finite part} of the bracket; ScaleMu stays symbolic.  slopeRG$ returns*)
(*{pole, mu d(finite)/dmu}.*)


msbarRG$[x_ /; PossibleZeroQ[x]] := {0, 0};
msbarRG$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   {SeriesCoefficient[v, -1], SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)}];
logRulesRG$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
PaXEvaluate[B0[2, 1, 1]];   (* loads Package-X *)
pxSymRG$[x_] := msbarRG$[I Pi^2 Quiet[PaXEvaluate[x /. D -> 4 - 2 Epsilon], PaXEvaluate::tens] KK/I] /. logRulesRG$;
slopeRG$[x_] := Module[{v = pxSymRG$[x]}, Simplify[{v[[1]], ScaleMu D[v[[2]], ScaleMu]}, {ScaleMu > 0, mt > 0}]];
symRG$ = <|
   "Pi, gluon + ghost loops" -> {slopeRG$[bPiYMRG$ /. eta -> 1 - xi], {(13/6 - xi/2) CA, (13/3 - xi) CA}},
   "Pi, massless quark loop" -> {slopeRG$[bPiQRG$[0]], {-4/3 TF, -8/3 TF}},
   "Pi, t loop" -> {slopeRG$[bPiQRG$[mt^2]], {-4/3 TF, -8/3 TF}},
   "Pitilde" -> {slopeRG$[bGhRG$ /. eta -> 1 - xi], {-(3 - xi)/4 CA, -(3 - xi)/2 CA}},
   "Sigma_V, u" -> {slopeRG$[bSVRG$[0]], {-xi CF, -2 xi CF}},
   "Sigma_V, t" -> {slopeRG$[bSVRG$[mt^2]], {-xi CF, -2 xi CF}},
   "Sigma_S, t" -> {slopeRG$[bSSRG$[mt^2]], {(3 + xi) CF, 2 (3 + xi) CF}},
   "(Sigma_V + Sigma_S)(m^2), t" -> {slopeRG$[(bSVRG$[mt^2] + bSSRG$[mt^2]) /. pp -> mt^2], {3 CF, 6 CF}},
   "R_Q - 1 (before -delta2)" -> {slopeRG$[rA0RG$[mt^2]], {-3 CF, -6 CF}},
   "Pi_Q(0) (t part of R_G)" -> {slopeRG$[bPiQ0RG$[mt^2]], {-4/3 TF, -8/3 TF}}|>;
KeyValueMap[Print["(b) ", #1, ":  {pole, mu d/dmu of the finite part} = ", InputForm[#2[[1]]], ",  minus the expectation = ",
    Simplify[#2[[1]] - #2[[2]]]] &, symRG$];
slYM$ = symRG$["Pi, gluon + ghost loops"][[1, 2]]; slQ$ = symRG$["Pi, t loop"][[1, 2]];
Print["(b) RG coefficients (g^2/K units): gamma_A = -(1/2) [slope(YM) + n_f slope(quark)] = ", Simplify[-(slYM$ + nf slQ$)/2],
  ",  gamma_c = (1/2) slope(Pitilde) = ", symRG$["Pitilde"][[1, 2]]/2, ",  gamma_psi = -(1/2) slope(Sigma_V) = ", -symRG$["Sigma_V, t"][[1, 2]]/2,
  ",  gamma_m/m = 2 gamma_psi - slope(Sigma_S) = ", Simplify[-symRG$["Sigma_V, t"][[1, 2]] - symRG$["Sigma_S, t"][[1, 2]]],
  ",  from the pole mass: ", -symRG$["(Sigma_V + Sigma_S)(m^2), t"][[1, 2]]];
(* finite parts against Eq. (VR) and Eq. (os), and the decoupling expansion *)
finRG$[x_] := pxSymRG$[x][[2]];
Print["(b) residue and Pi_Q(0) minus Eqs. (VR), (os) (finite parts; expect 0, 0): ",
  Simplify[{finRG$[rA0RG$[mt^2]] - CF (-4 - 3 Log[ScaleMu^2/mt^2]), finRG$[bPiQ0RG$[mt^2]] - (-4/3 TF Log[ScaleMu^2/mt^2])}, {ScaleMu > 0, mt > 0}]];
decRG$ = Normal[Series[finRG$[bPiQRG$[mt^2]] - finRG$[bPiQ0RG$[mt^2]], {qq, 0, 3}]];
Print["(b) decoupling: K [Pi_Q(k^2) - Pi_Q(0)] up to k^6 = ", InputForm[Simplify[decRG$, {ScaleMu > 0, mt > 0}]],
  ";  minus -(4/3) T_F [k^2/(5 m^2) + 3 k^4/(140 m^4)] = ", Simplify[Coefficient[decRG$, qq, {1, 2}] + 4/3 TF {1/(5 mt^2), 3/(140 mt^4)}, {ScaleMu > 0, mt > 0}],
  "  (expect {0, 0}; no mu)"];


(* ::Section:: *)
(*(c) the 1PI brackets at mu = 1/2, 1, 2 with Package-X and LoopTools*)


(* ::Text:: *)
(*The points of rg_collier.f90, SU(3), T_F = 1/2, m = 1.  The pole column is the pole minus the expected one (the counterterm,*)
(*or for the residue the UV + IR pole -3 C_F); the pole mass and the decoupling difference have none.  LoopTools evaluates the*)
(*residue with its DB0, DB1, Package-X with the A0 relations.*)


numRG$ = {CA -> 3, CF -> 4/3, TF -> 1/2, mt -> 1};
$MaxExtraPrecision = 200;     (* Pi_t(k^2) - Pi_t(0) at |k^2| = 10^-3 m^2 cancels to k^2/(5 m^2) *)
(* the exactly cancelling pole of Pi_t(k^2) - Pi_t(0) cannot be certified as 0 by N (N::meprec); Chop sets it to 0 *)
pxNumRG$[x_, muv_] := Chop[Quiet[N[msbarRG$[I Pi^2 Quiet[PaXEvaluate[x /. D -> 4 - 2 Epsilon], PaXEvaluate::tens] KK/I] /. ScaleMu -> muv /. logRulesRG$, 20], N::meprec], 10^-14];
ltNumRG$[x_, muv_] := Chop[N[msbarRG$[I Pi^2 Quiet[LToolsEvaluate[x /. D -> 4 - 2 Epsilon, LToolsSetMudim -> N[muv^2]], LToolsEvaluate::tens] KK/I]], 10^-14];
rowsOneRG$ = {};
addOneRG$[name_, arg_, xv_, muv_, xpx_, xlt_, pole_] := Module[{a = pxNumRG$[xpx /. numRG$, muv], b = ltNumRG$[xlt /. numRG$, muv]},
   AppendTo[rowsOneRG$, {name, arg, xv, muv, a[[1]] - pole, a[[2]], b[[1]] - pole, b[[2]]}]];
Do[
  Do[With[{r = {qq -> x, pp -> x, eta -> 1 - xv, xi -> xv}},
     addOneRG$["PiYM", x, xv, muv, bPiYMRG$ /. r, bPiYMRG$ /. r, 3 (13/6 - xv/2)];
     addOneRG$["Ghost", x, xv, muv, bGhRG$ /. r, bGhRG$ /. r, -3 (3 - xv)/4]], {x, {-5, -1, 1/2, 2, 6, 20}}, {xv, {0, 1, 3}}];
  Do[addOneRG$["PiQ0", x, 0, muv, bPiQRG$[0] /. qq -> x, bPiQRG$[0] /. qq -> x, -2/3], {x, {-5, -1, 1/2, 2, 6, 20}}];
  Do[addOneRG$["PiT", x, 0, muv, bPiQRG$[mt^2] /. qq -> x, bPiQRG$[mt^2] /. qq -> x, -2/3], {x, {-5, -1, 1/2, 2, 39/10, 6, 20}}];
  Do[With[{r = {pp -> x, xi -> xv}},
     addOneRG$["SigV_t", x, xv, muv, bSVRG$[mt^2] /. r, bSVRG$[mt^2] /. r, -xv 4/3];
     addOneRG$["SigS_t", x, xv, muv, bSSRG$[mt^2] /. r, bSSRG$[mt^2] /. r, (3 + xv) 4/3]], {x, {-5, 1/2, 2, 4, 10}}, {xv, {0, 1, 3}}];
  Do[addOneRG$["SigV_u", x, xv, muv, bSVRG$[0] /. {pp -> x, xi -> xv}, bSVRG$[0] /. {pp -> x, xi -> xv}, -xv 4/3], {x, {-5, 1/2, 2}}, {xv, {0, 1, 3}}];
  Do[With[{r = xi -> xv},
     addOneRG$["Mpole", 1, xv, muv, (bSVRG$[mt^2] + bSSRG$[mt^2]) /. pp -> mt^2 /. r, (bSVRG$[mt^2] + bSSRG$[mt^2]) /. pp -> mt^2 /. r, 4];
     addOneRG$["R_Q", 1, xv, muv, rA0RG$[mt^2] /. r, rDBRG$[mt^2] /. r, -4]], {xv, {0, 1, 3}}];
  addOneRG$["PiT0", 0, 0, muv, bPiQ0RG$[mt^2], bPiQ0RG$[mt^2], -2/3];
  Do[addOneRG$["PiTsub", x, 0, muv, (bPiQRG$[mt^2] /. qq -> x) - bPiQ0RG$[mt^2], (bPiQRG$[mt^2] /. qq -> x) - bPiQ0RG$[mt^2], 0],
   {x, {-1, -1/10, -1/100, -1/1000, 1/1000, 1/100, 1/10, 1}}],
  {muv, musRG$}];
devOneRG$ = Max[Abs[Flatten[(#[[{5, 6}]] - #[[{7, 8}]]) & /@ rowsOneRG$]]];
Print["(c) ", Length[rowsOneRG$], " values: max |Package-X - LoopTools| over poles and finite parts = ", N[devOneRG$, 3],
  " (without the decoupling difference PiTsub, where LoopTools loses digits at small k^2: ",
  N[Max[Abs[Flatten[(#[[{5, 6}]] - #[[{7, 8}]]) & /@ Select[rowsOneRG$, #[[1]] =!= "PiTsub" &]]]], 3], "),  max |pole - expected| = ",
  N[Max[Abs[Flatten[rowsOneRG$[[All, {5, 7}]]]]], 3]];


(* ::Subsubsection:: *)
(*Inspect: the 1PI brackets at the three scales*)


If[$Notebooks,
  TableForm[{#[[1]], N[#[[2]]], #[[3]], N[#[[4]]], NumberForm[#[[5]], 8], NumberForm[#[[6]], 12], NumberForm[#[[8]], 12]} & /@ rowsOneRG$,
    TableHeadings -> {None, {"func", "arg", "xi", "mu", "PX pole - expected", "PX finite", "LT finite"}}]
]


resultsDirRG$ = FileNameJoin[{srcDirRG$, "results"}];
Quiet[CreateDirectory[resultsDirRG$]];
strRG$[x_] := ToString[CForm[N[x]]];
Export[FileNameJoin[{resultsDirRG$, "rg_feyncalc_onepi.csv"}],
  StringRiffle[Prepend[StringRiffle[Join[{#[[1]], strRG$[#[[2]]], strRG$[#[[3]]], strRG$[#[[4]]]},
        Flatten[{strRG$[Re[#]], strRG$[Im[#]]} & /@ #[[5 ;; 8]]]], ","] & /@ rowsOneRG$,
     "func,arg,xi,mu,re_pole_px,im_pole_px,re_fin_px,im_fin_px,re_pole_lt,im_pole_lt,re_fin_lt,im_fin_lt"], "\n"] <> "\n", "Text"];
Print["(c) wrote results/rg_feyncalc_onepi.csv"];


(* ::Section:: *)
(*(d) K W of (A) and (B) at mu = 1/2, 1, 2 (LoopTools)*)


(* ::Text:: *)
(*As scat_eval.wl (c) and (b), Feynman gauge, SU(3): each TID amplitude is evaluated with LoopTools at mudim = mu^2 and*)
(*converted to MS-bar ((2 Pi)^(2 eps) e^(-eps (ln 4 Pi - gamma_E)), so that K x (value) is K W); the counterterms are the pure*)
(*poles of Eq. (ct) (n_f = 6) times the D-dimensional tree pieces, the residues R_u - 1 = xi C_F/eps, R_t - 1, R_G - 1 =*)
(*Pi_t(0) - delta_3 and the on-shell mass counterterm with LoopTools' A0, B1, DB0, DB1 at the same mu (m = 1).*)


workDirRG$ = FileNameJoin[{srcDirRG$, "work", "scat"}];
ep = Epsilon; Dd = 4 - 2 ep;
lmsRG$ = Log[4 Pi] - EulerGamma;
msLTRG$[x_, mu2_] := Normal[Series[(2 Pi)^(2 ep) Exp[-ep lmsRG$] LToolsEvaluate[x, LToolsFullResult -> True, LToolsSetMudim -> mu2], {ep, 0, 0}]];
su3RG$[x_] := x /. CF -> (CA^2 - 1)/(2 CA) /. CA -> 3 /. xi -> 1 /. gS -> 1;
coefsRG$[x_] := Table[Coefficient[x, ep, k], {k, -2, 0}];
wMuRG$[key_, muv_] := Module[{n1 = If[key === "A", 15, 46], tid, born, cc, w0, wm, a0, b1, db0, db1, rT, rU, rG, d1F, d2, d3, d1, dmOS,
    toD, bornD, wCT, xiv = 1, cf = 4/3, ca = 3, tf = 1/2, nfv = 6, mu2 = N[muv^2], loops},
   tid = Table[Get[FileNameJoin[{workDirRG$, key, "tid_" <> ToString[i] <> ".m"}]], {i, n1}];
   {born, cc, w0, wm} = su3RG$[Get[FileNameJoin[{workDirRG$, key, "tree.m"}]]];
   loops = Total[Expand[msLTRG$[su3RG$[#] /. D -> Dd, mu2]] & /@ tid];
   a0 = msLTRG$[A0[1], mu2]; b1 = msLTRG$[PaVe[1, {1}, {1, 0}], mu2]; db0 = msLTRG$[DB0[1, 1, 0], mu2]; db1 = msLTRG$[DB1[1, 1, 0], mu2];
   rT = cf (xiv (Dd - 2) b1 + 2 (xiv (Dd - 2) db1 + (Dd - 1 + xiv) db0)) + xiv cf/ep;
   rU = xiv cf/ep;
   d1F = -(xiv cf + (3 + xiv) ca/4); d2 = -xiv cf; d3 = ca (13/6 - xiv/2) - 4/3 tf nfv; d1 = ca (17/12 - 3 xiv/4) - 4/3 tf nfv;
   rG = -(2/3) tf (Dd - 2) a0 - d3/ep;
   dmOS = -cf (Dd - 1) (Dd - 2) a0/(2 (Dd - 3));
   toD[x_] := x /. D -> Dd;
   bornD = toD[born];
   wCT = If[key === "A",
     ((2 d1F - d3)/ep + rU + rT) bornD/KK,
     ((2 d1F - d2)/ep toD[w0["t"] + w0["u"]] + (d1 + d1F - d3)/ep toD[w0["s"]] + dmOS toD[wm] + (rG + rT) bornD)/KK];
   {N[born /. D -> 4], N[KK coefsRG$[Expand[loops + Normal[Series[wCT, {ep, 0, 0}]]]]]}];
rowsWRG$ = Flatten[Table[Module[{v = wMuRG$[key, muv]}, {key, muv, v[[1]], Sequence @@ v[[2]]}], {key, {"A", "B"}}, {muv, musRG$}], 1];
Do[Print["(d) (", r[[1]], ") mu = ", r[[2]], ":  K W = ", Chop[r[[4 ;; 6]], 10^-10], "  (1/eps^2, 1/eps, finite);  K Born(4) = ", r[[3]]], {r, rowsWRG$}];


(* ::Subsubsection:: *)
(*Inspect: K W at the three scales*)


If[$Notebooks,
  TableForm[rowsWRG$, TableHeadings -> {None, {"process", "mu", "K B(4)", "1/eps^2", "1/eps", "finite"}}]
]


Export[FileNameJoin[{resultsDirRG$, "rg_feyncalc.csv"}],
  StringRiffle[Prepend[StringRiffle[{#[[1]], strRG$[#[[2]]], strRG$[#[[3]]], strRG$[Re[#[[4]]]], strRG$[Im[#[[4]]]],
        strRG$[Re[#[[5]]]], strRG$[Im[#[[5]]]], strRG$[Re[#[[6]]]], strRG$[Im[#[[6]]]]}, ","] & /@ rowsWRG$,
     "process,mu,born4,re_m2,im_m2,re_m1,im_m1,re_fin,im_fin"], "\n"] <> "\n", "Text"];
Print["(d) wrote ", Length[rowsWRG$], " rows to results/rg_feyncalc.csv (K W at g = 1, LoopTools)"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirRG$, DeleteContents -> True];
