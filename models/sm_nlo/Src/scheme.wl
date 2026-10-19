(* ::Package:: *)

(* ::Title:: *)
(*Step (7) of the NLO note: the MS-bar couplings against the on-shell G_mu scheme at one loop*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (7).  The SM note's one-loop relations of its M_W scheme (models/sm/Src/msbar_fit.wl):*)
(*  g(mu)^2 = g0^2 (1 + dW - DeltaHat),  g(mu)^2 + g'(mu)^2 = G0^2 (1 + dZ - DeltaHat),  c-hat^2 = c0^2 (1 + dW - dZ),*)
(*  g0^2 = 4 sqrt2 G_F M_W^2, G0^2 = 4 sqrt2 G_F M_Z^2, c0^2 = M_W^2/M_Z^2  (the tree couplings of the on-shell G_mu scheme),*)
(*  dV = Re Sigma_T^VV(M_V^2)/M_V^2 with the tadpole parts (FJ), DeltaHat the muon decay of the SM note (mudecay_deltahat_finite.m;*)
(*  its tadpole parts cancel against those of dV in these combinations).  This script evaluates C_W = dW - DeltaHat,*)
(*  C_Z = dZ - DeltaHat and dW - dZ at the tree-level point of that fit (the pole M_W, M_Z of the SM note, e = g0 s0, the running*)
(*  light masses near M_t) at the mu of steps (4a)-(4c): (a) in three gauges (the pole masses, the MS-bar couplings and G_F do not*)
(*  depend on the gauge), (b) at mu = M/2, M, 2M of the Z, the W and the top.  scheme_compare.py uses them for the widths.*)
(*Package-X for the loop functions (MS-bar), 40 digits.  Writes results/scheme.csv.  Batch:  wolframscript -file scheme.wl*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
$MaxExtraPrecision = 200;
srcDirSC$ = DirectoryName[$InputFileName];
resDirSC$ = FileNameJoin[{srcDirSC$, "results"}];
t0SC$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0SC$], " s] ", s];
KK = 16 Pi^2;
sigMW$ = Association[Get[FileNameJoin[{srcDirSC$, "..", "..", "sm", "Src", "results", "oneloop_sigma.m"}]]];
kRuleMW$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
{wwPI$, wwTad$} = sigMW$["WW"] /. kRuleMW$;
{zzPI$, zzTad$} = sigMW$["ZZ"] /. kRuleMW$;
toSwMW$[x_] := x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2];

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


sigSC$ = Association[Get[FileNameJoin[{srcDirSC$, "..", "..", "sm", "Src", "results", "oneloop_sigma.m"}]]];
kRuleSC$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
toSwSC$[x_] := x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2];
dHatK$ = Get[FileNameJoin[{srcDirSC$, "..", "..", "sm", "Src", "results", "mudecay_deltahat_finite.m"}]];   (* K DeltaHat, MS-bar *)
Print["DeltaHat: gauge parameters ", Union[Cases[dHatK$, xiA | xiZ | xiW, Infinity]], ";  parameters ", Variables[dHatK$ /. Log[_] -> 1]];

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

(* the 1PI and the tadpole parts together (the tadpoles cancel against those of DeltaHat) *)
wwSC$ = limitMAMW$[toSwSC$[Total[sigSC$["WW"]] /. kRuleSC$]];
zzSC$ = limitMAMW$[toSwSC$[Total[sigSC$["ZZ"]] /. kRuleSC$]];
tick$["self-energies"];

(* the tree-level point of the SM note's M_W-scheme fit: the pole masses from the Breit-Wigner masses (Gamma_W = 2.085,
   Gamma_Z = 2.4955 GeV), e = g0 s0 with g0 = 2 M_W/v_G *)
