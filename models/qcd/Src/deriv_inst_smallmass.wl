(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: the small-mass term of the instanton quark determinant*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices.  app:inst 「小さい質量の展開。」 (N2a): the small-mass term of Gamma~^S*)
(*(isospin 1/2, rho = 1, g = 1), via d Gamma/dm^2 = int d^4x g_m(x), g_m(x) = lim_{y->x} {tr[G_m(x,y) Phi(y,x)] - tr G^0_m(x-y)}.*)
(*(1) the massless propagator in the singular gauge: which quaternion ordering solves -D_x^2 Delta = 0;*)
(*(2) g_0(x) from the straight-line transporter to second order, several directions n;*)
(*(3) far field: the colour-singlet part of Delta - Delta_0 -> -2 pi^2 Delta_0(x) Delta_0(y);*)
(*(4) D_0 = lim [int_{|x|<R} g_0 + (1/2) ln R] = 1/4 and C_K = int du/u [(u K_1(u))^2 - theta(1-u)] = ln 2 - gamma - 1/2;*)
(*(5) d Gamma/dm^2 = (1/2) ln m + D_0 - C_K/2, integrated: Gamma~ - alpha = (m^2/2)[ln(m/2) + gamma + 1/2];*)
(*(2') the e^2 coefficient for general x, n, rho.*)
(*Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_inst_smallmass.txt.*)
(*Usage (from Src/): wolframscript -file deriv_inst_smallmass.wl   (a few seconds)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_inst_smallmass.wl.  Interactive:  ~/hep/bin/wopen deriv_inst_smallmass.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


sig = PauliMatrix /@ {1, 2, 3}; id2 = IdentityMatrix[2]; eps3 = LeviCivitaTensor[3];
etab[a_, m_, n_] := Which[m <= 3 && n <= 3, eps3[[a, m, n]], n == 4 && m <= 3, -KroneckerDelta[a, m], m == 4 && n <= 3, KroneckerDelta[a, n], True, 0];
s = Append[I sig, id2]; sb = Append[-I sig, id2];
X = {x1, x2, x3, x4}; Yv = {y1, y2, y3, y4};
x2s = X . X; y2s = Yv . Yv; d2 = (X - Yv) . (X - Yv);
A = Table[Sum[2 etab[a, m, n] X[[n]]/(x2s (x2s + 1)) sig[[a]]/2, {a, 3}, {n, 4}], {m, 4}];

(* ::Section:: *)
(*(1) the massless propagator in the singular gauge*)


qq[b1_, b2_] := Sum[X[[m]] b1[[m]], {m, 4}] . Sum[Yv[[m]] b2[[m]], {m, 4}];
cands = {{"x.s y.sbar", qq[s, sb]}, {"x.sbar y.s", qq[sb, s]}, {"x.s y.s", qq[s, s]}, {"x.sbar y.sbar", qq[sb, sb]}};
Dx[m_, F_] := D[F, X[[m]]] - I A[[m]] . F;
pt = {x1 -> 3/7, x2 -> -2/5, x3 -> 1/3, x4 -> 5/4, y1 -> -1/2, y2 -> 2/3, y3 -> 1/5, y4 -> -3/4};
good = Null;
Do[Module[{Del, lap},
   Del = (id2 + c[[2]]/(x2s y2s))/(4 Pi^2 d2 Sqrt[(1 + 1/x2s) (1 + 1/y2s)]);
   lap = Sum[Dx[m, Dx[m, Del]], {m, 4}] /. pt;
   Print["(1) ", c[[1]], ": D_x^2 Delta at a rational point = ", Simplify[lap]];
   If[Simplify[lap] === {{0, 0}, {0, 0}} && good === Null, good = {c[[1]], Del, c[[2]]}]], {c, cands}];
Print["    -> propagator with ", good[[1]], ";  q(x) qbar(x) = x^2: ", Simplify[(good[[3]] /. Thread[Yv -> X]) - x2s id2] === {{0, 0}, {0, 0}}];


(* ::Subsubsection:: *)
(*Inspect: the massless propagator Delta(x, y) in the singular gauge*)


If[$Notebooks,
  good[[2]]
]


(* ::Section:: *)
(*(2) covariant point splitting*)


(* (2) covariant point splitting at x = (r,0,0,0), y = x + e n *)
Del = good[[2]];
nv = {n1, n2, n3, n4};
nA = Sum[nv[[m]] A[[m]], {m, 4}];
ndnA = Sum[nv[[k]] D[nA, X[[k]]], {k, 4}];
Phi = id2 + I e nA + e^2/2 (I ndnA + (I nA) . (I nA));
Fx = 4 Pi^2 d2 Del;
expr = Tr[(Fx /. Thread[Yv -> X + e nv]) . Phi] /. {x1 -> r, x2 -> 0, x3 -> 0, x4 -> 0};
ser = Series[expr, {e, 0, 2}];
c0 = Simplify[SeriesCoefficient[ser, 0], r > 0]; c1 = Simplify[SeriesCoefficient[ser, 1], r > 0]; c2 = SeriesCoefficient[ser, 2];


(* ::Subsubsection:: *)
(*Inspect: the e^2 coefficient for n = (1,0,0,0) at x = (r,0,0,0)*)


If[$Notebooks,
  Simplify[c2 /. Thread[nv -> {1, 0, 0, 0}], r > 0]
]


Print["(2) tr[4 pi^2 (x-y)^2 Delta Phi] = ", c0, " + e (", c1, ") + e^2 (...)"];
Do[Print["    n = ", nn, ":  4 pi^2 g_0 = ", Factor[Simplify[(c2 /. Thread[nv -> nn])/(nn . nn), r > 0]]], {nn, {{1, 0, 0, 0}, {0, 1, 0, 0}, {0, 0, 0, 1}, {1, 1, 0, 0}, {1, 2, -1, 3}}}];
g0 = -1/(4 Pi^2 (r^2 + 1)^2);

(* ::Section:: *)
(*(3) far field*)


(* (3) far field *)
far = Simplify[Tr[Del - id2/(4 Pi^2 d2)]/2 /. Thread[X -> lam X] /. Thread[Yv -> lam Yv]];
Print["(3) colour-singlet part of Delta - Delta_0, leading at large scale: ", Simplify[Limit[far lam^4, lam -> Infinity]], "  vs -2 pi^2 Delta_0(x) Delta_0(y) = ", Simplify[-2 Pi^2/(16 Pi^4 x2s y2s)]];

(* ::Section:: *)
(*(4) D_0 and C_K*)


(* (4) *)
D0 = Limit[Integrate[2 Pi^2 r^3 g0, {r, 0, R}, Assumptions -> R > 0] + Log[R]/2, R -> Infinity];
CK = NIntegrate[(u BesselK[1, u])^2/u - If[u < 1, 1/u, 0], {u, 0, 1, Infinity}, WorkingPrecision -> 30, PrecisionGoal -> 20];
Print["(4) D_0 = ", D0, ";  C_K = ", CK, "  vs ln 2 - EulerGamma - 1/2 = ", N[Log[2] - EulerGamma - 1/2, 25]];
CKexact = Limit[Integrate[u^(1 + 2 ep) BesselK[1, u]^2, {u, 0, Infinity}, Assumptions -> ep > 0] - 1/(2 ep), ep -> 0];
Print["    C_K in closed form (analytic regularization u^(2 ep)): ", FullSimplify[CKexact]];

(* ::Section:: *)
(*(5) d Gamma/dm^2 and the small-mass term*)


(* (5) *)
dG = Log[m]/2 + D0 - (Log[2] - EulerGamma - 1/2)/2;
Gt = Integrate[(dG /. m -> Sqrt[mm2]), {mm2, 0, m^2}, Assumptions -> m > 0];
Print["(5) d Gamma/dm^2 = ", Simplify[dG], ";  Gamma~ - alpha(1/2) = ", Simplify[Gt - m^2/2 (Log[m/2] + EulerGamma + 1/2), m > 0], " + (m^2/2)[ln(m/2) + gamma + 1/2]"];


(* ::Subsubsection:: *)
(*Inspect: Gamma~ - alpha(1/2) as a function of m*)


If[$Notebooks,
  Simplify[Gt, m > 0]
]


(* ::Section:: *)
(*(2') the e^2 coefficient for general x, n, rho*)


(* (2') the three pieces of the e^2 coefficient, general x and n, rho restored *)
Xn = {x1, x2, x3, x4}; nvec = {n1, n2, n3, n4};
ys = Xn + e nvec; xx = Xn . Xn; yy = ys . ys; xn = Xn . nvec; nn2 = nvec . nvec;
hsing = (xx yy + rho^2 Xn . ys)/Sqrt[xx yy (xx + rho^2) (yy + rho^2)];
c2s = Simplify[SeriesCoefficient[2 hsing, {e, 0, 2}], Assumptions -> rho > 0 && xx > 0];
Print["(2') singlet part 2h: e^1 coefficient ", Simplify[SeriesCoefficient[2 hsing, {e, 0, 1}]]];
Print["     e^2 coefficient minus [-rho^2 n^2/(x^2+rho^2)^2 - rho^4 (x^2 n^2 - (x.n)^2)/(x^4 (x^2+rho^2)^2)] = ",
  Simplify[c2s - (-rho^2 nn2/(xx + rho^2)^2 - rho^4 (xx nn2 - xn^2)/(xx^2 (xx + rho^2)^2))]];