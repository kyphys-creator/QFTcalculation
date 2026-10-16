(* ::Package:: *)

(* ::Title:: *)
(*Step (3): one-loop tadpole and self-energies in a general R_xi gauge with FeynArts + FeynCalc (SM, MS-bar, FJ tadpoles)*)


(* ::Text:: *)
(*Research note models/sm, step (3).  Uses the FeynArts model of this note (Src/generated/SM_FA, propagators with*)
(*GaugeXi[A], GaugeXi[Z], GaugeXi[W] and the ghost-scalar couplings with the same symbols), at particle level.*)
(*  (a) the tadpole T (iT = sum of the 17 one-point diagrams) in D dimensions against Eq. (T);*)
(*  (b) the 1PI self-energies Sigma_T^WW, Sigma_T^ZZ, Sigma_T^AA, Sigma_T^AZ, Sigma^H and the top Sigma^{L,R,S} (with*)
(*      QCD; Sigma^V = (Sigma^L + Sigma^R)/2 and Sigma^S), plus the diagrams with a tadpole attached through a*)
(*      zero-momentum H line (FJ);*)
(*  (c) the UV pole of Sigma(M^2) + tadpole part for W, Z, H, t against (1/2) dM^2/dln mu of Eqs. (vrun), (dM2) with*)
(*      xiA, xiZ, xiW independent; Sigma_T^AA(0) = 0;*)
(*  (d) the MS-bar finite parts are written to results/oneloop_sigma.m for oneloop_numeric.wl.*)
(*Conventions (note Eq. (Gamma2)): the product of Feynman rules is -i g_{mu nu} Sigma_T + ... (vectors), i Sigma^H*)
(*(Higgs), i [pslash P_L Sigma^L + pslash P_R Sigma^R + m Sigma^S] (fermions) and i T (tadpole).  FeynArts'*)
(*CreateFeynAmp returns that product divided by i (the amplitude M, not i M): the sum of the tadpole diagrams equals*)
(*T.  FCFAConvert supplies 1/(2 pi)^4 and TID i pi^2 times the LoopTools-normalized A0, B0, so K Sigma (K = 16 pi^2)*)
(*is a combination of A0, B0 and rational terms.*)
(*CreateFeynAmp[..., GaugeRules -> {}] keeps GaugeXi: the FeynArts default {_GaugeXi -> 1} is Feynman gauge.*)
(*Photon IR regulator: the photon and its ghost get the mass MA in a copy of the model (only to separate UV from IR in*)
(*the off-shell (1 - xiA) q q/q^4 terms, environment Table 11); MA -> 0 after the UV pole is taken.*)
(*Tadpole-attached diagrams: FeynArts also inserts Z and photon lines between the tadpole loop and the two-point*)
(*vertex; their one-point loops vanish by Lorentz invariance (the photon line is 1/0), so only the H line is kept, and*)
(*the Z-line diagrams are checked to vanish.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_feyncalc.wl  (about 15 minutes).  Interactive:  ~/hep/bin/wopen oneloop_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;


srcDirOL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirOL$ = FileNameJoin[{srcDirOL$, "results"}];
Quiet[CreateDirectory[resDirOL$]];
modelTmpDirOL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOL$, "generated", "SM_FA"}], FileNameJoin[{modelTmpDirOL$, "SM_FA"}]];
(* photon IR regulator: Mass -> MA for V[1] and U[1] in the copy of the model *)
modFileOL$ = FileNameJoin[{modelTmpDirOL$, "SM_FA", "SM_FA.mod"}];
modTextOL$ = Import[modFileOL$, "Text"];
modTextOL$ = StringReplace[modTextOL$, {
    RegularExpression["(?s)(V\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA",
    RegularExpression["(?s)(U\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA"}];
Export[modFileOL$, modTextOL$, "Text"];
Print["photon and photon-ghost masses in the model copy (expect {MA, MA}): ",
  StringCases[modTextOL$, RegularExpression["(?s)(?:V|U)\\[1\\] == \\{.*?Mass -> (\\w+)"] -> "$1"]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOL$, "SM_FA"}], Quiet -> True];
modelFileOL$ = FileNameJoin[{modelTmpDirOL$, "SM_FA", "SM_FA"}];


(* ::Text:: *)
(*Conversion of the FeynCalc output (as in tree_feyncalc.wl) and of the colour sums: a SumOver of an index that no*)
(*longer appears (closed quark loop) is the number of colours (FCFAConvert would drop it); otherwise the index is*)
(*summed implicitly by SUNSimplify.*)


