(* ::Package:: *)

(* ::Title:: *)
(*Step (5) of the CKM note: the one-loop vertex W+ -> u_i dbar_j in a general R_xi gauge (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm_ckm, step (5).  The 1PI one-loop electroweak vertex of W+(k) -> u_i(p1) dbar_j(p2) for the*)
(*six channels i = u, c and j = d, s, b, from the FeynArts model of this note (Src/generated/SM_CKM_FA) at particle level,*)
(*with the photon mass MA of steps (3), (4) (a copy of the model with Mass -> MA for V[1] and U[1]); the gluon (V[4]) is*)
(*left out (the QCD correction multiplies V_ij and is the same as for V = 1).  On shell: k^2 = MW^2, p1^2 = m_ui^2,*)
(*p2^2 = m_dj^2, eps.k = 0, Dirac equation for ubar(p1), v(p2).  The amplitude is written as*)
(*  M = (e/(sqrt2 sw)) ubar(p1) [ epsslash (FL P_L + FR P_R) + (eps.p1) (HL P_L + HR P_R) ] v(p2)*)
(*with the tree FL = V_ij; the one-loop vertex gives K FL, K FR, K HL, K HR (K = 16 pi^2) in A0, B0, C0 with D kept.*)
(*Checks: (a) the tree amplitude of FeynArts is I times the Feynman rule (i e/(sqrt2 sw)) V_ij gamma P_L of the note's*)
(*Table rules-ckm (Feynman rule = i x Lagrangian coefficient); (b) every form factor is proportional to V_ij alone (Fig. wud (a), (b)); (c) FR, HL, HR have no UV*)
(*pole, the pole of FL depends on the gauge parameters (it cancels against the external legs, wud_renormalized.wl);*)
(*(d) the spin and polarization sums of M0^* M1 for the four structures (4 dimensions) against the closed forms used*)
(*in wud_renormalized.wl.  Conventions as in step (4): the one-loop correction in units of the Feynman rule is I times*)
(*the FeynArts amplitudes after TID (TID gives I Pi^2 times the PaVe functions) have the normalization of the tree*)
(*amplitude, which is I times the rule (i e/(sqrt2 sw)) V_ij gamma P_L = -(e/(sqrt2 sw)) V_ij gamma P_L; so FL etc. are*)
(*-(sqrt2 sw/ee) times the coefficients of the FeynArts loop amplitude (the sign is confirmed by the UV finiteness in*)
(*wud_renormalized.wl and by FormCalc in wud_formcalc.wl).*)
(*Writes work/wud_vertex_<i><j>.m for each channel.*)


(* ::Text:: *)
(*How to run.  Batch, one channel per process (run_wud_check.sh starts the six in parallel, about 8 minutes):*)
(*  wolframscript -file wud_vertex_feyncalc.wl 2 3   (channel W+ -> c bbar).  Without arguments (batch or notebook)*)
(*all six channels are computed one after the other (about 45 minutes).  Interactive:  ~/hep/bin/wopen*)
(*wud_vertex_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirWV$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
workDirWV$ = FileNameJoin[{srcDirWV$, "work"}];
Quiet[CreateDirectory[workDirWV$]];
modelTmpDirWV$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirWV$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpDirWV$, "SM_CKM_FA"}]];
modFileWV$ = FileNameJoin[{modelTmpDirWV$, "SM_CKM_FA", "SM_CKM_FA.mod"}];
modTextWV$ = StringReplace[Import[modFileWV$, "Text"], {
    RegularExpression["(?s)(V\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA",
    RegularExpression["(?s)(U\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA"}];
Export[modFileWV$, modTextWV$, "Text"];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirWV$, "SM_CKM_FA"}], Quiet -> True];
modelFileWV$ = FileNameJoin[{modelTmpDirWV$, "SM_CKM_FA", "SM_CKM_FA"}];

massWV$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me, FCGV["MA"] -> MA};
lepMWV$ = {Me, MMU, MTA}; upMWV$ = {MU, MC, MT}; dnMWV$ = {MD, MS, MB};
yukWV$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMWV$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMWV$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMWV$[[i]]/vev, 0]};
(* V_ij as the opaque symbols cK[i, j], its conjugate cKc[i, j] (step (4)) *)
ckmWV$ = {Conjugate[CKM[i_Integer, j_Integer]] :> cKc[i, j], CKM[i_Integer, j_Integer] :> cK[i, j]};
convWV$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG,
    GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
    GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1},
   massWV$];
