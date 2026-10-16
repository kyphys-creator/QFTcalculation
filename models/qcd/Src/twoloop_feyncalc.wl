(* ::Package:: *)

(* ::Title:: *)
(*Step (7): two-loop gluon and ghost self-energies in the Landau gauge (FeynArts + FeynCalc, IBP reduction with Kira 3.1 and FIRE 7.1)*)


(* ::Text:: *)
(*Research note models/qcd, step (7).  In the Landau gauge the ghost vertex is not renormalized (Z~_1 = 1, Taylor), so*)
(*Z_alpha = 1/(Z~_3^2 Z_3) and the two-loop beta function follows from the two-loop gluon and ghost self-energies alone (Eq. (zalpha)).*)
(*(a) FeynArts diagrams (one-particle irreducible, no tadpoles) with one massless quark flavour u (MS-bar is mass independent; each*)
(*    closed quark loop is multiplied by n_f at the end): gluon 23, ghost 7.  GaugeRules -> {} and GaugeXi -> 0 give the Landau*)
(*    propagator -i (g - k k/k^2)/k^2, whose k k/k^4 part FeynArts writes as a repeated denominator.*)
(*(b) The same pipeline at one loop against Eq. (V) with xi = 0: fixes the normalization (V = A/(2 Pi)^(L D) for PreFactor -> 1;*)
(*    g^2 x int d^Dl/(2 Pi)^D -> i a J per loop with a = g^2/K and J = E^(eps EulerGamma) int d^Dl/(i Pi^(D/2)) in MS-bar), and FeynCalc's*)
(*    tr(T^a T^b) = delta^ab/2 (i.e. T_F = 1/2 in the comparison).*)
(*(c) Dirac traces, colour (SUNSimplify, C_A, C_F), the projections g_{mu nu} Pi^{mu nu} = (D-1) q^2 Pi and q_mu q_nu Pi^{mu nu} (which must*)
(*    vanish), and the loop momenta shifted (l1, l2) -> A (l1, l2) + c q per diagram so that all propagators lie in the family*)
(*    k2 = {l1^2, l2^2, (l1-q)^2, (l2-q)^2, (l1-l2)^2} (FeynCalc's FCLoopFindTopologyMappings does not map the four-propagator*)
(*    subtopologies onto k2, as in step (4)); numerators in terms of the five propagators -> GLI["k2", {n1, ..., n5}].*)
(*(d) Kira 3.1 and FIRE 7.1 reduce all integrals to the masters sunset GLI[k2, {1,0,0,1,1}] and bubble^2 GLI[k2, {1,1,1,1,0}];*)
(*    the two tables are compared after FCLoopFindIntegralMappings.  q_mu q_nu Pi^{mu nu} must reduce to 0 exactly in D.*)
(*(e) K Pi^(2)/a^2, K Pitilde^(2)/a^2 (bare, a = g0^2/K with the MS-bar measure) as coefficients of the masters, exact in D, are written*)
(*    to results/twoloop_reduction.m for twoloop_eval.wl.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file twoloop_feyncalc.wl  (after generate_QCD.wl; about 5 minutes).  Interactive:  ~/hep/bin/wopen twoloop_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).  The diagrams are shown before they are evaluated.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirTL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
kiraTL$ = FileNameJoin[{$HomeDirectory, "hep", "Kira-3.1", "bin", "kira"}];
fermatTL$ = FileNameJoin[{$HomeDirectory, "hep", "fermat-7.9b", "fer64"}];
fireTL$ = FileNameJoin[{$HomeDirectory, "hep", "FIRE-7.1", "FIRE7"}];
kernelTL$ = FileNameJoin[{$HomeDirectory, "hep", "opt", "Wolfram142", "Contents", "MacOS", "WolframKernel"}];
workTL$ = FileNameJoin[{srcDirTL$, "work", "twoloop"}];
(* a fresh working directory: Kira and FIRE reuse the databases of an earlier run *)
If[DirectoryQ[workTL$], DeleteDirectory[workTL$, DeleteContents -> True]];
CreateDirectory[workTL$, CreateIntermediateDirectories -> True];
modelTmpDirTL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTL$, "generated", "QCD_FA"}], FileNameJoin[{modelTmpDirTL$, "QCD_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirTL$, "QCD_FA"}], Quiet -> True];
modelTL$ = FileNameJoin[{modelTmpDirTL$, "QCD_FA", "QCD_FA"}];
(* fields: V[2] gluon, U[1] ghost, F[2] u; the photon, the electron and the other quarks are excluded *)
insTL$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelTL$, GenericModel -> modelTL$,
   ExcludeParticles -> {V[1], F[1], F[3], F[4], F[5], F[6], F[7]}];
convTL$[d_, lor_, loops_] := FCFAConvert[CreateFeynAmp[d, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
    IncomingMomenta -> {q}, OutgoingMomenta -> {q}, LoopMomenta -> loops, LorentzIndexNames -> lor, ChangeDimension -> D,
    List -> True, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI //
   ReplaceAll[#, {SMP["g_s"] -> gS, FCGV["GS"] -> gS, GaugeXi[V[2, ___]] -> 0, GaugeXi[G] -> 0}] &;
algTL$[x_] := Module[{y = x},
   y = DiracSimplify[y /. DiracTrace[z_] :> DiracTrace[z, DiracTraceEvaluate -> True]];
   y = SUNSimplify[y, SUNNToCACF -> True];
   y = y /. {SUNDelta[__] -> 1, SUNFDelta[__] -> 1, SD[__] -> 1, SDF[__] -> 1};
   ExpandScalarProduct[Contract[y]]];
(* a closed quark loop: one flavour computed, FeynCalc writes tr(T^a T^b) = delta^ab/2 -> 2 T_F n_f *)
weightTL$[a_] := If[FreeQ[a, DiracTrace], 1, 2 TF nf];
FCClearScalarProducts[];
SPD[q, q] = qq;


(* ::Section:: *)
(*(a) diagrams*)


topsTL$ = CreateTopologies[2, 1 -> 1, ExcludeTopologies -> {Tadpoles, Reducible}];
diagGTL$ = insTL$[topsTL$, {V[2]} -> {V[2]}];
diagCTL$ = insTL$[topsTL$, {U[1]} -> {U[1]}];


(* ::Subsubsection:: *)
(*Inspect: the 23 gluon and 7 ghost two-loop diagrams*)


If[$Notebooks,
  Column[{Show[#, ImageSize -> 760] & /@ Render[Paint[diagGTL$, ColumnsXRows -> {6, 4}, Numbering -> Simple, DisplayFunction -> Identity]],
    Show[#, ImageSize -> 760] & /@ Render[Paint[diagCTL$, ColumnsXRows -> {6, 2}, Numbering -> Simple, DisplayFunction -> Identity]]}, Spacings -> 2]
]


ampGTL$ = convTL$[diagGTL$, {mu, nu}, {l1, l2}];
ampCTL$ = convTL$[diagCTL$, {mu}, {l1, l2}];
wGTL$ = weightTL$ /@ ampGTL$; wCTL$ = weightTL$ /@ ampCTL$;
Print["(a) two-loop 1PI diagrams: gluon ", Length[ampGTL$], ", ghost ", Length[ampCTL$], "  (expect 23, 7);  with a closed quark loop: gluon ",
  Flatten[Position[wGTL$, Except[1], {1}, Heads -> False]], ", ghost ", Flatten[Position[wCTL$, Except[1], {1}, Heads -> False]]];


(* ::Section:: *)
(*(b) one-loop calibration*)


(* ::Text:: *)
(*One-loop integrals 1/((l^2)^a ((l-q)^2)^b) at -q^2 = mu^2 = 1: J = (-1)^(a+b) G(a, b), G(a, b) = Gamma(a+b-D/2) Gamma(D/2-a) Gamma(D/2-b)/*)
(*(Gamma(a) Gamma(b) Gamma(D-a-b)) (times E^(eps EulerGamma), common to both sides), 0 if a <= 0 or b <= 0.*)


canonTL$[k_] := Module[{e = Expand[k]}, If[OrderedQ[{e, Expand[-e]}], e, Expand[-e]]];
gTL$[a_, b_] := Gamma[a + b - D/2] Gamma[D/2 - a] Gamma[D/2 - b]/(Gamma[a] Gamma[b] Gamma[D - a - b]);
fam1TL$ = canonTL$ /@ {l1, l1 - q};
oneLoopTL$[x_] := Module[{y = FCE[x] /. FAD[a__] :> Times @@ (1/dd[First[FirstPosition[fam1TL$, canonTL$[If[ListQ[#], #[[1]], #]]]]] & /@ {a}), cr},
   y = Expand[(y /. {SPD[l1, l1] -> dd[1], SPD[l1, q] -> (dd[1] + qq - dd[2])/2, SPD[q, l1] -> (dd[1] + qq - dd[2])/2}) dd[1]^4 dd[2]^4];
   cr = CoefficientRules[y, {dd[1], dd[2]}];
   Total[(#[[2]] If[Min[4 - #[[1]]] <= 0, 0, (-1)^Total[4 - #[[1]]] gTL$ @@ (4 - #[[1]])]) & /@ cr]];
top1TL$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];
pi1FATL$ = oneLoopTL$[algTL$[Contract[Total[convTL$[insTL$[top1TL$, {V[2]} -> {V[2]}], {mu, nu}, {l1}]] MTD[mu, nu]]]] I/(I (D - 1) qq) /. {gS -> 1, qq -> -1};
pt1FATL$ = oneLoopTL$[algTL$[Total[convTL$[insTL$[top1TL$, {U[1]} -> {U[1]}], {mu}, {l1}]]]] I/(I qq) /. {gS -> 1, qq -> -1};
pi1NoteTL$ = (CA/2 ((3 D - 2)/(D - 1) + (2 D - 7) - (D - 4)/4) - TF 2 (D - 2)/(D - 1)) gTL$[1, 1];
pt1NoteTL$ = -CA (1/2 + (D - 3)/4) gTL$[1, 1];
Print["(b) one loop, Landau gauge, one massless flavour: pipeline / Eq. (V) for K Pi/g^2, K Pitilde/g^2 = ",
  Simplify[FunctionExpand[{pi1FATL$/pi1NoteTL$, pt1FATL$/pt1NoteTL$} /. TF -> 1/2]], "  (expect {1, 1})"];


(* ::Section:: *)
(*(c) algebra, shifts and the integral family*)


famTL$ = FCTopology["k2", {SFAD[l1], SFAD[l2], SFAD[l1 - q], SFAD[l2 - q], SFAD[l1 - l2]}, {l1, l2}, {q}, {Hold[SPD][q] -> qq}, {}];
famSetTL$ = canonTL$ /@ {l1, l2, l1 - q, l2 - q, l1 - l2};
matsTL$ = Select[Tuples[{-1, 0, 1}, 4], Abs[#[[1]] #[[4]] - #[[2]] #[[3]]] == 1 &];
candsTL$ = Flatten[Table[{l1 -> m[[1]] l1 + m[[2]] l2 + c1 q, l2 -> m[[3]] l1 + m[[4]] l2 + c2 q}, {m, matsTL$}, {c1, -1, 1}, {c2, -1, 1}], 2];
momsTL$[x_] := Union[canonTL$ /@ Cases[FCE[x], FAD[a__] :> Sequence @@ (If[ListQ[#], #[[1]], #] & /@ {a}), Infinity]];
findShiftTL$[x_] := Module[{ms = momsTL$[x]}, SelectFirst[candsTL$, SubsetQ[famSetTL$, canonTL$ /@ (ms /. #)] &, $Failed]];
spRulesTL$ = {SPD[l1, l1] -> d[1], SPD[l2, l2] -> d[2], SPD[l1, q] -> (d[1] + qq - d[3])/2, SPD[q, l1] -> (d[1] + qq - d[3])/2,
   SPD[l2, q] -> (d[2] + qq - d[4])/2, SPD[q, l2] -> (d[2] + qq - d[4])/2, SPD[l1, l2] -> (d[1] + d[2] - d[5])/2, SPD[l2, l1] -> (d[1] + d[2] - d[5])/2};
denRuleTL$ = FAD[a__] :> Times @@ (1/d[First[FirstPosition[famSetTL$, canonTL$[If[ListQ[#], #[[1]], #]]]]] & /@ {a});
toGLITL$[x_] := Module[{y = FCE[x] /. denRuleTL$ /. spRulesTL$, cr},
   If[!FreeQ[y, l1 | l2], Print["   loop momentum left in a numerator"]];
   cr = CoefficientRules[Expand[y Product[d[i]^4, {i, 5}]], Array[d, 5]];
   Total[(Factor[#[[2]]] GLI["k2", 4 - #[[1]]]) & /@ cr]];
procTL$[amp_, contr_] := Module[{sh = findShiftTL$[amp]},
   If[sh === $Failed, Print["   no shift onto k2 for ", momsTL$[amp]]; Return[$Failed]];
   toGLITL$[algTL$[contr[FCI[FCE[amp] /. sh]]]]];
timeTL$ = AbsoluteTime[];
gliCTL$ = procTL$[#, Identity] & /@ ampCTL$;
gliGTL$ = procTL$[#, Contract[# MTD[mu, nu]] &] & /@ ampGTL$;
gliLTL$ = procTL$[#, Contract[# FVD[q, mu] FVD[q, nu]] &] & /@ ampGTL$;
Print["(c) algebra, shifts and GLIs in ", Round[AbsoluteTime[] - timeTL$], " s: ", Length[Union[Cases[{gliGTL$, gliLTL$, gliCTL$}, _GLI, Infinity]]],
  " integrals of k2, indices from ", Min[Cases[{gliGTL$, gliLTL$, gliCTL$}, GLI[_, n_] :> Min[n], Infinity]], " to ",
  Max[Cases[{gliGTL$, gliLTL$, gliCTL$}, GLI[_, n_] :> Max[n], Infinity]]];


(* ::Subsubsection:: *)
(*Inspect: the ghost diagrams as integrals of the family k2*)


If[$Notebooks, Column[Short[#, 4] & /@ gliCTL$]]


(* ::Section:: *)
(*(d) IBP reduction with Kira and with FIRE*)


glisTL$ = Union[Cases[{gliGTL$, gliLTL$, gliCTL$}, _GLI, Infinity]];
rTL$ = Max[Total[Select[#[[2]], Positive]] & /@ glisTL$]; sTL$ = Max[-Total[Select[#[[2]], Negative]] & /@ glisTL$];
prefTL$ = {{1, 0, 0, 1, 1}, {1, 1, 1, 1, 0}};      (* sunset, bubble^2 *)
jobTL$ = StringJoin["jobs:\n  - reduce_sectors:\n      reduce:\n        - {topologies: [k2], sectors: [b11111], r: ", ToString[rTL$], ", s: ", ToString[sTL$],
   "}\n      select_integrals:\n        select_mandatory_list:\n          - \"KiraLoopIntegrals\"\n",
   "      preferred_masters: \"preferred\"\n      run_initiate: true\n      run_triangular: true\n      run_back_substitution: true\n",
   "      integral_ordering: 2\n  - kira2math:\n      target:\n       - [k2, \"KiraLoopIntegrals\"]\n"];


(* ::Subsubsection:: *)
(*Kira 3.1*)


kiraDirTL$ = FileNameJoin[{workTL$, "kira"}];
KiraCreateIntegralFile[glisTL$, famTL$, kiraDirTL$];
KiraCreateConfigFiles[famTL$, glisTL$, kiraDirTL$, KiraMassDimensions -> {qq -> 2}];
Export[FileNameJoin[{kiraDirTL$, "k2", "preferred"}], StringRiffle[("k2[" <> StringRiffle[ToString /@ #, ","] <> "]") & /@ prefTL$, "\n"] <> "\n", "Text"];
Export[FileNameJoin[{kiraDirTL$, "k2", "job.yaml"}], jobTL$, "Text"];
kiraOKTL$ = KiraRunReduction[FileNameJoin[{kiraDirTL$, "k2"}], KiraBinaryPath -> kiraTL$, KiraFermatPath -> fermatTL$];
kiraTabTL$ = KiraImportResults["k2", kiraDirTL$];
Print["(d) Kira (r = ", rTL$, ", s = ", sTL$, "): ", kiraOKTL$, ", masters ", Union[Cases[Values[kiraTabTL$], _GLI, Infinity]]];


(* ::Subsubsection:: *)
(*FIRE 7.1*)


fireDirTL$ = FileNameJoin[{workTL$, "fire"}];
FIREPrepareStartFile[famTL$, fireDirTL$, FIREPath -> FileNameJoin[{fireTL$, "FIRE7.m"}]];
fireStartTL$ = FIRECreateStartFile[fireDirTL$, famTL$, FIREMathematicaKernelPath -> kernelTL$];
FIRECreateIntegralFile[glisTL$, famTL$, fireDirTL$];
(* FIRE 7.1 was built without zstd; preferred masters as {{problem id, indices}, ...} *)
With[{cfg = FIRECreateConfigFile[famTL$, fireDirTL$, FIRECompressor -> "lz4"], dk = FileNameJoin[{fireDirTL$, "k2"}]},
  Export[FileNameJoin[{dk, "k2.preferred"}], ToString[{4242, #} & /@ prefTL$, InputForm], "Text"];
  Export[cfg, StringReplace[Import[cfg, "Text"], "#lbases" -> "#preferred k2.preferred\n#lbases"], "Text"]];
fireOKTL$ = FIRERunReduction[FileNameJoin[{fireDirTL$, "k2"}], FIREBinaryPath -> FileNameJoin[{fireTL$, "bin", "FIRE7"}]];
fireTabTL$ = FIREImportResults["k2", fireDirTL$];
Print["(d) FIRE: start file ", fireStartTL$, ", run ", fireOKTL$, ", masters ", Union[Cases[Values[fireTabTL$], _GLI, Infinity]]];


(* ::Subsubsection:: *)
(*Kira against FIRE (integrals equal by symmetry mapped first), transversality, the totals*)


allGLITL$ = Union[Cases[Join[Values[kiraTabTL$], Values[fireTabTL$], GLI["k2", #] & /@ prefTL$], _GLI, Infinity]];
symRulesTL$ = FCLoopFindIntegralMappings[allGLITL$, {famTL$}, PreferredIntegrals -> (GLI["k2", #] & /@ prefTL$)][[1]];
redTL$[tab_][x_] := Collect[x /. tab /. symRulesTL$, _GLI, Together];
devKFTL$ = Simplify[(GLI["k2", #[[2]]] /. kiraTabTL$ /. symRulesTL$) - (GLI["k2", #[[2]]] /. fireTabTL$ /. symRulesTL$)] & /@ glisTL$;
Print["(d) Kira - FIRE over the ", Length[glisTL$], " integrals: ", Union[devKFTL$], "  (expect {0})"];
(* K Pi^(2)/a^2 = (i)^2 x (sum of the g-contracted amplitudes)/(i (D-1) qq), K Pitilde^(2)/a^2 = (i)^2 x (sum)/(i qq) *)
pi2TL$ = Collect[Total[wGTL$ (redTL$[kiraTabTL$] /@ gliGTL$)] /. gS -> 1, _GLI, Together] (I)^2/(I (D - 1) qq);
pt2TL$ = Collect[Total[wCTL$ (redTL$[kiraTabTL$] /@ gliCTL$)] /. gS -> 1, _GLI, Together] (I)^2/(I qq);
long2TL$ = Collect[Total[wGTL$ (redTL$[kiraTabTL$] /@ gliLTL$)], _GLI, Together];
Print["(d) q_mu q_nu Pi^{mu nu} at two loops, reduced: ", Simplify[long2TL$], "  (expect 0: transverse in D dimensions)"];
pi2TL$ = Collect[pi2TL$, _GLI, Factor];
pt2TL$ = Collect[pt2TL$, _GLI, Factor];


(* ::Subsubsection:: *)
(*Inspect: K Pi^(2)/a^2 and K Pitilde^(2)/a^2 in terms of the two masters*)


If[$Notebooks, TableForm[{{"K Pi^(2)/a^2", TraditionalForm[pi2TL$]}, {"K Pitilde^(2)/a^2", TraditionalForm[pt2TL$]}}]]


(* ::Section:: *)
(*(e) output*)


Put[<|"Pi2" -> pi2TL$, "Pitilde2" -> pt2TL$, "masters" -> (GLI["k2", #] & /@ prefTL$)|>, FileNameJoin[{srcDirTL$, "results", "twoloop_reduction.m"}]];
Print["(e) wrote results/twoloop_reduction.m (masters: ", Union[Cases[{pi2TL$, pt2TL$}, _GLI, Infinity]], ")"];


(* ::Section:: *)
(*Cleanup*)


Quiet[DeleteDirectory[modelTmpDirTL$, DeleteContents -> True]];
