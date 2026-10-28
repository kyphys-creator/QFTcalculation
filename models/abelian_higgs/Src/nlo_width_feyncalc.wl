(* ::Package:: *)

(* ::Title:: *)
(*Step (5), FeynCalc: the one-loop h -> A A form factors in a general R_xi gauge (abelian Higgs model)*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (5).  Uses the FeynArts model of this note with GaugeXi kept.*)
(*  (a) the 1PI diagrams of h(p) -> A(k1) A(k2) and the diagrams with the tadpole attached to the A A h h vertex*)
(*      (zero-momentum h line), truncated, reduced to A0, B0, C0 with on-shell kinematics k1^2 = k2^2 = MA^2,*)
(*      p^2 = MH^2, exact in D;*)
(*  (b) the form factors of  M^{mu nu} = F_g g^{mu nu} + F_b k2^mu k1^nu + (terms with k1^mu or k2^nu, which vanish*)
(*      with physical polarizations), projected with the polarization sums P_i = -g + k_i k_i/MA^2 (exact in D);*)
(*  (c) at xi = 1 against FormCalc (results/nlo_width_formcalc.m from nlo_width_formcalc.wl): the UV poles and the*)
(*      MS-bar finite parts (FormCalc's four-dimensional coefficients with its rational terms) symbolically;*)
(*  (d) results/nlo_width_sigma.m (K x the form factors, 1PI and tadpole parts, general xi) for nlo_width_numeric.wl.*)
(*Normalization: K x (FeynArts amplitude) with K = 16 pi^2, as in oneloop_feyncalc.wl; the tree is 2 e MA g^{mu nu}.*)
(*Batch: wolframscript -file nlo_width_feyncalc.wl  (about 1 minute)*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirNW$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirNW$ = FileNameJoin[{srcDirNW$, "results"}];
modelTmpDirNW$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirNW$, "generated", "AbelianHiggs_FA"}], FileNameJoin[{modelTmpDirNW$, "AbelianHiggs_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirNW$, "AbelianHiggs_FA"}], Quiet -> True];
modelFileNW$ = FileNameJoin[{modelTmpDirNW$, "AbelianHiggs_FA", "AbelianHiggs_FA"}];

convNW$ = {FCGV["EL"] -> e, FCGV["MA"] -> MA, FCGV["MH"] -> MH, GaugeXi[A] -> xi, GaugeXi[V[1, ___]] -> xi,
   GaugeXi[S[2, ___]] -> xi, GaugeXi[U[1, ___]] -> xi, GaugeXi[S[1, ___]] -> 1, vev -> MA/e, lam -> e^2 MH^2/(2 MA^2)};
KK = (4 Pi)^2;

insertNW$[tops_] := Quiet[InsertFields[tops, {S[1]} -> {V[1], V[1]}, InsertionLevel -> {Particles},
    Model -> modelFileNW$, GenericModel -> modelFileNW$], RuleDelayed::rhs];
convertNW$[fa_] := Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> {p}, OutgoingMomenta -> {k1, k2},
      LoopMomenta -> {q}, LorentzIndexNames -> {mu, nu}, ChangeDimension -> D, List -> True, SMP -> False,
      DropSumOver -> True], RuleDelayed::rhs] /. convNW$ /.
   FeynAmpDenominator[PropagatorDenominator[0 | Momentum[0, ___], m_]] :> -1/m^2;
noTreeProp$[a_] := Cases[a, FeynAmpDenominator[x__] /; FreeQ[{x}, q], {0, Infinity}] === {};

tops1PI$ = CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Reducible}];
topsAll$ = CreateTopologies[1, 1 -> 2];
a1PI$ = convertNW$[CreateFeynAmp[insertNW$[tops1PI$], Truncated -> True, GaugeRules -> {}]];
aRed$ = convertNW$[CreateFeynAmp[insertNW$[Complement[topsAll$, tops1PI$]], Truncated -> True, GaugeRules -> {}]];
aTad$ = Select[aRed$, noTreeProp$];
Print["(a) diagrams: 1PI ", Length[a1PI$], ", tadpole attached to the vertex ", Length[aTad$], " (of ", Length[aRed$], " reducible)"];


(* ::Section:: *)
(*(a), (b) reduction and form factors*)


FCClearScalarProducts[];
SPD[k1, k1] = MA^2; SPD[k2, k2] = MA^2; SPD[k1, k2] = (MH^2 - 2 MA^2)/2;
reduceNW$[x_] := Module[{r},
   r = x /. Momentum[p, dim___] :> Momentum[k1 + k2, dim];
   r = TID[Contract[r], q, ToPaVe -> True];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {pp_}, {m1_, m2_}] :> B0[pp, m1, m2],
      PaVe[0, {a1_, a2_, a3_}, {m1_, m2_, m3_}] :> C0[a1, a2, a3, m1, m2, m3]};
   r = r /. {A0[0] -> 0};
   Contract[ExpandScalarProduct[r]]];

