(* ::Package:: *)

(* ::Title:: *)
(*Step (6): muon decay at one loop and G_F in the MS-bar scheme with FJ tadpoles, general R_xi (SM note)*)


(* ::Text:: *)
(*mu-(p1) -> nu_mu(p2) e-(p3) nubar_e(p4) with massless leptons at zero external momenta (all integrals are vacuum*)
(*integrals, A0 and B0(0, m1^2, m2^2) in D dimensions).  The bare one-loop amplitude is the tree times*)
(*  1 + Sigma_T^WW(0)/MW^2 + dV + dB - (1/2) sum_legs Sigma^L_f(0)                                   (note Eq. (GF1))*)
(*(Sigma^WW with the tadpole-attached diagrams, dV, dB = the 8 vertex and 5 box diagrams projected on the tree Dirac*)
(*structure, Sigma^L the left-handed self-energy of the massless external leptons at p = 0), and with*)
(*g0^2/(8 MW0^2) = 1/(2 v0^2) this gives G_F/sqrt 2 = (1 + DeltaHat)/(2 v^2).  The checks, made in mudecay_check.wl:*)
(*  (a) the UV pole of the bracket is (1/2) dln v^2/dln mu (Eq. (vrun)), for independent xiA, xiZ, xiW;*)
(*  (b) the photon mass MA (IR regulator) drops out as MA -> 0;*)
(*  (c) DeltaHat does not depend on xiA, xiZ, xiW;*)
(*  (d) in Feynman gauge dV + dB + dWF = (alpha/(4 pi sw^2)) [4 B0(0, MW, MW) + 6 + (7 - 4 sw^2)/(2 sw^2) ln cw^2]*)
(*      (Sirlin, Denner) in D dimensions to O(eps^0).*)
(*The Fermi-theory QED correction at zero momentum vanishes (V - A current, Ward identity), so nothing is subtracted.*)
(*Setup as in oneloop_feyncalc.wl.  Writes results/mudecay_deltahat.m.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file mudecay_feyncalc.wl  (about 15 minutes; then mudecay_check.wl).*)


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
(*Amplitudes at zero external momentum*)


lep0$ = {Me -> 0, MMU -> 0};
procMu$ = {F[2, {2}]} -> {F[1, {2}], F[2, {1}], -F[1, {1}]};
(* spinors keep their own momentum symbols, the momenta in the integrands are set to zero *)
spinRename$ = {Spinor[Momentum[p_, d___], r___] :> Spinor[Momentum[sp[p], d], r],
   Spinor[-Momentum[p_, d___], r___] :> Spinor[-Momentum[sp[p], d], r]};
(* the tree W propagator at zero momentum is the number -1/MW^2 *)
zeroMom$[x_] := FCReplaceMomenta[x /. spinRename$, {p1 -> 0, p2 -> 0, p3 -> 0, p4 -> 0}] /.
   FeynAmpDenominator[PropagatorDenominator[0 | Momentum[0, ___], m_]] :> -1/m^2;
