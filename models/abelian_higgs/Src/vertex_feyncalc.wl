(* ::Package:: *)

(* ::Title:: *)
(*Step (4): UV poles of the one-loop three- and four-point functions in a general R_xi gauge (abelian Higgs model)*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (4).  Uses the FeynArts model of this note (Src/generated/AbelianHiggs_FA) at*)
(*particle level, with GaugeXi kept.*)
(*  (a) three-point functions h h h, G G h, A A h, A G h with general external momenta: UV pole of the 1PI diagrams plus*)
(*      the diagrams with the tadpole attached through a zero-momentum h line (FJ), against the counterterm vertices of*)
(*      the note (Eq. (ctv)): c3 (h h h, G G h), cA (A A h), dZ_Phi (A G h);*)
(*  (b) four-point functions h h h h, G G G G, G G h h, A A h h, A A G G at zero external momenta (the UV pole of a*)
(*      function with omega = 0 is a constant): 1PI diagrams against c4 and dZ_Phi; A A A A has no pole;*)
(*  (c) C-odd functions (A A A, A h h, h h G, G G G, A G G, A A G): the UV pole of the 1PI diagrams vanishes.*)
(*Counterterms (K x Delta coefficients; note Eqs. (ct), (ctv)):*)
(*  dZ_Phi = (3 - xi) e^2, d_m2 = 4 lam - 3 e^2, d_lam = 10 lam - 6 e^2 + 3 e^4/lam,*)
(*  c3 = (d_lam + 3 dZ_Phi + d_m2)/2, c4 = d_lam + 2 dZ_Phi, cA = (dZ_Phi + d_m2 - d_lam)/2.*)
(*A counterterm vertex is c times the tree vertex (FeynArts form, the product of Feynman rules divided by i), so the*)
(*check is  K x UV(loop amplitude) + c x (tree amplitude) = 0.  The UV poles come from TID with UsePaVeBasis -> True and*)
(*FeynCalc's PaVeUVPart (no Gram determinants), with D = 4 - 2 ep and Delta = 1/ep.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file vertex_feyncalc.wl  (a few minutes).  Interactive:  ~/hep/bin/wopen vertex_feyncalc.wl, then "Run All Code" or Shift+Return cell by cell.*)


(* ::Section:: *)
(*Setup*)


$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
$FCAdvice = False;


srcDirVX$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelTmpDirVX$ = CreateDirectory[];
CopyDirectory[FileNameJoin[{srcDirVX$, "generated", "AbelianHiggs_FA"}], FileNameJoin[{modelTmpDirVX$, "AbelianHiggs_FA"}]];
FAPatch[PatchModelsOnly -> True, FAModelsDirectory -> FileNameJoin[{modelTmpDirVX$, "AbelianHiggs_FA"}], Quiet -> True];
modelFileVX$ = FileNameJoin[{modelTmpDirVX$, "AbelianHiggs_FA", "AbelianHiggs_FA"}];

(* everything in MA, MH, v, xi: EL -> MA/v, vev -> v, lam -> MH^2/(2 v^2) *)
convVX$ = {FCGV["EL"] -> MA/v, FCGV["MA"] -> MA, FCGV["MH"] -> MH, GaugeXi[A] -> xi, GaugeXi[V[1, ___]] -> xi,
   GaugeXi[S[2, ___]] -> xi, GaugeXi[U[1, ___]] -> xi, GaugeXi[S[1, ___]] -> 1, vev -> v, lam -> MH^2/(2 v^2)};
KK = (4 Pi)^2;
eN$ = MA/v; lamN$ = MH^2/(2 v^2);

insertVX$[tops_, proc_] := Quiet[InsertFields[tops, proc, InsertionLevel -> {Particles},
    Model -> modelFileVX$, GenericModel -> modelFileVX$], RuleDelayed::rhs];
convertVX$[fa_, in_, out_] := Quiet[FCFAConvert[fa /. M$FACouplings, IncomingMomenta -> in, OutgoingMomenta -> out,
      LoopMomenta -> {q}, LorentzIndexNames -> {mu, nu, rho, sig}, ChangeDimension -> D, List -> True, SMP -> False,
      DropSumOver -> True], RuleDelayed::rhs] /. convVX$ /.
   FeynAmpDenominator[PropagatorDenominator[0 | Momentum[0, ___], m_]] :> -1/m^2;

(* K x (coefficient of Delta) of the UV pole *)
uvVX$[x_] := Module[{r},
   r = TID[Contract[x], q, ToPaVe -> True, UsePaVeBasis -> True];
   r = PaVeUVPart[r];
   r = KK r /. D -> 4 - 2 ep;
   Simplify[SeriesCoefficient[r, {ep, 0, -1}]]];

(* a diagram belongs to the tadpole-at-the-vertex set if no tree propagator other than the zero-momentum h line
   (already replaced by -1/MH^2) is left *)
noTreeProp$[a_] := Cases[a, FeynAmpDenominator[x__] /; FreeQ[{x}, q], {0, Infinity}] === {};

tops3$ = CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {Reducible}];
tops3all$ = CreateTopologies[1, 1 -> 2];
tops4$ = CreateTopologies[1, 2 -> 2, ExcludeTopologies -> {Reducible}];
treeTops3$ = CreateTopologies[0, 1 -> 2];

