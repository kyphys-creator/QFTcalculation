(* ::Package:: *)

(* ::Title:: *)
(*Step (3): one-loop 1PI functions of QCD in a general covariant gauge (FeynArts + FeynCalc, Package-X, LoopTools)*)


(* ::Text:: *)
(*Research note models/qcd, step (3).  Compares with Eqs. (5) (eq:V), (6) (eq:Vpole), (7) (eq:ct), (8) (eq:VR) and (4) (eq:st).*)
(*(a) FeynArts 1PI diagrams from Src/generated/QCD_FA (photon and electron excluded), GaugeRules -> {} keeps xi:*)
(*    gluon 2-point 9 (seagull, 6 quark loops, ghost loop, gluon loop), ghost 2-point 1, u and t self-energies 1 each,*)
(*    quark-gluon vertex 2 (u and t), ghost vertex 2, three-gluon vertex 18, four-gluon vertex 54.*)
(*    With PreFactor -> 1 the amplitude is A = (2 Pi)^D V and TID writes A = I Pi^2 X with X built from PaVe functions:*)
(*      gluon: V = i Pi^{mu nu},  X = K Pi^{mu nu};   ghost: V = i p^2 Pitilde,  X = K p^2 Pitilde;   quark: V = -i Sigma, X = -K Sigma*)
(*    (K = (4 Pi)^2).  Doubled massless propagators are reduced by the IBP relations of App. E,*)
(*    I(2,1) = -(D-3)/k^2 I(1,1), I(2,2) = (D-3)(D-6)/k^4 I(1,1); the doubled gluon propagator of the t self-energy by the*)
(*    QED-note relation J12 = [(D-2) A0 - (D-3)(m^2 + p^2) B0]/(m^2 - p^2)^2.*)
(*(b) Two-point functions exact in D dimensions: each diagram contracted with g_{mu nu} and k_mu k_nu (App. E), the sum*)
(*    transverse, Pi, Pitilde, Sigma = Eq. (5) symbolically.*)
(*(c) UV poles of the four vertices by Taylor expansion in the external momenta and infrared rearrangement (every*)
(*    denominator -> l^2 - MM): quark-gluon (u and t, per diagram), ghost (per diagram), three-gluon (order 1),*)
(*    four-gluon (order 0, projected on the colour x Lorentz basis); counterterms Eq. (7); Slavnov-Taylor Eq. (4): delta_g*)
(*    from all four vertices.  Also: the same poles from TID at general momenta with PaVeUVPart (the pre-check found a wrong*)
(*    gauge part for the abelian quark-vertex diagram, note Sec. 4).*)
(*(d) MS-bar finite parts at g = 1, m = mu = 1 from Package-X and LoopTools -> results/oneloop_mathematica.csv*)
(*    (oneloop_numeric.py compares them with COLLIER and mpmath integrals of Eq. (8)).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_feyncalc.wl  (run generate_QCD.wl first).  Interactive:  ~/hep/bin/wopen oneloop_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).  The four-gluon section takes most of the time.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader", "FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;

