(* ::Package:: *)

(* ::Title:: *)
(*Step (4b), 3 of 3: the NLO UFO of QCDZp.fr (UV counterterms and R2 vertices of NLOCT)*)


(* ::Text:: *)
(*Research note models/sm_pp, step (4b), as the QCD note's nlo_ufo.wl.  The vertices with the Z' are printed here and tested*)
(*through MadLoop's virtual correction to u u~ > e+ e- against the note's own form factor (zp_madloop.py).  FeynmanGauge = True*)
(*(MadGraph's loops need it); the decimals NLOCT writes are made exact ratios (MG5 writes 7 digits).  -> generated/QCDZp_NLO_UFO.*)
(*Batch:  wolframscript -file zp_nlo_ufo.wl*)


srcDirZU$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirZU$];
LoadModel["QCDZp.fr"];
SetDirectory[FileNameJoin[{srcDirZU$, "generated"}]];
Get["QCDZp_CT.nlo"];
R2$vertlist = DeleteCases[R2$vertlist, Last[{}]];
Print["perturbed orders: ", FR$InteractionOrderPerturbativeExpansion, ";  R2 vertices: ", Length[R2$vertlist], ";  UV vertices: ",
  Length[UV$vertlist]];
Print["vertex legs: R2 ", R2$vertlist[[All, 1, All, 1]], ";  UV ", UV$vertlist[[All, 1, All, 1]]];
Do[If[MemberQ[v[[1, All, 1]], Zp], Print[t, " ", v[[1, All, 1]], ": ", InputForm[Simplify[v[[2]]]]]], {t, {"R2", "UV"}},
  {v, If[t === "R2", R2$vertlist, UV$vertlist]}];
FeynmanGauge = True;
If[DirectoryQ["QCDZp_NLO_UFO"], DeleteDirectory["QCDZp_NLO_UFO", DeleteContents -> True]];
WriteUFO[LQCDZp, UVCounterterms -> UV$vertlist, R2Vertices -> R2$vertlist, Output -> "QCDZp_NLO_UFO"];
exactUFO$[file_] := Module[{txt = Import[file, "Text"], new},
   new = StringReplace[txt, RegularExpression["(?<![\\w.])(\\d+\\.\\d{7,})"] :>
       Module[{r = Rationalize[ToExpression["$1"], 10^-15]},
         If[Head[r] === Rational, "(" <> ToString[Numerator[r]] <> "./" <> ToString[Denominator[r]] <> ".)", "$1"]]];
   Export[file, new, "Text"];
   Length[StringCases[txt, RegularExpression["(?<![\\w.])\\d+\\.\\d{7,}"]]]];
Print["decimal coefficients made exact in QCDZp_NLO_UFO: ",
  exactUFO$[FileNameJoin[{Directory[], "QCDZp_NLO_UFO", #}]] & /@ {"couplings.py", "CT_couplings.py"}];
Print["written: ", FileNames["QCDZp_NLO_UFO"]];
