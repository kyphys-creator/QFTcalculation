(* ::Package:: *)

(* ::Title:: *)
(*Step (2) of the NLO note: real emission and virtual correction for massless fermion pairs, exact in d = 4 - 2 eps*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (2).  Z(k) -> f(p1) fbar(p2) with the current gamma^mu Gam, Gam = 1 or gamma5 (the vector*)
(*and the axial parts of Eq. (lo) separately: their interference drops out of the width), and the abelian part of the*)
(*radiation: the radiated boson couples with e Q gamma^rho, and alpha C is alpha Q_f^2 for the photon, alpha_s C_F for the*)
(*gluon.  Everything in d dimensions (FeynCalc; gamma5 anticommuting).*)
(*  Real: Z -> f fbar gamma, two diagrams, sum|M_R|^2 over spins and polarizations (-g for both vectors: the currents are*)
(*        conserved), in y_ij = s_ij/M^2 (y12 + y13 + y23 = 1); the d-dimensional phase spaces*)
(*          int dPhi3 = M^2/(2 (4 pi)^3) (4 pi/M^2)^(2 eps)/Gamma(2 - 2 eps) int dy13 dy23 (y12 y13 y23)^(-eps),*)
(*          int dPhi2 = (4 pi/M^2)^eps Gamma(1 - eps)/(8 pi Gamma(2 - 2 eps));*)
(*        the y integrals are Dirichlet integrals.*)
(*  Virtual: the vertex with the radiated boson in Feynman gauge, reduced by TID to B0(M^2, 0, 0) and*)
(*        C0(0, 0, M^2, 0, 0, 0) = 2 (d - 3)/((4 - d) M^2) B0,  B0 = (4 pi mu^2/M^2)^eps Gamma(eps) Gamma(1 - eps)^2/Gamma(2 - 2 eps) e^(i pi eps)*)
(*        (LoopTools' normalization; the massless self-energies are scaleless and vanish, so the field constants are 0).*)
(*Both are written as N(eps) = (alpha C/(4 pi)) (4 pi mu^2/M^2)^eps/Gamma(1 - eps) times a function of eps only; the sum must*)
(*have no poles and give 3 N, that is (3/4) alpha C/pi.  The 4-dimensional sum|M_R|^2 is compared with the note's FeynArts*)
(*model for Z -> mu- mu+ gamma and Z -> u ubar g (massless mu, u; the colour factor C_F of the gluon).*)
(*Writes results/ir_massless.csv.  Batch:  wolframscript -file ir_massless_feyncalc.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirIM$ = DirectoryName[$InputFileName];
resDirIM$ = FileNameJoin[{srcDirIM$, "results"}];
Quiet[CreateDirectory[resDirIM$]];

(* ::Section:: *)
(*Born and real emission in d dimensions*)

spinsum$[amp_, idx_] := Module[{x = FermionSpinSum[amp ComplexConjugate[amp /. Thread[idx -> (idx /. {mu -> nu, rho -> sig})]]]},
   x = x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
   Simplify[Contract[x (-MTD[mu, nu]) If[MemberQ[idx, rho], -MTD[rho, sig], 1]] /. D -> 4 - 2 eps]];
amp0$[gam_] := Spinor[Momentum[p1, D], 0].GAD[mu].gam.Spinor[-Momentum[p2, D], 0];
ampR$[gam_] := eQ Spinor[Momentum[p1, D], 0].(GAD[rho].GSD[p1 + p3].GAD[mu].gam/(MM y13) -
      GAD[mu].gam.GSD[p2 + p3].GAD[rho]/(MM y23)).Spinor[-Momentum[p2, D], 0];

(* two-body kinematics for the Born: p1.p2 = M^2/2 *)
FCClearScalarProducts[];
ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[p1, p2] = MM/2;
born$ = <|"V" -> spinsum$[amp0$[1], {mu}], "A" -> spinsum$[amp0$[GA5], {mu}]|>;
Print["Born sum|M0|^2 (the coupling of the current stripped): vector ", born$["V"], ",  axial ", born$["A"]];

(* three-body kinematics *)
FCClearScalarProducts[];
ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[p3, p3] = 0;
ScalarProduct[p1, p2] = MM y12/2; ScalarProduct[p1, p3] = MM y13/2; ScalarProduct[p2, p3] = MM y23/2;
real$ = <|"V" -> spinsum$[ampR$[1], {mu, rho}], "A" -> spinsum$[ampR$[GA5], {mu, rho}]|>;
rV$ = Simplify[MM real$["V"]/(eQ^2 born$["V"]) /. y12 -> 1 - y13 - y23];
rA$ = Simplify[MM real$["A"]/(eQ^2 born$["A"]) /. y12 -> 1 - y13 - y23];
Print["r = M^2 sum|M_R|^2/(e^2 Q^2 sum|M_0|^2): vector ", rV$];
Print["  vector minus axial (expect 0): ", Simplify[rV$ - rA$]];
(* the note's Appendix: 2 (x1^2 + x2^2 - eps x3^2)/((1 - x1)(1 - x2)), x1 = 1 - y23, x2 = 1 - y13, x3 = y13 + y23 *)
rNote$ = 2 ((1 - y23)^2 + (1 - y13)^2 - eps (y13 + y23)^2)/(y13 y23);
Print["  minus the note's 2(x1^2 + x2^2 - eps x3^2)/((1 - x1)(1 - x2)) (expect 0): ", Simplify[rV$ - rNote$]];

(* the same r as monomials in y12, y13, y23, for the Dirichlet integrals
   int dy13 dy23 y12^(a - 1) y13^(b - 1) y23^(c - 1) = Gamma(a) Gamma(b) Gamma(c)/Gamma(a + b + c) *)
rMono$ = 2 (y13/y23 + y23/y13 + 2 y12/(y13 y23) - eps (y13/y23 + y23/y13 + 2));
Print["  the monomial form equals it: ", Simplify[(rMono$ /. y12 -> 1 - y13 - y23) - rV$] === 0];
dirichlet$[expr_] := Module[{t = Expand[expr], terms},
   terms = If[Head[t] === Plus, List @@ t, {t}];
   Total[Function[term, Module[{c, e12, e13, e23},
        c = term /. {y12 -> 1, y13 -> 1, y23 -> 1};
        {e12, e13, e23} = Exponent[term, #] & /@ {y12, y13, y23};
        c Gamma[1 - eps + e12] Gamma[1 - eps + e13] Gamma[1 - eps + e23]/Gamma[3 - 3 eps + e12 + e13 + e23]]] /@ terms]];
(* Gamma_R/Gamma_0 = (e^2 Q^2 mu^(2 eps)/M^2) int dPhi3 r (y12 y13 y23)^(-eps) / int dPhi2,  divided by N(eps) *)
gR$ = FullSimplify[dirichlet$[rMono$] (MM/(2 (4 Pi)^3) (4 Pi/MM)^(2 eps)/Gamma[2 - 2 eps]) /
     ((4 Pi/MM)^eps Gamma[1 - eps]/(8 Pi Gamma[2 - 2 eps])) (16 Pi^2/MM) Gamma[1 - eps] (4 Pi/MM)^(-eps)];
Print["Gamma_R/(Gamma_0 N(eps)), exact: ", gR$];
serR$ = Expand[Normal[Series[gR$, {eps, 0, 0}]]];
Print["  expanded: ", serR$];

(* ::Section:: *)
(*Virtual correction in d dimensions*)

FCClearScalarProducts[];
ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[p1, p2] = MM/2;
(* ubar(p1) gamma^rho S(p1 - q) Gam^mu S(-p2 - q) gamma_rho v(p2) D_gamma(q): the factors (-i eQ)^2 i^2 (-i) = -i e^2 Q^2, and the
   measure mu^(2 eps) int d^Dq/(2 pi)^D = (i/(16 pi^2)) x [the TID result, which carries i pi^2 in front of the PaVe functions] *)
vtx$[gam_] := Spinor[Momentum[p1, D], 0].GAD[rho].(GSD[p1] - GSD[q]).GAD[mu].gam.(-GSD[p2] - GSD[q]).GAD[rho].Spinor[-Momentum[p2, D], 0] *
   FAD[q, q - p1, q + p2];
virt$[gam_] := Module[{x},
   x = FermionSpinSum[vtx$[gam] ComplexConjugate[amp0$[gam] /. mu -> nu]];
   x = x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
   x = Contract[x (-MTD[mu, nu])];
   Simplify[TID[x, q, ToPaVe -> True] /. {B0[0, 0, 0] -> 0, PaVe[0, {0}, {0, 0}] -> 0}]];
vV$ = virt$[1]; vA$ = virt$[GA5];
Print["TID (vector current): ", vV$];
Print["  vector minus axial (expect 0): ", Simplify[vV$ - vA$]];
(* B0 -> b0r ph with b0r = (4 pi w)^eps Gamma(eps) Gamma(1 - eps)^2/Gamma(2 - 2 eps), w = mu^2/M^2, ph = e^(i pi eps) *)
b0r$ = (4 Pi w)^eps Gamma[eps] Gamma[1 - eps]^2/Gamma[2 - 2 eps];
toExact$[x_] := x /. {B0[MM, 0, 0] -> b0r$ ph, C0[0, 0, MM, 0, 0, 0] -> 2 (D - 3)/((4 - D) MM) b0r$ ph,
      C0[0, MM, 0, 0, 0, 0] -> 2 (D - 3)/((4 - D) MM) b0r$ ph, C0[MM, 0, 0, 0, 0, 0] -> 2 (D - 3)/((4 - D) MM) b0r$ ph} /. D -> 4 - 2 eps;
Print["  PaVe functions left (expect {}): ", Union[Cases[toExact$[vV$], _B0 | _C0 | _PaVe, Infinity]]];
(* M1/M0 summed: [TID/(i pi^2)] (-i e^2 Q^2)(i/(16 pi^2))/sum|M0|^2 = (e^2 Q^2/(16 pi^2)) b0r ph kV *)
kV$ = Simplify[toExact$[vV$]/(I Pi^2)/born$["V"] (-I eQ^2) (I/(16 Pi^2))/((eQ^2/(16 Pi^2)) b0r$ ph)];
Print["  kV (expect a real rational function of eps): ", kV$];
(* Gamma_V/Gamma_0 = 2 Re(M0^* M1)/|M0|^2 = 2 (e^2 Q^2/(16 pi^2)) b0r Re(kV e^(i pi eps)),  divided by N(eps) *)
gV$ = FullSimplify[2 ComplexExpand[Re[kV$ Exp[I Pi eps]]] Gamma[eps] Gamma[1 - eps]^3/Gamma[2 - 2 eps],
   Assumptions -> eps > 0 && eps < 1/2];
Print["Gamma_V/(Gamma_0 N(eps)), exact: ", gV$];
serV$ = Expand[Normal[Series[gV$, {eps, 0, 0}]]];
Print["  expanded: ", serV$];

(* ::Section:: *)
(*The sum*)

serSum$ = Simplify[Normal[Series[gR$ + gV$, {eps, 0, 1}]]];
Print["(Gamma_R + Gamma_V)/(Gamma_0 N(eps)) to O(eps): ", serSum$, "   (expect 3 + O(eps): N 3 = (3/4) alpha C/pi)"];
(* the note's Eq. (irexact), in units of (alpha C/(2 pi)) (4 pi mu^2/M^2)^eps: these over 2 Gamma(1 - eps) *)
noteR$ = 6 (1 - eps) (1 - 2 eps) (2 - 2 eps + eps^2) Gamma[1 - eps]^2/(eps^2 Gamma[4 - 3 eps]);
noteV$ = -(2 - eps + 2 eps^2) Gamma[1 + eps] Gamma[1 - eps]^2 Cos[Pi eps]/(eps^2 Gamma[2 - 2 eps]);
diffNote$ = FullSimplify[FunctionExpand[{gR$/(2 Gamma[1 - eps]) - noteR$, gV$/(2 Gamma[1 - eps]) - noteV$}]];
Print["the note's Eq. (irexact) minus the above, real and virtual (expect 0): ", diffNote$, ";  at eps = 0.123, 0.37: ",
  N[{gR$/(2 Gamma[1 - eps]) - noteR$, gV$/(2 Gamma[1 - eps]) - noteV$} /. eps -> # & /@ {123/1000, 37/100}, 20]];

(* ::Section:: *)
(*The 4-dimensional sum|M_R|^2 against the note's FeynArts model*)

tmpIM$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirIM$, "generated", "SM_CKM_FA"}], FileNameJoin[{tmpIM$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{tmpIM$, "SM_CKM_FA"}], Quiet -> True];
modelIM$ = FileNameJoin[{tmpIM$, "SM_CKM_FA", "SM_CKM_FA"}];
convIM$ = {FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["MZ"] -> MZ, FCGV["MW"] -> MW,
   FCGV["MMU"] -> 0, FCGV["MU"] -> 0, MMU -> 0, MU -> 0};
fa3$[out_] := Module[{d, a, x},
   d = Quiet[InsertFields[CreateTopologies[0, 1 -> 3], {V[2]} -> out, InsertionLevel -> {Particles},
       Model -> modelIM$, GenericModel -> modelIM$], RuleDelayed::rhs];
   a = Quiet[FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {k}, OutgoingMomenta -> {p1, p2, p3},
       ChangeDimension -> 4, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> True,
       TransversePolarizationVectors -> {}], RuleDelayed::rhs] /. convIM$;
   Print["   ", Length[a], " diagrams"];
   FCClearScalarProducts[];
   ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[p3, p3] = 0; ScalarProduct[k, k] = MZ^2;
   ScalarProduct[p1, p2] = MZ^2 y12/2; ScalarProduct[p1, p3] = MZ^2 y13/2; ScalarProduct[p2, p3] = MZ^2 y23/2;
   ScalarProduct[k, p1] = MZ^2 (y12 + y13)/2; ScalarProduct[k, p2] = MZ^2 (y12 + y23)/2; ScalarProduct[k, p3] = MZ^2 (y13 + y23)/2;
   x = FermionSpinSum[ComplexConjugate[Total[a]] Total[a], ExtraFactor -> 1];
   x = x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
   x = DoPolarizationSums[x, k];
   x = DoPolarizationSums[x, p3, 0, VirtualBoson -> True];
   x = Contract[FeynAmpDenominatorExplicit[SUNSimplify[DiracSimplify[x], SUNNToCACF -> False]]] /. SUNN -> 3;
   Simplify[x /. y12 -> 1 - y13 - y23 /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}]];
(* the hand value: N_c C (g_Z/2)^2 (v^2 + a^2) sum|M0|^2 (coupling^2/M^2) r, with sum|M0|^2 = 4 M^2 in 4 dimensions *)
s2IM$ = 1 - MW^2/MZ^2; gZIM$ = ee/Sqrt[s2IM$ (1 - s2IM$)];
r4$ = rV$ /. eps -> 0;
hand3$[nc_, c_, cpl_, t3_, q_] := nc c (gZIM$/2)^2 ((t3 - 2 q s2IM$)^2 + t3^2) 4 MZ^2 cpl^2 r4$/MZ^2;
Print["Z -> mu- mu+ gamma:"];
dMu$ = Simplify[fa3$[{F[2, {2}], -F[2, {2}], V[1]}] - hand3$[1, 1, ee, -1/2, -1]];
Print["   FeynArts model minus hand (expect 0): ", dMu$];
Print["Z -> u ubar g:"];
dU$ = Simplify[fa3$[{F[3, {1}], -F[3, {1}], V[4]}] - hand3$[3, 4/3, gS, 1/2, 2/3]];
Print["   FeynArts model minus hand, with C_F = 4/3 (expect 0): ", dU$];
DeleteDirectory[tmpIM$, DeleteContents -> True];

Export[FileNameJoin[{resDirIM$, "ir_massless.csv"}], {{"quantity", "value"},
   {"r_minus_note_appendix", ToString[InputForm[Simplify[rV$ - rNote$]]]},
   {"real_over_N_exact", ToString[InputForm[gR$]]}, {"virtual_over_N_exact", ToString[InputForm[gV$]]},
   {"real_over_N_series", ToString[InputForm[serR$]]}, {"virtual_over_N_series", ToString[InputForm[serV$]]},
   {"sum_over_N_to_O_eps", ToString[InputForm[serSum$]]}, {"note_irexact_minus_computed", ToString[InputForm[diffNote$]]},
   {"model_minus_hand_Z_mumugamma", ToString[InputForm[dMu$]]}, {"model_minus_hand_Z_uug", ToString[InputForm[dU$]]}}, "CSV"];
Print["written: results/ir_massless.csv"];
