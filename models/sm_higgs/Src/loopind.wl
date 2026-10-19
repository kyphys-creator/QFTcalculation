(* ::Package:: *)

(* ::Title:: *)
(*Step (2) of the Higgs note: H -> gamma gamma, Z gamma, g g at one loop, numerically (Package-X)*)


(* ::Text:: *)
(*Research note models/sm_higgs, step (2).  Reads work/loopind_<proc>.m (loopind_feyncalc.wl: Fg, F21 in A0, B0, C0, the*)
(*gauge parameters as symbols, the Yukawa couplings tagged by the fermion in the loop) and evaluates them with Package-X*)
(*(FeynHelpers; MS-bar ScaleMu^2 = pi e^gamma_E mu^2) at exact rational values of the H card (work/card_H.dat: the tree*)
(*relations e from aEWM1, s_W^2 = 1 - M_W^2/M_Z^2, v = 2 M_W s_W/e, y = sqrt(2) m/v), at M_H = 125.2 GeV and at M_H = 300 GeV*)
(*(above the W W threshold of the W loop and below the t tbar one: the complex A functions) and, for gamma gamma and g g, at*)
(*M_H = 1 GeV (the heavy-loop limits A_1/2 -> 4/3, A_1 -> -7 for the top and the W), for*)
(*(xiW, xiZ) = (1, 1), (2, 3), (1/2, 4) and mu = M_H, 1000 GeV.  Checks:*)
(*  (a) the 1/eps parts vanish; the finite parts do not depend on mu or on the gauge parameters;*)
(*  (b) the Ward identity of the photon (and of the gluon), Fg + (k1.k2) F21 = 0;*)
(*  (c) each loop against Eq. (loop): Fg = c N (N_c Q_f^2 A_1/2(tau_f) for a fermion, A_1(tau_W) for the W, Goldstone and ghost*)
(*      loops together), N = alpha (k1.k2)/(2 pi v) for gamma gamma, alpha_s (k1.k2)/(4 pi v) for g g (one colour pair), with one*)
(*      phase c for all loops (FeynArts' i);  Z gamma against the form of Djouadi (hep-ph/0503172, Eqs. (2.36)-(2.38)):*)
(*      N = 2 G_F M_W sqrt(alpha/(8 pi^3)) (k1.k2), N_c Q_f vhat_f/c_W A^Zgamma_1/2(tau, lambda) and A^Zgamma_1, vhat_f = 2 T3 - 4 Q s_W^2,*)
(*      tau = 4 m^2/M_H^2, lambda = 4 m^2/M_Z^2 there;*)
(*  (d) sum|M|^2 = 2 |Fg|^2 (gamma gamma, Z gamma), 16 |Fg|^2 (g g), at xi = 1, mu = M_H, at the card and at the point of the*)
(*      CKM note's NLO UFO, for loopind_madloop.py (work/loopind_me.txt).*)
(*Writes results/loopind.csv.  Batch:  wolframscript -file loopind.wl  (after loopind_feyncalc.wl aa, za, gg)*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynHelpers"};
Get["FeynCalc`"];
$FCAdvice = False;
$MaxExtraPrecision = 200;
srcDirLN$ = DirectoryName[$InputFileName];
workDirLN$ = FileNameJoin[{srcDirLN$, "work"}];
resDirLN$ = FileNameJoin[{srcDirLN$, "results"}];
t0LN$ = AbsoluteTime[];
tick$[s_] := Print["  [", Round[AbsoluteTime[] - t0LN$], " s] ", s];

procsLN$ = {"aa", "za", "gg"};
dataLN$ = Association[(# -> Association[Get[FileNameJoin[{workDirLN$, "loopind_" <> # <> ".m"}]] /. SD[__] -> 1]) & /@ procsLN$];   (* g g: per colour pair *)
fmt$[x_] := Module[{y = N[x, 16]}, If[Abs[Im[y]] > 10^-30 Abs[y], ToString[CForm[Re[y]]] <> If[Im[y] < 0, " - ", " + "] <> ToString[CForm[Abs[Im[y]]]] <> " i",
    ToString[CForm[Re[y]]]]];
sci$[x_] := ToString[CForm[N[x, 2]]];

(* the H card, rationalised to 15 digits *)
cardLN$ = Association[Cases[StringSplit[Import[FileNameJoin[{workDirLN$, "card_H.dat"}], "Text"], "\n"],
    l_ /; StringMatchQ[l, RegularExpression["\\s+\\d+\\s+\\S+\\s+#\\s+\\S+"]] :>
     Module[{w = StringSplit[l]}, w[[4]] -> Rationalize[ToExpression[StringReplace[w[[2]], "e" -> "*^"]], 10^-15]]]];
massRules$[mh_] := {MH -> mh, MZ -> cardLN$["MZ"], MW -> cardLN$["MW"], MT -> cardLN$["MT"], MB -> cardLN$["MB"],
   MC -> cardLN$["MC"], MS -> 0, MD -> 0, MU -> 0, MTA -> cardLN$["MTA"], MMU -> cardLN$["MMU"], Me -> cardLN$["Me"]};
eeLN$ = Sqrt[4 Pi/cardLN$["aEWM1"]]; gSLN$ = Sqrt[4 Pi cardLN$["aS"]];
swLN$ = Sqrt[1 - cardLN$["MW"]^2/cardLN$["MZ"]^2]; cwLN$ = cardLN$["MW"]/cardLN$["MZ"];
vLN$ = 2 cardLN$["MW"] swLN$/eeLN$;
coupRules$ = {ee -> eeLN$, gS -> gSLN$, sw -> swLN$, cw -> cwLN$, xiA -> 1, xiG -> 1};

(* Package-X: {1/eps coefficient, MS-bar finite part} of a loop function at exact arguments *)
pxCache$ = <||>;
pxVal$[f_, mu_] := Module[{key = {f, mu}, r, y},
   If[KeyExistsQ[pxCache$, key], Return[pxCache$[key]]];
   r = PaXEvaluate[f, PaXC0Expand -> True] /. ConditionalExpression[a_, _] :> a;
   y = Normal[Series[r /. ScaleMu -> Sqrt[Pi Exp[EulerGamma]] mu, {Epsilon, 0, 0}]];
   pxCache$[key] = N[{Coefficient[y, Epsilon, -1], y /. Epsilon -> Infinity}, 40]];
numeric$[x_, mu_] := Module[{fs, y},
   fs = Union[Cases[x, A0[__] | B0[__] | C0[__] | PaVe[__], Infinity]];
   y = x /. Thread[fs -> ((Function[v, v[[1]]/ep + v[[2]]][pxVal$[#, mu]]) & /@ fs)] /. D -> 4 - 2 ep;
   y = Expand[Normal[Series[y, {ep, 0, 0}]]];
   N[{Coefficient[y, ep, -1], Coefficient[y, ep, 0]}, 30]];
evalAt$[x_, mh_, xis_, mu_, tags_] := numeric$[x /. tags /. massRules$[mh] /. coupRules$ /. Thread[{xiW, xiZ} -> xis], mu];

(* Eq. (loop) and the Z gamma functions *)
fLN$[t_] := If[t <= 1, ArcSin[Sqrt[t]]^2, -1/4 (Log[(1 + Sqrt[1 - 1/t])/(1 - Sqrt[1 - 1/t])] - I Pi)^2];
gLN$[t_] := If[t <= 1, Sqrt[1/t - 1] ArcSin[Sqrt[t]], Sqrt[1 - 1/t]/2 (Log[(1 + Sqrt[1 - 1/t])/(1 - Sqrt[1 - 1/t])] - I Pi)];
aHalf$[t_] := 2 (t + (t - 1) fLN$[t])/t^2;
aOne$[t_] := -(2 t^2 + 3 t + 3 (2 t - 1) fLN$[t])/t^2;
i1$[ta_, la_] := ta la/(2 (ta - la)) + ta^2 la^2/(2 (ta - la)^2) (fLN$[1/ta] - fLN$[1/la]) + ta^2 la/(ta - la)^2 (gLN$[1/ta] - gLN$[1/la]);
i2$[ta_, la_] := -ta la/(2 (ta - la)) (fLN$[1/ta] - fLN$[1/la]);
aZgHalf$[ta_, la_] := i1$[ta, la] - i2$[ta, la];
aZgOne$[ta_, la_] := cwLN$ (4 (3 - swLN$^2/cwLN$^2) i2$[ta, la] + ((1 + 2/ta) swLN$^2/cwLN$^2 - (5 + 2/ta)) i1$[ta, la]);

fermLN$ = {{2, 3, MTA, 1, -1/2, -1, "tau"}, {2, 2, MMU, 1, -1/2, -1, "mu"}, {2, 1, Me, 1, -1/2, -1, "e"},
   {3, 3, MT, 3, 1/2, 2/3, "t"}, {3, 2, MC, 3, 1/2, 2/3, "c"}, {4, 3, MB, 3, -1/2, -1/3, "b"}};
allTags$ = Flatten[Table[tg[t, g], {t, 2, 4}, {g, 1, 3}]];
rowsLN$ = {}; meLN$ = {};
addRow$[r__] := AppendTo[rowsLN$, {r}];
gauges$ = {{1, 1}, {2, 3}, {1/2, 4}};

Do[Module[{d = dataLN$[p], m1, k1k2, fg, f21, base, vals, ward, spreadXi, spreadMu, norm, species, cph,
    mhs = If[p == "za", {12520/100, 300}, {12520/100, 300, 1}]},   (* M_H = 1 GeV: the heavy-loop limits A_1/2 -> 4/3, A_1 -> -7 *)
   m1 = d["m1"];
   Print["H -> ", p, ": ", d["nDiagrams"], " diagrams;  symbolic 1/eps of Fg, F21: ", d["uvFg"], ", ", d["uvF21"]];
   Do[Module[{mr = massRules$[mh], tagsOn = Thread[allTags$ -> 1]},
      k1k2 = (mh^2 - (m1 /. mr)^2)/2;
      vals = Table[{xis, mu, evalAt$[d["Fg"], mh, xis, mu, tagsOn], evalAt$[d["F21"], mh, xis, mu, tagsOn]},
        {xis, gauges$}, {mu, {mh, 1000}}];
      vals = Flatten[vals, 1];
      base = vals[[1, 3, 2]];
      ward = Max[Abs[#[[3, 2]] + k1k2 #[[4, 2]]] & /@ vals]/Abs[base];
      spreadXi = Max[Abs[#[[3, 2]] - base] & /@ vals]/Abs[base];
      Print["  M_H = ", N[mh], ":  Fg = ", fmt$[base], ";  max |1/eps| ", sci$[Max[Abs[Flatten[{#[[3, 1]], #[[4, 1]]} & /@ vals]]]],
       ";  spread over (xiW, xiZ) and mu: ", sci$[spreadXi], ";  Ward |Fg + k1.k2 F21|/|Fg|: ", sci$[ward]];
      addRow$[p, N[mh], "Fg_re", Re[base]]; addRow$[p, N[mh], "Fg_im", Im[base]];
      addRow$[p, N[mh], "spread_xi_mu", spreadXi]; addRow$[p, N[mh], "ward", ward];
      addRow$[p, N[mh], "max_pole", Max[Abs[Flatten[{#[[3, 1]], #[[4, 1]]} & /@ vals]]]];
      (* the loops one by one at xi = 1, mu = M_H *)
      norm = Switch[p, "aa", (eeLN$^2/(4 Pi)) k1k2/(2 Pi vLN$), "gg", (gSLN$^2/(4 Pi)) k1k2/(4 Pi vLN$),
        "za", 2 (Sqrt[2] eeLN$^2/(8 swLN$^2 cardLN$["MW"]^2)) cardLN$["MW"] Sqrt[(eeLN$^2/(4 Pi))/(8 Pi^3)] k1k2];
      species = Table[Module[{t = c[[1]], g = c[[2]], m = c[[3]] /. mr, nc = c[[4]], t3 = c[[5]], q = c[[6]], got, want},
          If[p == "gg" && t == 2, Nothing,
           got = (evalAt$[d["Fg"], mh, {1, 1}, mh, Thread[allTags$ -> 0] /. (tg[t, g] -> 0) -> (tg[t, g] -> 1)][[2]]
              - evalAt$[d["Fg"], mh, {1, 1}, mh, Thread[allTags$ -> 0]][[2]])/norm;
           want = Switch[p, "aa", nc q^2 aHalf$[mh^2/(4 m^2)], "gg", aHalf$[mh^2/(4 m^2)],
             "za", nc q (2 t3 - 4 q swLN$^2)/cwLN$ aZgHalf$[4 m^2/mh^2, 4 m^2/cardLN$["MZ"]^2]];
           {c[[7]], N[got, 20], N[want, 20]}]], {c, fermLN$}];
      If[p != "gg",
       Module[{mw = cardLN$["MW"], got, want},
        got = evalAt$[d["Fg"], mh, {1, 1}, mh, Thread[allTags$ -> 0]][[2]]/norm;
        want = If[p == "aa", aOne$[mh^2/(4 mw^2)], aZgOne$[4 mw^2/mh^2, 4 mw^2/cardLN$["MZ"]^2]];
        PrependTo[species, {"W", N[got, 20], N[want, 20]}]]];
      cph = species[[1, 2]]/species[[1, 3]];
      Print["    the phase c = ", fmt$[Chop[cph, 10^-20]], " (from the ", species[[1, 1]], " loop)"];
      Do[Print["    ", s[[1]], ": Fg/N = ", fmt$[s[[2]]], ";  formula x c = ", fmt$[cph s[[3]]], ";  rel. diff ", sci$[Abs[s[[2]]/(cph s[[3]]) - 1]]];
        addRow$[p, N[mh], "A_" <> s[[1]] <> "_re", Re[s[[2]]/cph]]; addRow$[p, N[mh], "A_" <> s[[1]] <> "_im", Im[s[[2]]/cph]];
        addRow$[p, N[mh], "reldiff_" <> s[[1]], Abs[s[[2]]/(cph s[[3]]) - 1]], {s, species}];
      If[mh == 12520/100,
       AppendTo[meLN$, p -> If[p == "gg", 16, 2] Abs[base]^2]]],
    {mh, mhs}]],
  {p, procsLN$}];

(* the point of the CKM note's NLO UFO (models/sm_ckm/Src/ckm_madloop_ext.py; alpha_s = 0.118): its field constants, the photon-Z
   mixing of the H Z gamma counterterm among them, are numbers at this point only *)
ckmPt$ = {MH -> 125, MZ -> 91, MW -> 80, MT -> 165, MB -> 286/100, MC -> 619/1000, MS -> 546/10000, MD -> 271/10000, MU -> 127/10000,
   MTA -> 1746/1000, MMU -> 1027/10000, Me -> 487/1000000};
ckmCoup$ = {ee -> Sqrt[4 Pi/128], gS -> Sqrt[4 Pi 118/1000], sw -> Sqrt[1 - 80^2/91^2], cw -> 80/91, xiA -> 1, xiG -> 1, xiW -> 1, xiZ -> 1};
Do[Module[{f = numeric$[dataLN$[p]["Fg"] /. Thread[allTags$ -> 1] /. ckmPt$ /. ckmCoup$, 125]},
   Print["H -> ", p, " at the CKM note's point: Fg = ", fmt$[f[[2]]], " (1/eps ", sci$[Abs[f[[1]]]], ")"];
   AppendTo[meLN$, p <> "_ckm" -> If[p == "gg", 16, 2] Abs[f[[2]]]^2]], {p, procsLN$}];
Export[FileNameJoin[{workDirLN$, "loopind_me.txt"}], StringRiffle[(#[[1]] <> " " <> ToString[CForm[N[#[[2]], 20]]]) & /@ meLN$, "\n"] <> "\n", "Text"];
Export[FileNameJoin[{resDirLN$, "loopind.csv"}], Prepend[{#[[1]], #[[2]], #[[3]], ToString[CForm[N[#[[4]], 16]]]} & /@ rowsLN$,
   {"process", "MH", "quantity", "value"}], "CSV"];
tick$["written: results/loopind.csv, work/loopind_me.txt"];
