(* ::Package:: *)

(* ::Title:: *)
(*Step (5): one-loop pole masses from the MS-bar parameters (SM note), without FeynCalc*)


(* ::Text:: *)
(*Reads results/oneloop_sigma.m (step (3)).*)
(*  (a) QCD part of the top: K (SigmaV + SigmaS)_QCD(m^2) = -C_F g_s^2 (4 + 3 ln(mu^2/m^2)) (MS-bar finite part,*)
(*      symbolic in D before the finite part is taken; xiG cancels);*)
(*  (b) the "MS-bar masses" of the beta_t scheme, g v_beta/2 etc. with v_beta = v + Delta v, in six gauges (Delta v from*)
(*      the tadpole part of the W self-energy of results/oneloop_numeric.csv);*)
(*  (c) RG: the MS-bar parameters of the benchmark at mu0 = MZ are run with the one-loop beta functions (Eq. (beta)) to*)
(*      mu1 = MZ/2, 2 MZ and 165 GeV, and the one-loop pole masses of W, Z, H, t are evaluated at mu1 (xiZ = xiW = 2,*)
(*      xiA = 1, LoopTools).  The pole masses change only at two-loop order: the change is compared with the size of*)
(*      the one-loop correction and with ln^2(mu1/mu0).*)
(*Output: results/pole_numeric.csv.  Batch: wolframscript -file pole_numeric.wl*)


(* ::Section:: *)
(*Setup*)


srcDirPN$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirPN$ = FileNameJoin[{srcDirPN$, "results"}];
sig$ = Association[Get[FileNameJoin[{resDirPN$, "oneloop_sigma.m"}]]];
KK = 16 Pi^2;
kRule$ = {SPD[k, k] -> kk2, Pair[Momentum[k, D], Momentum[k, D]] -> kk2};
ibp$ = PaVe[0, {0, pp_, pp_}, {0, 0, m2_}] :> ((D - 2) A0[m2] - (D - 3) (m2 + pp) B0[pp, m2, 0])/(m2 - pp)^2;
fin$[x_] := Module[{y = x /. {A0[m2_] :> m2/ep + a0f[m2], B0[p2_, a_, b_] :> 1/ep + b0f[p2, a, b]} /. D -> 4 - 2 ep},
   SeriesCoefficient[Series[y, {ep, 0, 0}], 0]];


(* ::Section:: *)
(*(a) QCD part of the top pole mass*)


qcdV$ = Coefficient[Expand[sig$["TT"][[1, 1]]], CF];
qcdS$ = Coefficient[Expand[sig$["TT"][[1, 2]]], CF];
qcd$ = Simplify[Together[(qcdV$ + qcdS$) /. kRule$ /. ibp$] /. kk2 -> MT^2];
qcdFin$ = Simplify[fin$[qcd$] /. {a0f[m2_] :> m2 (1 - Log[m2/mu^2]), b0f[mm2_, 0, mm2_] :> 2 - Log[mm2/mu^2],
     b0f[mm2_, mm2_, 0] :> 2 - Log[mm2/mu^2]}];
Print["(a) K (SigmaV + SigmaS)_QCD at k^2 = m_t^2 + C_F g_s^2 (4 + 3 ln(mu^2/m_t^2)) = ",
  Simplify[qcdFin$ + gS^2 (4 + 3 Log[mu^2/MT^2]), MT > 0 && mu > 0], "   (expect 0, any xiG)"];


(* ::Section:: *)
(*(b) beta_t-scheme masses*)


