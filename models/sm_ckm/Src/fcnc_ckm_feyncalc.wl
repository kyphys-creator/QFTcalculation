(* ::Package:: *)

(* ::Title:: *)
(*Step (7) of the CKM note: the one-loop vertices b -> s gamma and Z -> b sbar in a general R_xi gauge (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm_ckm, step (7).  The 1PI one-loop vertices of the flavour-changing neutral transitions*)
(*(Fig. fcncdiag (a)-(e), (i)), with the FeynArts model of this note (the photon-mass copy of steps (3)-(6); no photon*)
(*runs in these loops), general xiW (and xiA, xiZ, which do not enter), the gluon left out, the s quark massless:*)
(*  bsg: b(p1) -> s(p2) gamma(q), on shell (p1^2 = MB^2, p2^2 = 0, q^2 = 0, eps*.q = 0);*)
(*  zbs: Z(k) -> b(p1) sbar(p2), p1^2 = MB^2, p2^2 = 0, k^2 = kk symbolic (on shell at kk = MZ^2; kk -> 0 for the*)
(*       Inami-Lim function);*)
(*the internal up-type quarks u, c, t with their masses MU, MC, MT and lambda_k = V*_ks V_kb.  The amplitudes are written*)
(*with the four structures of step (5): [ubar ... u] eps-slash P_{L,R} and (eps.p1) P_{L,R}; the Dirac equation with*)
(*DiracOrder.  Also the FeynArts tree amplitudes of the flavour-diagonal b -> b gamma and Z -> b bbar, whose coefficients*)
(*normalize the external-leg (LSZ) terms of fcnc_ckm_numeric.wl in the same units as the loop amplitudes (the ratio of*)
(*FeynArts amplitudes of the same external configuration, step (5)).  Checks here: the diagram counts, every term is a*)
(*product V*_ks V_kb, and the UV poles of the (p1.eps) structures vanish.*)
(*Writes work/fcnc_<proc>.m (K times the coefficients: K = 16 pi^2; A0, B0, C0 and D kept).*)


(* ::Text:: *)
(*How to run.  Batch, one process per call (run_fcnc_check.sh starts both in parallel, about 10 minutes):*)
(*  wolframscript -file fcnc_ckm_feyncalc.wl bsg   (or zbs).  Without an argument (batch or notebook) both are computed.*)
(*Interactive:  ~/hep/bin/wopen fcnc_ckm_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirFN$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
workDirFN$ = FileNameJoin[{srcDirFN$, "work"}];
Quiet[CreateDirectory[workDirFN$]];
modelTmpDirFN$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirFN$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpDirFN$, "SM_CKM_FA"}]];
modFileFN$ = FileNameJoin[{modelTmpDirFN$, "SM_CKM_FA", "SM_CKM_FA.mod"}];
modTextFN$ = StringReplace[Import[modFileFN$, "Text"], {
    RegularExpression["(?s)(V\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA",
    RegularExpression["(?s)(U\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA"}];
Export[modFileFN$, modTextFN$, "Text"];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirFN$, "SM_CKM_FA"}], Quiet -> True];
modelFileFN$ = FileNameJoin[{modelTmpDirFN$, "SM_CKM_FA", "SM_CKM_FA"}];

massFN$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me, FCGV["MA"] -> MA};
lepMFN$ = {Me, MMU, MTA}; upMFN$ = {MU, MC, MT}; dnMFN$ = {MD, MS, MB};
yukFN$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMFN$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMFN$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMFN$[[i]]/vev, 0]};
ckmFN$ = {Conjugate[CKM[i_Integer, j_Integer]] :> cKc[i, j], CKM[i_Integer, j_Integer] :> cK[i, j]};
convFN$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG,
    GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
    GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1},
   massFN$];
sumOverFN$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];
KK = (4 Pi)^2;

