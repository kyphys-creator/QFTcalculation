(* ::Package:: *)

(* ::Title:: *)
(*Step (4): the on-shell counterterms from FormCalc's RenConst against the note (unpatched FeynArts 3.12, FormCalc 9.10, LoopTools)*)


(* ::Text:: *)
(*Research note models/sm, step (4).  Run in its own kernel: the patched (FeynCalc) and unpatched FeynArts must not be*)
(*loaded together.  CalcRenConst computes the renormalization constants of FeynArts' SM.mod (Denner's conventions,*)
(*Feynman gauge, self-energies without tadpoles, CKM = 1) from MassRC, FieldRC, TadpoleRC:*)
(*  dMWsq1, dMZsq1, dMHsq1, dZW1, dZZZ1, dZAA1, dZAZ1, dZZA1, dZH1, dTH1, dSW1 = CW^2/(2 SW) (dMZsq1/MZ^2 - dMWsq1/MW^2),*)
(*  dZe1 = -(dZAA1 + SW/CW dZZA1)/2.*)
(*Both they and the note's counterterms (results/ct_note.m from ct_feyncalc.wl, Eqs. (ct), (dsw), (dZe)) are evaluated*)
(*with the same LoopTools: Delta = 0, mu^2 = MZ^2, photon mass^2 lambda^2 = 1 GeV^2 for the IR-divergent derivative in*)
(*dZW1 (the same function appears in the note's delta Z_W).  Conventions: A^Denner = -A changes the sign of dZAZ1 and*)
(*dZZA1; dSW1 = delta s_W = (s_W/2) delta s_W^2/s_W^2; dTH1 = delta t.  "Finite" (the D - 4 times pole terms) is 1.*)
(*Point of oneloop_feyncalc.wl, section (e).  Writes results/ct_comparison.csv.*)


(* ::Text:: *)
(*How to run.  Batch:  wolframscript -file ct_formcalc.wl  (in its own kernel; run ct_feyncalc.wl first).*)


(* ::Section:: *)
(*FormCalc*)


Get["FeynArts`"];
Get["FormCalc`"];
srcDirRC$ = Which[
   StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName],
   $Notebooks, NotebookDirectory[],
   True, Directory[]];
SetDirectory[CreateDirectory[]];   (* FormCalc writes its FORM files here *)
rcNames$ = {dMWsq1, dZW1, dMZsq1, dZZZ1, dZAA1, dZZA1, dZAZ1, dMHsq1, dZH1, dTH1, dSW1, dZe1};
t0RC$ = AbsoluteTime[];
rcList$ = Quiet[CalcRenConst[rcNames$]];
rcRules$ = Flatten[rcList$ /. RenConstList[RenConst] -> List];
Print["(a) FormCalc: ", Length[rcRules$], " renormalization constants in ", Round[AbsoluteTime[] - t0RC$], " s: ", rcRules$[[All, 1]]];


(* ::Section:: *)
(*Numerical evaluation with LoopTools*)


Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
mwRC = 803692/10000; mzRC = 911880/10000; mhRC = 12520/100;
mu2RC = mzRC^2;
SetMudim[N[mu2RC]]; SetDelta[0]; SetLambda[1];
massesRC = <|{2, 1} -> 51099895/10^11, {2, 2} -> 1056583755/10^10, {2, 3} -> 177686/10^5,
   {3, 1} -> 216/10^5, {3, 2} -> 12730/10^4, {3, 3} -> 17257/100,
   {4, 1} -> 470/10^5, {4, 2} -> 935/10^4, {4, 3} -> 4183/10^3|>;
mfRC[1, _] := 0; mfRC[t_, g_] := massesRC[{t, g}];
cwRC = mwRC/mzRC; swRC = Sqrt[1 - cwRC^2];
parRC$ = {Alfa -> 1000000000/137035999177, Alfa2 -> (1000000000/137035999177)^2, EL -> Sqrt[4 Pi 1000000000/137035999177],
   MW -> mwRC, MW2 -> mwRC^2, MZ -> mzRC, MZ2 -> mzRC^2, MH -> mhRC, MH2 -> mhRC^2,
   SW -> swRC, CW -> cwRC, SW2 -> swRC^2, CW2 -> cwRC^2, Finite -> 1};
(* SM.mod's named fermion masses (FormCalc writes some of them, e.g. MB2, instead of Mf2[4, 3]) *)
namedRC$ = Flatten[MapThread[{#1 -> mfRC @@ #2, ToExpression[ToString[#1] <> "2"] -> (mfRC @@ #2)^2} &,
     {{ME, MM, ML, MU, MC, MT, MD, MS, MB}, {{2, 1}, {2, 2}, {2, 3}, {3, 1}, {3, 2}, {3, 3}, {4, 1}, {4, 2}, {4, 3}}}]];
parRC$ = Join[parRC$, namedRC$];
genRC$ = {a_. SumOver[g_, n_, ___] :> Sum[a /. g -> i, {i, n}]};
mfRulesRC$ = {Mf2[t_, g_Integer] :> mfRC[t, g]^2, Mf[t_, g_Integer] :> mfRC[t, g], CKM[i_, j_] :> KroneckerDelta[i, j],
   CKMC[i_, j_] :> KroneckerDelta[i, j], Conjugate[CKM[i_, j_]] :> KroneckerDelta[i, j]};
evalRC$[x_] := Module[{y = Expand[x //. genRC$] /. mfRulesRC$ /. parRC$},
   y = N[y, 20] /. B0i[id_, args__] :> B0i[id, Sequence @@ N[{args}]] /. A0[m_] :> A0[N[m]];
   N[y]];
fcVals$ = Association[];
Do[fcVals$[r[[1]]] = Re[evalRC$[r[[1]] //. rcRules$]], {r, rcRules$}];
Print["(b) FormCalc values: ", InputForm[Normal[fcVals$]]];
Print["   symbols left: ", Union[Cases[Values[fcVals$], _Symbol, Infinity]], "   (expect none)"];


(* ::Text:: *)
(*The note's counterterms (ct_feyncalc.wl): B0OL[p, m1^2, m2^2] and DB0OL -> LoopTools B0, DB0.*)


ctNote$ = Get[FileNameJoin[{srcDirRC$, "results", "ct_note.m"}]];
evalNote$[x_] := Re[N[x /. {B0OL[p_, a_, b_] :> B0[N[p], N[a], N[b]], DB0OL[p_, a_, b_] :> DB0[N[p], N[a], N[b]]}]];
noteVals$ = Association[Table[c[[1]] -> evalNote$[c[[2]]], {c, ctNote$}]];
noteVals$["dsw2"] = (cwRC^2/swRC^2) (noteVals$["dMZsq"]/mzRC^2 - noteVals$["dMWsq"]/mwRC^2);
noteVals$["dZe"] = -noteVals$["dZAA"]/2 + swRC/(2 cwRC) noteVals$["dZZA"];
Print["(c) note values: ", InputForm[Normal[noteVals$]]];


(* ::Section:: *)
(*Comparison*)


(* {name in the note, FormCalc symbol, factor: FormCalc = factor x note} *)
mapRC$ = {{"dMWsq", dMWsq1, 1}, {"dZW", dZW1, 1}, {"dMZsq", dMZsq1, 1}, {"dZZZ", dZZZ1, 1}, {"dZAA", dZAA1, 1},
   {"dZZA", dZZA1, -1}, {"dZAZ", dZAZ1, -1}, {"dMHsq", dMHsq1, 1}, {"dZH", dZH1, 1}, {"dt", dTH1, 1},
   {"dsw2", dSW1, N[swRC/2]}, {"dZe", dZe1, 1}};
rowsRC$ = Table[Module[{nv = noteVals$[m[[1]]], fv = fcVals$[m[[2]]]},
    {m[[1]], ToString[m[[2]]], m[[3]], nv, fv, If[fv == 0, Abs[nv m[[3]]], Abs[fv/(m[[3]] nv) - 1]]}], {m, mapRC$}];
fmtRC$[x_, n_] := ToString[NumberForm[x, n, NumberFormat -> (If[#3 == "", #1, Row[{#1, "e", #3}]] &)], OutputForm];
Do[Print["   ", StringPadRight[r[[1]], 6], StringPadRight[r[[2]], 8], " note x factor ", fmtRC$[N[r[[3]] r[[4]]], 16],
   "   FormCalc ", fmtRC$[r[[5]], 16], "   rel. diff. ", fmtRC$[r[[6]], 2]], {r, rowsRC$}];
Print["(d) max relative difference FormCalc vs the note: ", Max[rowsRC$[[All, 6]]], "   (", Length[rowsRC$], " counterterms; Delta = 0, mu = MZ)"];
Export[FileNameJoin[{srcDirRC$, "results", "ct_comparison.csv"}],
  StringRiffle[Prepend[StringRiffle[{#[[1]], #[[2]], ToString[CForm[N[#[[3]]]]], ToString[CForm[#[[4]]]], ToString[CForm[#[[5]]]],
        ToString[CForm[#[[6]]]]}, ","] & /@ rowsRC$, "name,formcalc,factor,note,formcalc_value,rel_diff"], "\n"] <> "\n", "Text"];
Print["(d) wrote results/ct_comparison.csv"];
(* the loop functions of the note's counterterms with their LoopTools values, for ct_numeric.py *)
funcsRC$ = Union[Cases[ctNote$, _B0OL | _DB0OL, Infinity]];
ltRC$[B0OL[p_, a_, b_]] := B0[N[p], N[a], N[b]];
ltRC$[DB0OL[p_, a_, b_]] := DB0[N[p], N[a], N[b]];
lineRC$[f_] := Module[{v = N[ltRC$[f]]},
   StringRiffle[Join[{If[Head[f] === B0OL, "B0", "DB0"]}, ToString[CForm[N[#, 17]]] & /@ (List @@ f),
     {ToString[CForm[Re[v]]], ToString[CForm[Im[v]]]}], ","]];
Export[FileNameJoin[{srcDirRC$, "results", "ct_functions.csv"}],
  StringRiffle[Prepend[lineRC$ /@ funcsRC$, "func,p2,m1sq,m2sq,re_lt,im_lt"], "\n"] <> "\n", "Text"];
Print["(d) wrote ", Length[funcsRC$], " loop functions to results/ct_functions.csv;  LoopTools lambda^2 = ", GetLambda[], ", mu^2 = ", GetMudim[]];
