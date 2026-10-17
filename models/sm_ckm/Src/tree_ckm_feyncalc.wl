(* ::Package:: *)

(* ::Title:: *)
(*Step (2) of the CKM note: tree-level squared amplitudes with the CKM matrix (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm_ckm, step (2): compare with Eq. (widthsckm) and the hand results of Sec. tree.  sum|M|^2 is*)
(*the sum (not the average) over spins, polarizations and colours.  Hand values (Appendix B of the note):*)
(*  W+ -> u_i dbar_j : |V_ij|^2 N_c g^2 MW^2 [1 - (x1 + x2)/2 - (x1 - x2)^2/2]                 (x = m^2/MW^2)*)
(*  t -> d_j W+      : |V_tj|^2 3 g^2/(2 MW^2) [(mt^2 - m_j^2)^2 + MW^2 (mt^2 + m_j^2) - 2 MW^4]*)
(*  tbar -> bbar W-  : the same as t -> b W+ (no CP violation at tree level)*)
(*  u_i(p1) dbar_j(p2) -> nu_e(k1) e+(k2), massless, Gamma_W = 0 : N_c g^4 |V_ij|^2 u^2/(s - MW^2)^2,  u = (p1 - k2)^2*)
(*  u(p1) ubar(p2) -> d(k1) sbar(k2), massless : N_c^2 g^4 |V_ud|^2 |V_us|^2 u^2/(t - MW^2)^2,  t = (p1 - k1)^2*)
(*  u ubar -> W+ W-, massless d-type quarks: equal to V = 1 once V^dagger V = 1 is used (explicit parametrization)*)
(*  t(p1) sbar(p2) -> W+(k1) H(k2), all masses: proportional to |V_ts|^2 and independent of xiW (the s-channel G+ and*)
(*      the longitudinal part of the W propagator carry the same V_ts^* as the transverse W)*)
(*V is written as vR[i, j] + I vI[i, j] with real vR, vI (FeynCalc's ComplexConjugate treats symbols as real and*)
(*conjugates the explicit I), so |V_ij|^2 = vR^2 + vI^2.  The FeynArts model sums the G+- couplings over a dummy*)
(*generation (IndexSum), which is written out here.  sum|M|^2 at benchmark points is written to*)
(*results/tree_ckm_points.csv for tree_ckm_numeric.py (explicit matrices).*)
(*Uses the FeynArts model in Src/generated/SM_CKM_FA (run generate_SM_CKM.wl first).  As in the SM note, the FeynArts*)
(*model does not know that the Yukawa matrices are diagonal, so FeynArts inserts generation-changing H and G0*)
(*exchanges; the off-diagonal Yukawa couplings are set to 0 after FCFAConvert (the number of amplitudes that vanish is*)
(*printed).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file tree_ckm_feyncalc.wl.  Interactive:  ~/hep/bin/wopen tree_ckm_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;


srcDirTC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirTC$ = FileNameJoin[{srcDirTC$, "results"}];
Quiet[CreateDirectory[resDirTC$]];
modelTmpDirTC$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTC$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpDirTC$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirTC$, "SM_CKM_FA"}], Quiet -> True];
modelFileTC$ = FileNameJoin[{modelTmpDirTC$, "SM_CKM_FA", "SM_CKM_FA"}];


(* ::Text:: *)
(*Field codes of the FeynArts model: F[1, {i}] = nu_i, F[2, {i}] = l_i, F[3, {i}] = u_i, F[4, {i}] = d_i (i = generation),*)
(*S[1] = H, S[2] = G0, S[3] = G+, V[1] = A, V[2] = Z, V[3] = W+, V[4] = gluon.*)


massTC$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me};
lepMTC$ = {Me, MMU, MTA}; upMTC$ = {MU, MC, MT}; dnMTC$ = {MD, MS, MB};
yukTC$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMTC$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMTC$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMTC$[[i]]/vev, 0]};
(* the conjugate first: ReplaceAll tries the outer Conjugate[...] before the CKM inside it *)
ckmTC$ = {Conjugate[CKM[i_Integer, j_Integer]] :> vR[i, j] - I vI[i, j], CKM[i_Integer, j_Integer] :> vR[i, j] + I vI[i, j]};
convTC$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[V[1, ___]] -> xiA,
    GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW},
   massTC$];
abs2TC$[i_, j_] := vR[i, j]^2 + vI[i, j]^2;

diagsTC$[in_, out_] := Quiet[InsertFields[CreateTopologies[0, Length[in] -> Length[out]], in -> out,
    InsertionLevel -> {Particles}, Model -> modelFileTC$, GenericModel -> modelFileTC$], RuleDelayed::rhs];
