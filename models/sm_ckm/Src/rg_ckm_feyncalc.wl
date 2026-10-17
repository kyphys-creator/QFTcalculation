(* ::Package:: *)

(* ::Title:: *)
(*Step (4) of the CKM note: the Yukawa-matrix beta functions from the note's model (ubar d G+ vertex and field renormalizations, general R_xi)*)


(* ::Text:: *)
(*Research note models/sm_ckm, step (4).  The MS-bar counterterms of the Yukawa matrices are solved from the one-loop UV*)
(*poles of the note's model in a general R_xi gauge, without using Eq. (betaY):*)
(*  - the 1PI vertex ubar_i d_j G+ (all 9 generation pairs, external momenta 0; its UV pole does not depend on them):*)
(*    the vertex is -A P_R + B P_L with A = Y_d = V yhat_d (doublet basis, Y_u diagonal) and B = Y_u^dagger V (note*)
(*    Table rules-ckm); the one-loop correction i M_FA has the UV pole c_R P_R + c_L P_L;*)
(*  - the hermitian MS-bar field renormalizations of the quarks in the mass basis, dZ^{qL} = -SL|UV, dZ^{qR} = -SR|UV*)
(*    (step (3), results/oneloop_ckm_sigma.m), and of G+, dZ_G = -d Sigma^G/dk^2 |UV (computed here);*)
(*  - finiteness of the vertex with the counterterm of the bare doublet-basis Lagrangian:*)
(*      dA = c_R - (1/2)(dZ^{uL+} A + A dZ^{dR} + dZ_G A),   dB = -c_L - (1/2)(dZ^{uR+} B + B dZ^{dL} + dZ_G B),*)
(*    dY_d = dA, dY_u^+ = dB V^+ (the doublet-basis field of the down-type quarks is V d).*)
(*The results are compared, matrix entry by matrix entry, with (Delta/2) beta of Eq. (betaY): exactly for a unitary V with*)
(*rational sines and cosines (masses, couplings, gauge parameters symbolic), and in 50 digits for the benchmark V; they are*)
(*checked to be free of xiA, xiZ, xiW, xiG.  The IBP identity for the IR-divergent scalar C0 is applied before the poles are read off (the*)
(*step-(3) field renormalizations have a spurious 1/k^2 gluon term otherwise).  K = 16 pi^2; all quantities are K times*)
(*the coefficient of 1/eps.  V_ij are opaque symbols cK[i, j] (and cKc[i, j] for the conjugate) until the comparison.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file rg_ckm_feyncalc.wl  (run oneloop_ckm_feyncalc.wl first; about 8 minutes).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirRG$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirRG$ = FileNameJoin[{srcDirRG$, "results"}];
modelTmpDirRG$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirRG$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpDirRG$, "SM_CKM_FA"}]];
modFileRG$ = FileNameJoin[{modelTmpDirRG$, "SM_CKM_FA", "SM_CKM_FA.mod"}];
modTextRG$ = StringReplace[Import[modFileRG$, "Text"], {
    RegularExpression["(?s)(V\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA",
    RegularExpression["(?s)(U\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA"}];
Export[modFileRG$, modTextRG$, "Text"];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirRG$, "SM_CKM_FA"}], Quiet -> True];
modelFileRG$ = FileNameJoin[{modelTmpDirRG$, "SM_CKM_FA", "SM_CKM_FA"}];

massRG$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me, FCGV["MA"] -> MA};
lepMRG$ = {Me, MMU, MTA}; upMRG$ = {MU, MC, MT}; dnMRG$ = {MD, MS, MB};
yukRG$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMRG$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMRG$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMRG$[[i]]/vev, 0]};
ckmRG$ = {Conjugate[CKM[i_Integer, j_Integer]] :> cKc[i, j], CKM[i_Integer, j_Integer] :> cK[i, j]};
convRG$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG,
    GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
    GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1},
   massRG$];
sumOverRG$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];
convertRG$[fa_, in_, out_] := Module[{a},
   a = Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q},
       ChangeDimension -> D, List -> True, SMP -> False, UndoChiralSplittings -> True, DropSumOver -> False,
       DropIndexSum -> False], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a = (sumOverRG$ /@ a) /. convRG$ /. yukRG$ /. ckmRG$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee;
   If[! FreeQ[a, CKM | IndexSum], Print["   WARNING: CKM or IndexSum left"]];
   DeleteCases[a, 0]];
KK = (4 Pi)^2;
(* diagram by diagram: FDS, Dirac and colour algebra, TID, reduction to A0, B0, C0 *)
redRG$[x_] := Module[{r = FDS[x, q]},
   r = DiracSimplify[SUNSimplify[DotSimplify[r], SUNNToCACF -> True] /. SUNFDelta[__] -> 1];
   r = TID[r, q, ToPaVe -> True];
   r = DiracSimplify[r];
   PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]}];
