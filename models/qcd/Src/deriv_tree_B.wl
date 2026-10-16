(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: colour-split spin sums of g g -> Q Qbar with traces (FeynCalc)*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices (FeynCalc 10.2.1, 4 dimensions).*)
(*  app:tree 「(B) の色で分けたスピンの和。」「偏極の和とゴースト。」「(B) の色の和。」 and app:ir 「(B) の色の相関。」 (T2):*)
(*  the six -g sums of the Eq. (Mtree) form against the hand results, the simplified structures N_t, N_u, N_s, the intermediate traces*)
(*  (i)-(v), (a)-(d), (a')-(d') of the text, S_kl, the transversality of the Eq. (Mtree) form, the Feynman-rule vertex (-g sums exceed S_kl*)
(*  by 4 tau1 tau2 (1,-1)x(1,-1), the ghost removes it), the physical polarization sums, and the colour sum = Eq. (sumtree) (B).*)
(*  Units s = 1: p1.p2 = 1/2, p1.k1 = p2.k2 = tau1/2, p1.k2 = p2.k1 = tau2/2, k1.k2 = 1/2 - m^2, m^2 = rho/4, tau2 = 1 - tau1;*)
(*  A_x = -g^2 ubar G_x v (g = 1), A_1 = A_t + A_s, A_2 = A_u - A_s.*)
(*Each line prints the difference and OK or FAIL.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_tree_B.txt.*)
(*Usage (from Src/): wolframscript -file deriv_tree_B.wl   (about 10 s)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_tree_B.wl.  Interactive:  ~/hep/bin/wopen deriv_tree_B.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
Get["FeynCalc`"];
$FCAdvice = False;
FCClearScalarProducts[];
tau2v = 1 - tau1;
ScalarProduct[p1, p1] = 0; ScalarProduct[p2, p2] = 0;
ScalarProduct[k1, k1] = rho/4; ScalarProduct[k2, k2] = rho/4;
ScalarProduct[p1, p2] = 1/2;
ScalarProduct[p1, k1] = tau1/2; ScalarProduct[p2, k2] = tau1/2;
ScalarProduct[p1, k2] = tau2v/2; ScalarProduct[p2, k1] = tau2v/2;
ScalarProduct[k1, k2] = (1 - rho/2)/2;
(* an arbitrary vector r for the transversality test *)
ScalarProduct[r, p1] = r1; ScalarProduct[r, p2] = r2; ScalarProduct[r, k1] = r3; ScalarProduct[r, k2] = r4; ScalarProduct[r, r] = r5;
mm = Sqrt[rho]/2;
Gt[mu_, nu_] := GA[mu] . (GS[k1 - p1] + mm) . GA[nu]/(-tau1);
Gu[mu_, nu_] := GA[nu] . (GS[k1 - p2] + mm) . GA[mu]/(-tau2v);
Gs[mu_, nu_] := MT[mu, nu] (GS[p1] - GS[p2]) + 2 FV[p2, mu] GA[nu] - 2 FV[p1, nu] GA[mu];
GsF[mu_, nu_] := MT[mu, nu] (GS[p1] - GS[p2]) + FV[2 p2 + p1, mu] GA[nu] - FV[2 p1 + p2, nu] GA[mu];
G1[mu_, nu_] := Gt[mu, nu] + Gs[mu, nu];  G2[mu_, nu_] := Gu[mu, nu] - Gs[mu, nu];
G1F[mu_, nu_] := Gt[mu, nu] + GsF[mu, nu]; G2F[mu_, nu_] := Gu[mu, nu] - GsF[mu, nu];
(* the simplified forms used in the text (valid between ubar(k1) ... v(k2)) *)
Nt[mu_, nu_] := (2 FV[k1, mu] GA[nu] - GA[mu] . GS[p1] . GA[nu])/(-tau1);
Nu[mu_, nu_] := (2 FV[k1, nu] GA[mu] - GA[nu] . GS[p2] . GA[mu])/(-tau2v);
Ns[mu_, nu_] := 2 (MT[mu, nu] GS[p1] + FV[p2, mu] GA[nu] - FV[p1, nu] GA[mu]);
(* Dirac conjugate of a chain with real coefficients = reversed order; Dot is Flat, so match the whole Dot object *)
rev[x_] := x /. d_Dot :> (Dot @@ Reverse[List @@ d]);
tr[x_] := Simplify[Contract[DiracSimplify[DiracTrace[x, DiracTraceEvaluate -> True]]]];
(* -g sums over both gluons: sum_{spins,pols} A_x A_y^* = Tr[(k1+m) G_x^{mu nu} (k2-m) bar(G_y)_{mu nu}]  ((-1)^2 from the -g's) *)
pair[gx_, gy_] := tr[(GS[k1] + mm) . gx[mu, nu] . (GS[k2] - mm) . rev[gy[mu, nu]]];
F = tau1^2 + tau2v^2 + rho - rho^2/(4 tau1 tau2v);
chk[label_, x_] := Print[label, " -> ", Simplify[x], If[Simplify[x] === 0, "   OK", "   FAIL"]];


(* ::Section:: *)
(*the six -g sums of the Eq. (Mtree) form*)


Print["--- the six -g sums (Eq. (Mtree) form) against the hand results"];
Ttt = pair[Gt, Gt]; Tuu = pair[Gu, Gu]; Ttu = pair[Gt, Gu]; Tts = pair[Gt, Gs]; Tus = pair[Gu, Gs]; Tss = pair[Gs, Gs];


(* ::Subsubsection:: *)
(*Inspect: the six -g sums Ttt, Tuu, Ttu, Tts, Tus, Tss (units g^4, s = 1)*)


If[$Notebooks,
  Simplify[{Ttt, Tuu, Ttu, Tts, Tus, Tss}]
]


chk["Ttt - (8tau2/tau1 + 4rho/tau1 - 2rho^2/tau1^2)", Ttt - (8 tau2v/tau1 + 4 rho/tau1 - 2 rho^2/tau1^2)];
chk["Tuu - (tau1<->tau2)", Tuu - (8 tau1/tau2v + 4 rho/tau2v - 2 rho^2/tau2v^2)];
chk["Ttu - 2rho(1-rho)/(tau1 tau2)", Ttu - 2 rho (1 - rho)/(tau1 tau2v)];
chk["Tts + 8tau2 + 2rho(tau1-tau2)/tau1", Tts + 8 tau2v + 2 rho (tau1 - tau2v)/tau1];
chk["Tus - 8tau1 - 2rho(tau2-tau1)/tau2", Tus - 8 tau1 - 2 rho (tau2v - tau1)/tau2v];
chk["Tss - 16 tau1 tau2", Tss - 16 tau1 tau2v];

(* ::Section:: *)
(*the simplified structures N_t, N_u, N_s*)


Print["--- the same sums with the simplified structures N_t, N_u, N_s of the text"];
chk["N: Ttt", pair[Nt, Nt] - Ttt]; chk["N: Ttu", pair[Nt, Nu] - Ttu]; chk["N: Tts", pair[Nt, Ns] - Tts]; chk["N: Tss", pair[Ns, Ns] - Tss];

(* ::Section:: *)
(*intermediate traces of the text*)


Print["--- intermediate traces of the text (units s = 1)"];
k1k2 = 1/2 - rho/4;
(* Tts: Tr[(k1+m) N_t (k2-m) N_s] = (i)+...+(v) with N_t, N_s without the 1/(-tau1) *)
ti = 4 tr[(GS[k1] + mm) . GS[k1] . (GS[k2] - mm) . GS[p1]];
tiii = -4 tr[(GS[k1] + mm) . GS[p1] . (GS[k2] - mm) . GS[k1]];
tii = 4 (tau2v/2) tr[(GS[k1] + mm) . GA[nu] . (GS[k2] - mm) . GA[nu]];
tiv = 4 tr[(GS[k1] + mm) . GS[p1] . (GS[k2] - mm) . GS[p1]];
tv = -2 tr[(GS[k1] + mm) . GS[p2] . GS[p1] . GA[nu] . (GS[k2] - mm) . GA[nu]];
chk["(i)+(iii)", ti + tiii];
chk["(ii) + 8 tau2 (1+rho/2)", tii + 8 tau2v (1 + rho/2)];
chk["(iv) - 8 tau1 tau2", tiv - 8 tau1 tau2v];
chk["(v) - (8 tau2 + 2 rho)", tv - (8 tau2v + 2 rho)];
chk["sum - [8 tau1 tau2 + 2 rho (tau1 - tau2)]", ti + tii + tiii + tiv + tv - (8 tau1 tau2v + 2 rho (tau1 - tau2v))];
chk["Tr[(k1+m) N_t (k2-m) N_s] (no 1/(-tau1)) vs (i)..(v)", -tau1 pair[Nt, Ns] - (ti + tii + tiii + tiv + tv)];
(* Ttt: (a)..(d) *)
ta = 4 (rho/4) tr[(GS[k1] + mm) . GA[nu] . (GS[k2] - mm) . GA[nu]];
tb = -2 tr[(GS[k1] + mm) . GA[nu] . (GS[k2] - mm) . GA[nu] . GS[p1] . GS[k1]];
tc = -2 tr[(GS[k1] + mm) . GS[k1] . GS[p1] . GA[nu] . (GS[k2] - mm) . GA[nu]];
td = tr[(GS[k1] + mm) . GA[mu] . GS[p1] . GA[nu] . (GS[k2] - mm) . GA[nu] . GS[p1] . GA[mu]];
chk["(a) + 32 m^2 (k1.k2 + 2m^2)", ta + 32 (rho/4) (k1k2 + rho/2)];
chk["(b) - 16 m^2 (2 k1.p1 + k2.p1)", tb - 16 (rho/4) (tau1 + tau2v/2)];
chk["(c) - (b)", tc - tb];
chk["(d) - 32 (k1.p1)(k2.p1)", td - 32 (tau1/2) (tau2v/2)];
chk["Ttt tau1^2 - [(a)+(b)+(c)+(d)]", Ttt tau1^2 - (ta + tb + tc + td)];
chk["(a)+(b)+(c)+(d) - (8 tau1 tau2 + 4 rho tau1 - 2 rho^2)", ta + tb + tc + td - (8 tau1 tau2v + 4 rho tau1 - 2 rho^2)];
(* Ttu: (a')..(d') *)
ua = 4 tr[(GS[k1] + mm) . GS[k1] . (GS[k2] - mm) . GS[k1]];
ub = -2 tr[(GS[k1] + mm) . GA[nu] . (GS[k2] - mm) . GS[k1] . GS[p2] . GA[nu]];
uc = -2 tr[(GS[k1] + mm) . GA[mu] . GS[p1] . GS[k1] . (GS[k2] - mm) . GA[mu]];
ud = tr[(GS[k1] + mm) . GA[mu] . GS[p1] . GA[nu] . (GS[k2] - mm) . GA[mu] . GS[p2] . GA[nu]];
chk["(a') - 16 m^2 (k1.k2 - m^2)", ua - 16 (rho/4) (k1k2 - rho/4)];
chk["(b') - 16[2(k1.k2)(k1.p2) - m^2 k2.p2] - 32 m^2 k1.p2", ub - 16 (2 k1k2 tau2v/2 - rho/4 tau1/2) - 32 rho/4 tau2v/2];
chk["(c') - 16[2(k1.p1)(k1.k2) - m^2 p1.k2] - 32 m^2 p1.k1", uc - 16 (2 tau1/2 k1k2 - rho/4 tau2v/2) - 32 rho/4 tau1/2];
chk["(d') + 32 (p1.p2)(k1.k2) + 16 m^2 p1.p2", ud + 32 (1/2) k1k2 + 16 (rho/4) (1/2)];
chk["sum - 16 m^2 (s/2 - 2 m^2) = 2 rho (1-rho)", ua + ub + uc + ud - 2 rho (1 - rho)];
chk["Ttu tau1 tau2 - sum", Ttu tau1 tau2v - (ua + ub + uc + ud)];

(* ::Section:: *)
(*S_kl*)


Print["--- S_kl from the -g sums of the Eq. (Mtree) form"];
S11 = Ttt + 2 Tts + Tss; S22 = Tuu - 2 Tus + Tss; S12 = Ttu - Tts + Tus - Tss;


(* ::Subsubsection:: *)
(*Inspect: S_11, S_22, S_12 and F*)


If[$Notebooks,
  Simplify[{S11, S22, S12, F}]
]


chk["S11 - 8F tau2/tau1", S11 - 8 F tau2v/tau1];
chk["S22 - 8F tau1/tau2", S22 - 8 F tau1/tau2v];
chk["S12 - 8F", S12 - 8 F];
chk["S11 + S22 + 2 S12 - 8F/(tau1 tau2)  (QED)", S11 + S22 + 2 S12 - 8 F/(tau1 tau2v)];
chk["pair[G1,G1] - S11", pair[G1, G1] - S11]; chk["pair[G1,G2] - S12", pair[G1, G2] - S12];

(* ::Section:: *)
(*transversality of the Eq. (Mtree) form*)


Print["--- transversality of the Eq. (Mtree) form: sum_spins |ubar (p1.B_k.r) v|^2 and |ubar (r.B_k.p2) v|^2 for arbitrary r"];
contr1[g_] := Contract[FV[p1, mu] FV[r, nu] g[mu, nu]]; contr2[g_] := Contract[FV[r, mu] FV[p2, nu] g[mu, nu]];
sq[x_] := tr[(GS[k1] + mm) . x . (GS[k2] - mm) . rev[x]];
chk["|p1.B_1.r|^2", sq[contr1[G1]]]; chk["|p1.B_2.r|^2", sq[contr1[G2]]];
chk["|r.B_1.p2|^2", sq[contr2[G1]]]; chk["|r.B_2.p2|^2", sq[contr2[G2]]];

(* ::Section:: *)
(*the Feynman-rule vertex and the ghost*)


Print["--- Feynman-rule vertex: -g sums exceed S_kl by 4 tau1 tau2 (1,-1)x(1,-1); ghost per colour component removes it"];
chk["S11^F(-g) - S11 - 4 tau1 tau2", pair[G1F, G1F] - S11 - 4 tau1 tau2v];
chk["S22^F(-g) - S22 - 4 tau1 tau2", pair[G2F, G2F] - S22 - 4 tau1 tau2v];
chk["S12^F(-g) - S12 + 4 tau1 tau2", pair[G1F, G2F] - S12 + 4 tau1 tau2v];
(* ghost: w = (g^2/s) ubar p1slash v per colour component (w_1 = w, w_2 = -w); 2 sum|w|^2 = 4 tau1 tau2 *)
chk["2 sum|ubar p1 v|^2 - 4 tau1 tau2", 2 tr[(GS[k1] + mm) . GS[p1] . (GS[k2] - mm) . GS[p1]] - 4 tau1 tau2v];

(* ::Section:: *)
(*physical polarization sums*)


Print["--- physical polarization sums with P = -g + (p1 p2 + p2 p1)/(p1.p2) for both gluons, Feynman-rule vertex"];
P[a_, b_] := -MT[a, b] + (FV[p1, a] FV[p2, b] + FV[p2, a] FV[p1, b])/(1/2);
phys[gx_, gy_] := tr[(GS[k1] + mm) . gx[mu, nu] . (GS[k2] - mm) . rev[gy[mu2, nu2]] P[mu, mu2] P[nu, nu2]];
chk["S11(phys) - 8F tau2/tau1", phys[G1F, G1F] - 8 F tau2v/tau1];
chk["S12(phys) - 8F", phys[G1F, G2F] - 8 F];
chk["S22(phys) - 8F tau1/tau2", phys[G2F, G2F] - 8 F tau1/tau2v];

(* ::Section:: *)
(*the colour sum*)


Print["--- colour sum: C_F d_F [C_F(S11+S22+2S12) - C_A S12] = Eq. (sumtree) (B) with T_F = 1/2, d_F = N"];
CFv = (CA^2 - 1)/(2 CA);
chk["sum|M_B|^2 - 8 CA CF (CF/(tau1 tau2) - CA) F", CFv CA (CFv (S11 + S22 + 2 S12) - CA S12) - 8 CA CFv (CFv/(tau1 tau2v) - CA) F];
chk["N CF^2 (S11+S22) - CF S12 (form used in app:ir) - same", CA CFv^2 (S11 + S22) - CFv S12 - 8 CA CFv (CFv/(tau1 tau2v) - CA) F];