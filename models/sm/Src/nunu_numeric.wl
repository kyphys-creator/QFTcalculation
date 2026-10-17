(* ::Package:: *)

(* ::Title:: *)
(*Step (9a): numbers for nu_e nubar_e -> nu_mu nubar_mu: MS-bar (FJ) amplitude, conversion to on-shell inputs, MadLoop*)


(* ::Text:: *)
(*Reads results/nunu_feyncalc.m: W = (rVS + rSE + rTad - 2 Sigma^L_nu(0)) B4 + W_box.  A0, B0 are split as A0 = a0 + m^2 Delta,*)
(*B0 = b0 + Delta with Delta = 1/eps and*)
(*D = 4 - 2 eps (MS-bar: the rational terms (D - 4) Delta are kept, the poles are dropped); a0, b0, C0, D0 are evaluated*)
(*with LoopTools (Delta = 0, mudim = mu^2).  The two-point functions at k^2 = 0 use the closed forms of alpha_matching.wl.*)
(*  (a) the Born: B4/4 against MadLoop's born (spin average 1/4);*)
(*  (b) the UV pole: pole[W] + B4 pole[dln M0] = 0 with the poles of the conversion (= the MS-bar counterterms);*)
(*  (c) W(MS-bar) for two gauges (xiZ, xiW) = (1, 1), (2, 3);  dln M0 (finite) the same in both gauges;*)
(*  (d) W_OS = W + B4 dln M0 at mu = MZ and mu = 500 GeV against MadLoop's finite = Re W_OS/2.*)
(*Inputs (as the MadLoop param_card): 1/alpha(MZ) = 128, MZ = 91.1876, MW = 80.369, MH = 125.2, MT = 172.57 GeV;*)
(*sqrt(s) = 500 GeV, scattering angle pi/3.  Writes results/nunu_numeric.csv.  Batch: wolframscript -file nunu_numeric.wl*)


srcDir$ = DirectoryName[$InputFileName];
r$ = Get[FileNameJoin[{srcDir$, "results", "nunu_feyncalc.m"}]];
(* FeynCalc's A0, B0, C0, D0, DB0 are renamed before LoopTools (whose functions have the same names) is loaded *)
r$ = r$ /. {A0 -> fA0, B0 -> fB0, C0 -> fC0, D0 -> fD0, DB0 -> fDB0};
(* older output kept the photon self-energy in two parts *)
If[!KeyExistsQ[r$, "sAA"], r$["sAA"] = r$["sAAlight"] + r$["sAAheavy"]];
(* the massless fermion loops of Sigma_T^AA and Sigma_T^AZ are the terms with B0(k^2, 0, 0) (their tensor integrals reduce
   to B0 only; the D dependence of the coefficient gives the rational part) *)
lightPart$[x_] := Coefficient[Expand[x], fB0[kk2, 0, 0]] fB0[kk2, 0, 0];
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
KK = 16 Pi^2; ep = Epsilon;
in$ = {ee -> Sqrt[4 Pi/128], MZ -> 911876/10000, MW -> 80369/1000, MH -> 1252/10, MT -> 17257/100};
swcw$ = {cw -> MW/MZ, sw -> Sqrt[1 - MW^2/MZ^2]};
sqs$ = 500; th$ = Pi/3;
kinN$ = {ss -> sqs$^2, tt -> -sqs$^2 (1 - Cos[th$])/2};

(* MS-bar split of the UV-divergent functions, then the eps expansion *)
split$ = {fA0[m2_] :> a0[m2] + m2/ep, fB0[pp_, m1_, m2_] :> b0[pp, m1, m2] + 1/ep};
(* x is linear in the loop functions: x = X0(D) + Delta X1(D) with Delta = 1/eps, so at D = 4 - 2 eps
   pole = X1(4) and finite = X0(4) - 2 X1'(4); lau$ returns {X1, X0} (D symbolic), evL$ the numbers *)
splitDD$ = {fA0[m2_] :> a0[m2] + m2 dd, fB0[pp_, m1_, m2_] :> b0[pp, m1, m2] + dd};
lau$[x_] := Module[{y = Expand[x /. splitDD$]}, {Coefficient[y, dd], y /. dd -> 0}];
evL$[{x1_, x0_}, gauge_, mu_] := Module[{y1 = num$[x1 /. D -> dimS, gauge]},
   {N[y1 /. dimS -> 4], lt$[num$[x0 /. D -> 4, gauge], mu] - 2 N[D[y1, dimS] /. dimS -> 4]}];
(* numerical evaluation with LoopTools at mu *)
lt$[x_, mu_] := Module[{}, SetMudim[N[mu]^2]; SetDelta[0];
   N[x /. {a0[m2_] :> If[m2 == 0, 0, LoopTools`A0[N[m2]]], b0[pp_, m1_, m2_] :> LoopTools`B0[N[pp], N[m1], N[m2]],
       fDB0[pp_, m1_, m2_] :> LoopTools`DB0[N[pp], N[m1], N[m2]],
       fC0[a_, b_, c_, m1_, m2_, m3_] :> LoopTools`C0[N[a], N[b], N[c], N[m1], N[m2], N[m3]],
       fD0[a_, b_, c_, d_, e_, f_, m1_, m2_, m3_, m4_] :> LoopTools`D0[N[a], N[b], N[c], N[d], N[e], N[f], N[m1], N[m2], N[m3], N[m4]]}]];
(* tree-level propagators left outside the loop integrals: FeynAmpDenominator[PropagatorDenominator[Momentum[k], m]] *)
dot$ = {{p1, p1} -> 0, {p2, p2} -> 0, {p3, p3} -> 0, {p4, p4} -> 0, {p1, p2} -> ss/2, {p3, p4} -> ss/2, {p1, p3} -> -tt/2,
   {p2, p4} -> -tt/2, {p1, p4} -> (ss + tt)/2, {p2, p3} -> (ss + tt)/2};
sq$[k_] := Module[{c = Coefficient[k, #] & /@ {p1, p2, p3, p4}, ps = {p1, p2, p3, p4}},
   Sum[c[[i]] c[[j]] If[i == j, 0, If[OrderedQ[{ps[[i]], ps[[j]]}], {ps[[i]], ps[[j]]}, {ps[[j]], ps[[i]]}] /. dot$], {i, 4}, {j, 4}]];
(* the momentum may be Momentum[p3 + p4] or Momentum[p3] + Momentum[p4] *)
fad$ = FeynAmpDenominator[ds__] :> Times @@ (1/(sq$[#[[1]] /. Momentum[k_, ___] :> k] - #[[2]]^2) & /@ {ds});
(* four-dimensional scalar products of the external momenta (from the box and Born traces) *)
pair$ = Pair[Momentum[a_, ___], Momentum[b_, ___]] :> sq$[a + b]/2 - sq$[a]/2 - sq$[b]/2;
(* Eps(p1, p2, p3, p4) = 0 for 2 -> 2 (p4 = p1 + p2 - p3) *)
num$[x_, gauge_] := x /. Eps[__] -> 0 /. fad$ /. pair$ /. gauge /. swcw$ /. in$ /. kinN$;

(* the closed forms at k^2 = 0 (alpha_matching.wl), for Pi_heavy(0) and Sigma_T^AZ(0) *)
dnB0Closed$[n_, a_, b_] := Which[
   a === b, (n!)^2/((2 n + 1)! n a^n),
   a === 0, 1/(n (n + 1) b^n), b === 0, 1/(n (n + 1) a^n),
   n === 1, (a^2 - b^2 - 2 a b Log[a/b])/(2 (a - b)^3),
   True, Integrate[(x (1 - x))^n/(x a + (1 - x) b)^n, {x, 0, 1}, Assumptions -> a > 0 && b > 0, GenerateConditions -> False]/n];
taylorB0$ = fB0[kk_, a_, b_] /; !FreeQ[kk, kk2] :> fB0[0, a, b] + Sum[(kk)^n dnB0[n, a, b], {n, 1, 2}];
closed0$ = {fDB0[0, a_, b_] :> dnB0Closed$[1, a, b], fA0[m2_] :> m2 (1/ep + 1 - Log[m2/mu^2]), fB0[0, 0, 0] -> 0, fB0[0, a_, a_] :> 1/ep - Log[a/mu^2],
   fB0[0, 0, b_] :> 1/ep + 1 - Log[b/mu^2], fB0[0, b_, 0] :> 1/ep + 1 - Log[b/mu^2],
   fB0[0, a_, b_] :> 1/ep + 1 - (a Log[a/mu^2] - b Log[b/mu^2])/(a - b), dnB0[n_, a_, b_] :> dnB0Closed$[n, a, b]};
atZero$[x_, n_, gauge_] := Module[{y = (x /. gauge /. swcw$ /. taylorB0$) /. closed0$ /. D -> 4 - 2 ep},
   y = Normal[Series[y, {kk2, 0, n}]];
   y = Coefficient[Expand[y], kk2, n];
   Normal[Series[y, {ep, 0, 0}]]];

(* the conversion dln M0 = 2 de - dln(sw^2 cw^2) + dMZ^2/(s - MZ^2), each d as {pole coefficient, finite} at mu *)
conv$[gauge_, mu0_] := Module[{dW, dZ, piH, sAZ0, piL, de, dlnSC, w2, z2},
   (* Re Sigma_T^VV(MV^2) *)
   dW = evL$[lau$[r$["sWW"] /. kk2 -> MW^2], gauge, mu0]; dZ = evL$[lau$[r$["sZZ"] /. kk2 -> MZ^2], gauge, mu0];
   dW = {dW[[1]], Re[dW[[2]]]}; dZ = {dZ[[1]], Re[dZ[[2]]]};
   (* Pi_heavy(0) = d Sigma_T^AA,heavy / dk^2 at 0; Sigma_T^AZ(0); Re Pi_light(MZ^2) = Re Sigma_T^AA,light(MZ^2)/MZ^2 *)
   Module[{cAZ = Coefficient[Expand[r$["sAZ"]], fB0[kk2, 0, 0]]},
     If[Simplify[cAZ /. kk2 -> 0] =!= 0, Print["   massless loops of Sigma_T^AZ do not vanish at k^2 = 0: ", cAZ]]];
   piH = atZero$[Expand[r$["sAA"] - lightPart$[r$["sAA"]]], 1, gauge];
   sAZ0 = atZero$[Expand[r$["sAZ"] - lightPart$[r$["sAZ"]]], 0, gauge];
   piL = evL$[lau$[lightPart$[r$["sAA"]] /. kk2 -> MZ^2], gauge, mu0];
   piL = {piL[[1]], Re[piL[[2]]]}/N[num$[MZ^2, gauge]];
   de = {num$[Coefficient[piH, ep, -1]/2 + sw/Sqrt[1 - sw^2] Coefficient[sAZ0, ep, -1]/MZ^2, gauge] + piL[[1]]/2,
     N[num$[(Coefficient[Expand[piH], ep, 0] /. mu -> mu0)/2 +
         sw/Sqrt[1 - sw^2] (Coefficient[Expand[sAZ0], ep, 0] /. mu -> mu0)/MZ^2, gauge]] + piL[[2]]/2};
   {w2, z2} = N[num$[{MW^2, MZ^2}, gauge]];
   dlnSC = dW/w2 + (dZ - dW)/(z2 - w2) - 2 dZ/z2;
   <|"de" -> de, "dMW2" -> dW, "dMZ2" -> dZ, "dlnM0" -> 2 de - dlnSC + dZ/(N[num$[ss, gauge]] - z2)|>];

gauges$ = {{xiA -> 1, xiZ -> 1, xiW -> 1}, {xiA -> 1, xiZ -> 2, xiW -> 3}};
b4$ = r$["B4"];
(* W = (rVS + rTad - 2 Sigma^L(0)) B4 + W_box *)
sLnuLau$ = Module[{y = Simplify[(r$["sLnu"] /. closed0$) /. D -> 4 - 2 ep]}, Normal[Series[y, {ep, 0, 0}]]];
Print["    K Sigma^L_nu(0) = ", Simplify[KK sLnuLau$]];
wLau$ = lau$[(r$["rVS"] + Lookup[r$, "rSE", 0] + r$["rTad"]) b4$ + r$["wBox"]];
legLau$ = {Coefficient[-2 sLnuLau$, ep, -1], Coefficient[-2 sLnuLau$, ep, 0]} b4$;
born$ = N[num$[b4$, gauges$[[1]]]];
Print["(a) B4/4 = ", NumberForm[born$/4, 16]];
rows$ = {};
Do[Module[{g = gauges$[[ig]], wPole, wFin, cv, wOS},
    {wPole, wFin} = evL$[wLau$, g, mu0] + N[num$[legLau$ /. mu -> mu0, g]];
    cv = conv$[g, mu0];
    wOS = wFin + born$ cv["dlnM0"][[2]];
    Print["(b,c,d) gauge ", {xiZ, xiW} /. g, ", mu = ", mu0, ":  pole[W] + B4 pole[dln M0] = ", wPole + born$ cv["dlnM0"][[1]],
      " (W pole ", wPole, ");  W(MS) = ", wFin, ";  dln M0 = ", cv["dlnM0"][[2]], " (de ", cv["de"][[2]], ", dMW2 ",
      cv["dMW2"][[2]], ", dMZ2 ", cv["dMZ2"][[2]], ");  Re W_OS/2 = ", NumberForm[Re[wOS]/2, 16]];
    AppendTo[rows$, {xiZ /. g, xiW /. g, mu0, Re[wFin], Im[wFin], cv["dlnM0"][[2]], Re[wOS]/2, born$/4}]],
  {ig, 2}, {mu0, {N[911876/10000], 500.}}];
Export[FileNameJoin[{srcDir$, "results", "nunu_numeric.csv"}],
  Prepend[rows$, {"xiZ", "xiW", "mu", "re_W_MSbar", "im_W_MSbar", "dlnM0_fin", "re_W_OS_over_2", "born_over_4"}], "CSV"];
