(* ::Package:: *)

(* ::Title:: *)
(*Step (1a): Drell-Yan at O(alpha_s) in D dimensions -- the MS-bar coefficient functions Delta_qqbar and Delta_qg (FeynCalc; 4-dimensional squared amplitudes against the note's FeynArts model)*)


(* ::Text:: *)
(*Research note models/sm_pp, step (1a).  q(p1) qbar(p2) -> V*(q) [+ g(k)] and q(p1) g(p2) -> V*(q) q(k), V = gamma, Z, W, massless quarks,*)
(*D = 4 - 2 eps, anticommuting gamma5.  The leptons are integrated out: their tensor is (q^mu q^nu - Q^2 g^munu) times a function of Q^2*)
(*common to all channels, and the quark currents are conserved, so only -g_munu H^munu enters, and*)
(*  dsigma_ij/dQ^2 = (sigma_0(Q^2)/shat) Delta_ij(z),  z = Q^2/shat,  Delta = delta(1 - z) + a_s Delta^(1) + ...,  a_s = alpha_s(mu_R)/(4 pi)*)
(*(sigma_0 = the Born q qbar' -> V* -> leptons at shat = Q^2; Delta_qg multiplies the Born of the quark's flavour).  With the bare coupling*)
(*g0^2 mu0^(2 eps) = 4 pi alpha_s mu_R^(2 eps) (e^gamma_E/(4 pi))^eps and the two-body phase space*)
(*  int dPS2 = (1/(8 pi)) (4 pi/shat)^eps (1 - z)^(1 - 2 eps)/Gamma(1 - eps) int_0^1 dv [v (1 - v)]^(-eps),  t = (p1 - k)^2 = -shat (1 - z) v,*)
(*the real part is  Delta_R/a_s = e^(eps gamma_E)/Gamma(1 - eps) (mu_R^2/Q^2)^eps z^eps (1 - z)^(1 - 2 eps) int dv [v(1 - v)]^(-eps) r(z, v),*)
(*r = Q^2 [-g H_R]/[-g H_B(shat = Q^2)] times the colour and average factors (C_F; T_R/(1 - eps) for qg: D - 2 gluon polarizations).*)
(*  (a) -g H of the Born and of the real emission in D dimensions, vector (Gam = 1) and axial (Gam = gamma5) currents; D = 4 forms.*)
(*  (b) the v integrals (Beta functions, exact in eps; checked by NIntegrate at eps < 0) and the expansion*)
(*      (1 - z)^(-1 - 2 eps) = -delta(1 - z)/(2 eps) + [1/(1 - z)]_+ - 2 eps [ln(1 - z)/(1 - z)]_+ + O(eps^2).*)
(*  (c) the vertex in Feynman gauge (TID: B0(Q^2), C0; C0 = -2 (D - 3)/((D - 4) s) B0, checked between the closed forms); the massless*)
(*      self-energies are scaleless, so the field constants vanish:  Delta_V = 2 Re F^(1)(Q^2 + i0) delta(1 - z).*)
(*  (d) the sum with the MS-bar collinear counterterms  (alpha_s/(2 pi)) (1/eps) (mu_R^2/mu_F^2)^eps [2 P_qq] (qqbar), [P_qg] (qg),*)
(*      P_qq = C_F [(1 + z^2)/(1 - z)]_+, P_qg = T_R [z^2 + (1 - z)^2]: no poles, no ln mu_R; Delta^(1) against the MS-bar form of*)
(*      Altarelli, Ellis, Martinelli (reference).*)
(*  (e) the 4-dimensional sum|M|^2 of u ubar -> gamma g, Z g, u dbar -> W+ g and u g -> gamma u from the note's FeynArts model (SM_CKM_FA of*)
(*      the NLO note) against (a) times the couplings.*)
(*Writes results/dy_feyncalc.csv (the checks, and Delta^(1) at sample points for dy_hadronic.py).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file dy_feyncalc.wl  (about 2 minutes).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirDY$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirDY$ = FileNameJoin[{srcDirDY$, "results"}];
Quiet[CreateDirectory[resDirDY$]];
$Assumptions = 0 < z < 1 && 0 < v < 1 && Q2 > 0;
eps2D$ = D -> 4 - 2 eps;
(* the average factors: quarks 2 spin states, gluons D - 2 = 2 (1 - eps) polarizations *)
cfDY$ = 4/3; trDY$ = 1/2;


(* ::Section:: *)
(*(a) the Born and the real emission in D dimensions*)


(* ::Text:: *)
(*q qbar -> V g: the gluon from the quark (propagator p1 - k, t) or from the antiquark (k - p2, u); q g -> V q: s- and u-channel.*)
(*The V vertex is gamma^mu Gam; colour, couplings and averages are put back in r.  Both polarization sums are -g (one gluon, conserved*)
(*current).*)


kinDY$[] := (FCClearScalarProducts[];
   SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[k, k] = 0;
   SPD[p1, p2] = sh/2; SPD[p1, k] = -t/2; SPD[p2, k] = -u/2);
trDYf$[x_] := Simplify[Contract[DiracSimplify[x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]]] /. eps2D$];
hB$[gam_] := (kinDY$[]; trDYf$[-DiracTrace[GSD[p2].GAD[mu].gam.GSD[p1].(gam /. GA5 -> -GA5).GAD[nu]] MTD[mu, nu]]);
(* q qbar -> V g: Gam_R^{mu,al} between vbar(p2) ... u(p1); its conjugate reversed (gamma5 changes sign moving to the other side) *)
ampQQ$[gam_, m_, a_] := GAD[m].gam.(GSD[p1] - GSD[k]).GAD[a]/t + GAD[a].(GSD[k] - GSD[p2]).GAD[m].gam/u;
ampQQc$[gam_, m_, a_] := GAD[a].(GSD[p1] - GSD[k]).(gam /. GA5 -> -GA5).GAD[m]/t + (gam /. GA5 -> -GA5).GAD[m].(GSD[k] - GSD[p2]).GAD[a]/u;
hRQQ$[gam_] := (kinDY$[]; trDYf$[DiracTrace[GSD[p2].ampQQ$[gam, mu, al].GSD[p1].ampQQc$[gam, nu, be]] MTD[mu, nu] MTD[al, be]]);
(* q(p1) g(p2) -> V(q) q(k): ubar(k) [gamma^mu Gam S(p1 + p2) gamma^al + gamma^al S(p1 - q) gamma^mu Gam] u(p1), p1 - q = k - p2 *)
ampQG$[gam_, m_, a_] := GAD[m].gam.(GSD[p1] + GSD[p2]).GAD[a]/sh + GAD[a].(GSD[k] - GSD[p2]).GAD[m].gam/u;
ampQGc$[gam_, m_, a_] := GAD[a].(GSD[p1] + GSD[p2]).(gam /. GA5 -> -GA5).GAD[m]/sh + (gam /. GA5 -> -GA5).GAD[m].(GSD[k] - GSD[p2]).GAD[a]/u;
hRQG$[gam_] := (kinDY$[]; trDYf$[DiracTrace[GSD[k].ampQG$[gam, mu, al].GSD[p1].ampQGc$[gam, nu, be]] MTD[mu, nu] MTD[al, be]]);

hBV$ = hB$[1]; hBA$ = hB$[GA5];
hQQV$ = hRQQ$[1]; hQQA$ = hRQQ$[GA5];
hQGV$ = hRQG$[1]; hQGA$ = hRQG$[GA5];
Print["(a) -g H_B (vector) = ", InputForm[hBV$], ";  axial - vector: Born ", Simplify[hBA$ - hBV$], ", q qbar g ", Simplify[hQQA$ - hQQV$],
  ", q g ", Simplify[hQGA$ - hQGV$], "  (expect 0, 0, 0)"];
(* r(z, v): Q^2 = sh + t + u;  r_qq = C_F Q^2 hR/hB(Q^2),  r_qg = T_R Q^2 hR/((1 - eps) hB(Q^2)) *)
zvDY$ = {t -> -sh (1 - z) v, u -> -sh (1 - z) (1 - v)};
rQQ$ = Factor[cf Q2 hQQV$/(hBV$ /. sh -> Q2) /. zvDY$ /. sh -> Q2/z];
rQG$ = Factor[tr Q2 hQGV$/((1 - eps) (hBV$ /. sh -> Q2)) /. zvDY$ /. sh -> Q2/z];
Print["(a) r_qqbar = ", InputForm[rQQ$]];
Print["(a) r_qg    = ", InputForm[rQG$]];
(* the textbook D-dimensional forms (reference): 2 C_F [(1 - eps)(u/t + t/u) + 2 Q^2 shat/(u t) - 2 eps] and, crossed,
   -2 T_R/(1 - eps) [(1 - eps)(u/shat + shat/u) + 2 Q^2 t/(u shat) - 2 eps] *)
refQQ$ = 2 cf ((1 - eps) (u/t + t/u) + 2 Q2 sh/(u t) - 2 eps) /. zvDY$ /. sh -> Q2/z;
refQG$ = -2 tr/(1 - eps) ((1 - eps) (u/sh + sh/u) + 2 Q2 t/(u sh) - 2 eps) /. zvDY$ /. sh -> Q2/z;
dRef1$ = Simplify[{rQQ$ - refQQ$, rQG$ - refQG$}];
Print["(a) r minus the textbook forms (expect {0, 0}): ", dRef1$];


(* ::Section:: *)
(*(b) the phase-space integrals and the plus distributions*)


(* int_0^1 dv [v (1 - v)]^(-eps) X(v) for X a sum of c v^n and c (v - 1)^m (Apart) *)
vTermDY$[x_] := Which[
   FreeQ[x, v], x Gamma[1 - eps]^2/Gamma[2 - 2 eps],
   MatchQ[x, c_. v^n_. /; FreeQ[c, v]], x /. c_. v^n_. :> c Gamma[n + 1 - eps] Gamma[1 - eps]/Gamma[n + 2 - 2 eps],
   MatchQ[x, c_. (-1 + v)^m_. /; FreeQ[c, v]], x /. c_. (-1 + v)^m_. :> c (-1)^m Gamma[1 - eps] Gamma[m + 1 - eps]/Gamma[m + 2 - 2 eps],
   True, Abort[]];
vIntDY$[x_] := Module[{e = Expand[Apart[Together[x], v]]}, Total[vTermDY$ /@ If[Head[e] === Plus, List @@ e, {e}]]];
iQQ$ = Simplify[vIntDY$[rQQ$]];
iQG$ = Simplify[vIntDY$[rQG$]];
(* numerical check at eps = -3/10 (the integrals converge for eps < 0), z = 0.37 *)
chkV$ = Module[{e = -3/10, zz = 37/100, nums = {cf -> cfDY$, tr -> trDY$}},
   {N[iQQ$ /. {eps -> e, z -> zz} /. nums, 15] - NIntegrate[(v (1 - v))^(-e) (rQQ$ /. {eps -> e, z -> zz} /. nums), {v, 0, 1}, WorkingPrecision -> 30, PrecisionGoal -> 15],
    N[iQG$ /. {eps -> e, z -> zz} /. nums, 15] - NIntegrate[(v (1 - v))^(-e) (rQG$ /. {eps -> e, z -> zz} /. nums), {v, 0, 1}, WorkingPrecision -> 30, PrecisionGoal -> 15]}];
Print["(b) v integrals minus NIntegrate at eps = -0.3, z = 0.37 (expect ~1e-15): ", chkV$];
(* Delta_R/a_s = H(z, eps) (1 - z)^(-1 - 2 eps) for q qbar, H regular at z = 1 *)
normDY$ = E^(eps EulerGamma)/Gamma[1 - eps] E^(eps lR) z^eps;
hQQ$ = Simplify[normDY$ vIntDY$[Cancel[(1 - z)^2 rQQ$]]];
Print["(b) H_qqbar(1, eps) = ", InputForm[FullSimplify[hQQ$ /. z -> 1]]];
(* the distributions: dlt = delta(1 - z), pl0 = [1/(1 - z)]_+, pl1 = [ln(1 - z)/(1 - z)]_+; c(z) pl_k -> c(1) pl_k + (c(z) - c(1)) f_k(z) *)
serDY$[x_, n_] := Normal[Series[x, {eps, 0, n}]];
plusDY$[c_, k_] := Module[{c1 = Simplify[c /. z -> 1]},
   c1 If[k == 0, pl0, pl1] + Simplify[(c - c1) If[k == 0, 1/(1 - z), Log[1 - z]/(1 - z)]]];
plusExpand$[x_, k_] := Module[{cs = Collect[Expand[x], eps, Simplify]},
   Sum[plusDY$[Coefficient[cs, eps, n], k] eps^n, {n, -1, 0}]];
(* H = H_-1/eps + H_0 + H_1 eps: delta needs H(1) to O(eps), pl0 to O(1), pl1 only H_-1 (the pl2 term is O(eps)) *)
realQQ$ = serDY$[-(hQQ$ /. z -> 1)/(2 eps), 0] dlt + plusExpand$[serDY$[hQQ$, 0], 0] - 2 eps plusExpand$[serDY$[hQQ$, -1], 1];
realQQ$ = Collect[Expand[realQQ$], {eps, dlt, pl0, pl1}, Simplify];
realQG$ = Collect[serDY$[normDY$ (1 - z)^(1 - 2 eps) iQG$, 0], eps, Simplify];
Print["(b) Delta_R,qqbar/a_s = ", InputForm[realQQ$]];
Print["(b) Delta_R,qg/a_s = ", InputForm[realQG$]];


(* ::Section:: *)
(*(c) the virtual correction*)


(* ::Text:: *)
(*v(p2)bar [gamma^rho S(-p2 - l) gamma^mu Gam S(p1 - l) gamma_rho] u(p1) / l^2: (-i g)^2 i^2 (-i) C_F = -i g^2 C_F; the MS-bar measure*)
(*g0^2 mu0^(2 eps) int d^Dl/(2 pi)^D = g^2 (i/(16 pi^2)) e^(eps gamma_E) mu^(2 eps) int d^Dl/(i pi^(D/2)); FeynCalc's TID gives*)
(*int d^Dl X = i pi^2 sum c_k PaVe_k, and each PaVe_k -> the unit-measure integral times e^(eps gamma_E) mu^(2 eps):*)
(*  B0(s) -> e^(eps gamma) (mu^2/(-s - i0))^eps Gamma(eps) Gamma(1 - eps)^2/Gamma(2 - 2 eps),*)
(*  C0(s) -> -e^(eps gamma) mu^(2 eps) (-s - i0)^(-1 - eps) Gamma(1 + eps) Gamma(-eps)^2/Gamma(1 - 2 eps),  -s - i0 = s e^(-i pi).*)


ibDY$ = E^(eps EulerGamma) E^(eps lR) E^(I Pi eps) Gamma[eps] Gamma[1 - eps]^2/Gamma[2 - 2 eps];        (* at s = Q2 = mu^2 e^(-lR) *)
icDY$ = E^(eps EulerGamma) E^(eps lR) E^(I Pi eps)/Q2 Gamma[1 + eps] Gamma[-eps]^2/Gamma[1 - 2 eps];
Print["(c) IBP: C0 + 2 (D - 3)/((D - 4) s) B0 between the closed forms: ", FullSimplify[icDY$ + 2 (1 - 2 eps)/((-2 eps) Q2) ibDY$], "  (expect 0)"];
vertDY$[gam_] := Module[{num, red},
   FCClearScalarProducts[];
   SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[p1, p2] = Q2/2;
   num = DiracSimplify[DiracTrace[GSD[p2].GAD[rho].(-GSD[p2] - GSD[l]).GAD[mu].gam.(GSD[p1] - GSD[l]).GAD[rho].GSD[p1].(gam /. GA5 -> -GA5).GAD[nu]]
       /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True]];
   num = Contract[-num MTD[mu, nu]];
   red = TID[num FAD[l, l - p1, l + p2], l, ToPaVe -> True];
   red = PaVeReduce[red] /. {B0[0, 0, 0] -> 0};
   red = red /. {B0[x_, 0, 0] :> ibDY$, C0[a_, b_, c_, 0, 0, 0] :> icDY$, PaVe[0, {x_}, {0, 0}] :> ibDY$,
      PaVe[0, {a_, b_, c_}, {0, 0, 0}] :> icDY$};
   (* F^(1)/a_s: -i C_F (i/(16 pi^2)) (TID/(i pi^2)) (16 pi^2)/(-g H_B), with g^2 = 16 pi^2 a_s *)
   Simplify[-I cf I (red/(I Pi^2))/(hB$[gam] /. sh -> Q2) /. eps2D$]];
fV$ = vertDY$[1]; fA$ = vertDY$[GA5];
Print["(c) PaVe functions left (expect {}): ", Union[Cases[{fV$, fA$}, _B0 | _C0 | _PaVe, Infinity]]];
Print["(c) F^(1)_axial - F^(1)_vector = ", FullSimplify[fA$ - fV$], "  (expect 0)"];
fRe$ = FullSimplify[fV$ E^(-I Pi eps)];
Print["(c) F^(1) e^(-i pi eps)/a_s = ", InputForm[fRe$], "  (expect real: the timelike phase only in e^(i pi eps))"];
fRef$ = -cf E^(eps EulerGamma) E^(eps lR) Gamma[1 + eps] Gamma[1 - eps]^2/Gamma[1 - 2 eps] (2 - eps + 2 eps^2)/(eps^2 (1 - 2 eps));
Print["(c) minus -C_F e^(eps gamma) Gamma(1+eps) Gamma(1-eps)^2/Gamma(1-2eps) (2 - eps + 2 eps^2)/(eps^2 (1 - 2 eps)) (reference): ",
  FullSimplify[fRe$ - fRef$]];
virtQQ$ = Collect[FunctionExpand[serDY$[2 Cos[Pi eps] fRe$, 0]], eps, FullSimplify] dlt;
Print["(c) Delta_V/a_s = ", InputForm[virtQQ$]];


(* ::Section:: *)
(*(d) the sum and the collinear counterterms*)


pqqDY$ = cf (2 pl0 - (1 + z) + 3/2 dlt);
pqgDY$ = tr (z^2 + (1 - z)^2);
ctQQ$ = Expand[serDY$[4/eps E^(eps (lR - lF)), 0] pqqDY$];     (* (alpha_s/(2 pi)) = 2 a_s, two legs *)
ctQG$ = Expand[serDY$[2/eps E^(eps (lR - lF)), 0] pqgDY$];
sumQQ$ = Collect[Expand[realQQ$ + virtQQ$ + ctQQ$] /. cf -> cfDY$, {eps, dlt, pl0, pl1, lF}, Simplify];
sumQG$ = Collect[Expand[realQG$ + ctQG$] /. tr -> trDY$, {eps, lF}, Simplify];
polesDY$ = Simplify[{Coefficient[sumQQ$, eps, -2], Coefficient[sumQQ$, eps, -1], Coefficient[sumQG$, eps, -1]}];
Print["(d) poles (1/eps^2, 1/eps qqbar; 1/eps qg; expect 0): ", polesDY$];
d1QQ$ = Collect[Coefficient[sumQQ$, eps, 0] /. cf -> cfDY$, {dlt, pl0, pl1, lF}, Simplify];
d1QG$ = Collect[Coefficient[sumQG$, eps, 0] /. tr -> trDY$, {lF}, Simplify];
Print["(d) d/d lR of Delta^(1) (expect 0, 0): ", Simplify[{D[d1QQ$, lR], D[d1QG$, lR]}]];
d1QQ$ = d1QQ$ /. lR -> 0; d1QG$ = d1QG$ /. lR -> 0;
Print["(d) Delta^(1)_qqbar = ", InputForm[d1QQ$]];
Print["(d) Delta^(1)_qg    = ", InputForm[d1QG$]];
(* Altarelli, Ellis, Martinelli in the MS-bar scheme (reference), lF = ln(mu_F^2/Q^2):
   C_F [16 pl1 - 8 (1 + z) ln(1 - z) - 4 (1 + z^2) ln z/(1 - z) + (8 zeta2 - 16) dlt] - 4 lF P_qq,
   T_R [2 (z^2 + (1 - z)^2) ln((1 - z)^2/z) + 1 + 6 z - 7 z^2] - 2 lF P_qg *)
refD1QQ$ = cfDY$ (16 pl1 - 8 (1 + z) Log[1 - z] - 4 (1 + z^2) Log[z]/(1 - z) + (8 Zeta[2] - 16) dlt) - 4 lF (pqqDY$ /. cf -> cfDY$);
refD1QG$ = trDY$ (2 (z^2 + (1 - z)^2) Log[(1 - z)^2/z] + 1 + 6 z - 7 z^2) - 2 lF (pqgDY$ /. tr -> trDY$);
dRef2$ = {FullSimplify[Expand[d1QQ$ - refD1QQ$]], FullSimplify[Expand[d1QG$ - refD1QG$] /. Log[(1 - z)^2/z] -> 2 Log[1 - z] - Log[z]]};
Print["(d) Delta^(1) minus the MS-bar forms of Altarelli-Ellis-Martinelli (reference, expect {0, 0}): ", dRef2$];


(* ::Section:: *)
(*(d2) the rapidity distribution: the pieces at fixed v*)


(* ::Text:: *)
(*At fixed (z, v) the lepton pair has the partonic rapidity y* = (1/2) ln[(z + v (1 - z))/(1 - v (1 - z))]: y* = (1/2) ln z at v = 0*)
(*(k along p1: parton 1 keeps z x1), -(1/2) ln z at v = 1, 0 at z = 1.  With G(z, v) the luminosity weighted by the observable,*)
(*G_a = G(z, 0), G_b = G(z, 1), G(1) = G(1, v), the D-dimensional real emission is expanded in distributions of v at fixed z < 1:*)
(*  q qbar: (1 - z)^2 v (1 - v) r_qqbar = R(z, v, eps),  [v (1 - v)]^(-1 - eps) = v^(-1 - eps) (1 - v)^(-eps) + (v <-> 1 - v);*)
(*  q(p1) g(p2): (1 - z)(1 - v) r_qg = S(z, v, eps), collinear only at v = 1 (the quark along the gluon).*)
(*The poles at v = 0, 1 cancel against the counterterms at the same kinematics and the delta(1 - z) part is that of (d), so*)
(*  Delta_qqbar G = cdelta G(1) + int dz/(1 - z) {-R1(z,0) G_a - R1(z,1) G_b - 2 C_F (1 + z^2) ln z (G_a + G_b)*)
(*        + int dv [(R0 G - R0(z,0) G_a)/v + (R0 G - R0(z,1) G_b)/(1 - v)]} + 4 C_F (1 + z^2) D1 (G_a + G_b) - 2 C_F lF (1 + z^2) D0 (G_a + G_b),*)
(*  Delta_qg G = int dz {2 T_R P (2 ln(1 - z) - ln z) G_b - S1(z,1) G_b + int dv (S0 G - S0(z,1) G_b)/(1 - v) - 2 T_R lF P G_b},*)
(*R = R0 + eps R1, S = S0 + eps S1, P = z^2 + (1 - z)^2 (g(p1) q(p2): v -> 1 - v, G_b -> G_a).  Here: R0, R1, S0, S1 against the*)
(*forms used by dy_hadronic.py, and with G independent of v (the integral over y) these give Delta^(1) of (d) exactly.*)


rDY$ = Collect[Series[Cancel[(1 - z)^2 v (1 - v) rQQ$] /. cf -> cfDY$, {eps, 0, 1}] // Normal, eps, Simplify];
sDY$ = Collect[Series[Cancel[(1 - z) (1 - v) rQG$] /. tr -> trDY$, {eps, 0, 1}] // Normal, eps, Simplify];
{r0DY$, r1DY$} = {Coefficient[rDY$, eps, 0], Coefficient[rDY$, eps, 1]};
{s0DY$, s1DY$} = {Coefficient[sDY$, eps, 0], Coefficient[sDY$, eps, 1]};
handRS$ = {2 cfDY$ ((1 - z)^2 (v^2 + (1 - v)^2) + 2 z), -2 cfDY$ (1 - z)^2, 2 trDY$ ((1 - z)^2 (1 - v)^2 + 1 - 2 z (1 - z) v), -4 trDY$ z (1 - z)};
dRS$ = Simplify[{r0DY$ - handRS$[[1]], (r1DY$ /. v -> 0) - handRS$[[2]], (r1DY$ /. v -> 1) - handRS$[[2]], s0DY$ - handRS$[[3]],
    (s1DY$ /. v -> 1) - handRS$[[4]]}];
Print["(d2) R0, R1(v = 0), R1(v = 1), S0, S1(v = 1) minus the forms of dy_hadronic.py (expect 0): ", dRS$];
(* the integral over y: G independent of v; D0 and D1 act on functions that vanish at z = 1 except the last two terms *)
ppDY$ = z^2 + (1 - z)^2;
(* (1 + z^2) D1 = 2 D1 - (1 + z) ln(1 - z), (1 + z^2) D0 = 2 D0 - (1 + z); G_a + G_b = 2 G *)
yIntQQ$ = (Simplify[(-(r1DY$ /. v -> 0) - (r1DY$ /. v -> 1) - 2 cfDY$ (1 + z^2) Log[z] 2 +
        Integrate[(r0DY$ - (r0DY$ /. v -> 0))/v + (r0DY$ - (r0DY$ /. v -> 1))/(1 - v), {v, 0, 1}])/(1 - z)] +
    8 cfDY$ (2 pl1 - (1 + z) Log[1 - z]) - 4 cfDY$ lF (2 pl0 - (1 + z)) + (cfDY$ (8 Zeta[2] - 16) - 6 cfDY$ lF) dlt);
yIntQG$ = Simplify[2 trDY$ ppDY$ (2 Log[1 - z] - Log[z]) - (s1DY$ /. v -> 1) + Integrate[(s0DY$ - (s0DY$ /. v -> 1))/(1 - v), {v, 0, 1}]
    - 2 trDY$ lF ppDY$];
dYint$ = {FullSimplify[Expand[yIntQQ$ - d1QQ$]], FullSimplify[Expand[yIntQG$ - d1QG$]]};
Print["(d2) the rapidity pieces integrated over v minus Delta^(1) (expect {0, 0}): ", dYint$];


(* ::Section:: *)
(*(e) the 4-dimensional squared amplitudes against the note's FeynArts model*)


tmpDY$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirDY$, "..", "..", "sm_nlo", "Src", "generated", "SM_CKM_FA"}], FileNameJoin[{tmpDY$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{tmpDY$, "SM_CKM_FA"}], Quiet -> True];
modelDY$ = FileNameJoin[{tmpDY$, "SM_CKM_FA", "SM_CKM_FA"}];
convDY$ = {FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["MZ"] -> MZ, FCGV["MW"] -> MW,
   FCGV["MU"] -> 0, FCGV["MD"] -> 0, MU -> 0, MD -> 0, Conjugate[CKM[1, 1]] -> 1, CKM[1, 1] -> 1};
(* in -> out with the colour-singlet boson q (Q^2 off shell) and the massless parton k; the second incoming momentum p2 *)
fa22DY$[in_, out_] := Module[{d, a, x},
   d = Quiet[InsertFields[CreateTopologies[0, 2 -> 2], in -> out, InsertionLevel -> {Particles},
       Model -> modelDY$, GenericModel -> modelDY$], RuleDelayed::rhs];
   a = Quiet[FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {q, k},
       ChangeDimension -> 4, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> True,
       TransversePolarizationVectors -> {}], RuleDelayed::rhs] /. convDY$;
   FCClearScalarProducts[];
   ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0; ScalarProduct[k, k] = 0; ScalarProduct[q, q] = sh + t + u;
   ScalarProduct[p1, p2] = sh/2; ScalarProduct[p1, k] = -t/2; ScalarProduct[p2, k] = -u/2;
   ScalarProduct[p1, q] = (sh + t)/2; ScalarProduct[p2, q] = (sh + u)/2; ScalarProduct[q, k] = -(t + u)/2;
   x = FermionSpinSum[ComplexConjugate[Total[a]] Total[a], ExtraFactor -> 1];
   x = x /. DiracTrace[y_] :> DiracTrace[y, DiracTraceEvaluate -> True];
   x = DoPolarizationSums[x, q, 0, VirtualBoson -> True];
   x = DoPolarizationSums[x, If[MemberQ[in, V[4]], p2, k], 0, VirtualBoson -> True];
   x = Contract[FeynAmpDenominatorExplicit[SUNSimplify[DiracSimplify[x], SUNNToCACF -> False]]] /. SUNN -> 3;
   {Length[a], Simplify[x /. {sw -> Sqrt[1 - MW^2/MZ^2], cw -> MW/MZ}]}];
(* the hand values: N_c C_F g_s^2 (cV^2 + cA^2) [-g H_R]_(D=4), cV, cA of the vertex gamma^mu (cV - cA gamma5) *)
s2DY$ = 1 - MW^2/MZ^2; gzDY$ = ee/Sqrt[s2DY$ (1 - s2DY$)];
handDY$[h_, cv_, ca_] := 3 cfDY$ gS^2 (cv^2 + ca^2) (h /. eps -> 0);
casesDY$ = {
   {"u ubar -> gamma g", {F[3, {1}], -F[3, {1}]}, {V[1], V[4]}, hQQV$, 2/3 ee, 0},
   {"u ubar -> Z g", {F[3, {1}], -F[3, {1}]}, {V[2], V[4]}, hQQV$, gzDY$ (1/2 - 2 (2/3) s2DY$)/2, gzDY$ (1/2)/2},
   {"u dbar -> W+ g", {F[3, {1}], -F[4, {1}]}, {V[3], V[4]}, hQQV$, ee/(Sqrt[2] Sqrt[s2DY$])/2, ee/(Sqrt[2] Sqrt[s2DY$])/2},
   {"u g -> gamma u", {F[3, {1}], V[4]}, {V[1], F[3, {1}]}, hQGV$, 2/3 ee, 0}};
faDY$ = Table[Module[{r = fa22DY$[c[[2]], c[[3]]], dd},
    dd = Simplify[r[[2]] - handDY$[c[[4]], c[[5]], c[[6]]]];
    Print["(e) ", c[[1]], ": ", r[[1]], " diagrams; FeynArts model minus hand (expect 0): ", dd];
    {c[[1]], r[[1]], dd}], {c, casesDY$}];
DeleteDirectory[tmpDY$, DeleteContents -> True];


(* ::Section:: *)
(*Export*)


(* Delta^(1) = cdelta dlt + c0 pl0 + c1 pl1 + reg(z), each = (lF^0 part) + lF (lF^1 part) *)
partDY$[x_, b_] := Coefficient[Expand[x], b];
regDY$[x_] := Expand[x] /. {dlt -> 0, pl0 -> 0, pl1 -> 0};
zsDY$ = {1/100, 1/10, 3/10, 1/2, 7/10, 9/10, 99/100};
numDY$[x_] := ToString[CForm[N[x]]];
(* a check: "0" when every entry is exactly 0, else the expression (commas as ";") *)
chkDY$[x_] := If[AllTrue[Flatten[{x}], # === 0 &], "0", StringReplace[ToString[InputForm[x]], "," -> ";"]];
rowsDY$ = Join[
   {{"quantity", "lF^0", "lF^1"}},
   Table[{"qqbar_" <> b[[1]], numDY$[partDY$[d1QQ$, b[[2]]] /. lF -> 0], numDY$[Coefficient[partDY$[d1QQ$, b[[2]]], lF]]},
     {b, {{"delta", dlt}, {"plus0", pl0}, {"plus1", pl1}}}],
   Table[{"qqbar_reg_z=" <> numDY$[zz], numDY$[regDY$[d1QQ$] /. lF -> 0 /. z -> zz], numDY$[Coefficient[regDY$[d1QQ$], lF] /. z -> zz]}, {zz, zsDY$}],
   Table[{"qg_z=" <> numDY$[zz], numDY$[d1QG$ /. lF -> 0 /. z -> zz], numDY$[Coefficient[d1QG$, lF] /. z -> zz]}, {zz, zsDY$}],
   {{"check_axial_minus_vector_real", chkDY$[Simplify[{hBA$ - hBV$, hQQA$ - hQQV$, hQGA$ - hQGV$}]], ""},
    {"check_r_minus_textbook", chkDY$[dRef1$], ""},
    {"check_v_integral_minus_NIntegrate", numDY$[Max[Abs[chkV$]]], ""},
    {"check_axial_minus_vector_virtual", chkDY$[FullSimplify[fA$ - fV$]], ""},
    {"check_F1_minus_reference", chkDY$[FullSimplify[fRe$ - fRef$]], ""},
    {"check_poles", chkDY$[polesDY$], ""},
    {"check_minus_AEM_reference", chkDY$[dRef2$], ""},
    {"check_rapidity_pieces_minus_dy_hadronic_forms", chkDY$[dRS$], ""},
    {"check_rapidity_pieces_integrated_minus_Delta1", chkDY$[dYint$], ""}},
   Table[{"check_FeynArts_minus_hand " <> f[[1]] <> " (" <> ToString[f[[2]]] <> " diagrams)", chkDY$[f[[3]]], ""}, {f, faDY$}]];
Export[FileNameJoin[{resDirDY$, "dy_feyncalc.csv"}], StringRiffle[StringRiffle[#, ","] & /@ rowsDY$, "\n"] <> "\n", "Text"];
Print["written: results/dy_feyncalc.csv"];