sumOverWV$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];
convertWV$[fa_, in_, out_] := Module[{a},
   a = Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q},
       ChangeDimension -> D, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> False,
       DropIndexSum -> False], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a = (sumOverWV$ /@ a) /. convWV$ /. yukWV$ /. ckmWV$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee;
   If[! FreeQ[a, CKM | IndexSum], Print["   WARNING: CKM or IndexSum left"]];
   (* the W polarization vector as a plain external vector epsW, and k = p1 + p2 *)
   a = a /. Polarization[k, I] -> epsW;
   FCReplaceMomenta[#, {k -> p1 + p2}] & /@ DeleteCases[a, 0]];
KK = (4 Pi)^2;
(* diagram by diagram: FDS, Dirac and colour algebra, TID, Dirac equation (DiracOrder puts pslash1 next to ubar(p1)
   and pslash2 next to v(p2)) *)
redWV$[x_] := Module[{r = FDS[x, q]},
   r = DiracSimplify[SUNSimplify[DotSimplify[r], SUNNToCACF -> True] /. SUNFDelta[__] -> 1];
   r = TID[r, q, ToPaVe -> True];
   r = DiracSimplify[r];
   DiracSimplify[DiracOrder[r, {p1, epsW, p2}]]];
(* the four on-shell structures; eps.p2 = -eps.p1 *)
structWV$[r_, mi_, mj_] := Module[{sp1 = Spinor[Momentum[p1, D], mi, 1], sp2 = Spinor[-Momentum[p2, D], mj, 1], x, c},
   x = FCE[r] /. SPD[epsW, p2] -> -SPD[epsW, p1];
   x = Expand[x /. {sp1 . GSD[epsW] . GA[7] . sp2 -> sEL$, sp1 . GSD[epsW] . GA[6] . sp2 -> sER$,
        sp1 . GA[7] . sp2 -> sSL$, sp1 . GA[6] . sp2 -> sSR$}];
   c = {Coefficient[x, sEL$], Coefficient[x, sER$], Coefficient[x, sSL$ SPD[epsW, p1]], Coefficient[x, sSR$ SPD[epsW, p1]]};
   If[Expand[x - c . {sEL$, sER$, sSL$ SPD[epsW, p1], sSR$ SPD[epsW, p1]}] =!= 0,
     Print["   WARNING: terms outside the four structures"]];
   c];
onShellWV$[mi_, mj_] := (FCClearScalarProducts[]; SPD[p1, p1] = mi^2; SPD[p2, p2] = mj^2;
   SPD[p1, p2] = (MW^2 - mi^2 - mj^2)/2;);
procWV$[i_, j_] := {V[3]} -> {F[3, {i}], -F[4, {j}]};
insertWV$[tops_, i_, j_] := Quiet[InsertFields[tops, procWV$[i, j], InsertionLevel -> {Particles}, Model -> modelFileWV$,
    GenericModel -> modelFileWV$, ExcludeParticles -> {V[4]}], RuleDelayed::rhs];
topsTreeWV$ = CreateTopologies[0, 1 -> 2];
topsVertWV$ = CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}];
uvWV$[x_] := Simplify[SeriesCoefficient[x /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep, C0[__] -> 0} /. D -> 4 - 2 ep,
     {ep, 0, -1}] /. MZ -> MW/cw];

channelsWV$ = If[Length[$ScriptCommandLine] >= 3,
   {ToExpression /@ $ScriptCommandLine[[2 ;; 3]]},
   Flatten[Table[{i, j}, {i, 2}, {j, 3}], 1]];
Print["channels W+ -> u_i dbar_j, {i, j}: ", channelsWV$];


(* ::Subsubsection:: *)
(*Inspect: the vertex diagrams of W+ -> c bbar*)


If[$Notebooks, Show /@ Render[Paint[insertWV$[topsVertWV$, 2, 3], DisplayFunction -> Identity]]]


(* ::Section:: *)
(*(a) Tree amplitudes*)


treeWV$ = Table[Module[{i = ch[[1]], j = ch[[2]], mi, mj, a, c},
    mi = upMWV$[[i]]; mj = dnMWV$[[j]]; onShellWV$[mi, mj];
    a = convertWV$[CreateFeynAmp[insertWV$[topsTreeWV$, i, j]], {k}, {p1, p2}];
    c = structWV$[DiracSimplify[Total[a] /. SUNFDelta[__] -> 1], mi, mj];
    (* expect I times the rule (i e/(sqrt2 sw)) V_ij gamma P_L *)
    Simplify[c/(I (I ee/(Sqrt[2] sw)) cK[i, j])]], {ch, channelsWV$}];
