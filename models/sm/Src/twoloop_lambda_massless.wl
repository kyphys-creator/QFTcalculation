(* ::Package:: *)

(* ::Title:: *)
(*Step (8'): the lambda-independent part of beta_lambda^(2) from the HHHH vertex without an auxiliary mass (cross-check)*)


(* ::Text:: *)
(*At la = 0 the external Higgs bosons couple only to the top quark, and the HHHH vertex with the momentum q in at H1 and out at*)
(*H3 (H2, H4 at zero momentum) is infrared finite with massless lines: it is computed as a massless propagator-type function at*)
(*-q^2 = mu^2 = 1 with the family k2 of twoloop_sym_setup.wl, as the two-point functions of twoloop_sym_feyncalc.wl.  Here the*)
(*internal quark field renormalization cancels against the bare fields (S Z lslash S = Z S for massless lines), so*)
(*  Z_Phi^2 (dla + G4^(1)(yt0, gS0) + G4^(2)) finite  (la = 0, the one-loop vertex has no la-linear part),*)
(*and the yt^6 and gS^2 yt^4 terms of beta_lambda^(2) follow without the auxiliary mass of twoloop_lambda_feyncalc.wl.*)
(*Reads results/twoloop_sym_z.m (twoloop_sym_eval.wl).  Batch: wolframscript -file twoloop_lambda_massless.wl*)


Get[FileNameJoin[{DirectoryName[$InputFileName], "twoloop_sym_setup.wl"}]];
workM$ = FileNameJoin[{srcDirSY$, "work", "twoloop_lambda_massless"}];
If[DirectoryQ[workM$], DeleteDirectory[workM$, DeleteContents -> True]];
CreateDirectory[workM$, CreateIntermediateDirectories -> True];
t0$ = AbsoluteTime[];

(* diagrams: third-generation quarks only (the light quarks do not couple to H), la -> 0, H2 and H4 at zero momentum *)
insM$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelSY$, GenericModel -> modelSY$,
    ExcludeParticles -> Join[exclSY$, {F[3, {1}], F[3, {2}], F[4, {1}], F[4, {2}]}]], RuleDelayed::rhs];
ampsM$ = Table[Select[(FCReplaceMomenta[#, {p2 -> 0, p4 -> 0}] & /@ convSY$[insM$[CreateTopologies[L, 2 -> 2,
         ExcludeTopologies -> {Tadpoles, Reducible}], {S[1], S[1]} -> {S[1], S[1]}], {q, p2}, {q, p4}, Take[{l1, l2}, L]]) /. la -> 0,
     # =!= 0 &], {L, 1, 2}];
Print["(a) nonzero HHHH diagrams at la = 0 (one loop, two loops): ", Length /@ ampsM$, ";  ", Round[AbsoluteTime[] - t0$], " s"];
(* G4 = Gamma_HHHH/(-6 i); value = (i/K)^L x integral *)
g41M$ = Simplify[Total[I oneLoopSY$[algSY$[#]] & /@ ampsM$[[1]]]/(-6 I)];
two$ = Total[twoLoopGLISY$[#, algSY$] & /@ ampsM$[[2]]];
glis$ = Union[Cases[two$, _GLI, Infinity]];
{kiraOK$, r$, s$, red$} = reduceK2SY$[glis$, FileNameJoin[{workM$, "kira"}]];
g42M$ = Collect[I^2 red$[two$] /. qq -> -1, _GLI, Factor]/(-6 I);
Print["(b) ", Length[glis$], " integrals of k2; Kira (r = ", r$, ", s = ", s$, "): ", kiraOK$, ", masters ",
  Union[Cases[g42M$, _GLI, Infinity]], ";  ", Round[AbsoluteTime[] - t0$], " s"];

(* renormalization at la = 0 (J per loop includes E^(eps EulerGamma); masters as in twoloop_sym_eval.wl) *)
ep = Epsilon;
mastersM$ = {GLI["k2", {1, 1, 1, 1, 0}] -> E^(2 ep EulerGamma) gSY$[1, 1]^2,
   GLI["k2", {1, 0, 0, 1, 1}] -> -E^(2 ep EulerGamma) gSY$[1, 1] gSY$[ep, 1]} /. D -> 4 - 2 ep;
pole$[x_] := Module[{s = Normal[Series[x, {ep, 0, 0}]]}, Expand[Coefficient[s, ep, -2]/ep^2 + Coefficient[s, ep, -1]/ep]];
zs$ = Get[FileNameJoin[{srcDirSY$, "results", "twoloop_sym_z.m"}]];
G41$ = E^(ep EulerGamma) g41M$ /. D -> 4 - 2 ep;
G42$ = g42M$ /. mastersM$ /. D -> 4 - 2 ep;
z1P$ = zs$["z1"]["H"];
dla1$ = -pole$[G41$];
dla2$ = -pole$[G42$ + zs$["dy1"] yt D[G41$, yt] + zs$["dg1"] gS D[G41$, gS] + 2 z1P$ (dla1$ + G41$)];
(* beta_la = (yt d/dyt + gS d/dgS - 2) a^(1) at la = 0: the yt^6 and gS^2 yt^4 terms are 4 times the residues *)
b2$ = Expand[4 Coefficient[dla2$, ep, -1]];
lit$ = 30 yt^6 - 32 gS^2 yt^4;
Print["(c) K dla^(1) = ", Expand[ep dla1$], "/eps;  K^2 beta_la^(2)(la = 0) = ", b2$, ";  minus literature: ", Expand[b2$ - lit$],
  " (expect 0);  double pole ", Expand[Coefficient[dla2$, ep, -2]], " (RG: -45/2 yt^6 + 24 gS^2 yt^4)"];
Export[FileNameJoin[{srcDirSY$, "results", "twoloop_lambda_massless.csv"}],
  {{"quantity", "expression"}, {"K2_beta_la_two_loop_at_la_0", ToString[InputForm[b2$]]},
   {"K2_beta_la_at_la_0_minus_literature", ToString[InputForm[Expand[b2$ - lit$]]]},
   {"ndiag_one_two", ToString[Length /@ ampsM$]}}, "CSV"];
Quiet[DeleteDirectory[modelTmpDirSY$, DeleteContents -> True]];
