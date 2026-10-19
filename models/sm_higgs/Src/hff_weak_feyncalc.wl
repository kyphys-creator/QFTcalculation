(* ::Package:: *)

(* ::Title:: *)
(*Step (5) of the Higgs note: the weak one-loop vertex H -> f fbar and the weak fermion self-energy in a general R_xi gauge*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (5); the Yukawa version of the NLO note's zff_feyncalc.wl (step (4a)).  From the note's*)
(*FeynArts model (generated/SM_CKM_FA, GaugeXi kept) at particle level, without the photon and the gluon in the loops (V[1],*)
(*V[4] excluded: their part, the photon exchange with the photonic field constants and the real photons, is the QED K of step*)
(*(4)); the rest (Z, W, H and Goldstone loops) is infrared finite.  For one fermion f = F[t, {g}] (command-line arguments t g):*)
(*  the tree and the 1PI vertex of H(k) -> f(p1) fbar(p2) on shell (k^2 = MH^2, p1^2 = p2^2 = m^2), written as*)
(*    M = -(i/sqrt2) y ubar(p1) (FL P_L + FR P_R) v(p2),  FL = FR = 1 at tree level*)
(*  (the vertex over the tree amplitude); there is no tadpole diagram of the vertex (no H H f fbar vertex: the count is printed);*)
(*  the weak self-energy of f, Gamma > i [pslash P_L SL + pslash P_R SR + m (P_L SSL + P_R SSR)], 1PI, and its tadpole-attached*)
(*  diagrams apart (they must be independent of p and scalar, so that they do not enter the field constants);*)
(*  K = 16 pi^2 times all of them, in A0, B0, C0 with D kept; the CKM matrix as the symbols cK[i, j], cKc[i, j].*)
(*Writes work/hff_<t><g>.m.  Batch:  wolframscript -file hff_weak_feyncalc.wl t g  (run_hff_weak_check.sh runs b, c, tau, mu)*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirHW$ = DirectoryName[$InputFileName];
workDirHW$ = FileNameJoin[{srcDirHW$, "work"}];
Quiet[CreateDirectory[workDirHW$]];
t0HW$ = AbsoluteTime[];
modelTmpHW$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirHW$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpHW$, "SM_CKM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpHW$, "SM_CKM_FA"}], Quiet -> True];
modelFileHW$ = FileNameJoin[{modelTmpHW$, "SM_CKM_FA", "SM_CKM_FA"}];

massHW$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me};
lepMHW$ = {Me, MMU, MTA}; upMHW$ = {MU, MC, MT}; dnMHW$ = {MD, MS, MB};
yukHW$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMHW$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMHW$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMHW$[[i]]/vev, 0]};
ckmHW$ = {Conjugate[CKM[i_Integer, j_Integer]] :> cKc[i, j], CKM[i_Integer, j_Integer] :> cK[i, j]};
convHW$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG,
    GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
    GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1},
   massHW$];
sumOverHW$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];
convertHW$[fa_, in_, out_] := Module[{a},
   a = Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q},
       ChangeDimension -> D, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> False,
       DropIndexSum -> False], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a = (sumOverHW$ /@ a) /. convHW$ /. yukHW$ /. ckmHW$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee;
   If[! FreeQ[a, CKM | IndexSum], Print["   WARNING: CKM or IndexSum left"]];
   FCReplaceMomenta[#, {k -> p1 + p2}] & /@ DeleteCases[a, 0]];
KK = (4 Pi)^2;
excl$ = {V[1], V[4]};
insertHW$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelFileHW$,
    GenericModel -> modelFileHW$, ExcludeParticles -> excl$], RuleDelayed::rhs];

