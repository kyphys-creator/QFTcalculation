(* ::Package:: *)

(* ::Title:: *)
(*Step (1): FeynRules on SpinorQED.fr -> FeynArts model and UFO (spinor QED with e and mu)*)


(* ::Text:: *)
(*Usage*)
(*  terminal :  wolframscript -file generate_SpinorQED.wl      (from any directory)*)
(*  notebook :  Get["<path>/models/spinor_qed/Src/generate_SpinorQED.wl"]*)
(*              or open this file and evaluate it (Src/ is then taken from NotebookDirectory[])*)
(**)
(*Output (overwritten on each run)*)
(*  Src/generated/SpinorQED_FA/                FeynArts model (SpinorQED_FA.mod, .gen, .pars)*)
(*  Src/generated/SpinorQED_UFO/               UFO for MadGraph*)
(*  Src/generated/FeynmanRules_SpinorQED.m     vertex list returned by FeynmanRules*)
(**)
(*Expected results*)
(*  CheckHermiticity -> {},  CheckKineticTermNormalisation -> True,*)
(*  vertices {{elecbar,1},{elec,2},{A,3}} and {{muonbar,1},{muon,2},{A,3}} -> -I ee gamma^mu (note Fig. 1:*)
(*  i e Q gamma^mu with Q = -1), no photon self-coupling, no messages.*)
(**)
(*Load FeynRules in a fresh kernel: do not mix it with FeynCalc in one session.  Global names below end in QED$*)
(*so that they cannot clash with model symbols (ee, Me, MMU, A, elec, muon).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file generate_SpinorQED.wl  (in a fresh kernel: FeynRules must not share a kernel with FeynCalc or FeynArts).  Interactive:  ~/hep/bin/wopen generate_SpinorQED.wl  (in a fresh kernel: FeynRules must not share a kernel with FeynCalc or FeynArts), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*locations*)


startDirQED$ = Directory[];
srcDirQED$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
outDirQED$ = FileNameJoin[{srcDirQED$, "generated"}];


(* ::Section:: *)
(*FeynRules*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];

SetDirectory[srcDirQED$];
LoadModel["SpinorQED.fr"];


(* ::Subsubsection:: *)
(*Inspect: the Lagrangian of SpinorQED.fr (Eq. (1) without gauge fixing and counterterms)*)


If[$Notebooks,
  LSpinorQED // TraditionalForm
]


(* ::Section:: *)
(*checks*)


Print["Hermiticity (expect {}): ", CheckHermiticity[LSpinorQED]];
Print["Kinetic-term normalisation (expect True): ", CheckKineticTermNormalisation[LSpinorQED]];
Print["Mass spectrum: ", CheckMassSpectrum[LSpinorQED]];

verticesQED$ = FeynmanRules[LSpinorQED, ScreenOutput -> False];
Print["Vertices (expect -I ee gamma^mu for elecbar elec A and muonbar muon A): ", InputForm[verticesQED$]];


(* ::Text:: *)
(*Each vertex must be i e Q gamma^mu = -I ee gamma^mu.  The coefficient of the Dirac matrix Ga[mu3, s1, s2] is*)
(*read off and compared with -I ee; a photon self-coupling must not appear (abelian group).*)


coefQED$[fbar_] := Module[{v = Select[verticesQED$, Sort[First /@ #[[1]]] === Sort[{fbar, ToExpression[StringDrop[ToString[fbar], -3]], A}] &]},
   If[Length[v] != 1, Missing["vertex"],
     Simplify[v[[1, 2]] /. Ga[_, _, _] -> 1]]];
Print["elec vertex coefficient of gamma^mu (expect -I ee): ", InputForm[coefQED$[elecbar]]];
Print["muon vertex coefficient of gamma^mu (expect -I ee): ", InputForm[coefQED$[muonbar]]];
Print["Number of vertices (expect 2: elecbar elec A, muonbar muon A): ", Length[verticesQED$]];


(* ::Subsubsection:: *)
(*Inspect: the Feynman rules*)


If[$Notebooks,
  TableForm[verticesQED$ /. {v_List, c_} :> {v, TraditionalForm[c]}]
]


(* ::Section:: *)
(*write outputs*)


Quiet[CreateDirectory[outDirQED$]];
SetDirectory[outDirQED$];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"SpinorQED_FA", "SpinorQED_UFO"}];

Put[verticesQED$, "FeynmanRules_SpinorQED.m"];
WriteFeynArtsOutput[LSpinorQED];      (* -> SpinorQED_FA/ *)
WriteUFO[LSpinorQED];                 (* -> SpinorQED_UFO/ *)

Print["Messages issued: ", Length[$MessageList], "   output in ", outDirQED$, ": ",
  FileNameTake /@ FileNames["*", outDirQED$]];


(* ::Subsubsection:: *)
(*Inspect: the start of the FeynArts model file SpinorQED_FA.mod*)


If[$Notebooks,
  StringTake[Import[FileNameJoin[{outDirQED$, "SpinorQED_FA", "SpinorQED_FA.mod"}], "Text"], UpTo[2500]]
]


SetDirectory[startDirQED$];
