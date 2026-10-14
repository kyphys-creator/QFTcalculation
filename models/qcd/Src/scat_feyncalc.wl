(* ::Package:: *)

(* ::Title:: *)
(*Step (4): one-loop q qbar -> Q Qbar and g g -> Q Qbar in a general covariant gauge (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/qcd, step (4), first stage.  Process (A) u(p1) ubar(p2) -> t(k1) tbar(k2), (B) g(p1) g(p2) -> t(k1) tbar(k2),*)
(*at m = 1, s = 10, t = (p1 - k1)^2 = -3 (u = -5), g = 1, general xi; CDR (Dirac algebra, spin and polarization sums in D dims).*)
(*(a) FeynArts diagrams from Src/generated/QCD_FA (photon, electron excluded), tadpoles and external self-energies excluded:*)
(*    (A) 15, (B) 46.  FCFAConvert with FeynArts' prefactor: the loop amplitude carries I/(16 Pi^4) and int d^4 l becomes*)
(*    int d^D l; scat_eval.wl adds the MS-bar normalization.*)
(*(b) trees: Born in D dims (the physical polarization sum -g + (p n + n p)/(p.n) with n = the other gluon), the colour*)
(*    correlations <T_i.T_j> (generators inserted into the colour sums, all particles outgoing), and for the counterterms*)
(*    of (B) the interference with each tree diagram (s, t, u channel) and the derivative with respect to the mass of the*)
(*    internal top line.  -> work/scat/{A,B}/tree.m*)
(*(c) the one-loop interference W_i = sum M0^* M1_i of each diagram, by powers of eta = 1 - xi and by tree diagram (smaller*)
(*    expressions): the gauge parts of s-channel gluon propagators are*)
(*    dropped (they end on the conserved top current, or on the external three-gluon vertex, where they vanish after the*)
(*    physical polarization sums); Dirac algebra and colour on the amplitude, then spin, polarization and colour sums; the*)
(*    loop momentum is shifted so that the propagators of each term are a subset of one of nine families (F1, F2, F3 for*)
(*    (A), plus the boxes G1..G6 for (B)), and the numerators are written in the propagators of that family -> integrals*)
(*    GLI[family, {n1..n4}] (FeynCalc's FCLoopFindTopologies is not used: with the numeric kinematics it misses momentum*)
(*    shifts).  -> work/scat/{A,B}/d<i>.m  (scat_litered.wl reduces them)*)
(*(d) the same interference in Feynman gauge by tensor reduction (TID, PaVe functions; no doubled propagators at xi = 1), an*)
(*    independent route for the comparison in scat_eval.wl.  -> work/scat/{A,B}/tid_<i>.m*)
(*(e) unitarity of (A): integrands of the s-channel two-particle cuts sum M0^*(i->f) M0(i->n) M0(n->f) for n = d dbar,*)
(*    u ubar, t tbar, g g (physical polarizations), in D dims, as functions of q1.p1, q1.p2, q1.k1.  -> work/scat/A/cuts.m*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file scat_feyncalc.wl TASK [first last [k]]  with TASK = tree, A, B (diagrams first..last;*)
(*with k only the eta^k piece of diagram first, eta = 1 - xi, -> part_<i>_<k>.m), tidA, tidB [first last], cuts; run_scat_check.sh runs the*)
(*diagrams of (B) in parallel and the slowest ones piece by piece.  Interactive:  ~/hep/bin/wopen scat_feyncalc.wl, then "Run All*)
(*Code" (all tasks, but only diagrams 1 and 2 of (B): nbRangeBSC$) or Shift+Return cell by cell; the cells under "Inspect" headings run only in*)
(*the notebook (If[$Notebooks, ...]) and show the diagrams before they are evaluated.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirSC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
workDirSC$ = FileNameJoin[{srcDirSC$, "work", "scat"}];
Quiet[CreateDirectory[FileNameJoin[{workDirSC$, #}], CreateIntermediateDirectories -> True]] & /@ {"A", "B"};
modelTmpDirSC$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirSC$, "generated", "QCD_FA"}], FileNameJoin[{modelTmpDirSC$, "QCD_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirSC$, "QCD_FA"}], Quiet -> True];
modelSC$ = FileNameJoin[{modelTmpDirSC$, "QCD_FA", "QCD_FA"}];
(* tasks: from the command line, or all of them in the notebook *)
argsSC$ = If[$Notebooks || Length[$ScriptCommandLine] < 2, {}, Rest[$ScriptCommandLine]];
(* in the notebook: everything for (A), the trees and the cuts, but only diagrams 1 and 2 of (B) and no TID for (B)
   (the full (B) takes about an hour on 8 cores: run_scat_check.sh); change nbRangeBSC$ to run more *)
tasksSC$ = Which[argsSC$ =!= {}, {First[argsSC$]}, $Notebooks, {"tree", "A", "B", "tidA", "cuts"}, True, {"tree", "A", "B", "tidA", "tidB", "cuts"}];
nbRangeBSC$ = {1, 2};
rangeSC$[n_] := Which[Length[argsSC$] >= 3, Range[ToExpression[argsSC$[[2]]], ToExpression[argsSC$[[3]]]], $Notebooks && n == 46, nbRangeBSC$, True, Range[n]];


(* ::Text:: *)
(*Helpers.  gS = g (GS is FeynCalc's slash), xi = gauge parameter (GaugeXi[V[2, {colour}]] renamed), mt = 1 after the*)
(*conversion.  Kinematics: p1, p2 massless, k1, k2 of mass 1; k2 = p1 + p2 - k1 is eliminated after the traces.*)


insSC$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelSC$, GenericModel -> modelSC$,
   ExcludeParticles -> {V[1], F[1]}];
convSC$[d_, in_, out_] := FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out,
    LoopMomenta -> {l}, ChangeDimension -> D, List -> True, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] //
   ReplaceAll[#, {SMP["g_s"] -> gS, FCGV["GS"] -> gS, GaugeXi[V[2, ___]] -> xi, GaugeXi[G] -> xi, FCGV["MT"] -> mt, SMP["m_t"] -> mt}] &;
procsSC$ = <|"A" -> ({F[2], -F[2]} -> {F[7], -F[7]}), "B" -> ({V[2], V[2]} -> {F[7], -F[7]})|>;
sv = 10; tv = -3; uv = 2 - sv - tv;
setKinSC$[] := (FCClearScalarProducts[];
   SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[k1, k1] = 1; SPD[k2, k2] = 1;
   SPD[p1, p2] = sv/2; SPD[k1, k2] = (sv - 2)/2; SPD[p1, k1] = (1 - tv)/2; SPD[p2, k2] = (1 - tv)/2;
   SPD[p1, k2] = (1 - uv)/2; SPD[p2, k1] = (1 - uv)/2);
setKinSC$[];
dropSSC$[x_] := x /. FeynAmpDenominator[a___, PropagatorDenominator[q_, 0], PropagatorDenominator[q_, 0], b___] /; FreeQ[q, l] :> 0;
polSumSC$[x_] := DoPolarizationSums[DoPolarizationSums[x, p1, p2], p2, p1];
colourSC$[x_] := SUNSimplify[x, SUNNToCACF -> True, Explicit -> True];
(* the integral families: propagators (l + offset)^2 - mass^2 *)
famDefsSC$ = {
   "F1" -> {{0, 0}, {-p1, 0}, {-p1 - p2, 0}, {-p1 - p2 + k1, 1}},
   "F2" -> {{0, 0}, {-p1, 0}, {-p1 - p2, 0}, {-k1, 1}},
   "F3" -> {{0, 0}, {k1, 1}, {-p1 - p2 + k1, 1}, {-p1, 0}},
   "G1" -> {{0, 1}, {-p1, 1}, {-p1 + k1, 0}, {p2, 1}},
   "G2" -> {{0, 0}, {-p1, 0}, {-p1 + k1, 1}, {p2, 0}},
   "G3" -> {{0, 1}, {-p1, 1}, {p2, 1}, {p2 - k1, 0}},
   "G4" -> {{0, 0}, {-p1, 0}, {p2, 0}, {p2 - k1, 1}},
   "G5" -> {{0, 1}, {-k1, 0}, {-p1, 1}, {p2 - k1, 0}},
   "G6" -> {{0, 0}, {-k1, 1}, {-p1, 0}, {p2 - k1, 1}}};
famNamesSC$ = famDefsSC$[[All, 1]]; famOffSC$ = famDefsSC$[[All, 2]];
shiftsSC$ = Flatten[Table[{sg, a p1 + b p2 + c k1}, {sg, {1, -1}}, {a, -1, 1}, {b, -1, 1}, {c, -1, 1}], 3];
findShiftSC$[props_] := Module[{res = $Failed},
   Do[If[res === $Failed && AllTrue[props, MemberQ[famOffSC$[[fi]], {Expand[sh[[1]] (#[[1]] - l + sh[[2]])], #[[2]]}] &], res = {sh, fi}],
    {fi, Length[famOffSC$]}, {sh, shiftsSC$}];
   res];
(* l^2, l.p1, l.p2, l.k1 in terms of the propagators dd[1..4] of family fi *)
spSolSC$[fi_] := spSolSC$[fi] = Module[{L0, L1, L2, L3, eqs, sol},
   eqs = Table[With[{o = famOffSC$[[fi, i, 1]], mm = famOffSC$[[fi, i, 2]]},
      dd[i] == L0 + 2 (Coefficient[o, p1] L1 + Coefficient[o, p2] L2 + Coefficient[o, k1] L3) + If[o === 0, 0, FCE[ExpandScalarProduct[SPD[o, o]]]] - mm^2], {i, 4}];
   sol = First[Solve[eqs, {L0, L1, L2, L3}]];
   {SPD[l, l] -> (L0 /. sol), SPD[l, p1] -> (L1 /. sol), SPD[p1, l] -> (L1 /. sol), SPD[l, p2] -> (L2 /. sol), SPD[p2, l] -> (L2 /. sol),
    SPD[l, k1] -> (L3 /. sol), SPD[k1, l] -> (L3 /. sol)}];
nFailSC$ = 0;
propsSC$[y_] := Select[Flatten[Cases[{FCE[y]}, FAD[a__] :> (If[ListQ[#], pd @@ Take[#, 2], pd[#, 0]] & /@ {a}), Infinity]] /. pd[q_, mm_] :> {Expand[q], mm},
    !FreeQ[#[[1]], l] &] /. {q_, mm_} /; Coefficient[q, l] == -1 :> {Expand[-q], mm};
toGLItermSC$[y_] := Module[{props = Union[propsSC$[y]], sf, sh, fi, ys, props0, nu, num, cr},
   If[props === {}, Return[0]];
   sf = findShiftSC$[props];
   If[sf === $Failed, nFailSC$++; Print["   no family for ", InputForm[props]]; Return[y]];
   {sh, fi} = sf;
   ys = FCE[ExpandScalarProduct[FCI[FCE[y] /. l -> sh[[1]] l + sh[[2]]]]];
   props0 = propsSC$[ys];
   nu = Table[Count[props0, {q_, mm_} /; Expand[q - l - famOffSC$[[fi, i, 1]]] === 0 && mm == famOffSC$[[fi, i, 2]]], {i, 4}];
   If[Total[nu] =!= Length[props0], nFailSC$++; Print["   propagator matching failed: ", InputForm[props0]]; Return[y]];
   num = Expand[FCE[ExpandScalarProduct[FCI[ys /. FAD[___] -> 1]]] /. spSolSC$[fi]];
   If[!FreeQ[num, l], nFailSC$++; Print["   l left in the numerator: ", InputForm[num]]; Return[y]];
   cr = CoefficientRules[num, Array[dd, 4]];
   Total[(#[[2]] GLI[famNamesSC$[[fi]], nu - #[[1]]]) & /@ cr]];
toGLISC$[x_] := Module[{xx = FCLoopIsolate[x, {l}, Head -> lInt]}, xx /. lInt[y_] :> toGLItermSC$[y]];


(* ::Section:: *)
(*(a) diagrams*)


d0SC$ = AssociationMap[insSC$[CreateTopologies[0, 2 -> 2], procsSC$[#]] &, {"A", "B"}];
d1SC$ = AssociationMap[insSC$[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], procsSC$[#]] &, {"A", "B"}];


(* ::Subsubsection:: *)
(*Inspect: the one-loop diagrams of (A) and (B) (FeynArts numbering, used in the note)*)


If[$Notebooks,
  {Show[#, ImageSize -> 560] & /@ Render[Paint[d1SC$["A"], ColumnsXRows -> {5, 3}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 560] & /@ Render[Paint[d1SC$["B"], ColumnsXRows -> {6, 4}, Numbering -> Simple, DisplayFunction -> Identity]]}
]


a0SC$ = AssociationMap[convSC$[d0SC$[#], {p1, p2}, {k1, k2}] &, {"A", "B"}];
a1SC$ = AssociationMap[convSC$[d1SC$[#], {p1, p2}, {k1, k2}] &, {"A", "B"}];
Print["(a) tree and one-loop diagrams: (A) ", Length[a0SC$["A"]], ", ", Length[a1SC$["A"]], ";  (B) ", Length[a0SC$["B"]], ", ",
  Length[a1SC$["B"]], "  (expect 1, 15; 3, 46)"];
m0SC$ = AssociationMap[dropSSC$[Total[a0SC$[#]] /. mt -> 1] &, {"A", "B"}];


(* ::Section:: *)
(*(b) trees: Born, colour correlations, counterterm pieces*)


spinPolSC$[key_, x_] := Module[{y = FermionSpinSum[x, ExtraFactor -> 1] // DiracSimplify // Contract},
   If[key === "B", y = Contract[polSumSC$[y]]]; y];
toNumSC$[x_] := Simplify[ExpandScalarProduct[FeynAmpDenominatorExplicit[x]]];
legsSC$ = <|"A" -> {{"qbar", SUNFIndex[Col1]}, {"q", SUNFIndex[Col2]}, {"q", SUNFIndex[Col3]}, {"qbar", SUNFIndex[Col4]}},
   "B" -> {{"g", SUNIndex[Glu1]}, {"g", SUNIndex[Glu2]}, {"q", SUNFIndex[Col3]}, {"qbar", SUNFIndex[Col4]}}|>;
primeSC$[(h : SUNIndex | SUNFIndex)[x_]] := h[Symbol[SymbolName[x] <> "p"]];
(* generators, all particles outgoing: outgoing quark T^c_{i'i}, outgoing antiquark -T^c_{ii'}, gluon -i f^{c a' a};
   the incoming quark of (A) is an outgoing antiquark and the incoming antiquark an outgoing quark *)
genSC$[{"g", a_}, c_] := -I SUNF[c, primeSC$[a], a];
genSC$[{"q", i_}, c_] := SUNTF[{c}, primeSC$[i], i];
genSC$[{"qbar", i_}, c_] := -SUNTF[{c}, i, primeSC$[i]];
corrSC$[key_, i_, j_] := Module[{lg = legsSC$[key], mc},
   mc = ComplexConjugate[m0SC$[key]] /. {lg[[i, 2]] -> primeSC$[lg[[i, 2]]], lg[[j, 2]] -> primeSC$[lg[[j, 2]]]};
   toNumSC$[colourSC$[spinPolSC$[key, mc FCI[genSC$[lg[[i]], SUNIndex[cc]] genSC$[lg[[j]], SUNIndex[cc]]] m0SC$[key]]]] /. gS -> 1];
pairsSC$ = {{1, 2}, {1, 3}, {1, 4}, {2, 3}, {2, 4}, {3, 4}};
treeSC$[key_] := Module[{born, cc, kinds, w0, wm, sun = CF -> (CA^2 - 1)/(2 CA), t0 = AbsoluteTime[]},
   born = toNumSC$[colourSC$[spinPolSC$[key, ComplexConjugate[m0SC$[key]] m0SC$[key]]]] /. gS -> 1;
   cc = Association[Table[p -> corrSC$[key, Sequence @@ p], {p, pairsSC$}]];
   Print["(b) (", key, ") Born(D) = ", InputForm[Factor[born]], ";  colour conservation sum_j <T_i.T_j> + C_i Born (i = 1, 3): ",
    Simplify[{cc[{1, 2}] + cc[{1, 3}] + cc[{1, 4}] + If[key === "A", CF, CA] born, cc[{1, 3}] + cc[{2, 3}] + cc[{3, 4}] + CF born} /. sun],
    "  (expect {0, 0})"];
   If[key === "A", Print["(b) (A) <T_i.T_j>/Born - Eq. (17) for 12, 13, 14, 23, 24, 34: ",
     Simplify[(cc /@ pairsSC$)/born - {(CA - 2 CF)/2, CA/2 - 2 CF, 2 CF - CA, 2 CF - CA, CA/2 - 2 CF, (CA - 2 CF)/2} /. sun], "  (expect 0)"]];
   {w0, wm} = If[key === "A", {<||>, 0},
     kinds = Table[With[{q = Cases[{FCE[a]}, FAD[___, {q_, mt}, ___] :> q, Infinity]},
        Which[!FreeQ[a, SUNF], "s", ExpandScalarProduct[SPD[First[q] /. k2 -> p1 + p2 - k1]] == tv, "t", True, "u"]], {a, a0SC$[key]}];
     {Association[Table[kinds[[i]] -> (toNumSC$[colourSC$[spinPolSC$[key, ComplexConjugate[m0SC$[key]] dropSSC$[a0SC$[key][[i]] /. mt -> 1]]]] /. gS -> 1), {i, 3}]],
      Simplify[Total[Table[If[kinds[[i]] == "s", 0,
          Module[{x = a0SC$[key][[i]] /. Spinor[p_, mt, s___] :> Spinor[p, 1, s] /. mt -> mi},
           x = ExpandScalarProduct[FeynAmpDenominatorExplicit[colourSC$[spinPolSC$[key, ComplexConjugate[m0SC$[key]] x]]]];
           D[x, mi] /. mi -> 1]], {i, 3}]] /. gS -> 1]}];
   If[key === "B", Print["(b) (B) tree diagrams ", Keys[w0], ";  Born - sum of the three interferences = ", Simplify[born - Total[Values[w0]]], "  (expect 0)"]];
   Put[{born, cc, w0, wm}, FileNameJoin[{workDirSC$, key, "tree.m"}]];
   Print["(b) (", key, ") trees done in ", Round[AbsoluteTime[] - t0], " s"]];
If[MemberQ[tasksSC$, "tree"], treeSC$["A"]; treeSC$["B"]];


(* ::Section:: *)
(*(c) one-loop interference, diagram by diagram, as family integrals*)


(* one piece: the coefficient of eta^k (eta = 1 - xi) of diagram i, interfered with each tree diagram in turn (smaller
   expressions; the slowest diagrams of (B) are run piece by piece in parallel).  No FDS: on the gluon triangle of (B) it ran
   for more than 12 minutes, and the shifts are found by toGLISC$ anyway. *)
pieceSC$[key_, i_, k_] := Module[{amp, r},
   amp = Coefficient[Expand[dropSSC$[a1SC$[key][[i]] /. mt -> 1] /. xi -> 1 - eta, eta], eta, k];
   If[amp === 0, Return[0]];
   amp = SUNSimplify[Contract[DiracSimplify[amp]], SUNNToCACF -> True];
   r = Sum[Module[{x},
      x = spinPolSC$[key, FermionSpinSum[ComplexConjugate[dropSSC$[t /. mt -> 1]] amp, ExtraFactor -> 1] // DiracSimplify];
      x = colourSC$[x];
      If[!FreeQ[x, SUNF | SUNT | SUNTF | SUNIndex | SUNFIndex], Print["   WARNING: colour objects left"]];
      x = ExpandScalarProduct[FCI[FCE[x] /. k2 -> p1 + p2 - k1]] // FCE;
      toGLISC$[x]], {t, a0SC$[key]}];
   r (1 - xi)^k];
etaMaxSC$[key_, i_] := Exponent[Expand[dropSSC$[a1SC$[key][[i]]] /. xi -> 1 - eta, eta], eta];
loopSC$[key_] := Do[Module[{t0 = AbsoluteTime[], r},
     If[Length[argsSC$] >= 4,
      (* a single piece: scat_feyncalc.wl B i i k *)
      r = pieceSC$[key, i, ToExpression[argsSC$[[4]]]];
      Put[r, FileNameJoin[{workDirSC$, key, "part_" <> ToString[i] <> "_" <> argsSC$[[4]] <> ".m"}]],
      r = Sum[pieceSC$[key, i, k], {k, 0, etaMaxSC$[key, i]}];
      Put[r, FileNameJoin[{workDirSC$, key, "d" <> ToString[i] <> ".m"}]]];
     Print["(c) (", key, ") diagram ", i, If[Length[argsSC$] >= 4, " eta^" <> argsSC$[[4]], ""], ": ", Round[AbsoluteTime[] - t0], " s, ",
      Length[Union[Cases[r, _GLI, Infinity]]], " integrals, families ", Union[Cases[r, GLI[f_, _] :> f, Infinity]], ", failures so far ", nFailSC$]],
    {i, rangeSC$[Length[a1SC$[key]]]}];
If[MemberQ[tasksSC$, "A"], loopSC$["A"]];
If[MemberQ[tasksSC$, "B"], loopSC$["B"]];


(* ::Subsubsection:: *)
(*Inspect: the family integrals of the soft heavy-quark vertex diagram of (A)*)


If[$Notebooks,
  Union[Cases[Get[FileNameJoin[{workDirSC$, "A", "d1.m"}]], _GLI, Infinity]]
]


(* ::Section:: *)
(*(d) Feynman gauge by tensor reduction (TID)*)


tidSC$[key_] := Do[Module[{t0 = AbsoluteTime[], amp, w},
     amp = SUNSimplify[Contract[DiracSimplify[dropSSC$[a1SC$[key][[i]] /. mt -> 1 /. xi -> 1]]], SUNNToCACF -> True];
     w = Sum[Module[{x},
        x = spinPolSC$[key, FermionSpinSum[ComplexConjugate[dropSSC$[t /. mt -> 1]] amp, ExtraFactor -> 1] // DiracSimplify];
        x = colourSC$[x];
        x = TID[x, l, ToPaVe -> True, UsePaVeBasis -> True] // FCE;
        FeynAmpDenominatorExplicit[PaVeReduce[x]] // FCI // ExpandScalarProduct // FCE], {t, a0SC$[key]}];
     Put[w, FileNameJoin[{workDirSC$, key, "tid_" <> ToString[i] <> ".m"}]];
     Print["(d) (", key, ") TID at xi = 1, diagram ", i, ": ", Round[AbsoluteTime[] - t0], " s"]], {i, rangeSC$[Length[a1SC$[key]]]}];
If[MemberQ[tasksSC$, "tidA"], tidSC$["A"]];
If[MemberQ[tasksSC$, "tidB"], tidSC$["B"]];


(* ::Section:: *)
(*(e) unitarity of (A): cut integrands*)


(* ::Text:: *)
(*n = (q1, q2), q2 = p1 + p2 - q1; tree amplitudes i -> n and n -> f from FeynArts; index symbols renamed apart (suffixes c, i, f)*)
(*and the colour indices of n identified.  The result depends on q1 through qp1 = q1.p1, qp2 = q1.p2, qk1 = q1.k1.*)


treeAmpSC$[proc_, in_, out_] := Total[convSC$[insSC$[CreateTopologies[0, 2 -> 2], proc], in, out]] /. {gS -> 1, xi -> 1, mt -> 1} // FCI;
renSC$[x_, ext_List, suf_] := x /. ext /. (h : SUNIndex | SUNFIndex | LorentzIndex)[s_Symbol, r___] /;
     !MemberQ[{Col1, Col2, Col3, Col4, cq1, cq2, gq1, gq2}, s] :> h[Symbol[SymbolName[s] <> suf], r];
cutSC$[nproc_, mn_, gluons_, m0c_] := Module[{ain, anf, x},
   SPD[q1, q1] = mn^2; SPD[q2, q2] = mn^2;
   ain = renSC$[treeAmpSC$[{F[2], -F[2]} -> nproc, {p1, p2}, {q1, q2}],
     If[gluons, {SUNIndex[Glu3] -> SUNIndex[gq1], SUNIndex[Glu4] -> SUNIndex[gq2]}, {SUNFIndex[Col3] -> SUNFIndex[cq1], SUNFIndex[Col4] -> SUNFIndex[cq2]}], "i"];
   anf = renSC$[treeAmpSC$[nproc -> {F[7], -F[7]}, {q1, q2}, {k1, k2}],
     If[gluons, {SUNIndex[Glu1] -> SUNIndex[gq1], SUNIndex[Glu2] -> SUNIndex[gq2]}, {SUNFIndex[Col1] -> SUNFIndex[cq1], SUNFIndex[Col2] -> SUNFIndex[cq2]}], "f"];
   x = FermionSpinSum[m0c dropSSC$[ain] dropSSC$[anf], ExtraFactor -> 1] // DiracSimplify // Contract;
   If[gluons, x = Contract[DoPolarizationSums[DoPolarizationSums[x, q1, q2], q2, q1]]];
   x = FeynAmpDenominatorExplicit[colourSC$[x]] // FCI;
   x = ExpandScalarProduct[x /. Momentum[q2, dd___] :> Momentum[p1 + p2 - q1, dd] /. Momentum[k2, dd___] :> Momentum[p1 + p2 - k1, dd]] // FCE;
   Together[x /. {SPD[p1, q1] -> qp1, SPD[p2, q1] -> qp2, SPD[k1, q1] -> qk1}]];
If[MemberQ[tasksSC$, "cuts"],
  Module[{m0c = renSC$[ComplexConjugate[m0SC$["A"] /. {gS -> 1, xi -> 1}], {}, "c"], cuts},
   cuts = <|"dd" -> cutSC$[{F[4], -F[4]}, 0, False, m0c], "uu" -> cutSC$[{F[2], -F[2]}, 0, False, m0c],
     "tt" -> cutSC$[{F[7], -F[7]}, 1, False, m0c], "gg" -> cutSC$[{V[2], V[2]}, 0, True, m0c]|>;
   setKinSC$[];
   Put[cuts, FileNameJoin[{workDirSC$, "A", "cuts.m"}]];
   Print["(e) cut integrands for n = ", Keys[cuts], "; symbols ", Union[Cases[Values[cuts], _Symbol, Infinity]]]]];
