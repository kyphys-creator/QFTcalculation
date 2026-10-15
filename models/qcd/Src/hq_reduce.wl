(* ::Package:: *)

(* ::Title:: *)
(*Step (9): real emission -> partial fractions -> cut families -> Kira (reverse unitarity) -> distinct master integrals*)


(* ::Text:: *)
(*Research note models/qcd, step (9).  Reads work/hq/real_<chan>.m (qq, qg) or work/hq/pairs_gg/ (gg: pair by pair, which keeps the*)
(*numerators small; the whole gg integrand at once gave 12875 partial-fraction pieces and 42 families instead of 172 and 15), applies*)
(*hq_pfrac.wl, writes the families (3 cut + 4 forms) and runs Kira 3.1 with the cut propagators 1, 2, 3 (symbolic s, d; m^2 = mt2 = 1;*)
(*preferred masters: each sector with a dot on a non-cut line or a numerator, so that no master has a dotted cut propagator).  The*)
(*masters of different families are then identified: an integral is fixed by its cut indices and the forms with their powers, up to*)
(*k1 <-> k2 and p1 <-> p2 (the integrals depend on s only); a few families that host a representative of every distinct integral are*)
(*chosen for AMFlow.  Writes work/hq/families_<chan>.m, work/hq/red_<chan>.m (sum |M|^2 integrated = combination of masters, with*)
(*SU(3), g = m = 1), work/hq/unique_<chan>.m.  Usage: wolframscript -file hq_reduce.wl chan  (qq, qg: about 2 minutes; gg: about 5).*)


(* ::Section:: *)
(*Setup*)


srcDirHK$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
Get[FileNameJoin[{srcDirHK$, "hq_pfrac.wl"}]];
chanHK$ = If[$Notebooks, "qq", $ScriptCommandLine[[2]]];
workHK$ = FileNameJoin[{srcDirHK$, "work", "hq"}];
famPrefix = "R" <> chanHK$;
kiraHK$ = FileNameJoin[{$HomeDirectory, "hep", "Kira-3.1", "bin", "kira"}];
fermatHK$ = FileNameJoin[{$HomeDirectory, "hep", "fermat-7.9b", "fer64"}];
su3HK$ = {CA -> 3, CF -> 4/3, gS -> 1, mt -> 1};


(* ::Section:: *)
(*(a) partial fractions and families*)