(* The reduction can leave the scalar C0 with a doubled massless (gluon) propagator, PaVe[0, {0, pp, pp}, {0, 0, m2}],
   which is IR divergent although the tensor integrals it came from are IR finite; dropping it as "UV finite" loses a
   1/eps with a 1/k^2 coefficient.  The exact D-dimensional IBP identity (SM note, oneloop_smmod.wl) rewrites it in A0
   and B0 first; then the coefficient of 1/eps is the UV pole. *)
ibpRG$ = PaVe[0, {0, pp_, pp_}, {0, 0, m2_}] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2;
(* K times the coefficient of 1/eps (C0 and the other finite functions drop out) *)
poleRG$[x_] := Simplify[KK SeriesCoefficient[x /. ibpRG$ /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep, C0[__] -> 0, PaVe[__] -> 0} /.
       D -> 4 - 2 ep, {ep, 0, -1}] /. MA -> 0];


(* ::Section:: *)
(*The vertex ubar_i d_j G+*)


topsV$ = CreateTopologies[1, 2 -> 1, ExcludeTopologies -> {Tadpoles, WFCorrections}];
vertexRG$[i_, j_] := Module[{d, a, poles, x},
   d = Quiet[InsertFields[topsV$, {F[4, {j}], S[3]} -> {F[3, {i}]}, InsertionLevel -> {Particles},
       Model -> modelFileRG$, GenericModel -> modelFileRG$], RuleDelayed::rhs];
   a = convertRG$[CreateFeynAmp[d, Truncated -> True, GaugeRules -> {}], {p1, p2}, {p3}];
   a = FCReplaceMomenta[#, {p1 -> 0, p2 -> 0, p3 -> 0}] & /@ a;
   (* the one-loop correction to the vertex is i M_FA *)
   x = Expand[FCE[poleRG$[I Total[redRG$ /@ a]]]];
   If[! FreeQ[x /. {GA[6] -> 0, GA[7] -> 0}, GA | GSD | DiracGamma | Dot], Print["   WARNING: Dirac structure"]];
   Print["   vertex ubar_", i, " d_", j, " G+: ", Length[a], " nonzero diagrams"];
   {Coefficient[x, GA[6]], Coefficient[x, GA[7]]}];


(* ::Subsubsection:: *)
(*Inspect: the vertex diagrams of ubar_c b G+*)


If[$Notebooks, Show /@ Render[Paint[Quiet[InsertFields[topsV$, {F[4, {3}], S[3]} -> {F[3, {2}]}, InsertionLevel -> {Particles},
     Model -> modelFileRG$, GenericModel -> modelFileRG$], RuleDelayed::rhs], DisplayFunction -> Identity]]]


FCClearScalarProducts[];
Print["(a) the vertex ubar_i d_j G+ (UV poles)"];
vtxRG$ = Table[vertexRG$[i, j], {i, 3}, {j, 3}];
cRRG$ = vtxRG$[[All, All, 1]]; cLRG$ = vtxRG$[[All, All, 2]];
Print["(a) every entry proportional to V_ij alone (expect True): ",
  And @@ Flatten[Table[FreeQ[{cRRG$[[i, j]], cLRG$[[i, j]]} /. cK[i, j] -> 0, cK | cKc], {i, 3}, {j, 3}]]];


(* ::Section:: *)
(*The G+ field renormalization*)


topsSE$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];
Print["(b) G+ self-energy"];
sigGRG$ = Module[{d, a, r},
   d = Quiet[InsertFields[topsSE$, {S[3]} -> {S[3]}, InsertionLevel -> {Particles}, Model -> modelFileRG$,
       GenericModel -> modelFileRG$], RuleDelayed::rhs];
   a = convertRG$[CreateFeynAmp[d, Truncated -> True, GaugeRules -> {}], {k}, {k}];
   Print["   G+ -> G+: ", Length[a], " nonzero 1PI diagrams"];
   (* FeynArts' amplitude is Sigma^G (Gamma^G > i Sigma^G) *)
   poleRG$[Total[redRG$ /@ a]] /. {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2}];
dZGRG$ = Simplify[-D[sigGRG$, kk2]];
Print["(b) K dZ_G (coefficient of 1/eps): ", dZGRG$ /. MZ -> MW/cw];


(* ::Section:: *)
(*Quark field renormalizations from step (3)*)


sig3RG$ = Association[Get[FileNameJoin[{resDirRG$, "oneloop_ckm_sigma.m"}]]];
uvKRG$[x_] := Simplify[SeriesCoefficient[(x /. ibpRG$ /. {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2}) /.
       {B0[__] -> 1/ep, A0[m2_] :> m2/ep} /. D -> 4 - 2 ep, {ep, 0, -1}] /. MA -> 0];
(* step (3) wrote V_ij as vR + I vI: the same entries as cK *)
toCKRG$ = {vR[i_, j_] :> (cK[i, j] + cKc[i, j])/2, vI[i_, j_] :> (cK[i, j] - cKc[i, j])/(2 I)};
dZLRG$[sec_] := Table[-Expand[uvKRG$[sig3RG$[sec][[i, j, 1, 1]]] /. toCKRG$], {i, 3}, {j, 3}];
dZRRG$[sec_] := Table[-Expand[uvKRG$[sig3RG$[sec][[i, j, 1, 2]]] /. toCKRG$], {i, 3}, {j, 3}];
Print["(c) the field renormalizations dZ^{L,R} (after the IBP identity) do not depend on k^2 (expect True): ",
  FreeQ[{dZLRG$["U"], dZLRG$["D"], dZRRG$["U"], dZRRG$["D"]}, kk2]];
dZuL$ = dZLRG$["U"]; dZdL$ = dZLRG$["D"]; dZuR$ = dZRRG$["U"]; dZdR$ = dZRRG$["D"];
(* hermitian conjugate: transpose and cK <-> cKc, I -> -I *)
herm$[m_] := Transpose[m /. {cK -> cKtmp$, cKc -> cK} /. cKtmp$ -> cKc /. Complex[a_, b_] :> Complex[a, -b]];


(* ::Section:: *)
(*The Yukawa counterterms and Eq. (betaY)*)


vevRG$ = 2 MW sw/ee;
yRG$[m_] := Sqrt[2] m/vevRG$;
vM$ = Array[cK, {3, 3}];
vMc$ = Array[cKc, {3, 3}];          (* complex conjugate entries *)
yuHat$ = DiagonalMatrix[yRG$ /@ upMRG$]; ydHat$ = DiagonalMatrix[yRG$ /@ dnMRG$];
aM$ = vM$ . ydHat$;                  (* A = Y_d *)
bM$ = yuHat$ . vM$;                  (* B = Y_u^dagger V *)
dA$ = cRRG$ - 1/2 (herm$[dZuL$] . aM$ + aM$ . dZdR$ + dZGRG$ aM$);
dB$ = -cLRG$ - 1/2 (herm$[dZuR$] . bM$ + bM$ . dZdL$ + dZGRG$ bM$);
dYuDag$ = dB$ . Transpose[vMc$];     (* dY_u^dagger = dB V^dagger *)
Print["(d) gauge parameters left in dY_d and dY_u^dagger before unitarity: ", Union[Cases[{dA$, dYuDag$}, xiA | xiZ | xiW | xiG, Infinity]]];

(* Eq. (betaY) times K Delta/2 (the coefficient of 1/eps of K delta Y = K (Delta/2) beta_Y) *)
gSqRG$ = ee^2/sw^2; gpSqRG$ = ee^2/(1 - sw^2);
TTRG$ = Sum[3 yRG$[m]^2, {m, Join[upMRG$, dnMRG$]}] + Sum[yRG$[m]^2, {m, lepMRG$}];
huM$ = yuHat$ . yuHat$;              (* H_u = Y_u Y_u^dagger = D_u in this basis *)
hdM$ = vM$ . ydHat$ . ydHat$ . Transpose[vMc$];   (* H_d = V D_d V^dagger *)
id3$ = IdentityMatrix[3];
betaYd$ = 1/2 (3/2 (hdM$ - huM$) + (TTRG$ - 8 gS^2 - 9/4 gSqRG$ - 5/12 gpSqRG$) id3$) . aM$;
betaYuDag$ = 1/2 yuHat$ . (3/2 (huM$ - hdM$) + (TTRG$ - 8 gS^2 - 9/4 gSqRG$ - 17/12 gpSqRG$) id3$);

(* explicit standard parametrization (real angles) for the unitarity of V *)
vStdRG$ = {
   {c12 c13, s12 c13, s13 Exp[-I dl]},
   {-s12 c23 - c12 s23 s13 Exp[I dl], c12 c23 - s12 s23 s13 Exp[I dl], s23 c13},
   {s12 s23 - c12 c23 s13 Exp[I dl], -c12 s23 - s12 c23 s13 Exp[I dl], c23 c13}} /.
   {c12 -> Sqrt[1 - s12^2], c23 -> Sqrt[1 - s23^2], c13 -> Sqrt[1 - s13^2]};
(* exact check: the identity must hold for any unitary V.  Angles with rational sines and cosines (Pythagorean
   triples, all three large) and the phase as a symbol ph = e^{i delta} (conjugate 1/ph) make every entry a rational
   function, so that zero is decided exactly; masses, couplings and gauge parameters stay symbolic.  With the
   benchmark angles the square roots sqrt(1 - s^2) are not denested by Simplify (they are checked numerically below). *)
angPyRG$ = {s12 -> 8/17, s23 -> 7/25, s13 -> 3/5};
vPyRG$ = vStdRG$ /. angPyRG$ /. Exp[I dl] -> ph /. Exp[-I dl] -> 1/ph;
vPycRG$ = vStdRG$ /. angPyRG$ /. Exp[I dl] -> 1/ph /. Exp[-I dl] -> ph;
explicitRG$ = {cK[i_, j_] :> vPyRG$[[i, j]], cKc[i_, j_] :> vPycRG$[[i, j]]};
simpRG$[x_] := Simplify[Together[x /. explicitRG$ /. {CF -> 4/3, CA -> 3} /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2]],
   0 < sw < 1 && MW > 0];
