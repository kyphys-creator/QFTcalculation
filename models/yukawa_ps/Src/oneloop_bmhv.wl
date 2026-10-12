(* ::Package:: *)

(* ::Title:: *)
(*Step (3), gamma5 scheme: the one-loop 1PI functions in BMHV compared with NDR (pseudoscalar Yukawa + phi^4)*)


(* ::Text:: *)
(*Research note models/yukawa_ps, step (3).  The note uses an anticommuting gamma5 (NDR, assumption 5).  Here the same*)
(*FeynArts diagrams as in oneloop_feyncalc.wl are evaluated with gamma5 in the Breitenlohner-Maison-'t Hooft-Veltman*)
(*scheme, where gamma5 anticommutes only with the 4-dimensional gamma matrices: gamma5 qslash gamma5 = -qbarslash + qhatslash*)
(*for the loop momentum q = qbar + qhat.  The external momenta are 4-dimensional, so their (D-4)-dimensional parts are set*)
(*to zero after the tensor reduction.  Expected: the UV poles are the same in both schemes, and BMHV - NDR is (D-4) times a*)
(*pole, i.e. a finite local polynomial in the external momenta and masses (a finite renormalization).  Checked here:*)
(*(i) BMHV - NDR vanishes at D = 4 for fixed scalar integrals; (ii) its 1/eps part is 0; (iii) its eps^0 part does not*)
(*depend on the finite parts of the scalar integrals.  The finite shifts are printed in the units of oneloop_feyncalc.wl:*)
(*  Delta b = (4 Pi)^2 Delta V / I  for V_phi, V_psi, V_4,   Delta b = (4 Pi)^2 Delta V  for V_y.*)
(*V_phi, V_psi, V_y use FeynCalc's BMHV scheme directly.  For V_4 FeynCalc's BMHV trace stops ("Not all non-chiral traces*)
(*were evaluated") and the tensor reduction with qhat did not finish in 10 minutes, so the shift is computed from the*)
(*explicit BMHV rule gamma5 (kslash + M) gamma5 = -kbarslash + khatslash + M and the terms of degree 4 in q (the argument of*)
(*the note's appendix on the gamma5 scheme); the same method reproduces the native result for V_y.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_bmhv.wl  (run generate_PsYukawa.wl first; about a minute).  Interactive:  ~/hep/bin/wopen oneloop_bmhv.wl, then "Run All Code" or Shift+Return cell by cell; the cells under "Inspect" headings run only in the notebook (If[$Notebooks, ...]).*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
SetOptions[DiracSimplify, ToDiracGamma67 -> False, DiracSubstitute67 -> True];

srcDirBM$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];

modelTmpDirBM$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirBM$, "generated", "PsYukawa_FA"}], FileNameJoin[{modelTmpDirBM$, "PsYukawa_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirBM$, "PsYukawa_FA"}], Quiet -> True];
modelBM$ = FileNameJoin[{modelTmpDirBM$, "PsYukawa_FA", "PsYukawa_FA"}];
insertBM$[tops_, proc_] := InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> modelBM$, GenericModel -> modelBM$];


(* ::Section:: *)
(*Diagrams and unreduced amplitudes*)


diagPhiBM$ = insertBM$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {S[1]} -> {S[1]}];
diagPsiBM$ = insertBM$[CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}], {F[1]} -> {F[1]}];
diagYBM$ = insertBM$[CreateTopologies[1, 2 -> 1, ExcludeTopologies -> {Tadpoles, WFCorrections}], {F[1], S[1]} -> {F[1]}];
diag4BM$ = insertBM$[CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Tadpoles, WFCorrections, Reducible}],
   {S[1], S[1]} -> {S[1], S[1]}];


(* ::Subsubsection:: *)
(*Inspect: the diagrams (the same as in oneloop_feyncalc.wl)*)


