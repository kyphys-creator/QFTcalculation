(* ::Package:: *)

(* ::Title:: *)
(*Step (3) of the CKM note: the quark self-energy matrices and the W self-energy in a general R_xi gauge (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm_ckm, step (3).  Uses the FeynArts model of this note (Src/generated/SM_CKM_FA) at particle*)
(*level, with the photon IR regulator MA of the SM note (a copy of the model with Mass -> MA for V[1] and U[1]).*)
(*  (a) the quark self-energies as 3 x 3 generation matrices, Gamma_ij > i [pslash P_L SL_ij + pslash P_R SR_ij*)
(*      + m_i P_L SSL_ij + m_j P_R SSR_ij] (q_j in, q_i out; note Eq. (Gammaq) has SSL = SSR = SS), 1PI and with the*)
(*      tadpole attached (FJ), for the down-type and the up-type quarks (18 entries);*)
(*  (b) checks: SSL = SSR for every entry (Denner's form); the off-diagonal UV poles against Eq. (uvoff) and their xi*)
(*      independence (with the explicit standard parametrization, i.e. unitarity); the diagonal UV pole of*)
(*      SigmaV + SigmaS (with the tadpole) at p^2 = m_i^2 against (1/4) dln m_i^2/dln mu of Eq. (yrun); V = 1*)
(*      against the SM note's top self-energy (models/sm/Src/results/oneloop_sigma.m);*)
(*  (c) the W self-energy Sigma_T^WW (1PI and tadpole part) with the CKM matrix: its UV pole at k^2 = MW^2 equals the*)
(*      one with V = 1 (unitarity);*)
(*  (d) results/oneloop_ckm_sigma.m for oneloop_ckm_numeric.wl (K Sigma, K = 16 pi^2, in A0, B0 with D kept).*)
(*V_ij = vR[i, j] + I vI[i, j] with real symbols (step (2)); the G+- couplings are summed over the dummy generation*)
(*(DropIndexSum -> False, step (2)).  The Dirac structure is read off after TID and DiracSimplify, where every term*)
(*is GSD[k].GA[7] (pslash P_L), GSD[k].GA[6], GA[7] (P_L) or GA[6] (P_R) times a scalar: no gamma5 traces.*)
(*Conventions of the SM note (step (3)): the FeynArts amplitude is the product of Feynman rules divided by i, and*)
(*FCFAConvert and TID together give 1/K times A0, B0, so K times the coefficient is K Sigma.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_ckm_feyncalc.wl  (about 10 minutes).  Interactive:  ~/hep/bin/wopen oneloop_ckm_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;


srcDirOC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirOC$ = FileNameJoin[{srcDirOC$, "results"}];
Quiet[CreateDirectory[resDirOC$]];
modelTmpDirOC$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOC$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpDirOC$, "SM_CKM_FA"}]];
modFileOC$ = FileNameJoin[{modelTmpDirOC$, "SM_CKM_FA", "SM_CKM_FA.mod"}];
modTextOC$ = Import[modFileOC$, "Text"];
modTextOC$ = StringReplace[modTextOC$, {
    RegularExpression["(?s)(V\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA",
    RegularExpression["(?s)(U\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA"}];
Export[modFileOC$, modTextOC$, "Text"];
Print["photon and photon-ghost masses in the model copy (expect {MA, MA}): ",
  StringCases[modTextOC$, RegularExpression["(?s)(?:V|U)\\[1\\] == \\{.*?Mass -> (\\w+)"] -> "$1"]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOC$, "SM_CKM_FA"}], Quiet -> True];
modelFileOC$ = FileNameJoin[{modelTmpDirOC$, "SM_CKM_FA", "SM_CKM_FA"}];


massOC$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me, FCGV["MA"] -> MA};
lepMOC$ = {Me, MMU, MTA}; upMOC$ = {MU, MC, MT}; dnMOC$ = {MD, MS, MB};
yukOC$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMOC$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMOC$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMOC$[[i]]/vev, 0]};
ckmOC$ = {Conjugate[CKM[i_Integer, j_Integer]] :> vR[i, j] - I vI[i, j], CKM[i_Integer, j_Integer] :> vR[i, j] + I vI[i, j]};
convOC$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG,
    GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
    GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1},
   massOC$];
