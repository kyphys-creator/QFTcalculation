(* ::Package:: *)

(* ::Title:: *)
(*Step (4c) of the NLO note: the electroweak one-loop vertex t -> d_j W+ with a massless photon (general R_xi)*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (4c).  The 1PI vertex of t(pt) -> d_j(p1) W+(k) from the note's FeynArts model at particle*)
(*level, all loops but the gluon (V[4] excluded; its part is the K of step (3)), the photon massless (its infrared divergence*)
(*in dimensional regularization, Package-X in tweak.wl), as wff_feyncalc.wl does for W+ -> f fbar'.  Channel (command line): j.*)
(*On shell: pt^2 = MT^2, p1^2 = m_j^2, k^2 = MW^2, eps.k = 0 (eps the conjugated polarization of the outgoing W), written as*)
(*  M = (e/(sqrt2 sw)) ubar(p1) [ epsslash (FL P_L + FR P_R) + (eps.p1) (HL P_L + HR P_R) ] u(pt),  tree FL = V_tj^*,*)
(*K = 16 pi^2 times the form factors in A0, B0, C0 with D kept.  Checks: the tree against V_tj^* gamma P_L; HL, HR, FR UV-finite.*)
(*Writes work/tff_<j>.m.  Batch:  wolframscript -file tff_feyncalc.wl j*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirTF$ = DirectoryName[$InputFileName];
workDirTF$ = FileNameJoin[{srcDirTF$, "work"}];
Quiet[CreateDirectory[workDirTF$]];
t0TF$ = AbsoluteTime[];
modelTmpWF$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTF$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpWF$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpWF$, "SM_CKM_FA"}], Quiet -> True];
modelFileWF$ = FileNameJoin[{modelTmpWF$, "SM_CKM_FA", "SM_CKM_FA"}];

massWF$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me};
lepMWF$ = {Me, MMU, MTA}; upMWF$ = {MU, MC, MT}; dnMWF$ = {MD, MS, MB};
yukWF$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMWF$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMWF$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMWF$[[i]]/vev, 0]};
ckmWF$ = {Conjugate[CKM[i_Integer, j_Integer]] :> cKc[i, j], CKM[i_Integer, j_Integer] :> cK[i, j]};
convWF$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG,
    GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
    GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1},
   massWF$];
sumOverWF$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];
convertWF$[fa_, in_, out_] := Module[{a},
   a = Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q},
       ChangeDimension -> D, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> False,
       DropIndexSum -> False], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a = (sumOverWF$ /@ a) /. convWF$ /. yukWF$ /. ckmWF$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee;
   If[! FreeQ[a, CKM | IndexSum], Print["   WARNING: CKM or IndexSum left"]];
   a = a /. {Polarization[k, -I] -> epsW, Polarization[k, I] -> epsW};
   FCReplaceMomenta[#, {k -> pt - p1}] & /@ DeleteCases[a, 0]];
KK = (4 Pi)^2;
excl$ = {V[4]};
insertWF$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelFileWF$,
    GenericModel -> modelFileWF$, ExcludeParticles -> excl$], RuleDelayed::rhs];

jTF$ = If[Length[$ScriptCommandLine] >= 2, ToExpression[$ScriptCommandLine[[2]]], 3];
{chWF$, procWF$, m1WF$, mtWF$, ckmFacWF$, nameWF$} = {{3, 3, jTF$}, {F[3, {3}]} -> {F[4, {jTF$}], V[3]}, dnMWF$[[jTF$]], MT,
   cKc[3, jTF$], "t" <> {"d", "s", "b"}[[jTF$]] <> "W"};
Print["channel ", nameWF$, ": ", procWF$, ";  masses ", {MT, m1WF$, MW}];

(* ::Section:: *)
(*Vertex*)

onShellWF$[m1_, mt_] := (FCClearScalarProducts[]; SPD[p1, p1] = m1^2; SPD[pt, pt] = mt^2; SPD[pt, p1] = (mt^2 + m1^2 - MW^2)/2;);
redWF$[x_] := Module[{r = FDS[x, q]},
   r = DiracSimplify[SUNSimplify[DotSimplify[r], SUNNToCACF -> True] /. SUNFDelta[__] -> 1];
   r = TID[r, q, ToPaVe -> True];
   r = DiracSimplify[r];
   DiracSimplify[DiracOrder[r, {p1, epsW, pt}]]];
