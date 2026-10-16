(* ::Package:: *)

(* ::Title:: *)
(*Step (2): tree-level squared amplitudes and decay widths with FeynArts + FeynCalc (SM, MS-bar parameters)*)


(* ::Text:: *)
(*Research note models/sm, step (2): compare with Eqs. (widths) and (eeff).  sum|M|^2 is the sum (not the average) over*)
(*spins, polarizations and colours.  The hand values of sum|M|^2 follow from Eq. (widths) and the two-body phase space:*)
(*  W+ -> f fbar'   : N_c g^2 MW^2 [1 - (x1 + x2)/2 - (x1 - x2)^2/2],          x_i = m_i^2/MW^2*)
(*  Z  -> f fbar    : 2 N_c e^2 MZ^2 [(gL^2 + gR^2)(1 - x) + 6 gL gR x],        x = m^2/MZ^2*)
(*  H  -> f fbar    : 2 N_c m^2 MH^2 beta^2/v^2,                                beta^2 = 1 - 4 m^2/MH^2*)
(*  t  -> b W+      : 3 g^2/(2 MW^2) [(mt^2 - mb^2)^2 + MW^2 (mt^2 + mb^2) - 2 MW^4]   (sum over the top spin and colour)*)
(*  e+ e- -> f fbar (massless, gamma + Z, width 0): Eq. (eeff)*)
(*and e+ e- -> W+ W- (massless electron) is written to results/tree_eeww_points.csv for tree_numeric.py.*)
(*Gauge parameters: the FeynArts propagators carry GaugeXi; d(sum|M|^2)/d xi = 0 is checked for e+ e- -> mu+ mu-*)
(*and e+ e- -> W+ W-.*)
(*Uses the FeynArts model in Src/generated/SM_FA (run generate_SM.wl first).  The FeynRules FeynArts model does not*)
(*know that the Yukawa matrices are diagonal, so FeynArts inserts generation-changing H and G0 exchanges with*)
(*yl[1, 2] etc.; the off-diagonal Yukawa couplings are set to 0 after FCFAConvert (and the number of amplitudes that*)
(*vanish is printed).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file tree_feyncalc.wl.  Interactive:  ~/hep/bin/wopen tree_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;


srcDirTree$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirTree$ = FileNameJoin[{srcDirTree$, "results"}];
Quiet[CreateDirectory[resDirTree$]];
modelTmpDirTree$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTree$, "generated", "SM_FA"}], FileNameJoin[{modelTmpDirTree$, "SM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirTree$, "SM_FA"}], Quiet -> True];
modelFileTree$ = FileNameJoin[{modelTmpDirTree$, "SM_FA", "SM_FA"}];


(* ::Text:: *)
(*Field codes of the FeynArts model: F[1, {i}] = nu_i, F[2, {i}] = l_i, F[3, {i}] = u_i, F[4, {i}] = d_i (i = generation),*)
(*S[1] = H, S[2] = G0, S[3] = G+, V[1] = A, V[2] = Z, V[3] = W+, V[4] = gluon.*)
(*Conversion of the FeynCalc output: FCGV["EL"] -> ee, the FCGV masses to plain symbols, y_f -> sqrt 2 m_f/v (diagonal),*)
(*off-diagonal Yukawa couplings -> 0, vev -> 2 MW sw/ee, GaugeXi -> xiA, xiZ, xiW.*)


massTree$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me};
lepMTree$ = {Me, MMU, MTA}; upMTree$ = {MU, MC, MT}; dnMTree$ = {MD, MS, MB};
yukTree$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMTree$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMTree$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMTree$[[i]]/vev, 0]};
convTree$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[V[1, ___]] -> xiA,
    GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW},
   massTree$];

treeDiagrams$[in_, out_] := Quiet[InsertFields[CreateTopologies[0, Length[in] -> Length[out]], in -> out,
    InsertionLevel -> {Particles}, Model -> modelFileTree$, GenericModel -> modelFileTree$], RuleDelayed::rhs];