t0HK$ = AbsoluteTime[];
splitHK$ = If[chanHK$ === "gg",
   (Get[#] /. su3HK$) & /@ FileNames["p_*.m", FileNameJoin[{workHK$, "pairs_gg"}]],
   {Get[FileNameJoin[{workHK$, "real_" <> chanHK$ <> ".m"}]] /. su3HK$}];
splitHK$ = pfRationalSplit /@ splitHK$;
Print["(a) ", chanHK$, ": partial fractions ", Round[AbsoluteTime[] - t0HK$], " s, ", Total[Length[#[[2]]] & /@ splitHK$], " pieces"];
famsHK$ = makeFamilies[Union[Flatten[Keys /@ #[[2]][[All, 2]] & /@ splitHK$, 1]]];
Put[famsHK$, FileNameJoin[{workHK$, "families_" <> chanHK$ <> ".m"}]];
Print["(a) ", Length[famsHK$], " families: ", famsHK$];
gliHK$ = Total[toGLIgroup[#[[1]], #[[2]], famsHK$] & /@ splitHK$];
Print["(a) ", Length[Union[Cases[gliHK$, _GLI, Infinity]]], " family integrals, ", Round[AbsoluteTime[] - t0HK$], " s"];


(* ::Subsubsection:: *)
(*Inspect: the integrand back from the family integrals at a point (symmetrized over k1 <-> k2), relative to the input*)


If[$Notebooks, Module[{r = Get[FileNameJoin[{workHK$, "real_" <> chanHK$ <> ".m"}]] /. su3HK$, back, pt = {x1 -> -3/7, x2 -> -11/13, x3 -> -5/17, x4 -> -2/3, s -> 16/3, D -> 37/10}},
   back = gliHK$ /. GLI[f_, n_] :> Module[{fam = famsHK$[[ToExpression[StringDrop[f, StringLength[famPrefix]]]]]}, Product[formsPF[fam[[j]]]^-n[[3 + j]], {j, 4}]];
   N[((r + (r /. swapX)) - (back + (back /. swapX)))/(r + (r /. swapX)) /. pt, 20]]]


(* ::Section:: *)
(*(b) Kira*)


propStrHK$[{p_, m_}] := "      - [ \"" <> StringReplace[ToString[p, InputForm], " " -> ""] <> "\", \"" <> ToString[m, InputForm] <> "\" ]\n";
preferredHK$ = Union[Flatten[Table[Module[{base = Table[If[MemberQ[sub, j], 1, 0], {j, 4}]},
       Join[{base}, Table[ReplacePart[base, j -> 2], {j, sub}], Table[ReplacePart[base, j -> -1], {j, Complement[Range[4], sub]}]]],
      {sub, Subsets[Range[4]]}], 1]];
runFamHK$[name_, glis_] := Module[{i = ToExpression[StringDrop[name, StringLength[famPrefix]]], d = FileNameJoin[{workHK$, "kira", name}], props, r, sm, ok},
   Quiet[DeleteDirectory[d, DeleteContents -> True]]; CreateDirectory[FileNameJoin[{d, "config"}], CreateIntermediateDirectories -> True];
   props = Join[{{k1, mt2}, {k2, mt2}, {p1 + p2 - k1 - k2, 0}}, momPF /@ famsHK$[[i]]];
   Export[FileNameJoin[{d, "config", "integralfamilies.yaml"}], "integralfamilies:\n  - name: " <> name <>
      "\n    loop_momenta: [k1, k2]\n    top_level_sectors: [b1111111]\n    propagators:\n" <> StringJoin[propStrHK$ /@ props] <>
      "    cut_propagators: [1, 2, 3]\n", "Text"];
   Export[FileNameJoin[{d, "config", "kinematics.yaml"}], "kinematics:\n  incoming_momenta: [p1, p2]\n  outgoing_momenta: [p3]\n" <>
      "  momentum_conservation: [p3, p1+p2]\n  kinematic_invariants:\n    - [s, 2]\n    - [mt2, 2]\n  scalarproduct_rules:\n" <>
      "    - [[p1,p1], 0]\n    - [[p2,p2], 0]\n    - [[p1,p2], s/2]\n  symbol_to_replace_by_one: mt2\n", "Text"];
   r = Max[Total[Select[#[[2]], Positive]] & /@ glis]; sm = Max[-Total[Select[#[[2]], Negative]] & /@ glis];
   Export[FileNameJoin[{d, "targets"}], StringRiffle[(name <> "[" <> StringRiffle[ToString /@ #[[2]], ","] <> "]") & /@ glis, "\n"] <> "\n", "Text"];
   Export[FileNameJoin[{d, "preferred"}], StringRiffle[(name <> "[" <> StringRiffle[ToString /@ Join[{1, 1, 1}, #], ","] <> "]") & /@ preferredHK$, "\n"] <> "\n", "Text"];
   Export[FileNameJoin[{d, "job.yaml"}], "jobs:\n  - reduce_sectors:\n      reduce:\n        - {topologies: [" <> name <> "], sectors: [b1111111], r: " <>
      ToString[r + 1] <> ", s: " <> ToString[sm] <> "}\n      select_integrals:\n        select_mandatory_list:\n          - [" <> name <> ", targets]\n" <>
      "      preferred_masters: preferred\n      run_initiate: true\n      run_triangular: true\n      run_back_substitution: true\n      integral_ordering: 2\n" <>
      "  - kira2math:\n      target:\n        - [" <> name <> ", targets]\n", "Text"];
   ok = RunProcess[{kiraHK$, "--parallel=8", "job.yaml"}, ProcessDirectory -> d, ProcessEnvironment -> <|"FERMATPATH" -> fermatHK$, "PATH" -> Environment["PATH"]|>];
   If[ok["ExitCode"] =!= 0, Print["   ", name, ": Kira failed"]; Print[StringTake[ok["StandardOutput"], -1500]]];
   Get[FileNameJoin[{d, "results", name, "kira_targets.m"}]]];
targetsHK$ = GroupBy[Union[Cases[gliHK$, _GLI, Infinity]], First];
toGHK$[e_] := e /. (f_Symbol)[a__Integer] /; StringMatchQ[SymbolName[f], famPrefix ~~ DigitCharacter ..] :> GLI[SymbolName[f], {a}];
rulesHK$ = Flatten[Table[toGHK$[Normal[runFamHK$[k, targetsHK$[k]]]], {k, Keys[targetsHK$]}]] /. Rule[a_, b_] :> Rule[toGHK$[a], toGHK$[b]];
redHK$ = Collect[gliHK$ /. rulesHK$ /. {d -> D}, _GLI, Factor];
mastersHK$ = Union[Cases[redHK$, _GLI, Infinity]];
Print["(b) Kira: ", Length[mastersHK$], " masters; dotted cut propagators among them: ", Select[mastersHK$, #[[2, 1 ;; 3]] =!= {1, 1, 1} &], "  (expect none); ",
  Round[AbsoluteTime[] - t0HK$], " s"];
Put[redHK$, FileNameJoin[{workHK$, "red_" <> chanHK$ <> ".m"}]];


(* ::Section:: *)
(*(c) distinct masters and the families for AMFlow*)


groupHK$ = {Identity, swapPF[#] &, pswapPF[#] &, pswapPF[swapPF[#]] &}; kswapHK$ = {False, True, False, True};
famOfHK$[g_GLI] := famsHK$[[ToExpression[StringDrop[g[[1]], StringLength[famPrefix]]]]];
canonHK$[g_GLI] := Module[{f = famOfHK$[g], n = g[[2]], k},
   k = {n[[1 ;; 3]], Sort[DeleteCases[Transpose[{f, n[[4 ;; 7]]}], {_, 0}]]};
   First[Sort[Table[{If[kswapHK$[[i]], k[[1, {2, 1, 3}]], k[[1]]], Sort[{groupHK$[[i]][#[[1]]], #[[2]]} & /@ k[[2]]]}, {i, 4}]]]];
keysHK$ = GroupBy[mastersHK$, canonHK$];
hostHK$[fi_, key_] := AnyTrue[groupHK$, Function[op, SubsetQ[famsHK$[[fi]], op /@ key[[2, All, 1]]]]];
needHK$ = Keys[keysHK$]; chosenHK$ = {};
While[needHK$ =!= {}, Module[{best = First[MaximalBy[Range[Length[famsHK$]], Count[needHK$, k_ /; hostHK$[#, k]] &]]},
   AppendTo[chosenHK$, best]; needHK$ = Select[needHK$, !hostHK$[best, #] &]]];
repHK$ = Association[Table[Module[{fi = First[Select[chosenHK$, hostHK$[#, k] &]], f, oi, idx},
     f = famsHK$[[fi]]; oi = First[Select[Range[4], Function[i, SubsetQ[f, groupHK$[[i]] /@ k[[2, All, 1]]]]]];
     idx = Table[Total[Cases[k[[2]], {x_, p_} /; groupHK$[[oi]][x] === f[[j]] :> p]], {j, 4}];
     k -> GLI[famPrefix <> ToString[fi], Join[If[kswapHK$[[oi]], k[[1, {2, 1, 3}]], k[[1]]], idx]]], {k, Keys[keysHK$]}]];
Put[<|"keys" -> keysHK$, "rep" -> repHK$, "chosen" -> chosenHK$|>, FileNameJoin[{workHK$, "unique_" <> chanHK$ <> ".m"}]];
Print["(c) ", Length[mastersHK$], " masters -> ", Length[keysHK$], " distinct integrals in ", Length[chosenHK$], " families for AMFlow: ", (famPrefix <> ToString[#]) & /@ chosenHK$];
