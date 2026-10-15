(* ::Package:: *)

(* ::Title:: *)
(*Step (8): R from the optical theorem -- the photon self-energy at one and two loops with a massless and a massive quark (FeynArts + FeynCalc, Kira 3.1)*)


(* ::Text:: *)
(*Research note models/qcd, step (8).  sigma(e+ e- -> q qbar (g)) is proportional to Im Pi_gamma(s + i0) (Eq. (rmass)), so at O(alpha_s)*)
(*    Delta^(1) = Im Pi^(2)/(4 C_F a Im Pi^(1))   (R = R_0 [1 + C_F (alpha_s/pi) Delta^(1)], alpha_s/pi = 4 a),*)
(*where Pi^(2) is the photon self-energy with one gluon (three diagrams: two quark self-energy insertions and the vertex) -- its two- and*)
(*three-particle cuts are the virtual and real corrections.  The quark field and vertex counterterms cancel (Ward identity), the QCD coupling*)
(*is not renormalized at this order, and the photon field counterterm is a real constant, so Im Pi^(2) is finite.  For the massive quark the*)
(*pole mass needs the on-shell mass counterterm: Pi^(2) + delta_m d Pi^(1)/dm, delta_m = -C_F a (D-1)(D-2) A0(m^2)/(2 (D-3) m) (m_bare = m + delta_m).*)
(*(a) FeynArts diagrams (one flavour; the photon-exchange diagrams dropped), Feynman gauge, g_{mu nu} contraction, the loop momenta shifted*)
(*    onto k2 = {l1^2, l2^2, (l1-q)^2, (l2-q)^2, (l1-l2)^2} (massless u) and k2m = the same with m on the four quark lines (t); the one-loop*)
(*    functions on k1 = {l1^2, (l1-q)^2} and k1m.  FCFAConvert drops the colour sum of the closed quark loop at one loop (SumOver): N = C_A*)
(*    is put back by hand (at two loops SUNSimplify gives C_F C_A from the trace).*)
(*(b) Kira reduces all integrals: k2 to sunset and bubble^2, k2m to five masters, k1m to A0 and B0.*)
(*(c) the massless case exactly: one loop  Im Pi^(1) -> (Im of (-s - i0)^(-eps) B0), two loops with the exact masters of step (7); Delta^(1) = 3/4.*)
(*(d) the massive reduction -> results/ee_optical_reduction.m for ee_amflow.wl.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file ee_optical.wl  (after generate_QCD.wl; about 2 minutes).  Interactive:  ~/hep/bin/wopen ee_optical.wl, then "Run All Code"; the cells under "Inspect" headings run only in the notebook.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirOP$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
kiraOP$ = FileNameJoin[{$HomeDirectory, "hep", "Kira-3.1", "bin", "kira"}];
fermatOP$ = FileNameJoin[{$HomeDirectory, "hep", "fermat-7.9b", "fer64"}];
workOP$ = FileNameJoin[{srcDirOP$, "work", "ee_optical"}];
If[DirectoryQ[workOP$], DeleteDirectory[workOP$, DeleteContents -> True]];
CreateDirectory[workOP$, CreateIntermediateDirectories -> True];
modelTmpDirOP$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOP$, "generated", "QCD_FA"}], FileNameJoin[{modelTmpDirOP$, "QCD_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOP$, "QCD_FA"}], Quiet -> True];
modelOP$ = FileNameJoin[{modelTmpDirOP$, "QCD_FA", "QCD_FA"}];
ep = Epsilon;
allQOP$ = {F[1], F[2], F[3], F[4], F[5], F[6], F[7]};
insOP$[loops_, fl_] := InsertFields[CreateTopologies[loops, 1 -> 1, ExcludeTopologies -> {Tadpoles, Reducible}], {V[1]} -> {V[1]},
   InsertionLevel -> {Particles}, Model -> modelOP$, GenericModel -> modelOP$, ExcludeParticles -> Complement[allQOP$, {fl}]];
convOP$[d_, loops_] := FCFAConvert[CreateFeynAmp[d, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
    IncomingMomenta -> {q}, OutgoingMomenta -> {q}, LoopMomenta -> loops, LorentzIndexNames -> {mu, nu}, ChangeDimension -> D,
    List -> True, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI //
   ReplaceAll[#, {SMP["g_s"] -> gS, FCGV["GS"] -> gS, GaugeXi[V[2, ___]] -> 1, GaugeXi[G] -> 1, GaugeXi[V[1, ___]] -> 1, GaugeXi[A] -> 1,
      SMP["e"] -> 1, FCGV["EL"] -> 1, FCGV["MT"] -> mt, SMP["m_t"] -> mt}] &;
algOP$[x_] := Module[{y = x},
   y = DiracSimplify[y /. DiracTrace[z_] :> DiracTrace[z, DiracTraceEvaluate -> True]];
   y = SUNSimplify[y, SUNNToCACF -> True];
   y = y /. {SUNDelta[__] -> 1, SUNFDelta[__] -> 1, SD[__] -> 1, SDF[__] -> 1};
   ExpandScalarProduct[Contract[y]]];
canonOP$[k_] := Module[{e = Expand[k]}, If[OrderedQ[{e, Expand[-e]}], e, Expand[-e]]];
FCClearScalarProducts[];
SPD[q, q] = qq;


(* ::Section:: *)
(*(a) diagrams and integral families*)


d1uOP$ = insOP$[1, F[2]]; d2uOP$ = insOP$[2, F[2]]; d1tOP$ = insOP$[1, F[7]]; d2tOP$ = insOP$[2, F[7]];


(* ::Subsubsection:: *)
(*Inspect: the two-loop photon self-energy diagrams with the u quark (those with a gluon are kept)*)


If[$Notebooks, Show[#, ImageSize -> 600] & /@ Render[Paint[d2uOP$, ColumnsXRows -> {6, 1}, Numbering -> Simple, DisplayFunction -> Identity]]]


a2uOP$ = Select[convOP$[d2uOP$, {l1, l2}], !FreeQ[#, gS] &];
a2tOP$ = Select[convOP$[d2tOP$, {l1, l2}], !FreeQ[#, gS] &];
a1uOP$ = Total[convOP$[d1uOP$, {l1}]]; a1tOP$ = Total[convOP$[d1tOP$, {l1}]];
Print["(a) two-loop photon self-energy diagrams: u ", Length[CreateFeynAmp[d2uOP$]], " (with a gluon ", Length[a2uOP$], "), t ",
  Length[CreateFeynAmp[d2tOP$]], " (", Length[a2tOP$], ")  (expect 6 (3), 6 (3))"];
(* the shift onto a family with masses: propagators {canonical momentum, mass} *)
momsOP$ = {l1, l2, l1 - q, l2 - q, l1 - l2};
matsOP$ = Select[Tuples[{-1, 0, 1}, 4], Abs[#[[1]] #[[4]] - #[[2]] #[[3]]] == 1 &];
candsOP$ = Flatten[Table[{l1 -> m[[1]] l1 + m[[2]] l2 + c1 q, l2 -> m[[3]] l1 + m[[4]] l2 + c2 q}, {m, matsOP$}, {c1, -1, 1}, {c2, -1, 1}], 2];
propsOP$[x_] := Union[Cases[FCE[x], FAD[a__] :> Sequence @@ ({canonOP$[#[[1]]], #[[2]]} & /@ (If[ListQ[#], #, {#, 0}] & /@ {a})), Infinity]];
toFamOP$[amp_, masses_, name_, loops_] := Module[{famSet, sh, spR, denR, y, cr, n = Length[masses], moms = If[loops == 1, {l1, l1 - q}, momsOP$]},
   famSet = Transpose[{canonOP$ /@ moms, masses}];
   sh = If[loops == 1, {}, SelectFirst[candsOP$, Function[c, SubsetQ[famSet, {canonOP$[#[[1]] /. c], #[[2]]} & /@ propsOP$[amp]]], $Failed]];
   If[sh === $Failed, Print["   no shift for ", propsOP$[amp]]; Return[$Failed]];
   spR = If[loops == 1,
     {SPD[l1, l1] -> d[1] + masses[[1]]^2, SPD[l1, q] -> (d[1] + masses[[1]]^2 + qq - d[2] - masses[[2]]^2)/2, SPD[q, l1] -> (d[1] + masses[[1]]^2 + qq - d[2] - masses[[2]]^2)/2},
     {SPD[l1, l1] -> d[1] + masses[[1]]^2, SPD[l2, l2] -> d[2] + masses[[2]]^2,
      SPD[l1, q] -> (d[1] + masses[[1]]^2 + qq - d[3] - masses[[3]]^2)/2, SPD[q, l1] -> (d[1] + masses[[1]]^2 + qq - d[3] - masses[[3]]^2)/2,
      SPD[l2, q] -> (d[2] + masses[[2]]^2 + qq - d[4] - masses[[4]]^2)/2, SPD[q, l2] -> (d[2] + masses[[2]]^2 + qq - d[4] - masses[[4]]^2)/2,
      SPD[l1, l2] -> (d[1] + masses[[1]]^2 + d[2] + masses[[2]]^2 - d[5] - masses[[5]]^2)/2, SPD[l2, l1] -> (d[1] + masses[[1]]^2 + d[2] + masses[[2]]^2 - d[5] - masses[[5]]^2)/2}];
   denR = FAD[a__] :> Times @@ (Module[{pm = If[ListQ[#], #, {#, 0}]}, 1/d[First[FirstPosition[famSet, {canonOP$[pm[[1]]], pm[[2]]}]]]] & /@ {a});
   y = FCE[algOP$[Contract[FCI[FCE[amp] /. sh] MTD[mu, nu]]]] /. denR /. spR;
   If[!FreeQ[y, l1 | l2], Print["   loop momentum left"]];
   cr = CoefficientRules[Expand[y Product[d[i]^4, {i, n}]], Array[d, n]];
   Total[(Factor[#[[2]]] GLI[name, 4 - #[[1]]]) & /@ cr]];
g2uOP$ = Total[toFamOP$[#, {0, 0, 0, 0, 0}, "k2", 2] & /@ a2uOP$];
g2tOP$ = Total[toFamOP$[#, {mt, mt, mt, mt, 0}, "k2m", 2] & /@ a2tOP$];
g1uOP$ = toFamOP$[a1uOP$, {0, 0}, "k1", 1];
g1tOP$ = toFamOP$[a1tOP$, {mt, mt}, "k1m", 1];
(* d/dm of the t loop: the explicit m and 1/(l^2 - m^2)^a -> 2 a m/(l^2 - m^2)^(a+1) *)
dg1tOP$ = Expand[(g1tOP$ /. GLI["k1m", {n1_, n2_}] :> 2 mt (If[n1 > 0, n1 GLI["k1m", {n1 + 1, n2}], 0] + If[n2 > 0, n2 GLI["k1m", {n1, n2 + 1}], 0])) +
    (D[g1tOP$ /. GLI -> glOP$, mt] /. glOP$ -> GLI)];
Print["(a) integrals: k2 ", Length[Union[Cases[g2uOP$, _GLI, Infinity]]], ", k2m ", Length[Union[Cases[g2tOP$, _GLI, Infinity]]],
  ", k1m ", Length[Union[Cases[{g1tOP$, dg1tOP$}, _GLI, Infinity]]]];


(* ::Subsubsection:: *)
(*Inspect: the one-loop photon self-energy (g-contracted, one colour)*)


If[$Notebooks, TableForm[{{"u", TraditionalForm[g1uOP$]}, {"t", TraditionalForm[g1tOP$]}}]]


(* ::Section:: *)
(*(b) IBP reduction with Kira*)


runKiraOP$[name_, props_, loops_, glis_, pref_, md_] := Module[{fam = FCTopology[name, props, loops, {q}, {Hold[SPD][q] -> qq}, {}], kdir = FileNameJoin[{workOP$, "kira_" <> name}], r, s, job, ok, tab},
   CreateDirectory[kdir];
   r = Max[Total[Select[#[[2]], Positive]] & /@ glis]; s = Max[-Total[Select[#[[2]], Negative]] & /@ glis];
   job = StringJoin["jobs:\n  - reduce_sectors:\n      reduce:\n        - {topologies: [", name, "], sectors: [b", StringJoin[Table["1", Length[props]]], "], r: ", ToString[r], ", s: ", ToString[s],
     "}\n      select_integrals:\n        select_mandatory_list:\n          - \"KiraLoopIntegrals\"\n",
     If[pref === {}, "", "      preferred_masters: \"preferred\"\n"], "      run_initiate: true\n      run_triangular: true\n      run_back_substitution: true\n",
     "      integral_ordering: 2\n  - kira2math:\n      target:\n       - [", name, ", \"KiraLoopIntegrals\"]\n"];
   KiraCreateIntegralFile[glis, fam, kdir];
   KiraCreateConfigFiles[fam, glis, kdir, KiraMassDimensions -> md];
   If[pref =!= {}, Export[FileNameJoin[{kdir, name, "preferred"}], StringRiffle[(name <> "[" <> StringRiffle[ToString /@ #, ","] <> "]") & /@ pref, "\n"] <> "\n", "Text"]];
   Export[FileNameJoin[{kdir, name, "job.yaml"}], job, "Text"];
   ok = KiraRunReduction[FileNameJoin[{kdir, name}], KiraBinaryPath -> kiraOP$, KiraFermatPath -> fermatOP$];
   tab = KiraImportResults[name, kdir];
   Print["(b) ", name, ": Kira ", ok, ", masters ", Union[Cases[Values[tab], _GLI, Infinity]]];
   tab];
tabK2OP$ = runKiraOP$["k2", {SFAD[l1], SFAD[l2], SFAD[l1 - q], SFAD[l2 - q], SFAD[l1 - l2]}, {l1, l2}, Union[Cases[g2uOP$, _GLI, Infinity]], {{1, 0, 0, 1, 1}, {1, 1, 1, 1, 0}}, {qq -> 2}];
tabK2mOP$ = runKiraOP$["k2m", {SFAD[{l1, mt^2}], SFAD[{l2, mt^2}], SFAD[{l1 - q, mt^2}], SFAD[{l2 - q, mt^2}], SFAD[l1 - l2]}, {l1, l2}, Union[Cases[g2tOP$, _GLI, Infinity]], {}, {qq -> 2, mt -> 1}];
tabK1mOP$ = runKiraOP$["k1m", {SFAD[{l1, mt^2}], SFAD[{l1 - q, mt^2}]}, {l1}, Union[Cases[{g1tOP$, dg1tOP$}, _GLI, Infinity]], {}, {qq -> 2, mt -> 1}];
r2uOP$ = Collect[g2uOP$ /. tabK2OP$, _GLI, Factor]; r2tOP$ = Collect[g2tOP$ /. tabK2mOP$, _GLI, Factor];
r1tOP$ = Collect[g1tOP$ /. tabK1mOP$, _GLI, Factor]; dr1tOP$ = Collect[dg1tOP$ /. tabK1mOP$, _GLI, Factor];


(* ::Section:: *)
(*(c) the massless case: Delta^(1) = 3/4*)


(* ::Text:: *)
(*Pi = (i a)^L x (amplitude)/(i (D-1) qq) (calibrated in step (7)); at q^2 = s = mu^2 = 1 + i0, (-s - i0)^x = e^(-i pi x).*)


gOP$[a_, b_] := Gamma[a + b - D/2] Gamma[D/2 - a] Gamma[D/2 - b]/(Gamma[a] Gamma[b] Gamma[D - a - b]);
phOP$[x_] := Exp[-I Pi x];
v1OP$ = {GLI["k1", {1, 1}] -> E^(ep EulerGamma) gOP$[1, 1] phOP$[-ep], GLI["k1", {n1_, n2_}] /; n1 <= 0 || n2 <= 0 :> 0};
v2OP$ = {GLI["k2", {1, 1, 1, 1, 0}] -> E^(2 ep EulerGamma) gOP$[1, 1]^2 phOP$[-2 ep], GLI["k2", {1, 0, 0, 1, 1}] -> -E^(2 ep EulerGamma) gOP$[1, 1] gOP$[ep, 1] phOP$[1 - 2 ep]};
p1uOP$ = CA (g1uOP$ /. v1OP$) I/(I (D - 1) qq) /. qq -> 1 /. D -> 4 - 2 ep;
p2uOP$ = (r2uOP$ /. v2OP$) (I)^2/(I (D - 1) qq) /. gS -> 1 /. qq -> 1 /. D -> 4 - 2 ep;
p1uSerOP$ = Collect[FullSimplify[Normal[Series[p1uOP$, {ep, 0, 0}]]], ep];
p2uSerOP$ = Collect[FullSimplify[Normal[Series[p2uOP$, {ep, 0, 0}]]], ep];
Print["(c) u: Pi^(1) = ", InputForm[p1uSerOP$], "  (pole: -(4/3) N_c Q^2/eps with Q = 2/3)"];
Print["(c) u: Pi^(2)/a = ", InputForm[p2uSerOP$], "  (single pole only: the subdivergences cancel)"];
delta1uOP$ = FullSimplify[Coefficient[ComplexExpand[Im[p2uSerOP$]], ep, 0]/(4 CF Coefficient[ComplexExpand[Im[p1uSerOP$]], ep, 0])];
Print["(c) Delta^(1) = Im Pi^(2)/(4 C_F a Im Pi^(1)) = ", delta1uOP$, "  (expect 3/4: R = R_0 (1 + alpha_s/pi) in SU(3))"];


(* ::Section:: *)
(*(d) output*)


Put[<|"A1t" -> r1tOP$, "dA1t" -> dr1tOP$, "A2t" -> r2tOP$, "Delta1_massless" -> delta1uOP$|>, FileNameJoin[{srcDirOP$, "results", "ee_optical_reduction.m"}]];
Print["(d) wrote results/ee_optical_reduction.m (masters ", Union[Cases[{r1tOP$, dr1tOP$, r2tOP$}, _GLI, Infinity]], ")"];
Quiet[DeleteDirectory[modelTmpDirOP$, DeleteContents -> True]];