ampsTC$[diags_, in_, out_, extra_ : {}] := Module[{a},
   (* GaugeRules -> {} keeps GaugeXi (the FeynArts default {_GaugeXi -> 1} is Feynman gauge) *)
   a = Quiet[FCFAConvert[CreateFeynAmp[diags, GaugeRules -> {}] /. M$FACouplings,
       IncomingMomenta -> in, OutgoingMomenta -> out, ChangeDimension -> 4, List -> True, SMP -> False,
       UndoChiralSplittings -> True, DropSumOver -> True, DropIndexSum -> False, TransversePolarizationVectors -> {}], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a = a /. convTC$ /. yukTC$ /. ckmTC$ /. vev -> 2 MW sw/ee /. extra;
   Print["   amplitudes: ", Length[a], ", vanishing after the diagonal-Yukawa (and massless) substitutions: ",
     Count[Simplify[DiracSimplify[#]] & /@ a, 0], "; CKM symbols left (expect {}): ",
     Union[Cases[a, _CKM | _IndexSum, Infinity]]];
   a];

evalTC$[x_] := Simplify[Contract[FeynAmpDenominatorExplicit[SUNSimplify[DiracSimplify[
       x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]], SUNNToCACF -> False]]] /. SUNN -> 3];
sumSqTC$[amp_, vecs_List] := Module[{x = FermionSpinSum[ComplexConjugate[amp] amp, ExtraFactor -> 1]},
   x = x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
   (* massive vectors: -g + k k/M^2 is DoPolarizationSums[x, k] *)
   Do[x = DoPolarizationSums[x, v], {v, vecs}];
   evalTC$[x]];

checkTC$[label_, got_, want_] := Module[{d = Simplify[got - want]},
   Print[label, ": FeynCalc - note = ", d, "   (expect 0)"]; d];
gTC$ = ee/sw;


(* ::Subsubsection:: *)
(*Inspect: ComplexConjugate on the CKM factors*)


Print["ComplexConjugate[(vR + I vI) GA[mu]] = ", ComplexConjugate[(vR[1, 2] + I vI[1, 2]) GA[mu]], "  (expect vR - I vI)"];


(* ::Section:: *)
(*Two-body decays*)


decayTC$[in_, out_, mIn_, m1_, m2_, vecs_] := Module[{d, a},
   d = diagsTC$[{in}, out];
   a = ampsTC$[d, {k}, {p1, p2}];
   FCClearScalarProducts[];
   ScalarProduct[k, k] = mIn^2; ScalarProduct[p1, p1] = m1^2; ScalarProduct[p2, p2] = m2^2;
   ScalarProduct[k, p1] = (mIn^2 + m1^2 - m2^2)/2; ScalarProduct[k, p2] = (mIn^2 - m1^2 + m2^2)/2;
   ScalarProduct[p1, p2] = (mIn^2 - m1^2 - m2^2)/2;
   sumSqTC$[Total[a], vecs]];

wHandTC$[m1_, m2_] := Module[{x1 = m1^2/MW^2, x2 = m2^2/MW^2}, 3 gTC$^2 MW^2 (1 - (x1 + x2)/2 - (x1 - x2)^2/2)];
tHandTC$[mj_] := 3 gTC$^2/(2 MW^2) ((MT^2 - mj^2)^2 + MW^2 (MT^2 + mj^2) - 2 MW^4);

(* W+ -> u_i dbar_j: diagonal, off-diagonal and t dbar (the formula is algebraic, so above-threshold masses test it) *)
resWTC$ = Table[With[{i = ij[[1]], j = ij[[2]]},
    checkTC$["W+ -> u" <> ToString[i] <> " dbar" <> ToString[j],
     decayTC$[V[3], {F[3, {i}], -F[4, {j}]}, MW, upMTC$[[i]], dnMTC$[[j]], {k}],
     abs2TC$[i, j] wHandTC$[upMTC$[[i]], dnMTC$[[j]]]]], {ij, {{1, 1}, {1, 2}, {2, 3}, {3, 1}}}];

sqTopTC$ = Table[decayTC$[F[3, {3}], {F[4, {j}], V[3]}, MT, dnMTC$[[j]], MW, {p2}], {j, 3}];
resTTC$ = Table[checkTC$["t -> d" <> ToString[j] <> " W+", sqTopTC$[[j]], abs2TC$[3, j] tHandTC$[dnMTC$[[j]]]], {j, 3}];
sqTbarTC$ = decayTC$[-F[3, {3}], {-F[4, {3}], -V[3]}, MT, MB, MW, {p2}];
resCPTC$ = {checkTC$["tbar -> bbar W- minus t -> b W+ (CP at tree level)", sqTbarTC$, sqTopTC$[[3]]]};


(* ::Section:: *)
(*u_i dbar_j -> nu_e e+ and u ubar -> d sbar (massless)*)


masslessTC$ = {MU -> 0, MC -> 0, MD -> 0, MS -> 0, MB -> 0, Me -> 0};

FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, 0, 0, 0, 0];
sqUDTC$ = Table[With[{i = ij[[1]], j = ij[[2]]}, Module[{a},
     a = ampsTC$[diagsTC$[{F[3, {i}], -F[4, {j}]}, {F[1, {1}], -F[2, {1}]}], {p1, p2}, {k1, k2}, masslessTC$];
     sumSqTC$[FeynAmpDenominatorExplicit[Total[a]], {}] /. t -> -s - u]], {ij, {{1, 1}, {1, 2}, {2, 3}}}];
resUDTC$ = Table[With[{i = {1, 1, 2}[[n]], j = {1, 2, 3}[[n]]},
    checkTC$["u" <> ToString[i] <> " dbar" <> ToString[j] <> " -> nu_e e+", sqUDTC$[[n]],
     3 gTC$^4 abs2TC$[i, j] u^2/(s - MW^2)^2]], {n, 3}];
Print["u dbar -> nu_e e+: gauge parameters left in sum|M|^2 (expect {}): ", Union[Cases[sqUDTC$, xiA | xiZ | xiW, Infinity]]];

ampUUDSTC$ = ampsTC$[diagsTC$[{F[3, {1}], -F[3, {1}]}, {F[4, {1}], -F[4, {2}]}], {p1, p2}, {k1, k2}, masslessTC$];
sqUUDSTC$ = sumSqTC$[FeynAmpDenominatorExplicit[Total[ampUUDSTC$]], {}] /. u -> -s - t;
resUUDSTC$ = {checkTC$["u ubar -> d sbar", sqUUDSTC$, 9 gTC$^4 abs2TC$[1, 1] abs2TC$[1, 2] (-s - t)^2/(t - MW^2)^2]};
Print["u ubar -> d sbar: gauge parameters left (expect {}): ", Union[Cases[sqUUDSTC$, xiA | xiZ | xiW, Infinity]]];


(* ::Section:: *)
(*u ubar -> W+ W- (massless d-type quarks): unitarity*)


(* ::Text:: *)
(*u(p1) ubar(p2) -> W+(k1) W-(k2), t = (p1 - k1)^2: s-channel gamma, Z and t-channel d, s, b with |V_uk|^2.  With the*)
(*explicit standard parametrization (real angles) sum_k |V_uk|^2 = 1, and sum|M|^2 equals the one with V = 1.*)


ampUUWWTC$ = ampsTC$[diagsTC$[{F[3, {1}], -F[3, {1}]}, {V[3], -V[3]}], {p1, p2}, {k1, k2}, masslessTC$];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, 0, 0, MW, MW];
sqUUWWTC$ = sumSqTC$[FeynAmpDenominatorExplicit[Total[ampUUWWTC$]], {k1, k2}] /. u -> 2 MW^2 - s - t;
Print["u ubar -> W+ W-: d(sum|M|^2)/d xiA, xiZ, xiW (expect 0, 0, 0): ",
  Simplify[{D[sqUUWWTC$, xiA], D[sqUUWWTC$, xiZ], D[sqUUWWTC$, xiW]}]];
Print["u ubar -> W+ W-: CKM entries in sum|M|^2: ", Union[Cases[sqUUWWTC$, (vR | vI)[__], Infinity]]];
vStdTC$ = {
   {c12 c13, s12 c13, s13 Exp[-I dl]},
   {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
   {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}} /.
   {c12 -> Sqrt[1 - s12^2], c23 -> Sqrt[1 - s23^2], c13 -> Sqrt[1 - s13^2]};
explicitTC$ = {vR[i_, j_] :> ComplexExpand[Re[vStdTC$[[i, j]]]], vI[i_, j_] :> ComplexExpand[Im[vStdTC$[[i, j]]]]};
unitTC$ = {vR[i_, j_] :> If[i == j, 1, 0], vI[__] -> 0};
assTC$ = 0 < s12 < 1 && 0 < s23 < 1 && 0 < s13 < 1 && Element[dl, Reals] && MW > 0;
resUUWWTC$ = {checkTC$["u ubar -> W+ W- with the explicit V minus V = 1",
    Simplify[sqUUWWTC$ /. explicitTC$, assTC$], sqUUWWTC$ /. unitTC$]};


(* ::Section:: *)
(*t sbar -> W+ H (all masses, general R_xi)*)


(* ::Text:: *)
(*t(p1) sbar(p2) -> W+(k1) H(k2): s-channel W and G+, t-channel top (H t t), u-channel s (H s s).  The G+ and the*)
(*xiW part of the W propagator cancel in sum|M|^2 only if the G+ vertex carries the same V_ts^* as the W vertex.*)


ampTSTC$ = ampsTC$[diagsTC$[{F[3, {3}], -F[4, {2}]}, {V[3], S[1]}], {p1, p2}, {k1, k2}];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, MT, MS, MW, MH];
sqTSTC$ = sumSqTC$[FeynAmpDenominatorExplicit[Total[ampTSTC$]], {k1}] /. u -> MT^2 + MS^2 + MW^2 + MH^2 - s - t;
Print["t sbar -> W+ H: gauge parameters in the amplitude: ", Union[Cases[ampTSTC$, xiA | xiZ | xiW, Infinity]],
  ";  d(sum|M|^2)/d xiW (expect 0): ", Simplify[D[sqTSTC$, xiW]]];
Print["t sbar -> W+ H: sum|M|^2/|V_ts|^2 free of the CKM entries (expect True): ",
  FreeQ[Simplify[sqTSTC$/abs2TC$[3, 2]], vR | vI]];
sqTSTC$ = Simplify[sqTSTC$ /. xiW -> 1];


(* ::Section:: *)
(*Benchmark points for tree_ckm_numeric.py*)


benchTC$ = {ee -> Sqrt[4 Pi/128], MW -> 80, MZ -> 91, sw -> Sqrt[1 - 80^2/91^2], cw -> 80/91, MH -> 125,
   MT -> 165, MS -> 546/10000};
vNumTC$ = N[vStdTC$ /. {s12 -> 22501/100000, s23 -> 4183/100000, s13 -> 3732/1000000, dl -> 1147/1000}, 30];
vBenchTC$ = {vR[i_, j_] :> Re[vNumTC$[[i, j]]], vI[i_, j_] :> Im[vNumTC$[[i, j]]]};
(* cos theta is the angle between p1 and k1 in every row: u = (p1 - k2)^2 = -s (1 + cos)/2, t = (p1 - k1)^2 = -s (1 - cos)/2 *)
rowsTC$ = Join[
   Flatten[Table[{"u dbar -> nu e+", rs, c, N[sqUDTC$[[1]] /. benchTC$ /. vBenchTC$ /. {s -> rs^2, u -> -rs^2 (1 + c)/2}, 20]},
     {rs, {100, 200}}, {c, {-0.6, 0.3}}], 1],
   Flatten[Table[{"u sbar -> nu e+ (from u1 dbar2)", rs, c,
      N[sqUDTC$[[2]] /. benchTC$ /. vBenchTC$ /. {s -> rs^2, u -> -rs^2 (1 + c)/2}, 20]}, {rs, {200}}, {c, {-0.6, 0.3}}], 1],
   Flatten[Table[{"u ubar -> d sbar", rs, c, N[sqUUDSTC$ /. benchTC$ /. vBenchTC$ /. {s -> rs^2, t -> -rs^2 (1 - c)/2}, 20]},
     {rs, {200}}, {c, {-0.6, 0.3}}], 1],
   Flatten[Table[Module[{sv = rs^2, pin, pout, e1, e3, tv},
      (* cos theta between t and W+ in the centre-of-mass frame *)
      pin = Sqrt[(sv - (165 + 0.0546)^2) (sv - (165 - 0.0546)^2)]/(2 rs);
      pout = Sqrt[(sv - (80 + 125)^2) (sv - (80 - 125)^2)]/(2 rs);
      e1 = (sv + 165^2 - 0.0546^2)/(2 rs); e3 = (sv + 80^2 - 125^2)/(2 rs);
      tv = 165^2 + 80^2 - 2 (e1 e3 - pin pout c);
      {"t sbar -> W+ H", rs, c, N[sqTSTC$ /. benchTC$ /. vBenchTC$ /. {s -> sv, t -> tv}, 20]}],
     {rs, {400, 1000}}, {c, {-0.6, 0.3}}], 1]];
Export[FileNameJoin[{resDirTC$, "tree_ckm_points.csv"}],
  Prepend[rowsTC$ /. x_Real :> CForm[x], {"process", "sqrt_s", "cos_theta", "sumM2_feyncalc"}], "CSV"];
Print["benchmark points written: ", Length[rowsTC$]];


(* ::Section:: *)
(*Summary*)


allTC$ = Join[resWTC$, resTTC$, resCPTC$, resUDTC$, resUUDSTC$, resUUWWTC$];
Print["Squared amplitudes compared: ", Length[allTC$], ", nonzero differences: ", Count[allTC$, x_ /; x =!= 0]];
