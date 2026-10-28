(* ::Package:: *)

(* ::Title:: *)
(*Step (6): the finite-temperature phase transition at the next order (3D EFT, gauge-invariant expansion)*)


(* ::Text:: *)
(*Research note models/abelian_higgs_2loop, step (6).  The model is reduced with DRalgo 1.5.0 to the 3D soft theory*)
(*(A_i, A_0, Phi) at NLO (two-loop mass, one-loop couplings).  Counting lam3/g3^2 = x small (lam ~ e^3 in 4D):*)
(*  V_LO  = m3^2 phi^2/2 + lam3 phi^4/4 - [2 g3^3 phi^3 + (mD^2 + h3 phi^2)^(3/2)]/(12 pi)              (gauge invariant),*)
(*  V_NLO = [g3^4 phi^2 (ln(4 g3^2 phi^2/L^2) - 1) + (3/4) k3 (mD^2 + h3 phi^2)*)
(*           - (1/2) h3^2 phi^2 (1 - ln(4 (mD^2 + h3 phi^2)/L^2))]/(16 pi^2)  -  (sqrt(xi3) g3/(8 pi)) V_LO'(phi)*)
(*(Hirvonen, Loefgren, Ramsey-Musolf, Schicho, Tenkanen, arXiv:2112.08912, Eqs. (B.54), (B.57); L the 3D MS-bar scale,*)
(*background-field R_xi gauge in 3D).  Scalar loops start at the next-to-next order.*)
(*  (a) the NLO 3D parameters of DRalgo against Kajantie, Karjalainen, Laine, Peisa (hep-lat/9711048), Appendix B*)
(*      (Nf = 0, gY = 0): e3^2, h3 (DRalgo's lamVL = 2 h3), lam3, lamA (lamVLL = 6 lamA = 6 k3), m3^2 at two loops;*)
(*  (b) DRalgo's two-loop potential of the soft theory (Landau gauge) in the strict limit (m3^2, lam3 -> 0 inside the*)
(*      loops) against V_NLO at xi3 = 0; its 3D scale dependence against the running of m3^2;*)
(*  (c) T_c and the jump of the condensate <Phi^+ Phi> at LO and NLO in the strict expansion around the LO*)
(*      transition; both are xi3-independent (symbolic); v_c/T_c = sqrt(2 Delta<Phi^+Phi>_3/T_c); the NLO shifts against*)
(*      a numerical derivative in s of the transition of V_LO + s V_NLO; the naive broken minimum moves by*)
(*      c = sqrt(xi3) g3/(8 pi) (no naive T_c exists: the strict V_NLO has g3^4 phi^2 ln phi^2 at small phi);*)
(*      for comparison the conventional Landau-gauge one- and two-loop potentials of DRalgo (scalar loops kept);*)
(*  (d) numbers at e = 1/2, MA = 1 (v = 2), 4D scale 1 (as in the one-loop note): MH = 1/2 (lam = e^3/4), MH = 1*)
(*      (lam = e^3), the 3D scale L = T/2, T, 2T; e = 1/2 ... 1/32 at lam = e^3/4 -> results/thermal_nlo.csv*)
(*      (kind strict: T_c and v_c/T_c at LO, NLO and the condensates; landau: T_c, phi/sqrt(T) at one, two loops;*)
(*      escan: as strict; xi: xi3, T_c^LO, phi_min/sqrt(T), V(phi_min) - V(0), c of the naive minimum).*)
(*Batch: wolframscript -file thermal_nlo.wl (DRalgo needs GroupMath; run in a kernel of its own).*)


(* ::Section:: *)
(*(a) NLO dimensional reduction*)


DRalgo`DRalgo`$LoadGroupMath = True;
Quiet[Get["DRalgo`DRalgo`"]];
srcDirTN$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirTN$ = FileNameJoin[{srcDirTN$, "results"}];
$NumberMarks = False;

Group = {"U1"}; CouplingName = {g1}; RepAdjoint = {0}; RepScalar = {{{1}, "C"}}; RepFermion = {};
{gvvv, gvff, gvss, \[Lambda]1, \[Lambda]3, \[Lambda]4, \[Mu]ij, \[Mu]IJC, \[Mu]IJ, Ysff, YsffC} =
  AllocateTensors[Group, RepAdjoint, CouplingName, RepFermion, RepScalar];
InputInv = {{1, 1}, {True, False}};
massTermTN$ = CreateInvariant[Group, RepScalar, InputInv][[1]] // Simplify;
\[Mu]ij = GradMass[msq massTermTN$] // Simplify // SparseArray;
\[Lambda]4 = GradQuartic[lam massTermTN$^2];
ImportModelDRalgo[Group, gvvv, gvff, gvss, \[Lambda]1, \[Lambda]3, \[Lambda]4, \[Mu]ij, \[Mu]IJ, \[Mu]IJC, Ysff, YsffC, Verbose -> False];
PerformDRhard[];
cplTN$ = Association[PrintCouplings[]];
tmpTN$ = Association[PrintTemporalScalarCouplings[]];
lbRuleTN$ = PrintConstants[];
mDTN$ = (\[Mu]sqU1 /. PrintDebyeMass["LO"]) + (\[Mu]sqU1 /. PrintDebyeMass["NLO"]);
m3TN$ = (msq3d /. PrintScalarMass["LO"]) + (msq3d /. PrintScalarMass["NLO"]);   (* contains g13d, lam3d, lamVL, mu3 *)
lamVLTN$ = tmpTN$[\[Lambda]VL[1]]; lamVLLTN$ = tmpTN$[\[Lambda]VLL[1]];
(* Kajantie et al., Appendix B, with Ns = 1, Nf = 0, gY = 0; nu^2 = -msq; their 3D scale is mu3 *)
Module[{kk = 16 Pi^2, e = g1, nu2 = -msq, lb = Lb, e32, h3, l3, lA, nut, c, m3k, ruleA, d},
  e32 = e^2 T (1 - e^2 lb/(3 kk));
  h3 = e^2 T (1 + (-e^2 lb/3 + 2 e^2 (1 - 1/3) + 8 lam)/kk);
  l3 = T (lam + ((-3 e^4 + 6 lam e^2 - 10 lam^2) lb + 2 e^4)/kk);
  lA = e^4 T/(6 Pi^2);
  nut = nu2 (1 + (3 e^2 - 4 lam) lb/kk);
  c = (Log[8 Pi/9] + zr - 2 EulerGamma)/2;                         (* zr = zeta'(2)/zeta(2) *)
  m3k = -nut + T (l3/3 + e32/4) + T^2/kk (-16 e^4/18 + 2/3 lam e^2) +
    (-2 h3d^2 - 4 g13d^4 + 8 lam3d g13d^2 - 8 lam3d^2)/kk (Log[3 T/\[Mu]3] + c);
  (* zeta'(2)/zeta(2) = gamma_E + ln(2 pi) - 12 ln A (Glaisher) *)
  ruleA = {zr -> EulerGamma + Log[2 Pi] - 12 Log[Glaisher]};
  d = {cplTN$[g13d^2] - e32, lamVLTN$ - 2 h3, cplTN$[lam3d] - l3, lamVLLTN$ - 6 lA,
    (m3TN$ /. \[Lambda]VL[1] -> 2 h3d) - m3k} /. ruleA /. lbRuleTN$;
  d = Simplify[PowerExpand[d], T > 0 && \[Mu] > 0 && \[Mu]3 > 0];
  Print["(a) DRalgo NLO minus Kajantie et al. App. B: e3^2, lamVL - 2 h3, lam3, lamVLL - 6 lamA (expect 0s): ", Most[d]];
  (* m3^2: DRalgo writes the two-loop log of the 4D scale with 4D couplings, Kajantie et al. with 3D ones *)
  Print["(a) m3^2 difference: ", d[[-1]], ";  with the 3D couplings at LO (g3^2 = e^2 T, h3 = e^2 T, lam3 = lam T), i.e. ",
   "at O(1/K) (expect 0): ", Simplify[d[[-1]] /. {g13d -> e Sqrt[T], h3d -> e^2 T, lam3d -> lam T}, T > 0]]];
Print["(a) Debye mass^2 at NLO: ", InputForm[Simplify[mDTN$]]];


(* ::Section:: *)
(*(b) The two-loop potential of the soft theory*)


UseSoftTheory[];
DefineVEVS[{\[Phi], 0, 0}];
CalculatePotential[];
v2DRTN$ = PrintEffectivePotential["NNLO"];
(* strict limit: the scalar masses (m3^2, lam3) -> 0 inside the two-loop part *)
v2StrictTN$ = Module[{e = PowerExpand[v2DRTN$ /. msq3d -> s^2 m0 /. lam3d -> s^2 l0]},
   Simplify[PowerExpand[Normal[Series[e, {s, 0, 0}]] /. {m0 -> 0, l0 -> 0}], \[Phi] > 0 && g13d > 0]];
vNLOTN$[phi_, g3_, h3_, mD2_, k3_, L_] := 1/(16 Pi^2) (g3^4 phi^2 (Log[4 g3^2 phi^2/L^2] - 1) + 3/4 k3 (mD2 + h3 phi^2) -
     1/2 h3^2 phi^2 (1 - Log[4 (mD2 + h3 phi^2)/L^2]));
Print["(b) DRalgo two-loop (Landau, strict) minus V_NLO at xi3 = 0 (expect 0): ",
  Simplify[PowerExpand[v2StrictTN$ - vNLOTN$[\[Phi], g13d, \[Lambda]VL[1]/2, \[Mu]sqU1, \[Lambda]VLL[1]/6, \[Mu]3US]],
   \[Phi] > 0 && g13d > 0 && \[Mu]sqU1 > 0 && \[Lambda]VL[1] > 0 && \[Mu]3US > 0]];
(* 3D scale: d/d ln L [m3^2(L) phi^2/2 + V_NLO] = 0 at this order (lam3 -> 0 in the running) *)
Print["(b) d/dlnL [m3^2(L) phi^2/2 + V_NLO] with lam3 -> 0 (expect 0): ",
  Simplify[PowerExpand[(L D[(m3TN$ /. {\[Mu]3 -> L, lam3d -> 0}) \[Phi]^2/2, L] +
       L D[vNLOTN$[\[Phi], g13d, \[Lambda]VL[1]/2, mD2, k3, L], L]) /. \[Lambda]VL[1] -> 2 h3]] /. h3 -> \[Lambda]VL[1]/2];


(* ::Section:: *)
(*(c) T_c and the condensate in the strict expansion*)


(* gauge independence for a generic V_LO(phi; m3^2): the xi3 part -c V_LO' adds nothing to Delta V at the LO extrema,
   and nothing to d Delta V_min/d m3^2 (the explicit m3^2 derivative cancels against the shift of phi_LO) *)
Module[{vg, c, p0, m},
  Print["(c) xi3 part: Delta V at phi_LO (V_LO'(phi_LO) = V_LO'(0) = 0), condensate (expect 0, 0): ",
   {(-c Derivative[1, 0][vg][p0, m] + c Derivative[1, 0][vg][0, m]) /. Derivative[1, 0][vg][_, m] -> 0,
    Simplify[D[-c Derivative[1, 0][vg][p0, m], m] +
      D[-c Derivative[1, 0][vg][f, m], f] (-Derivative[1, 1][vg][p0, m]/Derivative[2, 0][vg][p0, m]) /. f -> p0]}]];

(* the 3D parameters at temperature t: benchmark e, lam, m2 (msq = -m2) at the 4D scale mu = 1, 3D scale L = c3 t *)
pars3TN$[e_, l_, m2_, c3_, t_] := Module[{sub, g32, h3, l3, mD2, k3, m3},
   sub = {g1 -> e, lam -> l, msq -> -m2, \[Mu] -> 1, T -> t};
   g32 = cplTN$[g13d^2] /. lbRuleTN$ /. sub; l3 = cplTN$[lam3d] /. lbRuleTN$ /. sub;
   h3 = lamVLTN$/2 /. lbRuleTN$ /. sub; k3 = lamVLLTN$/6 /. lbRuleTN$ /. sub; mD2 = mDTN$ /. lbRuleTN$ /. sub;
   m3 = m3TN$ /. lbRuleTN$ /. sub /. {g13d -> Sqrt[g32], lam3d -> l3, \[Lambda]VL[1] -> 2 h3, \[Mu]3 -> c3 t};
   {g32, h3, l3, mD2, k3, m3}];
vLOf$[phi_, {g32_, h3_, l3_, mD2_, k3_, m3_}] := m3 phi^2/2 + l3 phi^4/4 - (2 g32^(3/2) phi^3 + (mD2 + h3 phi^2)^(3/2))/(12 Pi);
vNLOf$[phi_, {g32_, h3_, l3_, mD2_, k3_, m3_}, L_] :=
  If[phi === 0, 3/4 k3 mD2/(16 Pi^2), vNLOTN$[phi, Sqrt[g32], h3, mD2, k3, L]];
dvLOf$[phi_, p_] := D[vLOf$[ff, p], ff] /. ff -> phi;
vXiF$[phi_, p : {g32_, __}, xi_] := -Sqrt[xi] Sqrt[g32]/(8 Pi) dvLOf$[phi, p];
(* the LO transition: Delta V_LO = 0, V_LO' = 0 (a machine-precision root first, then refined) *)
rootTN$[v_, {t0_, p0_}, wp_, sc_] := Module[{sol, eqs},
   eqs = {(v[ph, t] - v[0, t])/(sc ph^2) == 0, (D[v[ff, t], ff] /. ff -> ph)/(sc ph) == 0};   (* no root at phi = 0 *)
   sol = FindRoot[eqs, {{t, t0}, {ph, p0}}];
   sol = FindRoot[eqs, {{t, SetPrecision[t /. sol, wp]}, {ph, SetPrecision[ph /. sol, wp]}},
     WorkingPrecision -> wp, AccuracyGoal -> wp - 15, PrecisionGoal -> wp - 15];
   {t, ph} /. sol];
guessTN$[e_, l_, m2_] := With[{t0 = Sqrt[12 m2/(4 l + 3 e^2)]}, N[{1.01 t0, 2 e^3/(6 Pi l) Sqrt[t0]}]];
(* the NLO shifts: dT = -Delta V_NLO/d_T Delta V_LO and
   Delta<Phi^+Phi>_3 = d Delta V_min/d m3^2 = phi_LO^2/2 + [d_m3 Delta V_xi + V_NLO'(phi_LO) dphi_LO/dm3^2]
                       + phi_LO dphi_LO/dT dT *)
transitionTN$[e_, l_, m2_, c3_, xi_] := Module[{p, tl, pl, pT, dVT, vn, dT, dvpp, dvpT, condNLO},
   p[t_] := pars3TN$[e, l, m2, c3, t];
   {tl, pl} = rootTN$[vLOf$[#1, p[#2]] &, guessTN$[e, l, m2], 40, l];
   pT = p[tl];
   dVT = D[vLOf$[pl, p[t]] - vLOf$[0, p[t]], t] /. t -> tl;
   vn[f_] := vNLOf$[f, pT, c3 tl] + vXiF$[f, pT, xi];
   dT = -(vn[pl] - vn[0])/dVT;
   dvpp = D[vLOf$[f, pT], {f, 2}] /. f -> pl;
   dvpT = D[dvLOf$[pl, p[t]], t] /. t -> tl;
   condNLO = (D[vXiF$[pl, ReplacePart[pT, 6 -> mm], xi] - vXiF$[0, ReplacePart[pT, 6 -> mm], xi], mm] /. mm -> pT[[6]]) +
     (D[vn[f], f] /. f -> pl) (-pl/dvpp) + pl (-dvpT/dvpp) dT;
   <|"TcLO" -> tl, "phiLO" -> pl, "dT" -> dT, "dcond" -> condNLO, "TcNLO" -> tl + dT, "condLO" -> pl^2/2,
     "condNLO" -> pl^2/2 + condNLO, "vTLO" -> Sqrt[pl^2/tl],
     "vTNLO" -> If[pl^2 + 2 condNLO > 0, Sqrt[(pl^2 + 2 condNLO)/(tl + dT)], Indeterminate]|>];
(* cross-check of the strict formulas: T_c(s) and phi_min(s)^2/2 for V_LO + s V_NLO (xi3 = 0, where V_NLO does not
   depend on m3^2), symmetric difference at s = +-1e-20 *)
fdCheckTN$[e_, l_, m2_, c3_] := Module[{p, r, v, sp, sm, h = 10^-20},
   p[t_] := pars3TN$[e, l, m2, c3, t];
   r = transitionTN$[e, l, m2, c3, 0];
   v[s_] := vLOf$[#1, p[#2]] + s vNLOf$[#1, p[#2], c3 #2] &;
   sp = rootTN$[v[h], {r["TcLO"], r["phiLO"]}, 70, l]; sm = rootTN$[v[-h], {r["TcLO"], r["phiLO"]}, 70, l];
   {(sp[[1]] - sm[[1]])/(2 h)/r["dT"] - 1, ((sp[[2]]^2 - sm[[2]]^2)/2/(2 h))/r["dcond"] - 1}];
Print["(c) strict NLO shifts against d/ds at s = 0 (MH = 1/2, L = T), relative (expect ~1e-30): ",
  N[fdCheckTN$[1/2, 1/32, 1/8, 1], 3]];
(* the naive order parameter: the broken minimum of V_LO + V_NLO + V_xi at fixed T moves by c = sqrt(xi3) g3/(8 pi)
   (an NLO effect; the condensate does not move), while V at the minimum changes only at the next-to-next order.
   (The strict V_NLO has g3^4 phi^2 ln phi^2, so phi = 0 is not a local minimum and no naive T_c exists.) *)
Module[{r = transitionTN$[1/2, 1/32, 1/8, 1, 0], pT, tl, mins},
  tl = r["TcLO"]; pT = pars3TN$[1/2, 1/32, 1/8, 1, tl];
  mins = Table[Module[{v, f0},
      v[f_] := vLOf$[f, pT] + vNLOf$[f, pT, tl] + vXiF$[f, pT, xi];
      f0 = ph /. FindRoot[(D[v[ff], ff] /. ff -> ph) == 0, {ph, r["phiLO"]}, WorkingPrecision -> 30];
      {xi, f0, v[f0] - v[0], Sqrt[xi pT[[1]]]/(8 Pi)}], {xi, {0, 1, 3}}];
  Print["(c) naive minimum at T = T_c^LO (MH = 1/2, L = T), xi3 = 1, 3: phi_min shift / c (expect 1 + O(g)) ",
   N[(#[[2]] - mins[[1, 2]])/#[[4]] & /@ Rest[mins], 4],
   ", relative change of V(phi_min) - V(0) (itself NLO at T_c^LO, Delta V_LO = 0; expect O(g)) ",
   N[(#[[3]] - mins[[1, 3]])/mins[[1, 3]] & /@ Rest[mins], 3], " (phi_min/sqrt(T) itself: ", N[#[[2]]/Sqrt[tl] & /@ mins, 5], ")"];
  xiRowsTN$ = {"xi", 0.5, N[1/32], 0.5, 1., #[[1]], tl, 0, #[[2]]/Sqrt[tl], #[[3]], #[[4]]} & /@ mins];
(* the conventional Landau-gauge results: DRalgo's full soft-theory potential (scalar masses kept) at one and two loops,
   minimized numerically; V(0) taken at phi = 1e-20 *)
vOneTN$ = PrintEffectivePotential["LO"] + PrintEffectivePotential["NLO"];
(* the symmetric phase: the phi -> 0 limit taken analytically (the Landau-gauge two-loop terms carry 1/m_A^2) *)
vZeroTN$ = {vOneTN$ /. \[Phi] -> 0, Simplify[Normal[Series[PowerExpand[v2DRTN$ /. \[Phi] -> eps], {eps, 0, 0}]],
     g13d > 0 && msq3d > 0 && lam3d > 0 && \[Mu]sqU1 > 0 && \[Mu]3US > 0]};
(* one loop, then two loops followed from the one-loop root: V_1 + s V_2, s = 1/4 ... 1 *)
convTN$[e_, l_, m2_, c3_, guess_] := Module[{v, g1l, g2l},
   v[s_] := Function[{f, t}, Module[{pp = pars3TN$[e, l, m2, c3, t]},
       If[f === 0, vZeroTN$[[1]] + s vZeroTN$[[2]], vOneTN$ + s v2DRTN$ /. \[Phi] -> f] /. {g13d -> Sqrt[pp[[1]]],
         lam3d -> pp[[3]], msq3d -> pp[[6]], \[Mu]sqU1 -> pp[[4]], \[Lambda]VL[1] -> 2 pp[[2]], \[Lambda]VLL[1] -> 6 pp[[5]],
         \[Mu]3US -> c3 t}]];
   g1l = Quiet[Check[rootTN$[v[0], guess, 30, l], $Failed]];
   g2l = If[g1l === $Failed, $Failed,
     Quiet[Check[Fold[rootTN$[v[#2], #1, 30, l] &, g1l, Range[1/4, 1, 1/4]], $Failed]]];
   If[# === $Failed || ! FreeQ[#, Complex], <|"Tc" -> Indeterminate, "vT" -> Indeterminate|>,
       <|"Tc" -> #[[1]], "vT" -> #[[2]]/Sqrt[#[[1]]]|>] & /@ {g1l, g2l}];


(* ::Section:: *)
(*(d) Numbers*)


bench$ = {{1/2, 1/32}, {1, 1/8}};                    (* MH, lam = MH^2/8 at e = 1/2, v = 2 (m2 = 4 lam) *)
rowsTN$ = {};
Do[Module[{e = 1/2, l = b[[2]], r, rx, cv},
   Do[r = transitionTN$[e, l, 4 l, c3, 0];
    rx = {transitionTN$[e, l, 4 l, c3, 1], transitionTN$[e, l, 4 l, c3, 3]};
    cv = convTN$[e, l, 4 l, c3, {r["TcLO"], r["phiLO"]}];
    Print["(d) MH = ", b[[1]], ", L/T = ", c3, ": strict T_c LO ", N[r["TcLO"], 7], ", NLO ", N[r["TcNLO"], 7],
     ";  v_c/T_c LO ", N[r["vTLO"], 7], ", NLO ", N[r["vTNLO"], 7],
     ";  xi3 = 1, 3 minus xi3 = 0 (T_c, v/T): ",
     N[Flatten[{#["TcNLO"] - r["TcNLO"], #["vTNLO"] - r["vTNLO"]} & /@ rx], 2],
     ";  Landau 3D 1-loop, 2-loop: T_c ", N[#["Tc"] & /@ cv, 7], ", phi/sqrt(T) ", N[#["vT"] & /@ cv, 7]];
    AppendTo[rowsTN$, {"strict", N[b[[1]]], N[l], N[e], N[c3], r["TcLO"], r["TcNLO"], r["vTLO"], r["vTNLO"],
      r["condLO"], r["condNLO"]}];
    AppendTo[rowsTN$, {"landau", N[b[[1]]], N[l], N[e], N[c3], cv[[1]]["Tc"], cv[[2]]["Tc"], cv[[1]]["vT"],
      cv[[2]]["vT"], 0, 0}],
    {c3, {1/2, 1, 2}}]], {b, bench$}];
(* the coupling scan at lam = e^3/4 (MH = e^(3/2), MA = 2 e), L = T *)
Do[Module[{l = e^3/4, r},
   r = transitionTN$[e, l, 4 l, 1, 0];
   Print["(d) e = ", e, ": T_c^NLO/T_c^LO - 1 = ", N[r["TcNLO"]/r["TcLO"] - 1, 6], ", (v/T)^NLO/(v/T)^LO - 1 = ",
    N[r["vTNLO"]/r["vTLO"] - 1, 6], "  (v/T LO ", N[r["vTLO"], 6], ")"];
   AppendTo[rowsTN$, {"escan", N[Sqrt[8 l]], N[l], N[e], 1., r["TcLO"], r["TcNLO"], r["vTLO"], r["vTNLO"],
     r["condLO"], r["condNLO"]}]], {e, {1/2, 1/4, 1/8, 1/16, 1/32}}];
rowsTN$ = Join[rowsTN$, xiRowsTN$];
Export[FileNameJoin[{resDirTN$, "thermal_nlo.csv"}],
  Prepend[Map[Which[StringQ[#], #, # === Indeterminate, "nan", True, ToString[CForm[N[#, 16]]]] &, rowsTN$, {2}],
   {"kind", "MH", "lam", "e", "L_over_T", "Tc_LO", "Tc_NLO", "vT_LO", "vT_NLO", "cond_LO", "cond_NLO"}]];
Print["written results/thermal_nlo.csv"];
