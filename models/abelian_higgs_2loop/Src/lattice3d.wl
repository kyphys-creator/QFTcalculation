(* ::Package:: *)

(* ::Title:: *)
(*Step (7): the 3D U(1)+Higgs theory against the lattice (Kajantie, Karjalainen, Laine, Peisa, hep-lat/9711048)*)


(* ::Text:: *)
(*Research note models/abelian_higgs_2loop, step (7).  With A_0 integrated out, the 3D theory is*)
(*L = F_ij^2/4 + |D_i Phi|^2 + m3^2 Phi^+Phi + lam3 (Phi^+Phi)^2 with x = lam3/e3^2, y = m3^2(mu3 = e3^2)/e3^4 and*)
(*l3 = <Phi^+Phi(e3^2)>/e3^2 (Kajantie et al., Eqs. (2.1)-(2.4)).  Units e3^2 = 1, Phi^+Phi = phi^2/2.*)
(*  (a) the strict expansion of step (6) without A_0: V_LO = y phi^2/2 + x phi^4/4 - phi^3/(6 pi),*)
(*      V_NLO = phi^2 (ln(4 phi^2/mu3^2) - 1)/(16 pi^2) - (sqrt(xi3)/(8 pi)) V_LO' give in closed form*)
(*      y_c = 1/(18 pi^2 x) - [ln(4/(9 pi^2 x^2)) - 1]/(8 pi^2),  Delta l3 = 1/(18 pi^2 x^2) - 1/(4 pi^2 x)*)
(*      (mu3- and xi3-independent; the running of y at this order: dy/dln mu3 = 4/(16 pi^2));*)
(*  (b) the conventional Landau-gauge one- and two-loop potentials (DRalgo's soft theory with A_0 decoupled,*)
(*      lamVL = lamVLL = 0; scalar loops kept; mu3 = e3^2), minimized numerically; with V''(0) at y_c (the two-loop*)
(*      curvature at the origin turns negative for x > 0.15: no coexisting symmetric minimum);*)
(*  (c) numbers at the lattice point x = 0.0463 (lattice: y_c = 0.1038(14), Delta l3 = 1.64(12); their two-loop*)
(*      perturbation theory at mu3 = e3^2: 0.0947, 2.25) and a scan in x -> results/lattice3d.csv;*)
(*  (d) the benchmarks of step (6) mapped to the ultrasoft x, y at their T_c (DRalgo PerformDRsoft)*)
(*      -> results/lattice3d_bench.csv.*)
(*Batch: wolframscript -file lattice3d.wl (after thermal_nlo.wl; DRalgo in a kernel of its own).*)


(* ::Section:: *)
(*Setup*)


DRalgo`DRalgo`$LoadGroupMath = True;
Quiet[Get["DRalgo`DRalgo`"]];
srcDirL3$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirL3$ = FileNameJoin[{srcDirL3$, "results"}];
$NumberMarks = False;

Group = {"U1"}; CouplingName = {g1}; RepAdjoint = {0}; RepScalar = {{{1}, "C"}}; RepFermion = {};
{gvvv, gvff, gvss, \[Lambda]1, \[Lambda]3, \[Lambda]4, \[Mu]ij, \[Mu]IJC, \[Mu]IJ, Ysff, YsffC} =
  AllocateTensors[Group, RepAdjoint, CouplingName, RepFermion, RepScalar];
InputInv = {{1, 1}, {True, False}};
massTermL3$ = CreateInvariant[Group, RepScalar, InputInv][[1]] // Simplify;
\[Mu]ij = GradMass[msq massTermL3$] // Simplify // SparseArray;
\[Lambda]4 = GradQuartic[lam massTermL3$^2];
ImportModelDRalgo[Group, gvvv, gvff, gvss, \[Lambda]1, \[Lambda]3, \[Lambda]4, \[Mu]ij, \[Mu]IJ, \[Mu]IJC, Ysff, YsffC, Verbose -> False];
PerformDRhard[];
cplL3$ = Association[PrintCouplings[]];
tmpL3$ = Association[PrintTemporalScalarCouplings[]];
lbRuleL3$ = PrintConstants[];
mDL3$ = (\[Mu]sqU1 /. PrintDebyeMass["LO"]) + (\[Mu]sqU1 /. PrintDebyeMass["NLO"]);
UseSoftTheory[];
DefineVEVS[{\[Phi], 0, 0}];
CalculatePotential[];
(* A_0 decoupled (lamVL = lamVLL = 0: its loops do not depend on phi), units e3^2 = 1, 3D scale mu3 = e3^2 *)
pureL3$ = {\[Lambda]VL[1] -> 0, \[Lambda]VLL[1] -> 0, \[Mu]sqU1 -> 1, g13d -> 1, \[Mu]3US -> 1};
v1L3$ = PrintEffectivePotential["LO"] + PrintEffectivePotential["NLO"] /. pureL3$;
v2L3$ = PrintEffectivePotential["NNLO"] /. pureL3$;
v20L3$ = Simplify[Normal[Series[PowerExpand[v2L3$ /. \[Phi] -> eps], {eps, 0, 0}]], msq3d > 0 && lam3d > 0];
(* the curvature at the origin, V''(0), at one and two loops: the symmetric phase is a local minimum only if > 0 *)
curvL3$ = Simplify[2 Coefficient[Normal[Series[PowerExpand[# /. \[Phi] -> eps], {eps, 0, 2}]], eps, 2],
     msq3d > 0 && lam3d > 0] & /@ {v1L3$, v1L3$ + v2L3$};


(* ::Section:: *)
(*(a) The strict expansion in closed form*)


Module[{vlo, vnlo, fc, yc0, dy, vpp, dpy, cond, ycE, ycForm, condForm, c = Sqrt[xi]/(8 Pi)},
  vlo[f_, y_] := y f^2/2 + x f^4/4 - f^3/(6 Pi);
  vnlo[0, y_] := 0;
  vnlo[f_, y_] := f^2 (Log[4 f^2/mu^2] - 1)/(16 Pi^2) - c D[vlo[ff, y], ff] /. ff -> f;
  fc = 1/(3 Pi x); yc0 = 1/(18 Pi^2 x);
  Print["(a) LO: V_LO'(phi_c) and Delta V_LO at y_c = 1/(18 pi^2 x), phi_c = 1/(3 pi x) (expect 0, 0): ",
   Simplify[{D[vlo[f, yc0], f] /. f -> fc, vlo[fc, yc0] - vlo[0, yc0]}]];
  dy = -(vnlo[fc, yc0] - vnlo[0, yc0])/(D[vlo[fc, y] - vlo[0, y], y] /. y -> yc0);
  vpp = D[vlo[f, yc0], {f, 2}] /. f -> fc;
  dpy = -(D[D[vlo[f, y], f], y] /. {f -> fc, y -> yc0})/vpp;
  cond = fc^2/2 + (D[vnlo[fc, y] - vnlo[0, y], y] /. y -> yc0) + (D[vnlo[f, yc0], f] /. f -> fc) dpy + fc dpy dy;
  ycE = yc0 + dy - Log[mu]/(4 Pi^2);                  (* y at mu3 = e3^2 from y(mu3): dy/dln mu3 = 4/(16 pi^2) *)
  ycForm = 1/(18 Pi^2 x) - (Log[4/(9 Pi^2 x^2)] - 1)/(8 Pi^2);
  condForm = 1/(18 Pi^2 x^2) - 1/(4 Pi^2 x);
  Print["(a) y_c(e3^2) and Delta l3 at NLO minus the closed forms (expect 0, 0; no mu3, no xi3): ",
   Simplify[PowerExpand[{ycE - ycForm, cond - condForm}], x > 0 && mu > 0 && xi > 0]]];
ycLOL3$[x_] := 1/(18 Pi^2 x);
ycNLOL3$[x_] := 1/(18 Pi^2 x) - (Log[4/(9 Pi^2 x^2)] - 1)/(8 Pi^2);
dlLOL3$[x_] := 1/(18 Pi^2 x^2);
dlNLOL3$[x_] := 1/(18 Pi^2 x^2) - 1/(4 Pi^2 x);


(* ::Section:: *)
(*(b) The Landau-gauge potentials*)


(* the transition in y: Delta V = 0, V' = 0 (divided by phi^2, phi: no root at phi = 0) *)
rootL3$[v_, {y0_, p0_}, xx_] := Module[{sol, eqs},
   eqs = {(v[ph, y] - v[0, y])/(xx ph^2) == 0, (D[v[ff, y], ff] /. ff -> ph)/(xx ph) == 0};
   sol = FindRoot[eqs, {{y, y0}, {ph, p0}}];
   sol = FindRoot[eqs, {{y, SetPrecision[y /. sol, 30]}, {ph, SetPrecision[ph /. sol, 30]}},
     WorkingPrecision -> 30, AccuracyGoal -> 15, PrecisionGoal -> 15];
   {y, ph} /. sol];
vL3$[s_, xx_] := Function[{f, y},
   If[f === 0, (v1L3$ /. \[Phi] -> 0) + s v20L3$, v1L3$ + s v2L3$ /. \[Phi] -> f] /. {msq3d -> y, lam3d -> xx}];
(* one loop from the LO point, two loops from the one-loop root (V_1 + s V_2, s = 1/4 ... 1);
   returns {y_c, Delta l3 = phi_b^2/2, V''(0) at y_c} for each (V''(0) <= 0: the origin is no longer a minimum) *)
landauL3$[xx_, guess_] := Module[{g1l, g2l},
   g1l = Quiet[Check[rootL3$[vL3$[0, xx], guess, xx], $Failed]];
   g2l = If[g1l === $Failed, $Failed,
     Quiet[Check[Fold[rootL3$[vL3$[#2, xx], #1, xx] &, g1l, Range[1/4, 1, 1/4]], $Failed]]];
   MapThread[If[#1 === $Failed || ! FreeQ[#1, Complex], {Indeterminate, Indeterminate, Indeterminate},
      {#1[[1]], #1[[2]]^2/2, #2 /. {msq3d -> #1[[1]], lam3d -> xx}}] &, {{g1l, g2l}, curvL3$}]];


(* ::Section:: *)
(*(c) The lattice point and the scan*)


Module[{xx = 463/10000, lan},
  lan = landauL3$[xx, N[{ycLOL3$[xx], 1/(3 Pi xx)}]];
  Print["(c) x = 0.0463: y_c LO ", N[ycLOL3$[xx], 6], ", NLO ", N[ycNLOL3$[xx], 6], ", Landau 1-loop ", N[lan[[1, 1]], 6],
   ", 2-loop ", N[lan[[2, 1]], 6], "  (lattice 0.1038(14); Kajantie et al. 2-loop 0.0947)"];
  Print["(c) x = 0.0463: Delta l3 LO ", N[dlLOL3$[xx], 6], ", NLO ", N[dlNLOL3$[xx], 6], ", Landau 1-loop ",
   N[lan[[1, 2]], 6], ", 2-loop ", N[lan[[2, 2]], 6], "  (lattice 1.64(12); Kajantie et al. 2-loop 2.25);  V''(0) at y_c: ",
   N[lan[[All, 3]], 4]];
  pointL3$ = {N[xx], ycLOL3$[xx], ycNLOL3$[xx], lan[[1, 1]], lan[[2, 1]], dlLOL3$[xx], dlNLOL3$[xx], lan[[1, 2]], lan[[2, 2]],
    lan[[1, 3]], lan[[2, 3]]}];
(* scan in x, each Landau point started from the previous one *)
scanL3$ = Module[{g = N[{ycLOL3$[1/100], 1/(3 Pi/100)}], lan},
   Table[lan = landauL3$[xx, g];
    If[FreeQ[lan[[1]], Indeterminate], g = {lan[[1, 1]], Sqrt[2 lan[[1, 2]]]}];
    {N[xx], ycLOL3$[xx], ycNLOL3$[xx], lan[[1, 1]], lan[[2, 1]], dlLOL3$[xx], dlNLOL3$[xx], lan[[1, 2]], lan[[2, 2]],
     lan[[1, 3]], lan[[2, 3]]},
    {xx, Union[Range[1/100, 9/100, 1/100], Range[1/10, 1/2, 1/50], Range[15/100, 26/100, 1/100], Range[151/1000, 159/1000, 1/500]]}]];
Print["(c) scan, Landau two loops: largest x with a root ", N[Max[First /@ Select[scanL3$, FreeQ[#[[5]], Indeterminate] &]], 3],
  ", largest x with V''(0) > 0 at y_c ", N[Max[First /@ Select[scanL3$, FreeQ[#[[11]], Indeterminate] && #[[11]] > 0 &]], 3],
  " (one loop: ", N[Max[First /@ Select[scanL3$, FreeQ[#[[10]], Indeterminate] && #[[10]] > 0 &]], 3], ")"];
Export[FileNameJoin[{resDirL3$, "lattice3d.csv"}],
  Prepend[Map[Which[# === Indeterminate, "nan", True, ToString[CForm[N[#, 12]]]] &,
    Join[{pointL3$}, scanL3$], {2}],
   {"x", "yc_LO", "yc_NLO", "yc_1L", "yc_2L", "dl3_LO", "dl3_NLO", "dl3_1L", "dl3_2L", "curv0_1L", "curv0_2L"}]];
Print["written results/lattice3d.csv"];



(* ::Section:: *)
(*(d) The benchmarks of step (6) on the x axis*)


(* soft parameters at T (4D scale 1, e, lam, msq = -m2), then the ultrasoft theory (A_0 integrated out at one loop):
   x_US = lam3US/g3^2 (the abelian A_0 does not couple to A_i, g3US = g3) *)
PerformDRsoft[{}];
cplUSL3$ = Association[PrintCouplingsUS[]];
Print["(d) ultrasoft couplings: ", Keys[cplUSL3$]];
benchL3$ = Module[{rows = Import[FileNameJoin[{resDirL3$, "thermal_nlo.csv"}]], strict},
   strict = Select[Rest[rows], #[[1]] === "strict" && ToExpression[#[[5]]] == 1 &];
   Table[Module[{mh = ToExpression[r[[2]]], l = Rationalize[ToExpression[r[[3]]]], e = 1/2, tc = ToExpression[r[[7]]], sub,
       soft, xs, xu},
      sub = {g1 -> e, lam -> l, msq -> -4 l, \[Mu] -> 1, T -> tc};
      soft = {g13d -> Sqrt[cplL3$[g13d^2] /. lbRuleL3$ /. sub], lam3d -> (cplL3$[lam3d] /. lbRuleL3$ /. sub),
        \[Lambda]VL[1] -> (tmpL3$[\[Lambda]VL[1]] /. lbRuleL3$ /. sub), \[Mu]sqU1 -> (mDL3$ /. lbRuleL3$ /. sub)};
      xs = lam3d/g13d^2 /. soft;
      xu = cplUSL3$[lam3dUS]/g13d^2 /. soft;
      Print["(d) MH = ", mh, ": at T_c^NLO = ", tc, " x (with A_0) = ", N[xs, 4], ", x_US = ", N[xu, 4],
       ";  pure 3D at x_US: y_c NLO ", N[ycNLOL3$[xu], 4], ", Delta l3 NLO ", N[dlNLOL3$[xu], 4]];
      {mh, N[l], tc, xs, xu, ycNLOL3$[xu], dlNLOL3$[xu]}], {r, strict}]];
Export[FileNameJoin[{resDirL3$, "lattice3d_bench.csv"}],
  Prepend[Map[ToString[CForm[N[#, 12]]] &, benchL3$, {2}], {"MH", "lam", "Tc_NLO", "x_soft", "x_US", "yc_NLO_xUS", "dl3_NLO_xUS"}]];
Print["written results/lattice3d_bench.csv"];
