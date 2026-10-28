# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 27 Oct 2026 19:37:01


from object_library import all_decays, Decay
import particles as P


Decay_h = Decay(name = 'Decay_h',
                particle = P.h,
                partial_widths = {(P.zp,P.zp):'((12*ee**4*vev**2 - (4*ee**4*MH**2*vev**2)/MA**2 + (ee**4*MH**4*vev**2)/MA**4)*cmath.sqrt(-4*MA**2*MH**2 + MH**4))/(32.*cmath.pi*abs(MH)**3)'})

