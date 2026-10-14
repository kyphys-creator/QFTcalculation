(* ::Package:: *)

(* ::Title:: *)
(*Step (11): Schwinger pair production -- symbolic constant-field results and independent numerics (Mathematica)*)


(* ::Text:: *)
(*Research note models/spinor_qed, step (11), Eqs. (eq:schw), (eq:wli), (eq:sauter), App. schw.  Units m = 1 in the*)
(*numerics, F = eE/m^2.  No loop tools: this step is the proper-time integral, the Dirac equation in the Sauter potential and*)
(*the worldline instanton, checked here with Mathematica and in schwinger_numeric.py with Python (scipy, mpmath).*)
(*(a) constant field, symbolic: the residues of the proper-time integrand at tau_n = n pi/(eE) give Im L of Eq. (schw);*)
(*    the weak-field coefficients from the series of z cot z equal zeta(2n) Gamma(2n-2)/(4 pi^(2n+2)) and equal the*)
(*    dispersion (Borel) integrals of Im L term by term.  Numerically: the proper-time integral along tau = t e^{0.4 i}.*)
(*(b) Sauter potential: the reduced Dirac equation by NDSolve at the modes of work/schw_points.txt (transmission T).*)
(*(c) worldline instantons by NDSolve (curvature eE(x3)/m) for E sech^2(k x3), and for E exp(-(k x3)^2): the action*)
(*    m l - e Phi.  (d) Im Gamma/(A T) from Nikishov's nbar by NIntegrate.  -> results/schwinger_mathematica.csv*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file schwinger_exact.wl  (after schwinger_numeric.py --points; run_schwinger_check.sh does both).  Interactive:  ~/hep/bin/wopen schwinger_exact.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


srcDirSW$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
ptsSW$ = StringSplit /@ ReadList[FileNameJoin[{srcDirSW$, "work", "schw_points.txt"}], String];
numSW$[s_] := ToExpression[StringReplace[s, "e" -> "*^"]];
outSW$ = {};


(* ::Section:: *)
(*(a) Constant field*)


(* the integrand of Eq. (schw): L = int_0^inf g(tau) dtau, F = eE *)
gSW$[tau_] := -1/(8 Pi^2) Exp[-mm tau] (FF tau Cot[FF tau] - 1 + (FF tau)^2/3)/tau^3;
(* the path passes above tau_n: 1/(tau - tau_n + i0) -> -i pi delta, so Im L = -pi Res *)
imResSW$ = Table[Simplify[-Pi Residue[gSW$[tau], {tau, n Pi/FF}], FF > 0 && mm > 0], {n, 1, 4}];
Print["(a) Im L from the residues at tau_n = n pi/(eE), n = 1..4 (minus F^2/(8 pi^3 n^2) e^(-n pi m^2/F), expect 0): ",
  Table[Simplify[imResSW$[[n]] - FF^2/(8 Pi^3 n^2) Exp[-n Pi mm/FF]], {n, 4}]];
serSW$ = Normal[Series[z Cot[z] - 1 + z^2/3, {z, 0, 24}]];
coefSW$ = Table[-1/(8 Pi^2) Coefficient[serSW$, z, 2 n] Gamma[2 n - 2], {n, 2, 12}];    (* coefficient of (eE)^(2n)/m^(4n-4) *)
Print["(a) weak-field coefficients minus zeta(2n) Gamma(2n-2)/(4 pi^(2n+2)), n = 2..12 (expect 0): ",
  Simplify[coefSW$ - Table[Zeta[2 n] Gamma[2 n - 2]/(4 Pi^(2 n + 2)), {n, 2, 12}]], ";  n = 2: ", coefSW$[[1]]];
(* dispersion (Borel): (1/pi) int_0^inf d eps Im L(eps)/eps^(n+1), Im L = (eps/(8 pi^3)) sum_k k^-2 exp(-k pi/Sqrt[eps]) *)
borelSW$ = Table[Module[{one = Integrate[eps^(-n) Exp[-kk Pi/Sqrt[eps]], {eps, 0, Infinity}, Assumptions -> kk > 0 && n > 1]},
     1/Pi 1/(8 Pi^3) Sum[one/kk^2, {kk, 1, Infinity}]], {n, 2, 8}];
Print["(a) dispersion integrals minus the coefficients, n = 2..8 (expect 0): ",
  Simplify[borelSW$ - Table[Zeta[2 n] Gamma[2 n - 2]/(4 Pi^(2 n + 2)), {n, 2, 8}]]];


(* ::Subsubsection:: *)
(*Inspect: the first coefficients and the residues*)


If[$Notebooks, {coefSW$[[;; 4]], imResSW$}]


lConstSW$[f_] := Module[{ph = Exp[I 4/10]},
   -1/(8 Pi^2) NIntegrate[ph Exp[-t ph] With[{z = f t ph}, If[Abs[z] < 10^-3, -z^4/45 - 2 z^6/945, z Cot[z] - 1 + z^2/3]]/(t ph)^3,
     {t, 0, 1, 5, 20, 60, 200}, WorkingPrecision -> 30, PrecisionGoal -> 20, MaxRecursion -> 30]];   (* e^(-t cos 0.4) < e^(-180) beyond *)
Do[If[p[[1]] === "const", Module[{f = Rationalize[numSW$[p[[2]]], 0], v},
     v = lConstSW$[f];
     AppendTo[outSW$, {"const", N[f], Re[v], Im[v]}]]], {p, ptsSW$}];
Print["(a) proper-time integral at ", Length[Select[outSW$, #[[1]] == "const" &]], " field strengths; Im L / series - 1 = ",
  ScientificForm[Max[Abs[#[[4]]/N[With[{f = Rationalize[#[[2]], 0]}, f^2/(8 Pi^3) Sum[Exp[-n Pi/f]/n^2, {n, 1, 400}]], 30] - 1] & /@
     Select[outSW$, #[[1]] == "const" &]], 2]];


(* ::Section:: *)
(*(b) The Dirac equation in the Sauter potential*)


(* u' = i[(w - V)u - mt v], v' = -i[(w - V)v - mt u], V = lam tanh(k x); start with the transmitted wave at x = X *)
transSW$[w_, mt_, lam_, k_] := Module[{X = 22/k, er, el, pr, pl, sol, u0, v0, ci, cr, a, b, uX, vX},
   er = w - lam Tanh[k X]; el = w + lam Tanh[k X];
   pr = Sqrt[er^2 - mt^2]; pl = Sqrt[el^2 - mt^2];
   u0 = Exp[-I pr X]; v0 = (er + pr)/mt u0;
   sol = NDSolve[{u'[x] == I ((w - lam Tanh[k x]) u[x] - mt v[x]), v'[x] == -I ((w - lam Tanh[k x]) v[x] - mt u[x]),
       u[X] == u0, v[X] == v0}, {u, v}, {x, -X, X}, WorkingPrecision -> 24, PrecisionGoal -> 16, AccuracyGoal -> Infinity,
      MaxSteps -> 10^6];
   {uX, vX} = {u[-X], v[-X]} /. sol[[1]];
   ci = (el - pl)/mt; cr = (el + pl)/mt;
   {a, b} = LinearSolve[{{Exp[-I pl X], Exp[I pl X]}, {ci Exp[-I pl X], cr Exp[I pl X]}}, {uX, vX}];
   (1 - ((er + pr)/mt)^2)/(Abs[a]^2 (1 - ci^2))];
Do[If[p[[1]] === "mode", Module[{v = Rationalize[numSW$ /@ p[[2 ;; 5]], 0]},
     AppendTo[outSW$, Join[{"mode"}, N[v], {transSW$ @@ v}]]]], {p, ptsSW$}];
nikSW$[w_, mt_, lam_, k_] := With[{p1 = Sqrt[(lam + w)^2 - mt^2], p2 = Sqrt[(lam - w)^2 - mt^2]},
   2 Sinh[Pi p1/k] Sinh[Pi p2/k]/(Cosh[2 Pi lam/k] - Cosh[Pi (p1 - p2)/k])];
Print["(b) Dirac equation vs Nikishov at ", Length[Select[outSW$, #[[1]] == "mode" &]], " modes: max |T/nbar - 1| = ",
  ScientificForm[Max[Abs[#[[6]]/nikSW$ @@ Rationalize[#[[2 ;; 5]], 0] - 1] & /@ Select[outSW$, #[[1]] == "mode" &]], 2]];


(* ::Section:: *)
(*(c) Worldline instantons*)


(* theta' = F h(k x3), x3' = cos theta, x4' = sin theta, flux' = (F/k) f(k x3) sin theta, from the left turning point *)
loopSW$[f0_, gt_, prof_] := Module[{k = gt f0, h, ff, c, sol, send},
   {h, ff} = If[prof === "sech", {Sech[#]^2 &, Tanh}, {Exp[-#^2] &, Sqrt[Pi]/2 Erf[#] &}];
   c = x /. FindRoot[ff[k x] == gt, {x, 1/k}, WorkingPrecision -> 30];
   sol = NDSolve[{x3'[s] == Cos[th[s]], x4'[s] == Sin[th[s]], th'[s] == f0 h[k x3[s]], fl'[s] == f0/k ff[k x3[s]] Sin[th[s]],
       x3[0] == -c, x4[0] == 0, th[0] == -Pi/2, fl[0] == 0, WhenEvent[th[s] == 3 Pi/2, send = s; "StopIntegration"]},
      {x3, x4, th, fl}, {s, 0, 10^4}, WorkingPrecision -> 25, PrecisionGoal -> 16, AccuracyGoal -> 20];
   {send - (fl[send] /. sol[[1]]), {x3[send] + c, x4[send]} /. sol[[1]], sol}];
Do[If[p[[1]] === "loop", Module[{gt = Rationalize[numSW$[p[[2]]], 0], r},
     r = loopSW$[1/2, gt, "sech"];
     AppendTo[outSW$, {"loop", N[gt], r[[1]]}]]], {p, ptsSW$}];
Print["(c) sech^2 instantons (F = 1/2): S0 numerical / closed form - 1 = ",
  ScientificForm[Abs[#[[3]]/(2 Pi 2/(1 + Sqrt[1 - #[[2]]^2])) - 1] & /@ Select[outSW$, #[[1]] == "loop" &], 2]];
Do[If[p[[1]] === "gauss", Module[{inv = numSW$[p[[2]]], gt = Rationalize[numSW$[p[[3]]], 0], r},
     r = loopSW$[1/inv, gt, "gauss"];
     AppendTo[outSW$, {"gauss", N[inv], N[gt], r[[1]]}]]], {p, ptsSW$}];
Print["(c) Gaussian instantons: S0 = ", Select[outSW$, #[[1]] == "gauss" &][[All, 4]]];


(* ::Subsubsection:: *)
(*Inspect: an instanton loop (sech^2, gt = 0.8, F = 1/2) against the closed form of Dunne and Schubert*)


If[$Notebooks, Module[{r = loopSW$[1/2, 4/5, "sech"], sol, send, a = 1/Sqrt[1 - (4/5)^2]},
  sol = r[[3]]; send = r[[1]];
  Show[ParametricPlot[{x3[s], x4[s]} /. sol[[1]], {s, 0, 50}, PlotStyle -> Thick],
   ParametricPlot[2 {ArcSinh[4/5 a Sin[t]]/(4/5), a ArcSin[4/5 Cos[t]]/(4/5) - a ArcSin[4/5]/(4/5)}, {t, 0, 2 Pi},
    PlotStyle -> Dashed], AspectRatio -> Automatic, PlotRange -> All]]]


(* ::Section:: *)
(*(d) Im Gamma for the Sauter potential*)


(* nbar with exponentials (no overflow) and Im Gamma/(A T) = -(1/8 pi^2) int dw d(mt^2) ln(1 - nbar) *)
nbarSW$[w_, m2_, lam_, k_] := Module[{p1 = Sqrt[(lam + w)^2 - m2], p2 = Sqrt[(lam - w)^2 - m2], a, b, c, d},
   a = Pi p1/k; b = Pi p2/k; c = 2 Pi lam/k; d = Abs[Pi (p1 - p2)/k];
   Exp[a + b - c] (1 - Exp[-2 a]) (1 - Exp[-2 b])/(1 + Exp[-2 c] - Exp[d - c] (1 + Exp[-2 d]))];
imGammaSW$[f0_, gt_] := Module[{k = gt f0, lam = 1/gt, sm, sw},
   sm = f0 Sqrt[1 - gt^2]/Pi;                                   (* decay scale of nbar in mt^2: mt^2 = 1 + sm y *)
   sw = 1/Sqrt[2 Pi k^2/(f0^3 (1 - gt^2)^(3/2))];               (* Gaussian width in omega: omega = sw u *)
   (* a numeric-only integrand: NIntegrate's symbolic preprocessing of the closed form fails (inumri) *)
   integrandSW$[uu_?NumericQ, yy_?NumericQ] := sw sm (-Log[1 - nbarSW$[sw uu, 1 + sm yy, lam, k]]);
   2/(8 Pi^2) NIntegrate[integrandSW$[u, y], {u, 0, (lam - 1)/sw}, {y, 0, ((lam - sw u)^2 - 1)/sm},
      WorkingPrecision -> 30, PrecisionGoal -> 12, MaxRecursion -> 50]];
Do[If[p[[1]] === "total", Module[{inv = numSW$[p[[2]]], gt = Rationalize[numSW$[p[[3]]], 0]},
     AppendTo[outSW$, {"total", N[inv], N[gt], imGammaSW$[1/inv, gt]}]]], {p, ptsSW$}];
Print["(d) Im Gamma/(A T) at ", Length[Select[outSW$, #[[1]] == "total" &]], " points; ratio to the semiclassical formula: ",
  NumberForm[#[[4]]/((1/#[[2]])^(5/2) (1 - #[[3]]^2)^(5/4)/(8 Pi^3 #[[3]]/#[[2]]) Exp[-Pi #[[2]] 2/(1 + Sqrt[1 - #[[3]]^2])]), 6] & /@
   Select[outSW$, #[[1]] == "total" &]];


(* ::Subsubsection:: *)
(*Inspect: the table*)


If[$Notebooks, TableForm[N[outSW$, 12]]]


strSW$[x_] := If[StringQ[x], x, ToString[CForm[N[x, 20]]]];
Quiet[CreateDirectory[FileNameJoin[{srcDirSW$, "results"}]]];
Export[FileNameJoin[{srcDirSW$, "results", "schwinger_mathematica.csv"}],
  StringRiffle[Prepend[StringRiffle[strSW$ /@ #, ","] & /@ outSW$, "kind,values"], "\n"] <> "\n", "Text"];
Print["(d) wrote results/schwinger_mathematica.csv"];
