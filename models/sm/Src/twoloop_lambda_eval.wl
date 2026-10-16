(* ::Package:: *)

(* ::Title:: *)
(*Step (8'): Z_lambda and the two-loop beta function of lambda from the note's model (symmetric, gaugeless, auxiliary mass)*)


(* ::Text:: *)
(*Reads results/twoloop_lambda_reduction.m (twoloop_lambda_feyncalc.wl), the masters (twoloop_lambda_masters.wl, AMFlow) and the*)
(*Z factors of the two-point functions and of yt, gS (twoloop_sym_eval.wl).  J per loop includes E^(eps EulerGamma); M = mu = 1.*)
(*  auxiliary scalar mass counterterm: Z_Phi M0^2 - Sigma_H(0) finite  ->  dM2 = pole[Sigma_H(0)] - z_Phi^(1);*)
(*  the auxiliary mass sits only in the quark denominators, so the quark kinetic counterterm on a line is not cancelled by the*)
(*  bare fields: S_M (i dZ lslash) S_M = -dZ S_M (1 + M^2/(l^2 - M^2)) = -dZ (1 + M^2 d/dM^2) S_M; the extra*)
(*  -zbar_t Mf^2 dG4^(1)/dMf^2 with zbar_t = (z_tL + z_tR)/2 (the gamma5 parts of the traces vanish) is added;*)
(*  G4 = Gamma_HHHH/(-6 i) = la0 + G4^(1)(la0, yt0, gS0, Ms0^2)/K + G4^(2)/K^2,  Z_Phi^2 G4 finite  ->  la0 = la + dla;*)
(*  beta_la = (sum_l rho_l x_l d/dx_l - 2) a_la^(1) (rho = 1 for yt, gS; 2 for la); double poles checked.*)
(*Compared with the SM two-loop RGE of lambda (Buttazzo et al., appendix B; Machacek-Vaughn / Luo-Wang-Xiao) at g = g' = 0, yb = ytau = 0.*)
(*Batch: wolframscript -file twoloop_lambda_eval.wl*)


srcDir$ = DirectoryName[$InputFileName];
red$ = Get[FileNameJoin[{srcDir$, "results", "twoloop_lambda_reduction.m"}]];
mas$ = Get[FileNameJoin[{srcDir$, "results", "twoloop_lambda_masters.m"}]];
zs$ = Get[FileNameJoin[{srcDir$, "results", "twoloop_sym_z.m"}]];
ep = Epsilon;
Print["diagrams: Sigma_H (one loop) ", red$["ndiag"][[1]], ", HHHH one loop ", red$["ndiag"][[2]], ", two loops ", red$["ndiag"][[3]]];
ser$[x_, n_] := Normal[Series[x, {ep, 0, n}]];
pole$[x_] := Module[{s = ser$[x, 0]}, Expand[Coefficient[s, ep, -2]/ep^2 + Coefficient[s, ep, -1]/ep]];
res$[x_, n_] := Expand[Coefficient[Expand[x], ep, -n]];

(* masters in the J normalization (E^(2 eps EulerGamma)); the sunset from AMFlow (30 digits), rationalized pole parts checked *)
sun$ = Normal[Series[E^(2 ep EulerGamma) mas$["sunset"], {ep, 0, 2}]];
Print["(a) sunset (J normalization): ", N[sun$, 12], ";  pole part - (3/(2 eps^2) + 9/(2 eps)) = ",
  N[Coefficient[sun$, ep, -2] - 3/2, 5], ", ", N[Coefficient[sun$, ep, -1] - 9/2, 5]];
mastersV$ = {GLI["v2", {1, 1, 1}] -> sun$, GLI["v2", {1, 1, 0}] -> E^(2 ep EulerGamma) Gamma[-1 + ep]^2};
G42$ = red$["G42"] /. mastersV$ /. D -> 4 - 2 ep;
G41$ = E^(ep EulerGamma) red$["G41"] /. D -> 4 - 2 ep;
sig$ = E^(ep EulerGamma) red$["sigH0"] /. D -> 4 - 2 ep;
z1P$ = zs$["z1"]["H"]; z2P$ = zs$["z2"]["H"]; dy1$ = zs$["dy1"]; dg1$ = zs$["dg1"];
zq$ = (zs$["z1"]["t_L"] + zs$["z1"]["t_R"])/2;

(* the auxiliary scalar mass counterterm (M^2 = 1) *)
dM2$ = Expand[pole$[sig$ /. {Ms -> 1, Mf -> 1}] - z1P$];
Print["(a) K Sigma_H(0) pole = ", pole$[sig$ /. {Ms -> 1, Mf -> 1}], ";  auxiliary K dM^2 = ", dM2$];
(* one loop *)
g41$ = G41$ /. {Ms -> 1, Mf -> 1};
dla1$ = -pole$[g41$ + 2 z1P$ la];
Print["(b) one loop: K dla = ", Expand[ep dla1$], "/eps"];
(* two loops *)
ctQ$ = Expand[-zq$ (mf2 D[G41$ /. Mf -> Sqrt[mf2], mf2] /. mf2 -> Mf^2) /. {Ms -> 1, Mf -> 1}];
Print["(b) quark kinetic counterterm on the regulated lines: -zbar_t Mf^2 dG4^(1)/dMf^2 = ", Expand[ser$[ctQ$, -1]], " + O(eps^0)"];
ct$ = Expand[(dla1$ D[G41$, la] + dy1$ yt D[G41$, yt] + dg1$ gS D[G41$, gS] + dM2$ D[G41$ /. Ms -> Sqrt[ms2], ms2] /. ms2 -> Ms^2)
     /. {Ms -> 1, Mf -> 1}] + ctQ$;
dla2$ = -pole$[G42$ + ct$ + 2 z1P$ (dla1$ + g41$) + (2 z2P$ + z1P$^2) la];
(* the residues are numbers from the AMFlow sunset: rationalize them (30 digits) *)
ratz$[x_] := Expand[x /. r_Real :> Rationalize[r, 10^-20]];
dla2$ = ratz$[dla2$];
aL1$ = res$[dla1$, 1] h + res$[dla2$, 1] h^2; aL2$ = res$[dla2$, 2] h^2;
Dop$[x_, rho_] := Expand[yt D[x, yt] + gS D[x, gS] + 2 la D[x, la] - rho x];
betaL$ = Dop$[aL1$, 2];
Print["(c) K beta_la (one loop) = ", Expand[Coefficient[betaL$, h, 1]], ";  K^2 beta_la (two loops) = ", Expand[Coefficient[betaL$, h, 2]]];
(* double poles: needs the one-loop beta functions of yt and gS *)
b1$ = {Coefficient[betaL$, h, 1] h, yt (9/2 yt^2 - 8 gS^2) h, -7 gS^3 h};
dbl$ = Expand[Coefficient[Dop$[aL2$, 2] - (b1$[[1]] D[aL1$, la] + b1$[[2]] D[aL1$, yt] + b1$[[3]] D[aL1$, gS]), h, 2]];
Print["(c) double-pole consistency (expect 0): ", dbl$];
litL1$ = 24 la^2 + 12 la yt^2 - 6 yt^4;
litL2$ = 2 (la^2 (-156 la - 72 yt^2) + la yt^2 (-3/2 yt^2 + 40 gS^2) + yt^4 (15 yt^2 - 16 gS^2));
Print["(d) K beta_la^(1) - literature = ", Expand[Coefficient[betaL$, h, 1] - litL1$], ";  K^2 beta_la^(2) - literature = ",
  Expand[Coefficient[betaL$, h, 2] - litL2$], "   (expect 0, 0)"];
Export[FileNameJoin[{srcDir$, "results", "twoloop_lambda_beta.csv"}],
  {{"quantity", "expression"}, {"K_beta_la_one_loop", ToString[InputForm[Expand[Coefficient[betaL$, h, 1]]]]},
   {"K2_beta_la_two_loop", ToString[InputForm[Expand[Coefficient[betaL$, h, 2]]]]},
   {"K2_beta_la_minus_literature", ToString[InputForm[Expand[Coefficient[betaL$, h, 2] - litL2$]]]},
   {"double_pole_check", ToString[InputForm[dbl$]]}}, "CSV"];
