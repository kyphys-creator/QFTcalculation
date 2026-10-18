(* ::Package:: *)

(* ::Title:: *)
(*Step (9), 7 of 7: the CKM NLO UFO with NLOCT's R2 vertices and the FJ counterterms with the CKM counterterm*)


(* ::Text:: *)
(*As the SM note's nlo_ufo.wl, for SM_CKM.fr.  FeynRules: R2 vertices from Src/generated/SM_CKM_R2.m (NLOCT, Feynman*)
(*gauge); UV counterterm vertices*)
(*  - of the counterterm Lagrangian (ctSym of nlo_ckm_ctrules.wl) with the constants replaced by the CT parameters of*)
(*    nlo_ckm_ctparams.wl: the MS-bar (FJ) parameter constants and NLOCT's on-shell field constants, with the off-diagonal*)
(*    quark ones (the LSZ factors of the external legs, which MadLoop does not dress with self-energies);*)
(*  - of the CKM counterterm (dvSym) with the MS-bar dV of note Eq. (dV);*)
(*  - of the tadpole shift H -> H + dvT (two and three legs).*)
(*The UFO's parameters are the note's MS-bar parameters at the scale MU_R; the CT parameters are numbers at the point of*)
(*nlo_ckm_ctparams.wl (the param_card must have that point; MU_R is free).  Post-processing as in the SM note: the CT*)
(*parameters move from parameters.py to CT_parameters.py, the UV vertices get empty loop_particles, and decimal*)
(*coefficients become ratios.  Writes Src/generated/SM_CKM_NLO_UFO (overwritten).  Batch: wolframscript -file nlo_ckm_ufo.wl*)


srcDirNU$ = DirectoryName[$InputFileName];
$FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
SetDirectory[$FeynRulesPath];
Get["FeynRules`"];
SetDirectory[srcDirNU$];
LoadModel["SM_CKM.fr", FileNameJoin[{"generated", "SM_CKM_FJct.fr"}]];
SetDirectory[FileNameJoin[{srcDirNU$, "generated"}]];
(* the two- and three-point R2 vertices only: the four-point ones (W W G+ G-, W W W W, ...: with the CKM sums up to 4e4
   leaves) keep WriteUFO for more than an hour in splitting the vertices, and no process of step (9) has them (W -> u dbar
   and the flavour-changing processes need the R2 vertices f fbar V, f fbar S and the two-point ones; there is no
   four-fermion R2 vertex) *)
r2AllNU$ = Get["SM_CKM_R2.m"];
R2$vertlist = Select[r2AllNU$, Length[#[[1]]] <= 3 &];
FR$InteractionOrderPerturbativeExpansion = {{QCD, 1}, {QED, 1}};
Print["NLOCT R2 vertices: ", Length[r2AllNU$], ";  used (two and three points): ", Length[R2$vertlist]];

symNU$ = Get["SM_CKM_CTsym.m"];
parNU$ = Get["SM_CKM_FJctpar.m"];
ctNU$ = DeleteCases[{#[[1]], Expand[#[[2]] /. parNU$["rules"]]} & /@ symNU$["ctSym"], {_, 0}];
dvNU$ = DeleteCases[{#[[1]], Expand[#[[2]] /. parNU$["rules"]]} & /@ symNU$["dvSym"], {_, 0}];
tadNU$ = {#[[1]], (FJdvT /. parNU$["rules"]) #[[2]]} & /@ Select[symNU$["tadSym"], Length[#[[1]]] >= 2 &];
uvFJ$ = {#[[1]], #[[2]] IPL[{W}]} & /@ MergeVertices[ctNU$, dvNU$, tadNU$];
Print["UV counterterm vertices: ", Length[uvFJ$], " (counterterm Lagrangian ", Length[ctNU$], ", CKM ", Length[dvNU$], ", tadpole ",
  Length[tadNU$], ");  legs ", Union[Length /@ uvFJ$[[All, 1]]]];
If[! FreeQ[uvFJ$, FR$delta | FR$deltaZ | dVsym | FJdvT], Print["renormalization constants left in the vertices: ",
   Union[Cases[uvFJ$, (FR$delta | FR$deltaZ | dVsym)[__], Infinity]]]; Abort[]];

FeynmanGauge = True;
If[DirectoryQ["SM_CKM_NLO_UFO"], DeleteDirectory["SM_CKM_NLO_UFO", DeleteContents -> True]];
WriteUFO[LSM, UVCounterterms -> uvFJ$, R2Vertices -> R2$vertlist, Output -> "SM_CKM_NLO_UFO"];

(* the CT parameters: out of parameters.py (block FJCT), into CT_parameters.py *)
ufoNU$ = FileNameJoin[{Directory[], "SM_CKM_NLO_UFO"}];
editNU$[file_, f_] := Export[FileNameJoin[{ufoNU$, file}], f[Import[FileNameJoin[{ufoNU$, file}], "Text"]], "Text"];
namesNU$ = parNU$["values"][[All, 1]];
editNU$["parameters.py", Function[txt, Module[{new = StringReplace[txt,
       RegularExpression["\\n(FJ\\w+) = Parameter\\(name = '\\1',[^)]*lhablock = 'FJCT',[^)]*\\)\\n"] -> "\n"]},
     If[StringContainsQ[new, "FJCT"] || StringCount[txt, "lhablock = 'FJCT'"] != Length[namesNU$], Print["parameters.py: FJCT not removed"]; Abort[]];
     new]]];
CopyFile[FileNameJoin[{srcDirNU$, "generated", "SM_CKM_CT_parameters.py"}], FileNameJoin[{ufoNU$, "CT_parameters.py"}], OverwriteTarget -> True];
editNU$["__init__.py", StringReplace[#, "try:\n   import CT_vertices" ->
     "try:\n   import CT_parameters\nexcept ImportError:\n   pass\nelse:\n   all_CTparameters = CT_parameters.all_CTparameters\n\ntry:\n   import CT_vertices"] &];
(* the couplings written with CT parameters are strings, not Laurent dictionaries (MadGraph's convention) *)
editNU$["CT_couplings.py", Function[txt, Module[{new = StringReplace[txt,
       RegularExpression["value = \\{0:'([^']*FJ[^']*)'\\}"] -> "value = '$1'"]},
     If[StringContainsQ[new, RegularExpression["\\{[^}]*FJ"]], Print["CT_couplings.py: CT parameters left in a dictionary"]; Abort[]];
     new]]];
editNU$["CT_vertices.py", StringReplace[#, RegularExpression["(type = 'UV',\\n(?:[^\\n]*\\n){3}\\s*loop_particles = )\\[ \\[ \\[P\\.W__plus__\\] \\] \\]"] ->
     "$1[ [ [] ] ]"] &];
Print["UV vertices with empty loop_particles: ", StringCount[Import[FileNameJoin[{ufoNU$, "CT_vertices.py"}], "Text"], "[ [ [] ] ]"],
  " of ", StringCount[Import[FileNameJoin[{ufoNU$, "CT_vertices.py"}], "Text"], "type = 'UV'"]];
(* MadGraph writes decimals with 7 digits in Fortran: rational coefficients back to ratios (spinor QED note) *)
exactUFO$[file_] := Module[{txt = Import[file, "Text"], new},
   new = StringReplace[txt, RegularExpression["(?<![\\w.])(\\d+\\.\\d{7,})"] :>
       Module[{r = Rationalize[ToExpression["$1"], 10^-15]},
         If[Head[r] === Rational, "(" <> ToString[Numerator[r]] <> "./" <> ToString[Denominator[r]] <> ".)", "$1"]]];
   Export[file, new, "Text"];
   Length[StringCases[txt, RegularExpression["(?<![\\w.])\\d+\\.\\d{7,}"]]]];
Print["decimal coefficients made exact: ", exactUFO$[FileNameJoin[{ufoNU$, #}]] & /@ {"couplings.py", "CT_couplings.py"}];
Print["written: ", FileNames["SM_CKM_NLO_UFO"], " (CT parameters: ", Length[namesNU$], ")"];
