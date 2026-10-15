(* ::Package:: *)

(* ::Title:: *)
(*Step (3a): all vertex classes of the FeynRules model against FeynArts' SM.mod, including the ghosts (Standard Model)*)


(* ::Text:: *)
(*Research note models/sm, step (3).  Step (2) (tree_feyncalc.wl) compared 38 vertex classes.  Here every class of the*)
(*FeynRules model except the five with gluons (88 of 93) is compared, read from the coupling list of generated/SM_FA:*)
(*for a coupling C[f1, f2, ...] the truncated tree amplitude of {f1} -> {anti f2, ...} is built in both models*)
(*(one vertex; four-point classes as 1 -> 3 with Adjacencies -> {4}), SM.mod at GaugeXi = 1 (the FeynRules model is in*)
(*Feynman gauge).  Field map FeynRules -> SM.mod: V[3] (W+) -> -V[3], S[3] (G+) -> -S[3], U[31] (u+) -> U[4],*)
(*U[32] (u-) -> U[3]; the rest unchanged.  The ratio FR/SM.mod must be a number; the rule is a factor c(f) for every*)
(*field f of the coupling: c(A) = -1, c(G+) = -i, c(G-) = +i (step (2)) and factors for the ghost fields fixed here.*)
(*A consistent field redefinition needs c(f) c(anti f) = 1 for every propagating field (internal lines cancel).*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file oneloop_conv.wl.  Interactive:  ~/hep/bin/wopen oneloop_conv.wl, then "Run All Code".*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;
$FAVerbose = 0;

srcDirCv$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirCv$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirCv$, "generated", "SM_FA"}], FileNameJoin[{modelTmpDirCv$, "SM_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirCv$, "SM_FA"}], Quiet -> True];
frModelCv$ = FileNameJoin[{modelTmpDirCv$, "SM_FA", "SM_FA"}];


(* ::Text:: *)
(*Symbols as in tree_feyncalc.wl: e, sw, cw, MW, MZ, MH, masses mf[class, generation]; Lorentz indices li1..li4.*)


frRulesCv$ = {yl[a_, b_] :> IndexDelta[a, b] Sqrt[2] mf[2, a]/vev, yu[a_, b_] :> IndexDelta[a, b] Sqrt[2] mf[3, a]/vev,
   yd[a_, b_] :> IndexDelta[a, b] Sqrt[2] mf[4, a]/vev, CKM[a_, b_] :> IndexDelta[a, b]};
frSumCv$ = IndexSum[x_, {i_, 1, 3}] :> Sum[x, {i, 1, 3}];
frParCv$ = {vev -> 2 MW sw/e, lam -> MH^2 e^2/(8 MW^2 sw^2)};
commonCv$ = {FCGV["EL"] -> e, FCGV["SW"] -> sw, FCGV["CW"] -> cw, FCGV["MW"] -> MW, FCGV["MZ"] -> MZ, FCGV["MH"] -> MH,
   FCGV["ME"] -> mf[2, 1], FCGV["MM"] -> mf[2, 2], FCGV["ML"] -> mf[2, 3], FCGV["MU"] -> mf[3, 1], FCGV["MC"] -> mf[3, 2],
   FCGV["MT"] -> mf[3, 3], FCGV["MD"] -> mf[4, 1], FCGV["MS"] -> mf[4, 2], FCGV["MB"] -> mf[4, 3],
   EL -> e, SMP["e"] -> e, SMP["sin_W"] -> sw, SMP["cos_W"] -> cw, SMP["m_W"] -> MW, SMP["m_Z"] -> MZ, SMP["m_H"] -> MH};
massCv$ = {Me -> mf[2, 1], MMU -> mf[2, 2], MTA -> mf[2, 3], MU -> mf[3, 1], MC -> mf[3, 2], MT -> mf[3, 3],
   MD -> mf[4, 1], MS -> mf[4, 2], MB -> mf[4, 3],
   FCGV["Ml"][g_] :> mf[2, g], FCGV["Mu"][g_, ___] :> mf[3, g], FCGV["Md"][g_, ___] :> mf[4, g]};
chiralCv$ = {DiracGamma[6] -> (1 + DiracGamma[5])/2, DiracGamma[7] -> (1 - DiracGamma[5])/2};
(* FeynArts 3.12 on Mathematica 14 prints harmless RuleDelayed::rhs messages when it initializes a model *)
insCv$[model_, tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles}, Model -> model,
    GenericModel -> If[model === "SM", "Lorentz", model]], RuleDelayed::rhs];
ampCv$[model_, diags_, nout_] := FCFAConvert[
     Quiet[CreateFeynAmp[diags, Truncated -> True, GaugeRules -> {_GaugeXi -> 1, FAGaugeXi[__] -> 1}], RuleDelayed::rhs] /.
        If[model === "SM", {}, M$FACouplings] /. frRulesCv$ //. frSumCv$ /. frParCv$,
     IncomingMomenta -> {q}, OutgoingMomenta -> Take[{k1, k2, k3}, nout], LorentzIndexNames -> Take[{li1, li2, li3, li4}, nout + 1],
     ChangeDimension -> 4, List -> False, SMP -> False, DropSumOver -> True, UndoChiralSplittings -> True,
     TransversePolarizationVectors -> {}] /. commonCv$ /. massCv$ /. Conjugate[x_] :> x /. (GaugeXi | FAGaugeXi)[__] -> 1;
