(* ::Package:: *)

(* ::Title:: *)
(*Step (9): the NLO partonic cross sections f^(1)_ij(rho) of heavy-quark pair production*)


(* ::Text:: *)
(*Research note models/qcd, step (9), Eqs. (hqf), (hqsum).  m = mu = 1, g = 1 (alpha_s = 1/(4 pi)), SU(3), n_l = 5, alpha_s^(n_l), pole mass,*)
(*MS-bar parton distributions; bare coupling g0^2 = g^2 e^(eps gamma_E) (4 pi)^-eps (the MS-bar factor in the coupling); initial-state*)
(*averages in D dimensions (2 N for a quark, 2 (1 - eps)(N^2 - 1) for a gluon).  K sigma^(1) = K (sigma_V + sigma_R + sigma_C), K = (4 pi)^2:*)
(*  sigma_V = 1/(2 s n) int dPhi_2 2 Re W,  W = Z^(1) (x) B(D) + W^(4)_fin  (Eq. (mlconv); Z (x) B(D) from Eq. (irpole) with the*)
(*            D-dimensional colour correlations of hq_born.wl, integrated with (1 - c^2)^-eps; W^(4)_fin from MadLoop, hq_virtual.py);*)
(*  sigma_R = 1/(2 s n) e^(3 eps gamma) (4 pi)^(-3 eps) x (hq_reduce.wl reduction) x (AMFlow masters, hq_amflow.wl);*)
(*  sigma_C = (alpha_s/(2 pi eps)) sum int dz P(z) sigma0(z s; eps)  (z/(1-z)_+ = [z/(1-z)]_+ - delta(1-z) in P_gg).*)
(*The poles cancel in the sum; f^(1) = K sigma^(1) at eps^0 (f = K sigma for alpha_s = 1/(4 pi), m = 1).  -> results/hq_f1_<chan>.csv*)
(*Usage: wolframscript -file hq_assemble.wl chan [s1,s2,...]   (default: the 20 values of results/hq_sgrid.txt)*)


s9 = FileNameJoin[{Which[StringQ[$InputFileName] && $InputFileName =!= "", DirectoryName[$InputFileName], $Notebooks, NotebookDirectory[], True, Directory[]], "work", "hq"}];
resDirHS$ = FileNameJoin[{ParentDirectory[ParentDirectory[s9]], "results"}];
chans = If[Length[$ScriptCommandLine] >= 2, StringSplit[$ScriptCommandLine[[2]], ","], {"qq", "qg"}];
CA = 3; CF = 4/3; TF = 1/2; nl = 5; KK = (4 Pi)^2; wp = 32;
dd = 4 - 2 ep;
vb = Get[FileNameJoin[{s9, "born.m"}]] /. {CA -> 3, CF -> 4/3};
ml = Import[FileNameJoin[{s9, "ml_scan.json"}], "RawJSON"];
pref = Exp[ep EulerGamma] (4 Pi)^(-ep);
beta[s_] := Sqrt[1 - 4/s];
phi2[sv_] := 2 Pi^((dd - 1)/2)/Gamma[(dd - 1)/2] (beta[sv] Sqrt[sv]/2)^(dd - 3)/(4 (2 Pi)^(dd - 2) Sqrt[sv]);
nAng = 2^(1 - 2 ep) Gamma[1 - ep]^2/Gamma[2 - 2 ep];
avgD = <|"A" -> 4 CA^2, "B" -> 4 (1 - ep)^2 (CA^2 - 1)^2, "qq" -> 4 CA^2, "qg" -> 4 (1 - ep) CA (CA^2 - 1), "gg" -> 4 (1 - ep)^2 (CA^2 - 1)^2|>;
ser[x_, n_] := Normal[Series[x, {ep, 0, n}]];
tOf[sv_, c_] := 1 - sv/2 (1 - beta[sv] c);
(* angular average <f> = int (1-c^2)^-eps f dc / nAng, as a series to eps^n; f is a function of (t, eps) *)
angAvg[f_, sv_?NumericQ, n_] := Module[{g = ser[(1 - cc^2)^(-ep) (f /. {t -> tOf[sv, cc], s -> sv}), n], co},
   co = Table[Module[{b = beta[sv], lv}, lv = Log[(1 + b)/(1 - b)];
       NIntegrate[(Coefficient[g, ep, k] /. cc -> Tanh[vv/2]/b) (1 - Tanh[vv/2]^2)/(2 b), {vv, -lv, 0, lv}, WorkingPrecision -> wp, PrecisionGoal -> 18, MaxRecursion -> 40]],
     {k, Exponent[g, ep, Min], n}];
   ser[(co . Table[ep^k, {k, Exponent[g, ep, Min], n}])/nAng, n]];
