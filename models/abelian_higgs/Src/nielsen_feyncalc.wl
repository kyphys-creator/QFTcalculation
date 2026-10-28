(* ::Package:: *)

(* ::Title:: *)
(*Step (7): the Nielsen identity for the tadpole and the h two-point function in a fixed R_xi gauge (abelian Higgs model)*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (7).  The xi dependence of the effective action is*)
(*    d Gamma/d xi = Integral (delta Gamma/delta phi_i) K_i,   K_i(z) = i < s phi_i(z)  Integral c-bar (MA G/2 - d.A/(2 xi)) >,*)
(*(S_gf + S_FP = Integral s[c-bar (F + xi B/2)], F = d.A + xi MA G, d Psi/d xi = c-bar (MA G + B/2), B -> -F/xi).  For h,*)
(*s h = -e c G.  Expanded about the tree vacuum v:*)
(*    d T/d xi = -MH^2 K_h,   d Sigma^H_1PI/d xi = Gamma_hhh K_h + 2 (p^2 - MH^2) K_hh(p^2),   Gamma_hhh = -3 MH^2/v,*)
(*and with the tadpole-attached diagrams (Sigma^H_tad = -3 T/v) d Sigma^H/d xi = 2 (p^2 - MH^2) K_hh(p^2).*)
(*K_h (one ghost-G bubble) and K_hh (three diagrams: h on the ghost line; h on the G line through GGh; h through AGh to*)
(*the d.A of the inserted operator) are written by hand from the Feynman rules of Table rules and reduced with FeynCalc.*)
(*  (a) d(K T)/d xi + MH^2 K K_h = 0, exact in D, against the tadpole of step (3) (results/oneloop_sigma.m);*)
(*  (b) the 1PI and tadpole parts of d(K Sigma^H)/d xi against Gamma_hhh K_h + 2 (p^2 - MH^2) K_hh and -Gamma_hhh K_h,*)
(*      exact in D (mass derivatives of A0, B0 in D dimensions; the C0(0, p^2, p^2; x, x, x) of the repeated propagator*)
(*      and B0(0; m, m) by integration by parts, checked numerically in nielsen_numeric.wl);*)
(*  (c) the UV poles: K K_hh |_pole = e^2/2, i.e. -(1/2) d dZ_Phi/d xi;*)
(*  (d) results/nielsen_k.m for nielsen_numeric.wl.*)
(*Batch: wolframscript -file nielsen_feyncalc.wl*)


$FeynCalcStartupMessages = False;
Get["FeynCalc`"];
$FCAdvice = False;

srcDirNF$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
resDirNF$ = FileNameJoin[{srcDirNF$, "results"}];
KK = (4 Pi)^2;
x = xi MA^2;


(* ::Section:: *)
(*Reduction*)


(* K x Integral d^Dq/(2 pi)^D f = (TID result)/pi^2: TID returns i pi^2 times the LoopTools-normalized A0, B0, C0 *)
reduceNF$[f_] := Module[{r},
   r = FDS[f, q];
   r = TID[Contract[r], q, ToPaVe -> True];
   r = PaVeReduce[FCE[r]] /. {PaVe[0, {}, {m2_}] :> A0[m2], PaVe[0, {p2_}, {m1_, m2_}] :> B0[p2, m1, m2],
       PaVe[0, {a1_, a2_, a3_}, {m1_, m2_, m3_}] :> C0[a1, a2, a3, m1, m2, m3]};
   r = r /. {Pair[Momentum[p, ___], Momentum[p, ___]] -> p2, SPD[p, p] -> p2} /. {A0[0] -> 0};
   r = r /. (h : B0 | C0)[a__] :> h @@ ({a} /. {Pair[Momentum[p, ___], Momentum[p, ___]] -> p2, SPD[p, p] -> p2});
   Simplify[r/Pi^2]];

