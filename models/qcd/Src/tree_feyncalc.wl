(* ::Package:: *)

(* ::Title:: *)
(*Step (2): tree-level amplitudes, spin/colour sums and gluon polarization sums with FeynArts + FeynCalc (QCD)*)


(* ::Text:: *)
(*Research note models/qcd, step (2): compare with Eq. (12) (eq:Mtree), Eq. (13) (eq:sumtree) and Eq. (14) (eq:ghostsum).*)
(*  (A) u(p1) ubar(p2) -> t(k1) tbar(k2):  M = g^2/s [vbar(p2) g^nu T^a u(p1)] [ubar(k1) g_nu T^a v(k2)]*)
(*  (B) g(p1,a) g(p2,b) -> t(k1) tbar(k2): M = -g^2 ubar(k1) [T^a T^b e1 (k1-p1+m) e2/(t-m^2) + T^b T^a e2 (k1-p2+m) e1/(u-m^2)*)
(*        + [T^a,T^b]/s ((e1.e2)(p1-p2) + 2(e1.p2) e2 - 2(e2.p1) e1)] v(k2)*)
(*  (C) g(p1,a) g(p2,b) -> g(k1,c) g(k2,d): the four Feynman-rule diagrams of Fig. 1 (s, t, u channel and contact)*)
(*  (D) e-(p1) e+(p2) -> u(k1) ubar(k2) g(k3): M = e^2 Q_u g/s [vbar(p2) g_nu u(p1)] ubar(k1) T^a [e*(k1+k3) g^nu/(2k1.k3)*)
(*        - g^nu (k2+k3) e*/(2k2.k3)] v(k2)*)
(*sum|M|^2 is the sum (not the average) over spins, polarizations and colours.  Gauge structure at tree level:*)
(*  - (A), (B): the (1 - xi) k k/k^2 part of the gluon propagator drops out (dM/dxi = 0);*)
(*  - (B): the -g polarization sum minus the physical one equals |M(c cbar -> t tbar)|^2 + |M(cbar c -> t tbar)|^2,*)
(*    and each ghost amplitude equals -(g^2/s) ubar [T^a,T^b] p2slash v (note App. I);*)
(*  - (C): the amplitude is evaluated with exact rational kinematics and explicit polarization vectors (the symbolic*)
(*    physical polarization sum over four gluons did not finish in 30 min): it is compared with the Feynman rules of*)
(*    the note diagram by diagram through colour projections, the Ward identity is checked, and the colour-summed*)
(*    |M|^2 is compared with Eq. (13).*)
(*Uses the FeynArts model in Src/generated/QCD_FA (run generate_QCD.wl first); a copy is patched with FAPatch.*)
(*Symbols: gS = g (FeynArts GS; NOT GS, which is FeynCalc's slash), mt = m (MT), eQ = e (EL), xi = GaugeXi[G].*)


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
modelTmpDirTree$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTree$, "generated", "QCD_FA"}], FileNameJoin[{modelTmpDirTree$, "QCD_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirTree$, "QCD_FA"}], Quiet -> True];
modelFileTree$ = FileNameJoin[{modelTmpDirTree$, "QCD_FA", "QCD_FA"}];


(* ::Text:: *)
(*Helpers.  Field codes of the FeynArts model: F[1] = e-, F[2] = u, F[7] = t, V[1] = photon, V[2] = gluon, U[1] = ghost.*)
(*M$FACouplings is applied by hand.  FCFAConvert writes the strong coupling as SMP["g_s"] and the gauge parameter of an*)
(*internal gluon as GaugeXi[V[2, {colour index}]]; both are replaced by plain symbols (a colour index inside GaugeXi*)
(*would appear three times and stop SUNSimplify).  External colours: SUNFIndex[Coli] for quark leg i, SUNIndex[Glui]*)
(*for gluon leg i (legs numbered 1, 2 incoming, 3, 4, ... outgoing).*)


treeDiagrams$[in_, out_, excl_] := InsertFields[CreateTopologies[0, Length[in] -> Length[out]], in -> out,
   InsertionLevel -> {Particles}, Model -> modelFileTree$, GenericModel -> modelFileTree$, ExcludeParticles -> excl];
treeAmps$[diags_, in_, out_] := FCFAConvert[CreateFeynAmp[diags, GaugeRules -> {}] /. M$FACouplings,
   IncomingMomenta -> in, OutgoingMomenta -> out, ChangeDimension -> 4, List -> True, SMP -> False,
   UndoChiralSplittings -> True, DropSumOver -> True, TransversePolarizationVectors -> {}] /.
   {SMP["g_s"] -> gS, FCGV["GS"] -> gS, FCGV["EL"] -> eQ, SMP["e"] -> eQ, FCGV["MT"] -> mt, SMP["m_t"] -> mt,
    GaugeXi[V[2, ___]] -> xi, GaugeXi[G] -> xi};
(* traces evaluated explicitly: replacing DiracTrace by Tr leaves Tr unevaluated (Yukawa-note gotcha) *)
evalTree$[x_] := Simplify[Contract[FeynAmpDenominatorExplicit[SUNSimplify[DiracSimplify[
       x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]], SUNNToCACF -> True]]] /. SUNN -> CA];
spinColTree$[amp_] := evalTree$[FermionSpinSum[ComplexConjugate[amp] amp]];
toCF$ = CF -> (CA^2 - 1)/(2 CA);
ub$[q_, m_] := Spinor[Momentum[q], m, 1];  uu$[q_, m_] := Spinor[Momentum[q], m, 1];
vb$[q_, m_] := Spinor[-Momentum[q], m, 1]; vv$[q_, m_] := Spinor[-Momentum[q], m, 1];
epsIn$[k_] := Momentum[Polarization[k, I]];  epsOut$[k_] := Momentum[Polarization[k, -I]];
TF = 1/2;


(* ::Section:: *)
(*(A)  u ubar -> t tbar*)


diagsA$ = treeDiagrams$[{F[2], -F[2]}, {F[7], -F[7]}, {V[1]}];


(* ::Subsubsection:: *)
(*Inspect: the diagram (s-channel gluon)*)


If[$Notebooks,
  Show[#, ImageSize -> 260] & /@ Render[Paint[diagsA$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampA$ = treeAmps$[diagsA$, {p1, p2}, {k1, k2}];
Print["(A) number of diagrams (expect 1): ", Length[ampA$]];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, 0, 0, mt, mt];
mA$ = FeynAmpDenominatorExplicit[Total[ampA$]];
Print["(A) d M/d xi after the Dirac equation (expect 0): ", Simplify[DiracSimplify[D[mA$, xi]]]];
mA$ = mA$ /. xi -> 1;
mAnote$ = gS^2/s SUNTF[{SUNIndex[aa]}, SUNFIndex[Col2], SUNFIndex[Col1]] SUNTF[{SUNIndex[aa]}, SUNFIndex[Col3], SUNFIndex[Col4]] *
   (vb$[p2, 0] . GA[nu] . uu$[p1, 0]) (ub$[k1, mt] . GA[nu] . vv$[k2, mt]);
mAnote$ = FCI[mAnote$];
dmA$ = Simplify[spinColTree$[mA$ - mAnote$] /. u -> 2 mt^2 - s - t /. toCF$];
spA$ = Simplify[spinColTree$[mA$ + mAnote$] /. u -> 2 mt^2 - s - t /. toCF$];
Print["(A) sum|M(FC) - M(note)|^2 = ", dmA$, ",  sum|M(FC) + M(note)|^2 = ", spA$, "   (expect one of them 0)"];
sqA$ = spinColTree$[mA$];
sqAnote$ = 8 gS^4 TF^2 (CA^2 - 1) ((t - mt^2)^2 + (u - mt^2)^2 + 2 mt^2 s)/s^2;
Print["(A) sum|M|^2(FeynCalc) - Eq. (13) = ", Simplify[(sqA$ - sqAnote$) /. toCF$ /. u -> 2 mt^2 - s - t], "   (expect 0)"];


(* ::Section:: *)
(*(B)  g g -> t tbar, and the ghost pairs*)


diagsB$ = treeDiagrams$[{V[2], V[2]}, {F[7], -F[7]}, {V[1]}];


(* ::Subsubsection:: *)
(*Inspect: the three diagrams (t, u channel quark, s channel gluon)*)


If[$Notebooks,
  Show[#, ImageSize -> 420] & /@ Render[Paint[diagsB$, ColumnsXRows -> {3, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampB$ = treeAmps$[diagsB$, {p1, p2}, {k1, k2}];
Print["(B) number of diagrams (expect 3): ", Length[ampB$]];
FCClearScalarProducts[];
SetMandelstam[s, t, u, p1, p2, -k1, -k2, 0, 0, mt, mt];
mB$ = FeynAmpDenominatorExplicit[Total[ampB$]];
Print["(B) d M/d xi after the Dirac equation (expect 0): ", Simplify[DiracSimplify[D[mB$, xi]]]];
mB$ = mB$ /. xi -> 1;
e1$ = epsIn$[p1]; e2$ = epsIn$[p2];
TaTb$ = SUNTF[{SUNIndex[Glu1], SUNIndex[Glu2]}, SUNFIndex[Col3], SUNFIndex[Col4]];
TbTa$ = SUNTF[{SUNIndex[Glu2], SUNIndex[Glu1]}, SUNFIndex[Col3], SUNFIndex[Col4]];
mBnote$ = -gS^2 (TaTb$ ub$[k1, mt] . GS[e1$] . (GS[k1 - p1] + mt) . GS[e2$] . vv$[k2, mt]/(t - mt^2) +
     TbTa$ ub$[k1, mt] . GS[e2$] . (GS[k1 - p2] + mt) . GS[e1$] . vv$[k2, mt]/(u - mt^2) +
     (TaTb$ - TbTa$)/s ub$[k1, mt] . (Pair[e1$, e2$] (GS[p1] - GS[p2]) + 2 Pair[e1$, Momentum[p2]] GS[e2$] -
         2 Pair[e2$, Momentum[p1]] GS[e1$]) . vv$[k2, mt]);
mBnote$ = FCI[mBnote$];
physB$[x_] := Simplify[DoPolarizationSums[DoPolarizationSums[
      SUNSimplify[DiracSimplify[FermionSpinSum[ComplexConjugate[x] x] /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]],
       SUNNToCACF -> True], p1, p2], p2, p1] // FeynAmpDenominatorExplicit // Contract // ReplaceAll[#, SUNN -> CA] & //
     ReplaceAll[#, toCF$] & // ReplaceAll[#, u -> 2 mt^2 - s - t] &];
dmB$ = physB$[mB$ - mBnote$]; spB$ = physB$[mB$ + mBnote$];
Print["(B) physical sum |M(FC) - M(note)|^2 = ", dmB$, ",  |M(FC) + M(note)|^2 = ", spB$, "   (expect one of them 0)"];
sqBphys$ = physB$[mB$];
sqBminusg$ = Simplify[DoPolarizationSums[DoPolarizationSums[
       SUNSimplify[DiracSimplify[FermionSpinSum[ComplexConjugate[mB$] mB$] /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]],
        SUNNToCACF -> True], p1, 0], p2, 0] // FeynAmpDenominatorExplicit // Contract // ReplaceAll[#, SUNN -> CA] & //
     ReplaceAll[#, toCF$] & // ReplaceAll[#, u -> 2 mt^2 - s - t] &];
tau1$ = (mt^2 - t)/s; tau2$ = (mt^2 - u)/s; rho$ = 4 mt^2/s;
sqBnote$ = 8 gS^4 CA CF (CF/(tau1$ tau2$) - CA) (tau1$^2 + tau2$^2 + rho$ - rho$^2/(4 tau1$ tau2$));
Print["(B) physical sum|M|^2(FeynCalc) - Eq. (13) = ", Simplify[(sqBphys$ - sqBnote$) /. toCF$ /. u -> 2 mt^2 - s - t], "   (expect 0)"];
Print["(B) SU(3), initial average: sum/256 - Combridge = ",
  Simplify[(sqBphys$/256 /. CA -> 3) - gS^4 (1/(6 tau1$ tau2$) - 3/8) (tau1$^2 + tau2$^2 + rho$ - rho$^2/(4 tau1$ tau2$)) /. u -> 2 mt^2 - s - t],
  "   (expect 0)"];


(* ::Text:: *)
(*Ghost pairs c(p1, a) cbar(p2, b) -> t tbar and cbar(p1, a) c(p2, b) -> t tbar (one s-channel diagram each).*)
(*Eq. (14): sum_{-g} - sum_phys = sum|M(c cbar)|^2 + sum|M(cbar c)|^2 and sum|M(c cbar)|^2 = g^4 C_A d_A tau1 tau2.*)
(*App. I: M(c cbar -> t tbar) = -(g^2/s) ubar [T^a, T^b] p2slash v.*)


diagsG1$ = treeDiagrams$[{U[1], -U[1]}, {F[7], -F[7]}, {V[1]}];
diagsG2$ = treeDiagrams$[{-U[1], U[1]}, {F[7], -F[7]}, {V[1]}];


(* ::Subsubsection:: *)
(*Inspect: the ghost-pair diagrams (s-channel gluon)*)


If[$Notebooks,
  (* FeynArts cannot Join the TopologyLists of two processes: paint them separately *)
  {Show[#, ImageSize -> 160] & /@ Render[Paint[diagsG1$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 160] & /@ Render[Paint[diagsG2$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]]}
]


ampG1$ = treeAmps$[diagsG1$, {p1, p2}, {k1, k2}];
ampG2$ = treeAmps$[diagsG2$, {p1, p2}, {k1, k2}];
Print["(B) ghost diagrams (expect 1, 1): ", {Length[ampG1$], Length[ampG2$]}];
mG1$ = FeynAmpDenominatorExplicit[Total[ampG1$]] /. xi -> 1;
mG2$ = FeynAmpDenominatorExplicit[Total[ampG2$]] /. xi -> 1;
gh1$ = Simplify[spinColTree$[mG1$] /. toCF$ /. u -> 2 mt^2 - s - t];
gh2$ = Simplify[spinColTree$[mG2$] /. toCF$ /. u -> 2 mt^2 - s - t];
Print["(B) sum|M(c cbar)|^2, sum|M(cbar c)|^2 minus g^4 CA dA tau1 tau2 = ",
  Simplify[{gh1$, gh2$} - gS^4 CA (CA^2 - 1) tau1$ tau2$ /. u -> 2 mt^2 - s - t], "   (expect {0, 0})"];
Print["(B) sum_{-g} - sum_phys - (ghost pairs) = ", Simplify[sqBminusg$ - sqBphys$ - gh1$ - gh2$], "   (expect 0)"];
mGnote$ = FCI[-gS^2/s (TaTb$ - TbTa$) ub$[k1, mt] . GS[p2] . vv$[k2, mt]];
Print["(B) ghost amplitude: sum|M(FC) - M(note)|^2, sum|M(FC) + M(note)|^2 = ",
  Simplify[{spinColTree$[mG1$ - mGnote$], spinColTree$[mG1$ + mGnote$]} /. toCF$ /. u -> 2 mt^2 - s - t], "   (expect one of them 0)"];


(* ::Section:: *)
(*(C)  g g -> g g  with exact rational kinematics*)


(* ::Text:: *)
(*Kinematics: p1 = (5,0,0,5), p2 = (5,0,0,-5), k1 = (5,3,0,4), k2 = (5,-3,0,-4) (s = 100, t = -10, u = -90, cos = 4/5),*)
(*with real transverse polarizations: e(p1), e(p2) in {x, y}, e(k1) in {(0,4/5,0,-3/5), y}, e(k2) in {(0,-4/5,0,3/5), y}.*)
(*All scalar products are set to exact numbers, so every comparison is an exact rational identity.*)
(*Colour: the FeynArts amplitude is projected on c1 = f^{abe}f^{cde} and c2 = f^{ace}f^{bde} (a, b, c, d = Glu1..Glu4);*)
(*f^{ade}f^{bce} = c2 - c1 (Jacobi), sum c1 c1 = sum c2 c2 = C_A^2 d_A, sum c1 c2 = C_A^2 d_A/2.*)


diagsC$ = treeDiagrams$[{V[2], V[2]}, {V[2], V[2]}, {V[1]}];


(* ::Subsubsection:: *)
(*Inspect: the four diagrams (s, t, u channel gluon and the contact term)*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diagsC$, ColumnsXRows -> {4, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampC$ = treeAmps$[diagsC$, {p1, p2}, {k1, k2}];
Print["(C) number of diagrams (expect 4): ", Length[ampC$]];
FCClearScalarProducts[];
vecC$ = <|p1 -> {5, 0, 0, 5}, p2 -> {5, 0, 0, -5}, k1 -> {5, 3, 0, 4}, k2 -> {5, -3, 0, -4}|>;
polC$ = <|p1 -> {{0, 1, 0, 0}, {0, 0, 1, 0}}, p2 -> {{0, 1, 0, 0}, {0, 0, 1, 0}},
   k1 -> {{0, 4/5, 0, -3/5}, {0, 0, 1, 0}}, k2 -> {{0, -4/5, 0, 3/5}, {0, 0, 1, 0}}|>;
mink$[a_, b_] := a[[1]] b[[1]] - a[[2 ;;]] . b[[2 ;;]];
(* replace the polarization momenta by plain symbols e1..e4, then set all scalar products *)
mC$ = FeynAmpDenominatorExplicit[Total[ampC$]] /. {Momentum[Polarization[p1, ___], ___] -> Momentum[e1],
     Momentum[Polarization[p2, ___], ___] -> Momentum[e2], Momentum[Polarization[k1, ___], ___] -> Momentum[e3],
     Momentum[Polarization[k2, ___], ___] -> Momentum[e4]};
setVecsC$[pols_] := Module[{all = Join[Normal[vecC$], {e1 -> pols[[1]], e2 -> pols[[2]], e3 -> pols[[3]], e4 -> pols[[4]]}]},
   FCClearScalarProducts[];
   Do[ScalarProduct[a[[1]], b[[1]]] = mink$[a[[2]], b[[2]]], {a, all}, {b, all}]];
(* the projectors use their own dummy index hh (the note's amplitude below uses ee) *)
c1$ = SUNF[SUNIndex[Glu1], SUNIndex[Glu2], SUNIndex[hh]] SUNF[SUNIndex[Glu3], SUNIndex[Glu4], SUNIndex[hh]];
c2$ = SUNF[SUNIndex[Glu1], SUNIndex[Glu3], SUNIndex[hh]] SUNF[SUNIndex[Glu2], SUNIndex[Glu4], SUNIndex[hh]];
projC$[x_, c_] := Simplify[SUNSimplify[Expand[ExpandScalarProduct[Contract[FCI[x]]]] c, SUNNToCACF -> False] /. SUNN -> 3];
numC$ = {s -> 100, t -> -10, u -> -90, gS -> 1};
(* the note's diagrams (Feynman rules of Fig. 1), with incoming momenta p1, p2, -k1, -k2 and polarizations e1..e4 *)
v3$[{m1_, q1_}, {m2_, q2_}, {m3_, q3_}] := MT[m1, m2] FV[q1 - q2, m3] + MT[m2, m3] FV[q2 - q3, m1] + MT[m3, m1] FV[q3 - q1, m2];
pc$ = Contract[ExpandScalarProduct[#]] &;
lorS$ = pc$[FV[e1, mu] FV[e2, nu] v3$[{mu, p1}, {nu, p2}, {al, -p1 - p2}] v3$[{al, p1 + p2}, {ro, -k1}, {si, -k2}] FV[e3, ro] FV[e4, si]];
lorT$ = pc$[FV[e1, mu] FV[e3, ro] v3$[{mu, p1}, {ro, -k1}, {al, k1 - p1}] v3$[{al, p1 - k1}, {nu, p2}, {si, -k2}] FV[e2, nu] FV[e4, si]];
lorU$ = pc$[FV[e1, mu] FV[e4, si] v3$[{mu, p1}, {si, -k2}, {al, k2 - p1}] v3$[{al, p1 - k2}, {nu, p2}, {ro, -k1}] FV[e2, nu] FV[e3, ro]];
sp$[a_, b_] := Pair[Momentum[a], Momentum[b]];
f4$[a_, b_, c_, d_] := SUNF[SUNIndex[a], SUNIndex[b], SUNIndex[ee]] SUNF[SUNIndex[c], SUNIndex[d], SUNIndex[ee]];
mCnote$ = -gS^2/s f4$[Glu1, Glu2, Glu3, Glu4] lorS$ - gS^2/t f4$[Glu1, Glu3, Glu2, Glu4] lorT$ -
   gS^2/u f4$[Glu1, Glu4, Glu2, Glu3] lorU$ -
   gS^2 (f4$[Glu1, Glu2, Glu3, Glu4] (sp$[e1, e3] sp$[e2, e4] - sp$[e1, e4] sp$[e2, e3]) +
      f4$[Glu1, Glu3, Glu2, Glu4] (sp$[e1, e2] sp$[e3, e4] - sp$[e1, e4] sp$[e2, e3]) +
      f4$[Glu1, Glu4, Glu2, Glu3] (sp$[e1, e2] sp$[e3, e4] - sp$[e1, e3] sp$[e2, e4]));
(* SU(3): Gram matrix of {c1, c2} *)
gramC$ = 72 {{1, 1/2}, {1/2, 1}};
resC$ = Table[
   setVecsC$[{polC$[p1][[i1]], polC$[p2][[i2]], polC$[k1][[i3]], polC$[k2][[i4]]}];
   Module[{x = mC$ /. xi -> 1 /. numC$, dx = D[mC$, xi] /. numC$, y = mCnote$ /. numC$, pFC, pNote, aFC},
    pFC = {projC$[x, c1$], projC$[x, c2$]};
    pNote = {projC$[y, c1$], projC$[y, c2$]};
    aFC = LinearSolve[gramC$, pFC];
    {pFC - pNote, pFC + pNote, Simplify[Conjugate[aFC] . gramC$ . aFC], {projC$[dx, c1$], projC$[dx, c2$]}}],
   {i1, 2}, {i2, 2}, {i3, 2}, {i4, 2}];
resC$ = Flatten[resC$, 3];
Print["(C) colour projections, M(FC) - M(note) for all 16 polarizations (expect all 0): ", Union[Flatten[resC$[[All, 1]]]],
  ",  M(FC) + M(note): ", Union[Flatten[resC$[[All, 2]]]]];
Print["(C) colour projections of d M/d xi (expect all 0): ", Union[Flatten[resC$[[All, 4]]]]];
sqC$ = Total[resC$[[All, 3]]];
sqCnote$ = 16 gS^4 9 8 (3 - t u/s^2 - s u/t^2 - s t/u^2) /. numC$;
Print["(C) sum|M|^2 at s = 100, cos = 4/5: FeynCalc ", sqC$, ", Eq. (13) ", sqCnote$, ", difference ", Simplify[sqC$ - sqCnote$], "   (expect 0)"];
(* Ward identity: e1 -> p1 with the other three physical polarizations *)
wardC$ = Table[
   setVecsC$[{vecC$[p1], polC$[p2][[i2]], polC$[k1][[i3]], polC$[k2][[i4]]}];
   {projC$[mC$ /. xi -> 1 /. numC$, c1$], projC$[mC$ /. xi -> 1 /. numC$, c2$]},
   {i2, 2}, {i3, 2}, {i4, 2}];
Print["(C) Ward identity e(p1) -> p1 (expect all 0): ", Union[Flatten[wardC$]]];
FCClearScalarProducts[];


(* ::Section:: *)
(*(D)  e+ e- -> u ubar g*)


diagsD$ = treeDiagrams$[{F[1], -F[1]}, {F[2], -F[2], V[2]}, {}];


(* ::Subsubsection:: *)
(*Inspect: the two diagrams (gluon from the quark or the antiquark)*)


If[$Notebooks,
  Show[#, ImageSize -> 320] & /@ Render[Paint[diagsD$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]]
]


ampD$ = treeAmps$[diagsD$, {p1, p2}, {k1, k2, k3}];
Print["(D) number of diagrams (expect 2): ", Length[ampD$]];


(* ::Text:: *)
(*x_i = 2 E_i/sqrt(s) with 2 k_i.Q = x_i s: k1.k2 = s(1-x3)/2, k1.k3 = s(1-x2)/2, k2.k3 = s(1-x1)/2.  The lepton*)
(*directions are averaged at fixed hadron momenta: <p1^mu p2^nu> = Q^mu Q^nu/6 + s g^{mu nu}/12 (note App. I).*)


FCClearScalarProducts[];
SP[p1, p1] = 0; SP[p2, p2] = 0; SP[k1, k1] = 0; SP[k2, k2] = 0; SP[k3, k3] = 0; SP[p1, p2] = s/2;
SP[k1, k2] = s (1 - x3)/2; SP[k1, k3] = s (1 - x2)/2; SP[k2, k3] = s (1 - x1)/2;
mD$ = FeynAmpDenominatorExplicit[Total[ampD$] /. FeynAmpDenominator[PropagatorDenominator[Momentum[k1 + k2 + k3], 0]] ->
      FeynAmpDenominator[PropagatorDenominator[Momentum[p1 + p2], 0]]];
mDnote$ = FCI[eQ^2 (2/3) gS/s SUNTF[{SUNIndex[Glu5]}, SUNFIndex[Col3], SUNFIndex[Col4]] (vb$[p2, 0] . GA[nu] . uu$[p1, 0]) *
    ((ub$[k1, 0] . GS[epsOut$[k3]] . (GS[k1] + GS[k3]) . GA[nu] . vv$[k2, 0])/(2 SP[k1, k3]) -
     (ub$[k1, 0] . GA[nu] . (GS[k2] + GS[k3]) . GS[epsOut$[k3]] . vv$[k2, 0])/(2 SP[k2, k3]))];
xxD$[k1] = x1; xxD$[k2] = x2; xxD$[k3] = x3;
avgD$[expr_] := Module[{y = Expand[FCE[ExpandScalarProduct[expr]]]},
   y = y /. SP[p1, a_] SP[p2, b_] :> (1/6) (xxD$[a] s/2) (xxD$[b] s/2) + (s/12) SP[a, b];
   y = y /. SP[p2, a_] SP[p1, b_] :> (1/6) (xxD$[a] s/2) (xxD$[b] s/2) + (s/12) SP[a, b];
   Simplify[y /. x3 -> 2 - x1 - x2]];
physD$[x_] := avgD$[Contract[FeynAmpDenominatorExplicit[SUNSimplify[DiracSimplify[DoPolarizationSums[
         FermionSpinSum[ComplexConjugate[x] x], k3, k1] /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]],
        SUNNToCACF -> True]]] /. SUNN -> CA];
Print["(D) orientation-averaged physical sum |M(FC) - M(note)|^2, |M(FC) + M(note)|^2 = ",
  Simplify[{physD$[mD$ - mDnote$], physD$[mD$ + mDnote$]}], "   (expect one of them 0)"];
sqD$ = physD$[mD$];
m0$ = treeAmps$[treeDiagrams$[{F[1], -F[1]}, {F[2], -F[2]}, {}], {p1, p2}, {k1, k2}];
FCClearScalarProducts[];
SP[p1, p1] = 0; SP[p2, p2] = 0; SP[k1, k1] = 0; SP[k2, k2] = 0; SP[p1, p2] = s/2; SP[k1, k2] = s/2;
xxD$[k1] = 1; xxD$[k2] = 1;
sq0$ = avgD$[Contract[FeynAmpDenominatorExplicit[SUNSimplify[DiracSimplify[FermionSpinSum[ComplexConjugate[Total[m0$]] Total[m0$]] /.
         DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]], SUNNToCACF -> True]]] /. SUNN -> CA];
xxD$[k1] = x1; xxD$[k2] = x2;
Print["(D) orientation-averaged Born sum|M0|^2 (expect 64 CA e^4/27 = N_c Q_u^2 e^4 x 16/3): ", sq0$];
ratioD$ = Simplify[(sqD$ s/(128 Pi^3))/(sq0$/(8 Pi))];
Print["(D) (1/sigma0) dsigma/dx1 dx2 / [CF alpha_s/2pi (x1^2+x2^2)/((1-x1)(1-x2))] (expect 1): ",
  Simplify[ratioD$/(CF gS^2/(8 Pi^2) (x1^2 + x2^2)/((1 - x1) (1 - x2))) /. toCF$]];


(* ::Section:: *)
(*Check point for tree_sigma.py*)


(* ::Text:: *)
(*sqrt(s) = 5, cos(theta) = 0.3 (angle of k1 to p1 in the CM frame), m = 1, g = 1, SU(3).*)


ptVals$[m_] := Module[{ss = 25, c = 3/10, beta},
   beta = Sqrt[1 - 4 m^2/ss];
   {s -> ss, t -> m^2 - ss/2 (1 - beta c), u -> m^2 - ss/2 (1 + beta c)}];
Print["(A) check point: ", ToString[NumberForm[N[sqAnote$ /. ptVals$[1] /. {mt -> 1, gS -> 1, CA -> 3}, 20], 16]]];
Print["(B) check point: ", ToString[NumberForm[N[sqBnote$ /. toCF$ /. ptVals$[1] /. {mt -> 1, gS -> 1, CA -> 3}, 20], 16]]];
Print["(C) check point: ", ToString[NumberForm[N[16 gS^4 9 8 (3 - t u/s^2 - s u/t^2 - s t/u^2) /. ptVals$[0] /. gS -> 1, 20], 16]]];
