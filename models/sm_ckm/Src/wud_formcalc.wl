(* ::Package:: *)

(* ::Title:: *)
(*Step (5) of the CKM note: W+ -> u_i dbar_j at one loop with FeynArts' SM.mod ($CKM = True) and FormCalc (on-shell scheme, Feynman gauge)*)


(* ::Text:: *)
(*Independent of FeynCalc and of this note's model (run in its own kernel: the patched FeynArts of FeynCalc must not*)
(*be loaded).  FeynArts 3.12 SM.mod with the CKM matrix (Denner's conventions and his on-shell counterterms, the CKM*)
(*counterterm of Denner and Sack, dCKM1), FormCalc 9.10, Feynman gauge, massless photon with LoopTools' lambda for the*)
(*IR divergences.  For the six channels W+ (= -V[3] of SM.mod) -> u_i dbar_j:*)
(*  - the 1PI vertex (no tadpoles, no external self-energies) and the vertex counterterm (C[-F[3], F[4], -V[3]] of*)
(*    SM.mod: CKM (dZe1 - dSW1/SW + dZW1/2) + dCKM1 + (1/2)(dZfL1^{u+} CKM + CKM dZfL1^d));*)
(*  - 2 Re(M0^* M1)/|M0|^2 summed over the spins and the W polarizations (HelicityME, PolarizationSum, D-dimensional*)
(*    Dirac algebra for the loop amplitude) for the vertex and for the counterterm;*)
(*  - the renormalization constants dZfL1 (u, d), dZW1, dCKM1, dZe1 - dSW1/SW (CalcRenConst, Re-tilde of FormCalc).*)
(*Compared with results/wud_numeric.csv of wud_renormalized.wl (this note's model, FeynCalc, the same benchmark, mu =*)
(*MZ, lambda^2 = 1 GeV^2, LoopTools with Delta = 0).  Writes results/wud_formcalc.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file wud_formcalc.wl  (run wud_renormalized.wl first; a few minutes).*)


(* ::Section:: *)
(*Setup*)


Get["FeynArts`"];
Get["FormCalc`"];
$CKM = True;
t0WF$ = AbsoluteTime[];
srcDirWF$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirWF$ = FileNameJoin[{srcDirWF$, "results"}];
workDirWF$ = CreateDirectory[];
SetDirectory[workDirWF$];
SetOptions[InsertFields, Model -> "SM", GenericModel -> "Lorentz", InsertionLevel -> {Particles}];
denRulesWF$ = {IGram[x_] :> 1/x, Den[p_, m_, d_] :> 1/(p - m)^d, Den[p_, m_] :> 1/(p - m)};
chansWF$ = Flatten[Table[{i, j}, {i, 2}, {j, 3}], 1];
chanNameWF$[{i_, j_}] := {"u", "c"}[[i]] <> {"d", "s", "b"}[[j]];

(* the benchmark of wud_renormalized.wl; SM.mod's symbols are matched by name *)
vStdWF$ = {
   {c12 c13, s12 c13, s13 Exp[-I dl]},
   {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
   {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}} /.
   {c12 -> Sqrt[1 - s12^2], c23 -> Sqrt[1 - s23^2], c13 -> Sqrt[1 - s13^2]};
vNumWF$ = N[vStdWF$ /. {s12 -> 22501/100000, s23 -> 4183/100000, s13 -> 3732/1000000, dl -> 1147/1000}, 30];
(* f = 10: m_u, m_d ten times larger (the second point of wud_renormalized.wl (c)) *)
valOfWF$[f_] := Module[{e = Sqrt[4 Pi/128], mz = 91, mw = 80, sw, m},
   sw = Sqrt[1 - mw^2/mz^2];
   m = <|"MZ" -> mz, "MW" -> mw, "MH" -> 125, "MT" -> 165, "MB" -> 286/100, "MC" -> 619/1000, "MS" -> 546/10000,
     "MD" -> f 271/100000, "MU" -> f 127/100000, "ML" -> 1746/1000, "MM" -> 1027/10000, "ME" -> 487/1000000|>;
   Join[m, Association[(# <> "2" -> m[#]^2) & /@ Keys[m]],
    <|"EL" -> e, "Alfa" -> e^2/(4 Pi), "Alfa2" -> e^4/(4 Pi)^2, "SW" -> sw, "CW" -> mw/mz, "SW2" -> sw^2,
     "CW2" -> mw^2/mz^2, "Finite" -> 1|>]];
valWF$ = valOfWF$[1];
byNameWF$ = s_Symbol /; KeyExistsQ[valWF$, SymbolName[s]] :> valWF$[SymbolName[s]];
ckmWF$ = {Conjugate[(c_Symbol /; SymbolName[c] === "CKM")[i_Integer, j_Integer]] :> Conjugate[vNumWF$[[i, j]]],
   (c_Symbol /; SymbolName[c] === "CKMC")[i_Integer, j_Integer] :> Conjugate[vNumWF$[[i, j]]],
   (c_Symbol /; SymbolName[c] === "CKM")[i_Integer, j_Integer] :> vNumWF$[[i, j]]};
numWF$[x_] := Module[{y = (x //. Subexpr[] //. Abbr[]) /. denRulesWF$, left},
   y = y /. ckmWF$ //. byNameWF$;
   left = Union[Cases[y, s_Symbol /; ! MemberQ[{"System`"}, Context[s]] && ! NumericQ[s], Infinity]];
   If[left =!= {}, Print["   symbols left before N: ", left]];
   N[y]];
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetMudim[91.^2]; SetDelta[0.]; SetLambda[1.];


(* ::Subsubsection:: *)
(*Inspect: the vertex diagrams of W+ -> c bbar in SM.mod (Feynman gauge)*)


If[$Notebooks, Show /@ Render[Paint[InsertFields[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}],
     {-V[3]} -> {F[3, {2}], -F[4, {3}]}], DisplayFunction -> Identity]]]


(* ::Section:: *)
(*Renormalization constants*)


rcListWF$ = Join[{dZe1, dSW1, dZW1}, Flatten[Table[{dZfL1[3, a, b], dZfL1[4, a, b], dCKM1[a, b]}, {a, 3}, {b, 3}]]];
rcWF$ = CalcRenConst[rcListWF$] //. Subexpr[] //. Abbr[];
ClearProcess[];
Print["CalcRenConst returned: head ", Head[rcWF$], ", length ", Length[rcWF$], ", depth ", Depth[rcWF$], ";  first: ",
  Short[InputForm[First[Flatten[{rcWF$}]]], 5]];
rcWF$ = Cases[Flatten[{rcWF$} /. RenConstList[_][x___] :> {x}], _Rule | _RuleDelayed];
(* the constants are defined through each other (dSW1 through dMWsq1, dMZsq1; dZe1 through dZAA1, dZZA1; dCKM1
   through dZfL1): insert them until only loop integrals are left *)
rcWF$ = (#[[1]] -> (#[[2]] //. rcWF$)) & /@ rcWF$;
(* the numbers depend on LoopTools' Delta: evaluated for the current Delta *)
rcNumNowWF$[] := Association[(#[[1]] -> numWF$[#[[2]]]) & /@ rcWF$];
rcNumWF$ = rcNumNowWF$[];
(* the index sum of the counterterm vertex (SumOver of FormCalc) is done before the numbers are inserted *)
sumOverWF$[x_] := Expand[x] /. Times[a___, SumOver[g_, n_Integer, ___], b___] :> Sum[Times[a, b], {g, 1, n}];
rcValWF$[x_, rc_] := numWF$[sumOverWF$[x //. Subexpr[] //. Abbr[]] /. Normal[rc]];
Print["(a) renormalization constants: ", Length[rcWF$], " computed;  ", Round[AbsoluteTime[] - t0WF$], " s"];


(* ::Section:: *)
(*The six channels and the comparison, at the benchmark and with m_u, m_d ten times larger*)


_Hel = 0;
evalSqWF$[res_] := If[MatchQ[res, {_, {___Rule}}], res[[1]] //. res[[2]], res];
(* the amplitudes do not depend on the numbers: computed once per channel *)
ampsWF$ = Association[Table[ch -> Module[{proc = {-V[3]} -> {F[3, {ch[[1]]}], -F[4, {ch[[2]]}]}, tree, vert, ct, hel, col, nd},
      ClearProcess[];
      tree = CalcFeynAmp[CreateFeynAmp[InsertFields[CreateTopologies[0, 1 -> 2], proc]], FermionChains -> VA];
      nd = Length[CreateFeynAmp[InsertFields[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], proc]]];
      vert = CalcFeynAmp[CreateFeynAmp[InsertFields[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}],
           proc]], Dimension -> D, FermionChains -> VA];
      ct = CalcFeynAmp[CreateFeynAmp[InsertFields[CreateCTTopologies[1, 1 -> 2, ExcludeTopologies -> {TadpoleCTs,
             WFCorrectionCTs}], proc]], FermionChains -> VA];
      hel = HelicityME[tree, Join[tree, vert, ct]];
      col = ColourME[tree, Join[tree, vert, ct]];
      Print["   ", chanNameWF$[ch], ": ", nd, " vertex diagrams"];
      (* everything with its abbreviations resolved, before the next process clears them *)
      <|"nd" -> nd, "sq" -> Table[(PolarizationSum[evalSqWF$[SquaredME[tree, a]] /. hel /. col] //. Subexpr[] //. Abbr[]),
          {a, {tree, vert, ct}}]|>], {ch, chansWF$}]];
Print["(b) amplitudes;  ", Round[AbsoluteTime[] - t0WF$], " s"];
chanWF$[ch_, rc_] := Module[{sq = ampsWF$[ch]["sq"], b0, wv, wc},
   b0 = numWF$[sq[[1]]]; wv = numWF$[sq[[2]]]; wc = rcValWF$[sq[[3]], rc];
   {chanNameWF$[ch], 2 Re[wv]/b0, 2 Re[wc]/b0}];
oursWF$ = Association[Rule @@@ (({#[[1]], #[[2]] + I #[[3]]} &) /@ Rest[Import[FileNameJoin[{resDirWF$, "wud_numeric.csv"}], "CSV"]])];
KKWF$ = 16 Pi^2;
cmpWF$ = {};
(* relative difference, and the absolute difference for the renormalization constants *)
addCmpWF$[name_, theirs_, ours_] := AppendTo[cmpWF$, {name, N[theirs], N[ours], Abs[N[theirs - ours]]/Max[Abs[N[ours]], 10^-300],
    Abs[N[theirs - ours]]}];
Do[Module[{res, resDelta},
   valWF$ = valOfWF$[pt[[1]]];
   SetDelta[0.];
   rcNumWF$ = rcNumNowWF$[];
   res = chanWF$[#, rcNumWF$] & /@ chansWF$;
   Print["(b)", pt[[2]], " 2 Re(M0^* M1)/|M0|^2 (FormCalc): ", {#[[1]], #[[2]], #[[3]]} & /@ res];
   (* UV finiteness of the FormCalc sum: change LoopTools' Delta (the renormalization constants are evaluated again) *)
   SetDelta[1000.];
   resDelta = chanWF$[#, rcNumNowWF$[]] & /@ chansWF$;
   SetDelta[0.];
   Print["(b)", pt[[2]], " the sum vertex + counterterm with Delta = 1000 minus Delta = 0, max (expect ~1e-12 or less): ",
     Max[Abs[(resDelta[[All, 2]] + resDelta[[All, 3]]) - (res[[All, 2]] + res[[All, 3]])]]];
   Do[addCmpWF$["delta_vertex_" <> r[[1]] <> pt[[2]], r[[2]], oursWF$["delta_vertex_" <> r[[1]] <> pt[[2]]]];
     addCmpWF$["delta_ct_OS_" <> r[[1]] <> pt[[2]], r[[3]], oursWF$["delta_ct_OS_" <> r[[1]] <> pt[[2]]]], {r, res}];
   Do[With[{ab = ToString[a] <> ToString[b]},
     addCmpWF$["K_dZuL_" <> ab <> pt[[2]], KKWF$ rcNumWF$[dZfL1[3, a, b]], oursWF$["K_dZuL_" <> ab <> pt[[2]]]];
     addCmpWF$["K_dZdL_" <> ab <> pt[[2]], KKWF$ rcNumWF$[dZfL1[4, a, b]], oursWF$["K_dZdL_" <> ab <> pt[[2]]]];
     addCmpWF$["K_dVDS_" <> ab <> pt[[2]], KKWF$ rcNumWF$[dCKM1[a, b]], oursWF$["K_dVDS_" <> ab <> pt[[2]]]]], {a, 3}, {b, 3}];
   addCmpWF$["K_dZW" <> pt[[2]], KKWF$ rcNumWF$[dZW1], oursWF$["K_dZW" <> pt[[2]]]];
   addCmpWF$["K_dZe_minus_dsw_over_sw_fin" <> pt[[2]], KKWF$ (rcNumWF$[dZe1] - rcNumWF$[dSW1]/N[valWF$["SW"]]),
     oursWF$["K_dZe_minus_dsw_over_sw_fin" <> pt[[2]]]]],
  {pt, {{1, ""}, {10, "_h"}}}];
Print["(c) FormCalc (SM.mod) against this note's model: quantity, FormCalc, note, relative difference, absolute difference"];
Scan[Print["   ", #[[1]], ":  ", #[[2]], ",  ", #[[3]], ",  ", ScientificForm[#[[4]], 2], ",  ", ScientificForm[#[[5]], 2]] &, cmpWF$];
Export[FileNameJoin[{resDirWF$, "wud_formcalc.csv"}],
  Prepend[{#[[1]], ToString[CForm[Re[#[[2]]]]], ToString[CForm[Im[#[[2]]]]], ToString[CForm[#[[4]]]], ToString[CForm[#[[5]]]]} & /@ cmpWF$,
   {"quantity", "re_formcalc", "im_formcalc", "rel_diff_to_note", "abs_diff_to_note"}], "CSV"];
selWF$[pat_, sfx_] := Select[cmpWF$, StringMatchQ[#[[1]], pat ~~ __ ~~ sfx] && If[sfx === "", ! StringEndsQ[#[[1]], "_h"], True] &];
Print["Summary: max relative difference of 2 Re(M0^* M1)/|M0|^2, vertex and counterterm (benchmark; m_u, m_d x 10): ",
  ScientificForm[Max[selWF$["delta_", ""][[All, 4]]], 2], "; ", ScientificForm[Max[selWF$["delta_", "_h"][[All, 4]]], 2],
  ";  max absolute difference of K dZ^L, K dV^DS, K dZ_W, K (dZ_e - dsw/sw) (benchmark; x 10): ",
  ScientificForm[Max[selWF$["K_", ""][[All, 5]]], 2], "; ", ScientificForm[Max[selWF$["K_", "_h"][[All, 5]]], 2],
  ";  total ", Round[AbsoluteTime[] - t0WF$], " s"];
ResetDirectory[];
Quiet[DeleteDirectory[workDirWF$, DeleteContents -> True]];
