(* Stage 2 of the EFT and dark-matter tools (environment.pdf): the DirectDM 1.2.1 (Mathematica) side of test_directdm.py.
   Writes out/ddm_mma.json. The nucleon inputs are those of DirectDM/inputs.m (sigma_s = 41.3 MeV, m_G = 848 MeV). *)
SetDirectory[DirectoryName[$InputFileName]];
Needs["DirectDM`"];
cc = 1.*^-6; mx = 100.; nr[b_] := CoeffsList[b] /. {MX -> mx, qsq -> 1.*^-6};
SetDMType["R"]; ResetBasis["3Flavor"];
Do[SetCoeff["3Flavor", Q6[3, f], cc], {f, {"u", "d", "s"}}]; SetCoeff["3Flavor", Q6[5], -3 cc];
ComputeCoeffs["3Flavor", "NR"];
r3 = <|"p" -> nr["NR_p"][[1]], "n" -> nr["NR_n"][[1]]|>;
SetDMType["R"]; ResetBasis["5Flavor"];
Do[SetCoeff["5Flavor", Q6[3, f], cc], {f, {"u", "d", "s", "c", "b"}}]; SetCoeff["5Flavor", Q6[5], -cc];
ComputeCoeffs["5Flavor", "NR", Running -> False]; r5n = nr["NR_p"][[1]];
ComputeCoeffs["5Flavor", "NR"]; r5r = nr["NR_p"][[1]];
SetDMType["D"]; ResetBasis["3Flavor"];
SetCoeff["3Flavor", Q6[1, "u"], 1.*^-6]; SetCoeff["3Flavor", Q6[1, "d"], 0.4*^-6]; SetCoeff["3Flavor", Q6[1, "s"], -0.2*^-6];
ComputeCoeffs["3Flavor", "NR"]; dv = nr["NR_p"][[1]];
ResetBasis["3Flavor"];
SetCoeff["3Flavor", Q6[4, "u"], 1.*^-6]; SetCoeff["3Flavor", Q6[4, "d"], 0.4*^-6]; SetCoeff["3Flavor", Q6[4, "s"], -0.2*^-6];
ComputeCoeffs["3Flavor", "NR"]; da = nr["NR_p"][[4]];
Export["out/ddm_mma.json", <|"R3" -> r3, "R5_norun" -> r5n, "R5_run" -> r5r, "Dvec_p1" -> dv, "Dax_p4" -> da|>, "RawJSON"];
