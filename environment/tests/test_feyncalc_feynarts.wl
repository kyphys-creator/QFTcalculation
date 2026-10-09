(* FeynCalc + patched FeynArts: one-loop photon self-energy (fermion loops), reduced to PaVe functions *)
$FeynCalcStartupMessages = False;
$LoadAddOns = {"FeynArtsLoader"};
Get["FeynCalc`"];
tops = CreateTopologies[1, 1 -> 1, ExcludeTopologies -> {Tadpoles}];
diags = InsertFields[tops, {V[1]} -> {V[1]}, InsertionLevel -> {Particles}, Model -> "SMQCD",
   ExcludeParticles -> {S[_], V[2 | 3], U[_]}];
amp = FCFAConvert[CreateFeynAmp[diags], IncomingMomenta -> {p}, OutgoingMomenta -> {p},
   LoopMomenta -> {l}, LorentzIndexNames -> {mu, nu}, UndoChiralSplittings -> True,
   ChangeDimension -> D, List -> False, SMP -> True, DropSumOver -> True];
res = TID[amp /. FCI[SUNFDelta[__]] -> 1, l, ToPaVe -> True];
Print["PaVe functions in the result: ", Union[Cases[res, (A0 | B0)[__], Infinity]] // Length,
  " distinct; transverse structure p^2 g - p p present: ", ! FreeQ[res, Pair[Momentum[p, D], Momentum[p, D]]]];
