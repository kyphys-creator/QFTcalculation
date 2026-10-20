(* ::Package:: *)

(* ::Title:: *)
(*Step (2a): g g -> H at O(alpha_s) in the heavy-top effective theory in D dimensions -- the MS-bar coefficient functions Delta_gg, Delta_qg, Delta_qqbar (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm_pp, step (2a).  The FeynArts model of the Higgs note (SM_CKM.fr with the operator -(1/4) cHgg (H/vev) G G,*)
(*models/sm_higgs/Src/generated/SM_CKM_HEFT_FA), only gluons, their ghosts and the five light quarks (massless, no Yukawa), D = 4 - 2 eps,*)
(*the gluon polarization sums physical (reference vector: another gluon's or quark's momentum).  As for Drell-Yan (dy_feyncalc.wl),*)
(*  sigma_ij(shat) = sigma_0 z Delta_ij(z),  z = M_H^2/shat,  Delta = delta_ig delta_jg delta(1 - z) + a_s Delta^(1) + ...,  a_s = alpha_s/(4 pi)*)
(*(the literature's Delta is z Delta),*)
(*sigma_0 the LO g g -> H at shat = M_H^2 (in the theory with cHgg; cHgg = -(alpha_s/(3 pi)) C1 in the note's numbers).*)
(*  Real:    g g -> H g (s, t, u-channel gluon and the contact g g g H vertex), q g -> H q, q qbar -> H g; r = M_H^2 [avg |M_R|^2]/(g_s^2 [avg|M_0|^2])*)
(*           with D - 2 gluon polarizations; Delta_R/a_s = e^(eps gamma)/Gamma(1 - eps) (mu_R^2/M_H^2)^eps z^eps (1 - z)^(1 - 2 eps) int dv [v(1 - v)]^-eps r.*)
(*  Virtual: the one-loop g g -> H of the operator (gluon and ghost loops; massless self-energies are scaleless), as the Higgs note's*)
(*           step (6) for H -> g g (the same timelike q^2 = M_H^2), 2 Re F^(1) delta(1 - z).*)
(*  UV:      cHgg is proportional to alpha_s: the MS-bar counterterm 2 delta alpha_s/alpha_s = -2 beta0 a_s/eps, beta0 = 11 - (2/3) n_f*)
(*           (alpha_s G G is finite at this order).*)
(*  Collinear: (alpha_s/(2 pi))(1/eps)(mu_R^2/mu_F^2)^eps times 2 P_gg (g g), P_gq (q g: the quark radiates the gluon that makes H);*)
(*           q qbar has no collinear singularity.*)
(*The sum has no poles; Delta^(1) against the literature (Dawson; Djouadi, Spira, Zerwas; the form of Harlander and Kilgore, a*)
(*reference).  The 4-dimensional sum|M_R|^2 against the known forms.  Writes results/gh_feyncalc.csv.*)
(*How to run.  Batch:  wolframscript -file gh_feyncalc.wl  (about 3 minutes).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirGH$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirGH$ = FileNameJoin[{srcDirGH$, "results"}];
Quiet[CreateDirectory[resDirGH$]];
t0GH$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0GH$], " s] ", s];
$Assumptions = 0 < z < 1 && 0 < v < 1 && MM > 0;
modelTmpGH$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirGH$, "..", "..", "sm_higgs", "Src", "generated", "SM_CKM_HEFT_FA"}], FileNameJoin[{modelTmpGH$, "SM_CKM_HEFT_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpGH$, "SM_CKM_HEFT_FA"}], Quiet -> True];
modelGH$ = FileNameJoin[{modelTmpGH$, "SM_CKM_HEFT_FA", "SM_CKM_HEFT_FA"}];
(* only QCD and the operator: no photon, Z, W, Goldstones, electroweak ghosts, leptons, top *)
exclGH$ = {V[1], V[2], V[3], S[2], S[3], U[1], U[2], U[3], U[4], F[1], F[2], F[3, {3}]};
convGH$ = {FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS, FCGV["EL"] -> ee, FCGV["MH"] -> MH, FCGV["MW"] -> MW, FCGV["MZ"] -> MZ,
   GaugeXi[V[4, ___]] -> 1, GaugeXi[U[5, ___]] -> 1, GaugeXi[G] -> 1, MU -> 0, MD -> 0, MS -> 0, MC -> 0, MB -> 0,
   FCGV["MU"] -> 0, FCGV["MD"] -> 0, FCGV["MS"] -> 0, FCGV["MC"] -> 0, FCGV["MB"] -> 0};
yukGH$ = {yl[__] -> 0, yu[__] -> 0, yd[__] -> 0};
ampGH$[d_, in_, out_, loop_, pols_] := Module[{a},
   a = Quiet[FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out,
       LoopMomenta -> loop, ChangeDimension -> D, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> True,
       TransversePolarizationVectors -> pols], RuleDelayed::rhs];
   a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}] /. convGH$ /. yukGH$ /. vev -> 2 MW sw/ee];
insGH$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelGH$, GenericModel -> modelGH$,
    ExcludeParticles -> exclGH$], RuleDelayed::rhs];
