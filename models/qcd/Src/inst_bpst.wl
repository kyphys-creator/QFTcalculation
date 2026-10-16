(* ::Package:: *)

(* ::Title:: *)
(*Step (10): the BPST instanton, its zero modes, the radial reduction of -D^2 and the heat-kernel and lattice coefficients*)


(* ::Text:: *)
(*Research note models/qcd, step (10).  Euclidean, g = 1 (A -> A/g), SU(2) with T^a = sigma^a/2, D_mu = d_mu - i A_mu, F = dA - dA - i[A, A].*)
(*(a) 't Hooft symbols; BPST in regular and singular gauge: self-duality, Yang-Mills equation, S = 8 pi^2, Q = 1, the gauge transformation*)
(*    between the two gauges and its winding number.*)
(*(b) The eight bosonic zero modes (singular gauge): background gauge, linearized Yang-Mills equation, norms.*)
(*(c) The fermion zero mode (x^2 + rho^2)^(-3/2) (spin-colour singlet) and its normalization.*)
(*(d) The radial reduction -D^2 = -d_r^2 - (3/r) d_r + 4 L^2/r^2 + 8 L.T/(r^2+rho^2) + 4 t(t+1) r^2/(r^2+rho^2)^2 (t = 1/2, 1) and the exact*)
(*    massless partial waves (symbolic l), their ratios at r -> infinity.*)
(*(e) The asymptotics of the massless partial-wave sums (t = 1/2, 1) and the constants alpha(1/2), alpha(1).*)
(*(f) The heat-kernel coefficients: int tr F^2, int tr F^3, int tr (DF)^2 -> the 1/m^2 term -T(R)/(75 (T(1/2)) m^2 rho^2); the O(a^2) term of the*)
(*    Wilson action -(1/5)(a/rho)^2 and of the clover charge -(4/5)(a/rho)^2.  -> results/inst_symbolic.txt*)
(*Usage: wolframscript -file inst_bpst.wl  (under a minute)*)


srcDirIB$ = Which[StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName], $Notebooks, NotebookDirectory[], True, Directory[]];
outIB$ = {};
fmt[x_InputForm] := ToString[First[x], InputForm]; fmt[x_?InexactNumberQ] := ToString[CForm[N[x, 12]]]; fmt[x_] := ToString[x, InputForm];
fmt[x_String] := x;
rep[s__] := Module[{line = StringJoin[fmt /@ {s}]}, Print[line]; AppendTo[outIB$, line]];
sig = PauliMatrix /@ {1, 2, 3}; T = sig/2; id2 = IdentityMatrix[2];
eps4 = LeviCivitaTensor[4]; eps3 = LeviCivitaTensor[3];
eta[a_, m_, n_] := Which[m <= 3 && n <= 3, eps3[[a, m, n]], n == 4 && m <= 3, KroneckerDelta[a, m], m == 4 && n <= 3, -KroneckerDelta[a, n], True, 0];
etab[a_, m_, n_] := Which[m <= 3 && n <= 3, eps3[[a, m, n]], n == 4 && m <= 3, -KroneckerDelta[a, m], m == 4 && n <= 3, KroneckerDelta[a, n], True, 0];
X = {x1, x2, x3, x4}; r2 = X . X;
$Assumptions = Element[X, Reals] && rho > 0 && r > 0;
fieldStrength[A_] := Table[Simplify[D[A[[n]], X[[m]]] - D[A[[m]], X[[n]]] - I (A[[m]] . A[[n]] - A[[n]] . A[[m]])], {m, 4}, {n, 4}];
dual[F_] := Table[1/2 Sum[eps4[[m, n, r, s]] F[[r, s]], {r, 4}, {s, 4}], {m, 4}, {n, 4}];
onAxis[f_] := f /. {x1 -> r, x2 -> 0, x3 -> 0, x4 -> 0};
radInt[f_] := Integrate[2 Pi^2 r^3 onAxis[f], {r, 0, Infinity}];
symmetricQ[f_] := Simplify[onAxis[f] - (f /. {x1 -> r/2, x2 -> r/2, x3 -> r/2, x4 -> r/2})] === 0;
zero2 = ConstantArray[0, {2, 2}];


