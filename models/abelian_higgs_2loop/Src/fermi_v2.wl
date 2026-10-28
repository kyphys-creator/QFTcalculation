(* ::Package:: *)

(* ::Title:: *)
(*Step (4), Fermi gauge: the general two-loop potential of Martin-Patel, RG invariance, and the minimum value*)


(* ::Text:: *)
(*Research note models/abelian_higgs_2loop, step (4).  Gauge fixing F = d.A - xi~ e phi G with weight 1/(2 xi)*)
(*(Martin-Patel, arXiv:1808.07615); Fermi gauge xi~ = 0, background-field R_xi gauge xi~ = xi.  Their ancillary file*)
(*V2AH (the two-loop potential for general xi, xi~; work/V2AH, fetched by run_fermi_check.sh) is used here:*)
(*  (a) its slice xi~ = xi against our diagrams (results/v2_rxi.m), its Landau form against step (1), and its*)
(*      Fermi form V2AHFermi against V2AH at xi~ = 0 (modulo Z+^2 - G Z+ + xi Z G = 0);*)
(*  (b) RG invariance of the Fermi-gauge potential through 1/K^2: Z+- = [G +- sqrt(G (G - 4 xi Z))]/2 are treated as*)
(*      the roots of x^2 - G x + xi Z G, beta_xi = -2 e^2 xi/(3K), beta_phi = (3 - xi) e^2 phi/K*)
(*      - (10 e^4/3 + 4 lam^2) phi/K^2;*)
(*  (c) the minimum of the fixed-order potential (real part; Z- < 0 near the minimum in Fermi gauge) found numerically*)
(*      in the Fermi and background-field R_xi gauges at one and two loops for xi = 0.05 ... 50 (benchmark, Q = 1), and*)
(*      its distance from the gauge-independent hbar expansion of step (3), also with the couplings scaled by s.*)
(*      I(x,y,z) from TSIL (work/v2_tsil, negative squared masses as x - i0) -> results/fermi_min.csv;*)
(*  (d) Fermi gauge as G -> 0 from below: the one-loop IR logarithm of Espinosa-Garny-Konstandin and V2*)
(*      -> results/fermi_ir.csv.*)
(*Batch: wolframscript -file fermi_v2.wl*)


(* ::Section:: *)
(*Setup*)


srcDirFG$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirFG$ = FileNameJoin[{srcDirFG$, "results"}];
tsilFG$ = FileNameJoin[{srcDirFG$, "work", "v2_tsil"}];
(* Martin-Patel's file: plain assignments V2AH, V2AHFermi, V2AHbackgroundRxi, V2AHLandau in Z, G, H, Zp, Zm, Zg, xi,
   xitilde, phi, A[x], I2[x,y,z] (their m2 has the opposite sign; only the squared masses enter here) *)
Get[FileNameJoin[{srcDirFG$, "work", "V2AH"}]];
{v2RFG$, massRFG$} = {"V2", "masses"} /. Get[FileNameJoin[{resDirFG$, "v2_rxi.m"}]];
{v2LFG$, massLFG$} = {"V2", "masses"} /. Get[FileNameJoin[{resDirFG$, "v2_landau.m"}]];
rgFG$ = Get[FileNameJoin[{resDirFG$, "rg2.m"}]];

