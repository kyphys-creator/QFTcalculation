(* ::Package:: *)

(* ::Title:: *)
(*Step (9): D-dimensional Born and colour correlations of u ubar -> t tbar and g g -> t tbar, symbolic in s and t*)


(* ::Text:: *)
(*Research note models/qcd, step (9).  Same definitions as scat_feyncalc.wl (step (4)), but with symbolic s, t (m = 1; sums over spins,*)
(*polarizations (physical, light-cone gauge for the gluons) and colours; g = 1).  <T_i.T_j> with the colour operators of Eq. (irpole)*)
(*(all particles outgoing).  Checks: colour conservation, Eq. (sumtree) at D = 4.  These give the D-dimensional Born sigma0(s; eps), the*)
(*D-dimensional pole part Z (x) B(D) of the virtual correction, and the collinear counterterms (hq_assemble.wl).  -> work/hq/born.m*)
(*Usage: wolframscript -file hq_born.wl  (about 1 minute)*)
$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDir = Which[StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName], $Notebooks, NotebookDirectory[], True, Directory[]];
s9 = FileNameJoin[{srcDir, "work", "hq"}];
Quiet[CreateDirectory[s9, CreateIntermediateDirectories -> True]];
modelTmp = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDir, "generated", "QCD_FA"}], FileNameJoin[{modelTmp, "QCD_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmp, "QCD_FA"}], Quiet -> True];
modelFile = FileNameJoin[{modelTmp, "QCD_FA", "QCD_FA"}];
TF = 1/2;
ins[proc_] := InsertFields[CreateTopologies[0, 2 -> 2], proc, InsertionLevel -> {Particles}, Model -> modelFile, GenericModel -> modelFile,
   ExcludeParticles -> {V[1], F[1]}];
conv[d_] := FCFAConvert[CreateFeynAmp[d, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {k1, k2},
    ChangeDimension -> D, List -> True, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] //
   ReplaceAll[#, {SMP["g_s"] -> gS, FCGV["GS"] -> gS, GaugeXi[V[2, ___]] -> 1, GaugeXi[G] -> 1, FCGV["MT"] -> 1, SMP["m_t"] -> 1}] &;
m0 = <|"A" -> FCI[Total[conv[ins[{F[2], -F[2]} -> {F[7], -F[7]}]]]], "B" -> FCI[Total[conv[ins[{V[2], V[2]} -> {F[7], -F[7]}]]]]|>;
FCClearScalarProducts[];
u = 2 - s - t;
SPD[p1, p1] = 0; SPD[p2, p2] = 0; SPD[k1, k1] = 1; SPD[k2, k2] = 1;
SPD[p1, p2] = s/2; SPD[k1, k2] = (s - 2)/2; SPD[p1, k1] = (1 - t)/2; SPD[p2, k2] = (1 - t)/2;
SPD[p1, k2] = (1 - u)/2; SPD[p2, k1] = (1 - u)/2;
polSum[x_] := DoPolarizationSums[DoPolarizationSums[x, p1, p2], p2, p1];
spinPol[key_, x_] := Module[{y = FermionSpinSum[x, ExtraFactor -> 1] // DiracSimplify // Contract}, If[key === "B", y = Contract[polSum[y]]]; y];
colour[x_] := SUNSimplify[x, SUNNToCACF -> True, Explicit -> True];
toNum[x_] := Factor[ExpandScalarProduct[FeynAmpDenominatorExplicit[x]]];
legs = <|"A" -> {{"qbar", SUNFIndex[Col1]}, {"q", SUNFIndex[Col2]}, {"q", SUNFIndex[Col3]}, {"qbar", SUNFIndex[Col4]}},
   "B" -> {{"g", SUNIndex[Glu1]}, {"g", SUNIndex[Glu2]}, {"q", SUNFIndex[Col3]}, {"qbar", SUNFIndex[Col4]}}|>;
prime[(h : SUNIndex | SUNFIndex)[x_]] := h[Symbol[SymbolName[x] <> "p"]];
gen[{"g", a_}, c_] := -I SUNF[c, prime[a], a];
gen[{"q", i_}, c_] := SUNTF[{c}, prime[i], i];
gen[{"qbar", i_}, c_] := -SUNTF[{c}, i, prime[i]];
corr[key_, i_, j_] := Module[{lg = legs[key], mc},
   mc = ComplexConjugate[m0[key]] /. {lg[[i, 2]] -> prime[lg[[i, 2]]], lg[[j, 2]] -> prime[lg[[j, 2]]]};
   toNum[colour[spinPol[key, mc FCI[gen[lg[[i]], SUNIndex[cc]] gen[lg[[j]], SUNIndex[cc]]] m0[key]]]] /. gS -> 1];
pairs = {{1, 2}, {1, 3}, {1, 4}, {2, 3}, {2, 4}, {3, 4}};
res = Association[Table[key -> Module[{born, cc, t0 = AbsoluteTime[]},
      born = toNum[colour[spinPol[key, ComplexConjugate[m0[key]] m0[key]]]] /. gS -> 1;
      cc = Association[Table[p -> corr[key, Sequence @@ p], {p, pairs}]];
      Print[key, ": Born(D) = ", InputForm[Factor[born]], " (", Round[AbsoluteTime[] - t0], " s)"];
      Print[key, ": colour conservation (expect 0, 0): ", Simplify[{cc[{1, 2}] + cc[{1, 3}] + cc[{1, 4}] + If[key === "A", CF, CA] born,
          cc[{1, 3}] + cc[{2, 3}] + cc[{3, 4}] + CF born} /. CF -> (CA^2 - 1)/(2 CA)]];
      <|"born" -> born, "cc" -> cc|>], {key, {"A", "B"}}]];
(* D = 4 checks against Eq. (13) *)
Print["A: Born(4) - Eq.(13): ", Simplify[(res["A"]["born"] /. D -> 4) - 8 TF^2 (CA^2 - 1) ((t - 1)^2 + (u - 1)^2 + 2 s)/s^2 /. CF -> (CA^2 - 1)/(2 CA)]];
Module[{t1 = (1 - t)/s, t2 = (1 - u)/s, rho = 4/s},
  Print["B: Born(4) - Eq.(13): ", Simplify[(res["B"]["born"] /. D -> 4) - 8 CA CF (CF/(t1 t2) - CA) (t1^2 + t2^2 + rho - rho^2/(4 t1 t2)) /. CF -> (CA^2 - 1)/(2 CA)]]];
Put[res, FileNameJoin[{s9, "born.m"}]];
Quiet[DeleteDirectory[modelTmp, DeleteContents -> True]];
