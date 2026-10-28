(* ::Package:: *)

(* ::Title:: *)
(*Step (7): the one-loop effective potential of the abelian Higgs model in Fermi and background R_xi gauges, Nielsen identity*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (7); no FeynCalc.  Background phi (Phi = (phi + h + i G)/sqrt 2), field-dependent*)
(*masses mh2 = -m2 + 3 lam phi^2, mG2 = -m2 + lam phi^2, mA2 = e^2 phi^2, x = xi mA2.*)
(*  (a) the G - A_L block from the determinant of the quadratic form: Fermi gauge (L_gf = -(d.A)^2/(2 xi)) gives*)
(*      (k^2 + m+^2)(k^2 + m-^2), m+^2 m-^2 = xi mA2 mG2, and massless ghosts; background R_xi (F = d.A + xi e phi G)*)
(*      gives G with mG2 + x, A_L with x, ghosts with x;*)
(*  (b) V1 = sum n m^4 (ln(m^2/mu^2) - c)/(4K) (MS-bar); the RG equation*)
(*      mu dV/dmu + beta_lam dV/dlam + beta_m2 dV/dm2 - gamma phi dV/dphi = (phi-independent)  holds with gamma =*)
(*      gamma_Phi = (xi - 3) e^2/K in Fermi gauge and gamma_v = -(xi + 3) e^2/K in background R_xi; the beta_t vev*)
(*      v_beta = v + T/MH^2 runs with (3 + xi) e^2/K, the result of Sperling, Stoeckinger and Voigt for this model;*)
(*  (c) Nielsen identity dV1/dxi = C dV0/dphi: C in closed form, equal to the one-loop Nielsen function*)
(*      K = i <s h  Integral c-bar dPsi/dxi> (one ghost-G bubble): C = -(e^2 phi/(2K)) B0(0; x, mG2 + x) in background*)
(*      R_xi, C = (e^2 phi/(2K)) B0(0; m+^2, m-^2) in Fermi gauge (MS-bar finite parts); C(v) finite in background R_xi,*)
(*      logarithmically divergent in Fermi gauge;*)
(*  (d) the tadpole: -dV1/dphi (background R_xi) at v = T of Eq. (T) (fixed R_xi, same xi); d(T/MH^2)/dxi = -C(v);*)
(*      V1(v) the same in every gauge; Fermi gauge: -dV1/dphi -> T(xi = 0) + c (ln(xi MA^2 |mG2|/mu^4) - 2) near v;*)
(*  (e) the curvature at the minimum (hbar-expanded) M_curv^2 = MH^2 + V1''(v) + 3 T/v in background R_xi,*)
(*      dM_curv^2/dxi = 2 C'(v) MH^2; numbers at the benchmark (e = 1/2, lam = 25/32, m2 = 25/8, mu = 1, v = 2);*)
(*  (f) the minimum of V0 + hbar V1 for hbar -> 0: (phi_min - v)/hbar -> T/MH^2 and V_min = V0(v) + hbar V1(v)*)
(*      - hbar^2 T^2/(2 MH^2) in background R_xi; phi_min - v ~ hbar ln hbar in Fermi gauge;*)
(*  results/effpot.csv, results/effpot_hbar.csv, results/effpot_curves.csv.*)
(*Batch: wolframscript -file effpot.wl*)


srcDirEP$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirEP$ = FileNameJoin[{srcDirEP$, "results"}];
$NumberMarks = False;
KK = 16 Pi^2;
mh2 = -m2 + 3 lam phi^2; mG2 = -m2 + lam phi^2; mA2 = e^2 phi^2;
V0 = -m2 phi^2/2 + lam phi^4/4;
vev$ = Sqrt[m2/lam];
pos$ = m2 > 0 && lam > 0 && e > 0 && xi > 0 && mu > 0 && phi > 0;
cell$[y_] := If[StringQ[y], y, ToString[CForm[Chop[N[y, 16], 10^-30]]]];   (* CSV entries *)


(* ::Section:: *)
(*(a) masses from the quadratic forms*)


(* Euclidean, A_mu = (k_mu/|k|) a: |D Phi|^2 gives the mixing e phi A.dG -> i e phi |k| a G *)
fermiM$ = {{k2 + mG2, I e phi Sqrt[k2]}, {-I e phi Sqrt[k2], k2/xi + mA2}};
bgM$ = {{k2 + mG2 + xi mA2, 0}, {0, k2/xi + mA2}};   (* the cross term of (d.A + xi e phi G)^2/(2 xi) cancels the mixing *)
Print["(a) Fermi gauge: xi det = ", Factor[Simplify[xi Det[fermiM$]]], ";  m+^2 + m-^2 = mG2, m+^2 m-^2 = xi mA2 mG2: ",
  Simplify[CoefficientList[Expand[xi Det[fermiM$]], k2] == {xi mA2 mG2, mG2, 1}]];
Print["(a) background R_xi: xi det = ", Factor[Simplify[xi Det[bgM$]]]];

f$[y_] := y^2 (Log[y/mu^2] - 3/2)/(4 KK);              (* one real scalar degree of freedom *)
fV$[y_] := 3 y^2 (Log[y/mu^2] - 5/6)/(4 KK);           (* transverse vector *)
mp$ = (mG2 + Sqrt[mG2^2 - 4 xi mA2 mG2])/2; mm$ = (mG2 - Sqrt[mG2^2 - 4 xi mA2 mG2])/2;
V1L = f$[mh2] + fV$[mA2] + f$[mG2];
V1F = f$[mh2] + fV$[mA2] + f$[mp$] + f$[mm$];
V1B = f$[mh2] + fV$[mA2] + f$[mG2 + xi mA2] - f$[xi mA2];   (* G, A_L (+1), ghosts (-2) *)
(* the limit phi -> v of expressions with mG2 Log[mG2]: m2 -> lam phi^2 - g2, g2 -> 0, then phi -> v *)
atV$[y_] := Simplify[PowerExpand[Limit[y /. m2 -> lam phi^2 - g2, g2 -> 0, Direction -> "FromAbove"] /. phi -> vev$], pos$];


(* ::Section:: *)
(*(b) RG equation, the running of the background and of v_beta*)


betaLam = (20 lam^2 - 12 e^2 lam + 6 e^4)/KK; betaM2 = m2 (8 lam - 6 e^2)/KK;
rgEq$[v1_, gam_] := Simplify[mu D[v1, mu] + betaLam D[V0, lam] + betaM2 D[V0, m2] - gam phi D[V0, phi]];
Print["(b) RG equation (expect -m2^2/K, the running of the vacuum energy): Landau, gamma = -3 e^2/K: ", rgEq$[V1L, -3 e^2/KK],
  ";  Fermi, gamma_Phi = (xi - 3) e^2/K: ", rgEq$[V1F, (xi - 3) e^2/KK]];
Print["(b) background R_xi with gamma_Phi: ", Factor[rgEq$[V1B, (xi - 3) e^2/KK]], ";  with gamma_v = -(xi + 3) e^2/K: ",
  rgEq$[V1B, -(xi + 3) e^2/KK]];
Print["(b) UV poles sum n m^4 minus Landau: Fermi ", Factor[Expand[mp$^2 + mm$^2 - mG2^2]], ";  background R_xi ",
  Factor[Expand[(mG2 + xi mA2)^2 - (xi mA2)^2 - mG2^2]], "  (= -+ 2 xi e^2 phi dV0/dphi)"];
(* v_beta = v + T/MH^2 with T of Eq. (T) (MS-bar finite part, (D - 1) A0 -> 3 A0 - 2 MA^2) *)
a0$[y_] := y (1 - Log[y/mu^2]);
tNote$ = 1/(KK vev$) ((e vev$)^2 (3 a0$[(e vev$)^2] - 2 (e vev$)^2) + 3/2 (2 m2) a0$[2 m2] + (2 m2)/2 a0$[xi (e vev$)^2]);
dvRun$ = vev$/2 (betaM2/m2 - betaLam/lam);                     (* d v/d ln mu of the tree minimum *)
dvBeta$ = Simplify[(dvRun$ + mu D[tNote$/(2 m2), mu])/vev$, pos$];
Print["(b) K d ln v/d ln mu = ", Simplify[dvRun$/vev$ KK], ";  K d ln v_beta/d ln mu = ", Simplify[dvBeta$ KK]];
(* Sperling-Stoeckinger-Voigt Eq. (30): beta_v = (1/K)[g^2 (3 - xi + 2 xi xi') C2(S) - Y2(S)] v with xi' = 1; for the charge-1
   scalar in real components theta = {{0, -i}, {i, 0}}: C2 = theta.theta = 1, no Yukawa couplings *)
theta$ = {{0, -I}, {I, 0}};
c2$ = (theta$.theta$)[[1, 1]];
Print["(b) SSV: C2(S) = ", c2$, ";  (3 - xi + 2 xi) e^2 C2/K - d ln v_beta/d ln mu = ", Simplify[(3 - xi + 2 xi) e^2 c2$/KK - dvBeta$],
  ";  -gamma_v - d ln v_beta/d ln mu = ", Simplify[(3 + xi) e^2/KK - dvBeta$]];


(* ::Section:: *)
(*(c) Nielsen identity*)


cB$ = Simplify[D[V1B, xi]/D[V0, phi]];
cF$ = Simplify[D[V1F, xi]/D[V0, phi]];
b0f$[a_, b_] := 1 - (a Log[a/mu^2] - b Log[b/mu^2])/(a - b);   (* MS-bar finite part of B0(0; a, b) *)
kB$ = -e^2 phi/(2 KK) b0f$[xi mA2, mG2 + xi mA2];
kF$ = e^2 phi/(2 KK) b0f$[mp$, mm$];
benchC$ = {e -> 1/2, lam -> 25/32, m2 -> 25/8, mu -> 1};
Print["(c) background R_xi: C = ", InputForm[cB$]];
Print["(c) background R_xi: C - (-(e^2 phi/(2K)) B0(0; x, mG2 + x)): ", Simplify[cB$ - kB$]];
Print["(c) Fermi gauge: C - (e^2 phi/(2K)) B0(0; m+^2, m-^2), at phi = 3/2, 19/10, 21/10, 3 (v = 2) and xi = 1/2, 3: ",
  If[# < 10^-30, "max |difference| < 10^-30", #] &[
   Max[Abs[Table[(cF$ - kF$) /. benchC$ /. {xi -> xv, phi -> SetPrecision[pv, 40]}, {xv, {1/2, 3}}, {pv, {3/2, 19/10, 21/10, 3}}]]]]];
cBv$ = atV$[cB$];
Print["(c) background R_xi: C(v) = ", InputForm[cBv$], "  (finite)"];
Print["(c) Fermi gauge, xi = 1: C at phi - v = 10^-2, 10^-4, 10^-6, 10^-8: ",
  Table[N[Re[N[cF$ /. benchC$ /. {xi -> 1, phi -> 2 + 10^-k}, 30]], 8], {k, {2, 4, 6, 8}}],
  ";  -(e^2 v/(4K))(ln(xi MA^2 mG2/mu^4) - 2): ",
  Table[N[-(1/4) 2/(4 KK) (Log[(lam (phi^2 - 4)) /. lam -> 25/32 /. phi -> 2 + 10^-k] - 2), 8], {k, {2, 4, 6, 8}}]];


(* ::Section:: *)
(*(d) the tadpole*)


Print["(d) -dV1/dphi at phi = v (background R_xi) - T of Eq. (T): ",
  Simplify[PowerExpand[(-D[V1B, phi] /. phi -> vev$) - tNote$], pos$]];
Print["(d) d(T/MH^2)/d xi + C(v) (expect 0; dv_beta/dxi = -C(v)): ", Simplify[PowerExpand[D[tNote$/(2 m2), xi] + cBv$], pos$]];
Print["(d) V1(v) - V1_Landau(v): background R_xi ", atV$[V1B - V1L], ", Fermi ", atV$[V1F - V1L]];
(* Fermi gauge near v: -dV1/dphi = T_L + c (ln(xi MA^2 |mG2|/mu^4) - 2) + o(1),  c = xi MA^2 MH^2/(4 K v) *)
bench$ = benchC$;
vB$ = 2; mhB$ = 5/2; maB$ = 1;
tOf$[xv_] := N[If[xv == 0, Limit[tNote$ /. bench$ /. xi -> z, z -> 0], tNote$ /. bench$ /. xi -> xv], 30];
tL$ = tOf$[0];
Do[Print["(d) Fermi gauge, xi = ", xv, ": -dV1/dphi - [T_L + c (ln(xi MA^2 |mG2|) - 2)] at phi - v = -10^-2, -10^-4, -10^-6, ",
    "10^-6, 10^-4, 10^-2: ",
    Table[N[Re[N[((-D[V1F, phi]) /. bench$ /. xi -> xv /. phi -> vB$ + d), 40]] -
        (tL$ + xv maB$^2 mhB$^2/(4 KK vB$) (Log[xv maB$^2 Abs[N[mG2 /. bench$ /. phi -> vB$ + d, 40]]] - 2)), 4],
     {d, {-10^-2, -10^-4, -10^-6, 10^-6, 10^-4, 10^-2}}]], {xv, {1, 3}}];


(* ::Section:: *)
(*(e) the curvature at the minimum and numbers at the benchmark*)


curvB$ = Simplify[PowerExpand[(2 lam phi^2 + D[V1B, {phi, 2}] /. phi -> vev$) + 3 tNote$/vev$], pos$];
cBprime$ = atV$[D[cB$, phi]];
Print["(e) C'(v) = ", InputForm[cBprime$]];
Print["(e) dM_curv^2/d xi - 2 C'(v) MH^2 (expect 0): ", Simplify[PowerExpand[D[curvB$, xi] - 2 cBprime$ 2 m2], pos$]];
vAtV$ = N[atV$[V0 + V1L] /. bench$, 30];
zero$[y_] := If[Abs[y] < 10^-14, 0, y];
rows$ = Table[Module[{vals = Join[bench$, {xi -> xv}]},
    {xv, N[atV$[V0 + V1B] /. vals, 16], N[tNote$/(2 m2) /. vals, 16], N[cBv$ /. vals, 16], N[curvB$ /. vals, 16]}],
   {xv, {1/2, 1, 3, 10}}];
Print["(e) V(v) = V0(v) + V1(v) in every gauge: ", N[vAtV$, 16]];
Do[Print["(e) xi = ", r[[1]], ": V(v) - (Landau) = ", zero$[r[[2]] - vAtV$], ", Delta v = T/MH^2 = ", r[[3]], ", C(v) = ", zero$[r[[4]]],
   ", M_curv^2 (background R_xi) = ", r[[5]], "  (pole mass^2 ", N[2.5591003465735151^2, 10], ")"], {r, rows$}];

(* Landau and Fermi gauges: V1'' diverges at v, as (MH^2/v)^2 ln|mG2|/(2K) and as -xi MA^2 (MH^2/v)^2/(4K mG2) *)
Do[Module[{pp = vB$ + d, y},
    y = N[mG2 /. bench$ /. phi -> pp, 40];
    Print["(e) phi - v = ", N[d, 2], ": V1_Landau'' - (MH^2/v)^2 ln|mG2|/(2K) = ",
      N[Re[N[D[V1L, {phi, 2}] /. bench$ /. phi -> pp, 40]] - (mhB$^2/vB$)^2 Log[Abs[y]]/(2 KK), 6],
      ";  mG2 V1_Fermi''(xi = 1) = ", N[y Re[N[D[V1F, {phi, 2}] /. bench$ /. xi -> 1 /. phi -> pp, 40]], 6],
      "  (-xi MA^2 (MH^2/v)^2/(4K) = ", N[-(mhB$^2/vB$)^2/(4 KK), 6], ")"]],
  {d, {-10^-3, -10^-5, -10^-7, 10^-7, 10^-5, 10^-3}}];

(* the one-loop potential minimized numerically (all orders in hbar mixed): root of dV/dphi below v (Brent) *)
dVre[v1_, xv_, hb_, p_?NumericQ] := Re[N[(D[V0 + hb v1, phi] /. bench$ /. xi -> xv) /. phi -> SetPrecision[p, 50], 50]];
vRe[v1_, xv_, hb_, p_?NumericQ] := Re[N[((V0 + hb v1) /. bench$ /. xi -> xv) /. phi -> SetPrecision[p, 50], 50]];
minOf[v1_, xv_, hb_] := Module[{p0},
   p0 = p /. FindRoot[dVre[v1, xv, hb, p], {p, vB$ - hb/2, vB$ - 10^-40}, Method -> "Brent", WorkingPrecision -> 40,
       AccuracyGoal -> 30, PrecisionGoal -> 30];
   {p0 - vB$, vRe[v1, xv, hb, p0], Re[N[(D[V0 + hb v1, {phi, 2}] /. bench$ /. xi -> xv) /. phi -> p0, 30]]}];
gaugesEP$ = {{"background R_xi", V1B}, {"Fermi", V1F}};
num$ = Join[Flatten[Table[Module[{m = minOf[g[[2]], xv, 1]},
       Print["(e) one-loop V minimized, ", g[[1]], " xi = ", xv, ": phi_min - v = ", N[m[[1]], 10], ", V_min - V(v) = ",
         N[m[[2]] - vAtV$, 6], ", V''(phi_min) = ", N[m[[3]], 8]];
       {g[[1]], xv, m[[1]], m[[2]] - vAtV$, m[[3]]}], {g, gaugesEP$}, {xv, {1/2, 1, 3, 10}}], 1],
   {Module[{m = minOf[V1L, 0, 1]},
     Print["(e) one-loop V minimized, Landau: phi_min - v = ", N[m[[1]], 10], ", V_min - V(v) = ", N[m[[2]] - vAtV$, 6],
       ", V''(phi_min) = ", N[m[[3]], 8], "  (T_L/MH^2 = ", N[tL$/mhB$^2, 10], ")"];
     {"Landau", 0, m[[1]], m[[2]] - vAtV$, m[[3]]}]}];
Export[FileNameJoin[{resDirEP$, "effpot.csv"}],
  Map[cell$, Join[{{"xi", "V_at_v", "Deltav_T_over_MH2", "C_at_v_bRxi", "Mcurv2_bRxi"}}, rows$,
    {{"gauge", "xi", "phimin_minus_v_numerical", "Vmin_minus_V_at_v", "curvature_at_min"}}, num$], {2}], "CSV"];


(* ::Section:: *)
(*(f) the hbar expansion of the minimum*)


hbars$ = 4^-Range[0, 6];
cF1$ = maB$^2 mhB$^2/(4 KK vB$);   (* c for xi = 1 *)
tB1$ = tOf$[1];
v0v$ = N[V0 /. bench$ /. phi -> vB$, 30]; v1v$ = vAtV$ - v0v$;
hrows$ = Table[Module[{mb = minOf[V1B, 1, hb], mf = minOf[V1F, 1, hb], ml = minOf[V1L, 0, hb], dPred},
    (* leading order in Fermi gauge: MH^2 d = hbar [T_L + c (ln(xi MA^2 (MH^2/v) |d|) - 2)] *)
    dPred = d /. FindRoot[mhB$^2 d - hb (tL$ + cF1$ (Log[maB$^2 mhB$^2/vB$ Abs[d]] - 2)), {d, -hb, -10^-30},
        Method -> "Brent", WorkingPrecision -> 30];
    Print["(f) hbar = 1/", 1/hb, ": background xi = 1: (phi_min - v)/hbar = ", N[mb[[1]]/hb, 10], ", (V_min - V0 - hbar V1)/hbar^2 = ",
      N[(mb[[2]] - v0v$ - hb v1v$)/hb^2, 8], ";  Fermi xi = 1: ", N[mf[[1]]/hb, 8], " (leading order ", N[dPred/hb, 8], "), ",
      N[(mf[[2]] - v0v$ - hb v1v$)/hb^2, 6], ";  Landau: ", N[ml[[1]]/hb, 10], ", ", N[(ml[[2]] - v0v$ - hb v1v$)/hb^2, 8]];
    {hb, mb[[1]]/hb, (mb[[2]] - v0v$ - hb v1v$)/hb^2, mf[[1]]/hb, dPred/hb, (mf[[2]] - v0v$ - hb v1v$)/hb^2, ml[[1]]/hb,
     (ml[[2]] - v0v$ - hb v1v$)/hb^2}], {hb, hbars$}];
Print["(f) limits, background xi = 1: T/MH^2 = ", N[tB1$/mhB$^2, 10], ", -T^2/(2 MH^2) = ", N[-tB1$^2/(2 mhB$^2), 8],
  ";  Landau: T_L/MH^2 = ", N[tL$/mhB$^2, 10], ", ", N[-tL$^2/(2 mhB$^2), 8]];
Export[FileNameJoin[{resDirEP$, "effpot_hbar.csv"}],
  Map[cell$, Prepend[hrows$, {"hbar", "dphi_over_hbar_bRxi1", "dV2_bRxi1", "dphi_over_hbar_Fermi1",
    "dphi_over_hbar_Fermi1_leading", "dV2_Fermi1", "dphi_over_hbar_Landau", "dV2_Landau"}], {2}], "CSV"];

(* curves for the figure: V1(xi) - V1(Landau) against phi/v *)
(* at phi = v the difference is 0 (part (d)); the expressions there are 0 Log[0] *)
curves$ = Table[Join[{xr},
     If[xr == 1, {0, 0, 0, 0}, Flatten[Table[Re[N[((v1 - V1L) /. bench$ /. xi -> xv) /. phi -> SetPrecision[vB$ xr, 30], 20]],
        {v1, {V1B, V1F}}, {xv, {1, 3}}]]]], {xr, 3/5, 7/5, 1/400}];
Export[FileNameJoin[{resDirEP$, "effpot_curves.csv"}],
  Map[cell$, Prepend[curves$, {"phi_over_v", "dV_bRxi_xi1", "dV_bRxi_xi3", "dV_Fermi_xi1", "dV_Fermi_xi3"}], {2}], "CSV"];
Print["(f) written results/effpot.csv, results/effpot_hbar.csv, results/effpot_curves.csv"];
