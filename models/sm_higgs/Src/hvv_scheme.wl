(* ::Package:: *)

(* ::Title:: *)
(*Step (7) of the Higgs note: H -> V V* with the FJ v against G_F, and the tadpole of the H H V V vertex*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (7).  The tree of H -> V V* depends on the couplings through X_V = g_HVV^2 g_V^2/M_V^2*)
(*(Eq. (vv); the pole M_V in the kinematics).  With the SM note's one-loop relations of its M_W-scheme fit (FJ tadpoles),*)
(*  v^2 = v_G^2 (1 + DeltaHat),  g^2 = g0^2 (1 + dW - DeltaHat),  g_Z^2 = G0^2 (1 + dZ - DeltaHat),  M_V^2(MS) = M_V^2 (1 + dV),*)
(*the MS-bar tree X_V = g_V^4 (1 + dV) against the G_mu tree G_V0^4 gives the ratio, at one loop,*)
(*  R_V = (1 + dV - DeltaHat)^2 (1 + dV) = 1 + 3 dV - 2 DeltaHat,*)
(*(for Z also the s^2 of delta'_Z: c-hat^2 = c0^2 (1 + dW - dZ)).  The tadpole parts: dV_tad = Sigma_T^VV,tad/M_V^2 is the same*)
(*for W and Z and in DeltaHat (a constant: it cancels in dV - DeltaHat), so the tadpole part of R_V - 1 is dV_tad once.*)
(*  (a) symbolic, in the note's FeynArts model (general R_xi, all masses): the H H V V vertex with a tadpole attached (the*)
(*      tadpole topologies of H -> W+ W-, Z Z without the external legs) over the tree, delta_A^tad, against -dV_tad/2 from the*)
(*      SM note's Sigma^WW, Sigma^ZZ tadpole parts: 2 delta_A^tad + dV_tad = 0, so that in the MS-bar NLO amplitude this diagram*)
(*      removes the tadpole part of the tree difference;*)
(*  (b) numbers at mu = M_t (the point of the SM note's fit; the note's v_FJ is fitted there): dW, dZ, DeltaHat with their*)
(*      tadpole parts (the NLO note's scheme.wl: Package-X, the tree point of the fit), the exact tree ratio R_V of the fitted*)
(*      g, g', v_FJ, the one-loop R_V, and R_V (1 + 2 delta_A^tad) against its tadpole-free one-loop part 3 dV_nt - 2 DeltaHat_nt.*)
(*Writes results/hvv_scheme.csv.  Batch:  wolframscript -file hvv_scheme.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
$MaxExtraPrecision = 200;
srcDirVS$ = DirectoryName[$InputFileName];
resDirVS$ = FileNameJoin[{srcDirVS$, "results"}];
smSrcVS$ = FileNameJoin[{srcDirVS$, "..", "..", "sm", "Src"}];
t0VS$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0VS$], " s] ", s];
KK = 16 Pi^2;

(* ::Section:: *)
(*(a) The tadpole of the H H V V vertex in the note's model*)

modelTmpVS$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirVS$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpVS$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpVS$, "SM_CKM_FA"}], Quiet -> True];
modelVS$ = FileNameJoin[{modelTmpVS$, "SM_CKM_FA", "SM_CKM_FA"}];
lepVS$ = {Me, MMU, MTA}; upVS$ = {MU, MC, MT}; dnVS$ = {MD, MS, MB};
yukVS$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepVS$[[i]]/vev, 0], yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upVS$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnVS$[[i]]/vev, 0]};
convVS$ = {FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT,
   FCGV["MB"] -> MB, FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA, FCGV["MMU"] -> MMU,
   FCGV["Me"] -> Me, GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG, GaugeXi[V[1, ___]] -> xiA,
   GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG, GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW,
   GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ, GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG,
   GaugeXi[S[1, ___]] -> 1, Conjugate[CKM[i_, j_]] :> cKc[i, j], CKM[i_, j_] :> cK[i, j]};
ampVS$[d_, loop_] := Module[{a},
   a = Quiet[FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {k}, OutgoingMomenta -> {p1, p2},
       LoopMomenta -> loop, ChangeDimension -> D, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> False,
       TransversePolarizationVectors -> {p1, p2}], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   (* a sum over an index that appears nowhere else (the colour of a closed quark loop) is its range *)
   a = (# /. SumOver[i_, n_, ___] :> If[FreeQ[# /. SumOver[__] -> 1, i], n, 1]) & /@ a;
   a /. convVS$ /. yukVS$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee];
insVS$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelVS$, GenericModel -> modelVS$],
   RuleDelayed::rhs];
