(* ::Package:: *)

(* ::Title:: *)
(*Step (10): photon-photon scattering at one loop (FeynArts + FeynCalc, Package-X, LoopTools)*)


(* ::Text:: *)
(*Research note models/spinor_qed, step (10), Eqs. (eq:lblamp)-(eq:lblopt), App. lbl.  The six boxes of one flavour from*)
(*FeynArts (12 diagrams = 3 cyclic orders x 2 orientations x 2 flavours), contracted with polarization vectors e1, e2, e3, e4*)
(*(e3, e4 stand for the conjugated vectors of the outgoing photons).  X = M/alpha^2 is the amplitude A/(I Pi^2) of FCFAConvert*)
(*with PreFactor -> 1 and e = 1 (A = (2 Pi)^D i M).*)
(*(a) the diagrams; the two orientations of each cyclic order give the same expression.*)
(*(b) zero external momenta: the sum of the six boxes vanishes in D dimensions (gauge invariance), while the same sum with a*)
(*    four-dimensional numerator (trace and loop momentum in four dimensions, integrals in D) leaves -X_R2, the R2 vertex of*)
(*    App. ren, X_R2 = (4/3)(e1.e2 e3.e4 + e1.e3 e2.e4 + e1.e4 e2.e3).*)
(*(c) the low-energy expansion: every propagator expanded in the external momenta (tadpoles, D = 4 for the UV-finite orders,*)
(*    loop momentum by components), the kinematics of the note (centre-of-mass frame, helicity vectors with symbolic*)
(*    w = sqrt(s)/2, cos theta = c and helicities l1..l4).  O(k^2) = 0, O(k^4) = Euler-Heisenberg (Eq. (eq:lbllow)) for all*)
(*    helicities at once, O(k^6) printed per helicity (the slope that lbl_numeric.py checks).*)
(*(d) TID in the PaVe basis (the mass M symbolic): the UV pole of the sum vanishes at general momenta; X at the points of*)
(*    work/lbl_points_exact.txt from Package-X (exact kinematics, N[., prec]) and LoopTools (rational input)*)
(*    -> results/lbl_feyncalc.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file lbl_feyncalc.wl  (after lbl_numeric.py --points; run_lbl_check.sh does both, about 15 min).  Interactive:  ~/hep/bin/wopen lbl_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirLB$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirLB$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirLB$, "generated", "SpinorQED_FA"}], FileNameJoin[{modelTmpDirLB$, "SpinorQED_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirLB$, "SpinorQED_FA"}], Quiet -> True];
modelLB$ = FileNameJoin[{modelTmpDirLB$, "SpinorQED_FA", "SpinorQED_FA"}];


(* ::Section:: *)
(*(a) The six boxes*)


diagLB$ = InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections, Reducible}],
   {V[1], V[1]} -> {V[1], V[1]}, InsertionLevel -> {Particles}, Model -> modelLB$, GenericModel -> modelLB$];


(* ::Subsubsection:: *)
(*Inspect: the 12 boxes (3 cyclic orders x 2 orientations x 2 flavours)*)


