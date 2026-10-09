(* LoopTools MathLink test.  Exact: B0(2;1,1) = 2 - Pi/2 ; C0(0,0,0;1,1,1) = -1/2 *)
Install[FileNameJoin[{$HomeDirectory, "hep", "bin", "LoopTools"}]];
Print["LoopTools B0(2;1,1) = ", ToString[B0[2., 1., 1.], InputForm], "   exact ", N[2 - Pi/2, 16]];
Print["LoopTools C0(0,0,0;1,1,1) = ", C0[0., 0., 0., 1., 1., 1.], "   exact -0.5"];
