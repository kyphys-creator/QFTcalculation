(* ::Package:: *)

(* ::Title:: *)
(*Step (16): two-loop self-energy in d = 4 (FeynArts + FeynCalc, IBP reduction with Kira 3.1 and FIRE 7.1)*)


(* ::Text:: *)
(*(a) FeynArts diagrams of the two-loop self-energy from Src/generated/Phi3_FA: all 10 diagrams, the 3 without tadpoles and the 2 one-particle-irreducible ones (kite and rainbow), each with symmetry factor 1/2.  The 7 diagrams with a tadpole contain a one-point subdiagram and are cancelled by the Y phi term of Eq. (1), order by order.*)
(*(b) The two amplitudes are mapped onto the integral family se2 = {q1^2-m^2, (q1-p)^2-m^2, q2^2-m^2, (q2-p)^2-m^2, (q1-q2)^2-m^2} by momentum shifts, checked as rational functions.  The insertion of the one-loop MS-bar mass counterterm delta_m = g^2/(32 Pi^2 eps) into the one-loop bubble gives an integral of se1 = {q^2-m^2, (q-p)^2-m^2}.  With the measure J = Integrate[d^Dq/(I Pi^(D/2)) ...] per loop (as in AMFlow) and mu-bar = m,*)
(*      Sigma^(2) = g^4/(16 Pi^2)^2 Shat,   Shat = (1/2) E^(2 eps EulerGamma) (J[se2,11111] + J[se2,21101]) - E^(eps EulerGamma)/(2 eps) J[se1,21].*)
(*(c) Both loop integrals are reduced with Kira 3.1 (Fermat 7.9b) and with FIRE 7.1 (start file from FIRE's Mathematica part with LiteRed), through FeynHelpers 2, with the same preferred master integrals: A^2, A B, the vacuum sunrise I, the sunrise S and T (one dot), the four-propagator U and the kite M.  FIRE keeps integrals that are equal by symmetry apart; FCLoopFindIntegralMappings maps them onto one another before the two tables are compared.*)
(*(d) Shat in terms of the masters (D = 4 - 2 eps) is written to Src/results/twoloop4_reduction.m for twoloop4_amflow.wl.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file twoloop4_feyncalc.wl  (run generate_Phi3.wl first; Kira, Fermat, FIRE paths below).  Interactive:  ~/hep/bin/wopen twoloop4_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.  The diagrams are shown before they are evaluated.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];

srcDirTL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
kiraTL$ = FileNameJoin[{$HomeDirectory, "hep", "Kira-3.1", "bin", "kira"}];
fermatTL$ = FileNameJoin[{$HomeDirectory, "hep", "fermat-7.9b", "fer64"}];
fireTL$ = FileNameJoin[{$HomeDirectory, "hep", "FIRE-7.1", "FIRE7"}];
kernelTL$ = FileNameJoin[{$HomeDirectory, "hep", "opt", "Wolfram142", "Contents", "MacOS", "WolframKernel"}];
workTL$ = FileNameJoin[{srcDirTL$, "work", "twoloop4"}];
(* a fresh working directory: Kira and FIRE reuse the databases of an earlier run *)
If[DirectoryQ[workTL$], DeleteDirectory[workTL$, DeleteContents -> True]];
CreateDirectory[workTL$, CreateIntermediateDirectories -> True];


(* ::Section:: *)
(*patched copy of the FeynRules-generated FeynArts model*)


modelTmpDirTL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirTL$, "generated", "Phi3_FA"}], FileNameJoin[{modelTmpDirTL$, "Phi3_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirTL$, "Phi3_FA"}], Quiet -> True];
modelTL$ = FileNameJoin[{modelTmpDirTL$, "Phi3_FA", "Phi3_FA"}];
insertTL$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles},
   Model -> modelTL$, GenericModel -> modelTL$];


(* ::Section:: *)
(*(a) diagrams*)


