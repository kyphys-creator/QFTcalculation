(* ::Package:: *)

(* ::Title:: *)
(*Step (6) of the CKM note: the semileptonic four-fermion amplitudes d_j -> u_i e nubar_e and muon decay at zero momentum (FeynArts + FeynCalc)*)


(* ::Text:: *)
(*Research note models/sm_ckm, step (6).  As the SM note's step (6) (models/sm/Src/mudecay_feyncalc.wl), with the*)
(*FeynArts model of this note (photon mass MA, general xiA, xiZ, xiW, the gluon left out):*)
(*  - d_j(p1) -> u_i(p2) e-(p3) nubar_e(p4) for the six channels i = u, c, j = d, s, b, and mu -> nu_mu e nubar_e;*)
(*  - all external momenta zero, the external fermions massless, and the light quarks massless everywhere (the*)
(*    zero-momentum matching: an internal line of an external flavour must have the external mass; only the top keeps*)
(*    its mass);*)
(*  - the tree, the 1PI vertex corrections and the boxes, the two Dirac chains [ubar_i ... d_j] ([nubar_mu ... mu]) and*)
(*    [ebar ... nu_e] projected on the tree structure with traces (vertices in D dimensions, the UV-finite boxes in 4);*)
(*  - the left-handed self-energies Sigma^L(0) of the massless mu and nu_mu (the quark ones come from step (3) in*)
(*    sl_ckm_check.wl).*)
(*Checks here: the diagram counts; every semileptonic vertex and box part is V_ij times one function, the same for the*)
(*six channels (no internal top: the internal fermions of the vertices and boxes are the external flavours).*)
(*Writes results/sl_ckm_amp.m: K dV, K dB per V_ij (semileptonic) and for muon decay, K Sigma^L_mu(0), K Sigma^L_numu(0),*)
(*in A0(m^2), B0(0, a, b), DB0(0, a, b) and D.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file sl_ckm_feyncalc.wl  (about 10 minutes; then sl_ckm_check.wl).*)
(*Interactive:  ~/hep/bin/wopen sl_ckm_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirSL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirSL$ = FileNameJoin[{srcDirSL$, "results"}];
modelTmpDirSL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirSL$, "generated", "SM_CKM_FA"}], FileNameJoin[{modelTmpDirSL$, "SM_CKM_FA"}]];
modFileSL$ = FileNameJoin[{modelTmpDirSL$, "SM_CKM_FA", "SM_CKM_FA.mod"}];
modTextSL$ = StringReplace[Import[modFileSL$, "Text"], {
    RegularExpression["(?s)(V\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA",
    RegularExpression["(?s)(U\\[1\\] == \\{.*?)Mass -> 0"] -> "$1Mass -> MA"}];
Export[modFileSL$, modTextSL$, "Text"];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirSL$, "SM_CKM_FA"}], Quiet -> True];
modelFileSL$ = FileNameJoin[{modelTmpDirSL$, "SM_CKM_FA", "SM_CKM_FA"}];

massSL$ = {FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH, FCGV["MT"] -> MT, FCGV["MB"] -> MB,
   FCGV["MC"] -> MC, FCGV["MS"] -> MS, FCGV["MD"] -> MD, FCGV["MU"] -> MU, FCGV["MTA"] -> MTA,
   FCGV["MMU"] -> MMU, FCGV["Me"] -> Me, FCGV["MA"] -> MA};
lepMSL$ = {Me, MMU, MTA}; upMSL$ = {MU, MC, MT}; dnMSL$ = {MD, MS, MB};
yukSL$ = {yl[i_Integer, j_Integer] :> If[i == j, Sqrt[2] lepMSL$[[i]]/vev, 0],
   yu[i_Integer, j_Integer] :> If[i == j, Sqrt[2] upMSL$[[i]]/vev, 0],
   yd[i_Integer, j_Integer] :> If[i == j, Sqrt[2] dnMSL$[[i]]/vev, 0]};
