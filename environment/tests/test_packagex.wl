(* Package-X (mule-tools source) + PVReduce *)
Get["X`"];
Print["LoopIntegrate B0: ", ToString[LoopRefine[LoopIntegrate[1, k, {k, m}, {k + p, m}]], InputForm]];
Get["X`PVReduce`"];
Print["PVReduce[PVB[0,1,s,m,m]] = ", ToString[PVReduce[PVB[0, 1, s, m, m]], InputForm], "   (expected -PVB[0,0,s,m,m]/2)"];
