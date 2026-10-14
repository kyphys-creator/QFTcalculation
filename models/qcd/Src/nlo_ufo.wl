(* ::Package:: *)

(* ::Title:: *)
(*Step (5), 3 of 3: the NLO UFO with UV counterterm and R2 vertices for MadLoop*)


(* ::Text:: *)
(*FeynRules: read Src/generated/QCD_CT.nlo (nlo_nloct.wl), compare NLOCT's UV counterterms and R2 vertices with the*)
(*note, and write Src/generated/QCD_NLO_UFO (overwritten).  Research note models/qcd, step (5).  SU(3), n_l = 5 massless*)
(*quarks + t (MT), Feynman gauge, K = (4 Pi)^2, L = ln(mu^2/MT^2) = 2 Log[FR$MU/MT]; NLOCT writes 1/FR$Eps for the pole and*)
(*sets its infrared marker FR$IR -> 1, so on-shell constants of massless fields vanish (UV and IR poles cancel).*)
(*UV counterterms (hand: Eqs. (7), (11) at xi = 1; the top field and mass on shell, aS = alpha_s^(n_l)):*)
(*  deltaZ_q = 0 (massless),  deltaZ_t = -C_F (g^2/K)(3/eps + 4 + 3 L),  deltam_t = MT deltaZ_t,*)
(*  deltaZ_G = -(4/3) T_F (g^2/K)(1/eps + L)  (only the top loop of Pi(0) survives),*)
(*  delta_g = (g^2/K) [(-(11/6) C_A + (2/3) T_F n_l)/eps + (2/3) T_F (1/eps + L)]  (MS-bar for n_l flavours, the top loop*)
(*            subtracted at zero momentum, i.e. aS = alpha_s^(n_l) of Eq. (11));*)
(*  vertices: psibar psi: I [deltaZ (pslash - m) - deltam];  G G: I deltaZ_G (k k - k^2 g);*)
(*  q qbar G, q qbar A, G G G, G G G G: tree x (delta_g + deltaZ_q + deltaZ_G/2), tree x deltaZ_q, tree x (delta_g + 3/2 deltaZ_G),*)
(*  tree x (2 delta_g + 2 deltaZ_G)  (the photon is not renormalized: QCD corrections only).*)
(*R2 vertices (Feynman gauge, 't Hooft-Veltman): the quark two-point function is C_F times the QED one (spinor QED note,*)
(*App. D), I C_F (g^2/K)(2 m - pslash); the others are compared with Draggiotis, Garzelli, Papadopoulos and Pittau*)
(*(DGPP, arXiv:0903.0356, Figs. 2, 3, lambda_HV = 1), whose Feynman rules have the opposite sign of g (their quark-gluon*)
(*vertex is -i g t gamma, ours i g T gamma; their V_{mu1 mu2 mu3} = -ours): their R2 vertices with g -> -g.  The four-gluon,*)
(*A A G G and A G G G vertices are compared numerically by contracting both sides with random polarization, momentum and*)
(*colour vectors (explicit Gell-Mann matrices; FeynArts' SUNF[a, b, c, d] = f^{abe} f^{ecd}).*)
(*FeynmanGauge = True writes gauge = [0, 1]; MadGraph needs Feynman gauge for loops.  MG5's UFO-to-Fortran converter writes*)
(*decimals with 7 digits, so decimal coefficients are turned back into exact ratios (as in the spinor QED note).*)
(**)
(*Usage:  wolframscript -file nlo_ufo.wl     (after nlo_nloct.wl)*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file nlo_ufo.wl  (in a fresh kernel).  Interactive:  ~/hep/bin/wopen nlo_ufo.wl  (in a fresh kernel), then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]) and show intermediate objects without changing anything.*)


(* ::Section:: *)
(*Setup*)


srcDirNU$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];


(* ::Section:: *)
(*FeynRules, the model and the NLOCT counterterms*)


$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNU$];
LoadModel["QCD.fr"];
SetDirectory[FileNameJoin[{srcDirNU$, "generated"}]];
Get["QCD_CT.nlo"];
R2$vertlist = DeleteCases[R2$vertlist, Last[{}]];
Print["perturbed orders: ", FR$InteractionOrderPerturbativeExpansion, ";  R2 vertices: ", Length[R2$vertlist], ";  UV vertices: ", Length[UV$vertlist]];
Print["vertex legs: R2 ", R2$vertlist[[All, 1, All, 1]], ";  UV ", UV$vertlist[[All, 1, All, 1]]];
treeNU$ = FeynmanRules[LQCD, ScreenOutput -> False];


(* ::Section:: *)
(*helpers*)


kNU$ = (4 Pi)^2; cfNU$ = 4/3; caNU$ = 3; tfNU$ = 1/2; nlNU$ = 5;
lgNU$ = 2 Log[FR$MU/MT];   (* ln(mu^2/MT^2) *)
spNU$ = {TensDot[SlashedP[k_], ProjP][a_, b_] :> SlashedP[k, a, b]/2 + slash5[k, a, b]/2,
   TensDot[SlashedP[k_], ProjM][a_, b_] :> SlashedP[k, a, b]/2 - slash5[k, a, b]/2,
   TensDot[Ga[mu_], ProjP][a_, b_] :> Ga[mu, a, b]/2 + ga5[mu, a, b]/2,
   TensDot[Ga[mu_], ProjM][a_, b_] :> Ga[mu, a, b]/2 - ga5[mu, a, b]/2,
   ProjP[a_, b_] :> IndexDelta[a, b]/2 + Ga[5, a, b]/2, ProjM[a_, b_] :> IndexDelta[a, b]/2 - Ga[5, a, b]/2};
massiveNU$ = If[a_, b_, c_] :> c;   (* NLOCT's If[MT == 0, ...]: MT != 0 *)
pickNU$[list_, legs_] := Expand[First[Cases[list, {lg_, v_} /; lg[[All, 1]] === legs :> v]] /. IPL[_] -> 1 /. massiveNU$ /. spNU$];
(* FeynRules' tree vertices use T and f; NLOCT uses FeynArts' SUNT and SUNF *)
treeVNU$[legs_] := Expand[First[Cases[treeNU$, {lg_, v_} /; Sort[lg[[All, 1]]] === Sort[legs] && lg[[All, 1]] === legs :> v]] /. spNU$ /.
    {T[a_, b_, c_] :> SUNT[a, b, c], f[a_, b_, c_] :> SUNF[a, b, c]}];
s12$ = Sequence[Index[Spin, Ext[1]], Index[Spin, Ext[2]]]; c12$ = Sequence[Index[Colour, Ext[1]], Index[Colour, Ext[2]]];
lor[i_] := Index[Lorentz, Ext[i]]; glu[i_] := Index[Gluon, Ext[i]];
cmp[name_, d_] := Print[name, ": NLOCT - hand = ", Simplify[d, Assumptions -> {MT > 0, FR$MU > 0}], "  (expect 0)"];
(* random multilinear contraction of pure-gluon and photon-gluon vertices: e[i] Lorentz vectors, p[i] momenta (sum 0),
   c[i] colour vectors; FeynArts' SUNF[a, b, c, d] = f^{abe} f^{ecd} *)
gm = {{{0, 1, 0}, {1, 0, 0}, {0, 0, 0}}, {{0, -I, 0}, {I, 0, 0}, {0, 0, 0}}, {{1, 0, 0}, {0, -1, 0}, {0, 0, 0}}, {{0, 0, 1}, {0, 0, 0}, {1, 0, 0}},
   {{0, 0, -I}, {0, 0, 0}, {I, 0, 0}}, {{0, 0, 0}, {0, 0, 1}, {0, 1, 0}}, {{0, 0, 0}, {0, 0, -I}, {0, I, 0}}, {{1, 0, 0}, {0, 1, 0}, {0, 0, -2}}/Sqrt[3]};
tt = gm/2;
fabc = Table[Chop[-2 I Tr[(tt[[a]] . tt[[b]] - tt[[b]] . tt[[a]]) . tt[[c]]]], {a, 8}, {b, 8}, {c, 8}];
metric = DiagonalMatrix[{1, -1, -1, -1}];
mdot[x_, y_] := x . metric . y;
contractNU$[expr_, n_, seed_] := Module[{e, p, c, cm, f3, f4, r},
   SeedRandom[seed];
   e = Table[RandomReal[{-1, 1}, 4, WorkingPrecision -> 30], {n}];
   p = Table[RandomReal[{-1, 1}, 4, WorkingPrecision -> 30], {n - 1}]; AppendTo[p, -Total[p]];
   c = Table[RandomReal[{-1, 1}, 8, WorkingPrecision -> 30], {n}];
   f3[i_, j_, k_] := Sum[fabc[[a, b, cc]] c[[i, a]] c[[j, b]] c[[k, cc]], {a, 8}, {b, 8}, {cc, 8}];
   f4[i_, j_, k_, l_] := Sum[(fabc[[All, All, x]] . c[[j]] . c[[i]]) (fabc[[x]] . c[[l]] . c[[k]]), {x, 8}];
   (* SUNT with gluon indices only = trace of the product; f f with a summed index (FeynRules' tree vertex) = f4 *)
   r = Expand[expr] /. {SUNF[glu[i_], glu[j_], x : Index[Gluon, _Symbol]] SUNF[glu[k_], glu[l_], x : Index[Gluon, _Symbol]] :> f4[i, j, k, l]};
   r = r /. {ME[lor[i_], lor[j_]] :> mdot[e[[i]], e[[j]]], FV[k_, lor[i_]] :> mdot[p[[k]], e[[i]]], SP[k_, l_] :> mdot[p[[k]], p[[l]]],
       IndexDelta[glu[i_], glu[j_]] :> c[[i]] . c[[j]], SUNF[glu[i_], glu[j_], glu[k_]] :> f3[i, j, k],
       SUNF[glu[i_], glu[j_], glu[k_], glu[l_]] :> f4[i, j, k, l],
       SUNT[glu[i_], glu[j_], glu[k_]] :> Tr[(c[[i]] . tt) . (c[[j]] . tt) . (c[[k]] . tt)],
       SUNT[glu[i_], glu[j_], glu[k_], glu[l_]] :> Tr[(c[[i]] . tt) . (c[[j]] . tt) . (c[[k]] . tt) . (c[[l]] . tt)]};
   N[r /. {gs -> 1, ee -> 1, MT -> 1}, 25]];
cmat[i_, c_] := c[[i]] . tt;   (* colour vector -> matrix *)


(* ::Section:: *)
(*R2 vertices*)


r2 = <||>;
r2["u"] = -I cfNU$ gs^2/kNU$ SlashedP[2, s12$] IndexDelta[c12$];
r2["t"] = I cfNU$ gs^2/kNU$ (2 MT IndexDelta[s12$] - SlashedP[2, s12$]) IndexDelta[c12$];
r2["uG"] = -2 I cfNU$ gs^3/kNU$ Ga[lor[3], s12$] SUNT[glu[3], c12$];
r2["tG"] = r2["uG"];
r2["uA"] = -2 I cfNU$ (2/3) ee gs^2/kNU$ Ga[lor[3], s12$] IndexDelta[c12$];
r2["tA"] = r2["uA"];
r2["dA"] = -2 I cfNU$ (-1/3) ee gs^2/kNU$ Ga[lor[3], s12$] IndexDelta[c12$];
(* DGPP gluon two-point: (I g^2 N/(48 Pi^2)) delta [p^2/2 g + (g p^2 - p p) + (1/N) sum_f (p^2 - 6 m_f^2) g], 5 massless + t *)
r2["GG"] = I gs^2 caNU$/(48 Pi^2) IndexDelta[glu[1], glu[2]] (SP[2, 2]/2 ME[lor[1], lor[2]] + (ME[lor[1], lor[2]] SP[2, 2] - FV[2, lor[1]] FV[2, lor[2]]) +
     (6 SP[2, 2] - 6 MT^2)/caNU$ ME[lor[1], lor[2]]);
(* DGPP three-gluon with g -> -g: -(g^3 N/(48 Pi^2))(7/4 + 1 + 2 N_f/N) f V_ours, V_ours = g12 (p1-p2)_3 + g23 (p2-p3)_1 + g31 (p3-p1)_2 *)
r2["GGG"] = -gs^3 caNU$/(48 Pi^2) (7/4 + 1 + 2 6/caNU$) SUNF[glu[1], glu[2], glu[3]] (ME[lor[1], lor[2]] (FV[1, lor[3]] - FV[2, lor[3]]) +
     ME[lor[2], lor[3]] (FV[2, lor[1]] - FV[3, lor[1]]) + ME[lor[3], lor[1]] (FV[3, lor[2]] - FV[1, lor[2]]));
qlegs = {{"u", {ubar, u}}, {"t", {tqbar, tq}}, {"uG", {ubar, u, G}}, {"tG", {tqbar, tq, G}}, {"uA", {ubar, u, A}}, {"tA", {tqbar, tq, A}},
   {"dA", {dbar, d, A}}, {"GG", {G, G}}, {"GGG", {G, G, G}}};
Do[cmp["R2 " <> q[[1]], pickNU$[R2$vertlist, q[[2]]] - Expand[r2[q[[1]]] /. spNU$]], {q, qlegs}];
(* four-gluon (DGPP, even in g), A A G G and A G G G (g -> -g, v = I ee Q, summed over the quarks), numerically *)
dgpp4[e_, c_] := Module[{perms = Permutations[{2, 3, 4}], g, tr, cmx},
   g[i_, j_] := mdot[e[[i]], e[[j]]];
   cmx[i_] := c[[i]] . tt;
   Total[Table[Module[{q = Prepend[pp, 1], a1, a2, a3, a4},
       {a1, a2, a3, a4} = cmx /@ q;
       ((c[[q[[1]]]] . c[[q[[2]]]] c[[q[[3]]]] . c[[q[[4]]]] + c[[q[[1]]]] . c[[q[[3]]]] c[[q[[4]]]] . c[[q[[2]]]] + c[[q[[1]]]] . c[[q[[4]]]] c[[q[[2]]]] . c[[q[[3]]]])/caNU$ +
          4 Tr[a1 . a3 . a2 . a4 + a1 . a4 . a2 . a3] (3 + 1) - Tr[(a1 . a2 + a2 . a1) . (a3 . a4 + a4 . a3)] (5 + 2)) g[q[[1]], q[[2]]] g[q[[3]], q[[4]]] +
        12 6/caNU$ Tr[a1 . a2 . a3 . a4] (5/3 g[q[[1]], q[[3]]] g[q[[2]], q[[4]]] - g[q[[1]], q[[2]]] g[q[[3]], q[[4]]] - g[q[[2]], q[[3]]] g[q[[1]], q[[4]]])],
      {pp, perms}]] (-I caNU$/(96 Pi^2))];
numCheck[name_, legs_, n_, hand_] := Module[{nl = pickNU$[R2$vertlist, legs], devs},
   devs = Table[Module[{e, p, c, v1, v2},
       v1 = contractNU$[nl, n, s];
       SeedRandom[s]; e = Table[RandomReal[{-1, 1}, 4, WorkingPrecision -> 30], {n}];
       p = Table[RandomReal[{-1, 1}, 4, WorkingPrecision -> 30], {n - 1}]; c = Table[RandomReal[{-1, 1}, 8, WorkingPrecision -> 30], {n}];
       v2 = N[hand[e, c], 25];
       Abs[v1 - v2]/Max[Abs[v2], 10^-20]], {s, 1, 3}];
   Print["R2 ", name, " (random contractions, relative): NLOCT vs hand ", Max[devs], "  (expect < 1e-20)"]];
numCheck["GGGG", {G, G, G, G}, 4, dgpp4];
symG[e_, i_, j_, k_, l_] := mdot[e[[i]], e[[j]]] mdot[e[[k]], e[[l]]] + mdot[e[[i]], e[[k]]] mdot[e[[j]], e[[l]]] + mdot[e[[i]], e[[l]]] mdot[e[[j]], e[[k]]];
(* A A G G: legs {A, A, G, G}; DGPP -(I g^2/(24 Pi^2)) delta v1 v2 x sym, v = I ee Q, sum_f Q^2 = 5/3 *)
numCheck["AAGG", {A, A, G, G}, 4, Function[{e, c}, I/(24 Pi^2) (5/3) c[[3]] . c[[4]] symG[e, 1, 2, 3, 4]]];
(* A G G G: DGPP -(g^3/(24 Pi^2)) v Tr(t^a1 {t^a2, t^a3}) sym, g -> -g, v = I ee Q, sum_f Q = 1 *)
numCheck["AGGG", {A, G, G, G}, 4, Function[{e, c}, I/(24 Pi^2) Tr[(c[[2]] . tt) . ((c[[3]] . tt) . (c[[4]] . tt) + (c[[4]] . tt) . (c[[3]] . tt))] symG[e, 1, 2, 3, 4]]];


(* ::Section:: *)
(*UV counterterms*)


dZtNU$ = -cfNU$ gs^2/kNU$ (3/FR$Eps + 4 + 3 lgNU$);
dmNU$ = MT dZtNU$;
dZGNU$ = -4/3 tfNU$ gs^2/kNU$ (1/FR$Eps + lgNU$);
dgNU$ = gs^2/kNU$ ((-11/6 caNU$ + 2/3 tfNU$ nlNU$)/FR$Eps + 2/3 tfNU$ (1/FR$Eps + lgNU$));
uv = <||>;
uv["u"] = 0;
uv["t"] = I (dZtNU$ (SlashedP[2, s12$] - MT IndexDelta[s12$]) - dmNU$ IndexDelta[s12$]) IndexDelta[c12$];
uv["GG"] = I dZGNU$ (FV[2, lor[1]] FV[2, lor[2]] - SP[2, 2] ME[lor[1], lor[2]]) IndexDelta[glu[1], glu[2]];
uv["uG"] = treeVNU$[{ubar, u, G}] (dgNU$ + dZGNU$/2);
uv["tG"] = treeVNU$[{tqbar, tq, G}] (dgNU$ + dZtNU$ + dZGNU$/2);
uv["uA"] = 0;
uv["tA"] = treeVNU$[{tqbar, tq, A}] dZtNU$;
uv["GGG"] = treeVNU$[{G, G, G}] (dgNU$ + 3/2 dZGNU$);
uv["GGGG"] = treeVNU$[{G, G, G, G}] (2 dgNU$ + 2 dZGNU$);
uvlegs = {{"u", {ubar, u}}, {"t", {tqbar, tq}}, {"GG", {G, G}}, {"uG", {ubar, u, G}}, {"tG", {tqbar, tq, G}}, {"uA", {ubar, u, A}},
   {"tA", {tqbar, tq, A}}, {"GGG", {G, G, G}}, {"GGGG", {G, G, G, G}}};
Do[cmp["UV " <> q[[1]], pickNU$[UV$vertlist, q[[2]]] - Expand[uv[q[[1]]] /. spNU$]], {q, Select[uvlegs, !MemberQ[{"GGG", "GGGG"}, #[[1]]] &]}];
Do[Module[{n = Length[q[[2]]], d, ref},
    d = Max[Table[Abs[contractNU$[(pickNU$[UV$vertlist, q[[2]]] - uv[q[[1]]]) /. {FR$Eps -> ep, FR$MU -> mu}, n, s]], {s, 3}, {ep, {1/3, 2/7}}, {mu, {1, 19/10}}]];
    ref = Max[Table[Abs[contractNU$[pickNU$[UV$vertlist, q[[2]]] /. {FR$Eps -> ep, FR$MU -> mu}, n, s]], {s, 3}, {ep, {1/3, 2/7}}, {mu, {1, 19/10}}]];
    Print["UV ", q[[1]], " (random contractions): max |NLOCT - hand| = ", d, " of ", ref, "  (expect < 1e-20 relative)"]], {q, Select[uvlegs, MemberQ[{"GGG", "GGGG"}, #[[1]]] &]}];


(* ::Subsubsection:: *)
(*Inspect: NLOCT's vertices (massive branch)*)


If[$Notebooks,
  TableForm[Join[{#[[1]], "R2", TraditionalForm[pickNU$[R2$vertlist, #[[2]]]]} & /@ qlegs,
    {#[[1]], "UV", TraditionalForm[pickNU$[UV$vertlist, #[[2]]]]} & /@ uvlegs]]
]


(* ::Section:: *)
(*UFO output*)


FeynmanGauge = True;
If[DirectoryQ["QCD_NLO_UFO"], DeleteDirectory["QCD_NLO_UFO", DeleteContents -> True]];
WriteUFO[LQCD, UVCounterterms -> UV$vertlist, R2Vertices -> R2$vertlist, Output -> "QCD_NLO_UFO"];
exactUFO$[file_] := Module[{txt = Import[file, "Text"], new},
   new = StringReplace[txt, RegularExpression["(?<![\\w.])(\\d+\\.\\d{7,})"] :>
       Module[{r = Rationalize[ToExpression["$1"], 10^-15]},
         If[Head[r] === Rational, "(" <> ToString[Numerator[r]] <> "./" <> ToString[Denominator[r]] <> ".)", "$1"]]];
   Export[file, new, "Text"];
   Length[StringCases[txt, RegularExpression["(?<![\\w.])\\d+\\.\\d{7,}"]]]];
Print["decimal coefficients made exact in QCD_NLO_UFO: ", exactUFO$[FileNameJoin[{Directory[], "QCD_NLO_UFO", #}]] & /@ {"couplings.py", "CT_couplings.py"}];
Print["written: ", FileNames["QCD_NLO_UFO"]];
