(* ::Package:: *)

(* ::Title:: *)
(*Appendix check: UV poles of the quark vertex (d1), (d2) and of the three-gluon vertex per diagram class*)


(* ::Text:: *)
(*Research note models/qcd, derivations of the appendices (FeynArts + FeynCalc).*)
(*  app:vertex 「クォークの頂点。」 (R7) and 「3グルーオンの頂点の図の種類ごとの極。」 with tab:v3class (R8).*)
(*  (A) Hand-coded amplitudes from the Feynman rules of fig:rules: UV poles of the quark-vertex diagrams (d1), (d2) at zero external*)
(*      momenta, and of the three-gluon vertex per diagram class (gluon triangle, the two ghost triangles, three bubbles with a four-gluon*)
(*      vertex, quark triangles) in general xi, by first-order Taylor expansion in the external momenta + infrared rearrangement (every*)
(*      denominator -> l^2 - MM), TID, PaVeUVPart.*)
(*  (B) The same classes from the FeynArts diagrams of the project (generated/QCD_FA, 18 diagrams), classified by their content, with the*)
(*      uvTaylor routine of oneloop_feyncalc.wl.  The diagrams are shown before they are evaluated (notebook).*)
(*  Normalisation: iGamma^(1)_pole = c (g^2/K) DUV (tree vertex rule); the printed number is c.*)
(*Reads generated/QCD_FA (run_model_check.sh; copied to a temporary directory and patched there).  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_vertex_d1_v3.txt.*)
(*Usage (from Src/): wolframscript -file deriv_vertex_d1_v3.wl   (about 2 minutes)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file deriv_vertex_d1_v3.wl  (after generate_QCD.wl; FeynCalc with FeynArts, in a kernel of its own).  Interactive:  ~/hep/bin/wopen deriv_vertex_d1_v3.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


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
(*(A) Feynman rules of fig:rules (all momenta incoming at 3g vertex; eta = 1 - xi)*)


V3[{a_, mu_, k_}, {b_, nu_, p_}, {c_, rho_, q_}] := gS SUNF[a, b, c] (MTD[mu, nu] (FVD[k, rho] - FVD[p, rho]) +
     MTD[nu, rho] (FVD[p, mu] - FVD[q, mu]) + MTD[rho, mu] (FVD[q, nu] - FVD[k, nu]));
GP[{a_, al_}, {b_, be_}, k_] := -I SUNDelta[a, b] (MTD[al, be] FAD[k] - eta FVD[k, al] FVD[k, be] FAD[k, k]);
CP[a_, b_, k_] := I SUNDelta[a, b] FAD[k];
(* ghost vertex: aout outgoing ghost with outgoing momentum pout, bin incoming ghost, gluon (c, mu) *)
GV[aout_, bin_, {c_, mu_}, pout_] := gS SUNF[aout, bin, c] FVD[pout, mu];
V4[{a_, mu_}, {b_, nu_}, {c_, rho_}, {d_, si_}, e_] := -I gS^2 (
    SUNF[a, b, e] SUNF[c, d, e] (MTD[mu, rho] MTD[nu, si] - MTD[mu, si] MTD[nu, rho]) +
    SUNF[a, c, e] SUNF[b, d, e] (MTD[mu, nu] MTD[rho, si] - MTD[mu, si] MTD[nu, rho]) +
    SUNF[a, d, e] SUNF[b, c, e] (MTD[mu, nu] MTD[rho, si] - MTD[mu, rho] MTD[nu, si]));

(* minus the momenta (FVD of a sum) *)
mexp[x_] := MomentumExpand[FCI[x]];


(* ::Section:: *)
(*R7: quark vertex at zero external momenta; quark (i -> j), external gluon (a, mu)*)


(* (d1): gluon b (momentum l) emitted from the incoming quark line and absorbed on the outgoing line; quark momenta -l.
   iGamma = (ig g^rho T^b) iS(-l) (ig g^mu T^a) iS(-l) (ig g^sigma T^b) (-i)P_{rho sigma}(l)/l^2 *)
qprop[k_] := I (-GSD[l]) FAD[l];   (* i S(-l) for a massless quark; the pole does not depend on the mass *)
d1 = SUNT[b, a, b] (I gS)^3 GAD[rho] . qprop[l] . GAD[mu] . qprop[l] . GAD[si] *
     (-I) (MTD[rho, si] FAD[l] - eta FVD[l, rho] FVD[l, si] FAD[l, l]);
rawd1 = uvTaylor$[d1, {}, 0]/(Pi^2 KK); Print["(R7) raw (d1) pole: ", InputForm[rawd1]];
pole$d1 = Simplify[rawd1/(I gS^3/KK GA[mu] SUNT[a]) /. eta -> 1 - xi];
(* (d2): quark line l (between the two quark-gluon vertices), gluons b (momentum -l into the 3g vertex... ) *)
(* external gluon (a, mu, 0) splits at the 3g vertex into internal gluons b (momentum l flowing out of the 3g vertex
   to the outgoing-quark vertex) and c (momentum -l flowing out to the incoming-quark vertex) *)
d2 = SUNT[c1, b1] (I gS)^2 GAD[sig] . (I GSD[l] FAD[l]) . GAD[rh] *
     GP[{b1, rh}, {b2, be}, l] GP[{c1, sig}, {c2, ga}, l] V3[{a, mu, pz}, {b2, be, -l}, {c2, ga, l}];
(* check of the momentum routing: incoming quark p=0 emits gluon c with momentum -l?  The quark between the vertices
   carries l; gluon c carries 0 - l = -l from the incoming-quark vertex into the 3g vertex, i.e. momentum l out of the
   3g vertex... the 3g vertex momenta incoming: external 0, b2: -l (b leaves with l), c2: +l (c arrives with l). *)
rawd2 = uvTaylor$[d2, {pz}, 0]/(Pi^2 KK); Print["(R7) raw (d2) pole: ", InputForm[rawd2]];
pole$d2 = Simplify[rawd2/(I gS^3/KK GA[mu] SUNT[a]) /. eta -> 1 - xi];
Print["(R7) quark vertex: (d1) pole/(g^2/K) = ", InputForm[Simplify[pole$d1 /. SUNN -> CA]],
  "   (expect (CF - CA/2) xi = ", InputForm[Simplify[(SUNN^2 - 1)/(2 SUNN) - SUNN/2] xi], ")"];
Print["(R7) quark vertex: (d2) pole/(g^2/K) = ", InputForm[Simplify[pole$d2]], "   (expect 3 CA (1 + xi)/4)"];


(* ::Subsubsection:: *)
(*Inspect: the UV poles of (d1) and (d2) in units g^2 DUV/K (SUNN = C_A)*)


If[$Notebooks,
  {pole$d1, pole$d2}
]


(* ::Section:: *)
(*R8: 3-gluon vertex, external (a,mu,p1), (b,nu,p2), (c,rho,p3), p3 = -p1 - p2, all incoming*)


tree3 = ChangeDimension[V3[{a, mu, p1}, {b, nu, p2}, {c, rho, -p1 - p2}] // mexp // ExpandScalarProduct, 4];


(* ::Subsubsection:: *)
(*Inspect: the tree three-gluon vertex (4 dimensions)*)


If[$Notebooks,
  tree3
]


(* gluon triangle: lines A<-C: l (into A), A->B: l+p1, B->C: l+p1+p2.  Vertex A: ext a, line CA (momentum l in),
   line AB (momentum -(l+p1) in).  Symmetry factor 1. *)
triG = V3[{a, mu, p1}, {x1, al1, l}, {x2, al2, -l - p1}] V3[{b, nu, p2}, {y2, be2, l + p1}, {y3, be3, -l - p1 - p2}] *
   V3[{c, rho, -p1 - p2}, {z3, ga3, l + p1 + p2}, {z1, ga1, -l}] *
   GP[{x1, al1}, {z1, ga1}, l] GP[{x2, al2}, {y2, be2}, l + p1] GP[{y3, be3}, {z3, ga3}, l + p1 + p2];
(* ghost triangles, factor -1 each.  Orientation 1: ghost C -> A -> B -> C with momenta l, l+p1, l+p1+p2.
   Vertex A: outgoing ghost x2 (momentum l+p1 out), incoming x1, gluon a. *)
CPn[k_] := I FAD[k];
triC1 = - GV[x2, x1, {a, mu}, l + p1] GV[x3, x2, {b, nu}, l + p1 + p2] GV[x1, x3, {c, rho}, l] CPn[l] CPn[l + p1] CPn[l + p1 + p2];
(* orientation 2: ghost flows A -> C -> B -> A.  Line A->C momentum -l (i.e. l from C to A reversed), line C->B
   momentum -l-p1-p2, line B->A momentum -l-p1.  Vertex A: outgoing ghost (A->C) y3, momentum -l; incoming (B->A) y2. *)
triC2 = - GV[y3, y2, {a, mu}, -l] GV[y2, y1, {b, nu}, -l - p1] GV[y1, y3, {c, rho}, -l - p1 - p2] CPn[-l] CPn[-l - p1] CPn[-l - p1 - p2];
(* bubbles, symmetry factor 1/2: the leg X attaches to a 3g vertex, the other two to the 4g vertex.
   Lines: from the 3g vertex to the 4g vertex momentum l (in at 4g), back with l + P (P = sum of the two 4g legs). *)
bub[{{ea_, ma_, pa_}, {eb_, mb_, pb_}}, {ec_, mc_, pc_}] := 1/2 V4[{ea, ma}, {eb, mb}, {u1, al1}, {u2, al2}, ee] *
   V3[{ec, mc, pc}, {v2, be2, l + pa + pb}, {v1, be1, -l}] GP[{u1, al1}, {v1, be1}, l] GP[{u2, al2}, {v2, be2}, l + pa + pb];
bubs = bub[{{a, mu, p1}, {b, nu, p2}}, {c, rho, -p1 - p2}] + bub[{{b, nu, p2}, {c, rho, -p1 - p2}}, {a, mu, p1}] +
   bub[{{c, rho, -p1 - p2}, {a, mu, p1}}, {b, nu, p2}];
(* quark triangle (massless; the pole does not depend on the mass), factor -1, two orientations.
   Orientation 1: quark C -> A -> B -> C with momenta l, l+p1, l+p1+p2:  -tr[V_A S(l) V_C S(l+p1+p2) V_B S(l+p1)] *)
SQ[k_] := I GSD[k] FAD[k];
triQ1 = - SUNTrace[SUNT[a, c, b]] DiracTrace[(I gS GAD[mu]) . SQ[l] . (I gS GAD[rho]) . SQ[l + p1 + p2] . (I gS GAD[nu]) . SQ[l + p1]];
triQ2 = - SUNTrace[SUNT[a, b, c]] DiracTrace[(I gS GAD[mu]) . SQ[-l - p1] . (I gS GAD[nu]) . SQ[-l - p1 - p2] . (I gS GAD[rho]) . SQ[-l]];

prep[x_] := Module[{y = mexp[x]},
   y = y /. DiracTrace[z_] :> DiracTrace[z, DiracTraceEvaluate -> True];
   y];
coef3[x_] := Module[{pole, cc, diff},
   pole = uvTaylor$[prep[x], {p1, p2}, 1]/(Pi^2 KK);
   pole = FCE[SUNSimplify[FCI[pole], SUNNToCACF -> True, Explicit -> True]];
   (* extract c: contract with g_{mu nu} r_rho, coefficient of r.p1 *)
   cc = Simplify[Coefficient[FCE[ExpandScalarProduct[Contract[FCI[pole] MT[mu, nu] FV[r, rho]]]] /. SUNF[a, b, c] -> 1, SP[p1, r]] /
      Coefficient[FCE[ExpandScalarProduct[Contract[FCI[gS^2/KK tree3] MT[mu, nu] FV[r, rho]]]] /. SUNF[a, b, c] -> 1, SP[p1, r]]];
   diff = Simplify[ExpandScalarProduct[FCI[pole - cc gS^2/KK tree3]]];
   {Simplify[cc /. eta -> 1 - xi /. SUNN -> CA], diff}];

t0 = AbsoluteTime[];
resG = coef3[triG]; Print["(R8 hand) gluon triangle: c = ", InputForm[resG[[1]]], ",  pole - c tree = ", resG[[2]], "  [", Round[AbsoluteTime[] - t0], " s]"];
resC = coef3[triC1 + triC2]; Print["(R8 hand) ghost triangles (2): c = ", InputForm[resC[[1]]], ",  pole - c tree = ", resC[[2]]];
resC1 = coef3[triC1]; Print["(R8 hand) ghost triangle, orientation 1 alone: c = ", InputForm[resC1[[1]]], ",  pole - c tree = ", resC1[[2]]];
resB = coef3[bubs]; Print["(R8 hand) bubbles with a 4g vertex (3): c = ", InputForm[resB[[1]]], ",  pole - c tree = ", resB[[2]]];
resQ = coef3[triQ1 + triQ2]; Print["(R8 hand) quark triangles (2 orientations, one flavour): c = ", InputForm[resQ[[1]]], ",  pole - c tree = ", resQ[[2]]];
tot = Simplify[resG[[1]] + resC[[1]] + resB[[1]]];
Print["(R8 hand) gluon + ghost + bubbles = ", InputForm[Expand[tot]], "   (expect CA (3 xi/4 - 17/12))"];


(* ::Subsubsection:: *)
(*Inspect: c per class: gluon triangle, ghost triangles, bubbles, quark triangles (one flavour)*)


If[$Notebooks,
  {resG[[1]], resC[[1]], resB[[1]], resQ[[1]]}
]


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
topV = CreateTopologies[1, 2 -> 1, ExcludeTopologies -> {Tadpoles, WFCorrections}];
diagV3 = ins[topV, {V[2], V[2]} -> {V[2]}];


(* ::Subsubsection:: *)
(*Inspect: the 18 one-loop diagrams of the three-gluon vertex (before they are evaluated)*)


If[$Notebooks,
  Show[#, ImageSize -> 760] & /@ Render[Paint[diagV3, ColumnsXRows -> {6, 3}, Numbering -> Simple, DisplayFunction -> Identity]]
]


rawV3 = raw[diagV3, {p1, p2}, {p3}, {mu, nu, rho}] /. Momentum[p3, D] -> Momentum[p1, D] + Momentum[p2, D] // MomentumExpand;
treeFA = FCE[ChangeDimension[ExpandScalarProduct[MomentumExpand[FCI[First[raw[ins[CreateTopologies[0, 2 -> 1], {V[2], V[2]} -> {V[2]}],
         {p1, p2}, {p3}, {mu, nu, rho}]] /. Momentum[p3, D] -> Momentum[p1, D] + Momentum[p2, D]]]], 4]];
nprops[x_] := Length[Union[Cases[FCI[x], PropagatorDenominator[mom_, _] :> MomentumExpand[mom], Infinity] /.
      Momentum[q_, D] :> Momentum[q, D]]];
classFA[x_] := Which[!FreeQ[x, DiracGamma] || !FreeQ[x, DiracTrace], "quark",
   FreeQ[x, xi], "ghost", nprops[x] >= 3, "gluon triangle", True, "bubble"];
classes = classFA /@ rawV3;
Print["(R8 FeynArts) ", Length[rawV3], " diagrams; classes: ", Tally[classes]];
Print["(R8 FeynArts) distinct propagator momenta per diagram: ", nprops /@ rawV3];


(* ::Subsubsection:: *)
(*Inspect: the class of each FeynArts diagram and the FeynArts tree vertex*)


If[$Notebooks,
  {classes, treeFA}
]


(* tree from FeynArts in FA's momentum convention: g(p1)+g(p2) -> g(p3) *)
coefFA[list_] := Module[{pole, cc, diff},
   pole = Sum[uvTaylor$[x, {p1, p2}, 1], {x, list}]/(Pi^2 KK);
   pole = FCE[SUNSimplify[FCI[pole], SUNNToCACF -> True, Explicit -> True]];
   cc = Simplify[Coefficient[FCE[ExpandScalarProduct[Contract[FCI[pole] MT[mu, nu] FV[r, rho]]]] /. SUNF[Glu1, Glu2, Glu3] -> 1, SP[p1, r]] /
      Coefficient[FCE[ExpandScalarProduct[Contract[FCI[gS^2/KK treeFA] MT[mu, nu] FV[r, rho]]]] /. SUNF[Glu1, Glu2, Glu3] -> 1, SP[p1, r]]];
   diff = Simplify[ExpandScalarProduct[FCI[pole - cc gS^2/KK treeFA]] /. SUNN -> CA];
   {Simplify[cc /. SUNN -> CA], diff}];
Do[selFA = Pick[rawV3, classes, cl];
  resFA = coefFA[selFA];
  Print["(R8 FeynArts) ", cl, " (", Length[selFA], " diagrams): c = ", InputForm[resFA[[1]]], ",  pole - c tree = ", resFA[[2]]],
  {cl, {"gluon triangle", "ghost", "bubble", "quark"}}];
Print["(R8) done in ", Round[AbsoluteTime[] - t0], " s"];