dG$[k_] := I FAD[{k, Sqrt[x]}];                        (* G and ghost propagator i/(k^2 - xi MA^2) *)
dA$[k_, mu_, nu_] := -I (MTD[mu, nu] - FVD[k, mu] FVD[k, nu] FAD[k]) FAD[{k, MA}] -
    I xi FVD[k, mu] FVD[k, nu] FAD[k, {k, Sqrt[x]}];  (* Eq. (propsplit) *)


(* ::Section:: *)
(*The Nielsen functions*)


(* K_h: i (-e) <c(z) c-bar(y)> (MA/2) <G(z) G(y)> *)
kKh$ = reduceNF$[I (-e) (MA/2) dG$[q] dG$[q]];
(* K_hh: external h with momentum p into the vertex w; ghost q from the inserted operator to z *)
kKhhA$ = reduceNF$[I (-e) (MA/2) (-I xi e MA) dG$[q] dG$[q - p] dG$[q - p]];          (* h on the ghost line *)
kKhhB$ = reduceNF$[I (-e) (MA/2) (-2 I lam v) dG$[q] dG$[q] dG$[q - p]];             (* h on the G line (GGh) *)
(* h through A G h: G (momentum p - q) to z, A (momentum -q) from the inserted d.A (factor -1/(2 xi), d -> i q1) *)
kKhhC$ = reduceNF$[I (-e) (-1/(2 xi)) dG$[q] dG$[p - q] e (FVD[p, mu] + FVD[p - q, mu]) dA$[-q, mu, nu] I FVD[-q, nu]];
kKhh$ = Simplify[(kKhhA$ + kKhhB$ + kKhhC$) /. {lam -> MH^2/(2 v^2), e -> MA/v}];
kKh$ = Simplify[kKh$ /. e -> MA/v];
Print["K K_h = ", InputForm[kKh$]];
Print["K K_hh (h on ghost, GGh, AGh) = ", InputForm[Simplify[{kKhhA$, kKhhB$, kKhhC$} /. {lam -> MH^2/(2 v^2), e -> MA/v}]]];
Print["C0 functions left after PaVeReduce: ", Union[Cases[kKhh$, _C0, Infinity]]];

(* the repeated propagator: Integral 1/(D1^2 D2) with equal masses, by integration by parts in D dimensions:
   C0(0, p2, p2; m, m, m) = [(D - 3) B0(p2; m, m) - (D - 2)/(2 m) A0(m)]/(4 m - p2)   (m = mass squared) *)
ibpC0$ = C0[a1_, a2_, a3_, m_, m_, m_] /; Sort[{a1, a2, a3}] === Sort[{0, p2, p2}] :>
   ((D - 3) B0[p2, m, m] - (D - 2)/(2 m) A0[m])/(4 m - p2);
(* PaVeReduce leaves B0(0; m, m) = Integral 1/D1^2, which is (D - 2) A0(m)/(2 m) in D dimensions *)
b00$ = B0[0, m_, m_] :> (D - 2) A0[m]/(2 m);
kKhhIBP$ = Simplify[kKhh$ /. ibpC0$ /. b00$];
Print["K K_hh with the IBP relation = ", InputForm[kKhhIBP$]];


(* ::Section:: *)
(*xi derivatives of the step (3) results*)


plain$[y_] := y /. {s_Symbol /; SymbolName[s] === "A0" :> A0, s_Symbol /; SymbolName[s] === "B0" :> B0};
sig$ = Association[Map[plain$, Get[FileNameJoin[{resDirNF$, "oneloop_sigma.m"}]]]];
(* d/d xi in D dimensions: d A0(m)/dm = (D - 2) A0(m)/(2 m); d B0(p2; m, m)/dm (both masses) = 2 C0(0, p2, p2; m, m, m) *)
dXi$[y_] := Module[{z = y /. {A0[m_] :> a0F[m], B0[pp_, m1_, m2_] :> b0F[pp, m1, m2]}, w},
   w = D[z, xi] /. {Derivative[1][a0F][m_] :> (D - 2) A0[m]/(2 m),
       Derivative[0, 1, 0][b0F][pp_, m1_, m2_] :> dB0m1[pp, m1, m2], Derivative[0, 0, 1][b0F][pp_, m1_, m2_] :> dB0m2[pp, m1, m2]};
   w = w /. {a0F -> A0, b0F -> B0};
   w /. {dB0m1[pp_, m_, m_] :> C0[0, pp, pp, m, m, m], dB0m2[pp_, m_, m_] :> C0[0, pp, pp, m, m, m]}];
