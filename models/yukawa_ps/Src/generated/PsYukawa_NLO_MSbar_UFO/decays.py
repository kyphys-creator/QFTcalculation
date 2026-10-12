# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Mon 12 Oct 2026 13:29:08


from object_library import all_decays, Decay
import particles as P


Decay_phi = Decay(name = 'Decay_phi',
                  particle = P.phi,
                  partial_widths = {(P.psi,P.psi__tilde__):'(mphi**2*yps**2*cmath.sqrt(mphi**4 - 4*mphi**2*Mpsi**2))/(8.*cmath.pi*abs(mphi)**3)'})

