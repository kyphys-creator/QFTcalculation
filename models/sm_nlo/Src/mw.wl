(* ::Package:: *)

(* ::Title:: *)
(*Step (6) of the NLO note: Delta rho from the self-energies and the prediction of M_W from alpha(0), G_F, M_Z*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (6).  The SM note's gauge-boson self-energies (models/sm/Src/results/oneloop_sigma.m:*)
(*Sigma_T^WW, Sigma_T^ZZ in general R_xi with all fermion masses, the 1PI part and the tadpole-attached part; K units):*)
(*  (a) the tadpole parts drop out of Sigma^WW/M_W^2 - Sigma^ZZ/M_Z^2 (symbolic, every k^2);*)
(*  (b) Delta rho = Sigma^ZZ_T(0)/M_Z^2 - Sigma^WW_T(0)/M_W^2 of the top-bottom doublet (the loop functions with m_t, m_b only)*)
(*      against N_c g^2/(4 M_W^2 K) F0(m_t^2, m_b^2), F0(a, b) = a + b - 2 a b/(a - b) ln(a/b)  (-> Eq. (drho) as m_b -> 0):*)
(*      no UV pole, no mu, no gauge parameter; the whole Delta rho (all loops) at mu = M_Z has a UV pole and depends on the gauge;*)
(*  (c) M_W from the couplings of the SM note's alpha scheme (inputs alpha(0), Delta alpha, G_F, M_Z, ...; nlo_inputs.at(mu,*)
(*      "PDG2024_alpha_scheme")), as in that note's fit (models/sm/Src/msbar_fit.wl, fitAlpha$), linear in the tadpole-free*)
(*      combination:  M_W = M_Z c-hat(mu) (1 + (dZ - dW)/2),  dV = Re Sigma_T^VV(M_V^2)/M_V^2 (MS-bar, the 1PI parts suffice by (a)),*)
(*      the loops at the tree-level point of that fit (e = 2 M_W s0/v_G, s0^2 = 1 - M_W^2/M_Z^2, the running masses of the light*)
(*      fermions near M_t), M_W iterated to a fixed point; M_Z the pole mass of the SM note (from the Breit-Wigner 91.1880 GeV).*)
(*      Checks: (xiZ, xiW) = (2, 2), (3, 3), (1/2, 4) (xiA = 1, the photon mass to 0 coefficient by coefficient); mu = M_Z/2,*)
(*      M_Z, M_t, 2 M_t with c-hat(mu) run with the one-loop RGE of nlo_inputs.py; at mu = M_t against the SM note's 80.38171 GeV.*)
(*Package-X for the loop functions (MS-bar), 40 digits.  Writes results/drho.csv and results/mw.csv.*)
(*Batch:  wolframscript -file mw.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
$MaxExtraPrecision = 200;
srcDirMW$ = DirectoryName[$InputFileName];
resDirMW$ = FileNameJoin[{srcDirMW$, "results"}];
t0MW$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0MW$], " s] ", s];
KK = 16 Pi^2;
sigMW$ = Association[Get[FileNameJoin[{srcDirMW$, "..", "..", "sm", "Src", "results", "oneloop_sigma.m"}]]];
kRuleMW$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
{wwPI$, wwTad$} = sigMW$["WW"] /. kRuleMW$;
{zzPI$, zzTad$} = sigMW$["ZZ"] /. kRuleMW$;
toSwMW$[x_] := x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2];

(* ::Section:: *)
(*(a) The tadpole parts*)

Print["(a) tadpole parts: Sigma^WW_tad/M_W^2 - Sigma^ZZ_tad/M_Z^2 (expect 0): ", Simplify[toSwMW$[wwTad$/MW^2 - zzTad$/MZ^2]],
  ";  they depend on k^2: ", ! FreeQ[{wwTad$, zzTad$}, kk2]];

(* ::Section:: *)
(*Package-X*)

pxCacheMW$ = <||>;
pxValMW$[f_, mu_] := Module[{key = {f, mu}, r, y},
   If[KeyExistsQ[pxCacheMW$, key], Return[pxCacheMW$[key]]];
   r = PaXEvaluate[f, PaXC0Expand -> True] /. ConditionalExpression[a_, _] :> a;
   y = Normal[Series[N[r /. ScaleMu -> N[Sqrt[Pi Exp[EulerGamma]] mu, 60] /. EulerGamma -> N[EulerGamma, 60], 60], {Epsilon, 0, 0}]];
   pxCacheMW$[key] = {Coefficient[y, Epsilon, -1], Coefficient[Expand[y], Epsilon, 0]}];