structWF$[r_, m1_, mt_] := Module[{sp1 = Spinor[Momentum[p1, D], m1, 1], sp2 = Spinor[Momentum[pt, D], mt, 1], x, c},
   x = FCE[r] /. SPD[epsW, pt] -> SPD[epsW, p1];
   x = Expand[x /. {sp1 . GSD[epsW] . GA[7] . sp2 -> sEL$, sp1 . GSD[epsW] . GA[6] . sp2 -> sER$,
        sp1 . GA[7] . sp2 -> sSL$, sp1 . GA[6] . sp2 -> sSR$, sp1 . GSD[epsW] . sp2 -> sEL$ + sER$, sp1 . sp2 -> sSL$ + sSR$,
        sp1 . GSD[epsW] . GA[5] . sp2 -> sER$ - sEL$, sp1 . GA[5] . sp2 -> sSR$ - sSL$}];
   c = {Coefficient[x, sEL$], Coefficient[x, sER$], Coefficient[x, sSL$ SPD[epsW, p1]], Coefficient[x, sSR$ SPD[epsW, p1]]};
   If[Expand[x - c . {sEL$, sER$, sSL$ SPD[epsW, p1], sSR$ SPD[epsW, p1]}] =!= 0,
     Print["   WARNING: terms outside the four structures: ",
      Short[Expand[x - c . {sEL$, sER$, sSL$ SPD[epsW, p1], sSR$ SPD[epsW, p1]}], 3]]];
   c];
uvWF$[x_] := Simplify[SeriesCoefficient[x /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep, C0[__] -> 0, PaVe[__] -> 0} /. D -> 4 - 2 ep,
     {ep, 0, -1}] /. MZ -> MW/cw];

onShellWF$[m1WF$, mtWF$];
treeWF$ = structWF$[DiracSimplify[Total[convertWF$[CreateFeynAmp[insertWF$[CreateTopologies[0, 1 -> 2], procWF$]], {pt}, {p1, k}]] /.
     SUNFDelta[__] -> 1], m1WF$, mtWF$];
tauWF$ = Simplify[treeWF$[[1]]/ckmFacWF$];
Print["tree {FL, FR, HL, HR} over the normalization (expect {V_tj^*, 0, 0, 0}): ", Simplify[treeWF$/tauWF$], ";  normalization ",
  Simplify[tauWF$], " (e/(sqrt2 sw) up to a phase)"];
diagsWF$ = insertWF$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], procWF$];
ampWF$ = convertWF$[CreateFeynAmp[diagsWF$, GaugeRules -> {}], {pt}, {p1, k}];
Print["vertex: ", Length[ampWF$], " diagrams;  ", Round[AbsoluteTime[] - t0TF$], " s"];
redAmpWF$ = redWF$ /@ ampWF$;
vtxWF$ = Collect[#, {_A0, _B0, _C0, _PaVe}, Together] & /@ (KK structWF$[Total[redAmpWF$], m1WF$, mtWF$]/tauWF$);
Print["vertex reduced;  ", Round[AbsoluteTime[] - t0TF$], " s;  UV poles of K FR, K HL, K HR (expect {0, 0, 0}): ",
  uvWF$ /@ vtxWF$[[2 ;; 4]], ";  gauge parameters in the pole of K FL: ", Union[Cases[uvWF$[vtxWF$[[1]]], xiA | xiZ | xiW | xiG, Infinity]]];
Put[<|"channel" -> chWF$, "name" -> nameWF$, "m1" -> m1WF$, "mt" -> mtWF$, "V" -> ckmFacWF$, "tree" -> treeWF$/tauWF$, "F" -> vtxWF$|>,
  FileNameJoin[{workDirTF$, "tff_" <> ToString[jTF$] <> ".m"}]];
Print["written: work/tff_", jTF$, ".m;  ", Round[AbsoluteTime[] - t0TF$], " s"];
DeleteDirectory[modelTmpWF$, DeleteContents -> True];
