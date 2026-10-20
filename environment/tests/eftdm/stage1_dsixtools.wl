(* Stage 1 of the EFT and dark-matter tools (environment.pdf): the DsixTools 2.1 side of test_eft_stage1.py.
   Reads out/stage1_in.json (written by `test_eft_stage1.py prepare`) and writes out/dsix_{B,A,C,D}.json and the WCxf
   export out/dsix_A_wcxf.json.
   Pitfalls (environment.pdf): DsixTools uses t (= log10 mu), t0, tf, g, gp, gs, m2, Mu, Md, Me, ... as its own symbols,
   so no variable of this file may have these names; the options file sets the loop orders without rebuilding the RGEs
   (SetSMEFTLoopOrder does, but only if the order changes); an input array that does not contain its redundant
   entries is "fixed" by averaging (so CHl1[1,2] alone becomes CHl1[1,2]/2); zero couplings give 0^-2 in the RGEs. *)
SetDirectory[DirectoryName[$InputFileName]];
Needs["DsixTools`"];
TurnOffMessages;
inData = Import["out/stage1_in.json", "RawJSON"];
num[x_] := N[x];                                             (* Mathematica 14 imports 1e-06 as 1/1000000 *)
cplx[{re_, im_}] := num[re] + I num[im];
reIm[z_] := <|"Re" -> Re[z], "Im" -> Im[z]|>;
smRules[c_] := Join[
  {g -> num[c["sm", "g"]], gp -> num[c["sm", "gp"]], gs -> num[c["sm", "gs"]], \[Lambda] -> num[c["sm", "Lambda"]], m2 -> num[c["sm", "m2"]]},
  Flatten@Table[{Gu[i, j] -> If[i == j, num[c["y", "Gu"][[i]]], 0.], Gd[i, j] -> If[i == j, num[c["y", "Gd"][[i]]], 0.],
    Ge[i, j] -> If[i == j, num[c["y", "Ge"][[i]]], 0.]}, {i, 3}, {j, 3}]];
