# User model backup (2026-10-09)

Copied before the old FeynCalc / FeynArts / Package-X / FeynRules / LieART /
FormCalc / MadGraph installs were moved to the Trash for the environment rebuild.
Every folder was checked with `diff -rq` against its source before the source
was removed.

| Folder | Source |
|---|---|
| `feynrules_Library_Models/` | `~/Library/Wolfram/Applications/FeynRules/Models/` (whole folder: user models AbelianHiggs, B-L-SM, EW, EW copy, EW+CS, EW+pions, Phi3, QCD, QED, SMnew, SU(2)xU(1), Yukawa, pseudoYukawa, scalarQED, scalarQED+selfInteraction, plus the stock FirstExample, SM, template.fr) |
| `feynrules_DocumentsApplications_Models/` | `~/Documents/Applications/FeynRules/Models/` (older copy; only QED differs from the Library copy) |
| `feynarts_Library_Models/` | User-added model folders in `~/Library/Wolfram/Applications/FeynCalc/FeynArts/Models/` (FeynRules exports): AbelianHiggs, EW, EW+CS, EW+pions, Phi3, Phi4, QCD, QED, SM, SMQCDrenoL, Yukawa, minimal_Zp, pseudoYukawa, scalarQED, scalarQED+SI |
| `feynarts_DocumentsApplications_Models/` | User-added model folders in `~/Documents/Applications/FeynCalc/FeynArts/Models/` |
| `nloct_Downloads_feynrules-current/` | NLOCT outputs from `~/Downloads/feynrules-current/` (SMQCDreno.nlo, SM_NLO UFO, Models/SM/SMQCDrenoL) |
| `nloct_Dropbox_feynrules-current/` | NLOCT outputs from `~/Dropbox/GraduateResearch/feynrules-current/` |
| `feynrules-samples_Downloads/` | `~/Downloads/feynrules-samples/` (model1 WEff, model2) |
| `Dropbox_Examples_FeynRules/` | `~/Dropbox/Examples/FeynRules/` (FeynCalc example models; many files were 0 bytes at copy time) |

To use a model with the new FeynRules install, load it from here, for example
`LoadModel[".../feynrules_Library_Models/AbelianHiggs/AbelianHiggs.fr"]`. You do
not need to copy models back into the FeynRules folder.