diagAllTL$ = insertTL$[CreateTopologies[2, 1 -> 1], {S[1]} -> {S[1]}];
diagNoTadTL$ = insertTL$[CreateTopologies[2, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {S[1]} -> {S[1]}];
diag1PITL$ = insertTL$[CreateTopologies[2, 1 -> 1, ExcludeTopologies -> {Tadpoles, Reducible}], {S[1]} -> {S[1]}];
diagTadTL$ = insertTL$[CreateTopologies[2, 1 -> 1, ExcludeTopologies -> {Reducible}], {S[1]} -> {S[1]}];


(* ::Subsubsection:: *)
(*Inspect: the two one-particle-irreducible diagrams (kite, rainbow) and all ten diagrams*)


If[$Notebooks,
  Column[{
    Row[Show[#, ImageSize -> 260] & /@ Render[Paint[diag1PITL$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]], "    "],
    Show[#, ImageSize -> 700] & /@ Render[Paint[diagAllTL$, ColumnsXRows -> {5, 2}, Numbering -> Simple, DisplayFunction -> Identity]]}, Spacings -> 2]
]


nAllTL$ = Length[CreateFeynAmp[diagAllTL$]];
nNoTadTL$ = Length[CreateFeynAmp[diagNoTadTL$]];
n1PITL$ = Length[CreateFeynAmp[diag1PITL$]];
Print["(a) number of two-loop self-energy diagrams: all ", nAllTL$, ", without tadpoles ", nNoTadTL$,
  ", without tadpoles and one-particle irreducible ", n1PITL$, "  (expect 10, 3, 2)"];
Print["(a) diagrams with a tadpole (a one-point subdiagram, cancelled by Y): ", nAllTL$ - nNoTadTL$, "  (expect 7)"];


ampTL$ = FCE[FCFAConvert[CreateFeynAmp[diag1PITL$, Truncated -> True, PreFactor -> 1],
    IncomingMomenta -> {p}, OutgoingMomenta -> {p}, LoopMomenta -> {q1, q2}, ChangeDimension -> D,
    List -> True, SMP -> False, DropSumOver -> True]];
Print["(a) kite    A = ", InputForm[ampTL$[[1]]]];
Print["(a) rainbow A = ", InputForm[ampTL$[[2]]]];


(* ::Section:: *)
(*(b) mapping onto the integral families*)


famTL$ = FCTopology["se2", {SFAD[{q1, m^2}], SFAD[{q1 - p, m^2}], SFAD[{q2, m^2}], SFAD[{q2 - p, m^2}], SFAD[{q1 - q2, m^2}]},
   {q1, q2}, {p}, {Hold[SPD][p] -> pp}, {}];
fam1TL$ = FCTopology["se1", {SFAD[{q1, m^2}], SFAD[{q1 - p, m^2}]}, {q1}, {p}, {Hold[SPD][p] -> pp}, {}];
(* kite: q1 -> -q1;  rainbow: q1 -> p - q1, q2 -> -q2 *)
shiftsTL$ = {{q1 -> -q1}, {q1 -> p - q1, q2 -> -q2}};
glisTL$ = {GLI["se2", {1, 1, 1, 1, 1}], GLI["se2", {2, 1, 1, 0, 1}]};
explTL$[x_] := Together[ExpandScalarProduct[FeynAmpDenominatorExplicit[FCI[x]]]];
mapCheckTL$ = Table[Simplify[explTL$[FCI[ampTL$[[i]] /. gphi -> 1] /. shiftsTL$[[i]]]*(2/I) -
     explTL$[FCLoopFromGLI[glisTL$[[i]], {famTL$}]]], {i, 2}];
Print["(b) amplitude - (I/2) g^4 J  after the shifts: ", mapCheckTL$, "  (expect {0, 0})"];

(* the counterterm insertion: (g^2/2) x 2 delta_m / D1 in the one-loop bubble = g^2 delta_m FAD[q1, q1, q1 - p] *)
ctCheckTL$ = Simplify[explTL$[FAD[{q1, m}, {q1, m}, {q1 - p, m}]] - explTL$[FCLoopFromGLI[GLI["se1", {2, 1}], {fam1TL$}]]];
Print["(b) counterterm insertion  FAD[q1,q1,q1-p] - J[se1,21]: ", ctCheckTL$, "  (expect 0)"];

shatTL$ = (1/2) E^(2 eps EulerGamma) (GLI["se2", {1, 1, 1, 1, 1}] + GLI["se2", {2, 1, 1, 0, 1}]) -
   E^(eps EulerGamma)/(2 eps) GLI["se1", {2, 1}];


(* ::Section:: *)
(*(c) IBP reduction with Kira and with FIRE*)


prefTL$ = {{1, 0, 1, 0, 0}, {1, 1, 1, 0, 0}, {1, 0, 1, 0, 1}, {0, 1, 1, 0, 1}, {0, 1, 1, 0, 2}, {1, 1, 1, 0, 1}, {1, 1, 1, 1, 1}};
pref1TL$ = {{1, 0}, {1, 1}};
mastersTL$ = Join[GLI["se2", #] & /@ prefTL$, GLI["se1", #] & /@ pref1TL$];
targetsTL$ = {glisTL$, {GLI["se1", {2, 1}]}};
(* the job files are written here: seeds up to r = 7 and s = 2 in the top sector (with r = 5, s = 0, as FeynHelpers derives from the
   targets, Kira keeps a third sunrise master) and the preferred masters *)
jobTL$[name_, top_, r_] := StringJoin["jobs:\n  - reduce_sectors:\n      reduce:\n        - {topologies: [", name, "], sectors: [b", top,
   "], r: ", ToString[r], ", s: 2}\n      select_integrals:\n        select_mandatory_list:\n          - \"KiraLoopIntegrals\"\n",
   "      preferred_masters: \"preferred\"\n      run_initiate: true\n      run_triangular: true\n      run_back_substitution: true\n",
   "      integral_ordering: 2\n  - kira2math:\n      target:\n       - [", name, ", \"KiraLoopIntegrals\"]\n"];
jobsTL$ = {jobTL$["se2", "11111", 7], jobTL$["se1", "11", 4]};
toposTL$ = {famTL$, fam1TL$};
namesTL$ = {"se2", "se1"};
prefListTL$ = {prefTL$, pref1TL$};


(* ::Subsubsection:: *)
(*Kira 3.1*)


kiraDirTL$ = FileNameJoin[{workTL$, "kira"}];
Do[
  KiraCreateIntegralFile[targetsTL$[[i]], toposTL$[[i]], kiraDirTL$];
  KiraCreateConfigFiles[toposTL$[[i]], targetsTL$[[i]], kiraDirTL$, KiraMassDimensions -> {m -> 1, pp -> 2}];
  With[{d = FileNameJoin[{kiraDirTL$, namesTL$[[i]]}]},
   Export[FileNameJoin[{d, "preferred"}], StringRiffle[(namesTL$[[i]] <> "[" <> StringRiffle[ToString /@ #, ","] <> "]") & /@ prefListTL$[[i]], "\n"] <> "\n", "Text"];
   Export[FileNameJoin[{d, "job.yaml"}], jobsTL$[[i]], "Text"]];
  kiraOK$[i] = KiraRunReduction[FileNameJoin[{kiraDirTL$, namesTL$[[i]]}], KiraBinaryPath -> kiraTL$, KiraFermatPath -> fermatTL$],
  {i, 2}];
kiraTabTL$ = Join[KiraImportResults["se2", kiraDirTL$], KiraImportResults["se1", kiraDirTL$]];
Print["(c) Kira runs succeeded: ", {kiraOK$[1], kiraOK$[2]}, "; masters in the Kira tables: ",
  Union[Cases[Values[kiraTabTL$], _GLI, Infinity]]];


(* ::Subsubsection:: *)
(*FIRE 7.1*)


fireDirTL$ = FileNameJoin[{workTL$, "fire"}];
Do[
  FIREPrepareStartFile[toposTL$[[i]], fireDirTL$, FIREPath -> FileNameJoin[{fireTL$, "FIRE7.m"}]];
  fireStart$[i] = FIRECreateStartFile[fireDirTL$, toposTL$[[i]], FIREMathematicaKernelPath -> kernelTL$];
  FIRECreateIntegralFile[targetsTL$[[i]], toposTL$[[i]], fireDirTL$];
  (* FIRE 7.1 was built without zstd; preferred masters as {{problem id, indices}, ...} *)
  With[{cfg = FIRECreateConfigFile[toposTL$[[i]], fireDirTL$, FIRECompressor -> "lz4"], d = FileNameJoin[{fireDirTL$, namesTL$[[i]]}]},
   Export[FileNameJoin[{d, namesTL$[[i]] <> ".preferred"}], ToString[{4242, #} & /@ prefListTL$[[i]], InputForm], "Text"];
   Export[cfg, StringReplace[Import[cfg, "Text"], "#lbases" -> "#preferred " <> namesTL$[[i]] <> ".preferred\n#lbases"], "Text"]];
  fireOK$[i] = FIRERunReduction[FileNameJoin[{fireDirTL$, namesTL$[[i]]}], FIREBinaryPath -> FileNameJoin[{fireTL$, "bin", "FIRE7"}]],
  {i, 2}];
fireTabTL$ = Join[FIREImportResults["se2", fireDirTL$], FIREImportResults["se1", fireDirTL$]];
Print["(c) FIRE start files and runs succeeded: ", {fireStart$[1], fireStart$[2], fireOK$[1], fireOK$[2]},
  "; masters in the FIRE tables: ", Union[Cases[Values[fireTabTL$], _GLI, Infinity]]];


(* ::Subsubsection:: *)
(*Kira against FIRE: map integrals that are equal by symmetry, then compare*)


allGLITL$ = Union[Cases[Join[Values[kiraTabTL$], Values[fireTabTL$], mastersTL$], GLI["se2", _], Infinity]];
allGLI1TL$ = Union[Cases[Join[Values[kiraTabTL$], Values[fireTabTL$], mastersTL$], GLI["se1", _], Infinity]];
symRulesTL$ = Join[
   FCLoopFindIntegralMappings[allGLITL$, {famTL$}, PreferredIntegrals -> (GLI["se2", #] & /@ prefTL$)][[1]],
   FCLoopFindIntegralMappings[allGLI1TL$, {fam1TL$}, PreferredIntegrals -> (GLI["se1", #] & /@ pref1TL$)][[1]]];
Print["(c) symmetry mappings among the integrals: ", InputForm[symRulesTL$]];
redKiraTL$ = (# /. kiraTabTL$ /. symRulesTL$) & /@ Flatten[targetsTL$];
redFireTL$ = (# /. fireTabTL$ /. symRulesTL$) & /@ Flatten[targetsTL$];
diffTL$ = Simplify[redKiraTL$ - redFireTL$];
Print["(c) Kira - FIRE for J[se2,11111], J[se2,21101], J[se1,21]: ", diffTL$, "  (expect {0, 0, 0})"];
Print["(c) masters after the mappings: ", Union[Cases[Join[redKiraTL$, redFireTL$], _GLI, Infinity]]];


(* ::Subsubsection:: *)
(*Inspect: the reduction of the rainbow J[se2,21101] (Kira, after the symmetry mappings)*)


If[$Notebooks, TraditionalForm[Collect[redKiraTL$[[2]], _GLI, Simplify]]]


(* ::Section:: *)
(*(d) Shat in terms of the masters*)


shatMastersTL$ = Collect[shatTL$ /. Thread[Flatten[targetsTL$] -> redKiraTL$] /. {D -> 4 - 2 eps}, _GLI, Simplify];
Print["(d) masters of Shat: ", Union[Cases[shatMastersTL$, _GLI, Infinity]]];
Print["(d) Shat = ", InputForm[shatMastersTL$]];
Put[shatMastersTL$, FileNameJoin[{srcDirTL$, "results", "twoloop4_reduction.m"}]];
Print["(d) wrote Src/results/twoloop4_reduction.m"];


(* ::Subsubsection:: *)
(*Inspect: Shat in terms of the masters*)


If[$Notebooks, TraditionalForm[shatMastersTL$]]


(* ::Section:: *)
(*Cleanup*)


Quiet[DeleteDirectory[modelTmpDirTL$, DeleteContents -> True]];