treeAmps$[diags_, in_, out_, extra_ : {}] := Module[{a},
   a = Quiet[FCFAConvert[CreateFeynAmp[diags] /. M$FACouplings,
       IncomingMomenta -> in, OutgoingMomenta -> out, ChangeDimension -> 4, List -> True, SMP -> False,
       UndoChiralSplittings -> True, DropSumOver -> True, TransversePolarizationVectors -> {}], RuleDelayed::rhs];
   a = a /. convTree$ /. yukTree$ /. vev -> 2 MW sw/ee /. extra;
   (* Spinor . 0 . Spinor is not reduced by Simplify: count after DiracSimplify *)
   Print["   amplitudes: ", Length[a], ", vanishing after the diagonal-Yukawa (and massless) substitutions: ",
     Count[Simplify[DiracSimplify[#]] & /@ a, 0]];
   a];

(* traces evaluated explicitly; colour: SUNFDelta of the external quarks summed by SUNSimplify *)
evalTree$[x_] := Simplify[Contract[FeynAmpDenominatorExplicit[SUNSimplify[DiracSimplify[
       x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]], SUNNToCACF -> False]]] /. SUNN -> 3];
sumSq$[amp_, vecs_List] := Module[{x = FermionSpinSum[ComplexConjugate[amp] amp, ExtraFactor -> 1]},
   x = x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
   (* massive vectors: -g + k k/M^2 is DoPolarizationSums[x, k] (the form x, k, 0 is the massless -g sum) *)
   Do[x = DoPolarizationSums[x, v], {v, vecs}];
   evalTree$[x]];

cwT$ = Sqrt[1 - sw^2];
gLT$[q_, t3_] := (t3 - q sw^2)/(sw cwT$); gRT$[q_] := -q sw/cwT$;
toMZ$ = {cw -> MW/MZ, sw -> Sqrt[1 - MW^2/MZ^2]};
checkT$[label_, got_, want_] := Module[{d = Simplify[(got - want) /. cw -> cwT$ /. toMZ$, MW > 0 && MZ > MW]},
   Print[label, ": FeynCalc - note = ", d, "   (expect 0)"]; d];


(* ::Section:: *)
(*Two-body decays*)


(* ::Text:: *)
(*W+(k) -> f(p1) fbar'(p2): the (t, b), (c, s) and (nu_tau, tau) pairs with their masses (the formula is algebraic, so*)
(*W+ -> t bbar is a valid check of the mass dependence).*)


decay$[in_, out_, mIn_, m1_, m2_, vecs_] := Module[{d, a, sq},
   d = treeDiagrams$[{in}, out];
   a = treeAmps$[d, {k}, {p1, p2}];
   FCClearScalarProducts[];
   ScalarProduct[k, k] = mIn^2; ScalarProduct[p1, p1] = m1^2; ScalarProduct[p2, p2] = m2^2;
   ScalarProduct[k, p1] = (mIn^2 + m1^2 - m2^2)/2; ScalarProduct[k, p2] = (mIn^2 - m1^2 + m2^2)/2;
   ScalarProduct[p1, p2] = (mIn^2 - m1^2 - m2^2)/2;
   sq = sumSq$[Total[a], vecs];
   sq];

wHand$[nc_, m1_, m2_] := Module[{x1 = m1^2/MW^2, x2 = m2^2/MW^2},
   nc (ee/sw)^2 MW^2 (1 - (x1 + x2)/2 - (x1 - x2)^2/2)];
resW$ = {
  checkT$["W+ -> t bbar", decay$[V[3], {F[3, {3}], -F[4, {3}]}, MW, MT, MB, {k}], wHand$[3, MT, MB]],
  checkT$["W+ -> c sbar", decay$[V[3], {F[3, {2}], -F[4, {2}]}, MW, MC, MS, {k}], wHand$[3, MC, MS]],
  checkT$["W+ -> nu_tau tau+", decay$[V[3], {F[1, {3}], -F[2, {3}]}, MW, 0, MTA, {k}], wHand$[1, 0, MTA]]};

zHand$[nc_, q_, t3_, m_] := Module[{x = m^2/MZ^2, gl = gLT$[q, t3], gr = gRT$[q]},
   2 nc ee^2 MZ^2 ((gl^2 + gr^2) (1 - x) + 6 gl gr x)];
resZ$ = {
  checkT$["Z -> b bbar", decay$[V[2], {F[4, {3}], -F[4, {3}]}, MZ, MB, MB, {k}], zHand$[3, -1/3, -1/2, MB]],
  checkT$["Z -> t tbar", decay$[V[2], {F[3, {3}], -F[3, {3}]}, MZ, MT, MT, {k}], zHand$[3, 2/3, 1/2, MT]],
  checkT$["Z -> tau+ tau-", decay$[V[2], {F[2, {3}], -F[2, {3}]}, MZ, MTA, MTA, {k}], zHand$[1, -1, -1/2, MTA]],
  checkT$["Z -> nu nubar", decay$[V[2], {F[1, {1}], -F[1, {1}]}, MZ, 0, 0, {k}], zHand$[1, 0, 1/2, 0]]};

hHand$[nc_, m_] := 2 nc m^2 MH^2 (1 - 4 m^2/MH^2)/(2 MW sw/ee)^2;
resH$ = {
  checkT$["H -> b bbar", decay$[S[1], {F[4, {3}], -F[4, {3}]}, MH, MB, MB, {}], hHand$[3, MB]],
  checkT$["H -> t tbar", decay$[S[1], {F[3, {3}], -F[3, {3}]}, MH, MT, MT, {}], hHand$[3, MT]],
  checkT$["H -> tau+ tau-", decay$[S[1], {F[2, {3}], -F[2, {3}]}, MH, MTA, MTA, {}], hHand$[1, MTA]]};

(* summed over the colours too (3); the width averages over the top spin and colour *)
tHand$ = 3 (ee/sw)^2/(2 MW^2) ((MT^2 - MB^2)^2 + MW^2 (MT^2 + MB^2) - 2 MW^4);
resT$ = {checkT$["t -> b W+", decay$[F[3, {3}], {F[4, {3}], V[3]}, MT, MB, MW, {p2}], tHand$]};


(* ::Section:: *)
(*e+ e- -> mu+ mu- (massless, gamma + Z)*)


(* ::Text:: *)
(*e-(p1) e+(p2) -> mu-(k1) mu+(k2).  Me = MMU = 0 removes the H and G0 exchanges.  t = (p1 - k1)^2.*)


diagsMM$ = treeDiagrams$[{F[2, {1}], -F[2, {1}]}, {F[2, {2}], -F[2, {2}]}];
ampMM$ = treeAmps$[diagsMM$, {p1, p2}, {k1, k2}, {Me -> 0, MMU -> 0}];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, 0, 0, 0, 0];
mMM$ = FeynAmpDenominatorExplicit[Total[ampMM$]];
sqMM$ = sumSq$[mMM$, {}] /. u -> -s - t;
Print["e+ e- -> mu+ mu-: d(sum|M|^2)/d xiA, d xiZ (expect 0, 0): ",
  Simplify[{D[sqMM$, xiA], D[sqMM$, xiZ]}]];
(* sign of the photon amplitude: Q_e Q_mu/s = +1/s; the helicity amplitudes are real for Gamma_Z = 0 *)
aLLMM$ = Function[{i, j}, 1/s + {gLT$[-1, -1/2], gRT$[-1]}[[i]] {gLT$[-1, -1/2], gRT$[-1]}[[j]]/(s - MZ^2)];
sqMMnote$ = 4 ee^4 (u^2 (aLLMM$[1, 1]^2 + aLLMM$[2, 2]^2) + t^2 (aLLMM$[1, 2]^2 + aLLMM$[2, 1]^2)) /. u -> -s - t;
resMM$ = checkT$["e+ e- -> mu+ mu- sum|M|^2 (Eq. (eeff), Gamma_Z = 0)", sqMM$, sqMMnote$];


(* ::Section:: *)
(*e+ e- -> W+ W- (massless electron)*)


(* ::Text:: *)
(*e-(p1) e+(p2) -> W-(k1) W+(k2), t = (p1 - k1)^2.  Three diagrams (s-channel gamma, Z; t-channel nu_e).  The*)
(*polarization sums use -g + k k/MW^2.  The result is evaluated at the points of tree_numeric.py and written out.*)


diagsWW$ = treeDiagrams$[{F[2, {1}], -F[2, {1}]}, {-V[3], V[3]}];
ampWW$ = treeAmps$[diagsWW$, {p1, p2}, {k1, k2}, {Me -> 0}];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, 0, 0, MW, MW];
mWW$ = FeynAmpDenominatorExplicit[Total[ampWW$]];
sqWW$ = sumSq$[mWW$, {k1, k2}] /. u -> 2 MW^2 - s - t;
Print["e+ e- -> W+ W-: d(sum|M|^2)/d xiA, xiZ, xiW (expect 0, 0, 0): ",
  Simplify[{D[sqWW$, xiA], D[sqWW$, xiZ], D[sqWW$, xiW]}]];
sqWW$ = Simplify[sqWW$ /. {xiA -> 1, xiZ -> 1, xiW -> 1}];
bench$ = {ee -> Sqrt[4 Pi/128], MW -> 80, MZ -> 91, sw -> Sqrt[1 - 80^2/91^2], cw -> 80/91};
ptsWW$ = Flatten[Table[{rs, c}, {rs, {200, 500, 3000}}, {c, {-0.9, 0., 0.7}}], 1];
rowsWW$ = Table[Module[{sv = p[[1]]^2, beta, tv},
     beta = Sqrt[1 - 4 80^2/sv];
     tv = 80^2 - sv/2 (1 - beta p[[2]]);
     {p[[1]], p[[2]], N[sqWW$ /. bench$ /. {s -> sv, t -> tv}, 20]}], {p, ptsWW$}];
Export[FileNameJoin[{resDirTree$, "tree_eeww_points.csv"}],
  Prepend[rowsWW$ /. x_Real :> CForm[x], {"sqrt_s", "cos_theta", "sumM2_feyncalc"}], "CSV"];
Print["e+ e- -> W+ W- sum|M|^2 at the benchmark (sqrt s, cos theta, value): ", rowsWW$ // N];


(* ::Section:: *)
(*Summary*)


allTree$ = Join[resW$, resZ$, resH$, resT$, {resMM$}];
Print["Squared amplitudes compared: ", Length[allTree$], ", nonzero differences: ", Count[allTree$, x_ /; x =!= 0]];