tabPN$ = Import[FileNameJoin[{resDirPN$, "oneloop_numeric.csv"}], "CSV"];
wRows$ = Select[tabPN$, #[[1]] === "W" &];
rowsB$ = Table[Module[{dvv = -r[[5]]/(2 80^2)},
    {r[[2]], r[[3]], dvv, 80 (1 + dvv), 91 (1 + dvv), 125 (1 + dvv), 165 (1 + dvv)}], {r, wRows$}];
Print["(b) xiZ, xiW, Delta v/v, and g v_beta/2, sqrt(g^2 + g'^2) v_beta/2, sqrt(2 lambda) v_beta, y_t v_beta/sqrt 2 (GeV):"];
Scan[Print["      ", NumberForm[N[#], 7]] &, rowsB$];
Print["    spread over the gauges (GeV): ", NumberForm[Max[#] - Min[#] & /@ Transpose[rowsB$[[All, 4 ;; 7]]], 4]];


(* ::Section:: *)
(*(c) RG check*)


(* MS-bar parameters of the benchmark at mu0 = MZ *)
mu0$ = 91;
eeB = Sqrt[4 Pi/128]; mwB = 80; mzB = 91; mhB = 125; swB = Sqrt[1 - mwB^2/mzB^2];
vB = 2 mwB swB/eeB;
massB$ = <|"MT" -> 165, "MB" -> 286/100, "MC" -> 619/1000, "MS" -> 546/10000, "MD" -> 271/100000, "MU" -> 127/100000,
   "MTA" -> 1746/1000, "MMU" -> 1027/10000, "Me" -> 487/1000000|>;
initPN$ = N[{gg -> eeB/swB, gp -> eeB/Sqrt[1 - swB^2], g3 -> Sqrt[4 Pi 118/1000], la -> mhB^2/(2 vB^2), m2 -> mhB^2/2,
     yt -> Sqrt[2] massB$["MT"]/vB, yc -> Sqrt[2] massB$["MC"]/vB, yu -> Sqrt[2] massB$["MU"]/vB,
     yb -> Sqrt[2] massB$["MB"]/vB, ys -> Sqrt[2] massB$["MS"]/vB, yd -> Sqrt[2] massB$["MD"]/vB,
     yta -> Sqrt[2] massB$["MTA"]/vB, ymu -> Sqrt[2] massB$["MMU"]/vB, ye -> Sqrt[2] massB$["Me"]/vB}, 30];
vars$ = {gg, gp, g3, la, m2, yt, yc, yu, yb, ys, yd, yta, ymu, ye};
rhs$[x_] := Module[{TT, NY4, bu, bd, bl},
   TT = 3 (yt[x]^2 + yc[x]^2 + yu[x]^2 + yb[x]^2 + ys[x]^2 + yd[x]^2) + yta[x]^2 + ymu[x]^2 + ye[x]^2;
   NY4 = 3 (yt[x]^4 + yc[x]^4 + yu[x]^4 + yb[x]^4 + ys[x]^4 + yd[x]^4) + yta[x]^4 + ymu[x]^4 + ye[x]^4;
   bu[u_, d_] := u (3/2 (u^2 - d^2) + TT - 8 g3[x]^2 - 9/4 gg[x]^2 - 17/12 gp[x]^2);
   bd[d_, u_] := d (3/2 (d^2 - u^2) + TT - 8 g3[x]^2 - 9/4 gg[x]^2 - 5/12 gp[x]^2);
   bl[l_] := l (3/2 l^2 + TT - 9/4 gg[x]^2 - 15/4 gp[x]^2);
   {-19/6 gg[x]^3, 41/6 gp[x]^3, -7 g3[x]^3,
    24 la[x]^2 + 4 la[x] TT - 2 NY4 - 3 la[x] (3 gg[x]^2 + gp[x]^2) + 3/8 (2 gg[x]^4 + (gg[x]^2 + gp[x]^2)^2),
    m2[x] (12 la[x] + 2 TT - 9/2 gg[x]^2 - 3/2 gp[x]^2),
    bu[yt[x], yb[x]], bu[yc[x], ys[x]], bu[yu[x], yd[x]], bd[yb[x], yt[x]], bd[ys[x], yc[x]], bd[yd[x], yu[x]],
    bl[yta[x]], bl[ymu[x]], bl[ye[x]]}/KK];
(* t = ln(mu/mu0) *)
solPN$ = NDSolve[Join[Thread[(D[#[t], t] & /@ vars$) == rhs$[t]], Thread[(#[0] & /@ vars$) == (vars$ /. initPN$)]],
   vars$, {t, Log[1/3], Log[3]}, WorkingPrecision -> 30, PrecisionGoal -> 25, AccuracyGoal -> 25, MaxSteps -> 10^6];
paramsAt$[mu_] := Module[{p = Association[Thread[vars$ -> (#[Log[mu/mu0$]] & /@ vars$ /. First[solPN$])]], v, e, s},
   v = Sqrt[p[m2]/p[la]]; e = p[gg] p[gp]/Sqrt[p[gg]^2 + p[gp]^2]; s = p[gp]/Sqrt[p[gg]^2 + p[gp]^2];
   <|"ee" -> e, "sw" -> s, "MW" -> p[gg] v/2, "MZ" -> Sqrt[p[gg]^2 + p[gp]^2] v/2, "MH" -> Sqrt[2 p[m2]], "gS" -> p[g3],
     "MT" -> p[yt] v/Sqrt[2], "MC" -> p[yc] v/Sqrt[2], "MU" -> p[yu] v/Sqrt[2], "MB" -> p[yb] v/Sqrt[2],
     "MS" -> p[ys] v/Sqrt[2], "MD" -> p[yd] v/Sqrt[2], "MTA" -> p[yta] v/Sqrt[2], "MMU" -> p[ymu] v/Sqrt[2],
     "Me" -> p[ye] v/Sqrt[2]|>];

(* finite parts evaluated with LoopTools at scale mu *)
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetDelta[0.];
poleAt$[mu_] := Module[{p = paramsAt$[mu], rules, eval, w, z, h, t, mz},
   SetMudim[N[mu^2]];
   rules = {ee -> p["ee"], sw -> p["sw"], MW -> p["MW"], MH -> p["MH"], gS -> p["gS"], MT -> p["MT"], MB -> p["MB"],
     MC -> p["MC"], MS -> p["MS"], MD -> p["MD"], MU -> p["MU"], MTA -> p["MTA"], MMU -> p["MMU"], Me -> p["Me"],
     CF -> 4/3, CA -> 3, xiG -> 1, xiA -> 1, xiZ -> 2, xiW -> 2};
   eval[expr_, m_] := Module[{x = expr /. MZ -> MW/cw /. cw -> Sqrt[1 - sw^2] /. rules},
     x = Together[x /. kRule$ /. ibp$] /. kk2 -> m^2;
     x = fin$[x] /. {a0f[y_] :> If[PossibleZeroQ[y /. MA -> 0], 0, (y /. MA -> 0) (1 - Log[(y /. MA -> 0)/mu^2])]} /.
       {b0f[pp_, a_, b_] :> LoopTools`B0[N[pp], N[a /. MA -> 0], N[b /. MA -> 0]]} /. MA -> 0;
     Re[N[x]]/KK];
   mz = p["MZ"];
   w = Sqrt[p["MW"]^2 - eval[Total[sig$["WW"]], p["MW"]]];
   z = Sqrt[mz^2 - eval[Total[sig$["ZZ"]], mz]];
   h = Sqrt[p["MH"]^2 - eval[Total[sig$["HH"]], p["MH"]]];
   t = p["MT"] (1 - eval[Total[Flatten[sig$["TT"]]], p["MT"]]);
   {mu, p["MW"], w, mz, z, p["MH"], h, p["MT"], t}];

polesPN$ = poleAt$ /@ {91, 91/2, 182, 165};
Print["(c) mu, then MS-bar and pole mass for W, Z, H, t (GeV):"];
Scan[Print["      ", NumberForm[N[#], 9]] &, polesPN$];
ref$ = First[polesPN$];
Do[Module[{r = polesPN$[[i]], l = Log[polesPN$[[i, 1]]/91]},
    Print["    mu = ", N[r[[1]]], ": change of the pole masses (W, Z, H, t) ", NumberForm[N[r[[{3, 5, 7, 9}]] - ref$[[{3, 5, 7, 9}]]], 4],
      " GeV; one-loop corrections at mu0 ", NumberForm[N[ref$[[{3, 5, 7, 9}]] - ref$[[{2, 4, 6, 8}]]], 4],
      "; change of the MS-bar masses ", NumberForm[N[r[[{2, 4, 6, 8}]] - ref$[[{2, 4, 6, 8}]]], 4]]], {i, 2, Length[polesPN$]}];

Export[FileNameJoin[{resDirPN$, "pole_numeric.csv"}],
  Join[{{"mu", "MW_msbar", "MW_pole", "MZ_msbar", "MZ_pole", "MH_msbar", "MH_pole", "mt_msbar", "mt_pole"}},
    N[polesPN$] /. x_Real :> CForm[x]], "CSV"];