srcDirOL$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirOL$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirOL$, "generated", "QCD_FA"}], FileNameJoin[{modelTmpDirOL$, "QCD_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirOL$, "QCD_FA"}], Quiet -> True];
modelOL$ = FileNameJoin[{modelTmpDirOL$, "QCD_FA", "QCD_FA"}];
KK = (4 Pi)^2;
TF = 1/2;


(* ::Text:: *)
(*Helpers.  Field codes: V[2] gluon, U[1] ghost, F[2] u, F[7] t (photon V[1] and electron F[1] excluded).  FCFAConvert*)
(*writes the coupling as SMP["g_s"] (renamed gS: GS is FeynCalc's slash) and the gauge parameter of an internal gluon as*)
(*GaugeXi[V[2, {colour}]] (renamed xi: the colour index would otherwise appear three times).  eta = 1 - xi.*)


insOL$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelOL$, GenericModel -> modelOL$,
   ExcludeParticles -> {V[1], F[1]}];
rawOL$[diags_, in_, out_, lor_] := FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1, GaugeRules -> {}] /. M$FACouplings,
    IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {l}, LorentzIndexNames -> lor, ChangeDimension -> D,
    List -> True, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True] // FCI // MomentumExpand //
   ReplaceAll[#, {SMP["g_s"] -> gS, FCGV["GS"] -> gS, GaugeXi[V[2, ___]] -> xi, GaugeXi[G] -> xi, FCGV["MT"] -> mt, SMP["m_t"] -> mt}] &;
redOL$[x_] := FCE[SUNSimplify[DiracSimplify[FeynAmpDenominatorExplicit[TID[SUNSimplify[DiracSimplify[x], SUNNToCACF -> True], l,
        ToPaVe -> True]]], SUNNToCACF -> True]] /. {SD[__] -> 1, SDF[__] -> 1, SUNDelta[__] -> 1, SUNFDelta[__] -> 1};
(* IBP: massless I(2,1), I(2,2); massive doubled gluon propagator (QED note App. D) *)
ibpOL$ = {PaVe[0, {0, qq_, qq_}, {0, 0, 0}] :> -(D - 3)/qq B0[qq, 0, 0], C0[0, qq_, qq_, 0, 0, 0] :> -(D - 3)/qq B0[qq, 0, 0],
   PaVe[0, {0, qq_, 0, qq_, qq_, qq_}, {0, 0, 0, 0}] :> (D - 3) (D - 6)/qq^2 B0[qq, 0, 0],
   C0[0, pp_, pp_, 0, 0, m2_] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2,
   PaVe[0, {0, pp_, pp_}, {0, 0, m2_}] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2,
   PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {qq_}, {ma_, mb_}] :> B0[qq, ma, mb],
   B0[qq_, 0, m2_] /; m2 =!= 0 :> B0[qq, m2, 0]};
fullRed$[x_] := Simplify[PaVeReduce[x] //. ibpOL$ /. {B0[0, 0, 0] -> 0, A0[0] -> 0}];


(* ::Section:: *)
(*(a) diagrams*)


topSE$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];
diagG$ = insOL$[topSE$, {V[2]} -> {V[2]}];
diagC$ = insOL$[topSE$, {U[1]} -> {U[1]}];
diagU$ = insOL$[topSE$, {F[2]} -> {F[2]}];
diagT$ = insOL$[topSE$, {F[7]} -> {F[7]}];
topV$ = CreateTopologies[1, 2 -> 1, ExcludeTopologies -> {Tadpoles, WFCorrections}];
diagVu$ = insOL$[topV$, {F[2], V[2]} -> {F[2]}];
diagVt$ = insOL$[topV$, {F[7], V[2]} -> {F[7]}];
diagVc$ = insOL$[topV$, {U[1], V[2]} -> {U[1]}];
diagV3$ = insOL$[topV$, {V[2], V[2]} -> {V[2]}];
diagV4$ = insOL$[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections, Reducible}], {V[2], V[2]} -> {V[2], V[2]}];


(* ::Subsubsection:: *)
(*Inspect: the two-point diagrams (gluon, ghost, u, t)*)


