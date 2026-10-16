(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: heat-kernel coefficients of -D^2 in the BPST background by the DeWitt recursion (exact)*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices.  app:inst 「大きい質量の展開。」 (N2b): heat-kernel coefficients of -D^2 in the*)
(*BPST background (rho = 1, g = 1, regular gauge, D = d - i A), isospin t = 1/2, by the DeWitt recursion in the Fock-Schwinger gauge at*)
(*x' = (r,0,0,0):  K(x'+y, x'; s) = (4 pi s)^-2 e^{-y^2/4s} sum_n a_n(y) s^n, (n + y.d) a_n = D'^2 a_{n-1}, a_0 = 1, y.A' = 0.*)
(*tr a_n(0) is evaluated exactly at rational r, fitted to P(r^2)/(1+r^2)^(2n), and A_n = (1/8) int_0^infinity r^3 tr a_n dr.*)
(*Expected: A_2 = -T/6, A_3 = 2T/75, A_4 = 8 T (7C-1)/735 (T = 1/2, C = 3/4).  Higher n: deriv_inst_dewitt_modp.py; t = 1:*)
(*deriv_inst_dewitt_num.py 4 both.*)
(*Argument: nmax (default 4; run_deriv_check.sh passes 4).  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_inst_dewitt.txt.*)
(*Usage (from Src/): wolframscript -file deriv_inst_dewitt.wl 4   (a few seconds)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_inst_dewitt.wl 4  (the argument nmax; 4 by default and in the notebook).  Interactive:  ~/hep/bin/wopen deriv_inst_dewitt.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


(* the argument nmax in batch; 4 in a notebook (where $ScriptCommandLine may hold the options of the front end or of wolframscript) *)
nmax = ToExpression[If[!$Notebooks && Length[$ScriptCommandLine] > 1, $ScriptCommandLine[[2]], "4"]];
sig = PauliMatrix /@ {1, 2, 3};
eps3 = LeviCivitaTensor[3];
eta[a_, m_, n_] := Which[m <= 3 && n <= 3, eps3[[a, m, n]], n == 4 && m <= 3, KroneckerDelta[a, m], m == 4 && n <= 3, -KroneckerDelta[a, n], True, 0];


(* ::Subsubsection:: *)
(*Inspect: the 't Hooft symbols eta_{a mu nu}, a = 1, 2, 3*)


If[$Notebooks,
  MatrixForm /@ Table[eta[a, m, n], {a, 3}, {m, 4}, {n, 4}]
]


Y = {y1, y2, y3, y4};

(* ::Section:: *)
(*the recursion in the Fock-Schwinger gauge*)


(* homogeneous-part representation: list {H_0, H_1, ..., H_K}, each a matrix of homogeneous polynomials of degree k *)
hmul[a_, b_, K_] := Table[Expand[Sum[a[[i + 1]] . b[[k - i + 1]], {i, 0, k}]], {k, 0, K}];
hd[a_, mu_] := Append[Table[Expand[D[a[[k + 2]], Y[[mu]]]], {k, 0, Length[a] - 2}], 0 a[[1]]];
coeffs[tiso_, rr_] := Module[{T, dim, K, xp, Aser, yA, Phi, PhiInv, Ap, aL, res, divA, AA, Dsq, lam},
  T = If[tiso == 1/2, sig/2, Table[-I eps3[[c]], {c, 3}]];
  dim = Length[T[[1]]];
  K = 2 nmax;   (* degree of Phi; A' needed to degree 2 nmax - 1, a_1 to degree 2 nmax - 2 *)
  xp = {rr, 0, 0, 0};
  (* A_mu(x'+lam y) as homogeneous parts in y *)
  Aser = Table[Module[{X = xp + lam Y, s},
      s = Normal[Series[Sum[2 eta[aa, mu, nu] X[[nu]]/(X . X + 1) T[[aa]], {aa, 3}, {nu, 4}], {lam, 0, K}]];
      Table[Map[Expand[Coefficient[#, lam, k]] &, s, {2}], {k, 0, K}]], {mu, 4}];
  (* lam y.A(x'+lam y): degree-j part = y.A^(j-1) *)
  yA = Prepend[Table[Expand[Sum[Y[[mu]] Aser[[mu, j]], {mu, 4}]], {j, 1, K}], 0 IdentityMatrix[dim]];
  Phi = {IdentityMatrix[dim]};
  Do[AppendTo[Phi, Expand[I/k Sum[yA[[j + 1]] . Phi[[k - j + 1]], {j, 1, k}]]], {k, 1, K}];
  PhiInv = {IdentityMatrix[dim]};
  Do[AppendTo[PhiInv, Expand[-Sum[PhiInv[[j + 1]] . Phi[[k - j + 1]], {j, 0, k - 1}]]], {k, 1, K}];
  Ap = Table[hmul[PhiInv, hmul[Aser[[mu]], Phi, K - 1], K - 1] + I hmul[PhiInv, hd[Phi, mu], K - 1], {mu, 4}];
  If[Union[Flatten[Table[Expand[Sum[Y[[mu]] Ap[[mu, k + 1]], {mu, 4}]], {k, 0, K - 1}]]] =!= {0}, Print["FS gauge check failed at r = ", rr]];
  divA = Total[Table[hd[Ap[[mu]], mu], {mu, 4}]];
  AA = Total[Table[hmul[Ap[[mu]], Ap[[mu]], K - 1], {mu, 4}]];
  Dsq[x_, Kx_] := Take[Total[Table[hd[hd[x, mu], mu], {mu, 4}]], Kx + 1] - I hmul[divA, x, Kx] - 2 I Total[Table[hmul[Ap[[mu]], hd[x, mu], Kx], {mu, 4}]] - hmul[AA, x, Kx];
  aL = Join[{IdentityMatrix[dim]}, Table[0 IdentityMatrix[dim], {K}]];
  res = {};
  Do[Module[{Kn = 2 (nmax - n), d2},
     d2 = Dsq[aL, Kn];
     aL = Join[Table[Expand[d2[[k + 1]]/(n + k)], {k, 0, Kn}], Table[0 IdentityMatrix[dim], {K - Kn}]];
     AppendTo[res, Tr[aL[[1]]]]], {n, 1, nmax}];
  res];


(* ::Subsubsection:: *)
(*Inspect: tr a_n(0), n = 1..nmax, at r = 1*)


If[$Notebooks,
  coeffs[1/2, 1]
]


(* ::Section:: *)
(*t = 1/2: tr a_n(0) at 12 points, the fit and A_n*)


Do[Module[{f, pts, vals, T, C, fits},
   f[rr_] := coeffs[t, rr];
   T = If[t == 1/2, 1/2, 2]; C = t (t + 1);
   pts = {0, 1/3, 1/2, 1, 3/2, 2, 3, 4, 5, 7, 9, 11};
   vals = Table[f[rr], {rr, pts}];
   Print["t = ", t, ":  tr a_1(0) at the points: ", vals[[All, 1]]];
   Do[Module[{u, poly, frac, An, deg, chk},
      poly = Expand[InterpolatingPolynomial[Table[{pts[[i]]^2, vals[[i, n]] (1 + pts[[i]]^2)^(2 n)}, {i, Length[pts] - 2}], u]];
      deg = Exponent[poly, u];
      chk = Table[(poly /. u -> pts[[i]]^2)/(1 + pts[[i]]^2)^(2 n) - vals[[i, n]], {i, Length[pts] - 1, Length[pts]}];
      frac = poly/(1 + u)^(2 n);
      An = Integrate[(frac /. u -> r^2) r^3, {r, 0, Infinity}]/8;
      Print["   n = ", n, ": tr a_n(0) = (", InputForm[poly], ")/(1+r^2)^", 2 n, "  [degree ", deg, ", extra-point check ", chk, "];  A_n = ", InputForm[An], " = ", N[An, 12]];
      If[n == 2, Print["      expected -T/6 = ", -T/6]];
      If[n == 3, Print["      expected 2T/75 = ", 2 T/75]];
      If[n == 4, Print["      expected 8T(7C-1)/735 = ", 8 T (7 C - 1)/735]];
      If[n == 5 && t == 1/2, Print["      literature: -2 A_5 = 232/2835 -> A_5 = ", -116/2835, ";  -2 A_5 = ", InputForm[-2 An]]];
      If[n == 6 && t == 1/2, Print["      literature: -6 A_6 = -7916/148225 -> A_6 = ", 7916/(6 148225), ";  -6 A_6 = ", InputForm[-6 An]]];
      ], {n, 2, nmax}]], {t, {1/2}}];  (* t = 1 (3x3 matrices) is too slow in exact arithmetic here; see deriv_inst_dewitt_num.py 4 both *)