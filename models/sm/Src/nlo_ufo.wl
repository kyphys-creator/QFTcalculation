(* ::Package:: *)

(* ::Title:: *)
(*Step (9b), 3 of 3: the note's NLO UFO with NLOCT's R2 vertices and the FJ counterterms in counterterm form*)


(* ::Text:: *)
(*FeynRules: R2 vertices from Src/generated/SM_R2.m (NLOCT, the note's own model, Feynman gauge); UV counterterm*)
(*vertices from results/nlo_fjct.m (nlo_fjct.wl), for nu nubar -> nu nubar (MadLoop has no tadpole diagrams and no*)
(*self-energies on external legs):*)
(*  Z Z:        I g^{mu nu} (dMZ2 - Sigma_tad^ZZ)                (MS-bar mass pole; the tadpole diagrams as a counterterm);*)
(*  Z f fbar:   the tree vertex times [de/e - (1/2) dcw2 (1/cw^2 - 1/sw^2) + dZnu]   (f = ve, vm, vt; MS-bar poles; dZnu on*)
(*              shell, -Sigma^L_nu(0), for the external legs; no Z field renormalization).*)
(*Poles are 1/FR$Eps, the scale FR$MU (the UFO's MU_R).  The parameters of the UFO are then the note's MS-bar parameters.*)
(*Writes Src/generated/SM_NLO_FJ_UFO (overwritten).  Batch: wolframscript -file nlo_ufo.wl  (after nlo_writect.wl, nlo_fjct.wl)*)


srcDirNU$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNU$];
LoadModel["SM.fr"];
SetDirectory[FileNameJoin[{srcDirNU$, "generated"}]];
R2$vertlist = Get["SM_R2.m"];
FR$InteractionOrderPerturbativeExpansion = {{QCD, 1}, {QED, 1}};   (* as in SM_CT.nlo *)
Print["NLOCT R2 vertices: ", Length[R2$vertlist], "  (NLOCT's on-shell UV vertices are not used)"];

ct$ = Get[FileNameJoin[{srcDirNU$, "results", "nlo_fjct.m"}]];
(* d/FR$Eps for the pole coefficients, {pole, finite} lists for the Laurent pairs *)
pole$[x_] := x/FR$Eps;
laur$[{p_, f_}] := p/FR$Eps + f;
dcw2$ = ct$["dMW2"]/MZ^2 - MW^2 ct$["dMZ2"]/MZ^4;
dlng$ = pole$[ct$["de"] - dcw2$/2 (1/cw^2 - 1/sw^2)];
gamPL$ = TensDot[Ga[Index[Lorentz, Ext[3]]], ProjM][Index[Spin, Ext[1]], Index[Spin, Ext[2]]];
treeZnn$ = I ee (cw^2 + sw^2)/(2 cw sw) gamPL$;
uvFJ$ = Join[
   Table[{{{anti[f], 1}, {f, 2}, {Z, 3}}, treeZnn$ (dlng$ + laur$[ct$["dZnuL"]]) IPL[{e, W}]}, {f, {ve, vm, vt}}],
   {{{{Z, 1}, {Z, 2}}, I (pole$[ct$["dMZ2"]] - laur$[ct$["tadZZ"]]) ME[Index[Lorentz, Ext[1]], Index[Lorentz, Ext[2]]] IPL[{W}]}}];
Print["FJ counterterm vertices: ", uvFJ$[[All, 1, All, 1]]];

FeynmanGauge = True;
If[DirectoryQ["SM_NLO_FJ_UFO"], DeleteDirectory["SM_NLO_FJ_UFO", DeleteContents -> True]];
WriteUFO[LSM, UVCounterterms -> uvFJ$, R2Vertices -> R2$vertlist, Output -> "SM_NLO_FJ_UFO"];
(* MadGraph writes decimals with 7 digits in Fortran: rational coefficients back to ratios (spinor QED note, nlo_ufo.wl) *)
exactUFO$[file_] := Module[{txt = Import[file, "Text"], new},
   new = StringReplace[txt, RegularExpression["(?<![\\w.])(\\d+\\.\\d{7,})"] :>
       Module[{r = Rationalize[ToExpression["$1"], 10^-15]},
         If[Head[r] === Rational, "(" <> ToString[Numerator[r]] <> "./" <> ToString[Denominator[r]] <> ".)", "$1"]]];
   Export[file, new, "Text"];
   Length[StringCases[txt, RegularExpression["(?<![\\w.])\\d+\\.\\d{7,}"]]]];
Print["decimal coefficients made exact: ", exactUFO$[FileNameJoin[{Directory[], "SM_NLO_FJ_UFO", #}]] & /@ {"couplings.py", "CT_couplings.py"}];
Print["written: ", FileNames["SM_NLO_FJ_UFO"]];
