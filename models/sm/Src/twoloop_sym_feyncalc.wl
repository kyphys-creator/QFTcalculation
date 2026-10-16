(* ::Package:: *)

(* ::Title:: *)
(*Step (8'): two-loop H, t, b, gluon, ghost two-point functions and the H t tbar vertex from the note's model (symmetric, gaugeless)*)


(* ::Text:: *)
(*Massless propagator-type integrals at -q^2 = mu^2 = 1 (the H of the vertex carries zero momentum, which only doubles fermion*)
(*propagators and is infrared safe).  Diagrams of the note's FeynArts model in the limit of twoloop_sym_setup.wl; algebra with*)
(*FeynCalc; the loop momenta shifted onto the family k2 = {l1^2, l2^2, (l1-q)^2, (l2-q)^2, (l1-l2)^2} (as in the QCD note,*)
(*step (7)); IBP reduction with Kira 3.1 to the masters sunset GLI[k2,{1,0,0,1,1}] and bubble^2 GLI[k2,{1,1,1,1,0}].*)
(*Normalization (calibrated at one loop in twoloop_sym_oneloop.wl): value = (i/K)^L x integral in J units, and*)
(*  P_H = i^L A/(i q^2),  P_tX = i^L tr[P_X qslash A]/(2 i q^2),  Lambda = i^L tr[P_L A]/tr[P_L A_tree],*)
(*  P_A = i^L g_{mu nu} A^{mu nu}/(i (D-1) q^2),  P_c = i^L A/(i q^2),  Pi_X = sum_L P_X^(L)/K^L  (bare couplings yt, gS, la).*)
(*Output: results/twoloop_sym_reduction.m (one loop exact in D, two loops in the two masters).*)
(*Batch: wolframscript -file twoloop_sym_feyncalc.wl*)


Get[FileNameJoin[{DirectoryName[$InputFileName], "twoloop_sym_setup.wl"}]];
workSY$ = FileNameJoin[{srcDirSY$, "work", "twoloop_sym"}];
If[DirectoryQ[workSY$], DeleteDirectory[workSY$, DeleteContents -> True]];
CreateDirectory[workSY$, CreateIntermediateDirectories -> True];
t0$ = AbsoluteTime[];


(* ::Section:: *)
(*(a) diagrams*)


tops$[L_, n_] := CreateTopologies[L, 1 -> n, ExcludeTopologies -> {Tadpoles, Reducible}];
procs$ = <|"H" -> {{S[1]} -> {S[1]}, 1, {q}, {q}}, "t" -> {{F[3, {3}]} -> {F[3, {3}]}, 1, {q}, {q}},
   "b" -> {{F[4, {3}]} -> {F[4, {3}]}, 1, {q}, {q}}, "V" -> {{F[3, {3}]} -> {F[3, {3}], S[1]}, 2, {q}, {q, pH}},
   "A" -> {{V[4]} -> {V[4]}, 1, {q}, {q}}, "c" -> {{U[5]} -> {U[5]}, 1, {q}, {q}}|>;
(* the Higgs of the vertex carries zero momentum: pH -> 0 right after the conversion (FeynArts keeps pH) *)
amps$ = Association[Table[k -> Table[FCReplaceMomenta[#, {pH -> 0}] & /@ convSY$[insSY$[tops$[L, procs$[k][[2]]], procs$[k][[1]]],
         procs$[k][[3]], procs$[k][[4]], Take[{l1, l2}, L]], {L, 1, 2}], {k, Keys[procs$]}]];
ampTree$ = convSY$[insSY$[CreateTopologies[0, 1 -> 2], procs$["V"][[1]]], {q}, {q, pH}, {}];
Print["(a) nonzero diagrams (one loop, two loops): ", Table[k -> Length /@ amps$[k], {k, Keys[amps$]}],
  ";  ", Round[AbsoluteTime[] - t0$], " s"];


(* ::Section:: *)
(*(b) projections and one loop (exact in D)*)


zeroPH$[x_] := FCReplaceMomenta[x, {pH -> 0}];
proj$ = <|"H" -> (# &), "t_L" -> (trSY$[GA[7] . GSD[q] . #] &), "t_R" -> (trSY$[GA[6] . GSD[q] . #] &),
   "b_L" -> (trSY$[GA[7] . GSD[q] . #] &), "V_L" -> (trSY$[GA[7] . zeroPH$[#]] &), "V_R" -> (trSY$[GA[6] . zeroPH$[#]] &),
   "A" -> (Contract[# MTD[mu, nu]] &), "A_long" -> (Contract[# FVD[q, mu] FVD[q, nu]] &), "c" -> (# &)|>;
procOf$ = <|"H" -> "H", "t_L" -> "t", "t_R" -> "t", "b_L" -> "b", "V_L" -> "V", "V_R" -> "V", "A" -> "A", "A_long" -> "A", "c" -> "c"|>;
trTree$ = <|"V_L" -> Total[algSY$[trSY$[GA[7] . zeroPH$[#]]] & /@ ampTree$], "V_R" -> Total[algSY$[trSY$[GA[6] . zeroPH$[#]]] & /@ ampTree$]|>;
(* normalization of each quantity: P = i^L x (projected value) / norm *)
norm$ = <|"H" -> I qq, "t_L" -> 2 I qq, "t_R" -> 2 I qq, "b_L" -> 2 I qq, "V_L" -> trTree$["V_L"], "V_R" -> trTree$["V_R"],
   "A" -> I (D - 1) qq, "A_long" -> 1, "c" -> I qq|>;
one$ = Association[Table[k -> Simplify[Total[I oneLoopSY$[algSY$[proj$[k][#]]] & /@ amps$[procOf$[k]][[1]]]/(norm$[k] /. qq -> -1)],
     {k, Keys[proj$]}]];
Print["(b) one loop: K P_H = ", Simplify[Series[one$["H"] /. D -> 4 - 2 Epsilon, {Epsilon, 0, -1}] // Normal],
  "; transverse gluon (q q Pi = 0): ", Simplify[one$["A_long"]], ";  ", Round[AbsoluteTime[] - t0$], " s"];


(* ::Section:: *)
(*(c) two loops: algebra, shifts onto k2, GLIs*)


two$ = Association[Table[k -> Module[{lst = amps$[procOf$[k]][[2]], res},
      res = Table[twoLoopGLISY$[a, algSY$[proj$[k][#]] &], {a, lst}];
      Total[res]], {k, Keys[proj$]}]];
glis$ = Union[Cases[Values[two$], _GLI, Infinity]];
Print["(c) two-loop integrals of k2: ", Length[glis$], ", indices from ", Min[Cases[glis$, GLI[_, n_] :> Min[n], Infinity]],
  " to ", Max[Cases[glis$, GLI[_, n_] :> Max[n], Infinity]], ";  ", Round[AbsoluteTime[] - t0$], " s"];


(* ::Section:: *)
(*(d) IBP reduction with Kira*)


{kiraOK$, r$, s$, red$} = reduceK2SY$[glis$, FileNameJoin[{workSY$, "kira"}]];
twoRed$ = Association[Table[k -> Collect[I^2 red$[two$[k]] /. qq -> -1, _GLI, Factor]/(norm$[k] /. qq -> -1), {k, Keys[proj$]}]];
Print["(d) Kira (r = ", r$, ", s = ", s$, "): ", kiraOK$, ", masters ", Union[Cases[Values[twoRed$], _GLI, Infinity]],
  ";  q_mu q_nu Pi^{mu nu} at two loops: ", Simplify[twoRed$["A_long"]], " (expect 0);  ", Round[AbsoluteTime[] - t0$], " s"];


(* ::Section:: *)
(*(e) output*)


Put[<|"one" -> one$, "two" -> twoRed$, "masters" -> (GLI["k2", #] & /@ prefSY$),
   "ndiag" -> Table[k -> Length /@ amps$[k], {k, Keys[amps$]}]|>, FileNameJoin[{srcDirSY$, "results", "twoloop_sym_reduction.m"}]];
Print["(e) wrote results/twoloop_sym_reduction.m;  total ", Round[AbsoluteTime[] - t0$], " s"];
Quiet[DeleteDirectory[modelTmpDirSY$, DeleteContents -> True]];