If[$Notebooks, Show[#, ImageSize -> 560] & /@ Render[Paint[diagLB$, ColumnsXRows -> {4, 3}, Numbering -> Simple, DisplayFunction -> Identity]]]


rawLB$ = FCFAConvert[CreateFeynAmp[diagLB$, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
    IncomingMomenta -> {k1, k2}, OutgoingMomenta -> {k3, k4}, LoopMomenta -> {l}, LorentzIndexNames -> {mu, nu, rho, si},
    ChangeDimension -> D, List -> True, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI //
   ReplaceAll[#, FCGV["EL"] -> 1] &;
(* the electron boxes with the mass symbolic (M); the muon boxes are the same with M -> m_mu *)
boxLB$ = Select[rawLB$, FreeQ[#, MMU] &] /. Me -> M;
polLB$ = Pair[LorentzIndex[mu, D], Momentum[e1, D]] Pair[LorentzIndex[nu, D], Momentum[e2, D]] *
   Pair[LorentzIndex[rho, D], Momentum[e3, D]] Pair[LorentzIndex[si, D], Momentum[e4, D]];
Print["(a) diagrams: ", Length[rawLB$], ";  electron boxes: ", Length[boxLB$],
  ";  orientations of each cyclic order identical after the trace (expect True): ",
  And @@ Table[Expand[DiracSimplify[Contract[(boxLB$[[i]] - boxLB$[[i + 1]]) polLB$], DiracTraceEvaluate -> True]] === 0, {i, 1, 5, 2}]];


(* ::Subsubsection:: *)
(*Inspect: one box before the trace*)


If[$Notebooks, boxLB$[[1]]]


(* ::Section:: *)
(*(b) Zero external momenta: D dimensions and the four-dimensional numerator*)


(* ::Text:: *)
(*Average over the directions of l in D dimensions.  A monomial prod_j (l.a_j) (l4^2)^p becomes L2^k/(D(D+2)...(D+2k-2))*)
(*times the sum over perfect matchings of the 2k slots; each l4^2 ties its two slots, closed chains give the trace of the*)
(*metric (4 for the four-dimensional l4, D for the D-dimensional l) and open chains the product a.b of their end vectors.*)


matchingsLB$[{}] = {{}};
matchingsLB$[{a_, rest___}] := Flatten[Table[Prepend[#, {a, {rest}[[j]]}] & /@ matchingsLB$[Delete[{rest}, j]], {j, Length[{rest}]}], 1];
chainValueLB$[match_, nvec_, vecs_, dimc_] := Module[{adj = <||>, seen = <||>, val = 1, tie, walk},
   (* slots 1..nvec are vectors, slots nvec+2i-1, nvec+2i are the two ends of the i-th l^2 *)
   Do[adj[m[[1]]] = m[[2]]; adj[m[[2]]] = m[[1]], {m, match}];
   tie[x_] := If[OddQ[x - nvec], x + 1, x - 1];
   walk[s0_] := Catch[Module[{s = s0, t},
      While[True, seen[s] = True; t = adj[s]; seen[t] = True; If[t <= nvec, Throw[t]]; s = tie[t]]]];
   Do[If[! KeyExistsQ[seen, v], val *= Pair[vecs[[v]], vecs[[walk[v]]]]], {v, nvec}];
   Do[If[! KeyExistsQ[seen, s0], Module[{s = s0, t},
       While[! KeyExistsQ[seen, s], seen[s] = True; t = adj[s]; seen[t] = True; s = tie[t]]]; val *= dimc],
     {s0, nvec + 1, Length[Flatten[match]]}];
   val];
(* returns {k, value}: the average is value (l^2)^k *)
avgLB$[vecs_List, p_, dimc_] := With[{n = Length[vecs] + 2 p},
   If[OddQ[n], {0, 0}, With[{k = n/2},
     {k, 1/Product[D + 2 j, {j, 0, k - 1}] Total[chainValueLB$[#, Length[vecs], vecs, dimc] & /@ matchingsLB$[Range[n]]]}]]];
(* d^Dl/(I Pi^(D/2)) of (l^2)^a/(l^2 - M^2)^b *)
tadLB$[a_, b_] := (-1)^(a + b) Pochhammer[D/2, a] Gamma[b - a - D/2]/Gamma[b] M^(2 (a + D/2 - b));
zeroMomLB$ = {Momentum[k1, D] -> 0, Momentum[k2, D] -> 0, Momentum[k3, D] -> 0, Momentum[k4, D] -> 0};
(* one box at zero momenta, trace in dim, averaged and integrated *)
zeroBoxLB$[box_, dim_] := Module[{x, terms},
   x = MomentumExpand[box] /. zeroMomLB$ /. FeynAmpDenominator[__] -> DEN^4;
   x = Expand[Contract[DiracSimplify[If[dim === 4, ChangeDimension[x polLB$, 4], x polLB$], DiracTraceEvaluate -> True]]];
   x = x /. {Pair[Momentum[l, d___], Momentum[l, d___]] -> LSQ} /. Momentum[a_, ___] :> a;
   terms = If[Head[x] === Plus, List @@ x, {x}];
   Total[Function[t, Module[{vs = Flatten[Cases[If[Head[t] === Times, List @@ t, {t}], Pair[l, v_]^n_. :> Table[v, {n}]]],
         p = Exponent[t, LSQ], c, av},
        c = t /. {Pair[l, _] -> 1, LSQ -> 1, DEN -> 1};
        av = avgLB$[vs, p, If[dim === 4, 4, D]];
        c av[[2]] tadLB$[av[[1]], 4]]] /@ terms]];
zeroD$ = Total[zeroBoxLB$[#, D] & /@ boxLB$];
Print["(b) zero momenta, D dimensions: sum of the six boxes / Gamma(2 - D/2) = ",
  Simplify[FunctionExpand[zeroD$/(Gamma[2 - D/2] M^(D - 4))]], "  (expect 0)"];
zero4$ = Total[zeroBoxLB$[#, 4] & /@ boxLB$];
zero4fin$ = Normal[Series[zero4$ /. D -> 4 - 2 eps, {eps, 0, 0}]];
r2LB$ = 4/3 (Pair[e1, e2] Pair[e3, e4] + Pair[e1, e3] Pair[e2, e4] + Pair[e1, e4] Pair[e2, e3]);
Print["(b) zero momenta, four-dimensional numerator: pole = ", Simplify[Coefficient[zero4fin$, eps, -1]],
  ";  finite part + X_R2 = ", Simplify[(zero4fin$ /. eps -> 0) + r2LB$ /. Log[_] -> 0], "  (expect 0, 0)"];


(* ::Section:: *)
(*(c) The low-energy expansion*)


(* ::Text:: *)
(*Centre-of-mass kinematics of the note: k1 = w(1,0,0,1), k2 = w(1,0,0,-1), k3 = w(1,sn,0,c), k4 = w(1,-sn,0,-c), the photon of*)
(*direction (theta, phi) and helicity l has e = (-l e_theta - i e_phi)/sqrt2, outgoing photons e^*.  The external momenta*)
(*carry the counting parameter kap; the loop momentum is (q0, q1, q2, q3).*)


gmLB$ = DiagonalMatrix[{1, -1, -1, -1}];
polvLB$[ct_, st_, cph_, lm_] := Join[{0}, (-lm {ct cph, 0, -st} - I {0, cph, 0})/Sqrt[2]];
polcLB$[ct_, st_, cph_, lm_] := Join[{0}, (-lm {ct cph, 0, -st} + I {0, cph, 0})/Sqrt[2]];   (* conjugate for real arguments *)
vecLB$ = <|k1 -> kap w {1, 0, 0, 1}, k2 -> kap w {1, 0, 0, -1}, k3 -> kap w {1, sn, 0, c}, k4 -> kap w {1, -sn, 0, -c},
   e1 -> polvLB$[1, 0, 1, l1], e2 -> polvLB$[-1, 0, 1, l2], e3 -> polcLB$[c, sn, 1, l3], e4 -> polcLB$[-c, sn, -1, l4],
   l -> {q0, q1, q2, q3}|>;
dotLB$[a_, b_] := a . gmLB$ . b;
toCompLB$[x_] := x /. Pair[Momentum[a_, D], Momentum[b_, D]] :> If[a === l && b === l, LSQ, dotLB$[vecLB$[a], vecLB$[b]]];
nmaxLB$ = 6;
expandBoxLB$[box_] := Module[{num, dens, lists},
   num = box /. FeynAmpDenominator[__] -> 1;
   dens = Cases[box, FeynAmpDenominator[x__] :> {x}, Infinity][[1]];
   num = Expand[toCompLB$[ExpandScalarProduct[MomentumExpand[DiracSimplify[Contract[num polLB$], DiracTraceEvaluate -> True]]]]];
   num = Table[Coefficient[num, kap, n], {n, 0, nmaxLB$}];
   lists = Table[Module[{p = MomentumExpand[d[[1]]] - Momentum[l, D], pv, dl},
       pv = If[p === 0, {0, 0, 0, 0}, Expand[p /. Momentum[x_, D] :> vecLB$[x]]];
       dl = Expand[2 dotLB$[vecLB$[l], pv] + dotLB$[pv, pv]];
       Table[Coefficient[Expand[DEN + Sum[(-dl)^n DEN^(n + 1), {n, 1, nmaxLB$}]], kap, n], {n, 0, nmaxLB$}]], {d, dens}];
   Fold[Function[{a, b}, Table[Expand[Sum[a[[i + 1]] b[[n - i + 1]], {i, 0, n}]], {n, 0, nmaxLB$}]], num, lists]];
(* averages of monomials in the components (D = 4: the orders k^2, k^4, k^6 are UV finite) and the tadpoles at M = 1 *)
dfactLB$[n_] := If[n <= 0, 1, n dfactLB$[n - 2]];
avgCompLB$[{a_, b_, cc_, d_}] := If[Or @@ OddQ[{a, b, cc, d}], 0,
   With[{k = (a + b + cc + d)/2}, LSQ^k dfactLB$[a - 1] dfactLB$[b - 1] dfactLB$[cc - 1] dfactLB$[d - 1] (-1)^((b + cc + d)/2)/
      Product[4 + 2 j, {j, 0, k - 1}]]];
tad4LB$[a_, b_] := (-1)^(a + b) (a + 1)! Gamma[b - a - 2]/Gamma[b];
integrateLB$[x_] := Module[{y = Expand[Total[(#[[2]] avgCompLB$[#[[1]]]) & /@ CoefficientRules[x, {q0, q1, q2, q3}]]]},
   Total[(#[[2]] tad4LB$ @@ #[[1]]) & /@ CoefficientRules[y, {LSQ, DEN}]]];
lowLB$ = expandBoxLB$ /@ (boxLB$ /. M -> 1);
redLB$[x_] := Expand[Expand[x] //. {sn^n_ /; n >= 2 :> sn^(n - 2) (1 - c^2), l1^n_ /; n >= 2 :> l1^(n - 2),
     l2^n_ /; n >= 2 :> l2^(n - 2), l3^n_ /; n >= 2 :> l3^(n - 2), l4^n_ /; n >= 2 :> l4^(n - 2)}];
o2LB$ = redLB$[Total[integrateLB$[#[[3]]] & /@ lowLB$]];
o4LB$ = redLB$[Total[integrateLB$[#[[5]]] & /@ lowLB$]];
o6LB$ = redLB$[Total[integrateLB$[#[[7]]] & /@ lowLB$]];
Print["(c) O(k^2) (expect 0): ", Simplify[o2LB$]];
(* Euler-Heisenberg with the same vectors: X = 8 c1 sum (f.f)(f.f) + 8 c2 sum (f.ft)(f.ft), c1 = 1/90, c2 = 7/360, all-incoming *)
epsLB$ = Normal[LeviCivitaTensor[4]];
qsLB$ = {vecLB$[k1], vecLB$[k2], -vecLB$[k3], -vecLB$[k4]} /. kap -> 1;
esLB$ = {vecLB$[e1], vecLB$[e2], vecLB$[e3], vecLB$[e4]};
fUpLB$ = Table[Outer[Times, qsLB$[[i]], esLB$[[i]]] - Outer[Times, esLB$[[i]], qsLB$[[i]]], {i, 4}];
fLoLB$ = gmLB$ . # . gmLB$ & /@ fUpLB$;
fDuLB$ = Table[1/2 TensorContract[TensorProduct[epsLB$, fLoLB$[[i]]], {{3, 5}, {4, 6}}], {i, 4}];
ffLB$[i_, j_] := Total[fLoLB$[[i]] fUpLB$[[j]], 2];
fdLB$[i_, j_] := Total[fLoLB$[[i]] fDuLB$[[j]], 2];
pairsLB$ = {{{1, 2}, {3, 4}}, {{1, 3}, {2, 4}}, {{1, 4}, {2, 3}}};
xEHLB$ = 8/90 Sum[ffLB$ @@ p[[1]] ffLB$ @@ p[[2]], {p, pairsLB$}] + 8 7/360 Sum[fdLB$ @@ p[[1]] fdLB$ @@ p[[2]], {p, pairsLB$}];
Print["(c) O(k^4) - Euler-Heisenberg, all helicities (expect 0): ", Simplify[redLB$[o4LB$ - xEHLB$]]];
helNamesLB$ = {"++++" -> {1, 1, 1, 1}, "+-+-" -> {1, -1, 1, -1}, "+--+" -> {1, -1, -1, 1}, "++--" -> {1, 1, -1, -1}, "+++-" -> {1, 1, 1, -1}};
(* s = 4 w^2, t = -2 w^2 (1 - c), u = -2 w^2 (1 + c) *)
mandLB$[x_] := Simplify[x /. w -> Sqrt[ss]/2 /. c -> 1 + 2 tt/ss /. sn -> Sqrt[1 - (1 + 2 tt/ss)^2], ss > 0 && -ss < tt < 0];
Do[Print["(c) ", h[[1]], ":  O(k^4) = ", InputForm[Factor[mandLB$[o4LB$ /. Thread[{l1, l2, l3, l4} -> h[[2]]]]]],
   ",  O(k^6) = ", InputForm[Factor[mandLB$[o6LB$ /. Thread[{l1, l2, l3, l4} -> h[[2]]]]]]], {h, helNamesLB$}];


(* ::Subsubsection:: *)
(*Inspect: the O(k^6) terms for all 16 helicities (w, c)*)


If[$Notebooks, TableForm[Table[{h, Factor[o6LB$ /. Thread[{l1, l2, l3, l4} -> h] /. sn^2 -> 1 - c^2]}, {h, Tuples[{-1, 1}, 4]}]]]


(* ::Section:: *)
(*(d) Tensor reduction and the values at the points*)


FCClearScalarProducts[];
SPD[k1, k1] = 0; SPD[k2, k2] = 0; SPD[k3, k3] = 0; SPD[k4, k4] = 0;
SPD[k1, k2] = ss/2; SPD[k3, k4] = ss/2; SPD[k1, k3] = -tt/2; SPD[k2, k4] = -tt/2; SPD[k1, k4] = -uu/2; SPD[k2, k3] = -uu/2;
SPD[e1, k1] = 0; SPD[e2, k2] = 0; SPD[e3, k3] = 0; SPD[e4, k4] = 0;
tidLB$ = Total[TID[FCE[MomentumExpand[Contract[DiracSimplify[# polLB$, DiracTraceEvaluate -> True]]]], l,
       UsePaVeBasis -> True, ToPaVe -> True] & /@ boxLB$] /. uu -> -ss - tt;
FCClearScalarProducts[];
pvLB$ = Union[Cases[tidLB$, _PaVe | _A0 | _B0 | _C0 | _D0, Infinity]];
(* X = tidLB$/(I Pi^2) = sum_j coef_j(D) PaVe_j *)
coefLB$ = Table[Coefficient[tidLB$, f], {f, pvLB$}]/(I Pi^2);
Print["(d) PaVe functions: ", Length[pvLB$], ";  remainder (expect 0): ", Simplify[tidLB$/(I Pi^2) - coefLB$ . pvLB$]];
poleLB$ = Normal[Series[(PaVeUVPart[#, Prefactor -> 1] /. D -> 4 - 2 eps) eps, {eps, 0, 0}]] & /@ pvLB$;
Print["(d) UV pole of the sum at general momenta (expect 0): ", Simplify[(coefLB$ /. D -> 4) . poleLB$]];


(* ::Subsubsection:: *)
(*Inspect: the PaVe functions*)


If[$Notebooks, pvLB$]


(* the points: label, w, c, sn, flavours (e or both), Package-X precision, LoopTools (1/0) *)
ptsLB$ = Select[StringSplit[ReadList[FileNameJoin[{srcDirLB$, "work", "lbl_points_exact.txt"}], String]], Length[#] == 7 &];
helsLB$ = Tuples[{-1, 1}, 4];
numCoefLB$[{wv_, cv_, snv_}, lam_, mv_] := Module[{v = <|k1 -> wv {1, 0, 0, 1}, k2 -> wv {1, 0, 0, -1}, k3 -> wv {1, snv, 0, cv},
     k4 -> wv {1, -snv, 0, -cv}, e1 -> polvLB$[1, 0, 1, lam[[1]]], e2 -> polvLB$[-1, 0, 1, lam[[2]]],
     e3 -> polcLB$[cv, snv, 1, lam[[3]]], e4 -> polcLB$[-cv, snv, -1, lam[[4]]]|>},
   coefLB$ /. Pair[Momentum[a_, D], Momentum[b_, D]] :> v[a] . gmLB$ . v[b] /. {ss -> 4 wv^2, tt -> -2 wv^2 (1 - cv), M -> mv}];
(* finite part of sum_j coef_j(4 - 2 eps) value_j(eps) (the pole is checked above) *)
finLB$[coefs_, vals_] := Module[{y = Expand[(coefs /. D -> 4 - 2 Epsilon) . vals]},
   Normal[Series[y, {Epsilon, 0, 0}]] /. Epsilon^(-1) -> 0 /. Epsilon -> 0];
evalPointLB$[{lab_, ws_, cs_, sns_, fl_, prec_, lt_}] := Module[{wv = ToExpression[ws], cv = ToExpression[cs], snv = ToExpression[sns],
    masses, rows},
   masses = If[fl === "both", {1, 17/10}, {1}];
   rows = Table[Module[{pvN = pvLB$ /. {ss -> 4 wv^2, tt -> -2 wv^2 (1 - cv), M -> mv}, pax, ltv},
       pax = N[Table[Quiet[PaXEvaluate[f, PaXD0Expand -> True, PaXC0Expand -> True]] /. ScaleMu -> 1, {f, pvN}], ToExpression[prec]];
       ltv = If[lt === "1", Quiet[LToolsEvaluate[#, LToolsSetMudim -> 1]] & /@ pvN, None];
       Table[Module[{cf = numCoefLB$[{wv, cv, snv}, h, mv]},
         {finLB$[cf, pax], If[ltv === None, Indeterminate, finLB$[cf, ltv]]}], {h, helsLB$}]], {mv, masses}];
   Table[{lab, 4 wv^2, cv, helsLB$[[i]], rows[[1, i, 1]], rows[[1, i, 2]],
     If[Length[rows] == 2, rows[[2, i, 1]], 0], If[Length[rows] == 2, rows[[2, i, 2]], 0]}, {i, 16}]];
outLB$ = Flatten[evalPointLB$ /@ ptsLB$, 1];
Print["(d) ", Length[ptsLB$], " points; max |Package-X - LoopTools| (both flavours, where LoopTools is used) = ",
  ScientificForm[Max[DeleteCases[Abs[N[#[[5]] - #[[6]]]] & /@ outLB$, Indeterminate]], 2]];


(* ::Subsubsection:: *)
(*Inspect: the first point*)


If[$Notebooks, TableForm[N[outLB$[[;; 16, {4, 5, 6}]], 14], TableHeadings -> {None, {"helicities", "Package-X X_e", "LoopTools X_e"}}]]


strLB$[x_] := If[x === Indeterminate, "nan", ToString[CForm[N[x, 20]]]];
Quiet[CreateDirectory[FileNameJoin[{srcDirLB$, "results"}]]];
Export[FileNameJoin[{srcDirLB$, "results", "lbl_feyncalc.csv"}],
  StringRiffle[Prepend[StringRiffle[Join[{#[[1]], strLB$[#[[2]]], strLB$[#[[3]]]}, ToString /@ #[[4]],
         strLB$ /@ Flatten[{Re[#[[5]]], Im[#[[5]]], Re[#[[6]]], Im[#[[6]]], Re[#[[7]]], Im[#[[7]]], Re[#[[8]]], Im[#[[8]]]}]], ","] & /@ outLB$,
     "label,s,cos,l1,l2,l3,l4,re_px_e,im_px_e,re_lt_e,im_lt_e,re_px_mu,im_px_mu,re_lt_mu,im_lt_mu"], "\n"] <> "\n", "Text"];
Print["(d) wrote results/lbl_feyncalc.csv (X = M/alpha^2 per flavour)"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


LToolsUnLoadLibrary[];
DeleteDirectory[modelTmpDirLB$, DeleteContents -> True];
