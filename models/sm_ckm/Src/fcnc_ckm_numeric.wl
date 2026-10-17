(* ::Package:: *)

(* ::Title:: *)
(*Step (7) of the CKM note: b -> s gamma and Z -> b sbar with the external legs: UV finiteness, gauge invariance, GIM, Inami-Lim*)


(* ::Text:: *)
(*Reads work/fcnc_bsg.m, work/fcnc_zbs.m (fcnc_ckm_feyncalc.wl: K times the 1PI form factors {eps-slash P_L, eps-slash P_R,*)
(*(eps.p1) P_L, (eps.p1) P_R} in FeynArts units, and the flavour-diagonal trees) and the down-type quark self-energies of*)
(*step (3).  There is no tree-level flavour-changing coupling and no counterterm; the external legs give the on-shell*)
(*LSZ terms (the bare neutral coupling psibar_0 gamma (g_L P_L + g_R P_R) psi_0):*)
(*  b -> s gamma:  c^gamma_{L,R} (1/2) [dZ^{L,R}_sb + dZ^{L,R}_bs^*],   Z -> b sbar:  c^Z_{L,R} (1/2) [dZ^{L,R}_bs + dZ^{L,R}_sb^*],*)
(*with Denner's off-diagonal constants for m_s = 0: dZ^L_sb = -2 (Sigma^L + Sigma^S)_sb(m_b^2), dZ^L_bs = 2 Sigma^S_bs(0),*)
(*dZ^R_sb = -2 Sigma^R_sb(m_b^2), dZ^R_bs = 0 (dZ^R_ij = 2/(m_i^2 - m_j^2)[m_j^2 Sigma^R + m_i m_j Sigma^L + 2 m_i m_j Sigma^S]),*)
(*and c^{gamma,Z} the coefficients of the FeynArts*)
(*trees b -> b gamma, Z -> b bbar.  Checks:*)
(*  (a) exact UV finiteness of the total (rational unitary V, general xiW; Z -> b sbar for any k^2); the 1PI parts alone*)
(*      are UV divergent;*)
(*  (b) b -> s gamma at the benchmark, 40 digits (Feynman parameters; the kinematics has no threshold): the*)
(*      electromagnetic gauge invariance F_L + (m_b/2) H_R = 0, F_R + (m_b/2) H_L = 0; independence of xiW;*)
(*      GIM (equal up-type masses give zero);*)
(*  (c) the dipole H_R against the function D'_0(x) of Inami and Lim (C_7 = -D'_0/2, literature, reference only):*)
(*      K H_R / (g^2 e m_b/MW^2 sum_k lambda_k D'_0(x_k)) for several m_t, as m_b -> 0;*)
(*  (d) Z -> b sbar on shell (k^2 = MZ^2, LoopTools: Z -> u ubar, c cbar are open): independence of xiW; at k^2 = 0*)
(*      (k^2 = 10^-16 MZ^2, 40 digits) the Feynman-gauge F_L against C_0(x) of Inami and Lim, and its xiW dependence there.*)
(*Writes results/fcnc_ckm_numeric.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file fcnc_ckm_numeric.wl  (run fcnc_ckm_feyncalc.wl first; a few minutes).*)


(* ::Section:: *)
(*Setup*)


srcDirFC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirFC$ = FileNameJoin[{srcDirFC$, "results"}];
workDirFC$ = FileNameJoin[{srcDirFC$, "work"}];
t0FC$ = AbsoluteTime[];
renFC$ = {A0 -> fA0$, B0 -> fB0$, C0 -> fC0$};
bsg$ = Get[FileNameJoin[{workDirFC$, "fcnc_bsg.m"}]] /. renFC$;
zbs$ = Get[FileNameJoin[{workDirFC$, "fcnc_zbs.m"}]] /. renFC$;
sig3$ = Association[Get[FileNameJoin[{resDirFC$, "oneloop_ckm_sigma.m"}]]] /. renFC$;
KK = 16 Pi^2;
kRuleFC$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
toCKFC$ = {vR[i_, j_] :> (cK[i, j] + cKc[i, j])/2, vI[i_, j_] :> (cK[i, j] - cKc[i, j])/(2 I)};
light0FC$ = {MS -> 0, MD -> 0};
conjFC$[x_] := x /. {cK -> cKtmp$, cKc -> cK} /. cKtmp$ -> cKc /. Complex[a_, b_] :> Complex[a, -b];
(* K Sigma^n_kj(p^2) of the down-type quarks (1PI + tadpole, electroweak), n = 1 SL, 2 SR, 3 SSL, 4 SSR *)
sdFC$[k_, j_, n_, p2_] := Total[sig3$["D"][[k, j, All, n]]] /. kRuleFC$ /. toCKFC$ /. gS -> 0 /. light0FC$ /. kk2 -> p2;
(* s = 2, b = 3; Sigma^S_sb from SSR (divided by m_b), Sigma^S_bs from SSL (divided by m_b) *)
dZLsb$ = -2 (sdFC$[2, 3, 1, MB^2] + sdFC$[2, 3, 4, MB^2]);
(* the on-shell conditions Sigma-hat_ij(p) u_j(p) = 0 (p^2 = m_j^2) give dZ^L_ij of Eq. (dZos) and
   dZ^R_ij = 2/(m_i^2 - m_j^2) [m_j^2 Sigma^R_ij + m_i m_j Sigma^L_ij + 2 m_i m_j Sigma^S_ij]: with m_s = 0, dZ^R_sb = -2 Sigma^R_sb, dZ^R_bs = 0 *)
dZRsb$ = -2 sdFC$[2, 3, 2, MB^2];
dZLbs$ = 2 sdFC$[3, 2, 3, 0];
dZRbs$ = 0;
legsBsg$ = {bsg$["tree"][[1]] (dZLsb$ + conjFC$[dZLbs$])/2, bsg$["tree"][[2]] (dZRsb$ + conjFC$[dZRbs$])/2, 0, 0};
legsZbs$ = {zbs$["tree"][[1]] (dZLbs$ + conjFC$[dZLsb$])/2, zbs$["tree"][[2]] (dZRbs$ + conjFC$[dZRsb$])/2, 0, 0};
totBsg$ = bsg$["F"] + legsBsg$;
totZbs$ = zbs$["F"] + legsZbs$;
Print["trees: b -> b gamma ", bsg$["tree"], ";  Z -> b bbar ", zbs$["tree"]];
sfrFC$[x_, n_] := Module[{y = N[x], e}, If[y == 0, "0", e = Floor[Log10[Abs[y]]];
    ToString[NumberForm[y/10^e, n]] <> "e" <> ToString[e]]];
sfFC$[x_, n_ : 3] := If[Im[N[x]] == 0 || Abs[Im[N[x]]] < 10^-25 Abs[N[x]], sfrFC$[Re[x], n], "(" <> sfrFC$[Re[x], n] <> ", " <> sfrFC$[Im[x], n] <> " i)"];
rowsFC$ = {};
addFC$[name_, val_] := AppendTo[rowsFC$, {name, ToString[CForm[N[Re[val]]]], ToString[CForm[N[Im[val]]]]}];


(* ::Section:: *)
(*(a) UV finiteness (exact)*)


vStdFC$ = {
   {c12 c13, s12 c13, s13 Exp[-I dl]},
   {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
   {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}} /.
   {c12 -> Sqrt[1 - s12^2], c23 -> Sqrt[1 - s23^2], c13 -> Sqrt[1 - s13^2]};
vPyFC$ = vStdFC$ /. {s12 -> 8/17, s23 -> 7/25, s13 -> 3/5} /. Exp[I dl] -> ph /. Exp[-I dl] -> 1/ph;
vPycFC$ = vStdFC$ /. {s12 -> 8/17, s23 -> 7/25, s13 -> 3/5} /. Exp[I dl] -> 1/ph /. Exp[-I dl] -> ph;
explicitFC$ = {cK[i_, j_] :> vPyFC$[[i, j]], cKc[i_, j_] :> vPycFC$[[i, j]]};
poleFC$[x_] := Simplify[Together[SeriesCoefficient[x /. {fA0$[m2_] :> m2/ep, fB0$[__] -> 1/ep, fC0$[__] -> 0} /. D -> 4 - 2 ep,
       {ep, 0, -1}] /. explicitFC$ /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2]], 0 < sw < 1 && MW > 0];
uvFC$ = {poleFC$ /@ totBsg$, poleFC$ /@ totZbs$};
uv1PIFC$ = {poleFC$ /@ bsg$["F"][[1 ;; 2]], poleFC$ /@ zbs$["F"][[1 ;; 2]]};
Print["(a) UV poles of K {F_L, F_R, H_L, H_R} with the legs: b -> s gamma ", uvFC$[[1]], ";  Z -> b sbar ", uvFC$[[2]],
  "   (expect all 0)"];
Print["(a) the 1PI F_L alone has a pole (expect True, True): ", (uv1PIFC$[[#, 1]] =!= 0) & /@ {1, 2}, ";  ",
  Round[AbsoluteTime[] - t0FC$], " s"];


(* ::Section:: *)
(*High-precision loop functions (real kinematics)*)


muFC$ = 91;
wpFC$ = 40;
(* B0 finite part (Delta = 0), below threshold *)
b0hp$[ps_, a_, b_] := b0hp$[ps, a, b] = If[a == 0 && b == 0, If[ps == 0, 0, Print["   B0(p^2, 0, 0) with p^2 != 0"]; Indeterminate],
    -NIntegrate[Log[(x a + (1 - x) b - x (1 - x) ps)/muFC$^2], {x, 0, 1}, WorkingPrecision -> wpFC$, PrecisionGoal -> wpFC$ - 8]];
(* C0 = -int dx dy / Delta (LoopTools' convention; checked against LoopTools), with one of p1s, p2s zero: the y integral in closed form *)
c0hp$[p1s_, p12s_, p2s_, m0_, m1_, m2_] := c0hp$[p1s, p12s, p2s, m0, m1, m2] = Which[
    p2s == 0, c0lin$[p1s, p12s, m0, m1, m2],
    p1s == 0, c0lin$[p2s, p12s, m0, m2, m1],
    True, Print["   no closed y integral for ", {p1s, p12s, p2s}]; Indeterminate];
c0lin$[p1s_, p12s_, m0_, m1_, m2_] := Module[{a, b, r},
   a = (1 - x) m0 + x m1 - x (1 - x) p1s;  (* Delta at y = 0 *)
   b = m2 - m0 + x (p1s - p12s);          (* d Delta/dy *)
   r = If[(m2 - m0) == 0 && (p1s - p12s) == 0,
    -NIntegrate[(1 - x)/a, {x, 0, 1}, WorkingPrecision -> wpFC$, PrecisionGoal -> wpFC$ - 8],
    -NIntegrate[Log[(a + b (1 - x))/a]/b, {x, 0, 1}, WorkingPrecision -> wpFC$, PrecisionGoal -> wpFC$ - 8]];
   If[! NumericQ[r], Print["   C0 not numeric: ", N[{p1s, p12s, m0, m1, m2}, 6]]];
   r];
(* {pole, finite} of an expression with numbers (exact rationals); finite part MS-bar at mu = MZ *)
hpFC$[x_] := Module[{y = x /. {fA0$[m2_] :> m2/ep + a0f$[m2], fB0$[pp_, a_, b_] :> 1/ep + b0f$[pp, a, b],
        fC0$[a__] :> c0f$[a]} /. D -> 4 - 2 ep, l},
   l = {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]};
   l /. {a0f$[m2_] :> If[m2 == 0, 0, N[m2 (1 - Log[m2/muFC$^2]), wpFC$]], b0f$[pp_, a_, b_] :> b0hp$[pp, a, b],
     c0f$[a__] :> c0hp$[a]}];
vNumFC$ = N[vStdFC$ /. {s12 -> 22501/100000, s23 -> 4183/100000, s13 -> 3732/1000000, dl -> 1147/1000}, wpFC$];
vRulesFC$ = {cK[i_, j_] :> vNumFC$[[i, j]], cKc[i_, j_] :> Conjugate[vNumFC$[[i, j]]]};
benchFC$ = {ee -> Sqrt[4 Pi/128], sw -> Sqrt[1881/8281], cw -> 80/91, MW -> 80, MZ -> 91, MH -> 125, MT -> 165,
   MB -> 286/100, MC -> 619/1000, MU -> 127/100000, MTA -> 1746/1000, MMU -> 1027/10000, Me -> 487/1000000};
(* evaluate a list of form factors at a parameter point (rules override the benchmark) *)
evalHP$[ffs_, rules_] := hpFC$[N[# /. vRulesFC$ /. rules /. benchFC$, 60]] & /@ ffs;
lamFC$[k_] := Conjugate[vNumFC$[[k, 2]]] vNumFC$[[k, 3]];     (* V*_ks V_kb *)


(* ::Section:: *)
(*(b) b -> s gamma at the benchmark*)


xisFC$ = {1, 1/2, 2, 3, 10};
bsgXi$ = Table[evalHP$[totBsg$, {xiW -> xw, xiA -> 1, xiZ -> 1}][[All, 2]], {xw, xisFC$}];
Print["(b) b -> s gamma, K {F_L, F_R, H_L, H_R} at xiW = 1: ", sfFC$ /@ bsgXi$[[1]], ";  ", Round[AbsoluteTime[] - t0FC$], " s"];
gaugeInvFC$ = Max[Table[Abs[{r[[1]] + 143/100 r[[4]], r[[2]] + 143/100 r[[3]]}], {r, bsgXi$}]]/Abs[143/100 bsgXi$[[1, 4]]];
Print["(b) electromagnetic gauge invariance: max |F_L + (m_b/2) H_R|, |F_R + (m_b/2) H_L| over the gauges, relative to |(m_b/2) H_R| ",
  "(expect ~1e-30): ", sfFC$[gaugeInvFC$]];
xiSpreadFC$ = Max[Abs[Flatten[Table[bsgXi$[[n]] - bsgXi$[[1]], {n, 2, Length[xisFC$]}]]]]/Abs[bsgXi$[[1, 4]]];
Print["(b) xiW = 1/2, 2, 3, 10 against 1: max |difference| of the four form factors relative to |H_R| (expect ~1e-30): ", sfFC$[xiSpreadFC$]];
(* the parts: the 1PI dipole and the 1PI F_L depend on xiW separately? *)
bsg1PIXi$ = Table[evalHP$[bsg$["F"], {xiW -> xw, xiA -> 1, xiZ -> 1}][[All, 2]], {xw, {1, 3}}];
Print["(b) the 1PI parts at xiW = 3 against 1: F_L ", sfFC$[Abs[bsg1PIXi$[[2, 1]] - bsg1PIXi$[[1, 1]]]/Abs[bsg1PIXi$[[1, 1]]]],
  ", H_R ", sfFC$[Abs[bsg1PIXi$[[2, 4]] - bsg1PIXi$[[1, 4]]]/Abs[bsg1PIXi$[[1, 4]]]], " (relative)"];
gimFC$ = evalHP$[totBsg$, {xiW -> 1, xiA -> 1, xiZ -> 1, MU -> 165, MC -> 165}][[All, 2]];
Print["(b) GIM: all up-type masses equal (165 GeV): |form factors| / |H_R(benchmark)| (expect ~1e-30): ",
  sfFC$[Max[Abs[gimFC$]]/Abs[bsgXi$[[1, 4]]]]];
addFC$["bsg_KHR_bench", bsgXi$[[1, 4]]]; addFC$["bsg_KFL_bench", bsgXi$[[1, 1]]];
addFC$["bsg_gauge_invariance_rel", gaugeInvFC$]; addFC$["bsg_xi_spread_rel", xiSpreadFC$];


(* ::Section:: *)
(*(c) The dipole against Inami-Lim*)


dp0FC$[x_] := -(8 x^3 + 5 x^2 - 7 x)/(12 (1 - x)^3) + x^2 (2 - 3 x) Log[x]/(2 (1 - x)^4);
(* K H_R / (g^2 e m_b/MW^2 sum_k lambda_k D'_0(x_k)) *)
ilRatioFC$[mt_, mb_] := Module[{hr, norm},
   hr = evalHP$[{totBsg$[[4]]}, {xiW -> 1, xiA -> 1, xiZ -> 1, MT -> mt, MB -> mb}][[1, 2]];
   norm = N[(ee^2/sw^2) ee mb/MW^2 Sum[lamFC$[k] dp0FC$[{MU, MC, mt}[[k]]^2/MW^2], {k, 3}] /. benchFC$, wpFC$];
   hr/norm];
ilFC$ = Table[{mt, mb, ilRatioFC$[mt, mb]}, {mt, {100, 165, 300}}, {mb, {286/100, 143/100, 286/1000}}];
Print["(c) K H_R / (g^2 e m_b/MW^2 sum lambda_k D'_0(x_k)) (rows m_t = 100, 165, 300; columns m_b = 2.86, 1.43, 0.286):"];
Do[Print["   ", row[[1, 1]], ": ", StringRiffle[(ToString[NumberForm[Re[#[[3]]], 10]] <> " (Im " <> sfFC$[Im[#[[3]]], 2] <> ")") & /@ row, ",  "]],
  {row, ilFC$}];
Do[addFC$["bsg_IL_ratio_mt" <> ToString[N[r[[1]]]] <> "_mb" <> ToString[N[r[[2]]]], r[[3]]], {r, Flatten[ilFC$, 1]}];


(* ::Section:: *)
(*(d) Z -> b sbar*)


Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetMudim[N[muFC$^2]]; SetDelta[0.];
(* the 40-digit C0 and B0 of (b), (c) against LoopTools (double precision) *)
memoArgsFC$[f_] := Cases[DownValues[f], HoldPattern[_[f[a__]] :> _?NumericQ] :> {a}];
ltCheckFC$ = Max[Join[Abs[(c0hp$ @@ # - LoopTools`C0 @@ N[#])/(c0hp$ @@ #)] & /@ Take[memoArgsFC$[c0hp$], UpTo[40]],
    Abs[(b0hp$ @@ # - LoopTools`B0 @@ N[#])/(b0hp$ @@ #)] & /@ Select[Take[memoArgsFC$[b0hp$], UpTo[40]], b0hp$ @@ # != 0 &]]];
Print["(d) the 40-digit C0, B0 used above against LoopTools: max relative difference ", sfFC$[ltCheckFC$], " (LoopTools' precision)"];
addFC$["hp_vs_looptools_maxrel", ltCheckFC$];
ltFC$[x_] := Module[{y = N[x /. vRulesFC$ /. benchFC$, 30] /. {fA0$[m2_] :> m2/ep + a0f$[m2], fB0$[pp_, a_, b_] :> 1/ep + b0f$[pp, a, b],
        fC0$[a__] :> c0f$[a]} /. D -> 4 - 2 ep, l},
   l = {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]};
   l /. {a0f$[m2_] :> If[m2 == 0, 0, m2 (1 - Log[m2/muFC$^2])], b0f$[pp_, a_, b_] :> LoopTools`B0[pp, a, b],
     c0f$[a__] :> LoopTools`C0[a]}];
zbsOS$ = Table[ltFC$[# /. {kk -> MZ^2, xiW -> xw, xiA -> 1, xiZ -> 1}][[2]] & /@ totZbs$, {xw, xisFC$}];
zbsSpread$ = Max[Abs[Flatten[Table[zbsOS$[[n]] - zbsOS$[[1]], {n, 2, Length[xisFC$]}]]]]/Abs[zbsOS$[[1, 1]]];
Print["(d) Z -> b sbar on shell, K {F_L, F_R, H_L, H_R} at xiW = 1: ", sfFC$ /@ zbsOS$[[1]],
  ";  xiW dependence relative to |F_L| (expect ~1e-12): ", sfFC$[zbsSpread$]];
zbs1PIOS$ = Table[ltFC$[zbs$["F"][[1]] /. {kk -> MZ^2, xiW -> xw, xiA -> 1, xiZ -> 1}][[2]], {xw, {1, 3}}];
Print["(d) the 1PI F_L alone at xiW = 3 against 1 (relative): ", sfFC$[Abs[zbs1PIOS$[[2]] - zbs1PIOS$[[1]]]/Abs[zbs1PIOS$[[1]]]]];
addFC$["zbs_KFL_onshell", zbsOS$[[1, 1]]]; addFC$["zbs_xi_spread_onshell_rel", zbsSpread$];
(* the on-shell value in the units of the Inami-Lim Z penguin (Feynman gauge, k^2 = 0) *)
c0ILFC$[x_] := x/8 ((x - 6)/(x - 1) + (3 x + 2) Log[x]/(x - 1)^2);
zbsOSnorm$ = N[-2 (ee/sw)^3/cw Sum[Conjugate[lamFC$[k]] c0ILFC$[{MU, MC, MT}[[k]]^2/MW^2], {k, 3}] /. benchFC$, 20];
Print["(d) on shell: K F_L / (-2 g^3/c_W sum lambda_k^* C_0(x_k)) = ", sfFC$[zbsOS$[[1, 1]]/zbsOSnorm$, 6], "   (gauge independent)"];
addFC$["zbs_onshell_over_C0", zbsOS$[[1, 1]]/zbsOSnorm$];
(* k^2 = 0 (40 digits): the Feynman-gauge F_L against C_0(x) of Inami and Lim *)
c0ILFC$[x_] := x/8 ((x - 6)/(x - 1) + (3 x + 2) Log[x]/(x - 1)^2);
(* the form factors have 1/k^2 terms that cancel as k^2 -> 0: k^2 = 10^-16 MZ^2 in the 60-digit arithmetic *)
kk0FC$ = 8281/10^16;
zbs0$[mt_, mb_, xw_] := evalHP$[{totZbs$[[1]]}, {kk -> kk0FC$, xiW -> xw, xiA -> 1, xiZ -> 1, MT -> mt, MB -> mb}][[1, 2]];
zbsIL$ = Table[Module[{fl = zbs0$[mt, mb, 1], norm},
     (* Z -> b sbar carries V*_kb V_ks = lambda_k^* *)
     norm = N[2 (ee/sw)^3/cw Sum[Conjugate[lamFC$[k]] c0ILFC$[{MU, MC, mt}[[k]]^2/MW^2], {k, 3}] /. benchFC$, wpFC$];
     {mt, mb, fl/norm}], {mt, {100, 165, 300}}, {mb, {286/100, 143/100, 286/1000}}];
Print["(d) k^2 = 0, Feynman gauge: K F_L / (2 g^3/c_W sum lambda_k^* C_0(x_k)) (rows m_t = 100, 165, 300; columns m_b = 2.86, 1.43, 0.286):"];
Do[Print["   ", row[[1, 1]], ": ", StringRiffle[(ToString[NumberForm[Re[#[[3]]], 10]] <> " (Im " <> sfFC$[Im[#[[3]]], 2] <> ")") & /@ row, ",  "]],
  {row, zbsIL$}];
zbs0Xi$ = Table[zbs0$[165, 286/100, xw], {xw, {1, 3}}];
Print["(d) k^2 = 0: F_L at xiW = 3 against 1 (relative; the off-shell Z penguin depends on the gauge, expect nonzero): ",
  sfFC$[Abs[zbs0Xi$[[2]] - zbs0Xi$[[1]]]/Abs[zbs0Xi$[[1]]]]];
Do[addFC$["zbs_IL_ratio_mt" <> ToString[N[r[[1]]]] <> "_mb" <> ToString[N[r[[2]]]], r[[3]]], {r, Flatten[zbsIL$, 1]}];
addFC$["zbs_k0_xi3_vs_1_rel", Abs[zbs0Xi$[[2]] - zbs0Xi$[[1]]]/Abs[zbs0Xi$[[1]]]];


(* ::Section:: *)
(*Output*)


Export[FileNameJoin[{resDirFC$, "fcnc_ckm_numeric.csv"}], Prepend[rowsFC$, {"quantity", "re", "im"}], "CSV"];
Print["Summary: UV ", Union[Flatten[uvFC$]], ";  b -> s gamma gauge invariance ", sfFC$[gaugeInvFC$], ", xi ", sfFC$[xiSpreadFC$],
  ";  Z -> b sbar on-shell xi ", sfFC$[zbsSpread$], ";  total ", Round[AbsoluteTime[] - t0FC$], " s"];
