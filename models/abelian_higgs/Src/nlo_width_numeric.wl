(* ::Package:: *)

(* ::Title:: *)
(*Step (5): the NLO width Gamma(h -> A A) in a general R_xi gauge (abelian Higgs model), without FeynCalc*)


(* ::Text:: *)
(*Reads results/nlo_width_sigma.m (K x the h -> A A form factors from nlo_width_feyncalc.wl) and results/oneloop_sigma.m*)
(*(K x the self-energies from oneloop_feyncalc.wl), all exact in D with A0, B0, C0.  Note Eqs. (nloamp), (nlowidth):*)
(*  K F_g^R = K F_g (1PI + tadpole) + K c_A 2 e MA - (1/2)[K Sigma^H'(MH^2) + K dZ_Phi + 2 (K Sigma_T'(MA^2) + K dZ_A)] 2 e MA,*)
(*  F_b^R = F_b,  delta_virt = Re[F_g^R + F_b S_b/S_g]/(e MA)  (S_g = 3 - MH^2/MA^2 + MH^4/(4 MA^4),*)
(*  S_b = MH^2 (MH^2 - 4 MA^2)(MH^2 - 2 MA^2)/(8 MA^4)), and in the on-shell mass scheme (e MS-bar at mu, MA and MH the*)
(*  pole masses)  delta_OS = delta_virt + Re Sigma_T(MA^2)/MA^2  (MS-bar finite part, tadpole included),*)
(*  Gamma = Gamma_0(e(mu), MA, MH) (1 + delta_OS).*)
(*  (a) the UV pole of K F_g^R and K F_b vanishes for every xi (symbolic);*)
(*  (b) delta_OS at the benchmark (e = 1/2, MA = 1, MH = 5/2) for xi = 1/2, 1, 3, 10 and mu = 1, 2 with the loop*)
(*      functions of Package-X (40 digits): the same for every xi, and delta(mu = 2) - delta(mu = 1) = -(2 e^2/(3 K)) ln 2*)
(*      (the running of e^2 in Gamma_0);*)
(*  (c) the parts: 1PI, tadpole, residues, mass shift; results/nlo_width.csv.*)
(*Batch: wolframscript -file nlo_width_numeric.wl*)


srcDirNN$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirNN$ = FileNameJoin[{srcDirNN$, "results"}];
$NumberMarks = False;
KK = 16 Pi^2;
plain$[x_] := x /. {s_Symbol /; SymbolName[s] === "A0" :> A0, s_Symbol /; SymbolName[s] === "B0" :> B0,
    s_Symbol /; SymbolName[s] === "C0" :> C0};
ff$ = Association[Map[plain$, Get[FileNameJoin[{resDirNN$, "nlo_width_sigma.m"}]]]];
sig$ = Association[Map[plain$, Get[FileNameJoin[{resDirNN$, "oneloop_sigma.m"}]]]];

(* the self-energies are written in MA, MH, v; here v = MA/e *)
toE$ = v -> MA/e;
kSigH$ = (Total[sig$["H"][[1]]] + Total[sig$["H"][[2]]]) /. toE$;
kSigT$ = (Total[sig$["T2"][[1]]] + Total[sig$["T2"][[2]]]) /. toE$;
(* derivative in p2: B0[p2, a, b] -> b0d[p2, a, b] *)
derivP2$[x_] := D[x /. B0[p2, a_, b_] :> bfun[p2, a, b], p2] /. {Derivative[1, 0, 0][bfun][pp_, a_, b_] :> B0p[pp, a, b],
    bfun[pp_, a_, b_] :> B0[pp, a, b]};
kSigHp$ = derivP2$[kSigH$] /. p2 -> MH^2;
kSigTp$ = derivP2$[kSigT$] /. p2 -> MA^2;
kSigTos$ = kSigT$ /. p2 -> MA^2;

lamE$ = e^2 MH^2/(2 MA^2);
kcA$ = 3 e^2 - xi e^2/2 - 3 lamE$ - 3 e^4/(2 lamE$);
kdZPhi$ = (3 - xi) e^2; kdZA$ = -e^2/3;
tree$ = 2 e MA;
(* poles as 1/ep (Delta = 1/ep in the MS-bar finite-part convention of the note) *)
kFgR$ = ff$["Fg1PI"] + ff$["FgTad"] + kcA$ tree$/ep - 1/2 (kSigHp$ + kdZPhi$/ep + 2 (kSigTp$ + kdZA$/ep)) tree$;
kFb$ = ff$["Fb1PI"] + ff$["FbTad"];
sG$ = 3 - MH^2/MA^2 + MH^4/(4 MA^4);
sB$ = MH^2 (MH^2 - 4 MA^2) (MH^2 - 2 MA^2)/(8 MA^4);

expandEp$[x_] := Module[{y = x /. A0[m2_] :> If[PossibleZeroQ[m2], 0, m2/ep + a0f[m2]] /. B0[pp_, a_, b_] :> 1/ep + b0f[pp, a, b] /.
       C0[c__] :> c0f[c] /. B0p[c__] :> b0pf[c] /. D -> 4 - 2 ep},
   Series[y, {ep, 0, 0}]];
poleOf$[x_] := Simplify[SeriesCoefficient[expandEp$[x], -1]];
finOf$[x_] := SeriesCoefficient[expandEp$[x], 0];


(* ::Section:: *)
(*(a) UV poles*)


