(* ::Package:: *)

(* ::Title:: *)
(*Step (1): FeynRules on SM_CKM.fr -> FeynArts model and UFO (Standard Model with the CKM matrix, MS-bar parameters, general R_xi gauge)*)


(* ::Text:: *)
(*Usage*)
(*  terminal :  wolframscript -file generate_SM_CKM.wl      (from any directory)*)
(*  notebook :  Get["<path>/models/sm_ckm/Src/generate_SM_CKM.wl"]*)
(*              or open this file and evaluate it (Src/ is then taken from NotebookDirectory[])*)
(**)
(*Output (overwritten on each run)*)
(*  Src/generated/SM_CKM_FA/              FeynArts model (SM_CKM_FA.mod, .gen, .pars); xiZ, xiW -> GaugeXi[Z], GaugeXi[W]*)
(*  Src/generated/SM_CKM_UFO/             UFO for MadGraph (Feynman gauge: xi = 1)*)
(*  Src/generated/FeynmanRules_SM_CKM.m   vertex list returned by FeynmanRules*)
(**)
(*Checks and expected results*)
(*  (a) CheckHermiticity -> {}, 93 vertex classes (as in the SM note: 23 fermion, 9 scalar, 8 gauge, 29 gauge-scalar,*)
(*      13 ghost-gauge, 11 ghost-scalar).*)
(*  (b) Every class against the note's tables, with the CKM matrix as a general complex matrix (the symbols CKM[i, j]*)
(*      and their conjugates): all 9 generation entries of each fermion class, 0 differences.  The charged quark*)
(*      vertices carry V_{ij} (ubar_i d_j W, ubar_i d_j G+) and conj(V_{ij}) (dbar_j u_i Wbar, dbar_j u_i G-); every other*)
(*      fermion vertex is diagonal.  The table copy with five deliberate errors (the three of the SM note and two in*)
(*      the CKM: V transposed in ubar d W, the conjugate missing in dbar u G-) gives exactly 5 nonzero differences.*)
(*  (c) The unitarity rules of SM_CKM.fr (ckmUnitarity): with the explicit standard parametrization in terms of*)
(*      (s12, s23, s13, dCKM), the fermion vertices of the Lagrangian without the rules equal those with the rules*)
(*      (0 differences in 23 classes x 9 entries).  The Lagrangian without the rules contains products V conj(V)*)
(*      with a summed index, the one with the rules none; the neutral vertices are free of CKM in both cases*)
(*      (FeynmanRules applies the unitarity of a tensor declared Unitary -> True by itself).*)
(*  (d) V = 1: every class equals the SM note's FeynRules output models/sm/Src/generated/FeynmanRules_SM.m*)
(*      (0 differences in 93 classes; fermions entry by entry).*)
(*  No messages.*)
(**)
(*Load FeynRules in a fresh kernel: do not mix it with FeynCalc in one session.  Global names below end in CK$*)
(*so that they cannot clash with model symbols (ee, sw, cw, MW, A, Z, W, H, G0, GP, b, c, s, ...).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file generate_SM_CKM.wl  (in a fresh kernel).  Interactive:  ~/hep/bin/wopen generate_SM_CKM.wl  (in a fresh kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*locations*)


startDirCK$ = Directory[];
srcDirCK$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
outDirCK$ = FileNameJoin[{srcDirCK$, "generated"}];
smRulesFileCK$ = FileNameJoin[{ParentDirectory[srcDirCK$], "..", "sm", "Src", "generated", "FeynmanRules_SM.m"}];


(* ::Section:: *)
(*FeynRules*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];

SetDirectory[srcDirCK$];
LoadModel["SM_CKM.fr"];


(* ::Section:: *)
(*(a) checks of the Lagrangian*)


(* Expected warnings: the neutrino kinetic terms (left-handed only) and the Goldstone mass terms (they come from the
   gauge-fixing term, which has no vertices and is not part of LSM). *)
Print["(a) Hermiticity (expect {}): ", CheckHermiticity[LSM]];
CheckKineticTermNormalisation[LSM];
CheckMassSpectrum[LSM];

verticesCK$ = FeynmanRules[LSM, ScreenOutput -> False];
Print["(a) Number of vertex classes (expect 93): ", Length[verticesCK$]];


(* ::Section:: *)
(*the note's tables*)


(* ::Text:: *)
(*Inert notation for the comparison (so that FeynRules' own rules, e.g. ProjP - ProjM -> Ga[5], do not act):*)
(*  gCK$[mu] = gamma^mu,  gLCK$[mu] = gamma^mu P_L,  gRCK$[mu] = gamma^mu P_R,  pLCK$ = P_L,  pRCK$ = P_R,*)
(*  metCK$[i, j] = g^{mu_i mu_j},  momCK$[i, j] = p_i^{mu_j}  (incoming momentum of leg i, index of leg j),*)
(*  tCK$[a, i, j] = (T^a)_{ij},  fCK$[a, b, c] = f^{abc}  (leg numbers).*)
(*Couplings in the tables are written with ee, sw, cw, MW, MH, m_f and CKM[i, j]; the FeynRules expressions with*)
(*ee, sw, cw, vev, lam, y_f are brought to the same variables by vev = 2 MW sw/ee, lam = MH^2/(2 vev^2),*)
(*y_f = sqrt 2 m_f/vev, MZ = MW/cw, cw = sqrt(1 - sw^2).*)


(* HoldPattern and distinct pattern names: FeynRules evaluates e.g. ProjM[x, x] to the trace 2, so a left-hand side
   ProjM[_, _] would turn every 2 into P_L *)
toInertCK$[expr_] := expr /. {
   HoldPattern[TensDot[Ga[mu_], ProjM][s1_, s2_]] :> gLCK$[mu /. Index[Lorentz, Ext[i_]] :> i],
   HoldPattern[TensDot[Ga[mu_], ProjP][s1_, s2_]] :> gRCK$[mu /. Index[Lorentz, Ext[i_]] :> i],
   HoldPattern[Ga[5, s1_, s2_]] :> pRCK$ - pLCK$,
   HoldPattern[Ga[mu_, s1_, s2_]] :> gCK$[mu /. Index[Lorentz, Ext[i_]] :> i],
   HoldPattern[ProjM[s1_, s2_]] :> pLCK$, HoldPattern[ProjP[s1_, s2_]] :> pRCK$,
   HoldPattern[IndexDelta[Index[Spin, Ext[i_]], Index[Spin, Ext[j_]]]] :> pLCK$ + pRCK$,
   HoldPattern[ME[Index[Lorentz, Ext[i_]], Index[Lorentz, Ext[j_]]]] :> metCK$ @@ Sort[{i, j}],
   HoldPattern[FV[i_, Index[Lorentz, Ext[j_]]]] :> momCK$[i, j],
   HoldPattern[T[Index[Gluon, Ext[a_]], Index[Colour, Ext[i_]], Index[Colour, Ext[j_]]]] :> tCK$[a, i, j],
   HoldPattern[f[x__]] :> (fCK$[x] /. toLegsCK$),
   HoldPattern[IndexDelta[Index[Colour, Ext[i_]], Index[Colour, Ext[j_]]]] :> 1};

(* f is totally antisymmetric; the dummy adjoint index of the four-gluon vertex is called eCK$ *)
fCanonCK$ = fCK$[x__] :> Signature[{x}] (fCK$ @@ Sort[{x}]) /; ! OrderedQ[{x}];
toLegsCK$ = {Index[Gluon, Ext[i_]] :> i, Index[Gluon, _Symbol] :> eCK$};

paramsCK$ = {vev -> 2 MW sw/ee, lam -> MH^2/(2 vev^2) /. vev -> 2 MW sw/ee, MZ -> MW/cw};
momConsCK$ = {momCK$[3, j_] :> -momCK$[1, j] - momCK$[2, j]};

(* generation-resolved expression of a class vertex: legs 1 and 2 carry the generations n1, n2.  The charged Yukawa
   vertices contain a summed dummy generation index (CKM[i, a] yd[a, j]); it is summed term by term, so that a term
   without that dummy is not multiplied by 3. *)
sumDummiesCK$[expr_] := Module[{terms = Expand[expr]},
   terms = If[Head[terms] === Plus, List @@ terms, {terms}];
   Total[Function[t, Module[{ds = Union[Cases[t, Index[Generation, d_Symbol] :> d, Infinity]], res = t},
       Do[res = Sum[res /. Index[Generation, d] -> k, {k, 3}], {d, ds}]; res]] /@ terms]];
genCK$[expr_, n1_, n2_] := sumDummiesCK$[expr /. {Index[Generation, Ext[1]] -> n1, Index[Generation, Ext[2]] -> n2}] /.
   {IndexDelta[i_Integer, j_Integer] :> If[i == j, 1, 0]};
massesCK$ = <|vl -> {0, 0, 0}, l -> {Me, MMU, MTA}, uq -> {MU, MC, MT}, dq -> {MD, MS, MB}|>;
yukCK$ = {yl[i_, i_] :> Sqrt[2] massesCK$[l][[i]]/vev, yu[i_, i_] :> Sqrt[2] massesCK$[uq][[i]]/vev,
   yd[i_, i_] :> Sqrt[2] massesCK$[dq][[i]]/vev, (yl | yu | yd)[_Integer, _Integer] -> 0};

normCK$[expr_] := Simplify[Together[Expand[expr /. yukCK$ /. paramsCK$ /. cw -> Sqrt[1 - sw^2] /. momConsCK$ /. fCanonCK$]],
   0 < sw < 1];


(* ::Text:: *)
(*Fermion vertices (Table rules-f).  Q, T3: charge and weak isospin of the class; leg 1 is the antifermion fb of*)
(*generation n1, leg 2 the fermion f of generation n2.  mixCK$ is the generation factor: V_{n1 n2} for ubar d W and*)
(*ubar d G+, conj(V_{n2 n1}) for dbar u Wbar and dbar u G-, delta_{n1 n2} otherwise.  bad -> True gives the two*)
(*deliberate CKM errors of the control table.*)


qCK$ = <|vl -> 0, l -> -1, uq -> 2/3, dq -> -1/3|>;
t3CK$ = <|vl -> 1/2, l -> -1/2, uq -> 1/2, dq -> -1/2|>;
barClassCK$ = <|vlbar -> vl, lbar -> l, uqbar -> uq, dqbar -> dq|>;

mixCK$[{uqbar, dq, W}, n1_, n2_, bad_] := If[bad, CKM[n2, n1], CKM[n1, n2]];
mixCK$[{uqbar, dq, GP}, n1_, n2_, bad_] := CKM[n1, n2];
mixCK$[{dqbar, uq, Wbar}, n1_, n2_, bad_] := Conjugate[CKM[n2, n1]];
mixCK$[{dqbar, uq, GPbar}, n1_, n2_, bad_] := If[bad, CKM[n2, n1], Conjugate[CKM[n2, n1]]];
mixCK$[flds_, n1_, n2_, bad_] := KroneckerDelta[n1, n2];

tableFCK$[flds : {fb_, f_, A}, n1_, n2_, bad_ : False] := mixCK$[flds, n1, n2, bad] I ee qCK$[f] gCK$[3];
tableFCK$[flds : {fb_, f_, Z}, n1_, n2_, bad_ : False] :=
  mixCK$[flds, n1, n2, bad] I ee/(sw cw) ((t3CK$[f] - sw^2 qCK$[f]) gLCK$[3] - sw^2 qCK$[f] gRCK$[3]);
tableFCK$[flds : {fb_, f_, G}, n1_, n2_, bad_ : False] := mixCK$[flds, n1, n2, bad] I gs tCK$[3, 1, 2] gCK$[3];
tableFCK$[flds : {fb_, f_, W | Wbar}, n1_, n2_, bad_ : False] := mixCK$[flds, n1, n2, bad] I ee/(Sqrt[2] sw) gLCK$[3];
tableFCK$[flds : {fb_, f_, H}, n1_, n2_, bad_ : False] :=
  -mixCK$[flds, n1, n2, bad] I massesCK$[f][[n2]] ee/(2 MW sw) (pLCK$ + pRCK$);
tableFCK$[flds : {fb_, f_, G0}, n1_, n2_, bad_ : False] :=
  -mixCK$[flds, n1, n2, bad] 2 t3CK$[f] massesCK$[f][[n2]] ee/(2 MW sw) (pRCK$ - pLCK$);
(* fbar_n1 f'_n2 G+-: (sqrt 2/v) X_{n1 n2} (m_{fbar, n1} P_L - m_{f', n2} P_R):
   ubar_i d_j G+ -> (sqrt 2/v) V_ij (m_u_i P_L - m_d_j P_R),  dbar_j u_i G- -> (sqrt 2/v) conj(V_ij) (m_d_j P_L - m_u_i P_R),
   nubar l G+ -> -(sqrt 2/v) m_l P_R,  lbar nu G- -> (sqrt 2/v) m_l P_L *)
tableFCK$[flds : {fb_, f_, GP | GPbar}, n1_, n2_, bad_ : False] := mixCK$[flds, n1, n2, bad] Sqrt[2] ee/(2 MW sw) *
   (massesCK$[barClassCK$[fb]][[n1]] pLCK$ - massesCK$[f][[n2]] pRCK$);


(* ::Text:: *)
(*Bosonic vertices (Tables rules-sv, rules-vs, rules-gh of the SM note; unchanged by the CKM matrix), field lists in*)
(*FeynRules' order, legs 1, 2, ...*)
(*Gamma[i, j, k] = g^{ij} (p_i - p_j)^k + g^{jk} (p_j - p_k)^i + g^{ki} (p_k - p_i)^j,*)
(*S[i, j, k, l] = 2 g^{ij} g^{kl} - g^{ik} g^{jl} - g^{il} g^{jk}.*)


metOCK$[i_, j_] := metCK$ @@ Sort[{i, j}];
gamCK$[i_, j_, k_] := metOCK$[i, j] (momCK$[i, k] - momCK$[j, k]) + metOCK$[j, k] (momCK$[j, i] - momCK$[k, i]) +
   metOCK$[k, i] (momCK$[k, j] - momCK$[i, j]);
sCK$[i_, j_, k_, l_] := 2 metOCK$[i, j] metOCK$[k, l] - metOCK$[i, k] metOCK$[j, l] - metOCK$[i, l] metOCK$[j, k];
lamCK$ = MH^2/(2 vev^2) /. vev -> 2 MW sw/ee;
vevCK$ = 2 MW sw/ee;
cwCK$ = Sqrt[1 - sw^2];

tableBCK$ = {
  (* scalar self-couplings *)
  {H, H, H} -> -6 I lamCK$ vevCK$,
  {G0, G0, H} -> -2 I lamCK$ vevCK$,
  {GP, GPbar, H} -> -2 I lamCK$ vevCK$,
  {H, H, H, H} -> -6 I lamCK$,
  {G0, G0, G0, G0} -> -6 I lamCK$,
  {GP, GP, GPbar, GPbar} -> -4 I lamCK$,
  {G0, G0, H, H} -> -2 I lamCK$,
  {GP, GPbar, H, H} -> -2 I lamCK$,
  {G0, G0, GP, GPbar} -> -2 I lamCK$,
  (* gauge self-couplings *)
  {A, W, Wbar} -> -I ee gamCK$[1, 2, 3],
  {W, Wbar, Z} -> -I ee cwCK$/sw gamCK$[1, 2, 3],
  {W, W, Wbar, Wbar} -> I ee^2/sw^2 sCK$[1, 2, 3, 4],
  {A, A, W, Wbar} -> -I ee^2 sCK$[1, 2, 3, 4],
  {W, Wbar, Z, Z} -> -I ee^2 cwCK$^2/sw^2 sCK$[3, 4, 1, 2],
  {A, W, Wbar, Z} -> -I ee^2 cwCK$/sw sCK$[1, 4, 2, 3],
  {G, G, G} -> gs fCK$[1, 2, 3] gamCK$[1, 2, 3],
  {G, G, G, G} -> -I gs^2 (fCK$[1, 2, eCK$] fCK$[3, 4, eCK$] (metOCK$[1, 3] metOCK$[2, 4] - metOCK$[1, 4] metOCK$[2, 3]) +
     fCK$[1, 3, eCK$] fCK$[2, 4, eCK$] (metOCK$[1, 2] metOCK$[3, 4] - metOCK$[1, 4] metOCK$[2, 3]) +
     fCK$[1, 4, eCK$] fCK$[2, 3, eCK$] (metOCK$[1, 2] metOCK$[3, 4] - metOCK$[1, 3] metOCK$[2, 4])),
  (* gauge-scalar, three legs *)
  {H, W, Wbar} -> I ee MW/sw metOCK$[2, 3],
  {H, Z, Z} -> I ee MW/(sw cwCK$^2) metOCK$[2, 3],
  {A, GP, GPbar} -> I ee (momCK$[2, 1] - momCK$[3, 1]),
  {GP, GPbar, Z} -> I ee (cwCK$^2 - sw^2)/(2 sw cwCK$) (momCK$[1, 3] - momCK$[2, 3]),
  {G0, H, Z} -> ee/(2 sw cwCK$) (momCK$[1, 3] - momCK$[2, 3]),
  {GP, H, Wbar} -> ee/(2 sw) (momCK$[1, 3] - momCK$[2, 3]),
  {GPbar, H, W} -> ee/(2 sw) (momCK$[1, 3] - momCK$[2, 3]),
  {G0, GP, Wbar} -> I ee/(2 sw) (momCK$[1, 3] - momCK$[2, 3]),
  {G0, GPbar, W} -> -I ee/(2 sw) (momCK$[1, 3] - momCK$[2, 3]),
  {A, GP, Wbar} -> ee MW metOCK$[1, 3],
  {A, GPbar, W} -> -ee MW metOCK$[1, 3],
  {GP, Wbar, Z} -> -ee MW sw/cwCK$ metOCK$[2, 3],
  {GPbar, W, Z} -> ee MW sw/cwCK$ metOCK$[2, 3],
  (* gauge-scalar, four legs *)
  {H, H, W, Wbar} -> I ee^2/(2 sw^2) metOCK$[3, 4],
  {G0, G0, W, Wbar} -> I ee^2/(2 sw^2) metOCK$[3, 4],
  {GP, GPbar, W, Wbar} -> I ee^2/(2 sw^2) metOCK$[3, 4],
  {H, H, Z, Z} -> I ee^2/(2 sw^2 cwCK$^2) metOCK$[3, 4],
  {G0, G0, Z, Z} -> I ee^2/(2 sw^2 cwCK$^2) metOCK$[3, 4],
  {GP, GPbar, Z, Z} -> I ee^2 (cwCK$^2 - sw^2)^2/(2 sw^2 cwCK$^2) metOCK$[3, 4],
  {A, A, GP, GPbar} -> 2 I ee^2 metOCK$[1, 2],
  {A, GP, GPbar, Z} -> I ee^2 (cwCK$^2 - sw^2)/(sw cwCK$) metOCK$[1, 4],
  {A, G0, GP, Wbar} -> -I ee^2/(2 sw) metOCK$[1, 4],
  {A, G0, GPbar, W} -> -I ee^2/(2 sw) metOCK$[1, 4],
  {A, GP, H, Wbar} -> ee^2/(2 sw) metOCK$[1, 4],
  {A, GPbar, H, W} -> -ee^2/(2 sw) metOCK$[1, 4],
  {G0, GP, Wbar, Z} -> I ee^2/(2 cwCK$) metOCK$[3, 4],
  {G0, GPbar, W, Z} -> I ee^2/(2 cwCK$) metOCK$[3, 4],
  {GP, H, Wbar, Z} -> -ee^2/(2 cwCK$) metOCK$[3, 4],
  {GPbar, H, W, Z} -> ee^2/(2 cwCK$) metOCK$[3, 4],
  (* ghost-gauge: p = momCK$[1, 3], the incoming momentum of the antighost leg 1 *)
  {ghAbar, ghWm, W} -> -I ee momCK$[1, 3],
  {ghAbar, ghWp, Wbar} -> I ee momCK$[1, 3],
  {ghZbar, ghWm, W} -> -I ee cwCK$/sw momCK$[1, 3],
  {ghZbar, ghWp, Wbar} -> I ee cwCK$/sw momCK$[1, 3],
  {ghWpbar, ghA, W} -> I ee momCK$[1, 3],
  {ghWmbar, ghA, Wbar} -> -I ee momCK$[1, 3],
  {ghWpbar, ghZ, W} -> I ee cwCK$/sw momCK$[1, 3],
  {ghWmbar, ghZ, Wbar} -> -I ee cwCK$/sw momCK$[1, 3],
  {ghWpbar, ghWp, A} -> -I ee momCK$[1, 3],
  {ghWmbar, ghWm, A} -> I ee momCK$[1, 3],
  {ghWpbar, ghWp, Z} -> -I ee cwCK$/sw momCK$[1, 3],
  {ghWmbar, ghWm, Z} -> I ee cwCK$/sw momCK$[1, 3],
  {ghGbar, ghG, G} -> -gs fCK$[1, 2, 3] momCK$[1, 3],
  (* ghost-scalar: xi of the antighost's gauge field *)
  {ghWpbar, ghA, GP} -> -xiW ee MW,
  {ghWmbar, ghA, GPbar} -> xiW ee MW,
  {ghWpbar, ghZ, GP} -> -xiW ee MW (cwCK$^2 - sw^2)/(2 sw cwCK$),
  {ghWmbar, ghZ, GPbar} -> xiW ee MW (cwCK$^2 - sw^2)/(2 sw cwCK$),
  {ghWpbar, ghWp, H} -> -I xiW ee MW/(2 sw),
  {ghWmbar, ghWm, H} -> -I xiW ee MW/(2 sw),
  {ghWpbar, ghWp, G0} -> xiW ee MW/(2 sw),
  {ghWmbar, ghWm, G0} -> -xiW ee MW/(2 sw),
  {ghZbar, ghWm, GP} -> xiZ ee MW/(2 sw cwCK$),
  {ghZbar, ghWp, GPbar} -> -xiZ ee MW/(2 sw cwCK$),
  {ghZbar, ghZ, H} -> -I xiZ ee MW/(2 sw cwCK$^2)
};


(* ::Section:: *)
(*(b) comparison with the tables*)


fermionClassesCK$ = {vl, l, uq, dq};
isFermionVertexCK$[flds_] := MemberQ[fermionClassesCK$, flds[[2]]];
classListCK$[verts_] := verts /. {{v_List, e_} :> {First /@ v, e}};

(* one row per class: {fields, Union of the differences over the 9 generation entries (fermions) or the difference} *)
compareCK$[{flds_, expr_}, tableB_, bad_] := Module[{inert = toInertCK$[expr]},
   If[isFermionVertexCK$[flds],
     {flds, Union[Flatten[Table[normCK$[genCK$[inert, n1, n2] - tableFCK$[flds, n1, n2, bad]], {n1, 3}, {n2, 3}]]]},
     {flds, Union[{normCK$[inert - (flds /. tableB)]}]}]];

reportCK$[tableB_, bad_, label_] := Module[{rows, nonzero},
   rows = compareCK$[#, tableB, bad] & /@ classListCK$[verticesCK$];
   nonzero = Select[rows, #[[2]] =!= {0} &];
   Print[label, ": ", Length[rows], " classes compared, nonzero differences: ", Length[nonzero]];
   Scan[Print["   ", #[[1]], "  difference ", #[[2]]] &, nonzero];
   rows];

rowsCK$ = reportCK$[tableBCK$, False, "(b) Note's tables with a general V (expect 0)"];
Print["(b) Classes not in the tables (expect {}): ",
  Complement[First /@ classListCK$[verticesCK$],
    Join[First /@ tableBCK$, Select[First /@ classListCK$[verticesCK$], isFermionVertexCK$]]]];
Print["(b) Fermion classes that contain CKM (expect the four charged quark vertices): ",
  First /@ Select[classListCK$[verticesCK$], ! FreeQ[#[[2]], CKM] &]];

(* control: five deliberate errors (a sign of the photon-W-W vertex, a factor 2 in H G0 G0, a missing xi, V transposed
   in ubar d W, the conjugate missing in dbar u G-) *)
tableBadCK$ = tableBCK$ /. {
   ({A, W, Wbar} -> x_) :> ({A, W, Wbar} -> -x),
   ({G0, G0, H} -> x_) :> ({G0, G0, H} -> 2 x),
   ({ghZbar, ghZ, H} -> x_) :> ({ghZbar, ghZ, H} -> (x /. xiZ -> 1))};
reportCK$[tableBadCK$, True, "(b) Table with five deliberate errors (expect 5)"];


(* ::Subsubsection:: *)
(*Inspect: the charged quark vertices*)


If[$Notebooks,
  TableForm[Select[classListCK$[verticesCK$], ! FreeQ[#[[2]], CKM] &] /. {f_List, c_} :> {f, TraditionalForm[c]}]
]


(* ::Section:: *)
(*(c) the unitarity rules against the explicit parametrization*)


(* V of SM_CKM.fr with real angles: c_ij = sqrt(1 - s_ij^2) *)
vExplicitCK$ = {
   {c12 c13, s12 c13, s13 Exp[-I dCKM]},
   {-s12 c23 - c12 s23 s13 Exp[I dCKM], c12 c23 - s12 s23 s13 Exp[I dCKM], s23 c13},
   {s12 s23 - c12 c23 s13 Exp[I dCKM], -c12 s23 - s12 c23 s13 Exp[I dCKM], c23 c13}} /.
   {c12 -> Sqrt[1 - s12^2], c23 -> Sqrt[1 - s23^2], c13 -> Sqrt[1 - s13^2]};
explicitCK$[expr_] := ComplexExpand[expr /. CKM[i_Integer, j_Integer] :> vExplicitCK$[[i, j]]];
angleAssCK$ = 0 < s12 < 1 && 0 < s23 < 1 && 0 < s13 < 1 && Element[dCKM, Reals] && 0 < sw < 1;
normExplicitCK$[expr_] := Simplify[explicitCK$[normCK$[expr]], angleAssCK$];

Print["(c) Unitarity of the explicit V (expect True): ",
  Simplify[ComplexExpand[ConjugateTranspose[vExplicitCK$] . vExplicitCK$] == IdentityMatrix[3], angleAssCK$]];
rawVerticesCK$ = FeynmanRules[LFermionRawSM + LYukawaRawSM, ScreenOutput -> False];
rawRowsCK$ = Module[{newF = Select[classListCK$[verticesCK$], isFermionVertexCK$[#[[1]]] &], oldF},
   oldF = classListCK$[rawVerticesCK$];
   Function[row, Module[{raw = Cases[oldF, {row[[1]], e_} :> e]},
       {row[[1]], Length[raw], If[raw === {}, {"missing"},
         Union[Flatten[Table[normExplicitCK$[genCK$[toInertCK$[First[raw]], n1, n2] - genCK$[toInertCK$[row[[2]]], n1, n2]],
             {n1, 3}, {n2, 3}]]]],
         (* the raw neutral-current entries before the explicit V: CKM sums still present? *)
         ! FreeQ[If[raw === {}, 0, Table[normCK$[genCK$[toInertCK$[First[raw]], n1, n2]], {n1, 3}, {n2, 3}]], CKM]}]] /@ newF];
Print["(c) Fermion classes without the rules: ", Length[classListCK$[rawVerticesCK$]], " (expect 23); with the rules: ",
  Length[rawRowsCK$]];
Print["(c) Classes whose explicit-V entries differ (expect {}): ", Select[rawRowsCK$, #[[3]] =!= {0} &]];
Print["(c) Classes whose vertices from the Lagrangian without the rules contain CKM (expect the four charged ones): ",
  First /@ Select[rawRowsCK$, #[[4]] &]];
(* the Lagrangian itself: products V_ab conj(V_ac) or V_ba conj(V_ca) with a summed dummy index *)
ckmPairsCK$[lag_] := Count[Expand[lag], HoldPattern[Times[___, CKM[i1_, _], Conjugate[CKM[i1_, _]], ___]] |
    HoldPattern[Times[___, CKM[_, i1_], Conjugate[CKM[_, i1_]], ___]], {1}];
Print["(c) Terms with a product V conj(V) (summed index): without the rules ", ckmPairsCK$[LFermionRawSM + LYukawaRawSM],
  ", with the rules (expect 0) ", ckmPairsCK$[LFermionSM + LYukawaSM],
  ".  Nonzero without the rules and no CKM in the neutral vertices: FeynmanRules uses Unitary -> True by itself."];


(* ::Section:: *)
(*(d) V = 1: the SM note's vertices*)


smVerticesCK$ = Get[smRulesFileCK$];
toUnitCK$ = {CKM[i_Integer, j_Integer] :> KroneckerDelta[i, j]};
v1RowsCK$ = Function[row, Module[{old = Cases[classListCK$[smVerticesCK$], {row[[1]], e_} :> e]},
     {row[[1]], If[old === {}, {"missing"},
       If[isFermionVertexCK$[row[[1]]],
         Union[Flatten[Table[normCK$[(genCK$[toInertCK$[row[[2]]], n1, n2] /. toUnitCK$) - genCK$[toInertCK$[First[old]], n1, n2]],
             {n1, 3}, {n2, 3}]]],
         Union[{normCK$[toInertCK$[row[[2]]] - toInertCK$[First[old]]]}]]]}]] /@ classListCK$[verticesCK$];
Print["(d) V = 1 against the SM note's FeynRules output: ", Length[smVerticesCK$], " classes there, ",
  Length[v1RowsCK$], " here; classes that differ (expect {}): ", Select[v1RowsCK$, #[[2]] =!= {0} &]];


(* ::Section:: *)
(*write outputs*)


Quiet[CreateDirectory[outDirCK$]];
SetDirectory[outDirCK$];
Scan[If[DirectoryQ[#], DeleteDirectory[#, DeleteContents -> True]] &, {"SM_CKM_FA", "SM_CKM_UFO"}];

Put[verticesCK$, "FeynmanRules_SM_CKM.m"];
(* The UFO first: after WriteFeynArtsOutput, the flavour-expanded FeynmanRules call inside WriteUFO returns a 94th,
   garbled class {dqbar, uq, W} (charge 2, CKM with one index, Index[Generation, {}]) with Inner::incom messages.
   FeynArts' own FeynmanRules call after WriteUFO gives the 93 classes and the same SM_CKM_FA.mod, .gen, .pars as
   in a fresh kernel (checked once by diff), but its parallel subkernels then print Simplify::time (a time-out of
   FeynRules' own Simplify with TimeConstraint -> 0.01); those messages are switched off on the subkernels. *)
WriteUFO[LSM, Output -> "SM_CKM_UFO"];
ParallelEvaluate[Off[Simplify::time]];
WriteFeynArtsOutput[LSM, Output -> "SM_CKM_FA", GenericFile -> True];
ufoLogCK$ = Import[FileNameJoin[{outDirCK$, "SM_CKM_UFO", "SM_CKM_UFO.log"}], "Text"];
Print["UFO log (expect 93 classes, 163 = 139 + 24 flavoured vertices, Q conserved): ",
  StringCases[ufoLogCK$, RegularExpression["Number of classes vertices: \\d+|\\d+ vertices written|Quantum number Q conserved[^\\n]*"]]];

(* FeynArts: the ghost-scalar couplings carry the gauge parameters of the propagators *)
modFileCK$ = FileNameJoin[{outDirCK$, "SM_CKM_FA", "SM_CKM_FA.mod"}];
modTextCK$ = Import[modFileCK$, "Text"];
Print["xi symbols in SM_CKM_FA.mod before the replacement: ",
  Counts[StringCases[modTextCK$, RegularExpression["\\bxi[AZWG]\\b"]]]];
modTextCK$ = StringReplace[modTextCK$, {
   RegularExpression["\\bxiZ\\b"] -> "GaugeXi[Z]", RegularExpression["\\bxiW\\b"] -> "GaugeXi[W]",
   RegularExpression["\\bxiA\\b"] -> "GaugeXi[A]", RegularExpression["\\bxiG\\b"] -> "GaugeXi[G]"}];
Export[modFileCK$, modTextCK$, "Text"];
Print["CKM in SM_CKM_FA.mod: ", Length[StringCases[modTextCK$, "CKM["]], " occurrences, ",
  Length[StringCases[modTextCK$, "Conjugate[CKM["]], " of them conjugated"];

Print["Messages issued: ", Length[$MessageList], "   output in ", outDirCK$, ": ",
  FileNameTake /@ FileNames["*", outDirCK$]];


(* ::Subsubsection:: *)
(*Inspect: the start of the FeynArts model file SM_CKM_FA.mod*)


If[$Notebooks,
  StringTake[Import[modFileCK$, "Text"], UpTo[2500]]
]


SetDirectory[startDirCK$];
