(* ::Package:: *)

(* ::Title:: *)
(*Size of the CKM effects on the quantities of the SM note, which sets V = 1*)


(* ::Text:: *)
(*In the mass basis the CKM matrix enters only the W and G^+- couplings, as |V_ij|^2 in loops.  A function S built*)
(*with V = 1 contains the pair (u_i, d_i) through m_{d_i} only, so with the CKM matrix*)
(*  Delta S = sum_ij |V_ij|^2 [S(m_{d_i} -> m_{d_j}) - S]                       (row unitarity used)*)
(*for the 1PI W self-energy, and Delta S = sum_j |V_tj|^2 [S(m_b -> m_{d_j}) - S] for the top self-energy.*)
(*Checks: (a) the UV pole of Delta Sigma^WW vanishes (row and column unitarity: dM_W^2/dln mu depends on the Yukawas*)
(*only through traces); (b) the UV pole of Delta(Sigma^V + Sigma^S) of the top is the change of (1/4) dln m_t^2/dln mu,*)
(*-(3/4) sum_j (|V_tj|^2 - delta_j3) y_{d_j}^2 / K, from the CKM term of beta_{y_t}.  Then, at the benchmark (mu = MZ):*)
(*the shifts of DeltaHat (Eq. (GF1), = Delta Sigma^WW(0)/MW^2), of the W and top pole masses, and of beta_{y_t}.*)
(*The tadpole and the Z, photon, H self-energies do not depend on V.*)
(*V from the standard parametrization with the PDG 2024 global fit (sin theta_12 = 0.22501, sin theta_13 = 0.003732,*)
(*sin theta_23 = 0.04183, delta = 1.147), exactly unitary.  Reads results/oneloop_sigma.m; writes results/ckm_estimate.csv.*)
(*Batch: wolframscript -file ckm_estimate.wl*)


srcDirCK$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
sig$ = Association[Get[FileNameJoin[{srcDirCK$, "results", "oneloop_sigma.m"}]]];
KK = 16 Pi^2;
kRule$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2};
toSw$[x_] := x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2];


(* ::Section:: *)
(*CKM matrix*)


{s12$, s13$, s23$, dl$} = SetPrecision[{0.22501, 0.003732, 0.04183, 1.147}, 40];
{c12$, c13$, c23$} = Sqrt[1 - {s12$, s13$, s23$}^2];
vCKM$ = {{c12$ c13$, s12$ c13$, s13$ Exp[-I dl$]},
   {-s12$ c23$ - c12$ s23$ s13$ Exp[I dl$], c12$ c23$ - s12$ s23$ s13$ Exp[I dl$], s23$ c13$},
   {s12$ s23$ - c12$ c23$ s13$ Exp[I dl$], -c12$ s23$ - s12$ c23$ s13$ Exp[I dl$], c23$ c13$}};
v2$ = Abs[vCKM$]^2;
jarl$ = Im[vCKM$[[1, 1]] vCKM$[[2, 2]] Conjugate[vCKM$[[1, 2]] vCKM$[[2, 1]]]];
sf$[x_, n_] := Module[{y = N[x], e}, If[y == 0, "0", e = Floor[Log10[Abs[y]]];
    ToString[NumberForm[y/10^e, n]] <> "e" <> ToString[e]]];
Print["|V_ij|: ", ToString[NumberForm[N[Abs[vCKM$]], 5]], ";  unitarity of rows and columns (deviation): ",
  sf$[Max[Abs[Total[v2$, {2}] - 1], Abs[Total[v2$] - 1]], 2], ";  J = ", sf$[jarl$, 3], " (PDG 2024: 3.12e-5)"];


(* ::Section:: *)
(*Shifts*)