(* ::Section:: *)
(*(a) BPST in regular and singular gauge*)


rep["(a) eta self-dual: ", And @@ Flatten[Table[eta[a, m, n] == 1/2 Sum[eps4[[m, n, r, s]] eta[a, r, s], {r, 4}, {s, 4}], {a, 3}, {m, 4}, {n, 4}]],
  ", etabar anti-self-dual: ", And @@ Flatten[Table[etab[a, m, n] == -1/2 Sum[eps4[[m, n, r, s]] etab[a, r, s], {r, 4}, {s, 4}], {a, 3}, {m, 4}, {n, 4}]]];
Areg = Table[Sum[2 eta[a, m, n] X[[n]]/(r2 + rho^2) T[[a]], {a, 3}, {n, 4}], {m, 4}];
Asin = Table[Sum[2 etab[a, m, n] X[[n]] rho^2/(r2 (r2 + rho^2)) T[[a]], {a, 3}, {n, 4}], {m, 4}];
Freg = fieldStrength[Areg]; Fsin = fieldStrength[Asin];
covDivF[A_, F_] := Table[Simplify[Sum[D[F[[m, n]], X[[m]]] - I (A[[m]] . F[[m, n]] - F[[m, n]] . A[[m]]), {m, 4}]], {n, 4}];
rep["    F^a_{mu nu} (regular) = -4 eta_{a mu nu} rho^2/(x^2+rho^2)^2: ",
  Simplify[Table[2 Tr[Freg[[m, n]] . T[[a]]] + 4 eta[a, m, n] rho^2/(r2 + rho^2)^2, {m, 4}, {n, 4}, {a, 3}]] === ConstantArray[0, {4, 4, 3}]];
rep["    self-dual: regular ", Simplify[Freg - dual[Freg]] === ConstantArray[0, {4, 4, 2, 2}], ", singular ", Simplify[Fsin - dual[Fsin]] === ConstantArray[0, {4, 4, 2, 2}],
  ";  D_mu F_mu nu = 0: regular ", covDivF[Areg, Freg] === ConstantArray[0, {4, 2, 2}], ", singular ", covDivF[Asin, Fsin] === ConstantArray[0, {4, 2, 2}]];
densIB = Simplify[1/2 Sum[Tr[Freg[[m, n]] . Freg[[m, n]]], {m, 4}, {n, 4}]];
qdIB = Simplify[1/(16 Pi^2) Sum[Tr[Freg[[m, n]] . dual[Freg][[m, n]]], {m, 4}, {n, 4}]];
rep["    (1/2) tr F F = ", InputForm[densIB], ",  S g^2 = ", radInt[densIB], ",  Q = (1/16 pi^2) int tr F Fdual = ", radInt[qdIB],
  ";  gauge-invariant density equal in both gauges: ", Simplify[1/2 Sum[Tr[Fsin[[m, n]] . Fsin[[m, n]]], {m, 4}, {n, 4}] - densIB] === 0];
U = (x4 id2 + I Sum[X[[k]] sig[[k]], {k, 3}])/Sqrt[r2]; Ub = ConjugateTranspose[U] /. Conjugate[z_] :> z;
gt[A_, V_, Vb_] := Table[Simplify[V . A[[m]] . Vb + I V . D[Vb, X[[m]]]], {m, 4}];
rep["    U = (x4 + i x.sigma)/|x|: A_sing = U^+ A_reg U + i U^+ dU: ", Simplify[gt[Areg, Ub, U] - Asin] === ConstantArray[0, {4, 2, 2}],
  ";  A_reg -> i (dU) U^+ at |x| -> infinity: ", Simplify[Limit[(Areg - Table[I D[U, X[[m]]] . Ub, {m, 4}]) /. Thread[X -> lam X], lam -> Infinity] ] === ConstantArray[0, {4, 2, 2}]];
