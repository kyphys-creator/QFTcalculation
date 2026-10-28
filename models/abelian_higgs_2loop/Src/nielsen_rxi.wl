(* ::Package:: *)

(* ::Title:: *)
(*Step (4): the background-field R_xi gauge -- Landau limit, RG invariance and the Nielsen identity at two loops*)


(* ::Text:: *)
(*Research note models/abelian_higgs_2loop, step (4).  V2 in the background-field R_xi gauge (Martin-Patel's Eq. (4.127),*)
(*checked against the diagrams in v2_rxi_feyncalc.wl, results/v2_rxi.m):*)
(*  (a) xi -> 0 gives the Landau-gauge V2 of step (1);*)
(*  (b) RG invariance through 1/K^2: [Q d/dQ + beta.d + beta_xi d/dxi + beta_xi~ d/dxi~ + beta_phi d/dphi] V = O(1/K^3),*)
(*      with the one-loop potential off the slice xi~ = xi to first order (Z+ = G + (2 xi~ - xi) Z, Z- = xi Z,*)
(*      eta = xi~ Z), the RG functions of step (2) and Martin-Patel's beta_phi, beta_xi, beta_xi~;*)
(*  (c) the Nielsen identity for the minimum value in the hbar expansion at fixed m2,*)
(*          V_min = V0 + V1/K + N/K^2,  N = V2 - V1'^2/(2 V0'')  at the tree minimum phi0 (G = 0):*)
(*      dN/dxi = 0 identically (derivatives of I from Martin's Eq. (A.23)), and N(xi -> 0) is the Landau value;*)
(*  (d) numbers at the benchmark (Q = 1): N, V_min and the one-loop shift of the VEV for several xi; the minimum of*)
(*      V0 + V1/K + V2/K^2 found numerically for xi = 1/2, 1, 3 with the couplings scaled by s, against the hbar*)
(*      expansion.  I(x,y,z) from TSIL (work/v2_tsil) -> results/nielsen_rxi.csv.*)
(*Batch: wolframscript -file nielsen_rxi.wl*)


(* ::Section:: *)
(*Setup*)


srcDirNR$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirNR$ = FileNameJoin[{srcDirNR$, "results"}];
tsilNR$ = FileNameJoin[{srcDirNR$, "work", "v2_tsil"}];
{v2RNR$, massRNR$} = {"V2", "masses"} /. Get[FileNameJoin[{resDirNR$, "v2_rxi.m"}]];
{v2LNR$, massLNR$} = {"V2", "masses"} /. Get[FileNameJoin[{resDirNR$, "v2_landau.m"}]];
rgNR$ = Get[FileNameJoin[{resDirNR$, "rg2.m"}]];

A[0] = 0;
Derivative[1][A] = (A[#]/# + 1) &;
canonNR$ = II[x__] :> II @@ Sort[{x}];
(* Martin, arXiv:1406.2355, Eq. (A.23) *)
dINR$[x_, y_, z_] := ((x - y - z) II[x, y, z] - 2 A[y] A[z] + (x - y + z) A[x] A[y]/x + (x + y - z) A[x] A[z]/x +
     (y + z - x) (A[x] + A[y] + A[z]) + x^2 - (y + z)^2)/(x^2 + y^2 + z^2 - 2 x y - 2 x z - 2 y z);
Derivative[1, 0, 0][II] = dINR$;
Derivative[0, 1, 0][II] = dINR$[#2, #1, #3] &;
Derivative[0, 0, 1][II] = dINR$[#3, #1, #2] &;
zeroQNR$[e_] := Module[{t = Together[e]}, Expand[Numerator[t]] === 0];
fNR$[x_] := (x A[x] - x^2/2)/4;                                     (* x^2 (ln x - 3/2)/4 *)
fVNR$[x_] := (x A[x] + x^2/6)/4;                                    (* x^2 (ln x - 5/6)/4 *)
qDNR$[f_] := 2 D[f /. {A[x_] :> A[x] - t x, II[x_, y_, z_] :> II[x, y, z] + t (A[x] + A[y] + A[z] - x - y - z)}, t] /.
   t -> 0;
v0NR$ = Lam - m2 phi^2/2 + lam phi^4/4;
(* one loop, to first order off xi~ = xi (symbol xit) *)
v1NR$ = Module[{H = -m2 + 3 lam phi^2, G = -m2 + lam phi^2, Z = el^2 phi^2},
   fNR$[H] + 3 fVNR$[Z] + fNR$[G + (2 xit - xi) Z] + fNR$[xi Z] - 2 fNR$[xit Z]];
v2NR$ = v2RNR$ /. massRNR$;                                         (* on the slice, in m2, lam, el, phi, xi *)


(* ::Section:: *)
(*(a) Landau limit*)


Module[{lim, land, d, f},
  lim = v2RNR$ /. {xe -> 0, xp -> xg} /. canonNR$;
  land = v2LNR$ /. {lam -> (xh - xg)/(2 phi^2), el -> Sqrt[xa]/phi} /. canonNR$;
  d = Expand[lim - land];
  f = Union[Cases[d, _A | _II, Infinity]];
  Print["(a) Eq. (4.127) at xi = 0 minus the Landau-gauge V2: nonzero coefficients (expect {}): ",
   Select[CoefficientRules[d, f], Simplify[#[[2]], xh > 0 && xg > 0 && xa > 0 && phi > 0] =!= 0 &]]];


(* ::Section:: *)
(*(b) RG invariance*)


Module[{b1, b2, dOp, ord1, ord2, toSym},
  (* Martin-Patel, Eqs. (4.123)-(4.126); the others from step (2) *)
  b1 = {rgNR$["lam"][[1]], rgNR$["el"][[1]], rgNR$["m2"][[1]], rgNR$["Lam"][[1]], -2 el^2 xi/3,
    2 el^2 (xi - xit - 10/3) xit, (3 - xi + 2 xit) el^2 phi};
  b2 = {rgNR$["lam"][[2]], rgNR$["el"][[2]], rgNR$["m2"][[2]], rgNR$["Lam"][[2]], 0, 0,
    (el^4 (-10/3 + 2 xit + 2 xi xit) - 4 lam^2) phi};
  dOp[b_, f_] := b.(D[f, #] & /@ {lam, el, m2, Lam, xi, xit, phi});
  toSym[e_] := Together[e /. xit -> xi /. canonNR$];
  ord1 = toSym[qDNR$[v1NR$] + dOp[b1, v0NR$]];
  ord2 = toSym[qDNR$[v2NR$] + dOp[b1, v1NR$] + dOp[b2, v0NR$]];
  Print["(b) Q dV/dQ at orders 1/K, 1/K^2 (expect 0, 0): ", {ord1, ord2}];
  Print["(b) the same with the Landau-gauge gamma (beta_phi = 3 e^2 phi + ...) instead (expect nonzero): ",
   Factor[toSym[qDNR$[v1NR$] + dOp[ReplacePart[b1, 7 -> 3 el^2 phi], v0NR$]]]]];


(* ::Section:: *)
(*(c) Nielsen identity for the minimum value*)


(* at the tree minimum m2 = lam phi^2 (G = 0); V0'' = 2 lam phi^2 *)
v1pNR$ = (D[v1NR$, phi] /. xit -> xi) /. m2 -> lam phi^2;
nNR$ = (v2NR$ /. m2 -> lam phi^2) - v1pNR$^2/(2 2 lam phi^2) /. canonNR$;
(* xi -> 0: A(xi Z) = xi Z (ln(xi Z) - 1), with ln(xi Z) kept as the symbol lx (xi lx -> 0) *)
n0NR$ = Expand[nNR$ /. A[xi el^2 phi^2] -> xi el^2 phi^2 (lx - 1)] /. xi -> 0 /. canonNR$;
Module[{d1, nL},
  d1 = 3 lam A[2 lam phi^2] + el^2 (3 A[el^2 phi^2] + 2 el^2 phi^2);
  Print["(c) V1'(phi0) - phi0 [Dh1 + lam A(xi Z)] (expect 0): ",
   zeroQNR$[v1pNR$ - phi (d1 + lam A[xi el^2 phi^2])] /. True -> 0];
  Print["(c) dN/dxi (expect 0): ", zeroQNR$[D[nNR$, xi] /. canonNR$] /. True -> 0];
  nL = (v2LNR$ /. massLNR$ /. m2 -> lam phi^2 /. canonNR$) - (phi d1)^2/(2 2 lam phi^2);
  Print["(c) N(xi -> 0): terms with ln(xi Z) left (expect 0): ", Coefficient[n0NR$, lx],
   ";  N(xi -> 0) - N(Landau) (expect 0): ", zeroQNR$[n0NR$ - nL] /. True -> 0]];


(* ::Section:: *)
(*(d) Numbers*)


numNR$[e_, qq_] := Module[{ii, vals, out},
   ii = Union[Cases[e, II[__?NumericQ], Infinity]];
   If[ii === {}, Return[N[e //. A[x_?NumericQ] :> x (Log[x/qq] - 1)]]];
   out = RunProcess[{tsilNR$}, "StandardOutput",
     StringJoin[(StringRiffle[ToString[CForm[N[#]]] & /@ Append[List @@ #, qq], ","] <> "\n") & /@ ii]];
   vals = ImportString[out, "CSV"][[2 ;;, 5]];
   N[e /. Thread[ii -> vals] //. A[x_?NumericQ] :> x (Log[x/qq] - 1)]];
kNR$ = 16. Pi^2;
bench$ = {lam -> 25/32, el -> 1/2, m2 -> 25/8, Lam -> 0};
(* (d1) the hbar expansion at the benchmark for several xi *)
rows1NR$ = Table[Module[{p = Join[bench$, {xi -> x, phi -> 2}], v1, v2, n, vmin, dv},
     v1 = numNR$[v1NR$ /. xit -> xi /. p, 1];
     v2 = numNR$[v2NR$ /. p /. canonNR$, 1];
     (* at xi = 0 the limits: N from n0NR$, V1'(phi0) = phi0 Dh1 *)
     n = numNR$[If[x == 0, n0NR$, nNR$] /. p, 1];
     vmin = -25/32 2^4/4 + v1/kNR$ + n/kNR$^2;
     dv = -numNR$[If[x == 0, phi (3 lam A[2 lam phi^2] + el^2 (3 A[el^2 phi^2] + 2 el^2 phi^2)), v1pNR$] /. p, 1]/
       (2 25/32 2^2);                                               (* v1 = -V1'/V0'' *)
     Print["(d) xi = ", x, ": V2(phi0) = ", v2, ",  N = ", n, ",  V_min = ", vmin, ",  VEV shift v1/K = ", dv/kNR$];
     {x, v2, n, vmin, 2 + dv/kNR$}], {x, {0, 1/2, 1, 3, 10}}];
Print["(d) spread of N over xi = 0 ... 10: ", Max[rows1NR$[[All, 3]]] - Min[rows1NR$[[All, 3]]],
  ";  of V2(phi0): ", Max[rows1NR$[[All, 2]]] - Min[rows1NR$[[All, 2]]]];
(* (d2) the minimum of V0 + V1/K + V2/K^2 found numerically, couplings scaled by s *)
dVNR$ = D[v0NR$ + v1NR$/kk + v2NR$/kk^2 /. xit -> xi, phi] /. canonNR$;
vNR$ = v0NR$ + (v1NR$ /. xit -> xi)/kk + v2NR$/kk^2 /. canonNR$;
rows2NR$ = Flatten[Table[Module[{p, p0, fd, vm, vval, vh},
      p = {lam -> s 25/32, el -> Sqrt[s]/2, m2 -> 25/8, Lam -> 0, xi -> x, kk -> kNR$};
      p0 = Sqrt[25/8/(s 25/32)];
      fd[ph_?NumericQ] := numNR$[dVNR$ /. p /. phi -> ph, 1];
      vm = ph /. FindRoot[fd[ph], {ph, N[p0]}, AccuracyGoal -> 13, PrecisionGoal -> 13];
      vval = numNR$[vNR$ /. p /. phi -> vm, 1];
      (* the hbar expansion (xi-independent): Lam - lam phi0^4/4 + V1/K + N/K^2 at phi0 *)
      vh = numNR$[(-lam phi^4/4 + (v1NR$ /. xit -> xi)/kk + nNR$/kk^2) /. p /. phi -> p0 /. canonNR$, 1];
      {s, x, vm, vval, vh}], {x, {1/2, 1, 3}}, {s, {1, 1/2, 1/4, 1/8}}], 1];
Do[Print["(d) xi = ", r[[2]], ", s = ", r[[1]], ": v (numerical) = ", r[[3]], ",  V_min (numerical) = ", r[[4]],
   ",  V_min (hbar) = ", r[[5]], ",  difference ", r[[4]] - r[[5]]], {r, rows2NR$}];
Do[Module[{rs = Select[rows2NR$, #[[2]] == x &]},
   Print["(d) xi = ", x, ": ratios of the V_min differences for s -> s/2 (expect 4): ",
    Ratios[(#[[4]] - #[[5]]) & /@ rs]^-1]], {x, {1/2, 1, 3}}];
Export[FileNameJoin[{resDirNR$, "nielsen_rxi.csv"}],
  Join[{{"xi", "V2_phi0", "N", "Vmin_hbar", "v_1loop"}}, Map[ToString[CForm[N[#]]] &, rows1NR$, {2}],
   {{"s", "xi", "v_num", "Vmin_num", "Vmin_hbar"}}, Map[ToString[CForm[N[#]]] &, rows2NR$, {2}]], "CSV"];
Print["(d) written results/nielsen_rxi.csv"];
