(* ::Package:: *)

(* ::Title:: *)
(*Step (4a) of the NLO note: the weak one-loop vertex Z -> f fbar and the weak fermion self-energy in a general R_xi gauge*)


(* ::Text:: *)
(*Research note models/sm_nlo, step (4a).  From the note's FeynArts model (Src/generated/SM_CKM_FA, GaugeXi kept) at particle*)
(*level, without the photon and the gluon in the loops (V[1], V[4] excluded): their part, the photon or gluon exchange with*)
(*the photonic and gluonic parts of the field constants and the real emission, is the K of steps (2), (3); the rest (Z, W, H*)
(*and Goldstone loops) is infrared finite.  For one fermion f = F[t, {g}] (command-line arguments t g):*)
(*  the tree and the 1PI vertex of Z(k) -> f(p1) fbar(p2) on shell (k^2 = MZ^2, p1^2 = p2^2 = m^2, eps.k = 0), written as*)
(*    M = g_Z ubar(p1) [ epsslash (FL P_L + FR P_R) + (eps.p1) (HL P_L + HR P_R) ] v(p2),  g_Z = e/(sw cw),*)
(*  with the tree FL = T3 - Q sw^2, FR = -Q sw^2 (the vertex over the tree amplitude, as the CKM note's wud_vertex_feyncalc.wl);*)
(*  the weak self-energy of f, Gamma > i [pslash P_L SL + pslash P_R SR + m (P_L SSL + P_R SSR)] (the CKM note's*)
(*  oneloop_ckm_feyncalc.wl), 1PI (the tadpole-attached diagrams only shift the mass: they do not enter the field constants);*)
(*  K = 16 pi^2 times all of them, in A0, B0, C0 with D kept; the CKM matrix as the symbols cK[i, j], cKc[i, j].*)
(*Checks: the tree against T3 - Q sw^2 and -Q sw^2 (one normalization for both chiralities); HL, HR have no UV pole; SSL = SSR.*)
(*Writes work/zff_<t><g>.m.  Batch:  wolframscript -file zff_feyncalc.wl t g  (run_zweak_check.sh runs the twelve fermions)*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirZF$ = DirectoryName[$InputFileName];
workDirZF$ = FileNameJoin[{srcDirZF$, "work"}];
Quiet[CreateDirectory[workDirZF$]];
t0ZF$ = AbsoluteTime[];
modelTmpZF$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirZF$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpZF$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpZF$, "SM_CKM_FA"}], Quiet -> True];
modelFileZF$ = FileNameJoin[{modelTmpZF$, "SM_CKM_FA", "SM_CKM_FA"}];

massZF$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me};
lepMZF$ = {Me, MMU, MTA}; upMZF$ = {MU, MC, MT}; dnMZF$ = {MD, MS, MB};
yukZF$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMZF$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMZF$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMZF$[[i]]/vev, 0]};
ckmZF$ = {Conjugate[CKM[i_Integer, j_Integer]] :> cKc[i, j], CKM[i_Integer, j_Integer] :> cK[i, j]};
convZF$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG,
    GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
    GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1},
   massZF$];
sumOverZF$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];
convertZF$[fa_, in_, out_] := Module[{a},
   a = Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q},
       ChangeDimension -> D, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> False,
       DropIndexSum -> False], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a = (sumOverZF$ /@ a) /. convZF$ /. yukZF$ /. ckmZF$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee;
   If[! FreeQ[a, CKM | IndexSum], Print["   WARNING: CKM or IndexSum left"]];
   a = a /. Polarization[k, I] -> epsZ;
   FCReplaceMomenta[#, {k -> p1 + p2}] & /@ DeleteCases[a, 0]];
KK = (4 Pi)^2;
excl$ = {V[1], V[4]};
insertZF$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelFileZF$,
    GenericModel -> modelFileZF$, ExcludeParticles -> excl$], RuleDelayed::rhs];

