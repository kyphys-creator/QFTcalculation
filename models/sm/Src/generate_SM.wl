(* ::Package:: *)

(* ::Title:: *)
(*Step (1): FeynRules on SM.fr -> FeynArts model and UFO (Standard Model, Feynman gauge with Goldstones and ghosts)*)


(* ::Text:: *)
(*Usage*)
(*  terminal :  wolframscript -file generate_SM.wl      (from any directory)*)
(*  notebook :  Get["<path>/models/sm/Src/generate_SM.wl"]*)
(*              or open this file and evaluate it (Src/ is then taken from NotebookDirectory[])*)
(**)
(*Input*)
(*  Src/SM.fr            the FeynRules SM 1.4.7 (FeynRules 2.3.49, Models/SM), unchanged; FeynmanGauge = True*)
(*  Src/DiagonalCKM.rst  CKM = 1, loaded after the UFO is written (FeynArts model only).  With this restriction*)
(*                       WriteUFO issues Inner::incom and writes a UFO that MadGraph cannot use; the UFO is written*)
(*                       without restrictions, and MadGraph's card restrict_massless.dat sets cabi = 0 instead.*)
(*  (run_model_check.sh adds MadGraph's restriction card restrict_massless.dat: cabi = 0 and the masses and Yukawa*)
(*   couplings of e, mu, u, d, s, c set to 0, as in MadGraph's sm model.  FeynRules' restriction Massless.rst gives*)
(*   the same kind of broken UFO: KeyError GetIntOrder[yu[2]] in MadGraph)*)
(**)
(*Output (overwritten on each run)*)
(*  Src/generated/SM_FA/                 FeynArts model (SM_FA.mod, .gen, .pars), all fermion masses kept*)
(*  Src/generated/SM_UFO/                UFO for MadGraph, no restriction (all fermion masses, Cabibbo angle)*)
(*  Src/generated/FeynmanRules_SM.m      vertex list returned by FeynmanRules (93 vertex classes)*)
(**)
(*Expected results*)
(*  CheckHermiticity -> {},  CheckKineticTermNormalisation -> True,  93 vertex classes, each equal to the note's*)
(*  table of Feynman rules (Tables "rules-f" to "rules-gh"); all 93 differences 0.*)
(**)
(*Load FeynRules in a fresh kernel: do not mix it with FeynCalc in one session.  Global names below end in SM$*)
(*so that they cannot clash with model symbols (ee, sw, cw, vev, lam, gs, yl, yu, yd, CKM, A, Z, W, H, G0, GP, ...).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file generate_SM.wl  (in a fresh kernel: FeynRules must not share a kernel with FeynCalc or FeynArts).  Interactive:  ~/hep/bin/wopen generate_SM.wl  (in a fresh kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*locations*)


startDirSM$ = Directory[];
srcDirSM$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
outDirSM$ = FileNameJoin[{srcDirSM$, "generated"}];


(* ::Section:: *)
(*FeynRules*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];

SetDirectory[srcDirSM$];
LoadModel["SM.fr"];


(* ::Subsubsection:: *)
(*Inspect: the pieces of the Lagrangian*)


If[$Notebooks,
  {LGauge, LFermions, LHiggs, LYukawa, LGhost} // Short[#, 20] &
]


(* ::Section:: *)
(*checks*)


Print["Hermiticity (expect {}): ", CheckHermiticity[LSM]];
Print["Kinetic-term normalisation (expect True): ", CheckKineticTermNormalisation[LSM]];
Print["Mass spectrum: ", CheckMassSpectrum[LSM]];

verticesSM$ = FeynmanRules[LSM, ScreenOutput -> False];
Print["Number of vertex classes (expect 93): ", Length[verticesSM$]];


(* ::Text:: *)
(*Each vertex is compared with the note's table of Feynman rules.  FeynRules writes FV[i, mu] for the incoming*)
(*momentum of leg i, ME for the metric, Ga[mu, s1, s2] for gamma^mu and TensDot[Ga[mu], ProjM/ProjP][s1, s2] for*)
(*gamma^mu P_L / P_R; the expected expressions below use the same symbols.  Before comparing, gamma^mu is split as*)
(*gamma^mu (P_L + P_R), the Yukawa matrices are made diagonal and real (y[i, j] -> delta_ij y[i]), the dummy*)
(*generation index of the CKM sums is contracted, and momentum conservation removes the momentum of leg 3.*)


vtxSM$[fields_List] := Module[{v = Select[verticesSM$, (First /@ #[[1]]) === fields &]},
   If[Length[v] != 1, Missing["vertex", fields], v[[1, 2]]]];
lorSM$[i_] := Index[Lorentz, Ext[i]];
spiSM$[i_] := Index[Spin, Ext[i]];
genSM$[i_] := Index[Generation, Ext[i]];
colSM$[i_] := Index[Colour, Ext[i]];
gluSM$[i_] := Index[Gluon, Ext[i]];
gSM$[i_, j_] := ME[lorSM$[i], lorSM$[j]];
pSM$[i_, j_] := FV[i, lorSM$[j]];
dgSM$ := IndexDelta[genSM$[1], genSM$[2]];
dcSM$ := IndexDelta[colSM$[1], colSM$[2]];
gaSM$ := Ga[lorSM$[3], spiSM$[1], spiSM$[2]];
gaLSM$ := TensDot[Ga[lorSM$[3]], ProjM][spiSM$[1], spiSM$[2]];
gaRSM$ := TensDot[Ga[lorSM$[3]], ProjP][spiSM$[1], spiSM$[2]];
pLSM$ := ProjM[spiSM$[1], spiSM$[2]];
pRSM$ := ProjP[spiSM$[1], spiSM$[2]];

(* Lorentz structures of the gauge self-couplings (legs 1, 2, 3 or 1, ..., 4, all momenta incoming) *)
vvvSM$ := gSM$[1, 2] (pSM$[1, 3] - pSM$[2, 3]) + gSM$[2, 3] (pSM$[2, 1] - pSM$[3, 1]) + gSM$[3, 1] (pSM$[3, 2] - pSM$[1, 2]);
(* S[i,j;k,l] = 2 g_ij g_kl - g_ik g_jl - g_il g_jk *)
s4SM$[i_, j_, k_, l_] := 2 gSM$[i, j] gSM$[k, l] - gSM$[i, k] gSM$[j, l] - gSM$[i, l] gSM$[j, k];


(* ::Subsection:: *)
(*the note's table*)


(* fermions: {barred field, field, Q, T3, Yukawa symbol or None, coloured} *)
fermSM$ = {{lbar, l, -1, -1/2, yl, False}, {vlbar, vl, 0, 1/2, None, False},
   {uqbar, uq, 2/3, 1/2, yu, True}, {dqbar, dq, -1/3, -1/2, yd, True}};
colFacSM$[True] := dcSM$; colFacSM$[False] := 1;
(* diagonal real Yukawa couplings y_f = sqrt2 m_f / v, one per generation *)
ydiagSM$[y_][i_] := ToExpression[ToString[y] <> "diagSM$"][i];

expectSM$ = Association[];
(* gauge couplings of the fermions *)
Do[With[{fb = fd[[1]], fp = fd[[2]], q = fd[[3]], t3 = fd[[4]], cf = colFacSM$[fd[[6]]]},
   If[q =!= 0, expectSM$[{fb, fp, A}] = I ee q gaSM$ dgSM$ cf];
   expectSM$[{fb, fp, Z}] = I ee/(sw cw) ((t3 - q sw^2) gaLSM$ - q sw^2 gaRSM$) dgSM$ cf;
   If[fd[[6]], expectSM$[{fb, fp, G}] = I gs gaSM$ dgSM$ T[gluSM$[3], colSM$[1], colSM$[2]]]],
  {fd, fermSM$}];
expectSM$[{uqbar, dq, W}] = I ee/(Sqrt[2] sw) CKM[genSM$[1], genSM$[2]] gaLSM$ dcSM$;
expectSM$[{dqbar, uq, Wbar}] = I ee/(Sqrt[2] sw) Conjugate[CKM[genSM$[2], genSM$[1]]] gaLSM$ dcSM$;
expectSM$[{vlbar, l, W}] = I ee/(Sqrt[2] sw) gaLSM$ dgSM$;
expectSM$[{lbar, vl, Wbar}] = I ee/(Sqrt[2] sw) gaLSM$ dgSM$;
(* Yukawa couplings: H, G0 (-2 T3 times y_f/sqrt2 times gamma5 = P_R - P_L), G+- *)
Do[With[{fb = fd[[1]], fp = fd[[2]], t3 = fd[[4]], y = fd[[5]], cf = colFacSM$[fd[[6]]]},
   If[y =!= None,
    expectSM$[{fb, fp, H}] = -I/Sqrt[2] ydiagSM$[y][genSM$[1]] (pLSM$ + pRSM$) dgSM$ cf;
    expectSM$[{fb, fp, G0}] = -2 t3/Sqrt[2] ydiagSM$[y][genSM$[1]] (pRSM$ - pLSM$) dgSM$ cf]],
  {fd, fermSM$}];
expectSM$[{uqbar, dq, GP}] = CKM[genSM$[1], genSM$[2]] (yudiagSM$[genSM$[1]] pLSM$ - yddiagSM$[genSM$[2]] pRSM$) dcSM$;
expectSM$[{dqbar, uq, GPbar}] = Conjugate[CKM[genSM$[2], genSM$[1]]] (yddiagSM$[genSM$[1]] pLSM$ - yudiagSM$[genSM$[2]] pRSM$) dcSM$;
expectSM$[{vlbar, l, GP}] = -yldiagSM$[genSM$[1]] pRSM$ dgSM$;
expectSM$[{lbar, vl, GPbar}] = yldiagSM$[genSM$[1]] pLSM$ dgSM$;

(* scalar self-couplings, V = -mu^2 |Phi|^2 + lam |Phi|^4 *)
expectSM$[{H, H, H}] = -6 I lam vev;   expectSM$[{G0, G0, H}] = -2 I lam vev;   expectSM$[{GP, GPbar, H}] = -2 I lam vev;
expectSM$[{H, H, H, H}] = -6 I lam;    expectSM$[{G0, G0, G0, G0}] = -6 I lam;  expectSM$[{GP, GP, GPbar, GPbar}] = -4 I lam;
expectSM$[{G0, G0, H, H}] = -2 I lam;  expectSM$[{GP, GPbar, H, H}] = -2 I lam; expectSM$[{G0, G0, GP, GPbar}] = -2 I lam;

(* gauge self-couplings: V W+ W- with g_A = e, g_Z = e c/s; quartic couplings *)
expectSM$[{A, W, Wbar}] = -I ee vvvSM$;
expectSM$[{W, Wbar, Z}] = -I ee cw/sw vvvSM$;
expectSM$[{W, W, Wbar, Wbar}] = I ee^2/sw^2 s4SM$[1, 2, 3, 4];
expectSM$[{A, A, W, Wbar}] = -I ee^2 s4SM$[1, 2, 3, 4];
expectSM$[{W, Wbar, Z, Z}] = -I ee^2 cw^2/sw^2 s4SM$[3, 4, 1, 2];
expectSM$[{A, W, Wbar, Z}] = -I ee^2 cw/sw s4SM$[1, 4, 2, 3];
expectSM$[{G, G, G}] = gs f[gluSM$[1], gluSM$[2], gluSM$[3]] vvvSM$;
f4SM$[i_, j_, k_, l_] := f[gluSM$[i], gluSM$[j], eSM$] f[gluSM$[k], gluSM$[l], eSM$];
expectSM$[{G, G, G, G}] = -I gs^2 (
    f4SM$[1, 2, 3, 4] (gSM$[1, 3] gSM$[2, 4] - gSM$[1, 4] gSM$[2, 3]) +
    f4SM$[1, 3, 2, 4] (gSM$[1, 2] gSM$[3, 4] - gSM$[1, 4] gSM$[2, 3]) +
    f4SM$[1, 4, 2, 3] (gSM$[1, 2] gSM$[3, 4] - gSM$[1, 3] gSM$[2, 4]));

(* gauge bosons and scalars: M_W = e v/(2 s), M_Z = M_W/c *)
expectSM$[{H, W, Wbar}] = I ee^2 vev/(2 sw^2) gSM$[2, 3];
expectSM$[{H, Z, Z}] = I ee^2 vev/(2 sw^2 cw^2) gSM$[2, 3];
expectSM$[{H, H, W, Wbar}] = I ee^2/(2 sw^2) gSM$[3, 4];
expectSM$[{G0, G0, W, Wbar}] = I ee^2/(2 sw^2) gSM$[3, 4];
expectSM$[{GP, GPbar, W, Wbar}] = I ee^2/(2 sw^2) gSM$[3, 4];
expectSM$[{H, H, Z, Z}] = I ee^2/(2 sw^2 cw^2) gSM$[3, 4];
expectSM$[{G0, G0, Z, Z}] = I ee^2/(2 sw^2 cw^2) gSM$[3, 4];
expectSM$[{GP, GPbar, Z, Z}] = I ee^2 (cw^2 - sw^2)^2/(2 sw^2 cw^2) gSM$[3, 4];
expectSM$[{A, A, GP, GPbar}] = 2 I ee^2 gSM$[1, 2];
expectSM$[{A, GP, GPbar, Z}] = I ee^2 (cw^2 - sw^2)/(sw cw) gSM$[1, 4];
expectSM$[{A, GP, GPbar}] = I ee (pSM$[2, 1] - pSM$[3, 1]);
expectSM$[{GP, GPbar, Z}] = I ee (cw^2 - sw^2)/(2 sw cw) (pSM$[1, 3] - pSM$[2, 3]);
expectSM$[{G0, H, Z}] = ee/(2 sw cw) (pSM$[1, 3] - pSM$[2, 3]);
expectSM$[{GPbar, H, W}] = ee/(2 sw) (pSM$[1, 3] - pSM$[2, 3]);
expectSM$[{GP, H, Wbar}] = ee/(2 sw) (pSM$[1, 3] - pSM$[2, 3]);
expectSM$[{G0, GPbar, W}] = -I ee/(2 sw) (pSM$[1, 3] - pSM$[2, 3]);
expectSM$[{G0, GP, Wbar}] = I ee/(2 sw) (pSM$[1, 3] - pSM$[2, 3]);
expectSM$[{A, GPbar, W}] = -ee^2 vev/(2 sw) gSM$[1, 3];
expectSM$[{A, GP, Wbar}] = ee^2 vev/(2 sw) gSM$[1, 3];
expectSM$[{GPbar, W, Z}] = ee^2 vev/(2 cw) gSM$[2, 3];
expectSM$[{GP, Wbar, Z}] = -ee^2 vev/(2 cw) gSM$[2, 3];
expectSM$[{A, G0, GPbar, W}] = -I ee^2/(2 sw) gSM$[1, 4];
expectSM$[{A, G0, GP, Wbar}] = -I ee^2/(2 sw) gSM$[1, 4];
expectSM$[{A, GPbar, H, W}] = -ee^2/(2 sw) gSM$[1, 4];
expectSM$[{A, GP, H, Wbar}] = ee^2/(2 sw) gSM$[1, 4];
expectSM$[{G0, GPbar, W, Z}] = I ee^2/(2 cw) gSM$[3, 4];
expectSM$[{G0, GP, Wbar, Z}] = I ee^2/(2 cw) gSM$[3, 4];
expectSM$[{GPbar, H, W, Z}] = ee^2/(2 cw) gSM$[3, 4];
expectSM$[{GP, H, Wbar, Z}] = -ee^2/(2 cw) gSM$[3, 4];

(* ghosts and gauge bosons: coefficient times the incoming momentum p1 of the antighost leg *)
ghvSM$ = {
   {ghAbar, ghWm, W, -I ee}, {ghAbar, ghWp, Wbar, I ee},
   {ghWmbar, ghA, Wbar, -I ee}, {ghWmbar, ghWm, A, I ee}, {ghWmbar, ghWm, Z, I ee cw/sw}, {ghWmbar, ghZ, Wbar, -I ee cw/sw},
   {ghWpbar, ghA, W, I ee}, {ghWpbar, ghWp, A, -I ee}, {ghWpbar, ghWp, Z, -I ee cw/sw}, {ghWpbar, ghZ, W, I ee cw/sw},
   {ghZbar, ghWm, W, -I ee cw/sw}, {ghZbar, ghWp, Wbar, I ee cw/sw}};
Do[expectSM$[gv[[1 ;; 3]]] = gv[[4]] pSM$[1, 3], {gv, ghvSM$}];
expectSM$[{ghGbar, ghG, G}] = -gs f[gluSM$[1], gluSM$[2], gluSM$[3]] pSM$[1, 3];
(* ghosts and scalars (Feynman gauge; in R_xi each is multiplied by the xi of the antighost), M_W = ee vev/(2 sw) *)
mwSM$ = ee vev/(2 sw);
ghsSM$ = {
   {ghWmbar, ghA, GPbar, ee mwSM$}, {ghWpbar, ghA, GP, -ee mwSM$},
   {ghWmbar, ghWm, G0, -ee/(2 sw) mwSM$}, {ghWpbar, ghWp, G0, ee/(2 sw) mwSM$},
   {ghWmbar, ghWm, H, -I ee/(2 sw) mwSM$}, {ghWpbar, ghWp, H, -I ee/(2 sw) mwSM$},
   {ghWmbar, ghZ, GPbar, ee (cw^2 - sw^2)/(2 sw cw) mwSM$}, {ghWpbar, ghZ, GP, -ee (cw^2 - sw^2)/(2 sw cw) mwSM$},
   {ghZbar, ghWm, GP, ee/(2 sw cw) mwSM$}, {ghZbar, ghWp, GPbar, -ee/(2 sw cw) mwSM$},
   {ghZbar, ghZ, H, -I ee/(2 sw cw^2) mwSM$}};
Do[expectSM$[gs3[[1 ;; 3]]] = gs3[[4]], {gs3, ghsSM$}];

Print["Vertex classes in the note's table (expect 93): ", Length[expectSM$]];


(* ::Subsection:: *)
(*comparison*)


(* momentum conservation p1 + p2 + p3 = 0 for the three-point vertices *)
momConsSM$ = {FV[3, mu_] :> -FV[1, mu] - FV[2, mu]};
(* f is totally antisymmetric: canonical order *)
fCanonSM$ = f[x__] :> Signature[{x}] (f @@ Sort[{x}]) /; !OrderedQ[{x}];
(* Dirac structures in inert symbols, because FeynRules evaluates ProjP - ProjM to Ga[5]:
   gamma5 = P_R - P_L, 1 = P_R + P_L, gamma^mu = gamma^mu P_L + gamma^mu P_R *)
splitGaSM$ = {Ga[5, s1_, s2_] :> pRinSM$[s1, s2] - pLinSM$[s1, s2],
   ProjP[s1_, s2_] :> pRinSM$[s1, s2], ProjM[s1_, s2_] :> pLinSM$[s1, s2],
   IndexDelta[s1 : Index[Spin, _], s2 : Index[Spin, _]] :> pRinSM$[s1, s2] + pLinSM$[s1, s2],
   TensDot[Ga[mu_], ProjM][s1_, s2_] :> gLinSM$[mu, s1, s2], TensDot[Ga[mu_], ProjP][s1_, s2_] :> gRinSM$[mu, s1, s2],
   Ga[mu_, s1_, s2_] :> gLinSM$[mu, s1, s2] + gRinSM$[mu, s1, s2]};
(* diagonal, real Yukawa matrices (the conjugated ones first).  Generation deltas become the inert dgenSM$:
   FeynRules' own IndexDelta rules contract external generation indices when they meet other factors. *)
genDeltaSM$ = IndexDelta[i : Index[Generation, _], j : Index[Generation, _]] :> dgenSM$[i, j];
yukSM$ = {Conjugate[yl[i_, j_]] :> dgenSM$[i, j] yldiagSM$[i], Conjugate[yu[i_, j_]] :> dgenSM$[i, j] yudiagSM$[i],
   Conjugate[yd[i_, j_]] :> dgenSM$[i, j] yddiagSM$[i],
   yl[i_, j_] :> dgenSM$[i, j] yldiagSM$[i], yu[i_, j_] :> dgenSM$[i, j] yudiagSM$[i],
   yd[i_, j_] :> dgenSM$[i, j] yddiagSM$[i]};
(* contract the dummy generation index of the CKM sums: one Kronecker delta per term *)
dummyGenSM$ = Index[Generation, Generation$1];
contractSM$[term_] := Module[{d = Cases[term, dgenSM$[dummyGenSM$, j_] | dgenSM$[j_, dummyGenSM$], {0, Infinity}]},
   If[d === {}, term,
    term /. d[[1]] -> 1 /. dummyGenSM$ -> First[DeleteCases[List @@ d[[1]], dummyGenSM$]]]];
normSM$[x_] := Module[{y = Expand[x /. genDeltaSM$ /. splitGaSM$ /. yukSM$ /. momConsSM$]},
   y = If[Head[y] === Plus, Plus @@ (contractSM$ /@ List @@ y), contractSM$[y]];
   Expand[y /. Index[Gluon, Gluon$1] -> eSM$ /. fCanonSM$ //. deltaSM$]];
(* inert generation deltas: symmetric, idempotent, and a diagonal Yukawa coupling takes the first index of its delta;
   pattern names end in SM$ because plain a, b, ... are model symbols (b is the bottom quark) *)
deltaSM$ = {dgenSM$[iSM$_, iSM$_] :> 1, dgenSM$[iSM$_, jSM$_] :> dgenSM$[jSM$, iSM$] /; !OrderedQ[{iSM$, jSM$}],
   dgenSM$[iSM$_, jSM$_]^nSM$_ :> dgenSM$[iSM$, jSM$],
   dgenSM$[iSM$_, jSM$_] (ySM$ : yldiagSM$ | yudiagSM$ | yddiagSM$)[jSM$_] :> dgenSM$[iSM$, jSM$] ySM$[iSM$]};
(* c_W^2 + s_W^2 = 1 is used: cw -> Sqrt[1 - sw^2] *)
diffSM$[fields_] := Simplify[normSM$[vtxSM$[fields]] - normSM$[expectSM$[fields]] /. cw -> Sqrt[1 - sw^2]];

fieldListsSM$ = (First /@ #[[1]]) & /@ verticesSM$;
missingSM$ = Complement[fieldListsSM$, Keys[expectSM$]];
extraSM$ = Complement[Keys[expectSM$], fieldListsSM$];
Print["FeynRules vertex classes not in the note (expect {}): ", missingSM$];
Print["note's vertex classes not produced by FeynRules (expect {}): ", extraSM$];
resultsSM$ = AssociationMap[diffSM$, Intersection[fieldListsSM$, Keys[expectSM$]]];
badSM$ = Select[resultsSM$, # =!= 0 &];
Print["Vertex classes compared: ", Length[resultsSM$], ";  nonzero differences (expect none): ", Length[badSM$]];
If[Length[badSM$] > 0, Print[InputForm[badSM$]]];

(* the counts per family, as in the note *)
familySM$[fl_] := Which[
   MemberQ[fl, ghAbar | ghZbar | ghWpbar | ghWmbar | ghGbar] && MemberQ[fl, H | G0 | GP | GPbar], "ghost-scalar",
   MemberQ[fl, ghAbar | ghZbar | ghWpbar | ghWmbar | ghGbar], "ghost-gauge",
   MemberQ[fl, lbar | vlbar | uqbar | dqbar], "fermion",
   SubsetQ[{H, G0, GP, GPbar}, fl], "scalar",
   SubsetQ[{A, Z, W, Wbar, G}, fl], "gauge",
   True, "gauge-scalar"];
Print["Vertex classes per family (expect fermion 23, scalar 9, gauge 8, gauge-scalar 29, ghost-gauge 13, ghost-scalar 11): ",
  Counts[familySM$ /@ fieldListsSM$]];


(* ::Subsubsection:: *)
(*Inspect: the Feynman rules*)


If[$Notebooks,
  TableForm[verticesSM$ /. {v_List, c_} :> {First /@ v, TraditionalForm[c]}]
]


(* ::Section:: *)
(*write outputs*)


Quiet[CreateDirectory[outDirSM$]];
SetDirectory[outDirSM$];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"SM_FA", "SM_UFO"}];

Put[verticesSM$, "FeynmanRules_SM.m"];
WriteUFO[LSM, Output -> "SM_UFO"];                 (* no restriction; see the header *)
LoadRestriction[FileNameJoin[{srcDirSM$, "DiagonalCKM.rst"}]];
WriteFeynArtsOutput[LSM, Output -> "SM_FA"];      (* CKM = 1, all fermion masses kept *)

Print["Messages issued: ", Length[$MessageList], "   output in ", outDirSM$, ": ",
  FileNameTake /@ FileNames["*", outDirSM$]];


(* ::Subsubsection:: *)
(*Inspect: the start of the FeynArts model file SM_FA.mod*)


If[$Notebooks,
  StringTake[Import[FileNameJoin[{outDirSM$, "SM_FA", "SM_FA.mod"}], "Text"], UpTo[2500]]
]


SetDirectory[startDirSM$];
