(* ::Package:: *)

(* Step 1 of the stable-lepton workflow (../README.md): the UFO of VLL.fr on FeynRules' SM.fr and the check of its
   vertices.  LoadModel[SM.fr, VLL.fr] with the restrictions DiagonalCKM.rst and Massless.rst (t, b, tau massive), then
     (1) the LV LV A and LV LV Z vertices against the e e A and e e Z vertices of SM.fr's fermion Lagrangian
         (flavour-expanded): the photon vertices must be the same, and the Z vertex of LV must be the right-handed part of
         the electron's in both chiralities (written as a gamma^mu + b gamma^mu P_L: LV's a is the electron's a, LV's b is 0);
     (2) WriteUFO[LSM + LLV] to <out>/VLL_UFO (Feynman gauge, as SM.fr).
   Batch:  wolframscript -file generate_vll.wl <out directory> *)

outDir$ = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], FileNameJoin[{DirectoryName[$InputFileName], "out"}]];
srcDir$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
smDir$ = FileNameJoin[{$FeynRulesPath, "Models", "SM"}];
SetDirectory[srcDir$];
LoadModel[FileNameJoin[{smDir$, "SM.fr"}], FileNameJoin[{srcDir$, "VLL.fr"}]];
LoadRestriction[FileNameJoin[{smDir$, "DiagonalCKM.rst"}], FileNameJoin[{smDir$, "Massless.rst"}]];

(* (1) the vertices *)
vLV$ = FeynmanRules[LLV, ScreenOutput -> False];
vSM$ = FeynmanRules[LFermions, FlavorExpand -> True, ScreenOutput -> False];
pick$[v_, f_, V_] := Select[v, Sort[#[[1]][[All, 1]]] === Sort[{f, f /. {LV -> LVbar, e -> ebar}, V}] &];
(* a gamma^mu + b gamma^mu P_L, with gamma^mu P_R = gamma^mu - gamma^mu P_L, cw^2 = 1 - sw^2.  TensDot is renamed first:
   FeynRules' TensDot[Ga[_], ProjM][_, _] does not match itself as a pattern *)
ab$[x_] := Module[{y = Expand[(x /. TensDot -> td$) /. {td$[Ga[_], ProjP][_, _] -> gV$ - gL$, td$[Ga[_], ProjM][_, _] -> gL$,
                                                        Ga[_, _, _] -> gV$}]},
  Simplify[{Coefficient[y, gV$], Coefficient[y, gL$], y /. {gV$ -> 0, gL$ -> 0}} /. cw -> Sqrt[1 - sw^2]]];
res$ = Table[
  Module[{l = pick$[vLV$, LV, V], s = pick$[vSM$, e, V], cl, cs},
    If[Length[l] != 1 || Length[s] != 1, {V, False, l, s},
      cl = ab$[l[[1, 2]]]; cs = ab$[s[[1, 2]]];
      Print[V, " vertex: LV ", InputForm[l[[1]]], ";  e ", InputForm[s[[1]]]];
      Print[V, " vertex as {a, b, rest} of a gamma^mu + b gamma^mu P_L: LV ", InputForm[cl], ";  e ", InputForm[cs]];
      {V, Simplify[cl[[1]] - cs[[1]]] === 0 && cl[[2]] === 0 && cl[[3]] === 0 && cs[[3]] === 0}]],
  {V, {A, Z}}];
Print["LV vertices: ", Length[vLV$], ";  the photon and Z vertices are the right-handed electron's: ",
  And @@ (#[[2]] & /@ res$)];

(* (2) the UFO *)
If[!DirectoryQ[outDir$], CreateDirectory[outDir$]];
SetDirectory[outDir$];
WriteUFO[LSM + LLV, Output -> "VLL_UFO"];
Print["UFO written to ", FileNameJoin[{outDir$, "VLL_UFO"}]];
