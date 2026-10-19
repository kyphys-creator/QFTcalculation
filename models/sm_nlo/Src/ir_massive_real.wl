(* ::Package:: *)

(* ::Title:: *)
(*Step (3) of the NLO note: the hard real emission for massive emitters and the total*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (3).  The same decays as ir_massive_virtual.wl, Gamma^(1)/Gamma_0 = (alpha C/pi) K:*)
(*  Z(k) -> Q(p1) Qbar(p2) g(p3) with the currents gamma^mu (V) and gamma^mu gamma5 (A), and t(P) -> b(p1) W+(p2) g(p3).*)
(*The sum over spins and polarizations R = sum|M_R|^2/(g^2 C) in 4 dimensions (FeynCalc; the Z and W sums -g + k k/M^2, the*)
(*gluon -g), checked (a) against the note's FeynArts model (Z -> b bbar g, t -> b W+ g, symbolic) and (b) against the eikonal*)
(*factor of Eq. (eikonal) near E_g -> 0.  The hard part, E_g > Delta E = delta E_max in the rest frame of the decaying particle,*)
(*  K_H = int ds12 ds13 R/(32 pi M^2 Phi_2 sum|M_0|^2),  Phi_2 = lambda^(1/2)(M^2, m1^2, m2^2)/(8 pi M^2),*)
(*is integrated with NIntegrate in logarithmic variables (x = M^2 - s12 = 2 M E_g from the cut, and 2 p_i.p3 from the*)
(*collinear edges); with K_V + K_S of ir_massive_virtual.wl (results/ir_massive_vs.csv) it gives K, which must not depend on*)
(*delta (up to the O(delta) error of the soft approximation).  Writes results/ir_massive.csv and work/me_massive.txt (the CForm*)
(*of R for ir_massive_mg5.py).  Batch:  wolframscript -file ir_massive_real.wl*)


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
(*Kinematics in s12, s13 (s23 = M^2 + m1^2 + m2^2 - s12 - s13)*)

kin3$[M_, m1_, m2_, top_: False] := (FCClearScalarProducts[];
   ScalarProduct[p1, p1] = m1^2; ScalarProduct[p2, p2] = m2^2; ScalarProduct[p3, p3] = 0;
   ScalarProduct[p1, p2] = (s12 - m1^2 - m2^2)/2; ScalarProduct[p1, p3] = (s13 - m1^2)/2;
   ScalarProduct[p2, p3] = (M^2 + m1^2 + m2^2 - s12 - s13 - m2^2)/2;
   ScalarProduct[pk, pk] = M^2; ScalarProduct[pk, p1] = (M^2 + m1^2 - (M^2 + m1^2 + m2^2 - s12 - s13))/2;
   ScalarProduct[pk, p2] = (M^2 + m2^2 - s13)/2; ScalarProduct[pk, p3] = (M^2 - s12)/2;);
kin2$[M_, m1_, m2_] := (FCClearScalarProducts[];
   ScalarProduct[p1, p1] = m1^2; ScalarProduct[p2, p2] = m2^2; ScalarProduct[p1, p2] = (M^2 - m1^2 - m2^2)/2;
   ScalarProduct[pk, pk] = M^2; ScalarProduct[pk, p1] = (M^2 + m1^2 - m2^2)/2; ScalarProduct[pk, p2] = (M^2 - m1^2 + m2^2)/2;);
sq$[amp_, pols_] := Simplify[Contract[trEval$[FermionSpinSum[amp ComplexConjugate[amp /. {mu -> nu, rho -> sig}]]] pols]];

(* Z -> Q Qbar (g): mass m, M^2 = MM *)
polZ3$ = (-MT[mu, nu] + FV[pk, mu] FV[pk, nu]/MM) (-MT[rho, sig]);
ampRZ$[gam_] := Spinor[Momentum[p1], m].(GA[rho].(GS[p1] + GS[p3] + m).GA[mu].gam/(s13 - m^2) -
      GA[mu].gam.(GS[p2] + GS[p3] - m).GA[rho]/(MM + 2 m^2 - s12 - s13 - m^2)).Spinor[-Momentum[p2], m];
kin3$[Sqrt[MM], m, m];
rZ$ = <|"V" -> sq$[ampRZ$[1], polZ3$], "A" -> sq$[ampRZ$[GA5], polZ3$]|>;
kin2$[Sqrt[MM], m, m];
amp0Z$[gam_] := Spinor[Momentum[p1], m].GA[mu].gam.Spinor[-Momentum[p2], m];
b0Z$ = <|"V" -> sq$[amp0Z$[1], -MT[mu, nu] + FV[pk, mu] FV[pk, nu]/MM], "A" -> sq$[amp0Z$[GA5], -MT[mu, nu] + FV[pk, mu] FV[pk, nu]/MM]|>;
Print["Born Z (4 dimensions): V ", b0Z$["V"], ",  A ", b0Z$["A"]];

(* t -> b W+ (g): P = p1 + p2 + p3 *)
polT3$ = (-MT[mu, nu] + FV[p2, mu] FV[p2, nu]/MW^2) (-MT[rho, sig]);
ampRT$ = Spinor[Momentum[p1], mb].(GA[rho].(GS[p1] + GS[p3] + mb).GA[mu].GA[7]/(s13 - mb^2) +
      GA[mu].GA[7].(GS[p1] + GS[p2] + mt).GA[rho]/(s12 - mt^2)).Spinor[Momentum[pk], mt];
kin3$[mt, mb, MW];
ScalarProduct[pk, p1] = (mt^2 + mb^2 - (mt^2 + mb^2 + MW^2 - s12 - s13))/2;
rT$ = sq$[ampRT$, polT3$];
kin2$[mt, mb, MW];
b0T$ = sq$[Spinor[Momentum[p1], mb].GA[mu].GA[7].Spinor[Momentum[pk], mt], -MT[mu, nu] + FV[pk - p1, mu] FV[pk - p1, nu]/MW^2];
Print["Born t -> b W+ (4 dimensions): ", Simplify[b0T$]];
tick$["squared amplitudes"];

(* ::Section:: *)
(*Checks of R: the soft limit and the FeynArts model*)

(* the eikonal factor at the 3-body point, divided out: R/(sum|M0|^2 eik) -> 1 as E_g -> 0 *)
eikZ$ = Module[{pp12 = (s12 - 2 m^2)/2, pp13 = (s13 - m^2)/2, pp23 = (MM + m^2 - s12 - s13)/2},
   2 pp12/(pp13 pp23) - m^2/pp13^2 - m^2/pp23^2];
eikT$ = Module[{pP1 = (mt^2 + mb^2 - (mt^2 + mb^2 + MW^2 - s12 - s13))/2 + (s13 - mb^2)/2, pP3 = (mt^2 - s12)/2, pp13 = (s13 - mb^2)/2},
   (* P.p1 = p1.(p1 + p2 + p3) *)
   pP1 = mb^2 + (s12 - mb^2 - MW^2)/2 + (s13 - mb^2)/2;
   2 pP1/(pP3 pp13) - mt^2/pP3^2 - mb^2/pp13^2];
softPt$[Mv_, m1v_, m2v_, eg_] := Module[{s12v = Mv^2 - 2 Mv eg, e1, p1s, e3},
   e1 = (s12v + m1v^2 - m2v^2)/(2 Sqrt[s12v]); p1s = Sqrt[e1^2 - m1v^2]; e3 = (Mv^2 - s12v)/(2 Sqrt[s12v]);
   {s12 -> s12v, s13 -> m1v^2 + 2 e3 e1}];   (* the gluon at right angles to p1 in the 12 rest frame *)
Print["R/(sum|M0|^2 eik) - 1 at E_g = 1e-4, 1e-6 E_max: Z V ",
  N[Table[(rZ$["V"]/(b0Z$["V"] eikZ$) - 1) /. softPt$[1, 1/10, 1/10, ef (1 - 4/100)/2] /. {MM -> 1, m -> 1/10}, {ef, {10^-4, 10^-6}}], 6],
  ",  Z A ", N[Table[(rZ$["A"]/(b0Z$["A"] eikZ$) - 1) /. softPt$[1, 1/10, 1/10, ef (1 - 4/100)/2] /. {MM -> 1, m -> 1/10},
     {ef, {10^-4, 10^-6}}], 6],
  ",  t ", N[Table[(rT$/(b0T$ eikT$) - 1) /. softPt$[1, 1/10, 1/2, ef ((1 - (6/10)^2)/2)] /. {mt -> 1, mb -> 1/10, MW -> 1/2},
     {ef, {10^-4, 10^-6}}], 6]];

tmpMR$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirMR$, "generated", "SM_CKM_FA"}], FileNameJoin[{tmpMR$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{tmpMR$, "SM_CKM_FA"}], Quiet -> True];
modelMR$ = FileNameJoin[{tmpMR$, "SM_CKM_FA", "SM_CKM_FA"}];
convMR$ = {FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["MZ"] -> MZ, FCGV["MW"] -> MW,
   FCGV["MB"] -> mb, FCGV["MT"] -> mt, MB -> mb, MT -> mt,
   Conjugate[CKM[i_Integer, j_Integer]] :> vR[i, j] - I vI[i, j], CKM[i_Integer, j_Integer] :> vR[i, j] + I vI[i, j]};