bornD[key_] := vb[key]["born"] /. D -> dd;
(* sigma0(s; eps) for process key ("A" = q qbar, "B" = g g), series to eps^n *)
sig0[key_, sv_?NumericQ, n_] := ser[1/(2 sv) pref^2 phi2[sv]/avgD[key] angAvg[bornD[key], sv, n], n];
f0[key_, sv_] := N[KK sig0[key, sv, 0] /. ep -> 0, 20];
(* ---- virtual ---- *)
casim = <|"A" -> {CF, CF}, "B" -> {CA, CA}|>;
gam = <|"A" -> {-3 CF, -3 CF}, "B" -> {-(11/3 CA - 4/3 TF nl), -(11/3 CA - 4/3 TF nl)}|>;
reG[key_, sv_] := Module[{cc = vb[key]["cc"] /. {D -> dd, s -> sv}, u = 2 - sv - t, b = beta[sv], bb},
   bb = ArcCosh[(sv - 2)/2];
   4 cc[{1, 2}] (-Log[sv]) - 4 cc[{3, 4}] (sv - 2)/(sv b) bb + 4 (cc[{1, 3}] (-Log[1 - t]) + cc[{2, 4}] (-Log[1 - t]) + cc[{1, 4}] (-Log[1 - u]) + cc[{2, 3}] (-Log[1 - u])) +
    (Total[gam[key]] - 4 CF) (bornD[key] /. s -> sv)];