colGH$[x_] := SUNSimplify[x, SUNNToCACF -> True] /. {CA -> 3, CF -> 4/3};
trGH$[x_] := x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
(* sum over spins, polarizations (pols: {momentum, reference}) and colours of a b^* *)
sqGH$[a_, b_, pols_] := Module[{x = (Total[a] ComplexConjugate[Total[b]])},
   x = FermionSpinSum[x, ExtraFactor -> 1];
   x = trGH$[x];
   Do[x = DoPolarizationSums[x, pp[[1]], pp[[2]]], {pp, pols}];
   x = colGH$[Contract[FeynAmpDenominatorExplicit[x]]];
   Simplify[ExpandScalarProduct[x] /. D -> 4 - 2 eps]];
dropCC$[amps_] := DeleteCases[Expand[#] /. cHgg^n_ /; n > 1 -> 0 & /@ amps, 0];


(* ::Section:: *)
(*(a) Born*)


FCClearScalarProducts[];
SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[p1, p2] = MM/2;
born$ = ampGH$[insGH$[CreateTopologies[0, 2 -> 1], {V[4], V[4]} -> {S[1]}], {p1, p2}, {q}, {}, {p1, p2}];
born$ = FCReplaceMomenta[#, {q -> p1 + p2}] & /@ born$;
bornSq$ = sqGH$[born$, born$, {{p1, p2}, {p2, p1}}];
Print["(a) g g -> H: ", Length[born$], " diagram;  sum|M0|^2 = ", InputForm[bornSq$]];
tick$["Born"];


(* ::Section:: *)
(*(b) the real emission in D dimensions*)


(* in -> H(q) + parton(k); t = (p1 - k)^2, u = (p2 - k)^2, shat + t + u = M_H^2 *)
kin2$[] := (FCClearScalarProducts[];
   SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[k, k] = 0;
   SPD[p1, p2] = sh/2; SPD[p1, k] = -t/2; SPD[p2, k] = -u/2);
real$[in_, out_, pols_, tpol_] := Module[{a},
   kin2$[];
   a = dropCC$[ampGH$[insGH$[CreateTopologies[0, 2 -> 2], in -> out], {p1, p2}, {q, k}, {}, tpol]];
   a = FCReplaceMomenta[#, {q -> p1 + p2 - k}] & /@ a;
   {Length[a], sqGH$[a, a, pols] /. MM -> sh + t + u}];
{nGG$, sqGG$} = real$[{V[4], V[4]}, {S[1], V[4]}, {{p1, p2}, {p2, p1}, {k, p1}}, {p1, p2, k}];
tick$["g g -> H g"];
{nQG$, sqQG$} = real$[{F[3, {1}], V[4]}, {S[1], F[3, {1}]}, {{p2, p1}}, {p2}];
tick$["q g -> H q"];
{nQQ$, sqQQ$} = real$[{F[3, {1}], -F[3, {1}]}, {S[1], V[4]}, {{k, p1}}, {k}];
tick$["q qbar -> H g"];
Print["(b) diagrams: g g -> H g ", nGG$, ", q g -> H q ", nQG$, ", q qbar -> H g ", nQQ$];
(* r = M_H^2 [avg|M_R|^2]/(g_s^2 [avg|M_0|^2(shat = M_H^2)]): averages g g 1/(4 (1 - eps)^2 64), q g 1/(2 2 (1 - eps) 3 8), q qbar 1/(4 9) *)
zvGH$ = {t -> -sh (1 - z) v, u -> -sh (1 - z) (1 - v)};
rOf$[sq_, avg_] := Factor[MM avg sq/(gS^2 bornSq$) /. zvGH$ /. sh -> MM/z];
rGG$ = rOf$[sqGG$, 1];
rQG$ = rOf$[sqQG$, (4 (1 - eps)^2 64)/(4 (1 - eps) 24)];
rQQ$ = rOf$[sqQQ$, (4 (1 - eps)^2 64)/36];
Print["(b) r_gg = ", InputForm[rGG$]];
Print["(b) r_qg = ", InputForm[rQG$]];
Print["(b) r_qqbar = ", InputForm[rQQ$]];
(* 4 dimensions: sum|M|^2 proportional to (M^8 + s^4 + t^4 + u^4)/(s t u), -(s^2 + u^2)/t, (t^2 + u^2)/s *)
chk4$ = Simplify[{(sqGG$ /. eps -> 0) sh t u/((sh + t + u)^4 + sh^4 + t^4 + u^4), (sqQG$ /. eps -> 0) t/(sh^2 + u^2),
    (sqQQ$ /. eps -> 0) sh/(t^2 + u^2)}];
Print["(b) 4-dimensional sum|M_R|^2 over the known forms (expect constants): ", InputForm[chk4$]];
tick$["real ratios"];


(* ::Section:: *)
(*(c) the phase-space integrals and the plus distributions*)


vTermGH$[x_] := Which[
   FreeQ[x, v], x Gamma[1 - eps]^2/Gamma[2 - 2 eps],
   MatchQ[x, c_. v^n_. /; FreeQ[c, v]], x /. c_. v^n_. :> c Gamma[n + 1 - eps] Gamma[1 - eps]/Gamma[n + 2 - 2 eps],
   MatchQ[x, c_. (-1 + v)^m_. /; FreeQ[c, v]], x /. c_. (-1 + v)^m_. :> c (-1)^m Gamma[1 - eps] Gamma[m + 1 - eps]/Gamma[m + 2 - 2 eps],
   True, Print["vTerm: ", x]; Abort[]];
vIntGH$[x_] := Module[{e = Expand[Apart[Together[x], v]]}, Total[vTermGH$ /@ If[Head[e] === Plus, List @@ e, {e}]]];
normGH$ = E^(eps EulerGamma)/Gamma[1 - eps] E^(eps lR) z^eps;
serGH$[x_, n_] := Normal[Series[x, {eps, 0, n}]];
plusGH$[c_, k_] := Module[{c1 = Simplify[c /. z -> 1]}, c1 If[k == 0, pl0, pl1] + Simplify[(c - c1) If[k == 0, 1/(1 - z), Log[1 - z]/(1 - z)]]];
plusExpGH$[x_, k_] := Module[{cs = Collect[Expand[x], eps, Simplify]}, Sum[plusGH$[Coefficient[cs, eps, n], k] eps^n, {n, -1, 0}]];
(* (1 - z)^(-1 - 2 eps) H(z, eps), H regular at z = 1 *)
distGH$[h_] := Collect[Expand[serGH$[-(h /. z -> 1)/(2 eps), 0] dlt + plusExpGH$[serGH$[h, 0], 0] - 2 eps plusExpGH$[serGH$[h, -1], 1]],
   {eps, dlt, pl0, pl1}, Simplify];
hGG$ = Simplify[normGH$ vIntGH$[Cancel[(1 - z)^2 rGG$]]];
Print["(c) H_gg(1, eps) = ", InputForm[FullSimplify[hGG$ /. z -> 1]]];
realGG$ = distGH$[hGG$];
(* q g, q qbar: at most (1 - z)^(-1) times (1 - z)^(1 - 2 eps): check that (1 - z) times the integrand vanishes at z = 1 *)
iQG$ = Simplify[vIntGH$[rQG$]]; iQQ$ = Simplify[vIntGH$[rQQ$]];
Print["(c) (1 - z)^(2 - 2 eps) x v-integral at z -> 1, q g and q qbar (expect 0, 0): ",
  Simplify[{Limit[(1 - z)^2 iQG$ /. eps -> -1/10, z -> 1], Limit[(1 - z)^2 iQQ$ /. eps -> -1/10, z -> 1]}]];
realQG$ = Collect[serGH$[normGH$ (1 - z)^(1 - 2 eps) iQG$, 0], eps, Simplify];
realQQ$ = Collect[serGH$[normGH$ (1 - z)^(1 - 2 eps) iQQ$, 0], eps, Simplify];
Print["(c) Delta_R,gg/a_s = ", InputForm[realGG$]];
Print["(c) Delta_R,qg/a_s = ", InputForm[realQG$]];
Print["(c) Delta_R,qqbar/a_s = ", InputForm[realQQ$]];
tick$["phase space"];


(* ::Section:: *)
(*(d) the virtual correction*)


FCClearScalarProducts[];
SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[p1, p2] = MM/2;
virtD$ = insGH$[CreateTopologies[1, 2 -> 1, ExcludeTopologies -> {Tadpoles, WFCorrections}], {V[4], V[4]} -> {S[1]}];
virtA$ = ampGH$[virtD$, {p1, p2}, {q}, {l}, {p1, p2}];
virtA$ = FCReplaceMomenta[#, {q -> p1 + p2}] & /@ virtA$;
nVall$ = Length[virtA$];
virtA$ = dropCC$[virtA$];
Print["(d) virtual: ", Length[virtA$], " diagrams of the order cHgg g_s^2 (of ", nVall$, ")"];
redV$[x_] := Module[{r = x},
   r = colGH$[r]; r = FDS[r, l]; r = TID[r, l, ToPaVe -> True];
   r /. {B0[0, 0, 0] -> 0, A0[0] -> 0, PaVe[0, {0}, {0, 0}] -> 0}];
virtR$ = redV$ /@ virtA$;
intV$ = Module[{x = Total[virtR$] ComplexConjugate[Total[born$]]},
   x = DoPolarizationSums[x, p1, p2]; x = DoPolarizationSums[x, p2, p1];
   x = colGH$[Contract[x]];
   Simplify[ExpandScalarProduct[x]]];
Print["(d) PaVe functions: ", Union[Cases[intV$, _B0 | _C0 | _PaVe | _A0, Infinity]]];
(* FeynArts' default prefactor -i (2 pi)^-4 is in the amplitudes, so TID (int d^Dl -> i pi^2 PaVe) gives the loop amplitude
   M1 itself (as the Higgs note's step (6)); each PaVe -> e^(eps gamma) (mu^2)^eps x the unit-measure integral (the MS-bar
   alpha_s in place of the bare one), timelike (-M^2 - i0)^(-eps) = M^(-2 eps) e^(i pi eps) *)
ibGH$ = E^(eps EulerGamma) E^(eps lR) E^(I Pi eps) Gamma[eps] Gamma[1 - eps]^2/Gamma[2 - 2 eps];
icGH$ = E^(eps EulerGamma) E^(eps lR) E^(I Pi eps)/MM Gamma[1 + eps] Gamma[-eps]^2/Gamma[1 - 2 eps];
toExGH$[x_] := x /. {B0[MM, 0, 0] -> ibGH$, C0[a_, b_, c_, 0, 0, 0] :> icGH$, PaVe[0, {MM}, {0, 0}] -> ibGH$,
     PaVe[0, {a_, b_, c_}, {0, 0, 0}] :> icGH$} /. D -> 4 - 2 eps;
f1GH$ = Simplify[toExGH$[intV$]/bornSq$ /. gS -> Sqrt[16 Pi^2 as]];
Print["(d) PaVe left (expect {}): ", Union[Cases[f1GH$, _B0 | _C0 | _PaVe | _A0, Infinity]]];
fReGH$ = FullSimplify[Coefficient[Expand[f1GH$], as] E^(-I Pi eps)];
Print["(d) F^(1) e^(-i pi eps)/a_s (expect real) = ", InputForm[fReGH$]];
virtGG$ = Collect[FunctionExpand[serGH$[2 Cos[Pi eps] fReGH$, 0]], eps, FullSimplify] dlt;
Print["(d) Delta_V/a_s = ", InputForm[virtGG$]];
tick$["virtual"];


(* ::Section:: *)
(*(e) the counterterms and the sum*)


nf = 5; beta0GH$ = 11 - 2/3 nf;
(* UV: cHgg ~ alpha_s, MS-bar: 2 delta alpha_s/alpha_s = -2 beta0 a_s/eps (the loops carry e^(eps gamma)(mu_R^2)^eps) *)
uvGG$ = -2 beta0GH$/eps dlt;
(* the splitting functions: P_gg = 2 C_A [z/(1 - z)_+ + (1 - z)/z + z (1 - z)] + beta0/2 delta(1 - z), P_gq = C_F (1 + (1 - z)^2)/z *)
pggGH$ = 6 (pl0 - 1 + (1 - z)/z + z (1 - z)) + beta0GH$/2 dlt;     (* z/(1 - z)_+ = [1/(1 - z)]_+ - 1 *)
pgqGH$ = 4/3 (1 + (1 - z)^2)/z;
ctGG$ = Expand[serGH$[4/eps E^(eps (lR - lF)), 0] pggGH$];
ctQG$ = Expand[serGH$[2/eps E^(eps (lR - lF)), 0] pgqGH$];
sumGG$ = Collect[Expand[realGG$ + virtGG$ + uvGG$ + ctGG$], {eps, dlt, pl0, pl1, lF, lR}, Simplify];
sumQG$ = Collect[Expand[realQG$ + ctQG$], {eps, lF, lR}, Simplify];
sumQQ$ = Collect[Expand[realQQ$], {eps, lF, lR}, Simplify];
polesGH$ = Simplify[{Coefficient[sumGG$, eps, -2], Coefficient[sumGG$, eps, -1], Coefficient[sumQG$, eps, -1], Coefficient[sumQQ$, eps, -1]}];
Print["(e) poles (gg 1/eps^2, 1/eps; qg 1/eps; qqbar 1/eps; expect 0): ", polesGH$];
d1GG$ = Collect[Coefficient[sumGG$, eps, 0], {dlt, pl0, pl1, lF, lR}, Simplify];
d1QG$ = Collect[Coefficient[sumQG$, eps, 0], {lF, lR}, Simplify];
d1QQ$ = Collect[Coefficient[sumQQ$, eps, 0], {lF, lR}, Simplify];
Print["(e) Delta^(1)_gg = ", InputForm[d1GG$]];
Print["(e) Delta^(1)_qg = ", InputForm[d1QG$]];
Print["(e) Delta^(1)_qqbar = ", InputForm[d1QQ$]];
(* mu_R enters only through the Born's alpha_s^2: d/d lR = 2 beta0 delta(1 - z) in the gg channel, 0 elsewhere *)
Print["(e) d/d lR (expect 2 beta0 = ", 2 beta0GH$, " times delta, 0, 0): ", Simplify[{D[d1GG$, lR], D[d1QG$, lR], D[d1QQ$, lR]}]];
(* the literature (reference) writes sigma_ij = sigma_0 Delta_lit(z), here sigma_ij = sigma_0 z Delta(z): Delta_lit = z Delta, with
   z [g]_+ = [g]_+ - (1 - z) g.  At mu_F = mu_R = M_H, units of alpha_s/pi = 4 a_s, without the Wilson coefficient's 11/2:
   gg: 6 zeta2 delta + 12 [ln(1 - z)/(1 - z)]_+ - 12 z (2 - z + z^2) ln(1 - z) - 6 (1 - z + z^2)^2/(1 - z) ln z - (11/2)(1 - z)^3,
   q g: (2/3)[1 + (1 - z)^2] ln((1 - z)^2/z) - 1 + 2 z - z^2/3,   q qbar: (32/27)(1 - z)^3 *)
timesZ$[x_] := Expand[z x] /. {z dlt -> dlt, z pl0 -> pl0 - 1, z pl1 -> pl1 - Log[1 - z]};
refGG$ = 4 (6 Zeta[2] dlt + 12 pl1 - 12 z (2 - z + z^2) Log[1 - z] - 6 (1 - z + z^2)^2/(1 - z) Log[z] - 11/2 (1 - z)^3);
refQG$ = 4 (2/3 (1 + (1 - z)^2) Log[(1 - z)^2/z] - 1 + 2 z - z^2/3);
refQQ$ = 4 (32/27 (1 - z)^3);
dRefGH$ = {FullSimplify[Expand[timesZ$[d1GG$ /. {lF -> 0, lR -> 0}] - refGG$]],
   FullSimplify[Expand[timesZ$[d1QG$ /. {lF -> 0, lR -> 0}] - refQG$] /. Log[(1 - z)^2/z] -> 2 Log[1 - z] - Log[z]],
   FullSimplify[Expand[timesZ$[d1QQ$ /. {lF -> 0, lR -> 0}] - refQQ$]]};
Print["(e) z Delta^(1) minus the literature (gg, q g, q qbar; reference, expect {0, 0, 0}): ", dRefGH$];
Print["(e) Delta^(1)_qg at mu = M_H in units of alpha_s/pi: ", InputForm[Simplify[d1QG$/4 /. {lF -> 0, lR -> 0}]]];
DeleteDirectory[modelTmpGH$, DeleteContents -> True];
tick$["sum"];


(* ::Section:: *)
(*(f) the renormalized virtual correction in MadLoop's normalization*)


(* MadLoop gives 2 Re(M0^* M1)/|M0|^2 = a_s (4 pi)^eps/Gamma(1 - eps) [A/eps^2 + B/eps + C] with ln(mu_R^2/M_H^2) inside A, B, C and the
   MS-bar alpha_s, while MS-bar strips (4 pi)^eps e^(-eps gamma): [..] = Gamma(1 - eps) e^(-eps gamma) x (the exact virtual here, in
   units of a_s) = (1 + (pi^2/12) eps^2 + ...) x it (the QCD note: C larger by pi^2/12 A), plus the pure-pole counterterm -2 beta0/eps *)
mlGH$ = Collect[Normal[Series[Gamma[1 - eps] E^(-eps EulerGamma) 2 Cos[Pi eps] fReGH$ - 2 beta0GH$/eps, {eps, 0, 0}]], eps, FullSimplify];
mlCoef$[lr_] := N[{Coefficient[mlGH$, eps, -2], Coefficient[mlGH$, eps, -1], Coefficient[mlGH$, eps, 0]} /. lR -> lr, 16];
Print["(f) MadLoop's A, B, C (units a_s) at mu_R = M_H/2, M_H, 2 M_H: ", mlCoef$ /@ {2 Log[1/2], 0, 2 Log[2]}];


(* ::Section:: *)
(*Export*)


numGH$[x_] := ToString[CForm[N[x]]];
chkGH$[x_] := If[AllTrue[Flatten[{x}], # === 0 &], "0", StringReplace[ToString[InputForm[x]], "," -> ";"]];
partGH$[x_, b_] := Coefficient[Expand[x], b];
regGH$[x_] := Expand[x] /. {dlt -> 0, pl0 -> 0, pl1 -> 0};
zsGH$ = {1/100, 1/10, 3/10, 1/2, 7/10, 9/10, 99/100};
cfs$[x_] := {numGH$[x /. {lF -> 0, lR -> 0}], numGH$[Coefficient[x, lF] /. lR -> 0], numGH$[Coefficient[x, lR] /. lF -> 0]};
rowsGH$ = Join[
   {{"quantity", "lF^0 lR^0", "lF^1", "lR^1"}},
   Table[Join[{"gg_" <> b[[1]]}, cfs$[partGH$[d1GG$, b[[2]]]]], {b, {{"delta", dlt}, {"plus0", pl0}, {"plus1", pl1}}}],
   Table[Join[{"gg_reg_z=" <> numGH$[zz]}, cfs$[regGH$[d1GG$] /. z -> zz]], {zz, zsGH$}],
   Table[Join[{"qg_z=" <> numGH$[zz]}, cfs$[d1QG$ /. z -> zz]], {zz, zsGH$}],
   Table[Join[{"qqbar_z=" <> numGH$[zz]}, cfs$[d1QQ$ /. z -> zz]], {zz, zsGH$}],
   {{"check_real_4d_over_known_forms", chkGH$[Simplify[D[chk4$, sh]]], "", ""},
    {"check_poles", chkGH$[polesGH$], "", ""},
    {"check_dlR_minus_2beta0", chkGH$[Simplify[{D[d1GG$, lR] - 2 beta0GH$ dlt, D[d1QG$, lR], D[d1QQ$, lR]}]], "", ""},
    {"check_z_times_Delta_minus_literature_gg_qg_qqbar", chkGH$[dRefGH$], "", ""}},
   Table[{"madloop_ABC_muR_over_MH=" <> numGH$[f], Sequence @@ (numGH$ /@ mlCoef$[2 Log[f]])}, {f, {1/2, 1, 2}}]];
Export[FileNameJoin[{resDirGH$, "gh_feyncalc.csv"}], StringRiffle[StringRiffle[#, ","] & /@ rowsGH$, "\n"] <> "\n", "Text"];
Print["written: results/gh_feyncalc.csv"];
