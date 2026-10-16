(* ::Package:: *)

(* ::Title:: *)
(*Step (3): the tadpole and the 1PI self-energies from FeynArts' own SMQCD.mod against the note's model (SM note)*)


(* ::Text:: *)
(*Independent model check: FeynArts' SM.mod / SMQCD.mod (Denner's conventions, written independently of this note)*)
(*gives T, Sigma_T^WW, Sigma_T^ZZ, Sigma_T^AA, Sigma_T^AZ, Sigma^H and the top SigmaV, SigmaS (1PI, D dimensions,*)
(*general xiA, xiZ, xiW).  They are compared symbolically with results/oneloop_sigma.m of oneloop_feyncalc.wl.  As there,*)
(*the photon and its ghost get the mass MA (in a copy of SM.mod), so both models are regularized in the same way.*)
(*Field conventions: A(Denner) = -A, so Sigma^AZ changes sign;*)
(*the W, Z, H, top two-point functions and T are the same.  SMQCD's quark-gluon vertex is -i g_s gamma T (the note's*)
(*is +i g_s gamma T); the sign cancels in the self-energy.  $CKM is False (CKM = 1).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_smmod.wl  (run oneloop_feyncalc.wl first).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirSMM$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirSMM$ = FileNameJoin[{srcDirSMM$, "results"}];
oursSMM$ = Association[Get[FileNameJoin[{resDirSMM$, "oneloop_sigma.m"}]]];
(* copies of SM.mod and SMQCD.mod (SMQCD.mod loads SM.mod from its own folder) with the photon mass MA *)
faModelsSMM$ = FileNameJoin[{$FeynArtsDirectory, "Models"}];
tmpSMM$ = CreateDirectory[];
CopyFile[FileNameJoin[{faModelsSMM$, "SMQCD.mod"}], FileNameJoin[{tmpSMM$, "SMQCD.mod"}]];
smText$ = Import[FileNameJoin[{faModelsSMM$, "SM.mod"}], "Text"];
smText$ = StringReplace[smText$, {
    RegularExpression["(?s)(V\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> FCGV[\"MA\"]",
    RegularExpression["(?s)(U\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> FCGV[\"MA\"]"}];
Export[FileNameJoin[{tmpSMM$, "SM.mod"}], smText$, "Text"];
Print["photon and photon-ghost masses in the copy of SM.mod: ",
  StringCases[smText$, RegularExpression["(?s)(?:V|U)\\[1\\] == \\{.*?Mass -> ([^,]+),"] -> "$1"]];
modelSMM$ = FileNameJoin[{tmpSMM$, "SMQCD"}];

convSMM$ = {FCGV["EL"] -> ee, FCGV["SW"] -> sw, FCGV["CW"] -> cw, FCGV["MW"] -> MW, FCGV["MZ"] -> MZ,
   FCGV["MH"] -> MH, FCGV["ME"] -> Me, FCGV["MM"] -> MMU, FCGV["ML"] -> MTA, FCGV["MU"] -> MU, FCGV["MC"] -> MC,
   FCGV["MT"] -> MT, FCGV["MD"] -> MD, FCGV["MS"] -> MS, FCGV["MB"] -> MB, FCGV["GS"] -> gS, SMP["g_s"] -> gS,
   SMP["e"] -> ee, SMP["sin_W"] -> sw, SMP["cos_W"] -> cw,
   FCGV["MA"] -> MA, GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG, GaugeXi[g] -> xiG,
   GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[5, ___]] -> xiG,
   GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
   GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1};
sumOverSMM$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];

insertSMM$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelSMM$,
    GenericModel -> "Lorentz"], RuleDelayed::rhs];
convertSMM$[fa_, in_, out_] := Module[{a},
   a = Quiet[FCFAConvert[fa, IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q},
       LorentzIndexNames -> {mu, nu}, ChangeDimension -> D, List -> True, SMP -> False,
       UndoChiralSplittings -> True, DropSumOver -> False], RuleDelayed::rhs];
   a = (sumOverSMM$ /@ a) /. convSMM$ /. {DiracGamma[6] -> 1/2 + DiracGamma[5]/2, DiracGamma[7] -> 1/2 - DiracGamma[5]/2};
   a];