(* the coefficient of e1.e2 (the polarization vectors of the two V) *)
coefVS$[x_] := Coefficient[Expand[FCE[Contract[x]] /. {Polarization[p1, -I, ___] -> e1, Polarization[p2, -I, ___] -> e2}], SPD[e1, e2]];
tadVS$ = Association[Table[v -> Module[{proc, tree, all, noTad, ta, tr},
      proc = {S[1]} -> If[v === "W", {V[3], -V[3]}, {V[2], V[2]}];
      FCClearScalarProducts[];
      SPD[p1, p1] = If[v === "W", MW^2, MZ^2]; SPD[p2, p2] = If[v === "W", MW^2, MZ^2];
      SPD[p1, p2] = (MH^2 - 2 If[v === "W", MW^2, MZ^2])/2;
      tree = ampVS$[insVS$[CreateTopologies[0, 1 -> 2], proc], {}];
      (* the reducible one-loop topologies without the external-leg corrections: the tadpoles on the vertex *)
      all = ampVS$[insVS$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {WFCorrections, Irreducible}], proc], {q}];
      Print["H -> ", v, " ", v, ": ", Length[all], " tadpole diagrams of the vertex"];
      (* the H line at zero momentum to the tadpole: -1/MH^2; the fermion traces first *)
      ta = Total[all] /. FeynAmpDenominator[PropagatorDenominator[0, m_]] :> -1/m^2;
      ta = DiracSimplify[ta /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]];
      ta = Contract[TID[FDS[ta, q], q, ToPaVe -> True]] /. {A0[0] -> 0};
      tr = coefVS$[Total[tree]];
      Simplify[KK coefVS$[ta]/tr]], {v, {"W", "Z"}}]];
DeleteDirectory[modelTmpVS$, DeleteContents -> True];
tick$["tadpole vertices"];
sigVS$ = Association[Get[FileNameJoin[{smSrcVS$, "results", "oneloop_sigma.m"}]]];
kRuleVS$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
wwTad$ = sigVS$["WW"][[2]] /. kRuleVS$; zzTad$ = sigVS$["ZZ"][[2]] /. kRuleVS$;
toSwVS$[x_] := x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2];
Print["the tadpole parts of Sigma^WW, Sigma^ZZ depend on k^2: ", ! FreeQ[{wwTad$, zzTad$}, kk2], " (expect False)"];
chkW$ = Simplify[toSwVS$[2 tadVS$["W"] + wwTad$/MW^2]];
chkZ$ = Simplify[toSwVS$[2 tadVS$["Z"] + zzTad$/MZ^2]];
Print["(a) K (2 delta_A^tad + dV_tad): W ", chkW$, ",  Z ", chkZ$, "   (expect 0, 0)"];
Print["    dW_tad - dZ_tad: ", Simplify[toSwVS$[wwTad$/MW^2 - zzTad$/MZ^2]], "  (expect 0)"];
tick$["(a)"];

