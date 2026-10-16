(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: the exact NLO f^(1) of Czakon-Mitov very close to threshold*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices.  app:hq 「閾値の対数。」 (I2): the exact NLO f^(1) of Czakon and Mitov*)
(*(arXiv:0811.4119, NLOXSections.m) at beta = 1e-2 ... 1e-6 against Eq. (hqthr) with the logarithmic coefficients 2 C_i and*)
(*-(8 C_i + w8 C_A) derived from the soft real emission.  SU(3), n_l = 5, m = mu = 1 (both alpha_s schemes coincide);*)
(*f0 = coefficient of as^2, f1 = coefficient of as^3/(4 Pi).  The residual r(beta) = f1/(f0/(4 Pi^2)) - [Coulomb + 2 C_i L^2 -*)
(*(8 C_i + w8 C_A) L + a_ij], L = Log[8 beta^2], must vanish like beta (up to logs); a wrong log coefficient would make it grow like L.*)
(*Reads ../Ref/cm08_src/x/NLOXSections.m, the same file as hq_cm.wl.  Ref/ is not in the repository: download it as described in hq_cm.wl*)
(*(in models/qcd/Ref/cm08_src: curl -o cm08.tar.gz https://arxiv.org/e-print/0811.4119; mkdir -p x; tar -xzf cm08.tar.gz -C x); without it*)
(*the script stops with a message.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_hq_thr_cm.txt.*)
(*Usage (from Src/): wolframscript -file deriv_hq_thr_cm.wl   (about 4 minutes)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_hq_thr_cm.wl.  Interactive:  ~/hep/bin/wopen deriv_hq_thr_cm.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


srcDirCM$ = Which[StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName], $Notebooks, NotebookDirectory[], True, Directory[]];
cmFileCM$ = FileNameJoin[{ParentDirectory[srcDirCM$], "Ref", "cm08_src", "x", "NLOXSections.m"}];
If[!FileExistsQ[cmFileCM$],
  Print["deriv_hq_thr_cm.wl needs models/qcd/Ref/cm08_src/x/NLOXSections.m (the source of arXiv:0811.4119), which is not in ",
    "the repository: in models/qcd/Ref/cm08_src run  curl -o cm08.tar.gz https://arxiv.org/e-print/0811.4119; mkdir -p x; ",
    "tar -xzf cm08.tar.gz -C x  (as for hq_cm.wl)."];
  If[$Notebooks, Abort[], Exit[1]]];
Get[cmFileCM$];

(* ::Section:: *)
(*harmonic polylogarithms and Eq. (hqthr)*)


wp = 50;
fw[0][t_] := 1/t; fw[1][t_] := 1/(1 - t); fw[-1][t_] := 1/(1 + t);
ClearAll[hpl];
hpl[w_List, x_?NumericQ] := hpl[w, x] = Which[
   AllTrue[w, # == 0 &], Log[x]^Length[w]/Length[w]!,
   Length[w] == 1, Switch[w[[1]], 1, -Log[1 - x], -1, Log[1 + x]],
   True, NIntegrate[fw[First[w]][t] hpl[Rest[w], t], {t, 0, x}, WorkingPrecision -> wp, PrecisionGoal -> 30, MaxRecursion -> 30]];
(* auxiliary gg integrals: use the expansions around x = 1 supplied in the file (truncation (1-x)^11 ~ 1e-30 here) *)
aux = {f1[x] -> (f1x1[x] /. Ox1[_] -> 0), f2[x] -> (f2x1[x] /. Ox1[_] -> 0), f3[x] -> (f3x1[x] /. Ox1[_] -> 0), f4[x] -> (f4x1[x] /. Ox1[_] -> 0)};
CA = 3; CF = 4/3; nl = 5; w8gg = (9 - 4)/(9 - 2);
aqq = CF (8 - Pi^2/3 + 3 Log[2] - 2 Log[2]^2) + CA (77/9 - Pi^2/4 - 2 Log[2]) + nl (-5/9 + 2 Log[2]/3) - 8/9;
agg = CA ((21*9 - 50)/(9 - 2) - (17*9 - 40) Pi^2/(24 (9 - 2)) + (9 - 4) Log[2]/(9 - 2) - 2 Log[2]^2) + CF (-5 + Pi^2/4);
thr[c_, b_] := Module[{L = Log[8 b^2]}, Switch[c,
    "qq", (CF - CA/2) Pi^2/(2 b) + 2 CF L^2 - (8 CF + CA) L + aqq,
    "gg", (CF - w8gg CA/2) Pi^2/(2 b) + 2 CA L^2 - (8 CA + w8gg CA) L + agg]];
expr = <|"qq" -> NLOXSectionQQ, "gg" -> NLOXSectionGG|>;


(* ::Subsubsection:: *)
(*Inspect: the q qbar cross section of Czakon and Mitov (SU(3), n_l = 5, m = mu = 1) in HPLs H[..., x]*)


If[$Notebooks,
  Short[NLOXSectionQQ /. {N -> 3, nl -> 5, m -> 1, mu -> 1}, 6]
]


Print["a_qq = ", N[aqq, 12], ",  a_gg = ", N[agg, 12], "  (Czakon-Mitov Eqs. (26), (27), SU(3), n_l = 5)"];

(* ::Section:: *)
(*beta -> 0: the residuals for q qbar and g g*)


Do[Module[{t0 = AbsoluteTime[], e = expr[c] /. {N -> 3, nl -> 5, m -> 1, mu -> 1} /. aux},
   Do[Module[{b = SetPrecision[10^-k, wp], xv, ev, f0, f1, r},
      xv = (1 - b)/(1 + b);
      ev = Expand[e /. s -> 4/(1 - b^2) /. x -> xv /. H[a__, y_] :> hpl[{a}, y]];
      f0 = Coefficient[ev, as, 2]; f1 = Coefficient[ev, as, 3]/(4 Pi);
      r = f1/(f0/(4 Pi^2)) - thr[c, b];
      Print[c, "  beta = 1e-", k, ":  f0 = ", ScientificForm[N[f0, 12]], ",  f1 = ", ScientificForm[N[f1, 15]],
        ",  bracket f1/(f0/4pi^2) = ", N[f1/(f0/(4 Pi^2)), 15], ",  residual r = ", ScientificForm[N[r, 6]], ",  r/beta = ", N[r/b, 6]]],
     {k, {2, 3, 4, 5, 6}}];
   Print["   (", c, " done in ", Round[AbsoluteTime[] - t0], " s)"]], {c, {"qq", "gg"}}];
(* sensitivity: changing the ln coefficient by 1 would change r by L = Log[8 beta^2] *)
Print["for comparison, Log[8 beta^2] at beta = 1e-6: ", N[Log[8 10^-12], 6]];


(* ::Subsubsection:: *)
(*Inspect: Eq. (hqthr) at beta = 10^-3 for q qbar and g g*)


If[$Notebooks,
  N[{thr["qq", 10^-3], thr["gg", 10^-3]}, 12]
]
