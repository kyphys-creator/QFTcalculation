(* ::Package:: *)

(* ::Title:: *)
(*Step (4): Slavnov-Taylor identities of the two-point functions in a general R_xi gauge (SM note)*)


(* ::Text:: *)
(*The BRST invariance of L_gf + L_FP keeps the two-point function of each gauge-fixing function at its tree value*)
(*(<F^+ F^-> = -i xiW, <F^A F^Z> = 0, ...; note Eq. (st)).  At one loop this relates the longitudinal vector*)
(*self-energies, the vector-Goldstone mixings and the Goldstone self-energies, all unrenormalized and with the*)
(*tadpole-attached diagrams.  Same model, conventions and machinery as oneloop_feyncalc.wl (setup copied).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file st_feyncalc.wl  (about 2 minutes).*)


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
(*Two-point functions*)


topsOPI$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];
topsTad$ = Complement[CreateTopologies[1, 1 -> 1], topsOPI$];

(* K times the projected sum of the 1PI and tadpole-attached (H line) diagrams, diagram by diagram *)
twoPoint$[proc_, proj_] := Module[{d1, a1, dT, faT, keep, drop, aT, tot},
   d1 = insertOL$[topsOPI$, proc];
   a1 = convertOL$[CreateFeynAmp[d1, Truncated -> True, GaugeRules -> {}], {k}, {k}];
   dT = insertOL$[topsTad$, proc];
   faT = Quiet[CreateFeynAmp[dT, Truncated -> True, GaugeRules -> {}], RuleDelayed::rhs];
   {keep, drop} = tadSplitOL$[faT];
   aT = If[keep === {}, {0}, convertOL$[faT[[0]] @@ keep, {k}, {k}]];
   Print["   ", proc, ": 1PI ", Length[a1], ", tadpole-attached (H line) ", Length[keep], ", dropped ", Length[drop]];
   tadPartST$[proc] = KK Simplify[Total[reduceOL$[Contract[proj #]] & /@ aT]];
   KK Simplify[Total[reduceOL$[Contract[proj #]] & /@ a1]] + tadPartST$[proc]];

FCClearScalarProducts[];
(* FeynArts amplitude A (Feynman-rule product / i): vectors A_{mu nu} = -g Sigma_T - (k k/k^2)(Sigma_L - Sigma_T),
   so Sigma_L = -k^mu k^nu A_{mu nu}/k^2; vector-scalar A^mu = k^mu a, a = k_mu A^mu/k^2; scalars Sigma = A *)
projL$ = -FVD[k, mu] FVD[k, nu]/SPD[k, k];
(* LorentzIndexNames gives the first name (mu) to the only vector leg, incoming or outgoing *)
projM$[ix_] := FVD[k, ix]/SPD[k, k];
Print["W sector"];
sLW$ = twoPoint$[{V[3]} -> {V[3]}, projL$];
aWG$ = twoPoint$[{V[3]} -> {S[3]}, projM$[mu]];
aGW$ = twoPoint$[{S[3]} -> {V[3]}, projM$[mu]];
sGp$ = twoPoint$[{S[3]} -> {S[3]}, 1];
Print["Z sector"];
sLZ$ = twoPoint$[{V[2]} -> {V[2]}, projL$];
aZG$ = twoPoint$[{V[2]} -> {S[2]}, projM$[mu]];
aGZ$ = twoPoint$[{S[2]} -> {V[2]}, projM$[mu]];
sG0$ = twoPoint$[{S[2]} -> {S[2]}, 1];
Print["photon"];
sLA$ = twoPoint$[{V[1]} -> {V[1]}, projL$];
sLAZ$ = twoPoint$[{V[1]} -> {V[2]}, projL$];
aAG$ = twoPoint$[{V[1]} -> {S[2]}, projM$[mu]];
aGA$ = twoPoint$[{S[2]} -> {V[1]}, projM$[mu]];


(* ::Section:: *)
(*Slavnov-Taylor identities (note Eq. (st))*)


(* <F F> keeps its tree value; with <W+_mu G-> the G+ -> W+ transition (a_GW) and <G+ W-_nu> the W+ -> G+ one
   (a_WG):  k^2 Sigma_L^W + i MW k^2 (a_GW - a_WG) - MW^2 Sigma^G = 0, the same for Z, G0, and for the photon
   Sigma_L^AA = 0, Sigma_L^AZ + i MZ a_GA = 0 *)
cleanST$[x_] := Simplify[(x /. SPD[k, k] -> kk2 /. Pair[Momentum[k, D], Momentum[k, D]] -> kk2 /.
       B0[p_, a_, b_] :> B0[p /. SPD[k, k] -> kk2, a, b]) /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2], 0 < sw < 1];
stWMA$ = cleanST$[kk2 sLW$ + I MW kk2 (aGW$ - aWG$) - MW^2 sGp$];
(* the photon mass MA (IR regulator) breaks BRST in the W-photon loops: the residual is O(MA^2) *)
Print["ST (W) with the photon mass MA: residual vanishes as MA -> 0? terms without MA^2 or A0[MA^2 ...]: ",
  Simplify[stWMA$ /. {A0[x_] /; !FreeQ[x, MA] :> 0} /. MA -> 0]];
stW$ = Simplify[stWMA$ /. MA -> 0 /. A0[0] -> 0];
stZ$ = cleanST$[kk2 sLZ$ + I MZ kk2 (aGZ$ - aZG$) - MZ^2 sG0$];
stA$ = cleanST$[sLA$];
stAZ$ = cleanST$[sLAZ$ + I MZ aGA$];
Print["ST (W):  k^2 Sigma_L^W + i MW k^2 (a_GW - a_WG) - MW^2 Sigma^G+ = ", stW$, "   (expect 0)"];
Print["ST (Z):  k^2 Sigma_L^Z + i MZ k^2 (a_GZ - a_ZG) - MZ^2 Sigma^G0 = ", stZ$, "   (expect 0)"];
Print["ST (A):  Sigma_L^AA = ", stA$, "   (expect 0)"];
Print["ST (AZ): Sigma_L^AZ + i MZ a_GA = ", stAZ$, "   (expect 0)"];
Print["mixing antisymmetry a_WG + a_GW, a_ZG + a_GZ, a_AG + a_GA: ",
  cleanST$[{aWG$ + aGW$, aZG$ + aGZ$, aAG$ + aGA$}]];
(* the same identities without the tadpole-attached diagrams *)
noTad$[x_, proc_] := x - tadPartST$[proc];
stW1PI$ = Simplify[cleanST$[kk2 noTad$[sLW$, {V[3]} -> {V[3]}] + I MW kk2 (noTad$[aGW$, {S[3]} -> {V[3]}] -
       noTad$[aWG$, {V[3]} -> {S[3]}]) - MW^2 noTad$[sGp$, {S[3]} -> {S[3]}]] /. MA -> 0 /. A0[0] -> 0];
stZ1PI$ = cleanST$[kk2 noTad$[sLZ$, {V[2]} -> {V[2]}] + I MZ kk2 (noTad$[aGZ$, {S[2]} -> {V[2]}] -
      noTad$[aZG$, {V[2]} -> {S[2]}]) - MZ^2 noTad$[sG0$, {S[2]} -> {S[2]}]];
Print["without the tadpole-attached diagrams, ST (W), (Z) residuals (expect nonzero): ",
  {Simplify[stW1PI$] =!= 0, Simplify[stZ1PI$] =!= 0}, ";  (Z) residual = ", Short[stZ1PI$, 5]];
Print["Summary: ", {stW$, stZ$, stA$, stAZ$}];
