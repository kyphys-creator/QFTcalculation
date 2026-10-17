(* ::Package:: *)

(* ::Title:: *)
(*Step (9a): nu_e nubar_e -> nu_mu nubar_mu at one loop in the MS-bar scheme with FJ tadpoles, general R_xi (SM note)*)


(* ::Text:: *)
(*nu_e(p1) nubar_e(p2) -> nu_mu(p3) nubar_mu(p4), all fermions massless except the top (as MadGraph's loop_qcd_qed_sm*)
(*with restrict_no_widths), no photon couples to the external states, so the one-loop amplitude is infrared finite.*)
(*Diagrams of the note's FeynArts model (Src/generated/SM_FA) with xiA, xiZ, xiW kept:*)
(*  vertex insertions and the tadpole attached to the s-channel Z through a zero-momentum H line (FJ): D-dimensional*)
(*      Dirac algebra, each reduced to the tree structure [vbar2 g^mu P_L u1][ubar3 g_mu P_L v4];*)
(*  the s-channel self-energy: M0 (-Sigma_T^ZZ(s)/(s - MZ^2)) from the (1PI) transverse self-energy;*)
(*  boxes (UV finite): interfered with the tree with four-dimensional traces;*)
(*  external legs: LSZ factor sqrt(R) = 1 - Sigma^L_nu(0)/2 per leg (massless neutrinos).*)
(*W = sum_spins M0^* M1.  The UV pole of W cancels against the MS-bar counterterms of e, MW^2, MZ^2 (the tree depends on*)
(*e^2/(sw^2 cw^2) and 1/(s - MZ^2)), so the MS-bar amplitude is the bare one with Delta_UV -> 0 (and mu).*)
(*Conversion to on-shell inputs (alpha(MZ) scheme with massless light fermions, on-shell MW, MZ; as loop_qcd_qed_sm):*)
(*  MV^2(MS) = MV^2(OS) + Re Sigma_T^VV(MV^2)  (FJ: with the tadpole part),*)
(*  e(mu)/e_alphaMZ - 1 = [Pi_heavy(0) + Re Pi_light(MZ^2)]/2 + (sw/cw) Sigma_T^AZ(0)/MZ^2  (alpha_matching.wl, note sign),*)
(*  W_OS = W + B4 dln M0,  dln M0 = 2 de - dln(sw^2 cw^2) + dMZ^2/(s - MZ^2).*)
(*Writes results/nunu_feyncalc.m (symbolic pieces, A0 B0 C0 D0 in FeynCalc's conventions = LoopTools').*)
(*Batch: wolframscript -file nunu_feyncalc.wl*)


(* ::Section:: *)
(*Setup (as mudecay_feyncalc.wl)*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
t0$ = AbsoluteTime[];

srcDirOL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirOL$ = FileNameJoin[{srcDirOL$, "results"}];
modelTmpDirOL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOL$, "generated", "SM_FA"}], FileNameJoin[{modelTmpDirOL$, "SM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOL$, "SM_FA"}], Quiet -> True];
modelFileOL$ = FileNameJoin[{modelTmpDirOL$, "SM_FA", "SM_FA"}];

massOL$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me};
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
(* all fermions massless except the top *)
light0$ = {Me -> 0, MMU -> 0, MTA -> 0, MU -> 0, MC -> 0, MD -> 0, MS -> 0, MB -> 0};
sumOverOL$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];
insertOL$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles},
    Model -> modelFileOL$, GenericModel -> modelFileOL$], RuleDelayed::rhs];