(* counterterm coefficients (K x Delta) *)
dZPhi$ = (3 - xi) eN$^2; dm2$ = 4 lamN$ - 3 eN$^2; dlam$ = 10 lamN$ - 6 eN$^2 + 3 eN$^4/lamN$;
c3$ = (dlam$ + 3 dZPhi$ + dm2$)/2; c4$ = dlam$ + 2 dZPhi$; cA$ = (dZPhi$ + dm2$ - dlam$)/2;
Print["counterterm coefficients (K x Delta): c3 = ", Simplify[c3$ /. MH -> Sqrt[2 lam] v /. MA -> e v],
  ", c4 = ", Simplify[c4$ /. MH -> Sqrt[2 lam] v /. MA -> e v], ", cA = ", Simplify[cA$ /. MH -> Sqrt[2 lam] v /. MA -> e v]];


(* ::Section:: *)
(*(a) three-point functions*)


three$[label_, proc_, c_] := Module[{d1, a1, dAll, faAll, aAll, aTad, tree, uv1, uvT, res},
   d1 = insertVX$[tops3$, proc];
   a1 = convertVX$[CreateFeynAmp[d1, Truncated -> True, GaugeRules -> {}], {p1}, {p2, p3}];
   dAll = insertVX$[Complement[tops3all$, tops3$], proc];
   faAll = Quiet[CreateFeynAmp[dAll, Truncated -> True, GaugeRules -> {}], RuleDelayed::rhs];
   aAll = If[Length[faAll] == 0, {}, convertVX$[faAll, {p1}, {p2, p3}]];
   aTad = Select[aAll, noTreeProp$];
   tree = Total[convertVX$[CreateFeynAmp[insertVX$[treeTops3$, proc], Truncated -> True], {p1}, {p2, p3}]];
   FCClearScalarProducts[];
   uv1 = Total[uvVX$ /@ a1];
   uvT = If[aTad === {}, 0, Total[uvVX$ /@ aTad]];
   (* the poles come out with 4-dimensional metric tensors and momenta, the tree vertex with D-dimensional ones *)
   res = Simplify[ExpandScalarProduct[Contract[ChangeDimension[uv1 + uvT + c tree, 4] /. Momentum[p1, dim___] :> Momentum[p2 + p3, dim]]]];
   Print["(a) ", label, ": 1PI diagrams ", Length[a1], ", tadpole-attached ", Length[aTad], " (of ", Length[aAll],
     " reducible);  K UV(1PI) = ", InputForm[Simplify[uv1]], ",  K UV(tadpole part) = ", InputForm[Simplify[uvT]],
     ";  UV + counterterm = ", InputForm[res], "   (expect 0)"];
   res];

res3$ = {
   three$["h h h", {S[1]} -> {S[1], S[1]}, c3$],
   three$["G G h", {S[1]} -> {S[2], S[2]}, c3$],
   three$["A A h", {S[1]} -> {V[1], V[1]}, cA$],
   three$["A G h", {V[1]} -> {S[2], S[1]}, dZPhi$]};


(* ::Section:: *)
(*(b) four-point functions at zero external momenta*)


zeroMom$ = {Momentum[p1 | p2 | p3 | p4, dim___] :> 0};
four$[label_, proc_, c_, treeContact_] := Module[{d1, a1, uv1, res},
   d1 = insertVX$[tops4$, proc];
   a1 = convertVX$[CreateFeynAmp[d1, Truncated -> True, GaugeRules -> {}], {p1, p2}, {p3, p4}];
   a1 = a1 /. Momentum[pp_, dim___] :> Momentum[pp /. {p1 -> 0, p2 -> 0, p3 -> 0, p4 -> 0}, dim] /;
        FreeQ[pp, Polarization] /. Momentum[0, ___] -> 0;
   uv1 = Simplify[Total[uvVX$ /@ a1]];
   res = Simplify[Contract[ChangeDimension[uv1 + c treeContact, 4]]];
   Print["(b) ", label, ": 1PI diagrams ", Length[a1], ";  K UV = ", InputForm[uv1], ";  UV + counterterm = ",
     InputForm[res], "   (expect 0)"];
   res];

gMN$ = Pair[LorentzIndex[mu, D], LorentzIndex[nu, D]];
res4$ = {
   four$["h h h h", {S[1], S[1]} -> {S[1], S[1]}, c4$, -6 lamN$],
   four$["G G G G", {S[2], S[2]} -> {S[2], S[2]}, c4$, -6 lamN$],
   four$["G G h h", {S[2], S[2]} -> {S[1], S[1]}, c4$, -2 lamN$],
   four$["A A h h", {S[1], S[1]} -> {V[1], V[1]}, dZPhi$, 2 eN$^2 gMN$],
   four$["A A G G", {S[2], S[2]} -> {V[1], V[1]}, dZPhi$, 2 eN$^2 gMN$],
   four$["A A A A (no counterterm)", {V[1], V[1]} -> {V[1], V[1]}, 0, 0]};


(* ::Section:: *)
(*(c) C-odd functions*)


resOdd$ = Table[Module[{a1 = convertVX$[CreateFeynAmp[insertVX$[tops3$, pr], Truncated -> True, GaugeRules -> {}], {p1}, {p2, p3}], u},
    u = If[a1 === {}, 0, Simplify[ExpandScalarProduct[Contract[Total[uvVX$ /@ a1]]]]];
    Print["(c) ", pr, ": 1PI diagrams ", Length[a1], " (FeynArts makes none: no C-odd vertex), K UV = ", InputForm[u], "   (expect 0)"]; u],
   {pr, {{V[1]} -> {V[1], V[1]}, {V[1]} -> {S[1], S[1]}, {S[2]} -> {S[1], S[1]}, {S[2]} -> {S[2], S[2]},
     {V[1]} -> {S[2], S[2]}, {S[2]} -> {V[1], V[1]}}}];

Print["Summary (expect all 0): three-point ", res3$, ", four-point ", res4$, ", C-odd ", resOdd$];