massOL$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me, FCGV["MA"] -> MA};
lepMOL$ = {Me, MMU, MTA}; upMOL$ = {MU, MC, MT}; dnMOL$ = {MD, MS, MB};
yukOL$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMOL$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMOL$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMOL$[[i]]/vev, 0]};
convOL$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG,
    GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
    GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1},
   massOL$];
sumOverOL$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];

insertOL$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles},
    Model -> modelFileOL$, GenericModel -> modelFileOL$], RuleDelayed::rhs];
convertOL$[fa_, in_, out_] := Module[{a},
   a = Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out,
       LoopMomenta -> {q}, LorentzIndexNames -> {mu, nu}, ChangeDimension -> D, List -> True, SMP -> False,
       UndoChiralSplittings -> True, DropSumOver -> False], RuleDelayed::rhs];
   (* the zero-momentum H propagator of the tadpole-attached diagrams is the number 1/(0 - MH^2): left inside
      the loop expressions it makes FCLoopSplit fail *)
   a = (sumOverOL$ /@ a) /. convOL$ /. yukOL$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee /.
     FeynAmpDenominator[PropagatorDenominator[0 | Momentum[0, ___], m_]] :> -1/m^2;
   (* chirality projectors as (1 -+ gamma5)/2: a bare (P_L + P_R) outside a Dirac chain is not reduced to 1 *)
   a = a /. {DiracGamma[6] -> 1/2 + DiracGamma[5]/2, DiracGamma[7] -> 1/2 - DiracGamma[5]/2};
   a];

