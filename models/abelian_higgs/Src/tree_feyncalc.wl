(* ::Package:: *)

(* ::Title:: *)
(*Step (2): tree amplitudes with FeynArts + FeynCalc in a general R_xi gauge (abelian Higgs model)*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (2).  Uses the FeynArts model of this note (Src/generated/AbelianHiggs_FA,*)
(*propagators with GaugeXi[A], ghost coupling with the same symbol; run generate_AbelianHiggs.wl first).*)
(*  (a) h -> A A:  sum|M|^2 against Eq. (width) of the note;*)
(*  (b) A A -> A A:  amplitude against Eq. (Maa) (polarization vectors kept as symbols), xi independence;*)
(*  (c) A A -> h h:  amplitude against Eq. (Mahh) (unitary-gauge form), d/dxi = 0 with transversality;*)
(*  (d) h h -> h h,  G G -> G G  and  G G -> h h  (Landau gauge, massless G) against Eqs. (Mhh), (et), (Mgghh);*)
(*  (e) sum|M|^2 of A A -> A A and A A -> h h over all polarizations (massive sums -g + k k/M^2), exactly at the*)
(*      kinematic points of tree_numeric.py -> results/tree_feyncalc_points.csv (20 digits).*)
(*FeynArts' CreateFeynAmp gives M (the product of Feynman rules divided by i), the same normalization as the note.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file tree_feyncalc.wl  (about 1 minute).  Interactive:  ~/hep/bin/wopen tree_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;


srcDirTr$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirTr$ = FileNameJoin[{srcDirTr$, "results"}];
Quiet[CreateDirectory[resDirTr$]];
modelTmpDirTr$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTr$, "generated", "AbelianHiggs_FA"}], FileNameJoin[{modelTmpDirTr$, "AbelianHiggs_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirTr$, "AbelianHiggs_FA"}], Quiet -> True];
modelFileTr$ = FileNameJoin[{modelTmpDirTr$, "AbelianHiggs_FA", "AbelianHiggs_FA"}];


(* ::Text:: *)
(*Field codes: V[1] = A, S[1] = h, S[2] = G, U[1] = ghost.  Conversion: FCGV["EL"] -> ee, FCGV masses -> MA, MH,*)
(*GaugeXi[A] -> xi, vev -> MA/ee, lam -> ee^2 MH^2/(2 MA^2).*)


convTr$ = {FCGV["EL"] -> ee, FCGV["MA"] -> MA, FCGV["MH"] -> MH, GaugeXi[A] -> xi, GaugeXi[V[1, ___]] -> xi,
   GaugeXi[S[2, ___]] -> xi, GaugeXi[U[1, ___]] -> xi};
parTr$ = {vev -> MA/ee, lam -> ee^2 MH^2/(2 MA^2)};

treeDiagrams$[in_, out_] := Quiet[InsertFields[CreateTopologies[0, Length[in] -> Length[out]], in -> out,
    InsertionLevel -> {Particles}, Model -> modelFileTr$, GenericModel -> modelFileTr$], RuleDelayed::rhs];
treeAmps$[diags_, in_, out_] := Module[{a},
   (* GaugeRules -> {} keeps GaugeXi (the FeynArts default {_GaugeXi -> 1} is Feynman gauge) *)
   a = Quiet[FCFAConvert[CreateFeynAmp[diags, GaugeRules -> {}] /. M$FACouplings,
       IncomingMomenta -> in, OutgoingMomenta -> out, ChangeDimension -> 4, List -> True, SMP -> False,
       DropSumOver -> True, TransversePolarizationVectors -> {}], RuleDelayed::rhs];
   Print["   ", in, " -> ", out, ": ", Length[a], " amplitudes"];
   a /. convTr$ /. parTr$];

(* momentum conservation in the momenta (not in the polarization vectors), then FAD -> 1/(q^2 - m^2) *)
consTr$[x_, rule_] := x /. Momentum[q_, dim___] :> Momentum[q /. rule, dim] /; FreeQ[q, Polarization];
normTr$[x_, rule_] := Simplify[ExpandScalarProduct[FeynAmpDenominatorExplicit[Contract[consTr$[x, rule]]]] /.
    Pair[Momentum[k_], Momentum[Polarization[k_, __]]] -> 0];
checkTr$[label_, d_] := (Print[label, ": FeynCalc - note = ", InputForm[d], "   (expect 0)"]; d);


(* ::Section:: *)
(*(a) h -> A A*)


ampHAA$ = treeAmps$[treeDiagrams$[{S[1]}, {V[1], V[1]}], {k}, {p1, p2}];
FCClearScalarProducts[];
SP[k, k] = MH^2; SP[p1, p1] = MA^2; SP[p2, p2] = MA^2; SP[p1, p2] = (MH^2 - 2 MA^2)/2;
SP[k, p1] = MH^2/2; SP[k, p2] = MH^2/2;
sqHAA$ = Simplify[Contract[DoPolarizationSums[DoPolarizationSums[
       Contract[ComplexConjugate[Total[ampHAA$]] Total[ampHAA$]], p1], p2]]];
(* note Eq. (width): sum|M|^2 = 4 e^2 MA^2 [2 + (p1.p2)^2/MA^4] = (e^2 MH^4/MA^2)(1 - 4x + 12x^2) *)
resA$ = checkTr$["(a) h -> A A, sum|M|^2", Simplify[sqHAA$ - ee^2 MH^4/MA^2 (1 - 4 x + 12 x^2) /. x -> MA^2/MH^2]];


(* ::Section:: *)
(*(b) A A -> A A*)


(* polarization vectors as inert symbols for the comparison: eps[i] incoming (i = 1, 2), conjugated outgoing (3, 4) *)
polSym$ = {Momentum[Polarization[k1, I, ___]] -> Momentum[eps1], Momentum[Polarization[k2, I, ___]] -> Momentum[eps2],
   Momentum[Polarization[k3, -I, ___]] -> Momentum[eps3], Momentum[Polarization[k4, -I, ___]] -> Momentum[eps4]};

ampAAAA$ = treeAmps$[treeDiagrams$[{V[1], V[1]}, {V[1], V[1]}], {k1, k2}, {k3, k4}];
FCClearScalarProducts[];
SP[k1, k1] = MA^2; SP[k2, k2] = MA^2; SP[k3, k3] = MA^2;
SP[k1, k2] = (s - 2 MA^2)/2; SP[k1, k3] = (2 MA^2 - t)/2; SP[k2, k3] = (2 MA^2 - (4 MA^2 - s - t))/2;
mAAAA$ = normTr$[Total[ampAAAA$] /. polSym$, k4 -> k1 + k2 - k3];
uMan$ = 4 MA^2 - s - t;
handAAAA$ = -4 ee^2 MA^2 (SP[eps1, eps2] SP[eps3, eps4]/(s - MH^2) + SP[eps1, eps3] SP[eps2, eps4]/(t - MH^2) +
     SP[eps1, eps4] SP[eps2, eps3]/(uMan$ - MH^2));
resB$ = checkTr$["(b) A A -> A A, amplitude", Simplify[ExpandScalarProduct[mAAAA$ - handAAAA$]]];
Print["(b) A A -> A A, d/dxi (expect 0): ", Simplify[D[mAAAA$, xi]]];


(* ::Section:: *)
(*(c) A A -> h h*)


(* invariants: eps1.eps2, eps1.k2, eps1.p1, eps2.k1, eps2.p1 (p2 = k1 + k2 - p1, eps_i.k_i = 0) *)
polSym2$ = {Momentum[Polarization[k1, I, ___]] -> Momentum[eps1], Momentum[Polarization[k2, I, ___]] -> Momentum[eps2]};
transv2$ = {Pair[Momentum[eps1], Momentum[k1]] -> 0, Pair[Momentum[eps2], Momentum[k2]] -> 0};

ampAAhh$ = treeAmps$[treeDiagrams$[{V[1], V[1]}, {S[1], S[1]}], {k1, k2}, {p1, p2}];
FCClearScalarProducts[];
SP[k1, k1] = MA^2; SP[k2, k2] = MA^2; SP[p1, p1] = MH^2;
SP[k1, k2] = (s - 2 MA^2)/2; SP[k1, p1] = (MA^2 + MH^2 - t)/2; SP[k2, p1] = (MA^2 + MH^2 - (2 MA^2 + 2 MH^2 - s - t))/2;
normAAhh$[x_] := Simplify[ExpandScalarProduct[FeynAmpDenominatorExplicit[Contract[consTr$[x /. polSym2$, p2 -> k1 + k2 - p1]]]] /. transv2$];
mAAhh$ = normAAhh$[Total[ampAAhh$]];
Print["(c) A A -> h h, d/dxi of the sum of the 6 diagrams (expect 0): ", Simplify[D[mAAhh$, xi]]];
uMan2$ = 2 MA^2 + 2 MH^2 - s - t;
(* note Eq. (Mahh): eps1.p2 = eps1.k2 - eps1.p1, eps2.p2 = eps2.k1 - eps2.p1 *)
e1e2$ = SP[eps1, eps2]; e1p1$ = SP[eps1, p1]; e2p1$ = SP[eps2, p1];
e1p2$ = SP[eps1, k2] - SP[eps1, p1]; e2p2$ = SP[eps2, k1] - SP[eps2, p1];
handAAhh$ = 2 ee^2 e1e2$ (1 + 3 MH^2/(s - MH^2)) + 4 ee^2 (MA^2 e1e2$ + e1p1$ e2p2$)/(t - MA^2) +
   4 ee^2 (MA^2 e1e2$ + e1p2$ e2p1$)/(uMan2$ - MA^2);
resC$ = checkTr$["(c) A A -> h h, amplitude", Simplify[ExpandScalarProduct[mAAhh$ - handAAhh$]]];


(* ::Section:: *)
(*(d) h h -> h h, G G -> G G, G G -> h h*)


FCClearScalarProducts[];
SP[k1, k1] = MH^2; SP[k2, k2] = MH^2; SP[p1, p1] = MH^2;
SP[k1, k2] = (s - 2 MH^2)/2; SP[k1, p1] = (2 MH^2 - t)/2; SP[k2, p1] = (2 MH^2 - (4 MH^2 - s - t))/2;
mhhhh$ = normTr$[Total[treeAmps$[treeDiagrams$[{S[1], S[1]}, {S[1], S[1]}], {k1, k2}, {p1, p2}]], p2 -> k1 + k2 - p1];
vT$ = MA/ee; lamT$ = ee^2 MH^2/(2 MA^2);
resD1$ = checkTr$["(d) h h -> h h", Simplify[mhhhh$ - (-6 lamT$ - 9 MH^4/vT$^2 (1/(s - MH^2) + 1/(t - MH^2) +
        1/(4 MH^2 - s - t - MH^2)))]];

(* G G -> G G and G G -> h h in Landau gauge: xi -> 0, massless external Goldstone bosons *)
FCClearScalarProducts[];
SP[k1, k1] = 0; SP[k2, k2] = 0; SP[p1, p1] = 0;
SP[k1, k2] = s/2; SP[k1, p1] = -t/2; SP[k2, p1] = -(-s - t)/2;
mGGGG$ = normTr$[Total[treeAmps$[treeDiagrams$[{S[2], S[2]}, {S[2], S[2]}], {k1, k2}, {p1, p2}]] /. xi -> 0, p2 -> k1 + k2 - p1];
resD2$ = checkTr$["(d) G G -> G G (Landau)", Simplify[mGGGG$ - (-6 lamT$ - MH^4/vT$^2 (1/(s - MH^2) + 1/(t - MH^2) +
        1/(-s - t - MH^2)))]];
FCClearScalarProducts[];
SP[k1, k1] = 0; SP[k2, k2] = 0; SP[p1, p1] = MH^2;
SP[k1, k2] = s/2; SP[k1, p1] = (MH^2 - t)/2; SP[k2, p1] = (MH^2 - (2 MH^2 - s - t))/2;
mGGhh$ = normTr$[Total[treeAmps$[treeDiagrams$[{S[2], S[2]}, {S[1], S[1]}], {k1, k2}, {p1, p2}]] /. xi -> 0, p2 -> k1 + k2 - p1];
uMan3$ = 2 MH^2 - s - t;
(* note Eq. (Mgghh): contact, s-channel h, t/u-channel G (massless) and A (Landau propagator) *)
(* (p1 + k1).(p2 + k2) = s - u in the t channel, s - t in the u channel (massless G) *)
handGGhh$ = -2 lamT$ - 3 MH^4/(vT$^2 (s - MH^2)) - MH^4/vT$^2 (1/t + 1/uMan3$) -
   ee^2 (s - uMan3$ + MH^4/t)/(t - MA^2) - ee^2 (s - t + MH^4/uMan3$)/(uMan3$ - MA^2);
resD3$ = checkTr$["(d) G G -> h h (Landau)", Simplify[mGGhh$ - handGGhh$]];


(* ::Section:: *)
(*(e) polarization sums at the kinematic points of tree_numeric.py*)


(* sum over all polarizations of |M|^2 (no averaging, no identical-particle factor) as a function of s and t,
   with the polarization vectors restored *)
unSym$ = {Momentum[eps1] -> Momentum[Polarization[k1, I]], Momentum[eps2] -> Momentum[Polarization[k2, I]],
   Momentum[eps3] -> Momentum[Polarization[k3, -I]], Momentum[eps4] -> Momentum[Polarization[k4, -I]]};

FCClearScalarProducts[];
SP[k1, k1] = MA^2; SP[k2, k2] = MA^2; SP[k3, k3] = MA^2; SP[k4, k4] = MA^2;
SP[k1, k2] = (s - 2 MA^2)/2; SP[k3, k4] = (s - 2 MA^2)/2; SP[k1, k3] = (2 MA^2 - t)/2; SP[k2, k4] = (2 MA^2 - t)/2;
SP[k1, k4] = (2 MA^2 - (4 MA^2 - s - t))/2; SP[k2, k3] = (2 MA^2 - (4 MA^2 - s - t))/2;
mFull$ = handAAAA$ /. {SP[a_, b_] :> Pair[Momentum[a], Momentum[b]]} /. unSym$;
sqAAAA$ = Contract[ComplexConjugate[mFull$] mFull$];
Do[sqAAAA$ = Contract[DoPolarizationSums[sqAAAA$, kk]], {kk, {k1, k2, k3, k4}}];
sqAAAA$ = Simplify[sqAAAA$];

(* A A -> h h: the FeynCalc amplitude itself (all 6 diagrams, general xi), squared and summed *)
FCClearScalarProducts[];
SP[k1, k1] = MA^2; SP[k2, k2] = MA^2; SP[p1, p1] = MH^2; SP[p2, p2] = MH^2;
SP[k1, k2] = (s - 2 MA^2)/2; SP[p1, p2] = (s - 2 MH^2)/2;
SP[k1, p1] = (MA^2 + MH^2 - t)/2; SP[k2, p2] = (MA^2 + MH^2 - t)/2;
SP[k1, p2] = (MA^2 + MH^2 - uMan2$)/2; SP[k2, p1] = (MA^2 + MH^2 - uMan2$)/2;
mAAhhFull$ = FeynAmpDenominatorExplicit[Contract[Total[ampAAhh$]]];
sqAAhh$ = Contract[ComplexConjugate[mAAhhFull$] mAAhhFull$];
Do[sqAAhh$ = Contract[DoPolarizationSums[sqAAhh$, kk]], {kk, {k1, k2}}];
sqAAhh$ = Simplify[sqAAhh$];
Print["(e) A A -> h h, d/dxi of sum|M|^2 (expect 0): ", Simplify[D[sqAAhh$, xi]]];

(* points: (process, sqrt s, cos theta); benchmark ee = 1/2, MA = 1, MH = 5/2 *)
benchTr$ = {ee -> 1/2, MA -> 1, MH -> 5/2, xi -> 1};
tOf$[rs_, c_, m1_, m2_, m3_, m4_] := Module[{s0 = rs^2, p, q, e1, e3},
   p = Sqrt[(s0 - (m1 + m2)^2) (s0 - (m1 - m2)^2)]/(2 rs); q = Sqrt[(s0 - (m3 + m4)^2) (s0 - (m3 - m4)^2)]/(2 rs);
   e1 = (s0 + m1^2 - m2^2)/(2 rs); e3 = (s0 + m3^2 - m4^2)/(2 rs);
   m1^2 + m3^2 - 2 (e1 e3 - p q c)];
pointsTr$ = {{"AAAA", 6, 7/10}, {"AAAA", 6, -3/10}, {"AAAA", 20, 1/2}, {"AAAA", 200, 1/5}, {"AAAA", 2000, 1/5},
   {"AAhh", 6, 7/10}, {"AAhh", 6, -1/2}, {"AAhh", 20, 1/5}, {"AAhh", 200, 1/5}, {"AAhh", 2000, 1/5}};
rowsTr$ = Table[Module[{proc = pt[[1]], rs = pt[[2]], c = pt[[3]], val},
    val = If[proc === "AAAA",
      sqAAAA$ /. {s -> rs^2, t -> tOf$[rs, c, 1, 1, 1, 1]} /. benchTr$,
      sqAAhh$ /. {s -> rs^2, t -> tOf$[rs, c, 1, 1, 5/2, 5/2]} /. benchTr$];
    {proc, rs, c, N[val, 20]}], {pt, pointsTr$}];
Export[FileNameJoin[{resDirTr$, "tree_feyncalc_points.csv"}],
  Prepend[{#[[1]], #[[2]], ToString[#[[3]], InputForm], ToString[NumberForm[#[[4]], 20, ExponentFunction -> (Null &)]]} & /@ rowsTr$,
   {"process", "sqrt_s", "cos_theta", "sum_M2"}], "CSV"];
Scan[Print["(e) ", #[[1]], " sqrt(s) = ", #[[2]], " cos = ", #[[3]], ": sum|M|^2 = ", #[[4]]] &, rowsTr$];
Print["(e) written ", FileNameJoin[{resDirTr$, "tree_feyncalc_points.csv"}]];


(* ::Subsubsection:: *)
(*Inspect: the A A -> h h amplitude in the invariants*)


If[$Notebooks, Collect[mAAhh$, {Pair[__]}, Simplify]]