(* 2 Re [Z (x) B(D)] = (2/K) [ -(C1+C2)/eps^2 B(D) + Re G/(2 eps) ] *)
virtZ[key_, sv_] := (2/KK) (-Total[casim[key]]/ep^2 (bornD[key] /. s -> sv) + reG[key, sv]/(2 ep));
skey[x_] := StringReplace[ToString[x, InputForm], "/" -> "o"];
mlKey[key_, sv_] := key <> "_" <> skey[sv];
sigV[key_, sv_] := Module[{d = ml[mlKey[key, sv]], v4, vz, chk},
   v4 = Total[d["w"] (2 #["KW4fin"]/KK & /@ d["rows"])];   (* w: weights of 1/2 int dc *)
   (* check the MadLoop poles against Z (x) B(4) at each angle *)
   chk = Max[Table[Module[{r = d["rows"][[i]], tt},
        tt = r["t"];
        Max[Abs[(-Total[casim[key]] bornD[key] /. ep -> 0 /. {t -> tt, s -> sv})/r["KW4m2"] - 1], Abs[(reG[key, sv]/2 /. ep -> 0 /. t -> tt)/r["KW4m1"] - 1]]],
       {i, Length[d["rows"]]}]];
   Print["   (", key, ") s = ", sv, ": MadLoop poles vs Z(x)B(4), max rel. dev. ", ScientificForm[chk, 3]];
   vz = angAvg[virtZ[key, sv], sv, 0];
   ser[1/(2 sv) pref^2 phi2[sv]/avgD[key] (vz + v4), 0]];
(* ---- collinear counterterms (MS-bar, mu_F = m): (alpha_s/2 pi)(1/eps) int dz P(z) sigma0(z s), alpha_s/2 pi = 1/(8 pi^2) ---- *)
sig0z[key_, k_, sz_?NumericQ] := If[sz <= 4, 0, Coefficient[sig0[key, sz, 1], ep, k]];
plusInt[h_, key_, sv_, k_] := Module[{rho = 4/sv, g1 = sig0z[key, k, sv]},
   NIntegrate[h[z] (sig0z[key, k, z sv] - g1), {z, rho, 1}, WorkingPrecision -> 24, PrecisionGoal -> 14] - g1 NIntegrate[h[z], {z, 0, rho}, WorkingPrecision -> 24]];
regInt[h_, key_, sv_, k_] := NIntegrate[h[z] sig0z[key, k, z sv], {z, 4/sv, 1}, WorkingPrecision -> 24, PrecisionGoal -> 14];
(* convolution of one leg: returns {coefficient of 1/eps, eps^0} with the O(eps) Born *)
convQQ[key_, sv_] := Table[CF plusInt[Function[z, (1 + z^2)/(1 - z)], key, sv, k], {k, 0, 1}];
convGG[key_, sv_] := Table[2 CA plusInt[Function[z, z/(1 - z)], key, sv, k] + 2 CA regInt[Function[z, (1 - z)/z + z (1 - z)], key, sv, k] +
    ((11 CA - 4 nl TF)/6 - 2 CA) sig0z[key, k, sv], {k, 0, 1}];   (* z/(1-z)_+ = [z/(1-z)]_+ - delta(1-z) *)
convGQ[key_, sv_] := Table[CF regInt[Function[z, (1 + (1 - z)^2)/z], key, sv, k], {k, 0, 1}];   (* quark leg emits the gluon that enters *)
convQG[key_, sv_] := Table[TF regInt[Function[z, z^2 + (1 - z)^2], key, sv, k], {k, 0, 1}];      (* gluon leg gives the (anti)quark *)
sigC[chan_, sv_] := Module[{c = Switch[chan, "qq", 2 convQQ["A", sv], "gg", 2 convGG["B", sv], "qg", convGQ["B", sv] + convQG["A", sv]]},
   1/(8 Pi^2) (c[[1]]/ep + c[[2]])];
(* ---- real ---- *)
sigR[chan_, sv_] := Module[{red, ms, vals, sub},
   red = Get[FileNameJoin[{s9, "red_" <> chan <> ".m"}]] /. {gS -> 1, CA -> 3, CF -> 4/3, mt -> 1};
   ms = Union[Cases[red, _GLI, Infinity]];
   vals = Flatten[Get /@ FileNames["R" <> chan <> "*_s" <> skey[sv] <> ".m", FileNameJoin[{s9, "amflow"}]]];
   (* masters equal by relabeling (amf_unique.wl): use the value of the representative *)
   If[FileExistsQ[FileNameJoin[{s9, "unique_" <> chan <> ".m"}]],
    Module[{u = Get[FileNameJoin[{s9, "unique_" <> chan <> ".m"}]], vrep},
     vrep = Association[vals];
     vals = Flatten[KeyValueMap[Function[{k, list}, Module[{known = Select[Prepend[list, u["rep"][k]], KeyExistsQ[vrep, #] &]},
          If[known === {}, {}, (# -> vrep[First[known]]) & /@ list]]], u["keys"]]]]];
   If[!SubsetQ[vals[[All, 1]], ms], Return[Missing["masters"]]];
   sub = ser[(red /. vals /. {D -> dd, s -> sv}), 0];
   ser[1/(2 sv) pref^3/avgD[chan] sub, 0]];
(* ---- run ---- *)
svals = If[Length[$ScriptCommandLine] >= 3, ToExpression /@ StringSplit[$ScriptCommandLine[[3]], ","],
   ToExpression /@ StringSplit[StringTrim[Import[FileNameJoin[{resDirHS$, "hq_sgrid.txt"}], "Text"]], ","]];
rows = {};
Do[Do[Module[{b = beta[sv], key = Switch[chan, "qq", "A", "gg", "B", "qg", None], v, c, r, tot, f00},
     v = If[key === None, 0, sigV[key, sv]];
     c = sigC[chan, sv];
     r = sigR[chan, sv];
     f00 = If[key === None, 0, f0[key, sv]];
     Print[chan, " s = ", sv, " (beta = ", N[b, 8], "): f0 = ", f00, ";  K sigma_V = ", N[Expand[KK v], 12], ";  K sigma_C = ", N[Expand[KK c], 12]];
     If[MissingQ[r], Print["   real masters missing"],
      totRaw = N[Expand[KK (v + c + r)], 16]; tot = Chop[totRaw, 10^-12];
      Print["   K sigma_R = ", N[Expand[KK r], 12], ";  f1 = K (V + C + R) = ", tot];
      (* the finite part is real; numerical noise of the masters gives an imaginary part ~1e-20, recorded separately *)
      AppendTo[rows, {chan, sv, N[b, 20], f00, Abs[Coefficient[totRaw, ep, -2]], Abs[Coefficient[totRaw, ep, -1]], Re[Coefficient[totRaw, ep, 0]], Abs[Im[Coefficient[totRaw, ep, 0]]]}]]],
   {sv, svals}], {chan, chans}];
(* |x|, or the bound 10^-accuracy for a zero of finite accuracy *)
bndHS$[x_] := ToString[CForm[N[If[x == 0, 10^-Round[Accuracy[x]], Abs[x]], 3]]];
Export[FileNameJoin[{resDirHS$, "hq_f1_" <> StringJoin[chans] <> ".csv"}],
  "chan,s,beta,f0,abs_pole2,abs_pole1,f1,abs_im_f1\n" <> StringJoin[(StringRiffle[{#[[1]], ToString[#[[2]], InputForm], ToString[CForm[N[#[[3]], 17]]], ToString[CForm[N[#[[4]], 17]]],
        bndHS$[#[[5]]], bndHS$[#[[6]]], ToString[CForm[N[#[[7]], 17]]], bndHS$[#[[8]]]}, ","] <> "\n") & /@ rows], "Text"];
