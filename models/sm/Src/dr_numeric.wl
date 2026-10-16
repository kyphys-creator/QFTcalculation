(* ::Package:: *)

(* ::Title:: *)
(*Step (5): Delta r and M_W at one loop -- the note's formulas with LoopTools, Denner's parameter set, FormCalc (Standard Model)*)


(* ::Text:: *)
(*Research note models/sm, step (5).  A plain kernel with the LoopTools MathLink (no FeynArts, FormCalc or FeynCalc:*)
(*FormCalc's own definitions of MW, MZ, MH, ... would clash with the note's symbols); needs results/dr_note.m from*)
(*dr_feyncalc.wl.  Eq. (dr) with the note's self-energies (Eqs. (SAA)-(SWW), (Pi0)), B0 and DB0 from*)
(*LoopTools (Delta = 0, mu^2 set below; Delta r does not depend on mu):*)
(*  Delta r = Pi^AA(0) - c^2/s^2 [Sigma^ZZ_T(MZ^2)/MZ^2 - Sigma^W_T(MW^2)/MW^2] + (Sigma^W_T(0) - Sigma^W_T(MW^2))/MW^2*)
(*            - 2 (c/s) Sigma^AZ_T(0)/MZ^2 + alpha/(4 Pi s^2) [6 + (7 - 4 s^2)/(2 s^2) ln c^2],*)
(*Sigma^W_T(0) from B0(k^2) = B0(0) + k^2 DB0(0) + O(k^4) (the formula has (B0(k^2) - B0(0))/k^2 terms).*)
(*(a) Denner's parameter set (Fortschr. Phys. 41 (1993) 307, Sec. 8.1: alpha = 1/137.0359895, MZ = 91.177, G_F = 1.16637e-5,*)
(*    m_t = 140, MH = 100 GeV, effective light-quark masses of his Eq. (8.10)) and his Eq. (8.13),*)
(*    MW^2 (1 - MW^2/MZ^2) = pi alpha/(sqrt2 G_F) (1 + Delta r), the note's Eq. (mw) with 1/(1 - Delta r), and his resummed*)
(*    Eq. (8.23): his result MW = 80.23 GeV (Eq. (8.15), from Eq. (8.23)).*)
(*(b) The note's point (assumption 7, PDG 2024): the light-fermion Pi^AA(0) - Re Pi^AA(MZ^2) is replaced by the data*)
(*    Delta alpha = Delta alpha_lep + Delta alpha_had^(5), Eq. (mw) with 1/(1 - Delta r); Delta alpha, Delta rho_t, rest.*)
(*Writes results/dr_values.csv (dr_formcalc.wl compares FormCalc's Delta r with the note's at the MW of (b)).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file dr_numeric.wl  (run dr_feyncalc.wl first).*)


(* ::Section:: *)
(*Setup*)


srcDirDN$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetDelta[0]; SetLambda[1];
noteDN$ = Get[FileNameJoin[{srcDirDN$, "results", "dr_note.m"}]];
(* Together cancels the factor (m1^2 - m2^2) of the doublet function G against its denominator (Denner's set has equal u and
   d masses, where the uncancelled form would be 0/0) *)
nF$ = Together /@ noteDN$["noteF"]; nB$ = noteDN$["noteB"];
KK = (4 Pi)^2;
fmtN$[x_, n_] := ToString[NumberForm[N[x], n], OutputForm];


(* ::Text:: *)
(*A parameter set: <|"alpha", "MZ", "MH", "GF", "gens" -> {{ml^2, mu^2, md^2} x 3}|>; MW is the variable.*)


ltB0$[p_, a_, b_] := B0[N[p, 20], N[a, 20], N[b, 20]];
ltDB0$[p_, a_, b_] := DB0[N[p, 20], N[a, 20], N[b, 20]];
(* B0(0, 0, 0) = 0 (scaleless in dimensional regularization; LoopTools returns the same), set before calling LoopTools *)
evalLT$[x_] := Re[N[x /. B0OL[0, 0, 0] -> 0 /. {B0OL[p_, a_, b_] :> ltB0$[p, a, b], DB0OL[p_, a_, b_] :> ltDB0$[p, a, b]}]];
b0zDN$ = {B0OL[0, 0, 0] -> 0, B0OL[0, a_, b_] /; a =!= b :> (a (B0OL[0, a, a] + 1) - b (B0OL[0, b, b] + 1))/(a - b) /. B0OL[0, 0, 0] -> 0};
sumGen$[key_, gens_] := Sum[nF$[key] /. {ml -> Sqrt[g[[1]]], mu -> Sqrt[g[[2]]], md -> Sqrt[g[[3]]]}, {g, gens}] /.
   {Sqrt[x_]^2 :> x};
(* the note's K Sigma summed over the generations, with MW symbolic (MWs); at k^2 = 0 the expansion B0(k^2) = B0(0) +
   k^2 DB0(0) with B0(0, m1, m2) written through B0(0, m, m) as in the formulas; the 1/k^2 coefficient must vanish *)
sigSym$[key_, par_] := sigSym$[key, par] = Module[{x = (sumGen$[key, par["gens"]] + nB$[key]) /.
      {e -> Sqrt[4 Pi par["alpha"]], c -> MWs/par["MZ"], MW -> MWs, MH -> par["MH"], Nc -> 3}}, x];
sigSym0$[key_, par_] := sigSym0$[key, par] = Module[{x = Expand[sigSym$[key, par] /. B0OL[kk, a_, b_] :> B0OL[0, a, b] + kk DB0OL[0, a, b] /. b0zDN$]},
   If[!PossibleZeroQ[Simplify[Coefficient[x, kk, -1]]], Print["   1/k^2 term left in ", key, ": ", Short[Coefficient[x, kk, -1], 3]]];
   Coefficient[x, kk, 0]];
sigma$[key_, par_, mw_, kk0_] := evalLT$[If[kk0 === 0, sigSym0$[key, par], sigSym$[key, par] /. kk -> kk0] /. MWs -> mw]/KK;
pi0$[par_, mw_] := Module[{al = par["alpha"], qf},
   evalLT$[-4 Pi al (-(4/3) Sum[g[[1]]/g[[1]] B0OL[0, g[[1]], g[[1]]] + 3 (4/9) B0OL[0, g[[2]], g[[2]]] + 3 (1/9) B0OL[0, g[[3]], g[[3]]],
          {g, par["gens"]}] + 3 B0OL[0, mw^2, mw^2] + 2/3)]/KK];
az0$[par_, mw_] := Module[{c = mw/par["MZ"]}, evalLT$[-4 Pi par["alpha"] 2 mw^2/(Sqrt[1 - c^2] c) B0OL[0, mw^2, mw^2]]/KK];
deltaR$[par_, mw_] := Module[{mz = par["MZ"], c, s2, sWW, sZZ, sW0},
   c = mw/mz; s2 = 1 - c^2;
   sWW = sigma$["WW", par, mw, mw^2]; sZZ = sigma$["ZZ", par, mw, mz^2]; sW0 = sigma$["WW", par, mw, 0];
   <|"Pi0" -> pi0$[par, mw], "ZZ" -> sZZ, "WW" -> sWW, "W0" -> sW0, "AZ0" -> az0$[par, mw],
    "dr" -> pi0$[par, mw] - (c^2/s2) (sZZ/mz^2 - sWW/mw^2) + (sW0 - sWW)/mw^2 - 2 (c/Sqrt[s2]) az0$[par, mw]/mz^2 +
      par["alpha"]/(4 Pi s2) (6 + (7 - 4 s2)/(2 s2) Log[c^2])|>];
mwFrom$[par_, dr_, form_] := Module[{a = Pi par["alpha"]/(Sqrt[2] par["GF"]), mz = par["MZ"], rhs},
   rhs = If[form === "1+dr", a (1 + dr), a/(1 - dr)];
   Sqrt[mz^2/2 (1 + Sqrt[1 - 4 rhs/mz^2])]];


ffDN$[k2_, m2_] := -(k2 + 2 m2) B0OL[k2, m2, m2] + 2 m2 B0OL[0, m2, m2] + k2/3;


(* ::Section:: *)
(*(a) Denner's parameter set*)


denner$ = <|"alpha" -> 1/1370359895*10^7, "MZ" -> 91177/1000, "MH" -> 100, "GF" -> 116637/10^10, "mt" -> 140,
   "gens" -> {{(51099906/10^11)^2, (41/1000)^2, (41/1000)^2}, {(105658387/10^9)^2, (15/10)^2, (15/100)^2},
     {(17841/10^4)^2, 140^2, (45/10)^2}}|>;
SetMudim[N[denner$["MZ"]^2]];
iterate$[par_, form_, extra_] := Module[{mw = 80, r},
   Do[r = deltaR$[par, mw]; mw = mwFrom$[par, r["dr"] + extra[r, mw], form], {8}];
   r = deltaR$[par, mw]; {mw, r, r["dr"] + extra[r, mw]}];
resD$ = iterate$[denner$, "1+dr", 0 &];
Print["(a) Denner's set, Eq. (8.13) with 1 + Delta r: Delta r = ", fmtN$[resD$[[3]], 8], ",  MW = ", fmtN$[resD$[[1]], 8],
  " GeV   (Denner: 80.23)"];
(* the note's Eq. (mw), 1/(1 - Delta r), with the same parameters *)
resD2$ = iterate$[denner$, "1/(1-dr)", 0 &];
Print["(a) Denner's set, the note's Eq. (mw) with 1/(1 - Delta r): Delta r = ", fmtN$[resD2$[[3]], 8], ",  MW = ", fmtN$[resD2$[[1]], 8], " GeV"];
(* Denner's Eq. (8.23): the fermionic Delta alpha (all fermions, s = MZ^2) and the leading m_t^2 terms resummed:
   G_F = pi alpha/(sqrt2 s^2 MW^2) 1/(1 - Dalpha) 1/(1 + c^2/s^2 Drhobar) [1 + Delta r - Dalpha + c^2/s^2 Drho],
   Drho = 3 alpha m_t^2/(16 pi s^2 MW^2) (one loop, Eq. (8.20)), Drhobar = 3 G_F m_t^2/(8 sqrt2 pi^2)[1 + G_F m_t^2/(8 sqrt2 pi^2)(19 - 2 pi^2)] *)
dalphaAll$[par_] := Module[{mz2 = par["MZ"]^2, g = par["gens"], all},
   all = Flatten[Table[{{1, 1, g[[i, 1]]}, {3, 4/9, g[[i, 2]]}, {3, 1/9, g[[i, 3]]}}, {i, 3}], 1];
   evalLT$[Sum[-4 Pi par["alpha"] (4/3) f[[1]] f[[2]] (-B0OL[0, f[[3]], f[[3]]] - ffDN$[mz2, f[[3]]]/mz2), {f, all}]]/KK];
resum823$[par_] := Module[{mw = resD$[[1]], mz = par["MZ"], gf = par["GF"], al = par["alpha"], mt = par["mt"], dal, xt, drb, s2, c2, r, f},
   dal = dalphaAll$[par]; xt = gf mt^2/(8 Sqrt[2] Pi^2); drb = 3 xt (1 + xt (19 - 2 Pi^2));
   Do[c2 = mw^2/mz^2; s2 = 1 - c2; r = deltaR$[par, mw]["dr"];
     f = (1/(1 - dal)) (1/(1 + c2/s2 drb)) (1 + r - dal + c2/s2 3 al mt^2/(16 Pi s2 mw^2));
     mw = Sqrt[mz^2/2 (1 + Sqrt[1 - 4 Pi al f/(Sqrt[2] gf mz^2)])], {8}];
   {mw, dal, drb}];
res823$ = resum823$[denner$];
Print["(a) Denner's set, resummed Eq. (8.23): MW = ", fmtN$[res823$[[1]], 8], " GeV (fermionic Delta alpha(MZ^2) = ", fmtN$[res823$[[2]], 6],
  ", Delta rho bar = ", fmtN$[res823$[[3]], 6], ")   (Denner: 80.23)"];
SetMudim[1.];
Print["(a) the same Delta r with mu = 1 GeV instead of MZ: ", fmtN$[deltaR$[denner$, resD$[[1]]]["dr"], 16],
  "  (MZ: ", fmtN$[resD$[[3]], 16], ")"];
SetMudim[N[denner$["MZ"]^2]];


(* ::Section:: *)
(*(b) The note's point*)


pdg$ = <|"alpha" -> 1000000000/137035999177, "MZ" -> 911880/10000, "MH" -> 12520/100, "GF" -> 11663788/10^12, "mt" -> 17257/100,
   "gens" -> {{(51099895/10^11)^2, (6/100)^2, (7/100)^2}, {(1056583755/10^10)^2, (127/100)^2, (1/10)^2},
     {(177686/10^5)^2, (17257/100)^2, (418/100)^2}}|>;
SetMudim[N[pdg$["MZ"]^2]];
dalLep$ = 0.031497687; dalHad$ = 0.02783;
(* light fermions (all but t): Pi(0) - Re Pi(MZ^2) = sum_f -(e^2/K)(4/3) Nc Q^2 [-B0(0,m,m) - Re F_f(MZ^2)/MZ^2], Eq. (FG) *)
piLightDiff$[par_, mw_] := Module[{mz2 = par["MZ"]^2, g = par["gens"], light},
   light = {{1, 1, g[[1, 1]]}, {1, 1, g[[2, 1]]}, {1, 1, g[[3, 1]]}, {3, 4/9, g[[1, 2]]}, {3, 4/9, g[[2, 2]]},
     {3, 1/9, g[[1, 3]]}, {3, 1/9, g[[2, 3]]}, {3, 1/9, g[[3, 3]]}};
   evalLT$[Sum[-4 Pi par["alpha"] (4/3) f[[1]] f[[2]] (-B0OL[0, f[[3]], f[[3]]] - ffDN$[mz2, f[[3]]]/mz2), {f, light}]]/KK];
resP$ = iterate$[pdg$, "1/(1-dr)", (-piLightDiff$[pdg$, #2] + dalLep$ + dalHad$) &];
drhoP$ = 3 pdg$["GF"] pdg$["mt"]^2/(8 Sqrt[2] Pi^2);
dalPert$ = piLightDiff$[pdg$, resP$[[1]]];
drhoTerm$ = -(resP$[[1]]^2/pdg$["MZ"]^2)/(1 - resP$[[1]]^2/pdg$["MZ"]^2) drhoP$;
restP$ = resP$[[3]] - (dalLep$ + dalHad$) - drhoTerm$;
Print["(b) note's point, Eq. (mw): Delta r = ", fmtN$[resP$[[3]], 8], ",  MW = ", fmtN$[resP$[[1]], 8],
  " GeV;  Delta alpha (data) = ", dalLep$ + dalHad$, ", Delta alpha (perturbative, these masses) = ", fmtN$[dalPert$, 6],
  ";  -c^2/s^2 Delta rho_t = ", fmtN$[drhoTerm$, 6], ";  rest = ", fmtN$[restP$, 6],
  "   (the note: 0.02978, 80.473, 0.05933, -0.03286, 0.00331)"];


(* ::Section:: *)
(*Output*)


Export[FileNameJoin[{srcDirDN$, "results", "dr_values.csv"}], StringRiffle[{
    "quantity,value",
    "denner_delta_r," <> ToString[CForm[resD$[[3]]]], "denner_MW_8.13," <> ToString[CForm[resD$[[1]]]],
    "denner_MW_8.23," <> ToString[CForm[res823$[[1]]]], "denner_delta_r_mw," <> ToString[CForm[resD2$[[3]]]],
    "denner_MW_mw," <> ToString[CForm[resD2$[[1]]]], "denner_drhobar," <> ToString[CForm[N[res823$[[3]]]]], "denner_dalpha_ferm," <> ToString[CForm[res823$[[2]]]],
    "note_delta_r," <> ToString[CForm[resP$[[3]]]], "note_MW," <> ToString[CForm[resP$[[1]]]],
    "note_dalpha_data," <> ToString[CForm[dalLep$ + dalHad$]], "note_dalpha_pert," <> ToString[CForm[dalPert$]],
    "note_drho_term," <> ToString[CForm[drhoTerm$]], "note_rest," <> ToString[CForm[restP$]],
    "note_formula_delta_r_at_note_MW," <> ToString[CForm[deltaR$[pdg$, resP$[[1]]]["dr"]]]}, "\n"] <> "\n", "Text"];
Print["(d) wrote results/dr_values.csv"];
