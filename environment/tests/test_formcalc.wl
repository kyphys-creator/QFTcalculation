(* unpatched FeynArts 3.12 + FormCalc 9.10: tree-level e+ e- -> mu+ mu- (no scalars) *)
Get["FeynArts`"];
Get["FormCalc`"];
testOutDir$ = FileNameJoin[{DirectoryName[$InputFileName], "out", "formcalc"}];
Quiet[CreateDirectory[testOutDir$, CreateIntermediateDirectories -> True]]; SetDirectory[testOutDir$];
tops = CreateTopologies[0, 2 -> 2];
ins = InsertFields[tops, {-F[2, {1}], F[2, {1}]} -> {-F[2, {2}], F[2, {2}]}, Model -> "SM", ExcludeParticles -> {S[_]}];
amp = CalcFeynAmp[CreateFeynAmp[ins]];
Print["FeynArts ", $FeynArts, " + FormCalc: ", Length[amp], " amplitude(s), ", Length[Abbr[]], " abbreviations"];
