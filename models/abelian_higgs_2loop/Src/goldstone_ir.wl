(* ::Package:: *)

(* ::Title:: *)
(*Step (3): the Goldstone boson at small G and its resummation (abelian Higgs model, Landau gauge)*)


(* ::Text:: *)
(*Research note models/abelian_higgs_2loop, step (3).  G = xg = -m2 + lam phi^2 vanishes at the tree minimum.  Following*)
(*Martin (arXiv:1406.2355), with one Goldstone boson:*)
(*  (a) soft limit: V2 = (Delta1/2) G ln G + (terms without ln G) + O(G^2 ln G),*)
(*      Delta1 = 3 lam A(H) + e^2 [3 A(xa) + 2 xa]  (the zero-momentum Goldstone self-energy from h and A loops),*)
(*      checked with the small-G expansions of I (Martin's Eqs. (A.27), (A.28));*)
(*  (b) the minimization condition: delta2 = (1/phi) dV2/dphi = lam Delta1 ln G + finite as G -> 0 (derivatives of I from*)
(*      Martin's Eq. (A.23)); the G-free form  G = -Dh1/K - Dh2/K^2  of the resummed potential,*)
(*      Dh1 = 3 lam A(h) + e^2 [3 A(xa) + 2 xa],  Dh2 = lim [delta2 - lam Delta1 ln G] - 3 lam Dh1 ln h,  h = 2 lam v^2;*)
(*  (c) the hbar expansion of the VEV around the tree minimum (v = phi0 + phi1/K + phi2/K^2) from the usual potential:*)
(*      the ln G of V2' and phi1 V1'' cancel, and phi2 equals the one from the G-free condition;*)
(*  (d) the minimum value Vh_min(v) of the resummed potential, against the hbar expansion*)
(*      V_min = V0 + V1/K + [V2 - V1'^2/(2 V0'')]/K^2 at phi0;*)
(*  (e) RG invariance of the minimization condition and of Vh_min through 1/K^2 (RG functions of step (2));*)
(*  (f) numbers at the benchmark (Q = 1 and Q = 2, couplings scaled by s), I(x,y,z) from TSIL (work/v2_tsil)*)
(*      -> results/goldstone_min.csv; the formulas -> results/goldstone.m.*)
(*Batch: wolframscript -file goldstone_ir.wl*)


(* ::Section:: *)
(*Setup*)


srcDirGI$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirGI$ = FileNameJoin[{srcDirGI$, "results"}];
tsilGI$ = FileNameJoin[{srcDirGI$, "work", "v2_tsil"}];
{v2GI$, massesGI$} = {"V2", "masses"} /. Get[FileNameJoin[{resDirGI$, "v2_landau.m"}]];
rgGI$ = Get[FileNameJoin[{resDirGI$, "rg2.m"}]];

A[0] = 0;
Derivative[1][A] = (A[#]/# + 1) &;                                  (* dA/dx = ln x *)
canonGI$ = II[x__] :> II @@ Sort[{x}];
(* Martin, arXiv:1406.2355, Eq. (A.23): dI(x,y,z)/dx *)
dIGI$[x_, y_, z_] := ((x - y - z) II[x, y, z] - 2 A[y] A[z] + (x - y + z) A[x] A[y]/x + (x + y - z) A[x] A[z]/x +
     (y + z - x) (A[x] + A[y] + A[z]) + x^2 - (y + z)^2)/(x^2 + y^2 + z^2 - 2 x y - 2 x z - 2 y z);
Derivative[1, 0, 0][II] = dIGI$;
Derivative[0, 1, 0][II] = dIGI$[#2, #1, #3] &;
Derivative[0, 0, 1][II] = dIGI$[#3, #1, #2] &;
zeroQGI$[e_] := Module[{t = Together[e]}, Expand[Numerator[t]] === 0];

delta1GI$[hh_, xa_] := 3 lam A[hh] + el^2 (3 A[xa] + 2 xa);
d1hatGI$[v_] := delta1GI$[2 lam v^2, el^2 v^2];
v1GI$ = 1/4 (xh A[xh] - xh^2/2 + xg A[xg] - xg^2/2 + 3 xa A[xa] + xa^2/2) /. massesGI$;
v0GI$ = Lam - m2 phi^2/2 + lam phi^4/4;
(* G -> 0 at fixed phi (m2 = lam phi^2 - G), keeping ln G as the symbol lG *)
smallGGI$[e_] := Expand[(e /. m2 -> lam phi^2 - G) /. A[G] -> G (lG - 1)] /. G -> 0 /. canonGI$;


(* ::Section:: *)
(*(a) V2 for small G*)


SetAttributes[IIo, Orderless];
softRulesGI$ = {
   (* Martin Eq. (A.27): I(G,G,x) *)
   IIo[xg, xg, x_] :> II[0, 0, x] + 2 xg (-x - II[0, 0, x] + 3 A[x] - A[x] lG)/x,
   (* Martin Eq. (A.28): I(G,x,y), symmetric in x, y; x = 0 allowed *)
   IIo[xg, x_, y_] :> II[0, x, y] + xg (-(x + y) II[0, x, y] - 2 A[x] A[y] + 3 x A[x] + 3 y A[y] - y A[x] - x A[y] -
        (x + y)^2 + (x - y) (A[y] - A[x]) lG)/(x - y)^2};
v2SoftGI$ = Normal[Series[v2GI$ /. II -> IIo /. softRulesGI$ /. IIo -> II /. A[xg] -> xg (lG - 1), {xg, 0, 1}]] /.
   canonGI$;
Module[{c1 = Coefficient[Expand[v2SoftGI$], xg, 1], cL, c2},
  cL = Coefficient[c1, lG, 1]; c2 = Coefficient[c1, lG, 2];
  Print["(a) terms G ln^2 G in V2 (expect 0): ", c2];
  Print["(a) [coefficient of G ln G] - Delta1/2 at xh = 2 lam phi^2, xa = e^2 phi^2 (expect 0): ",
   Simplify[(cL - delta1GI$[xh, xa]/2) /. {lam -> xh/(2 phi^2), el -> Sqrt[xa]/phi}, xh > 0 && xa > 0 && phi > 0]]];


(* ::Section:: *)
(*(b) The minimization condition*)


delta2GI$ = smallGGI$[D[v2GI$ /. massesGI$, phi]/phi];
Print["(b) delta2 at G -> 0: coefficient of ln^2 G (expect 0): ", Coefficient[Expand[delta2GI$], lG, 2],
  ";  coefficient of ln G - lam Dh1 (expect 0): ", zeroQGI$[Coefficient[Expand[delta2GI$], lG, 1] - lam d1hatGI$[phi]] /.
   True -> 0];
(* Dh2(v): the remainder, with H = h + G and G = -Dh1/K + ... in 3 lam A(H) *)
d2hatGI$ = Collect[Expand[(delta2GI$ /. lG -> 0) - 3 lam d1hatGI$[phi] (A[2 lam phi^2]/(2 lam phi^2) + 1)],
   {_A, _II}, Together];
Print["(b) Dh2 has no G, m2, ln G: ", FreeQ[d2hatGI$, G | m2 | lG], ";  the I functions in it: ",
  Union[Cases[d2hatGI$, _II, Infinity]]];
d2hatFnGI$[v_] := d2hatGI$ /. phi -> v;


(* ::Section:: *)
(*(c) hbar expansion of the VEV*)


Module[{v1p, v1pp, phi1, phi2h, phi2g},
  v1p = smallGGI$[D[v1GI$, phi]];
  v1pp = smallGGI$[D[v1GI$, {phi, 2}]];
  Print["(c) V1'(phi0) - phi0 Dh1 (expect 0): ", zeroQGI$[v1p - phi d1hatGI$[phi]] /. True -> 0];
  phi1 = -d1hatGI$[phi]/(2 lam phi);
  (* from the usual potential: phi2 = -[V2' + phi1 V1'' + phi1^2 V0'''/2]/V0'', V0'' = 2 lam phi0^2, V0''' = 6 lam phi0 *)
  phi2h = -(phi delta2GI$ + phi1 v1pp + phi1^2/2 6 lam phi)/(2 lam phi^2);
  (* from the G-free condition lam v^2 - m2 + Dh1(v)/K + Dh2(v)/K^2 = 0 *)
  phi2g = -(lam phi1^2 + (D[d1hatGI$[v], v] /. v -> phi) phi1 + d2hatGI$)/(2 lam phi);
  Print["(c) ln G in phi2 from the usual potential (expect 0): ",
   zeroQGI$[Coefficient[Expand[phi2h], lG, 1]] /. True -> 0,
   ";  phi2 (usual) - phi2 (G-free) (expect 0): ", zeroQGI$[phi2h - phi2g] /. True -> 0]];


(* ::Section:: *)
(*(d) The minimum value*)


fGI$[x_] := (x A[x] - x^2/2)/4;                                     (* x^2 (ln x - 3/2)/4 *)
fVGI$[x_] := (x A[x] + x^2/6)/4;                                    (* x^2 (ln x - 5/6)/4 *)
v2G0GI$[v_] := v2GI$ /. {xg -> 0, xh -> 2 lam v^2, xa -> el^2 v^2, phi -> v} /. canonGI$;
(* Vh_min(v) = Lam - lam v^4/4 + [f(h) + 3 fV(xa) - v^2 Dh1/2]/K + [V2(G = 0) - v^2 Dh2/2 - Dh1 A(h)/2]/K^2 *)
vhMinGI$[v_] := Lam - lam v^4/4 + kk (fGI$[2 lam v^2] + 3 fVGI$[el^2 v^2] - v^2 d1hatGI$[v]/2) +
   kk^2 (v2G0GI$[v] - v^2 d2hatFnGI$[v]/2 - d1hatGI$[v] A[2 lam v^2]/2);
Module[{phi1, phi2, vh, vmh},
  phi1 = -d1hatGI$[phi]/(2 lam phi);
  phi2 = -(lam phi1^2 + (D[d1hatGI$[v], v] /. v -> phi) phi1 + d2hatGI$)/(2 lam phi);
  vh = Normal[Series[vhMinGI$[phi + kk phi1 + kk^2 phi2], {kk, 0, 2}]];
  (* hbar expansion at fixed m2 = lam phi0^2 *)
  vmh = Lam - lam phi^4/4 + kk (fGI$[2 lam phi^2] + 3 fVGI$[el^2 phi^2]) +
    kk^2 (v2G0GI$[phi] - (phi d1hatGI$[phi])^2/(2 2 lam phi^2));
  Print["(d) Vh_min(v(m2)) - V_min (hbar expansion), orders 1, 1/K, 1/K^2 (expect 0): ",
   Table[zeroQGI$[Coefficient[vh - vmh, kk, k] /. canonGI$] /. True -> 0, {k, 0, 2}]]];


(* ::Section:: *)
(*(e) RG invariance*)


qDGI$[f_] := 2 D[f /. {A[x_] :> A[x] - t x, II[x_, y_, z_] :> II[x, y, z] + t (A[x] + A[y] + A[z] - x - y - z)}, t] /.
   t -> 0;
rgOpGI$[f_, k_] := rgGI$["lam"][[k]] D[f, lam] + rgGI$["el"][[k]] D[f, el] + rgGI$["m2"][[k]] D[f, m2] +
   rgGI$["Lam"][[k]] D[f, Lam] - rgGI$["gamma"][[k]] phi D[f, phi];
Module[{fmin, sol, dF, vm, dV},
  sol = m2 -> lam phi^2 + kk d1hatGI$[phi] + kk^2 d2hatGI$;
  fmin = lam phi^2 - m2 + kk d1hatGI$[phi] + kk^2 d2hatGI$;
  dF = Normal[Series[(qDGI$[fmin] + kk rgOpGI$[fmin, 1] + kk^2 rgOpGI$[fmin, 2]) /. sol, {kk, 0, 2}]] /. canonGI$;
  Print["(e) Q d/dQ of the minimization condition, orders 1/K, 1/K^2 (expect 0): ",
   Table[zeroQGI$[Coefficient[dF, kk, k]] /. True -> 0, {k, 1, 2}]];
  vm = vhMinGI$[phi];
  dV = Normal[Series[(qDGI$[vm] + kk rgOpGI$[vm, 1] + kk^2 rgOpGI$[vm, 2]) /. sol, {kk, 0, 2}]] /. canonGI$;
  Print["(e) Q d/dQ of Vh_min, orders 1, 1/K, 1/K^2 (expect 0): ",
   Table[zeroQGI$[Coefficient[dV, kk, k]] /. True -> 0, {k, 0, 2}]]];


(* ::Section:: *)
(*(f) Numbers*)


(* I(x,y,z) at Q^2 = qq from TSIL; A(x) = x (ln(x/qq) - 1) *)
numGI$[e_, qq_] := Module[{ii, vals, out},
   ii = Union[Cases[e, II[__?NumericQ], Infinity]];
   If[ii === {}, Return[N[e //. A[x_?NumericQ] :> x (Log[x/qq] - 1)]]];
   out = RunProcess[{tsilGI$}, "StandardOutput",
     StringJoin[(StringRiffle[ToString[CForm[N[#]]] & /@ Append[List @@ #, qq], ","] <> "\n") & /@ ii]];
   vals = ImportString[out, "CSV"][[2 ;;, 5]];
   N[e /. Thread[ii -> vals] //. A[x_?NumericQ] :> x (Log[x/qq] - 1)]];
rowsGI$ = Flatten[Table[
    Module[{pars, p0, d1, d2, fv, vG, phi1, phi2, vhb, vhG, vmh, vm1},
     pars = {lam -> s 25/32, el -> Sqrt[s]/2, m2 -> 25/8, Lam -> 0, kk -> 1/(16 Pi^2)};
     p0 = Sqrt[m2/lam] /. pars;
     d1[v_] := numGI$[d1hatGI$[v] /. pars, qq];
     d2[v_] := numGI$[d2hatFnGI$[v] /. pars, qq];
     fv[v_?NumericQ] := (lam v^2 - m2 /. pars) + d1[v]/(16 Pi^2) + d2[v]/(16 Pi^2)^2;
     vG = v /. FindRoot[fv[v], {v, N[p0]}, AccuracyGoal -> 14, PrecisionGoal -> 14];
     phi1 = -d1[p0]/(2 lam p0) /. pars;
     phi2 = numGI$[-(lam phi1^2 + (D[d1hatGI$[v], v] /. v -> p0) phi1 + d2hatFnGI$[p0])/(2 lam p0) /. pars, qq];
     vhb = p0 + phi1/(16 Pi^2) + phi2/(16 Pi^2)^2;
     vhG = numGI$[vhMinGI$[vG] /. pars, qq];
     vm1 = numGI$[Lam - lam p0^4/4 + kk (fGI$[2 lam p0^2] + 3 fVGI$[el^2 p0^2]) /. pars, qq];
     vmh = numGI$[Lam - lam p0^4/4 + kk (fGI$[2 lam p0^2] + 3 fVGI$[el^2 p0^2]) +
         kk^2 (v2G0GI$[p0] - (p0 d1hatGI$[p0])^2/(4 lam p0^2)) /. pars, qq];
     Print["(f) Q^2 = ", qq, ", s = ", s, ": G at the minimum ~ -Dh1/K = ", -d1[p0]/(16 Pi^2), ",  v (G-free) = ",
      vG, ",  v (hbar) = ", vhb, ",  Vh_min = ", vhG,
      ",  V_min (hbar) = ", vmh];
     {Sqrt[qq], s, N[p0], N[d1[p0]], N[d2[p0]], vG, vhb, vm1, vhG, vmh}],
    {qq, {1, 4}}, {s, {1, 1/2, 1/4, 1/8}}], 1];
Export[FileNameJoin[{resDirGI$, "goldstone_min.csv"}],
  Prepend[Map[ToString[CForm[#]] &, rowsGI$, {2}],
   {"Q", "s", "phi0", "Dh1", "Dh2", "v_Gfree", "v_hbar", "Vmin_1loop", "Vhat_min", "Vmin_hbar"}], "CSV"];
Put[{"Dh1" -> d1hatGI$[phi], "Dh2" -> d2hatGI$, "Vhat_min" -> vhMinGI$[phi]}, FileNameJoin[{resDirGI$, "goldstone.m"}]];
Print["(f) written results/goldstone_min.csv and results/goldstone.m"];


(* ::Section:: *)
(*(g) The minimization condition near G = 0 (for figs/goldstone.pdf)*)


(* K (1/phi) d(V - V0)/dphi at Q = 1 for the benchmark, from the analytic derivatives (Eq. (A.23)) and TSIL values of I:
   one loop: Y1;  two loops: Y1 + Y2/K;  resummed: Y1 + Y2/K + (1/phi) d/dphi [f(G + Delta1/K) - f(G) - Delta1 A(G)/(2K)].
   Finite differences are not used: TSIL's I(G,G,h) in double precision is off by ~1e-6 at G/h ~ 1e-9. *)
Module[{pars, xg, d1, y1, y2, yr, grid, rows, kv = 1/(16 Pi^2)},
  pars = {lam -> 25/32, el -> 1/2, m2 -> 25/8};
  xg = -m2 + lam phi^2;
  d1 = 3 lam A[-m2 + 3 lam phi^2] + el^2 (3 A[el^2 phi^2] + 2 el^2 phi^2);
  y1 = D[v1GI$, phi]/phi;
  y2 = D[v2GI$ /. massesGI$, phi]/phi;
  yr = D[fGI$[xg + kv d1] - fGI$[xg] - kv d1 A[xg]/2, phi]/phi;
  grid = Table[10.^(-10 + k/4), {k, 0, 40}];
  rows = Table[Module[{p = {phi -> Sqrt[(25/8 + g)/(25/32)]}, a, b, c},
      {a, b, c} = numGI$[{y1, y2, yr} /. pars /. p /. canonGI$, 1];
      {g, a, a + kv b, a + kv b + c}], {g, grid}];
  Export[FileNameJoin[{resDirGI$, "goldstone_curve.csv"}],
   Prepend[Map[ToString[CForm[#]] &, rows, {2}], {"G", "one_loop", "two_loops", "resummed"}], "CSV"];
  Print["(g) K (1/phi) d(V - V0)/dphi at G = 1e-10, 1e-6, 1e-2, 1: one loop ", rows[[{1, 17, 33, 41}, 2]],
   ", two loops ", rows[[{1, 17, 33, 41}, 3]], ", resummed ", rows[[{1, 17, 33, 41}, 4]]];
  Print["(g) two loops: slope in ln G between G = 1e-10 and 1e-6: ", (rows[[1, 3]] - rows[[17, 3]])/Log[rows[[1, 1]]/rows[[17, 1]]],
   ";  lam Dh1/K at phi0 = 2: ", N[kv lam d1hatGI$[2] /. pars /. A[x_] :> x (Log[x] - 1)],
   ";  resummed: change between G = 1e-10 and 1e-6: ", rows[[1, 4]] - rows[[17, 4]]];
  Print["(g) written results/goldstone_curve.csv"]];
