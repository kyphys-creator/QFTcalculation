(* ::Package:: *)

(* ::Title:: *)
(*Step (5) of the Higgs note: the weak correction to H -> f fbar (MS-bar Yukawa couplings, FJ tadpoles, general R_xi)*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (5); the Yukawa version of the NLO note's zweak.wl.  Reads work/hff_<t><g>.m*)
(*(hff_weak_feyncalc.wl: the weak 1PI vertex {K FL, K FR} over the tree and the weak self-energy {K SL, K SR, K SSL, K SSR} of f,*)
(*with its tadpole-attached part apart) and the SM note's Sigma^HH (models/sm/Src/results/oneloop_sigma.m: general R_xi, all*)
(*fermion masses, 1PI + tadpoles; it does not depend on V at one loop).  The S-matrix element is the bare amputated vertex*)
(*times the on-shell LSZ factors with the bare Yukawa coupling y0 = y(mu) + dy:*)
(*  FL = 1 + FL_vertex + dZ_H/2 + (dZ^L_f + dZ^R_f)/2 + dy/y,  and FR alike,*)
(*  dZ_H = -Re Sigma^HH'(MH^2),  dZ^L = -SL - m^2 (SL' + SR' + 2 SSL') at p^2 = m^2 (both legs together, the NLO note's form),*)
(*  dy/y the weak MS-bar pole: the one-loop Yukawa beta function of the SM (16 pi^2 beta_y = y B) minus its QED part -6 Q^2 e^2*)
(*  (that part is in the QED K of step (4)):  K dy/y = (B - B_QED)/(2 eps),*)
(*    B_l = (3/2) y_l^2 + Y2 - (9/4) g^2 - (15/4) g'^2,   B_d = (3/2)(y_d^2 - sum_j |V_jd|^2 y_uj^2) + Y2 - (9/4) g^2 - (5/12) g'^2,*)
(*    B_u = (3/2)(y_u^2 - sum_j |V_uj|^2 y_dj^2) + Y2 - (9/4) g^2 - (17/12) g'^2,   Y2 = sum (3 y_u^2 + 3 y_d^2 + y_l^2).*)
(*No tadpole diagram enters: the vertex has none, and the tadpole parts of Sigma_f and Sigma^HH are constants (checked).*)
(*  (a) UV finiteness of FL, FR (symbolic masses and gauge parameters, an explicit rational unitary V), and without dy;*)
(*  (b) delta_weak = Re(FL + FR) - 2 (the interference over the Born) with Package-X at the note's MS-bar couplings at mu = M_H*)
(*      and the pole masses (in the loops M_W = M_Z c-hat, the tree relations), for (xiZ, xiW) = (1, 1), (2, 3), (1/2, 4);*)
(*      FL - FR (CP);*)
(*  (c) mu = M_H/2, 2 M_H with the couplings run to mu;*)
(*  (d) the point of the CKM note's MadLoop checks (for hff_weak_madloop.py), mu_R = 125, 500.*)
(*Writes results/hff_weak.csv, results/hff_weak_ml.csv.  Batch:  wolframscript -file hff_weak.wl  (after hff_weak_feyncalc.wl)*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
$MaxExtraPrecision = 200;
srcDirHV$ = DirectoryName[$InputFileName];
workDirHV$ = FileNameJoin[{srcDirHV$, "work"}];
resDirHV$ = FileNameJoin[{srcDirHV$, "results"}];
nloSrcHV$ = FileNameJoin[{srcDirHV$, "..", "..", "sm_nlo", "Src"}];
t0HV$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0HV$], " s] ", s];
KK = 16 Pi^2;
chansHV$ = {{2, 3}, {2, 2}, {4, 3}, {3, 2}};
(* the colour delta of the quark tree (SDF) cancels in the ratio vertex/tree: set to 1 (as the NLO note) *)
hffHV$ = Association[(# -> (Get[FileNameJoin[{workDirHV$, "hff_" <> ToString[#[[1]]] <> ToString[#[[2]]] <> ".m"}]] /.
       {SDF[__] -> 1, SUNFDelta[__] -> 1})) & /@ chansHV$];
smSigHV$ = Association[Get[FileNameJoin[{srcDirHV$, "..", "..", "sm", "Src", "results", "oneloop_sigma.m"}]]];
kRuleHV$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2, SPD[k] -> kk2};
sigHH$ = Total[smSigHV$["HH"]] /. kRuleHV$;
Print["Sigma^HH: ", Length[smSigHV$["HH"]], " pieces;  the derivative of each in k^2 vanishes: ",
  (Simplify[D[# /. kRuleHV$, kk2]] === 0) & /@ smSigHV$["HH"], "  (expect False for the 1PI part, True for the tadpoles)"];

(* ::Section:: *)
(*The renormalized form factors*)

lepHV$ = {Me, MMU, MTA}; upHV$ = {MU, MC, MT}; dnHV$ = {MD, MS, MB};
yOf$[m_] := Sqrt[2] m ee/(2 MW sw);
y2HV$ = Sum[3 yOf$[upHV$[[i]]]^2 + 3 yOf$[dnHV$[[i]]]^2 + yOf$[lepHV$[[i]]]^2, {i, 3}];
gg2$ = ee^2/sw^2; gp2$ = ee^2/cw^2;
bOf$[t_, g_] := Switch[t,
   2, 3/2 yOf$[lepHV$[[g]]]^2 + y2HV$ - 9/4 gg2$ - 15/4 gp2$ + 6 ee^2,
   4, 3/2 (yOf$[dnHV$[[g]]]^2 - Sum[cK[j, g] cKc[j, g] yOf$[upHV$[[j]]]^2, {j, 3}]) + y2HV$ - 9/4 gg2$ - 5/12 gp2$ + 6 (1/9) ee^2,
   3, 3/2 (yOf$[upHV$[[g]]]^2 - Sum[cK[g, j] cKc[g, j] yOf$[dnHV$[[j]]]^2, {j, 3}]) + y2HV$ - 9/4 gg2$ - 17/12 gp2$ + 6 (4/9) ee^2];
dZfSymHV$[se_, m_] := Module[{sl, sr, ss},
   {sl, sr, ss} = (se[[{1, 2, 3}]] /. {SPD[p, p] -> pp2, Pair[Momentum[p, D], Momentum[p, D]] -> pp2, SPD[p] -> pp2});
   {-sl - m^2 D[sl + sr + 2 ss, pp2], -sr - m^2 D[sl + sr + 2 ss, pp2]}];
dZH$ = -D[sigHH$, kk2] /. kk2 -> MH^2;
piecesHV$ = Association[Table[ch -> Module[{z = hffHV$[ch], dzf},
      dzf = dZfSymHV$[z["SE"], z["mass"]];
      <|"vertex" -> z["F"], "H leg" -> {dZH$/2, dZH$/2}, "f legs" -> {Total[dzf]/2, Total[dzf]/2},
       "MS-bar" -> {bOf$ @@ ch/(2 ep), bOf$ @@ ch/(2 ep)}|>], {ch, chansHV$}]];
totalHV$[ch_] := Total[Values[piecesHV$[ch]]];
tick$["pieces"];

(* ::Section:: *)
(*(a) UV finiteness and the tadpoles*)

poleHV$[x_] := SeriesCoefficient[x /. {A0[m2_] :> m2/ep2, B0[__] -> 1/ep2, Derivative[1, 0, 0][B0][__] -> 0, DB0[__] -> 0, C0[__] -> 0} /.
     D -> 4 - 2 ep2 /. ep -> ep2, {ep2, 0, -1}];
vStdHV$ = {{c12 c13, s12 c13, s13/ph}, {-s12 c23 - c12 s23 s13 ph, c12 c23 - s12 s23 s13 ph, s23 c13},
    {s12 s23 - c12 c23 s13 ph, -c12 s23 - s12 c23 s13 ph, c23 c13}} /. {c12 -> Sqrt[1 - s12^2], c23 -> Sqrt[1 - s23^2], c13 -> Sqrt[1 - s13^2]};
vPyHV$ = vStdHV$ /. {s12 -> 8/17, s23 -> 7/25, s13 -> 3/5};
explicitHV$ = {cK[i_, j_] :> vPyHV$[[i, j]], cKc[i_, j_] :> (vPyHV$[[i, j]] /. ph -> 1/ph)};
simpHV$[x_] := Simplify[Together[x /. explicitHV$ /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2]], 0 < sw < 1 && MW > 0];
uvLimHV$[ch_, x_] := Module[{m = hffHV$[ch]["mass"]}, Limit[Together[x], pp2 -> m^2]];
uvHV$ = Table[ch -> simpHV$[uvLimHV$[ch, #] & /@ poleHV$[totalHV$[ch]]], {ch, chansHV$}];
Print["(a) UV pole of K FL, K FR for tau, mu, b, c (expect all {0, 0}): ", Last /@ uvHV$];
Print["    without the MS-bar dy/y (expect nonzero): ",
  Table[simpHV$[uvLimHV$[ch, #] & /@ poleHV$[(totalHV$[ch] - piecesHV$[ch]["MS-bar"])[[1]]]], {ch, chansHV$}] // Short];
Print["    the tadpole-attached self-energies of f: {SL, SR} ", Union[Flatten[Table[hffHV$[ch]["SEtad"][[1 ;; 2]], {ch, chansHV$}]]],
  ", SS depend on p: ", Or @@ Table[! FreeQ[hffHV$[ch]["SEtad"][[3 ;; 4]], p], {ch, chansHV$}], ";  vertex tadpole insertions: ",
  Table[hffHV$[ch]["nTadVertex"], {ch, chansHV$}]];
tick$["(a)"];

(* ::Section:: *)
(*Package-X*)

pxCache$ = <||>;
pxVal$[f_, mu_] := Module[{key = {f, mu}, r, y},
   If[KeyExistsQ[pxCache$, key], Return[pxCache$[key]]];
   r = PaXEvaluate[f, PaXC0Expand -> True] /. ConditionalExpression[a_, _] :> a;
   y = Normal[Series[r /. ScaleMu -> Sqrt[Pi Exp[EulerGamma]] mu, {Epsilon, 0, 0}]];
   y = {Coefficient[y, Epsilon, -1], y /. Epsilon -> Infinity};
   pxCache$[key] = If[FreeQ[y, pp2], N[y, 60], y]];
pxDB0$[s_, a_, b_, mu_] := Module[{key = {"DB0", s, a, b, mu}, r, y},
   If[KeyExistsQ[pxCache$, key], Return[pxCache$[key]]];
   r = PaXEvaluate[B0[xx$, a, b]] /. ConditionalExpression[a1_, _] :> a1;
   y = Normal[Series[D[r /. ScaleMu -> Sqrt[Pi Exp[EulerGamma]] mu, xx$] /. xx$ -> s, {Epsilon, 0, 0}]];
   y = {Coefficient[y, Epsilon, -1], y /. Epsilon -> Infinity};
   pxCache$[key] = If[FreeQ[y, pp2], N[y, 60], y]];
(* an expression in A0, B0, B0', C0 and D: its 1/eps and MS-bar parts (the MS-bar pole of dy is the pure 1/ep there) *)
numericHV$[x_, mu_] := Module[{fs, vals, y},
   fs = Union[Cases[x, A0[__] | B0[__] | C0[__] | DB0[__] | Derivative[1, 0, 0][B0][__], Infinity]];
   vals = Function[f, Module[{v = If[MatchQ[f, DB0[__] | Derivative[1, 0, 0][B0][__]], pxDB0$[Sequence @@ f, mu], pxVal$[f, mu]]},
        v[[1]]/ep + v[[2]]]] /@ fs;
   y = x /. Thread[fs -> vals] /. D -> 4 - 2 ep;
   y = Expand[Normal[Series[y, {ep, 0, 0}]]];
   N[{Coefficient[y, ep, -1], Coefficient[y, ep, 0]}, 50]];
(* the light quarks massless in the note: 0.1 MeV here (the NLO note: their symbols sit in denominators of the self-energies) *)
poleMassesHV$ = {MZ -> 911876/10000, MH -> 12520/100, MT -> 17257/100, MB -> 478/100, MC -> 167/100, MS -> 1/10000, MD -> 1/10000,
   MU -> 1/10000, MTA -> 177693/100000, MMU -> 1056584/10000000, Me -> 510999/1000000000};
deltaHV$[ch_, mu_, xis_, inp_, masses_: poleMassesHV$] := Module[{z = hffHV$[ch], s2 = Rationalize[inp["s2"], 10^-14], e2, rules, f1,
    pole, fin, m, mz = MZ /. masses},
   e2 = Rationalize[inp["e"]^2, 10^-14];
   m = z["mass"] /. masses;
   rules = Join[{sw -> Sqrt[s2], cw -> Sqrt[1 - s2], ee -> Sqrt[e2]}, xis, masses, {MW -> Sqrt[mz^2 (1 - s2)]},
     {cK[i_, j_] :> inp["V"][[i, j]], cKc[i_, j_] :> Conjugate[inp["V"][[i, j]]]}];
   f1 = totalHV$[ch] /. pp2 -> m^2 /. rules;
   {pole, fin} = Transpose[numericHV$[#, mu] & /@ f1];
   (* dZ_H and the field constants enter with their real parts *)
   {Re[Total[fin]]/KK, Max[Abs[pole]], Abs[fin[[1]] - fin[[2]]]/KK}];
inputsHV$[mu_] := Module[{out = RunProcess[{"python3", "-c",
       "import sys; sys.path.insert(0, '" <> nloSrcHV$ <> "'); from nlo_inputs import at, POLE; p = at(" <> ToString[CForm[N[mu, 17]]] <>
        "); V = p['V']; print(' '.join('%.17e' % float(x) for x in [p['s2'], p['e']] + list(V.real.ravel()) + list(V.imag.ravel())))"},
      ProcessDirectory -> nloSrcHV$]["StandardOutput"], nums},
   nums = ToExpression[StringReplace[#, "e" -> "*^"]] & /@ StringSplit[out];
   <|"s2" -> nums[[1]], "e" -> nums[[2]], "V" -> Partition[nums[[3 ;; 11]], 3] + I Partition[nums[[12 ;; 20]], 3]|>];

(* ::Section:: *)
(*(b), (c) delta_weak at the MS-bar couplings*)

xiSets$ = {{xiZ -> 1, xiW -> 1}, {xiZ -> 2, xiW -> 3}, {xiZ -> 1/2, xiW -> 4}};
inpMH$ = inputsHV$[12520/100];
Print["(b) inputs at mu = M_H: s^2 = ", inpMH$["s2"], ", 1/alpha = ", 4 Pi/inpMH$["e"]^2, ", |V_tb| = ", Abs[inpMH$["V"][[3, 3]]]];
rowsHV$ = {};
Do[Module[{r = deltaHV$[ch, 12520/100, #, inpMH$] & /@ xiSets$},
   Print["   ", hffHV$[ch]["name"], ": delta_weak at (xiZ, xiW) = (1, 1), (2, 3), (1/2, 4): ",
    ToString[CForm[N[#, 12]]] & /@ r[[All, 1]], ";  spread ", ToString[CForm[N[Max[r[[All, 1]]] - Min[r[[All, 1]]], 2]]],
    ";  largest UV pole left ", ToString[CForm[N[Max[r[[All, 2]]], 2]]], ";  |FL - FR| ", ToString[CForm[N[Max[r[[All, 3]]], 2]]]];
   AppendTo[rowsHV$, {hffHV$[ch]["name"], 125.2, ToString[CForm[N[r[[1, 1]], 16]]], ToString[CForm[N[Max[r[[All, 1]]] - Min[r[[All, 1]]], 3]]]}]],
  {ch, chansHV$}];
tick$["(b)"];
Do[Module[{inp = inputsHV$[mu]},
   Do[Module[{r = deltaHV$[ch, mu, xiSets$[[1]], inp]},
      Print["(c) mu = ", N[mu], ", ", hffHV$[ch]["name"], ": delta_weak = ", ToString[CForm[N[r[[1]], 12]]]];
      AppendTo[rowsHV$, {hffHV$[ch]["name"], N[mu], ToString[CForm[N[r[[1]], 16]]], ""}]], {ch, chansHV$}]],
  {mu, {12520/200, 12520/50}}];
Export[FileNameJoin[{resDirHV$, "hff_weak.csv"}], Prepend[rowsHV$, {"fermion", "mu", "delta_weak", "xi_spread"}], "CSV"];
tick$["(c); written results/hff_weak.csv"];

(* ::Section:: *)
(*(d) The point of the CKM note's MadLoop checks*)

pointMassesHV$ = {MZ -> 91, MH -> 125, MT -> 165, MB -> 286/100, MC -> 619/1000, MS -> 546/10000, MD -> 271/10000, MU -> 127/10000,
   MTA -> 1746/1000, MMU -> 1027/10000, Me -> 487/1000000};
ckmStdHV$[s12_, s23_, s13_, dl_] := Module[{c12 = Sqrt[1 - s12^2], c23 = Sqrt[1 - s23^2], c13 = Sqrt[1 - s13^2], e = Exp[I dl]},
   N[{{c12 c13, s12 c13, s13/e}, {-s12 c23 - c12 s23 s13 e, c12 c23 - s12 s23 s13 e, s23 c13},
     {s12 s23 - c12 c23 s13 e, -c12 s23 - s12 c23 s13 e, c23 c13}}, 40]];
inpPointHV$ = <|"s2" -> 1 - 80^2/91^2, "e" -> Sqrt[4 Pi/128], "V" -> ckmStdHV$[22501/100000, 4183/100000, 3732/1000000, 1147/1000]|>;
mlRowsHV$ = {};
Do[Module[{r = deltaHV$[ch, muR, xiSets$[[1]], inpPointHV$, pointMassesHV$]},
    Print["(d) MadLoop point, ", hffHV$[ch]["name"], ", mu_R = ", muR, ": delta_weak = ", ToString[CForm[N[r[[1]], 14]]]];
    AppendTo[mlRowsHV$, {hffHV$[ch]["name"], muR, ToString[CForm[N[r[[1]], 20]]]}]], {ch, {{2, 3}, {2, 2}, {4, 3}}}, {muR, {125, 500}}];
Export[FileNameJoin[{resDirHV$, "hff_weak_ml.csv"}], Prepend[mlRowsHV$, {"fermion", "mu_R", "delta_weak"}], "CSV"];
tick$["(d); written results/hff_weak_ml.csv"];
