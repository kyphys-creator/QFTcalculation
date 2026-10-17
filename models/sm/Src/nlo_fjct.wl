(* ::Package:: *)

(* ::Title:: *)
(*Step (9b): the FJ counterterms in counterterm form for the note's NLO UFO (Feynman gauge)*)


(* ::Text:: *)
(*MadLoop has no tadpole diagrams and no self-energies on external legs, so the FJ scheme enters the UFO as counterterm*)
(*vertices (Feynman gauge, all fermions massless except the top).  For nu nubar -> nu nubar:*)
(*  Z Z:        I g^{mu nu} (dMZ2 - Sigma_tad^ZZ),  dMZ2 = MS-bar pole of Sigma_T^ZZ(MZ^2) with the tadpole part, Sigma_tad^ZZ the*)
(*              tadpole-attached diagrams (H line at zero momentum; pole and finite part);*)
(*  Z nu nubar: the tree vertex times [de/e - (1/2) dcw2 (1/cw^2 - 1/sw^2) + dZnu]  (de, dcw2 = dMW2/MZ^2 - MW^2 dMZ2/MZ^4 the*)
(*              MS-bar poles; dZnu = -Sigma^L_nu(0) on shell, for the external legs; no Z field renormalization);*)
(*the note's MS-bar parameters and the poles as 1/FR$Eps (NLOCT's convention: 1/FR$Eps = Delta_UV), the scale FR$MU.*)
(*Writes results/nlo_fjct.m (the checks of nlo_fjdelta.wl; the note's Eq. (fjct)).  Batch: wolframscript -file nlo_fjct.wl*)


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
(*two-point functions in Feynman gauge*)


fey$ = {xiA -> 1, xiZ -> 1, xiW -> 1, xiG -> 1};
reduceOL$[x_] := Module[{r},
   r = FDS[x, q];
   r = TID[DiracSimplify[SUNSimplify[r]], q, ToPaVe -> True];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]};
   Simplify[r /. {B0[0, 0, 0] -> 0, A0[0] -> 0}]];
