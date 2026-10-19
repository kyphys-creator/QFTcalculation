(* ::Package:: *)

(* ::Title:: *)
(*Step (4) of the Higgs note: the hard real emission of H -> Q Qbar g with massive quarks, and the total*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (4); the scalar-current version of the NLO note's ir_massive_real.wl.  H(k) -> Q(p1) Qbar(p2)*)
(*g(p3), Gamma^(1)/Gamma_0 = (alpha C/pi) K.  R = sum|M_R|^2/(g^2 C) in 4 dimensions (the Yukawa coupling y/sqrt(2) and the*)
(*colour stripped; the gluon sum -g), checked (a) against the note's FeynArts model (H -> b bbar g, H -> tau- tau+ gamma, the*)
(*Yukawa couplings as their own symbols) and (b) against the eikonal factor near E_g -> 0.  The hard part, E_g > delta E_max in the*)
(*H rest frame, K_H = int ds12 ds13 R/(32 pi M^2 Phi_2 sum|M_0|^2), with the NLO note's Gauss-Legendre rule in logarithmic*)
(*variables; with K_V + K_S of hqq_massive_virtual.wl (results/hqq_massive_vs.csv, the on-shell Yukawa coupling) it gives K_OS,*)
(*which must not depend on delta.  Then*)
(*  (a) K_OS against the closed form of Drees and Hikasa (Phys. Lett. B 240, 455 (1990); a reference), Delta_H(beta);*)
(*  (b) the massless limit: K_OS -> 9/4 + (3/2) ln(m^2/M^2) (Eq. (hqqpole)), and K_MS(mu = M) = K_OS + 2 + (3/2) ln(M^2/m^2) -> 17/4;*)
(*  (c) the threshold: K_OS - pi^2/(2 beta) (the Coulomb term) at beta = 0.05, 0.01.*)
(*Writes results/hqq_massive.csv and work/me_hqq.txt (the CForm of R for hqq_massive_mg5.py).*)
(*Batch:  wolframscript -file hqq_massive_real.wl  (after hqq_massive_virtual.wl)*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirMR$ = DirectoryName[$InputFileName];
resDirMR$ = FileNameJoin[{srcDirMR$, "results"}];
t0MR$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0MR$], " s] ", s];
trEval$[x_] := x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];

(* ::Section:: *)
(*R and the Born in 4 dimensions, s12 = (p1 + p2)^2, s13 = (p1 + p3)^2*)

kin3$[M_, m1_, m2_] := (FCClearScalarProducts[];
   ScalarProduct[p1, p1] = m1^2; ScalarProduct[p2, p2] = m2^2; ScalarProduct[p3, p3] = 0;
   ScalarProduct[p1, p2] = (s12 - m1^2 - m2^2)/2; ScalarProduct[p1, p3] = (s13 - m1^2)/2;
   ScalarProduct[p2, p3] = (M^2 + m1^2 + m2^2 - s12 - s13 - m2^2)/2;
   ScalarProduct[pk, pk] = M^2; ScalarProduct[pk, p1] = (M^2 + m1^2 - (M^2 + m1^2 + m2^2 - s12 - s13))/2;
   ScalarProduct[pk, p2] = (M^2 + m2^2 - s13)/2; ScalarProduct[pk, p3] = (M^2 - s12)/2;);
ampRH$ = Spinor[Momentum[p1], m].(GA[rho].(GS[p1] + GS[p3] + m)/(s13 - m^2) -
      (GS[p2] + GS[p3] - m).GA[rho]/(MM + 2 m^2 - s12 - s13 - m^2)).Spinor[-Momentum[p2], m];
kin3$[Sqrt[MM], m, m];
rH$ = Simplify[Contract[trEval$[FermionSpinSum[ampRH$ ComplexConjugate[ampRH$ /. rho -> sig]]] (-MT[rho, sig])]];
b0H$ = 2 (MM - 4 m^2);
Print["R symmetric under 1 <-> 2 (expect 0): ", Simplify[rH$ - (rH$ /. s13 -> MM + 2 m^2 - s12 - s13)]];
eik$ = Module[{pp12 = (s12 - 2 m^2)/2, pp13 = (s13 - m^2)/2, pp23 = (MM + m^2 - s12 - s13)/2},
   2 pp12/(pp13 pp23) - m^2/pp13^2 - m^2/pp23^2];