wcRules[c_] := (If[#[[2]] === {}, ToExpression[#[[1]]], ToExpression[#[[1]]] @@ #[[2]]] -> cplx[#[[3 ;; 4]]]) & /@ c["wc"];
SetRGEsMethod[1];
SetSMEFTLoopOrder[1]; SetLEFTLoopOrder[1];
Unprotect[UseRGEsSM]; UseRGEsSM = 0;                         (* the SM input is given at the UV scale *)
tight = {PrecisionGoal -> 10, AccuracyGoal -> 20};          (* with the full SM, AccuracyGoal 30 stops NDSolve at the first step *)
runSMEFT[c_] := (NewInput[Join[smRules[c], wcRules[c]], HIGHSCALE -> num[c["scale_in"]]]; SMEFTRunRGEs);
at[x_, scale_] := D6run[x] /. \[Mu] -> scale;

(* B: pure-QCD toy, with tight and with default NDSolve tolerances *)
cB = inData["B"];
resB = Association @@ Table[
   SetOptions[NDSolve, If[tag == "tight", {PrecisionGoal -> 12, AccuracyGoal -> 30}, {PrecisionGoal -> Automatic, AccuracyGoal -> Automatic}]];
   runSMEFT[cB];
   tag -> <|"gs" -> Re@at[gs, EWSCALE], "ledq" -> Re@at[Cledq[1, 1, 1, 1], EWSCALE], "lequ1" -> Re@at[Clequ1[1, 1, 1, 1], EWSCALE],
     "lequ3" -> Re@at[Clequ3[1, 1, 1, 1], EWSCALE], "lq1" -> Re@at[Clq1[1, 1, 1, 1], EWSCALE], "phiG" -> Re@at[CHG, EWSCALE]|>,
   {tag, {"tight", "default"}}];
Export["out/dsix_B.json", resB, "RawJSON"];
Print["B done"];

(* A: full SM, all redundant entries given; WCxf export at the EW scale *)
SetOptions[NDSolve, tight];
cA = inData["A"];
runSMEFT[cA];
inDiff = Max[Abs[(#[[1]] /. InputValues) - #[[2]]] & /@ wcRules[cA]];
SMEFTrunnerExport["JSON", "out/dsix_A_wcxf"];
smA = <|"gs" -> Re@at[gs, EWSCALE], "g" -> Re@at[g, EWSCALE], "gp" -> Re@at[gp, EWSCALE], "Lambda" -> Re@at[\[Lambda], EWSCALE],
   "m2" -> Re@at[m2, EWSCALE]|>;
(* DsixTools' own WCxf reader on the same coefficients (out/caseA_wcxf.json) *)
Export["out/Options_A.dat", "Block SCALES\n1 1000.0\n2 91.1876\nBlock OPTIONS\n1 1\n2 0\n3 1\n4 1\n5 0\n", "Text"];
SetDirectory["out"];
ReadInputFiles["Options_A.dat", "caseA_wcxf.json", FileNameJoin[{$UserBaseDirectory, "Applications", "DsixTools", "IO", "SMInput.dat"}], "SMEFT"];
ResetDirectory[];
imp = <|"CHl1_12" -> Re[CHl1[1, 2] /. InputValues], "Clq1_1123" -> Re[Clq1[1, 1, 2, 3] /. InputValues],
   "Cdd_1112" -> Re[Cdd[1, 1, 1, 2] /. InputValues]|>;
Export["out/dsix_A.json", <|"sm" -> smA, "input_maxdiff" -> inDiff, "import" -> imp|>, "RawJSON"];
Print["A done; largest difference between the given and the stored input entries: ", inDiff];

(* C: analytic tree-level matching, coefficients of Clq1, Clq3, Cledq at LoopParameter -> 0 *)
SetMatchingLoopOrder[0];
coef[x_] := (D[MatchEW[x], #] /. LoopParameter -> 0) & /@ {Clq1[1, 1, 1, 1], Clq3[1, 1, 1, 1], Cledq[1, 1, 1, 1]};
Export["out/dsix_C.json", <|"LedVLL" -> coef[LedVLL[1, 1, 1, 1]], "LnudVLL" -> coef[L\[Nu]dVLL[1, 1, 1, 1]],
   "LedSRL" -> coef[LedSRL[1, 1, 1, 1]]|>, "RawJSON"];
Print["C done"];

(* D: LEFT running M_Z -> 5 GeV at one loop, without QED (eQED = 1e-8) and with QED (DsixTools' default eQED) *)
cD = inData["D"];
wcD = {LedSRL[1, 1, 1, 1] -> 1.*^-6, LeuTRR[1, 1, 1, 1] -> 1.*^-6, LeuSRR[1, 1, 1, 1] -> 1.*^-6, LedVLL[1, 1, 1, 1] -> 1.*^-6};
resD = Association @@ Table[
   NewInput[Join[wcD, {gQCD -> Sqrt[4 Pi num[cD["alpha_s"]]]}, If[tag == "noqed", {eQED -> 1.*^-8}, {}]],
     EWSCALE -> num[cD["scale_in"]], LOWSCALE -> num[cD["scale_out"]]];
   InitializeLEFTrunnerInput; LEFTRunRGEs;
   tag -> <|"gQCD_in" -> (gQCD /. InputValues), "eQED_in" -> (eQED /. InputValues), "gQCD_out" -> Re@at[gQCD, LOWSCALE],
     "SedRL_1111" -> Re@at[LedSRL[1, 1, 1, 1], LOWSCALE], "TeuRR_1111" -> Re@at[LeuTRR[1, 1, 1, 1], LOWSCALE],
     "SeuRR_1111" -> Re@at[LeuSRR[1, 1, 1, 1], LOWSCALE], "VedLL_1111" -> Re@at[LedVLL[1, 1, 1, 1], LOWSCALE]|>,
   {tag, {"noqed", "qed"}}];
Export["out/dsix_D.json", resD, "RawJSON"];
Print["D done"];
