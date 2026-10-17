(* ::Package:: *)

(* ::Title:: *)
(*Step (9d): the counterterm parameters of the note's general NLO UFO (massless light fermions)*)


(* ::Text:: *)
(*The UV counterterm vertices of the UFO are those of the counterterm Lagrangian (nlo_ctrules.wl), linear in the*)
(*renormalization constants, plus the tadpole vertices times dvT.  The constants become CT parameters of the UFO (their*)
(*poles 1/FR$Eps and finite parts, MadGraph's CTParameter), and the vertices are written in terms of them:*)
(*  - the MS-bar parameter constants of the FJ scheme and dvT = T/MH^2 (nlo_fjdelta.wl), with*)
(*    FR$delta[{aEWM1}] = -2 aEWM1 FJdlne (FJdlne = de/e) and FR$delta[{aS}] = 2 aS FJdlngs;*)
(*  - the on-shell field constants of the external legs (nlo_dz.wl, NLOCT), the Goldstone ones 0.*)
(*The counterterms are for massless light fermions u, d, s, c, b, e, mu, ta (as MadGraph's default restriction): the light*)
(*masses are set to 0 and NLOCT's conditions If[...] are resolved with the heavy masses of the note's point (the physical*)
(*ordering MH < 2 MW, MT > MW + MB, ...; the UFO is then valid near these values).  The constants are split into the*)
(*electroweak part (coupling order QED 2; dvT QED 1) and the QCD part (QCD 2), each its own parameter.*)
(*Writes Src/generated/SM_FJct.fr (the parameters for FeynRules, to be loaded with SM.fr) and Src/generated/SM_FJctpar.m*)
(*(the substitution rules and the values) for nlo_ufo.wl.  Batch: wolframscript -file nlo_ctparams.wl  (plain kernel)*)


srcDirCP$ = DirectoryName[$InputFileName];
dzCP$ = Get[FileNameJoin[{srcDirCP$, "generated", "SM_dZ.m"}]]["dZ"] /. IPL[_] -> 1;
fdCP$ = Get[FileNameJoin[{srcDirCP$, "generated", "SM_FJdelta.m"}]];
lightCP$ = {MU, MC, MD, MS, MB, Me, MMU, MTA};
light0CP$ = Thread[lightCP$ -> 0];
heavyCP$ = {MZ -> 911876/10000, MW -> 80369/1000, MH -> 1252/10, MT -> 17257/100};
swcwCP$ = {cw -> MW/MZ, sw -> Sqrt[1 - MW^2/MZ^2]};
(* NLOCT's conditions at light masses 0 and the heavy masses of the point; the If factors first, then the light masses *)
truthCP$[c_] := Module[{v = c /. light0CP$ /. heavyCP$}, If[v === True || v === False, v, Print["undecided condition ", c]; Abort[]]];
resolveCP$[x_] := Module[{y = x //. If[c_, a_, b_] :> If[truthCP$[c], a, b]},
   y = y /. light0CP$;
   If[!FreeQ[y, Indeterminate | ComplexInfinity | DirectedInfinity], Print["singular at light masses 0"]; Abort[]];
   y];
(* dvT has m^4 ln m^2 of the light fermions: those terms (each with a positive power of a light mass) are dropped first *)
light0LogCP$[x_] := Module[{y = Expand[x], t},
   t = If[Head[y] === Plus, List @@ y, {y}];
   t = GroupBy[t, FreeQ[Cases[#, Log[a_] :> (a /. light0CP$), Infinity], 0] &];
   If[!AllTrue[Lookup[t, False, {}], ((# /. Log[_] -> 1) /. light0CP$) === 0 &],
    Print["a light-mass log without a power of the mass"]; Abort[]];
   Total[Lookup[t, True, {}]] /. light0CP$];
(* the poles and finite parts; the QCD part is the part proportional to gs^2 (aS = gs^2/(4 Pi)) *)
laurCP$[x_] := Module[{y = Expand[x]}, {Coefficient[y, FR$Eps, -1], Coefficient[y, FR$Eps, 0]}];
splitCP$[x_] := Module[{y = Expand[x /. aS -> gs^2/(4 Pi)]}, {Coefficient[y, gs, 0], gs^2 Coefficient[y, gs, 2]}];
simpCP$[x_] := Simplify[x, Assumptions -> MZ > MW > 0 && MH > 0 && MT > 0 && FR$MU > 0 && ee > 0 && gs > 0];

(* the field constants *)
nameZ$[FR$deltaZ[{f1_, f2_}, {{}}]] := "FJdZ" <> ToString[f1] <> ToString[f2];
nameZ$[FR$deltaZ[{f_, f_}, {{}}, ch_]] := "FJdZ" <> ToString[f] <> ToString[ch];
t0CP$ = AbsoluteTime[];
zCP$ = Table[Module[{k = r[[1]], v = r[[2]], ew, qcd},
     If[v === 0, k -> {}, (* the Goldstone constants *)
      {ew, qcd} = simpCP$ /@ splitCP$[resolveCP$[v]];
      k -> Select[{{nameZ$[k], {QED, 2}, ew}, {nameZ$[k] <> "qcd", {QCD, 2}, qcd}}, #[[3]] =!= 0 &]]],
    {r, dzCP$}];
Print["field constants resolved: ", Length[zCP$], ";  ", Round[AbsoluteTime[] - t0CP$], " s"];
(* the parameter constants and dvT (light masses 0) *)
dCP$ = Association[(#[[1]] -> (#[[2]] /. light0CP$)) & /@ fdCP$["delta"]];
pCP$ = {
   {"FJdlne", {QED, 2}, dCP$[FR$delta[{aEWM1}, {}]]/(-2 aEWM1) /. aEWM1 -> 4 Pi/ee^2},
   {"FJdlngs", {QCD, 2}, dCP$[FR$delta[{aS}, {}]]/(2 aS) /. aS -> gs^2/(4 Pi)},
   {"FJdMZ", {QED, 2}, dCP$[FR$delta[{MZ}, {}]]},
   {"FJdMW", {QED, 2}, dCP$[FR$delta[{MW}, {}]]},
   {"FJdMH", {QED, 2}, dCP$[FR$delta[{MH}, {}]]},
   {"FJdMT", {QED, 2}, splitCP$[dCP$[FR$delta[{MT}, {}]]][[1]]},
   {"FJdMTqcd", {QCD, 2}, splitCP$[dCP$[FR$delta[{MT}, {}]]][[2]]},
   {"FJdvT", {QED, 1}, light0LogCP$[fdCP$["dvT"]]}};
pCP$ = {#[[1]], #[[2]], simpCP$[#[[3]] /. swcwCP$]} & /@ pCP$;
Print["check: the light-mass constants vanish: ", Union[Simplify[Lookup[dCP$, FR$delta[{#}, {}] & /@ lightCP$]]]];
(* the substitution rules for the counterterm vertices *)
symCP$[n_] := ToExpression[n];
rulesCP$ = Join[
   (#[[1]] -> Total[symCP$ /@ #[[2, All, 1]]]) & /@ zCP$,
   {FR$delta[{aEWM1}, {}] -> -2 aEWM1 symCP$["FJdlne"], FR$delta[{aS}, {}] -> 2 aS symCP$["FJdlngs"],
    FR$delta[{MZ}, {}] -> symCP$["FJdMZ"], FR$delta[{MW}, {}] -> symCP$["FJdMW"], FR$delta[{MH}, {}] -> symCP$["FJdMH"],
    FR$delta[{MT}, {}] -> symCP$["FJdMT"] + symCP$["FJdMTqcd"]},
   (FR$delta[{#}, {}] -> 0) & /@ lightCP$];
allCP$ = Join[Flatten[Values[Association[zCP$]], 1], pCP$];
valuesCP$ = (#[[1]] -> laurCP$[#[[3]]]) & /@ allCP$;
Print["CT parameters: ", Length[allCP$], " (", Count[allCP$[[All, 2, 1]], QCD], " QCD);  leaf counts of the values: ",
  MinMax[LeafCount /@ valuesCP$[[All, 2]]]];
(* the numbers at the note's point (FR$Eps = 1/3, FR$MU = 100), for the record *)
ptCP$ = Join[heavyCP$, {ee -> Sqrt[4 Pi/128], gs -> Sqrt[4 Pi 118/1000], FR$MU -> 100}];
Scan[Print["   ", #[[1]], ":  pole ", N[#[[2, 1]] /. ptCP$, 10], ",  finite ", N[#[[2, 2]] /. ptCP$, 10]] &, valuesCP$];

(* FeynRules: the parameters as external parameters with their coupling orders (block FJCT; removed from the UFO's*)
(* parameters and written as CT parameters by nlo_ufo.wl) *)
frCP$ = "(* generated by nlo_ctparams.wl: the counterterm parameters of the FJ scheme as FeynRules parameters *)\n\nM$Parameters = {\n" <>
   StringRiffle[MapIndexed[Function[{p, i},
      "  " <> p[[1]] <> " == {\n    ParameterType -> External,\n    BlockName -> FJCT,\n    OrderBlock -> " <> ToString[i[[1]]] <>
       ",\n    Value -> " <> ToString[i[[1]]] <> "/1000,\n    InteractionOrder -> {" <> ToString[p[[2, 1]]] <> ", " <>
       ToString[p[[2, 2]]] <> "},\n    Description -> \"FJ counterterm parameter\"}"], allCP$], ",\n"] <> "\n};\n";
Export[FileNameJoin[{srcDirCP$, "generated", "SM_FJct.fr"}], frCP$, "Text"];
Put[<|"rules" -> rulesCP$, "values" -> valuesCP$, "orders" -> ((#[[1]] -> #[[2]]) & /@ allCP$)|>,
  FileNameJoin[{srcDirCP$, "generated", "SM_FJctpar.m"}]];
Print["written: generated/SM_FJct.fr, generated/SM_FJctpar.m;  ", Round[AbsoluteTime[] - t0CP$], " s"];