Print["(a) FeynArts tree amplitudes / (I x rule), {FL, FR, HL, HR} (expect {1, 0, 0, 0}): ", Union[treeWV$]];


(* ::Section:: *)
(*(b), (c) The one-loop vertex*)


vertexWV$[i_, j_] := Module[{mi = upMWV$[[i]], mj = dnMWV$[[j]], a, t0 = AbsoluteTime[], r, c, f, prop, poles},
   onShellWV$[mi, mj];
   a = convertWV$[CreateFeynAmp[insertWV$[topsVertWV$, i, j], GaugeRules -> {}], {k}, {p1, p2}];
   r = redWV$ /@ a;
   c = structWV$[Total[r], mi, mj];
   (* K FL, K FR, K HL, K HR in units of e/(sqrt2 sw): the loop amplitude over the tree amplitude -(e/(sqrt2 sw)) V_ij *)
   f = -KK Sqrt[2] sw/ee c;
   prop = FreeQ[f /. cK[i, j] -> 0, cK | cKc] && (Expand[f /. cK[i, j] -> 0] === {0, 0, 0, 0});
   f = Collect[#, {_A0, _B0, _C0}, Together] & /@ Expand[f /. cK[i, j] -> 1];
   poles = uvWV$ /@ f;
   Print["   W+ -> u_", i, " dbar_", j, ": ", Count[r, x_ /; x =!= 0], " nonzero diagrams, ",
     Round[AbsoluteTime[] - t0], " s;  proportional to V_ij alone: ", prop,
     ";  UV poles of K FR, K HL, K HR (expect {0, 0, 0}): ", Rest[poles],
     ";  gauge parameters in the pole of K FL: ", Union[Cases[poles[[1]], xiA | xiZ | xiW | xiG, Infinity]]];
   <|"channel" -> {i, j}, "F" -> f, "pole" -> poles, "prop" -> prop|>];

Print["(b) the vertex for each channel"];
vtxWV$ = Table[Module[{res = vertexWV$[ch[[1]], ch[[2]]]},
    Put[res, FileNameJoin[{workDirWV$, "wud_vertex_" <> ToString[ch[[1]]] <> ToString[ch[[2]]] <> ".m"}]];
    res], {ch, channelsWV$}];


(* ::Section:: *)
(*(d) Spin and polarization sums*)


(* sum over spins and W polarizations of M0^* M1 for M0 = ubar epsslash P_L v and M1 one of the four structures, in 4
   dimensions; closed forms of wud_renormalized.wl with a = m_i, b = m_j, s = MW^2 *)
FCClearScalarProducts[];
SP[p1, p1] = a$^2; SP[p2, p2] = b$^2; SP[p1, p2] = (s$ - a$^2 - b$^2)/2;
polWV$ = -MT[mu, nu] + (FV[p1, mu] + FV[p2, mu]) (FV[p1, nu] + FV[p2, nu])/s$;
gWV$ = {GA[nu] . GA[7], GA[nu] . GA[6], FV[p1, nu] GA[7], FV[p1, nu] GA[6]};
trWV$ = Simplify[Contract[polWV$ DiracTrace[GA[6] . GA[mu] . (GS[p1] + a$) . # . (GS[p2] - b$), DiracTraceEvaluate -> True]]] & /@ gWV$;
pp$ = (s$ - a$^2 - b$^2)/2; kp1$ = a$^2 + pp$; kp2$ = b$^2 + pp$;
closedWV$ = {2 (pp$ + 2 kp1$ kp2$/s$), 6 a$ b$, 2 a$ (-pp$ + kp1$ kp2$/s$), -2 b$ (-a$^2 + kp1$^2/s$)};
Print["(d) traces minus the closed forms (expect {0, 0, 0, 0}): ", Simplify[trWV$ - closedWV$]];

Print["Summary (expect {1, 0, 0, 0}; True; {0, 0, 0}; {0, 0, 0, 0}): ", Union[treeWV$], "; ", And @@ (#["prop"] & /@ vtxWV$),
  "; ", Union[Rest[#["pole"]] & /@ vtxWV$], "; ", Simplify[trWV$ - closedWV$]];
