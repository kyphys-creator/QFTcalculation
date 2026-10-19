(* ::Package:: *)

(* ::Title:: *)
(*Step (1) of the Higgs note: the squared tree amplitudes of H -> f fbar, H -> V f fbar' and H -> 4 f (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (1).  sum|M|^2 (summed over spins, polarizations and colours) from the note's FeynArts*)
(*model of SM_CKM.fr (generated/SM_CKM_FA, generate_SM_CKM.wl) against the hand forms of the note's Appendix A:*)
(*  H -> f fbar        : N_c y^2 (MH^2 - 4 m^2), the Yukawa coupling y and the kinematic mass m as independent symbols;*)
(*  H -> V(p1) f(p2) fbar'(p3), in the general R_xi gauge with all masses (y = sqrt(2) m/vev, the tree relation that the*)
(*                       gauge cancellation needs): no xiW, xiZ;  at m_f = 0*)
(*                       N_c g_HVV^2 (cL^2 + cR^2) [s23 + 4 (p1.p2)(p1.p3)/MV^2]/(s23 - MV^2)^2,  s_ij = (p_i + p_j)^2;*)
(*  H -> f1(p1) fbar2(p2) f3(p3) fbar4(p4), m_f = 0, general R_xi:*)
(*                       16 N_c1 N_c3 g_HVV^2 [(cL1^2 cL3^2 + cR1^2 cR3^2)(p1.p3)(p2.p4) + (cL1^2 cR3^2 + cR1^2 cL3^2)(p1.p4)(p2.p3)]*)
(*                       / [(s12 - MV^2)(s34 - MV^2)]^2,*)
(*with g_HWW = g MW, g_HZZ = gZ MZ (g = e/sw, gZ = e/(sw cw), cw = MW/MZ), the W couplings cL = g V/sqrt(2), cR = 0 and the Z*)
(*couplings cL = gZ (T3 - Q sw^2), cR = -gZ Q sw^2.  Writes results/lo_feyncalc.csv and work/me_hvff.txt: the sum|M|^2 of*)
(*H -> V f fbar' with the masses, in Feynman gauge, |V| = 1, in CForm in s12, s13 (for lo_mg5.py).*)
(*Batch:  wolframscript -file lo_feyncalc.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirLF$ = DirectoryName[$InputFileName];
resDirLF$ = FileNameJoin[{srcDirLF$, "results"}];
workDirLF$ = FileNameJoin[{srcDirLF$, "work"}];
Quiet[CreateDirectory /@ {resDirLF$, workDirLF$}];
tmpLF$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirLF$, "generated", "SM_CKM_FA"}], FileNameJoin[{tmpLF$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{tmpLF$, "SM_CKM_FA"}], Quiet -> True];
modelLF$ = FileNameJoin[{tmpLF$, "SM_CKM_FA", "SM_CKM_FA"}];

(* field codes: F[1, {i}] nu_i, F[2, {i}] l_i, F[3, {i}] u_i, F[4, {i}] d_i, S[1] H, V[2] Z, V[3] W+ *)
massLF$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB, FCGV["MC"] -> MC,
   FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA, FCGV["MMU"] -> MMU, FCGV["Me"] -> Me};
lepLF$ = {Me, MMU, MTA}; upLF$ = {MU, MC, MT}; dnLF$ = {MD, MS, MB};
(* y = sqrt(2) m/vev (the tree relation), or the Yukawa couplings as their own symbols yL[i], yU[i], yD[i] *)
yukTreeLF$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepLF$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upLF$[[i]]/vev, 0], yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnLF$[[i]]/vev, 0]};
yukSymLF$ = {yl[i_Integer, j_Integer] :> If[i == j, yL[i], 0], yu[i_Integer, j_Integer] :> If[i == j, yU[i], 0],
   yd[i_Integer, j_Integer] :> If[i == j, yD[i], 0]};
ckmLF$ = {Conjugate[CKM[i_Integer, j_Integer]] :> vR[i, j] - I vI[i, j], CKM[i_Integer, j_Integer] :> vR[i, j] + I vI[i, j]};
convLF$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ,
    GaugeXi[W] -> xiW, GaugeXi[G] -> xiG, GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[S[1, ___]] -> 1}, massLF$];
