(* ::Package:: *)

(* ::Title:: *)
(*Step (8'): two-loop HHHH vertex of the note's model (symmetric, gaugeless) with an auxiliary mass (infrared rearrangement)*)


(* ::Text:: *)
(*The four-point function has a zero-momentum channel for every routing of external momenta, so it is evaluated at zero external*)
(*momenta with a common auxiliary mass in all propagators (Chetyrkin, Misiak, Muenz, Nucl. Phys. B 518 (1998) 473): the overall*)
(*UV counterterm of a logarithmically divergent graph does not depend on masses, and the M^2 poles of quadratically divergent*)
(*subgraphs (here only the scalar two-point function; the fermion self-energy pole is proportional to pslash and the gluon*)
(*self-energy does not occur at two loops in HHHH) are removed by an auxiliary scalar mass counterterm.  The quark kinetic*)
(*counterterm on a regulated line gives -dZ (1 + M^2 d/dM^2) S_M; its M^2 d/dM^2 part is added in twoloop_lambda_eval.wl.  The scalar and fermion*)
(*masses are kept apart at one loop (Ms, Mf; the counterterm acts on Ms only) and set equal, M = mu = 1, at two loops.*)
(*  one loop: Sigma_H(0) and G4^(1) = Gamma_HHHH/(-6 i) exactly in D (tadpoles (-1)^n Gamma(n - D/2)/Gamma(n) (M^2)^(D/2 - n));*)
(*  two loops: vacuum family v2 = {l1^2 - M^2, l2^2 - M^2, (l1 - l2)^2 - M^2}, IBP reduction with Kira 3.1.*)
(*Output: results/twoloop_lambda_reduction.m.  Batch: wolframscript -file twoloop_lambda_feyncalc.wl*)


Get[FileNameJoin[{DirectoryName[$InputFileName], "twoloop_sym_setup.wl"}]];
workL$ = FileNameJoin[{srcDirSY$, "work", "twoloop_lambda"}];
If[DirectoryQ[workL$], DeleteDirectory[workL$, DeleteContents -> True]];
CreateDirectory[workL$, CreateIntermediateDirectories -> True];
t0$ = AbsoluteTime[];

(* the same limit, but with the auxiliary masses: scalars Ms, quarks Mf, the massless gluon Mg *)
limitCMM$ = Join[Thread[(FCGV /@ {"MH", "MZ", "MW"}) -> Ms],
   Thread[(FCGV /@ {"MT", "MB", "MC", "MS", "MD", "MU", "Mu", "Md", "MTA", "MMU", "Me"}) -> Mf],
   DeleteCases[limitSY$, (FCGV["MW" | "MZ" | "MH" | "MT" | "MB" | "MC" | "MS" | "MD" | "MU" | "MTA" | "MMU" | "Me" | "Mu" | "Md"] -> _)]];
convCMM$[d_, in_, out_, loops_] := Module[{a},
   a = Quiet[FCFAConvert[CreateFeynAmp[d, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
       IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> loops, LorentzIndexNames -> {mu, nu},
       ChangeDimension -> D, List -> True, SMP -> False, DropSumOver -> False, UndoChiralSplittings -> True], RuleDelayed::rhs];
   a = DotSimplify /@ FCI[(sumOverSY$ /@ a) /. limitCMM$];
   a = a /. PropagatorDenominator[p_, 0] :> PropagatorDenominator[p, Mg];
   (* the auxiliary mass sits only in the denominators: the quark numerators stay lslash (no Dirac mass, which would need a
      quark mass counterterm); the denominator mass of the quarks is renamed first *)
   a = a /. PropagatorDenominator[p_, Mf] :> PropagatorDenominator[p, Mfd] /. Mf -> 0 /. Mfd -> Mf;
   a = FCReplaceMomenta[#, {p1 -> 0, p2 -> 0, p3 -> 0, p4 -> 0, q -> 0}] & /@ a;
   (* drop only exact zeros (vanishing couplings) *)
   Select[a, # =!= 0 &]];
ep = Epsilon;
algL$[x_] := Module[{y = DotSimplify[x]},
   y = y /. DiracTrace[z_] :> trSY$[z];
   y = colourSY$[y];
   ExpandScalarProduct[Contract[DiracSimplify[y]]]];
(* the light quarks couple only to gluons and cannot enter HHHH or Sigma_H below three loops: third generation only *)
insL$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelSY$,
    GenericModel -> modelSY$, ExcludeParticles -> Join[exclSY$, {F[3, {1}], F[3, {2}], F[4, {1}], F[4, {2}]}]], RuleDelayed::rhs];


(* ::Section:: *)
(*(a) one loop: Sigma_H(0) and the four-point function, exact in D*)


(* tadpoles int d^Dl/(i Pi^(D/2)) 1/(l^2 - m^2)^n (no E^(eps EulerGamma)) *)
tad$[n_, m_] := (-1)^n Gamma[n - D/2]/Gamma[n] (m^2)^(D/2 - n);
oneLoopV$[x_] := Module[{y = FCE[x], ms, m, cr},
   ms = Union[Cases[y, FAD[a__] :> Sequence @@ (If[ListQ[#], #[[2]], 0] & /@ {a}), Infinity]];
   If[Length[ms] != 1, Print["   one-loop diagram with masses ", ms]];
   m = First[ms];
   y = y /. FAD[a__] :> Times @@ (1/dd & /@ {a});
   y = Expand[(y /. {SPD[l1, l1] -> dd + m^2}) dd^8];
   If[!FreeQ[y, l1], Print["   loop momentum left: ", Short[y, 3]]];
   cr = CoefficientRules[y, {dd}];
   Total[(#[[2]] If[8 - #[[1, 1]] <= 0, 0, tad$[8 - #[[1, 1]], m]]) & /@ cr]];
tops1$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Reducible}];
topsV1$ = CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Reducible}];
ampH1$ = convCMM$[insL$[tops1$, {S[1]} -> {S[1]}], {q}, {q}, {l1}];
amp41$ = convCMM$[insL$[topsV1$, {S[1], S[1]} -> {S[1], S[1]}], {p1, p2}, {p3, p4}, {l1}];
amp40$ = convCMM$[insL$[CreateTopologies[0, 2 -> 2], {S[1], S[1]} -> {S[1], S[1]}], {p1, p2}, {p3, p4}, {}];
Print["(a) tree HHHH: ", InputForm[Total[algL$ /@ amp40$]], ";  one-loop diagrams: Sigma_H ", Length[ampH1$], ", HHHH ", Length[amp41$]];
(* Sigma_bare(0) = value/i with value = (i/K) x integral: K Sigma = integral; G4 = value/(-6 i): K G4^(1) = i integral/(-6 i) *)
sigH0$ = Simplify[Total[oneLoopV$[algL$[#]] & /@ ampH1$]];
g41$ = Simplify[Total[I oneLoopV$[algL$[#]] & /@ amp41$]/(-6 I)];
Print["(a) K Sigma_H(0) = ", Short[sigH0$, 4], ";  K G4^(1) = ", Short[g41$, 4], ";  ", Round[AbsoluteTime[] - t0$], " s"];


(* ::Section:: *)
(*(b) two loops: algebra, shifts onto v2, GLIs*)


topsV2$ = CreateTopologies[2, 2 -> 2, ExcludeTopologies -> {Reducible}];
amp42$ = convCMM$[insL$[topsV2$, {S[1], S[1]} -> {S[1], S[1]}], {p1, p2}, {p3, p4}, {l1, l2}] /. {Ms -> 1, Mf -> 1, Mg -> 1};
Print["(b) two-loop HHHH diagrams (nonzero): ", Length[amp42$], ";  ", Round[AbsoluteTime[] - t0$], " s"];
famV$ = FCTopology["v2", {SFAD[{l1, 1}], SFAD[{l2, 1}], SFAD[{l1 - l2, 1}]}, {l1, l2}, {}, {}, {}];
famSetV$ = canonSY$ /@ {l1, l2, l1 - l2};
candsV$ = ({l1 -> #[[1]] l1 + #[[2]] l2, l2 -> #[[3]] l1 + #[[4]] l2} &) /@ Select[Tuples[{-1, 0, 1}, 4], Abs[#[[1]] #[[4]] - #[[2]] #[[3]]] == 1 &];
momsV$[x_] := Union[canonSY$ /@ Cases[FCE[x], FAD[a__] :> Sequence @@ (If[ListQ[#], #[[1]], #] & /@ {a}), Infinity]];
findShiftV$[x_] := Module[{ms = momsV$[x]}, SelectFirst[candsV$, SubsetQ[famSetV$, canonSY$ /@ (ms /. #)] &, $Failed]];
spRulesV$ = {SPD[l1, l1] -> d[1] + 1, SPD[l2, l2] -> d[2] + 1, SPD[l1, l2] -> (d[1] + d[2] - d[3] + 1)/2,
   SPD[l2, l1] -> (d[1] + d[2] - d[3] + 1)/2};
denRuleV$ = FAD[a__] :> Times @@ (1/d[First[FirstPosition[famSetV$, canonSY$[If[ListQ[#], #[[1]], #]]]]] & /@ {a});
toGLIV$[x_] := Module[{y = FCE[x] /. denRuleV$ /. spRulesV$, cr},
   If[!FreeQ[y, l1 | l2], Print["   loop momentum left in a numerator"]];
   cr = CoefficientRules[Expand[y Product[d[i]^10, {i, 3}]], Array[d, 3]];
   Total[(Factor[#[[2]]] GLI["v2", 10 - #[[1]]]) & /@ cr]];
two42$ = Total[Table[Module[{sh = findShiftV$[a]},
     If[sh === $Failed, Print["   no shift onto v2 for ", momsV$[a]]; 0, toGLIV$[algL$[FCI[FCE[a] /. sh]]]]], {a, amp42$}]];
glisV$ = Union[Cases[two42$, _GLI, Infinity]];
Print["(b) two-loop integrals of v2: ", Length[glisV$], ", indices up to ", Max[Cases[glisV$, GLI[_, n_] :> Max[n], Infinity]],
  ";  ", Round[AbsoluteTime[] - t0$], " s"];


(* ::Section:: *)
(*(c) IBP reduction with Kira*)


rV$ = Max[Total[Select[#[[2]], Positive]] & /@ glisV$]; sV$ = Max[-Total[Select[#[[2]], Negative]] & /@ glisV$];
prefV$ = {{1, 1, 1}, {1, 1, 0}};
jobV$ = StringJoin["jobs:\n  - reduce_sectors:\n      reduce:\n        - {topologies: [v2], sectors: [b111], r: ", ToString[rV$], ", s: ",
   ToString[sV$], "}\n      select_integrals:\n        select_mandatory_list:\n          - \"KiraLoopIntegrals\"\n",
   "      preferred_masters: \"preferred\"\n      run_initiate: true\n      run_triangular: true\n      run_back_substitution: true\n",
   "      integral_ordering: 2\n  - kira2math:\n      target:\n       - [v2, \"KiraLoopIntegrals\"]\n"];
kiraDirV$ = FileNameJoin[{workL$, "kira"}];
KiraCreateIntegralFile[glisV$, famV$, kiraDirV$];
KiraCreateConfigFiles[famV$, glisV$, kiraDirV$];
Export[FileNameJoin[{kiraDirV$, "v2", "preferred"}], StringRiffle[("v2[" <> StringRiffle[ToString /@ #, ","] <> "]") & /@ prefV$, "\n"] <> "\n", "Text"];
Export[FileNameJoin[{kiraDirV$, "v2", "job.yaml"}], jobV$, "Text"];
kiraOKV$ = KiraRunReduction[FileNameJoin[{kiraDirV$, "v2"}], KiraBinaryPath -> kiraSY$, KiraFermatPath -> fermatSY$];
kiraTabV$ = KiraImportResults["v2", kiraDirV$];
allGLIV$ = Union[Cases[Join[Values[kiraTabV$], GLI["v2", #] & /@ prefV$], _GLI, Infinity]];
symRulesV$ = FCLoopFindIntegralMappings[allGLIV$, {famV$}, PreferredIntegrals -> (GLI["v2", #] & /@ prefV$)][[1]];
g42$ = Collect[I^2 (two42$ /. kiraTabV$ /. symRulesV$)/(-6 I), _GLI, Factor];
Print["(c) Kira (r = ", rV$, ", s = ", sV$, "): ", kiraOKV$, ", masters ", Union[Cases[g42$, _GLI, Infinity]], ";  ",
  Round[AbsoluteTime[] - t0$], " s"];


(* ::Section:: *)
(*(d) output*)


Put[<|"sigH0" -> sigH0$, "G41" -> g41$, "G42" -> g42$, "masters" -> (GLI["v2", #] & /@ prefV$),
   "ndiag" -> {Length[ampH1$], Length[amp41$], Length[amp42$]}|>, FileNameJoin[{srcDirSY$, "results", "twoloop_lambda_reduction.m"}]];
Print["(d) wrote results/twoloop_lambda_reduction.m;  total ", Round[AbsoluteTime[] - t0$], " s"];
Quiet[DeleteDirectory[modelTmpDirSY$, DeleteContents -> True]];
