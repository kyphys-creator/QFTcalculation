(* ::Package:: *)

(* Stage 6 of the LHC tools (environment.pdf): the UFO of the SSM Z' (ZpSSM.fr on FeynRules' SM.fr) and the check of its
   vertices.  LoadModel[SM.fr, ZpSSM.fr] with the restrictions DiagonalCKM.rst and Massless.rst (t, b, tau massive), then
     (1) the Z' f f vertices against the Z f f vertices of SM.fr's fermion Lagrangian (both flavour-expanded): with Zp -> Z and
         gZp -> 1 they must be the same (the same couplings, the same sign), up to gamma = gamma P_L + gamma P_R, cw^2 + sw^2 = 1;
     (2) WriteUFO[LSM + LZp] to <out>/ZpSSM_UFO (Feynman gauge, as SM.fr).
   Batch:  wolframscript -file generate_zp.wl <out directory> *)

outDir$ = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], FileNameJoin[{DirectoryName[$InputFileName], "out"}]];
srcDir$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
smDir$ = FileNameJoin[{$FeynRulesPath, "Models", "SM"}];
SetDirectory[srcDir$];
LoadModel[FileNameJoin[{smDir$, "SM.fr"}], FileNameJoin[{srcDir$, "ZpSSM.fr"}]];
LoadRestriction[FileNameJoin[{smDir$, "DiagonalCKM.rst"}], FileNameJoin[{smDir$, "Massless.rst"}]];

(* (1) the vertices *)
fermionsQ$[v_] := Length[v[[1]]] == 3 && Count[v[[1]][[All, 1]], (vl | vlbar | l | lbar | uq | uqbar | dq | dqbar |
    e | mu | ta | ve | vm | vt | u | c | t | d | s | b | e | ebar | mubar | tabar | vebar | vmbar | vtbar | ubar | cbar | tbar |
    dbar | sbar | bbar)] == 2;
(* both flavour-expanded: SM.fr's LFermions keeps the generation index, LZpF is expanded by the restrictions *)
vZ$ = Select[FeynmanRules[LFermions, FlavorExpand -> True, ScreenOutput -> False], MemberQ[#[[1]][[All, 1]], Z] && fermionsQ$[#] &];
vZp$ = Select[FeynmanRules[LZpF, FlavorExpand -> True, ScreenOutput -> False], MemberQ[#[[1]][[All, 1]], Zp] && fermionsQ$[#] &];
key$[v_] := Sort[v[[1]] /. Zp -> Z];
zMap$ = Association[(key$[#] -> #[[2]]) & /@ vZ$];
(* the same form: gamma^mu P_R = gamma^mu - gamma^mu P_L (SM.fr's vertices are written with P_L and P_R; FeynRules turns
   gamma P_L + gamma P_R back into gamma, so the replacement goes this way), cw^2 = 1 - sw^2 *)
canon$[x_] := Simplify[Expand[x /. TensDot[Ga[a_], ProjP][s1_, s2_] :> Ga[a, s1, s2] - TensDot[Ga[a], ProjM][s1, s2]] /. cw -> Sqrt[1 - sw^2]];
diff$ = (canon$[(#[[2]] /. gZp -> 1) - Lookup[zMap$, Key[key$[#]], Missing[]]]) & /@ vZp$;
same$ = Length[vZp$] == Length[vZ$] && AllTrue[diff$, # === 0 &];
Print["Z f f vertices: ", Length[vZ$], ";  Z' f f vertices: ", Length[vZp$], ";  the same with Zp -> Z, gZp -> 1: ", same$];
If[!same$, Print["differences: ", diff$]];
Print["Z' e+ e- vertex: ", Select[vZp$, MemberQ[#[[1]][[All, 1]], e] &]];

(* (2) the UFO *)
If[!DirectoryQ[outDir$], CreateDirectory[outDir$]];
SetDirectory[outDir$];
WriteUFO[LSM + LZp, Output -> "ZpSSM_UFO"];
Print["UFO written to ", FileNameJoin[{outDir$, "ZpSSM_UFO"}]];
