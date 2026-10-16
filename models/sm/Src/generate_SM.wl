(* ::Package:: *)

(* ::Title:: *)
(*Step (1): FeynRules on SM.fr -> FeynArts model and UFO (Standard Model, MS-bar parameters, general R_xi gauge)*)


(* ::Text:: *)
(*Usage*)
(*  terminal :  wolframscript -file generate_SM.wl      (from any directory)*)
(*  notebook :  Get["<path>/models/sm/Src/generate_SM.wl"]*)
(*              or open this file and evaluate it (Src/ is then taken from NotebookDirectory[])*)
(**)
(*Output (overwritten on each run)*)
(*  Src/generated/SM_FA/                FeynArts model (SM_FA.mod, .gen, .pars); xiZ, xiW -> GaugeXi[Z], GaugeXi[W]*)
(*  Src/generated/SM_UFO/               UFO for MadGraph (Feynman gauge: xi = 1)*)
(*  Src/generated/FeynmanRules_SM.m     vertex list returned by FeynmanRules*)
(**)
(*Expected results*)
(*  CheckHermiticity -> {},  93 vertex classes (23 fermion, 9 scalar, 8 gauge, 29 gauge-scalar, 13 ghost-gauge,*)
(*  11 ghost-scalar), every difference from the note's tables (Tables rules-f ... rules-gh) equal to 0, and every*)
(*  generation-off-diagonal entry equal to 0.  The table copy with three deliberate errors gives exactly 3 nonzero*)
(*  differences.  No messages.*)
(**)
(*Load FeynRules in a fresh kernel: do not mix it with FeynCalc in one session.  Global names below end in SM$*)
(*so that they cannot clash with model symbols (ee, sw, cw, MW, A, Z, W, H, G0, GP, b, ...): FeynRules patterns*)
(*with the name of a model symbol leak that symbol into the result.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file generate_SM.wl  (in a fresh kernel).  Interactive:  ~/hep/bin/wopen generate_SM.wl  (in a fresh kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


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
(*Inspect: the ghost-scalar part of the Faddeev-Popov term (generated from s Phi in SM.fr)*)


If[$Notebooks, LGhostScalarSM // TraditionalForm]


(* ::Section:: *)
(*checks of the Lagrangian*)


(* Expected warnings: the neutrino kinetic terms (left-handed only) and the Goldstone mass terms (they come from the
   gauge-fixing term, which has no vertices and is not part of LSM). *)
Print["Hermiticity (expect {}): ", CheckHermiticity[LSM]];
CheckKineticTermNormalisation[LSM];
CheckMassSpectrum[LSM];

verticesSM$ = FeynmanRules[LSM, ScreenOutput -> False];
Print["Number of vertex classes (expect 93): ", Length[verticesSM$]];


(* ::Section:: *)
(*the note's tables*)


(* ::Text:: *)
(*Inert notation for the comparison (so that FeynRules' own rules, e.g. ProjP - ProjM -> Ga[5], do not act):*)
(*  gSM$[mu] = gamma^mu,  gLSM$[mu] = gamma^mu P_L,  gRSM$[mu] = gamma^mu P_R,  pLSM$ = P_L,  pRSM$ = P_R,*)
(*  metSM$[i, j] = g^{mu_i mu_j},  momSM$[i, j] = p_i^{mu_j}  (incoming momentum of leg i, index of leg j),*)
(*  tSM$[a, i, j] = (T^a)_{ij},  fSM$[a, b, c] = f^{abc}  (leg numbers).*)
(*Couplings in the tables are written with ee, sw, cw, MW, MH, m_f; the FeynRules expressions with ee, sw, cw, vev,*)
(*lam, y_f are brought to the same variables by vev = 2 MW sw/ee, lam = MH^2/(2 vev^2), y_f = sqrt 2 m_f/vev,*)
(*MZ = MW/cw, cw = sqrt(1 - sw^2).*)


(* HoldPattern and distinct pattern names: FeynRules evaluates e.g. ProjM[x, x] to the trace 2, so a left-hand side
   ProjM[_, _] would turn every 2 into P_L *)
toInertSM$[expr_] := expr /. {
   HoldPattern[TensDot[Ga[mu_], ProjM][s1_, s2_]] :> gLSM$[mu /. Index[Lorentz, Ext[i_]] :> i],
   HoldPattern[TensDot[Ga[mu_], ProjP][s1_, s2_]] :> gRSM$[mu /. Index[Lorentz, Ext[i_]] :> i],
   HoldPattern[Ga[5, s1_, s2_]] :> pRSM$ - pLSM$,
   HoldPattern[Ga[mu_, s1_, s2_]] :> gSM$[mu /. Index[Lorentz, Ext[i_]] :> i],
   HoldPattern[ProjM[s1_, s2_]] :> pLSM$, HoldPattern[ProjP[s1_, s2_]] :> pRSM$,
   HoldPattern[IndexDelta[Index[Spin, Ext[i_]], Index[Spin, Ext[j_]]]] :> pLSM$ + pRSM$,
   HoldPattern[ME[Index[Lorentz, Ext[i_]], Index[Lorentz, Ext[j_]]]] :> metSM$ @@ Sort[{i, j}],
   HoldPattern[FV[i_, Index[Lorentz, Ext[j_]]]] :> momSM$[i, j],
   HoldPattern[T[Index[Gluon, Ext[a_]], Index[Colour, Ext[i_]], Index[Colour, Ext[j_]]]] :> tSM$[a, i, j],
   HoldPattern[f[x__]] :> (fSM$[x] /. toLegsSM$),
   HoldPattern[IndexDelta[Index[Colour, Ext[i_]], Index[Colour, Ext[j_]]]] :> 1};

(* f is totally antisymmetric; the dummy adjoint index of the four-gluon vertex is called eSM$ *)
fCanonSM$ = fSM$[x__] :> Signature[{x}] (fSM$ @@ Sort[{x}]) /; ! OrderedQ[{x}];
toLegsSM$ = {Index[Gluon, Ext[i_]] :> i, Index[Gluon, _Symbol] :> eSM$};

paramsSM$ = {vev -> 2 MW sw/ee, lam -> MH^2/(2 vev^2) /. vev -> 2 MW sw/ee, MZ -> MW/cw};
momConsSM$ = {momSM$[3, j_] :> -momSM$[1, j] - momSM$[2, j]};

(* generation-resolved expression of a class vertex: legs 1 and 2 carry the generations n1, n2 *)
genSM$[expr_, n1_, n2_] := expr /. {Index[Generation, Ext[1]] -> n1, Index[Generation, Ext[2]] -> n2} /.
   {IndexDelta[i_Integer, j_Integer] :> If[i == j, 1, 0]};
massesSM$ = <|vl -> {0, 0, 0}, l -> {Me, MMU, MTA}, uq -> {MU, MC, MT}, dq -> {MD, MS, MB}|>;
yukSM$ = {yl[i_, i_] :> Sqrt[2] massesSM$[l][[i]]/vev, yu[i_, i_] :> Sqrt[2] massesSM$[uq][[i]]/vev,
   yd[i_, i_] :> Sqrt[2] massesSM$[dq][[i]]/vev, (yl | yu | yd)[_Integer, _Integer] -> 0};

normSM$[expr_] := Simplify[Together[Expand[expr /. yukSM$ /. paramsSM$ /. cw -> Sqrt[1 - sw^2] /. momConsSM$ /. fCanonSM$]],
   0 < sw < 1];


(* ::Text:: *)
(*Fermion vertices (Table rules-f).  Q, T3: charge and weak isospin of the class; m: mass of the generation.*)


qSM$ = <|vl -> 0, l -> -1, uq -> 2/3, dq -> -1/3|>;
t3SM$ = <|vl -> 1/2, l -> -1/2, uq -> 1/2, dq -> -1/2|>;
partnerSM$ = <|vl -> l, l -> vl, uq -> dq, dq -> uq|>;

tableFSM$[{fb_, f_, A}, n_] := I ee qSM$[f] gSM$[3];
tableFSM$[{fb_, f_, Z}, n_] := I ee/(sw cw) ((t3SM$[f] - sw^2 qSM$[f]) gLSM$[3] - sw^2 qSM$[f] gRSM$[3]);
tableFSM$[{fb_, f_, G}, n_] := I gs tSM$[3, 1, 2] gSM$[3];
tableFSM$[{fb_, f_, W | Wbar}, n_] := I ee/(Sqrt[2] sw) gLSM$[3];
tableFSM$[{fb_, f_, H}, n_] := -I massesSM$[f][[n]] ee/(2 MW sw) (pLSM$ + pRSM$);
tableFSM$[{fb_, f_, G0}, n_] := -2 t3SM$[f] massesSM$[f][[n]] ee/(2 MW sw) (pRSM$ - pLSM$);
(* fbar f' G+-: (sqrt 2/v) (m_up P_L - m_down P_R) for ubar d G+, (sqrt 2/v) (m_down P_L - m_up P_R) for dbar u G- *)
(* fbar f' G+-: (sqrt 2/v)(m_partner P_L - m_f P_R): ubar d G+ -> (sqrt 2/v)(m_u P_L - m_d P_R),
   dbar u G- -> (sqrt 2/v)(m_d P_L - m_u P_R), nubar l G+ -> -(sqrt 2/v) m_l P_R, lbar nu G- -> (sqrt 2/v) m_l P_L *)
tableFSM$[{fb_, f_, GP | GPbar}, n_] :=
  Sqrt[2] ee/(2 MW sw) (massesSM$[partnerSM$[f]][[n]] pLSM$ - massesSM$[f][[n]] pRSM$);


(* ::Text:: *)
(*Bosonic vertices (Tables rules-sv, rules-vs, rules-gh), field lists in FeynRules' order, legs 1, 2, ...*)
(*Gamma[i, j, k] = g^{ij} (p_i - p_j)^k + g^{jk} (p_j - p_k)^i + g^{ki} (p_k - p_i)^j,*)
(*S[i, j, k, l] = 2 g^{ij} g^{kl} - g^{ik} g^{jl} - g^{il} g^{jk}.*)


metOSM$[i_, j_] := metSM$ @@ Sort[{i, j}];
gamSM$[i_, j_, k_] := metOSM$[i, j] (momSM$[i, k] - momSM$[j, k]) + metOSM$[j, k] (momSM$[j, i] - momSM$[k, i]) +
   metOSM$[k, i] (momSM$[k, j] - momSM$[i, j]);
sSM$[i_, j_, k_, l_] := 2 metOSM$[i, j] metOSM$[k, l] - metOSM$[i, k] metOSM$[j, l] - metOSM$[i, l] metOSM$[j, k];
lamSM$ = MH^2/(2 vev^2) /. vev -> 2 MW sw/ee;
vevSM$ = 2 MW sw/ee;
cwSM$ = Sqrt[1 - sw^2];

tableBSM$ = {
  (* scalar self-couplings *)
  {H, H, H} -> -6 I lamSM$ vevSM$,
  {G0, G0, H} -> -2 I lamSM$ vevSM$,
  {GP, GPbar, H} -> -2 I lamSM$ vevSM$,
  {H, H, H, H} -> -6 I lamSM$,
  {G0, G0, G0, G0} -> -6 I lamSM$,
  {GP, GP, GPbar, GPbar} -> -4 I lamSM$,
  {G0, G0, H, H} -> -2 I lamSM$,
  {GP, GPbar, H, H} -> -2 I lamSM$,
  {G0, G0, GP, GPbar} -> -2 I lamSM$,
  (* gauge self-couplings *)
  {A, W, Wbar} -> -I ee gamSM$[1, 2, 3],
  {W, Wbar, Z} -> -I ee cwSM$/sw gamSM$[1, 2, 3],
  {W, W, Wbar, Wbar} -> I ee^2/sw^2 sSM$[1, 2, 3, 4],
  {A, A, W, Wbar} -> -I ee^2 sSM$[1, 2, 3, 4],
  {W, Wbar, Z, Z} -> -I ee^2 cwSM$^2/sw^2 sSM$[3, 4, 1, 2],
  {A, W, Wbar, Z} -> -I ee^2 cwSM$/sw sSM$[1, 4, 2, 3],
  {G, G, G} -> gs fSM$[1, 2, 3] gamSM$[1, 2, 3],
  {G, G, G, G} -> -I gs^2 (fSM$[1, 2, eSM$] fSM$[3, 4, eSM$] (metOSM$[1, 3] metOSM$[2, 4] - metOSM$[1, 4] metOSM$[2, 3]) +
     fSM$[1, 3, eSM$] fSM$[2, 4, eSM$] (metOSM$[1, 2] metOSM$[3, 4] - metOSM$[1, 4] metOSM$[2, 3]) +
     fSM$[1, 4, eSM$] fSM$[2, 3, eSM$] (metOSM$[1, 2] metOSM$[3, 4] - metOSM$[1, 3] metOSM$[2, 4])),
  (* gauge-scalar, three legs *)
  {H, W, Wbar} -> I ee MW/sw metOSM$[2, 3],
  {H, Z, Z} -> I ee MW/(sw cwSM$^2) metOSM$[2, 3],
  {A, GP, GPbar} -> I ee (momSM$[2, 1] - momSM$[3, 1]),
  {GP, GPbar, Z} -> I ee (cwSM$^2 - sw^2)/(2 sw cwSM$) (momSM$[1, 3] - momSM$[2, 3]),
  {G0, H, Z} -> ee/(2 sw cwSM$) (momSM$[1, 3] - momSM$[2, 3]),
  {GP, H, Wbar} -> ee/(2 sw) (momSM$[1, 3] - momSM$[2, 3]),
  {GPbar, H, W} -> ee/(2 sw) (momSM$[1, 3] - momSM$[2, 3]),
  {G0, GP, Wbar} -> I ee/(2 sw) (momSM$[1, 3] - momSM$[2, 3]),
  {G0, GPbar, W} -> -I ee/(2 sw) (momSM$[1, 3] - momSM$[2, 3]),
  {A, GP, Wbar} -> ee MW metOSM$[1, 3],
  {A, GPbar, W} -> -ee MW metOSM$[1, 3],
  {GP, Wbar, Z} -> -ee MW sw/cwSM$ metOSM$[2, 3],
  {GPbar, W, Z} -> ee MW sw/cwSM$ metOSM$[2, 3],
  (* gauge-scalar, four legs *)
  {H, H, W, Wbar} -> I ee^2/(2 sw^2) metOSM$[3, 4],
  {G0, G0, W, Wbar} -> I ee^2/(2 sw^2) metOSM$[3, 4],
  {GP, GPbar, W, Wbar} -> I ee^2/(2 sw^2) metOSM$[3, 4],
  {H, H, Z, Z} -> I ee^2/(2 sw^2 cwSM$^2) metOSM$[3, 4],
  {G0, G0, Z, Z} -> I ee^2/(2 sw^2 cwSM$^2) metOSM$[3, 4],
  {GP, GPbar, Z, Z} -> I ee^2 (cwSM$^2 - sw^2)^2/(2 sw^2 cwSM$^2) metOSM$[3, 4],
  {A, A, GP, GPbar} -> 2 I ee^2 metOSM$[1, 2],
  {A, GP, GPbar, Z} -> I ee^2 (cwSM$^2 - sw^2)/(sw cwSM$) metOSM$[1, 4],
  {A, G0, GP, Wbar} -> -I ee^2/(2 sw) metOSM$[1, 4],
  {A, G0, GPbar, W} -> -I ee^2/(2 sw) metOSM$[1, 4],
  {A, GP, H, Wbar} -> ee^2/(2 sw) metOSM$[1, 4],
  {A, GPbar, H, W} -> -ee^2/(2 sw) metOSM$[1, 4],
  {G0, GP, Wbar, Z} -> I ee^2/(2 cwSM$) metOSM$[3, 4],
  {G0, GPbar, W, Z} -> I ee^2/(2 cwSM$) metOSM$[3, 4],
  {GP, H, Wbar, Z} -> -ee^2/(2 cwSM$) metOSM$[3, 4],
  {GPbar, H, W, Z} -> ee^2/(2 cwSM$) metOSM$[3, 4],
  (* ghost-gauge: p = momSM$[1, 3], the incoming momentum of the antighost leg 1 *)
  {ghAbar, ghWm, W} -> -I ee momSM$[1, 3],
  {ghAbar, ghWp, Wbar} -> I ee momSM$[1, 3],
  {ghZbar, ghWm, W} -> -I ee cwSM$/sw momSM$[1, 3],
  {ghZbar, ghWp, Wbar} -> I ee cwSM$/sw momSM$[1, 3],
  {ghWpbar, ghA, W} -> I ee momSM$[1, 3],
  {ghWmbar, ghA, Wbar} -> -I ee momSM$[1, 3],
  {ghWpbar, ghZ, W} -> I ee cwSM$/sw momSM$[1, 3],
  {ghWmbar, ghZ, Wbar} -> -I ee cwSM$/sw momSM$[1, 3],
  {ghWpbar, ghWp, A} -> -I ee momSM$[1, 3],
  {ghWmbar, ghWm, A} -> I ee momSM$[1, 3],
  {ghWpbar, ghWp, Z} -> -I ee cwSM$/sw momSM$[1, 3],
  {ghWmbar, ghWm, Z} -> I ee cwSM$/sw momSM$[1, 3],
  {ghGbar, ghG, G} -> -gs fSM$[1, 2, 3] momSM$[1, 3],
  (* ghost-scalar: xi of the antighost's gauge field *)
  {ghWpbar, ghA, GP} -> -xiW ee MW,
  {ghWmbar, ghA, GPbar} -> xiW ee MW,
  {ghWpbar, ghZ, GP} -> -xiW ee MW (cwSM$^2 - sw^2)/(2 sw cwSM$),
  {ghWmbar, ghZ, GPbar} -> xiW ee MW (cwSM$^2 - sw^2)/(2 sw cwSM$),
  {ghWpbar, ghWp, H} -> -I xiW ee MW/(2 sw),
  {ghWmbar, ghWm, H} -> -I xiW ee MW/(2 sw),
  {ghWpbar, ghWp, G0} -> xiW ee MW/(2 sw),
  {ghWmbar, ghWm, G0} -> -xiW ee MW/(2 sw),
  {ghZbar, ghWm, GP} -> xiZ ee MW/(2 sw cwSM$),
  {ghZbar, ghWp, GPbar} -> -xiZ ee MW/(2 sw cwSM$),
  {ghZbar, ghZ, H} -> -I xiZ ee MW/(2 sw cwSM$^2)
};


(* ::Section:: *)
(*comparison*)


fermionClassesSM$ = {vl, l, uq, dq};
isFermionVertexSM$[flds_] := MemberQ[fermionClassesSM$, flds[[2]]];

(* one row per class: {fields, max |difference| over generations (diagonal), off-diagonal entries} *)
compareSM$[{flds_, expr_}, tableB_] := Module[{inert, diffs, off},
   inert = toInertSM$[expr];
   If[isFermionVertexSM$[flds],
     diffs = Table[normSM$[genSM$[inert, n, n] - tableFSM$[flds, n]], {n, 3}];
     off = Union[Flatten[Table[If[n1 != n2, normSM$[genSM$[inert, n1, n2]], Nothing], {n1, 3}, {n2, 3}]]];
     {flds, Union[diffs], off},
     {flds, Union[{normSM$[inert - (flds /. tableB)]}], {0}}]];

reportSM$[tableB_, label_] := Module[{rows, bad},
   rows = compareSM$[#, tableB] & /@ (verticesSM$ /. {{v_List, e_} :> {First /@ v, e}});
   bad = Select[rows, #[[2]] =!= {0} || #[[3]] =!= {0} &];
   Print[label, ": ", Length[rows], " classes compared, nonzero differences: ", Length[bad]];
   Scan[Print["   ", #[[1]], "  difference ", #[[2]], "  off-diagonal ", #[[3]]] &, bad];
   rows];

rowsSM$ = reportSM$[tableBSM$, "Note's tables (expect 0)"];
Print["Classes not in the tables (expect {}): ",
  Complement[First /@ (verticesSM$ /. {{v_List, e_} :> {First /@ v, e}}),
    Join[First /@ tableBSM$, Select[First /@ (verticesSM$ /. {{v_List, e_} :> {First /@ v, e}}), isFermionVertexSM$]]]];

(* control: three deliberate errors (a sign of the photon-W-W vertex, a factor 2 in H G0 G0, a missing xi) *)
tableBadSM$ = tableBSM$ /. {
   ({A, W, Wbar} -> x_) :> ({A, W, Wbar} -> -x),
   ({G0, G0, H} -> x_) :> ({G0, G0, H} -> 2 x),
   ({ghZbar, ghZ, H} -> x_) :> ({ghZbar, ghZ, H} -> (x /. xiZ -> 1))};
reportSM$[tableBadSM$, "Table with three deliberate errors (expect 3)"];


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
WriteFeynArtsOutput[LSM, Output -> "SM_FA", GenericFile -> True];
WriteUFO[LSM, Output -> "SM_UFO"];

(* FeynArts: the ghost-scalar couplings carry the gauge parameters of the propagators *)
modFileSM$ = FileNameJoin[{outDirSM$, "SM_FA", "SM_FA.mod"}];
modTextSM$ = Import[modFileSM$, "Text"];
Print["xi symbols in SM_FA.mod before the replacement: ",
  Counts[StringCases[modTextSM$, RegularExpression["\\bxi[AZWG]\\b"]]]];
modTextSM$ = StringReplace[modTextSM$, {
   RegularExpression["\\bxiZ\\b"] -> "GaugeXi[Z]", RegularExpression["\\bxiW\\b"] -> "GaugeXi[W]",
   RegularExpression["\\bxiA\\b"] -> "GaugeXi[A]", RegularExpression["\\bxiG\\b"] -> "GaugeXi[G]"}];
Export[modFileSM$, modTextSM$, "Text"];

Print["Messages issued: ", Length[$MessageList], "   output in ", outDirSM$, ": ",
  FileNameTake /@ FileNames["*", outDirSM$]];


(* ::Subsubsection:: *)
(*Inspect: the start of the FeynArts model file SM_FA.mod*)


If[$Notebooks,
  StringTake[Import[modFileSM$, "Text"], UpTo[2500]]
]


SetDirectory[startDirSM$];
