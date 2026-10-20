(* ::Package:: *)

(* ::Title:: *)
(*Step (2b), 3 of 3: the NLO UFO of QCDH.fr (UV counterterms and R2 vertices of NLOCT)*)


(* ::Text:: *)
(*Research note models/sm_pp, step (2b), as the QCD note's nlo_ufo.wl.  The QCD vertices are the QCD note's (checked there against*)
(*the hand values and DGPP); the vertices with H are printed here and tested through MadLoop's virtual correction to g g -> H*)
(*against the note's own F^(1) (gh_madloop.py).  FeynmanGauge = True (MadGraph's loops need it); the decimals NLOCT writes are made*)
(*exact ratios (MG5 writes 7 digits).  -> generated/QCDH_NLO_UFO.*)
(*Batch:  wolframscript -file gh_nlo_ufo.wl*)


srcDirGU$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirGU$];
LoadModel["QCDH.fr"];
SetDirectory[FileNameJoin[{srcDirGU$, "generated"}]];
Get["QCDH_CT.nlo"];
R2$vertlist = DeleteCases[R2$vertlist, Last[{}]];
Print["perturbed orders: ", FR$InteractionOrderPerturbativeExpansion, ";  R2 vertices: ", Length[R2$vertlist], ";  UV vertices: ",
  Length[UV$vertlist]];
Print["vertex legs: R2 ", R2$vertlist[[All, 1, All, 1]], ";  UV ", UV$vertlist[[All, 1, All, 1]]];
Do[If[MemberQ[v[[1, All, 1]], H], Print["R2 ", v[[1, All, 1]], ": ", InputForm[Simplify[v[[2]]]]]], {v, R2$vertlist}];
Do[If[MemberQ[v[[1, All, 1]], H], Print["UV ", v[[1, All, 1]], ": ", InputForm[Simplify[v[[2]]]]]], {v, UV$vertlist}];
FeynmanGauge = True;
If[DirectoryQ["QCDH_NLO_UFO"], DeleteDirectory["QCDH_NLO_UFO", DeleteContents -> True]];
WriteUFO[LQCDH, UVCounterterms -> UV$vertlist, R2Vertices -> R2$vertlist, Output -> "QCDH_NLO_UFO"];
exactUFO$[file_] := Module[{txt = Import[file, "Text"], new},
   new = StringReplace[txt, RegularExpression["(?<![\\w.])(\\d+\\.\\d{7,})"] :>
       Module[{r = Rationalize[ToExpression["$1"], 10^-15]},
         If[Head[r] === Rational, "(" <> ToString[Numerator[r]] <> "./" <> ToString[Denominator[r]] <> ".)", "$1"]]];
   Export[file, new, "Text"];
   Length[StringCases[txt, RegularExpression["(?<![\\w.])\\d+\\.\\d{7,}"]]]];
Print["decimal coefficients made exact in QCDH_NLO_UFO: ",
  exactUFO$[FileNameJoin[{Directory[], "QCDH_NLO_UFO", #}]] & /@ {"couplings.py", "CT_couplings.py"}];
Print["written: ", FileNames["QCDH_NLO_UFO"]];
