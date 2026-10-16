(* ::Package:: *)

(* ::Title:: *)
(*Step (8'): the note's FeynArts model in the symmetric, gaugeless limit (common setup for the two-loop scripts)*)


(* ::Text:: *)
(*The beta functions of the dimensionless MS-bar couplings do not depend on masses, so they are computed in the symmetric phase*)
(*of the note's own model: the FeynArts model generated from SM.fr (Src/generated/SM_FA) with vev -> 0 (no cubic couplings),*)
(*all masses -> 0, and the electroweak gauge couplings EL -> 0 (gaugeless limit).  What is left are the quartic couplings*)
(*-6 i lam (HHHH) etc., the Yukawa couplings of the top quark (yu[3,3] = yt, all other Yukawa couplings 0), and QCD (GS) with*)
(*the gluon in the Landau gauge (GaugeXi[G] -> 0).  The photon, Z, W, their ghosts and the leptons are excluded from the*)
(*insertions.  Also the two-loop massless propagator family k2 and its IBP reduction.  Read by twoloop_sym_feyncalc.wl,*)
(*twoloop_lambda_feyncalc.wl and twoloop_lambda_massless.wl.*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirSY$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirSY$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirSY$, "generated", "SM_FA"}], FileNameJoin[{modelTmpDirSY$, "SM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirSY$, "SM_FA"}], Quiet -> True];
modelSY$ = FileNameJoin[{modelTmpDirSY$, "SM_FA", "SM_FA"}];
(* fields kept: S[1] H, S[2] G0, S[3] G+, F[3] up quarks, F[4] down quarks, V[4] gluon, U[5] gluon ghost *)
exclSY$ = {V[1], V[2], V[3], U[1], U[2], U[3], U[4], F[1], F[2]};
insSY$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelSY$,
    GenericModel -> modelSY$, ExcludeParticles -> exclSY$], RuleDelayed::rhs];

(* the symmetric, gaugeless limit; yt, la, gS are the bare couplings of the diagrams *)
limitSY$ = Join[
   Thread[(FCGV /@ {"MW", "MZ", "MH", "MT", "MB", "MC", "MS", "MD", "MU", "MTA", "MMU", "Me", "Mu", "Md"}) -> 0],
   {FCGV["EL"] -> 0, SMP["e"] -> 0, vev -> 0, lam -> la, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    yu[3, 3] -> yt, yu[_, _] -> 0, yd[_, _] -> 0, yl[_, _] -> 0,
    GaugeXi[V[4, ___]] -> 0, GaugeXi[G] -> 0, GaugeXi[_] -> 1}];
(* a SumOver of an index that no longer appears (closed quark loop) is the number of colours; otherwise the index is summed
   implicitly by SUNSimplify (as in oneloop_feyncalc.wl) *)
sumOverSY$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];
convSY$[d_, in_, out_, loops_] := Module[{a},
   a = Quiet[FCFAConvert[CreateFeynAmp[d, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
       IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> loops, LorentzIndexNames -> {mu, nu},
       ChangeDimension -> D, List -> True, SMP -> False, DropSumOver -> False, UndoChiralSplittings -> True], RuleDelayed::rhs];
   a = DotSimplify /@ FCI[(sumOverSY$ /@ a) /. limitSY$];
   (* drop only exact zeros (vanishing couplings): replacing the Dirac matrices by 1 would also drop numerators such as
      lslash1 - lslash2 *)
   Select[a, # =!= 0 &]];
colourSY$[x_] := Module[{y = SUNSimplify[DotSimplify[x], SUNNToCACF -> True]},
   y /. {SUNDelta[__] -> 1, SUNFDelta[__] -> 1, SD[__] -> 1, SDF[__] -> 1} /. {CA -> 3, CF -> 4/3}];
(* chiral projectors stay inside the chains; DotSimplify pulls the couplings out of the DOT products first *)
trSY$[z_] := DiracTrace[DiracSimplify[DotSimplify[z]], DiracTraceEvaluate -> True];
algSY$[x_] := Module[{y = colourSY$[x]},
   y = y /. DiracTrace[z_] :> trSY$[z];
   ExpandScalarProduct[Contract[DiracSimplify[y]]]];
FCClearScalarProducts[];
SPD[q, q] = qq;

(* one-loop integrals 1/((l1^2)^a ((l1-q)^2)^b) at -q^2 = mu^2 = 1: (-1)^(a+b) G(a, b) in the MS-bar measure, exact in D *)
gSY$[a_, b_] := Gamma[a + b - D/2] Gamma[D/2 - a] Gamma[D/2 - b]/(Gamma[a] Gamma[b] Gamma[D - a - b]);
canonSY$[k_] := Module[{e = Expand[k]}, If[OrderedQ[{e, Expand[-e]}], e, Expand[-e]]];
fam1SY$ = canonSY$ /@ {l1, l1 - q};
oneLoopSY$[x_] := Module[{y, cr},
   y = FCE[x] /. FAD[a__] :> Times @@ (1/dd[First[FirstPosition[fam1SY$, canonSY$[If[ListQ[#], #[[1]], #]], {0}]]] & /@ {a});
   If[!FreeQ[y, dd[0]], Print["   propagator outside the one-loop family: ", Short[x, 3]]];
   y = Expand[(y /. {SPD[l1, l1] -> dd[1], SPD[l1, q] -> (dd[1] + qq - dd[2])/2, SPD[q, l1] -> (dd[1] + qq - dd[2])/2}) dd[1]^6 dd[2]^6];
   If[!FreeQ[y, l1], Print["   loop momentum left: ", Short[y, 3]]];
   cr = CoefficientRules[y, {dd[1], dd[2]}];
   Total[(#[[2]] If[Min[6 - #[[1]]] <= 0, 0, (-1)^Total[6 - #[[1]]] gSY$ @@ (6 - #[[1]])]) & /@ cr] /. qq -> -1];

(* the two-loop massless propagator family at -q^2 = mu^2 = 1 (as in the QCD note, step (7)): shifts of the loop momenta onto
   k2 = {l1^2, l2^2, (l1-q)^2, (l2-q)^2, (l1-l2)^2}, GLIs, and the IBP reduction with Kira 3.1 onto the masters
   sunset GLI[k2,{1,0,0,1,1}] and bubble^2 GLI[k2,{1,1,1,1,0}] *)
kiraSY$ = FileNameJoin[{$HomeDirectory, "hep", "Kira-3.1", "bin", "kira"}];
fermatSY$ = FileNameJoin[{$HomeDirectory, "hep", "fermat-7.9b", "fer64"}];
famSY$ = FCTopology["k2", {SFAD[l1], SFAD[l2], SFAD[l1 - q], SFAD[l2 - q], SFAD[l1 - l2]}, {l1, l2}, {q}, {Hold[SPD][q] -> qq}, {}];
famSetSY$ = canonSY$ /@ {l1, l2, l1 - q, l2 - q, l1 - l2};
candsSY$ = Flatten[Table[{l1 -> m[[1]] l1 + m[[2]] l2 + c1 q, l2 -> m[[3]] l1 + m[[4]] l2 + c2 q},
    {m, Select[Tuples[{-1, 0, 1}, 4], Abs[#[[1]] #[[4]] - #[[2]] #[[3]]] == 1 &]}, {c1, -1, 1}, {c2, -1, 1}], 2];
momsSY$[x_] := Union[canonSY$ /@ Cases[FCE[x], FAD[a__] :> Sequence @@ (If[ListQ[#], #[[1]], #] & /@ {a}), Infinity]];
findShiftSY$[x_] := Module[{ms = momsSY$[x]}, SelectFirst[candsSY$, SubsetQ[famSetSY$, canonSY$ /@ (ms /. #)] &, $Failed]];
spRulesSY$ = {SPD[l1, l1] -> d[1], SPD[l2, l2] -> d[2], SPD[l1, q] -> (d[1] + qq - d[3])/2, SPD[q, l1] -> (d[1] + qq - d[3])/2,
   SPD[l2, q] -> (d[2] + qq - d[4])/2, SPD[q, l2] -> (d[2] + qq - d[4])/2, SPD[l1, l2] -> (d[1] + d[2] - d[5])/2,
   SPD[l2, l1] -> (d[1] + d[2] - d[5])/2};
denRuleSY$ = FAD[a__] :> Times @@ (1/d[First[FirstPosition[famSetSY$, canonSY$[If[ListQ[#], #[[1]], #]]]]] & /@ {a});
toGLISY$[x_] := Module[{y = FCE[x] /. denRuleSY$ /. spRulesSY$, cr},
   If[!FreeQ[y, l1 | l2], Print["   loop momentum left in a numerator"]];
   cr = CoefficientRules[Expand[y Product[d[i]^8, {i, 5}]], Array[d, 5]];
   Total[(Factor[#[[2]]] GLI["k2", 8 - #[[1]]]) & /@ cr]];
(* a two-loop amplitude after the algebra alg (applied to the shifted amplitude) as a sum of GLIs *)
twoLoopGLISY$[a_, alg_] := Module[{sh = findShiftSY$[a]},
   If[sh === $Failed, Print["   no shift onto k2 for ", momsSY$[a]]; 0, toGLISY$[alg[FCI[FCE[a] /. sh]]]]];
prefSY$ = {{1, 0, 0, 1, 1}, {1, 1, 1, 1, 0}};
(* Kira in the directory dir: returns {success, r, s, reduction function} *)
reduceK2SY$[glis_, dir_] := Module[{r, s, job, ok, tab, all, sym},
   r = Max[Total[Select[#[[2]], Positive]] & /@ glis]; s = Max[-Total[Select[#[[2]], Negative]] & /@ glis];
   job = StringJoin["jobs:\n  - reduce_sectors:\n      reduce:\n        - {topologies: [k2], sectors: [b11111], r: ", ToString[r],
     ", s: ", ToString[s], "}\n      select_integrals:\n        select_mandatory_list:\n          - \"KiraLoopIntegrals\"\n",
     "      preferred_masters: \"preferred\"\n      run_initiate: true\n      run_triangular: true\n      run_back_substitution: true\n",
     "      integral_ordering: 2\n  - kira2math:\n      target:\n       - [k2, \"KiraLoopIntegrals\"]\n"];
   KiraCreateIntegralFile[glis, famSY$, dir];
   KiraCreateConfigFiles[famSY$, glis, dir, KiraMassDimensions -> {qq -> 2}];
   Export[FileNameJoin[{dir, "k2", "preferred"}], StringRiffle[("k2[" <> StringRiffle[ToString /@ #, ","] <> "]") & /@ prefSY$, "\n"] <> "\n", "Text"];
   Export[FileNameJoin[{dir, "k2", "job.yaml"}], job, "Text"];
   ok = KiraRunReduction[FileNameJoin[{dir, "k2"}], KiraBinaryPath -> kiraSY$, KiraFermatPath -> fermatSY$];
   tab = KiraImportResults["k2", dir];
   all = Union[Cases[Join[Values[tab], GLI["k2", #] & /@ prefSY$], _GLI, Infinity]];
   sym = FCLoopFindIntegralMappings[all, {famSY$}, PreferredIntegrals -> (GLI["k2", #] & /@ prefSY$)][[1]];
   {ok, r, s, Function[x, Collect[x /. tab /. sym, _GLI, Together]]}];
