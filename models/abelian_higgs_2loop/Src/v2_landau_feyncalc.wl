(* ::Package:: *)

(* ::Title:: *)
(*Step (1): the two-loop effective potential in Landau gauge from the Feynman diagrams (abelian Higgs model)*)


(* ::Text:: *)
(*Research note models/abelian_higgs_2loop, step (1).  Background field phi, Phi = (phi + h + i G)/sqrt 2, masses*)
(*    xh = -m2 + 3 lam phi^2,  xg = -m2 + lam phi^2,  xa = e^2 phi^2,*)
(*Landau gauge (vector propagator transverse, ghosts massless and decoupled), MS-bar at the scale Q.*)
(*  (a) FeynArts: the two-loop vacuum diagrams (one-particle irreducible) from the FeynRules model of the one-loop note*)
(*      (models/abelian_higgs/Src/generated/AbelianHiggs_FA), in a patched copy where the Goldstone boson has its own*)
(*      mass MG (its Landau-gauge mass xg; the model gives it sqrt(xi) MA) and GaugeXi -> 0;*)
(*  (b) FeynCalc: Lorentz algebra, partial fractions, integral families (FCLoopFindTopologies, mappings, basis*)
(*      completion);*)
(*  (c) Kira 3.1 (through FeynHelpers): reduction to the masters (products of tadpoles and vacuum sunsets);*)
(*  (d) the bare diagrams plus the one-loop counterterm insertions (Landau-gauge MS-bar constants of the one-loop note at*)
(*      xi = 0), expanded with TSIL's "bold" forms of the masters (Minkowski -> Euclidean; per loop*)
(*      16 pi^2 mu^(2 eps) d^Dk/(2 pi)^D):*)
(*          t(x) = -x/eps + A(x) + eps Aeps(x),   A(x) = x (ln(x/Q^2) - 1),   Aeps(x) = x (-1 - z2/2 + L - L^2/2),*)
(*          s(x,y,z) = -(x+y+z)/(2 eps^2) + (A(x)+A(y)+A(z) - (x+y+z)/2)/eps*)
(*                     + I(x,y,z) - ((x+y+z)(1 + z2) + A(x)^2/x + A(y)^2/y + A(z)^2/z)/2;*)
(*      the 1/eps^2 and 1/eps parts must be local (no A, I left) and the finite part must equal Martin's general*)
(*      Landau-gauge formula (hep-ph/0111209) with the couplings of the model (Eq. (V2) of the note);*)
(*  (e) results/v2_landau.m: V2 (coefficient of 1/(16 pi^2)^2) in A[x], I[x,y,z].*)
(*Batch: wolframscript -file v2_landau_feyncalc.wl*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$NumberMarks = False;

srcDirVL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirVL$ = FileNameJoin[{srcDirVL$, "results"}];
kiraVL$ = FileNameJoin[{$HomeDirectory, "hep", "Kira-3.1", "bin", "kira"}];
fermatVL$ = FileNameJoin[{$HomeDirectory, "hep", "fermat-7.9b", "fer64"}];
workVL$ = FileNameJoin[{srcDirVL$, "work", "v2_landau"}];
(* a fresh working directory: Kira reuses the databases of an earlier run *)
If[DirectoryQ[workVL$], DeleteDirectory[workVL$, DeleteContents -> True]];
CreateDirectory[workVL$, CreateIntermediateDirectories -> True];


(* ::Section:: *)
(*(a) diagrams*)


(* patched copy of the FeynRules model of the one-loop note: FeynCalc's FeynArts patch, and the Goldstone mass MG *)
modelSrcVL$ = FileNameJoin[{srcDirVL$, "..", "..", "abelian_higgs", "Src", "generated", "AbelianHiggs_FA"}];
modelTmpVL$ = CreateDirectory[];
CopyDirectory[modelSrcVL$, FileNameJoin[{modelTmpVL$, "AbelianHiggs_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpVL$, "AbelianHiggs_FA"}], Quiet -> True];
With[{mf = FileNameJoin[{modelTmpVL$, "AbelianHiggs_FA", "AbelianHiggs_FA.mod"}],
   g = "PropagatorLabel -> \"G\",\n    PropagatorType -> ScalarDash,\n    PropagatorArrow -> None,\n    Mass -> "},
  Module[{s = Import[mf, "Text"]},
   If[StringCount[s, g <> "MA"] =!= 1, Print["ERROR: Goldstone mass entry not found"]; Exit[1]];
   Export[mf, StringReplace[s, g <> "MA" -> g <> "MG"], "Text"]]];
modelVL$ = FileNameJoin[{modelTmpVL$, "AbelianHiggs_FA", "AbelianHiggs_FA"}];

topsVL$ = CreateTopologies[2, 0 -> 0, ExcludeTopologies -> {Reducible}];
insVL$ = InsertFields[topsVL$, {} -> {}, InsertionLevel -> {Particles}, Model -> modelVL$, GenericModel -> modelVL$];
fampVL$ = CreateFeynAmp[insVL$, GaugeRules -> {}];
Print["(a) one-particle-irreducible two-loop vacuum diagrams: ", Length[fampVL$], "  (expect 10)"];


(* ::Subsubsection:: *)
(*Inspect: the diagrams*)


If[$Notebooks, Paint[insVL$, ColumnsXRows -> {5, 2}, Numbering -> Simple]]


(* ::Section:: *)
(*(b) Lorentz algebra and integral families*)


(* FeynArts writes 1/(2 pi)^4 per loop; the measure d^Dk/(2 pi)^D per loop is kept implicit.  Landau gauge: the Goldstone
   propagator 1/(k^2 - MG^2) (the model writes sqrt(GaugeXi) MG), then GaugeXi -> 0.  Lower-case mass symbols for Kira. *)
ampVL$ = FCFAConvert[fampVL$, LoopMomenta -> {q1, q2}, ChangeDimension -> D, List -> True, SMP -> False,
     DropSumOver -> True] /. FCGV[x_String] :> ToExpression[x];
ampVL$ = ampVL$ /. MG Sqrt[GaugeXi[A]] -> MG /. GaugeXi[A] -> 0 /. {gc9 -> EL};
ampVL$ = (2 Pi)^8 ampVL$ /. {MH -> mh, MG -> mg, MA -> ma, EL -> el, vev -> phi};
ampVL$ = Expand[FCE[Contract[#]]] & /@ ampVL$;
Print["(b) diagrams that vanish (expect 1, the ghost loop): ", Count[ampVL$, 0]];
(* the potential is minus the sum of the amplitudes: V2 = i x (vacuum graphs) and FeynArts' amplitude is -i x graph *)
v2IntVL$ = -Total[ampVL$];

apVL$ = ApartFF[v2IntVL$, {q1, q2}, FCE -> True];
{expTVL$, toposVL$} = FCLoopFindTopologies[apVL$, {q1, q2}, Names -> "v"];
mapVL$ = FCLoopFindTopologyMappings[toposVL$];
(* complete the families that lack a propagator (renamed "...C"), as in FeynCalc's example B-EtaC *)
incVL$ = Select[mapVL$[[2]], FCLoopBasisIncompleteQ];
compIncVL$ = FCLoopBasisFindCompletion[incVL$];
compRulesVL$ = Flatten[FCLoopCreateRuleGLIToGLI[compIncVL$, List /@ incVL$]];
compVL$ = mapVL$[[2]] /. Thread[incVL$ -> compIncVL$];
glExpVL$ = FCLoopApplyTopologyMappings[expTVL$ /. compRulesVL$, {mapVL$[[1]] /. compRulesVL$, compVL$}];
glisVL$ = Union[Cases[glExpVL$, _GLI, Infinity]];
Print["(b) families after the mappings: ", Length[compVL$], ";  integrals to reduce: ", Length[glisVL$]];


(* ::Section:: *)
(*(c) reduction with Kira*)


kiraDirVL$ = FileNameJoin[{workVL$, "kira"}];
redVL$ = {};
Do[Module[{name = topo[[1]], targets, d, ok, pref, n},
    targets = Select[glisVL$, #[[1]] === name &];
    If[targets === {}, Continue[]];
    n = Length[topo[[2]]];
    (* preferred masters: no dots, at most one propagator removed *)
    pref = Select[Tuples[{0, 1}, n], Total[#] >= n - 1 &];
    KiraCreateIntegralFile[targets, topo, kiraDirVL$];
    KiraCreateConfigFiles[topo, targets, kiraDirVL$, KiraMassDimensions -> {mh -> 1, mg -> 1, ma -> 1}];
    d = FileNameJoin[{kiraDirVL$, ToString[name]}];
    Export[FileNameJoin[{d, "preferred"}],
     StringRiffle[(ToString[name] <> "[" <> StringRiffle[ToString /@ #, ","] <> "]") & /@ pref, "\n"] <> "\n", "Text"];
    Export[FileNameJoin[{d, "job.yaml"}], StringJoin["jobs:\n  - reduce_sectors:\n      reduce:\n        - {topologies: [",
       ToString[name], "], sectors: [b", StringJoin[ToString /@ ConstantArray[1, n]], "], r: ", ToString[n],
       ", s: 3}\n      select_integrals:\n        select_mandatory_list:\n          - \"KiraLoopIntegrals\"\n",
       "      preferred_masters: \"preferred\"\n      run_initiate: true\n      run_triangular: true\n      run_back_substitution: true\n",
       "      integral_ordering: 2\n  - kira2math:\n      target:\n       - [", ToString[name], ", \"KiraLoopIntegrals\"]\n"], "Text"];
    ok = KiraRunReduction[d, KiraBinaryPath -> kiraVL$, KiraFermatPath -> fermatVL$];
    If[ok =!= True, Print["ERROR: Kira failed for ", name]; Exit[1]];
    redVL$ = Join[redVL$, KiraImportResults[ToString[name], kiraDirVL$]]],
  {topo, compVL$}];
v2RedVL$ = glExpVL$ /. FCGV["GLIProduct"] -> Times /. Dispatch[redVL$];
mastVL$ = Union[Cases[v2RedVL$, _GLI, Infinity]];
Print["(c) masters after the reduction: ", Length[mastVL$], ";  any with dots or numerators: ",
  Select[mastVL$, Max[#[[2]]] > 1 || Min[#[[2]]] < 0 &]];
Print["(c) factors with D in the denominators of the coefficients (expect none at D = 4): ",
  Union[Select[Flatten[FactorList[Denominator[Together[Coefficient[v2RedVL$, #]]]][[All, 1]] & /@ mastVL$], !FreeQ[#, D] &]]];


(* ::Section:: *)
(*(d) renormalization and comparison with Martin's formula*)


(* the masses on the propagators of a master: Minkowski integral -> TSIL bold form (coefficient of 1/(16 pi^2)^2) *)
propMassVL$[topo_FCTopology] := topo[[2]] /. FeynAmpDenominator[StandardPropagatorDenominator[_, 0, mm_, {1, 1}]] :> -mm;
masterBoldVL$[GLI[name_, idx_]] := Module[{topo = Select[compVL$, #[[1]] === name &][[1]], ms, on},
   ms = propMassVL$[topo];
   on = Pick[ms, idx, 1];
   Switch[Length[on],
    2, -tB[on[[1]]] tB[on[[2]]],          (* (-i T)(-i T) *)
    3, sB @@ Sort[on],                    (* i^2 (-1)^3 S_E *)
    _, Print["ERROR: unexpected master ", GLI[name, idx]]; Abort[]]];
tB[0] = 0;
boldVL$ = {tB[x_] :> -x/eps + A[x] + eps Aeps[x],
   sB[x_, y_, z_] :> -(x + y + z)/(2 eps^2) + (A[x] + A[y] + A[z] - (x + y + z)/2)/eps + II[x, y, z] -
      ((x + y + z) (1 + z2) + Total[If[# === 0, 0, A[#]^2/#] & /@ {x, y, z}])/2};

v2BareVL$ = v2RedVL$ /. GLI[n_, i_] :> masterBoldVL$[GLI[n, i]] /. D -> 4 - 2 eps;
Print["(d) bare two-loop part in t(x) and s(x,y,z): ", InputForm[Collect[Expand[v2BareVL$], {_tB, _sB}, Factor]]];
(* one-loop counterterm insertions, Landau gauge (xi = 0): dZ_Phi = 3 e^2, dZ_A = -e^2/3, d_m2 = 4 lam - 3 e^2,
   d_lam = 10 lam - 6 e^2 + 3 e^4/lam, all times 1/(16 pi^2 eps):
   (1/2) X_h t(xh) + (1/2) X_g t(xg) + (1/2)(D - 1) xa (dZ_Phi - dZ_A) t(xa) *)
ctVL$ = With[{ch = -m2 (4 lam - 3 el^2) + 3 lam phi^2 (10 lam - 3 el^2 + 3 el^4/lam),
     cg = -m2 (4 lam - 3 el^2) + lam phi^2 (10 lam - 3 el^2 + 3 el^4/lam)},
   (ch/2 tB[mh^2] + cg/2 tB[mg^2] + (3 - 2 eps)/2 (10/3) el^2 ma^2 tB[ma^2])/eps];
totVL$ = v2BareVL$ + ctVL$ /. boldVL$;

(* the background-field masses in the polynomial coefficients; function arguments stay symbolic.  A(0) = Aeps(0) = 0. *)
argsVL$ = {mh^2 -> xh, mg^2 -> xg, ma^2 -> xa};
toSymVL$[e_] := e /. f : (A | Aeps | II)[__] :> (f /. argsVL$) /. {A[0] -> 0, Aeps[0] -> 0};
coefRulesVL$ = {mh -> Sqrt[-m2 + 3 lam phi^2], mg -> Sqrt[-m2 + lam phi^2], ma -> el phi,
   xh -> -m2 + 3 lam phi^2, xg -> -m2 + lam phi^2, xa -> el^2 phi^2};
funcsVL$[e_] := Union[Cases[e, (A | Aeps | II)[__], Infinity]];
(* the coefficients of all monomials in A, Aeps, I (products included), with the masses of the model inserted *)
coefsVL$[e_] := With[{f = funcsVL$[e]},
   If[f === {}, {1 -> Simplify[e /. coefRulesVL$]},
    (Times @@ (f^#1) -> Simplify[#2 /. coefRulesVL$]) & @@@ CoefficientRules[Expand[e], f]]];
serVL$ = Series[toSymVL$[totVL$], {eps, 0, 0}];
polesVL$ = Table[SeriesCoefficient[serVL$, -k], {k, 2, 1, -1}];
(* Aeps is not independent: Aeps(x) = x (-1 - z2/2 + L - L^2/2) = -(x (1 + z2) + A(x)^2/x)/2 *)
finVL$ = Expand[SeriesCoefficient[serVL$, 0] /. Aeps[x_] :> -(x (1 + z2) + A[x]^2/x)/2];
nonlocalVL$[e_] := Select[coefsVL$[e], #[[1]] =!= 1 && #[[2]] =!= 0 &];
Print["(d) non-local terms (with A, Aeps, I) in the 1/eps^2 and 1/eps parts (expect {} {}): ",
  nonlocalVL$[polesVL$[[1]]], " ", nonlocalVL$[polesVL$[[2]]]];
Print["(d) local poles: 1/eps^2: ", Collect[Simplify[polesVL$[[1]] /. coefRulesVL$], phi, Simplify],
  ";  1/eps: ", Collect[Simplify[polesVL$[[2]] /. coefRulesVL$], phi, Simplify]];

(* Martin's functions (MS-bar, Landau gauge) and the couplings of the model:
   lam^{hhh} = 6 lam phi, lam^{hGG} = 2 lam phi, lam^{hhhh} = lam^{GGGG} = 6 lam, lam^{hhGG} = 2 lam,
   g^{AAh} = 2 e^2 phi, g^{AAhh} = g^{AAGG} = 2 e^2, g^{AGh} = -g^{AhG} = e *)
fSSV[x_, y_, z_] := 1/z ((-x^2 - y^2 - z^2 + 2 x y + 2 x z + 2 y z) II[x, y, z] + (x - y)^2 II[0, x, y] +
      (y - x - z) A[x] A[z] + (x - y - z) A[y] A[z] + z A[x] A[y]) + 2 (x + y - z/3) A[z];
fVS[x_, y_] := 3 A[x] A[y] + 2 x A[y];
fVVS[x_, y_, z_] := 1/(4 x y) ((-x^2 - y^2 - z^2 - 10 x y + 2 x z + 2 y z) II[x, y, z] + (x - z)^2 II[0, x, z] +
      (y - z)^2 II[0, y, z] - z^2 II[0, 0, z] + (z - x - y) A[x] A[y] + y A[x] A[z] + x A[y] A[z]) +
    A[x]/2 + A[y]/2 + 2 A[z] - x - y - z;
v2MartinVL$ = -3 lam^2 phi^2 II[xh, xh, xh] - lam^2 phi^2 II[xh, xg, xg] +
   3/4 lam (A[xh]^2 + A[xg]^2) + 1/2 lam A[xh] A[xg] +
   el^2/2 fSSV[xh, xg, xa] + el^2/2 (fVS[xa, xh] + fVS[xa, xg]) + el^4 phi^2 fVVS[xa, xa, xh];
canonVL$ = II[x__] :> II @@ Sort[{x}];
diffVL$ = Expand[(finVL$ - v2MartinVL$) /. canonVL$ /. {A[0] -> 0, Aeps[0] -> 0}];
diffCoefVL$ = Select[coefsVL$[diffVL$], #[[2]] =!= 0 &];
Print["(d) finite part - Martin: monomials with a nonzero coefficient (expect {}): ", diffCoefVL$];
Print["(d) monomials in the finite part: ", Length[coefsVL$[finVL$ /. canonVL$]], ", in Martin's formula: ",
  Length[coefsVL$[Expand[v2MartinVL$ /. canonVL$ /. A[0] -> 0]]]];


(* ::Section:: *)
(*(e) output*)


(* "poles": the 1/eps^2 and 1/eps coefficients (times 1/K^2) of the two-loop diagrams plus the counterterm insertions,
   used in step (2) *)
Put[{"V2" -> v2MartinVL$, "masses" -> {xh -> -m2 + 3 lam phi^2, xg -> -m2 + lam phi^2, xa -> el^2 phi^2},
   "poles" -> (Collect[Simplify[# /. coefRulesVL$], phi, Simplify] & /@ polesVL$)},
  FileNameJoin[{resDirVL$, "v2_landau.m"}]];
Print["(e) written results/v2_landau.m"];