(* tadpole-attached two-point diagrams: keep the zero-momentum H line, return also the other ones *)
tadSplitOL$[fa_] := Module[{l = List @@ fa},
   {Select[l, ! FreeQ[#, FAPropagatorDenominator[0, FCGV["MH"] | MH]] &],
    Select[l, FreeQ[#, FAPropagatorDenominator[0, FCGV["MH"] | MH]] &]}];

(* reduction to A0, B0 with D kept; FDS first (repeated denominators, QCD note step (3)) *)
reduceOL$[x_] := Module[{r},
   r = FDS[x, q];
   r = TID[DiracSimplify[SUNSimplify[r]], q, ToPaVe -> True];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]};
   r = Simplify[r /. {B0[0, 0, 0] -> 0, A0[0] -> 0}];
   r];

(* i pi^2 (from TID) times 1/(16 pi^4) (from FCFAConvert) = i/K *)
KK = (4 Pi)^2;
uvOL$[x_] := Simplify[SeriesCoefficient[x /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep} /. D -> 4 - 2 ep, {ep, 0, -1}]];


(* ::Section:: *)
(*(a) Tadpole*)


diagsT$ = insertOL$[CreateTopologies[1, 1 -> 0], {S[1]} -> {}];
ampsT$ = convertOL$[CreateFeynAmp[diagsT$, GaugeRules -> {}], {}, {}];
Print["(a) tadpole diagrams (expect 17): ", Length[ampsT$]];
(* the FeynArts sum of diagrams is T (the Feynman rules give i T); tOL$ = K T *)
tOL$ = Simplify[KK reduceOL$[Total[ampsT$]] /. MA -> 0];
vevOL$ = 2 MW sw/ee;
a0$[m_] := A0[m^2];
tNote$ = 1/(KK vevOL$) (2 MW^2 (D - 1) a0$[MW] + MZ^2 (D - 1) a0$[MZ] + 3/2 MH^2 a0$[MH] +
     MH^2/2 (a0$[Sqrt[xiZ] MZ] + 2 a0$[Sqrt[xiW] MW]) -
     4 (Me^2 a0$[Me] + MMU^2 a0$[MMU] + MTA^2 a0$[MTA] + 3 Sum[m^2 a0$[m], {m, {MU, MC, MT, MD, MS, MB}}])) /.
   {A0[MZ^2 xiZ] -> A0[xiZ MZ^2], A0[MW^2 xiW] -> A0[xiW MW^2]};
dT$ = Simplify[(tOL$ - KK tNote$ /. MZ -> MW/cw) /. cw -> Sqrt[1 - sw^2]];
Print["(a) T(FeynCalc) - Eq. (T), exact in D (expect 0): ", dT$];


(* ::Section:: *)
(*(b) Self-energies*)


topsOPI$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];
topsTad$ = Complement[CreateTopologies[1, 1 -> 1], topsOPI$];

selfEnergy$[proc_, mom_, kind_] := Module[{d1, a1, dT, faT, keep, drop, aT, aDrop, tot, proj},
   d1 = insertOL$[topsOPI$, proc];
   a1 = convertOL$[CreateFeynAmp[d1, Truncated -> True, GaugeRules -> {}], {mom}, {mom}];
   dT = insertOL$[topsTad$, proc];
   faT = Quiet[CreateFeynAmp[dT, Truncated -> True, GaugeRules -> {}], RuleDelayed::rhs];
   {keep, drop} = tadSplitOL$[faT];
   aT = If[keep === {}, {0}, convertOL$[faT[[0]] @@ keep, {mom}, {mom}]];
   Print["   ", proc, ": 1PI diagrams ", Length[a1], ", tadpole-attached with the H line ", Length[keep],
     ", with a Z or photon line (dropped) ", Length[drop]];
   proj = Switch[kind,
     "V", -1/(D - 1) (MTD[mu, nu] - FVD[mom, mu] FVD[mom, nu]/SPD[mom, mom]),
     "S", 1,
     _, 1];
   (* project and reduce diagram by diagram *)
   tot = {a1, aT};
   If[kind === "V", tot = Map[Contract[proj #] &, tot, {2}], If[kind === "S", tot = proj tot]];
   tot = Simplify[Total[reduceOL$ /@ #]] & /@ tot;
   (* K Sigma *)
   KK tot];

(* fermion self-energy: the FeynArts sum is pslash P_L SL + pslash P_R SR + m SS; the pole mass needs only
   SigmaV = (SL + SR)/2 = tr[pslash Sigma]/(4 p^2) and SigmaS = tr[Sigma]/(4 m) (no gamma5 in the traces) *)
selfEnergyF$[proc_, mom_, m_] := Module[{d1, a1, dT, faT, keep, drop, aT, ext},
   d1 = insertOL$[topsOPI$, proc];
   a1 = convertOL$[CreateFeynAmp[d1, Truncated -> True, GaugeRules -> {}], {mom}, {mom}];
   dT = insertOL$[topsTad$, proc];
   faT = Quiet[CreateFeynAmp[dT, Truncated -> True, GaugeRules -> {}], RuleDelayed::rhs];
   {keep, drop} = tadSplitOL$[faT];
   aT = If[keep === {}, {0}, convertOL$[faT[[0]] @@ keep, {mom}, {mom}]];
   Print["   ", proc, ": 1PI diagrams ", Length[a1], ", tadpole-attached with the H line ", Length[keep],
     ", dropped ", Length[drop]];
   (* colour matrices sit inside the Dirac chain of the gluon diagram: DotSimplify pulls them out first *)
   ext[x_] := Module[{y = SUNSimplify[DotSimplify[x], SUNNToCACF -> True] /. SUNFDelta[__] -> 1, tr},
     tr[z_] := DiracTrace[DiracSimplify[FCI[z]], DiracTraceEvaluate -> True];
     {tr[GSD[mom] . y]/(4 SPD[mom, mom]), tr[y]/(4 m)}];
   (* K Sigma^{L,R,S}, diagram by diagram *)
   KK {Simplify[Total[reduceOL$ /@ #]] & /@ Transpose[ext /@ a1], Simplify[Total[reduceOL$ /@ #]] & /@ Transpose[ext /@ aT]}];

FCClearScalarProducts[];
Print["(b) W self-energy"];
sigWW$ = selfEnergy$[{V[3]} -> {V[3]}, k, "V"];
Print["(b) Z self-energy"];
sigZZ$ = selfEnergy$[{V[2]} -> {V[2]}, k, "V"];
Print["(b) photon self-energy"];
sigAA$ = selfEnergy$[{V[1]} -> {V[1]}, k, "V"];
Print["(b) photon-Z mixing"];
sigAZ$ = selfEnergy$[{V[1]} -> {V[2]}, k, "V"];
Print["(b) Higgs self-energy"];
sigHH$ = selfEnergy$[{S[1]} -> {S[1]}, k, "S"];
Print["(b) top self-energy"];
sigTT$ = selfEnergyF$[{F[3, {3}]} -> {F[3, {3}]}, k, MT];


(* ::Section:: *)
(*(c) UV poles at k^2 = M^2 against (1/2) dM^2/dln mu*)


(* MS-bar beta functions of the note (Eq. (beta)) in terms of the masses *)
gSq$ = ee^2/sw^2; gpSq$ = ee^2/(1 - sw^2); lamOL$ = MH^2/(2 vevOL$^2);
yOL$[m_] := Sqrt[2] m/vevOL$;
yuks$ = {{MU, MD}, {MC, MS}, {MT, MB}};
TT$ = Sum[3 yOL$[p[[1]]]^2 + 3 yOL$[p[[2]]]^2, {p, yuks$}] + Sum[yOL$[m]^2, {m, lepMOL$}];
NY4$ = Sum[3 yOL$[p[[1]]]^4 + 3 yOL$[p[[2]]]^4, {p, yuks$}] + Sum[yOL$[m]^4, {m, lepMOL$}];
dlnv2$ = (-12 lamOL$ - 2 TT$ + 9/2 gSq$ + 3/2 gpSq$ + 2/lamOL$ NY4$ - 3/(8 lamOL$) (2 gSq$^2 + (gSq$ + gpSq$)^2))/KK;
dlnMW2$ = dlnv2$ - 19/3 gSq$/KK;
dlnMZ2$ = dlnv2$ + 2 (-19/6 gSq$^2 + 41/6 gpSq$^2)/((gSq$ + gpSq$) KK);
dlnMH2$ = (12 lamOL$ + 2 TT$ - 9/2 gSq$ - 3/2 gpSq$)/KK;
dlnmt2$ = dlnv2$ + 2 (3/2 (yOL$[MT]^2 - yOL$[MB]^2) + TT$ - 8 gS^2 - 9/4 gSq$ - 17/12 gpSq$)/KK;

onshellOL$[x_, m2_] := x /. {SPD[k, k] -> m2, Pair[Momentum[k, D], Momentum[k, D]] -> m2} /.
   {B0[kk_, a_, b_] :> B0[kk /. SPD[k, k] -> m2, a, b]};
cleanOL$[x_] := Simplify[x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2], 0 < sw < 1 && MW > 0];
reportUV$[label_, sig_, m2_, pred_] := Module[{uv1, uvT, d},
   (* the photon regulator is removed after the pole is taken (terms like A0[MA^2]/MA^2) *)
   uv1 = Simplify[uvOL$[onshellOL$[sig[[1]], m2]]] /. MA -> 0;
   uvT = Simplify[uvOL$[onshellOL$[sig[[2]], m2]]] /. MA -> 0;
   d = cleanOL$[uv1 + uvT - pred];
   Print["(c) ", label, ": UV pole of Sigma(M^2) + tadpole part - (1/2) dM^2/dln mu = ", d,
     "   (expect 0);  xi dependence of the 1PI part alone: ",
     cleanOL$[{D[uv1, xiA], D[uv1, xiZ], D[uv1, xiW]}] =!= {0, 0, 0}];
   d];
(* all quantities are K Sigma, so the predictions are K (1/2) dM^2/dln mu *)
resUV$ = {
   reportUV$["W", sigWW$, MW^2, KK MW^2 dlnMW2$/2 /. MZ -> MW/cw],
   reportUV$["Z", sigZZ$, MZ^2, KK MZ^2 dlnMZ2$/2 /. MZ -> MW/cw],
   reportUV$["H", sigHH$, MH^2, KK MH^2 dlnMH2$/2]};

(* top: m_p = m_0 - m (SigmaV + SigmaS), SigmaV = (SL + SR)/2, m_0 = m + dm with dm/m = (Delta/2) dln m/dln mu, so the
   UV pole of SigmaV + SigmaS must be (1/4) dln m^2/dln mu *)
uvTop$ = Module[{s1 = onshellOL$[#, MT^2] & /@ sigTT$[[1]], sT = onshellOL$[#, MT^2] & /@ sigTT$[[2]], tot},
   tot = s1[[1]] + s1[[2]] + sT[[1]] + sT[[2]] /. {CF -> 4/3, CA -> 3};
   cleanOL$[(Simplify[uvOL$[tot]] /. MA -> 0) - KK dlnmt2$/4]];
Print["(c) top: UV pole of SigmaV + SigmaS (with tadpole) - (1/4) dln m_t^2/dln mu = ", uvTop$, "   (expect 0)"];
uvAA$ = Simplify[uvOL$[onshellOL$[sigAA$[[1]], kk2]]] /. MA -> 0;
Print["(c) UV pole of Sigma_T^AA(k^2) (expect a multiple of k^2): ", Factor[uvAA$], ";  at k^2 = 0: ",
  Simplify[uvAA$ /. kk2 -> 0]];


(* ::Section:: *)
(*(d) Output for the finite parts*)


Put[{"T" -> tOL$, "WW" -> sigWW$, "ZZ" -> sigZZ$, "AA" -> sigAA$, "AZ" -> sigAZ$, "HH" -> sigHH$, "TT" -> sigTT$},
  FileNameJoin[{resDirOL$, "oneloop_sigma.m"}]];
Print["Summary (expect all 0): tadpole ", dT$, ", UV poles W, Z, H ", resUV$, ", top ", uvTop$];