wdIB = Simplify[Sum[eps4[[m, n, r, s]] X[[m]]/Sqrt[r2] Tr[(U . D[Ub, X[[n]]]) . (U . D[Ub, X[[r]]]) . (U . D[Ub, X[[s]]])], {m, 4}, {n, 4}, {r, 4}, {s, 4}]];
rep["    winding number (1/24 pi^2) int_{S^3} eps tr (U dU^+)^3 = ", Simplify[2 Pi^2 r2^(3/2) wdIB/(24 Pi^2)]];


(* ::Subsubsection:: *)
(*Inspect: the action density and the gauge field in the two gauges*)


If[$Notebooks, Plot[{onAxis[densIB] /. rho -> 1, onAxis[Sqrt[Sum[2 Tr[Areg[[m]] . Areg[[m]]], {m, 4}]]] /. rho -> 1, onAxis[Sqrt[Sum[2 Tr[Asin[[m]] . Asin[[m]]], {m, 4}]]] /. rho -> 1},
  {r, 0, 4}, PlotLegends -> {"(1/2) tr F^2", "|A| regular", "|A| singular"}, AxesLabel -> {"|x|/rho", ""}, PlotRange -> {0, 6}]]


(* ::Section:: *)
(*(b) bosonic zero modes (singular gauge)*)


Dadj[A_, m_, M_] := D[M, X[[m]]] - I (A[[m]] . M - M . A[[m]]);
modesIB = Join[Table[Table[Fsin[[m, l]], {m, 4}], {l, 4}], {Simplify[D[Asin, rho]]}, Table[Table[Simplify[Dadj[Asin, m, r2/(r2 + rho^2) T[[b]]]], {m, 4}], {b, 3}]];
namesIB = {"translation 1", "translation 2", "translation 3", "translation 4", "dilatation", "gauge 1", "gauge 2", "gauge 3"};
Do[Module[{a = modesIB[[i]], nd},
   nd = Simplify[2 Sum[Tr[a[[m]] . a[[m]]], {m, 4}]];
   rep["(b) ", namesIB[[i]], ": D_mu a_mu = 0 ", Simplify[Sum[Dadj[Asin, m, a[[m]]], {m, 4}]] === zero2,
    ", linearized YM ", Table[Simplify[Sum[Dadj[Asin, m, Dadj[Asin, m, a[[n]]] - Dadj[Asin, n, a[[m]]]] - I (a[[m]] . Fsin[[m, n]] - Fsin[[m, n]] . a[[m]]), {m, 4}]], {n, 4}] === ConstantArray[zero2, 4],
    ", |a|^2 g^2 = ", radInt[nd], " (density spherically symmetric: ", symmetricQ[nd], ")"]], {i, Length[modesIB]}];


(* ::Section:: *)
(*(c) fermion zero mode*)


sE = Append[I sig, id2]; sbE = Append[-I sig, id2];        (* gamma_mu = {{0, s_mu}, {sb_mu, 0}} *)
rep["(c) {gamma_mu, gamma_nu} = 2 delta: ", And @@ Flatten[Table[sE[[m]] . sbE[[n]] + sE[[n]] . sbE[[m]] == 2 KroneckerDelta[m, n] id2, {m, 4}, {n, 4}]]];
chiIB = (r2 + rho^2)^(-3/2) {{0, 1}, {-1, 0}};                (* chi[[alpha, i]], colour index acted on by A^T *)
Dc[A_, m_, chi_] := D[chi, X[[m]]] - I chi . Transpose[A[[m]]];
rep["    chi = (x^2+rho^2)^(-3/2) eps_{alpha i}: sb_mu D_mu chi = 0 ", Simplify[Sum[sbE[[m]] . Dc[Areg, m, chiIB], {m, 4}]] === zero2,
  " (the other chirality: s_mu D_mu chi = 0 ", Simplify[Sum[sE[[m]] . Dc[Areg, m, chiIB], {m, 4}]] === zero2, "),  normalization c = ",
  Simplify[Sqrt[1/radInt[Simplify[Tr[chiIB . ConjugateTranspose[chiIB]]]]]], " (psi = c chi, int psi^+ psi = 1)"];


(* ::Section:: *)
(*(d) radial reduction and the massless partial waves*)