ampMu$[tops_] := Module[{d = insertOL$[tops, procMu$], a},
   a = convertOL$[CreateFeynAmp[d, GaugeRules -> {}], {p1}, {p2, p3, p4}] /. lep0$;
   a = Select[zeroMom$ /@ a, Simplify[DiracSimplify[#]] =!= 0 &];
   a];
treeMu$ = ampMu$[CreateTopologies[0, 1 -> 3]];
vertMu$ = ampMu$[CreateTopologies[1, 1 -> 3, ExcludeTopologies -> {Tadpoles, WFCorrections, SelfEnergies, Boxes}]];
boxMu$ = ampMu$[CreateTopologies[1, 1 -> 3, ExcludeTopologies -> {Tadpoles, WFCorrections, SelfEnergies, Triangles}]];
Print["tree, vertex, box amplitudes (nonzero, massless leptons): ", Length /@ {treeMu$, vertMu$, boxMu$},
  "   (expect 1, 8, 5)"];

(* Dirac chains: [nubar_mu ... mu] and [ebar ... nu_e] *)
chainRule$ = {Dot[Spinor[Momentum[sp[p2], ___], ___], x___, Spinor[Momentum[sp[p1], ___], ___]] :> chA[Dot[x]],
   Dot[Spinor[Momentum[sp[p3], ___], ___], y___, Spinor[-Momentum[sp[p4], ___], ___]] :> chB[Dot[y]]};
projChains$[x_, dim_] := Module[{y = Expand[x /. chainRule$], tr, gb},
   gb = If[dim === 4, GA[bb$], GAD[bb$]];
   tr[z_] := DiracTrace[ChangeDimension[DiracSimplify[FCI[z]], dim], DiracTraceEvaluate -> True];
   (* contract the whole product: the metric of the W propagator (and the g^{mu nu} from TID) multiplies the two
      traces from outside.  Contract twice: an Eps^2 from the two traces is not contracted in one call (environment Table 11) *)
   y = Contract[Contract[y /. chA[a_] chB[b_] :> tr[a . gb] tr[b . gb]]];
   If[!FreeQ[y, LorentzIndex], Print["   uncontracted Lorentz indices left: ", Short[y, 3]]];
   If[!FreeQ[y, chA | chB | Spinor], Print["   unprojected chains left: ", Short[y, 3]]];
   y];
reduceMu$[x_] := Module[{r = TID[DiracSimplify[x], q, ToPaVe -> True]},
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {0}, {m1_, m2_}] :> B0[0, m1, m2]};
   r];

pTree$ = Simplify[projChains$[Total[treeMu$], D]];
(* vertex corrections: D-dimensional Dirac algebra (UV divergent); boxes: UV finite, projected in 4 dimensions *)
pVert$ = Simplify[Total[projChains$[reduceMu$[FDS[#, q]], D] & /@ vertMu$]];
pBox$ = Simplify[Total[projChains$[ChangeDimension[reduceMu$[FDS[#, q]], 4], 4] & /@ boxMu$]];
dV$ = Simplify[pVert$/pTree$]; dB$ = Simplify[(pBox$/pTree$) /. D -> 4];
Print["dV, dB computed; leaf counts ", LeafCount /@ {dV$, dB$}];


(* ::Section:: *)
(*External legs and the W self-energy at zero momentum*)


(* Sigma^L(p^2) of a massless lepton from its self-energy, then p^2 -> 0 with B0(p^2, a, b) = B0(0, a, b) + p^2 DB0(0, a, b) *)
sigmaL0$[fld_] := Module[{d, a, ext, r},
   d = insertOL$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {fld} -> {fld}];
   a = convertOL$[CreateFeynAmp[d, Truncated -> True, GaugeRules -> {}], {k}, {k}] /. lep0$;
   ext[x_] := Module[{y = DiracSimplify[FCI[x]]},
     (DiracTrace[DiracSimplify[GSD[k] . y], DiracTraceEvaluate -> True] -
       DiracTrace[DiracSimplify[GA5 . GSD[k] . y], DiracTraceEvaluate -> True])/(4 SPD[k, k])];
   r = Total[reduceOL$[ext[#]] & /@ a] /. {SPD[k, k] -> pp2, Pair[Momentum[k, D], Momentum[k, D]] -> pp2};
   r = r /. B0[pp_, m1_, m2_] :> (B0[0, m1, m2] + (pp /. {SPD[k, k] -> pp2}) DB0[0, m1, m2]);
   Simplify[Normal[Series[r, {pp2, 0, 0}]]]];
sLmu$ = sigmaL0$[F[2, {2}]]; sLe$ = sigmaL0$[F[2, {1}]];
sLnm$ = sigmaL0$[F[1, {2}]]; sLne$ = sigmaL0$[F[1, {1}]];
dWF$ = Simplify[-(sLmu$ + sLe$ + sLnm$ + sLne$)/2];

(* W self-energy at k = 0, 1PI and tadpole-attached (H line): A_{mu nu}(0) = -g_{mu nu} Sigma(0) *)
sigW0$ = Module[{t1 = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], tT, d1, a1, faT, keep, drop, aT, all},
   tT = Complement[CreateTopologies[1, 1 -> 1], t1];
   d1 = insertOL$[t1, {V[3]} -> {V[3]}];
   a1 = convertOL$[CreateFeynAmp[d1, Truncated -> True, GaugeRules -> {}], {k}, {k}] /. lep0$;
   faT = Quiet[CreateFeynAmp[insertOL$[tT, {V[3]} -> {V[3]}], Truncated -> True, GaugeRules -> {}], RuleDelayed::rhs];
   {keep, drop} = tadSplitOL$[faT];
   aT = convertOL$[faT[[0]] @@ keep, {k}, {k}] /. lep0$;
   all = FCReplaceMomenta[Join[a1, aT], {k -> 0}];
   Simplify[Total[reduceOL$[Contract[-MTD[mu, nu] #/D]] & /@ all]]];

(* the products of FCFAConvert carry 1/(16 pi^4) and TID i pi^2: KK x (dimensionless loop quantities) *)
brK$ = KK Simplify[sigW0$/MW^2 + dV$ + dB$ + dWF$];
Put[{"sigW0" -> KK sigW0$, "dV" -> KK dV$, "dB" -> KK dB$, "dWF" -> KK dWF$, "sLmu" -> KK sLmu$, "sLe" -> KK sLe$,
   "sLnm" -> KK sLnm$, "sLne" -> KK sLne$}, FileNameJoin[{resDirOL$, "mudecay_deltahat.m"}]];
Print["K x (Sigma^W(0)/MW^2 + dV + dB + dWF) written to results/mudecay_deltahat.m"];
