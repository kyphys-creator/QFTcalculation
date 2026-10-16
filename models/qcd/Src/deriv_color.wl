(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: the colour algebra for general SU(N) (FeynCalc)*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices (FeynCalc 10.2.1, SUNSimplify with symbolic N).*)
(*  app:color (T1): T^c T^b T^c, f^{acd} f^{bcd}, tr([T^a,T^c][T^b,T^c]), the four traces, f^{abc} T^b T^c;*)
(*  app:tree 「(C) gg -> gg。」 (T3): the colour matrix of g g -> g g in (c_s, c_t) / (C_A^2 d_A) and the Jacobi identity c_u = c_t - c_s.*)
(*Each line prints the difference (0).  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_color.txt.*)
(*Usage (from Src/): wolframscript -file deriv_color.wl   (a few seconds)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_color.wl.  Interactive:  ~/hep/bin/wopen deriv_color.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
Get["FeynCalc`"];
$FCAdvice = False;
s[x_] := Simplify[SUNSimplify[x, SUNNToCACF -> False] /. SUNN -> NN];
CFv = (NN^2 - 1)/(2 NN); CAv = NN; dA = NN^2 - 1;

(* ::Section:: *)
(*colour identities of app:color (general N)*)


Print["T^c T^b T^c + T_F/N T^b: ", s[SUNT[c] . SUNT[b] . SUNT[c] + 1/(2 NN) SUNT[b]]];
Print["f^{acd}f^{bcd} - 2 T_F N delta^{ab}: ", s[SUNF[a, c, d] SUNF[b, c, d] - NN SUNDelta[a, b]]];
Print["tr([Ta,Tc][Tb,Tc]) + 2 T_F^2 N delta^{ab}: ",
  s[SUNTrace[(SUNT[a] . SUNT[c] - SUNT[c] . SUNT[a]) . (SUNT[b] . SUNT[c] - SUNT[c] . SUNT[b])] + NN/2 SUNDelta[a, b]]];
Print["four traces: ", s[{SUNTrace[SUNT[a] . SUNT[c] . SUNT[b] . SUNT[c]] + 1/(4 NN) SUNDelta[a, b],
    SUNTrace[SUNT[a] . SUNT[c] . SUNT[c] . SUNT[b]] - CFv/2 SUNDelta[a, b],
    SUNTrace[SUNT[c] . SUNT[a] . SUNT[b] . SUNT[c]] - CFv/2 SUNDelta[a, b],
    SUNTrace[SUNT[c] . SUNT[a] . SUNT[c] . SUNT[b]] + 1/(4 NN) SUNDelta[a, b]}]];
Print["f^{abc} T^b T^c - i/2 C_A T^a: ", s[SUNF[a, b, c] SUNT[b] . SUNT[c] - I/2 NN SUNT[a]]];


(* ::Subsubsection:: *)
(*Inspect: two of the four traces before the comparison*)


If[$Notebooks,
  s[{SUNTrace[SUNT[a] . SUNT[c] . SUNT[b] . SUNT[c]], SUNTrace[SUNT[a] . SUNT[c] . SUNT[c] . SUNT[b]]}]
]


(* ::Section:: *)
(*the g g -> g g colour matrix (app:tree (C))*)


(* colour matrix of gg -> gg in the basis c_s = f^{abe}f^{cde}, c_t = f^{ace}f^{bde}; c_u = f^{ade}f^{bce} = c_t - c_s *)
cs[e_] := SUNF[a, b, e] SUNF[c, d, e]; ct[e_] := SUNF[a, c, e] SUNF[b, d, e]; cu[e_] := SUNF[a, d, e] SUNF[b, c, e];
Print["sum c_s c_s / (C_A^2 d_A): ", s[cs[e] cs[g]]/(CAv^2 dA) // Simplify];
Print["sum c_s c_t / (C_A^2 d_A): ", s[cs[e] ct[g]]/(CAv^2 dA) // Simplify];
Print["sum c_t c_t / (C_A^2 d_A): ", s[ct[e] ct[g]]/(CAv^2 dA) // Simplify];


(* ::Subsubsection:: *)
(*Inspect: the colour matrix in (c_s, c_t), units C_A^2 d_A*)


If[$Notebooks,
  MatrixForm[Simplify[{{s[cs[e] cs[g]], s[cs[e] ct[g]]}, {s[ct[e] cs[g]], s[ct[e] ct[g]]}}/(CAv^2 dA)]]
]


Print["sum (c_u - c_t + c_s)^2 (Jacobi, expect 0): ", s[(cu[e] - ct[e] + cs[e]) (cu[g] - ct[g] + cs[g])]];