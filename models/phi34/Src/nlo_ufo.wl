(* ::Package:: *)

(* ::Title:: *)
(*Step (5), 3 of 3: UFOs with counterterm vertices (on-shell and MS-bar) for MadLoop*)


(* ::Text:: *)
(*FeynRules: read Src/generated/Phi34_CT.nlo, compare the counterterms with the note's App. H, and*)
(*write two UFOs with counterterm vertices (overwritten):*)
(*  Src/generated/Phi34_NLO_OS_UFO     NLOCT's counterterms: field and mass on shell, gphi and lamphi MS-bar*)
(*  Src/generated/Phi34_NLO_MSbar_UFO  MS-bar: only the poles of the 2-, 3- and 4-point counterterms, i.e. Eq. (5)*)
(*FeynmanGauge = True writes gauge = [0, 1] (the model has no gauge field); MadGraph refuses*)
(*non-QCD loops for a model that does not allow Feynman gauge.*)
(**)
(*Usage:  wolframscript -file nlo_ufo.wl     (after nlo_nloct.wl)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file nlo_ufo.wl  (in a fresh kernel).  Interactive:  ~/hep/bin/wopen nlo_ufo.wl  (in a fresh kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


srcDirNU$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

(* ::Section:: *)
(*FeynRules, the model and the NLOCT counterterms*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNU$];
LoadModel["Phi34.fr"];

SetDirectory[FileNameJoin[{srcDirNU$, "generated"}]];
Get["Phi34_CT.nlo"];
R2$vertlist = DeleteCases[R2$vertlist, Last[{}]];   (* scalar theory: no R2 vertices *)
Print["R2 vertices: ", R2$vertlist, ";  perturbed orders: ", FR$InteractionOrderPerturbativeExpansion];


(* ::Section:: *)
(*comparison with App. H*)


(* NLOCT's vertices: 2-point I [deltaZ (p^2 - m^2) - 2 m deltam], 3-point -I (deltag + 3/2 gphi deltaZ), 4-point
   -I (deltalambda + 2 lamphi deltaZ).  App. H: deltaZ = Sigma'(m^2) = -g^2 B0'(m^2)/(2 (4 Pi)^2),
   2 m deltam = -Sigma_0(m^2) = [g^2 (DeltaUV + B0(m^2)) + lambda (m^2 DeltaUV + A0(m^2))]/(2 (4 Pi)^2),
   deltag = 3 g lambda DeltaUV/(2 (4 Pi)^2), deltalambda = 3 lambda^2 DeltaUV/(2 (4 Pi)^2) (MS-bar, Eq. (5)),
   with B0(m^2) = 2 - Pi/Sqrt[3] - 2 Log[m/mu], m^2 B0'(m^2) = 2 Pi/(3 Sqrt[3]) - 1, A0 = m^2 (1 - Log[m^2/mu^2]). *)
vtxNU$[legs_] := First[Cases[UV$vertlist, {legs, v_} :> v]] /. {IPL[_] -> 1, If[m == 0, 0, 1] -> 1};
uv2NU$ = vtxNU$[{{phi, 1}, {phi, 2}}];
uv3NU$ = vtxNU$[{{phi, 1}, {phi, 2}, {phi, 3}}];
uv4NU$ = vtxNU$[{{phi, 1}, {phi, 2}, {phi, 3}, {phi, 4}}];
k4NU$ = (4 Pi)^2;
dZNU$ = Simplify[Coefficient[Expand[uv2NU$], SP[2, 2]]/I];
twoMdmNU$ = Simplify[-(Expand[uv2NU$] /. SP[2, 2] -> m^2)/I];
handdZ$ = -gphi^2/(2 k4NU$ m^2) (2 Pi/(3 Sqrt[3]) - 1);
hand2mdm$ = (gphi^2 (1/FR$Eps + 2 - Pi/Sqrt[3] - 2 Log[m/FR$MU]) + lamphi (m^2/FR$Eps + m^2 (1 - Log[m^2/FR$MU^2])))/(2 k4NU$);
Print["deltaZ (NLOCT) = ", InputForm[dZNU$], "  App. H -> ", Simplify[dZNU$ - handdZ$] === 0];
Print["2 m deltam (NLOCT) = ", InputForm[twoMdmNU$], "  App. H -> ",
  Simplify[PowerExpand[twoMdmNU$ - hand2mdm$], m > 0 && FR$MU > 0] === 0];
Print["vertex counterterm, 3-point (NLOCT) = ", InputForm[uv3NU$], "  -I (deltag + 3/2 g deltaZ) -> ",
  Simplify[uv3NU$ + I (3 gphi lamphi/(2 k4NU$ FR$Eps) + 3/2 gphi dZNU$)] === 0];
Print["vertex counterterm, 4-point (NLOCT) = ", InputForm[uv4NU$], "  -I (deltalambda + 2 lambda deltaZ) -> ",
  Simplify[uv4NU$ + I (3 lamphi^2/(2 k4NU$ FR$Eps) + 2 lamphi dZNU$)] === 0];


(* ::Subsubsection:: *)
(*Inspect: the NLOCT counterterms against App. H*)


If[$Notebooks,
  TableForm[{{"two-point vertex", TraditionalForm[uv2NU$]}, {"deltaZ", TraditionalForm[dZNU$]}, {"2 m deltam", TraditionalForm[twoMdmNU$]}, {"three-point vertex", TraditionalForm[uv3NU$]}, {"four-point vertex", TraditionalForm[uv4NU$]}}]
]


(* ::Section:: *)
(*UFO outputs*)


FeynmanGauge = True;
uvOSNU$ = UV$vertlist;
(* MS-bar: the 1/FR$Eps parts of the three counterterm vertices (deltaZ is finite) *)
uvMSNU$ = {#[[1]], Coefficient[Expand[#[[2]]], FR$Eps, -1]/FR$Eps} & /@ uvOSNU$;
Print["MS-bar two-point counterterm: ", InputForm[uvMSNU$]];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"Phi34_NLO_OS_UFO", "Phi34_NLO_MSbar_UFO"}];
WriteUFO[LPhi34, UVCounterterms -> uvOSNU$, R2Vertices -> R2$vertlist, Output -> "Phi34_NLO_OS_UFO"];
WriteUFO[LPhi34, UVCounterterms -> uvMSNU$, R2Vertices -> R2$vertlist, Output -> "Phi34_NLO_MSbar_UFO"];
Print["written: ", FileNames["Phi34_NLO_*_UFO"]];