diffD$ = Table[simpRG$[dA$[[i, j]] - betaYd$[[i, j]]], {i, 3}, {j, 3}];
diffU$ = Table[simpRG$[dYuDag$[[i, j]] - betaYuDag$[[i, j]]], {i, 3}, {j, 3}];
Print["(d) exact, rational unitary V: K dY_d - K (Delta/2) beta_{Y_d} of Eq. (betaY), 9 entries (expect all 0): ", Union[Flatten[diffD$]]];
Print["(d) exact, rational unitary V: K dY_u^dagger - K (Delta/2) beta_{Y_u}^dagger, 9 entries (expect all 0): ", Union[Flatten[diffU$]]];
xiFreeRG$ = FreeQ[Table[simpRG$[{dA$[[i, j]], dYuDag$[[i, j]]}], {i, 3}, {j, 3}], xiA | xiZ | xiW | xiG];
Print["(d) dY_d, dY_u^dagger free of the gauge parameters after unitarity (expect True): ", xiFreeRG$];
(* without the off-diagonal parts of the field renormalizations the counterterms do not match Eq. (betaY) *)
offDrop$[m_] := Table[If[i == j, m[[i, j]], 0], {i, 3}, {j, 3}];
dAnoOff$ = cRRG$ - 1/2 (herm$[offDrop$[dZuL$]] . aM$ + aM$ . offDrop$[dZdR$] + dZGRG$ aM$);
Print["(d) control: dY_d with only the diagonal field renormalizations, entries that differ from Eq. (betaY) (expect > 0): ",
  Count[Flatten[Table[simpRG$[dAnoOff$[[i, j]] - betaYd$[[i, j]]], {i, 3}, {j, 3}]], x_ /; x =!= 0]];