reduceSMM$[x_] := Module[{r},
   r = FDS[x, q];
   r = TID[DiracSimplify[SUNSimplify[r]], q, ToPaVe -> True];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]};
   Simplify[r /. {B0[0, 0, 0] -> 0, A0[0] -> 0}]];
KK = (4 Pi)^2;
topsOPI$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];

sigmaSMM$[proc_, kind_] := Module[{d, a, proj},
   d = insertSMM$[topsOPI$, proc];
   a = convertSMM$[CreateFeynAmp[d, Truncated -> True, GaugeRules -> {}], {k}, {k}];
   Print["   ", proc, ": 1PI diagrams ", Length[a]];
   proj = Switch[kind, "V", -1/(D - 1) (MTD[mu, nu] - FVD[k, mu] FVD[k, nu]/SPD[k, k]), "S", 1];
   KK Simplify[Total[reduceSMM$[Contract[proj #]] & /@ a]]];
sigmaFSMM$[proc_, m_] := Module[{d, a, ext},
   d = insertSMM$[topsOPI$, proc];
   a = convertSMM$[CreateFeynAmp[d, Truncated -> True, GaugeRules -> {}], {k}, {k}];
   Print["   ", proc, ": 1PI diagrams ", Length[a]];
   ext[x_] := Module[{y = SUNSimplify[DotSimplify[x], SUNNToCACF -> True] /. SUNFDelta[__] -> 1, tr},
     tr[z_] := DiracTrace[DiracSimplify[FCI[z]], DiracTraceEvaluate -> True];
     {tr[GSD[k] . y]/(4 SPD[k, k]), tr[y]/(4 m)}];
   KK {Simplify[Total[reduceSMM$ /@ #]] & /@ Transpose[ext /@ a]}[[1]]];


(* ::Section:: *)
(*SMQCD.mod*)


FCClearScalarProducts[];
dT$ = insertSMM$[CreateTopologies[1, 1 -> 0], {S[1]} -> {}];
tSMM$ = KK Simplify[reduceSMM$[Total[convertSMM$[CreateFeynAmp[dT$, GaugeRules -> {}], {}, {}]]]];
Print["tadpole diagrams: ", Length[Flatten[List @@ dT$[[All, 2]]]]];
sWW$ = sigmaSMM$[{V[3]} -> {V[3]}, "V"];
sZZ$ = sigmaSMM$[{V[2]} -> {V[2]}, "V"];
sAA$ = sigmaSMM$[{V[1]} -> {V[1]}, "V"];
sAZ$ = sigmaSMM$[{V[1]} -> {V[2]}, "V"];
sHH$ = sigmaSMM$[{S[1]} -> {S[1]}, "S"];
sTT$ = sigmaFSMM$[{F[3, {3}]} -> {F[3, {3}]}, MT];


(* ::Section:: *)
(*Comparison*)


cleanSMM$[x_] := Simplify[x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2] /. CF -> 4/3 /. CA -> 3, 0 < sw < 1 && MW > 0];
oursAt$[x_] := x;
ibpSMM$ = PaVe[0, {0, pp_, pp_}, {0, 0, m2_}] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2;
cmp$[label_, ours_, theirs_, sign_] := Module[{d = cleanSMM$[(oursAt$[ours] - sign theirs) /. ibpSMM$]},
   Print[label, ": note's model - ", If[sign === 1, "", "(-1) "], "SMQCD.mod = ", d, "   (expect 0)"]; d];
resSMM$ = {
   cmp$["T", oursSMM$["T"], tSMM$, 1],
   cmp$["Sigma_T^WW (1PI)", oursSMM$["WW"][[1]], sWW$, 1],
   cmp$["Sigma_T^ZZ (1PI)", oursSMM$["ZZ"][[1]], sZZ$, 1],
   cmp$["Sigma_T^AA", oursSMM$["AA"][[1]], sAA$, 1],
   cmp$["Sigma_T^AZ", oursSMM$["AZ"][[1]], sAZ$, -1],
   cmp$["Sigma^H (1PI)", oursSMM$["HH"][[1]], sHH$, 1],
   cmp$["top SigmaV (1PI)", oursSMM$["TT"][[1, 1]], sTT$[[1]], 1],
   cmp$["top SigmaS (1PI)", oursSMM$["TT"][[1, 2]], sTT$[[2]], 1]};
Print["Summary: ", Length[resSMM$], " functions compared, nonzero differences: ", Count[resSMM$, x_ /; x =!= 0]];
