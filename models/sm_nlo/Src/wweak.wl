(* ::Package:: *)

(* ::Title:: *)
(*Step (4b) of the NLO note: the electroweak virtual correction and the soft photon of W+ -> f fbar'*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (4b).  The S-matrix element of W+(k) -> f(p1) fbar'(p2) is the bare amputated vertex*)
(*(wff_feyncalc.wl: all loops but the gluon, the photon massless) with the on-shell LSZ factors and the MS-bar counterterms:*)
(*  FL = V + FL_vertex + V dZ_W/2 + (1/2) [dZ^{f L+} V + V dZ^{f' L}] + V dg/g + dV,   FR, HL, HR from the vertex alone,*)
(*  dZ_W = -Sigma_T^WW'(M_W^2) (wsig_feyncalc.wl: the derivative taken on the integrand, its photonic infrared pole kept),*)
(*  dZ^{fL} on the diagonal: the weak part of zff_feyncalc.wl (step (4a)) plus the photonic part (the photon loop of*)
(*      step (3), Feynman gauge, its infrared pole kept); off the diagonal: the CKM note's quark self-energies*)
(*      (models/sm_ckm/Src/results/oneloop_ckm_sigma.m; no photon, no gluon there), Denner's form;*)
(*  dg/g = (Delta/2)(-19/6) g^2/K and dV of the CKM note's Eq. (Vrun) (as its wud_renormalized.wl).*)
(*The photon of the vertex in Feynman gauge (xiA = 1, as the photonic field constants); xiZ, xiW general.  With a massless photon*)
(*the virtual correction keeps an infrared pole: its coefficient must equal minus that of the soft emission,*)
(*  K_S = -(1/(4 eps)) (4 pi mu^2/Delta E^2)^eps Sigma(eps)/Gamma(1 - eps),  Sigma = -sum_ij eta_i eta_j e_i e_j A_ij*)
(*(eta = -1 for the incoming W, +1 for f, fbar'; e the charges), Gamma_S/Gamma_0 = (alpha/pi) K_S, with the angular integrals*)
(*A_ij of step (3) in the W rest frame.  Package-X for the loop functions (MS-bar: ScaleMu^2 = pi e^gamma_E mu^2, the poles*)
(*shown separately).  Writes results/wweak_vs.csv (the finite part of virtual + soft per Delta E) and results/wweak_ml.csv*)
(*(the virtual alone at the CKM note's MadLoop point).  Batch:  wolframscript -file wweak.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
$MaxExtraPrecision = 200;
srcDirWW$ = DirectoryName[$InputFileName];
workDirWW$ = FileNameJoin[{srcDirWW$, "work"}];
resDirWW$ = FileNameJoin[{srcDirWW$, "results"}];
t0WW$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0WW$], " s] ", s];
KK = 16 Pi^2;
chansWW$ = {{1, 1}, {1, 2}, {1, 3}, {3, 1, 1}, {3, 1, 2}, {3, 1, 3}, {3, 2, 1}, {3, 2, 2}, {3, 2, 3}};
wffWW$ = Association[(# -> (Get[FileNameJoin[{workDirWW$, "wff_" <> StringJoin[ToString /@ #] <> ".m"}]] /.
       {SDF[__] -> 1, SUNFDelta[__] -> 1})) & /@ chansWW$];
zffWW$[t_, g_] := Get[FileNameJoin[{workDirWW$, "zff_" <> ToString[t] <> ToString[g] <> ".m"}]] /. {SDF[__] -> 1, SUNFDelta[__] -> 1};
wsigWW$ = Get[FileNameJoin[{workDirWW$, "wsig.m"}]];
(* Sigma_T'(M_W^2): the derivative of the reduced Sigma_T(k^2) (wsig_feyncalc.wl), B0' at threshold with the massless photon
   evaluated in dimensional regularization below (pxDB0WW$) *)
dsigWW$ = (D[wsigWW$["sigT"], kk2] /. kk2 -> MW^2) /. Derivative[1, 0, 0][B0][a__] :> DB0[a];
If[FreeQ[dsigWW$, DB0], Print["WARNING: no B0 derivative in Sigma_T'"]];
sig3WW$ = Association[Get[FileNameJoin[{srcDirWW$, "..", "..", "sm_ckm", "Src", "results", "oneloop_ckm_sigma.m"}]]];
kRuleWW$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
toCKWW$ = {vR[i_, j_] :> (cK[i, j] + cKc[i, j])/2, vI[i_, j_] :> (cK[i, j] - cKc[i, j])/(2 I)};
upMWW$ = {MU, MC, MT}; dnMWW$ = {MD, MS, MB}; lepMWW$ = {Me, MMU, MTA};

(* ::Section:: *)
(*Field constants*)

(* the photonic field constant of a fermion of charge Q, mass m (K units): e^2 Q^2 TID[Sigma_V + 2 m^2 (Sigma_V' + Sigma_S')]/(i pi^2)
   (step (3): the photon loop, Feynman gauge; checked there against -(alpha Q^2/(4 pi)) [3 (1/eps - gamma_E + ln(4 pi mu^2/m^2)) + 4]) *)
FCClearScalarProducts[];
numSEWW$ = GAD[rho] . (GSD[p] - GSD[q] + mq) . GAD[rho];
intVWW$ = DiracTrace[GSD[p] . numSEWW$, DiracTraceEvaluate -> True]/(4 SPD[p, p]) FAD[q, {q - p, mq}];
intSWW$ = DiracTrace[numSEWW$, DiracTraceEvaluate -> True]/(4 mq) FAD[q, {q - p, mq}];
ddp2WW$[f_] := Contract[FVD[p, al] FourDivergence[f, FVD[p, al]]]/(2 SPD[p, p]);
{dIntVWW$, dIntSWW$} = ddp2WW$ /@ {intVWW$, intSWW$};
ScalarProduct[p, p] = mq^2;
dZgamWW$ = Simplify[TID[intVWW$ + 2 mq^2 (dIntVWW$ + dIntSWW$), q, ToPaVe -> True]/(I Pi^2)];
FCClearScalarProducts[];
Print["photonic field constant (K units, per e^2 Q^2): ", dZgamWW$];
kdZgamWW$[q_, m_] := ee^2 q^2 (dZgamWW$ /. mq -> m);
(* the weak diagonal field constants (left-handed) of step (4a), p^2 = pp2 kept *)
dZweakLWW$[t_, g_] := Module[{z = zffWW$[t, g], sl, sr, ss, m},
   m = z["mass"];
   {sl, sr, ss} = (z["SE"][[{1, 2, 3}]] /. {SPD[p, p] -> pp2, Pair[Momentum[p, D], Momentum[p, D]] -> pp2, SPD[p] -> pp2});
   -sl - m^2 D[sl + sr + 2 ss, pp2]];
(* off-diagonal (Denner), the CKM note's self-energy matrices *)
sgWW$[sec_, i_, j_, n_] := Total[sig3WW$[sec][[i, j, All, n]]] /. kRuleWW$ /. toCKWW$ /. gS -> 0;
dZoffWW$[sec_, i_, j_] := Module[{ms = If[sec === "U", upMWW$, dnMWW$], mi, mj, sl, sr, ss},
   mi = ms[[i]]; mj = ms[[j]];
   {sl, sr, ss} = sgWW$[sec, i, j, #] & /@ {1, 2, 3};
   2/(mi^2 - mj^2) (mj^2 sl + mi mj sr + (mi^2 + mj^2) ss) /. kk2 -> mj^2];
hermWW$[x_] := x /. {cK -> cKtmp$, cKc -> cK} /. cKtmp$ -> cKc /. Complex[a_, b_] :> Complex[a, -b];
vMWW$ = Array[cK, {3, 3}]; vMcWW$ = Array[cKc, {3, 3}];
vevWW$ = 2 MW sw/ee; yWW$[m_] := Sqrt[2] m/vevWW$;
kdVdlnmuWW$ = Module[{yu = yWW$ /@ upMWW$, yd = yWW$ /@ dnMWW$, hd, hu, au, ad},
   hd = vMWW$ . DiagonalMatrix[yd^2] . Transpose[vMcWW$]; hu = Transpose[vMcWW$] . DiagonalMatrix[yu^2] . vMWW$;
   au = Table[If[i == k, 0, -3/2 (yu[[i]]^2 + yu[[k]]^2)/(yu[[k]]^2 - yu[[i]]^2) hd[[i, k]]], {i, 3}, {k, 3}];
   ad = Table[If[k == j, 0, -3/2 (yd[[k]]^2 + yd[[j]]^2)/(yd[[j]]^2 - yd[[k]]^2) hu[[k, j]]], {k, 3}, {j, 3}];
   -au . vMWW$ + vMWW$ . ad];

(* ::Section:: *)
(*The renormalized form factors, K units*)

kFWW$[ch_] := Module[{w = wffWW$[ch], fl, dzu, dzd},
   If[ch[[1]] == 1,
    (* W+ -> nu_g l+_g: the neutrino weak, the lepton weak + photonic *)
    fl = w["F"][[1]] - dsigWW$/2 + (1/2) (dZweakLWW$[1, ch[[2]]] /. pp2 -> pp2nu) +
      (1/2) ((dZweakLWW$[2, ch[[2]]] /. pp2 -> lepMWW$[[ch[[2]]]]^2) + kdZgamWW$[-1, lepMWW$[[ch[[2]]]]]) + (-19/12) ee^2/sw^2/ep,
    Module[{i = ch[[2]], j = ch[[3]], diagU, diagD, offU, offD},
     (* only the diagonal entries of the legs of this channel enter: (dZ^{uL+} V)_ij = sum_a conj(dZ_ai) V_aj, (V dZ^{dL})_ij = sum_b V_ib dZ_bj *)
     diagU = Table[If[a == b == i, (dZweakLWW$[3, a] /. pp2 -> upMWW$[[a]]^2) + kdZgamWW$[2/3, upMWW$[[a]]], 0], {a, 3}, {b, 3}];
     diagD = Table[If[a == b == j, (dZweakLWW$[4, a] /. pp2 -> dnMWW$[[a]]^2) + kdZgamWW$[-1/3, dnMWW$[[a]]], 0], {a, 3}, {b, 3}];
     offU = Table[If[a == b, 0, dZoffWW$["U", a, b]], {a, 3}, {b, 3}];
     offD = Table[If[a == b, 0, dZoffWW$["D", a, b]], {a, 3}, {b, 3}];
     fl = w["F"][[1]] - cK[i, j] dsigWW$/2 + (1/2) (Transpose[hermWW$[diagU + offU]] . vMWW$)[[i, j]] +
       (1/2) (vMWW$ . (diagD + offD))[[i, j]] + cK[i, j] (-19/12) ee^2/sw^2/ep + kdVdlnmuWW$[[i, j]]/(2 ep)]];
   {fl, w["F"][[2]], w["F"][[3]], w["F"][[4]]}];

(* ::Section:: *)
(*Born interference and the soft photon*)

FCClearScalarProducts[];
SP[p1, p1] = am^2; SP[p2, p2] = bm^2; SP[p1, p2] = (ss - am^2 - bm^2)/2;
polWW$ = -MT[mu, nu] + (FV[p1, mu] + FV[p2, mu]) (FV[p1, nu] + FV[p2, nu])/ss;
strWW$ = {GA[mu] . GA[7], GA[mu] . GA[6], FV[p1, mu] GA[7], FV[p1, mu] GA[6]};
(* sum over spins and W polarizations of (ubar epsslash P_L v)^* (ubar S_i v) *)
trWW$ = Simplify[Contract[polWW$ DiracTrace[(GS[p2] - bm) . GA[nu] . GA[7] . (GS[p1] + am) . #, DiracTraceEvaluate -> True]]] & /@ strWW$;
FCClearScalarProducts[];
(* the angular integrals in closed form (Integrate, checked numerically): J1 = int dc/(1 - b c), J2 = int dc/(1 - b c)^2 and
   I1, I2 the same with the weight ln(1 - c^2) *)
j1WW$[b_] := Log[(1 + b)/(1 - b)]/b; j2WW$[b_] := 2/(1 - b^2);
i1WW$[b_] := Re[((I Pi + 2 Log[b] - Log[1 - b^2]) Log[-1 + 2/(1 + b)] - PolyLog[2, (1 + b)/(1 - b)] + PolyLog[2, -1 + 2/(1 + b)])/b];
i2WW$[b_] := 4 (ArcTanh[b] - b Log[2])/(-b + b^3);
(* {Sigma0, Sigma1} of the soft photon in the W rest frame: W at rest, f along +z, fbar' along -z, common |p|;
   A = A0 - eps A1;  1/((1 - b1 c)(1 + b2 c)) = [b1/(1 - b1 c) + b2/(1 + b2 c)]/(b1 + b2) *)
softWW$[mw_, m1_, m2_, e1_, e2_] := Module[{p, en1, en2, b1, b2, eW = e1 + e2, aWW, aW1, aW2, a11, a22, a12, f12},
   p = Sqrt[(mw^2 - (m1 + m2)^2) (mw^2 - (m1 - m2)^2)]/(2 mw); en1 = Sqrt[p^2 + m1^2]; en2 = Sqrt[p^2 + m2^2]; b1 = p/en1; b2 = p/en2;
   aWW = {2, 4 Log[2] - 4};
   aW1 = If[e1 == 0, {0, 0}, {j1WW$[b1], i1WW$[b1]}]; aW2 = If[e2 == 0, {0, 0}, {j1WW$[b2], i1WW$[b2]}];
   a11 = If[e1 == 0, {0, 0}, (1 - b1^2) {j2WW$[b1], i2WW$[b1]}]; a22 = If[e2 == 0, {0, 0}, (1 - b2^2) {j2WW$[b2], i2WW$[b2]}];
   f12 = (en1 en2 + p^2)/(en1 en2);
   a12 = If[e1 == 0 || e2 == 0, {0, 0}, f12 (b1 {j1WW$[b1], i1WW$[b1]} + b2 {j1WW$[b2], i1WW$[b2]})/(b1 + b2)];
   N[-eW^2 aWW - e1^2 a11 - e2^2 a22 + 2 eW e1 aW1 + 2 eW e2 aW2 - 2 e1 e2 a12, 50]];

(* ::Section:: *)
(*Package-X*)

pxCacheWW$ = <||>;
pxValWW$[f_, mu_] := Module[{key = {f, mu}, r, y},
   If[KeyExistsQ[pxCacheWW$, key], Return[pxCacheWW$[key]]];
   r = PaXEvaluate[f, PaXC0Expand -> True] /. ConditionalExpression[a_, _] :> a;
   y = Normal[Series[N[r /. ScaleMu -> N[Sqrt[Pi Exp[EulerGamma]] mu, 80] /. EulerGamma -> N[EulerGamma, 80], 80], {Epsilon, 0, 0}]];
   y = {Coefficient[y, Epsilon, -1], Coefficient[Expand[y], Epsilon, 0]};
   pxCacheWW$[key] = y];
(* B0'(s; a, b); at threshold with a massless line (B0'(m^2; 0, m^2)) the infrared pole in dimensional regularization,
   B0' = -(1/(2 m^2)) [1/eps - gamma_E + ln(4 pi mu^2/m^2) + 2] (MS-bar normalization: -(1/(2 m^2)) [1/eps + ln(mu^2/m^2) + 2]) *)
pxDB0WW$[s_, a_, b_, mu_] := Module[{key = {"DB0", s, a, b, mu}, r, y},
   If[KeyExistsQ[pxCacheWW$, key], Return[pxCacheWW$[key]]];
   If[(a === 0 && b === s) || (b === 0 && a === s),
    Return[pxCacheWW$[key] = N[{-1/(2 s), -(Log[mu^2/s] + 2)/(2 s)}, 80]]];
   r = PaXEvaluate[B0[xx$, a, b]] /. ConditionalExpression[a1_, _] :> a1;
   y = Normal[Series[D[r /. ScaleMu -> Sqrt[Pi Exp[EulerGamma]] mu, xx$] /. xx$ -> s, {Epsilon, 0, 0}]];
   y = {Coefficient[y, Epsilon, -1], Coefficient[Expand[y], Epsilon, 0]};
   pxCacheWW$[key] = N[y /. EulerGamma -> N[EulerGamma, 80], 80]];
numericWW$[x_, mu_] := Module[{fs, vals, y},
   fs = Union[Cases[x, A0[__] | B0[__] | C0[__] | DB0[__] | PaVe[__] | Derivative[1, 0, 0][B0][__], Infinity]];
   vals = Function[f, Module[{v = If[MatchQ[f, DB0[__] | Derivative[1, 0, 0][B0][__]], pxDB0WW$[Sequence @@ f, mu], pxValWW$[f, mu]]},
        v[[1]]/ep + v[[2]]]] /@ fs;
   y = x /. Thread[fs -> vals] /. D -> 4 - 2 ep;
   y = Expand[Normal[Series[y, {ep, 0, 0}]]];
   y = {Coefficient[y, ep, -1], Coefficient[y, ep, 0]};
   (* the massless neutrino: the p^0 coefficient at p^2 = pp2nu -> 0; the 1/pp2nu terms cancel analytically and are left as
      numerical noise, which is checked to be small *)
   If[FreeQ[y, pp2nu], N[y, 40],
    Module[{m1},
     y = Chop[y, 10^-30];
     m1 = SeriesCoefficient[#, {pp2nu, 0, -1}] & /@ y;
     If[Max[Abs[N[m1]]] > 10^-9, Print["   WARNING: 1/p^2 left at the neutrino leg: ", N[m1, 3]]];
     N[SeriesCoefficient[#, {pp2nu, 0, 0}] & /@ y, 40]]]];

(* ::Section:: *)
(*Inputs*)

inputsWW$[mu_] := Module[{out = RunProcess[{"python3", "-c",
       "import sys; sys.path.insert(0, '" <> srcDirWW$ <> "'); from nlo_inputs import at; p = at(" <> ToString[CForm[N[mu, 17]]] <>
        "); V = p['V']; print(' '.join('%.17e' % float(x) for x in [p['s2'], p['e']] + list(V.real.ravel()) + list(V.imag.ravel())))"},
      ProcessDirectory -> srcDirWW$]["StandardOutput"], nums},
   nums = ToExpression[StringReplace[#, "e" -> "*^"]] & /@ StringSplit[out];
   <|"s2" -> nums[[1]], "e" -> nums[[2]], "V" -> Partition[nums[[3 ;; 11]], 3] + I Partition[nums[[12 ;; 20]], 3]|>];
(* the pole masses of nlo_inputs.py; u, d, s: the benchmark masses of the CKM note (Eq. (bench)) as regulators of their collinear
   logarithms, which cancel in the inclusive width (and distinct, as the off-diagonal field constants need) *)
massesWW$ = {MW -> 803692/10000, MH -> 12520/100, MT -> 17257/100, MB -> 478/100, MC -> 167/100, MS -> 546/10000, MD -> 271/100000,
   MU -> 127/100000, MTA -> 177693/100000, MMU -> 1056584/10000000, Me -> 510999/1000000000};
chanMassesWW$[ch_, masses_] := If[ch[[1]] == 1, {0, lepMWW$[[ch[[2]]]] /. masses},
   {upMWW$[[ch[[2]]]] /. masses, dnMWW$[[ch[[3]]]] /. masses}];
chanChargesWW$[ch_] := If[ch[[1]] == 1, {0, 1}, {2/3, 1/3}];   (* f and fbar' *)
deltaVWW$[ch_, mu_, xis_, inp_, masses_] := Module[{s2 = Rationalize[inp["s2"], 10^-14], e2, mw = MW /. masses, rules, f1, pole, fin, m1, m2,
    tr, v},
   e2 = Rationalize[inp["e"]^2, 10^-14];
   {m1, m2} = chanMassesWW$[ch, masses];
   rules = Join[{sw -> Sqrt[s2], cw -> Sqrt[1 - s2], ee -> Sqrt[e2]}, xis, masses, {MZ -> Sqrt[mw^2/(1 - s2)]},
     {cK[i_, j_] :> inp["V"][[i, j]], cKc[i_, j_] :> Conjugate[inp["V"][[i, j]]]}];
   f1 = kFWW$[ch] /. rules;
   {pole, fin} = Transpose[numericWW$[#, mu] & /@ f1];
   v = If[ch[[1]] == 1, 1, inp["V"][[ch[[2]], ch[[3]]]]];
   tr = trWW$ /. {am -> m1, bm -> m2, ss -> mw^2};
   {Re[2 Conjugate[v] tr . fin/(Abs[v]^2 tr[[1]])]/KK, Re[2 Conjugate[v] tr . pole/(Abs[v]^2 tr[[1]])]/KK}];

(* ::Section:: *)
(*(a), (b) Gauge independence and the infrared pole at mu = M_W; virtual + soft*)

muWW$ = 803692/10000;
(* "Feynman gauge" as xiZ = xiW = 1 + 1e-10: the reduction of the longitudinal W parts leaves coefficients 1/(xiW - 1) that
   cancel only at xiW = 1 (as in the CKM note, environment notes); 80 digits.  Not 1 + 1e-20: the expansion in p^2 at the
   massless neutrino leg cancels powers of 1/(xiW - 1) and runs out of the 80 digits, and at 1e-20 the lepton channels come out
   wrong by a few per cent of delta_V with no warning from Mathematica (1e-30: Indeterminate); at 1e-10 they agree with
   xi = (2, 3) and with xiW = 1 + 1e-3 *)
xiF$ = 1 + 10^-10;
xiSetsWW$ = {{xiA -> 1, xiZ -> xiF$, xiW -> xiF$}, {xiA -> 1, xiZ -> 2, xiW -> 3}, {xiA -> 1, xiZ -> 1/2, xiW -> 4}};
deltasWW$ = {10^-4, 10^-5, 10^-6, 10^-7, 10^-8};
rowsWW$ = {};
runMuWW$[mu_, xiList_] := Module[{inp = inputsWW$[mu], alpha},
   alpha = inp["e"]^2/(4 Pi);
   Do[Module[{r = deltaVWW$[ch, mu, #, inp, massesWW$] & /@ xiList, m1, m2, e1, e2, sg, emax, mw = MW /. massesWW$},
      {m1, m2} = chanMassesWW$[ch, massesWW$]; {e1, e2} = chanChargesWW$[ch];
      sg = softWW$[mw, m1, m2, e1, e2];
      emax = (mw^2 - (m1 + m2)^2)/(2 mw);
      Print["   ", wffWW$[ch]["name"], ", mu = ", N[mu, 6], ": delta_V (finite) ", NumberForm[#, 12] & /@ r[[All, 1]],
       ";  spread ", ScientificForm[N[Max[r[[All, 1]]] - Min[r[[All, 1]]]], 2], ";  pole + soft pole (expect 0): ",
       ScientificForm[N[r[[1, 2]] + alpha/Pi (-sg[[1]]/4)], 3]];
      If[Max[r[[All, 1]]] - Min[r[[All, 1]]] > 10^-9, Print["   WARNING: delta_V depends on the gauge"]];
      Do[Module[{ks = -(sg[[1]] Log[mu^2/(dl emax)^2] - sg[[2]])/4},
        AppendTo[rowsWW$, {wffWW$[ch]["name"], N[mu], N[dl], ToString[CForm[N[r[[1, 1]] + alpha/Pi ks, 20]]],
          ToString[CForm[N[alpha/Pi, 20]]]}]], {dl, deltasWW$}]], {ch, chansWW$}]];
runMuWW$[muWW$, xiSetsWW$];
tick$["(a), (b) mu = M_W"];
(* (c) mu = M_W/2, 2 M_W, Feynman gauge *)
runMuWW$[muWW$/2, xiSetsWW$[[{1}]]];
runMuWW$[2 muWW$, xiSetsWW$[[{1}]]];
Export[FileNameJoin[{resDirWW$, "wweak_vs.csv"}], Prepend[rowsWW$, {"channel", "mu", "delta", "deltaV_plus_soft", "alpha_over_pi"}], "CSV"];
tick$["(c); written results/wweak_vs.csv"];

(* ::Section:: *)
(*(d) The virtual alone at the CKM note's MadLoop point (MadLoop's normalization)*)

pointMassesWW$ = {MW -> 80, MH -> 125, MT -> 165, MB -> 286/100, MC -> 619/1000, MS -> 546/10000, MD -> 271/10000, MU -> 127/10000,
   MTA -> 1746/1000, MMU -> 1027/10000, Me -> 487/1000000};
ckmStdWW$[s12_, s23_, s13_, dl_] := Module[{c12 = Sqrt[1 - s12^2], c23 = Sqrt[1 - s23^2], c13 = Sqrt[1 - s13^2], e = Exp[I dl]},
   N[{{c12 c13, s12 c13, s13/e}, {-s12 c23 - c12 s23 s13 e, c12 c23 - s12 s23 s13 e, s23 c13},
     {s12 s23 - c12 c23 s13 e, -c12 s23 - s12 c23 s13 e, c23 c13}}]];
inpPointWW$ = <|"s2" -> 1 - 80^2/91^2, "e" -> Sqrt[4 Pi/128], "V" -> ckmStdWW$[0.22501, 0.04183, 0.003732, 1.147]|>;
mlRowsWW$ = {};
(* the S-matrix element does not depend on the gauge: (xiZ, xiW) = (2, 3) and (1/2, 4) (the 1 + 1e-10 of the Feynman gauge would need
   the CKM matrix of this point to more than double precision) *)
Do[Module[{r = deltaVWW$[ch, muR, xiSetsWW$[[2]], inpPointWW$, pointMassesWW$], r3 = deltaVWW$[ch, muR, xiSetsWW$[[3]], inpPointWW$, pointMassesWW$]},
    Print["(d) MadLoop point, ", wffWW$[ch]["name"], ", mu_R = ", muR, ": virtual pole ", NumberForm[r[[2]], 12], ", finite ",
     NumberForm[r[[1]], 12], ";  the other gauge minus this one: ", ScientificForm[N[r3[[1]] - r[[1]]], 2]];
    AppendTo[mlRowsWW$, {wffWW$[ch]["name"], muR, ToString[CForm[N[r[[2]], 20]]], ToString[CForm[N[r[[1]], 20]]]}]],
  {ch, {{1, 3}, {3, 2, 3}, {3, 1, 1}}}, {muR, {91, 500}}];
Export[FileNameJoin[{resDirWW$, "wweak_ml.csv"}], Prepend[mlRowsWW$, {"channel", "mu_R", "pole", "finite"}], "CSV"];
tick$["(d); written results/wweak_ml.csv"];
