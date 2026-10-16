(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: class sums of the two-loop diagrams for the LaTeX tables, and diagram (c)*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices.  From results/twoloop_perdiag.m (deriv_twoloop_perdiag.wl):*)
(*  - the class sums (colour stripped, as functions of eps: b, s and the 1/eps^2, 1/eps poles) in the row order of tab:twoloopclass and*)
(*    tab:twoloopclassgh (app:rg 「図の組ごとの値と z_21、z~_21（式 (z2)）。」) -> results/twoloop_latex_ref.txt*)
(*    (one row per line: name|b|s|eps^-2|eps^-1, read by deriv_twoloop_latex.py);*)
(*  - diagram 4 of the gluon self-energy, (c) (the quark loop crossed by a gluon): b and s exact in D -> results/twoloop_diag4.txt (read by*)
(*    deriv_twoloop_cftf.py, app:rg 「C_F T_F n_f の部分の手計算。」); its field content is printed.*)
(*Reads results/twoloop_perdiag.m.  Writes results/twoloop_latex_ref.txt, results/twoloop_diag4.txt.*)
(*Usage (from Src/): wolframscript -file deriv_twoloop_export.wl   (a few seconds)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_twoloop_export.wl.  Interactive:  ~/hep/bin/wopen deriv_twoloop_export.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


srcDirTE$ = Which[StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName], $Notebooks, NotebookDirectory[], True, Directory[]];
dat = Get[FileNameJoin[{srcDirTE$, "results", "twoloop_perdiag.m"}]];

(* ::Section:: *)
(*class sums in the row order of the LaTeX tables*)


vg = #["value"] & /@ dat["gluon"]; vc = #["value"] & /@ dat["ghost"];
bsOf[x_] := {Coefficient[x, GLI["k2", {1, 1, 1, 1, 0}]], -qq Coefficient[x, GLI["k2", {1, 0, 0, 1, 1}]]} /. D -> 4 - 2 ep;
strip[x_, col_] := Simplify[Which[col === "CA2", Coefficient[Expand[x], CA, 2] /. {CF -> 0, nf -> 0},
    col === "CATF", Coefficient[Expand[x], CA TF nf], col === "CFTF", Coefficient[Expand[x], CF TF nf]]];
gF[a_, b_] := Gamma[a + b - DD/2] Gamma[DD/2 - a] Gamma[DD/2 - b]/(Gamma[a] Gamma[b] Gamma[DD - a - b]);
jb = E^(2 ep EulerGamma) gF[1, 1]^2 /. DD -> 4 - 2 ep; jsh = -E^(2 ep EulerGamma) gF[1, 1] gF[ep, 1] /. DD -> 4 - 2 ep;
poles[{b_, s_}] := Module[{ser = Normal[Series[b jb + s jsh, {ep, 0, -1}]]}, {FullSimplify[Coefficient[ser, ep, -2]], FullSimplify[Coefficient[ser, ep, -1]]}];
row[name_, idx_, vals_, col_] := Module[{bs = strip[#, col] & /@ bsOf[Total[vals[[idx]]]]}, {name, bs[[1]], bs[[2]], Sequence @@ poles[bs]}];
rowsG = {row["a_gc", {16, 17}, vg, "CA2"], row["c_se", {13, 14}, vg, "CA2"], row["b", {10}, vg, "CA2"], row["d_tri", {5, 8, 9}, vg, "CA2"], row["ef", {2, 3, 19, 23}, vg, "CA2"],
   row["a_q", {15}, vg, "CATF"], row["q_tri", {6, 7}, vg, "CATF"], row["c_CA", {4}, vg, "CATF"], row["c_CF", {4}, vg, "CFTF"], row["q_se", {11, 12}, vg, "CFTF"]};
rowsC = {row["g_gc", {5, 7}, vc, "CA2"], row["c_se_line", {6}, vc, "CA2"], row["h", {3}, vc, "CA2"], row["crossed", {2}, vc, "CA2"], row["g_q", {4}, vc, "CATF"]};


(* ::Subsubsection:: *)
(*Inspect: the rows {name, b, s, eps^-2, eps^-1}*)


If[$Notebooks,
  TableForm[Join[rowsG, rowsC]]
]


str[x_] := StringReplace[ToString[InputForm[x /. ep -> eps]], {"^" -> "**"}];
Export[FileNameJoin[{srcDirTE$, "results", "twoloop_latex_ref.txt"}],
  StringRiffle[(StringRiffle[{#[[1]], str[#[[2]]], str[#[[3]]], str[#[[4]]], str[#[[5]]]}, "|"]) & /@ Join[rowsG, rowsC], "\n"] <> "\n", "Text"];
Print["wrote results/twoloop_latex_ref.txt with ", Length[rowsG] + Length[rowsC], " rows"];


(* ::Section:: *)
(*diagram 4, (c): the quark loop crossed by a gluon, for deriv_twoloop_cftf.py*)


v = dat["gluon"][[4]]["value"];
b = Factor[Coefficient[v, GLI["k2", {1, 1, 1, 1, 0}]]]; s = Factor[-qq Coefficient[v, GLI["k2", {1, 0, 0, 1, 1}]]];


(* ::Subsubsection:: *)
(*Inspect: b and s of diagram (c), exact in D*)


If[$Notebooks,
  {b, s}
]


Export[FileNameJoin[{srcDirTE$, "results", "twoloop_diag4.txt"}], StringJoin[ToString[InputForm[b]], "\n", ToString[InputForm[s]], "\n"], "Text"];
Print[dat["gluon"][[4]]["descr"]];