diagsLF$[in_, out_] := Quiet[InsertFields[CreateTopologies[0, Length[in] -> Length[out]], in -> out,
    InsertionLevel -> {Particles}, Model -> modelLF$, GenericModel -> modelLF$], RuleDelayed::rhs];
outMomLF$ = {p1, p2, p3, p4};
ampsLF$[diags_, nout_, yuk_] := Module[{a},
   a = Quiet[FCFAConvert[CreateFeynAmp[diags, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {k},
       OutgoingMomenta -> Take[outMomLF$, nout], ChangeDimension -> 4, List -> True, SMP -> False, UndoChiralSplittings -> True,
       DropSumOver -> True, DropIndexSum -> False, TransversePolarizationVectors -> {}], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a /. convLF$ /. yuk /. ckmLF$ /. vev -> 2 MW sw/ee];
evalLF$[x_] := Contract[FeynAmpDenominatorExplicit[SUNSimplify[DiracSimplify[
      x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]], SUNNToCACF -> False]]] /. SUNN -> 3;
squareLF$[a_, vecs_] := Module[{x},
   x = FermionSpinSum[ComplexConjugate[Total[a]] Total[a], ExtraFactor -> 1];
   x = x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
   Do[x = DoPolarizationSums[x, v], {v, vecs}];
   evalLF$[x]];
(* two-body: k -> p1 p2 *)
decay2LF$[in_, out_, mIn_, m1_, m2_, yuk_] := Module[{a},
   a = ampsLF$[diagsLF$[{in}, out], 2, yuk];
   FCClearScalarProducts[];
   ScalarProduct[k, k] = mIn^2; ScalarProduct[p1, p1] = m1^2; ScalarProduct[p2, p2] = m2^2;
   ScalarProduct[k, p1] = (mIn^2 + m1^2 - m2^2)/2; ScalarProduct[k, p2] = (mIn^2 - m1^2 + m2^2)/2;
   ScalarProduct[p1, p2] = (mIn^2 - m1^2 - m2^2)/2;
   Together[squareLF$[a, {}]]];
(* three-body: k -> V(p1) f(p2) fbar'(p3) in s12 = (p1 + p2)^2, s13 = (p1 + p3)^2 *)
s23LF$[mIn_, m1_, m2_, m3_] := mIn^2 + m1^2 + m2^2 + m3^2 - s12 - s13;
decay3LF$[in_, out_, mIn_, {m1_, m2_, m3_}] := Module[{a, pp12, pp13, pp23},
   a = ampsLF$[diagsLF$[{in}, out], 3, yukTreeLF$];
   Print["    ", Length[a], " diagrams"];
   FCClearScalarProducts[];
   pp12 = (s12 - m1^2 - m2^2)/2; pp13 = (s13 - m1^2 - m3^2)/2; pp23 = (s23LF$[mIn, m1, m2, m3] - m2^2 - m3^2)/2;
   ScalarProduct[p1, p1] = m1^2; ScalarProduct[p2, p2] = m2^2; ScalarProduct[p3, p3] = m3^2;
   ScalarProduct[p1, p2] = pp12; ScalarProduct[p1, p3] = pp13; ScalarProduct[p2, p3] = pp23;
   ScalarProduct[k, p1] = m1^2 + pp12 + pp13; ScalarProduct[k, p2] = pp12 + m2^2 + pp23; ScalarProduct[k, p3] = pp13 + pp23 + m3^2;
   ScalarProduct[k, k] = mIn^2;
   Together[squareLF$[a, {p1}]]];
(* four-body, massless: k -> p1 p2 p3 p4 with k = p1 + p2 + p3 + p4 and the p_i.p_j left as symbols *)
decay4LF$[in_, out_] := Module[{a},
   a = ampsLF$[diagsLF$[{in}, out], 4, yukTreeLF$] /. {Me -> 0, MMU -> 0};   (* the spinor masses come as the bare symbols *)
   Print["    ", Length[a], " diagrams"];
   a = MomentumExpand[a /. Momentum[k, d___] :> Momentum[p1, d] + Momentum[p2, d] + Momentum[p3, d] + Momentum[p4, d]];
   FCClearScalarProducts[];
   Do[ScalarProduct[p, p] = 0, {p, outMomLF$}];
   Together[ExpandScalarProduct[squareLF$[a, {}]]]];

swRuleLF$ = {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ};
gLF$ = ee/sw; gZLF$ = ee/(sw cw);
gHWWLF$ = gLF$ MW; gHZZLF$ = gZLF$ MZ;
cZLF$[t3_, q_] := {gZLF$ (t3 - q sw^2), -gZLF$ q sw^2};
cWLF$ = {gLF$/Sqrt[2], 0};
hand2LF$[nc_, y_, m_] := nc y^2 (MH^2 - 4 m^2);
hand3LF$[nc_, gH_, {cL_, cR_}, mV_] := Module[{s23 = s23LF$[MH, mV, 0, 0]},
   nc gH^2 (cL^2 + cR^2) (s23 + 4 ((s12 - mV^2)/2) ((s13 - mV^2)/2)/mV^2)/(s23 - mV^2)^2];
hand4LF$[nc1_, nc3_, gH_, {c1L_, c1R_}, {c3L_, c3R_}, mV_] :=
  FCI[16 nc1 nc3 gH^2 ((c1L^2 c3L^2 + c1R^2 c3R^2) SP[p1, p3] SP[p2, p4] + (c1L^2 c3R^2 + c1R^2 c3L^2) SP[p1, p4] SP[p2, p3])/
   ((2 SP[p1, p2] - mV^2) (2 SP[p3, p4] - mV^2))^2];

rowsLF$ = {};
zeroQLF$[x_] := Module[{t = Together[x /. swRuleLF$]}, If[t === 0, 0, Simplify[t]]];
checkLF$[label_, what_, d_] := (Print["  ", label, ", ", what, ": ", d, "   (expect 0)"];
   AppendTo[rowsLF$, {label, what, ToString[InputForm[d]]}]; d);
exportLF$ = {};

(* H -> f fbar with the Yukawa coupling and the mass as independent symbols *)
Print["H -> f fbar:"];
Do[With[{f = c[[1]], nc = c[[2]], y = c[[3]], m = c[[4]]},
   checkLF$["H -> " <> c[[5]], "FeynCalc - hand",
    zeroQLF$[decay2LF$[S[1], {f, -f}, MH, m, m, yukSymLF$] - hand2LF$[nc, y, m]]]],
  {c, {{F[4, {3}], 3, yD[3], MB, "b bbar"}, {F[3, {2}], 3, yU[2], MC, "c cbar"}, {F[2, {3}], 1, yL[3], MTA, "tau- tau+"},
       {F[2, {2}], 1, yL[2], MMU, "mu- mu+"}}}];

(* H -> V f fbar' with the masses, general R_xi *)
Print["H -> V f fbar':"];
ch3LF$ = {
   (* label, final state, V mass, {m_f, m_fbar'}, N_c, g_HVV, {cL, cR} (|V| = 1), |V|^2, the masses that vanish in the limit *)
   {"W+ e- nuebar", {V[3], F[2, {1}], -F[1, {1}]}, MW, {Me, 0}, 1, gHWWLF$, cWLF$, 1, {Me}},
   {"W+ tau- nutaubar", {V[3], F[2, {3}], -F[1, {3}]}, MW, {MTA, 0}, 1, gHWWLF$, cWLF$, 1, {MTA}},
   {"W+ b cbar", {V[3], F[4, {3}], -F[3, {2}]}, MW, {MB, MC}, 3, gHWWLF$, cWLF$, vR[2, 3]^2 + vI[2, 3]^2, {MB, MC}},
   {"Z nue nuebar", {V[2], F[1, {1}], -F[1, {1}]}, MZ, {0, 0}, 1, gHZZLF$, cZLF$[1/2, 0], 1, {}},
   {"Z tau- tau+", {V[2], F[2, {3}], -F[2, {3}]}, MZ, {MTA, MTA}, 1, gHZZLF$, cZLF$[-1/2, -1], 1, {MTA}},
   {"Z b bbar", {V[2], F[4, {3}], -F[4, {3}]}, MZ, {MB, MB}, 3, gHZZLF$, cZLF$[-1/2, -1/3], 1, {MB}}};
Do[Module[{lab = c[[1]], res, v2 = c[[8]], hand0},
   Print["  H -> ", lab, ":"];
   res = decay3LF$[S[1], c[[2]], MH, {c[[3]], c[[4, 1]], c[[4, 2]]}];
   checkLF$["H -> " <> lab, "d/d xiW", zeroQLF$[D[res, xiW]]];
   checkLF$["H -> " <> lab, "d/d xiZ", zeroQLF$[D[res, xiZ]]];
   If[v2 =!= 1, checkLF$["H -> " <> lab, "d/d vR of sum|M|^2/|V|^2", zeroQLF$[D[res/v2, vR[2, 3]]]]];
   hand0 = hand3LF$[c[[5]], c[[6]], c[[7]], c[[3]]] v2;
   checkLF$["H -> " <> lab, "FeynCalc - hand at m_f = 0", zeroQLF$[(res /. Thread[c[[9]] -> 0]) - hand0]];
   AppendTo[exportLF$, lab -> Together[(res /. {xiW -> 1, xiZ -> 1, vR[2, 3] -> 1, vI[2, 3] -> 0}) /. swRuleLF$]]],
  {c, ch3LF$}];

(* H -> 4 f, massless *)
Print["H -> 4 f (massless):"];
massLF$ = Join[massLF$, {FCGV["Me"] -> 0, FCGV["MMU"] -> 0}];
convLF$ = Join[DeleteCases[convLF$, FCGV["Me" | "MMU"] -> _], {FCGV["Me"] -> 0, FCGV["MMU"] -> 0}];
lepLF$ = {0, 0, MTA};
yukTreeLF$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepLF$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upLF$[[i]]/vev, 0], yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnLF$[[i]]/vev, 0]};
Module[{res},
  Print["  H -> nue e+ mu- numubar (W+ W-):"];
  res = decay4LF$[S[1], {F[1, {1}], -F[2, {1}], F[2, {2}], -F[1, {2}]}];
  checkLF$["H -> nue e+ mu- numubar", "d/d xiW", zeroQLF$[D[res, xiW]]];
  checkLF$["H -> nue e+ mu- numubar", "FeynCalc - hand", zeroQLF$[res - hand4LF$[1, 1, gHWWLF$, cWLF$, cWLF$, MW]]];
  Print["  H -> e- e+ mu- mu+ (Z Z):"];
  res = decay4LF$[S[1], {F[2, {1}], -F[2, {1}], F[2, {2}], -F[2, {2}]}];
  checkLF$["H -> e- e+ mu- mu+", "d/d xiZ", zeroQLF$[D[res, xiZ]]];
  checkLF$["H -> e- e+ mu- mu+", "FeynCalc - hand",
   zeroQLF$[res - hand4LF$[1, 1, gHZZLF$, cZLF$[-1/2, -1], cZLF$[-1/2, -1], MZ]]]];

nz$ = Count[rowsLF$[[All, 3]], Except["0"]];
Print["checks: ", Length[rowsLF$], ";  not zero: ", nz$];
Export[FileNameJoin[{resDirLF$, "lo_feyncalc.csv"}], Prepend[rowsLF$, {"channel", "check", "result"}], "CSV"];
Export[FileNameJoin[{workDirLF$, "me_hvff.txt"}],
  StringRiffle[(#[[1]] <> "|" <> ToString[CForm[#[[2]]]]) & /@ exportLF$, "\n"] <> "\n", "Text"];
Print["written: results/lo_feyncalc.csv, work/me_hvff.txt"];
DeleteDirectory[tmpLF$, DeleteContents -> True];