If[$Notebooks,
  {Show[#, ImageSize -> 600] & /@ Render[Paint[diagG$, ColumnsXRows -> {5, 2}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 160] & /@ Render[Paint[diagC$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 160] & /@ Render[Paint[diagU$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 160] & /@ Render[Paint[diagT$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]]}
]


(* ::Subsubsection:: *)
(*Inspect: the vertex diagrams (u-gluon, ghost, three-gluon; the 54 four-gluon diagrams in 5 pages)*)


If[$Notebooks,
  {Show[#, ImageSize -> 320] & /@ Render[Paint[diagVu$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 320] & /@ Render[Paint[diagVc$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 600] & /@ Render[Paint[diagV3$, ColumnsXRows -> {6, 3}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 600] & /@ Render[Paint[diagV4$, ColumnsXRows -> {6, 2}, Numbering -> Simple, DisplayFunction -> Identity]]}
]


nDiag$ = Length[CreateFeynAmp[#]] & /@ {diagG$, diagC$, diagU$, diagT$, diagVu$, diagVt$, diagVc$, diagV3$, diagV4$};
Print["(a) number of 1PI diagrams: gluon, ghost, u, t, u-vertex, t-vertex, ghost vertex, 3g, 4g = ", nDiag$,
  "   (expect {9, 1, 1, 1, 2, 2, 2, 18, 54})"];


(* ::Section:: *)
(*(b) two-point functions in D dimensions*)


(* ::Text:: *)
(*Gluon: each diagram is contracted with g_{mu nu} and k_mu k_nu and divided by (g^2 C_A/K) times (D-1) k^2 B0 and k^4 B0*)
(*(the quark loops by g^2/K).  Expected (App. E): gluon loop {3/2 + (2D-7) eta/2 - (D-4) eta^2/8, -1/4}, ghost loop*)
(*{1/(2(D-1)), 1/4}, seagull {0, 0}; massless quark loop (per flavour) -T_F 2(D-2)/(D-1) B0 and 0; the t loop T_F x QED.*)


FCClearScalarProducts[]; ScalarProduct[q, q] = qq;
rawG$ = rawOL$[diagG$, {q}, {q}, {mu, nu}] /. xi -> 1 - eta;
redG$ = redOL$ /@ rawG$;
projOL$[x_] := {fullRed$[Contract[FCI[x] MTD[mu, nu]] /. SPD[q, q] -> qq], fullRed$[Contract[FCI[x] FVD[q, mu] FVD[q, nu]] /. SPD[q, q] -> qq]};
projG$ = projOL$ /@ redG$;
classG$[x_] := Which[!FreeQ[x, eta], "gluon loop", !FreeQ[x, DiracTrace] || !FreeQ[x, mt] && FreeQ[x, CA], "quark loop",
   FreeQ[x, CA], "quark loop", True, "ghost or seagull"];
Do[With[{pr = projG$[[i]]},
   Print["(b) gluon diagram ", i, ": g-contraction/(I Pi^2 g^2 (D-1) qq), kk-contraction/(I Pi^2 g^2 qq^2) = ",
    InputForm[Simplify[{pr[[1]]/(I Pi^2 gS^2 (D - 1) qq), pr[[2]]/(I Pi^2 gS^2 qq^2)}]]]], {i, Length[projG$]}];
totG$ = Total[projG$];
Print["(b) gluon: k_mu k_nu Pi^{mu nu} summed over diagrams (expect 0): ", Simplify[totG$[[2]]]];
PiOL$ = Simplify[totG$[[1]]/(I Pi^2 KK (D - 1) qq)];
PiQED$[m2_] := gS^2/KK 2/((D - 1) qq) (2 (D - 2) A0[m2] - (4 m2 + (D - 2) qq) B0[qq, m2, m2]);
PiNote$ = gS^2/KK (CA/2 ((3 D - 2)/(D - 1) + (2 D - 7) eta - (D - 4)/4 eta^2) B0[qq, 0, 0]) + TF (5 PiQED$[0] + PiQED$[mt^2]) /. A0[0] -> 0;
Print["(b) gluon: Pi - Eq. (5) = ", Simplify[PiOL$ - PiNote$], "   (expect 0; n_l = 5 massless + t)"];


(* ::Text:: *)
(*Ghost: X = K p^2 Pitilde.  Eq. (5): Pitilde = -(g^2 C_A/K)[1/2 + (D-3) eta/4] B0(p^2; 0, 0).*)


FCClearScalarProducts[]; ScalarProduct[p, p] = pp;
ampC$ = Total[redOL$ /@ (rawOL$[diagC$, {p}, {p}, {mu}] /. xi -> 1 - eta)];
PitOL$ = Simplify[fullRed$[ampC$ /. SPD[p, p] -> pp]/(I Pi^2 KK pp)];
Print["(b) ghost: Pitilde - Eq. (5) = ", Simplify[PitOL$ + gS^2 CA/KK (1/2 + (D - 3) eta/4) B0[pp, 0, 0]], "   (expect 0)"];


(* ::Text:: *)
(*Quarks: X = -K Sigma.  Eq. (5): Sigma = C_F (g^2/K)[xi (D-2) pslash B1(p^2; m^2, 0) + (D-1+xi) m B0(p^2; m^2, 0)];*)
(*for the massless u, B1(p^2; 0, 0) = -B0/2 and the m term is absent.*)


sigOL$[diag_, m_] := Module[{x = Total[redOL$ /@ rawOL$[diag, {p}, {p}, {mu}]], g = GSD[p], a, b},
   x = Expand[fullRed$[x /. SPD[p, p] -> pp]/(I Pi^2)];
   a = Coefficient[x, g]; b = Simplify[x - a g];
   {-a/KK, If[m === 0, -b/KK, -b/(KK m)]}];     (* {Sigma_V, Sigma_S} *)
{sVu$, sSu$} = sigOL$[diagU$, 0];
{sVt$, sSt$} = sigOL$[diagT$, mt];
b1Rule$ = B1[pp_, m2_, 0] :> (A0[m2] - (pp + m2) B0[pp, m2, 0])/(2 pp);
Print["(b) u: Sigma_V - Eq. (5) = ", Simplify[sVu$ - CF gS^2/KK xi (D - 2) (-1/2) B0[pp, 0, 0]], ",  Sigma_S = ", sSu$, "   (expect 0, 0)"];
Print["(b) t: Sigma_V - Eq. (5) = ", Simplify[sVt$ - (CF gS^2/KK xi (D - 2) B1[pp, mt^2, 0] /. b1Rule$)],
  ",  Sigma_S - Eq. (5) = ", Simplify[sSt$ - CF gS^2/KK (D - 1 + xi) B0[pp, mt^2, 0]], "   (expect 0, 0)"];


(* ::Section:: *)
(*(c) poles, counterterms and the Slavnov-Taylor identities*)


(* ::Text:: *)
(*Poles of the two-point functions from (b): B0 -> 1/eps, A0(m^2) -> m^2/eps, D -> 4 - 2 eps; the coefficient of 1/eps*)
(*times g^2/K is the coefficient of DUV.  delta3 = pole(Pi), delta3tilde = -pole(Pitilde), delta2 = pole(Sigma_V)*)
(*... with the sign of the counterterm insertions of Fig. 1: i[delta2 pslash - (delta2 + delta_m) m] + (-i Sigma) finite.*)


poleOL$[x_] := Simplify[SeriesCoefficient[x /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep} /. D -> 4 - 2 ep, {ep, 0, -1}]/(gS^2/KK)];
d3$ = poleOL$[PiOL$]; d3t$ = -poleOL$[PitOL$];
d2$ = poleOL$[sVt$]; dm$ = Simplify[-poleOL$[sSt$] - d2$];
Print["(c) delta3, delta3tilde, delta2, delta_m in units of g^2 DUV/K: ", InputForm[{d3$, d3t$, d2$, dm$} /. eta -> 1 - xi // Simplify],
  "   (expect {(13/6 - xi/2) CA - 4 (4/3 T_F n_f = 4 for n_f = 6), (3 - xi) CA/4, -xi CF, -3 CF})"];


(* ::Text:: *)
(*UV poles of the vertices.  uvTaylor expands every propagator 1/((c l + q)^2 - m^2) to the given order in the external*)
(*momentum q (tracked by tt) and replaces every denominator by l^2 - MM (infrared rearrangement); the coefficient of*)
(*1/eps of A/(Pi^2 K) is V_pole/(g^2/K) in units of the tree vertex.*)


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


(* ::Text:: *)
(*Quark-gluon vertex q(p1) + g(k1, Glu2) -> q(p2): tree i g gamma^mu T^a; per diagram (abelian, non-abelian).*)


FCClearScalarProducts[];
colQ$ = SUNTF[{Glu2}, Col3, Col1];
Do[Module[{r = rawOL$[d[[1]], {p1, k1}, {p2}, {mu}], per},
    per = Simplify[uvTaylor$[#, {p1, k1, p2}, 0]/(Pi^2 KK)/(I gS^3/KK GA[mu] colQ$)] & /@ r;
    Print["(c) ", d[[2]], "-gluon vertex: Lambda_F pole per diagram ", InputForm[per], ", total ", InputForm[Simplify[Total[per] /. CF -> (CA^2 - 1)/(2 CA)]],
     "   (expect (CF - CA/2) xi + 3 CA (1 + xi)/4 = ", InputForm[Simplify[xi (CA^2 - 1)/(2 CA) + (3 + xi) CA/4]], ")"]],
  {d, {{diagVu$, "u"}, {diagVt$, "t"}}}];
lamF$ = xi CF + (3 + xi) CA/4;


(* ::Text:: *)
(*Ghost vertex c(p1, Glu1) + g(k1, Glu2) -> c(p2, Glu3): tree g f^{Glu1 Glu2 Glu3} p2^mu (k1 = p2 - p1); order 1 in p1, p2.*)


rawVc$ = rawOL$[diagVc$, {p1, k1}, {p2}, {mu}] /. Momentum[k1, D] -> Momentum[p2, D] - Momentum[p1, D] // MomentumExpand;
perC$ = Simplify[uvTaylor$[#, {p1, p2}, 1]/(Pi^2 KK)/(gS^3/KK FV[p2, mu] SUNF[Glu1, Glu2, Glu3])] & /@ rawVc$;
Print["(c) ghost vertex: Lambdatilde pole per diagram ", InputForm[perC$], ", total ", InputForm[Simplify[Total[perC$]]],
  "   (expect xi CA/8 + 3 xi CA/8 = xi CA/2)"];
lamC$ = Simplify[Total[perC$]];


(* ::Text:: *)
(*Three-gluon vertex g(p1, Glu1, mu) + g(p2, Glu2, nu) -> g(p3 = p1 + p2, Glu3, rho), order 1; compared with c3 x tree.*)


rawV3$ = rawOL$[diagV3$, {p1, p2}, {p3}, {mu, nu, rho}] /. Momentum[p3, D] -> Momentum[p1, D] + Momentum[p2, D] // MomentumExpand;
pole3$ = Sum[uvTaylor$[rawV3$[[i]], {p1, p2}, 1], {i, Length[rawV3$]}]/(Pi^2 KK);
tree3$ = FCE[ChangeDimension[ExpandScalarProduct[MomentumExpand[FCI[First[rawOL$[insOL$[CreateTopologies[0, 2 -> 1], {V[2], V[2]} -> {V[2]}],
         {p1, p2}, {p3}, {mu, nu, rho}]] /. Momentum[p3, D] -> Momentum[p1, D] + Momentum[p2, D]]]], 4]];
lam3$ = Simplify[(pole3$ /. SUNN -> CA)/(gS^2/KK) /. tree3$ -> T3];   (* placeholder: compared below by subtraction *)
c3$ = CA (3 xi/4 - 17/12) + 4/3 TF 6;
Print["(c) three-gluon vertex: pole - (g^2/K)(CA (3 xi/4 - 17/12) + 4/3 T_F n_f) x tree = ",
  Simplify[ExpandScalarProduct[FCI[pole3$ - gS^2/KK c3$ tree3$]] /. SUNN -> CA], "   (expect 0; n_f = 6)"];


(* ::Text:: *)
(*Four-gluon vertex, order 0 (all external momenta 0).  The pole is projected on the colour structures f^{abe}f^{cde},*)
(*f^{ace}f^{bde}, f^{ade}f^{bce} and the symmetrized trace tr(T^aT^bT^cT^d) + reversed, times the three metric*)
(*structures, and compared with c4 x tree, c4 = CA (xi - 2/3) + 4/3 T_F n_f.  The symmetrized quark-box trace (a d-symbol*)
(*structure, not present in the tree) must project like the tree, i.e. cancel in the sum.*)


rawV4$ = rawOL$[diagV4$, {p1, p2}, {p3, p4}, {mu, nu, rho, si}];
t4start$ = AbsoluteTime[];
pole4$ = Sum[uvTaylor$[rawV4$[[i]], {p1, p2, p3, p4}, 0], {i, Length[rawV4$]}]/(Pi^2 KK);
Print["(c) four-gluon vertex: ", Length[rawV4$], " diagrams expanded in ", Round[AbsoluteTime[] - t4start$], " s"];
tree4$ = FCE[ChangeDimension[SUNSimplify[FCI[First[rawOL$[insOL$[CreateTopologies[0, 2 -> 2, Adjacencies -> {4}], {V[2], V[2]} -> {V[2], V[2]}],
        {p1, p2}, {p3, p4}, {mu, nu, rho, si}]]]], 4]];
c4$ = 3 (xi - 2/3) + 4/3 TF 6;    (* SU(3) numbers for the projections *)
colsOL$ = {SUNF[Glu1, Glu2, hh] SUNF[Glu3, Glu4, hh], SUNF[Glu1, Glu3, hh] SUNF[Glu2, Glu4, hh], SUNF[Glu1, Glu4, hh] SUNF[Glu2, Glu3, hh],
   SUNTrace[SUNT[Glu1, Glu2, Glu3, Glu4]] + SUNTrace[SUNT[Glu4, Glu3, Glu2, Glu1]]};
lorsOL$ = {MT[mu, nu] MT[rho, si], MT[mu, rho] MT[nu, si], MT[mu, si] MT[nu, rho]};
(* Explicit -> True: closed networks of six f's in the shape of K(3,3) (ghost/gluon boxes times the projector) are left
   unevaluated by SUNSimplify, also with SUNFToTraces -> True; with Explicit -> True they evaluate (to 0, as numerically) *)
proj4$[x_, c_, lo_] := Simplify[SUNSimplify[Contract[FCI[x c lo]], SUNNToCACF -> False, Explicit -> True] /. SUNN -> 3];
diff4$ = Table[Simplify[proj4$[pole4$, c, lo] - proj4$[gS^2/KK c4$ tree4$, c, lo]], {c, colsOL$}, {lo, lorsOL$}];
Print["(c) four-gluon vertex: 12 projections of pole - (g^2/K)(CA (xi - 2/3) + 4/3 T_F n_f) x tree = ", Union[Flatten[diff4$]],
  "   (expect {0})"];


(* ::Text:: *)
(*Slavnov-Taylor, Eq. (4): delta_g = delta1 - 3/2 delta3 = delta4/2 - delta3 = delta1tilde - delta3tilde - delta3/2 = delta1F - delta2 - delta3/2*)
(*with delta1 = -c3, delta4 = -c4, delta1tilde = -lamC, delta1F = -lamF (units g^2 DUV/K).*)


d3x$ = d3$ /. eta -> 1 - xi; d2x$ = d2$ /. eta -> 1 - xi;
c4CA$ = CA (xi - 2/3) + 4/3 TF 6;
dgList$ = Simplify[{-c3$ - 3/2 d3x$, -c4CA$/2 - d3x$, -lamC$ - d3t$ - d3x$/2, -lamF$ - d2x$ - d3x$/2} /. eta -> 1 - xi /. CF -> (CA^2 - 1)/(2 CA)];
Print["(c) delta_g from the 3g, 4g, ghost and quark vertices: ", InputForm[dgList$],
  "   (expect four times -(11/6) CA + 2/3 T_F n_f = -(11/6) CA + 2)"];


(* ::Text:: *)
(*The same abelian quark-vertex pole from TID at general momenta with PaVeUVPart (the pre-check found (CF - CA/2)(2 - xi)*)
(*instead of (CF - CA/2) xi).  FeynArts writes the gauge part 1/k^4 of the internal gluon as the same denominator twice,*)
(*FAD[l, k1 + l, k1 + l - p2, k1 + l - p2]; TID then treats it as a four-point function with a zero momentum (Gram*)
(*determinant 0).  With UsePaVeBasis -> True the UV pole has the wrong gauge part; without it the "pole" even depends on the*)
(*external momenta.  Merging the two denominators first with FDS (FeynAmpDenominatorSimplify) gives the right pole.*)


rawVuG$ = rawOL$[diagVu$, {p1, k1}, {p2}, {mu}];
poleTID$[x_] := Simplify[FCE[SUNSimplify[DiracSimplify[Normal[Series[PaVeUVPart[FCI[x], Prefactor -> 1] /. D -> 4 - 2 ep, {ep, 0, -1}]] /.
         ep -> 1], SUNNToCACF -> True]]/(Pi^2 KK)/(I gS^3/KK GA[mu] colQ$)];
Print["(c) abelian quark-vertex diagram, denominators: ", InputForm[Union[Cases[FCE[rawVuG$[[1]]], _FAD, Infinity]]]];
Print["(c) TID (UsePaVeBasis) + PaVeUVPart: ", InputForm[poleTID$[TID[SUNSimplify[DiracSimplify[rawVuG$[[1]]], SUNNToCACF -> True], l,
      ToPaVe -> True, UsePaVeBasis -> True]]], ",  after FDS: ", InputForm[poleTID$[TID[SUNSimplify[DiracSimplify[FDS[rawVuG$[[1]], l]],
       SUNNToCACF -> True], l, ToPaVe -> True, UsePaVeBasis -> True]]], "   (expect (CF - CA/2) xi)"];


(* ::Section:: *)
(*(d) MS-bar finite parts at g = 1, m = mu = 1*)


(* ::Text:: *)
(*Brackets are K/g^2 times the note's quantities, as PaVe expressions in D dimensions taken from (b): the YM part of Pi*)
(*(gluon + ghost loops), one massless and the t quark loop of Pi, Pitilde, Sigma_V and Sigma_S of t, Sigma_V of u.*)
(*Conversion to MS-bar as in the earlier notes: V = A/(2 Pi)^D; the eps^0 coefficient of (2 Pi)^(2 eps) A/(2 Pi)^4 minus*)
(*its 1/eps coefficient times (Log[4 Pi] - EulerGamma).  msbarOL$ returns {pole, finite}; the pole column printed is the*)
(*pole minus the counterterm, so it must vanish.*)


msbarOL$[x_ /; PossibleZeroQ[x]] := {0, 0};
msbarOL$[ampValue_] := Module[{v = Series[(2 Pi)^(2 Epsilon) ampValue/(2 Pi)^4, {Epsilon, 0, 0}]},
   {SeriesCoefficient[v, -1], SeriesCoefficient[v, 0] - SeriesCoefficient[v, -1] (Log[4 Pi] - EulerGamma)}];
logRulesOL$ = {Log[4 Pi] -> 2 Log[2] + Log[Pi], Log[2 Pi] -> Log[2] + Log[Pi]};
PaXEvaluate[B0[2, 1, 1]];   (* loads Package-X *)
pxOL$[x_] := Chop[N[Simplify[msbarOL$[I Pi^2 Quiet[PaXEvaluate[x /. D -> 4 - 2 Epsilon], PaXEvaluate::tens] /. ScaleMu -> 1] KK/I /. logRulesOL$], 20], 10^-14];
ltOL$[x_] := Chop[N[msbarOL$[I Pi^2 Quiet[LToolsEvaluate[x /. D -> 4 - 2 Epsilon], LToolsEvaluate::tens]] KK/I], 10^-14];
numOL$ = {CA -> 3, CF -> 4/3, gS -> 1, mt -> 1};
isYM$[x_] := !FreeQ[x, CA];
isT$[x_] := FreeQ[x, CA] && !FreeQ[x, mt];
isQ0$[x_] := FreeQ[x, CA] && FreeQ[x, mt] && !PossibleZeroQ[x];
gBr$[sel_] := Simplify[Total[Select[projG$[[All, 1]], sel]]/(I Pi^2 gS^2 (D - 1) qq)];
bPiYM$ = gBr$[isYM$];
bPiT$ = gBr$[isT$];
bPiQ0$ = Simplify[gBr$[isQ0$]/5];          (* one massless flavour *)
bGh$ = Simplify[PitOL$ KK/gS^2];
bSVt$ = Simplify[sVt$ KK/gS^2]; bSSt$ = Simplify[sSt$ KK/gS^2]; bSVu$ = Simplify[sVu$ KK/gS^2];
Print["(d) brackets: K Pi_YM/g^2 = ", InputForm[bPiYM$], ",  K Pi_t/g^2 = ", InputForm[bPiT$], ",  K Pi_q/g^2 = ", InputForm[bPiQ0$]];
rowsOL$ = {};
addRowOL$[name_, a1_, a2_, x_, ct_] := Module[{px = pxOL$[x], lt = ltOL$[x]},
   AppendTo[rowsOL$, {name, a1, a2, px[[1]] - ct, px[[2]], lt[[1]] - ct, lt[[2]]}]];
Do[addRowOL$["PiYM", x, xx, bPiYM$ /. eta -> 1 - xx /. numOL$ /. qq -> x, 3 (13/6 - xx/2)];
   addRowOL$["Ghost", x, xx, bGh$ /. eta -> 1 - xx /. numOL$ /. pp -> x, -3 (3 - xx)/4],
  {x, {-5, -1, 1/2, 2, 6, 20}}, {xx, {0, 1, 3}}];
Do[addRowOL$["PiQ0", x, 0, bPiQ0$ /. numOL$ /. qq -> x, -2/3];
   addRowOL$["PiT", x, 0, bPiT$ /. numOL$ /. qq -> x, -2/3], {x, {-5, -1, 1/2, 2, 39/10, 6, 20}}];
Do[addRowOL$["SigV_t", x, xx, bSVt$ /. numOL$ /. {pp -> x, xi -> xx}, -xx 4/3];
   addRowOL$["SigS_t", x, xx, bSSt$ /. numOL$ /. {pp -> x, xi -> xx}, (3 + xx) 4/3],
  {x, {-5, 1/2, 2, 4, 10}}, {xx, {0, 1, 3}}];
Do[addRowOL$["SigV_u", x, xx, bSVu$ /. numOL$ /. {pp -> x, xi -> xx}, -xx 4/3], {x, {-5, 1/2, 2}}, {xx, {0, 1, 3}}];


(* ::Subsubsection:: *)
(*Inspect: the brackets from Package-X and LoopTools*)


If[$Notebooks,
  TableForm[{#[[1]], N[#[[2]]], N[#[[3]]], NumberForm[#[[4]], 10], NumberForm[#[[5]], 12], NumberForm[#[[6]], 10], NumberForm[#[[7]], 12]} & /@ rowsOL$,
    TableHeadings -> {None, {"func", "arg", "xi", "PX pole-ct", "PX finite", "LT pole-ct", "LT finite"}}]
]


Print["(d) max |pole - counterterm| over all rows (Package-X, LoopTools): ", Max[Abs[Flatten[rowsOL$[[All, {4, 6}]]]]], "   (expect 0)"];
Print["(d) max |Package-X - LoopTools| of the finite parts: ", Max[Abs[rowsOL$[[All, 5]] - rowsOL$[[All, 7]]]]];
resultsDirOL$ = FileNameJoin[{srcDirOL$, "results"}];
Quiet[CreateDirectory[resultsDirOL$]];
numStrOL$[x_] := If[x === Indeterminate, "nan", ToString[CForm[N[x]]]];
cplxOL$[x_] := If[x === Indeterminate, {"nan", "nan"}, {numStrOL$[Re[x]], numStrOL$[Im[x]]}];
csvLinesOL$ = Prepend[
   StringRiffle[Join[{#[[1]], numStrOL$[#[[2]]], numStrOL$[#[[3]]]}, Flatten[cplxOL$ /@ #[[4 ;; 7]]]], ","] & /@ rowsOL$,
   "func,arg,xi,re_pole_px,im_pole_px,re_px,im_px,re_pole_lt,im_pole_lt,re_lt,im_lt"];
Export[FileNameJoin[{resultsDirOL$, "oneloop_mathematica.csv"}], StringRiffle[csvLinesOL$, "\n"] <> "\n", "Text"];
Print["(d) wrote ", Length[rowsOL$], " rows to results/oneloop_mathematica.csv"];