(* {1/eps coefficient, MS-bar finite part} of an expression in A0, B0, PaVe and D *)
numericMW$[x_, mu_] := Module[{fs, vals, y},
   fs = Union[Cases[x, A0[__] | B0[__] | PaVe[__], Infinity]];
   vals = (#[[1]]/ep + #[[2]]) & /@ (pxValMW$[#, mu] & /@ fs);
   y = Expand[Normal[Series[x /. Thread[fs -> vals] /. D -> 4 - 2 ep, {ep, 0, 0}]]];
   N[{Coefficient[y, ep, -1], Coefficient[y, ep, 0]}, 40]];

(* ::Section:: *)
(*(b) Delta rho*)

(* the part of an expression whose loop functions have only m_t, m_b *)
tbMW$[x_] := Module[{y = Expand[x], fs, tb},
   fs = Union[Cases[y, A0[__] | B0[__] | PaVe[__], Infinity]];
   tb = Select[fs, FreeQ[#, MW | MZ | MH | MA | MC | MD | MS | MU | Me | MMU | MTA] && ! FreeQ[#, MT | MB] &];
   y = Collect[y, fs];
   Total[Coefficient[y, #] # & /@ tb]];
(* k^2 -> 0: the transverse projection leaves 1/k^2 terms that cancel only between the loop functions, so k^2 = 1e-12 GeV^2
   (60 digits; the error is of order k^2/m^2) *)
kk0MW$ = 10^-12;
drhoTbK$ = toSwMW$[tbMW$[zzPI$]/MZ^2 - tbMW$[wwPI$]/MW^2] /. kk2 -> kk0MW$;
f0MW$[a_, b_] := a + b - 2 a b/(a - b) Log[a/b];
drhoTbFormulaK$[mt_, mb_, e_, s_, mw_] := 3 e^2/(4 s^2 mw^2) f0MW$[mt^2, mb^2];
drhoRows$ = {};
Do[Module[{num = {MT -> pt[[1]], MB -> pt[[2]], ee -> 31/100, sw -> 48/100, MW -> 80}, v, f},
   v = Table[numericMW$[drhoTbK$ /. num, mu], {mu, {50, 300}}];
   f = N[drhoTbFormulaK$[pt[[1]], pt[[2]], 31/100, 48/100, 80], 30];
   Print["(b) K Delta rho of t, b at (m_t, m_b) = ", N[pt], ": pole ", ScientificForm[v[[1, 1]], 2], ", finite at mu = 50, 300 GeV ",
    NumberForm[v[[All, 2]], 15], ";  the formula ", NumberForm[f, 15], ";  minus the formula ", ScientificForm[v[[1, 2]] - f, 2]];
   AppendTo[drhoRows$, {N[pt[[1]]], N[pt[[2]]], ToString[CForm[N[v[[1, 2]], 20]]], ToString[CForm[N[f, 20]]]}]],
  {pt, {{17257/100, 478/100}, {17257/100, 1/1000}, {100, 50}}}];
Print["    gauge parameters in the t, b part: ", Union[Cases[drhoTbK$, xiA | xiZ | xiW, Infinity]]];
(* the whole Delta rho (1PI; the tadpoles drop out) at mu = M_Z, three gauges, a physical point *)
lightMW$ = With[{c = 246.21965/Sqrt[2]}, {MB -> 0.015480097 c, MC -> 0.0033820038 c, MS -> 0.00029094484 c,
    MD -> 1.4609792*^-5 c, MU -> 6.7227779*^-6 c, MTA -> 0.0099944422 c, MMU -> 0.00058837986 c, Me -> 2.7929820*^-6 c}];
lightRatMW$ = lightMW$ /. (m_ -> x_) :> (m -> Rationalize[x, 0]);
(* the photon: xiA = 1, then MA -> 0 coefficient by coefficient of the loop functions (as wsig_feyncalc.wl) *)
limitMAMW$[x_] := Module[{y = x /. xiA -> 1, fs, cs, c0},
   fs = Union[Cases[y, A0[__] | B0[__] | PaVe[__], Infinity]];
   y = Expand[y /. Thread[fs -> Array[lf$, Length[fs]]]];
   cs = Together[Coefficient[y, lf$[#]]] & /@ Range[Length[fs]];
   c0 = Together[y /. lf$[_] -> 0];
   If[! FreeQ[Denominator /@ Append[cs, c0], MA], Print["   WARNING: 1/MA left after xiA = 1"]];
   (Append[cs, c0] /. MA -> 0) . Append[fs /. MA -> 0, 1] /. {A0[0] -> 0, B0[0, 0, 0] -> 0}];
wwPI0$ = limitMAMW$[toSwMW$[wwPI$]]; zzPI0$ = limitMAMW$[toSwMW$[zzPI$]];
tick$["(b) symbolic parts"];
xiSetsMW$ = {{xiZ -> 2, xiW -> 2}, {xiZ -> 3, xiW -> 3}, {xiZ -> 1/2, xiW -> 4}};
ptMW$ = Join[{MT -> 17257/100, MH -> 12520/100, MW -> 803692/10000, ee -> 31/100, sw -> Rationalize[N[Sqrt[1 - (803692/10000)^2/(911876/10000)^2], 40], 10^-35]}, lightRatMW$];
Do[Module[{x = (zzPI0$/MZ^2 - wwPI0$/MW^2) /. kk2 -> kk0MW$ /. MZ -> MW/Sqrt[1 - sw^2] /. ptMW$ /. xs, v},
   v = numericMW$[x, 911876/10000]/KK;
   Print["    the whole Delta rho at mu = M_Z, ", xs, ": pole ", NumberForm[v[[1]], 8], ", finite ", NumberForm[v[[2]], 10],
    ";  the t, b part ", NumberForm[N[drhoTbFormulaK$[17257/100, MB /. lightMW$, 31/100, sw /. ptMW$, 803692/10000]/KK], 10]];
   AppendTo[drhoRows$, {"all, " <> ToString[xs], "", ToString[CForm[N[v[[2]], 20]]], ToString[CForm[N[v[[1]], 20]]]}]], {xs, xiSetsMW$}];
Export[FileNameJoin[{resDirMW$, "drho.csv"}], Prepend[drhoRows$, {"m_t_or_case", "m_b", "K_drho_or_finite", "formula_or_pole"}], "CSV"];
tick$["(b)"];

(* ::Section:: *)
(*(c) M_W from the alpha scheme*)

GF$ = 11663788/10^12;
vG$ = 1/Sqrt[Sqrt[2] GF$];
(* the SM note's M_Z pole from the Breit-Wigner mass (rationalized for Package-X) *)
mzPole$ = Rationalize[N[91188/1000/Sqrt[1 + (24955/10000)^2/(91188/1000)^2], 40], 10^-35];
c2At$[mu_] := Module[{out = RunProcess[{"python3", "-c",
       "import sys; sys.path.insert(0, '" <> srcDirMW$ <> "'); from nlo_inputs import at; p = at(" <> ToString[CForm[N[mu, 17]]] <>
        ", 'PDG2024_alpha_scheme'); print('%.17e' % (1 - p['s2']))"}, ProcessDirectory -> srcDirMW$]["StandardOutput"]},
   Rationalize[ToExpression[StringReplace[StringTrim[out], "e" -> "*^"]], 0]];
dVdiffMW$[mw_, mu_, xs_] := Module[{s0 = Sqrt[1 - mw^2/mzPole$^2], rules, dW, dZ},
   rules = Join[{ee -> Rationalize[N[2 mw s0/vG$, 40], 10^-35], sw -> Rationalize[N[s0, 40], 10^-35], MW -> mw, MT -> 17257/100, MH -> 12520/100},
     lightRatMW$, xs];
   dW = numericMW$[wwPI0$ /. kk2 -> mw^2 /. MZ -> MW/Sqrt[1 - sw^2] /. rules, mu];
   dZ = numericMW$[zzPI0$ /. kk2 -> mzPole$^2 /. MZ -> MW/Sqrt[1 - sw^2] /. rules, mu];
   {Re[dZ[[2]]/mzPole$^2 - dW[[2]]/mw^2]/KK, Abs[dZ[[1]]/mzPole$^2 - dW[[1]]/mw^2]/KK}];
mwPredMW$[mu_, xs_] := Module[{c2 = c2At$[mu], mw = 8035/100, mwP, d, it},
   Do[d = dVdiffMW$[Rationalize[mw, 10^-30], mu, xs]; mwP = N[mzPole$ Sqrt[c2] (1 + d[[1]]/2), 30];
    If[Abs[mwP - mw] < 10^-12, Break[]]; mw = mwP, {it, 12}];
   {mwP, d[[1]], d[[2]], N[c2, 17]}];
mwRows$ = {};
(* at mu = M_t: three gauges; then the mu dependence in the first *)
Do[Module[{r = mwPredMW$[17257/100, xs]},
   Print["(c) mu = M_t, ", xs, ": M_W pole ", NumberForm[r[[1]], 12], " GeV;  dZ - dW ", NumberForm[r[[2]], 10], ";  UV pole of dZ - dW (in the 1/eps",
    " of the K units, the MS-bar counterterm of c-hat removes it) ", ScientificForm[r[[3]], 3]];
   AppendTo[mwRows$, {N[17257/100], ToString[xs], ToString[CForm[r[[1]]]], ToString[CForm[r[[2]]]], ToString[CForm[r[[4]]]]}]], {xs, xiSetsMW$}];
tick$["(c) gauges"];
Do[Module[{r = mwPredMW$[mu, xiSetsMW$[[1]]]},
   Print["(c) mu = ", N[mu, 6], ": c-hat^2 ", NumberForm[r[[4]], 10], ";  M_W pole ", NumberForm[r[[1]], 12], " GeV"];
   AppendTo[mwRows$, {N[mu], ToString[xiSetsMW$[[1]]], ToString[CForm[r[[1]]]], ToString[CForm[r[[2]]]], ToString[CForm[r[[4]]]]}]],
  {mu, {mzPole$/2, mzPole$, 2 17257/100}}];
Export[FileNameJoin[{resDirMW$, "mw.csv"}], Prepend[mwRows$, {"mu", "gauge", "MW_pole", "dZ_minus_dW", "c2hat"}], "CSV"];
tick$["(c); written results/drho.csv, results/mw.csv"];
