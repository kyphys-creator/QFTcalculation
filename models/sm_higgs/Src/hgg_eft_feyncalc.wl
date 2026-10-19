(* ::Package:: *)

(* ::Title:: *)
(*Step (6) of the Higgs note: H -> g g at NLO QCD in the heavy-top effective theory, exact in d = 4 - 2 eps*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (6).  The FeynArts model of SM_CKM.fr with the operator -(1/4) cHgg (H/vev) G G*)
(*(generated/SM_CKM_HEFT_FA, generate_HggEFT.wl), only gluons, their ghosts and the light quarks (massless, so that their Yukawa*)
(*vertices vanish) in the diagrams; everything in d dimensions (FeynCalc), the gluon polarization sums physical (reference*)
(*vectors: another gluon's momentum).*)
(*  Born:    H -> g(p1) g(p2), sum|M0|^2;*)
(*  Real:    H -> g g g (contact H g g g and H g g + g g g) and H -> g q qbar for one massless flavour, in y_ij = s_ij/M^2, the*)
(*           Dirichlet integrals of the d-dimensional three-body phase space, with 1/3! for the three gluons against 1/2! of the*)
(*           Born and no factor for g q qbar;*)
(*  Virtual: the one-loop H -> g g of the operator (gluon loops; the external self-energies are scaleless, 0), TID to*)
(*           B0(M^2, 0, 0) and C0(0, 0, M^2, 0, 0, 0) in their exact forms (the NLO note's ir_massless_feyncalc.wl);*)
(*  Counterterm: the MS-bar alpha_s in cHgg = -(alpha_s/(3 pi))(...): 2 d alpha_s/alpha_s = -2 beta0 (alpha_s/(4 pi)) S_eps/eps,*)
(*           beta0 = (11/3) C_A - (4/3) T_F N_F (the product alpha_s G G is finite at this order).*)
(*In units of N(eps) = (alpha_s/(4 pi)) (4 pi mu^2/M^2)^eps/Gamma(1 - eps) the sum must have no poles; its eps^0 term, against the*)
(*heavy-top literature (Spira et al.; a reference): 4 [73/4 - (7/6) N_F + (beta0/2) ln(mu^2/M^2)] = 73 - (14/3) N_F + 2 beta0 ln w;*)
(*with the Wilson coefficient's 2 (11/4) it becomes Eq. (hgg).  The 4-dimensional real |M|^2 against the known forms*)
(*(M^8 + s12^4 + s13^4 + s23^4)/(s12 s13 s23) and (s12^2 + s13^2)/s23.  Writes results/hgg_eft.csv and work/me_hgg.txt (CForm of*)
(*the 4-dimensional sums for hgg_mg5.py).  Batch:  wolframscript -file hgg_eft_feyncalc.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirHE$ = DirectoryName[$InputFileName];
resDirHE$ = FileNameJoin[{srcDirHE$, "results"}];
workDirHE$ = FileNameJoin[{srcDirHE$, "work"}];
t0HE$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0HE$], " s] ", s];
modelTmpHE$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirHE$, "generated", "SM_CKM_HEFT_FA"}], FileNameJoin[{modelTmpHE$, "SM_CKM_HEFT_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpHE$, "SM_CKM_HEFT_FA"}], Quiet -> True];
modelHE$ = FileNameJoin[{modelTmpHE$, "SM_CKM_HEFT_FA", "SM_CKM_HEFT_FA"}];
(* only QCD: no photon, Z, W, Goldstones, electroweak ghosts, leptons, top *)
exclHE$ = {V[1], V[2], V[3], S[2], S[3], U[1], U[2], U[3], U[4], F[1], F[2], F[3, {3}]};
convHE$ = {FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS, FCGV["EL"] -> ee, FCGV["MH"] -> MH, FCGV["MW"] -> MW, FCGV["MZ"] -> MZ,
   GaugeXi[V[4, ___]] -> 1, GaugeXi[U[5, ___]] -> 1, GaugeXi[G] -> 1, MU -> 0, MD -> 0, MS -> 0, MC -> 0, MB -> 0,
   FCGV["MU"] -> 0, FCGV["MD"] -> 0, FCGV["MS"] -> 0, FCGV["MC"] -> 0, FCGV["MB"] -> 0};
yukHE$ = {yl[__] -> 0, yu[__] -> 0, yd[__] -> 0};
ampHE$[d_, in_, out_, loop_] := Module[{a},
   a = Quiet[FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out,
       LoopMomenta -> loop, ChangeDimension -> D, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> True,
       TransversePolarizationVectors -> out], RuleDelayed::rhs];
   a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}] /. convHE$ /. yukHE$ /. vev -> 2 MW sw/ee];
insHE$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelHE$, GenericModel -> modelHE$,
    ExcludeParticles -> exclHE$], RuleDelayed::rhs];