(* the benchmark V of Eq. (bench), 50 digits, with the benchmark masses and couplings and two sets of gauge parameters *)
vNumRG$ = N[vStdRG$ /. {s12 -> 22501/100000, s23 -> 4183/100000, s13 -> 3732/1000000, dl -> 1147/1000}, 50];
benchRG$ = {ee -> Sqrt[4 Pi/128], sw -> Sqrt[1881/8281], cw -> 80/91, MW -> 80, MZ -> 91, MH -> 125, MT -> 165,
   MB -> 286/100, MC -> 619/1000, MS -> 546/10000, MD -> 271/100000, MU -> 127/100000, MTA -> 1746/1000,
   MMU -> 1027/10000, Me -> 487/1000000, gS -> Sqrt[4 Pi 118/1000], CF -> 4/3, CA -> 3};
numRG$[x_, xis_] := N[x /. {cK[i_, j_] :> vNumRG$[[i, j]], cKc[i_, j_] :> Conjugate[vNumRG$[[i, j]]]} /. benchRG$ /. xis, 50];
devRG$ = Max[Table[Max[Abs[Flatten[{numRG$[dA$ - betaYd$, xis], numRG$[dYuDag$ - betaYuDag$, xis]}]]]/
     Max[Abs[Flatten[{numRG$[betaYd$, xis], numRG$[betaYuDag$, xis]}]]],
    {xis, {{xiA -> 1/2, xiZ -> 2, xiW -> 3, xiG -> 5}, {xiA -> 7, xiZ -> 1/3, xiW -> 4/5, xiG -> 0}}}]];
Print["(d) benchmark V (50 digits), two sets of gauge parameters: max |dY - (Delta/2) beta_Y| / max |entry| = ", N[devRG$, 3],
  "  (expect < 1e-40)"];

Put[{"cR" -> cRRG$, "cL" -> cLRG$, "dZG" -> dZGRG$}, FileNameJoin[{resDirRG$, "rg_ckm_vertex.m"}]];
Print["Summary (expect {0}, {0}, True, < 1e-40): ", Union[Flatten[diffD$]], ", ", Union[Flatten[diffU$]], ", ", xiFreeRG$, ", ", N[devRG$, 3]];
