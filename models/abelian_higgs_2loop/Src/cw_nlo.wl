(* ::Package:: *)

(* ::Title:: *)
(*Step (5): the Coleman-Weinberg model at the next order (abelian Higgs model, m2 = 0, lam ~ e^4/K)*)


(* ::Text:: *)
(*Research note models/abelian_higgs_2loop, step (5).  m2 = 0, Q = 1, Z = e^2 phi^2, L = ln Z.  Counting lam ~ e^4/K,*)
(*the leading order is V_LO = (phi^4/4)[lam + (3 e^4/K)(L - 5/6)] and the next order (relative e^2/K) collects*)
(*  - the one-loop term linear in lam in the background-field R_xi gauge, f(G + xi Z) - f(xi Z) -> (lam phi^2/2) A(xi Z);*)
(*  - the two-loop V2 at lam -> 0 (Landau: results/v2_landau.m; background R_xi: results/v2_rxi.m).*)
(*  (a) V2 at lam -> 0 in Landau gauge against e^6 phi^4 [5/2 L^2 - 31/3 L + 71/6] (Andreassen-Frost-Schwartz's Eq. (5.20)*)
(*      at xi = 0; Espinosa-Garny-Konstandin's Eq. (14));*)
(*  (b) the two-loop Nielsen identity at lam -> 0: V2(xi) - V2(0) = (3/2) xi e^6 phi^4 (L - 1/3)(L + ln xi - 1), from*)
(*      d_xi V2 = C1 d_phi V1 with C1 = (e^2 phi/2) ln(xi Z) (one-loop note);*)
(*  (c) the minimum value at the next order and its RG invariance with the two-loop beta functions (step (2));*)
(*  (d) the curvature ratio V''(v)/(e^2 v^2) at the next order: its xi dependence, against*)
(*      d ln R/d xi = 2 C1' + 2 C1/v;*)
(*  (e) numbers: the full two-loop potential minimized numerically for e = 1/2 ... 1/16 at lam = e^4/K, against (c), (d).*)
(*      I(x,y,z) from TSIL (work/v2_tsil) -> results/cw_nlo.csv, results/cw_nlo.m.*)
(*Batch: wolframscript -file cw_nlo.wl*)


(* ::Section:: *)
(*Setup*)


srcDirCW$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirCW$ = FileNameJoin[{srcDirCW$, "results"}];
tsilCW$ = FileNameJoin[{srcDirCW$, "work", "v2_tsil"}];
{v2LCW$, massLCW$} = {"V2", "masses"} /. Get[FileNameJoin[{resDirCW$, "v2_landau.m"}]];
{v2RCW$, massRCW$} = {"V2", "masses"} /. Get[FileNameJoin[{resDirCW$, "v2_rxi.m"}]];
rgCW$ = Get[FileNameJoin[{resDirCW$, "rg2.m"}]];

A[0] = 0;
Derivative[1][A] = (A[#]/# + 1) &;
canonCW$ = II[x__] :> II @@ Sort[{x}];
dICW$[x_, y_, z_] := ((x - y - z) II[x, y, z] - 2 A[y] A[z] + (x - y + z) A[x] A[y]/x + (x + y - z) A[x] A[z]/x +
     (y + z - x) (A[x] + A[y] + A[z]) + x^2 - (y + z)^2)/(x^2 + y^2 + z^2 - 2 x y - 2 x z - 2 y z);
Derivative[1, 0, 0][II] = dICW$;
Derivative[0, 1, 0][II] = dICW$[#2, #1, #3] &;
Derivative[0, 0, 1][II] = dICW$[#3, #1, #2] &;
(* closed forms at Q = 1: I(0,0,x) and I(0,x,x) (Martin, hep-ph/0111209; 1406.2355 Eq. (A.22)) *)
closedCW$ = {II[0, 0, x_] :> -x Log[x]^2/2 + 2 x Log[x] - (5/2 + Pi^2/6) x,
   II[0, x_, x_] :> 2 A[x] - 2 x - A[x]^2/x, II[0, 0, 0] -> 0};
explicitACW$ = A[x_] :> x (Log[x] - 1);
zeroQCW$[e_] := Module[{t = Together[e]}, Expand[Numerator[t]] === 0];
kCW$ = 16 Pi^2;


(* ::Section:: *)
(*(a) V2 at lam -> 0 in Landau gauge*)


(* H = 3 lam phi^2, G = lam phi^2 -> 0: the lam terms of V2 are O(lam ln lam) and go to the next-to-next order *)
v2L0CW$ = Module[{e},
   e = v2LCW$ /. {xh -> 0, xg -> 0, xa -> el^2 phi^2} /. lam -> 0 /. canonCW$ /. closedCW$ /. explicitACW$;
   Expand[PowerExpand[e /. Log[el^2 phi^2] -> L]]];
Print["(a) Landau V2 at lam -> 0, in units of e^6 phi^4: ", Collect[Simplify[v2L0CW$/(el^6 phi^4)], L],
  ";  minus [5/2 L^2 - 31/3 L + 71/6] (expect 0): ", Simplify[v2L0CW$/(el^6 phi^4) - (5/2 L^2 - 31/3 L + 71/6)]];


(* ::Section:: *)
(*(b) The background-field R_xi gauge at lam -> 0*)


(* G = lam phi^2 -> 0: Z+ = eta = xi Z; I(0, Z, xi Z) is kept (symbol), its xi derivative from Eq. (A.23) *)
Module[{z = el^2 phi^2, v2x, d, rhs},
  v2x = v2RCW$ /. {xh -> 0, xp -> xi el^2 phi^2, xa -> el^2 phi^2, xe -> xi el^2 phi^2} /. canonCW$;
  v2x = v2x /. II[0, a_, b_] /; a === b :> (II[0, a, a] /. closedCW$) /. II[0, 0, 0] -> 0;
  rhs = 3/2 xi el^6 phi^4 (Log[z] - 1/3) (Log[z] + Log[xi] - 1);
  d = v2x - (v2LCW$ /. {xh -> 0, xg -> 0, xa -> z} /. lam -> 0 /. canonCW$ /. closedCW$) - rhs;
  Print["(b) I functions left in V2(xi) at lam -> 0: ", Union[Cases[v2x, _II, Infinity]]];
  Print["(b) d/dxi [V2(xi) - V2(0) - (3/2) xi e^6 phi^4 (L - 1/3)(L + ln xi - 1)] (expect 0): ",
   zeroQCW$[PowerExpand[D[d, xi] /. canonCW$ /. closedCW$ /. explicitACW$]] /. True -> 0];
  (* xi -> 0: I(0, Z, xi Z) -> I(0, 0, Z), A(xi Z) = xi Z (ln(xi Z) - 1) -> 0 *)
  Print["(b) the same difference at xi -> 0 (expect 0): ",
   Simplify[Limit[PowerExpand[d /. II[0, a_, b_] /; !FreeQ[{a, b}, xi] :> II[0, 0, el^2 phi^2] /. closedCW$ /.
        explicitACW$], xi -> 0], el > 0 && phi > 0]]];


(* ::Section:: *)
(*(c) The minimum value at the next order*)


(* L0 = 1/3 - K lam/(3 e^4) minimizes V_LO; at L0 the next-order terms add (stationarity):
   V_min = -(3 e^4/(8K)) v0^4 + (e^6 v0^4/K^2) P(L0),  P(L) = 5/2 L^2 - 31/3 L + 71/6,  v0^4 = exp(2 L0)/e^4 (Q = 1) *)
pCW$[L_] := 5/2 L^2 - 31/3 L + 71/6;
vminCW$ = Module[{l0 = 1/3 - kk lam/(3 el^4)},
   Exp[2 l0]/el^4 (-3 el^4/(8 kk) + el^6/kk^2 pCW$[l0])] /. kk -> kCW$;
Module[{bl, be, mu, vq, dv, s},
  (* restore Q: v0^4 = Q^4 exp(2 L0)/e^4 with L0 = ln(e^2 v0^2/Q^2); then [Q d/dQ + beta.d] V_min *)
  vq = Q^4 vminCW$;
  bl = (6 el^4 - 12 el^2 lam)/kCW$ - 208/3 el^6/kCW$^2;          (* through the next order at lam ~ e^4/K *)
  be = el^3/(3 kCW$);
  dv = Q D[vq, Q] + bl D[vq, lam] + be D[vq, el] /. Q -> 1;
  (* lam = s e^4/K: dv/V_min must be O(e^4/K^2) *)
  s = Series[Simplify[dv/vminCW$ /. lam -> sl el^4/kCW$], {el, 0, 2}];
  Print["(c) [Q d/dQ + beta.d] ln V_min at lam = s e^4/K, orders e^0 and e^2 (expect 0, 0): ",
   Simplify[{SeriesCoefficient[s, 0], SeriesCoefficient[s, 2]}]]];
Print["(c) V_min/V_LO - 1 at L0 = 0 (lam = e^4/K): ", Simplify[-8/3 pCW$[0]] el^2/K];


(* ::Section:: *)
(*(d) The curvature ratio*)


(* With V = phi^4 W(L), L = ln(e^2 phi^2): V' = (2/phi) dV/dL, the minimum is 2W + W' = 0, and there
   R = V''/(e^2 v^2) = (4/e^2)(W'' + 2W').  At the next order W' and W'' are needed only at L0:
   R = (6 e^2/K)[1 + (e^2/K) r1],  r1 = (2/3)[xi (1 - 3 L0) + 2 Pxi'(L0) + Pxi''(L0)]  (background R_xi gauge),
   Pxi(L) = P(L) + (3/2) xi (L - 1/3)(L + ln xi - 1) by (b). *)
pxiCW$[L_] := pCW$[L] + 3/2 xi (L - 1/3) (L + Log[xi] - 1);
r1CW$ = Simplify[2/3 (xi (1 - 3 L0) + 2 D[pxiCW$[L], L] + D[pxiCW$[L], {L, 2}]) /. L -> L0];
Print["(d) r1 = ", r1CW$, ";  at xi = 0 (Landau): ", Limit[r1CW$, xi -> 0]];
Print["(d) dr1/dxi - 2 (L0 + ln xi + 1) (expect 0; Nielsen: d ln R/dxi = 2 C1' + 2 C1/v, C1 = (e^2 phi/2K) ln(xi Z)): ",
  Simplify[D[r1CW$, xi] - 2 (L0 + Log[xi] + 1)]];
Print["(d) one loop only (the one-loop note): r1 = (2/3) xi (1 - 3 L0); with V2 the xi dependence becomes 2 xi (L0 + ln xi)"];


(* ::Section:: *)
(*(e) Numbers*)


(* the full potential at m2 = 0, Q = 1, lam = e^4/K (L0 = 0, so e v0 = 1): one or two loops, Landau (xi = 0) or
   background R_xi; V' and V'' analytic (Eq. (A.23)), I from TSIL *)
kNCW$ = N[kCW$];
numCW$[e_] := Module[{ii, vals, out, aRule},
   aRule = A[x_?NumericQ] :> Which[x == 0, 0, x < 0, x (Log[-x] - I Pi - 1), True, x (Log[x] - 1)];
   ii = Union[Cases[e, II[__?NumericQ], Infinity]];
   If[ii === {}, Return[N[e //. aRule]]];
   out = ImportString[RunProcess[{tsilCW$}, "StandardOutput",
      StringJoin[(StringRiffle[ToString[CForm[N[#]]] & /@ Append[List @@ #, 1], ","] <> "\n") & /@ ii]], "CSV"];
   vals = (#[[5]] + I #[[9]]) & /@ out[[2 ;;]];
   N[e /. Thread[ii -> vals] //. aRule]];
fCW$[x_] := (x A[x] - x^2/2)/4;
fVCW$[x_] := (x A[x] + x^2/6)/4;
potCW$[x_, loops_] := Module[{h = 3 lam phi^2, g = lam phi^2, z = el^2 phi^2, v1, v2},
   If[x === 0,
    v1 = fCW$[h] + fCW$[g] + 3 fVCW$[z];
    v2 = v2LCW$ /. {xh -> h, xg -> g, xa -> z},
    v1 = fCW$[h] + 3 fVCW$[z] + fCW$[g + x z] - fCW$[x z];
    v2 = v2RCW$ /. {xh -> h, xp -> g + x z, xa -> z, xe -> x z}];
   lam phi^4/4 + v1/kNCW$ + If[loops == 2, v2/kNCW$^2, 0] /. canonCW$];
(* derivatives once per gauge and loop order; numbers substituted once per e *)
derivCW$ = Association[Table[{x, n} -> Module[{v = potCW$[x, n]}, {v, D[v, phi] /. canonCW$, D[v, {phi, 2}] /. canonCW$}],
    {x, {0, 1., 3.}}, {n, {1, 2}}]];
rowsCW$ = Flatten[Table[Module[{v, dv, ddv, pars, fd, vm, vval, rr, vnlo, rnlo, vlo},
      pars = {el -> e, lam -> e^4/kNCW$};
      {v, dv, ddv} = derivCW$[{x, n}] /. pars;
      fd[ph_?NumericQ] := Re[numCW$[dv /. phi -> ph]];
      vm = ph /. FindRoot[fd[ph], {ph, 1/e}, AccuracyGoal -> 15, PrecisionGoal -> 13];
      vval = Re[numCW$[v /. phi -> vm]];
      rr = Re[numCW$[ddv /. phi -> vm]]/(e^2 vm^2);
      (* the leading and next orders at L0 = 0 *)
      vlo = -3 e^4/(8 kNCW$)/e^4;
      vnlo = N[vminCW$ /. {lam -> e^4/kCW$, el -> e}];
      rnlo = 6 e^2/kNCW$ (1 + e^2/kNCW$ If[x === 0, Limit[r1CW$, xi -> 0], r1CW$ /. xi -> x] /. L0 -> 0);
      {x, n, e, vm, vval, vval/vnlo - 1, vval/vlo - 1, rr, rr/rnlo - 1}],
     {x, {0, 1., 3.}}, {n, {1, 2}}, {e, 2.^-Range[1, 4]}], 2];
Do[Print["(e) xi = ", r[[1]], ", ", r[[2]], " loop(s), e = ", r[[3]], ": v = ", r[[4]], ",  V_min/V_NLO - 1 = ",
   r[[6]], ",  V_min/V_LO - 1 = ", r[[7]], ",  R = ", r[[8]], ",  R/R_NLO - 1 = ", r[[9]]], {r, rowsCW$}];
Do[Module[{rs = Select[rowsCW$, #[[1]] == x && #[[2]] == 2 &]},
   Print["(e) xi = ", x, ", two loops: ratios for e -> e/2 of (V_min/V_NLO - 1): ", Ratios[rs[[All, 6]]]^-1,
    ";  of (R/R_NLO - 1): ", Ratios[rs[[All, 9]]]^-1, "  (next-to-next order: 16 up to logs)"]], {x, {0, 1., 3.}}];
Do[Module[{rs1 = Select[rowsCW$, #[[1]] == x && #[[2]] == n && #[[3]] == 2.^-4 &][[1]],
     rs0 = Select[rowsCW$, #[[1]] == 0 && #[[2]] == n && #[[3]] == 2.^-4 &][[1]]},
   Print["(e) e = 1/16, ", n, " loop(s): V_min(xi = ", x, ")/V_min(Landau) - 1 = ", rs1[[5]]/rs0[[5]] - 1,
    ",  R(xi)/R(Landau) - 1 = ", rs1[[8]]/rs0[[8]] - 1]], {n, {1, 2}}, {x, {1., 3.}}];
Export[FileNameJoin[{resDirCW$, "cw_nlo.csv"}],
  Prepend[Map[ToString[CForm[#]] &, rowsCW$, {2}],
   {"xi", "loops", "e", "v", "Vmin", "Vmin_over_VNLO_minus_1", "Vmin_over_VLO_minus_1", "R", "R_over_RNLO_minus_1"}],
  "CSV"];
Put[{"P" -> pCW$[L], "Vmin" -> vminCW$, "r1" -> r1CW$}, FileNameJoin[{resDirCW$, "cw_nlo.m"}]];
Print["(e) written results/cw_nlo.csv and results/cw_nlo.m"];
