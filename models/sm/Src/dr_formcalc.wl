(* ::Package:: *)

(* ::Title:: *)
(*Step (5): Delta r from FormCalc's renormalization constants against the note (unpatched FeynArts 3.12, FormCalc 9.10, LoopTools)*)


(* ::Text:: *)
(*Research note models/sm, step (5).  Run in its own kernel after dr_numeric.wl.  At the MW of dr_numeric.wl, section (b)*)
(*(the note's point, all fermions perturbative with the effective light-quark masses), Delta r from FeynArts' SM.mod*)
(*(Denner's signs: Sigma^AZ and dZZA1 opposite to the note's):*)
(*  (Sigma^W_T(0) - dMWsq1)/MW^2 + 2 dZe1 - 2 dSW1/SW + dZZA1/(SW CW) + alpha/(4 Pi SW^2)[6 + (7 - 4 SW^2)/(2 SW^2) ln CW^2],*)
(*with Sigma^W_T(0) = SelfEnergy[V[3] -> V[3], 0], against the value of the note's Eq. (dr) in results/dr_values.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file dr_formcalc.wl  (in its own kernel; run dr_numeric.wl first).*)


Get["FeynArts`"];
Get["FormCalc`"];
srcDirDF$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
SetDirectory[CreateDirectory[]];
vals$ = Association[Rule @@@ (Import[FileNameJoin[{srcDirDF$, "results", "dr_values.csv"}], "CSV"][[2 ;;]])];
mwFix$ = Rationalize[vals$["note_MW"], 0];
drNoteFix$ = vals$["note_formula_delta_r_at_note_MW"];
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
SetDelta[0]; SetLambda[1]; SetMudim[N[(911880/10000)^2]];
pdg$ = <|"alpha" -> 1000000000/137035999177, "MZ" -> 911880/10000, "MH" -> 12520/100,
   "gens" -> {{(51099895/10^11)^2, (6/100)^2, (7/100)^2}, {(1056583755/10^10)^2, (127/100)^2, (1/10)^2},
     {(177686/10^5)^2, (17257/100)^2, (418/100)^2}}|>;


rcDN$ = Flatten[Quiet[CalcRenConst[{dMWsq1, dZe1, dSW1, dZZA1}]] /. RenConstList[RenConst] -> List];
(* without options SelfEnergy uses CreateTopologies' defaults, which include the tadpole-attached diagrams; RenConst passes
   ExcludeTopologies -> Internal (no tadpoles, the note's delta t = -T scheme) *)
sW0FC$ = Quiet[SelfEnergy[V[3] -> V[3], 0, ExcludeTopologies -> Internal]];
mfDN[1, _] := 0; mfDN[t_, g_] := Sqrt[pdg$["gens"][[g, t - 1]]];
evalFC$[x_, mw_] := Module[{cw = mw/pdg$["MZ"], sw, y},
   sw = Sqrt[1 - cw^2];
   y = x //. {a_. SumOver[g_, n_, ___] :> Sum[a /. g -> i, {i, n}]};
   y = y /. {Mf2[t_, g_Integer] :> mfDN[t, g]^2, Mf[t_, g_Integer] :> mfDN[t, g], CKM[i_, j_] :> KroneckerDelta[i, j],
       Conjugate[CKM[i_, j_]] :> KroneckerDelta[i, j]} /.
     Flatten[MapThread[{#1 -> mfDN @@ #2, ToExpression[ToString[#1] <> "2"] -> (mfDN @@ #2)^2} &,
       {{ME, MM, ML, MU, MC, MT, MD, MS, MB}, {{2, 1}, {2, 2}, {2, 3}, {3, 1}, {3, 2}, {3, 3}, {4, 1}, {4, 2}, {4, 3}}}]] /.
     {Alfa -> pdg$["alpha"], Alfa2 -> pdg$["alpha"]^2, EL -> Sqrt[4 Pi pdg$["alpha"]], MW -> mw, MW2 -> mw^2, MZ -> pdg$["MZ"],
      MZ2 -> pdg$["MZ"]^2, MH -> pdg$["MH"], MH2 -> pdg$["MH"]^2, SW -> sw, CW -> cw, SW2 -> sw^2, CW2 -> cw^2, Finite -> 1};
   y = y /. {Den[pp_, mm_] :> 1/(pp - mm), Den[pp_, mm_, d_] :> 1/(pp - mm)^d, IGram[gg_] :> 1/gg};
   Re[N[N[y, 20] /. B0i[id_, args__] :> B0i[id, Sequence @@ N[{args}]] /. A0[m_] :> A0[N[m]]]]];
fcVals$ = Association[Table[r[[1]] -> evalFC$[r[[1]] //. rcDN$, mwFix$], {r, rcDN$}]];
sW0num$ = evalFC$[sW0FC$, mwFix$];
drFC$ = Module[{cw = mwFix$/pdg$["MZ"], sw},
   sw = Sqrt[1 - cw^2];
   (sW0num$ - fcVals$[dMWsq1])/mwFix$^2 + 2 fcVals$[dZe1] - 2 fcVals$[dSW1]/sw + fcVals$[dZZA1]/(sw cw) +
    pdg$["alpha"]/(4 Pi sw^2) (6 + (7 - 4 sw^2)/(2 sw^2) Log[cw^2])];



fmtDF$[x_] := ToString[NumberForm[x, 16], OutputForm];
Print["(c) at MW = ", fmtDF$[N[mwFix$]], ": Delta r from FormCalc = ", fmtDF$[drFC$], ",  from the note's Eq. (dr) = ",
  fmtDF$[drNoteFix$], ",  rel. diff. ", ToString[NumberForm[Abs[drFC$/drNoteFix$ - 1], 2, NumberFormat -> (If[#3 == "", #1, Row[{#1, "e", #3}]] &)], OutputForm],
  ";  symbols left: ", Union[Cases[{drFC$}, _Symbol, Infinity]]];
Export[FileNameJoin[{srcDirDF$, "results", "dr_formcalc.csv"}], "quantity,value\nformcalc_delta_r_at_note_MW," <> ToString[CForm[drFC$]] <>
   "\nnote_delta_r_at_note_MW," <> ToString[CForm[drNoteFix$]] <> "\n", "Text"];
