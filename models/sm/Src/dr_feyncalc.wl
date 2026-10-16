(* ::Package:: *)

(* ::Title:: *)
(*Step (5): muon decay at one loop -- vertex and box corrections, Delta r in R_xi gauge (FeynArts SM.mod + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm, step (5).  Compares with Eqs. (dr), (dZe), (dsw), (dmxi).*)
(*mu^-(p) -> nu_mu(k1) e^-(k2) nubar_e(k3) at zero external momenta (q^2 << MW^2), massless leptons.  At zero momenta the*)
(*QED corrections of the Fermi model in the charge-retention form vanish (Ward identity: vertex correction + field*)
(*renormalization = 0), so the one-loop amplitude is M0 (1 + Delta r) with*)
(*  Delta r = (Sigma^W_T(0) - delta M_W^2)/MW^2 + 2 delta Z_e - delta s_W^2/s_W^2 + delta'_VB,*)
(*  delta'_VB = vertex corrections + box diagrams + sum over the four leptons of delta Z^L/2 (photonic parts included).*)
(*IR divergences (gamma W boxes, charged-lepton field renormalization) are regularized by a photon mass lam (a copy of SM.mod*)
(*with Mass[V[1]] = MLam); lam -> 0 at the end.  The loop integrals at zero momenta are vacuum integrals: symmetric tensor*)
(*reduction of the loop momentum, partial fractions in q^2, int (q^2 - M^2)^-n = prod(D/2 - j)/(n-1)! A0(M)/M^(2(n-1)).*)
(*The box diagrams (UV and IR finite) are projected on the tree structure [gamma^r PL] x [gamma_r PL] in 4 dimensions*)
(*(4D Fierz-type identities 16 and 4); vertex corrections and self-energies stay in D dimensions.*)
(*(a) Feynman gauge: delta'_VB against e^2/s^2 [4 B0(0,MW,MW) + 6 + (7 - 4 s^2)/(2 s^2) ln c^2] / K, i.e. the note's*)
(*    -(2/(s c)) Sigma^AZ_T(0)/MZ^2 + alpha/(4 Pi s^2)(6 + ...); the cancellation of ln lam; Eq. (dr) from the pieces.*)
(*(b) General R_xi (xi_A, xi_Z, xi_W): Delta r(xi) - Delta r(1) = 0 with Sigma^W_T(0), delta'_VB in general xi and the*)
(*    xi dependence of delta M_W^2 from step (4) (Eq. (dmxi)); delta Z_e and delta s_W^2 do not depend on xi (step (4)).*)
(*(c) The note's self-energy formulas -> results/dr_note.m for the numbers in dr_numeric.wl.*)
(*Normalization: with PreFactor -> 1 the tree amplitude is i M0 and the loop amplitude (2 Pi)^D i M1; with X = (loop*)
(*integral)/(I Pi^2): delta = M1/M0 = I X/(K T), T the projected tree, K = (4 Pi)^2.  Fermion self-energy: K Sigma = X.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file dr_feyncalc.wl.  Interactive:  ~/hep/bin/wopen dr_feyncalc.wl, then "Run All Code".*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FAVerbose = 0;
FCSetDiracGammaScheme["NDR-Discard"];
(* SM.mod copy with a photon mass MLam (IR regulator) *)
faModels = FileNameJoin[{$FeynArtsDirectory, "Models"}];
srcDirDR$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
tmp = CreateDirectory[];
txt = Import[FileNameJoin[{faModels, "SM.mod"}], "Text"];
pos = StringPosition[txt, "V[1] == {"][[1, 1]];
blk = StringTake[txt, {pos, pos + 200}];
blk2 = StringReplace[blk, "Mass -> 0" -> "Mass -> MLam", 1];
txt2 = StringReplace[txt, blk -> blk2, 1];
Export[FileNameJoin[{tmp, "SMlam.mod"}], txt2, "Text"];
Print["photon mass in model copy: ", StringContainsQ[txt2, "Mass -> MLam"]];
modelLam = FileNameJoin[{tmp, "SMlam"}];
gauge1 = {_GaugeXi -> 1, _FAGaugeXi -> 1};
clean = {FCGV["EL"] -> e, FCGV["SW"] -> sw, FCGV["CW"] -> cw, FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH,
   FCGV["ME"] -> 0, FCGV["MM"] -> 0, FCGV["ML"] -> 0, MLE[_] -> 0, FCGV["MLam"] -> lam, MLam -> lam};
proc = {F[2, {2}]} -> {F[1, {2}], F[2, {1}], -F[1, {1}]};
conv[diags_, gr_] := FCFAConvert[Quiet[CreateFeynAmp[diags, Truncated -> False, PreFactor -> 1, GaugeRules -> gr], RuleDelayed::rhs],
    IncomingMomenta -> {p}, OutgoingMomenta -> {k1, k2, k3}, LoopMomenta -> {q}, ChangeDimension -> D, List -> True, SMP -> False,
    DropSumOver -> True, UndoChiralSplittings -> True] /. clean;
ins[tops_, pr_] := Quiet[InsertFields[tops, pr, InsertionLevel -> {Particles}, Model -> modelLam, GenericModel -> "Lorentz",
    ExcludeParticles -> {S[_]}], RuleDelayed::rhs];

(* external momenta -> 0 outside the spinors *)
extMoms = {p, k1, k2, k3};
zeroExt[x_] := Module[{y = FCI[x], sps, reps},
   sps = Union[Cases[y, _Spinor, Infinity]];
   reps = Thread[sps -> Array[spS, Length[sps]]];
   y = y /. reps;
   y = MomentumExpand[y] /. (Momentum[#, D] -> 0 & /@ extMoms) /. {DiracGamma[0, ___] -> 0, Pair[0, _] -> 0, Pair[_, 0] -> 0};
   y = y /. PropagatorDenominator[0, m_] :> pd0[m];
   y = y /. FeynAmpDenominator[a___, pd0[m_], b___] :> -1/m^2 FeynAmpDenominator[a, b] /. FeynAmpDenominator[] -> 1;
   y /. (Reverse /@ reps)];
(* symmetric tensor reduction of the loop momentum and vacuum integrals in q^2 *)
pairings[{}] := {{}};
pairings[l_List] := Flatten[Table[Prepend[#, {l[[1]], l[[i]]}] & /@ pairings[Delete[l, {{1}, {i}}]], {i, 2, Length[l]}], 1];
tensRed[x_] := Module[{y = Expand[Uncontract[FCI[x], q, Pair -> All, DiracGamma -> True]], terms},
   terms = If[Head[y] === Plus, List @@ y, {y}];
   Total[Function[t, Module[{idx = Join[Cases[t, Pair[LorentzIndex[mu_, D], Momentum[q, D]] :> mu, {1}],
          Flatten[Cases[t, Power[Pair[LorentzIndex[mu_, D], Momentum[q, D]], n_] :> ConstantArray[mu, n], {1}]]], rest, r},
       r = Length[idx];
       rest = t /. Power[Pair[LorentzIndex[_, D], Momentum[q, D]], _] -> 1 /. Pair[LorentzIndex[_, D], Momentum[q, D]] -> 1;
       If[!FreeQ[rest, Momentum[q, D]] && !FreeQ[rest /. FeynAmpDenominator[__] -> 1, Momentum[q, D]], Print["q left: ", InputForm[Short[rest, 5]]]];
       If[OddQ[r], 0,
        rest q2^(r/2)/Product[D + 2 j, {j, 0, r/2 - 1}] Total[Times @@ (Pair[LorentzIndex[#[[1]], D], LorentzIndex[#[[2]], D]] & /@ #) & /@ pairings[idx]]]]] /@ terms]];
vac[mm_, n_] := If[mm === 0, 0, Product[D/2 - j, {j, 1, n - 1}]/(n - 1)! A0L[mm]/mm^(n - 1)];
vacEval[x_] := Module[{y = x, terms},
   y = y /. Pair[Momentum[q, D], Momentum[q, D]] -> q2 /. FeynAmpDenominator[pds__] :> Times @@ (1/(q2 - #[[2]]^2) & /@ {pds});
   y = Expand[y];
   terms = If[Head[y] === Plus, List @@ y, {y}];
   terms = Flatten[(If[Head[#] === Plus, List @@ #, {#}] &[Apart[#, q2]]) & /@ terms];
   terms = terms /. Power[sq_, pp_?Negative] /; !FreeQ[sq, q2] && Exponent[sq, q2] == 1 :>
       Coefficient[sq, q2]^pp vacS[-(sq /. q2 -> 0)/Coefficient[sq, q2], -pp];
   Together[Total[Select[terms, !FreeQ[#, vacS] &]] /. vacS -> vac]];
(* projection of a two-chain structure on the tree structure [gamma^r PL] x [gamma_r PL] (4D) *)
proj[x_] := Module[{y = FCI[x]},
   y = y /. DOT[Spinor[Momentum[k1, ___], ___], a___, Spinor[Momentum[p, ___], ___]] :> ch1[DOT[a]] /.
     DOT[Spinor[Momentum[k2, ___], ___], b___, Spinor[-Momentum[k3, ___], ___]] :> ch2[DOT[b]];
   y = ChangeDimension[y, 4] /. D -> D;
   y = Expand[y] /. ch1[a_] ch2[b_] :> DiracTrace[a . GA[sig]] DiracTrace[b . GA[sig]]/16;
   (* Contract twice: products of the two traces' epsilon tensors are contracted only in the second pass *)
   Simplify[Contract[Contract[y /. DiracTrace[t_] :> DiracTrace[t, DiracTraceEvaluate -> True]]]]];


(* ::Section:: *)
(*(a) Feynman gauge: delta'_VB from the diagrams*)


(* tree *)
d0 = ins[CreateTopologies[0, 1 -> 3], proc];
a0 = conv[d0, gauge1];
tree = proj[DiracSimplify[zeroExt[Total[a0]]]];
Print["(a) tree diagrams ", Length[a0], ";  projected tree T = ", InputForm[tree], "   (expect i e^2/(2 s^2 MW^2))"];
(* vertices and boxes *)
tV = CreateTopologies[1, 1 -> 3, ExcludeTopologies -> {Tadpoles, WFCorrections, SelfEnergies, Boxes}];
tB = CreateTopologies[1, 1 -> 3, ExcludeTopologies -> {Tadpoles, WFCorrections, SelfEnergies, Triangles}];
dV = ins[tV, proc]; dB = ins[tB, proc];
aV = conv[dV, gauge1]; aB = conv[dB, gauge1];
Print["(a) vertex diagrams ", Length[aV], ", box diagrams ", Length[aB], "   (scalars excluded: their lepton couplings are proportional to the masses)"];
loopVal[a_] := Module[{y = zeroExt[a]},
   y = tensRed[y];
   y = DiracSimplify[Contract[y]];
   y = vacEval[y];
   proj[y]];
vV = loopVal /@ aV;
vB = loopVal /@ aB;
deltaV = Simplify[I Total[vV]/(16 Pi^2 tree)];
deltaB = Simplify[I Total[vB]/(16 Pi^2 tree)];


(* external field renormalization of the massless leptons: delta Z^L = -Sigma^L(0), Sigma = p-slash PL Sigma^L + ...,
   K Sigma = X; expansion of the 1PI self-energy to first order in p (tt) *)
DataType[tt, FCVariable] = True;
expF[PropagatorDenominator[mom_, m_]] := Module[{mm = MomentumExpand[mom], a, b, y},
   a = Coefficient[mm, Momentum[q, D]]; b = Coefficient[mm, Momentum[p, D]];
   (* p has already been scaled by tt, so b contains tt *)
   If[b === 0, denF[m], y = 2 a b Pair[Momentum[q, D], Momentum[p, D]] + b^2 Pair[Momentum[p, D], Momentum[p, D]];
     denF[m] - y denF[m]^2]];
seL[fld_] := Module[{d, a, y, x1, ar},
   d = ins[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {fld} -> {fld}];
   a = Total[FCFAConvert[Quiet[CreateFeynAmp[d, Truncated -> True, PreFactor -> 1, GaugeRules -> gauge1], RuleDelayed::rhs],
       IncomingMomenta -> {p}, OutgoingMomenta -> {p}, LoopMomenta -> {q}, ChangeDimension -> D, List -> True, SMP -> False,
       DropSumOver -> True, UndoChiralSplittings -> True] /. clean];
   y = MomentumExpand[FCI[a]] /. Momentum[p, D] -> tt Momentum[p, D];
   y = y /. FeynAmpDenominator[pds__] :> Times @@ (expF /@ {pds});
   y = Coefficient[Expand[ExpandScalarProduct[DiracGammaExpand[y]]], tt, 1];
   y = y /. denF[m_]^n_. :> FeynAmpDenominator @@ Table[PropagatorDenominator[Momentum[q, D], m], {n}];
   y = tensRed[y];
   y = DiracSimplify[Contract[y]];
   y = vacEval[y];
   ar = DiracSimplify[DiracTrace[y . GSD[p] . GA[6], DiracTraceEvaluate -> True]]/(2 SPD[p, p]);
   Simplify[FCE[ar]]];
xL = seL[F[2, {2}]]; xN = seL[F[1, {2}]];
Print["(a) K Sigma^L(0) (D dimensions): charged lepton ", InputForm[xL], ";  neutrino ", InputForm[xN]];
(* delta'_VB = (dZL_l + dZL_nu) + delta_vertex + delta_box, times K *)
kVB = Together[-xL - xN + 16 Pi^2 deltaV + 16 Pi^2 deltaB];
to4[x_] := Module[{y = Expand[x], fs, c},
   fs = Union[Cases[y, _A0L, Infinity]];
   Sum[c = Together[Coefficient[y, f]]; (c /. D -> 4) f - 2 (D[c, D] /. D -> 4) f[[1]], {f, fs}] + (y /. _A0L -> 0 /. D -> 4)];
kVB4 = Expand[to4[kVB] /. A0L[m2_] :> m2 (B00[m2] + 1)];
kVB4lam = Normal[Series[kVB4 /. B00[lam^2] -> LL, {lam, 0, 0}]] /. lam -> 0;
Print["(a) coefficient of ln lam^2 (B0(0,lam,lam)) in K delta'_VB: ", Simplify[Coefficient[Expand[kVB4lam], LL]], "   (expect 0: IR finite)"];
expect = e^2/sw^2 (4 B00[MW^2] + 6 + (7 - 4 sw^2)/(2 sw^2) (B00[MZ^2] - B00[MW^2]));
Print["(a) K delta'_VB - e^2/s^2 [4 B0(0,MW,MW) + 6 + (7-4s^2)/(2s^2) ln c^2] (d = 4, lam -> 0): ",
  Simplify[(kVB4lam - expect) /. {cw -> MW/MZ, sw -> Sqrt[1 - MW^2/MZ^2]}, MZ > MW > 0]];
Print["(a) pieces (d = 4, ln lam^2 -> LL): vertex ", InputForm[Simplify[Normal[Series[Expand[to4[16 Pi^2 deltaV] /. A0L[m2_] :> m2 (B00[m2] + 1)] /. B00[lam^2] -> LL, {lam, 0, 0}]]]],
  ";  box ", InputForm[Simplify[Normal[Series[Expand[to4[16 Pi^2 deltaB] /. A0L[m2_] :> m2 (B00[m2] + 1)] /. B00[lam^2] -> LL, {lam, 0, 0}]]]]];

(* Eq. (dr) from the pieces: Delta r = (Sigma^W(0) - dMW2)/MW^2 + 2 dZe - dsw2 + delta'_VB with Eqs. (dZe), (dsw) *)
drAssembled = (sW0 - dMW2)/MW^2 + (pi0 + 2 (sw/cw) az0/MZ^2) - (cw^2/sw^2) (dMZ2/MZ^2 - dMW2/MW^2) - 2/(sw cw) az0/MZ^2 + fin;
drNote = pi0 - (cw^2/sw^2) (dMZ2/MZ^2 - dMW2/MW^2) + (sW0 - dMW2)/MW^2 - 2 (cw/sw) az0/MZ^2 + fin;
Print["(a) Delta r assembled from the pieces minus Eq. (dr) (with c^2 + s^2 = 1): ", Simplify[(drAssembled - drNote) /. cw -> Sqrt[1 - sw^2]], "   (expect 0)"];


(* ::Section:: *)
(*(b) General R_xi: Delta r does not depend on xi*)


(* ===== general R_xi ===== *)
xiR = {(GaugeXi | FAGaugeXi)[A | V[1] | U[1]] -> xA, (GaugeXi | FAGaugeXi)[Z | V[2] | S[2] | U[2]] -> xZ,
   (GaugeXi | FAGaugeXi)[W | V[3] | S[3] | U[3] | U[4]] -> xW};
gauge1 = {};   (* keep GaugeXi in CreateFeynAmp *)
clean = Join[clean, xiR];
a0x = conv[d0, {}] /. xiR; treeX = proj[DiracSimplify[zeroExt[Total[a0x]]]];
aVx = conv[dV, {}] /. xiR; aBx = conv[dB, {}] /. xiR;
t0 = AbsoluteTime[];
kVBxi = Together[16 Pi^2 I (Total[loopVal /@ aVx] + Total[loopVal /@ aBx])/(16 Pi^2 treeX) - seL[F[2, {2}]] - seL[F[1, {2}]]];
Print["(b) general xi: K delta'_VB computed in ", Round[AbsoluteTime[] - t0], " s"];
(* Sigma^W_T(0) = -g_{mu nu} X^{mu nu}(0)/D in general xi (1PI, no tadpoles) *)
sigW0[] := Module[{d, a},
   d = Quiet[InsertFields[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {-V[3]} -> {-V[3]}, InsertionLevel -> {Classes},
      Model -> modelLam, GenericModel -> "Lorentz"], RuleDelayed::rhs];
   a = FCFAConvert[Quiet[CreateFeynAmp[d, Truncated -> True, PreFactor -> 1, GaugeRules -> {}], RuleDelayed::rhs] /.
       {SumOver[Index[Colour, _], 3, ___] :> Nc}, IncomingMomenta -> {k}, OutgoingMomenta -> {k}, LoopMomenta -> {q},
      LorentzIndexNames -> {li1, li2}, ChangeDimension -> D, List -> True, SMP -> False, DropSumOver -> True,
      UndoChiralSplittings -> True] /. clean /. {MQU[_] -> mu, MQD[_] -> md, CKM[__] -> 1, Conjugate[x_] :> x, IndexDelta[__] -> 1};
   a = (zeroExt[#] & /@ a) /. extMoms -> extMoms;
   Together[-Total[vacEval[DiracSimplify[Contract[tensRed[# /. DiracTrace[t_] :> DiracTrace[t, DiracTraceEvaluate -> True]] MTD[li1, li2]]]] & /@
        (zeroExtK /@ a)]/D]];
zeroExtK[x_] := Module[{y = MomentumExpand[FCI[x]] /. Momentum[k, D] -> 0 /. {DiracGamma[0, ___] -> 0, Pair[0, _] -> 0, Pair[_, 0] -> 0}},
   y /. PropagatorDenominator[0, m_] :> pd0[m] /. FeynAmpDenominator[a___, pd0[m_], b___] :> -1/m^2 FeynAmpDenominator[a, b] /.
     FeynAmpDenominator[] -> 1];
kSW0 = sigW0[];

(* xi dependence of delta M_W^2 (delta t = -T), step (4): K(dMW2(xi) - dMW2(1)) = e^2/(4 s^2)[2(A0(xW MW^2) - A0(MW^2)) + A0(xZ MZ^2) - A0(MZ^2)] *)
kdMW2xi = e^2/(4 sw^2) (2 (A0L[MW^2 xW] - A0L[MW^2]) + A0L[MZ^2 xZ] - A0L[MZ^2]);
kDrXi = Together[kSW0/MW^2 - kdMW2xi/MW^2 + kVBxi];
kDr1 = kDrXi /. {xA -> 1, xZ -> 1, xW -> 1};
scal = {A0L[m_ x : (xW | xZ | xA)] :> x^(D/2 - 1) A0L[m]};
diffXi = Together[(kDrXi - kDr1) /. scal];
d4 = Expand[to4[diffXi] /. A0L[m2_] :> m2 (B00[m2] + 1)];
d4lam = Normal[Series[d4 /. B00[lam^2] -> LL, {lam, 0, 0}]] /. lam -> 0;
Print["(b) K (Delta r(xi) - Delta r(1)), d = 4, lam -> 0: ", InputForm[Simplify[d4lam /. {cw -> MW/MZ, sw -> Sqrt[1 - MW^2/MZ^2]}, MZ > MW > 0]]];
xiDep[x_] := Simplify[Normal[Series[Expand[to4[Together[(x - (x /. {xA -> 1, xZ -> 1, xW -> 1})) /. scal]] /.
        A0L[m2_] :> m2 (B00[m2] + 1)] /. B00[lam^2] -> LL, {lam, 0, 0}]] /. lam -> 0 /. {cw -> MW/MZ, sw -> Sqrt[1 - MW^2/MZ^2]}, MZ > MW > 0];
Print["(b) the pieces depend on xi: K(Sigma^W(0)(xi) - Sigma^W(0)(1))/MW^2 is ", If[xiDep[kSW0/MW^2] === 0, "0", "nonzero"],
  ", K(delta'_VB(xi) - delta'_VB(1)) is ", If[xiDep[kVBxi] === 0, "0", "nonzero"], ";  their xi_A parts cancel: ",
  Simplify[Coefficient[Expand[xiDep[kSW0/MW^2 + kVBxi]], xA]]];


(* ::Section:: *)
(*(c) The note's formulas for the numbers*)


(* ::Text:: *)
(*The note's formulas, times K, per generation (ml, mu, md; Nc), with c = MW/MZ, s = sqrt(1 - c^2) and B0OL[k2, m1^2, m2^2].*)


b00OL[m2_] := B0OL[0, m2, m2];
a0nOL[m2_] := m2 (b00OL[m2] + 1);
b0zOL[m1_, m2_] := Which[m1 === m2, b00OL[m1], m1 === 0, b00OL[m2] + 1, m2 === 0, b00OL[m1] + 1, True, (a0nOL[m1] - a0nOL[m2])/(m1 - m2)];
FFOL[k2_, m2_] := -(k2 + 2 m2) B0OL[k2, m2, m2] + 2 m2 b00OL[m2] + k2/3;
GGOL[k2_, m12_, m22_] := (-(k2 - (m12 + m22)/2) B0OL[k2, Sequence @@ Sort[{m12, m22}]] + k2/3 + m12 b00OL[m12] + m22 b00OL[m22] +
    (m12 - m22)^2/(2 k2) (B0OL[k2, Sequence @@ Sort[{m12, m22}]] - b0zOL[m12, m22])) /. b00OL[0] -> 0 /. B0OL[0, 0, 0] -> 0;
sN = Sqrt[1 - c^2]; MZ2N = MW^2/c^2;
fermOL$ = {{1, -1, -1/2, ml^2}, {1, 0, 1/2, 0}, {Nc, 2/3, 1/2, mu^2}, {Nc, -1/3, -1/2, md^2}};
gVN[q_, t3_] := (t3 - 2 q sN^2)/(2 sN c); gAN[t3_] := t3/(2 sN c);
noteF["AA"] = -e^2 (4/3) Sum[f[[1]] f[[2]]^2 FFOL[kk, f[[4]]], {f, fermOL$}];
noteF["AZ"] = -e^2 (4/3) Sum[f[[1]] f[[2]] gVN[f[[2]], f[[3]]] FFOL[kk, f[[4]]], {f, fermOL$}];
noteF["ZZ"] = -e^2 Sum[f[[1]] ((4/3) (gVN[f[[2]], f[[3]]]^2 + gAN[f[[3]]]^2) FFOL[kk, f[[4]]] + f[[4]]/(2 sN^2 c^2) B0OL[kk, f[[4]], f[[4]]]), {f, fermOL$}];
noteF["WW"] = -e^2/(3 sN^2) (GGOL[kk, 0, ml^2] + Nc GGOL[kk, mu^2, md^2]);
noteF["HH"] = -e^2 Sum[f[[1]] f[[4]]/(2 sN^2 MW^2) (2 a0nOL[f[[4]]] + (4 f[[4]] - kk) B0OL[kk, f[[4]], f[[4]]]), {f, fermOL$}];
noteF["T"] = -2 e/(sN MW) Sum[f[[1]] f[[4]] a0nOL[f[[4]]], {f, fermOL$}];
noteB["AA"] = -e^2 ((3 kk + 4 MW^2) B0OL[kk, MW^2, MW^2] - 4 MW^2 b00OL[MW^2]);
noteB["AZ"] = -e^2/(3 sN c) (((9 c^2 + 1/2) kk + (12 c^2 + 4) MW^2) B0OL[kk, MW^2, MW^2] - (12 c^2 - 2) MW^2 b00OL[MW^2] + kk/3);
noteB["ZZ"] = -e^2 (1/(6 sN^2 c^2) (((18 c^4 + 2 c^2 - 1/2) kk + (24 c^4 + 16 c^2 - 10) MW^2) B0OL[kk, MW^2, MW^2] -
       (24 c^4 - 8 c^2 + 2) MW^2 b00OL[MW^2] + (4 c^2 - 1) kk/3) +
     1/(12 sN^2 c^2) ((2 MH^2 - 10 MZ2N - kk) B0OL[kk, Sequence @@ Sort[{MH^2, MZ2N}]] - 2 MZ2N b00OL[MZ2N] - 2 MH^2 b00OL[MH^2] -
       (MZ2N - MH^2)^2/kk (B0OL[kk, Sequence @@ Sort[{MH^2, MZ2N}]] - b0zOL[MZ2N, MH^2]) - 2 kk/3));
noteB["WW"] = -e^2 ((2/3) ((2 MW^2 + 5 kk) B0OL[kk, 0, MW^2] - 2 MW^2 b00OL[MW^2] - MW^4/kk (B0OL[kk, 0, MW^2] - b0zOL[MW^2, 0]) + kk/3) +
     1/(12 sN^2) (((40 c^2 - 1) kk + (16 c^2 + 54 - 10/c^2) MW^2) B0OL[kk, Sequence @@ Sort[{MW^2, MZ2N}]] -
       (16 c^2 + 2) (MW^2 b00OL[MW^2] + MZ2N b00OL[MZ2N]) + (4 c^2 - 1) 2 kk/3 -
       (8 c^2 + 1) (MW^2 - MZ2N)^2/kk (B0OL[kk, Sequence @@ Sort[{MW^2, MZ2N}]] - b0zOL[MW^2, MZ2N])) +
     1/(12 sN^2) ((2 MH^2 - 10 MW^2 - kk) B0OL[kk, Sequence @@ Sort[{MH^2, MW^2}]] - 2 MW^2 b00OL[MW^2] - 2 MH^2 b00OL[MH^2] -
       (MW^2 - MH^2)^2/kk (B0OL[kk, Sequence @@ Sort[{MH^2, MW^2}]] - b0zOL[MW^2, MH^2]) - 2 kk/3));
noteB["HH"] = e^2/(8 sN^2 MW^2) (3 MH^2 a0nOL[MH^2] + 2 (MH^2 + 6 MW^2) a0nOL[MW^2] + (MH^2 + 6 MZ2N) a0nOL[MZ2N] +
     9 MH^4 B0OL[kk, MH^2, MH^2] + 2 (MH^4 - 4 kk MW^2 + 12 MW^4) B0OL[kk, MW^2, MW^2] + (MH^4 - 4 kk MZ2N + 12 MZ2N^2) B0OL[kk, MZ2N, MZ2N] -
     24 MW^4 - 12 MZ2N^2);
noteB["T"] = e/(4 sN MW) (3 MH^2 a0nOL[MH^2] + 2 (MH^2 + 6 MW^2) a0nOL[MW^2] + (MH^2 + 6 MZ2N) a0nOL[MZ2N] - 8 MW^4 - 4 MZ2N^2);
toCOL$[x_] := x /. {cw -> c, sw -> Sqrt[1 - c^2]} /. MZ -> MW/c /. B0OL[p_, m1_, m2_] :> B0OL[p, Sequence @@ Sort[{m1, m2}]];
diffOL$[x_, y_] := Simplify[Expand[toCOL$[x] - toCOL$[y]] /. Sqrt[1 - c^2]^n_ :> (1 - c^2)^(n/2), 0 < c < 1];

Put[<|"noteF" -> Association[Table[key -> noteF[key], {key, {"AA", "AZ", "ZZ", "WW", "HH", "T"}}]],
    "noteB" -> Association[Table[key -> noteB[key], {key, {"AA", "AZ", "ZZ", "WW", "HH", "T"}}]]|>,
  FileNameJoin[{srcDirDR$, "results", "dr_note.m"}]];
Print["(c) wrote the note's self-energy formulas (K Sigma per generation; symbols kk, e, c, MW, MH, ml, mu, md, Nc; B0OL) to results/dr_note.m"];
DeleteDirectory[tmp, DeleteContents -> True];