softPt$[Mv_, m1v_, m2v_, eg_] := Module[{s12v = Mv^2 - 2 Mv eg, e1, e3},
   e1 = (s12v + m1v^2 - m2v^2)/(2 Sqrt[s12v]); e3 = (Mv^2 - s12v)/(2 Sqrt[s12v]);
   {s12 -> s12v, s13 -> m1v^2 + 2 e3 e1}];
Print["R/(sum|M0|^2 eik) - 1 at E_g = 1e-4, 1e-6 E_max (expect -> 0 linearly): ",
  N[Table[(rH$/(b0H$ eik$) - 1) /. softPt$[1, 1/10, 1/10, ef (1 - 4/100)/2] /. {MM -> 1, m -> 1/10}, {ef, {10^-4, 10^-6}}], 6]];

tmpMR$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirMR$, "generated", "SM_CKM_FA"}], FileNameJoin[{tmpMR$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{tmpMR$, "SM_CKM_FA"}], Quiet -> True];
modelMR$ = FileNameJoin[{tmpMR$, "SM_CKM_FA", "SM_CKM_FA"}];
convMR$ = {FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["MZ"] -> MZ, FCGV["MW"] -> MW, FCGV["MH"] -> MH,
   FCGV["MB"] -> mb, MB -> mb, FCGV["MTA"] -> mta, MTA -> mta};
yukMR$ = {yl[i_Integer, j_Integer] :> If[i == j, yL[i], 0], yu[i_Integer, j_Integer] :> If[i == j, yU[i], 0],
   yd[i_Integer, j_Integer] :> If[i == j, yD[i], 0]};
faSq$[out_] := Module[{d, a, x},
   d = Quiet[InsertFields[CreateTopologies[0, 1 -> 3], {S[1]} -> out, InsertionLevel -> {Particles},
       Model -> modelMR$, GenericModel -> modelMR$, ExcludeParticles -> {S[2], S[3], V[2], V[3]}], RuleDelayed::rhs];
   a = Quiet[FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {pk},
       OutgoingMomenta -> {p1, p2, p3}, ChangeDimension -> 4, List -> True, SMP -> False, UndoChiralSplittings -> True,
       DropSumOver -> True, TransversePolarizationVectors -> {}], RuleDelayed::rhs] /. convMR$ /. yukMR$;
   Print["   ", Length[a], " diagrams"];
   x = FermionSpinSum[ComplexConjugate[Total[a]] Total[a], ExtraFactor -> 1];
   x = trEval$[x];
   x = DoPolarizationSums[x, p3, 0, VirtualBoson -> True];
   Simplify[Contract[FeynAmpDenominatorExplicit[SUNSimplify[DiracSimplify[x], SUNNToCACF -> False]]] /. SUNN -> 3]];
Print["H -> b bbar g:"];
kin3$[MH, mb, mb];
dHb$ = Simplify[faSq$[{F[4, {3}], -F[4, {3}], V[4]}] - 3 (4/3) gS^2 (yD[3]^2/2) (rH$ /. {m -> mb, MM -> MH^2})];
Print["   FeynArts model minus N_c C_F g_s^2 (y^2/2) R (expect 0): ", dHb$];
Print["H -> tau- tau+ gamma:"];
kin3$[MH, mta, mta];
dHt$ = Simplify[faSq$[{F[2, {3}], -F[2, {3}], V[1]}] - ee^2 (yL[3]^2/2) (rH$ /. {m -> mta, MM -> MH^2})];
Print["   FeynArts model minus e^2 (y^2/2) R (expect 0): ", dHt$];
DeleteDirectory[tmpMR$, DeleteContents -> True];
tick$["model checks"];