Lop[a_, f_] := -I/2 Sum[eta[a, m, n] X[[m]] D[f, X[[n]]], {m, 4}, {n, 4}];
hh = h[x1, x2, x3, x4];
lap[f_] := Sum[D[f, X[[m]], X[[m]]], {m, 4}];
rdr[f_] := Sum[X[[m]] D[f, X[[m]]], {m, 4}];
rep["(d) [L^1, L^2] = i L^3: ", Simplify[Lop[1, Lop[2, hh]] - Lop[2, Lop[1, hh]] - I Lop[3, hh]] === 0,
  ";  -r^2 Laplacian = -(r d_r)^2 - 2 r d_r + 4 L^2: ", Simplify[-r2 lap[hh] - (-rdr[rdr[hh]] - 2 rdr[hh] + 4 Sum[Lop[a, Lop[a, hh]], {a, 3}])] === 0];
psiIB = {h1[x1, x2, x3, x4], h2[x1, x2, x3, x4]};
DD[A_, m_, v_] := D[v, X[[m]]] - I A[[m]] . v;
rep["    t = 1/2: -D^2 = -lap + 8 L.T/(r^2+rho^2) + 3 r^2/(r^2+rho^2)^2: ",
  Simplify[-Sum[DD[Areg, m, DD[Areg, m, psiIB]], {m, 4}] - (-lap[psiIB] + 8/(r2 + rho^2) Sum[T[[a]] . Lop[a, psiIB], {a, 3}] + 3 r2/(r2 + rho^2)^2 psiIB)] === {0, 0}];
MfIB = {{h1[x1, x2, x3, x4], h2[x1, x2, x3, x4]}, {h3[x1, x2, x3, x4], -h1[x1, x2, x3, x4]}};
rep["    t = 1:   -D^2 = -lap + 8 L.T/(r^2+rho^2) + 8 r^2/(r^2+rho^2)^2: ",
  Simplify[-Sum[Dadj[Areg, m, Dadj[Areg, m, MfIB]], {m, 4}] - (-lap[MfIB] + 8/(r2 + rho^2) Sum[T[[a]] . Lop[a, MfIB] - Lop[a, MfIB] . T[[a]], {a, 3}] + 8 r2/(r2 + rho^2)^2 MfIB)] === zero2];
(* radial operator, rho = 1: H = -d^2 - (3/r) d + 4 l(l+1)/r^2 + 4 (j(j+1) - l(l+1))/(r^2+1) - 4 t(t+1)/(r^2+1)^2 *)
Hrad[l_, j_, t_][w_] := -D[w, {r, 2}] - 3/r D[w, r] + (4 l (l + 1)/r^2 + 4 (j (j + 1) - l (l + 1))/(r^2 + 1) - 4 t (t + 1)/(r^2 + 1)^2) w;
waves = {
   {"t=1/2 (l, l+1/2)", 1/2, l, l + 1/2, r^(2 l) ((2 l + 2) + (2 l + 1) r^2)/((2 l + 2) Sqrt[1 + r^2])},
   {"t=1/2 (l, l-1/2)", 1/2, l, l - 1/2, r^(2 l)/Sqrt[1 + r^2]},
   {"t=1   (l, l+1)", 1, l, l + 1, r^(2 l) ((2 l + 2) (2 l + 3)/2 + (2 l + 1) (2 l + 3) r^2 + (2 l + 1) (2 l + 2)/2 r^4)/((2 l + 2) (2 l + 3)/2 (1 + r^2))},
   {"t=1   (l, l)", 1, l, l, r^(2 l) ((2 l + 2) + 2 l r^2)/((2 l + 2) (1 + r^2))},
   {"t=1   (l, l-1)", 1, l, l - 1, r^(2 l)/(1 + r^2)}};
Do[Module[{w = wv[[5]]},
   rep["    ", wv[[1]], ": psi0 = ", InputForm[w], ";  H psi0 = 0 for symbolic l: ", Simplify[Hrad[wv[[3]], wv[[4]], wv[[2]]][w], l > 0] === 0,
    ";  psi0/r^(2l) -> 1 at r -> 0: ", Limit[w/r^(2 l), r -> 0, Assumptions -> l > 0], ";  psi0/r^(2j) at r -> infinity: ", Simplify[Limit[w/r^(2 wv[[4]]), r -> Infinity, Assumptions -> l > 0]]]],
  {wv, waves}];