convertOL$[fa_, in_, out_] := Module[{a},
   a = Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out,
       LoopMomenta -> {q}, LorentzIndexNames -> {mu, nu, rho, sig}, ChangeDimension -> D, List -> True, SMP -> False,
       UndoChiralSplittings -> True, DropSumOver -> False], RuleDelayed::rhs];
   a = (sumOverOL$ /@ a) /. convOL$ /. yukOL$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee /. light0$ /.
     FeynAmpDenominator[PropagatorDenominator[0 | Momentum[0, ___], m_]] :> -1/m^2;
   a = a /. {DiracGamma[6] -> 1/2 + DiracGamma[5]/2, DiracGamma[7] -> 1/2 - DiracGamma[5]/2};
   Select[a, # =!= 0 &]];
(* tadpole topologies: keep the zero-momentum H line; the Z and photon lines attach a vanishing one-point vector loop
   (the photon line is 1/0) *)
tadSplitOL$[fa_] := Module[{l = List @@ fa},
   {Select[l, ! FreeQ[#, FAPropagatorDenominator[0, FCGV["MH"] | MH]] &],
    Select[l, FreeQ[#, FAPropagatorDenominator[0, FCGV["MH"] | MH]] &]}];
KK = (4 Pi)^2;
FCClearScalarProducts[];
(* massless kinematics: s = (p1 + p2)^2, t = (p1 - p3)^2, u = (p1 - p4)^2 = -s - t *)
kin$ = {SPD[p1, p1] -> 0, SPD[p2, p2] -> 0, SPD[p3, p3] -> 0, SPD[p4, p4] -> 0, SPD[p1, p2] -> ss/2, SPD[p3, p4] -> ss/2,
   SPD[p1, p3] -> -tt/2, SPD[p2, p4] -> -tt/2, SPD[p1, p4] -> (ss + tt)/2, SPD[p2, p3] -> (ss + tt)/2};
Scan[(Set @@ #) &, kin$];
Scan[(Set @@ (# /. SPD -> SP)) &, kin$];


(* ::Section:: *)
(*(a) diagrams*)


procNN$ = {F[1, {1}], -F[1, {1}]} -> {F[1, {2}], -F[1, {2}]};
ampNN$[tops_] := convertOL$[CreateFeynAmp[insertOL$[tops, procNN$], GaugeRules -> {}], {p1, p2}, {p3, p4}];
tree$ = ampNN$[CreateTopologies[0, 2 -> 2]];
topsAll$ = CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {WFCorrections}];
topsNoTad$ = CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {WFCorrections, Tadpoles}];
topsBox$ = CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {WFCorrections, Tadpoles, SelfEnergies, Triangles}];
(* vertex corrections as four-point diagrams; the s-channel self-energies from Sigma_T^ZZ(s) below (the k k terms of the
   propagators vanish on the massless currents, so they are M0 (-Sigma_T^ZZ(s)/(s - MZ^2)); in a general R_xi gauge
   the projection of the four-point self-energy diagrams is very slow) *)
topsVS$ = CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {WFCorrections, Tadpoles, Boxes, SelfEnergies}];
topsTad$ = Complement[topsAll$, topsNoTad$];
vs$ = ampNN$[topsVS$];
box$ = ampNN$[topsBox$];
faTad$ = Quiet[CreateFeynAmp[insertOL$[topsTad$, procNN$], GaugeRules -> {}], RuleDelayed::rhs];
{tadKeep$, tadDrop$} = tadSplitOL$[faTad$];
tad$ = convertOL$[faTad$[[0]] @@ tadKeep$, {p1, p2}, {p3, p4}];
Print["(a) diagrams (nonzero): tree ", Length[tree$], ", vertex ", Length[vs$], ", boxes ", Length[box$],
  ", tadpole-attached (H line) ", Length[tad$], " (dropped Z/photon lines: ", Length[tadDrop$], ");  ",
  Round[AbsoluteTime[] - t0$], " s"];


(* ::Section:: *)
(*(b) loop reduction and the projection on the tree structure*)


(* momentum conservation for the Dirac equation: a loop on the [vbar(p2) ... u(p1)] chain is written with p1, p2 (p4 ->
   p1 + p2 - p3), a loop on the [ubar(p3) ... v(p4)] chain with p3, p4 (p1 -> p3 + p4 - p2); the spinors keep their momenta.
   (FeynArts' routing may give e.g. p3 + p4 - p2 - q for the momentum next to u(p1), and DiracSimplify does not know
   p3 + p4 - p2 = p1.) *)
chainMom$[x_] := Module[{inA, inB, y, rule},
   inA = !FreeQ[Cases[x, d_Dot /; !FreeQ[d, Spinor[Momentum[p1, ___], ___]], Infinity], q];
   inB = !FreeQ[Cases[x, d_Dot /; !FreeQ[d, Spinor[Momentum[p3, ___], ___]], Infinity], q];
   rule = Which[inA && !inB, {p4 -> p1 + p2 - p3}, inB && !inA, {p1 -> p3 + p4 - p2}, True, {}];
   If[rule === {}, Return[x]];
   y = x /. {Spinor[Momentum[k_, d___], r___] :> spH$[k, {d}, {r}], Spinor[-Momentum[k_, d___], r___] :> spHm$[k, {d}, {r}]};
   y = FCReplaceMomenta[y, rule];
   y /. {spH$[k_, {d___}, {r___}] :> Spinor[Momentum[k, d], r], spHm$[k_, {d___}, {r___}] :> Spinor[-Momentum[k, d], r]}];
reduceNN$[x_] := Module[{r = FDS[chainMom$[x], q]},
   r = TID[DiracSimplify[r], q, ToPaVe -> True];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2],
       PaVe[0, {a_, b_, c_}, {m1_, m2_, m3_}] :> C0[a, b, c, m1, m2, m3],
       PaVe[0, {a_, b_, c_, d_, e_, f_}, {m1_, m2_, m3_, m4_}] :> D0[a, b, c, d, e, f, m1, m2, m3, m4]};
   r];
(* the two Dirac chains of each term: [vbar(p2) ... u(p1)] and [ubar(p3) ... v(p4)] *)
chA$[x_] := MatchQ[x, Dot[Spinor[-Momentum[p2, ___], ___], ___, Spinor[Momentum[p1, ___], ___]]];
chB$[x_] := MatchQ[x, Dot[Spinor[Momentum[p3, ___], ___], ___, Spinor[-Momentum[p4, ___], ___]]];
(* reduce a D-dimensional amplitude to c x [g^mu P_L][g_mu P_L]; returns the coefficients of the chirality combinations
   {LL, LR, RL, RR} (only LL may be nonzero; anything else is reported) *)
chirOf$[inner_] := Switch[inner,
   Dot[DiracGamma[LorentzIndex[_, ___], ___], DiracGamma[7]], {{1, 0}, inner[[1, 1, 1]]},
   Dot[DiracGamma[LorentzIndex[_, ___], ___], DiracGamma[6]], {{0, 1}, inner[[1, 1, 1]]},
   Dot[DiracGamma[LorentzIndex[_, ___], ___], DiracGamma[5]], {{-1, 1}, inner[[1, 1, 1]]},
   DiracGamma[LorentzIndex[_, ___], ___], {{1, 1}, inner[[1, 1]]},
   _, {{"?", "?"}, 0}];
(* the chains as {coefficient of g^mu P_L, of g^mu P_R}: g^mu = L + R, g^mu g5 = R - L *)
markChains$ = {Dot[Spinor[-Momentum[p2, ___], ___], x__, Spinor[Momentum[p1, ___], ___]] :> chA[chirOf$[Dot[x]]],
   Dot[Spinor[Momentum[p3, ___], ___], y__, Spinor[-Momentum[p4, ___], ___]] :> chB[chirOf$[Dot[y]]]};
treeCoef$[x_] := Module[{y = DiracSimplify[x], z},
   (* the closed fermion loops of the Z self-energy: D-dimensional traces (the gamma5 parts give Eps(p3, p4, mu, rho),
      whose coefficient cancels: the self-energy depends on p3 + p4 only) *)
   y = y /. DiracTrace[t_] /; FreeQ[t, DiracGamma[5]] :> DiracTrace[t, DiracTraceEvaluate -> True];
   (* NDR leaves the D-dimensional gamma5 traces alone; they come in pairs Eps(p3, mu, p4, rho) + Eps(p4, mu, p3, rho) = 0
      (TID writes the s-channel momentum p3 + p4 in the basis p3, p4), so they are evaluated in four dimensions *)
   y = y /. DiracTrace[t_] /; !FreeQ[t, DiracGamma[5]] :> DiracTrace[ChangeDimension[t, 4], DiracTraceEvaluate -> True];
   y = Expand[DiracSimplify[Contract[ExpandScalarProduct[Contract[y]]]]];
   y = Expand[y /. Eps[a___] :> Eps[a]];
   z = Expand[y /. markChains$];
   z = z /. chA[{{a1_, a2_}, i_}] chB[{{b1_, b2_}, i_}] :> a1 b1 sG["LL"] + a1 b2 sG["LR"] + a2 b1 sG["RL"] + a2 b2 sG["RR"];
   If[!FreeQ[z, Spinor | chA | chB | "?"], Print["   chain structure outside [g^mu P_X][g_mu P_Y]: ", Short[z, 4]]];
   z = Expand[z];
   Coefficient[z, sG[#]] & /@ {"LL", "LR", "RL", "RR"}];
cTree$ = treeCoef$[Total[tree$]];
Print["(b) tree: coefficients of [g][g], [g][g g5], [g g5][g], [g g5][g g5]: ", Simplify[cTree$]];
(* each loop amplitude as a multiple of the tree: r = c/c_tree, checked on the four chiral components *)
(* the chirality combinations other than LL vanish term by term (massless fermions, left-handed couplings) *)
ratio$[x_] := Module[{c = treeCoef$[x]},
   If[c[[2 ;; 4]] =!= {0, 0, 0}, Print["   not proportional to the tree: ", Short[c[[2 ;; 4]], 4]]];
   c[[1]]/cTree$[[1]]];
progress$[f_, l_, name_] := Module[{n = Length[l]},
   Total[Table[If[Mod[i, 10] == 0, Print["   ", name, " ", i, "/", n, ";  ", Round[AbsoluteTime[] - t0$], " s"]]; f[l[[i]]],
     {i, n}]]];
rVS$ = progress$[ratio$[reduceNN$[#]] &, vs$, "vertex"];
rTad$ = progress$[ratio$[reduceNN$[#]] &, tad$, "tadpole-attached"];
Print["(b) vertex and tadpole parts reduced;  ", Round[AbsoluteTime[] - t0$], " s"];

(* the Born and the boxes: sum_spins M0^* M with four-dimensional traces (massless spinors) *)
spinSum4$[m0_, m1_] := Module[{y},
   y = FermionSpinSum[ComplexConjugate[ChangeDimension[m0, 4]] ChangeDimension[m1, 4], ExtraFactor -> 1];
   y = DiracSimplify[y /. DiracTrace[z_] :> DiracTrace[z, DiracTraceEvaluate -> True]];
   Expand[ExpandScalarProduct[Contract[Contract[y]]]]];
born4$ = spinSum4$[Total[tree$], Total[tree$]];
Print["(b) B4 = sum_spins |M0|^2 = ", born4$];
wBox$ = progress$[spinSum4$[Total[tree$], reduceNN$[#]] &, box$, "boxes"];
If[!FreeQ[wBox$, Eps | LorentzIndex | Spinor], Print["   box: Eps, indices or spinors left: ", Short[wBox$, 4]]];
Print["(b) boxes interfered with the tree;  ", Round[AbsoluteTime[] - t0$], " s"];


(* ::Section:: *)
(*(c) external neutrinos, the W, Z and photon two-point functions for the conversion*)


(* Sigma^L(p^2 -> 0) of a massless neutrino (mudecay_feyncalc.wl) *)
reduceOL$[x_] := Module[{r},
   r = FDS[x, q];
   r = TID[DiracSimplify[SUNSimplify[r]], q, ToPaVe -> True];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]};
   Simplify[r /. {B0[0, 0, 0] -> 0, A0[0] -> 0}]];
sigmaL0$[fld_] := Module[{d, a, ext, r},
   d = insertOL$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {fld} -> {fld}];
   a = convertOL$[CreateFeynAmp[d, Truncated -> True, GaugeRules -> {}], {k}, {k}];
   ext[x_] := Module[{y = DiracSimplify[FCI[x]]},
     (DiracTrace[DiracSimplify[GSD[k] . y], DiracTraceEvaluate -> True] -
       DiracTrace[DiracSimplify[GA5 . GSD[k] . y], DiracTraceEvaluate -> True])/(4 SPD[k, k])];
   r = Total[reduceOL$[ext[#]] & /@ a] /. {SPD[k, k] -> pp2, Pair[Momentum[k, D], Momentum[k, D]] -> pp2};
   r = r /. B0[pp_, m1_, m2_] :> (B0[0, m1, m2] + (pp /. {SPD[k, k] -> pp2}) DB0[0, m1, m2]);
   Simplify[Normal[Series[r, {pp2, 0, 0}]]]];
sLne$ = sigmaL0$[F[1, {1}]]; sLnm$ = sigmaL0$[F[1, {2}]];
Print["(c) Sigma^L(0): nu_e - nu_mu = ", Simplify[sLne$ - sLnm$], " (expect 0)"];

(* transverse self-energies at a symbolic k^2 = kk2, with the tadpole-attached diagrams (H line) for W and Z *)
(* xiA = 1 in Sigma_T^WW: the (1 - xiA) k k/k^4 photon terms are 0 x infinity at k^2 = MW^2 without a photon mass
   (step (7)); Sigma_T^WW(MW^2) with the tadpole part does not depend on the gauge (step (3)), and xiA does not occur in
   the amplitude (no photon line) *)
sigmaT$[v1_, v2_] := Module[{t1 = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], tT, a1, faT, keep, drop, aT, all, proj},
   tT = Complement[CreateTopologies[1, 1 -> 1], t1];
   a1 = convertOL$[CreateFeynAmp[insertOL$[t1, {v1} -> {v2}], Truncated -> True, GaugeRules -> {}], {k}, {k}];
   faT = Quiet[CreateFeynAmp[insertOL$[tT, {v1} -> {v2}], Truncated -> True, GaugeRules -> {}], RuleDelayed::rhs];
   {keep, drop} = tadSplitOL$[faT];
   aT = If[keep === {}, {}, convertOL$[faT[[0]] @@ keep, {k}, {k}]];
   (* A_{mu nu} = -g_{mu nu} Sigma_T + k_mu k_nu (...): transverse projection; {1PI, tadpole-attached} *)
   proj[x_] := Contract[-(MTD[mu, nu] - FVD[k, mu] FVD[k, nu]/SPD[k, k]) x/(D - 1)];
   Table[Total[reduceOL$[proj[#]] & /@ part] /. {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2}, {part, {a1, aT}}]];
sWW$ = Total[sigmaT$[V[3], V[3]]] /. xiA -> 1; sZZp$ = sigmaT$[V[2], V[2]]; sZZ$ = Total[sZZp$];
sAZ$ = Total[sigmaT$[V[1], V[2]]];
(* the s-channel self-energy (1PI; the tadpole-attached part is rTad) as a multiple of the tree *)
rSE$ = -sZZp$[[1]]/(kk2 - MZ^2) /. kk2 -> ss;
Print["(c) Sigma_T^WW, Sigma_T^ZZ, Sigma_T^AZ;  ", Round[AbsoluteTime[] - t0$], " s"];
(* the photon self-energy (no tadpole-attached diagrams: no H A A vertex); nunu_numeric.wl splits off the massless
   fermion loops, the terms with B0(k^2, 0, 0) *)
sAA$ = Total[sigmaT$[V[1], V[1]]];
Print["(c) Sigma_T^AA;  ", Round[AbsoluteTime[] - t0$], " s"];


(* ::Section:: *)
(*(d) output*)


Put[<|"rTree" -> 1, "cTree" -> cTree$, "B4" -> born4$, "rVS" -> rVS$, "rSE" -> rSE$, "rTad" -> rTad$, "wBox" -> wBox$,
   "sLnu" -> sLne$, "sWW" -> sWW$, "sZZ" -> sZZ$, "sAZ" -> sAZ$, "sAA" -> sAA$,
   "ndiag" -> {Length[tree$], Length[vs$], Length[box$], Length[tad$]}|>, FileNameJoin[{resDirOL$, "nunu_feyncalc.m"}]];
Print["(d) wrote results/nunu_feyncalc.m;  total ", Round[AbsoluteTime[] - t0$], " s"];
Quiet[DeleteDirectory[modelTmpDirOL$, DeleteContents -> True]];
