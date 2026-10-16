(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: UV poles of the four-gluon vertex per diagram class*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices (FeynArts + FeynCalc).*)
(*  app:vertex 「3グルーオンと4グルーオンの頂点。」 (R8): the 54 one-loop diagrams of g g -> g g without tadpoles, self-energy insertions*)
(*  and reducible ones (generated/QCD_FA), in five classes (bubbles with two four-gluon vertices, triangles with one, ghost boxes, gluon*)
(*  boxes, quark boxes); the UV pole of each class (uvTaylor of oneloop_feyncalc.wl, general xi) projected onto the SU(3) colour structures*)
(*  f f (three orderings) and tr(T T T T) + reversed times the three metric structures, and the ratios to the same projections of the tree*)
(*  vertex (zero tree projections give Indeterminate ratios and the Power::infy messages, which are expected).  The diagrams are shown*)
(*  before they are evaluated (notebook).*)
(*Reads generated/QCD_FA (run_model_check.sh; copied to a temporary directory and patched there).  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_vertex_4g.txt.*)
(*Usage (from Src/): wolframscript -file deriv_vertex_4g.wl   (about 4 minutes)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_vertex_4g.wl  (after generate_QCD.wl; FeynCalc with FeynArts, in a kernel of its own).  Interactive:  ~/hep/bin/wopen deriv_vertex_4g.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
KK = (4 Pi)^2;


(* ::Section:: *)
(*uvTaylor (copied from Src/oneloop_feyncalc.wl)*)


DataType[tt, FCVariable] = True;
facDen$[PropagatorDenominator[mom_, m_], order_] := Module[{mm = MomentumExpand[mom], c, q, x},
   c = Coefficient[mm, Momentum[l, D]];
   q = Expand[mm - c Momentum[l, D]];
   If[q === 0, den$, x = 2 c Pair[Momentum[l, D], q] + Pair[q, q]; Sum[(-x)^n den$^(n + 1), {n, 0, order}]]];
uvTaylor$[amp_, moms_, order_] := Module[{y, res},
   y = SUNSimplify[DiracSimplify[FCI[amp]], SUNNToCACF -> True];
   y = FCI[y] /. (Momentum[#, D] -> Momentum[tt #, D] & /@ moms);
   y = y /. FeynAmpDenominator[pds__] :> Times @@ (facDen$[#, order] & /@ {pds});
   y = DiracGammaExpand[ExpandScalarProduct[MomentumExpand[y]]] /. DiracGamma[a_ Momentum[b_, D], D] :> a DiracGamma[Momentum[b, D], D];
   y = ExpandScalarProduct[y];
   res = If[order == 0, y /. tt -> 0, Coefficient[Expand[y], tt, order]];
   res = res /. den$^n_. :> FeynAmpDenominator @@ Table[PropagatorDenominator[Momentum[l, D], MM], {n}];
   res = TID[DiracSimplify[res], l, ToPaVe -> True];
   res = PaVeUVPart[FCI[res], Prefactor -> 1];
   Simplify[FCE[SUNSimplify[DiracSimplify[Contract[Normal[Series[res /. D -> 4 - 2 ep, {ep, 0, -1}]] /. ep -> 1]], SUNNToCACF -> True]]]];
(* uvTaylor/(Pi^2 K) is the pole of iGamma = Integral d^Dl/(2Pi)^D (integrand), in units of DUV *)


(* ::Section:: *)
(*(B) FeynArts diagrams of the project*)


srcDir = Which[StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName], $Notebooks, NotebookDirectory[], True, Directory[]];
tmpDir = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDir, "generated", "QCD_FA"}], FileNameJoin[{tmpDir, "QCD_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{tmpDir, "QCD_FA"}], Quiet -> True];
model = FileNameJoin[{tmpDir, "QCD_FA", "QCD_FA"}];
ins[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> model, GenericModel -> model,
   ExcludeParticles -> {V[1], F[1]}];
raw[diags_, in_, out_, lor_] := FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
    IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {l}, LorentzIndexNames -> lor, ChangeDimension -> D,
    List -> True, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI // MomentumExpand //
   ReplaceAll[#, {SMP["g_s"] -> gS, FCGV["GS"] -> gS, GaugeXi[V[2, ___]] -> xi, GaugeXi[G] -> xi, FCGV["MT"] -> mt, SMP["m_t"] -> mt}] &;


(* ::Section:: *)
(*the 54 diagrams of g g -> g g and the tree projections*)


t0 = AbsoluteTime[];
diagV4 = ins[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections, Reducible}], {V[2], V[2]} -> {V[2], V[2]}];


(* ::Subsubsection:: *)
(*Inspect: the 54 one-loop diagrams of g g -> g g (before they are evaluated)*)


If[$Notebooks,
  Show[#, ImageSize -> 760] & /@ Render[Paint[diagV4, ColumnsXRows -> {9, 6}, Numbering -> Simple, DisplayFunction -> Identity]]
]


rawV4 = raw[diagV4, {p1, p2}, {p3, p4}, {mu, nu, rho, si}];
nprops[x_] := Length[Union[Cases[FCI[x], PropagatorDenominator[mom_, _] :> MomentumExpand[mom], Infinity]]];
class4[x_] := Which[!FreeQ[x, DiracGamma] || !FreeQ[x, DiracTrace], "quark boxes",
   FreeQ[x, xi], "ghost boxes", nprops[x] >= 4, "gluon boxes", nprops[x] == 3, "triangles (one 4g vertex)", True, "bubbles (two 4g vertices)"];
cl4 = class4 /@ rawV4;
Print["(R8-4g) ", Length[rawV4], " diagrams; classes: ", Tally[cl4]];
tree4 = FCE[ChangeDimension[SUNSimplify[FCI[First[raw[ins[CreateTopologies[0, 2 -> 2, Adjacencies -> {4}], {V[2], V[2]} -> {V[2], V[2]}],
        {p1, p2}, {p3, p4}, {mu, nu, rho, si}]]]], 4]];
cols = {SUNF[Glu1, Glu2, hh] SUNF[Glu3, Glu4, hh], SUNF[Glu1, Glu3, hh] SUNF[Glu2, Glu4, hh], SUNF[Glu1, Glu4, hh] SUNF[Glu2, Glu3, hh],
   SUNTrace[SUNT[Glu1, Glu2, Glu3, Glu4]] + SUNTrace[SUNT[Glu4, Glu3, Glu2, Glu1]]};
lors = {MT[mu, nu] MT[rho, si], MT[mu, rho] MT[nu, si], MT[mu, si] MT[nu, rho]};
proj4[x_, c_, lo_] := Simplify[SUNSimplify[Contract[FCI[x c lo]], SUNNToCACF -> False, Explicit -> True] /. SUNN -> 3];
treeP = Table[proj4[gS^2/KK tree4, c, lo], {c, cols}, {lo, lors}];
Print["(R8-4g) tree projections (units g^2/K x gS^2...): ", InputForm[Simplify[treeP]]];


(* ::Subsubsection:: *)
(*Inspect: the tree projections onto the colour (rows) and metric (columns) structures*)


If[$Notebooks,
  treeP // MatrixForm
]


(* ::Section:: *)
(*the UV pole of each class, projected*)


Do[sel = Pick[rawV4, cl4, cl];
  t1 = AbsoluteTime[];
  pole = Sum[uvTaylor$[x, {p1, p2, p3, p4}, 0], {x, sel}]/(Pi^2 KK);
  P = Table[proj4[pole, c, lo], {c, cols}, {lo, lors}];
  ratios = Simplify[Flatten[P]/Flatten[treeP]];
  Print["(R8-4g) ", cl, " (", Length[sel], "): projections ", InputForm[Simplify[P/(gS^4/KK)]], "  ratios to tree ", InputForm[ratios], "  [", Round[AbsoluteTime[] - t1], " s]"],
  {cl, {"bubbles (two 4g vertices)", "triangles (one 4g vertex)", "ghost boxes", "gluon boxes", "quark boxes"}}];
Print["(R8-4g) done in ", Round[AbsoluteTime[] - t0], " s"];