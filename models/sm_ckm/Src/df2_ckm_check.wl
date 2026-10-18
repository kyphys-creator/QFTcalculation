(* ::Package:: *)

(* ::Title:: *)
(*Step (8) of the CKM note: the Delta F = 2 boxes - GIM, gauge independence and the Inami-Lim function S_0 (no FeynCalc)*)


(* ::Text:: *)
(*Reads work/df2_<proc>.m (df2_ckm_feyncalc.wl).  At zero momentum every integral is a vacuum integral: exact closed*)
(*forms (A0, B0(0, a, b)), so all checks are symbolic in the masses and xiW:*)
(*  (a) the Fierz identity of the matrices used for the crossed pairing; the amplitude of each process is*)
(*      sum_{k,l} lambda_k lambda_l F(m_k, m_l) with lambda_k = V*_kq V_kQ (B_s: V*_ks V_kb, B_d: V*_kd V_kb, K: V*_kd V_ks)*)
(*      and one function F, the same for the three processes;*)
(*  (b) UV finiteness of every F(m_k, m_l);*)
(*  (c) the xiW dependence of F(m_k, m_l) is h(m_k) + h(m_l) (+ const), so that it cancels in the sum by unitarity*)
(*      (GIM); the GIM-subtracted function S(m_k, m_l) = F_kl - F_k0 - F_0l + F_00 is free of xiW;*)
(*  (d) S against the Inami-Lim functions S_0(x) and S_0(x_i, x_j) (literature, reference only): S = N S_0 with one*)
(*      constant N for all masses (compared with the normalization of the effective Hamiltonian, g^4/(4 MW^2)).*)
(*Writes results/df2_ckm_S.m (the function S of this note's model, for df2_physics.py) and results/df2_ckm_check.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file df2_ckm_check.wl  (run df2_ckm_feyncalc.wl first).*)


(* ::Section:: *)
(*Setup*)


srcDirDC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirDC$ = FileNameJoin[{srcDirDC$, "results"}];
workDirDC$ = FileNameJoin[{srcDirDC$, "work"}];
t0DC$ = AbsoluteTime[];
procsDC$ = {"Bs", "Bd", "K"};
(* the external flavours {q, Q} of lambda_k = V*_kq V_kQ: B_s {s, b}, B_d {d, b}, K {d, s} *)
flavDC$ = <|"Bs" -> {2, 3}, "Bd" -> {1, 3}, "K" -> {1, 2}|>;
ampDC$ = Association[Table[p -> Get[FileNameJoin[{workDirDC$, "df2_" <> p <> ".m"}]], {p, procsDC$}]];
KK = 16 Pi^2;
closedDC$ = {A0[m2_] :> m2 (1/ep + 1 - Log[m2/mu^2]),
   B0[0, 0, 0] -> 0, B0[0, a_, a_] :> 1/ep - Log[a/mu^2],
   B0[0, 0, b_] :> 1/ep + 1 - Log[b/mu^2], B0[0, b_, 0] :> 1/ep + 1 - Log[b/mu^2],
   B0[0, a_, b_] :> 1/ep + 1 - (a Log[a/mu^2] - b Log[b/mu^2])/(a - b)};
logRuleDC$ = Log[x_] :> PowerExpand[Log[x]];
canonDC$[x_] := Module[{y = Expand[x /. logRuleDC$], ls},
   ls = Union[Cases[y, _Log, Infinity]];
   If[ls === {}, Together[y], Collect[y, ls, Together]]];
laurDC$[x_] := Module[{y = x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2] /. closedDC$ /. D -> 4 - 2 ep},
   canonDC$ /@ {SeriesCoefficient[y, {ep, 0, -1}], SeriesCoefficient[y, {ep, 0, 0}]}];
sfDC$[x_, n_ : 6] := Module[{y = N[x], e}, If[y == 0, "0", e = Floor[Log10[Abs[y]]];
    ToString[NumberForm[y/10^e, n]] <> "e" <> ToString[e]]];
rowsDC$ = {};
addDC$[name_, val_] := AppendTo[rowsDC$, {name, ToString[CForm[N[val, 16]]]}];


(* ::Section:: *)
(*(a) The CKM structure and the function F*)


(* Fierz: (gamma^mu P_L)_ab (gamma_mu P_L)_cd = -(gamma^mu P_L)_ad (gamma_mu P_L)_cb, with explicit Dirac matrices *)
g0DC$ = {{1, 0, 0, 0}, {0, 1, 0, 0}, {0, 0, -1, 0}, {0, 0, 0, -1}};
sigDC$ = {{{0, 1}, {1, 0}}, {{0, -I}, {I, 0}}, {{1, 0}, {0, -1}}};
gDC$ = Prepend[ArrayFlatten[{{0, #}, {-#, 0}}] & /@ sigDC$, g0DC$];
g5DC$ = I gDC$[[1]] . gDC$[[2]] . gDC$[[3]] . gDC$[[4]];
pLDC$ = (IdentityMatrix[4] - g5DC$)/2;
etaDC$ = {1, -1, -1, -1};
fierzDC$ = Module[{t1, t2},
   t1 = Sum[etaDC$[[m]] TensorProduct[gDC$[[m]] . pLDC$, gDC$[[m]] . pLDC$], {m, 4}];
   t2 = Sum[etaDC$[[m]] Transpose[TensorProduct[gDC$[[m]] . pLDC$, gDC$[[m]] . pLDC$], {1, 4, 3, 2}], {m, 4}];
   Simplify[Flatten[t1 + t2]] === ConstantArray[0, 256]];
Print["(a) Fierz identity for the crossed pairing, sign -1 (expect True): ", fierzDC$];
(* the coefficient of lambda_k lambda_l = (cKc[k,q] cK[k,Q]) (cKc[l,q] cK[l,Q]), symmetrized: F_kl *)
fklDC$[p_] := Module[{f = Expand[ampDC$[p]["F"]], q = flavDC$[p][[1]], qq = flavDC$[p][[2]], m},
   m[k_, l_] := If[k == l, cKc[k, q]^2 cK[k, qq]^2, cKc[k, q] cK[k, qq] cKc[l, q] cK[l, qq]];
   Table[If[k == l, Coefficient[f, m[k, k]], Coefficient[f, m[k, l]]/2], {k, 3}, {l, 3}]];
fDC$ = Association[Table[p -> fklDC$[p], {p, procsDC$}]];
(* nothing else than the products lambda_k lambda_l *)
restDC$ = Table[Module[{q = flavDC$[p][[1]], qq = flavDC$[p][[2]], f = Expand[ampDC$[p]["F"]]},
    Simplify[f - Sum[fDC$[p][[k, l]] cKc[k, q] cK[k, qq] cKc[l, q] cK[l, qq], {k, 3}, {l, 3}]]], {p, procsDC$}];
Print["(a) the amplitudes minus sum_{k,l} lambda_k lambda_l F_kl (expect {0, 0, 0}): ", restDC$];
(* one function F(m_k, m_l): the entries are F(MU|MC|MT, ...), the same for the three processes and symmetric *)
fGenDC$[m1_, m2_] := Module[{ms = {MU, MC, MT}, k, l},
   k = First[Flatten[Position[ms, m1]]]; l = First[Flatten[Position[ms, m2]]]; fDC$["Bs"][[k, l]]];
sameDC$ = And @@ Flatten[Table[Simplify[fDC$[p][[k, l]] - fDC$["Bs"][[k, l]]] === 0, {p, procsDC$}, {k, 3}, {l, 3}]];
symDC$ = And @@ Flatten[Table[Simplify[fDC$["Bs"][[k, l]] - fDC$["Bs"][[l, k]]] === 0, {k, 3}, {l, 3}]];
Print["(a) F_kl the same for B_s, B_d, K (expect True): ", sameDC$, ";  symmetric (expect True): ", symDC$, ";  ",
  Round[AbsoluteTime[] - t0DC$], " s"];


(* ::Section:: *)
(*(b), (c) UV finiteness, gauge dependence and GIM*)


(* F as a function of two internal masses: replace the masses of the (t, t), (t, c), ... entries by symbols m1, m2 *)
fSymDC$ = fDC$["Bs"][[3, 2]] /. {MT -> m1, MC -> m2};   (* F(m1, m2) for m1 != m2 *)
fDiagDC$ = fDC$["Bs"][[3, 3]] /. MT -> m1;              (* F(m1, m1) *)
lfOff$ = laurDC$[fSymDC$]; lfDiag$ = laurDC$[fDiagDC$];
Print["(b) UV poles of F(m1, m2) and F(m1, m1) (expect 0, 0): ", lfOff$[[1]], ", ", lfDiag$[[1]]];
fOffFin$ = lfOff$[[2]]; fDiagFin$ = lfDiag$[[2]];
(* F with a massless quark (m -> 0 as a limit: the logarithms of the light masses cancel in S) *)
lim0$[x_, m_] := canonDC$[Normal[Series[x, {m, 0, 0}]]];
fm0$ = lim0$[fOffFin$, m2];             (* F(m1, 0) *)
f00$ = lim0$[lim0$[fOffFin$, m2], m1];  (* F(0, 0) *)
Print["(b) F(m1, 0) and F(0, 0) are finite (no Log[0]) (expect True): ", FreeQ[{fm0$, f00$}, Log[0] | ComplexInfinity | Indeterminate]];
dxiOff$ = canonDC$[D[fOffFin$, xiW]]; dxiDiag$ = canonDC$[D[fDiagFin$, xiW]];
Print["(c) F(m1, m2) depends on xiW (expect True): ", dxiOff$ =!= 0];
(* separable: dF(m1, m2)/dxi - [dF(m1, m1) + dF(m2, m2)]/2 = 0 *)
sepDC$ = canonDC$[dxiOff$ - (dxiDiag$ + (dxiDiag$ /. m1 -> m2))/2];
Print["(c) d F(m1, m2)/d xiW = h(m1) + h(m2) (expect 0): ", sepDC$];
sDC$ = canonDC$[fOffFin$ - (fm0$) - (fm0$ /. m1 -> m2) + f00$];            (* S(m1, m2), m1 != m2 *)
sDiagDC$ = canonDC$[fDiagFin$ - 2 fm0$ + f00$];                              (* S(m1, m1) *)
Print["(c) the GIM-subtracted S(m1, m2), S(m1, m1) free of xiW (expect True, True): ", FreeQ[sDC$, xiW], ", ", FreeQ[sDiagDC$, xiW],
  ";  free of mu (expect True, True): ", FreeQ[sDC$, mu], ", ", FreeQ[sDiagDC$, mu], ";  ", Round[AbsoluteTime[] - t0DC$], " s"];


(* ::Section:: *)
(*(d) Inami-Lim*)


s0IL$[x_] := (4 x - 11 x^2 + x^3)/(4 (1 - x)^2) - 3 x^3 Log[x]/(2 (1 - x)^3);
s0IL2$[xi_, xj_] := xi xj ((1/4 + 3/(2 (1 - xj)) - 3/(4 (1 - xj)^2)) Log[xj]/(xj - xi) +
     (1/4 + 3/(2 (1 - xi)) - 3/(4 (1 - xi)^2)) Log[xi]/(xi - xj) - 3/(4 (1 - xi) (1 - xj)));
normDC$ = canonDC$[sDiagDC$/(s0IL$[m1^2/MW^2] /. logRuleDC$)];
Print["(d) N = S(m1, m1)/S_0(x_1): ", Simplify[normDC$], ";  free of m1 (expect True): ", FreeQ[Simplify[normDC$], m1],
  ";  N/(g^2/(4 MW^2) g^2) = ", Simplify[normDC$/((ee/sw)^4/(4 MW^2))]];
(* the coefficients of the logarithms need a full simplification here (Together alone leaves 0 in a non-canonical form) *)
twoDC$ = Module[{d = Expand[(sDC$ - normDC$ (s0IL2$[m1^2/MW^2, m2^2/MW^2])) /. logRuleDC$], ls},
   ls = Union[Cases[d, _Log, Infinity]];
   Simplify[Collect[d, ls, Simplify[Together[#], m1 > 0 && m2 > 0 && MW > 0] &], m1 > 0 && m2 > 0 && MW > 0]];
Print["(d) S(m1, m2) - N S_0(x_1, x_2) (expect 0): ", twoDC$];
(* the function of this note's model in the units of S_0, for df2_physics.py: S(x_i, x_j) = s(m_i, m_j)/N *)
Put[{"S_offdiag" -> canonDC$[sDC$/normDC$], "S_diag" -> canonDC$[sDiagDC$/normDC$], "N" -> normDC$},
  FileNameJoin[{resDirDC$, "df2_ckm_S.m"}]];
xtB$ = 165^2/80^2;
addDC$["S0_xt_bench_note", sDiagDC$/normDC$ /. {m1 -> 165, MW -> 80}];
addDC$["S0_xt_bench_IL", s0IL$[xtB$]];
(* the function of this note's model at the masses used for Delta m and epsilon_K (df2_physics.py): MS-bar
   m_t(m_t) = 162.5 GeV, m_c(m_c) = 1.2730 GeV, M_W = 80.3692 GeV (PDG 2024) *)
physMDC$ = {MW -> 803692/10000};
sPhysDC$ = {"S_tt" -> N[sDiagDC$/normDC$ /. m1 -> 1625/10 /. physMDC$, 20],
   "S_cc" -> N[sDiagDC$/normDC$ /. m1 -> 12730/10000 /. physMDC$, 20],
   "S_ct" -> N[sDC$/normDC$ /. {m1 -> 1625/10, m2 -> 12730/10000} /. physMDC$, 20]};
Scan[addDC$[#[[1]], #[[2]]] &, sPhysDC$];
Print["(d) this note's S at m_t(m_t) = 162.5, m_c(m_c) = 1.273, M_W = 80.3692 GeV: S(x_t) ", sfDC$["S_tt" /. sPhysDC$, 8],
  ", S(x_c) ", sfDC$["S_cc" /. sPhysDC$, 8], ", S(x_c, x_t) ", sfDC$["S_ct" /. sPhysDC$, 8]];
Export[FileNameJoin[{resDirDC$, "df2_ckm_check.csv"}], Prepend[rowsDC$, {"quantity", "value"}], "CSV"];
Print["(d) S_0(x_t) at the benchmark (m_t = 165, MW = 80): note ", sfDC$[sDiagDC$/normDC$ /. {m1 -> 165, MW -> 80}, 10],
  ", Inami-Lim ", sfDC$[s0IL$[xtB$], 10]];
Print["Summary (expect True; {0,0,0}; True, True; 0, 0; 0; True, True; True; 0): ", fierzDC$, "; ", restDC$, "; ", sameDC$, ", ", symDC$,
  "; ", lfOff$[[1]], ", ", lfDiag$[[1]], "; ", sepDC$, "; ", FreeQ[sDC$, xiW], ", ", FreeQ[sDiagDC$, xiW], "; ",
  FreeQ[Simplify[normDC$], m1], "; ", twoDC$, ";  total ", Round[AbsoluteTime[] - t0DC$], " s"];