A[0] = 0;
Derivative[1][A] = (A[#]/# + 1) &;
canonFG$ = II[x__] :> II @@ Sort[{x}];
coefZeroFG$[d_, assum_] := Module[{f = Union[Cases[d, _A | _II, Infinity]]},
   Select[CoefficientRules[Expand[d], f], Simplify[#[[2]], assum] =!= 0 &]];
fFG$[x_] := (x A[x] - x^2/2)/4;
fVFG$[x_] := (x A[x] + x^2/6)/4;
qDFG$[f_] := 2 D[f /. {A[x_] :> A[x] - t x, II[x_, y_, z_] :> II[x, y, z] + t (A[x] + A[y] + A[z] - x - y - z)}, t] /.
   t -> 0;


(* ::Section:: *)
(*(a) The file against our results*)


Module[{gen, land, d},
  (* slice xi~ = xi (G > 0): Z+ = G + xi Z, Z- = Zg = xi Z; then our symbols xh, xp, xa, xe *)
  gen = V2AH /. I2 -> II /. {xitilde -> xi, Zg -> xi Z, Zp -> G + xi Z, Zm -> xi Z} /.
      {H -> xh, G -> xp - xe, Z -> xa} /. xi -> xe/xa /. canonFG$;
  Print["(a) V2AH at xi~ = xi minus the diagrams of v2_rxi_feyncalc.wl: nonzero coefficients (expect {}): ",
   coefZeroFG$[gen - (v2RFG$ /. canonFG$), xh > 0 && xa > 0 && xe > 0 && xp > xe && phi > 0]];
  land = V2AHLandau /. I2 -> II /. {H -> xh, G -> xg, Z -> xa} /. canonFG$;
  Print["(a) V2AHLandau minus step (1) (expect {}): ",
   coefZeroFG$[land - (v2LFG$ /. {lam -> (xh - xg)/(2 phi^2), el -> Sqrt[xa]/phi} /. canonFG$),
    xh > 0 && xg > 0 && xa > 0 && phi > 0]];
  (* Fermi form: V2AH at xi~ = 0, coefficients reduced modulo Zp^2 - G Zp + xi Z G (Zm = G - Zp) *)
  d = Expand[(V2AH /. {xitilde -> 0, Zg -> 0}) - V2AHFermi];
  Print["(a) V2AH at xi~ = 0 minus V2AHFermi, coefficients modulo the root relation (expect {}): ",
   Select[CoefficientRules[d, Union[Cases[d, _A | _I2, Infinity]]],
    Module[{t = Together[#[[2]]]},
      PolynomialRemainder[Expand[Numerator[t]], Zp^2 - G Zp + xi Z G, Zp] =!= 0] &]]];


(* ::Section:: *)
(*(b) RG invariance in Fermi gauge*)


Module[{hF, gF, zF, v0, v1, v2, dz, dTot, b1, b2, dOp, red, ord1, ord2},
  hF = -m2 + 3 lam phi^2; gF = -m2 + lam phi^2; zF = el^2 phi^2;
  v0 = Lam - m2 phi^2/2 + lam phi^4/4;
  v1 = fFG$[hF] + 3 fVFG$[zF] + fFG$[zp] + fFG$[zm];
  v2 = V2AHFermi /. I2 -> II /. {H -> hF, G -> gF, Z -> zF, Zp -> zp, Zm -> zm};
  (* zp, zm: roots of x^2 - gF x + xi zF gF *)
  dz[w_, p_] := (w D[gF, p] - D[xi zF gF, p])/(2 w - gF);
  dTot[e_, p_] := D[e, p] + D[e, zp] dz[zp, p] + D[e, zm] dz[zm, p];
  b1 = {rgFG$["lam"][[1]], rgFG$["el"][[1]], rgFG$["m2"][[1]], rgFG$["Lam"][[1]], -2 el^2 xi/3, (3 - xi) el^2 phi};
  b2 = {rgFG$["lam"][[2]], rgFG$["el"][[2]], rgFG$["m2"][[2]], rgFG$["Lam"][[2]], 0, (-10/3 el^4 - 4 lam^2) phi};
  dOp[b_, e_] := b.(dTot[e, #] & /@ {lam, el, m2, Lam, xi, phi});
  red[e_] := Module[{t = Together[e /. {A[zp] -> ap, A[zm] -> am}]},
    PolynomialRemainder[Expand[Numerator[t] /. zm -> gF - zp], zp^2 - gF zp + xi zF gF, zp]];
  ord1 = red[qDFG$[v1] + dOp[b1, v0]];
  ord2 = red[qDFG$[v2] + dOp[b1, v1] + dOp[b2, v0]];
  Print["(b) Fermi gauge, Q dV/dQ at orders 1/K, 1/K^2 (expect 0, 0): ", Simplify[{ord1, ord2}]];
  Print["(b) the same with beta_phi of the background-field R_xi gauge, (3 + xi) e^2 phi (expect nonzero): ",
   Factor[red[qDFG$[v1] + dOp[ReplacePart[b1, 6 -> (3 + xi) el^2 phi], v0]]]]];


(* ::Section:: *)
(*(c) The minimum of the fixed-order potential*)


kFG$ = 16. Pi^2;
(* TSIL values (complex for negative squared masses, x - i0) *)
numFG$[e_, qq_] := Module[{ii, vals, out, aRule},
   aRule = A[x_?NumericQ] :> Which[x == 0, 0, x < 0, x (Log[-x/qq] - I Pi - 1), True, x (Log[x/qq] - 1)];
   ii = Union[Cases[e, II[__?NumericQ], Infinity]];
   If[ii === {}, Return[N[e //. aRule]]];
   out = ImportString[RunProcess[{tsilFG$}, "StandardOutput",
      StringJoin[(StringRiffle[ToString[CForm[N[#]]] & /@ Append[List @@ #, qq], ","] <> "\n") & /@ ii]], "CSV"];
   vals = (#[[5]] + I #[[9]]) & /@ out[[2 ;;]];
   N[e /. Thread[ii -> vals] //. aRule]];
(* the potentials (Lam = 0) as functions of numbers: gauge "F" (Fermi), "R" (background R_xi); loops 1 or 2 *)
potFG$[gauge_, loops_, {l_, e_, m_, x_}, ph_] := Module[{hF, gF, zF, s, zp, zm, v1, v2},
   hF = -m + 3 l ph^2; gF = -m + l ph^2; zF = e^2 ph^2;
   Which[
    gauge === "F",
    s = Sqrt[gF (gF - 4 x zF)]; zp = (gF + s)/2; zm = (gF - s)/2;
    v1 = fFG$[hF] + 3 fVFG$[zF] + fFG$[zp] + fFG$[zm];
    v2 = V2AHFermi /. I2 -> II /. {H -> hF, G -> gF, Z -> zF, Zp -> zp, Zm -> zm, xi -> x, phi -> ph},
    gauge === "R",
    v1 = fFG$[hF] + 3 fVFG$[zF] + fFG$[gF + x zF] - fFG$[x zF];
    v2 = v2RFG$ /. {xh -> hF, xp -> gF + x zF, xa -> zF, xe -> x zF, phi -> ph}];
   Re[numFG$[-m ph^2/2 + l ph^4/4 + v1/kFG$ + If[loops == 2, v2/kFG$^2, 0], 1]]];
minFG$[gauge_, loops_, pars_] := Module[{l, e, m, x, p0, h0, z0, gEst, lo, hi, f, r},
   {l, e, m, x} = pars; p0 = Sqrt[m/l];
   (* start near the Landau-gauge estimate G = -Dh1/K (step (3)); in Fermi gauge stay at G < 0 (real Z+-) *)
   h0 = 2 l p0^2; z0 = e^2 p0^2;
   gEst = -(3 l h0 (Log[h0] - 1) + e^2 (3 z0 (Log[z0] - 1) + 2 z0))/kFG$;
   {lo, hi} = {Sqrt[(m + 8 gEst)/l], If[gauge === "F", p0 Sqrt[1 - 1.*^-9], Sqrt[(m - 4 gEst)/l]]};
   f[ph_?NumericQ] := If[ph <= lo || ph >= hi, 10.^6, potFG$[gauge, loops, pars, ph]];
   r = FindMinimum[f[ph], {ph, Sqrt[(m + 1.2 gEst)/l], Sqrt[(m + 0.9 gEst)/l]},
     AccuracyGoal -> 12, PrecisionGoal -> 10];
   {ph /. r[[2]], r[[1]]}];
(* the gauge-independent hbar expansion (step (3)): -lam phi0^4/4 + V1/K + [V2 - V1'^2/(2 V0'')]/K^2 at the tree
   minimum, from the Landau-gauge V2 at G = 0; {one loop, two loops} *)
hbarFG$[{l_, e_, m_, _}] := Module[{p0 = Sqrt[m/l], h0, z0, d1, v1, n},
   h0 = 2 l p0^2; z0 = e^2 p0^2;
   d1 = 3 l A[h0] + e^2 (3 A[z0] + 2 z0);
   v1 = fFG$[h0] + 3 fVFG$[z0];
   n = (v2LFG$ /. {xh -> h0, xg -> 0, xa -> z0, lam -> l, el -> e, phi -> p0}) - (p0 d1)^2/(4 l p0^2);
   Re[numFG$[{-l p0^4/4 + v1/kFG$, -l p0^4/4 + v1/kFG$ + n/kFG$^2}, 1]]];
xisFG$ = {0.05, 0.1, 0.2, 0.5, 1., 2., 5., 10., 20., 50.};
hb1FG$ = hbarFG$[{25/32., 0.5, 25/8., 0}];
Print["(c) hbar expansion at the benchmark: V_min = ", hb1FG$, " (one, two loops; step (3): -3.10839050792763, ",
  "-3.112735344770952)"];
rowsFG$ = Flatten[Table[Module[{p = {25/32., 0.5, 25/8., x}, r},
      r = minFG$[g, n, p];
      Print["(c) ", g, ", ", n, " loop(s), xi = ", x, ": v = ", r[[1]], ",  G at the minimum = ",
       25/32. r[[1]]^2 - 25/8., ",  V_min = ", r[[2]], ",  minus hbar ", r[[2]] - hb1FG$[[n]]];
      {g, n, x, r[[1]], r[[2]], r[[2]] - hb1FG$[[n]]}], {g, {"F", "R"}}, {n, {1, 2}}, {x, xisFG$}], 2];
(* Landau gauge, real part of the fixed-order potential *)
landFG$ = Table[Module[{r = minFG$["R", n, {25/32., 0.5, 25/8., 0}]},
     Print["(c) Landau, ", n, " loop(s): v = ", r[[1]], ",  V_min = ", r[[2]], ",  minus hbar ", r[[2]] - hb1FG$[[n]]];
     {"L", n, 0., r[[1]], r[[2]], r[[2]] - hb1FG$[[n]]}], {n, {1, 2}}];
(* couplings scaled by s (lam -> s lam, e^2 -> s e^2), two loops *)
sclFG$ = Flatten[Table[Module[{p = {s 25/32., Sqrt[s] 0.5, 25/8., x}, r},
      r = minFG$[g, 2, p];
      {g, x, s, r[[1]], r[[2]], r[[2]] - hbarFG$[p][[2]]}], {g, {"F", "R"}}, {x, {0.5, 1., 3., 10.}},
     {s, 2.^-Range[0, 5]}], 2];
Do[Module[{rs = Select[sclFG$, #[[1]] === g && #[[2]] == x &]},
   Print["(c) ", g, ", xi = ", x, ", two loops: V_min - hbar for s = 1 ... 1/32: ", rs[[All, 6]],
    ";  ratios s -> s/2: ", rs[[;; -2, 6]]/rs[[2 ;;, 6]], ";  G at the minimum: ",
    (#[[3]] 25/32. #[[4]]^2 - 25/8.) & /@ rs]], {g, {"F", "R"}}, {x, {0.5, 1., 3., 10.}}];
Export[FileNameJoin[{resDirFG$, "fermi_min.csv"}],
  Join[{{"gauge", "loops", "xi", "v", "Vmin", "Vmin_minus_hbar"}}, Map[If[StringQ[#], #, ToString[CForm[#]]] &, Join[rowsFG$, landFG$], {2}],
   {{"gauge", "xi", "s", "v", "Vmin", "Vmin_minus_hbar"}}, Map[If[StringQ[#], #, ToString[CForm[#]]] &, sclFG$, {2}]], "CSV"];
Print["(c) written results/fermi_min.csv"];


(* ::Section:: *)
(*(d) Fermi gauge near the tree minimum*)


(* at fixed phi-independent couplings, G -> 0 from below (xi = 1): the one-loop Goldstone-longitudinal part against
   Espinosa-Garny-Konstandin's -(1/4) xi Z G [ln(xi Z |G|) - 3], and the two-loop V2 *)
Module[{l = 25/32., e = 0.5, m = 25/8., x = 1., rows},
  rows = Table[Module[{ph = Sqrt[(m + g)/l], hF, zF, s, zp, zm, v1, v2},
      hF = -m + 3 l ph^2; zF = e^2 ph^2; s = Sqrt[g (g - 4 x zF)]; zp = (g + s)/2; zm = (g - s)/2;
      v1 = Re[numFG$[fFG$[zp] + fFG$[zm], 1]];
      v2 = numFG$[V2AHFermi /. I2 -> II /. {H -> hF, G -> g, Z -> zF, Zp -> zp, Zm -> zm, xi -> x, phi -> ph}, 1];
      {g, v1, -x zF g (Log[x zF Abs[g]] - 3)/4, Re[v2], Im[v2]}], {g, -10.^-Range[2, 6]}];
  Do[Print["(d) G = ", r[[1]], ":  Re[f(Z+) + f(Z-)] = ", r[[2]], ",  EGK form ", r[[3]], " (relative difference ",
     r[[2]]/r[[3]] - 1, "),  V2 = ", r[[4]], " + ", r[[5]], " i"], {r, rows}];
  Export[FileNameJoin[{resDirFG$, "fermi_ir.csv"}], Prepend[rows, {"G", "Re_fZp_fZm", "EGK", "Re_V2", "Im_V2"}], "CSV"];
  Print["(d) written results/fermi_ir.csv"]];
