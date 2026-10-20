(* SM + real scalar dark matter in Feynman gauge -> NLO UFO with NLOCT's R2 vertices and its on-shell h Z a and h a a counterterm
   vertices, into ../out/model_nlo, for MadDM's loop-induced lines S S -> a a, a Z.  Three kernels:
     wolframscript -file make_nlo_ufo.wl ren   FeynRules + NLOCT: OnShellRenormalization (FlavorMixing -> False; the
                                               tadpole constant set to 0), FeynArts model SM_SingletDM_ren
     wolframscript -file make_nlo_ufo.wl ct    FeynArts + NLOCT (no FeynRules): WriteCT (on-shell; about 3 min, the .nlo is
                                               90 MB) -> SM_SingletDM_R2.m, SM_SingletDM_UV.m
     wolframscript -file make_nlo_ufo.wl ufo   FeynRules: WriteUFO with these vertices -> SM_SingletDM_NLO_UFO
   S S -> V a has no tree, so the only counterterm vertices that enter at one loop are those of h V a behind the tree S S h:
   h Z a, i (g_hZZ/2) dZ_ZA with NLOCT's on-shell dZ_ZA = -(alpha/pi)(c_W/s_W) B0(0, M_W, M_W) (the photon-Z mixing on the
   external photon, which MadLoop does not attach to external legs; without it the Z gamma line depends on mu_R), and h a a,
   whose pole parts (split by loop content) add up to 0.  The other UV vertices are left out (the tadpole and the finite parts
   of the coupling constants are not on-shell here: OnShellRenormalization's FR$deltat is set to 0).
   The Higgs portal is SingletDM.fr's with Phi^dagger Phi written out in Feynman gauge (Phi = (-i GP, (vev + H + i G0)/sqrt2)
   of FeynRules' SM.fr), so that S S G+ G- and S S G0 G0 are in the model:
     L = 1/2 (d S)^2 - 1/2 (MS0^2 - lamHS vev^2/2) S^2 - (lamHS/2) S^2 (G+ G- + ((vev + H)^2 + G0^2)/2).
   The CKM matrix is set to the identity (no W-quark loop enters S S -> a a, a Z at one loop; with it NLOCT runs much
   longer, as in the CKM note).  FeynRules 2.3.49 with the local patches of environment/files (FeynRules.m, Loop.m).
   Each package is loaded at the top level before the expressions that use its symbols are read. *)