GFSC$ = 11663788/10^12; vGSC$ = 1/Sqrt[Sqrt[2] GFSC$];
ratSC$[x_] := Rationalize[N[x, 40], 10^-35];
mwSC$ = ratSC$[803692/10000/Sqrt[1 + (2085/1000)^2/(803692/10000)^2]];
mzSC$ = ratSC$[91188/1000/Sqrt[1 + (24955/10000)^2/(91188/1000)^2]];
s0SC$ = ratSC$[Sqrt[1 - mwSC$^2/mzSC$^2]];
treeSC$ = Join[{ee -> ratSC$[2 mwSC$ s0SC$/vGSC$], sw -> s0SC$, MW -> mwSC$, MT -> 17257/100, MH -> 12520/100}, lightRatMW$];
Print["tree point: M_W ", N[mwSC$, 10], ", M_Z ", N[mzSC$, 10], ", s0^2 ", N[s0SC$^2, 10], ", e ", N[ee /. treeSC$, 10]];
(* the scale as muv: the symbol mu stands in DeltaHat *)
convSC$[muv_, xs_] := Module[{dW, dZ, dh},
   dW = numericMW$[wwSC$ /. kk2 -> mwSC$^2 /. MZ -> MW/Sqrt[1 - sw^2] /. treeSC$ /. xs, muv];
   dZ = numericMW$[zzSC$ /. kk2 -> mzSC$^2 /. MZ -> MW/Sqrt[1 - sw^2] /. treeSC$ /. xs, muv];
   dh = N[dHatK$ /. treeSC$ /. mu -> muv, 40];
   {Re[dW[[2]]]/mwSC$^2/KK, Re[dZ[[2]]]/mzSC$^2/KK, Re[dh]/KK}];
xiSetsSC$ = {{xiZ -> 2, xiW -> 2}, {xiZ -> 3, xiW -> 3}, {xiZ -> 1/2, xiW -> 4}};
rowsSC$ = {};
(* (a) three gauges at mu = M_Z *)
Do[Module[{c = convSC$[911876/10000, xs]},
   Print["(a) mu = M_Z, ", xs, ": dW ", NumberForm[c[[1]], 10], ", dZ ", NumberForm[c[[2]], 10], ", DeltaHat ", NumberForm[c[[3]], 10],
    ";  dW - DeltaHat ", NumberForm[c[[1]] - c[[3]], 12], ", dZ - DeltaHat ", NumberForm[c[[2]] - c[[3]], 12], ", dW - dZ ", NumberForm[c[[1]] - c[[2]], 12]];
   AppendTo[rowsSC$, {N[911876/10000], ToString[xs], ToString[CForm[c[[1]] - c[[3]]]], ToString[CForm[c[[2]] - c[[3]]]], ToString[CForm[c[[1]] - c[[2]]]]}]],
  {xs, xiSetsSC$}];
tick$["(a)"];
(* (b) the mu of steps (4a)-(4c) *)
Do[Module[{c = convSC$[muv, xiSetsSC$[[1]]]},
   Print["(b) mu = ", N[muv, 7], ": dW - DeltaHat ", NumberForm[c[[1]] - c[[3]], 10], ", dZ - DeltaHat ", NumberForm[c[[2]] - c[[3]], 10],
    ", dW - dZ ", NumberForm[c[[1]] - c[[2]], 10]];
   AppendTo[rowsSC$, {N[muv], ToString[xiSetsSC$[[1]]], ToString[CForm[c[[1]] - c[[3]]]], ToString[CForm[c[[2]] - c[[3]]]], ToString[CForm[c[[1]] - c[[2]]]]}]],
  {muv, {911876/20000, 911876/10000, 911876/5000, 803692/20000, 803692/10000, 803692/5000, 17257/200, 17257/100, 17257/50}}];
Export[FileNameJoin[{resDirSC$, "scheme.csv"}], Prepend[rowsSC$, {"mu", "gauge", "dW_minus_dHat", "dZ_minus_dHat", "dW_minus_dZ"}], "CSV"];
tick$["(b); written results/scheme.csv"];
