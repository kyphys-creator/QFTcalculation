(* ::Package:: *)

(* ::Title:: *)
(*Step (8'): Z factors and two-loop beta functions of yt and gS from the note's model (symmetric, gaugeless, Landau gauge)*)


(* ::Text:: *)
(*Reads results/twoloop_sym_reduction.m (twoloop_sym_feyncalc.wl).  At -q^2 = mu^2 (all logarithms 0), J per loop includes*)
(*E^(eps EulerGamma) (QCD note, step (7)):  bubble^2 = E^(2 eps EulerGamma) G(1,1)^2,  sunset = -E^(2 eps EulerGamma) G(1,1) G(eps,1).*)
(*Bare couplings yt0 = Z_yt yt, gS0 = Z_g gS, la0 = la (lambda enters first at two loops); h = 1/K counts loops.*)
(*Finiteness (MS-bar, pure poles):  Z_X (1 + Pi_X) for X = Phi (H), t_L, t_R, b_L, ghost;  Z_3 (1 - Pi_A);*)
(*  Z_yt Z_Phi^(1/2) Z_tL^(1/2) Z_tR^(1/2) (1 + Lambda);  Z_g = 1/(Z~_3 Z_3^(1/2)) (Landau gauge, Z~_1 = 1).*)
(*beta_x = (sum_l rho_l x_l d/dx_l - rho_x) a_x^(1) with a_x^(1) the 1/eps residue of x Z_x (rho = 1 for yt, gS; 2 for la);*)
(*the double poles are checked against (sum_l rho_l x_l d/dx_l - rho_x) a_x^(2) = beta_l d a_x^(1)/dx_l.*)
(*Compared with the SM two-loop RGEs (Buttazzo et al., appendix B; also Machacek-Vaughn / Luo-Wang-Xiao) in the same limit.*)
(*Writes results/twoloop_sym_beta.csv.  Batch: wolframscript -file twoloop_sym_eval.wl*)


srcDir$ = DirectoryName[$InputFileName];
red$ = Get[FileNameJoin[{srcDir$, "results", "twoloop_sym_reduction.m"}]];
ep = Epsilon;
g$[a_, b_] := Gamma[a + b - D/2] Gamma[D/2 - a] Gamma[D/2 - b]/(Gamma[a] Gamma[b] Gamma[D - a - b]);
masters$ = {GLI["k2", {1, 1, 1, 1, 0}] -> E^(2 ep EulerGamma) g$[1, 1]^2,
   GLI["k2", {1, 0, 0, 1, 1}] -> -E^(2 ep EulerGamma) g$[1, 1] g$[ep, 1]} /. D -> 4 - 2 ep;
P1$ = Association[KeyValueMap[#1 -> (E^(ep EulerGamma) #2 /. D -> 4 - 2 ep) &, red$["one"]]];
P2$ = Association[KeyValueMap[#1 -> (#2 /. masters$ /. D -> 4 - 2 ep) &, red$["two"]]];
Print["diagrams (one loop, two loops): ", red$["ndiag"]];
ser$[x_, n_] := Normal[Series[x, {ep, 0, n}]];
pole$[x_] := Module[{s = ser$[x, 0]}, Expand[Coefficient[s, ep, -2]/ep^2 + Coefficient[s, ep, -1]/ep]];
simp$[x_] := Expand[FullSimplify[x]];

(* the bare couplings: yt0 = yt (1 + h dy), gS0 = gS (1 + h dg) at one loop inside the one-loop functions *)
ct$[P_, dy_, dg_] := Expand[dy yt D[P, yt] + dg gS D[P, gS]];

(* one loop *)
z1$ = <|"H" -> -pole$[P1$["H"]], "t_L" -> -pole$[P1$["t_L"]], "t_R" -> -pole$[P1$["t_R"]], "b_L" -> -pole$[P1$["b_L"]],
   "c" -> -pole$[P1$["c"]], "A" -> pole$[P1$["A"]]|>;
f1$ = (z1$["H"] + z1$["t_L"] + z1$["t_R"])/2;
dy1$ = -pole$[f1$ + P1$["V_L"]];
dg1$ = Expand[-z1$["c"] - z1$["A"]/2];
Print["(a) one loop (K units, x 1/eps): z_Phi ", simp$[ep z1$["H"]], ", z_tL ", simp$[ep z1$["t_L"]], ", z_tR ", simp$[ep z1$["t_R"]],
  ", z_bL ", simp$[ep z1$["b_L"]], ", z_3 ", simp$[ep z1$["A"]], ", z~_3 ", simp$[ep z1$["c"]], ";  dy ", simp$[ep dy1$], ", dg ", simp$[ep dg1$]];

(* two loops: Z_X^(2) = -pole[P2 + ct(P1) + z1 P1] (Z_3: Z_3 (1 - Pi)) *)
z2$[k_, s_] := -pole$[s P2$[k] + s ct$[P1$[k], dy1$, dg1$] + z1$[k] s P1$[k]];
z2v$ = <|"H" -> z2$["H", 1], "t_L" -> z2$["t_L", 1], "t_R" -> z2$["t_R", 1], "b_L" -> z2$["b_L", 1], "c" -> z2$["c", 1],
   "A" -> z2$["A", -1]|>;
(* F = Z_Phi^(1/2) Z_tL^(1/2) Z_tR^(1/2) to second order *)
fSer$ = Normal[Series[Sqrt[(1 + h z1$["H"] + h^2 z2v$["H"]) (1 + h z1$["t_L"] + h^2 z2v$["t_L"]) (1 + h z1$["t_R"] + h^2 z2v$["t_R"])],
     {h, 0, 2}]];
f2$ = Expand[Coefficient[fSer$, h, 2]];
dy2$ = -pole$[f2$ + P2$["V_L"] + ct$[P1$["V_L"], dy1$, dg1$] + dy1$ f1$ + (dy1$ + f1$) P1$["V_L"]];
gSer$ = Normal[Series[1/((1 + h z1$["c"] + h^2 z2v$["c"]) Sqrt[1 + h z1$["A"] + h^2 z2v$["A"]]), {h, 0, 2}]];
dg2$ = Expand[Coefficient[gSer$, h, 2]];
Print["(b) two loops: Lambda_L - Lambda_R = ", simp$[ser$[P2$["V_L"] - P2$["V_R"], 0]], ";  Z_bL - Z_tL = ",
  simp$[z2v$["b_L"] - z2v$["t_L"]], "   (expect 0, 0)"];

(* beta functions *)
res$[x_, n_] := Expand[Coefficient[Expand[x], ep, -n]];
aY1$ = yt (res$[dy1$, 1] h + res$[dy2$, 1] h^2); aY2$ = yt res$[dy2$, 2] h^2;
aG1$ = gS (res$[dg1$, 1] h + res$[dg2$, 1] h^2); aG2$ = gS res$[dg2$, 2] h^2;
Dop$[x_, rho_] := Expand[yt D[x, yt] + gS D[x, gS] + 2 la D[x, la] - rho x];
betaY$ = Dop$[aY1$, 1]; betaG$ = Dop$[aG1$, 1];
Print["(c) K beta_yt (one loop) = ", Factor[Coefficient[betaY$, h, 1]], ";  K^2 beta_yt (two loops) = ", Expand[Coefficient[betaY$, h, 2]]];
Print["(c) K beta_gS (one loop) = ", Factor[Coefficient[betaG$, h, 1]], ";  K^2 beta_gS (two loops) = ", Expand[Coefficient[betaG$, h, 2]]];
(* double poles from the one-loop functions *)
b1$ = {Coefficient[betaY$, h, 1] h, Coefficient[betaG$, h, 1] h};
dbl$[a2_, a1_, rho_] := Expand[Coefficient[Dop$[a2, rho] - (b1$[[1]] D[a1, yt] + b1$[[2]] D[a1, gS]), h, 2]];
Print["(c) double-pole consistency (expect 0, 0): ", {dbl$[aY2$, aY1$, 1], dbl$[aG2$, aG1$, 1]}];

(* literature: Buttazzo et al. appendix B in the gaugeless limit (g1 = g2 = 0, yb = ytau = 0), d/d ln mu *)
litY2$ = yt (-12 yt^4 - 12 la yt^2 + 36 gS^2 yt^2 + 6 la^2 - 108 gS^4);
litG2$ = gS (-26 gS^4 - 2 gS^2 yt^2);
Print["(d) K^2 beta_yt^(2) - literature = ", Expand[Coefficient[betaY$, h, 2] - litY2$], "   (expect 0)"];
Print["(d) K^2 beta_gS^(2) - literature = ", Expand[Coefficient[betaG$, h, 2] - litG2$], "   (expect 0)"];
gamma$ = <|"Phi" -> -2 res$[z2v$["H"], 1], "t_L" -> -2 res$[z2v$["t_L"], 1], "t_R" -> -2 res$[z2v$["t_R"], 1]|>;
Print["(e) two-loop anomalous dimensions (K^2 units, Landau gauge): ", gamma$];
Export[FileNameJoin[{srcDir$, "results", "twoloop_sym_beta.csv"}],
  {{"quantity", "expression"}, {"K2_beta_yt_two_loop", ToString[InputForm[Expand[Coefficient[betaY$, h, 2]]]]},
   {"K2_beta_gS_two_loop", ToString[InputForm[Expand[Coefficient[betaG$, h, 2]]]]},
   {"K2_beta_yt_minus_literature", ToString[InputForm[Expand[Coefficient[betaY$, h, 2] - litY2$]]]},
   {"K2_beta_gS_minus_literature", ToString[InputForm[Expand[Coefficient[betaG$, h, 2] - litG2$]]]},
   {"K2_gamma_Phi_two_loop_Landau", ToString[InputForm[gamma$["Phi"]]]}}, "CSV"];
(* the Z factors for the four-point function (twoloop_lambda_eval.wl) *)
Put[<|"z1" -> z1$, "z2" -> z2v$, "dy1" -> dy1$, "dy2" -> dy2$, "dg1" -> dg1$, "dg2" -> dg2$|>,
  FileNameJoin[{srcDir$, "results", "twoloop_sym_z.m"}]];