here = DirectoryName[$InputFileName];
outDir = FileNameJoin[{ParentDirectory[here], "out", "model_nlo"}];
step = If[Length[$ScriptCommandLine] >= 2, $ScriptCommandLine[[2]], ""];
If[!MemberQ[{"ren", "ct", "ufo"}, step], Print["usage: wolframscript -file make_nlo_ufo.wl ren|ct|ufo"]; Exit[1]];
t0 = AbsoluteTime[];
Quiet[CreateDirectory[outDir, CreateIntermediateDirectories -> True]];
If[step === "ct",
  Get["FeynArts`"]; Get[FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules", "NLOCT.m"}]],
  $FeynRulesPath = FileNameJoin[{$UserBaseDirectory, "Applications", "FeynRules"}];
  SetDirectory[$FeynRulesPath]; Get["FeynRules`"]];
If[step =!= "ct",
  LoadModel["Models/SM/SM.fr", FileNameJoin[{here, "SingletDM.fr"}]];
  FeynmanGauge = True];
SetDirectory[outDir];

If[step =!= "ct",
  LDMfg = 1/2 del[sdm, mu] del[sdm, mu] - 1/2 (MS0^2 - lamHS vev^2/2) sdm^2 -
    lamHS/2 sdm^2 (GP GPbar + ((vev + H)^2 + G0^2)/2);
  lagNLO = (LSM + LDMfg) /. {Conjugate[CKM[a_, b_]] :> IndexDelta[a, b], CKM[a_, b_] :> IndexDelta[a, b]};
  Print["CKM left in the Lagrangian: ", !FreeQ[lagNLO, CKM]]];

If[step === "ren",
  (* the portal written out against -(lamHS/2) S^2 Phi^dagger Phi of the doublet, and its vertices *)
  Print["Feynman rules of the written-out portal minus those of -(lamHS/2) S^2 Phibar Phi: ",
    FeynmanRules[LDMfg - (1/2 del[sdm, mu] del[sdm, mu] - 1/2 (MS0^2 - lamHS vev^2/2) sdm^2 -
        lamHS/2 sdm^2 ExpandIndices[Phibar[ii] Phi[ii], FlavorExpand -> SU2D]), ScreenOutput -> False]];
  Print["sdm vertices: ", InputForm[FeynmanRules[LDMfg, ScreenOutput -> False]]];
  lagRen = OnShellRenormalization[lagNLO, FlavorMixing -> False];
  (* the one-point vertex of the tadpole constant has no generic coupling in FeynArts' Lorentz.gen (SM note) *)
  lagRen = lagRen /. FR$deltat[_] -> 0;
  Print["renormalized: ", Round[AbsoluteTime[] - t0], " s"];
  If[DirectoryQ["SM_SingletDM_ren"], DeleteDirectory["SM_SingletDM_ren", DeleteContents -> True]];
  WriteFeynArtsOutput[lagRen, Output -> "SM_SingletDM_ren", GenericFile -> False, FlavorExpand -> True];
  Print["written: ", FileNames["*", "SM_SingletDM_ren"], ";  ", Round[AbsoluteTime[] - t0], " s"]];

If[step === "ct",
  WriteCT[FileNameJoin[{outDir, "SM_SingletDM_ren", "SM_SingletDM_ren"}], "Lorentz", Output -> "SM_SingletDM_CT"];
  Get["SM_SingletDM_CT.nlo"];
  r2 = DeleteCases[R2$vertlist, Last[{}]];
  uv = Select[UV$vertlist, MemberQ[{Sort[{A, H, Z}], Sort[{A, A, H}]}, Sort[#[[1, All, 1]]]] &];
  Put[r2, "SM_SingletDM_R2.m"];
  Put[uv, "SM_SingletDM_UV.m"];
  Print["written: SM_SingletDM_R2.m (", Length[r2], " R2 vertices), SM_SingletDM_UV.m (", Length[uv], " of ", Length[UV$vertlist],
    " UV vertices);  ", Round[AbsoluteTime[] - t0], " s"];
  Print["R2 vertices with the singlet: ", Select[r2[[All, 1, All, 1]], !FreeQ[#, sdm] &]];
  Print["h a a UV vertex, summed over the loop content: ", Simplify[uv[[Position[Sort[#[[1, All, 1]]] & /@ uv, Sort[{A, A, H}]][[1, 1]], 2]] /. IPL[_] -> 1]];
  (* i (g_hZZ/2) dZ_ZA, g_hZZ = ee^2 vev/(2 cw^2 sw^2), against dZ_ZA = -(alpha/pi)(cw/sw) B0(0, MW, MW) *)
  Print["h Z a UV vertex / (i g_hZZ/2) + (alpha/pi)(cw/sw)(1/eps + Log[mu^2/MW^2]) (MW > 0): ", Simplify[
    ((uv[[Position[Sort[#[[1, All, 1]]] & /@ uv, Sort[{A, H, Z}]][[1, 1]], 2]] /. {IPL[_] -> 1, ME[__] -> 1}) / (I ee^2 vev/(4 cw^2 sw^2)) +
      ee^2/(4 Pi^2) cw/sw (1/FR$Eps + Log[FR$MU^2/MW^2])) //. {vev -> 2 MW sw/ee, MW -> MZ cw, cw -> Sqrt[1 - sw^2]},
    MZ > 0 && FR$MU > 0 && 0 < sw < 1]]];

If[step === "ufo",
  R2$vertlist = Get["SM_SingletDM_R2.m"];
  UV$vertlist = Get["SM_SingletDM_UV.m"];
  FR$InteractionOrderPerturbativeExpansion = {{QCD, 1}, {QED, 1}};
  If[DirectoryQ["SM_SingletDM_NLO_UFO"], DeleteDirectory["SM_SingletDM_NLO_UFO", DeleteContents -> True]];
  WriteUFO[lagNLO, R2Vertices -> R2$vertlist, UVCounterterms -> UV$vertlist, Output -> "SM_SingletDM_NLO_UFO"];
  (* MadGraph writes decimals with 7 digits in Fortran: rational coefficients back to ratios (SM note, nlo_ufo.wl) *)
  exactUFO[file_] := Module[{txt = Import[file, "Text"]},
    Export[file, StringReplace[txt, RegularExpression["(?<![\\w.])(\\d+\\.\\d{7,})"] :>
        Module[{r = Rationalize[ToExpression["$1"], 10^-15]},
          If[Head[r] === Rational, "(" <> ToString[Numerator[r]] <> "./" <> ToString[Denominator[r]] <> ".)", "$1"]]], "Text"];
    Length[StringCases[txt, RegularExpression["(?<![\\w.])\\d+\\.\\d{7,}"]]]];
  Print["decimal coefficients made exact (couplings.py, CT_couplings.py): ",
    exactUFO[FileNameJoin[{outDir, "SM_SingletDM_NLO_UFO", #}]] & /@ {"couplings.py", "CT_couplings.py"}];
  Print["written: SM_SingletDM_NLO_UFO;  ", Round[AbsoluteTime[] - t0], " s"]];
Print["messages: ", Length[$MessageList]];
