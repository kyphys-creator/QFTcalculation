(* ::Package:: *)

(* ::Title:: *)
(*Step (4b) of the NLO note: the electroweak one-loop vertex W+ -> f fbar' with a massless photon (general R_xi)*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (4b).  The 1PI vertex of W+(k) -> f(p1) fbar'(p2) from the note's FeynArts model at particle*)
(*level, all loops but the gluon (V[4] excluded; its part is the alpha_s/pi of step (2)), the photon massless: its infrared*)
(*divergence is left to dimensional regularization (Package-X in wweak.wl), as in steps (2), (3).  Channels (command line):*)
(*  1 g    : W+ -> nu_g l+_g;   3 i j : W+ -> u_i dbar_j.*)
(*On shell: k^2 = MW^2, p1^2 = m1^2, p2^2 = m2^2, eps.k = 0; written as the CKM note's wud_vertex_feyncalc.wl does,*)
(*  M = (e/(sqrt2 sw)) ubar(p1) [ epsslash (FL P_L + FR P_R) + (eps.p1) (HL P_L + HR P_R) ] v(p2),  tree FL = V_ij (1 for leptons),*)
(*K = 16 pi^2 times the form factors in A0, B0, C0 with D kept.  Checks: the tree against V_ij gamma P_L; HL, HR, FR UV-finite.*)
(*Writes work/wff_<t><i><j>.m.  Batch:  wolframscript -file wff_feyncalc.wl 1 g  |  3 i j*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirWF$ = DirectoryName[$InputFileName];
workDirWF$ = FileNameJoin[{srcDirWF$, "work"}];
Quiet[CreateDirectory[workDirWF$]];
t0WF$ = AbsoluteTime[];
modelTmpWF$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirWF$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpWF$, "SM_CKM_FA"}]];
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
   a = a /. Polarization[k, I] -> epsW;
   FCReplaceMomenta[#, {k -> p1 + p2}] & /@ DeleteCases[a, 0]];
KK = (4 Pi)^2;
excl$ = {V[4]};
insertWF$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelFileWF$,
    GenericModel -> modelFileWF$, ExcludeParticles -> excl$], RuleDelayed::rhs];

argsWF$ = If[Length[$ScriptCommandLine] >= 3, ToExpression /@ Rest[$ScriptCommandLine], {3, 2, 3}];
{chWF$, procWF$, m1WF$, m2WF$, ckmFacWF$, nameWF$} = If[argsWF$[[1]] == 1,
   With[{g = argsWF$[[2]]}, {{1, g}, {V[3]} -> {F[1, {g}], -F[2, {g}]}, 0, lepMWF$[[g]], 1, "lnu" <> ToString[g]}],
   With[{i = argsWF$[[2]], j = argsWF$[[3]]}, {{3, i, j}, {V[3]} -> {F[3, {i}], -F[4, {j}]}, upMWF$[[i]], dnMWF$[[j]], cK[i, j],
     {"u", "c"}[[i]] <> {"d", "s", "b"}[[j]]}]];
Print["channel ", nameWF$, ": ", procWF$, ";  masses ", {m1WF$, m2WF$}];

(* ::Section:: *)
(*Vertex*)

onShellWF$[m1_, m2_] := (FCClearScalarProducts[]; SPD[p1, p1] = m1^2; SPD[p2, p2] = m2^2; SPD[p1, p2] = (MW^2 - m1^2 - m2^2)/2;);
redWF$[x_] := Module[{r = FDS[x, q]},
   r = DiracSimplify[SUNSimplify[DotSimplify[r], SUNNToCACF -> True] /. SUNFDelta[__] -> 1];
   r = TID[r, q, ToPaVe -> True];
   r = DiracSimplify[r];
   DiracSimplify[DiracOrder[r, {p1, epsW, p2}]]];
structWF$[r_, m1_, m2_] := Module[{sp1 = Spinor[Momentum[p1, D], m1, 1], sp2 = Spinor[-Momentum[p2, D], m2, 1], x, c},
   x = FCE[r] /. SPD[epsW, p2] -> -SPD[epsW, p1];
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

onShellWF$[m1WF$, m2WF$];
treeWF$ = structWF$[DiracSimplify[Total[convertWF$[CreateFeynAmp[insertWF$[CreateTopologies[0, 1 -> 2], procWF$]], {k}, {p1, p2}]] /.
     SUNFDelta[__] -> 1], m1WF$, m2WF$];
tauWF$ = Simplify[treeWF$[[1]]/ckmFacWF$];
Print["tree {FL, FR, HL, HR} over the normalization (expect {V, 0, 0, 0}): ", Simplify[treeWF$/tauWF$], ";  normalization ",
  Simplify[tauWF$], " (e/(sqrt2 sw) up to a phase)"];
diagsWF$ = insertWF$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], procWF$];
ampWF$ = convertWF$[CreateFeynAmp[diagsWF$, GaugeRules -> {}], {k}, {p1, p2}];
Print["vertex: ", Length[ampWF$], " diagrams;  ", Round[AbsoluteTime[] - t0WF$], " s"];
redAmpWF$ = redWF$ /@ ampWF$;
vtxWF$ = Collect[#, {_A0, _B0, _C0, _PaVe}, Together] & /@ (KK structWF$[Total[redAmpWF$], m1WF$, m2WF$]/tauWF$);
Print["vertex reduced;  ", Round[AbsoluteTime[] - t0WF$], " s;  UV poles of K FR, K HL, K HR (expect {0, 0, 0}): ",
  uvWF$ /@ vtxWF$[[2 ;; 4]], ";  gauge parameters in the pole of K FL: ", Union[Cases[uvWF$[vtxWF$[[1]]], xiA | xiZ | xiW | xiG, Infinity]]];
Put[<|"channel" -> chWF$, "name" -> nameWF$, "m1" -> m1WF$, "m2" -> m2WF$, "V" -> ckmFacWF$, "tree" -> treeWF$/tauWF$, "F" -> vtxWF$|>,
  FileNameJoin[{workDirWF$, "wff_" <> StringJoin[ToString /@ chWF$] <> ".m"}]];
Print["written: work/wff_", StringJoin[ToString /@ chWF$], ".m;  ", Round[AbsoluteTime[] - t0WF$], " s"];
DeleteDirectory[modelTmpWF$, DeleteContents -> True];
