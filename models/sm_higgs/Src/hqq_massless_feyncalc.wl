(* ::Package:: *)

(* ::Title:: *)
(*Step (3) of the Higgs note: H -> q qbar at NLO QCD for massless quarks, exact in d = 4 - 2 eps*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (3); the scalar-current version of the NLO note's ir_massless_feyncalc.wl (step (2)).*)
(*H(k) -> f(p1) fbar(p2) through the Yukawa vertex (the coupling y/sqrt(2) and the colour stripped; the current is the unit*)
(*matrix), and the abelian part of the radiation: the boson couples with e Q gamma^rho, alpha C = alpha_s C_F for the gluon,*)
(*alpha Q_f^2 for the photon.  Everything in d dimensions (FeynCalc).*)
(*  Real: H -> f fbar g, two diagrams, sum|M_R|^2 (polarization sum -g: the colour current is conserved), in y_ij = s_ij/M^2;*)
(*        the phase spaces and the Dirichlet integrals as in the NLO note.*)
(*  Virtual: the vertex with the boson in Feynman gauge, TID to B0(M^2, 0, 0) and C0(0, 0, M^2, 0, 0, 0) (the massless*)
(*        self-energies are scaleless: the field constants are 0), and the MS-bar counterterm of the Yukawa coupling,*)
(*        y0 = y(mu) (1 + dy/y), dy/y = -3 (alpha C/(4 pi)) S_eps/eps, S_eps = (4 pi)^eps e^(-gamma eps).  Unlike the vector current*)
(*        of the Z, the scalar vertex is UV divergent; the counterterm removes that pole.*)
(*In units of N(eps) = (alpha C/(4 pi)) (4 pi mu^2/M^2)^eps/Gamma(1 - eps) the real and the vertex are functions of eps only and*)
(*the counterterm is -6 e^(-gamma eps) Gamma(1 - eps) w^(-eps)/eps, w = mu^2/M^2; the sum must have no poles and give*)
(*17 + 6 ln w, that is Gamma = Gamma_0(y(mu)) [1 + C_F (alpha_s/pi)(17/4 + (3/2) ln(mu^2/M^2))], Eq. (hqq).*)
(*The 4-dimensional sum|M_R|^2 is compared with the note's FeynArts model for H -> u ubar g and H -> mu- mu+ gamma (the masses*)
(*set to 0 and the Yukawa couplings kept as their own symbols).  Writes results/hqq_massless.csv.*)
(*Batch:  wolframscript -file hqq_massless_feyncalc.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirHM$ = DirectoryName[$InputFileName];
resDirHM$ = FileNameJoin[{srcDirHM$, "results"}];
Quiet[CreateDirectory[resDirHM$]];

(* ::Section:: *)
(*Born and real emission in d dimensions*)

spinsum$[amp_, idx_] := Module[{x = FermionSpinSum[amp ComplexConjugate[amp /. Thread[idx -> (idx /. {rho -> sig})]]]},
   x = x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
   Simplify[Contract[x If[MemberQ[idx, rho], -MTD[rho, sig], 1]] /. D -> 4 - 2 eps]];
amp0$ = Spinor[Momentum[p1, D], 0].Spinor[-Momentum[p2, D], 0];
ampR$ = eQ Spinor[Momentum[p1, D], 0].(GAD[rho].GSD[p1 + p3]/(MM y13) - GSD[p2 + p3].GAD[rho]/(MM y23)).Spinor[-Momentum[p2, D], 0];

FCClearScalarProducts[];
ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[p1, p2] = MM/2;
born$ = spinsum$[amp0$, {}];
Print["Born sum|M0|^2 (coupling and colour stripped): ", born$, "   (expect 2 M^2)"];

FCClearScalarProducts[];
ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[p3, p3] = 0;
ScalarProduct[p1, p2] = MM y12/2; ScalarProduct[p1, p3] = MM y13/2; ScalarProduct[p2, p3] = MM y23/2;
real$ = spinsum$[ampR$, {rho}];
r$ = Simplify[MM real$/(eQ^2 born$) /. y12 -> 1 - y13 - y23];
Print["r = M^2 sum|M_R|^2/(e^2 Q^2 sum|M_0|^2): ", r$];
(* the note's Appendix: 2 [(1 - eps)(1 + y12^2) + 2 eps y12]/(y13 y23) *)
rNote$ = 2 ((1 - eps) (1 + (1 - y13 - y23)^2) + 2 eps (1 - y13 - y23))/(y13 y23);
Print["  minus the form of Appendix A (expect 0): ", Simplify[r$ - rNote$]];

(* the Dirichlet integrals: int dy13 dy23 y12^(a - 1) y13^(b - 1) y23^(c - 1) = Gamma(a) Gamma(b) Gamma(c)/Gamma(a + b + c), with the
   weight (y12 y13 y23)^(-eps) of the d-dimensional phase space; r as monomials in y12, y13, y23 *)
(* r with y12 eliminated is a Laurent polynomial in y13, y23 (its denominator is y13 y23): expand it into monomials *)
rMono$ = Expand[Together[r$]];
Print["  denominator of r: ", Denominator[Together[r$]], ";  the monomials reproduce r: ", Simplify[rMono$ - r$] === 0];
dirichlet$[expr_] := Module[{t = Expand[expr], terms},
   terms = If[Head[t] === Plus, List @@ t, {t}];
   Total[Function[term, Module[{c, e12, e13, e23},
        c = term /. {y12 -> 1, y13 -> 1, y23 -> 1};
        {e12, e13, e23} = Exponent[term, #] & /@ {y12, y13, y23};
        c Gamma[1 - eps + e12] Gamma[1 - eps + e13] Gamma[1 - eps + e23]/Gamma[3 - 3 eps + e12 + e13 + e23]]] /@ terms]];
gR$ = FullSimplify[dirichlet$[rMono$] (MM/(2 (4 Pi)^3) (4 Pi/MM)^(2 eps)/Gamma[2 - 2 eps]) /
     ((4 Pi/MM)^eps Gamma[1 - eps]/(8 Pi Gamma[2 - 2 eps])) (16 Pi^2/MM) Gamma[1 - eps] (4 Pi/MM)^(-eps)];
Print["Gamma_R/(Gamma_0 N(eps)), exact: ", gR$];
serR$ = Expand[Normal[Series[gR$, {eps, 0, 0}]]];
Print["  expanded: ", serR$];

(* ::Section:: *)
(*Virtual correction in d dimensions*)

FCClearScalarProducts[];
ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[p1, p2] = MM/2;
vtx$ = Spinor[Momentum[p1, D], 0].GAD[rho].(GSD[p1] - GSD[q]).(-GSD[p2] - GSD[q]).GAD[rho].Spinor[-Momentum[p2, D], 0] *
   FAD[q, q - p1, q + p2];
x$ = FermionSpinSum[vtx$ ComplexConjugate[amp0$]];
x$ = Contract[x$ /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]];
v$ = Simplify[TID[x$, q, ToPaVe -> True] /. {B0[0, 0, 0] -> 0, PaVe[0, {0}, {0, 0}] -> 0}];
Print["TID: ", v$];
b0r$ = (4 Pi w)^eps Gamma[eps] Gamma[1 - eps]^2/Gamma[2 - 2 eps];
toExact$[x_] := x /. {B0[MM, 0, 0] -> b0r$ ph, C0[0, 0, MM, 0, 0, 0] -> 2 (D - 3)/((4 - D) MM) b0r$ ph,
      C0[0, MM, 0, 0, 0, 0] -> 2 (D - 3)/((4 - D) MM) b0r$ ph, C0[MM, 0, 0, 0, 0, 0] -> 2 (D - 3)/((4 - D) MM) b0r$ ph} /. D -> 4 - 2 eps;
Print["  PaVe functions left (expect {}): ", Union[Cases[toExact$[v$], _B0 | _C0 | _PaVe, Infinity]]];
(* the factors of the NLO note: M1/M0 = [TID/(i pi^2)] (-i e^2 Q^2)(i/(16 pi^2))/sum|M0|^2 = (e^2 Q^2/(16 pi^2)) b0r ph k *)
k$ = Simplify[toExact$[v$]/(I Pi^2)/born$ (-I eQ^2) (I/(16 Pi^2))/((eQ^2/(16 Pi^2)) b0r$ ph)];
Print["  k (expect a real rational function of eps): ", k$];
gV$ = FullSimplify[2 ComplexExpand[Re[k$ Exp[I Pi eps]]] Gamma[eps] Gamma[1 - eps]^3/Gamma[2 - 2 eps],
   Assumptions -> eps > 0 && eps < 1/2];
Print["Gamma_V(vertex)/(Gamma_0 N(eps)), exact: ", gV$];
serV$ = Expand[Normal[Series[gV$, {eps, 0, 0}]]];
Print["  expanded: ", serV$];
(* the MS-bar counterterm: 2 dy/y over N(eps) *)
gCT$ = -6 Exp[-EulerGamma eps] Gamma[1 - eps] wR^(-eps)/eps;
serCT$ = Expand[Normal[Series[gCT$, {eps, 0, 0}]]];
Print["2 dy/y/(Gamma_0 N(eps)), MS-bar: ", serCT$, "   (wR = mu^2/M^2)"];

(* ::Section:: *)
(*The sum*)

serSum$ = Simplify[Normal[Series[gR$ + gV$ + gCT$, {eps, 0, 1}]]];
Print["(Gamma_R + Gamma_V + counterterm)/(Gamma_0 N(eps)) to O(eps): ", serSum$];
Print["  at eps = 0, minus (17 + 6 ln w) (expect 0): ", Simplify[(serSum$ /. eps -> 0) - (17 + 6 Log[wR])]];
Print["  without the counterterm, the pole of real + vertex: ", Simplify[Coefficient[Expand[Normal[Series[gR$ + gV$, {eps, 0, 0}]]], eps, -1]],
  "   (the UV pole of the vertex: +6/eps)"];

(* ::Section:: *)
(*The 4-dimensional sum|M_R|^2 against the note's FeynArts model*)

tmpHM$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirHM$, "generated", "SM_CKM_FA"}], FileNameJoin[{tmpHM$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{tmpHM$, "SM_CKM_FA"}], Quiet -> True];
modelHM$ = FileNameJoin[{tmpHM$, "SM_CKM_FA", "SM_CKM_FA"}];
(* the spinor masses come as bare symbols (the Higgs note's step (1)) *)
convHM$ = {FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["MZ"] -> MZ, FCGV["MW"] -> MW, FCGV["MH"] -> MH,
   MMU -> 0, MU -> 0, FCGV["MMU"] -> 0, FCGV["MU"] -> 0};
yukHM$ = {yl[i_Integer, j_Integer] :> If[i == j, yL[i], 0], yu[i_Integer, j_Integer] :> If[i == j, yU[i], 0],
   yd[i_Integer, j_Integer] :> If[i == j, yD[i], 0]};
fa3$[out_] := Module[{d, a, x},
   d = Quiet[InsertFields[CreateTopologies[0, 1 -> 3], {S[1]} -> out, InsertionLevel -> {Particles},
       Model -> modelHM$, GenericModel -> modelHM$, ExcludeParticles -> {S[2], S[3], V[2], V[3]}], RuleDelayed::rhs];
   a = Quiet[FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {k}, OutgoingMomenta -> {p1, p2, p3},
       ChangeDimension -> 4, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> True,
       TransversePolarizationVectors -> {}], RuleDelayed::rhs] /. convHM$ /. yukHM$;
   Print["   ", Length[a], " diagrams"];
   FCClearScalarProducts[];
   ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[p3, p3] = 0; ScalarProduct[k, k] = MH^2;
   ScalarProduct[p1, p2] = MH^2 y12/2; ScalarProduct[p1, p3] = MH^2 y13/2; ScalarProduct[p2, p3] = MH^2 y23/2;
   ScalarProduct[k, p1] = MH^2 (y12 + y13)/2; ScalarProduct[k, p2] = MH^2 (y12 + y23)/2; ScalarProduct[k, p3] = MH^2 (y13 + y23)/2;
   x = FermionSpinSum[ComplexConjugate[Total[a]] Total[a], ExtraFactor -> 1];
   x = x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
   x = DoPolarizationSums[x, p3, 0, VirtualBoson -> True];
   x = Contract[FeynAmpDenominatorExplicit[SUNSimplify[DiracSimplify[x], SUNNToCACF -> False]]] /. SUNN -> 3;
   Simplify[x /. y12 -> 1 - y13 - y23]];
(* the hand value: sum|M_R|^2 = N_c C cpl^2 y^2 r (Born: (y^2/2) N_c 2 M^2) *)
r4$ = r$ /. eps -> 0;
Print["H -> u ubar g:"];
dU$ = Simplify[fa3$[{F[3, {1}], -F[3, {1}], V[4]}] - 3 (4/3) gS^2 yU[1]^2 r4$];
Print["   FeynArts model minus hand, with C_F = 4/3 (expect 0): ", dU$];
Print["H -> mu- mu+ gamma:"];
dMu$ = Simplify[fa3$[{F[2, {2}], -F[2, {2}], V[1]}] - ee^2 yL[2]^2 r4$];
Print["   FeynArts model minus hand (expect 0): ", dMu$];
DeleteDirectory[tmpHM$, DeleteContents -> True];

Export[FileNameJoin[{resDirHM$, "hqq_massless.csv"}], {{"quantity", "value"},
   {"born_over_2M2", ToString[InputForm[Simplify[born$/(2 MM)]]]},
   {"r_minus_appendix", ToString[InputForm[Simplify[r$ - rNote$]]]},
   {"real_over_N_exact", ToString[InputForm[gR$]]}, {"vertex_over_N_exact", ToString[InputForm[gV$]]},
   {"real_over_N_series", ToString[InputForm[serR$]]}, {"vertex_over_N_series", ToString[InputForm[serV$]]},
   {"counterterm_over_N_series", ToString[InputForm[serCT$]]},
   {"sum_over_N_to_O_eps", ToString[InputForm[serSum$]]},
   {"sum_at_eps0_minus_17_plus_6lnw", ToString[InputForm[Simplify[(serSum$ /. eps -> 0) - (17 + 6 Log[wR])]]]},
   {"model_minus_hand_H_uug", ToString[InputForm[dU$]]}, {"model_minus_hand_H_mumugamma", ToString[InputForm[dMu$]]}}, "CSV"];
Print["written: results/hqq_massless.csv"];