{tHW$, gHW$} = If[Length[$ScriptCommandLine] >= 3, ToExpression /@ $ScriptCommandLine[[2 ;; 3]], {4, 3}];
massOfHW$ = {0, lepMHW$[[gHW$]], upMHW$[[gHW$]], dnMHW$[[gHW$]]}[[tHW$]];
{t3HW$, qHW$} = {{1/2, 0}, {-1/2, -1}, {1/2, 2/3}, {-1/2, -1/3}}[[tHW$]];
nameHW$ = {"nu", "l", "u", "d"}[[tHW$]] <> ToString[gHW$];
Print["fermion F[", tHW$, ", {", gHW$, "}] (", nameHW$, "), mass ", massOfHW$, ", T3 = ", t3HW$, ", Q = ", qHW$];
procHW$ = {S[1]} -> {F[tHW$, {gHW$}], -F[tHW$, {gHW$}]};

(* ::Section:: *)
(*Vertex*)

onShellHW$[m_] := (FCClearScalarProducts[]; SPD[p1, p1] = m^2; SPD[p2, p2] = m^2; SPD[p1, p2] = (MH^2 - 2 m^2)/2;);
redHW$[x_] := Module[{r = FDS[x, q]},
   r = DiracSimplify[SUNSimplify[DotSimplify[r], SUNNToCACF -> True] /. SUNFDelta[__] -> 1];
   r = TID[r, q, ToPaVe -> True];
   DiracSimplify[r]];
structHW$[r_, m_] := Module[{sp1 = Spinor[Momentum[p1, D], m, 1], sp2 = Spinor[-Momentum[p2, D], m, 1], x, c},
   x = Expand[FCE[r] /. {sp1 . GA[7] . sp2 -> sSL$, sp1 . GA[6] . sp2 -> sSR$, sp1 . sp2 -> sSL$ + sSR$, sp1 . GA[5] . sp2 -> sSR$ - sSL$}];
   c = {Coefficient[x, sSL$], Coefficient[x, sSR$]};
   If[Expand[x - c . {sSL$, sSR$}] =!= 0, Print["   WARNING: terms outside the two structures: ", Short[Expand[x - c . {sSL$, sSR$}], 3]]];
   c];
uvHW$[x_] := Simplify[SeriesCoefficient[x /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep, C0[__] -> 0} /. D -> 4 - 2 ep, {ep, 0, -1}] /. MZ -> MW/cw];

onShellHW$[massOfHW$];
treeHW$ = structHW$[DiracSimplify[Total[convertHW$[CreateFeynAmp[insertHW$[CreateTopologies[0, 1 -> 2], procHW$]], {k}, {p1, p2}]]],
   massOfHW$];
(* the normalization -(i/sqrt2) y with y = sqrt(2) m/v, v = 2 MW sw/e *)
tauHW$ = Simplify[treeHW$[[1]]];
Print["tree {FL, FR} over the normalization (expect {1, 1}): ", Simplify[treeHW$/tauHW$], ";  normalization ", tauHW$,
  " (expect -(i/sqrt2) sqrt(2) m e/(2 MW sw) = ", Simplify[-I massOfHW$ ee/(2 MW sw)], ")"];

nTadHW$ = Length[CreateFeynAmp[insertHW$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {WFCorrections}], procHW$]]] -
   Length[CreateFeynAmp[insertHW$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], procHW$]]];
diagsHW$ = insertHW$[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections}], procHW$];
ampHW$ = convertHW$[CreateFeynAmp[diagsHW$, GaugeRules -> {}], {k}, {p1, p2}];
Print["vertex: ", Length[ampHW$], " diagrams (the tadpole topologies add ", nTadHW$,
  " insertions: the tadpoles on the external lines, a part of the masses);  ", Round[AbsoluteTime[] - t0HW$], " s"];
