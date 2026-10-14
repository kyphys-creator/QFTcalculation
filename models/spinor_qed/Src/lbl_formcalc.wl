(* ::Package:: *)

(* ::Title:: *)
(*Step (10): photon-photon scattering with the unpatched FeynArts 3.12 and FormCalc 9.10*)


(* ::Text:: *)
(*Research note models/spinor_qed, step (10); independent of FeynCalc.  Run in its own kernel: the patched (FeynCalc) and*)
(*unpatched FeynArts must not be loaded together.  CalcFeynAmp with Dimension -> D (Dirac algebra in the loop in D dimensions),*)
(*one amplitude per flavour (the boxes selected by the fermion in the loop), FormCalc's own tensor reduction to LoopTools'*)
(*coefficient functions (D0i up to dd3333).  X = M/alpha^2 at the points of work/lbl_points_exact.txt (those marked for*)
(*LoopTools), with the explicit helicity vectors of the note: k1 along +z, k3 at angle theta, e = (-l e_theta - i e_phi)/sqrt2,*)
(*FormCalc's e[1], e[2] (incoming) and ec[3], ec[4] (outgoing, conjugated).  -> results/lbl_formcalc.csv*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file lbl_formcalc.wl  (in its own kernel; after lbl_numeric.py --points).  Interactive:  ~/hep/bin/wopen lbl_formcalc.wl  (in its own kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


Get["FeynArts`"];
Get["FormCalc`"];

srcDirLF$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelLF$ = FileNameJoin[{srcDirLF$, "generated", "SpinorQED_FA", "SpinorQED_FA"}];   (* FeynRules output, unpatched *)
workDirLF$ = CreateDirectory[];
SetDirectory[workDirLF$];   (* FormCalc writes its FORM files here *)
diagLF$ = InsertFields[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections, Reducible}],
   {V[1], V[1]} -> {V[1], V[1]}, InsertionLevel -> {Particles}, Model -> modelLF$, GenericModel -> modelLF$];


(* ::Section:: *)
(*(a) One amplitude per flavour*)


(* ::Subsubsection:: *)
(*Inspect: the boxes (unpatched FeynArts)*)


If[$Notebooks,
  Show[#, ImageSize -> 560] & /@ Render[Paint[diagLF$, ColumnsXRows -> {4, 3}, Numbering -> Simple, DisplayFunction -> Identity]]
]


diagELF$ = DiagramSelect[diagLF$, FreeQ[#, F[2]] &];
diagMLF$ = DiagramSelect[diagLF$, FreeQ[#, F[1]] &];
ampELF$ = CalcFeynAmp[CreateFeynAmp[diagELF$] /. M$FACouplings, Dimension -> D];
ampMLF$ = CalcFeynAmp[CreateFeynAmp[diagMLF$] /. M$FACouplings, Dimension -> D];
abbrLF$ = Abbr[];
Print["(a) boxes: electron ", Length[CreateFeynAmp[diagELF$]], ", muon ", Length[CreateFeynAmp[diagMLF$]],
  ";  loop functions in the electron amplitude: ", Length[Union[Cases[ampELF$, (h : A0i | B0i | C0i | D0i)[__], Infinity]]],
  ";  muon mass absent from the electron amplitude (expect True): ", FreeQ[ampELF$, MMU]];


(* ::Subsubsection:: *)
(*Inspect: the electron amplitude in FormCalc's abbreviations*)


If[$Notebooks, Short[ampELF$, 20]]


(* ::Section:: *)
(*(b) LoopTools values at the points*)


Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetMudim[1]; SetDelta[0];
gmLF$ = DiagonalMatrix[{1, -1, -1, -1}];
polvLF$[ct_, st_, cph_, lm_] := Join[{0}, (-lm {ct cph, 0, -st} - I {0, cph, 0})/Sqrt[2]];
polcLF$[ct_, st_, cph_, lm_] := Join[{0}, (-lm {ct cph, 0, -st} + I {0, cph, 0})/Sqrt[2]];
xLF$[amp_, {wv_, cv_, snv_}, lam_] := Module[{vecs, val},
   vecs = {k[1] -> wv {1, 0, 0, 1}, k[2] -> wv {1, 0, 0, -1}, k[3] -> wv {1, snv, 0, cv}, k[4] -> wv {1, -snv, 0, -cv},
     e[1] -> polvLF$[1, 0, 1, lam[[1]]], e[2] -> polvLF$[-1, 0, 1, lam[[2]]],
     ec[3] -> polcLF$[cv, snv, 1, lam[[3]]], ec[4] -> polcLF$[-cv, snv, -1, lam[[4]]]};
   val = amp[[1]] //. abbrLF$ /. Pair[a_, b_] :> ((a /. vecs) . gmLF$ . (b /. vecs)) /.
      {S -> 4 wv^2, T -> -2 wv^2 (1 - cv), U -> -2 wv^2 (1 + cv), Me -> 1, MMU -> 17/10, Alfa -> 1/(4 Pi), Alfa2 -> 1/(4 Pi)^2};
   N[val (4 Pi)^2]];
ptsLF$ = Select[StringSplit[ReadList[FileNameJoin[{srcDirLF$, "work", "lbl_points_exact.txt"}], String]], Length[#] == 7 && #[[7]] === "1" &];
helsLF$ = Tuples[{-1, 1}, 4];
rowsLF$ = Flatten[Table[Module[{wv = ToExpression[p[[2]]], cv = ToExpression[p[[3]]], snv = ToExpression[p[[4]]]},
      Table[{p[[1]], 4 wv^2, cv, h, xLF$[ampELF$, {wv, cv, snv}, h], If[p[[5]] === "both", xLF$[ampMLF$, {wv, cv, snv}, h], 0]},
       {h, helsLF$}]], {p, ptsLF$}], 1];
Print["(b) ", Length[ptsLF$], " points; first point (+,+,+,+): X_e = ", rowsLF$[[16, 5]], ", X_mu = ", rowsLF$[[16, 6]]];


(* ::Subsubsection:: *)
(*Inspect: the values at the first point*)


If[$Notebooks, TableForm[rowsLF$[[;; 16, {4, 5, 6}]], TableHeadings -> {None, {"helicities", "X_e", "X_mu"}}]]


strLF$[x_] := ToString[CForm[N[x]]];
Quiet[CreateDirectory[FileNameJoin[{srcDirLF$, "results"}]]];
Export[FileNameJoin[{srcDirLF$, "results", "lbl_formcalc.csv"}],
  StringRiffle[Prepend[StringRiffle[Join[{#[[1]], strLF$[#[[2]]], strLF$[#[[3]]]}, ToString /@ #[[4]],
         strLF$ /@ {Re[#[[5]]], Im[#[[5]]], Re[#[[6]]], Im[#[[6]]]}], ","] & /@ rowsLF$,
     "label,s,cos,l1,l2,l3,l4,re_e,im_e,re_mu,im_mu"], "\n"] <> "\n", "Text"];
Print["(b) wrote results/lbl_formcalc.csv"];


(* ::Section:: *)
(*Cleanup*)


(* ::Text:: *)
(*Skip this cell while you are still inspecting: it closes LoopTools and removes FormCalc's work directory.*)


Uninstall[Links["*LoopTools*"]];
ResetDirectory[];
DeleteDirectory[workDirLF$, DeleteContents -> True];