nDiagCv$[diags_] := Length[Quiet[CreateFeynAmp[diags], RuleDelayed::rhs]];
momConsCv$[x_, n_] := Expand[ExpandScalarProduct[MomentumExpand[FCI[x]] /.
     Momentum[q, d___] :> Sum[Momentum[ToExpression["k" <> ToString[i]], d], {i, n}]]];
normCv$[x_, n_] := Simplify[Expand[FCE[momConsCv$[DiracSimplify[x], n] /. chiralCv$] /. cw -> Sqrt[1 - sw^2] /. MZ -> MW/Sqrt[1 - sw^2]]];


(* ::Section:: *)
(*The vertex classes*)


(* ::Text:: *)
(*The coupling list C[...] of SM_FA.mod; generation and colour indices of the fermions are set to generation 1.*)


couplingsCv$ = Module[{txt = Import[FileNameJoin[{srcDirCv$, "generated", "SM_FA", "SM_FA.mod"}], "Text"]},
   ToExpression[StringReplace[#, RegularExpression["\\{e[0-9x, e]*\\}"] -> "{1}"]] & /@
    StringCases[txt, RegularExpression["(?m)^C\\[([^=]*)\\] =="] -> "{$1}"]];
couplingsCv$ = Select[couplingsCv$, FreeQ[#, V[4, ___] | U[4, ___]] &];
selfConjCv$ = V[1] | V[2] | S[1] | S[2];
antiCv$[f_] := If[MatchQ[f, selfConjCv$], f, -f];
toSMCv$[f_] := f /. {V[3] -> -V[3], S[3] -> -S[3], U[31] -> U[4], U[32] -> U[3]};
procCv$[c_] := {First[c]} -> (antiCv$ /@ Rest[c]);
Print["(a) vertex classes of the FeynRules model without gluons: ", Length[couplingsCv$], "   (expect 88)"];

t12Cv$ = CreateTopologies[0, 1 -> 2];
t13Cv$ = CreateTopologies[0, 1 -> 3, Adjacencies -> {4}];
resCv$ = Table[Module[{proc = procCv$[c], nout = Length[c] - 1, tops, dFR, dSM, aFR, aSM, r},
    tops = If[nout == 3, t13Cv$, t12Cv$];
    dFR = insCv$[frModelCv$, tops, proc];
    dSM = insCv$["SM", tops, toSMCv$ /@ proc /. -(-x_) :> x];
    aFR = normCv$[ampCv$[frModelCv$, dFR, nout], nout];
    aSM = normCv$[ampCv$["SM", dSM, nout], nout];
    r = If[aSM === 0, "SM.mod amplitude 0", Simplify[aFR/aSM]];
    {c, nDiagCv$[dFR], nDiagCv$[dSM], r, aFR =!= 0}], {c, couplingsCv$}];

(* ::Text:: *)
(*The rule.  Factors per field of the coupling: photon and photon ghost/antighost -1, G+ -i, G- +i, all others 1*)
(*(the ghost factors solved from the 23 ghost classes; the W and Z ghosts keep their sign although G+- changes phase).*)
(*Internal lines cancel: c(A)^2 = c(uA) c(-uA) = c(G+) c(G-) = 1.*)


cCv$[f_] := Switch[f, V[1] | U[1] | -U[1], -1, S[3], -I, -S[3], I, _, 1];
ruleCv$[c_] := Times @@ (cCv$ /@ (c /. F[n_, _] :> F[n]));
badCv$ = Select[resCv$, !(#[[4]] === ruleCv$[#[[1]]] && #[[2]] == 1 && #[[3]] == 1 && #[[5]]) &];
groupCv$ = GroupBy[resCv$, #[[4]] &, Length];
Print["(a) FR/SM.mod per class = product of c(f) over the fields (c = -1 for A, uA, -uA; -i for G+; +i for G-): ",
  Length[resCv$] - Length[badCv$], " of ", Length[resCv$], " classes;  exceptions: ", InputForm[badCv$]];
Print["(a) classes by ratio: ", InputForm[Normal[groupCv$]], ";  ghost classes: ", Count[resCv$, {c_, __} /; !FreeQ[c, U]],
  ";  internal lines: c(A)^2 = ", cCv$[V[1]]^2, ", c(uA) c(-uA) = ", cCv$[U[1]] cCv$[-U[1]], ", c(G+) c(G-) = ", cCv$[S[3]] cCv$[-S[3]]];


(* ::Subsubsection:: *)
(*Inspect: the table (coupling, FR diagrams, SM.mod diagrams, FR/SM.mod, rule)*)


If[$Notebooks, TableForm[{#[[1]], #[[2]], #[[3]], #[[4]], ruleCv$[#[[1]]]} & /@ resCv$]]

DeleteDirectory[modelTmpDirCv$, DeleteContents -> True];
