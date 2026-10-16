(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: per-diagram values of the two-loop gluon and ghost self-energies*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices.  Per-diagram version of twoloop_feyncalc.wl (step (7)): the same FeynArts +*)
(*FeynCalc pipeline in the Landau gauge and the same Kira 3.1 reduction (without the FIRE comparison and the one-loop calibration), but each*)
(*diagram's reduced value (coefficients of the two masters, exact in D) and its field content are written out, for*)
(*  app:rg 「図の組ごとの値と z_21、z~_21（式 (z2)）。」, tab:twoloopclass, tab:twoloopclassgh*)
(*  (deriv_twoloop_export.wl, deriv_twoloop_table.wl, deriv_twoloop_latex.py, deriv_twoloop_cftf.py read the result).*)
(*(a) the 23 gluon and 7 ghost diagrams (shown before they are evaluated, notebook) and their field content (FeynArts field rules);*)
(*(c) algebra and shifts onto the family k2; (d) Kira; (e) the sum over the diagrams equals results/twoloop_reduction.m of*)
(*twoloop_feyncalc.wl (0, 0).*)
(*Reads generated/QCD_FA (run_model_check.sh) and results/twoloop_reduction.m; Kira works in work/twoloop_perdiag (deleted at the start).*)
(*Writes results/twoloop_perdiag.m (<|"gluon" -> {<|"descr", "weight", "gli", "value"|>, ...}, "ghost" -> ...|>, value = K^2 Pi^(2)/g^4 per*)
(*diagram as coefficients of GLI["k2", {1,0,0,1,1}] (sunset) and GLI["k2", {1,1,1,1,0}] (bubble^2)); run_deriv_check.sh saves the check*)
(*lines as results/deriv_twoloop_perdiag.txt.*)
(*Usage (from Src/): wolframscript -file deriv_twoloop_perdiag.wl   (about 3 minutes)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_twoloop_perdiag.wl  (after generate_QCD.wl; FeynCalc with FeynArts, in a kernel of its own).  Interactive:  ~/hep/bin/wopen deriv_twoloop_perdiag.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirTL$ = Which[StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName], $Notebooks, NotebookDirectory[], True, Directory[]];
kiraTL$ = FileNameJoin[{$HomeDirectory, "hep", "Kira-3.1", "bin", "kira"}];
fermatTL$ = FileNameJoin[{$HomeDirectory, "hep", "fermat-7.9b", "fer64"}];
workTL$ = FileNameJoin[{srcDirTL$, "work", "twoloop_perdiag"}];
If[DirectoryQ[workTL$], DeleteDirectory[workTL$, DeleteContents -> True]];
CreateDirectory[workTL$, CreateIntermediateDirectories -> True];
modelTmpDirTL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTL$, "generated", "QCD_FA"}], FileNameJoin[{modelTmpDirTL$, "QCD_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirTL$, "QCD_FA"}], Quiet -> True];
modelTL$ = FileNameJoin[{modelTmpDirTL$, "QCD_FA", "QCD_FA"}];
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
weightTL$[a_] := If[FreeQ[a, DiracTrace], 1, 2 TF nf];
FCClearScalarProducts[];
SPD[q, q] = qq;


(* ::Section:: *)
(*(a) diagrams*)


topsTL$ = CreateTopologies[2, 1 -> 1, ExcludeTopologies -> {Tadpoles, Reducible}];
diagGTL$ = insTL$[topsTL$, {V[2]} -> {V[2]}];
diagCTL$ = insTL$[topsTL$, {U[1]} -> {U[1]}];


(* ::Subsubsection:: *)
(*Inspect: the 23 gluon and 7 ghost two-loop diagrams (before they are evaluated)*)


If[$Notebooks,
  Column[{Show[#, ImageSize -> 760] & /@ Render[Paint[diagGTL$, ColumnsXRows -> {6, 4}, Numbering -> Simple, DisplayFunction -> Identity]],
    Show[#, ImageSize -> 760] & /@ Render[Paint[diagCTL$, ColumnsXRows -> {6, 2}, Numbering -> Simple, DisplayFunction -> Identity]]}, Spacings -> 2]
]


(* field content of each diagram, in the order of CreateFeynAmp: propagators {from, to, field} *)
descr$[tl_] := Reap[DiagramSelect[tl, (Sow[List @@ (# /. Propagator[ty_][v1_, v2_, f_, ___] :> {ty, v1, v2, f})]; True) &]][[2, 1]];
dG$ = descr$[diagGTL$]; dC$ = descr$[diagCTL$];
Print["(a) descriptions: ", Length[dG$], " gluon, ", Length[dC$], " ghost"];


(* ::Subsubsection:: *)
(*Inspect: the field content of gluon diagram 4, (c) (FeynArts field rules)*)


If[$Notebooks,
  dG$[[4]]
]


ampGTL$ = convTL$[diagGTL$, {mu, nu}, {l1, l2}];
ampCTL$ = convTL$[diagCTL$, {mu}, {l1, l2}];
wGTL$ = weightTL$ /@ ampGTL$; wCTL$ = weightTL$ /@ ampCTL$;
Print["(a) two-loop 1PI diagrams: gluon ", Length[ampGTL$], ", ghost ", Length[ampCTL$]];


(* ::Section:: *)
(*(c) shifts onto the family k2 and the algebra*)


canonTL$[k_] := Module[{e = Expand[k]}, If[OrderedQ[{e, Expand[-e]}], e, Expand[-e]]];
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
Print["(c) algebra in ", Round[AbsoluteTime[] - timeTL$], " s"];


(* ::Section:: *)
(*(d) IBP reduction with Kira*)


glisTL$ = Union[Cases[{gliGTL$, gliCTL$}, _GLI, Infinity]];
rTL$ = Max[Total[Select[#[[2]], Positive]] & /@ glisTL$]; sTL$ = Max[-Total[Select[#[[2]], Negative]] & /@ glisTL$];
prefTL$ = {{1, 0, 0, 1, 1}, {1, 1, 1, 1, 0}};
jobTL$ = StringJoin["jobs:\n  - reduce_sectors:\n      reduce:\n        - {topologies: [k2], sectors: [b11111], r: ", ToString[rTL$], ", s: ", ToString[sTL$],
   "}\n      select_integrals:\n        select_mandatory_list:\n          - \"KiraLoopIntegrals\"\n",
   "      preferred_masters: \"preferred\"\n      run_initiate: true\n      run_triangular: true\n      run_back_substitution: true\n",
   "      integral_ordering: 2\n  - kira2math:\n      target:\n       - [k2, \"KiraLoopIntegrals\"]\n"];
kiraDirTL$ = FileNameJoin[{workTL$, "kira"}];
KiraCreateIntegralFile[glisTL$, famTL$, kiraDirTL$];
KiraCreateConfigFiles[famTL$, glisTL$, kiraDirTL$, KiraMassDimensions -> {qq -> 2}];
Export[FileNameJoin[{kiraDirTL$, "k2", "preferred"}], StringRiffle[("k2[" <> StringRiffle[ToString /@ #, ","] <> "]") & /@ prefTL$, "\n"] <> "\n", "Text"];
Export[FileNameJoin[{kiraDirTL$, "k2", "job.yaml"}], jobTL$, "Text"];
kiraOKTL$ = KiraRunReduction[FileNameJoin[{kiraDirTL$, "k2"}], KiraBinaryPath -> kiraTL$, KiraFermatPath -> fermatTL$];
kiraTabTL$ = KiraImportResults["k2", kiraDirTL$];
Print["(d) Kira: ", kiraOKTL$, ", masters ", Union[Cases[Values[kiraTabTL$], _GLI, Infinity]]];


(* ::Subsubsection:: *)
(*Inspect: the number of reduction rules from Kira and the first one*)


If[$Notebooks,
  {Length[kiraTabTL$], First[kiraTabTL$]}
]


allGLITL$ = Union[Cases[Join[Values[kiraTabTL$], GLI["k2", #] & /@ prefTL$], _GLI, Infinity]];
symRulesTL$ = FCLoopFindIntegralMappings[allGLITL$, {famTL$}, PreferredIntegrals -> (GLI["k2", #] & /@ prefTL$)][[1]];
redTL$[x_] := Collect[x /. kiraTabTL$ /. symRulesTL$, _GLI, Together];
(* per diagram: K^2 Pi^(2)/g^4 and K^2 Pitilde^(2)/g^4 contributions *)

(* ::Section:: *)
(*(e) per-diagram values and their sum*)


piG$ = Table[Collect[(wGTL$[[i]] redTL$[gliGTL$[[i]]] /. gS -> 1) (I)^2/(I (D - 1) qq), _GLI, Factor], {i, Length[gliGTL$]}];
piC$ = Table[Collect[(wCTL$[[i]] redTL$[gliCTL$[[i]]] /. gS -> 1) (I)^2/(I qq), _GLI, Factor], {i, Length[gliCTL$]}];


(* ::Subsubsection:: *)
(*Inspect: gluon diagram 4, (c): K^2 Pi^(2)/g^4 in the two masters*)


If[$Notebooks,
  piG$[[4]]
]


ref$ = Get[FileNameJoin[{srcDirTL$, "results", "twoloop_reduction.m"}]];
Print["(e) sum of diagrams - Src/results/twoloop_reduction.m: gluon ", Simplify[Total[piG$] - ref$["Pi2"]], ", ghost ", Simplify[Total[piC$] - ref$["Pitilde2"]]];
Put[<|"gluon" -> Table[<|"descr" -> dG$[[i]], "weight" -> wGTL$[[i]], "gli" -> gliGTL$[[i]], "value" -> piG$[[i]]|>, {i, Length[piG$]}],
     "ghost" -> Table[<|"descr" -> dC$[[i]], "weight" -> wCTL$[[i]], "gli" -> gliCTL$[[i]], "value" -> piC$[[i]]|>, {i, Length[piC$]}]|>,
  FileNameJoin[{srcDirTL$, "results", "twoloop_perdiag.m"}]];
Print["(f) wrote results/twoloop_perdiag.m"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it releases libraries and temporary files.*)


Quiet[DeleteDirectory[modelTmpDirTL$, DeleteContents -> True]];
