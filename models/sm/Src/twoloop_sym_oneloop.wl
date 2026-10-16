(* ::Package:: *)

(* ::Title:: *)
(*Step (8'): one-loop calibration of the symmetric, gaugeless limit of the note's model*)


(* ::Text:: *)
(*One-loop H, t, b, gluon, ghost two-point functions and the H t tbar vertex at zero Higgs momentum, from the note's FeynArts*)
(*model (twoloop_sym_setup.wl), with the one-loop integrals 1/((l^2)^a ((l-q)^2)^b) = (-1)^(a+b) G(a, b) at -q^2 = mu^2 = 1 (MS-bar*)
(*measure, each loop i/K, QCD note step (7)).  Definitions (bare, PreFactor -> 1, value = (i/K)^L x integrand):*)
(*  Gamma_H = q^2 (1 + Pi_H),  Gamma_t = qslash [P_L (1 + S_L) + P_R (1 + S_R)],  Gamma_b similar,*)
(*  Gamma_Htt = Gamma^(0) (1 + Lambda),  gluon: Z_3 (1 - Pi_A), ghost: Z~_3 (1 + Pi_c) (Landau gauge, as in the QCD note),*)
(*with Pi_H = value/(i q^2), S_X = tr[P_X qslash value]/(2 i q^2), Lambda = tr[P_L value]/tr[P_L value^(0)].*)
(*Expected one-loop poles (K = 16 pi^2, gaugeless, Landau): Z_Phi = 1 - 3 yt^2/(K eps), Z_tL = Z_bL = 1 - yt^2/(2 K eps),*)
(*Z_tR = 1 - yt^2/(K eps), and with Z_yt from Z_yt Z_Phi^(1/2) Z_tL^(1/2) Z_tR^(1/2) (1 + Lambda) finite: beta_yt = 2 yt z_yt,*)
(*K beta_yt = yt (9/2 yt^2 - 8 gS^2) (note Eq. (beta)).  Batch: wolframscript -file twoloop_sym_oneloop.wl*)


Get[FileNameJoin[{DirectoryName[$InputFileName], "twoloop_sym_setup.wl"}]];
ep = Epsilon;
gSY$[a_, b_] := Gamma[a + b - D/2] Gamma[D/2 - a] Gamma[D/2 - b]/(Gamma[a] Gamma[b] Gamma[D - a - b]);
canon$[k_] := Module[{e = Expand[k]}, If[OrderedQ[{e, Expand[-e]}], e, Expand[-e]]];
fam1$ = canon$ /@ {l1, l1 - q};
(* one-loop integrand -> value / (i/K) at -q^2 = 1, exact in D *)
oneLoop$[x_] := Module[{y, cr, mom},
   y = FCE[x] /. FAD[a__] :> Times @@ (1/dd[First[FirstPosition[fam1$, canon$[If[ListQ[#], #[[1]], #]], {0}]]] & /@ {a});
   If[!FreeQ[y, dd[0]], Print["   propagator outside the family: ", Short[x, 3]]];
   y = Expand[(y /. {SPD[l1, l1] -> dd[1], SPD[l1, q] -> (dd[1] + qq - dd[2])/2, SPD[q, l1] -> (dd[1] + qq - dd[2])/2}) dd[1]^4 dd[2]^4];
   If[!FreeQ[y, l1], Print["   loop momentum left: ", Short[y, 3]]];
   cr = CoefficientRules[y, {dd[1], dd[2]}];
   Total[(#[[2]] If[Min[4 - #[[1]]] <= 0, 0, (-1)^Total[4 - #[[1]]] gSY$ @@ (4 - #[[1]])]) & /@ cr] /. qq -> -1];
tops1$ = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles, Reducible}];
topsV1$ = CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Tadpoles, Reducible}];
topsV0$ = CreateTopologies[0, 1 -> 2];

amp$[proc_, tops_, in_, out_] := convSY$[insSY$[tops, proc], in, out, {l1}];
(* value/(i/K) -> i x integral; Pi = i oneLoop[...] / (i norm) *)
piH1$ = Total[I oneLoop$[algSY$[#]] & /@ amp$[{S[1]} -> {S[1]}, tops1$, {q}, {q}]]/(I (-1));
sL$[proc_] := Module[{a = amp$[proc, tops1$, {q}, {q}]},
   {Total[I oneLoop$[algSY$[trSY$[GA[7] . GSD[q] . #]]] & /@ a], Total[I oneLoop$[algSY$[trSY$[GA[6] . GSD[q] . #]]] & /@ a]}/(2 I (-1))];
{sLt1$, sRt1$} = sL$[{F[3, {3}]} -> {F[3, {3}]}];
{sLb1$, sRb1$} = sL$[{F[4, {3}]} -> {F[4, {3}]}];
(* vertex at zero Higgs momentum: incoming t (q), outgoing t (q) and H (pH, eliminated by momentum conservation) *)
v0$ = convSY$[insSY$[topsV0$, {F[3, {3}]} -> {F[3, {3}], S[1]}], {q}, {q, pH}, {}];
v1$ = convSY$[insSY$[topsV1$, {F[3, {3}]} -> {F[3, {3}], S[1]}], {q}, {q, pH}, {l1}];
zeroPH$[x_] := FCReplaceMomenta[x, {pH -> 0}];
trV0$ = Total[algSY$[trSY$[GA[7] . zeroPH$[#]]] & /@ v0$];
lam1$ = Total[I oneLoop$[algSY$[trSY$[GA[7] . zeroPH$[#]]]] & /@ v1$]/trV0$;
lam1R$ = Total[I oneLoop$[algSY$[trSY$[GA[6] . zeroPH$[#]]]] & /@ v1$]/Total[algSY$[trSY$[GA[6] . zeroPH$[#]]] & /@ v0$];
Print["diagrams (one loop): H ", Length[amp$[{S[1]} -> {S[1]}, tops1$, {q}, {q}]], ", t ",
  Length[amp$[{F[3, {3}]} -> {F[3, {3}]}, tops1$, {q}, {q}]], ", vertex ", Length[v1$], ";  tree vertex tr[P_L Gamma] = ", trV0$];
pole$[x_] := Simplify[SeriesCoefficient[x /. D -> 4 - 2 ep, {ep, 0, -1}]];
zPhi$ = -pole$[piH1$]; ztL$ = -pole$[sLt1$]; ztR$ = -pole$[sRt1$]; zbL$ = -pole$[sLb1$];
Print["(a) K x one-loop poles: z_Phi = ", zPhi$, ", z_tL = ", ztL$, ", z_tR = ", ztR$, ", z_bL = ", zbL$, ", (b_R part: ", pole$[sRb1$], ")"];
Print["    expected: -3 yt^2, -yt^2/2, -yt^2, -yt^2/2 (Landau gauge: no gluon term)"];
Print["(a) vertex: Lambda_L - Lambda_R = ", Simplify[lam1$ - lam1R$], ";  pole of K Lambda = ", pole$[lam1$]];
zyt$ = Simplify[-pole$[lam1$] - (zPhi$ + ztL$ + ztR$)/2];
Print["(a) K z_yt = ", zyt$, ";  K beta_yt = 2 yt z_yt = ", Expand[2 yt zyt$], "   (expect yt (9/2 yt^2 - 8 gS^2))"];
