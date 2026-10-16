(* ::Package:: *)

(* ::Title:: *)
(*Step (4): one-loop q qbar -> Q Qbar and g g -> Q Qbar with the unpatched FeynArts 3.12 and FormCalc 9.10*)


(* ::Text:: *)
(*Research note models/qcd, step (4); independent of FeynCalc.  Run in its own kernel: the patched (FeynCalc) and unpatched*)
(*FeynArts must not be loaded together.  Feynman gauge (FeynArts' default GaugeRules), g = 1, m = 1, s = 10, t = -3.*)
(*CalcFeynAmp with Dimension -> 0 keeps the whole amplitude D-dimensional (no rational terms; D - 4 = Dminus4), and*)
(*HelicityME and PolarizationSum with Dimension -> 0 form the spin and polarization sums in D dimensions: this is CDR,*)
(*the scheme of scat_feyncalc.wl (the Born comes out as 16 |M0|^2 = 288/25 + 8 Dminus4 for (A), 4 |M0|^2 =*)
(*184 (226 + 228 Dminus4 + 75 Dminus4^2)/675 for (B) in SU(3), Eq. (sumtree) continued to D dimensions).  _Hel = 0 makes*)
(*HelicityME use (pslash + m)/2 per external fermion, hence the factors 16 and 4.  The physical polarization sums of the*)
(*gluons keep the gauge terms with the reference vectors eta[1] = k[2], eta[2] = k[1] (GaugeTerms -> True), as in*)
(*scat_feyncalc.wl.  Output: the interference of each diagram, sum M0^* M1 = SquaredME[M0, M1], with the LoopTools*)
(*functions B0i, C0i, D0i and Dminus4 left symbolic -> work/scat/A/formcalc.m, work/scat/B/formcalc.m; scat_eval.wl*)
(*evaluates them (LoopTools through FeynHelpers, MS-bar) and compares diagram by diagram with FeynCalc at xi = 1.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file scat_formcalc.wl  (in its own kernel).  Interactive:  ~/hep/bin/wopen scat_formcalc.wl  (in its own kernel), then "Run All Code"; the Inspect cells run only in the notebook.*)


(* ::Section:: *)
(*Setup*)


Get["FeynArts`"];
Get["FormCalc`"];
srcDirFC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelFC$ = FileNameJoin[{srcDirFC$, "generated", "QCD_FA", "QCD_FA"}];   (* FeynRules output, unpatched *)
outDirFC$ = FileNameJoin[{srcDirFC$, "work", "scat"}];
workDirFC$ = CreateDirectory[];
SetDirectory[workDirFC$];   (* FormCalc writes its FORM files here *)
denRulesFC$ = {IGram[x_] :> 1/x, Den[p_, m_, d_] :> 1/(p - m)^d, Den[p_, m_] :> 1/(p - m)};
insFC$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelFC$, GenericModel -> modelFC$,
   ExcludeParticles -> {V[1], F[1]}];
procsFC$ = <|"A" -> ({F[2], -F[2]} -> {F[7], -F[7]}), "B" -> ({V[2], V[2]} -> {F[7], -F[7]})|>;
(* k[i].k[j] at s = 10, t = -3, m = 1 (k[1], k[2] incoming, k[3] = Q, k[4] = Qbar); FormCalc's T = (k1 - k3)^2, U = (k2 - k3)^2 *)
kpFC$ = {{0, 5, 2, 3}, {5, 0, 3, 2}, {2, 3, 1, 4}, {3, 2, 4, 1}};
numRulesFC$ = {Alfas -> 1/(4 Pi), Alfas2 -> 1/(4 Pi)^2, GS -> 1, MT -> 1, MT2 -> 1};
evalSqFC$[res_] := If[MatchQ[res, {_, {___Rule}}], res[[1]] //. res[[2]], res];


(* ::Section:: *)
(*Amplitudes, spin, colour and polarization sums*)


runFC$[key_] := Module[{d0, d1, tree, n1, amps, hel, col, num, factor, born, interf, t0 = AbsoluteTime[]},
   d0 = insFC$[CreateTopologies[0, 2 -> 2], procsFC$[key]];
   d1 = insFC$[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], procsFC$[key]];
   tree = CalcFeynAmp[CreateFeynAmp[d0] /. M$FACouplings, Dimension -> 0, FermionChains -> VA];
   n1 = Length[CreateFeynAmp[d1]];
   amps = Quiet[Table[CalcFeynAmp[CreateFeynAmp[DiagramExtract[d1, i]] /. M$FACouplings, Dimension -> 0, FermionChains -> VA], {i, n1}],
     CalcFeynAmp::ddim];
   _Hel = 0;
   hel = HelicityME[tree, Flatten[{tree, amps}], Dimension -> 0];
   col = ColourME[tree, Flatten[{tree, amps}]];
   factor = If[key === "A", 16, 4];
   num[x_] := Module[{y = x /. hel /. col},
     If[key === "B", y = PolarizationSum[y, GaugeTerms -> True, Dimension -> 0]];
     y //. Subexpr[] //. Abbr[] /. denRulesFC$ /. {eta[1] -> k[2], eta[2] -> k[1]} /. Pair[k[i_], k[j_]] :> kpFC$[[i, j]] /.
       numRulesFC$ /. {S -> 10, T -> -3, U -> -5}];
   born = Simplify[factor num[evalSqFC$[SquaredME[tree, tree]]]];
   interf = Table[factor num[evalSqFC$[SquaredME[tree, amps[[i]]]]], {i, n1}];
   Print["(", key, ") ", n1, " one-loop diagrams in ", Round[AbsoluteTime[] - t0], " s;  Born (SU(3), D = 4 + Dminus4) = ", InputForm[born],
    ";  symbols left: ", Complement[Union[Cases[interf, _Symbol, Infinity]], {Dminus4, Pi}]];
   Quiet[CreateDirectory[FileNameJoin[{outDirFC$, key}], CreateIntermediateDirectories -> True]];
   Put[{born, interf}, FileNameJoin[{outDirFC$, key, "formcalc.m"}]];
   {born, interf}];
resA$ = runFC$["A"];
resB$ = runFC$["B"];


(* ::Subsubsection:: *)
(*Inspect: the loop functions in each diagram of (A)*)


If[$Notebooks,
  Union[Cases[#, (h : B0i | C0i | D0i)[id_, ___] :> {h, id}, Infinity]] & /@ resA$[[2]]
]


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it removes FormCalc's work directory.*)


ResetDirectory[];
DeleteDirectory[workDirFC$, DeleteContents -> True];
