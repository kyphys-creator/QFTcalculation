(* ::Package:: *)

(* ::Title:: *)
(*Step (1) of the NLO note: the squared tree amplitudes of the two-body decays (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (1).  sum|M|^2 (summed over spins, polarizations and colours) from the FeynArts model*)
(*of SM_CKM.fr (generated/SM_CKM_FA, generate_SM_CKM.wl) against the hand values of the note's Appendix A, with all masses*)
(*and a general complex V (vR + I vI, as the CKM note's tree_ckm_feyncalc.wl):*)
(*  Z -> f fbar   : N_c gZ^2 [v^2 (MZ^2 + 2 m^2) + a^2 (MZ^2 - 4 m^2)],  gZ = e/(sw cw), v = T3 - 2 Q sw^2, a = T3*)
(*  H -> f fbar   : N_c y^2 (MH^2 - 4 m^2),  y = sqrt(2) m/vev*)
(*  W+ -> u_i dbar_j, nu_l l+ : N_c |V_ij|^2 g^2 MW^2 [1 - (x1 + x2)/2 - (x1 - x2)^2/2],  x = m^2/MW^2*)
(*  t -> d_j W+   : |V_tj|^2 (3 g^2/(2 MW^2)) [(mt^2 - m_j^2)^2 + MW^2 (mt^2 + m_j^2) - 2 MW^4]*)
(*in the model's parameters (e, sw, cw = MW/MZ, the masses; FeynArts' generic masses).  Writes results/lo_feyncalc.csv.*)
(*Batch:  wolframscript -file lo_feyncalc.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirLF$ = DirectoryName[$InputFileName];
resDirLF$ = FileNameJoin[{srcDirLF$, "results"}];
Quiet[CreateDirectory[resDirLF$]];
tmpLF$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirLF$, "generated", "SM_CKM_FA"}], FileNameJoin[{tmpLF$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{tmpLF$, "SM_CKM_FA"}], Quiet -> True];
modelLF$ = FileNameJoin[{tmpLF$, "SM_CKM_FA", "SM_CKM_FA"}];

(* field codes: F[1, {i}] nu_i, F[2, {i}] l_i, F[3, {i}] u_i, F[4, {i}] d_i, S[1] H, V[2] Z, V[3] W+ *)
massLF$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB, FCGV["MC"] -> MC,
   FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA, FCGV["MMU"] -> MMU, FCGV["Me"] -> Me};
lepLF$ = {Me, MMU, MTA}; upLF$ = {MU, MC, MT}; dnLF$ = {MD, MS, MB};
yukLF$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepLF$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upLF$[[i]]/vev, 0], yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnLF$[[i]]/vev, 0]};
ckmLF$ = {Conjugate[CKM[i_Integer, j_Integer]] :> vR[i, j] - I vI[i, j], CKM[i_Integer, j_Integer] :> vR[i, j] + I vI[i, j]};
convLF$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ,
    GaugeXi[W] -> xiW, GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[S[2, ___]] -> xiZ,
    GaugeXi[S[3, ___]] -> xiW}, massLF$];
diagsLF$[in_, out_] := Quiet[InsertFields[CreateTopologies[0, Length[in] -> Length[out]], in -> out,
    InsertionLevel -> {Particles}, Model -> modelLF$, GenericModel -> modelLF$], RuleDelayed::rhs];