faSq$[in_, out_, inMom_, pols_] := Module[{d, a, x},
   d = Quiet[InsertFields[CreateTopologies[0, 1 -> 3], {in} -> out, InsertionLevel -> {Particles},
       Model -> modelMR$, GenericModel -> modelMR$], RuleDelayed::rhs];
   a = Quiet[FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {inMom},
       OutgoingMomenta -> {p1, p2, p3}, ChangeDimension -> 4, List -> True, SMP -> False, UndoChiralSplittings -> True,
       DropSumOver -> True, TransversePolarizationVectors -> {}], RuleDelayed::rhs] /. convMR$;
   Print["   ", Length[a], " diagrams"];
   x = FermionSpinSum[ComplexConjugate[Total[a]] Total[a], ExtraFactor -> 1];
   x = trEval$[x];
   Do[x = DoPolarizationSums[x, Sequence @@ pp], {pp, pols}];
   x = Contract[FeynAmpDenominatorExplicit[SUNSimplify[DiracSimplify[x], SUNNToCACF -> False]]] /. SUNN -> 3;
   Simplify[x /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}]];
s2MR$ = 1 - MW^2/MZ^2; gZMR$ = ee/Sqrt[s2MR$ (1 - s2MR$)];
Print["Z -> b bbar g:"];
kin3$[MZ, mb, mb];
dZb$ = Simplify[faSq$[V[2], {F[4, {3}], -F[4, {3}], V[4]}, pk, {{pk}, {p3, 0, VirtualBoson -> True}}] -
    4 gS^2 (gZMR$/2)^2 ((-1/2 + 2/3 s2MR$)^2 rZ$["V"] + (1/4) rZ$["A"]) /. {m -> mb, MM -> MZ^2}];