(* ::Subsubsection:: *)
(*Inspect: massless partial waves psi0/r^(2l) for l = 0, 1, 2 (t = 1/2)*)


If[$Notebooks, Plot[Evaluate[Flatten[Table[{waves[[1, 5]]/r^(2 l), If[l > 0, waves[[2, 5]]/r^(2 l), Nothing]}, {l, {1/2, 1, 2}}]]], {r, 0, 5}, AxesLabel -> {"r/rho", "psi0/r^(2l)"}]]


(* ::Section:: *)
(*(e) massless partial-wave sums and alpha(1/2), alpha(1)*)


(* t = 1/2: pairs (l, l+1/2) & (l+1/2, l), ratio (2l+1)/(2l+2), degeneracy (2l+1)(2l+2); k = 2l+1 *)
s12 = Sum[k (k + 1) Log[k/(k + 1)], {k, 1, NN}];
ser12 = Normal[Series[s12 /. NN -> 2 L + 1, {L, Infinity, 1}]] // PowerExpand // Expand;
cst[ser_] := Limit[ser - Limit[ser/L^2, L -> Infinity] L^2 - Limit[(ser - Limit[ser/L^2, L -> Infinity] L^2)/L, L -> Infinity] L -
     Limit[(ser - Limit[ser/L^2, L -> Infinity] L^2 - Limit[(ser - Limit[ser/L^2, L -> Infinity] L^2)/L, L -> Infinity] L)/Log[L], L -> Infinity] Log[L], L -> Infinity];
glaisher = Log[Glaisher] -> 1/12 - Derivative[1][Zeta][-1];
Z12 = FullSimplify[cst[ser12] /. glaisher];
rep["(e) t = 1/2: sum_{l <= L} (2l+1)(2l+2) ln((2l+1)/(2l+2)) = ", Limit[ser12/L^2, L -> Infinity], " L^2 + ", Limit[(ser12 - Limit[ser12/L^2, L -> Infinity] L^2)/L, L -> Infinity],
  " L + (1/6) ln L + Z, Z = ", InputForm[Z12]];
alpha12 = FullSimplify[Z12 + 127/72 - Log[2]/3];
rep["    alpha(1/2) = Z + 127/72 - (1/3) ln 2 (Dunne-Hur-Lee-Min) = ", InputForm[alpha12], " = ", N[alpha12, 15]];
(* t = 1: pairs (l, l+1) & (l+1, l): (2l+1)/(2l+3), degeneracy (2l+1)(2l+3); singles (l, l), l >= 1/2: 2l/(2l+2), degeneracy (2l+1)^2 *)
s1 = Sum[(k + 1) (k + 3) Log[(k + 1)/(k + 3)], {k, 0, NN}] + Sum[(k + 1)^2 Log[k/(k + 2)], {k, 1, NN}];
ser1 = Normal[Series[s1 /. NN -> 2 L, {L, Infinity, 2}]] // PowerExpand // Expand;
Z1 = FullSimplify[cst[ser1] /. glaisher];
rep["    t = 1:   sum_{l <= L} = ", Limit[ser1/L^2, L -> Infinity], " L^2 + ", Limit[(ser1 - Limit[ser1/L^2, L -> Infinity] L^2)/L, L -> Infinity],
  " L + (2/3) ln L + Z, Z = ", InputForm[Z1], " = ", N[Z1, 15]];
alpha1 = FullSimplify[4 alpha12 + Log[2] - 5/6];
rep["    alpha(1) = 4 alpha(1/2) + ln 2 - 5/6 (literature) = ", InputForm[alpha1], " = ", N[alpha1, 15], ";  implied kappa_1 = alpha(1) - Z = ", FullSimplify[alpha1 - Z1],
  " = ", N[alpha1 - Z1, 15], "  (inst_gy.py determines it from decoupling)"];


(* ::Section:: *)
(*(f) heat-kernel and lattice coefficients*)


