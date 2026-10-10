(* ::Package:: *)

(* nlo_ufo.wl -- step 3 of 3 of the NLO UFO generation (research note, step (6)).
   FeynRules: read Src/generated/Phi3_CT.nlo, compare the counterterms with the note's App. J, and
   write two UFOs with counterterm vertices (overwritten):
     Src/generated/Phi3_NLO_OS_UFO     NLOCT's on-shell counterterms (deltaZ, deltam on shell; deltag = 0)
     Src/generated/Phi3_NLO_MSbar_UFO  MS-bar: only the pole of the two-point counterterm, i.e. Eq. (7)
   FeynmanGauge = True writes gauge = [0, 1] (the model has no gauge field); MadGraph refuses
   non-QCD loops for a model that does not allow Feynman gauge.

   Usage:  wolframscript -file nlo_ufo.wl     (after nlo_nloct.wl) *)

srcDirNU$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNU$];
LoadModel["Phi3.fr"];

SetDirectory[FileNameJoin[{srcDirNU$, "generated"}]];
Get["Phi3_CT.nlo"];
R2$vertlist = DeleteCases[R2$vertlist, Last[{}]];   (* scalar theory: no R2 vertices *)
Print["R2 vertices: ", R2$vertlist, ";  perturbed orders: ", FR$InteractionOrderPerturbativeExpansion];

(* ---------- comparison with App. J ---------- *)
(* the two-point counterterm is I [deltaZ (p^2 - m^2) - 2 m deltam]; App. J: deltaZ = -g^2/(2(4Pi)^2) B0'(m^2),
   2 m deltam = deltam_os - deltaZ m^2 = -Sigma_0(m^2) = g^2/(2(4Pi)^2) (DeltaUV + B0(m^2)),
   with B0(m^2) = 2 - Pi/Sqrt[3] - 2 Log[m/mu] and m^2 B0'(m^2) = 2 Pi/(3 Sqrt[3]) - 1 *)
uv2NU$ = First[Cases[UV$vertlist, {{{phi, 1}, {phi, 2}}, v_} :> v]] /. {IPL[_] -> 1, If[m == 0, 0, 1] -> 1};
uv3NU$ = First[Cases[UV$vertlist, {{{phi, 1}, {phi, 2}, {phi, 3}}, v_} :> v]] /. {IPL[_] -> 1, If[m == 0, 0, 1] -> 1};
dZNU$ = Simplify[Coefficient[Expand[uv2NU$], SP[2, 2]]/I];
twoMdmNU$ = Simplify[-(Expand[uv2NU$] /. SP[2, 2] -> m^2)/I];   (* = 2 m deltam, pole included *)
k4NU$ = (4 Pi)^2;
Print["deltaZ (NLOCT) = ", InputForm[dZNU$], "  App. J -> ",
  Simplify[dZNU$ + gphi^2/(2 k4NU$ m^2) (2 Pi/(3 Sqrt[3]) - 1)] === 0];
Print["2 m deltam (NLOCT) = ", InputForm[twoMdmNU$], "  App. J -> ",
  Simplify[twoMdmNU$ - gphi^2/(2 k4NU$) (1/FR$Eps + 2 - Pi/Sqrt[3] - 2 Log[m/FR$MU]), m > 0 && FR$MU > 0] === 0];
Print["vertex counterterm (NLOCT) = ", InputForm[uv3NU$], "  -3/2 I gphi deltaZ -> ",
  Simplify[uv3NU$ + 3/2 I gphi dZNU$] === 0];

(* ---------- UFO outputs ---------- *)
FeynmanGauge = True;
uvOSNU$ = UV$vertlist;
uvMSNU$ = {{{{phi, 1}, {phi, 2}},
    Coefficient[Expand[First[Cases[uvOSNU$, {{{phi, 1}, {phi, 2}}, v_} :> v]]], FR$Eps, -1]/FR$Eps}};
Print["MS-bar two-point counterterm: ", InputForm[uvMSNU$]];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"Phi3_NLO_OS_UFO", "Phi3_NLO_MSbar_UFO"}];
WriteUFO[LPhi3, UVCounterterms -> uvOSNU$, R2Vertices -> R2$vertlist, Output -> "Phi3_NLO_OS_UFO"];
WriteUFO[LPhi3, UVCounterterms -> uvMSNU$, R2Vertices -> R2$vertlist, Output -> "Phi3_NLO_MSbar_UFO"];
Print["written: ", FileNames["Phi3_NLO_*_UFO"]];
