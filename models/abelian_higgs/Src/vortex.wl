(* ::Package:: *)

(* ::Title:: *)
(*Step (11): the vortex tension by direct minimization (abelian Higgs model)*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (11); an independent check of vortex.py.  The tension*)
(*    T/(pi v^2) = 2 Integral rho drho [ n^2 a'^2/(2 rho^2) + f'^2/2 + n^2 f^2 (1 - a)^2/(2 rho^2) + (beta/8)(1 - f^2)^2 ]*)
(*is discretized on rho = R u^2 (u uniform, N intervals, midpoint rule, f = a = 0 at rho = 0 and 1 at rho = R) and*)
(*minimized over the 2(N - 1) values of f and a with FindMinimum (no Euler-Lagrange equations); N = 200 and 400 with*)
(*Richardson extrapolation (second order).*)
(*  (a) the Bogomolny identity: the discretized tension minus n equals the sum of the squares of the first-order*)
(*      combinations plus the boundary term, so the minimum at beta = 1 tends to n;*)
(*  (b) T/(pi v^2) for (n, beta) = (1, 0.5), (1, 1), (1, 2), (2, 0.5), (2, 1), (2, 2) against results/vortex.csv*)
(*      (solve_bvp);*)
(*  results/vortex_min.csv.*)
(*Batch: wolframscript -file vortex.wl*)


srcDirVX$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirVX$ = FileNameJoin[{srcDirVX$, "results"}];
$NumberMarks = False;


(* ::Section:: *)
(*(a) the Bogomolny identity in the continuum*)


dens$ = n^2 a'[r]^2/(2 r^2) + f'[r]^2/2 + n^2 f[r]^2 (1 - a[r])^2/(2 r^2) + b/8 (1 - f[r]^2)^2;
bog$ = (n a'[r]/r - (1 - f[r]^2)/2)^2/2 + (f'[r] - n f[r] (1 - a[r])/r)^2/2 + n/(2 r) D[(a[r] - 1) (1 - f[r]^2), r];
Print["(a) density - [Bogomolny squares + total derivative] at beta = 1 (expect 0): ", Simplify[(dens$ - bog$) /. b -> 1]];


(* ::Section:: *)
(*(b) direct minimization*)


tension$[nn_, bb_, nGrid_, rMax_, guess_ : None] := Module[{u, rr, fv, av, fs, as, en, vars, init, sol, h, rm, fm, am, df, da},
   u = Range[0, nGrid]/nGrid; rr = N[rMax u^2];
   fs = Table[Symbol["f" <> ToString[i]], {i, 1, nGrid - 1}]; as = Table[Symbol["a" <> ToString[i]], {i, 1, nGrid - 1}];
   fv = Join[{0}, fs, {1}]; av = Join[{0}, as, {1}];
   en = Sum[h = rr[[i + 1]] - rr[[i]]; rm = (rr[[i + 1]] + rr[[i]])/2; fm = (fv[[i + 1]] + fv[[i]])/2; am = (av[[i + 1]] + av[[i]])/2;
     df = (fv[[i + 1]] - fv[[i]])/h; da = (av[[i + 1]] - av[[i]])/h;
     2 h rm (nn^2 da^2/(2 rm^2) + df^2/2 + nn^2 fm^2 (1 - am)^2/(2 rm^2) + bb/8 (1 - fm^2)^2), {i, 1, nGrid}];
   init = If[guess === None,
     Join[Thread[{fs, Tanh[rr[[2 ;; -2]]/1.5]^nn}], Thread[{as, Tanh[rr[[2 ;; -2]]/2.]^2}]],
     Join[Thread[{fs, guess[[1]] /@ rr[[2 ;; -2]]}], Thread[{as, guess[[2]] /@ rr[[2 ;; -2]]}]]];
   sol = Quiet[FindMinimum[en, init, Method -> "QuasiNewton", AccuracyGoal -> 12, PrecisionGoal -> 12, MaxIterations -> 100000],
     {FindMinimum::cvmit, FindMinimum::lstol}];   (* stops at the machine-precision limit of the line search *)
   {sol[[1]], Interpolation[Transpose[{rr, fv /. sol[[2]]}]], Interpolation[Transpose[{rr, av /. sol[[2]]}]]}];

ref$ = Import[FileNameJoin[{resDirVX$, "vortex.csv"}], "CSV", "HeaderLines" -> 1];
refT$[nn_, bb_] := First[Select[ref$, #[[1]] == nn && Abs[#[[2]] - bb] < 10^-9 &]][[3]];
rowsVX$ = {};
Do[Module[{r1, r2, rich, nn = c[[1]], bb = c[[2]]},
    r1 = tension$[nn, bb, 200, 25.];
    r2 = tension$[nn, bb, 400, 25., {r1[[2]], r1[[3]]}];
    rich = (4 r2[[1]] - r1[[1]])/3;
    Print["(b) n = ", nn, ", beta = ", bb, ": N = 200 ", ToString[NumberForm[r1[[1]], 12]], ", N = 400 ",
      ToString[NumberForm[r2[[1]], 12]], ", extrapolated ", ToString[NumberForm[rich, 12]], ";  solve_bvp ",
      ToString[NumberForm[refT$[nn, bb], 12]], ", difference ", ToString[CForm[N[rich - refT$[nn, bb], 2]]]];
    AppendTo[rowsVX$, {nn, bb, r1[[1]], r2[[1]], rich, refT$[nn, bb]}]],
  {c, {{1, 0.5}, {1, 1.}, {1, 2.}, {2, 0.5}, {2, 1.}, {2, 2.}}}];
Export[FileNameJoin[{resDirVX$, "vortex_min.csv"}],
  Prepend[Map[ToString[CForm[#]] &, rowsVX$, {2}], {"n", "beta", "T_N200", "T_N400", "T_extrapolated", "T_solve_bvp"}], "CSV"];
Print["(b) written results/vortex_min.csv"];