(* a SumOver of an index that no longer appears (closed quark loop) is the number of colours *)
sumOverOC$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];

insertOC$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles},
    Model -> modelFileOC$, GenericModel -> modelFileOC$], RuleDelayed::rhs];
convertOC$[fa_, in_, out_] := Module[{a},
   a = Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out,
       LoopMomenta -> {q}, LorentzIndexNames -> {mu, nu}, ChangeDimension -> D, List -> True, SMP -> False,
       UndoChiralSplittings -> True, DropSumOver -> False, DropIndexSum -> False], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a = (sumOverOC$ /@ a) /. convOC$ /. yukOC$ /. ckmOC$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee /.
     FeynAmpDenominator[PropagatorDenominator[0 | Momentum[0, ___], m_]] :> -1/m^2;
   If[! FreeQ[a, CKM | IndexSum], Print["   WARNING: CKM or IndexSum left: ", Union[Cases[a, _CKM | _IndexSum, Infinity]]]];
   a];
tadSplitOC$[fa_] := Module[{l = List @@ fa},
   {Select[l, ! FreeQ[#, FAPropagatorDenominator[0, FCGV["MH"] | MH]] &],
    Select[l, FreeQ[#, FAPropagatorDenominator[0, FCGV["MH"] | MH]] &]}];
KK = (4 Pi)^2;
(* the colour matrices of the gluon loop sit inside the Dirac chain: DotSimplify pulls them out (SM note) *)
reduceOC$[x_] := Module[{r},
   r = FDS[x, q];
   r = TID[DiracSimplify[SUNSimplify[DotSimplify[r], SUNNToCACF -> True] /. SUNFDelta[__] -> 1], q, ToPaVe -> True];
   r = DiracSimplify[r];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]};
   r /. {B0[0, 0, 0] -> 0, A0[0] -> 0}];
(* K times the coefficients of pslash P_L, pslash P_R, P_L, P_R; a bare pslash is pslash (P_L + P_R), gamma5 is
   P_R - P_L, and a term without Dirac matrices is (P_L + P_R) times it *)
chiralOC$[r_] := Module[{x, x0, c},
   x = Expand[FCE[r] /. {GSD[k] . GA[7] -> pLs$, GSD[k] . GA[6] -> pRs$, GSD[k] . GA[5] -> pRs$ - pLs$,
         GA[7] -> pL$, GA[6] -> pR$, GA[5] -> pR$ - pL$} /. GSD[k] -> pLs$ + pRs$];
   If[! FreeQ[x, GA | GSD | DiracGamma | Dot],
     Print["   WARNING: unexpected Dirac structure: ", Union[Cases[x, _GA | _GSD | _Dot | _DiracGamma, Infinity]]]];
   x0 = x /. {pLs$ -> 0, pRs$ -> 0, pL$ -> 0, pR$ -> 0};
   c = (Coefficient[x, #] & /@ {pLs$, pRs$, pL$, pR$}) + {0, 0, x0, x0};
   If[Simplify[x - (c - {0, 0, x0, x0}) . {pLs$, pRs$, pL$, pR$} - x0] =!= 0, Print["   WARNING: terms outside the four structures"]];
   KK c];

topsOPI$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];
topsTad$ = Complement[CreateTopologies[1, 1 -> 1], topsOPI$];

(* quark self-energy: q_j(k) in, q_i(k) out.  Returns {1PI, tadpole-attached}, each {K SL, K SR, K SSL, K SSR} with
   SSL = (coefficient of P_L)/m_i and SSR = (coefficient of P_R)/m_j *)
seQOC$[cls_, i_, j_] := Module[{ms = If[cls === 3, upMOC$, dnMOC$], d1, a1, dT, faT, keep, drop, aT, c1, cT, fix},
   d1 = insertOC$[topsOPI$, {F[cls, {j}]} -> {F[cls, {i}]}];
   a1 = convertOC$[CreateFeynAmp[d1, Truncated -> True, GaugeRules -> {}], {k}, {k}];
   dT = insertOC$[topsTad$, {F[cls, {j}]} -> {F[cls, {i}]}];
   faT = Quiet[CreateFeynAmp[dT, Truncated -> True, GaugeRules -> {}], RuleDelayed::rhs];
   {keep, drop} = tadSplitOC$[faT];
   aT = If[keep === {}, {0}, convertOC$[faT[[0]] @@ keep, {k}, {k}]];
   c1 = chiralOC$[reduceOC$[Total[a1]]];
   cT = If[aT === {0}, {0, 0, 0, 0}, chiralOC$[reduceOC$[Total[aT]]]];
   fix[c_] := Simplify[{c[[1]], c[[2]], c[[3]]/ms[[i]], c[[4]]/ms[[j]]}];
   Print["   ", {"", "", "u", "d"}[[cls]], "-type ", {i, j}, ": 1PI diagrams ", Length[a1], ", tadpole-attached (H line) ",
     Length[keep], ", dropped ", Length[drop]];
   {fix[c1], fix[cT]}];


(* ::Subsubsection:: *)
(*Inspect: the diagrams of one off-diagonal entry (Fig. seckm: s <- b)*)


If[$Notebooks, Show /@ Render[Paint[insertOC$[topsOPI$, {F[4, {3}]} -> {F[4, {2}]}], DisplayFunction -> Identity]]]


(* ::Section:: *)
(*(a) Quark self-energy matrices*)


FCClearScalarProducts[];
Print["(a) down-type quarks"];
sigD$ = Table[seQOC$[4, i, j], {i, 3}, {j, 3}];
Print["(a) up-type quarks"];
sigU$ = Table[seQOC$[3, i, j], {i, 3}, {j, 3}];


(* ::Section:: *)
(*(b) Checks of the quark self-energies*)


kRuleOC$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
uvOC$[x_] := Simplify[SeriesCoefficient[(x /. kRuleOC$) /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep} /. D -> 4 - 2 ep,
     {ep, 0, -1}] /. MA -> 0];
cwOC$ = Sqrt[1 - sw^2];
cleanOC$ = {MZ -> MW/cwOC$, cw -> cwOC$};

(* Denner's form: the P_L and P_R scalar parts have one function (exact, before unitarity) *)
dennerOC$ = Union[Flatten[Table[Simplify[(s[[i, j, n, 3]] - s[[i, j, n, 4]]) /. cleanOC$], {s, {sigD$, sigU$}}, {i, 3}, {j, 3}, {n, 2}]]];
Print["(b) SSL - SSR for all 36 entries (1PI and tadpole parts; expect {0}): ", dennerOC$];

(* explicit standard parametrization (real angles) *)
vStdOC$ = {
   {c12 c13, s12 c13, s13 Exp[-I dl]},
   {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
   {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}} /.
   {c12 -> Sqrt[1 - s12^2], c23 -> Sqrt[1 - s23^2], c13 -> Sqrt[1 - s13^2]};
explicitOC$ = {vR[i_, j_] :> ComplexExpand[Re[vStdOC$[[i, j]]]], vI[i_, j_] :> ComplexExpand[Im[vStdOC$[[i, j]]]]};
unitOC$ = {vR[i_, j_] :> If[i == j, 1, 0], vI[__] -> 0};
assOC$ = 0 < s12 < 1 && 0 < s23 < 1 && 0 < s13 < 1 && Element[dl, Reals] && 0 < sw < 1 && MW > 0;
simpVOC$[x_] := Simplify[ComplexExpand[x /. explicitOC$ /. cleanOC$], assOC$];

vevOC$ = 2 MW sw/ee;
yOC$[m_] := Sqrt[2] m/vevOC$;
vmatOC$ = Array[vR[#1, #2] + I vI[#1, #2] &, {3, 3}];
duOC$ = DiagonalMatrix[yOC$ /@ upMOC$]^2; ddOC$ = DiagonalMatrix[yOC$ /@ dnMOC$]^2;
(* X of Eq. (uvoff): V^dagger D_u V (down-type), V D_d V^dagger (up-type); conjugate as vR - I vI *)
conjOC$[m_] := m /. {vI[a_, b_] :> -vI[a, b]};
xDOC$ = Transpose[conjOC$[vmatOC$]] . duOC$ . vmatOC$;
xUOC$ = vmatOC$ . ddOC$ . Transpose[conjOC$[vmatOC$]];

offRowsOC$ = Flatten[Table[If[i == j, Nothing, Module[{sig = s[[1]][[i, j, 1]], x = s[[2]][[i, j]], uv, uvx, raw},
      raw = uvOC$[sig[[1]]];
      uv = simpVOC$[uvOC$[#]] & /@ sig;
      uvx = simpVOC$[x];
      {s[[3]], {i, j}, ! FreeQ[raw, xiW | xiZ | xiA | xiG],
       Simplify[{uv[[1]] - uvx/2, uv[[2]], uv[[3]] + uvx, uv[[4]] + uvx}, assOC$], ! FreeQ[uv, xiW | xiZ | xiA | xiG]}]],
     {s, {{sigD$, xDOC$, "d"}, {sigU$, xUOC$, "u"}}}, {i, 3}, {j, 3}], 2];
Print["(b) off-diagonal UV poles, 12 entries: K SL - X/2, K SR, K SSL + X, K SSR + X with the explicit V (expect all 0): ",
  Union[Flatten[offRowsOC$[[All, 4]]]]];
Print["(b) xi in the off-diagonal UV pole of SL before unitarity (expect True), after (expect False): ",
  Union[offRowsOC$[[All, 3]]], ", ", Union[offRowsOC$[[All, 5]]]];

(* diagonal: SigmaV + SigmaS (with the tadpole) at p^2 = m_i^2, UV pole against (1/4) K dln m_i^2/dln mu, Eq. (yrun) *)
gSqOC$ = ee^2/sw^2; gpSqOC$ = ee^2/(1 - sw^2); lamOC$ = MH^2/(2 vevOC$^2);
TTOC$ = Sum[3 yOC$[m]^2, {m, Join[upMOC$, dnMOC$]}] + Sum[yOC$[m]^2, {m, lepMOC$}];
NY4OC$ = Sum[3 yOC$[m]^4, {m, Join[upMOC$, dnMOC$]}] + Sum[yOC$[m]^4, {m, lepMOC$}];
dlnv2OC$ = -12 lamOC$ - 2 TTOC$ + 9/2 gSqOC$ + 3/2 gpSqOC$ + 2/lamOC$ NY4OC$ - 3/(8 lamOC$) (2 gSqOC$^2 + (gSqOC$ + gpSqOC$)^2);
abs2OC$[i_, j_] := vR[i, j]^2 + vI[i, j]^2;
(* K dln m^2/dln mu = K dln v^2/dln mu + 2 K beta_y/y *)
kdlnm2OC$[3, i_] := dlnv2OC$ + 2 (3/2 yOC$[upMOC$[[i]]]^2 - 3/2 Sum[abs2OC$[i, k] yOC$[dnMOC$[[k]]]^2, {k, 3}] + TTOC$ -
      8 gS^2 - 9/4 gSqOC$ - 17/12 gpSqOC$);
kdlnm2OC$[4, j_] := dlnv2OC$ + 2 (3/2 yOC$[dnMOC$[[j]]]^2 - 3/2 Sum[abs2OC$[k, j] yOC$[upMOC$[[k]]]^2, {k, 3}] + TTOC$ -
      8 gS^2 - 9/4 gSqOC$ - 5/12 gpSqOC$);
onshellOC$[x_, m2_] := x /. kRuleOC$ /. kk2 -> m2;
diagRowsOC$ = Flatten[Table[Module[{sig = s[[1]][[i, i]], m = s[[2]][[i]], tot},
      tot = Total[Table[(sig[[n, 1]] + sig[[n, 2]])/2 + sig[[n, 3]], {n, 2}]];
      {s[[3]], i, simpVOC$[uvOC$[onshellOC$[tot /. {CF -> 4/3, CA -> 3}, m^2]] - kdlnm2OC$[s[[4]], i]/4]}],
     {s, {{sigU$, upMOC$, "u", 3}, {sigD$, dnMOC$, "d", 4}}}, {i, 3}], 1];
Print["(b) diagonal UV poles of SigmaV + SigmaS (with the tadpole) - (1/4) K dln m^2/dln mu, 6 quarks (expect 0): ",
  Union[diagRowsOC$[[All, 3]]]];

(* V = 1: the top self-energy of the SM note *)
smSigOC$ = Association[Get[FileNameJoin[{ParentDirectory[srcDirOC$], "..", "sm", "Src", "results", "oneloop_sigma.m"}]]];
topV1OC$ = Table[{(sigU$[[3, 3, n, 1]] + sigU$[[3, 3, n, 2]])/2, sigU$[[3, 3, n, 3]]} /. unitOC$, {n, 2}];
dTopOC$ = Simplify[(topV1OC$ - smSigOC$["TT"]) /. {CF -> 4/3, CA -> 3} /. cleanOC$];
Print["(b) top SigmaV, SigmaS (1PI, tadpole) at V = 1 minus the SM note (expect {{0, 0}, {0, 0}}): ", dTopOC$];


(* ::Section:: *)
(*(c) W self-energy with the CKM matrix*)


selfEnergyVOC$[proc_] := Module[{d1, a1, dT, faT, keep, drop, aT, proj, tot},
   d1 = insertOC$[topsOPI$, proc];
   a1 = convertOC$[CreateFeynAmp[d1, Truncated -> True, GaugeRules -> {}], {k}, {k}];
   dT = insertOC$[topsTad$, proc];
   faT = Quiet[CreateFeynAmp[dT, Truncated -> True, GaugeRules -> {}], RuleDelayed::rhs];
   {keep, drop} = tadSplitOC$[faT];
   aT = If[keep === {}, {0}, convertOC$[faT[[0]] @@ keep, {k}, {k}]];
   Print["   ", proc, ": 1PI diagrams ", Length[a1], ", tadpole-attached with the H line ", Length[keep]];
   proj = -1/(D - 1) (MTD[mu, nu] - FVD[k, mu] FVD[k, nu]/SPD[k, k]);
   tot = Map[Contract[proj #] &, {a1, aT}, {2}];
   tot = Simplify[Total[Module[{r = FDS[#, q]},
         r = TID[DiracSimplify[SUNSimplify[r, SUNNToCACF -> True] /. SUNFDelta[__] -> 1], q, ToPaVe -> True];
         r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]};
         r /. {B0[0, 0, 0] -> 0, A0[0] -> 0}] & /@ #]] & /@ tot;
   KK tot];
Print["(c) W self-energy"];
sigWW$ = selfEnergyVOC$[{V[3]} -> {V[3]}];
uvWWOC$ = simpVOC$[uvOC$[onshellOC$[Total[sigWW$], MW^2]]];
uvWWV1OC$ = Simplify[uvOC$[onshellOC$[Total[sigWW$], MW^2]] /. unitOC$ /. cleanOC$];
Print["(c) UV pole of Sigma_T^WW(MW^2) + tadpole part: explicit V minus V = 1 (expect 0): ", Simplify[uvWWOC$ - uvWWV1OC$, assOC$],
  ";  minus the SM note's (expect 0): ",
  Simplify[uvWWV1OC$ - Simplify[uvOC$[onshellOC$[Total[smSigOC$["WW"]], MW^2]] /. cleanOC$], 0 < sw < 1 && MW > 0]];


(* ::Section:: *)
(*(d) Output*)


Put[{"D" -> sigD$, "U" -> sigU$, "WW" -> sigWW$}, FileNameJoin[{resDirOC$, "oneloop_ckm_sigma.m"}]];
Print["Summary (expect {0}, {0}, {0}, {{0, 0}, {0, 0}}): Denner form ", dennerOC$, ", off-diagonal UV ",
  Union[Flatten[offRowsOC$[[All, 4]]]], ", diagonal UV ", Union[diagRowsOC$[[All, 3]]], ", V = 1 top ", dTopOC$];