(* massless external fermions and light quarks; the top and the tau keep their masses *)
light0SL$ = {Me -> 0, MMU -> 0, MU -> 0, MC -> 0, MD -> 0, MS -> 0, MB -> 0};
ckmSL$ = {Conjugate[CKM[i_Integer, j_Integer]] :> cKc[i, j], CKM[i_Integer, j_Integer] :> cK[i, j]};
convSL$ = Join[{FCGV["EL"] -> ee, SMP["e"] -> ee, FCGV["GS"] -> gS, SMP["g_s"] -> gS, FCGV["G"] -> gS,
    GaugeXi[A] -> xiA, GaugeXi[Z] -> xiZ, GaugeXi[W] -> xiW, GaugeXi[G] -> xiG,
    GaugeXi[V[1, ___]] -> xiA, GaugeXi[V[2, ___]] -> xiZ, GaugeXi[V[3, ___]] -> xiW, GaugeXi[V[4, ___]] -> xiG,
    GaugeXi[S[2, ___]] -> xiZ, GaugeXi[S[3, ___]] -> xiW, GaugeXi[U[1, ___]] -> xiA, GaugeXi[U[2, ___]] -> xiZ,
    GaugeXi[U[3, ___]] -> xiW, GaugeXi[U[4, ___]] -> xiW, GaugeXi[U[5, ___]] -> xiG, GaugeXi[S[1, ___]] -> 1},
   massSL$];
sumOverSL$[x_] := x /. SumOver[i_, n_, ___] :> If[FreeQ[x /. SumOver[__] -> 1, i], n, 1];
insertSL$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelFileSL$,
    GenericModel -> modelFileSL$, ExcludeParticles -> {V[4]}], RuleDelayed::rhs];
convertSL$[fa_, in_, out_] := Module[{a},
   a = Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q},
       LorentzIndexNames -> {mu, nu}, ChangeDimension -> D, List -> True, SMP -> False, UndoChiralSplittings -> True,
       DropSumOver -> False, DropIndexSum -> False], RuleDelayed::rhs];
   a = a /. IndexSum[x_, {g_, i0_, i1_}] :> Sum[x, {g, i0, i1}];
   a = (sumOverSL$ /@ a) /. convSL$ /. yukSL$ /. ckmSL$ /. {lam -> MH^2/(2 vev^2)} /. vev -> 2 MW sw/ee /. light0SL$ /.
     FeynAmpDenominator[PropagatorDenominator[0 | Momentum[0, ___], m_]] :> -1/m^2;
   If[! FreeQ[a, CKM | IndexSum], Print["   WARNING: CKM or IndexSum left"]];
   (* chirality projectors as (1 -+ gamma5)/2 (SM note) *)
   a /. {DiracGamma[6] -> 1/2 + DiracGamma[5]/2, DiracGamma[7] -> 1/2 - DiracGamma[5]/2}];
KK = (4 Pi)^2;
reduceSL$[x_] := Module[{r},
   r = FDS[x, q];
   r = TID[DiracSimplify[SUNSimplify[r]], q, ToPaVe -> True];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2]};
   Simplify[r /. {B0[0, 0, 0] -> 0, A0[0] -> 0}]];


(* ::Section:: *)
(*Amplitudes at zero external momentum*)


(* spinors keep their own momentum symbols, the momenta in the integrands are set to zero (SM note) *)
spinRenameSL$ = {Spinor[Momentum[p_, d___], r___] :> Spinor[Momentum[sp[p], d], r],
   Spinor[-Momentum[p_, d___], r___] :> Spinor[-Momentum[sp[p], d], r]};
zeroMomSL$[x_] := FCReplaceMomenta[x /. spinRenameSL$, {p1 -> 0, p2 -> 0, p3 -> 0, p4 -> 0}] /.
   FeynAmpDenominator[PropagatorDenominator[0 | Momentum[0, ___], m_]] :> -1/m^2;