ups$ = {MU, MC, MT}; dns$ = {MD, MS, MB};
shiftW$[s_] := Sum[If[i == j, 0, v2$[[i, j]] ((s /. dns$[[i]] -> dns$[[j]]) - s)], {i, 3}, {j, 3}];
shiftT$[s_] := Sum[If[j == 3, 0, v2$[[3, j]] ((s /. MB -> dns$[[j]]) - s)], {j, 3}];
(* Laurent coefficients in eps after inserting A0 = m^2/eps + a0f, B0 = 1/eps + b0f *)
laurCK$[x_] := Module[{y = toSw$[x] /. kRule$ /. {A0[m2_] :> m2/ep + a0f[m2], B0[p2_, a_, b_] :> 1/ep + b0f[p2, a, b]} /.
      D -> 4 - 2 ep},
   {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];
(* expand first, so that the terms without the shifted masses (bosonic loops, other fermions) cancel term by term *)
dWexpr$ = shiftW$[Expand[toSw$[sig$["WW"][[1]]] /. kRule$]];  (* K Delta Sigma_T^WW (1PI), function of kk2 *)
dTexpr$ = shiftT$[Expand[toSw$[Total[sig$["TT"][[1]]]] /. kRule$]];  (* K Delta (Sigma^V + Sigma^S) of the top *)
Print["    Delta Sigma^WW free of the gauge parameters and the photon mass (expect True): ",
  FreeQ[dWexpr$, xiA | xiZ | xiW | xiG | MA], ";  the top shift keeps xiW off shell (expect True): ", !FreeQ[dTexpr$, xiW]];
dW$ = laurCK$[dWexpr$]; dT$ = laurCK$[dTexpr$];
(* k^2 -> 0 of the W shift: B0(k^2, a, b) = B0(0, a, b) + k^2 DB0 + k^4 D2B0 (1/k^2 terms of the projection) *)
dnB0CK$[n_, a_, b_] := Which[a == b, (n!)^2/((2 n + 1)! n a^n),
   n == 1, (a^2 - b^2 - 2 a b Log[a/b])/(2 (a - b)^3),
   True, Integrate[(x (1 - x))^n/(x a + (1 - x) b)^n, {x, 0, 1}]/n];
closedCK$ = {A0[m2_] :> m2 (1/ep + 1 - Log[m2/mu^2]), B0[0, a_, b_] :> If[a == b, 1/ep - Log[a/mu^2],
     1/ep + 1 - (a Log[a/mu^2] - b Log[b/mu^2])/(a - b)], dnB0[n_, a_, b_] :> dnB0CK$[n, a, b]};
dW0$[rules_] := Module[{y = dWexpr$ /. rules /. B0[kk_, a_, b_] /; !FreeQ[kk, kk2] :>
       B0[0, a, b] + kk dnB0[1, a, b] + kk^2 dnB0[2, a, b]},
   y = y /. closedCK$ /. D -> 4 - 2 ep;
   SeriesCoefficient[Normal[Series[y, {kk2, 0, 0}]], {ep, 0, 0}]];


(* ::Section:: *)
(*Benchmark*)


eeB = Sqrt[4 Pi/128]; swB = Sqrt[1881/8281]; mwB = 80; vB = 2 mwB swB/eeB; muB = 91;
benchCK$ = {ee -> eeB, sw -> swB, MW -> mwB, MH -> 125, MT -> 165, MB -> 286/100, MC -> 619/1000, MS -> 546/10000,
   MD -> 271/100000, MU -> 127/100000, MTA -> 1746/1000, MMU -> 1027/10000, Me -> 487/1000000, gS -> Sqrt[4 Pi 118/1000],
   CF -> 4/3, CA -> 3, MA -> 0, xiA -> 1, xiZ -> 1, xiW -> 1, xiG -> 1};
yd$ = Sqrt[2] {271/100000, 546/10000, 286/100}/vB;

uvW$ = N[dW$[[1]] /. benchCK$ /. kk2 -> mwB^2, 30];
predT$ = -3/4 Sum[(v2$[[3, j]] - If[j == 3, 1, 0]) yd$[[j]]^2, {j, 3}];
uvT$ = N[dT$[[1]] /. benchCK$ /. kk2 -> 165^2, 30];
Print["(a) UV pole of K Delta Sigma_T^WW at k^2 = MW^2 (expect 0 up to the precision of V): ", sf$[uvW$, 2]];
Print["(b) UV pole of K Delta(Sigma^V + Sigma^S) of the top: ", sf$[uvT$, 6],
  ";  -(3/4) sum_j (|V_tj|^2 - delta_j3) y_dj^2: ", sf$[predT$, 6]];

(* finite parts: LoopTools at mu = MZ *)
linkLT$ = Quiet[Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]]];
SetDelta[0.]; SetMudim[N[muB^2]];
numCK$[x_, p2_] := Re[N[x /. benchCK$ /. kk2 -> p2 /. {a0f[m2_] :> If[m2 == 0, 0, m2 (1 - Log[m2/muB^2])]} /.
       {b0f[pp_, a_, b_] :> LoopTools`B0[N[pp], N[a], N[b]]}]];
dDeltaHat$ = Re[N[dW0$[benchCK$] /. mu -> muB, 20]]/KK/mwB^2;
dMW$ = -numCK$[dW$[[2]], mwB^2]/KK/(2 mwB);
dMt$ = -165 numCK$[dT$[[2]], 165^2]/KK;
dMtXi3$ = -165 numCK$[dT$[[2]] /. xiW -> 3, 165^2]/KK;
Print["    top pole-mass shift at xiW = 1 and 3 (expect equal): ", sf$[dMt$, 8], ", ", sf$[dMtXi3$, 8]];
(* beta_{y_t}: the y_b^2 term -(3/2) y_t y_b^2 becomes -(3/2) y_t sum_j |V_tj|^2 y_dj^2 *)
ytB = Sqrt[2] 165/vB; gsB2 = 4 Pi 118/1000; gB2 = eeB^2/swB^2; gpB2 = eeB^2/(1 - swB^2);
ttB = 3 Total[(Sqrt[2] {127/100000, 619/1000, 165}/vB)^2] + 3 Total[yd$^2] + Total[(Sqrt[2] {487/1000000, 1027/10000, 1746/1000}/vB)^2];
betaYt$ = ytB (3/2 (ytB^2 - yd$[[3]]^2) + ttB - 8 gsB2 - 9/4 gB2 - 17/12 gpB2);
dBetaYt$ = -3/2 ytB Sum[(v2$[[3, j]] - If[j == 3, 1, 0]) yd$[[j]]^2, {j, 3}];
Print["(c) benchmark (mu = MZ), V = 1 -> PDG 2024:  Delta(DeltaHat) = ", sf$[dDeltaHat$, 3],
  ";  Delta M_W,pole = ", sf$[dMW$, 3], " GeV;  Delta m_t,pole = ", sf$[dMt$, 3],
  " GeV;  Delta beta_yt/beta_yt = ", sf$[dBetaYt$/betaYt$, 3]];
Export[FileNameJoin[{srcDirCK$, "results", "ckm_estimate.csv"}],
  {{"quantity", "value"}, {"jarlskog", ToString[CForm[N[jarl$]]]}, {"uv_pole_dSigmaWW", ToString[CForm[N[uvW$]]]},
   {"uv_pole_dSigmaTop", ToString[CForm[N[uvT$]]]}, {"uv_pole_dSigmaTop_expected", ToString[CForm[N[predT$]]]},
   {"d_DeltaHat", ToString[CForm[N[dDeltaHat$]]]}, {"d_MW_pole_GeV", ToString[CForm[N[dMW$]]]},
   {"d_mt_pole_GeV", ToString[CForm[N[dMt$]]]}, {"d_beta_yt_relative", ToString[CForm[N[dBetaYt$/betaYt$]]]}}, "CSV"];
Print["Summary: ", N[{uvW$, uvT$ - predT$, dDeltaHat$, dMW$, dMt$, dBetaYt$/betaYt$}]];
