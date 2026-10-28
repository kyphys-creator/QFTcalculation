(* ::Package:: *)

(* ::Title:: *)
(*Step (5), FormCalc: the one-loop h -> A A amplitude in Feynman gauge with the unpatched FeynArts 3.12 and FormCalc 9.10*)


(* ::Text:: *)
(*Research note models/abelian_higgs, step (5); independent of FeynCalc.  Run in its own kernel: the patched (FeynCalc) and*)
(*unpatched FeynArts must not be loaded together.  Feynman gauge (FeynArts' default GaugeRules), the FeynRules model*)
(*Src/generated/AbelianHiggs_FA.*)
(*  - one-loop diagrams of h(k1) -> A(k2) A(k3) without the external-leg corrections: the 1PI diagrams and the tadpole*)
(*    attached to the A A h h vertex (FJ), 14 in all;*)
(*  - CalcFeynAmp with Dimension -> D (the rational terms of the UV poles are added, FormCalc's symbol Finite = 1) and*)
(*    PaVeReduce -> True (only A0, B0, C0 are left);*)
(*  - the two form factors of  M = F_g conj(eps2).conj(eps3) + F_b (conj(eps2).k1)(conj(eps3).k1)  and the tree*)
(*    (2 e MA conj(eps2).conj(eps3)) are written to results/nlo_width_formcalc.m with the loop functions as fcA0[m^2],*)
(*    fcB0[p^2, m1^2, m2^2], fcC0[p1^2, p2^2, (p1 + p2)^2, m1^2, m2^2, m3^2] (LoopTools' arguments), in e, MA, mhsq = MH^2.*)
(*FormCalc's loop amplitude carries the factor 1/(16 pi^2) through Alfa = e^2/(4 pi) and Alfa2 = Alfa^2.*)
(*Batch: wolframscript -file nlo_width_formcalc.wl  (in its own kernel)*)


Get["FeynArts`"];
Get["FormCalc`"];

srcDirWF$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
modelWF$ = FileNameJoin[{srcDirWF$, "generated", "AbelianHiggs_FA", "AbelianHiggs_FA"}];   (* FeynRules output, unpatched *)
workDirWF$ = CreateDirectory[];
SetDirectory[workDirWF$];   (* FormCalc writes its FORM files here *)

procWF$ = {S[1]} -> {V[1], V[1]};
diag0WF$ = InsertFields[CreateTopologies[0, 1 -> 2], procWF$, InsertionLevel -> {Particles}, Model -> modelWF$,
   GenericModel -> modelWF$];
diag1WF$ = InsertFields[CreateTopologies[1, 1 -> 2, ExcludeTopologies -> {WFCorrections}], procWF$,
   InsertionLevel -> {Particles}, Model -> modelWF$, GenericModel -> modelWF$];
Print["one-loop diagrams (expect 14: 10 1PI, 4 tadpole-attached): ", Length[CreateFeynAmp[diag1WF$]]];

tree$ = CalcFeynAmp[CreateFeynAmp[diag0WF$] /. M$FACouplings];
loop$ = CalcFeynAmp[CreateFeynAmp[diag1WF$] /. M$FACouplings, Dimension -> D, PaVeReduce -> True];

(* everything explicit: subexpressions, abbreviations, FormCalc's constants, the model's parameters *)
explicitWF$[a_] := Module[{x = a[[1]] //. Subexpr[] //. Abbr[]},
   (* FormCalc evaluates MH^2 to MH2 and EL^2 to 4 Pi Alfa, so EL is replaced by the plain symbol e first and MH2 by
      mhsq (MH^2 again in the reading script) *)
   x = x /. {IGram[y_] :> 1/y, Finite -> 1} /. {Alfa2 -> e^4/(16 Pi^2), Alfa -> e^2/(4 Pi), MH2 -> mhsq} /. EL -> e /.
     {lam -> mhsq e^2/(2 MA^2), vev -> MA/e};
   x /. {A0[m2_] :> fcA0[m2], B0i[bb0, p_, m1_, m2_] :> fcB0[p, m1, m2],
     C0i[cc0, a1_, a2_, a3_, m1_, m2_, m3_] :> fcC0[a1, a2, a3, m1, m2, m3]}];
treeX$ = explicitWF$[tree$];
loopX$ = Expand[explicitWF$[loop$]];
Print["loop functions left: ", Union[Cases[loopX$, (fcA0 | fcB0 | fcC0)[__], Infinity]]];
Print["other heads (expect none): ", Union[Cases[loopX$, (h : B0i | C0i | A0i | D0i | Den | Pair)[x___] /; FreeQ[{x}, ec | k], Infinity]]];

e23$ = Pair[ec[2], ec[3]]; e2k$ = Pair[ec[2], k[1]]; e3k$ = Pair[ec[3], k[1]];
fgWF$ = Simplify[Coefficient[loopX$, e23$] /. {e2k$ -> 0, e3k$ -> 0}];
fbWF$ = Simplify[Coefficient[Coefficient[loopX$, e2k$], e3k$]];
restWF$ = Simplify[loopX$ - fgWF$ e23$ - fbWF$ e2k$ e3k$];
treeG$ = Simplify[Coefficient[treeX$, e23$]];
Print["tree: coefficient of conj(eps2).conj(eps3) (expect 2 e MA): ", treeG$, ";  remainder of the loop amplitude (expect 0): ", restWF$];

Put[{"tree" -> treeG$, "Fg" -> fgWF$, "Fb" -> fbWF$}, FileNameJoin[{srcDirWF$, "results", "nlo_width_formcalc.m"}]];
Print["written results/nlo_width_formcalc.m"];
