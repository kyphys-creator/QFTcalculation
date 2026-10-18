(* ::Package:: *)

(* ::Title:: *)
(*Step (8) of the CKM note: the Delta F = 2 box diagrams at zero momentum in a general R_xi gauge (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm_ckm, step (8).  The one-loop amplitudes of b sbar -> s bbar (B_s mixing), b dbar -> d bbar (B_d)*)
(*and s dbar -> d sbar (K) with the FeynArts model of this note (the photon-mass copy of the earlier steps; no photon*)
(*runs in these loops), general xiW, the gluon left out (Fig. fcncdiag (g), (h)):*)
(*  - only box diagrams contribute (no tree-level flavour-changing neutral coupling, so no one-particle-reducible*)
(*    diagram changes the flavour by two at one loop); they have W+- or G+- on the two charged lines and the up-type*)
(*    quarks u_k, u_l inside;*)
(*  - zero external momenta and massless external quarks (the down-type quarks massless everywhere: they do not run in*)
(*    the boxes), the up-type quarks with their masses MU, MC, MT: the zero-momentum matching;*)
(*  - the Dirac structure: each diagram has the spinor pairing [out_1 ... in_1][in_2bar ... out_2bar] or the crossed*)
(*    one; each pair of chains is projected on gamma^mu P_L x gamma_mu P_L with traces in 4 dimensions (the boxes are UV*)
(*    finite); the crossed pairing equals minus the direct one by the Fierz identity of the matrices*)
(*    (gamma^mu P_L)_ab (gamma_mu P_L)_cd = -(gamma^mu P_L)_ad (gamma_mu P_L)_cb (checked in df2_ckm_check.wl).*)
(*Writes work/df2_<proc>.m: K times the coefficient of [out_1 gamma^mu P_L in_1][in_2bar gamma_mu P_L out_2bar] in*)
(*FeynArts units, in A0, B0(0, a, b), C0, D0 at zero momentum and D.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file df2_ckm_feyncalc.wl  (about 10 minutes; then df2_ckm_check.wl).*)
(*Interactive:  ~/hep/bin/wopen df2_ckm_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirDF$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
workDirDF$ = FileNameJoin[{srcDirDF$, "work"}];
Quiet[CreateDirectory[workDirDF$]];
modelTmpDirDF$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirDF$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpDirDF$, "SM_CKM_FA"}]];
modFileDF$ = FileNameJoin[{modelTmpDirDF$, "SM_CKM_FA", "SM_CKM_FA.mod"}];
modTextDF$ = StringReplace[Import[modFileDF$, "Text"], {
    RegularExpression["(?s)(V\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA",
    RegularExpression["(?s)(U\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA"}];
Export[modFileDF$, modTextDF$, "Text"];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirDF$, "SM_CKM_FA"}], Quiet -> True];
modelFileDF$ = FileNameJoin[{modelTmpDirDF$, "SM_CKM_FA", "SM_CKM_FA"}];

massDF$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me, FCGV["MA"] -> MA};
lepMDF$ = {Me, MMU, MTA}; upMDF$ = {MU, MC, MT}; dnMDF$ = {MD, MS, MB};
yukDF$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMDF$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMDF$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMDF$[[i]]/vev, 0]};
light0DF$ = {MD -> 0, MS -> 0, MB -> 0};
ckmDF$ = {Conjugate[CKM[i_Integer, j_Integer]] :> cKc[i, j], CKM[i_Integer, j_Integer] :> cK[i, j]};
convDF$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG,
    GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
    GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1},
   massDF$];
sumOverDF$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];
insertDF$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelFileDF$,
    GenericModel -> modelFileDF$, ExcludeParticles -> {V[4]}], RuleDelayed::rhs];
convertDF$[fa_] := Module[{a},
   a = Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> {p1, p2}, OutgoingMomenta -> {p3, p4}, LoopMomenta -> {q},
       ChangeDimension -> D, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> False,
       DropIndexSum -> False], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a = (sumOverDF$ /@ a) /. convDF$ /. yukDF$ /. ckmDF$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee /. light0DF$;
   If[! FreeQ[a, CKM | IndexSum], Print["   WARNING: CKM or IndexSum left"]];
   a /. SUNFDelta[__] -> 1];
KK = (4 Pi)^2;
(* zero external momenta; the spinors keep their own momentum symbols (SM note, step (6)) *)
spinRenameDF$ = {Spinor[Momentum[p_, d___], r___] :> Spinor[Momentum[sp[p], d], r],
   Spinor[-Momentum[p_, d___], r___] :> Spinor[-Momentum[sp[p], d], r]};
