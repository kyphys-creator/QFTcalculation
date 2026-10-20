# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 20 Oct 2026 12:21:32


from object_library import all_decays, Decay
import particles as P


Decay_h = Decay(name = 'Decay_h',
                particle = P.h,
                partial_widths = {(P.g,P.g):'(aS**2*kHgg**2*MH**6)/(72.*cmath.pi**3*vev**2*abs(MH)**3)'})

