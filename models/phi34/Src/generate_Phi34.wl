(* ::Package:: *)

(* ::Title:: *)
(*Step (1): FeynRules on Phi34.fr -> FeynArts model and UFO (phi^3 + phi^4)*)


(* ::Text:: *)
(*Usage*)
(*  terminal :  wolframscript -file generate_Phi34.wl      (from any directory)*)
(*  notebook :  Get["<path>/models/phi34/Src/generate_Phi34.wl"]*)
(*              or open this file and evaluate it (Src/ is then taken from NotebookDirectory[])*)
(**)
(*Output (overwritten on each run)*)
(*  Src/generated/Phi34_FA/                FeynArts model (Phi34_FA.mod, .gen, .pars)*)
(*  Src/generated/Phi34_UFO/               UFO for MadGraph*)
(*  Src/generated/FeynmanRules_Phi34.m     vertex list returned by FeynmanRules*)
(**)
(*Expected results*)
(*  CheckHermiticity -> {},  CheckKineticTermNormalisation -> True,*)
(*  vertices {{phi,1},{phi,2},{phi,3}} -> -I gphi  and  {{phi,1},...,{phi,4}} -> -I lamphi,  no messages.*)
(**)
(*Load FeynRules in a fresh kernel: do not mix it with FeynCalc in one session.  Global*)
(*names below end in Phi34$ so that they cannot clash with model symbols (gphi, lamphi, m, phi).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file generate_Phi34.wl  (in a fresh kernel: FeynRules must not share a kernel with FeynCalc or FeynArts).  Interactive:  ~/hep/bin/wopen generate_Phi34.wl  (in a fresh kernel: FeynRules must not share a kernel with FeynCalc or FeynArts), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*locations*)


startDirPhi34$ = Directory[];
srcDirPhi34$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
outDirPhi34$ = FileNameJoin[{srcDirPhi34$, "generated"}];


(* ::Section:: *)
(*FeynRules*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];

SetDirectory[srcDirPhi34$];
LoadModel["Phi34.fr"];


(* ::Subsubsection:: *)
(*Inspect: the Lagrangian of Phi34.fr (Eq. (1) without counterterms and the linear term)*)


If[$Notebooks,
  LPhi34 // TraditionalForm
]


(* ::Section:: *)
(*checks*)


Print["Hermiticity (expect {}): ", CheckHermiticity[LPhi34]];
Print["Kinetic-term normalisation (expect True): ", CheckKineticTermNormalisation[LPhi34]];
Print["Mass spectrum: ", CheckMassSpectrum[LPhi34]];

verticesPhi34$ = FeynmanRules[LPhi34, ScreenOutput -> False];
Print["Vertices (expect -I gphi for 3 phi and -I lamphi for 4 phi): ", verticesPhi34$];


(* ::Subsubsection:: *)
(*Inspect: the Feynman rules*)


If[$Notebooks,
  TableForm[verticesPhi34$ /. {v_List, c_} :> {v, TraditionalForm[c]}]
]


(* ::Section:: *)
(*write outputs*)


Quiet[CreateDirectory[outDirPhi34$]];
SetDirectory[outDirPhi34$];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"Phi34_FA", "Phi34_UFO"}];

Put[verticesPhi34$, "FeynmanRules_Phi34.m"];
WriteFeynArtsOutput[LPhi34];      (* -> Phi34_FA/ *)
WriteUFO[LPhi34];                 (* -> Phi34_UFO/ *)

Print["Messages issued: ", Length[$MessageList], "   output in ", outDirPhi34$, ": ",
  FileNameTake /@ FileNames["*", outDirPhi34$]];


(* ::Subsubsection:: *)
(*Inspect: the start of the FeynArts model file Phi34_FA.mod*)


If[$Notebooks,
  StringTake[Import[FileNameJoin[{outDirPhi34$, "Phi34_FA", "Phi34_FA.mod"}], "Text"], UpTo[2500]]
]


SetDirectory[startDirPhi34$];