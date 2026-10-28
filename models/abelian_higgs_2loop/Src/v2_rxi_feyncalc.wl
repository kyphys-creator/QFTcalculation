(* ::Package:: *)

(* ::Title:: *)
(*Step (4): the two-loop effective potential in the background-field R_xi gauge from the Feynman diagrams*)


(* ::Text:: *)
(*Research note models/abelian_higgs_2loop, step (4).  Background field phi, Phi = (phi + h + i G)/sqrt 2, gauge fixing*)
(*F = d.A - xi e phi G (the R_xi gauge of the FeynRules model of the one-loop note with vev -> phi; Martin-Patel's*)
(*xi~ = xi), MS-bar at the scale Q.  Masses (Martin-Patel's notation, arXiv:1808.07615):*)
(*    H = xh = -m2 + 3 lam phi^2,  Z = xa = e^2 phi^2,  G = -m2 + lam phi^2,  Z+ = xp = G + xi Z,  eta = xe = xi Z*)
(*(transverse vector Z; Goldstone Z+; the xi pole of the vector, the ghost: eta).*)
(*  (a) FeynArts: the two-loop vacuum diagrams of the model (ghost loop included);*)
(*  (b) FeynCalc: Lorentz algebra, partial fractions, integral families;*)
(*  (c) Kira 3.1: reduction to the masters;*)
(*  (d) the bare diagrams plus the one-loop counterterm insertions, i.e. the first-order variation of the bare one-loop*)
(*      potential  V1_B = [H A(H) + Z+ A(Z+) + Z- A(Z-) - 2 eta A(eta) + (3 - 2 eps) Z A(Z)]/(4 - 2 eps)  (bold A),*)
(*      Z+- = xi~ Z + [G +- sqrt(G (G + 4 (xi~ - xi) Z))]/2, with Martin-Patel's one-loop MS-bar counterterms of m2, lam,*)
(*      e, xi, xi~, phi^2 at xi~ = xi;  the poles against those of the bare tree potential with their two-loop*)
(*      counterterms, and the finite part against their Eq. (4.127);*)
(*  (e) results/v2_rxi.m: V2 (coefficient of 1/(16 pi^2)^2) in A[x], II[x,y,z] and the poles.*)
(*Batch: wolframscript -file v2_rxi_feyncalc.wl*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$NumberMarks = False;

srcDirRX$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirRX$ = FileNameJoin[{srcDirRX$, "results"}];
kiraRX$ = FileNameJoin[{$HomeDirectory, "hep", "Kira-3.1", "bin", "kira"}];
fermatRX$ = FileNameJoin[{$HomeDirectory, "hep", "fermat-7.9b", "fer64"}];
workRX$ = FileNameJoin[{srcDirRX$, "work", "v2_rxi"}];
(* a fresh working directory: Kira reuses the databases of an earlier run *)
If[DirectoryQ[workRX$], DeleteDirectory[workRX$, DeleteContents -> True]];
CreateDirectory[workRX$, CreateIntermediateDirectories -> True];


(* ::Section:: *)
(*(a) diagrams*)


(* patched copy of the FeynRules model of the one-loop note: FeynCalc's FeynArts patch, and the Goldstone mass MG *)
modelSrcRX$ = FileNameJoin[{srcDirRX$, "..", "..", "abelian_higgs", "Src", "generated", "AbelianHiggs_FA"}];
modelTmpRX$ = CreateDirectory[];
CopyDirectory[modelSrcRX$, FileNameJoin[{modelTmpRX$, "AbelianHiggs_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpRX$, "AbelianHiggs_FA"}], Quiet -> True];
With[{mf = FileNameJoin[{modelTmpRX$, "AbelianHiggs_FA", "AbelianHiggs_FA.mod"}],
   g = "PropagatorLabel -> \"G\",\n    PropagatorType -> ScalarDash,\n    PropagatorArrow -> None,\n    Mass -> "},
  Module[{s = Import[mf, "Text"]},
   If[StringCount[s, g <> "MA"] =!= 1, Print["ERROR: Goldstone mass entry not found"]; Exit[1]];
   Export[mf, StringReplace[s, g <> "MA" -> g <> "MG"], "Text"]]];
modelRX$ = FileNameJoin[{modelTmpRX$, "AbelianHiggs_FA", "AbelianHiggs_FA"}];

topsRX$ = CreateTopologies[2, 0 -> 0, ExcludeTopologies -> {Reducible}];
insRX$ = InsertFields[topsRX$, {} -> {}, InsertionLevel -> {Particles}, Model -> modelRX$, GenericModel -> modelRX$];
fampRX$ = CreateFeynAmp[insRX$, GaugeRules -> {}];
Print["(a) one-particle-irreducible two-loop vacuum diagrams: ", Length[fampRX$], "  (expect 10)"];


(* ::Subsubsection:: *)
(*Inspect: the diagrams*)


If[$Notebooks, Paint[insRX$, ColumnsXRows -> {5, 2}, Numbering -> Simple]]


(* ::Section:: *)
(*(b) Lorentz algebra and integral families*)


(* FeynArts writes 1/(2 pi)^4 per loop; the measure d^Dk/(2 pi)^D per loop is kept implicit.  Background-field R_xi
   gauge (the model's R_xi gauge with vev -> phi): the Goldstone propagator mass sqrt(GaugeXi) MG -> mg
   (mg^2 = G + xi Z), the ghost and the xi pole of the vector sqrt(GaugeXi) MA -> mx (mx^2 = xi Z), then
   GaugeXi -> mx^2/ma^2 in the rest.  Lower-case mass symbols for Kira. *)
ampRX$ = FCFAConvert[fampRX$, LoopMomenta -> {q1, q2}, ChangeDimension -> D, List -> True, SMP -> False,
     DropSumOver -> True] /. FCGV[x_String] :> ToExpression[x];
ampRX$ = ampRX$ /. {MG Sqrt[GaugeXi[A]] -> mg, MA Sqrt[GaugeXi[A]] -> mx} /. GaugeXi[A] -> mx^2/MA^2 /. {gc9 -> EL};
ampRX$ = (2 Pi)^8 ampRX$ /. {MH -> mh, MA -> ma, EL -> el, vev -> phi};
ampRX$ = Expand[FCE[Contract[#]]] & /@ ampRX$;
Print["(b) diagrams that vanish (expect 0; the ghost loop now contributes): ", Count[ampRX$, 0],
  ";  GaugeXi or MG left: ", !FreeQ[ampRX$, GaugeXi | MG | MA | MH]];
(* the potential is minus the sum of the amplitudes: V2 = i x (vacuum graphs) and FeynArts' amplitude is -i x graph *)
v2IntRX$ = -Total[ampRX$];

apRX$ = ApartFF[v2IntRX$, {q1, q2}, FCE -> True];
{expTRX$, toposRX$} = FCLoopFindTopologies[apRX$, {q1, q2}, Names -> "v"];
mapRX$ = FCLoopFindTopologyMappings[toposRX$];
(* complete the families that lack a propagator (renamed "...C"), as in FeynCalc's example B-EtaC *)
incRX$ = Select[mapRX$[[2]], FCLoopBasisIncompleteQ];
compIncRX$ = FCLoopBasisFindCompletion[incRX$];
compRulesRX$ = Flatten[FCLoopCreateRuleGLIToGLI[compIncRX$, List /@ incRX$]];
compRX$ = mapRX$[[2]] /. Thread[incRX$ -> compIncRX$];
glExpRX$ = FCLoopApplyTopologyMappings[expTRX$ /. compRulesRX$, {mapRX$[[1]] /. compRulesRX$, compRX$}];
glisRX$ = Union[Cases[glExpRX$, _GLI, Infinity]];
Print["(b) families after the mappings: ", Length[compRX$], ";  integrals to reduce: ", Length[glisRX$]];


(* ::Section:: *)
(*(c) reduction with Kira*)


kiraDirRX$ = FileNameJoin[{workRX$, "kira"}];
redRX$ = {};
Do[Module[{name = topo[[1]], targets, d, ok, pref, n},
    targets = Select[glisRX$, #[[1]] === name &];
    If[targets === {}, Continue[]];
    n = Length[topo[[2]]];
    (* preferred masters: no dots, at most one propagator removed *)
    pref = Select[Tuples[{0, 1}, n], Total[#] >= n - 1 &];
    KiraCreateIntegralFile[targets, topo, kiraDirRX$];
    KiraCreateConfigFiles[topo, targets, kiraDirRX$, KiraMassDimensions -> {mh -> 1, mg -> 1, ma -> 1, mx -> 1}];
    d = FileNameJoin[{kiraDirRX$, ToString[name]}];
    Export[FileNameJoin[{d, "preferred"}],
     StringRiffle[(ToString[name] <> "[" <> StringRiffle[ToString /@ #, ","] <> "]") & /@ pref, "\n"] <> "\n", "Text"];
    Export[FileNameJoin[{d, "job.yaml"}], StringJoin["jobs:\n  - reduce_sectors:\n      reduce:\n        - {topologies: [",
       ToString[name], "], sectors: [b", StringJoin[ToString /@ ConstantArray[1, n]], "], r: ", ToString[n],
       ", s: 3}\n      select_integrals:\n        select_mandatory_list:\n          - \"KiraLoopIntegrals\"\n",
       "      preferred_masters: \"preferred\"\n      run_initiate: true\n      run_triangular: true\n      run_back_substitution: true\n",
       "      integral_ordering: 2\n  - kira2math:\n      target:\n       - [", ToString[name], ", \"KiraLoopIntegrals\"]\n"], "Text"];
    ok = KiraRunReduction[d, KiraBinaryPath -> kiraRX$, KiraFermatPath -> fermatRX$];
    If[ok =!= True, Print["ERROR: Kira failed for ", name]; Exit[1]];
    redRX$ = Join[redRX$, KiraImportResults[ToString[name], kiraDirRX$]]],
  {topo, compRX$}];
v2RedRX$ = glExpRX$ /. FCGV["GLIProduct"] -> Times /. Dispatch[redRX$];
mastRX$ = Union[Cases[v2RedRX$, _GLI, Infinity]];
Print["(c) masters after the reduction: ", Length[mastRX$], ";  any with dots or numerators: ",
  Select[mastRX$, Max[#[[2]]] > 1 || Min[#[[2]]] < 0 &]];
Print["(c) factors with D in the denominators of the coefficients (expect none at D = 4): ",
  Union[Select[Flatten[FactorList[Denominator[Together[Coefficient[v2RedRX$, #]]]][[All, 1]] & /@ mastRX$], !FreeQ[#, D] &]]];


(* ::Section:: *)
(*(d) renormalization and comparison with Martin-Patel*)


(* the masses on the propagators of a master: Minkowski integral -> TSIL bold form (coefficient of 1/(16 pi^2)^2) *)
propMassRX$[topo_FCTopology] := topo[[2]] /. FeynAmpDenominator[StandardPropagatorDenominator[_, 0, mm_, {1, 1}]] :> -mm;
masterBoldRX$[GLI[name_, idx_]] := Module[{topo = Select[compRX$, #[[1]] === name &][[1]], ms, on},
   ms = propMassRX$[topo];
   on = Pick[ms, idx, 1];
   Switch[Length[on],
    2, -tB[on[[1]]] tB[on[[2]]],          (* (-i T)(-i T) *)
    3, sB @@ Sort[on],                    (* i^2 (-1)^3 S_E *)
    _, Print["ERROR: unexpected master ", GLI[name, idx]]; Abort[]]];
tB[0] = 0;
boldRX$ = {tB[x_] :> -x/eps + A[x] + eps Aeps[x],
   sB[x_, y_, z_] :> -(x + y + z)/(2 eps^2) + (A[x] + A[y] + A[z] - (x + y + z)/2)/eps + II[x, y, z] -
      ((x + y + z) (1 + z2) + Total[If[# === 0, 0, A[#]^2/#] & /@ {x, y, z}])/2};
v2BareRX$ = v2RedRX$ /. GLI[n_, i_] :> masterBoldRX$[GLI[n, i]] /. D -> 4 - 2 eps;

(* one-loop counterterm insertions: the first-order variation of V1_B.  Martin-Patel's one-loop counterterms (times
   1/(16 pi^2 eps)), at xi~ = xi: m2 (4 lam - 3 e^2), lam: 10 lam^2 - 6 lam e^2 + 3 e^4, e: e^3/6, xi: -e^2 xi/3,
   xi~: e^2 xi~ (xi~ - xi - 10/3) = -10 e^2 xi/3, phi^2: e^2 (3 - xi + 2 xi~) phi^2 = (3 + xi) e^2 phi^2.
   To first order off xi~ = xi:  Z+ = G + (2 xi~ - xi) Z,  Z- = xi Z,  eta = xi~ Z. *)
ctRX$ = Module[{dm2, dlam, de, dxi, dxit, dphi2, dZ, dH, dG, dZp, cEta},
   dm2 = (4 lam - 3 el^2) m2; dlam = 10 lam^2 - 6 lam el^2 + 3 el^4; de = el^3/6;
   dxi = -el^2 xi/3; dxit = -10 el^2 xi/3; dphi2 = (3 + xi) el^2 phi^2;
   dZ = 2 el de phi^2 + el^2 dphi2;
   dH = -dm2 + 3 phi^2 dlam + 3 lam dphi2;
   dG = -dm2 + phi^2 dlam + lam dphi2;
   dZp = dG + (2 dxit - dxi) el^2 phi^2 + xi dZ;
   cEta = (dxi/2 - dxit) el^2 phi^2 - xi dZ/2;               (* (1/2) dZ- - d eta *)
   (dH/2 tB[mh^2] + dZp/2 tB[mg^2] + cEta tB[mx^2] + (3 - 2 eps)/2 dZ tB[ma^2])/eps];
totRX$ = v2BareRX$ + ctRX$ /. boldRX$;

argsRX$ = {mh^2 -> xh, mg^2 -> xp, ma^2 -> xa, mx^2 -> xe};
toSymRX$[e_] := e /. f : (A | Aeps | II)[__] :> (f /. argsRX$) /. {A[0] -> 0, Aeps[0] -> 0};
massesRX$ = {xh -> -m2 + 3 lam phi^2, xp -> -m2 + lam phi^2 + xi el^2 phi^2, xa -> el^2 phi^2, xe -> xi el^2 phi^2};
coefRulesRX$ = Join[{mh -> Sqrt[-m2 + 3 lam phi^2], mg -> Sqrt[-m2 + lam phi^2 + xi el^2 phi^2], ma -> el phi,
    mx -> Sqrt[xi] el phi}, massesRX$];
funcsRX$[e_] := Union[Cases[e, (A | Aeps | II)[__], Infinity]];
coefsRX$[e_] := With[{f = funcsRX$[e]},
   If[f === {}, {1 -> Simplify[e /. coefRulesRX$, xi > 0 && el > 0 && phi > 0]},
    (Times @@ (f^#1) -> Simplify[#2 /. coefRulesRX$, xi > 0 && el > 0 && phi > 0]) & @@@
     CoefficientRules[Expand[e], f]]];
serRX$ = Series[toSymRX$[totRX$], {eps, 0, 0}];
polesRX$ = Table[SeriesCoefficient[serRX$, -k], {k, 2, 1, -1}];
finRX$ = Expand[SeriesCoefficient[serRX$, 0] /. Aeps[x_] :> -(x (1 + z2) + A[x]^2/x)/2];
nonlocalRX$[e_] := Select[coefsRX$[e], #[[1]] =!= 1 && #[[2]] =!= 0 &];
Print["(d) non-local terms (with A, Aeps, I) in the 1/eps^2 and 1/eps parts (expect {} {}): ",
  nonlocalRX$[polesRX$[[1]]], " ", nonlocalRX$[polesRX$[[2]]]];
polesLocRX$ = Collect[Simplify[# /. coefRulesRX$, xi > 0 && el > 0 && phi > 0], phi, Simplify] & /@ polesRX$;
Print["(d) local poles: 1/eps^2: ", InputForm[polesLocRX$[[1]]], ";  1/eps: ", InputForm[polesLocRX$[[2]]]];

(* the bare tree potential mu^(2 eps)[Lam_B + m2_B phi_B^2/2 + lam_B phi_B^4/4] (Martin-Patel's sign of m2: mMP = -m2)
   with their two-loop counterterm coefficients, Eqs. (4.95)-(4.109), at xi~ = xi; its 1/K^2 poles cancel ours *)
Module[{mMP = -m2, cm11, cm21, cm22, cl11, cl21, cl22, cL21, cL22, cp11, cp21, cp22, p2, p1},
  cm11 = (4 lam - 3 el^2) mMP; cm21 = (-10 lam^2 + 16 lam el^2 + 43 el^4/6) mMP;
  cm22 = (28 lam^2 - 24 lam el^2 + 10 el^4) mMP;
  cl11 = 10 lam^2 - 6 lam el^2 + 3 el^4; cl21 = -60 lam^3 + 28 lam^2 el^2 + 79 lam el^4/3 - 52 el^6/3;
  cl22 = 100 lam^3 - 90 lam^2 el^2 + 47 lam el^4 - 8 el^6;
  cL21 = 2 el^2 mMP^2; cL22 = (2 lam - 3 el^2/2) mMP^2;
  cp11 = el^2 (3 - xi + 2 xi); cp21 = -2 lam^2 + el^4 (-5/3 + xi (1 + xi));
  cp22 = el^4 (5 - 3 xi + xi^2/2 + xi (3 - xi + xi));
  p2 = cL22 + phi^2/2 (mMP cp22 + cm11 cp11 + cm22) + phi^4/4 (lam (2 cp22 + cp11^2) + 2 cl11 cp11 + cl22);
  p1 = cL21 + phi^2/2 (mMP cp21 + cm21) + phi^4/4 (lam 2 cp21 + cl21);
  Print["(d) diagrams + insertions + Martin-Patel's two-loop counterterms, 1/eps^2 and 1/eps (expect {0, 0}): ",
   Simplify[{polesLocRX$[[1]] + p2, polesLocRX$[[2]] + p1}]]];

(* Martin-Patel, Eq. (4.127): V2 at xi~ = xi; lamK(G,H,Z) the Kallen function *)
v2MPRX$ = Module[{H = xh, Z = xa, Zp = xp, et = xe, G = xp - xe, lk},
   lk = G^2 + H^2 + Z^2 - 2 G H - 2 G Z - 2 H Z;
   1/phi^2 ((H Z - H^2/4 - 3 Z^2) II[H, Z, Z] + ((H + Z - G) et - et^2/2 - lk/2) II[H, Z, Zp] -
      (H - G)^2/4 II[H, Zp, Zp] + ((H + et - Z)^2/2 - 2 et H) II[H, Z, et] + (H - Zp)^2/2 II[H, et, Zp] +
      (et H - et^2/2 - H^2/4) II[H, et, et] - 3 (H - G)^2/4 II[H, H, H] +
      (H/4 - Z/2) A[Z]^2 + (H/4 - et/2) A[et]^2 + 3 (H - G)/8 A[Zp]^2 + 3 (H - G)/8 A[H]^2 +
      (H + 2 Z - et - G)/2 A[Z] A[Zp] + (Zp - H)/2 A[et] A[Zp] + (Z + et - H)/2 A[Z] A[et] +
      (3 Z - H + G)/2 A[H] A[Z] + (H + 2 Z - G)/4 A[H] A[Zp] + (H - Z - G)/2 A[H] A[et] +
      Z (G + H + 2 Z/3) A[Z] + 3 Z^2 A[H] + Z^2 A[Zp] - Z^2 (2 Z + H))];
canonRX$ = II[x__] :> II @@ Sort[{x}];
diffRX$ = Expand[(finRX$ - v2MPRX$) /. canonRX$];
Print["(d) finite part - Martin-Patel (4.127): monomials with a nonzero coefficient (expect {}): ",
  Select[coefsRX$[diffRX$], #[[2]] =!= 0 &]];
Print["(d) monomials in the finite part: ", Length[coefsRX$[finRX$ /. canonRX$]], ", in Eq. (4.127): ",
  Length[coefsRX$[Expand[v2MPRX$ /. canonRX$]]], ";  I functions: ", Union[Cases[finRX$ /. canonRX$, _II, Infinity]]];


(* ::Section:: *)
(*(e) output*)


Put[{"V2" -> v2MPRX$, "masses" -> massesRX$, "poles" -> polesLocRX$}, FileNameJoin[{resDirRX$, "v2_rxi.m"}]];
Print["(e) written results/v2_rxi.m"];