(* the two processes: FeynArts process, external momenta, kinematics, the polarization vector and momentum rules *)
procsFN$ = <|
   "bsg" -> <|"proc" -> {F[4, {3}]} -> {F[4, {2}], V[1]}, "tree" -> {F[4, {3}]} -> {F[4, {3}], V[1]},
     "in" -> {p1}, "out" -> {p2, q}, "pol" -> Polarization[q, -I], "eps" -> epsP, "elim" -> {q -> p1 - p2},
     "kin" -> {MB^2, 0, MB^2/2}, "treeKin" -> {MB^2, MB^2, MB^2},
     "spin" -> {Spinor[Momentum[p2, D], 0, 1], Spinor[Momentum[p1, D], MB, 1]},
     "treeSpin" -> {Spinor[Momentum[p2, D], MB, 1], Spinor[Momentum[p1, D], MB, 1]},
     (* eps*.q = 0: eps*.p2 = eps*.p1 *)
     "epsRule" -> {SPD[epsP, p2] -> SPD[epsP, p1]}, "order" -> {p2, epsP, p1}|>,
   "zbs" -> <|"proc" -> {V[2]} -> {F[4, {3}], -F[4, {2}]}, "tree" -> {V[2]} -> {F[4, {3}], -F[4, {3}]},
     "in" -> {k}, "out" -> {p1, p2}, "pol" -> Polarization[k, I], "eps" -> epsZ, "elim" -> {k -> p1 + p2},
     "kin" -> {MB^2, 0, (kk - MB^2)/2}, "treeKin" -> {MB^2, MB^2, (kk - 2 MB^2)/2},
     "spin" -> {Spinor[Momentum[p1, D], MB, 1], Spinor[-Momentum[p2, D], 0, 1]},
     "treeSpin" -> {Spinor[Momentum[p1, D], MB, 1], Spinor[-Momentum[p2, D], MB, 1]},
     (* eps.k = 0: eps.p2 = -eps.p1 *)
     "epsRule" -> {SPD[epsZ, p2] -> -SPD[epsZ, p1]}, "order" -> {p1, epsZ, p2}|>|>;

(* the s quark (and the other light down-type quarks) massless; the up-type quarks keep their masses *)
light0FN$ = {MS -> 0, MD -> 0};
convertFN$[fa_, pr_] := Module[{a},
   a = Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> pr["in"], OutgoingMomenta -> pr["out"], LoopMomenta -> {q0},
       ChangeDimension -> D, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> False,
       DropIndexSum -> False], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a = (sumOverFN$ /@ a) /. convFN$ /. yukFN$ /. ckmFN$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee /. light0FN$;
   If[! FreeQ[a, CKM | IndexSum], Print["   WARNING: CKM or IndexSum left"]];
   a = a /. pr["pol"] -> pr["eps"] /. SUNFDelta[__] -> 1;
   If[! FreeQ[a, Polarization], Print["   WARNING: polarization vector not replaced: ", Union[Cases[a, _Polarization, Infinity]]]];
   FCReplaceMomenta[#, pr["elim"]] & /@ DeleteCases[a, 0]];
onShellFN$[kin_] := (FCClearScalarProducts[]; SPD[p1, p1] = kin[[1]]; SPD[p2, p2] = kin[[2]]; SPD[p1, p2] = kin[[3]];);
redFN$[x_, ord_] := Module[{r = FDS[x, q0]},
   r = DiracSimplify[SUNSimplify[DotSimplify[r], SUNNToCACF -> True] /. SUNFDelta[__] -> 1];
   r = TID[r, q0, ToPaVe -> True];
   r = DiracSimplify[r];
   DiracSimplify[DiracOrder[r, ord]]];
(* the four structures [spinbar . eps-slash . P . spin] and (eps.p1) [spinbar . P . spin] *)
structFN$[r_, pr_, spin_] := Module[{e = pr["eps"], x, c, sb = spin[[1]], s = spin[[2]]},
   x = FCE[r] /. pr["epsRule"];
   (* a vector or axial chain without projectors is written with them: 1 = P_L + P_R, gamma5 = P_R - P_L *)
   x = Expand[x /. {sb . GSD[e] . GA[7] . s -> sEL$, sb . GSD[e] . GA[6] . s -> sER$, sb . GA[7] . s -> sSL$, sb . GA[6] . s -> sSR$,
        sb . GSD[e] . GA[5] . s -> sER$ - sEL$, sb . GSD[e] . s -> sEL$ + sER$, sb . GA[5] . s -> sSR$ - sSL$, sb . s -> sSL$ + sSR$}];
   c = {Coefficient[x, sEL$], Coefficient[x, sER$], Coefficient[x, sSL$ SPD[e, p1]], Coefficient[x, sSR$ SPD[e, p1]]};
   If[Expand[x - c . {sEL$, sER$, sSL$ SPD[e, p1], sSR$ SPD[e, p1]}] =!= 0, Print["   WARNING: terms outside the four structures"]];
   c];
insertFN$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelFileFN$,
    GenericModel -> modelFileFN$, ExcludeParticles -> {V[4]}], RuleDelayed::rhs];