{tZF$, gZF$} = If[Length[$ScriptCommandLine] >= 3, ToExpression /@ $ScriptCommandLine[[2 ;; 3]], {4, 3}];
massOfZF$ = {0, lepMZF$[[gZF$]], upMZF$[[gZF$]], dnMZF$[[gZF$]]}[[tZF$]];
{t3ZF$, qZF$} = {{1/2, 0}, {-1/2, -1}, {1/2, 2/3}, {-1/2, -1/3}}[[tZF$]];
nameZF$ = {"nu", "l", "u", "d"}[[tZF$]] <> ToString[gZF$];
Print["fermion F[", tZF$, ", {", gZF$, "}] (", nameZF$, "), mass ", massOfZF$, ", T3 = ", t3ZF$, ", Q = ", qZF$];
procZF$ = {V[2]} -> {F[tZF$, {gZF$}], -F[tZF$, {gZF$}]};

(* ::Section:: *)
(*Vertex*)

onShellZF$[m_] := (FCClearScalarProducts[]; SPD[p1, p1] = m^2; SPD[p2, p2] = m^2; SPD[p1, p2] = (MZ^2 - 2 m^2)/2;);
redZF$[x_] := Module[{r = FDS[x, q]},
   r = DiracSimplify[SUNSimplify[DotSimplify[r], SUNNToCACF -> True] /. SUNFDelta[__] -> 1];
   r = TID[r, q, ToPaVe -> True];
   r = DiracSimplify[r];
   DiracSimplify[DiracOrder[r, {p1, epsZ, p2}]]];
structZF$[r_, m_] := Module[{sp1 = Spinor[Momentum[p1, D], m, 1], sp2 = Spinor[-Momentum[p2, D], m, 1], x, c},
   x = FCE[r] /. SPD[epsZ, p2] -> -SPD[epsZ, p1];
   x = Expand[x /. {sp1 . GSD[epsZ] . GA[7] . sp2 -> sEL$, sp1 . GSD[epsZ] . GA[6] . sp2 -> sER$,
        sp1 . GA[7] . sp2 -> sSL$, sp1 . GA[6] . sp2 -> sSR$, sp1 . GSD[epsZ] . sp2 -> sEL$ + sER$, sp1 . sp2 -> sSL$ + sSR$,
        sp1 . GSD[epsZ] . GA[5] . sp2 -> sER$ - sEL$, sp1 . GA[5] . sp2 -> sSR$ - sSL$}];
   c = {Coefficient[x, sEL$], Coefficient[x, sER$], Coefficient[x, sSL$ SPD[epsZ, p1]], Coefficient[x, sSR$ SPD[epsZ, p1]]};
   If[Expand[x - c . {sEL$, sER$, sSL$ SPD[epsZ, p1], sSR$ SPD[epsZ, p1]}] =!= 0,
     Print["   WARNING: terms outside the four structures: ",
      Short[Expand[x - c . {sEL$, sER$, sSL$ SPD[epsZ, p1], sSR$ SPD[epsZ, p1]}], 3]]];
   c];
uvZF$[x_] := Simplify[SeriesCoefficient[x /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep, C0[__] -> 0} /. D -> 4 - 2 ep,
     {ep, 0, -1}] /. MZ -> MW/cw];

onShellZF$[massOfZF$];
treeZF$ = structZF$[DiracSimplify[Total[convertZF$[CreateFeynAmp[insertZF$[CreateTopologies[0, 1 -> 2], procZF$]], {k}, {p1, p2}]]],
   massOfZF$];
(* one normalization for both chiralities: tree FL = T3 - Q sw^2, FR = -Q sw^2 in units of g_Z *)
tauZF$ = Simplify[treeZF$[[1]]/(t3ZF$ - qZF$ sw^2)];
Print["tree {FL, FR, HL, HR} over the normalization (expect {T3 - Q sw^2, -Q sw^2, 0, 0} = ",
  {t3ZF$ - qZF$ sw^2, -qZF$ sw^2, 0, 0}, "): ", Simplify[treeZF$/tauZF$ /. cw -> Sqrt[1 - sw^2]], ";  normalization ",
  Simplify[tauZF$ /. cw -> Sqrt[1 - sw^2]], " (g_Z = e/(sw cw) up to a phase)"];