redAmpHW$ = redHW$ /@ ampHW$;
vtxHW$ = Collect[#, {_A0, _B0, _C0}, Together] & /@ (KK structHW$[Total[redAmpHW$], massOfHW$]/tauHW$);
Print["vertex reduced;  ", Round[AbsoluteTime[] - t0HW$], " s;  gauge parameters in the poles of K FL, K FR: ",
  Union[Cases[uvHW$ /@ vtxHW$, xiA | xiZ | xiW | xiG, Infinity]]];

(* ::Section:: *)
(*Weak self-energy of f, without and with the tadpole-attached diagrams*)

chiralHW$[r_] := Module[{x, x0, c},
   x = Expand[FCE[r] /. {GSD[p] . GA[7] -> pLs$, GSD[p] . GA[6] -> pRs$, GSD[p] . GA[5] -> pRs$ - pLs$,
         GA[7] -> pL$, GA[6] -> pR$, GA[5] -> pR$ - pL$} /. GSD[p] -> pLs$ + pRs$];
   If[! FreeQ[x, GA | GSD | DiracGamma | Dot],
     Print["   WARNING: unexpected Dirac structure: ", Union[Cases[x, _GA | _GSD | _Dot | _DiracGamma, Infinity]]]];
   x0 = x /. {pLs$ -> 0, pRs$ -> 0, pL$ -> 0, pR$ -> 0};
   c = (Coefficient[x, #] & /@ {pLs$, pRs$, pL$, pR$}) + {0, 0, x0, x0};
   KK c];
reduceSEHW$[x_] := Module[{r},
   r = FDS[x, q];
   r = TID[DiracSimplify[SUNSimplify[DotSimplify[r], SUNNToCACF -> True] /. SUNFDelta[__] -> 1], q, ToPaVe -> True];
   r = DiracSimplify[r];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]};
   r /. {B0[0, 0, 0] -> 0, A0[0] -> 0}];
seOf$[tops_] := Module[{d, a},
   d = insertHW$[tops, {F[tHW$, {gHW$}]} -> {F[tHW$, {gHW$}]}];
   a = Quiet[FCFAConvert[CreateFeynAmp[d, Truncated -> True, GaugeRules -> {}] /. M$FACouplings,
       IncomingMomenta -> {p}, OutgoingMomenta -> {p}, LoopMomenta -> {q}, ChangeDimension -> D, List -> True, SMP -> False,
       UndoChiralSplittings -> True, DropSumOver -> False, DropIndexSum -> False], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a = (sumOverHW$ /@ a) /. convHW$ /. yukHW$ /. ckmHW$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee;
   {Length[a], If[a === {}, {0, 0, 0, 0}, chiralHW$[reduceSEHW$[Total[a]]]]}];
FCClearScalarProducts[];
{nSE$, seRaw$} = seOf$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}]];
{nAll$, seAllRaw$} = seOf$[CreateTopologies[1, 1 -> 1]];
norm$[c_] := Simplify /@ {c[[1]], c[[2]], c[[3]]/massOfHW$, c[[4]]/massOfHW$};
seHW$ = norm$[seRaw$];
seTadHW$ = Simplify /@ (norm$[seAllRaw$] - seHW$);
Print["self-energy: ", nSE$, " diagrams (1PI);  SSL - SSR (expect 0): ", Simplify[seHW$[[3]] - seHW$[[4]]],
  ";  the ", nAll$ - nSE$, " tadpole-attached diagrams: {SL, SR} ", seTadHW$[[1 ;; 2]], " (expect {0, 0}), SS depends on p: ",
  ! FreeQ[seTadHW$[[3 ;; 4]], p], " (expect False);  ", Round[AbsoluteTime[] - t0HW$], " s"];

Put[<|"fermion" -> {tHW$, gHW$}, "name" -> nameHW$, "mass" -> massOfHW$, "T3" -> t3HW$, "Q" -> qHW$, "tree" -> treeHW$/tauHW$,
   "F" -> vtxHW$, "SE" -> seHW$, "SEtad" -> seTadHW$, "nTadVertex" -> nTadHW$|>,
  FileNameJoin[{workDirHW$, "hff_" <> ToString[tHW$] <> ToString[gHW$] <> ".m"}]];
Print["written: work/hff_", tHW$, gHW$, ".m;  ", Round[AbsoluteTime[] - t0HW$], " s"];
DeleteDirectory[modelTmpHW$, DeleteContents -> True];
