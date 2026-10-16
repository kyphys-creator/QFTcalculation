(* ::Package:: *)

(* ::Title:: *)
(*Step (10): Pauli-Villars versus MS-bar for the instanton density -- background-field two-point functions of heavy loops*)


(* ::Text:: *)
(*Research note models/qcd, step (10), App. M.  The PV-regularized one-loop vacuum polarization of a background field is the MS-bar one at*)
(*mu = M minus the MS-bar value of the regulator loop at zero momentum (the poles cancel and the regulated difference is finite in 4 dims).*)
(*This computes, in D dimensions (FeynCalc TID + Package-X, g = 1, Minkowski, D = d - i A), the transverse Pi(k^2 -> 0) of*)
(*  (1) a Dirac fermion of mass M (the quark's PV regulator), (2) a complex scalar of mass M,*)
(*  (3) the PV regulator of the gauge sector in background Feynman gauge: a real adjoint vector with operator (D^2 + M^2) g + 2 ad G*)
(*      (D components) and a complex Grassmann adjoint ghost with D^2 + M^2.*)
(*MS-bar at mu = M: (1), (2) give 0 (PV = MS-bar at mu = M for quarks, so C_q is the same in both schemes); (3) gives C_A/3 against the log*)
(*coefficient 11 C_A/3, i.e. ln mu shifted by 1/22: Lambda_PV/Lambda_MSbar = e^(1/22) for the gauge loops only (from the (D/2 - 1) component*)
(*count), so with n_f quarks Lambda_PV/Lambda_MSbar = exp[N/(6 beta0)] and C_N^MS = C_N^PV e^(N/6).  -> results/inst_scheme.txt*)
(*Usage: wolframscript -file inst_scheme.wl  (under a minute)*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"]; $FCAdvice = False;
srcDirIS$ = Which[StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName], $Notebooks, NotebookDirectory[], True, Directory[]];
outIS$ = {};
rep[s__] := Module[{line = StringJoin[ToString[#, InputForm] & /@ {s}] // StringReplace[#, "\"" -> ""] &}, Print[line]; AppendTo[outIS$, line]];


(* ::Section:: *)
(*amplitudes: A^a_mu(k) in at vertex 1, A^a'_nu(-k) at vertex 2; loop lines p (into vertex 1) and p + k (out of vertex 1)*)


(* colour by hand: tr(T^a T^a') = TF delta, f^{a b c} f^{a' c b} = -CA delta *)
ferm = -TF*DiracTrace[(I GAD[mu]) . (I (GSD[p] + M)) . (I GAD[nu]) . (I (GSD[p + k] + M)), DiracTraceEvaluate -> True] FAD[{p, M}, {p + k, M}];
scal = TF*((I (2 FVD[p, mu] + FVD[k, mu])) (I (2 FVD[p, nu] + FVD[k, nu])) I I FAD[{p, M}, {p + k, M}] + 2 I MTD[mu, nu] I FAD[{p, M}]);
(* real adjoint vector, vertex A^a_lam V^b_sig(p) V^c_tau(q) = f^{abc}[(p-q)_lam g_{sig tau} + 2 kap (k_sig g_{tau lam} - k_tau g_{sig lam})], kap = 1 *)
G1 = (2 FVD[p, mu] + FVD[k, mu]) MTD[s1, t1] + 2 kap (FVD[k, s1] MTD[t1, mu] - FVD[k, t1] MTD[s1, mu]);
G2 = (2 FVD[p, nu] + FVD[k, nu]) MTD[s2, t2] + 2 kap (-FVD[k, s2] MTD[t2, nu] + FVD[k, t2] MTD[s2, nu]);
vec = 1/2 (-CA) G1 G2 (-I MTD[s1, t2]) (-I MTD[t1, s2]) FAD[{p, M}, {p + k, M}] (* bubble, symmetry 1/2 *) +
   1/2 (-I) (2 CA) MTD[mu, nu] D (-I) FAD[{p, M}] (* seagull *) +
   -1 (-CA) (-(2 FVD[p, mu] + FVD[k, mu])) (-(2 FVD[p, nu] + FVD[k, nu])) I I FAD[{p, M}, {p + k, M}] (* ghost bubble *) +
   2 CA MTD[mu, nu] FAD[{p, M}] (* ghost seagull: (-1) i (-1)(-2 CA) i *);
loops = <|"Dirac fermion" -> DiracSimplify[ferm], "complex scalar" -> scal, "PV vector + ghost (gauge regulator)" -> Contract[vec /. kap -> 1]|>;


(* ::Section:: *)
(*transverse part at k -> 0 and its MS-bar value at mu = M*)


pax[x_] := PaXEvaluate[x, PaXImplicitPrefactor -> 1/(2 Pi)^(4 - 2 Epsilon)];
Do[Module[{amp = loops[c], tr, lo, ex0, msb, logc},
   tr = TID[Contract[amp MTD[mu, nu]], p, ToPaVe -> True]; lo = TID[Contract[amp FVD[k, mu] FVD[k, nu]], p, ToPaVe -> True];
   ex0 = Simplify[Normal[Series[pax[(tr - lo/SPD[k, k])/(D - 1)/SPD[k, k]] /. Pair[Momentum[k, D], Momentum[k, D]] -> kk, {kk, 0, 0}]]];
   logc = Simplify[Coefficient[Expand[ex0 /. Log[ScaleMu^2/M^2] -> lmu], lmu]];
   msb = Simplify[Coefficient[Normal[Series[ex0 /. Log[4 Pi] -> EulerGamma + lg /. ScaleMu -> M, {Epsilon, 0, 0}]], Epsilon, 0] /. lg -> 0];
   rep[c, ": k_mu k_nu Pi^{mu nu} = ", Simplify[pax[lo]], ";  Pi(0) = ", ex0];
   rep["    coefficient of ln(mu^2/M^2): ", logc, " = (i/16 pi^2) x ", Simplify[logc 16 Pi^2/I], ";  MS-bar remainder at mu = M: ", msb,
    If[msb =!= 0, StringJoin[" = (i/16 pi^2) x ", ToString[Simplify[msb 16 Pi^2/I], InputForm], " -> shift of ln mu = ", ToString[Simplify[msb/logc/2], InputForm]], ""]]],
  {c, Keys[loops]}];
rep["=> quark loops: PV(M) = MS-bar(mu = M), C_q unchanged; gauge loops: ln mu shifted by 1/22 (Lambda_PV/Lambda_MSbar = e^(1/22) for SU(N) without quarks);",
  " with n_f quarks Lambda_PV/Lambda_MSbar = exp[(N/6)/beta0], C_N^MS = C_N^PV e^(N/6)"];
Export[FileNameJoin[{srcDirIS$, "results", "inst_scheme.txt"}], StringRiffle[outIS$, "\n"] <> "\n", "Text"];
Print["wrote results/inst_scheme.txt"];