ampsLF$[diags_] := Module[{a},
   a = Quiet[FCFAConvert[CreateFeynAmp[diags, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {k},
       OutgoingMomenta -> {p1, p2}, ChangeDimension -> 4, List -> True, SMP -> False, UndoChiralSplittings -> True,
       DropSumOver -> True, DropIndexSum -> False, TransversePolarizationVectors -> {}], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a /. convLF$ /. yukLF$ /. ckmLF$ /. vev -> 2 MW sw/ee];
evalLF$[x_] := Simplify[Contract[FeynAmpDenominatorExplicit[SUNSimplify[DiracSimplify[
       x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]], SUNNToCACF -> False]]] /. SUNN -> 3];
decayLF$[in_, out_, mIn_, m1_, m2_, vecs_] := Module[{a, x},
   a = ampsLF$[diagsLF$[{in}, out]];
   FCClearScalarProducts[];
   ScalarProduct[k, k] = mIn^2; ScalarProduct[p1, p1] = m1^2; ScalarProduct[p2, p2] = m2^2;
   ScalarProduct[k, p1] = (mIn^2 + m1^2 - m2^2)/2; ScalarProduct[k, p2] = (mIn^2 - m1^2 + m2^2)/2;
   ScalarProduct[p1, p2] = (mIn^2 - m1^2 - m2^2)/2;
   x = FermionSpinSum[ComplexConjugate[Total[a]] Total[a], ExtraFactor -> 1];
   x = x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
   Do[x = DoPolarizationSums[x, v], {v, vecs}];
   evalLF$[x]];

swRuleLF$ = {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ};
gLF$ = ee/sw; gZLF$ = ee/(sw cw);
zHand$[nc_, t3_, q_, m_] := nc gZLF$^2 ((t3 - 2 q sw^2)^2 (MZ^2 + 2 m^2) + t3^2 (MZ^2 - 4 m^2));
hHand$[nc_, m_] := nc (Sqrt[2] m/(2 MW sw/ee))^2 (MH^2 - 4 m^2);
wHand$[nc_, v2_, m1_, m2_] := Module[{x1 = m1^2/MW^2, x2 = m2^2/MW^2}, nc v2 gLF$^2 MW^2 (1 - (x1 + x2)/2 - (x1 - x2)^2/2)];
tHand$[v2_, mj_] := v2 3 gLF$^2/(2 MW^2) ((MT^2 - mj^2)^2 + MW^2 (MT^2 + mj^2) - 2 MW^4);
abs2LF$[i_, j_] := vR[i, j]^2 + vI[i, j]^2;

rowsLF$ = {};
checkLF$[label_, got_, want_] := Module[{d = Simplify[(got - want) /. swRuleLF$]},
   Print["  ", label, ": FeynCalc - hand = ", d, "   (expect 0)"]; AppendTo[rowsLF$, {label, ToString[InputForm[d]]}]; d];
(* Z -> f fbar: nu_e, e, u, d with their masses (symbols) *)
Do[With[{in = c[[1]], nc = c[[2]], t3 = c[[3]], q = c[[4]], m = c[[5]]},
   checkLF$["Z -> " <> c[[6]], decayLF$[V[2], {in, -in}, MZ, m, m, {k}], zHand$[nc, t3, q, m]]],
  {c, {{F[1, {1}], 1, 1/2, 0, 0, "nu_e nubar_e"}, {F[2, {3}], 1, -1/2, -1, MTA, "tau- tau+"},
       {F[3, {2}], 3, 1/2, 2/3, MC, "c cbar"}, {F[4, {3}], 3, -1/2, -1/3, MB, "b bbar"}}}];
(* H -> f fbar *)
Do[With[{in = c[[1]], nc = c[[2]], m = c[[3]]}, checkLF$["H -> " <> c[[4]], decayLF$[S[1], {in, -in}, MH, m, m, {}], hHand$[nc, m]]],
  {c, {{F[4, {3}], 3, MB, "b bbar"}, {F[2, {3}], 1, MTA, "tau- tau+"}, {F[3, {2}], 3, MC, "c cbar"}}}];
(* W+ -> u_i dbar_j (all six, general complex V) and nu_l l+ *)
Do[checkLF$["W+ -> u" <> ToString[i] <> " dbar" <> ToString[j],
   decayLF$[V[3], {F[3, {i}], -F[4, {j}]}, MW, upLF$[[i]], dnLF$[[j]], {k}], wHand$[3, abs2LF$[i, j], upLF$[[i]], dnLF$[[j]]]],
  {i, 2}, {j, 3}];
Do[checkLF$["W+ -> nu" <> ToString[l] <> " l+" <> ToString[l], decayLF$[V[3], {F[1, {l}], -F[2, {l}]}, MW, 0, lepLF$[[l]], {k}],
   wHand$[1, 1, 0, lepLF$[[l]]]], {l, 3}];
(* t -> d_j W+ *)
Do[checkLF$["t -> d" <> ToString[j] <> " W+", decayLF$[F[3, {3}], {F[4, {j}], V[3]}, MT, dnLF$[[j]], MW, {p2}],
   tHand$[abs2LF$[3, j], dnLF$[[j]]]], {j, 3}];
nz$ = Count[rowsLF$[[All, 2]], Except["0"]];
Print["channels: ", Length[rowsLF$], ";  not zero: ", nz$];
Export[FileNameJoin[{resDirLF$, "lo_feyncalc.csv"}], Prepend[rowsLF$, {"channel", "feyncalc_minus_hand"}], "CSV"];
Print["written: results/lo_feyncalc.csv"];
DeleteDirectory[tmpLF$, DeleteContents -> True];