Print["   FeynArts model minus N_c C_F g_s^2 (g_Z/2)^2 (v^2 R_V + a^2 R_A) (expect 0): ", dZb$];
Print["t -> b W+ g:"];
kin3$[mt, mb, MW];
ScalarProduct[pk, p1] = (mt^2 + mb^2 - (mt^2 + mb^2 + MW^2 - s12 - s13))/2;
dTb$ = Simplify[faSq$[F[3, {3}], {F[4, {3}], V[3], V[4]}, pk, {{p2}, {p3, 0, VirtualBoson -> True}}] -
    4 gS^2 (ee^2/(2 (1 - MW^2/MZ^2))) (vR[3, 3]^2 + vI[3, 3]^2) rT$];
Print["   FeynArts model minus N_c C_F g_s^2 (g^2/2) |V_tb|^2 R_L (expect 0): ", dTb$];
DeleteDirectory[tmpMR$, DeleteContents -> True];
tick$["model checks"];

(* ::Section:: *)
(*Hard integrals*)

(* Gauss-Legendre product rule on npan panels of npt points in each of u and v, on packed arrays (R is a rational function, so
   it evaluates elementwise); in u = ln(x/x_lo)/ln(x_hi/x_lo), x = M^2 - s12 = 2 M E_g, and in v, the logarithm of 2 p1.p3 (or of
   2 p2.p3) from its collinear edge to the middle of its range.  sym: R is symmetric under 1 <-> 2 (Z), so the edge along
   particle 2 is evaluated as R(s12, m^2 + 2 p2.p3), without the cancellation in s23. *)