If[$Notebooks,
  {Show[#, ImageSize -> 360] & /@ Render[Paint[diagPhiBM$, ColumnsXRows -> {2, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 180] & /@ Render[Paint[diagPsiBM$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 180] & /@ Render[Paint[diagYBM$, ColumnsXRows -> {1, 1}, Numbering -> Simple, DisplayFunction -> Identity]],
   Show[#, ImageSize -> 560] & /@ Render[Paint[diag4BM$, ColumnsXRows -> {5, 2}, Numbering -> Simple, DisplayFunction -> Identity]]}
]


rawBM$[diags_, in_, out_, list_ : False] := FCFAConvert[CreateFeynAmp[diags, Truncated -> True, PreFactor -> 1] /. M$FACouplings,
   IncomingMomenta -> in, OutgoingMomenta -> out, LoopMomenta -> {q}, ChangeDimension -> D,
   List -> list, SMP -> False, DropSumOver -> True] /. {DiracGamma[6] -> (1 + DiracGamma[5])/2, DiracGamma[7] -> (1 - DiracGamma[5])/2};
onShellBM$ = {u -> 4 mphi^2 - s - t};
rPhi$ = rawBM$[diagPhiBM$, {p}, {p}];
rPsi$ = rawBM$[diagPsiBM$, {p}, {p}];
rY$ = rawBM$[diagYBM$, {p, k}, {p + k}];
(* V_4 is treated separately below (explicit BMHV rule); its diagrams are shown for reference only. *)


(* ::Section:: *)
(*The finite shifts BMHV - NDR*)


(* ::Text:: *)
(*A0(m^2) -> m^2/eps + a0, B0 -> 1/eps + b0, C0 -> c0, D0 -> d0 (FeynCalc normalization of the pole), D -> 4 - 2 eps.*)


epsBM$[x_] := Normal[Series[FCI[x] /. {A0[m2_] :> m2/epsBM + a0[m2], B0[a__] :> 1/epsBM + b0[a], C0[a__] :> c0[a],
       D0[a__] :> d0[a]} /. D -> 4 - 2 epsBM, {epsBM, 0, 0}]];
shiftBM$[bmhv_, ndr_] := Module[{d = Expand[FCI[bmhv] - FCI[ndr]], ser},
   ser = epsBM$[d];
   {Simplify[d /. D -> 4], Simplify[Coefficient[ser, epsBM, -1]], Simplify[ser /. epsBM -> 0],
    FreeQ[Simplify[ser /. epsBM -> 0], a0 | b0 | c0 | d0]}];

(* ::Section:: *)
(*Reduction in both schemes*)


(* ::Text:: *)
(*The (D-4)-dimensional parts of the external momenta are set to zero after the reduction (hatZeroBM$).  In BMHV the*)
(*traces and the open line keep qhat, and TID reduces e.g. qhat^2 to (D-4) times the g^{mu nu} coefficient.*)


hatZeroBM$[x_, ext_List] := x /. {Pair[Momentum[a_, D - 4], Momentum[b_, D - 4]] /; MemberQ[ext, a] || MemberQ[ext, b] :> 0,
    DiracGamma[Momentum[a_, D - 4], D - 4] /; MemberQ[ext, a] :> 0};
reduceBM$[x_, ext_] := FCE[hatZeroBM$[FCI[FeynAmpDenominatorExplicit[TID[DiracSimplify[x], q, ToPaVe -> True]]], ext]];
kinBM$["phi"] := (FCClearScalarProducts[]; ScalarProduct[p, p] = pp);
kinBM$["y"] := (FCClearScalarProducts[]; ScalarProduct[p, p] = pp; ScalarProduct[k, k] = kk; ScalarProduct[p, k] = (ppr - pp - kk)/2);
kinBM$["4"] := (FCClearScalarProducts[]; SetMandelstam[s, t, u, p1, p2, -k1, -k2, mphi, mphi, mphi, mphi]);
bothBM$[raw_, kin_, ext_, post_] := Table[FCSetDiracGammaScheme[sch]; kinBM$[kin]; post[reduceBM$[raw, ext]], {sch, {"NDR", "BMHV"}}];
postY$[x_] := FCE[DiracOrder[DiracSimplify[x], {k, p}]];

reportBM$[name_, sh_, unit_] := (Print["(d) ", name, ": BMHV - NDR at D = 4 (expect 0) ", sh[[1]], ";  1/eps part (expect 0) ", sh[[2]],
    ";  free of finite parts (expect True) ", sh[[4]], ";  Delta b = ", InputForm[Simplify[FCE[sh[[3]]]/unit]]]; Simplify[FCE[sh[[3]]]/unit]);
timeBM$ = AbsoluteTime[];
{nPhi$, bPhi$} = bothBM$[rPhi$, "phi", {p}, (# /. SPD[p] -> pp) &];
dbPhi$ = reportBM$["V_phi", shiftBM$[bPhi$, nPhi$], I Pi^2];
{nPsi$, bPsi$} = bothBM$[rPsi$, "phi", {p}, (# /. SPD[p] -> pp) &];
dbPsi$ = reportBM$["V_psi", shiftBM$[bPsi$, nPsi$], I Pi^2];
{nY$, bY$} = bothBM$[rY$, "y", {p, k}, postY$];
dbY$ = reportBM$["V_y", shiftBM$[bY$, nY$], Pi^2];
Print["(d) time for V_phi, V_psi, V_y: ", Round[AbsoluteTime[] - timeBM$], " s"];
(* V_4.  FeynCalc's native BMHV trace aborts for the box with four gamma5 ("Not all non-chiral traces were evaluated"),
   and the full tensor reduction of the box with qhat components did not finish in 10 minutes.  The shift is therefore
   computed from BMHV's defining rule gamma5 (kslash + M) gamma5 = -kbarslash + khatslash + M (khat = qhat, the external
   momenta being 4-dimensional), which turns the trace into one without gamma5:
     T_BMHV = tr[(M - kbar1 + qhat)(M + k2)(M - kbar3 + qhat)(M + k4)],  T_NDR = tr[(M - k1)(M + k2)(M - k3)(M + k4)].
   BMHV - NDR contains qhat; only its terms of degree 4 in q survive (lower terms give UV-finite integrals, (D-4) times a
   finite number -> 0), and for them the denominators may be replaced by (q^2 - M^2)^4.  Each of the six boxes gives the
   same shift.  The method is checked on V_y, where the native BMHV result above is available. *)
uvLeadBM$[dnum_, deg_, nprop_] := Module[{x = Expand[DotSimplify[ExpandScalarProduct[FCI[dnum] /. Momentum[q, d___] :> lamBM Momentum[q, d]]]]},
   x = Coefficient[x, lamBM, deg];
   (* DiracSimplify contracts the Lorentz indices left by TID: gbar.g = 4, ghat.g = D - 4 *)
   FCE[DiracSimplify[TID[x FeynAmpDenominator @@ Table[PropagatorDenominator[Momentum[q, D], Mpsi], {nprop}], q, ToPaVe -> True]]]];
FCSetDiracGammaScheme["BMHV"]; FCClearScalarProducts[];
(* check on V_y: numerator difference of gamma5 (k+q+M) gamma5 (q+M) gamma5, leading degree 2 over three propagators *)
dNumY$ = DiracSimplify[(Mpsi - GS[k] - GS[q] + GSE[q]) . (Mpsi + GSD[q]) . GA5 - (Mpsi - GSD[k] - GSD[q]) . (Mpsi + GSD[q]) . GA5];
dbYlead$ = Simplify[FCE[shiftBM$[-I yps^3 uvLeadBM$[dNumY$, 2, 3], 0][[3]]]/Pi^2];
Print["(d) V_y by the leading-UV method: Delta b = ", InputForm[dbYlead$], "  (native BMHV above: ", InputForm[dbY$], ")"];
(* V_4: one box, momenta k_i = q + r_i *)
kvBM$ = {q, q + r1, q + r1 + r2, q + r1 + r2 + r3};
trBMHV$ = DiracSimplify[DiracTrace[(Mpsi - GS[kvBM$[[1]]] + GSE[q]) . (Mpsi + GSD[kvBM$[[2]]]) . (Mpsi - GS[kvBM$[[3]]] + GSE[q]) . (Mpsi + GSD[kvBM$[[4]]])]];
trNDR$ = DiracSimplify[DiracTrace[(Mpsi - GSD[kvBM$[[1]]]) . (Mpsi + GSD[kvBM$[[2]]]) . (Mpsi - GSD[kvBM$[[3]]]) . (Mpsi + GSD[kvBM$[[4]]])]];
dTlead$ = uvLeadBM$[trBMHV$ - trNDR$, 4, 4];
FCSetDiracGammaScheme["NDR"]; FCClearScalarProducts[];
(* one box diagram is -y^4 int T/(D1 D2 D3 D4); six boxes *)
sh4$ = shiftBM$[6 (-yps^4) dTlead$, 0];
db4$ = reportBM$["V_4 (six boxes, leading-UV method)", sh4$, I Pi^2];
FCSetDiracGammaScheme["NDR"]; FCClearScalarProducts[];


(* ::Subsubsection:: *)
(*Inspect: V_phi in the two schemes*)


If[$Notebooks,
  {nPhi$, bPhi$} // TraditionalForm
]


Print["(d) summary: Delta b_phi, Delta b_psi, Delta b_y, Delta b_4 = ", InputForm[{dbPhi$, dbPsi$, dbY$, db4$}]];


(* ::Subsubsection:: *)
(*Inspect: the shifts*)


If[$Notebooks,
  TableForm[{{"Delta b_phi", TraditionalForm[dbPhi$]}, {"Delta b_psi", TraditionalForm[dbPsi$]},
    {"Delta b_y", TraditionalForm[dbY$]}, {"Delta b_4", TraditionalForm[db4$]}}]
]


(* ::Section:: *)
(*Cleanup*)


DeleteDirectory[modelTmpDirBM$, DeleteContents -> True];
