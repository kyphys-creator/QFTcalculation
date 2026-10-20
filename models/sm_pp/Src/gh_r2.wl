(* ::Package:: *)

(* ::Title:: *)
(*Step (2f): the R2 vertex and the UV counterterm of the g g H vertex of the heavy-top effective theory (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm_pp, step (2f).  NLOCT leaves unevaluated integrals in the R2 and UV vertices of the operator, so they are*)
(*derived here for the note's own NLO UFO (gh_nlo_ufo.wl).  The amputated one-loop vertex G(k1, mu, a) G(k2, nu, b) -> H with off-shell*)
(*gluons (the Higgs note's FeynArts model SM_CKM_HEFT_FA, gluon loops, Feynman gauge; ghosts do not couple to the 1PI vertex at one*)
(*loop, the tadpole with the H G G G G vertex is scaleless) in the 't Hooft-Veltman scheme (external indices and momenta 4-dimensional,*)
(*the loop D-dimensional, as MadLoop's lambda_HV = 1).  OPP reconstructs the loop with a 4-dimensional numerator N(q); the rest is R2:*)
(*  R2 = i [M(numerator in D dimensions) - M(numerator in 4 dimensions)],  qbar = q + qtilde, qbar^2 = q^2 + qtilde^2:*)
(*  (1) the D of the numerator algebra (g^a_a = D) against 4: (D - 4) x the UV pole of the reduced integrals (B0 -> 1/eps, C0 finite);*)
(*  (2) qbar^2 -> q^2 = qbar^2 - qtilde^2: int qtilde^2 Y = (D - 4) [coefficient of g^{al be} in int q^al q^be Y], and for qtilde^4 the*)
(*      symmetric g g coefficient times (D - 4)(D - 2).*)
(*The vertex Feynman rule is i M (FeynArts' prefactor -i(2 pi)^-4 makes the amplitude M): checked on the tree vertex,*)
(*  i (cHgg/v) delta^ab [k1.k2 g^{mu nu} - k2^mu k1^nu].*)
(*The UV counterterm: cHgg ~ alpha_s, the MS-bar 2 delta g_s/g_s = delta alpha_s/alpha_s = -beta0 (g_s^2/(16 pi^2))/eps (beta0 = 11 - 2 n_f/3,*)
(*n_f = 5), times the tree vertex; the on-shell field constants of massless gluons are 0.  Against HC_NLO_X0 (a reference):*)
(*  R2 = i gHgg G^2/(128 pi^2) [-17 k1^2 g - 93 k1.k2 g - 17 k2^2 g + 14 k1^mu k1^nu + k1^mu k2^nu + 89 k2^mu k1^nu + 14 k2^mu k2^nu].*)
(*Writes results/gh_r2.csv and generated/QCDH_H_CT.m (the two vertices for gh_nlo_ufo.wl).  Batch:  wolframscript -file gh_r2.wl  (about 40 seconds)*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
srcDirR2$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirR2$ = FileNameJoin[{srcDirR2$, "results"}];
Quiet[CreateDirectory[resDirR2$]];
modelTmpR2$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirR2$, "..", "..", "sm_higgs", "Src", "generated", "SM_CKM_HEFT_FA"}], FileNameJoin[{modelTmpR2$, "SM_CKM_HEFT_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpR2$, "SM_CKM_HEFT_FA"}], Quiet -> True];
modelR2$ = FileNameJoin[{modelTmpR2$, "SM_CKM_HEFT_FA", "SM_CKM_HEFT_FA"}];
exclR2$ = {V[1], V[2], V[3], S[2], S[3], U[1], U[2], U[3], U[4], F[1], F[2], F[3, {3}]};
convR2$ = {FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS, FCGV["EL"] -> ee, FCGV["MH"] -> MH, FCGV["MW"] -> MW, FCGV["MZ"] -> MZ,
   GaugeXi[V[4, ___]] -> 1, GaugeXi[U[5, ___]] -> 1, GaugeXi[G] -> 1, MU -> 0, MD -> 0, MS -> 0, MC -> 0, MB -> 0,
   FCGV["MU"] -> 0, FCGV["MD"] -> 0, FCGV["MS"] -> 0, FCGV["MC"] -> 0, FCGV["MB"] -> 0};
yukR2$ = {yl[__] -> 0, yu[__] -> 0, yd[__] -> 0};
ampR2$[loops_] := Module[{d, a},
   d = Quiet[InsertFields[CreateTopologies[loops, 2 -> 1, ExcludeTopologies -> {Tadpoles, WFCorrections}], {V[4], V[4]} -> {S[1]},
       InsertionLevel -> {Particles}, Model -> modelR2$, GenericModel -> modelR2$, ExcludeParticles -> exclR2$], RuleDelayed::rhs];
   a = Quiet[FCFAConvert[CreateFeynAmp[d, Truncated -> True, GaugeRules -> {}] /. M$FACouplings, IncomingMomenta -> {k1, k2},
       OutgoingMomenta -> {qh}, LoopMomenta -> {l}, LorentzIndexNames -> {mu, nu}, SUNIndexNames -> {a1, a2}, ChangeDimension -> D,
       List -> True, SMP -> False, DropSumOver -> True], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}] /. convR2$ /. yukR2$ /. vev -> vv;
   a = FCReplaceMomenta[#, {qh -> k1 + k2}] & /@ a;
   DeleteCases[Expand[#] /. cHgg^n_ /; n > 1 -> 0 & /@ a, 0]];
colR2$[x_] := SUNSimplify[x, SUNNToCACF -> True] /. {CA -> 3, CF -> 4/3};
FCClearScalarProducts[];
(* the 4-dimensional tensor basis of the vertex: g^{mu nu}, k_i^mu k_j^nu *)
basisR2$ = {MT[mu, nu] SP[k1, k1], MT[mu, nu] SP[k1, k2], MT[mu, nu] SP[k2, k2], FV[k1, mu] FV[k1, nu], FV[k1, mu] FV[k2, nu],
   FV[k2, mu] FV[k1, nu], FV[k2, mu] FV[k2, nu]};
coefR2$[x_] := Module[{y = Expand[ExpandScalarProduct[ChangeDimension[FCI[x], 4]] /. SUNDelta[__] -> 1]},
   Coefficient[y, #] & /@ (Expand[ExpandScalarProduct[#]] & /@ basisR2$)];


(* ::Section:: *)
(*(a) the tree vertex: the convention i M*)


treeR2$ = Total[ampR2$[0]];
vTree$ = Simplify[coefR2$[I colR2$[Contract[treeR2$]]]];
vTreeHand$ = I {0, cHgg/vv, 0, 0, 0, -cHgg/vv, 0};    (* i (cHgg/v)[k1.k2 g - k2^mu k1^nu] in the basis *)
Print["(a) tree vertex (i M) in the basis: ", vTree$, ";  minus i (cHgg/v)[k1.k2 g - k2^mu k1^nu] (expect 0): ", Simplify[vTree$ - vTreeHand$]];


(* ::Section:: *)
(*(b) the one-loop vertex: the numerator in D and in 4 dimensions*)


loopR2$ = ampR2$[1];
Print["(b) one-loop diagrams of the order cHgg g_s^2: ", Length[loopR2$]];
(* the numerator algebra: contract and the colour, then call its explicit D "Dn" (the integrals keep D) *)
numR2$ = Expand[colR2$[Contract[Total[loopR2$]]]];
numR2$ = numR2$ /. D -> Dn /. {Momentum[x_, Dn] :> Momentum[x, D], LorentzIndex[x_, Dn] :> LorentzIndex[x, D]};
Print["(b) explicit Dn in the numerator: ", !FreeQ[numR2$, Dn], ";  loop denominators: ", Union[Cases[numR2$, _FeynAmpDenominator, Infinity]] // Length];
l2$ = Pair[Momentum[l, D], Momentum[l, D]];
maxPow$ = Exponent[numR2$ /. l2$ -> l2s, l2s];
Print["(b) the highest power of l^2 in the numerator: ", maxPow$];
(* TID and PaVeReduce return the FCE form (MTD, FVD, SPD): the explicit D is then only the dimension of the algebra *)
redR2$[x_] := Module[{r = TID[x, l, ToPaVe -> True]}, r = FCE[PaVeReduce[r]]; r /. {A0[0] -> 0, B0[0, 0, 0] -> 0, PaVe[0, {0}, {0, 0}] -> 0}];
(* the UV pole of the scalar functions in FeynCalc's normalization (B0 = 1/eps + ..., C0 finite), D = 4 - 2 eps *)
uvPole$[x_] := x /. {B0[__] -> 1/eps, PaVe[0, {_}, {0, 0}] -> 1/eps, C0[__] -> 0, PaVe[0, {_, _, _}, {0, 0, 0}] -> 0};
rat$[x_] := ChangeDimension[FCI[Normal[Series[FCE[uvPole$[x]] /. D -> 4 - 2 eps, {eps, 0, 0}]]], 4];


(* ::Section:: *)
(*(c) R2*)


(* (1) Dn - 4 in the numerator *)
dN$ = Expand[(numR2$ - (numR2$ /. Dn -> 4)) /. Dn -> D];
r2a$ = rat$[redR2$[dN$]];
(* (2) l^2 -> l^2 - lt^2 in the 4-dimensional numerator: M_D - M_4 gets + sum_k N_k [(l^2)^k - (l^2 - lt^2)^k] *)
n4$ = numR2$ /. Dn -> 4;
nk$ = Table[Coefficient[Expand[n4$ /. l2$ -> l2s], l2s, k], {k, 0, maxPow$}];
(* int lt^2 Y = (D - 4) [g^{al be} coefficient of int l^al l^be Y];  int lt^4 Y = (D - 4)(D - 2) [g^{al be} g^{ga de} (sym) coefficient] *)
lt2Int$[y_] := Module[{t = redR2$[FVD[l, al] FVD[l, be] y], c},
   c = Coefficient[Expand[t], MTD[al, be]];
   (D - 4) c];
lt4Int$[y_] := Module[{t = redR2$[FVD[l, al] FVD[l, be] FVD[l, ga] FVD[l, de] y], c},
   c = Coefficient[Expand[t], MTD[al, be] MTD[ga, de]];
   (D - 4) (D - 2) c];
r2b$ = 0;
Do[Module[{nkk = nk$[[k + 1]]},
    If[nkk =!= 0,
     (* (l^2)^k - (l^2 - lt^2)^k = k (l^2)^(k-1) lt^2 - C(k,2) (l^2)^(k-2) lt^4 + ... *)
     r2b$ += rat$[lt2Int$[Expand[k nkk l2$^(k - 1)]]];
     If[k >= 2, r2b$ -= rat$[lt4Int$[Expand[Binomial[k, 2] nkk l2$^(k - 2)]]]];
     If[k >= 3, Print["   WARNING: (l^2)^", k, " needs lt^6 terms"]]]],
  {k, 1, maxPow$}];
(* the vertex: i (1/(16 pi^2)) ... is in the amplitude through FeynArts' prefactor and TID's i pi^2 *)
Print["(c) the D_n - 4 part: ", InputForm[Simplify[coefR2$[I r2a$]]], ";  the qtilde part: ", InputForm[Simplify[coefR2$[I r2b$]]]];
r2$ = Simplify[I (r2a$ + r2b$)];
r2c$ = Simplify[coefR2$[r2$]];
Print["(c) R2 (i M_D - i M_4) in the basis {g k1^2, g k1.k2, g k2^2, k1k1, k1^mu k2^nu, k2^mu k1^nu, k2k2}: ", InputForm[r2c$]];
(* HC_NLO_X0: i gHgg G^2/(128 pi^2) {-17, -93, -17, 14, 1, 89, 14}, gHgg = cHgg/v *)
hcR2$ = I cHgg/vv gS^2/(128 Pi^2) {-17, -93, -17, 14, 1, 89, 14};
dR2$ = Simplify[r2c$ - hcR2$];
Print["(c) own R2 minus HC_NLO_X0's (a reference; expect {0, ...}): ", dR2$];
Print["(c) own R2 over i (cHgg/v) g_s^2/(128 pi^2): ", Simplify[r2c$/(I cHgg/vv gS^2/(128 Pi^2))]];


(* ::Section:: *)
(*(d) the UV counterterm*)


beta0R2$ = 11 - 2/3 5;
uvR2$ = Simplify[vTree$ (-beta0R2$ gS^2/(16 Pi^2))];
Print["(d) UV counterterm (coefficient of 1/eps) in the basis: ", InputForm[uvR2$]];
(* HC_NLO_X0 with the note's pole patch: (i/2) gHgg G^2/(4 pi^2) (11 C_A/6 - 2 T_F n_f/3)/eps x [p2^mu p1^nu - p1.p2 g] (VVS2) *)
hcUV$ = (I/2) cHgg/vv gS^2/(4 Pi^2) (11 3/6 - 2 (1/2) 5/3) {0, -1, 0, 0, 0, 1, 0};
Print["(d) own UV minus HC_NLO_X0's patched one (expect 0): ", Simplify[uvR2$ - hcUV$]];
DeleteDirectory[modelTmpR2$, DeleteContents -> True];


(* ::Section:: *)
(*Export*)


(* the vertices (i M) in the basis, of cHgg (the operator's coefficient), vv (the vev) and gS; "uv" is the coefficient of 1/eps *)
Put[<|"tree" -> vTree$, "r2" -> r2c$, "uv" -> uvR2$, "basis" -> {"g k1^2", "g k1.k2", "g k2^2", "k1^mu k1^nu", "k1^mu k2^nu", "k2^mu k1^nu", "k2^mu k2^nu"}|>,
  FileNameJoin[{srcDirR2$, "generated", "QCDH_H_CT.m"}]];
chkR2$[x_] := If[AllTrue[Flatten[{x}], # === 0 &], "0", StringReplace[ToString[InputForm[x]], "," -> ";"]];
Export[FileNameJoin[{resDirR2$, "gh_r2.csv"}], StringRiffle[StringRiffle[#, ","] & /@ {
     {"quantity", "value"},
     {"check_tree_minus_hand", chkR2$[Simplify[vTree$ - vTreeHand$]]},
     {"R2_over_i_cHgg_v_gs2_128pi2", StringReplace[ToString[InputForm[Simplify[r2c$/(I cHgg/vv gS^2/(128 Pi^2))]]], "," -> ";"]},
     {"check_R2_minus_HC_NLO_X0", chkR2$[dR2$]},
     {"check_UV_minus_HC_NLO_X0_patched", chkR2$[Simplify[uvR2$ - hcUV$]]}}, "\n"] <> "\n", "Text"];
Print["written: results/gh_r2.csv, generated/QCDH_H_CT.m"];
