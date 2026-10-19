(* ::Package:: *)

(* ::Title:: *)
(*Step (2) of the Higgs note: the one-loop H -> gamma gamma, Z gamma, g g in a general R_xi gauge (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (2).  From the note's FeynArts model (generated/SM_CKM_FA, GaugeXi kept), all one-loop*)
(*diagrams of H(k) -> V1(k1) V2(k2) at particle level (CreateTopologies[1, 1 -> 2]: the 1PI triangles and bubbles and, for*)
(*Z gamma, the photon-Z mixing on the photon leg, H -> Z Z*, Z* -> gamma with the Z propagator at k2^2 = 0; no other reducible*)
(*diagram exists, as there is no tree H gamma gamma, H Z gamma or H g g vertex, and no tadpole, as there is no H H gamma gamma*)
(*vertex).  On shell, k1^2 = m1^2, k2^2 = 0, eps_i.k_i = 0, the amplitude is*)
(*    M = Fg (e1.e2) + F21 (k2.e1)(k1.e2)   (e_i the conjugated polarization vectors; terms with an epsilon tensor apart),*)
(*in A0, B0, C0 and the PaVe coefficients where the Gram determinant vanishes, with D kept, the gauge parameters as symbols, the Yukawa couplings y = sqrt(2) m/v times a tag tg[t, g] of the*)
(*fermion in the loop (each fermion loop has one Yukawa vertex, so the amplitude is linear in the tags; the boson loops carry*)
(*none).  Checks here, symbolic: the 1/eps coefficient of Fg and F21 (FeynCalc's PaVeUVPart) is 0.*)
(*Writes work/loopind_<proc>.m.  Batch:  wolframscript -file loopind_feyncalc.wl aa | za | gg*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirLI$ = DirectoryName[$InputFileName];
workDirLI$ = FileNameJoin[{srcDirLI$, "work"}];
Quiet[CreateDirectory[workDirLI$]];
t0LI$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0LI$], " s] ", s];
modelTmpLI$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirLI$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpLI$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpLI$, "SM_CKM_FA"}], Quiet -> True];
modelFileLI$ = FileNameJoin[{modelTmpLI$, "SM_CKM_FA", "SM_CKM_FA"}];

massLI$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me};
lepLI$ = {Me, MMU, MTA}; upLI$ = {MU, MC, MT}; dnLI$ = {MD, MS, MB};
yukLI$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepLI$[[i]]/vev tg[2, i], 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upLI$[[i]]/vev tg[3, i], 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnLI$[[i]]/vev tg[4, i], 0]};
ckmLI$ = {Conjugate[CKM[i_Integer, j_Integer]] :> cKc[i, j], CKM[i_Integer, j_Integer] :> cK[i, j]};
convLI$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG,
    GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
    GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1},
   massLI$];
sumOverLI$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];

procLI$ = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], "aa"];
{fieldsLI$, m1LI$} = Switch[procLI$, "aa", {{V[1], V[1]}, 0}, "za", {{V[2], V[1]}, MZ}, "gg", {{V[4], V[4]}, 0}];
Print["H -> ", procLI$, ": ", fieldsLI$, ", k1^2 = ", m1LI$^2];

topsLI$ = CreateTopologies[1, 1 -> 2];
diagsLI$ = Quiet[InsertFields[topsLI$, {S[1]} -> fieldsLI$, InsertionLevel -> {Particles}, Model -> modelFileLI$,
    GenericModel -> modelFileLI$], RuleDelayed::rhs];