ampSL$[tops_, proc_] := Module[{d = insertSL$[tops, proc], a},
   (* the colour delta of the external quarks is common to the tree and the loops (no gluon) *)
   a = convertSL$[CreateFeynAmp[d, GaugeRules -> {}], {p1}, {p2, p3, p4}] /. SUNFDelta[__] -> 1;
   Select[zeroMomSL$ /@ a, Simplify[DiracSimplify[#]] =!= 0 &]];
topsTreeSL$ = CreateTopologies[0, 1 -> 3];
topsVertSL$ = CreateTopologies[1, 1 -> 3, ExcludeTopologies -> {Tadpoles, WFCorrections, SelfEnergies, Boxes}];
topsBoxSL$ = CreateTopologies[1, 1 -> 3, ExcludeTopologies -> {Tadpoles, WFCorrections, SelfEnergies, Triangles}];

(* Dirac chains [fbar(p2) ... f(p1)] and [ebar(p3) ... nu(p4)], projected on the tree structure with gamma_beta *)
chainRuleSL$ = {Dot[Spinor[Momentum[sp[p2], ___], ___], x___, Spinor[Momentum[sp[p1], ___], ___]] :> chA[Dot[x]],
   Dot[Spinor[Momentum[sp[p3], ___], ___], y___, Spinor[-Momentum[sp[p4], ___], ___]] :> chB[Dot[y]]};
projChainsSL$[x_, dim_] := Module[{y = Expand[x /. chainRuleSL$], tr, gb},
   gb = If[dim === 4, GA[bb$], GAD[bb$]];
   tr[z_] := DiracTrace[ChangeDimension[DiracSimplify[FCI[z]], dim], DiracTraceEvaluate -> True];
   (* contract twice: an Eps^2 from the two traces is not contracted in one call (environment Table 11) *)
   y = Contract[Contract[y /. chA[a_] chB[b_] :> tr[a . gb] tr[b . gb]]];
   If[! FreeQ[y, LorentzIndex], Print["   uncontracted Lorentz indices left"]];
   If[! FreeQ[y, chA | chB | Spinor], Print["   unprojected chains left"]];
   y];
reduceZeroSL$[x_] := Module[{r = TID[DiracSimplify[x], q, ToPaVe -> True]},
   PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {0}, {m1_, m2_}] :> B0[0, m1, m2]}];
(* K dV, K dB of one process (relative to its tree), and the numbers of diagrams *)
fourFermionSL$[proc_] := Module[{tree, vert, box, pT, pV, pB},
   tree = ampSL$[topsTreeSL$, proc]; vert = ampSL$[topsVertSL$, proc]; box = ampSL$[topsBoxSL$, proc];
   pT = Simplify[projChainsSL$[Total[tree], D]];
   pV = Simplify[Total[projChainsSL$[reduceZeroSL$[FDS[#, q]], D] & /@ vert]];
   pB = Simplify[Total[projChainsSL$[ChangeDimension[reduceZeroSL$[FDS[#, q]], 4], 4] & /@ box]];
   <|"n" -> Length /@ {tree, vert, box}, "tree" -> pT, "dV" -> Simplify[KK pV/pT], "dB" -> Simplify[KK (pB/pT) /. D -> 4]|>];


(* ::Subsubsection:: *)
(*Inspect: the vertex and box diagrams of b -> c e nubar_e*)


If[$Notebooks, Show /@ Render[Paint[insertSL$[#, {F[4, {3}]} -> {F[3, {2}], F[2, {1}], -F[1, {1}]}], DisplayFunction -> Identity]] & /@
  {topsVertSL$, topsBoxSL$}]


(* ::Section:: *)
(*(a) The six semileptonic channels and muon decay*)


FCClearScalarProducts[];
t0SL$ = AbsoluteTime[];
chansSL$ = Flatten[Table[{i, j}, {i, 2}, {j, 3}], 1];
slSL$ = Association[Table[ch -> Module[{r = fourFermionSL$[{F[4, {ch[[2]]}]} -> {F[3, {ch[[1]]}], F[2, {1}], -F[1, {1}]}]},
      Print["   d_", ch[[2]], " -> u_", ch[[1]], " e nubar_e: diagrams (tree, vertex, box) ", r["n"], ";  ",
        Round[AbsoluteTime[] - t0SL$], " s"];
      r], {ch, chansSL$}]];
muSL$ = fourFermionSL$[{F[2, {2}]} -> {F[1, {2}], F[2, {1}], -F[1, {1}]}];
Print["   mu -> nu_mu e nubar_e: diagrams (tree, vertex, box) ", muSL$["n"], "   (SM note: 1, 8, 5)"];

(* the tree of d_j -> u_i e nubar_e is V_ij times the tree of muon decay (the same projected structure) *)
treeRatioSL$ = Table[Simplify[slSL$[ch]["tree"]/muSL$["tree"]], {ch, chansSL$}];
Print["(a) projected trees, semileptonic / muon decay (expect V_ij): ", treeRatioSL$];
(* every vertex and box part: V_ij is divided out by the tree; the same function for all six channels *)
univSL$ = {Union[Simplify /@ Table[slSL$[ch]["dV"], {ch, chansSL$}]], Union[Simplify /@ Table[slSL$[ch]["dB"], {ch, chansSL$}]]};
Print["(a) distinct K dV and K dB over the six channels (expect 1 each): ", Length /@ univSL$,
  ";  CKM symbols left in them (expect False): ", ! FreeQ[univSL$, cK | cKc]];


(* ::Section:: *)
(*(b) The lepton legs of muon decay*)


(* Sigma^L(p^2) of a massless lepton from its self-energy, then p^2 -> 0 with B0(p^2, a, b) = B0(0, a, b) + p^2 DB0(0, a, b) *)
sigmaL0SL$[fld_] := Module[{d, a, ext, r},
   d = insertSL$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {fld} -> {fld}];
   a = convertSL$[CreateFeynAmp[d, Truncated -> True, GaugeRules -> {}], {k}, {k}];
   ext[x_] := Module[{y = DiracSimplify[FCI[x]]},
     (DiracTrace[DiracSimplify[GSD[k] . y], DiracTraceEvaluate -> True] -
       DiracTrace[DiracSimplify[GA5 . GSD[k] . y], DiracTraceEvaluate -> True])/(4 SPD[k, k])];
   r = Total[reduceSL$[ext[#]] & /@ a] /. {SPD[k, k] -> pp2, Pair[Momentum[k, D], Momentum[k, D]] -> pp2};
   r = r /. B0[pp_, m1_, m2_] :> (B0[0, m1, m2] + (pp /. {SPD[k, k] -> pp2}) DB0[0, m1, m2]);
   Simplify[KK Normal[Series[r, {pp2, 0, 0}]]]];
sLmuSL$ = sigmaL0SL$[F[2, {2}]];
sLnmSL$ = sigmaL0SL$[F[1, {2}]];
Print["(b) K Sigma^L(0) of mu and nu_mu computed;  ", Round[AbsoluteTime[] - t0SL$], " s"];


(* ::Section:: *)
(*Output*)


Put[{"dVsl" -> univSL$[[1, 1]], "dBsl" -> univSL$[[2, 1]], "dVmu" -> muSL$["dV"], "dBmu" -> muSL$["dB"],
   "sLmu" -> sLmuSL$, "sLnumu" -> sLnmSL$}, FileNameJoin[{resDirSL$, "sl_ckm_amp.m"}]];
Print["Summary (expect V_ij for each channel; {1, 1}; False): ", Union[Table[treeRatioSL$[[n]] === cK @@ chansSL$[[n]], {n, 6}]],
  "; ", Length /@ univSL$, "; ", ! FreeQ[univSL$, cK | cKc], ";  total ", Round[AbsoluteTime[] - t0SL$], " s"];