colHE$[x_] := SUNSimplify[x, SUNNToCACF -> True];
trHE$[x_] := x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];

(* ::Section:: *)
(*Born*)

FCClearScalarProducts[];
SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[p1, p2] = MM/2;
born0$ = ampHE$[insHE$[CreateTopologies[0, 1 -> 2], {S[1]} -> {V[4], V[4]}], {k}, {p1, p2}, {}];
born0$ = FCReplaceMomenta[#, {k -> p1 + p2}] & /@ born0$;
Print["Born: ", Length[born0$], " diagram"];
sqHE$[a_, b_, pols_] := Module[{x = (Total[a] ComplexConjugate[Total[b]])},
   x = FermionSpinSum[x, ExtraFactor -> 1];
   x = trHE$[x];
   Do[x = DoPolarizationSums[x, pp[[1]], pp[[2]]], {pp, pols}];
   x = colHE$[Contract[FeynAmpDenominatorExplicit[x]]];
   Simplify[ExpandScalarProduct[x] /. D -> 4 - 2 eps]];
bornSq$ = sqHE$[born0$, born0$, {{p1, p2}, {p2, p1}}];
Print["Born sum|M0|^2: ", bornSq$];
tick$["Born"];

(* ::Section:: *)
(*Real emission*)

FCClearScalarProducts[];
SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[p3, p3] = 0;
SPD[p1, p2] = MM y12/2; SPD[p1, p3] = MM y13/2; SPD[p2, p3] = MM y23/2;
realGGG$ = ampHE$[insHE$[CreateTopologies[0, 1 -> 3], {S[1]} -> {V[4], V[4], V[4]}], {k}, {p1, p2, p3}, {}];
realGGG$ = FCReplaceMomenta[#, {k -> p1 + p2 + p3}] & /@ realGGG$;
Print["H -> g g g: ", Length[realGGG$], " diagrams"];
sqGGG$ = sqHE$[realGGG$, realGGG$, {{p1, p2}, {p2, p3}, {p3, p1}}];
tick$["H -> g g g squared"];
realGQQ$ = ampHE$[insHE$[CreateTopologies[0, 1 -> 3], {S[1]} -> {V[4], F[3, {1}], -F[3, {1}]}], {k}, {p1, p2, p3}, {}];
realGQQ$ = FCReplaceMomenta[#, {k -> p1 + p2 + p3}] & /@ realGQQ$;
Print["H -> g u ubar: ", Length[realGQQ$], " diagrams"];
sqGQQ$ = sqHE$[realGQQ$, realGQQ$, {{p1, p2}}];
tick$["H -> g u ubar squared"];
(* r = M^2 sum|M_R|^2/(g_s^2 sum|M0|^2), with y12 + y13 + y23 = 1 kept implicit (monomials) *)
rOf$[sq_] := Together[MM sq/(gS^2 bornSq$)];
rGGG$ = rOf$[sqGGG$]; rGQQ$ = rOf$[sqGQQ$];
Print["r(g g g) denominator: ", Factor[Denominator[rGGG$]], ";  r(g q qbar) denominator: ", Factor[Denominator[rGQQ$]]];
(* the 4-dimensional forms: proportional to (1 + y12^4 + y13^4 + y23^4)/(y12 y13 y23) and (y12^2 + y13^2)/y23 *)
onShell3$ = {y12 -> 1 - y13 - y23};
Print["4d: r(g g g) y12 y13 y23/(1 + y12^4 + y13^4 + y23^4) = ",
  Simplify[(rGGG$ /. eps -> 0) y12 y13 y23/(1 + y12^4 + y13^4 + y23^4) /. onShell3$],
  ";  r(g q qbar) y23/(y12^2 + y13^2) = ", Simplify[(rGQQ$ /. eps -> 0) y23/(y12^2 + y13^2) /. onShell3$]];
dirichlet$[expr_] := Module[{t = Expand[expr], terms},
   terms = If[Head[t] === Plus, List @@ t, {t}];
   Total[Function[term, Module[{c, e12, e13, e23},
        c = term /. {y12 -> 1, y13 -> 1, y23 -> 1};
        {e12, e13, e23} = Exponent[term, #] & /@ {y12, y13, y23};
        If[! FreeQ[c, y12 | y13 | y23], Print["   WARNING: not a monomial: ", term]];
        c Gamma[1 - eps + e12] Gamma[1 - eps + e13] Gamma[1 - eps + e23]/Gamma[3 - 3 eps + e12 + e13 + e23]]] /@ terms]];
psRatio$ = (MM/(2 (4 Pi)^3) (4 Pi/MM)^(2 eps)/Gamma[2 - 2 eps])/((4 Pi/MM)^eps Gamma[1 - eps]/(8 Pi Gamma[2 - 2 eps])) *
   (16 Pi^2/MM) Gamma[1 - eps] (4 Pi/MM)^(-eps);
monomials$[r_] := Expand[Numerator[r]/Denominator[r]];
gRggg$ = FullSimplify[(1/3) dirichlet$[monomials$[rGGG$]] psRatio$];
gRgqq$ = FullSimplify[2 dirichlet$[monomials$[rGQQ$]] psRatio$];
Print["Gamma_R(g g g)/(Gamma_0 N), exact: ", gRggg$];
Print["Gamma_R(g q qbar)/(Gamma_0 N) per flavour, exact: ", gRgqq$];
serRggg$ = Expand[Normal[Series[gRggg$, {eps, 0, 0}]]]; serRgqq$ = Expand[Normal[Series[gRgqq$, {eps, 0, 0}]]];
Print["  expanded: g g g ", serRggg$, ";  g q qbar ", serRgqq$];
tick$["real"];

(* ::Section:: *)
(*Virtual correction*)

FCClearScalarProducts[];
SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[p1, p2] = MM/2;
virtD$ = insHE$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], {S[1]} -> {V[4], V[4]}];
virtA$ = ampHE$[virtD$, {k}, {p1, p2}, {q}];
virtA$ = FCReplaceMomenta[#, {k -> p1 + p2}] & /@ virtA$;
(* the order cHgg g_s^2 only: the diagrams with two operator vertices (an internal H) are another order *)
nV2$ = Count[virtA$, x_ /; ! FreeQ[x, cHgg^2]];
virtA$ = DeleteCases[Expand[#] /. cHgg^n_ /; n > 1 -> 0 & /@ virtA$, 0];
Print["virtual: ", Length[virtA$], " diagrams of the order cHgg (", nV2$, " of the order cHgg^2 dropped)"];
redV$[x_] := Module[{r = x},
   r = colHE$[r];
   r = FDS[r, q];
   r = TID[r, q, ToPaVe -> True];
   r /. {B0[0, 0, 0] -> 0, A0[0] -> 0, PaVe[0, {0}, {0, 0}] -> 0}];
virtR$ = redV$ /@ virtA$;
tick$["virtual reduced"];
(* 2 Re(M0^* M1): the interference with the polarization sums *)
intV$ = Module[{x = Total[virtR$] ComplexConjugate[Total[born0$]]},
   x = DoPolarizationSums[x, p1, p2]; x = DoPolarizationSums[x, p2, p1];
   x = colHE$[Contract[x]];
   Simplify[ExpandScalarProduct[x]]];
Print["  PaVe functions: ", Union[Cases[intV$, _B0 | _C0 | _PaVe | _A0, Infinity]]];
b0r$ = (4 Pi w)^eps Gamma[eps] Gamma[1 - eps]^2/Gamma[2 - 2 eps];
toExact$[x_] := x /. {B0[MM, 0, 0] -> b0r$ ph, C0[0, 0, MM, 0, 0, 0] -> 2 (D - 3)/((4 - D) MM) b0r$ ph,
      C0[0, MM, 0, 0, 0, 0] -> 2 (D - 3)/((4 - D) MM) b0r$ ph, C0[MM, 0, 0, 0, 0, 0] -> 2 (D - 3)/((4 - D) MM) b0r$ ph} /. D -> 4 - 2 eps;
(* the ratio M1/M0 summed, with the loop measure of FCFAConvert and TID: written as (g_s^2/(16 pi^2)) b0r ph k, k a function of eps *)
kV$ = Simplify[toExact$[intV$]/(bornSq$ /. eps -> eps) /((gS^2/(16 Pi^2)) b0r$ ph)];
Print["  k (expect a rational function of eps; the loop measure's normalization shows here): ", kV$];
tick$["virtual"];
gV$ = FullSimplify[2 ComplexExpand[Re[kV$ Exp[I Pi eps]]] Gamma[eps] Gamma[1 - eps]^3/Gamma[2 - 2 eps], Assumptions -> eps > 0 && eps < 1/2];
Print["Gamma_V/(Gamma_0 N), exact: ", gV$];
serV$ = Expand[Normal[Series[gV$, {eps, 0, 0}]]];
Print["  expanded: ", serV$];

(* ::Section:: *)
(*The sum*)

(* the MS-bar alpha_s of cHgg: 2 d alpha_s/alpha_s over N, beta0 = (11/3) C_A - (4/3) T_F N_F *)
beta0$ = 11/3 CA - 4/3 TF nF;
gCT$ = -2 beta0$ Exp[-EulerGamma eps] Gamma[1 - eps] wR^(-eps)/eps;
(* T_F = 1/2 is in the colour algebra of g q qbar: its per-flavour value times nF is the T_F N_F part *)
sum$ = gRggg$ + nF gRgqq$ + gV$ + gCT$ /. TF -> 1/2;
serSum$ = Simplify[Normal[Series[sum$, {eps, 0, 1}]]];
Print["(Gamma_R + Gamma_V + counterterm)/(Gamma_0 N) to O(eps): ", serSum$];
fin$ = Simplify[serSum$ /. eps -> 0];
Print["  at eps = 0: ", fin$, ";  minus 4 [73/4 - (7/6) N_F + (beta0/2) ln w] at C_A = 3 (expect 0): ",
  Simplify[(fin$ /. CA -> 3) - 4 (73/4 - 7/6 nF + (11 - 2/3 nF)/2 Log[wR])]];
Print["  in units of alpha_s/pi (divide by 4), with C_A: ", Collect[Expand[fin$/4], {nF, Log[wR]}],
  ";  with the Wilson coefficient 2 (11/4) and N_F = 5 at mu = M_H: ", (fin$/4 /. {CA -> 3, nF -> 5, wR -> 1}) + 11/2,
  " = 95/4 - 35/6 = ", 95/4 - 35/6];
Export[FileNameJoin[{resDirHE$, "hgg_eft.csv"}], {{"quantity", "value"},
   {"born", ToString[InputForm[bornSq$]]}, {"r_ggg", ToString[InputForm[Simplify[rGGG$ /. onShell3$]]]},
   {"r_gqq", ToString[InputForm[Simplify[rGQQ$ /. onShell3$]]]},
   {"real_ggg_over_N_exact", ToString[InputForm[gRggg$]]}, {"real_gqq_over_N_exact_per_flavour", ToString[InputForm[gRgqq$]]},
   {"virtual_over_N_exact", ToString[InputForm[gV$]]}, {"real_ggg_series", ToString[InputForm[serRggg$]]},
   {"real_gqq_series", ToString[InputForm[serRgqq$]]}, {"virtual_series", ToString[InputForm[serV$]]},
   {"sum_over_N_to_O_eps", ToString[InputForm[serSum$]]}, {"sum_over_N_eps0", ToString[InputForm[fin$]]}}, "CSV"];
(* the 4-dimensional sums for MadGraph: sum|M_R|^2 in s12, s13 at eps = 0 (y -> s/MM, y12 = (MM - s13 - s23)/MM) *)
Export[FileNameJoin[{workDirHE$, "me_hgg.txt"}], StringRiffle[{
    "GGG|" <> ToString[CForm[Simplify[(sqGGG$ /. eps -> 0) /. {y12 -> s12/MM, y13 -> s13/MM, y23 -> (MM - s12 - s13)/MM}]]],
    "GQQ|" <> ToString[CForm[Simplify[(sqGQQ$ /. eps -> 0) /. {y12 -> s12/MM, y13 -> s13/MM, y23 -> (MM - s12 - s13)/MM}]]]}, "\n"] <> "\n",
  "Text"];
Put[<|"born" -> bornSq$, "rGGG" -> rGGG$, "rGQQ" -> rGQQ$, "gRggg" -> gRggg$, "gRgqq" -> gRgqq$, "intV" -> intV$, "kV" -> kV$, "gV" -> gV$,
   "sum" -> serSum$|>, FileNameJoin[{workDirHE$, "hgg_eft.m"}]];
Print["written: results/hgg_eft.csv, work/me_hgg.txt, work/hgg_eft.m"];
DeleteDirectory[modelTmpHE$, DeleteContents -> True];