Print["(a) UV pole of K F_g^R (expect 0 for every xi): ", poleOf$[kFgR$]];
Print["(a) UV pole of K F_b (expect 0): ", poleOf$[kFb$]];
Print["(a) UV pole of K F_g (1PI + tadpole) alone: ", Factor[poleOf$[ff$["Fg1PI"] + ff$["FgTad"]]]];


(* ::Section:: *)
(*(b) numbers with Package-X*)


Get["X`"];
evalPX$[x_, vals_, mu_] := Module[{y = x /. vals},
   y = y /. {a0f[m2_] :> m2 (1 - Log[m2/mu^2]),
      b0f[pp_, a_, b_] :> pxB0$[pp, a, b, mu], b0pf[pp_, a_, b_] :> pxB0p$[pp, a, b, mu],
      c0f[a1_, a2_, a3_, m1_, m2_, m3_] :> pxC0$[a1, a2, a3, m1, m2, m3]};
   N[y, 30]];
dropEps$[r_] := r /. {sy_Symbol /; SymbolName[sy] === "Eps" :> Infinity};
pxB0$[pp_, a_, b_, mu_] := N[dropEps$[LoopRefine[PVB[0, 0, pp, Sqrt[a], Sqrt[b]]]] /.
    {sy_Symbol /; SymbolName[sy] === "Mu" :> mu}, 40];
pxB0p$[pp_, a_, b_, mu_] := Module[{s, r},
   r = dropEps$[LoopRefine[PVB[0, 0, s, Sqrt[a], Sqrt[b]]]] /. {sy_Symbol /; SymbolName[sy] === "Mu" :> mu};
   N[D[r, s] /. s -> pp, 40]];
pxC0$[a1_, a2_, a3_, m1_, m2_, m3_] := N[LoopRefine[PVC[0, 0, 0, a1, a2, a3, Sqrt[m1], Sqrt[m2], Sqrt[m3]]], 40];

bench$ = {e -> 1/2, MA -> 1, MH -> 5/2};
deltaParts$[xv_, mu_] := Module[{vals = Join[bench$, {xi -> xv}], fg, fb, dVirt, dMass, p1PI, pTad, pRes},
   fg = evalPX$[finOf$[kFgR$], vals, mu];
   fb = evalPX$[finOf$[kFb$], vals, mu];
   dVirt = Re[(fg + fb (sB$/sG$ /. bench$))/KK]/(e MA /. bench$);
   dMass = Re[evalPX$[finOf$[kSigTos$], vals, mu]]/KK;
   p1PI = Re[evalPX$[finOf$[ff$["Fg1PI"] + ff$["Fb1PI"] (sB$/sG$)], vals, mu]]/KK/(e MA /. bench$);
   pTad = Re[evalPX$[finOf$[ff$["FgTad"]], vals, mu]]/KK/(e MA /. bench$);
   pRes = Re[evalPX$[finOf$[-1/2 (kSigHp$ + 2 kSigTp$) tree$], vals, mu]]/KK/(e MA /. bench$);
   {dVirt + dMass, dVirt, dMass, p1PI, pTad, pRes}];
rows$ = {};
Do[Module[{r = deltaParts$[xv, mu]},
    Print["(b) xi = ", xv, ", mu = ", mu, ": delta_OS = ", N[r[[1]], 16], "  (virtual ", N[r[[2]], 12],
      ", mass shift ", N[r[[3]], 12], ";  1PI ", N[r[[4]], 10], ", tadpole ", N[r[[5]], 10],
      ", residues ", N[r[[6]], 10], ")"];
    AppendTo[rows$, Join[{xv, mu}, r]]],
  {mu, {1, 2}}, {xv, {1/2, 1, 3, 10}}];
spread$[mu_] := Module[{d = #[[3]] & /@ Select[rows$, #[[2]] == mu &]}, If[Max[d] - Min[d] == 0, 0, N[Max[d] - Min[d], 3]]];
Print["(b) spread of delta_OS over xi: mu = 1 ", spread$[1], ", mu = 2 ", spread$[2], "   (expect 0)"];
d1$ = First[Select[rows$, #[[1]] == 1 && #[[2]] == 1 &]][[3]];
d2$ = First[Select[rows$, #[[1]] == 1 && #[[2]] == 2 &]][[3]];
Print["(b) delta_OS(mu = 2) - delta_OS(mu = 1) = ", N[d2$ - d1$, 16], ",  -(2 e^2/(3 K)) ln 2 = ",
  N[N[-(2 (1/4)/(3 KK)) Log[2], 30], 16]];
gam0$ = N[(1/2)^2 (5/2)^3/(32 Pi) (3/5) (1 - 4 (4/25) + 12 (4/25)^2), 30];
Print["(b) Gamma_0 = ", N[gam0$, 16], ",  Gamma_NLO(mu = 1) = Gamma_0 (1 + delta_OS) = ", N[gam0$ (1 + d1$), 16]];

Export[FileNameJoin[{resDirNN$, "nlo_width.csv"}],
  Join[{{"xi", "mu", "delta_OS", "delta_virt", "mass_shift", "part_1PI", "part_tadpole", "part_residues"}},
    Map[If[NumericQ[#], CForm[N[#, 17]], #] &, rows$, {2}],
    {{"Gamma0", CForm[gam0$]}, {"Gamma_NLO_mu1", CForm[N[gam0$ (1 + d1$), 17]]}}], "CSV"];
Print["(c) written results/nlo_width.csv"];