diagsZF$ = insertZF$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], procZF$];
ampZF$ = convertZF$[CreateFeynAmp[diagsZF$, GaugeRules -> {}], {k}, {p1, p2}];
Print["vertex: ", Length[ampZF$], " diagrams;  ", Round[AbsoluteTime[] - t0ZF$], " s"];
redAmpZF$ = redZF$ /@ ampZF$;
vtxZF$ = Collect[#, {_A0, _B0, _C0}, Together] & /@ (KK structZF$[Total[redAmpZF$], massOfZF$]/tauZF$);
Print["vertex reduced;  ", Round[AbsoluteTime[] - t0ZF$], " s;  UV poles of K HL, K HR (expect {0, 0}): ",
  uvZF$ /@ vtxZF$[[3 ;; 4]], ";  gauge parameters in the poles of K FL, K FR: ",
  Union[Cases[uvZF$ /@ vtxZF$[[1 ;; 2]], xiA | xiZ | xiW | xiG, Infinity]]];

(* ::Section:: *)
(*Weak self-energy of f*)

chiralZF$[r_] := Module[{x, x0, c},
   x = Expand[FCE[r] /. {GSD[p] . GA[7] -> pLs$, GSD[p] . GA[6] -> pRs$, GSD[p] . GA[5] -> pRs$ - pLs$,
         GA[7] -> pL$, GA[6] -> pR$, GA[5] -> pR$ - pL$} /. GSD[p] -> pLs$ + pRs$];
   If[! FreeQ[x, GA | GSD | DiracGamma | Dot],
     Print["   WARNING: unexpected Dirac structure: ", Union[Cases[x, _GA | _GSD | _Dot | _DiracGamma, Infinity]]]];
   x0 = x /. {pLs$ -> 0, pRs$ -> 0, pL$ -> 0, pR$ -> 0};
   c = (Coefficient[x, #] & /@ {pLs$, pRs$, pL$, pR$}) + {0, 0, x0, x0};
   KK c];
reduceSEZF$[x_] := Module[{r},
   r = FDS[x, q];
   r = TID[DiracSimplify[SUNSimplify[DotSimplify[r], SUNNToCACF -> True] /. SUNFDelta[__] -> 1], q, ToPaVe -> True];
   r = DiracSimplify[r];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]};
   r /. {B0[0, 0, 0] -> 0, A0[0] -> 0}];
FCClearScalarProducts[];
seDiagsZF$ = insertZF$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {F[tZF$, {gZF$}]} -> {F[tZF$, {gZF$}]}];
seAmpZF$ = Quiet[FCFAConvert[CreateFeynAmp[seDiagsZF$, Truncated -> True, GaugeRules -> {}] /. M$FACouplings,
     IncomingMomenta -> {p}, OutgoingMomenta -> {p}, LoopMomenta -> {q}, ChangeDimension -> D, List -> True, SMP -> False,
     UndoChiralSplittings -> True, DropSumOver -> False, DropIndexSum -> False], RuleDelayed::rhs];
seAmpZF$ = seAmpZF$ /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
seAmpZF$ = (sumOverZF$ /@ seAmpZF$) /. convZF$ /. yukZF$ /. ckmZF$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee;
seZF$ = chiralZF$[reduceSEZF$[Total[seAmpZF$]]];
(* SSL = (coefficient of P_L)/m, SSR = (coefficient of P_R)/m *)
seZF$ = Simplify /@ If[massOfZF$ === 0, {seZF$[[1]], seZF$[[2]], 0, 0}, {seZF$[[1]], seZF$[[2]], seZF$[[3]]/massOfZF$, seZF$[[4]]/massOfZF$}];
Print["self-energy: ", Length[seAmpZF$], " diagrams;  SSL - SSR (expect 0): ", Simplify[seZF$[[3]] - seZF$[[4]]],
  If[massOfZF$ === 0, ";  massless: the P_L, P_R terms are 0", ""], ";  ", Round[AbsoluteTime[] - t0ZF$], " s"];

Put[<|"fermion" -> {tZF$, gZF$}, "name" -> nameZF$, "mass" -> massOfZF$, "T3" -> t3ZF$, "Q" -> qZF$, "tree" -> treeZF$/tauZF$,
   "F" -> vtxZF$, "SE" -> seZF$|>, FileNameJoin[{workDirZF$, "zff_" <> ToString[tZF$] <> ToString[gZF$] <> ".m"}]];
Print["written: work/zff_", tZF$, gZF$, ".m;  ", Round[AbsoluteTime[] - t0ZF$], " s"];
DeleteDirectory[modelTmpZF$, DeleteContents -> True];