topsVertFN$ = CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}];
uvFN$[x_] := Simplify[SeriesCoefficient[x /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep, C0[__] -> 0} /. D -> 4 - 2 ep, {ep, 0, -1}]];

namesFN$ = If[Length[$ScriptCommandLine] >= 2, {$ScriptCommandLine[[2]]}, {"bsg", "zbs"}];
Print["processes: ", namesFN$];


(* ::Subsubsection:: *)
(*Inspect: the vertex diagrams of b -> s gamma and of Z -> b sbar*)


If[$Notebooks, Show /@ Render[Paint[insertFN$[topsVertFN$, procsFN$[#]["proc"]], DisplayFunction -> Identity]] & /@ {"bsg", "zbs"}]


(* ::Section:: *)
(*The vertices*)


runFN$[name_] := Module[{pr = procsFN$[name], t0 = AbsoluteTime[], aT, cT, a, r, c, poles},
   (* the flavour-diagonal tree: normalization of the external-leg terms *)
   onShellFN$[pr["treeKin"]];
   aT = convertFN$[CreateFeynAmp[insertFN$[CreateTopologies[0, 1 -> 2], pr["tree"]]], pr];
   cT = structFN$[DiracSimplify[Total[aT]], pr, pr["treeSpin"]];
   Print["   ", name, ": flavour-diagonal tree {eps P_L, eps P_R, (eps.p1) P_L, (eps.p1) P_R} = ", cT];
   (* the 1PI vertex *)
   onShellFN$[pr["kin"]];
   a = convertFN$[CreateFeynAmp[insertFN$[topsVertFN$, pr["proc"]], GaugeRules -> {}], pr];
   r = redFN$[#, pr["order"]] & /@ a;
   c = KK structFN$[Total[r], pr, pr["spin"]];
   c = Collect[#, {_A0, _B0, _C0}, Together] & /@ Expand[c];
   poles = uvFN$ /@ c;
   Print["   ", name, ": ", Count[r, x_ /; x =!= 0], " nonzero diagrams, ", Round[AbsoluteTime[] - t0], " s;  CKM products: ",
     Union[Cases[c, _cK | _cKc, Infinity]], ";  UV poles of the (eps.p1) parts (expect {0, 0}): ",
     Simplify[poles[[3 ;; 4]]], ";  gauge parameters in the poles: ", Union[Cases[poles, xiA | xiZ | xiW | xiG, Infinity]]];
   <|"name" -> name, "tree" -> cT, "F" -> c, "pole" -> poles|>];

resFN$ = Table[Module[{res = runFN$[name]}, Put[res, FileNameJoin[{workDirFN$, "fcnc_" <> name <> ".m"}]]; res], {name, namesFN$}];
Print["Summary: ", Table[{r["name"], Simplify[r["pole"][[3 ;; 4]]]}, {r, resFN$}]];
