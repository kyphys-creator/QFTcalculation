(* ::Package:: *)

(* ::Title:: *)
(*Step (9) of the CKM note: this note's flavour-changing loop amplitudes squared, as MadLoop computes loop-induced processes*)


(* ::Text:: *)
(*MadLoop computes a loop-induced process ([sqrvirt=QED]) from the loop diagrams, the R2 vertices and the UV vertices of*)
(*the UFO, which have empty loop_particles and are attached to every loop of their topology (nlo_ckm_ufo.wl): for b -> s*)
(*gamma and Z -> b sbar these are the vertices gamma sbar b, Z sbar b of the off-diagonal on-shell field constants, i.e. the*)
(*LSZ factors of the external legs.  MadLoop drops the self-energies on the external legs (madgraph/loop), so the result is*)
(*the on-shell amplitude: the 1PI vertex plus the legs, UV finite and independent of MU_R (checked).  The references from*)
(*this note's amplitudes (Feynman gauge; the totals do not depend on the gauge, step (7)):*)
(*  (a) Z(k) -> b(p1) sbar(p2) on shell, m_s = 0: the 1PI form factors of step (7) (work/fcnc_zbs.m) plus the external legs*)
(*      with the off-diagonal constants for m_s = 0 (fcnc_ckm_numeric.wl), LoopTools at mu (Z -> u ubar, c cbar open);*)
(*      summed over spins, the three Z polarizations (-g + k k/MZ^2) averaged, colours summed (3);*)
(*  (b) b(p1) -> s(p2) gamma(q), m_s = 0: the same from work/fcnc_bsg.m (Feynman-parameter integrals at 40 digits, as*)
(*      fcnc_ckm_numeric.wl), the b spin averaged; the photon polarizations of MadLoop (HELAS, transverse in the b rest*)
(*      frame: -g + (q p1 + p1 q)/(q.p1) - m_b^2 q q/(q.p1)^2), the same as any other sum for the gauge-invariant total;*)
(*  in (a), (b) the UV poles of the totals vanish (checked); the 1PI parts alone are also given (they have poles);*)
(*  (c) b(p1) sbar(p2) -> s(p3) bbar(p4), massless: the zero-momentum boxes of step (8) (work/df2_Bs.m: the direct and*)
(*      the crossed pairing separately, here equal and opposite), i.e. the amplitude [D] (d delta_31 delta_24 - c*)
(*      delta_34 delta_21), [D] = [ubar_3 gamma^mu P_L u_1][vbar_2 gamma_mu P_L v_4], summed over spins and colours,*)
(*      averaged (1/36).  MadLoop at sqrt(s) << m_c, MW approaches it as s/m^2.*)
(*Writes results/fcnc_madloop_ref.csv.  Batch:  wolframscript -file fcnc_madloop_ref.wl  (after the step (7), (8) scripts)*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
Get["FeynCalc`"];
$FCAdvice = False;
srcDirMF$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirMF$ = FileNameJoin[{srcDirMF$, "results"}];
workDirMF$ = FileNameJoin[{srcDirMF$, "work"}];
t0MF$ = AbsoluteTime[];
renMF$ = {A0 -> fA0$, B0 -> fB0$, C0 -> fC0$, D0 -> fD0$};
bsgMF$ = Get[FileNameJoin[{workDirMF$, "fcnc_bsg.m"}]] /. renMF$;
zbsMF$ = Get[FileNameJoin[{workDirMF$, "fcnc_zbs.m"}]] /. renMF$;
df2MF$ = Get[FileNameJoin[{workDirMF$, "df2_Bs.m"}]] /. renMF$;
(* the external legs of step (7) (fcnc_ckm_numeric.wl): Denner's off-diagonal constants for m_s = 0 from the down-type
   self-energies of step (3) (1PI + tadpole, electroweak); n = 1 SL, 2 SR, 3 SSL, 4 SSR *)
sig3MF$ = Association[Get[FileNameJoin[{resDirMF$, "oneloop_ckm_sigma.m"}]]] /. renMF$;
toCKMF$ = {vR[i_, j_] :> (cK[i, j] + cKc[i, j])/2, vI[i_, j_] :> (cK[i, j] - cKc[i, j])/(2 I)};
kRuleMF$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
conjMF$[x_] := x /. {cK -> cKtmp$, cKc -> cK} /. cKtmp$ -> cKc /. Complex[a_, b_] :> Complex[a, -b];
sdMF$[k_, j_, n_, p2_] := Total[sig3MF$["D"][[k, j, All, n]]] /. kRuleMF$ /. toCKMF$ /. gS -> 0 /. {MS -> 0, MD -> 0} /. kk2 -> p2;
dZLsbMF$ = -2 (sdMF$[2, 3, 1, MB^2] + sdMF$[2, 3, 4, MB^2]);
dZRsbMF$ = -2 sdMF$[2, 3, 2, MB^2];
dZLbsMF$ = 2 sdMF$[3, 2, 3, 0];
totBsgMF$ = bsgMF$["F"] + {bsgMF$["tree"][[1]] (dZLsbMF$ + conjMF$[dZLbsMF$])/2, bsgMF$["tree"][[2]] dZRsbMF$/2, 0, 0};
totZbsMF$ = zbsMF$["F"] + {zbsMF$["tree"][[1]] (dZLbsMF$ + conjMF$[dZLsbMF$])/2, zbsMF$["tree"][[2]] conjMF$[dZRsbMF$]/2, 0, 0};
KK = 16 Pi^2;
muMF$ = 91;
wpMF$ = 40;
(* the point: step (5)'s benchmark with m_u, m_d ten times larger (wud_madloop_ref.wl), m_s = 0 here *)
pointMF$ = {ee -> Sqrt[4 Pi/128], sw -> Sqrt[1881/8281], cw -> 80/91, MW -> 80, MZ -> 91, MH -> 125, MT -> 165,
   MB -> 286/100, MC -> 619/1000, MU -> 127/10000};
vStdMF$ = Module[{c12, c23, c13, s12 = 22501/100000, s23 = 4183/100000, s13 = 3732/1000000, dl = 1147/1000},
   {c12, c23, c13} = Sqrt[1 - {s12, s23, s13}^2];
   {{c12 c13, s12 c13, s13 Exp[-I dl]}, {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
    {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}}];
vNumMF$ = N[vStdMF$, wpMF$];
vRulesMF$ = {cK[i_, j_] :> vNumMF$[[i, j]], cKc[i_, j_] :> Conjugate[vNumMF$[[i, j]]]};
num$[x_] := N[x /. pointMF$, wpMF$];
rowsMF$ = {};
addMF$[name_, val_] := AppendTo[rowsMF$, {name, ToString[CForm[N[Re[val], 17]]], ToString[CForm[N[Im[val], 17]]]}];
sf$[x_] := ToString[CForm[N[x, 16]]];

(* the FeynArts units: the stored trees against the couplings *)
Print["trees / couplings (expect -1, -1 and -1, -1): b -> b gamma ", Simplify[bsgMF$["tree"][[1 ;; 2]]/(-ee/3)],
  ";  Z -> b bbar ", Simplify[(zbsMF$["tree"][[1 ;; 2]]/({-1/2 + sw^2/3, sw^2/3} ee/(sw cw))) /. cw -> Sqrt[1 - sw^2]]];


(* ::Section:: *)
(*Spin and polarization sums*)


(* the four structures {eps P_L, eps P_R, (eps.p1) P_L, (eps.p1) P_R} as Dirac matrices with the polarization index *)
gamMF$[mu_] := {GA[mu] . GA[7], GA[mu] . GA[6], FV[p1, mu] GA[7], FV[p1, mu] GA[6]};
gamBarMF$[mu_] := {GA[6] . GA[mu], GA[7] . GA[mu], FV[p1, mu] GA[6], FV[p1, mu] GA[7]};
(* (a) Z -> b(p1) sbar(p2): sum u ubar = p1slash + m_b, v vbar = p2slash; polarization sum -g + k k/MZ^2 *)
FCClearScalarProducts[];
SP[p1, p1] = mb2; SP[p2, p2] = 0; SP[p1, p2] = (mz2 - mb2)/2;
polZ$ = -MT[li1, li2] + (FV[p1, li1] + FV[p2, li1]) (FV[p1, li2] + FV[p2, li2])/mz2;
matZ$ = Table[Contract[polZ$ DiracTrace[(GS[p1] + Sqrt[mb2]) . gamMF$[li1][[n]] . GS[p2] . gamBarMF$[li2][[m]], DiracTraceEvaluate -> True]],
   {n, 4}, {m, 4}] // Simplify;
(* (b) b(p1) -> s(p2) gamma(q): sum u_s ubar_s = p2slash, u_b ubar_b = p1slash + m_b; q = p1 - p2; the photon polarizations
   of the b rest frame *)
FCClearScalarProducts[];
SP[p1, p1] = mb2; SP[p2, p2] = 0; SP[p1, p2] = mb2/2;
qv$[li_] := FV[p1, li] - FV[p2, li];
polA$ = -MT[li1, li2] + (qv$[li1] FV[p1, li2] + FV[p1, li1] qv$[li2])/(mb2/2) - mb2 qv$[li1] qv$[li2]/(mb2/2)^2;
matA$ = Table[Contract[polA$ DiracTrace[GS[p2] . gamMF$[li1][[n]] . (GS[p1] + Sqrt[mb2]) . gamBarMF$[li2][[m]], DiracTraceEvaluate -> True]],
   {n, 4}, {m, 4}] // Simplify;
Print["spin sums: Z -> b sbar ", ToString[InputForm[matZ$[[1, 1]]]], " ...;  b -> s gamma ", ToString[InputForm[matA$[[1, 1]]]], " ..."];
(* (c) [D] = [ubar_3 gamma^mu P_L u_1][vbar_2 gamma_mu P_L v_4], massless *)
FCClearScalarProducts[];
spinD$ = Contract[DiracTrace[GS[p3] . GA[li1] . GA[7] . GS[p1] . GA[6] . GA[li2], DiracTraceEvaluate -> True]
     DiracTrace[GS[p2] . GA[li1] . GA[7] . GS[p4] . GA[6] . GA[li2], DiracTraceEvaluate -> True]] // Simplify;
spinDStr$ = ToString[InputForm[FCE[spinD$] /. SP[a_, b_] :> sp[a, b]]];
Print["sum_spins |[D]|^2 = ", spinDStr$];


(* ::Section:: *)
(*Numbers*)


Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetMudim[N[muMF$^2]]; SetDelta[0.];
laurMF$[x_] := Module[{y = x /. {fA0$[m2_] :> m2/ep + a0f$[m2], fB0$[pp_, a_, b_] :> 1/ep + b0f$[pp, a, b], fC0$[a__] :> c0f$[a]} /.
      D -> 4 - 2 ep}, {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];
a0v$[m2_] := If[m2 == 0, 0, m2 (1 - Log[m2/muMF$^2])];
(* (a) LoopTools (double precision; Z -> u ubar, c cbar are open) *)
ltMF$[x_] := laurMF$[N[x /. vRulesMF$ /. pointMF$, 30]] /. {a0f$[m2_] :> a0v$[m2], b0f$[pp_, a_, b_] :> LoopTools`B0[pp, a, b],
     c0f$[a__] :> LoopTools`C0[a]};
(* (b) 40 digits (fcnc_ckm_numeric.wl): B0 below threshold and C0 with one zero invariant by a one-dimensional integral *)
b0hp$[ps_, a_, b_] := b0hp$[ps, a, b] = If[a == 0 && b == 0, 0,
    -NIntegrate[Log[(x a + (1 - x) b - x (1 - x) ps)/muMF$^2], {x, 0, 1}, WorkingPrecision -> wpMF$, PrecisionGoal -> wpMF$ - 8, MaxRecursion -> 40]];
c0lin$[p1s_, p12s_, m0_, m1_, m2_] := Module[{a, b},
   a = (1 - x) m0 + x m1 - x (1 - x) p1s; b = m2 - m0 + x (p1s - p12s);
   If[(m2 - m0) == 0 && (p1s - p12s) == 0, -NIntegrate[(1 - x)/a, {x, 0, 1}, WorkingPrecision -> wpMF$, PrecisionGoal -> wpMF$ - 8, MaxRecursion -> 40],
    -NIntegrate[Log[(a + b (1 - x))/a]/b, {x, 0, 1}, WorkingPrecision -> wpMF$, PrecisionGoal -> wpMF$ - 8, MaxRecursion -> 40]]];
c0hp$[p1s_, p12s_, p2s_, m0_, m1_, m2_] := c0hp$[p1s, p12s, p2s, m0, m1, m2] = Which[
    p2s == 0, c0lin$[p1s, p12s, m0, m1, m2], p1s == 0, c0lin$[p2s, p12s, m0, m2, m1], True, Indeterminate];
hpMF$[x_] := laurMF$[N[x /. vRulesMF$ /. pointMF$, 60]] /. {a0f$[m2_] :> N[a0v$[m2], wpMF$], b0f$[pp_, a_, b_] :> b0hp$[pp, a, b],
     c0f$[a__] :> c0hp$[a]};
xi1MF$ = {xiW -> 1, xiA -> 1, xiZ -> 1, xiG -> 1, xiA -> 1};
(* sum over n, m of A_n A_m^* mat_nm, for the three Laurent combinations *)
sqMF$[ff_, mat_] := Module[{am = ff[[All, 1]]/KK, a0 = ff[[All, 2]]/KK},
   {Re[a0 . mat . Conjugate[a0]], 2 Re[a0 . mat . Conjugate[am]], Re[am . mat . Conjugate[am]]}];
zMat$ = N[matZ$ /. {mb2 -> MB^2, mz2 -> MZ^2} /. pointMF$, 30];
bMat$ = N[matA$ /. mb2 -> MB^2 /. pointMF$, wpMF$];
Do[Module[{zFF, bFF, zRes, bRes},
   zFF = ltMF$[# /. kk -> MZ^2 /. MA -> 0 /. xi1MF$] & /@ ff[[1]];
   bFF = hpMF$[# /. MA -> 0 /. xi1MF$] & /@ ff[[2]];
   zRes = sqMF$[zFF, zMat$] 3/3;   (* colours summed (3), Z polarizations averaged (1/3) *)
   bRes = sqMF$[bFF, bMat$]/2;     (* b spin averaged; colour: averaged 1/3, summed 3 *)
   Print[ff[[3]], ", mu = ", muMF$, ":  Z -> b sbar |M|^2 finite ", sf$[zRes[[1]]], ", 1eps ", sf$[zRes[[2]]], ", 2eps ", sf$[zRes[[3]]],
     ";  b -> s gamma finite ", sf$[bRes[[1]]], ", 1eps ", sf$[bRes[[2]]], ", 2eps ", sf$[bRes[[3]]]];
   Do[addMF$["zbs_" <> ff[[4]] <> {"finite", "1eps", "2eps"}[[n]], zRes[[n]]]; addMF$["bsg_" <> ff[[4]] <> {"finite", "1eps", "2eps"}[[n]], bRes[[n]]], {n, 3}];
   Do[addMF$["zbs_" <> ff[[4]] <> "KF" <> ToString[n] <> "_" <> {"pole", "fin"}[[l]], zFF[[n, l]]];
     addMF$["bsg_" <> ff[[4]] <> "KF" <> ToString[n] <> "_" <> {"pole", "fin"}[[l]], bFF[[n, l]]], {n, 4}, {l, 2}]],
  {ff, {{totZbsMF$, totBsgMF$, "(a), (b) on shell (1PI + legs)", ""}, {zbsMF$["F"], bsgMF$["F"], "    the 1PI vertex alone", "1PI_"}}}];

(* (c) the zero-momentum boxes: direct and crossed coefficients (K times, FeynArts units), A0 and B0(0, a, b) only; each
   is UV finite, but the poles of A0, B0 times D - 4 leave rational terms: the eps^0 coefficient is taken *)
b00v$[a_, b_] := Which[a == 0 && b == 0, 0, a == 0, 1 - Log[b/muMF$^2], b == 0, 1 - Log[a/muMF$^2], a == b, -Log[a/muMF$^2],
    True, 1 - (a Log[a/muMF$^2] - b Log[b/muMF$^2])/(a - b)];
(* the coefficients have 1/(xiW - 1): Feynman gauge as the limit xiW = 1 + 10^-20 at 80 digits; the CKM sum removes the
   xiW dependence (step (8)), checked with xiW = 2 *)
dcAtMF$[xw_] := Module[{y = {df2MF$["direct"], df2MF$["crossed"]}, l},
   If[! FreeQ[y, fC0$ | fD0$ | PaVe], Print["   WARNING: loop functions other than A0, B0 in the boxes"]];
   y = N[y /. xiW -> xw /. vRulesMF$ /. pointMF$ /. {MD -> 0, MS -> 0, MB -> 0}, 80];
   l = laurMF$ /@ y;
   {Abs[l[[All, 1]]], l[[All, 2]] /. {a0f$[m2_] :> a0v$[m2], b0f$[0, a_, b_] :> b00v$[a, b]}}];
dc1MF$ = dcAtMF$[1 + 10^-20]; dc2MF$ = dcAtMF$[2];
Print["(c) UV poles of the direct and crossed boxes (expect ~0): ", N[dc1MF$[[1]], 3], ";  xiW = 2 against 1 (relative, expect ~1e-20): ",
  N[Max[Abs[(dc2MF$[[2]] - dc1MF$[[2]])/dc1MF$[[2]]]], 3]];
dcMF$ = dc1MF$[[2]];
Print["(c) zero-momentum boxes, K x {direct, crossed} = ", dcMF$, ";  (direct + crossed)/direct (expect 0) ", Abs[Total[dcMF$]/dcMF$[[1]]]];
(* the full colour sum of |d delta_31 delta_24 - c delta_34 delta_21|^2 = 9|d|^2 + 9|c|^2 - 6 Re(d conj(c)) *)
colMF$ = (9 Abs[dcMF$[[1]]]^2 + 9 Abs[dcMF$[[2]]]^2 - 6 Re[dcMF$[[1]] Conjugate[dcMF$[[2]]]])/KK^2;
Print["(c) b sbar -> s bbar: sum |M|^2 / 36 = ", sf$[colMF$/36], " x (", spinDStr$, ")"];
addMF$["df2_colour_sum_over_36", colMF$/36];
addMF$["df2_direct_K", dcMF$[[1]]]; addMF$["df2_crossed_K", dcMF$[[2]]];
Export[FileNameJoin[{resDirMF$, "fcnc_madloop_ref.csv"}], Prepend[rowsMF$, {"quantity", "re", "im"}], "CSV"];
Print["written: results/fcnc_madloop_ref.csv;  ", Round[AbsoluteTime[] - t0MF$], " s"];
Uninstall[First[Select[Links[], StringContainsQ[First[#], "LoopTools"] &]]];