ampLI$ = Quiet[FCFAConvert[CreateFeynAmp[diagsLI$, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {k},
    OutgoingMomenta -> {k1, k2}, LoopMomenta -> {q}, ChangeDimension -> D, List -> True, SMP -> False,
    UndoChiralSplittings -> True, DropSumOver -> False, DropIndexSum -> False, TransversePolarizationVectors -> {k1, k2}],
   RuleDelayed::rhs];
ampLI$ = ampLI$ /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
ampLI$ = (sumOverLI$ /@ ampLI$) /. convLI$ /. yukLI$ /. ckmLI$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee;
ampLI$ = ampLI$ /. {Polarization[k1, -I, ___] -> e1, Polarization[k2, -I, ___] -> e2};
ampLI$ = FCReplaceMomenta[#, {k -> k1 + k2}] & /@ ampLI$;
nDiagLI$ = Length[ampLI$];
tick$["diagrams: " <> ToString[nDiagLI$] <> " (nonzero after the substitutions: " <> ToString[Count[ampLI$, Except[0]]] <> ")"];
If[! FreeQ[ampLI$, Polarization], Print["  WARNING: a polarization vector was not replaced"]];

FCClearScalarProducts[];
SPD[k1, k1] = m1LI$^2; SPD[k2, k2] = 0; SPD[k1, k2] = (MH^2 - m1LI$^2)/2;
SPD[k1, e1] = 0; SPD[k2, e2] = 0;

redLI$[x_] := Module[{r = x},
   r = r /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
   r = SUNSimplify[r, SUNNToCACF -> False] /. SUNN -> 3;
   r = DiracSimplify[r];
   r = FDS[r, q];
   r = TID[r, q, ToPaVe -> True];
   r = ExpandScalarProduct[Contract[r]];
   FCE[r]];
partsLI$ = Table[Module[{r = redLI$[ampLI$[[i]]]},
    If[Mod[i, 10] == 0, tick$["reduced " <> ToString[i] <> "/" <> ToString[nDiagLI$]]]; r], {i, nDiagLI$}];
totLI$ = Expand[Total[partsLI$] /. {SUNDelta[__] -> 1, SUNFDelta[__] -> 1}];
(* the photon-Z mixing diagram: its Z propagator at k2^2 = 0, and the fermion traces of the mixing with gamma5 left by NDR,
   Tr[k2slash e2slash k2slash e1slash gamma5], which vanish with k2^2 = k2.e2 = 0 *)
totLI$ = totLI$ /. DiracTrace[x_] :> DiracTrace[DiracSimplify[x], DiracTraceEvaluate -> True];
totLI$ = Expand[FCE[ExpandScalarProduct[FeynAmpDenominatorExplicit[totLI$]]]];
If[! FreeQ[totLI$, DiracTrace | FeynAmpDenominator | FAD], Print["  WARNING: a trace or a propagator is left"]];
tick$["reduced all"];

fgLI$ = Coefficient[totLI$, SPD[e1, e2]];
f21LI$ = Coefficient[totLI$, SPD[e1, k2] SPD[e2, k1]];
restLI$ = Expand[totLI$ - fgLI$ SPD[e1, e2] - f21LI$ SPD[e1, k2] SPD[e2, k1]];
fgLI$ = Collect[fgLI$ /. {SPD[e1, e2] -> 0}, {A0[__], B0[__], C0[__], PaVe[__]}, Together];
f21LI$ = Collect[f21LI$, {A0[__], B0[__], C0[__], PaVe[__]}, Together];
Print["  left over (epsilon tensor or other structures): ", If[restLI$ === 0, 0, Short[restLI$, 5]]];

(* the UV pole of all the PaVe functions (TID leaves B1, B00, ... where the Gram determinant vanishes, p^2 = k2^2 = 0) *)
uvLI$[x_] := Simplify[(Together[(D - 4) PaVeUVPart[x]] /. D -> 4) /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}];
uvFg$ = uvLI$[fgLI$]; uvF21$ = uvLI$[f21LI$];
Print["  1/eps coefficient of Fg: ", uvFg$, ";  of F21: ", uvF21$, "   (expect 0)"];
Print["  gauge parameters in Fg: ", Union[Cases[fgLI$, xiA | xiZ | xiW | xiG, Infinity]], ", in F21: ", Union[Cases[f21LI$, xiA | xiZ | xiW | xiG, Infinity]],
  ";  tags: ", Union[Cases[fgLI$, tg[__], Infinity]]];
Put[{"proc" -> procLI$, "m1" -> m1LI$, "nDiagrams" -> nDiagLI$, "Fg" -> fgLI$, "F21" -> f21LI$, "rest" -> restLI$,
   "uvFg" -> uvFg$, "uvF21" -> uvF21$}, FileNameJoin[{workDirLI$, "loopind_" <> procLI$ <> ".m"}]];
tick$["written: work/loopind_" <> procLI$ <> ".m"];
DeleteDirectory[modelTmpLI$, DeleteContents -> True];