kT$ = sig$["T"];
kSH1PI$ = Total[sig$["H"][[1]]];
kSHtad$ = Total[sig$["H"][[2]]];
Print["xi-dependent loop functions in K Sigma^H (1PI, tadpole): ",
  Union[Cases[Simplify[kSH1PI$], (A0 | B0)[___, m_ /; ! FreeQ[m, xi], ___], Infinity]], ", ",
  Union[Cases[Simplify[kSHtad$], (A0 | B0)[___, m_ /; ! FreeQ[m, xi], ___], Infinity]]];


(* ::Section:: *)
(*(a) the tadpole, (b) the two-point function*)


gHHH$ = -3 MH^2/v;
resA$ = Simplify[(dXi$[kT$] + MH^2 kKh$) /. b00$];
Print["(a) d(K T)/d xi + MH^2 K K_h (expect 0): ", resA$];
res1PI$ = Simplify[(dXi$[kSH1PI$] - gHHH$ kKh$ - 2 (p2 - MH^2) kKhh$) /. ibpC0$ /. b00$];
resTad$ = Simplify[(dXi$[kSHtad$] + gHHH$ kKh$) /. b00$];
resTot$ = Simplify[(dXi$[kSH1PI$ + kSHtad$] - 2 (p2 - MH^2) kKhh$) /. ibpC0$ /. b00$];
Print["(b) d(K Sigma^H_1PI)/d xi - Gamma_hhh K K_h - 2 (p^2 - MH^2) K K_hh (expect 0): ", res1PI$];
Print["(b) d(K Sigma^H_tad)/d xi + Gamma_hhh K K_h (expect 0): ", resTad$];
Print["(b) d(K Sigma^H)/d xi - 2 (p^2 - MH^2) K K_hh (expect 0): ", resTot$];
(* the same against the closed form of Eq. (se): xi part (p^2 - MH^2)[A0(x) - (p^2 + MH^2)/2 B0(p^2; x, x)]/v^2 *)
resSe$ = Simplify[(dXi$[(p2 - MH^2) (A0[x] - (p2 + MH^2)/2 B0[p2, x, x])/v^2] - 2 (p2 - MH^2) kKhh$) /. ibpC0$ /. b00$];
Print["(b) d/d xi of the xi part of Eq. (se) - 2 (p^2 - MH^2) K K_hh (expect 0): ", resSe$];


(* ::Section:: *)
(*(c) UV poles*)


uvNF$[y_] := Simplify[SeriesCoefficient[y /. ibpC0$ /. {B0[__] -> 1/ep, A0[m2_] :> m2/ep} /. D -> 4 - 2 ep, {ep, 0, -1}]];
Print["(c) UV pole of K K_h: ", uvNF$[kKh$], ";  of K K_hh: ", uvNF$[kKhh$], "  (MA^2/v^2 = e^2;  d(K dZ_Phi)/d xi = -e^2)"];
Print["(c) UV pole of the three K_hh diagrams: ", uvNF$ /@ ({kKhhA$, kKhhB$, kKhhC$} /. {lam -> MH^2/(2 v^2), e -> MA/v})];


(* ::Section:: *)
(*(d) output*)


Put[{"Kh" -> kKh$, "Khh" -> kKhh$, "KhhIBP" -> kKhhIBP$,
   "KhhDiagrams" -> ({kKhhA$, kKhhB$, kKhhC$} /. {lam -> MH^2/(2 v^2), e -> MA/v})},
  FileNameJoin[{resDirNF$, "nielsen_k.m"}]];
Print["Summary (expect all 0): ", {resA$, res1PI$, resTad$, resTot$, resSe$}, ";  written results/nielsen_k.m"];
