(* ::Package:: *)

(* ::Title:: *)
(*Step (7): MS-bar parameters from measured quantities at one loop (FJ tadpoles), SM note*)


(* ::Text:: *)
(*One-loop relations (note Eqs. (pole), (GF1), (alphahat)), with the loop functions evaluated at the tree-level values*)
(*made from the on-shell inputs (the truncation theta = theta^(0) + theta^(1) of Buttazzo et al.):*)
(*  v^2 = v_G^2 (1 + DeltaHat),  v_G^2 = 1/(sqrt 2 G_F);   M_V^2(MS) = M_V^2 (1 + dV),  dV = Re Sigma_T^VV(M_V^2)/M_V^2;*)
(*  M_H^2(MS) = 2 mu^2 = M_h^2 (1 + dH);   m_t(MS) = M_t (1 + dt),  dt = Re(Sigma^V + Sigma^S)(M_t^2)*)
(*(Sigma with the tadpole-attached diagrams), so that*)
(*  g = g0 (1 + (dW - DeltaHat)/2),  g^2 + g'^2 = G0^2 (1 + dZ - DeltaHat),  lambda = lambda0 (1 + dH - DeltaHat),*)
(*  m^2 = 2 mu^2 = M_h^2 (1 + dH),  y_t = y0 (1 + dt - DeltaHat/2),  v = v_G (1 + DeltaHat/2).*)
(*Input schemes: "MW" (G_F, M_W, M_Z, M_h, M_t, alpha_s; as Buttazzo et al.) and "alpha" (alpha(0), Delta alpha, G_F,*)
(*M_Z, M_h, M_t, alpha_s; M_W is predicted; as Martin-Robertson): e(mu) from Eq. (alphahat) (1/alpha-hat linear),*)
(*g^2 g'^2 = e^2 (g^2 + g'^2), and M_W,pole^2 = (g v/2)^2 (1 - dW); the loop functions are then evaluated at the predicted*)
(*M_W, iterated to a fixed point.  alpha_s^(6)(mu) from alpha_s^(5)(MZ) with one-loop running and decoupling.*)
(*Variant for the comparison of y_t: pure QCD to three loops, m_t(M_t)/M_t = 1 - (4/3) a - k2 a^2 - k3 a^3*)
(*(a = alpha_s^(6)(M_t)/pi), derived below from Marquard et al. 2016 Eq. (2.5) and the six-flavour running of m.*)
(*Checks: (a) Buttazzo et al. inputs -> their NLO values (Table 3); (b) gauge independence (xiZ = xiW = xiG = 2 and 3,*)
(*xiA = 1 as in step (5));*)
(*(c) mu dependence: matching at MZ, run with the one-loop RGE to M_t, compared with matching at M_t;*)
(*(d) Martin-Robertson inputs (alpha scheme) -> their values; (e) PDG 2024 inputs, both schemes.*)
(*Reads results/oneloop_sigma.m, mudecay_deltahat_finite.m, alpha_deltae.m; writes results/msbar_fit.csv.*)
(*Batch: wolframscript -file msbar_fit.wl*)


(* ::Section:: *)
(*Setup*)


srcDirMF$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirMF$ = FileNameJoin[{srcDirMF$, "results"}];
sig$ = Association[Get[FileNameJoin[{resDirMF$, "oneloop_sigma.m"}]]];
dHatK$ = Get[FileNameJoin[{resDirMF$, "mudecay_deltahat_finite.m"}]];          (* K DeltaHat, MS-bar *)
deBosK$ = Association[Get[FileNameJoin[{resDirMF$, "alpha_deltae.m"}]]]["deltaE_bosonic_finite"];  (* K delta_e, bosons *)
KK = 16 Pi^2;
kRule$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2};
ibp$ = PaVe[0, {0, pp_, pp_}, {0, 0, m2_}] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2;
fin$[x_] := Module[{y = x /. {A0[m2_] :> m2/ep + a0f[m2], B0[p2_, a_, b_] :> 1/ep + b0f[p2, a, b]} /. D -> 4 - 2 ep},
   SeriesCoefficient[Series[y, {ep, 0, 0}], 0]];
