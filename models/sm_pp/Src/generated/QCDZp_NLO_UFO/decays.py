# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 20 Oct 2026 14:26:05


from object_library import all_decays, Decay
import particles as P


Decay_Zp = Decay(name = 'Decay_Zp',
                 particle = P.Zp,
                 partial_widths = {(P.d,P.d__tilde__):'(MZp**2*((-2*ee**2*gZp**2*MZp**2)/cw**2 + (3*ee**2*gZp**2*MZp**2)/(2.*cw**2*sw**2) + (4*ee**2*gZp**2*MZp**2*sw**2)/(3.*cw**2)))/(48.*cmath.pi*abs(MZp)**3)',
                                   (P.s,P.s__tilde__):'(MZp**2*((-2*ee**2*gZp**2*MZp**2)/cw**2 + (3*ee**2*gZp**2*MZp**2)/(2.*cw**2*sw**2) + (4*ee**2*gZp**2*MZp**2*sw**2)/(3.*cw**2)))/(48.*cmath.pi*abs(MZp)**3)',
                                   (P.e__minus__,P.e__plus__):'(MZp**2*((-2*ee**2*gZp**2*MZp**2)/cw**2 + (ee**2*gZp**2*MZp**2)/(2.*cw**2*sw**2) + (4*ee**2*gZp**2*MZp**2*sw**2)/cw**2))/(48.*cmath.pi*abs(MZp)**3)',
                                   (P.c,P.c__tilde__):'(MZp**2*((-4*ee**2*gZp**2*MZp**2)/cw**2 + (3*ee**2*gZp**2*MZp**2)/(2.*cw**2*sw**2) + (16*ee**2*gZp**2*MZp**2*sw**2)/(3.*cw**2)))/(48.*cmath.pi*abs(MZp)**3)',
                                   (P.u,P.u__tilde__):'(MZp**2*((-4*ee**2*gZp**2*MZp**2)/cw**2 + (3*ee**2*gZp**2*MZp**2)/(2.*cw**2*sw**2) + (16*ee**2*gZp**2*MZp**2*sw**2)/(3.*cw**2)))/(48.*cmath.pi*abs(MZp)**3)'})

