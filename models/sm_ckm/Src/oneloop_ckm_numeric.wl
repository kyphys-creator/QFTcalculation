(* ::Package:: *)

(* ::Title:: *)
(*Step (3) of the CKM note: finite parts of the quark self-energy matrices, the Denner-Sack counterterm, and the CKM shifts (LoopTools)*)


(* ::Text:: *)
(*Reads results/oneloop_ckm_sigma.m (K Sigma from oneloop_ckm_feyncalc.wl, A0, B0 with D kept).  At the benchmark of the*)
(*note (mu = MZ = 91 GeV, Eq. (bench) for V):*)
(*  (f) the off-diagonal entries Sigma^{L,R,S}_ij(m_j^2) (1PI; MS-bar finite parts) for xiW = 1/2, 2, 3;*)
(*  (g) the on-shell off-diagonal field constants delta Z^L_ij, Eq. (dZos) (real part of the loop integrals, SSL = SSR*)
(*      checked in oneloop_ckm_feyncalc.wl), and the Denner-Sack counterterm delta V^DS, Eq. (dVds): the UV pole against*)
(*      (1/2) K dV/dln mu of Eq. (Vrun) (MS-bar delta V, Eq. (dV)), unitarity V^dagger dV + dV^dagger V = 0, and the xiW*)
(*      dependence of the finite part;*)
(*  (h) the exact CKM shifts (V of Eq. (bench) minus V = 1) of DeltaHat (Sigma_T^WW(0)/MW^2), the W pole mass and the*)
(*      top pole mass, against the SM note's estimate models/sm/Src/results/ckm_estimate.csv.*)
(*Finite parts: A0(m^2) = m^2/eps + a0f, B0 = 1/eps + b0f, D = 4 - 2 eps, coefficient of eps^0; a0f = m^2 (1 - ln(m^2/mu^2)),*)
(*b0f = LoopTools' B0 with Delta = 0.  Writes results/oneloop_ckm_numeric.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_ckm_numeric.wl  (run oneloop_ckm_feyncalc.wl first).*)


(* ::Section:: *)
(*Setup*)


srcDirON$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirON$ = FileNameJoin[{srcDirON$, "results"}];
(* rename A0, B0 at once: LoopTools' A0, B0 would shadow them (environment, SM2) *)
sig$ = Association[Get[FileNameJoin[{resDirON$, "oneloop_ckm_sigma.m"}]]] /. {A0 -> fA0$, B0 -> fB0$};
smEst$ = Association[Rule @@@ Rest[Import[FileNameJoin[{ParentDirectory[srcDirON$], "..", "sm", "Src", "results",
       "ckm_estimate.csv"}], "CSV"]]];
KK = 16 Pi^2;
kRuleON$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};

muB$ = 91;
benchON$ = {ee -> Sqrt[4 Pi/128], sw -> Sqrt[1881/8281], cw -> 80/91, MW -> 80, MZ -> 91, MH -> 125, MT -> 165,
   MB -> 286/100, MC -> 619/1000, MS -> 546/10000, MD -> 271/100000, MU -> 127/100000, MTA -> 1746/1000,
   MMU -> 1027/10000, Me -> 487/1000000, gS -> Sqrt[4 Pi 118/1000], CF -> 4/3, CA -> 3, xiA -> 1, xiZ -> 1, xiG -> 1};
upB$ = {127/100000, 619/1000, 165}; dnB$ = {271/100000, 546/10000, 286/100};
vevB$ = 2 80 Sqrt[1881/8281]/Sqrt[4 Pi/128];
vStdON$ = N[{
    {c12 c13, s12 c13, s13 Exp[-I dl]},
    {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
    {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}} /.
    {c12 -> Sqrt[1 - s12^2], c23 -> Sqrt[1 - s23^2], c13 -> Sqrt[1 - s13^2]} /.
    {s12 -> 22501/100000, s23 -> 4183/100000, s13 -> 3732/1000000, dl -> 1147/1000}, 30];
vNumON$ = {vR[i_, j_] :> Re[vStdON$[[i, j]]], vI[i_, j_] :> Im[vStdON$[[i, j]]]};
unitON$ = {vR[i_, j_] :> If[i == j, 1, 0], vI[__] -> 0};

(* Laurent coefficients {1/eps, eps^0} of a number-valued expression in fA0, fB0, D *)
laurON$[x_] := Module[{y = x /. {fA0$[m2_] :> m2/ep + a0f$[m2], fB0$[pp_, a_, b_] :> 1/ep + b0f$[pp, a, b]} /. D -> 4 - 2 ep},
   {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];

Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetDelta[0.]; SetMudim[N[muB$^2]];
(* re = True: real part of the loop integrals only (the Re-tilde of Eq. (dZos)) *)
evalON$[x_, re_] := x /. a0f$[m2_] :> If[m2 == 0, 0, N[m2 (1 - Log[m2/muB$^2])]] /.
   b0f$[pp_, a_, b_] :> If[re, Re[LoopTools`B0[N[pp], N[a], N[b]]], LoopTools`B0[N[pp], N[a], N[b]]];
(* K Sigma entry n (1 SL, 2 SR, 3 SSL, 4 SSR) of the 1PI part, at k^2 = p2, for a value of xiW: {UV, finite} *)
entryON$[sec_, i_, j_, n_, p2_, xw_] := laurON$[N[sig$[sec][[i, j, 1, n]] /. kRuleON$ /. kk2 -> p2 /. benchON$ /.
      xiW -> xw /. vNumON$, 30] /. MA -> 0];
sfON$[x_, n_ : 4] := Module[{y = N[x], e}, If[y == 0, "0", e = Floor[Log10[Abs[y]]];
    ToString[NumberForm[y/10^e, n]] <> "e" <> ToString[e]]];
rowsOut$ = {};
addOut$[name_, val_] := AppendTo[rowsOut$, {name, ToString[CForm[N[val]]]}];


(* ::Section:: *)
(*(f) Off-diagonal finite parts and xiW*)


xisON$ = {1/2, 2, 3, 10};
Print["(f) off-diagonal 1PI entries at p^2 = m_j^2, real part of the MS-bar finite part of K Sigma (xiW = 1/2, 2, 3, 10):"];
Do[Module[{ms = If[sec === "D", dnB$, upB$], vals},
    vals = Table[Re[evalON$[entryON$[sec, ij[[1]], ij[[2]], n, ms[[ij[[2]]]]^2, xw][[2]], False]], {n, {1, 2, 3}}, {xw, xisON$}];
    Print["   ", sec, ij, "  K SL: ", sfON$ /@ vals[[1]], "   K SR: ", sfON$ /@ vals[[2]], "   K SS: ", sfON$ /@ vals[[3]]];
    addOut$["KSL_fin_" <> sec <> ToString[ij[[1]]] <> ToString[ij[[2]]] <> "_xiW_half_2_3_10", vals[[1]]]],
  {sec, {"D", "U"}}, {ij, {{2, 3}, {1, 3}, {1, 2}}}];


(* ::Section:: *)
(*(g) Denner-Sack counterterm*)


(* delta Z^L_ij (i != j) of Eq. (dZos) from K Sigma: {UV, finite} for the given xiW; the diagonal is not needed *)
dZLON$[sec_, xw_] := Module[{ms = If[sec === "D", dnB$, upB$], z},
   z = Table[If[i == j, {0, 0}, Module[{sl, sr, ss, mi = ms[[i]], mj = ms[[j]]},
        {sl, sr, ss} = entryON$[sec, i, j, #, mj^2, xw] & /@ {1, 2, 3};
        (* UV parts carry no integrals; the finite parts take the real part of the loop integrals *)
        {(2/(mi^2 - mj^2)) (mj^2 sl[[1]] + mi mj sr[[1]] + (mi^2 + mj^2) ss[[1]]),
         (2/(mi^2 - mj^2)) evalON$[mj^2 sl[[2]] + mi mj sr[[2]] + (mi^2 + mj^2) ss[[2]], True]}/KK]], {i, 3}, {j, 3}];
   {z[[All, All, 1]], z[[All, All, 2]]}];
vMatON$ = vStdON$;
dsON$[zu_, zd_] := 1/4 ((zu - ConjugateTranspose[zu]) . vMatON$ - vMatON$ . (zd - ConjugateTranspose[zd]));
(* (1/2) K dV/dln mu of Eq. (Vrun), generators with zero diagonal *)
yuB$ = Sqrt[2] upB$/vevB$; ydB$ = Sqrt[2] dnB$/vevB$;
kdVON$ = Module[{du = DiagonalMatrix[yuB$^2], dd = DiagonalMatrix[ydB$^2], hd, hu, au, ad},
   hd = vMatON$ . dd . ConjugateTranspose[vMatON$]; hu = ConjugateTranspose[vMatON$] . du . vMatON$;
   au = Table[If[i == k, 0, -3/2 (yuB$[[i]]^2 + yuB$[[k]]^2)/(yuB$[[k]]^2 - yuB$[[i]]^2) hd[[i, k]]], {i, 3}, {k, 3}];
   ad = Table[If[k == j, 0, -3/2 (ydB$[[k]]^2 + ydB$[[j]]^2)/(ydB$[[j]]^2 - ydB$[[k]]^2) hu[[k, j]]], {k, 3}, {j, 3}];
   N[-au . vMatON$ + vMatON$ . ad, 30]];
dsResON$ = Table[Module[{zu = dZLON$["U", xw], zd = dZLON$["D", xw], uv, fin},
     uv = dsON$[zu[[1]], zd[[1]]]; fin = dsON$[zu[[2]], zd[[2]]];
     {xw, uv, fin}], {xw, xisON$}];
uvDevON$ = Max[Abs[Flatten[KK dsResON$[[1, 2]] - kdVON$/2]]]/Max[Abs[Flatten[kdVON$/2]]];
Print["(g) K delta V^DS |UV against (1/2) K dV/dln mu of Eq. (Vrun): max |difference|/max|entry| = ", sfON$[uvDevON$, 2],
  " (expect ~1e-15 or less);  xiW dependence of the UV pole: ",
  sfON$[Max[Abs[Flatten[dsResON$[[2, 2]] - dsResON$[[1, 2]]]]], 2], ", ", sfON$[Max[Abs[Flatten[dsResON$[[3, 2]] - dsResON$[[1, 2]]]]], 2]];
addOut$["dVDS_uv_vs_MSbar_maxrel", uvDevON$];
uniON$[dv_] := Max[Abs[Flatten[ConjugateTranspose[vMatON$] . dv + ConjugateTranspose[dv] . vMatON$]]];
Print["(g) unitarity |V^dagger dV + dV^dagger V| of delta V^DS (UV, finite at xiW = 1/2, 2, 3, 10): ",
  sfON$[uniON$[dsResON$[[1, 2]]], 2], ", ", sfON$ /@ (uniON$ /@ dsResON$[[All, 3]])];
names$ = {"ud", "us", "ub", "cd", "cs", "cb", "td", "ts", "tb"};
relAbs$[dv_] := Flatten[Table[Re[Conjugate[vMatON$[[i, j]]] dv[[i, j]]]/Abs[vMatON$[[i, j]]]^2, {i, 3}, {j, 3}]];
Print["(g) finite part of delta V^DS as delta|V_ij|/|V_ij| (no factor K), xiW = 1/2, 2, 3, 10, and the spread max - min:"];
Do[Module[{v = relAbs$[#[[3]]][[n]] & /@ dsResON$}, Print["   V_", names$[[n]], ": ", sfON$ /@ v, "   spread ", sfON$[Max[v] - Min[v], 3]]], {n, 9}];
Do[addOut$["dVDS_fin_relabs_" <> names$[[n]] <> "_xiW_half_2_3_10", relAbs$[#[[3]]][[n]] & /@ dsResON$], {n, 9}];
(* the xiW-dependent part of delta V^DS itself (not only of |V|): max |dV(xi) - dV(1/2)| over the entries, times K *)
Print["(g) K max_ij |delta V^DS_fin(xiW) - delta V^DS_fin(1/2)|, xiW = 2, 3, 10: ",
  sfON$[KK Max[Abs[Flatten[#[[3]] - dsResON$[[1, 3]]]]], 3] & /@ Rest[dsResON$], ";  K max_ij |delta V^DS_fin(1/2)| = ",
  sfON$[KK Max[Abs[Flatten[dsResON$[[1, 3]]]]], 3]];
jarlON$[v_] := Im[v[[1, 2]] v[[2, 3]] Conjugate[v[[1, 3]]] Conjugate[v[[2, 2]]]];
dJON$[dv_] := Im[dv[[1, 2]] vMatON$[[2, 3]] Conjugate[vMatON$[[1, 3]]] Conjugate[vMatON$[[2, 2]]] +
     vMatON$[[1, 2]] dv[[2, 3]] Conjugate[vMatON$[[1, 3]]] Conjugate[vMatON$[[2, 2]]] +
     vMatON$[[1, 2]] vMatON$[[2, 3]] Conjugate[dv[[1, 3]]] Conjugate[vMatON$[[2, 2]]] +
     vMatON$[[1, 2]] vMatON$[[2, 3]] Conjugate[vMatON$[[1, 3]]] Conjugate[dv[[2, 2]]]];
Print["(g) finite part of delta V^DS as delta J/J, xiW = 1/2, 2, 3, 10: ", sfON$[dJON$[#[[3]]]/jarlON$[vMatON$]] & /@ dsResON$];
addOut$["dVDS_fin_dJ_over_J_xiW_half_2_3_10", dJON$[#[[3]]]/jarlON$[vMatON$] & /@ dsResON$];


(* ::Section:: *)
(*(h) CKM shifts of the SM note's quantities*)


(* difference V(bench) - (V = 1), taken after Expand so that the V-independent terms cancel exactly *)
diffON$[x_] := Expand[x] /. vNumON$ // # - (Expand[x] /. unitON$) &;
dWW$ = diffON$[sig$["WW"][[1]]];
dTop$[xw_] := Module[{s = sig$["U"][[3, 3, 1]]}, diffON$[(s[[1]] + s[[2]])/2 + s[[3]]] /. xiW -> xw];
Print["(h) Delta Sigma_T^WW free of gauge parameters and of MA (expect True): ", FreeQ[dWW$, xiA | xiZ | xiW | xiG | MA]];
numDiffON$[x_, p2_] := Module[{l = laurON$[N[x /. kRuleON$ /. kk2 -> p2 /. benchON$ /. MA -> 0, 30]]},
   {l[[1]], Re[evalON$[l[[2]], False]]}];
wAtMW$ = numDiffON$[dWW$, 80^2];
dMW$ = -wAtMW$[[2]]/KK/(2 80);
tAtMt$ = numDiffON$[dTop$[1], 165^2]; tAtMt3$ = numDiffON$[dTop$[3], 165^2];
dMt$ = -165 tAtMt$[[2]]/KK; dMt3$ = -165 tAtMt3$[[2]]/KK;
predUVTop$ = -3/4 Sum[(Abs[vStdON$[[3, j]]]^2 - If[j == 3, 1, 0]) ydB$[[j]]^2, {j, 3}];
Print["(h) UV pole of K Delta Sigma_T^WW(MW^2) (expect 0): ", sfON$[wAtMW$[[1]], 2],
  ";  of K Delta(SigmaV + SigmaS)_top(mt^2): ", sfON$[tAtMt$[[1]], 8], " vs -(3/4) sum_j (|V_tj|^2 - delta_j3) y_dj^2 = ",
  sfON$[predUVTop$, 8]];
(* k^2 -> 0 of Sigma_T^WW (closed forms, as in the SM note's ckm_estimate.wl) *)
dnB0ON$[n_, a_, b_] := Which[a == b, (n!)^2/((2 n + 1)! n a^n),
   n == 1, (a^2 - b^2 - 2 a b Log[a/b])/(2 (a - b)^3),
   True, Integrate[(x (1 - x))^n/(x a + (1 - x) b)^n, {x, 0, 1}]/n];
closedON$ = {fA0$[m2_] :> m2 (1/ep + 1 - Log[m2/mu^2]), fB0$[0, a_, b_] :> If[a == b, 1/ep - Log[a/mu^2],
     1/ep + 1 - (a Log[a/mu^2] - b Log[b/mu^2])/(a - b)], dnB0$[n_, a_, b_] :> dnB0ON$[n, a, b]};
w0$ = Module[{y = dWW$ /. kRuleON$ /. fB0$[kk_, a_, b_] /; ! FreeQ[kk, kk2] :>
       fB0$[0, a, b] + kk dnB0$[1, a, b] + kk^2 dnB0$[2, a, b]},
   y = y /. benchON$ /. closedON$ /. D -> 4 - 2 ep;
   SeriesCoefficient[Normal[Series[y, {kk2, 0, 0}]], {ep, 0, 0}] /. mu -> muB$];
dDeltaHat$ = Re[N[w0$, 20]]/KK/80^2;
Print["(h) top pole-mass shift at xiW = 1 and 3 (expect equal): ", sfON$[dMt$, 10], ", ", sfON$[dMt3$, 10]];
Print["(h) exact CKM shifts (this note's model) vs the SM note's estimate (ckm_estimate.csv):"];
cmpON$ = {{"Delta(DeltaHat)", dDeltaHat$, smEst$["d_DeltaHat"]}, {"Delta M_W,pole [GeV]", dMW$, smEst$["d_MW_pole_GeV"]},
   {"Delta m_t,pole [GeV]", dMt$, smEst$["d_mt_pole_GeV"]}};
Scan[Print["   ", #[[1]], ": ", sfON$[#[[2]], 10], "  estimate ", sfON$[#[[3]], 10], "  relative difference ",
    sfON$[#[[2]]/#[[3]] - 1, 2]] &, cmpON$];
addOut$["d_DeltaHat", dDeltaHat$]; addOut$["d_MW_pole_GeV", dMW$]; addOut$["d_mt_pole_GeV", dMt$];
addOut$["d_mt_pole_GeV_xiW3", dMt3$];


(* ::Section:: *)
(*Output*)


Export[FileNameJoin[{resDirON$, "oneloop_ckm_numeric.csv"}], Prepend[rowsOut$, {"quantity", "value"}], "CSV"];
Print["Summary: dVDS UV vs MS-bar ", sfON$[uvDevON$, 2], ", shifts vs estimate ", sfON$[#[[2]]/#[[3]] - 1, 2] & /@ cmpON$];