(* polarization sums in D dimensions; with T = F_g g + F_b k2^mu k1^nu + ..., the two contractions
   Q1 = P1_{mu a} P2_{nu b} g^{ab} T^{mu nu},  Q2 = P1_{mu a} P2_{nu b} k2^a k1^b T^{mu nu}
   give Q1 = F_g s11 + F_b s12, Q2 = F_g s12 + F_b s22 *)
pol1$[a_, b_] := -MTD[a, b] + FVD[k1, a] FVD[k1, b]/MA^2;
pol2$[a_, b_] := -MTD[a, b] + FVD[k2, a] FVD[k2, b]/MA^2;
contractNW$[t_, w_] := Simplify[Contract[ExpandScalarProduct[Contract[pol1$[mu, al] pol2$[nu, be] w t]]]];
s11$ = contractNW$[MTD[mu, nu], MTD[al, be]];
s12$ = contractNW$[FVD[k2, mu] FVD[k1, nu], MTD[al, be]];
s22$ = contractNW$[FVD[k2, mu] FVD[k1, nu], FVD[k2, al] FVD[k1, be]];
Print["(b) D-dimensional sums: s11 = ", s11$, ", s12 = ", Factor[s12$], ", s22 = ", Factor[s22$]];
formFactors$[amp_] := Module[{t = KK reduceNW$[amp], q1, q2, sol},
   q1 = contractNW$[t, MTD[al, be]];
   q2 = contractNW$[t, FVD[k2, al] FVD[k1, be]];
   sol = Solve[{q1 == fg s11$ + fb s12$, q2 == fg s12$ + fb s22$}, {fg, fb}][[1]];
   Simplify[{fg, fb} /. sol]];
ff1PI$ = Simplify[Total[formFactors$ /@ a1PI$]];
ffTad$ = Simplify[Total[formFactors$ /@ aTad$]];
Print["(b) K F_g (tadpole part) = ", InputForm[ffTad$[[1]]], ",  K F_b (tadpole part) = ", ffTad$[[2]]];
Print["(b) xi dependence: d(K F_g)/dxi and d(K F_b)/dxi of the 1PI part vanish? ",
  {Simplify[D[ff1PI$[[1]] /. {A0[x_] :> a0F[x], B0[x__] :> b0F[x], C0[x__] :> c0F[x]}, xi]] === 0,
   Simplify[D[ff1PI$[[2]] /. {A0[x_] :> a0F[x], B0[x__] :> b0F[x], C0[x__] :> c0F[x]}, xi]] === 0}];


(* ::Section:: *)
(*(c) comparison with FormCalc at xi = 1*)


(* canonical C0: the six relabellings of the triangle (cyclic, reflection) acting on (p1^2, p2^2, p3^2; m1^2, m2^2, m3^2) *)
canonC0$[a1_, a2_, a3_, m1_, m2_, m3_] := Module[{cyc, all},
   cyc = {{a1, a2, a3, m1, m2, m3}, {a2, a3, a1, m2, m3, m1}, {a3, a1, a2, m3, m1, m2}};
   all = Join[cyc, {#[[3]], #[[2]], #[[1]], #[[4]], #[[6]], #[[5]]} & /@ cyc];
   cC0 @@ First[Sort[all]]];
(* pole and MS-bar finite part: A0 = m^2/ep + a0f, B0 = 1/ep + b0f, C0 finite; D = 4 - 2 ep *)
splitFC$[x_] := Module[{y = x /. {A0[m2_] :> m2/ep + a0f[m2], B0[pp_, m1_, m2_] :> 1/ep + b0f[pp, Sequence @@ Sort[{m1, m2}]],
       C0[c__] :> canonC0$[c]} /. D -> 4 - 2 ep},
   Simplify[{SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}]];
fcRes$ = Association[Get[FileNameJoin[{resDirNW$, "nlo_width_formcalc.m"}]]];
fromFormCalc$[x_] := x /. mhsq -> MH^2 /. {fcA0[m2_] :> A0[m2], fcB0[pp_, m1_, m2_] :> B0[pp, m1, m2], fcC0[c__] :> C0[c]};
(* FormCalc's coefficients are four-dimensional (with its rational terms), so D -> 4 there *)
splitFormCalc$[x_] := splitFC$[fromFormCalc$[x] /. D -> 4];
ffXi1$ = Simplify[ff1PI$ + ffTad$ /. xi -> 1];
cmp$ = Table[Simplify[splitFC$[ffXi1$[[i]]] - splitFormCalc$[KK {fcRes$["Fg"], fcRes$["Fb"]}[[i]]]], {i, 2}];
Print["(c) xi = 1, {pole, finite} of FeynCalc - FormCalc:  F_g ", cmp$[[1]], ",  F_b ", cmp$[[2]], "   (expect {0, 0})"];
Print["(c) tree from FormCalc (expect 2 e MA): ", fcRes$["tree"]];


(* ::Section:: *)
(*(d) output*)


Put[{"Fg1PI" -> ff1PI$[[1]], "Fb1PI" -> ff1PI$[[2]], "FgTad" -> ffTad$[[1]], "FbTad" -> ffTad$[[2]]},
  FileNameJoin[{resDirNW$, "nlo_width_sigma.m"}]];
Print["(d) written results/nlo_width_sigma.m"];