(* ::Section:: *)
(*(b) The numbers at mu = M_t (the NLO note's scheme.wl)*)

pxCache$ = <||>;
pxVal$[f_, mu_] := Module[{key = {f, mu}, r, y},
   If[KeyExistsQ[pxCache$, key], Return[pxCache$[key]]];
   r = PaXEvaluate[f, PaXC0Expand -> True] /. ConditionalExpression[a_, _] :> a;
   y = Normal[Series[N[r /. ScaleMu -> N[Sqrt[Pi Exp[EulerGamma]] mu, 60] /. EulerGamma -> N[EulerGamma, 60], 60], {Epsilon, 0, 0}]];
   pxCache$[key] = {Coefficient[y, Epsilon, -1], Coefficient[Expand[y], Epsilon, 0]}];
numeric$[x_, mu_] := Module[{fs, vals, y},
   fs = Union[Cases[x, A0[__] | B0[__] | PaVe[__], Infinity]];
   vals = (#[[1]]/ep + #[[2]]) & /@ (pxVal$[#, mu] & /@ fs);
   y = Expand[Normal[Series[x /. Thread[fs -> vals] /. D -> 4 - 2 ep, {ep, 0, 0}]]];
   N[{Coefficient[y, ep, -1], Coefficient[y, ep, 0]}, 40]];
dHatK$ = Get[FileNameJoin[{smSrcVS$, "results", "mudecay_deltahat_finite.m"}]];
lightVS$ = With[{c = 246.21965/Sqrt[2]}, {MB -> 0.015480097 c, MC -> 0.0033820038 c, MS -> 0.00029094484 c,
    MD -> 1.4609792*^-5 c, MU -> 6.7227779*^-6 c, MTA -> 0.0099944422 c, MMU -> 0.00058837986 c, Me -> 2.7929820*^-6 c}] /.
   (m_ -> x_) :> (m -> Rationalize[x, 0]);
limitMA$[x_] := Module[{y = x /. xiA -> 1, fs, cs, c0},
   fs = Union[Cases[y, A0[__] | B0[__] | PaVe[__], Infinity]];
   y = Expand[y /. Thread[fs -> Array[lf$, Length[fs]]]];
   cs = Together[Coefficient[y, lf$[#]]] & /@ Range[Length[fs]];
   c0 = Together[y /. lf$[_] -> 0];
   (Append[cs, c0] /. MA -> 0) . Append[fs /. MA -> 0, 1] /. {A0[0] -> 0, B0[0, 0, 0] -> 0}];
wwAll$ = limitMA$[toSwVS$[Total[sigVS$["WW"]] /. kRuleVS$]];
zzAll$ = limitMA$[toSwVS$[Total[sigVS$["ZZ"]] /. kRuleVS$]];
wwT$ = limitMA$[toSwVS$[wwTad$]];
GF$ = 11663788/10^12; vG$ = 1/Sqrt[Sqrt[2] GF$];
rat$[x_] := Rationalize[N[x, 40], 10^-35];
mw$ = rat$[803692/10000/Sqrt[1 + (2085/1000)^2/(803692/10000)^2]];
mz$ = rat$[91188/1000/Sqrt[1 + (24955/10000)^2/(91188/1000)^2]];
s0$ = rat$[Sqrt[1 - mw$^2/mz$^2]];
tree$ = Join[{ee -> rat$[2 mw$ s0$/vG$], sw -> s0$, MW -> mw$, MT -> 17257/100, MH -> 12520/100, xiZ -> 1, xiW -> 1}, lightVS$];
muT$ = 17257/100;
dW$ = Re[numeric$[wwAll$ /. kk2 -> mw$^2 /. tree$, muT$][[2]]]/mw$^2/KK;
dZ$ = Re[numeric$[zzAll$ /. kk2 -> mz$^2 /. tree$, muT$][[2]]]/mz$^2/KK;
dT$ = Re[numeric$[wwT$ /. tree$, muT$][[2]]]/mw$^2/KK;
dH$ = Re[N[dHatK$ /. tree$ /. mu -> muT$, 40]]/KK;
Print["(b) mu = M_t:  dW = ", N[dW$, 10], ", dZ = ", N[dZ$, 10], ", DeltaHat = ", N[dH$, 10], ";  the tadpole part dV_tad = ", N[dT$, 10]];
Print["    without the tadpoles: dW_nt = ", N[dW$ - dT$, 10], ", dZ_nt = ", N[dZ$ - dT$, 10], ", DeltaHat_nt = ", N[dH$ - dT$, 10]];
(* the fitted MS-bar values at M_t (the SM note's PDG 2024 M_W-scheme fit): g2, gY, v_FJ *)
fitRow$ = SelectFirst[Import[FileNameJoin[{smSrcVS$, "results", "msbar_fit.csv"}], "CSV"], #[[1]] == "PDG2024_MW_scheme" &];
{gF$, gpF$, vF$} = Rationalize[#, 0] & /@ fitRow$[[{5, 6, 8}]];
g0sq$ = 4 Sqrt[2] GF$ mw$^2; G0sq$ = 4 Sqrt[2] GF$ mz$^2; c0sq$ = mw$^2/mz$^2;
dpZ$[s2_] := 7/12 - 10/9 s2 + 40/27 s2^2;
gzF$ = Sqrt[gF$^2 + gpF$^2]; s2F$ = gpF$^2/gzF$^2;
rW$ = gF$^6 vF$^2/(4 mw$^2)/g0sq$^2;
rZ$ = gzF$^6 vF$^2/(4 mz$^2) dpZ$[s2F$]/(G0sq$^2 dpZ$[1 - c0sq$]);
(* one loop: R_W = 1 + 3 dW - 2 DeltaHat;  R_Z = 1 + 3 dZ - 2 DeltaHat + (d ln delta'_Z/d s^2) (-c0^2 (dW - dZ)) *)
dlnZ$ = D[Log[dpZ$[x]], x] /. x -> 1 - c0sq$;
rW1$ = 1 + 3 dW$ - 2 dH$;
rZ1$ = 1 + 3 dZ$ - 2 dH$ + dlnZ$ (-c0sq$ (dW$ - dZ$));
ntW$ = 3 (dW$ - dT$) - 2 (dH$ - dT$); ntZ$ = 3 (dZ$ - dT$) - 2 (dH$ - dT$) + dlnZ$ (-c0sq$ (dW$ - dZ$));
Print["    exact tree ratio (fitted g, g', v_FJ at M_t, G_F, pole masses): R_W = ", N[rW$, 10], ", R_Z = ", N[rZ$, 10],
  ";  (v_FJ/v_G)^2 = ", N[vF$^2/vG$^2, 10], " (1 + DeltaHat = ", N[1 + dH$, 10], ")"];
Print["    one loop: R_W = ", N[rW1$, 10], ", R_Z = ", N[rZ1$, 10], ";  of R - 1, the tadpole part dV_tad = ", N[dT$, 8],
  ", the rest: W ", N[ntW$, 8], ", Z ", N[ntZ$, 8]];
Print["    the MS-bar tree with the H H V V tadpole vertex, R_V (1 + 2 delta_A^tad) = R_V (1 - dV_tad): W ", N[rW$ (1 - dT$), 10],
  ", Z ", N[rZ$ (1 - dT$), 10], ";  minus 1 against the tadpole-free one-loop part: W ", N[rW$ (1 - dT$) - 1 - ntW$, 4],
  ", Z ", N[rZ$ (1 - dT$) - 1 - ntZ$, 4], " (O(alpha^2): dV_tad^2 = ", N[dT$^2, 4], ")"];
tick$["(b) loop numbers"];
Export[FileNameJoin[{resDirVS$, "hvv_scheme.csv"}], {{"quantity", "value"},
   {"K_2deltaA_tad_plus_dV_tad_W", ToString[InputForm[chkW$]]}, {"K_2deltaA_tad_plus_dV_tad_Z", ToString[InputForm[chkZ$]]},
   {"dW", ToString[CForm[N[dW$, 20]]]}, {"dZ", ToString[CForm[N[dZ$, 20]]]}, {"DeltaHat", ToString[CForm[N[dH$, 20]]]},
   {"dV_tad", ToString[CForm[N[dT$, 20]]]}, {"mw_pole", ToString[CForm[N[mw$, 20]]]}, {"mz_pole", ToString[CForm[N[mz$, 20]]]},
   {"R_W_exact", ToString[CForm[N[rW$, 16]]]}, {"R_Z_exact", ToString[CForm[N[rZ$, 16]]]}, {"R_W_oneloop", ToString[CForm[N[rW1$, 16]]]},
   {"R_Z_oneloop", ToString[CForm[N[rZ1$, 16]]]}, {"nontadpole_W", ToString[CForm[N[ntW$, 16]]]}, {"nontadpole_Z", ToString[CForm[N[ntZ$, 16]]]},
   {"R_W_times_1_minus_dVtad", ToString[CForm[N[rW$ (1 - dT$), 16]]]}, {"R_Z_times_1_minus_dVtad", ToString[CForm[N[rZ$ (1 - dT$), 16]]]}}, "CSV"];
Print["written: results/hvv_scheme.csv"];