proj$[x_] := Contract[-(MTD[mu, nu] - FVD[k, mu] FVD[k, nu]/SPD[k, k]) x/(D - 1)];
sig$[v1_, v2_, which_] := Module[{t1 = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], tT, a1, faT, keep, drop, aT, all},
   tT = Complement[CreateTopologies[1, 1 -> 1], t1];
   a1 = If[which === "tad", {}, convertOL$[CreateFeynAmp[insertOL$[t1, {v1} -> {v2}], Truncated -> True, GaugeRules -> {}], {k}, {k}]];
   faT = Quiet[CreateFeynAmp[insertOL$[tT, {v1} -> {v2}], Truncated -> True, GaugeRules -> {}], RuleDelayed::rhs];
   {keep, drop} = tadSplitOL$[faT];
   aT = If[keep === {} || which === "1PI", {}, convertOL$[faT[[0]] @@ keep, {k}, {k}]];
   all = Join[a1, aT];
   Total[reduceOL$[proj$[#]] & /@ all] /. {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2} /. fey$];
sZZtad$ = sig$[V[2], V[2], "tad"];
sZZ$ = sig$[V[2], V[2], "all"]; sWW$ = sig$[V[3], V[3], "all"]; sAZ$ = sig$[V[1], V[2], "all"]; sAA$ = sig$[V[1], V[1], "all"];
Print["(a) Sigma_tad^ZZ (independent of k^2): ", Simplify[sZZtad$]];

(* the neutrino Sigma^L(0) as in nunu_feyncalc.wl *)
sigmaL0$[fld_] := Module[{d, a, ext, r},
   d = insertOL$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {fld} -> {fld}];
   a = convertOL$[CreateFeynAmp[d, Truncated -> True, GaugeRules -> {}], {k}, {k}];
   ext[x_] := Module[{y = DiracSimplify[FCI[x]]},
     (DiracTrace[DiracSimplify[GSD[k] . y], DiracTraceEvaluate -> True] -
       DiracTrace[DiracSimplify[GA5 . GSD[k] . y], DiracTraceEvaluate -> True])/(4 SPD[k, k])];
   r = Total[reduceOL$[ext[#]] & /@ a] /. {SPD[k, k] -> pp2, Pair[Momentum[k, D], Momentum[k, D]] -> pp2};
   r = r /. B0[pp_, m1_, m2_] :> (B0[0, m1, m2] + (pp /. {SPD[k, k] -> pp2}) DB0[0, m1, m2]);
   Simplify[Normal[Series[r, {pp2, 0, 0}]]] /. fey$];
sLnu$ = sigmaL0$[F[1, {1}]];


(* ::Section:: *)
(*Laurent coefficients in the model's symbols*)


ep = Epsilon;
(* A0, B0 at the points needed: closed forms with Delta = 1/ep; B0(MZ^2, 0, 0) etc. of the 1PI parts only enter the poles *)
closed$ = {A0[m2_] :> m2 (1/ep + 1 - Log[m2/FR$MU^2]), B0[0, 0, 0] -> 0, B0[0, a_, a_] :> 1/ep - Log[a/FR$MU^2],
   B0[0, 0, b_] :> 1/ep + 1 - Log[b/FR$MU^2], B0[0, b_, 0] :> 1/ep + 1 - Log[b/FR$MU^2],
   B0[0, a_, b_] :> 1/ep + 1 - (a Log[a/FR$MU^2] - b Log[b/FR$MU^2])/(a - b),
   DB0[0, 0, b_] :> 1/(2 b), DB0[0, b_, 0] :> 1/(2 b)};
poleOnly$[x_] := Module[{y = Expand[x /. {A0[m2_] :> m2 dd, B0[__] :> dd}]}, Simplify[Coefficient[y, dd] /. D -> 4]];
lauClosed$[x_] := Module[{y = Simplify[(x /. closed$) /. D -> 4 - 2 ep]}, Simplify /@ {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];
(* MS-bar mass poles (FJ: with the tadpole part) and the charge pole *)
dMZ2$ = poleOnly$[sZZ$ /. kk2 -> MZ^2]; dMW2$ = poleOnly$[sWW$ /. kk2 -> MW^2];
(* e(mu): Pi(0)/2 + (sw/cw) Sigma^AZ(0)/MZ^2; the poles do not depend on the k^2 at which Pi is taken *)
(* the pole parts of Sigma_T^AA(k^2) = k^2 Pi and of Sigma_T^AZ(k^2) are polynomials in k^2 *)
piPole$ = Simplify[poleOnly$[sAA$]/kk2]; azPole$ = Simplify[poleOnly$[sAZ$]] /. kk2 -> 0;
Print["(b) pole of Pi^AA free of k^2 (expect True): ", FreeQ[piPole$, kk2]];
de$ = Simplify[piPole$/2 + sw/cw azPole$/MZ^2];
tadL$ = lauClosed$[sZZtad$];
dZnuL$ = -lauClosed$[sLnu$];
Print["(b) MS-bar poles: K dMZ2 = ", Simplify[KK dMZ2$], ";  K dMW2 = ", Simplify[KK dMW2$], ";  K de/e = ", Simplify[KK de$],
  " (expect 11/6 ee^2)"];
Print["(b) K Sigma_tad^ZZ = ", Simplify[KK tadL$[[1]]], "/eps + ", Simplify[KK tadL$[[2]]]];
Print["(b) K dZnu^L = ", Simplify[KK dZnuL$[[1]]], "/eps + ", Simplify[KK dZnuL$[[2]]]];
toFR$[x_] := x /. {ee -> ee, cw -> cw, sw -> sw};
Put[<|"dMZ2" -> dMZ2$, "dMW2" -> dMW2$, "de" -> de$, "tadZZ" -> tadL$, "dZnuL" -> dZnuL$|>,
  FileNameJoin[{resDirOL$, "nlo_fjct.m"}]];
Print["(c) wrote results/nlo_fjct.m"];
Quiet[DeleteDirectory[modelTmpDirOL$, DeleteContents -> True]];
