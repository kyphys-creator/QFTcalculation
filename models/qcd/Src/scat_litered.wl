(* ::Package:: *)

(* ::Title:: *)
(*Step (4): IBP reduction of the one-loop integrals of q qbar -> Q Qbar and g g -> Q Qbar (LiteRed 1.83)*)


(* ::Text:: *)
(*Research note models/qcd, step (4), second stage (after scat_feyncalc.wl, before scat_eval.wl).  Runs in a kernel without*)
(*FeynCalc (LiteRed's Vectors` context shadows FeynCalc's MetricTensor).  Reads the family integrals GLI[family, {n1..n4}]*)
(*of work/scat/A/d*.m and work/scat/B/d*.m and reduces them to master integrals with LiteRed (the copy shipped with FIRE 7.1)*)
(*at the kinematic point of the note: m = 1, s = 10, t = -3 (p1.p2 = 5, p1.k1 = 2, p2.k1 = 3).  The nine families*)
(*(propagators (l + offset)^2 - mass^2, same order as famDefs$ in scat_feyncalc.wl):*)
(*  F1 = {l, l-p1, l-p1-p2, (l-p1-p2+k1, m)}  crossed q qbar box;   F2 = {l, l-p1, l-p1-p2, (l-k1, m)}  direct q qbar box;*)
(*  F3 = {l, (l+k1, m), (l-p1-p2+k1, m), l-p1}  heavy-quark vertex;   G1..G6  the six g g -> Q Qbar boxes.*)
(*Output: work/scat/A/ibp.m, work/scat/B/ibp.m with rules {family, indices} -> sum of coefficients(dd) x mJ[family, indices]*)
(*(dd = D).  The coefficients contain 1/(dd - 4) only in front of the A0 and B0 masters (degenerate triangles with a vanishing*)
(*Cayley determinant, i.e. the soft triangles); scat_eval.wl evaluates those masters to O(eps^2).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file scat_litered.wl  (after scat_feyncalc.wl).  Interactive:  ~/hep/bin/wopen scat_litered.wl in a fresh kernel, then "Run All Code"; the Inspect cells run only in the notebook.*)


(* ::Section:: *)
(*Setup*)


srcDirLR$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
workDirLR$ = FileNameJoin[{srcDirLR$, "work", "scat"}];
famDefsLR$ = {
   "F1" -> {{0, 0}, {-p1, 0}, {-p1 - p2, 0}, {-p1 - p2 + k1, 1}},
   "F2" -> {{0, 0}, {-p1, 0}, {-p1 - p2, 0}, {-k1, 1}},
   "F3" -> {{0, 0}, {k1, 1}, {-p1 - p2 + k1, 1}, {-p1, 0}},
   "G1" -> {{0, 1}, {-p1, 1}, {-p1 + k1, 0}, {p2, 1}},
   "G2" -> {{0, 0}, {-p1, 0}, {-p1 + k1, 1}, {p2, 0}},
   "G3" -> {{0, 1}, {-p1, 1}, {p2, 1}, {p2 - k1, 0}},
   "G4" -> {{0, 0}, {-p1, 0}, {p2, 0}, {p2 - k1, 1}},
   "G5" -> {{0, 1}, {-k1, 0}, {-p1, 1}, {p2 - k1, 0}},
   "G6" -> {{0, 0}, {-k1, 1}, {-p1, 0}, {p2 - k1, 1}}};
AppendTo[$Path, FileNameJoin[{$HomeDirectory, "hep", "src", "fire-7.1", "FIRE7", "extra", "LiteRed", "Setup"}]];
Quiet[Get["LiteRed`"]];
SetDim[dd];
Declare[{ql, e1, e2, e3}, Vector];
sp[e1, e1] = 0; sp[e2, e2] = 0; sp[e3, e3] = 1; sp[e1, e2] = 5; sp[e1, e3] = 2; sp[e2, e3] = 3;


(* ::Section:: *)
(*The bases*)


If[DirectoryQ[FileNameJoin[{workDirLR$, "litered"}]], DeleteDirectory[FileNameJoin[{workDirLR$, "litered"}], DeleteContents -> True]];
Quiet[Do[With[{b = Symbol[fd[[1]]]},
    NewBasis[b, (sp[ql + (#[[1]] /. {p1 -> e1, p2 -> e2, k1 -> e3})] - #[[2]]^2) & /@ fd[[2]], {ql},
     Directory -> FileNameJoin[{workDirLR$, "litered", fd[[1]]}]];
    GenerateIBP[b]; AnalyzeSectors[b]; FindSymmetries[b]; SolvejSector /@ UniqueSectors[b]], {fd, famDefsLR$}]];
Print["(a) LiteRed bases: ", famDefsLR$[[All, 1]], ";  masters per family: ", Table[Length[MIs[Symbol[f]]], {f, famDefsLR$[[All, 1]]}]];


(* ::Subsubsection:: *)
(*Inspect: the master integrals of each family*)


If[$Notebooks,
  Table[f -> MIs[Symbol[f]], {f, famDefsLR$[[All, 1]]}]
]


(* ::Section:: *)
(*Reduction*)


(* the slowest diagrams of (B) come as pieces part_<i>_<k>.m (k = power of 1 - xi): sum them into d<i>.m *)
mergeLR$[proc_] := Module[{parts = FileNames["part_*.m", FileNameJoin[{workDirLR$, proc}]], ids},
   ids = Union[StringCases[FileNameTake[#], "part_" ~~ i : DigitCharacter .. ~~ "_" :> i][[1]] & /@ parts];
   Do[Put[Total[Get /@ Select[parts, StringStartsQ[FileNameTake[#], "part_" <> i <> "_"] &]], FileNameJoin[{workDirLR$, proc, "d" <> i <> ".m"}]], {i, ids}];
   If[ids =!= {}, Print["(b) process ", proc, ": diagrams merged from pieces: ", ToExpression /@ ids]]];
reduceLR$[proc_] := Module[{files, gl, glis, red, t0 = AbsoluteTime[]},
   mergeLR$[proc];
   files = FileNames["d*.m", FileNameJoin[{workDirLR$, proc}]];
   gl = Get /@ files;
   glis = Union[Cases[gl, GLI[f_String, n_List] :> {f, n}, Infinity]];
   red = Table[g -> Collect[IBPReduce[j[Symbol[g[[1]]], Sequence @@ g[[2]]]] /. j[b_, i__] :> mJ[SymbolName[b], {i}], _mJ, Factor], {g, glis}];
   Put[red, FileNameJoin[{workDirLR$, proc, "ibp.m"}]];
   Print["(b) process ", proc, ": ", Length[files], " diagram files, ", Length[glis], " integrals reduced in ", Round[AbsoluteTime[] - t0],
    " s to ", Length[Union[Cases[red[[All, 2]], _mJ, Infinity]]], " masters; 1/(dd-4) in front of ",
    Union[Cases[Select[Flatten[Table[{m, Coefficient[r[[2]], m]}, {r, red}, {m, Union[Cases[r[[2]], _mJ, Infinity]]}], 1],
        !FreeQ[Denominator[Together[#[[2]]]], dd - 4] &][[All, 1]], _mJ]]];
   red];
redA$ = reduceLR$["A"];
redB$ = reduceLR$["B"];


(* ::Subsubsection:: *)
(*Inspect: the reduction of the soft heavy-quark triangle F3 {1,1,1,0} (vanishing Cayley determinant)*)


If[$Notebooks,
  Select[redA$, #[[1]] == {"F3", {1, 1, 1, 0}} &]
]