glRule$[npan_, npt_] := Module[{g = NIntegrate`GaussRuleData[npt, MachinePrecision]},
   {Flatten[Table[(i - 1 + g[[1]])/npan, {i, npan}]], Flatten[Table[g[[2]]/npan, {i, npan}]]}];
(* rexpr: R written exactly in xx = M^2 - s12 = 2 P.p3 and ww = s13 - m1^2 = 2 p1.p3 (so that no difference of large numbers is
   formed near the soft edge); the momenta of the 12 rest frame from lambda^(1/2) without cancellations near the threshold *)
hardK$[rexpr_, b0_, Mv_, m1v_, m2v_, dl_, sym_, npan_, npt_: 20] := Module[
   {xhi = Mv^2 - (m1v + m2v)^2, xlo, xc, phi2, U, WU, uu, vv, wgt, pieces},
   xlo = dl xhi; xc = xhi/2;
   phi2 = Sqrt[(Mv^2 - (m1v + m2v)^2) (Mv^2 - (m1v - m2v)^2)]/(8 Pi Mv^2);
   {U, WU} = glRule$[npan, npt];
   uu = Flatten[Transpose[ConstantArray[U, Length[U]]]]; vv = Flatten[ConstantArray[U, Length[U]]];
   wgt = Flatten[Outer[Times, WU, WU]];
   (* x from the cut to xhi/2 logarithmically, and from xhi/2 to xhi as x = xhi - (xhi/2) t^2: the Dalitz range in w shrinks as
      sqrt(xhi - x) at the hard end, and the square root would spoil the Gauss rule; {x, xhi - x, dx/du} *)
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
rZx$ = <|"V" -> Together[rZ$["V"] /. {s12 -> MM - xx, s13 -> m^2 + ww}], "A" -> Together[rZ$["A"] /. {s12 -> MM - xx, s13 -> m^2 + ww}]|>;
rTx$ = Together[rT$ /. {s12 -> mt^2 - xx, s13 -> mb^2 + ww}];
Print["R_Z symmetric under 1 <-> 2 (expect 0): ",
  Simplify[{rZ$["V"] - (rZ$["V"] /. s13 -> MM + 2 m^2 - s12 - s13), rZ$["A"] - (rZ$["A"] /. s13 -> MM + 2 m^2 - s12 - s13)}]];

vs$ = Association[(#[[1]] <> "|" <> ToString[#[[2]]] -> ToExpression[#[[3]]]) & /@ Rest[Import[FileNameJoin[{resDirMR$, "ir_massive_vs.csv"}], "CSV"]]];
massesMR$ = {"MZ" -> 911876/10000, "MW" -> 803692/10000, "MT" -> 17257/100, "MB" -> 478/100, "MC" -> 167/100,
   "MTA" -> 177693/100000, "MMU" -> 1056584/10000000};
massMR$[k_] := N[k /. massesMR$];
deltasMR$ = {10^-4, 10^-5, 10^-6, 10^-7, 10^-8};
chanZMR$ = {{"Z_b", massMR$["MB"], massMR$["MZ"]}, {"Z_c", massMR$["MC"], massMR$["MZ"]}, {"Z_ta", massMR$["MTA"], massMR$["MZ"]},
   {"Z_mu", massMR$["MMU"], massMR$["MZ"]}, {"Z_m1e-3", 0.001, 1.}, {"Z_m1e-5", 0.00001, 1.},
   {"Z_b0.05", N[Sqrt[1 - (5/100)^2]/2], 1.}, {"Z_b0.01", N[Sqrt[1 - (1/100)^2]/2], 1.}};
chanTMR$ = {{"t_bW", massMR$["MT"], massMR$["MB"], massMR$["MW"]}, {"t_mb1e-3_MW1e-3", 1., 0.001, 0.001}, {"t_mb1e-4_MW1e-4", 1., 0.0001, 0.0001}};
fmtList$[l_, n_: 12] := StringRiffle[ToString[NumberForm[#, n, NumberFormat -> (If[#3 === "", #1, #1 <> "e" <> #3] &),
       ExponentFunction -> (If[-5 < # < 5, Null, #] &)]] & /@ l, ", "];
rowsMR$ = {};
Do[Module[{name = c[[1]], mv = c[[2]], Mv = c[[3]]},
   Do[Module[{rf = rZx$[X] /. {m -> mv, MM -> Mv^2}, b0 = b0Z$[X] /. {m -> mv, MM -> Mv^2}, ks, conv},
      ks = Table[Module[{kh = hardK$[rf, b0, Mv, mv, mv, N[dl], True, 24], kvs = vs$[name <> "_" <> X <> "|" <> ToString[N[dl]]]},
         If[dl == Last[deltasMR$], conv = kh - hardK$[rf, b0, Mv, mv, mv, N[dl], True, 16]];
         AppendTo[rowsMR$, {name <> "_" <> X, N[dl], kvs, kh, kvs + kh}]; kvs + kh], {dl, deltasMR$}];
      Print[name, " ", X, ": K at delta = 1e-4 ... 1e-8: ", fmtList$[ks], ";  minus the value at 1e-8: ",
       fmtList$[ks - Last[ks], 2], ";  24 minus 16 panels: ", fmtList$[{conv}, 2]]], {X, {"V", "A"}}]], {c, chanZMR$}];
Do[Module[{name = c[[1]], mtv = c[[2]], mbv = c[[3]], mwv = c[[4]]},
   Module[{rf = rTx$ /. {mt -> mtv, mb -> mbv, MW -> mwv}, b0 = b0T$ /. {mt -> mtv, mb -> mbv, MW -> mwv}, ks, conv},
    ks = Table[Module[{kh = hardK$[rf, b0, mtv, mbv, mwv, N[dl], False, 24], kvs = vs$[name <> "|" <> ToString[N[dl]]]},
       If[dl == Last[deltasMR$], conv = kh - hardK$[rf, b0, mtv, mbv, mwv, N[dl], False, 16]];
       AppendTo[rowsMR$, {name, N[dl], kvs, kh, kvs + kh}]; kvs + kh], {dl, deltasMR$}];
    Print[name, ": K at delta = 1e-4 ... 1e-8: ", fmtList$[ks], ";  minus the value at 1e-8: ",
     fmtList$[ks - Last[ks], 2], ";  24 minus 16 panels: ", fmtList$[{conv}, 2]]]], {c, chanTMR$}];
tick$["hard integrals"];
(* delta -> 0: the soft approximation errs by O(delta), so K(0) = K(1e-8) - (K(1e-7) - K(1e-8))/9 *)
kOf$[name_, dl_] := SelectFirst[rowsMR$, #[[1]] == name && #[[2]] == N[dl] &][[5]];
k0$[name_] := kOf$[name, 10^-8] - (kOf$[name, 10^-7] - kOf$[name, 10^-8])/9;
rowsMR$ = Join[rowsMR$, Function[nm, {nm, 0., "", "", k0$[nm]}] /@ DeleteDuplicates[rowsMR$[[All, 1]]]];
Print["K extrapolated to delta -> 0: ", StringRiffle[(# <> " " <> fmtList$[{k0$[#]}, 10]) & /@ DeleteDuplicates[rowsMR$[[All, 1]]], ";  "]];
Print["massless limit (m/M = 1e-5), K - 3/4: V ", fmtList$[{k0$["Z_m1e-5_V"] - 3/4}, 3], ", A ", fmtList$[{k0$["Z_m1e-5_A"] - 3/4}, 3]];
Print["threshold, K - pi^2/(2 b) at b = 0.05, 0.01: V ", fmtList$[{k0$["Z_b0.05_V"] - Pi^2/(2 0.05), k0$["Z_b0.01_V"] - Pi^2/(2 0.01)}, 6],
  " (the vector-current matching coefficient: -4 as b -> 0);  A ", fmtList$[{k0$["Z_b0.05_A"] - Pi^2/(2 0.05), k0$["Z_b0.01_A"] - Pi^2/(2 0.01)}, 6]];
Print["t -> b W+ as m_b, M_W -> 0 (1e-3, 1e-4 m_t), K + (pi^2/3 - 5/4) (Jezabek-Kuehn's limit): ",
  fmtList$[{k0$["t_mb1e-3_MW1e-3"] + Pi^2/3 - 5/4, k0$["t_mb1e-4_MW1e-4"] + Pi^2/3 - 5/4}, 3]];
Export[FileNameJoin[{resDirMR$, "ir_massive.csv"}], Prepend[rowsMR$, {"channel", "delta", "KV_plus_KS", "KH", "K"}], "CSV"];

(* ::Section:: *)
(*R for MadGraph*)

Export[FileNameJoin[{srcDirMR$, "work", "me_massive.txt"}], StringRiffle[{
    "RZV|" <> ToString[CForm[rZ$["V"]]], "RZA|" <> ToString[CForm[rZ$["A"]]], "RT|" <> ToString[CForm[rT$]]}, "\n"], "Text"];
Print["written: results/ir_massive.csv, work/me_massive.txt"];