zeroMomDF$[x_] := FCReplaceMomenta[x /. spinRenameDF$, {p1 -> 0, p2 -> 0, p3 -> 0, p4 -> 0}];
topsBoxDF$ = CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections, SelfEnergies, Triangles}];
(* the two pairings: direct [out1 ... in1][in2bar ... out2bar] -> chA chB, crossed [out1 ... out2bar][in2bar ... in1] -> chC chD *)
chainRuleDF$ = {
   Dot[Spinor[Momentum[sp[p3], ___], ___], x___, Spinor[Momentum[sp[p1], ___], ___]] :> chA[Dot[x]],
   Dot[Spinor[-Momentum[sp[p2], ___], ___], y___, Spinor[-Momentum[sp[p4], ___], ___]] :> chB[Dot[y]],
   Dot[Spinor[Momentum[sp[p3], ___], ___], x___, Spinor[-Momentum[sp[p4], ___], ___]] :> chC[Dot[x]],
   Dot[Spinor[-Momentum[sp[p2], ___], ___], y___, Spinor[Momentum[sp[p1], ___], ___]] :> chD[Dot[y]]};
(* projection of a pair of chains on gamma^mu P_L x gamma_mu P_L in 4 dimensions: Tr[A g_beta] Tr[B g^beta] / 16 *)
trDF$[z_] := DiracTrace[DiracSimplify[FCI[z]], DiracTraceEvaluate -> True];
(* the reduced (D-dimensional) amplitude is written in 4 dimensions before the chains are cut out and traced *)
projDF$[x_] := Module[{y = Expand[ChangeDimension[x, 4] /. chainRuleDF$], dir, crs},
   dir = Contract[Contract[y /. {chA[a_] chB[b_] :> trDF$[a . GA[bb$]] trDF$[b . GA[bb$]], chC[_] chD[_] -> 0}]]/16;
   crs = Contract[Contract[y /. {chC[a_] chD[b_] :> trDF$[a . GA[bb$]] trDF$[b . GA[bb$]], chA[_] chB[_] -> 0}]]/16;
   If[! FreeQ[{dir, crs}, LorentzIndex | chA | chB | chC | chD | Spinor], Print["   WARNING: unprojected structure left"]];
   (* the crossed pairing is -1 times the direct one (Fierz) *)
   {dir, crs, dir - crs}];
(* the tensor reduction in D dimensions (as the SM note's boxes); the traces of projDF$ are taken in 4 *)
reduceDF$[x_] := Module[{r = TID[DiracSimplify[x], q, ToPaVe -> True]},
   PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {0}, {m1_, m2_}] :> B0[0, m1, m2]}];
procsDF$ = <|"Bs" -> ({F[4, {3}], -F[4, {2}]} -> {F[4, {2}], -F[4, {3}]}),
   "Bd" -> ({F[4, {3}], -F[4, {1}]} -> {F[4, {1}], -F[4, {3}]}),
   "K" -> ({F[4, {2}], -F[4, {1}]} -> {F[4, {1}], -F[4, {2}]})|>;


(* ::Subsubsection:: *)
(*Inspect: the box diagrams of b sbar -> s bbar*)


If[$Notebooks, Show /@ Render[Paint[insertDF$[topsBoxDF$, procsDF$["Bs"]], DisplayFunction -> Identity]]]


(* ::Section:: *)
(*The three processes*)


t0DF$ = AbsoluteTime[];
resDF$ = Association[Table[name -> Module[{d, a, r, pr, nonzero},
      d = insertDF$[topsBoxDF$, procsDF$[name]];
      a = zeroMomDF$ /@ convertDF$[CreateFeynAmp[d, GaugeRules -> {}]];
      r = Table[projDF$[reduceDF$[FDS[x, q]]], {x, a}];
      nonzero = Count[r[[All, 3]], y_ /; Simplify[y] =!= 0];
      pr = KK Total[r];
      pr = Collect[#, {_A0, _B0, _C0, _D0, _PaVe}, Together] & /@ pr;
      Print["   ", name, ": ", Length[a], " box diagrams (", nonzero, " nonzero), ", Round[AbsoluteTime[] - t0DF$], " s;  CKM symbols ",
        Union[Cases[pr, _cK | _cKc, Infinity]], ";  loop functions ", Union[Head /@ Cases[pr, _A0 | _B0 | _C0 | _D0 | _PaVe, Infinity]]];
      Put[<|"name" -> name, "direct" -> pr[[1]], "crossed" -> pr[[2]], "F" -> pr[[3]]|>,
       FileNameJoin[{workDirDF$, "df2_" <> name <> ".m"}]];
      pr], {name, Keys[procsDF$]}]];
Print["Summary: ", Table[{name, LeafCount[resDF$[name][[3]]]}, {name, Keys[procsDF$]}], ";  total ", Round[AbsoluteTime[] - t0DF$], " s"];
