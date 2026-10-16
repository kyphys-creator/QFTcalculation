(* ::Package:: *)

(* ::Title:: *)
(*Step (1): FeynRules on QCD.fr -> FeynArts model and UFO (QCD with five massless quarks and one heavy quark)*)


(* ::Text:: *)
(*Usage*)
(*  terminal :  wolframscript -file generate_QCD.wl      (from any directory)*)
(*  notebook :  Get["<path>/models/qcd/Src/generate_QCD.wl"]*)
(*              or open this file and evaluate it (Src/ is then taken from NotebookDirectory[])*)
(**)
(*Output (overwritten on each run)*)
(*  Src/generated/QCD_FA/                FeynArts model (QCD_FA.mod, .gen, .pars)*)
(*  Src/generated/QCD_UFO/               UFO for MadGraph*)
(*  Src/generated/FeynmanRules_QCD.m     vertex list returned by FeynmanRules*)
(**)
(*Expected results (note Fig. 1, all momenta incoming)*)
(*  CheckHermiticity -> {},  CheckKineticTermNormalisation -> True,  16 vertices:*)
(*  qbar q G  -> I gs T^a gamma^mu (six quarks),  qbar q A -> I ee Q gamma^mu (six quarks and the electron),*)
(*  G G G     -> gs f^{a1a2a3} [g^{12}(p1-p2)^3 + g^{23}(p2-p3)^1 + g^{31}(p3-p1)^2],*)
(*  G G G G   -> -I gs^2 [f^{12e}f^{34e}(g^{13}g^{24}-g^{14}g^{23}) + (2<->3) + (2<->4)],*)
(*  ghGbar ghG G -> -gs f^{a1a2a3} p1^mu3  (p1 = incoming momentum of the antighost leg), no messages.*)
(**)
(*Load FeynRules in a fresh kernel: do not mix it with FeynCalc in one session.  Global names below end in QCD$*)
(*so that they cannot clash with model symbols (gs, aS, ee, MT, G, A, uq, dq, tq, elec, ghG).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file generate_QCD.wl  (in a fresh kernel: FeynRules must not share a kernel with FeynCalc or FeynArts).  Interactive:  ~/hep/bin/wopen generate_QCD.wl  (in a fresh kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*locations*)


startDirQCD$ = Directory[];
srcDirQCD$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
outDirQCD$ = FileNameJoin[{srcDirQCD$, "generated"}];


(* ::Section:: *)
(*FeynRules*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];

SetDirectory[srcDirQCD$];
LoadModel["QCD.fr"];


(* ::Subsubsection:: *)
(*Inspect: the Lagrangian of QCD.fr (Eq. (L) without gauge fixing and counterterms)*)


If[$Notebooks,
  {LGaugeQCD, LFermionQCD, LGhostQCD} // TraditionalForm
]


(* ::Section:: *)
(*checks*)


Print["Hermiticity (expect {}): ", CheckHermiticity[LQCD]];
Print["Kinetic-term normalisation (expect True): ", CheckKineticTermNormalisation[LQCD]];
Print["Mass spectrum: ", CheckMassSpectrum[LQCD]];

verticesQCD$ = FeynmanRules[LQCD, ScreenOutput -> False];
Print["Number of vertices (expect 16: 6 qqG, 7 ffA, GGG, GGGG, ghost): ", Length[verticesQCD$]];


(* ::Text:: *)
(*Each vertex is compared with the note (Fig. 1).  FeynRules writes FV[i, mu] for the incoming momentum of leg i and*)
(*ME for the metric; the expected expressions below use the same symbols, so the difference must vanish identically.*)
(*The four-gluon colour structures carry a dummy adjoint index; it is renamed to e before comparing.*)


vtxQCD$[fields_List] := Module[{v = Select[verticesQCD$, (First /@ #[[1]]) === fields &]},
   If[Length[v] != 1, Missing["vertex", fields], v[[1, 2]]]];
lorQCD$[i_] := Index[Lorentz, Ext[i]];
gluQCD$[i_] := Index[Gluon, Ext[i]];
colQCD$[i_] := Index[Colour, Ext[i]];
spiQCD$[i_] := Index[Spin, Ext[i]];

expectQCD$["qqG"] = I gs Ga[lorQCD$[3], spiQCD$[1], spiQCD$[2]] T[gluQCD$[3], colQCD$[1], colQCD$[2]];
expectQCD$["ffA"][q_] := I ee q Ga[lorQCD$[3], spiQCD$[1], spiQCD$[2]];
expectQCD$["GGG"] = gs f[gluQCD$[1], gluQCD$[2], gluQCD$[3]] (
    ME[lorQCD$[1], lorQCD$[2]] (FV[1, lorQCD$[3]] - FV[2, lorQCD$[3]]) +
    ME[lorQCD$[2], lorQCD$[3]] (FV[2, lorQCD$[1]] - FV[3, lorQCD$[1]]) +
    ME[lorQCD$[3], lorQCD$[1]] (FV[3, lorQCD$[2]] - FV[1, lorQCD$[2]]));
fe4QCD$[i_, j_, k_, l_] := f[gluQCD$[i], gluQCD$[j], eQCD$] f[gluQCD$[k], gluQCD$[l], eQCD$];
expectQCD$["GGGG"] = -I gs^2 (
    fe4QCD$[1, 2, 3, 4] (ME[lorQCD$[1], lorQCD$[3]] ME[lorQCD$[2], lorQCD$[4]] - ME[lorQCD$[1], lorQCD$[4]] ME[lorQCD$[2], lorQCD$[3]]) +
    fe4QCD$[1, 3, 2, 4] (ME[lorQCD$[1], lorQCD$[2]] ME[lorQCD$[3], lorQCD$[4]] - ME[lorQCD$[1], lorQCD$[4]] ME[lorQCD$[2], lorQCD$[3]]) +
    fe4QCD$[1, 4, 2, 3] (ME[lorQCD$[1], lorQCD$[2]] ME[lorQCD$[3], lorQCD$[4]] - ME[lorQCD$[1], lorQCD$[3]] ME[lorQCD$[2], lorQCD$[4]]));
expectQCD$["ghost"] = -gs f[gluQCD$[1], gluQCD$[2], gluQCD$[3]] FV[1, lorQCD$[3]];

(* momentum conservation p1 + p2 + p3 = 0 for the three-point vertices; colour of the photon vertices is diagonal *)
momConsQCD$ = {FV[3, mu_] :> -FV[1, mu] - FV[2, mu]};
(* f is totally antisymmetric: bring its arguments into canonical order before comparing *)
fCanonQCD$ = f[x__] :> Signature[{x}] (f @@ Sort[{x}]) /; !OrderedQ[{x}];
diffQCD$[got_, want_] := Expand[(got - want) /. momConsQCD$ /. IndexDelta[colQCD$[1], colQCD$[2]] -> 1 /.
     Index[Gluon, Gluon$1] -> eQCD$ /. fCanonQCD$];

quarksQCD$ = {{ubar, u, 2/3}, {cbar, c, 2/3}, {dbar, d, -1/3}, {sbar, s, -1/3}, {bbar, b, -1/3}, {tqbar, tq, 2/3}};
Print["qbar q G - I gs T gamma (expect six 0): ",
  Table[diffQCD$[vtxQCD$[{q[[1]], q[[2]], G}], expectQCD$["qqG"]], {q, quarksQCD$}]];
Print["qbar q A - I ee Q gamma (expect six 0): ",
  Table[diffQCD$[vtxQCD$[{q[[1]], q[[2]], A}], expectQCD$["ffA"][q[[3]]]], {q, quarksQCD$}]];
Print["elecbar elec A - (-I ee gamma) (expect 0): ", diffQCD$[vtxQCD$[{elecbar, elec, A}], expectQCD$["ffA"][-1]]];
Print["G G G - note (expect 0): ", diffQCD$[vtxQCD$[{G, G, G}], expectQCD$["GGG"]]];
Print["G G G G - note (expect 0): ", diffQCD$[vtxQCD$[{G, G, G, G}], expectQCD$["GGGG"]]];
Print["ghGbar ghG G - note (expect 0): ", diffQCD$[vtxQCD$[{ghGbar, ghG, G}], expectQCD$["ghost"]]];


(* ::Subsubsection:: *)
(*Inspect: the Feynman rules*)


If[$Notebooks,
  TableForm[verticesQCD$ /. {v_List, c_} :> {v, TraditionalForm[c]}]
]


(* ::Section:: *)
(*write outputs*)


Quiet[CreateDirectory[outDirQCD$]];
SetDirectory[outDirQCD$];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"QCD_FA", "QCD_UFO"}];

Put[verticesQCD$, "FeynmanRules_QCD.m"];
WriteFeynArtsOutput[LQCD];      (* -> QCD_FA/ *)
WriteUFO[LQCD];                 (* -> QCD_UFO/ *)

Print["Messages issued: ", Length[$MessageList], "   output in ", outDirQCD$, ": ",
  FileNameTake /@ FileNames["*", outDirQCD$]];


(* ::Subsubsection:: *)
(*Inspect: the start of the FeynArts model file QCD_FA.mod*)


If[$Notebooks,
  StringTake[Import[FileNameJoin[{outDirQCD$, "QCD_FA", "QCD_FA.mod"}], "Text"], UpTo[2500]]
]


SetDirectory[startDirQCD$];