(* ::Section:: *)
(*Hard integrals (the NLO note's rule)*)

glRule$[npan_, npt_] := Module[{g = NIntegrate`GaussRuleData[npt, MachinePrecision]},
   {Flatten[Table[(i - 1 + g[[1]])/npan, {i, npan}]], Flatten[Table[g[[2]]/npan, {i, npan}]]}];
hardK$[rexpr_, b0_, Mv_, m1v_, m2v_, dl_, sym_, npan_, npt_: 20] := Module[
   {xhi = Mv^2 - (m1v + m2v)^2, xlo, xc, phi2, U, WU, uu, vv, wgt, pieces},
   xlo = dl xhi; xc = xhi/2;
   phi2 = Sqrt[(Mv^2 - (m1v + m2v)^2) (Mv^2 - (m1v - m2v)^2)]/(8 Pi Mv^2);
   {U, WU} = glRule$[npan, npt];
   uu = Flatten[Transpose[ConstantArray[U, Length[U]]]]; vv = Flatten[ConstantArray[U, Length[U]]];
   wgt = Flatten[Outer[Times, WU, WU]];
   pieces = {{xlo Exp[uu Log[xc/xlo]], xhi - xlo Exp[uu Log[xc/xlo]], xlo Exp[uu Log[xc/xlo]] Log[xc/xlo]},
     {xhi - xc uu^2, xc uu^2, 2 xc uu}};
   Total[Function[pc, Module[{x = pc[[1]], xmx = pc[[2]], jac = pc[[3]], s, e1, e2, p1s, e3, wlo, whi, wm, wa, wplo, wpm, wb, ra, rb},
       s = Mv^2 - x;
       e1 = (s + m1v^2 - m2v^2)/(2 Sqrt[s]); e2 = (s + m2v^2 - m1v^2)/(2 Sqrt[s]);
       p1s = Sqrt[xmx (s - (m1v - m2v)^2)]/(2 Sqrt[s]); e3 = x/(2 Sqrt[s]);
       wlo = 2 e3 m1v^2/(e1 + p1s); whi = 2 e3 (e1 + p1s); wm = (wlo + whi)/2;
       wa = wlo (wm/wlo)^vv;
       wplo = 2 e3 m2v^2/(e2 + p1s); wpm = x - wm; wb = wplo (wpm/wplo)^vv;
       ra = rexpr /. {xx -> x, ww -> wa};
       rb = If[sym, rexpr /. {xx -> x, ww -> wb}, rexpr /. {xx -> x, ww -> x - wb}];
       Total[wgt jac (ra wa Log[wm/wlo] + rb wb Log[wpm/wplo])]]] /@ pieces]/(32 Pi Mv^2 phi2 b0)];
rHx$ = Together[rH$ /. {s12 -> MM - xx, s13 -> m^2 + ww}];

vs$ = Association[(#[[1]] <> "|" <> ToString[#[[2]]] -> ToExpression[#[[3]]]) & /@ Rest[Import[FileNameJoin[{resDirMR$, "hqq_massive_vs.csv"}], "CSV"]]];
massesMR$ = {"MH" -> 12520/100, "MB" -> 478/100, "MC" -> 167/100, "MTA" -> 177693/100000, "MMU" -> 1056584/10000000};
massMR$[k_] := N[k /. massesMR$];
deltasMR$ = {10^-4, 10^-5, 10^-6, 10^-7, 10^-8};
chanMR$ = {{"H_b", massMR$["MB"], massMR$["MH"]}, {"H_c", massMR$["MC"], massMR$["MH"]}, {"H_ta", massMR$["MTA"], massMR$["MH"]},
   {"H_mu", massMR$["MMU"], massMR$["MH"]}, {"H_m1e-3", 0.001, 1.}, {"H_m1e-5", 0.00001, 1.},
   {"H_b0.05", N[Sqrt[1 - (5/100)^2]/2], 1.}, {"H_b0.01", N[Sqrt[1 - (1/100)^2]/2], 1.}};
fmtList$[l_, n_: 12] := StringRiffle[ToString[NumberForm[#, n, NumberFormat -> (If[#3 === "", #1, #1 <> "e" <> #3] &),
       ExponentFunction -> (If[-5 < # < 5, Null, #] &)]] & /@ l, ", "];
rowsMR$ = {};
Do[Module[{name = c[[1]], mv = c[[2]], Mv = c[[3]], rf, b0, ks, conv},
   rf = rHx$ /. {m -> mv, MM -> Mv^2}; b0 = b0H$ /. {m -> mv, MM -> Mv^2};
   ks = Table[Module[{kh = hardK$[rf, b0, Mv, mv, mv, N[dl], True, 24], kvs = vs$[name <> "|" <> ToString[N[dl]]]},
      If[dl == Last[deltasMR$], conv = kh - hardK$[rf, b0, Mv, mv, mv, N[dl], True, 16]];
      AppendTo[rowsMR$, {name, N[dl], kvs, kh, kvs + kh}]; kvs + kh], {dl, deltasMR$}];
   Print[name, ": K_OS at delta = 1e-4 ... 1e-8: ", fmtList$[ks], ";  minus the value at 1e-8: ", fmtList$[ks - Last[ks], 2],
    ";  24 minus 16 panels: ", fmtList$[{conv}, 2]]], {c, chanMR$}];
tick$["hard integrals"];
kOf$[name_, dl_] := SelectFirst[rowsMR$, #[[1]] == name && #[[2]] == N[dl] &][[5]];
k0$[name_] := kOf$[name, 10^-8] - (kOf$[name, 10^-7] - kOf$[name, 10^-8])/9;
names$ = DeleteDuplicates[rowsMR$[[All, 1]]];
(* Drees-Hikasa's Delta_H (a reference) *)
dh$[b_] := Module[{L = Log[(1 + b)/(1 - b)], A},
   A = (1 + b^2) (4 PolyLog[2, (1 - b)/(1 + b)] + 2 PolyLog[2, -(1 - b)/(1 + b)] - 3 Log[2/(1 + b)] L - 2 Log[b] L) -
     3 b Log[4/(1 - b^2)] - 4 b Log[b];
   A/b + (3 + 34 b^2 - 13 b^4)/(16 b^3) L + 3 (-1 + 7 b^2)/(8 b^2)];
betaOf$[name_] := Module[{c = SelectFirst[chanMR$, #[[1]] == name &]}, Sqrt[1 - 4 c[[2]]^2/c[[3]]^2]];
Print["K_OS extrapolated to delta -> 0, and minus Drees-Hikasa's Delta_H(beta):"];
Do[Print["  ", nm, ": beta = ", fmtList$[{betaOf$[nm]}, 10], ",  K_OS = ", fmtList$[{k0$[nm]}, 12], ",  minus Delta_H: ",
   fmtList$[{k0$[nm] - dh$[betaOf$[nm]]}, 3]], {nm, names$}];
Module[{c = SelectFirst[chanMR$, #[[1]] == "H_m1e-5" &]},
  Print["massless limit (m/M = 1e-5): K_OS - (9/4 + (3/2) ln(m^2/M^2)) = ", fmtList$[{k0$["H_m1e-5"] - (9/4 + 3/2 Log[c[[2]]^2/c[[3]]^2])}, 3],
   ";  K_MS(mu = M) - 17/4 = ", fmtList$[{k0$["H_m1e-5"] + 2 + 3/2 Log[c[[3]]^2/c[[2]]^2] - 17/4}, 3]]];
Print["threshold: K_OS - pi^2/(2 beta) at beta = 0.05, 0.01: ", fmtList$[{k0$["H_b0.05"] - Pi^2/(2 0.05), k0$["H_b0.01"] - Pi^2/(2 0.01)}, 6],
  " (Delta_H - pi^2/(2 beta): ", fmtList$[{dh$[0.05] - Pi^2/(2 0.05), dh$[0.01] - Pi^2/(2 0.01)}, 6], ")"];
rowsMR$ = Join[rowsMR$, Function[nm, {nm, 0., "", "", k0$[nm]}] /@ names$];
Export[FileNameJoin[{resDirMR$, "hqq_massive.csv"}], Prepend[Join[rowsMR$,
     Function[nm, {nm <> "_DreesHikasa", 0., "", "", dh$[betaOf$[nm]]}] /@ names$], {"channel", "delta", "KV_plus_KS", "KH", "K_OS"}], "CSV"];
Export[FileNameJoin[{srcDirMR$, "work", "me_hqq.txt"}], "RH|" <> ToString[CForm[rH$]] <> "\n", "Text"];
Print["written: results/hqq_massive.csv, work/me_hqq.txt"];