linkMF$ = Quiet[Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]]];
SetDelta[0.];
nf$[x_, n_] := Module[{y = N[x], e}, Which[!NumericQ[y], ToString[y], y == 0, "0",
    Abs[y] < 10^-3, e = Floor[Log10[Abs[y]]]; ToString[NumberForm[y/10^e, n]] <> "e" <> ToString[e],
    True, ToString[NumberForm[y, n]]]];

(* the Sigma's with the tadpole parts; K x finite part at k^2 = p2 and scale mu0.  Numbers first (with xiA = 1, which
   removes the (A0(MA^2) - A0(xiA MA^2))/((1 - xiA) MA^2) terms), then Together, then the finite part.  The photon
   keeps a small mass maMF$: on shell the IR logarithms ln MA^2 come with a factor k^2 - M^2 = 0, and terms with
   1/MA^2 have numerators of order MA^2, so MA -> 0 cannot be taken term by term (0 x infinity); the MA dependence
   of the result is O(MA^2/M^2) and is checked with two values of MA *)
sWW$ = Total[sig$["WW"]]; sZZ$ = Total[sig$["ZZ"]]; sHH$ = Total[sig$["HH"]]; sTT$ = Total[Flatten[sig$["TT"]]];
maMF$ = 10^-3;
evalK$[expr_, p2_, rules_, mu0_] := Module[{x},
   SetMudim[N[mu0^2]];
   x = expr /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2] /. rules /. MA -> SetPrecision[maMF$, 40];
   (* the external k^2 from the same 40-digit numbers: a mismatch of 1e-16 in k^2 - M^2 is enhanced by 1/MA^2 *)
   x = Together[x /. kRule$ /. ibp$] /. kk2 -> (p2 /. MZ -> MW/Sqrt[1 - sw^2] /. rules);
   x = fin$[x] /. {a0f[y_] :> If[y == 0, 0, y (1 - Log[y/mu0^2])]} /. {b0f[pp_, a_, b_] :> LoopTools`B0[N[pp], N[a], N[b]]};
   Re[N[x]]];

(* light fermions: running masses near M_t (Martin-Robertson Yukawas times v_G/sqrt 2).  Exactly massless fermions
   (and xi = 1) give 0/0 in the closed forms of the Sigma's, so the gauges are xi = 2, 3 and the light masses are
   halved to see their effect *)
lightMR$ = With[{c = 246.21965/Sqrt[2]}, {MB -> 0.015480097 c, MC -> 0.0033820038 c, MS -> 0.00029094484 c,
    MD -> 1.4609792*^-5 c, MU -> 6.7227779*^-6 c, MTA -> 0.0099944422 c, MMU -> 0.00058837986 c, Me -> 2.7929820*^-6 c}];
lightHalf$ = lightMR$ /. (m_ -> x_) :> (m -> x/2);   (* sensitivity to the light masses *)

(* alpha_s^(6)(mu) from alpha_s^(5)(MZ): one-loop running (nf = 5) and one-loop decoupling at M_t *)
alphaS6$[as5_, mz_, mt_, mu0_] := Module[{a5 = 1/(1/as5 + (23/3)/(2 Pi) Log[mu0/mz])},
   a5 (1 + a5/(6 Pi) Log[mu0^2/mt^2])];
(* m_t(M_t)/M_t from m_t(m_t)/M_t = 1 - c1 a - c2 a^2 - c3 a^3 (Marquard et al. 2016, Eq. (2.5): 0.4244, 0.65441,
   1.944 in powers of alpha_s) and m(M) = m(mbar) exp(-int gamma_m dln mu^2), gamma_m = a + gamma1 a^2,
   gamma1 = 202/48 - 20 nf/144 = 27/8 (nf = 6); L = ln(M^2/mbar^2) = -2 ln(m(m)/M) is O(a) *)
{c1QCD$, c2QCD$, c3QCD$} = {4/3, 0.65441 Pi^2, 1.944 Pi^3}; gam1QCD$ = 27/8;
k2QCD$ = c2QCD$ + 2 c1QCD$; k3QCD$ = c3QCD$ + 2 c2QCD$ + 2 gam1QCD$ c1QCD$ - c1QCD$^2;
Print["    m_t(M_t)/M_t = 1 - 4/3 a - ", nf$[k2QCD$, 6], " a^2 - ", nf$[k3QCD$, 6], " a^3  (rounding of 1.944: +-",
  nf$[0.0005 Pi^3, 2], ")"];
(* pole mass from the variable-width Breit-Wigner mass *)
poleFromBW$[m_, g_] := m/Sqrt[1 + g^2/m^2];


(* ::Section:: *)
(*One-loop matching*)


(* corrections at the tree-level point {ee, sw, MW, MH, MT, gS, light}; returns <|dW, dZ, dH, dt, dHat|> *)
corr$[tree_, mu0_, xi_] := Module[{rules, mz},
   rules = Join[tree /. (x_ -> y_?NumericQ) :> (x -> SetPrecision[y, 40]),
     {xiA -> 1, xiZ -> xi, xiW -> xi, xiG -> xi, CF -> 4/3, CA -> 3}];
   mz = (MW/Sqrt[1 - sw^2]) /. tree;
   <|"dW" -> evalK$[sWW$, MW^2, rules, mu0]/KK/(MW^2 /. tree),
     "dZ" -> evalK$[sZZ$, MZ^2, rules, mu0]/KK/mz^2,
     "dH" -> evalK$[sHH$, MH^2, rules, mu0]/KK/(MH^2 /. tree),
     "dt" -> evalK$[sTT$, MT^2, rules, mu0]/KK,
     "dHat" -> N[dHatK$ /. rules /. mu -> mu0]/KK|>];
(* m^2 is the Lagrangian parameter: theta = m^2 is expanded, m = M_h sqrt(1 + dH) (as Buttazzo et al.) *)

(* scheme "MW": inputs <|GF, MW, MZ, Mh, Mt, as5|> (pole masses) *)
fitMW$[in_, mu0_, light_, xi_, opts___] := Module[{vG, s0, g0, G0, gp0, tree, c, as6, g, G2, gp, lam, m, yt, ho},
   vG = 1/Sqrt[Sqrt[2] in["GF"]];
   s0 = Sqrt[1 - in["MW"]^2/in["MZ"]^2]; g0 = 2 in["MW"]/vG; G0 = 2 in["MZ"]/vG; gp0 = Sqrt[G0^2 - g0^2];
   as6 = If[KeyExistsQ[in, "g3"], in["g3"]^2/(4 Pi), alphaS6$[in["as5"], in["MZ"], in["Mt"], mu0]];
   tree = Join[{ee -> g0 s0, sw -> s0, MW -> in["MW"], MH -> in["Mh"], MT -> in["Mt"], gS -> Sqrt[4 Pi as6]}, light];
   c = corr$[tree, mu0, xi];
   g = g0 (1 + (c["dW"] - c["dHat"])/2);
   gp = gp0 (1 + (G0^2 (c["dZ"] - c["dHat"]) - g0^2 (c["dW"] - c["dHat"]))/(2 gp0^2));
   lam = in["Mh"]^2/(2 vG^2) (1 + c["dH"] - c["dHat"]);
   m = in["Mh"] Sqrt[1 + c["dH"]];
   ho = With[{a = as6/Pi}, -k2QCD$ a^2 - k3QCD$ a^3];
   yt = Sqrt[2] in["Mt"]/vG (1 + c["dt"] - c["dHat"]/2);
   <|"lambda" -> lam, "yt" -> yt, "yt_QCD3" -> yt + Sqrt[2] in["Mt"]/vG ho, "g2" -> g, "gY" -> gp,
     "m" -> m, "v" -> vG (1 + c["dHat"]/2), "g3" -> Sqrt[4 Pi as6], "corr" -> c|>];

(* scheme "alpha": inputs <|alpha0, dalLep, dalHad, GF, MZ, Mh, Mt, as5|>; M_W predicted.  The tadpole parts of
   dW, dZ, DeltaHat (about 0.12 each at mu = M_t) cancel only in the combinations DeltaHat - dZ and dZ - dW, so the
   relations are linear in them (products would leave spurious tadpole^2 terms):
     s^2 c^2 = e(mu)^2 / (4 sqrt 2 G_F M_Z^2) (1 + DeltaHat - dZ),   M_W = M_Z c (1 + (dZ - dW)/2),
   with e(mu) from Eq. (alphahat); the loop functions are evaluated at the predicted M_W (fixed point), and the
   couplings then follow from the formulas of scheme "MW" with this M_W *)
fitAlpha$[in_, mu0_, light_, xi_] := Module[{vG, mz, mw, s0, g0, tree, c, as6, e2, dAh, sc2, c2, mwP, it, ePert, r},
   vG = 1/Sqrt[Sqrt[2] in["GF"]]; mz = in["MZ"]; mw = 80.35;
   as6 = alphaS6$[in["as5"], mz, in["Mt"], mu0];
   Do[
    s0 = Sqrt[1 - mw^2/mz^2]; g0 = 2 mw/vG;
    tree = Join[{ee -> g0 s0, sw -> s0, MW -> mw, MH -> in["Mh"], MT -> in["Mt"], gS -> Sqrt[4 Pi as6]}, light];
    c = corr$[tree, mu0, xi];
    (* Eq. (alphahat): bosons (W loop), top, massless light fermions at MZ^2, Delta alpha *)
    ePert = With[{e0 = Sqrt[4 Pi in["alpha0"]]},
      (2 deBosK$ /. {ee -> e0, sw -> s0, MW -> mw, mu -> mu0}) - e0^2 16/9 Log[in["Mt"]^2/mu0^2] +
       e0^2 4/3 20/3 (5/3 - Log[mz^2/mu0^2])];
    dAh = in["dalLep"] + in["dalHad"] + ePert/KK;
    e2 = 4 Pi in["alpha0"]/(1 - dAh);
    sc2 = e2/(4 Sqrt[2] in["GF"] mz^2) (1 + c["dHat"] - c["dZ"]);
    c2 = (1 + Sqrt[1 - 4 sc2])/2;
    mwP = mz Sqrt[c2] (1 + (c["dZ"] - c["dW"])/2);
    If[Abs[mwP - mw] < 10^-9, Break[]]; mw = mwP, {it, 30}];
   r = fitMW$[<|"GF" -> in["GF"], "MW" -> mw, "MZ" -> mz, "Mh" -> in["Mh"], "Mt" -> in["Mt"], "as5" -> in["as5"]|>,
     mu0, light, xi];
   Join[r, <|"MW_pred" -> mw, "alphaInv" -> 4 Pi/e2|>]];

keys$ = {"lambda", "yt", "g2", "gY", "m"};
row$[r_] := nf$[#, 6] & /@ Lookup[r, keys$];


(* ::Section:: *)
(*(a) Buttazzo et al. inputs: NLO row of their Table 3*)


inB$ = <|"GF" -> 1/(Sqrt[2] 246.21971^2), "MW" -> 80.384, "MZ" -> 91.1876, "Mh" -> 125.15, "Mt" -> 173.34,
   "as5" -> 0.1184|>;
butLO$ = {0.12917, 0.99561, 0.65294, 0.34972, 125.15};
butNLO$ = {0.12774, 0.95113, 0.64754, 0.35940, 132.37};
butNNLO$ = {0.12604, 0.94018, 0.64779, 0.35830, 131.55};
fitB$ = fitMW$[inB$, 173.34, lightMR$, 2];
fitB0$ = fitMW$[inB$, 173.34, lightHalf$, 2];
fitBg$ = fitMW$[Append[inB$, "g3" -> 1.1666], 173.34, lightMR$, 2];
Print["(a) Buttazzo et al. inputs, mu = M_t: (lambda, y_t, g2, gY, m/GeV)"];
Print["    tree level (ours):        ", nf$[#, 6] & /@ {125.15^2/(2 246.21971^2), Sqrt[2] 173.34/246.21971,
     2 80.384/246.21971, 2 Sqrt[91.1876^2 - 80.384^2]/246.21971, 125.15}, "   Buttazzo LO ", butLO$];
Print["    one loop, light masses:   ", row$[fitB$], "   (g3 = ", nf$[fitB$["g3"], 5], ")"];
Print["    one loop, light masses / 2:", row$[fitB0$]];
Print["    one loop, g3(M_t) = 1.1666:", row$[fitBg$]];
Print["    Buttazzo NLO:             ", butNLO$, ";  NNLO ", butNNLO$];
Print["    ours - Buttazzo NLO (g3 = 1.1666): ", nf$[#, 3] & /@ (Lookup[fitBg$, keys$] - butNLO$)];
Print["    y_t with QCD to 3 loops (g3 = 1.1666): ", nf$[fitBg$["yt_QCD3"], 6],
  "  (Buttazzo NNLO 0.94018, with 3-loop QCD 0.93690)"];


(* ::Section:: *)
(*(b) gauge independence*)


fitB3$ = fitMW$[inB$, 173.34, lightMR$, 3];
maMF$ = 10^-2; fitBma$ = fitMW$[inB$, 173.34, lightMR$, 2]; maMF$ = 10^-3;
Print["(b) photon mass 1e-2 minus 1e-3 GeV (lambda, y_t, g2, gY, m, v): ",
  nf$[#, 3] & /@ (Lookup[fitBma$, Append[keys$, "v"]] - Lookup[fitB$, Append[keys$, "v"]])];
Print["(b) xi = 3 minus xi = 2 (lambda, y_t, g2, gY, m, v): ",
  nf$[#, 3] & /@ (Lookup[fitB3$, Append[keys$, "v"]] - Lookup[fitB$, Append[keys$, "v"]])];
Print["    corrections at xi = 3 minus xi = 2: ", nf$[#, 3] & /@ Values[fitB3$["corr"] - fitB$["corr"]]];
Print["    corrections at xi = 2 (dW, dZ, dH, dt, DeltaHat): ", nf$[#, 8] & /@ Values[fitB$["corr"]]];


(* ::Section:: *)
(*(c) mu dependence: match at MZ, run to M_t with the one-loop RGE (note Eq. (beta), all Yukawas)*)


rge$[x_] := Module[{TT, NY4, bu, bd, bl},
   TT = 3 (yt[x]^2 + yc[x]^2 + yu[x]^2 + yb[x]^2 + ys[x]^2 + yd[x]^2) + yta[x]^2 + ymu[x]^2 + ye[x]^2;
   NY4 = 3 (yt[x]^4 + yc[x]^4 + yu[x]^4 + yb[x]^4 + ys[x]^4 + yd[x]^4) + yta[x]^4 + ymu[x]^4 + ye[x]^4;
   bu[u_, d_] := u (3/2 (u^2 - d^2) + TT - 8 g3[x]^2 - 9/4 gg[x]^2 - 17/12 gp[x]^2);
   bd[d_, u_] := d (3/2 (d^2 - u^2) + TT - 8 g3[x]^2 - 9/4 gg[x]^2 - 5/12 gp[x]^2);
   bl[l_] := l (3/2 l^2 + TT - 9/4 gg[x]^2 - 15/4 gp[x]^2);
   {-19/6 gg[x]^3, 41/6 gp[x]^3, -7 g3[x]^3,
    24 la[x]^2 + 4 la[x] TT - 2 NY4 - 3 la[x] (3 gg[x]^2 + gp[x]^2) + 3/8 (2 gg[x]^4 + (gg[x]^2 + gp[x]^2)^2),
    m2[x] (12 la[x] + 2 TT - 9/2 gg[x]^2 - 3/2 gp[x]^2),
    bu[yt[x], yb[x]], bu[yc[x], ys[x]], bu[yu[x], yd[x]], bd[yb[x], yt[x]], bd[ys[x], yc[x]], bd[yd[x], yu[x]],
    bl[yta[x]], bl[ymu[x]], bl[ye[x]]}/KK];
varsR$ = {gg, gp, g3, la, m2, yt, yc, yu, yb, ys, yd, yta, ymu, ye};
runTo$[f_, mu0_, mu1_, light_] := Module[{v = f["v"], init, sol},
   init = {gg -> f["g2"], gp -> f["gY"], g3 -> f["g3"], la -> f["lambda"], m2 -> f["m"]^2/2, yt -> f["yt"],
     yc -> Sqrt[2] (MC /. light)/v, yu -> Sqrt[2] (MU /. light)/v, yb -> Sqrt[2] (MB /. light)/v,
     ys -> Sqrt[2] (MS /. light)/v, yd -> Sqrt[2] (MD /. light)/v, yta -> Sqrt[2] (MTA /. light)/v,
     ymu -> Sqrt[2] (MMU /. light)/v, ye -> Sqrt[2] (Me /. light)/v};
   sol = NDSolve[Join[Thread[(D[#[t], t] & /@ varsR$) == rge$[t]], Thread[(#[0] & /@ varsR$) == (varsR$ /. init)]],
     varsR$, {t, 0, Log[mu1/mu0]}, PrecisionGoal -> 12, AccuracyGoal -> 14];
   With[{p = Association[Thread[varsR$ -> (#[Log[mu1/mu0]] & /@ varsR$ /. First[sol])]]},
    <|"lambda" -> p[la], "yt" -> p[yt], "g2" -> p[gg], "gY" -> p[gp], "m" -> Sqrt[2 p[m2]]|>]];
fitBz$ = fitMW$[inB$, 91.1876, lightMR$, 2];
runB$ = runTo$[fitBz$, 91.1876, 173.34, lightMR$];
Print["(c) matched at MZ and run to M_t:  ", row$[runB$]];
Print["    matched at M_t:                ", row$[fitB$]];
Print["    difference (two-loop size):    ", nf$[#, 3] & /@ (Lookup[runB$, keys$] - Lookup[fitB$, keys$]),
  ";  Buttazzo NNLO - NLO: ", nf$[#, 3] & /@ (butNNLO$ - butNLO$)];


(* ::Section:: *)
(*(d) Martin-Robertson inputs (alpha scheme)*)


inMR$ = <|"alpha0" -> 1/137.035999139, "dalLep" -> 0.03149769, "dalHad" -> 0.02764, "GF" -> 1.1663787*^-5,
   "MZ" -> poleFromBW$[91.1876, 2.4952], "Mh" -> 125.1, "Mt" -> 173.1, "as5" -> 0.1181|>;
mrVals$ = {0.12603842, 0.93480082, 0.64765961, 0.35853877, Sqrt[2] 92.878850};
fitMR$ = fitAlpha$[inMR$, 173.1, lightMR$, 2];
Print["(d) Martin-Robertson inputs (M_Z pole ", nf$[inMR$["MZ"], 7], "), mu = 173.1 GeV:"];
Print["    one loop (ours):    ", row$[fitMR$], ";  y_t with QCD to 3 loops ", nf$[fitMR$["yt_QCD3"], 6],
  ";  g3 ", nf$[fitMR$["g3"], 5], " (MR 1.16362)"];
Print["    Martin-Robertson:   ", nf$[#, 6] & /@ mrVals$];
Print["    ours - MR:          ", nf$[#, 3] & /@ (Lookup[fitMR$, keys$] - mrVals$)];
Print["    M_W predicted (pole, one loop): ", nf$[fitMR$["MW_pred"], 6], " GeV, Breit-Wigner ",
  nf$[fitMR$["MW_pred"] Sqrt[1 + (2.085/80.35)^2], 6], " GeV;  1/alpha-hat(mu) ", nf$[fitMR$["alphaInv"], 7]];


(* ::Section:: *)
(*(e) PDG 2024 inputs*)


gzP$ = 2.4955; gwP$ = 2.085;
inP$ = <|"GF" -> 1.1663788*^-5, "MW" -> poleFromBW$[80.3692, gwP$], "MZ" -> poleFromBW$[91.1880, gzP$],
   "Mh" -> 125.20, "Mt" -> 172.57, "as5" -> 0.1180, "alpha0" -> 1/137.035999177, "dalLep" -> 0.03149769,
   "dalHad" -> 0.02783|>;
fitPw$ = fitMW$[inP$, 172.57, lightMR$, 2];
fitPa$ = fitAlpha$[inP$, 172.57, lightMR$, 2];
Print["(e) PDG 2024 (M_Z, M_W pole ", nf$[inP$["MZ"], 7], ", ", nf$[inP$["MW"], 7], "), mu = M_t = 172.57 GeV:"];
Print["    scheme MW:     ", row$[fitPw$], ";  v ", nf$[fitPw$["v"], 6], ";  y_t QCD3 ", nf$[fitPw$["yt_QCD3"], 6],
  ";  g3 ", nf$[fitPw$["g3"], 5]];
Print["    scheme alpha:  ", row$[fitPa$], ";  v ", nf$[fitPa$["v"], 6], ";  y_t QCD3 ", nf$[fitPa$["yt_QCD3"], 6]];
Print["    M_W predicted (alpha scheme): pole ", nf$[fitPa$["MW_pred"], 6], " GeV, Breit-Wigner ",
  nf$[fitPa$["MW_pred"] Sqrt[1 + (gwP$/fitPa$["MW_pred"])^2], 6], " GeV (measured 80.3692)"];

csvRow$[label_, r_] := Prepend[ToString[CForm[N[#]]] & /@ Lookup[r, {"lambda", "yt", "yt_QCD3", "g2", "gY", "m", "v", "g3",
      "MW_pred"}, 0], label];
Export[FileNameJoin[{resDirMF$, "msbar_fit.csv"}],
  {{"case", "lambda", "yt", "yt_QCD3", "g2", "gY", "m_GeV", "v_FJ_GeV", "g3", "MW_pole_predicted_GeV"},
   csvRow$["Buttazzo_inputs_mu_Mt", fitB$], csvRow$["Buttazzo_inputs_g3_1.1666", fitBg$],
   csvRow$["Buttazzo_inputs_light_masses_half", fitB0$], csvRow$["Buttazzo_inputs_xi3", fitB3$],
   csvRow$["MartinRobertson_inputs_alpha_scheme", fitMR$],
   csvRow$["PDG2024_MW_scheme", fitPw$], csvRow$["PDG2024_alpha_scheme", fitPa$],
   csvRow$["Buttazzo_inputs_matched_MZ_run_to_Mt", runB$]}, "CSV"];
Print["Summary: ", {Lookup[fitBg$, keys$] - butNLO$, Max[Abs[Lookup[fitB3$, keys$] - Lookup[fitB$, keys$]]]}];
