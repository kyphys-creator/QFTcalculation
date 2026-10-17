(* ::Package:: *)

(* ::Title:: *)
(*Step (3) of the CKM note: the quark self-energy matrices from FeynArts' own SMQCD.mod with the CKM matrix ($CKM = True)*)


(* ::Text:: *)
(*Independent model check, as in the SM note's step (3) (models/sm/Src/oneloop_smmod.wl): FeynArts' SM.mod / SMQCD.mod*)
(*(Denner's conventions, written independently of this note) with $CKM = True gives the 1PI quark self-energies*)
(*Sigma_ij of the down-type and up-type quarks in a general R_xi gauge (D dimensions).  They are compared symbolically,*)
(*entry by entry (SL, SR, SSL, SSR), with results/oneloop_ckm_sigma.m of oneloop_ckm_feyncalc.wl.  The photon sign*)
(*(A Denner = -A), the phase of the charged Goldstone and the sign of SMQCD's quark-gluon vertex cancel in a*)
(*self-energy; SM.mod's CKM[j1, j2] multiplies ubar_j1 d_j2 W+ as in the note.  The photon gets the mass MA in a copy of*)
(*SM.mod, as in oneloop_ckm_feyncalc.wl.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_ckm_smmod.wl  (run oneloop_ckm_feyncalc.wl first; a few minutes).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
$CKM = True;

srcDirSC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirSC$ = FileNameJoin[{srcDirSC$, "results"}];
oursSC$ = Association[Get[FileNameJoin[{resDirSC$, "oneloop_ckm_sigma.m"}]]];
faModelsSC$ = FileNameJoin[{$FeynArtsDirectory, "Models"}];
tmpSC$ = CreateDirectory[];
CopyFile[FileNameJoin[{faModelsSC$, "SMQCD.mod"}], FileNameJoin[{tmpSC$, "SMQCD.mod"}]];
smTextSC$ = Import[FileNameJoin[{faModelsSC$, "SM.mod"}], "Text"];
smTextSC$ = StringReplace[smTextSC$, {
    RegularExpression["(?s)(V\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> FCGV[\"MA\"]",
    RegularExpression["(?s)(U\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> FCGV[\"MA\"]"}];
Export[FileNameJoin[{tmpSC$, "SM.mod"}], smTextSC$, "Text"];
modelSC$ = FileNameJoin[{tmpSC$, "SMQCD"}];

convSC$ = {FCGV["EL"] -> ee, FCGV["SW"] -> sw, FCGV["CW"] -> cw, FCGV["MW"] -> MW, FCGV["MZ"] -> MZ,
   FCGV["MH"] -> MH, FCGV["ME"] -> Me, FCGV["MM"] -> MMU, FCGV["ML"] -> MTA, FCGV["MU"] -> MU, FCGV["MC"] -> MC,
   FCGV["MT"] -> MT, FCGV["MD"] -> MD, FCGV["MS"] -> MS, FCGV["MB"] -> MB, FCGV["GS"] -> gS, SMP["g_s"] -> gS,
   SMP["e"] -> ee, SMP["sin_W"] -> sw, SMP["cos_W"] -> cw,
   FCGV["MA"] -> MA, GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG, GaugeXi[g] -> xiG,
   GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[5, ___]] -> xiG,
   GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
   GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1};
(* SM.mod's CKM symbol is matched by name (its context is FeynArts'); the conjugate first *)
ckmSC$ = {Conjugate[(c_Symbol /; SymbolName[c] === "CKM")[i_Integer, j_Integer]] :> vR[i, j] - I vI[i, j],
   (c_Symbol /; SymbolName[c] === "CKM")[i_Integer, j_Integer] :> vR[i, j] + I vI[i, j]};
sumOverSC$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];

insertSC$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelSC$,
    GenericModel -> "Lorentz"], RuleDelayed::rhs];
convertSC$[fa_] := Module[{a},
   a = Quiet[FCFAConvert[fa, IncomingMomenta -> {k}, OutgoingMomenta -> {k}, LoopMomenta -> {q},
       LorentzIndexNames -> {mu, nu}, ChangeDimension -> D, List -> True, SMP -> False,
       UndoChiralSplittings -> True, DropSumOver -> False, DropIndexSum -> False], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a = (sumOverSC$ /@ a) /. convSC$ /. ckmSC$;
   If[! FreeQ[a, _Symbol?(SymbolName[#] === "CKM" &)], Print["   WARNING: CKM left"]];
   a];
KK = (4 Pi)^2;
reduceSC$[x_] := Module[{r},
   r = FDS[x, q];
   r = TID[DiracSimplify[SUNSimplify[DotSimplify[r], SUNNToCACF -> True] /. SUNFDelta[__] -> 1], q, ToPaVe -> True];
   r = DiracSimplify[r];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]};
   r /. {B0[0, 0, 0] -> 0, A0[0] -> 0}];
(* the same reading of the Dirac structure as in oneloop_ckm_feyncalc.wl *)
chiralSC$[r_] := Module[{x, x0, c},
   x = Expand[FCE[r] /. {GSD[k] . GA[7] -> pLs$, GSD[k] . GA[6] -> pRs$, GSD[k] . GA[5] -> pRs$ - pLs$,
         GA[7] -> pL$, GA[6] -> pR$, GA[5] -> pR$ - pL$} /. GSD[k] -> pLs$ + pRs$];
   If[! FreeQ[x, GA | GSD | DiracGamma | Dot], Print["   WARNING: unexpected Dirac structure"]];
   x0 = x /. {pLs$ -> 0, pRs$ -> 0, pL$ -> 0, pR$ -> 0};
   c = (Coefficient[x, #] & /@ {pLs$, pRs$, pL$, pR$}) + {0, 0, x0, x0};
   KK c];
topsOPI$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];
upMSC$ = {MU, MC, MT}; dnMSC$ = {MD, MS, MB};
seSC$[cls_, i_, j_] := Module[{ms = If[cls === 3, upMSC$, dnMSC$], d, a, c},
   d = insertSC$[topsOPI$, {F[cls, {j}]} -> {F[cls, {i}]}];
   a = convertSC$[CreateFeynAmp[d, Truncated -> True, GaugeRules -> {}]];
   c = chiralSC$[reduceSC$[Total[a]]];
   Print["   ", {"", "", "u", "d"}[[cls]], "-type ", {i, j}, ": 1PI diagrams ", Length[a]];
   Simplify[{c[[1]], c[[2]], c[[3]]/ms[[i]], c[[4]]/ms[[j]]}]];


(* ::Section:: *)
(*SMQCD.mod with the CKM matrix*)


FCClearScalarProducts[];
theirsD$ = Table[seSC$[4, i, j], {i, 3}, {j, 3}];
theirsU$ = Table[seSC$[3, i, j], {i, 3}, {j, 3}];


(* ::Section:: *)
(*Comparison*)


cleanSC$[x_] := Simplify[x /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2] /. CF -> 4/3 /. CA -> 3, 0 < sw < 1 && MW > 0];
ibpSC$ = PaVe[0, {0, pp_, pp_}, {0, 0, m2_}] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2;
rowsSC$ = Flatten[Table[{s[[3]], {i, j}, cleanSC$[(s[[1]][[i, j, 1]] - s[[2]][[i, j]]) /. ibpSC$]},
    {s, {{oursSC$["D"], theirsD$, "d"}, {oursSC$["U"], theirsU$, "u"}}}, {i, 3}, {j, 3}], 2];
Scan[If[#[[3]] =!= {0, 0, 0, 0}, Print["   ", #[[1]], #[[2]], ": note's model - SMQCD.mod = ", #[[3]]]] &, rowsSC$];
Print["Summary: ", Length[rowsSC$], " entries x 4 functions compared (general R_xi, D dimensions), nonzero differences: ",
  Count[Flatten[rowsSC$[[All, 3]]], x_ /; x =!= 0]];
