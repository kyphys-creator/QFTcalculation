(* ::Package:: *)

(* ::Title:: *)
(*Step (9): f^(1)_ij of this work against the exact NLO result of Czakon and Mitov*)


(* ::Text:: *)
(*Research note models/qcd, step (9).  Reads the Mathematica file of arXiv:0811.4119 (NLOXSections.m: the NLO total cross sections of*)
(*q qbar, q g, g g for SU(N), in harmonic polylogarithms H[..., x], x = (1 - beta)/(1 + beta), and the integrals f1..f4 for g g) from*)
(*models/qcd/Ref/cm08_src/x/ (the source of arXiv:0811.4119, not in the repository: curl -o cm08.tar.gz https://arxiv.org/e-print/0811.4119,*)
(*tar -xzf cm08.tar.gz -C x).  The file contains definitions only.  At mu = m both schemes for alpha_s (n_l + 1 and n_l flavours) coincide.*)
(*The harmonic polylogarithms (weight <= 3) are evaluated from their integral representation (30 digits).  N = 3, n_l = 5, m = mu = 1:*)
(*f^(1) = (coefficient of as^3)/(4 pi).  -> results/hq_cm.csv (chan, s, f1 this work, f1 Czakon-Mitov, relative difference)*)
(*Also the exact f^(1) at the 80 Gauss-Legendre nodes of the hadronic integrals of hq_hadronic.py at 13 TeV and 1.96 TeV*)
(*(m_t = 172.5 GeV), from which hq_hadronic.py estimates the error of its interpolation of f^(1).  -> results/hq_cm_nodes.csv*)
(*Usage: wolframscript -file hq_cm.wl  (about 12 minutes)*)


srcDirHC$ = Which[StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName], $Notebooks, NotebookDirectory[], True, Directory[]];
Get[FileNameJoin[{ParentDirectory[srcDirHC$], "Ref", "cm08_src", "x", "NLOXSections.m"}]];
fwHC$[0][t_] := 1/t; fwHC$[1][t_] := 1/(1 - t); fwHC$[-1][t_] := 1/(1 + t);
ClearAll[hplHC$];
hplHC$[w_List, x_?NumericQ] := hplHC$[w, x] = Which[
   AllTrue[w, # == 0 &], Log[x]^Length[w]/Length[w]!,
   Length[w] == 1, Switch[w[[1]], 1, -Log[1 - x], -1, Log[1 + x]],
   True, NIntegrate[fwHC$[First[w]][t] hplHC$[Rest[w], t], {t, 0, x}, WorkingPrecision -> 30, PrecisionGoal -> 18, MaxRecursion -> 20]];
cmHC$ = <|"qq" -> NLOXSectionQQ, "qg" -> NLOXSectionGQ, "gg" -> NLOXSectionGG|>;
rowsHC$ = Flatten[Table[Module[{expr = cmHC$[c] /. {N -> 3, nl -> 5, m -> 1, mu -> 1}, tab},
     tab = Rest[Import[FileNameJoin[{srcDirHC$, "results", "hq_f1_" <> c <> ".csv"}], "CSV"]];
     Table[Module[{s0 = ToExpression[ToString[r[[2]]]], xv, f1cm, f1},
        xv = N[(1 - Sqrt[1 - 4/s0])/(1 + Sqrt[1 - 4/s0]), 30];
        f1cm = Coefficient[Expand[expr /. s -> s0 /. x -> xv /. H[a__, y_] :> hplHC$[{a}, y]], as, 3]/(4 Pi);
        f1 = r[[7]];
        {c, s0, f1, f1cm, (f1 - f1cm)/f1cm}], {r, tab}]], {c, {"qq", "qg", "gg"}}], 1];
Do[Print[c, ": max |f1/f1(Czakon-Mitov) - 1| = ", ToString[CForm[N[Max[Abs[Select[rowsHC$, #[[1]] == c &][[All, 5]]]], 3]]], " over ",
   Count[rowsHC$, {c, ___}], " points"], {c, {"qq", "qg", "gg"}}];
Export[FileNameJoin[{srcDirHC$, "results", "hq_cm.csv"}], "chan,s,f1,f1_cm,rel_diff\n" <>
   StringJoin[(StringRiffle[{#[[1]], ToString[#[[2]], InputForm], ToString[CForm[N[#[[3]], 17]]], ToString[CForm[N[#[[4]], 17]]], ToString[CForm[N[#[[5]], 4]]]}, ","] <> "\n") & /@ rowsHC$], "Text"];
Print["wrote results/hq_cm.csv"];
nodesHC$ = Flatten[Table[Module[{tau0 = 4 (345/2)^2/e^2}, Table[{e, tau0^u}, {u, NIntegrate`GaussRuleData[80, 30][[1]]}]], {e, {13000, 1960}}], 1];
nodeRowsHC$ = Flatten[Table[Module[{expr = cmHC$[c] /. {N -> 3, nl -> 5, m -> 1, mu -> 1}},
     Table[Module[{s0 = 4/nd[[2]], xv},
        xv = (1 - Sqrt[1 - 4/s0])/(1 + Sqrt[1 - 4/s0]);
        {nd[[1]], nd[[2]], c, Coefficient[Expand[expr /. s -> s0 /. x -> xv /. H[a__, y_] :> hplHC$[{a}, y]], as, 3]/(4 Pi)}], {nd, nodesHC$}]],
    {c, {"qq", "qg", "gg"}}], 1];
Export[FileNameJoin[{srcDirHC$, "results", "hq_cm_nodes.csv"}], "sqrtS,rho,chan,f1_cm\n" <>
   StringJoin[(StringRiffle[{ToString[#[[1]]], ToString[CForm[N[#[[2]], 17]]], #[[3]], ToString[CForm[N[#[[4]], 17]]]}, ","] <> "\n") & /@ nodeRowsHC$], "Text"];
Print["wrote results/hq_cm_nodes.csv"];