T1 = Table[-I eps3[[a]], {a, 3}];
A1 = Table[Sum[2 eta[a, m, n] X[[n]]/(r2 + rho^2) T1[[a]], {a, 3}, {n, 4}], {m, 4}];
F1 = fieldStrength[A1];
covD[A_, m_, M_] := D[M, X[[m]]] - I (A[[m]] . M - M . A[[m]]);
Do[Module[{A = tt[[2]], F = tt[[3]], f2, f3, df2, a3},
   f2 = radInt[Simplify[Sum[Tr[F[[i, j]] . F[[i, j]]], {i, 4}, {j, 4}]]];
   f3 = radInt[Simplify[Sum[Tr[F[[i, j]] . F[[j, k]] . F[[k, i]]], {i, 4}, {j, 4}, {k, 4}]]];
   df2 = radInt[Simplify[Sum[Tr[# . #] &[covD[A, k, F[[i, j]]]], {i, 4}, {j, 4}, {k, 4}]]];
   (* a_3 (E = 0, flat; Vassilevich): (4 pi)^-2 (1/360) int tr[-4 (D Omega)^2 + 2 (D_j Omega_ij)^2 - 12 Omega^3], Omega = -i F, D_j F_ij = 0 *)
   a3 = Simplify[1/(16 Pi^2) 1/360 (4 df2 - 12 I f3)];
   rep["(f) ", tt[[1]], ": int tr F^2 = ", f2, ", int tr F_ij F_jk F_ki = ", f3, ", int tr (D F)^2 = ", df2, " (= 4 i int tr F^3: ", Simplify[df2 - 4 I f3] === 0,
    ");  A_3 = ", a3, " -> ln det(-D^2+m^2)/det(-d^2+m^2) contains -", a3, "/m^2"]], {tt, {{"isospin 1/2", Areg, Freg}, {"isospin 1", A1, F1}}}];
sphIB = {r Cos[b1], r Sin[b1] Cos[b2], r Sin[b1] Sin[b2] Cos[b3], r Sin[b1] Sin[b2] Sin[b3]};
wdens = Simplify[Sum[Tr[# . #] &[covD[Areg, m, Freg[[m, n]]]], {m, 4}, {n, 4}]];
wint = Integrate[(wdens /. Thread[X -> sphIB] /. rho -> 1 // Simplify) r^3 Sin[b1]^2 Sin[b2], {b3, 0, 2 Pi}, {b2, 0, Pi}, {b1, 0, Pi}, {r, 0, Infinity}];
rep["    Wilson action: S_W = int [(1/2) tr F^2 - (a^2/12) sum_{mu nu} tr (D_mu F_mu nu)^2] + O(a^4): sum density = ", InputForm[wdens], ", int = ", wint,
  " -> S_W/(8 pi^2) = 1 + (", Simplify[-wint/12/(8 Pi^2)], ") (a/rho)^2"];
cdens = Simplify[Sum[If[eps4[[m, n, s1, s2]] == 0, 0, eps4[[m, n, s1, s2]] Tr[Freg[[m, n]] . (covD[Areg, s1, covD[Areg, s1, Freg[[s1, s2]]]] + covD[Areg, s2, covD[Areg, s2, Freg[[s1, s2]]]])]],
     {m, 4}, {n, 4}, {s1, 4}, {s2, 4}]];
cint = Integrate[(cdens /. Thread[X -> sphIB] /. rho -> 1 // Simplify) r^3 Sin[b1]^2 Sin[b2], {b3, 0, 2 Pi}, {b2, 0, Pi}, {b1, 0, Pi}, {r, 0, Infinity}];
rep["    clover charge: F_clover = F + (a^2/6)(D_mu^2 + D_nu^2) F + O(a^4) -> Q_clover = 1 + (", Simplify[cint 2/6/(32 Pi^2)], ") (a/rho)^2"];
Export[FileNameJoin[{srcDirIB$, "results", "inst_symbolic.txt"}], StringRiffle[outIB$, "\n"] <> "\n", "Text"];
Print["wrote results/inst_symbolic.txt"];
