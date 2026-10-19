(* ::Package:: *)

(* ::Title:: *)
(*Step (4b) of the NLO note: the W self-energy with a massless photon (general R_xi)*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (4b).  The 1PI W self-energy of the note's FeynArts model (all loops; the photon massless,*)
(*the CKM matrix as cK, cKc), projected on the transverse part as the SM note's oneloop_feyncalc.wl does,*)
(*  K Sigma_T(k^2) = K [ -(g_{mu nu} - k_mu k_nu/k^2)/(D - 1) ] x (the FeynArts amplitude),  in A0, B0 with D kept, k^2 = kk2,*)
(*for the field constant dZ_W = -Sigma_T'(M_W^2) of wweak.wl (the derivative of B0 at threshold with the massless photon is*)
(*taken there in dimensional regularization).  The tadpole-attached diagrams do not depend on k^2.*)
(*Check: Sigma_T(k^2) at V = 1 against the SM note's (models/sm/Src/results/oneloop_sigma.m, photon mass MA -> 0, xiA = 1).*)
(*Writes work/wsig.m.  Batch:  wolframscript -file wsig_feyncalc.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirWS$ = DirectoryName[$InputFileName];
workDirWS$ = FileNameJoin[{srcDirWS$, "work"}];
t0WS$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0WS$], " s] ", s];
modelTmpWS$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirWS$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpWS$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpWS$, "SM_CKM_FA"}], Quiet -> True];
modelFileWS$ = FileNameJoin[{modelTmpWS$, "SM_CKM_FA", "SM_CKM_FA"}];
massWS$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me};
lepMWS$ = {Me, MMU, MTA}; upMWS$ = {MU, MC, MT}; dnMWS$ = {MD, MS, MB};
yukWS$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMWS$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMWS$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMWS$[[i]]/vev, 0]};
ckmWS$ = {Conjugate[CKM[i_Integer, j_Integer]] :> cKc[i, j], CKM[i_Integer, j_Integer] :> cK[i, j]};
convWS$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG,
    GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
    GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1}, massWS$];
sumOverWS$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];
KK = (4 Pi)^2;
diagsWS$ = Quiet[InsertFields[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {V[3]} -> {V[3]},
    InsertionLevel -> {Particles}, Model -> modelFileWS$, GenericModel -> modelFileWS$], RuleDelayed::rhs];
ampWS$ = Quiet[FCFAConvert[CreateFeynAmp[diagsWS$, Truncated -> True, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {k},
     OutgoingMomenta -> {k}, LoopMomenta -> {q}, LorentzIndexNames -> {mu, nu}, ChangeDimension -> D, List -> True, SMP -> False,
     UndoChiralSplittings -> True, DropSumOver -> False, DropIndexSum -> False], RuleDelayed::rhs];
ampWS$ = ampWS$ /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
ampWS$ = (sumOverWS$ /@ ampWS$) /. convWS$ /. yukWS$ /. ckmWS$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee;
ampWS$ = ampWS$ /. {DiracGamma[6] -> 1/2 + DiracGamma[5]/2, DiracGamma[7] -> 1/2 - DiracGamma[5]/2};
Print["W self-energy: ", Length[ampWS$], " 1PI diagrams"];
DeleteDirectory[modelTmpWS$, DeleteContents -> True];
projWS$ = -1/(D - 1) (MTD[mu, nu] - FVD[k, mu] FVD[k, nu]/SPD[k, k]);
reduceWS$[x_] := Module[{r},
   r = FDS[x, q];
   r = TID[DiracSimplify[SUNSimplify[r]], q, ToPaVe -> True];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]};
   r /. {B0[0, 0, 0] -> 0, A0[0] -> 0}];
projAmpWS$ = Contract[projWS$ #] & /@ ampWS$;

(* (i) Sigma_T(k^2) against the SM note *)
FCClearScalarProducts[];
kRuleWS$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
(* k^2 as the symbol kk2 at once: a later ScalarProduct[k, k] = ... would otherwise be applied when the value is used *)
sigTWS$ = (KK Total[reduceWS$ /@ projAmpWS$]) /. kRuleWS$;
smSigWS$ = Association[Get[FileNameJoin[{srcDirWS$, "..", "..", "sm", "Src", "results", "oneloop_sigma.m"}]]];
smWWWS$ = smSigWS$["WW"][[1]];   (* the 1PI part *)
kRuleWS$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
(* the SM note's photon mass: xiA = 1, then MA -> 0 coefficient by coefficient of the loop functions (as the CKM note's
   wud_renormalized.wl; no 1/MA may be left) *)
limitMAWS$[x_] := Module[{y = x /. xiA -> 1, fs, cs, c0},
   fs = Union[Cases[y, _A0 | _B0 | _C0 | _PaVe, Infinity]];
   y = Expand[y /. Thread[fs -> Array[lf$, Length[fs]]]];
   cs = Together[Coefficient[y, lf$[#]]] & /@ Range[Length[fs]];
   c0 = Together[y /. lf$[_] -> 0];
   If[! FreeQ[Denominator /@ Append[cs, c0], MA], Print["   WARNING: 1/MA left after xiA = 1"]];
   (Append[cs, c0] /. MA -> 0) . Append[fs /. MA -> 0, 1] /. {A0[0] -> 0, B0[0, 0, 0] -> 0}];
mineWS$ = sigTWS$ /. kRuleWS$ /. {cK[i_, j_] :> KroneckerDelta[i, j], cKc[i_, j_] :> KroneckerDelta[i, j]} /. xiA -> 1;
theirsWS$ = limitMAWS$[smWWWS$ /. kRuleWS$];
dWWWS$ = Simplify[Expand[mineWS$ - theirsWS$ /. MZ -> MW/cw] /. cw -> Sqrt[1 - sw^2], 0 < sw < 1];
Print["(i) K Sigma_T^WW(k^2) at V = 1, xiA = 1 minus the SM note's (photon mass MA -> 0), symbolic (expect 0): ", dWWWS$];
tick$["(i)"];

Put[<|"sigT" -> sigTWS$|>, FileNameJoin[{workDirWS$, "wsig.m"}]];
Print["written: work/wsig.m"];
