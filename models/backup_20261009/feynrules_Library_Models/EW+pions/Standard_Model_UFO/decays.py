# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.1.0 for Mac OS X ARM (64-bit) (July 16, 2024)
# Date: Sat 10 May 2025 13:58:04


from object_library import all_decays, Decay
import particles as P


Decay_b = Decay(name = 'Decay_b',
                particle = P.b,
                partial_widths = {(P.H,P.d):'((MB**2 - MH**2)*((3*I1a1*I2a3*MB**2*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(yd(2))*yd(2))/2. - (3*I1a1*I2a3*MH**2*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(yd(2))*yd(2))/2.))/(96.*cmath.pi*abs(MB)**3)',
                                  (P.H,P.s):'((MB**2 - MH**2)*((3*I1a2*I2a3*MB**2*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(yd(2))*yd(2))/2. - (3*I1a2*I2a3*MH**2*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(yd(2))*yd(2))/2.))/(96.*cmath.pi*abs(MB)**3)',
                                  (P.W__minus__,P.t):'(((3*ee**2*MB**2)/(2.*sw**2) + (3*ee**2*MT**2)/(2.*sw**2) + (3*ee**2*MB**4)/(2.*MW**2*sw**2) - (3*ee**2*MB**2*MT**2)/(MW**2*sw**2) + (3*ee**2*MT**4)/(2.*MW**2*sw**2) - (3*ee**2*MW**2)/sw**2)*cmath.sqrt(MB**4 - 2*MB**2*MT**2 + MT**4 - 2*MB**2*MW**2 - 2*MT**2*MW**2 + MW**4))/(96.*cmath.pi*abs(MB)**3)'})

Decay_H = Decay(name = 'Decay_H',
                particle = P.H,
                partial_widths = {(P.b,P.b__tilde__):'(cmath.sqrt(-4*MB**2*MH**2 + MH**4)*(-3*MB**2*yb**2 + (3*MH**2*yb**2)/2. - 3*I1a3*I2a3*MB**2*yb*complexconjugate(yd(2)) - 3*MB**2*yb*complexconjugate(I1a3)*complexconjugate(I2a3)*yd(2) - 3*I1a3*I2a3*MB**2*complexconjugate(I1a3)*complexconjugate(I2a3)*complexconjugate(yd(2))*yd(2) + (3*I1a3*I2a3*MH**2*complexconjugate(I1a3)*complexconjugate(I2a3)*complexconjugate(yd(2))*yd(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.b,P.d__tilde__):'((-MB**2 + MH**2)*((-3*I1a3*I2a1*MB**2*complexconjugate(I1a3)*complexconjugate(I2a1)*complexconjugate(yd(2))*yd(2))/2. + (3*I1a3*I2a1*MH**2*complexconjugate(I1a3)*complexconjugate(I2a1)*complexconjugate(yd(2))*yd(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.b,P.s__tilde__):'((-MB**2 + MH**2)*((-3*I1a3*I2a2*MB**2*complexconjugate(I1a3)*complexconjugate(I2a2)*complexconjugate(yd(2))*yd(2))/2. + (3*I1a3*I2a2*MH**2*complexconjugate(I1a3)*complexconjugate(I2a2)*complexconjugate(yd(2))*yd(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.c,P.c__tilde__):'(3*I1a2*I2a2*MH**4*complexconjugate(I1a2)*complexconjugate(I2a2)*complexconjugate(yu(2))*yu(2))/(32.*cmath.pi*abs(MH)**3)',
                                  (P.c,P.t__tilde__):'((MH**2 - MT**2)*((3*I1a2*I2a3*MH**2*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(yu(2))*yu(2))/2. - (3*I1a2*I2a3*MT**2*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(yu(2))*yu(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.c,P.u__tilde__):'(3*I1a2*I2a1*MH**4*complexconjugate(I1a2)*complexconjugate(I2a1)*complexconjugate(yu(2))*yu(2))/(32.*cmath.pi*abs(MH)**3)',
                                  (P.d,P.b__tilde__):'((-MB**2 + MH**2)*((-3*I1a1*I2a3*MB**2*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(yd(2))*yd(2))/2. + (3*I1a1*I2a3*MH**2*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(yd(2))*yd(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.d,P.d__tilde__):'(3*I1a1*I2a1*MH**4*complexconjugate(I1a1)*complexconjugate(I2a1)*complexconjugate(yd(2))*yd(2))/(32.*cmath.pi*abs(MH)**3)',
                                  (P.d,P.s__tilde__):'(3*I1a1*I2a2*MH**4*complexconjugate(I1a1)*complexconjugate(I2a2)*complexconjugate(yd(2))*yd(2))/(32.*cmath.pi*abs(MH)**3)',
                                  (P.e__minus__,P.e__plus__):'(I1a1*I2a1*MH**4*complexconjugate(I1a1)*complexconjugate(I2a1)*complexconjugate(yl(2))*yl(2))/(32.*cmath.pi*abs(MH)**3)',
                                  (P.e__minus__,P.mu__plus__):'(I1a1*I2a2*MH**4*complexconjugate(I1a1)*complexconjugate(I2a2)*complexconjugate(yl(2))*yl(2))/(32.*cmath.pi*abs(MH)**3)',
                                  (P.e__minus__,P.ta__plus__):'((MH**2 - MTA**2)*((I1a1*I2a3*MH**2*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(yl(2))*yl(2))/2. - (I1a1*I2a3*MTA**2*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(yl(2))*yl(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.mu__minus__,P.e__plus__):'(I1a2*I2a1*MH**4*complexconjugate(I1a2)*complexconjugate(I2a1)*complexconjugate(yl(2))*yl(2))/(32.*cmath.pi*abs(MH)**3)',
                                  (P.mu__minus__,P.mu__plus__):'(I1a2*I2a2*MH**4*complexconjugate(I1a2)*complexconjugate(I2a2)*complexconjugate(yl(2))*yl(2))/(32.*cmath.pi*abs(MH)**3)',
                                  (P.mu__minus__,P.ta__plus__):'((MH**2 - MTA**2)*((I1a2*I2a3*MH**2*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(yl(2))*yl(2))/2. - (I1a2*I2a3*MTA**2*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(yl(2))*yl(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.s,P.b__tilde__):'((-MB**2 + MH**2)*((-3*I1a2*I2a3*MB**2*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(yd(2))*yd(2))/2. + (3*I1a2*I2a3*MH**2*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(yd(2))*yd(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.s,P.d__tilde__):'(3*I1a2*I2a1*MH**4*complexconjugate(I1a2)*complexconjugate(I2a1)*complexconjugate(yd(2))*yd(2))/(32.*cmath.pi*abs(MH)**3)',
                                  (P.s,P.s__tilde__):'(3*I1a2*I2a2*MH**4*complexconjugate(I1a2)*complexconjugate(I2a2)*complexconjugate(yd(2))*yd(2))/(32.*cmath.pi*abs(MH)**3)',
                                  (P.t,P.c__tilde__):'((MH**2 - MT**2)*((3*I1a3*I2a2*MH**2*complexconjugate(I1a3)*complexconjugate(I2a2)*complexconjugate(yu(2))*yu(2))/2. - (3*I1a3*I2a2*MT**2*complexconjugate(I1a3)*complexconjugate(I2a2)*complexconjugate(yu(2))*yu(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.t,P.t__tilde__):'(cmath.sqrt(MH**4 - 4*MH**2*MT**2)*((3*MH**2*yt**2)/2. - 3*MT**2*yt**2 - 3*I1a3*I2a3*MT**2*yt*complexconjugate(yu(2)) - 3*MT**2*yt*complexconjugate(I1a3)*complexconjugate(I2a3)*yu(2) + (3*I1a3*I2a3*MH**2*complexconjugate(I1a3)*complexconjugate(I2a3)*complexconjugate(yu(2))*yu(2))/2. - 3*I1a3*I2a3*MT**2*complexconjugate(I1a3)*complexconjugate(I2a3)*complexconjugate(yu(2))*yu(2)))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.t,P.u__tilde__):'((MH**2 - MT**2)*((3*I1a3*I2a1*MH**2*complexconjugate(I1a3)*complexconjugate(I2a1)*complexconjugate(yu(2))*yu(2))/2. - (3*I1a3*I2a1*MT**2*complexconjugate(I1a3)*complexconjugate(I2a1)*complexconjugate(yu(2))*yu(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.ta__minus__,P.e__plus__):'((MH**2 - MTA**2)*((I1a3*I2a1*MH**2*complexconjugate(I1a3)*complexconjugate(I2a1)*complexconjugate(yl(2))*yl(2))/2. - (I1a3*I2a1*MTA**2*complexconjugate(I1a3)*complexconjugate(I2a1)*complexconjugate(yl(2))*yl(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.ta__minus__,P.mu__plus__):'((MH**2 - MTA**2)*((I1a3*I2a2*MH**2*complexconjugate(I1a3)*complexconjugate(I2a2)*complexconjugate(yl(2))*yl(2))/2. - (I1a3*I2a2*MTA**2*complexconjugate(I1a3)*complexconjugate(I2a2)*complexconjugate(yl(2))*yl(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.ta__minus__,P.ta__plus__):'(cmath.sqrt(MH**4 - 4*MH**2*MTA**2)*((MH**2*ytau**2)/2. - MTA**2*ytau**2 - I1a3*I2a3*MTA**2*ytau*complexconjugate(yl(2)) - MTA**2*ytau*complexconjugate(I1a3)*complexconjugate(I2a3)*yl(2) + (I1a3*I2a3*MH**2*complexconjugate(I1a3)*complexconjugate(I2a3)*complexconjugate(yl(2))*yl(2))/2. - I1a3*I2a3*MTA**2*complexconjugate(I1a3)*complexconjugate(I2a3)*complexconjugate(yl(2))*yl(2)))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.u,P.c__tilde__):'(3*I1a1*I2a2*MH**4*complexconjugate(I1a1)*complexconjugate(I2a2)*complexconjugate(yu(2))*yu(2))/(32.*cmath.pi*abs(MH)**3)',
                                  (P.u,P.t__tilde__):'((MH**2 - MT**2)*((3*I1a1*I2a3*MH**2*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(yu(2))*yu(2))/2. - (3*I1a1*I2a3*MT**2*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(yu(2))*yu(2))/2.))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.u,P.u__tilde__):'(3*I1a1*I2a1*MH**4*complexconjugate(I1a1)*complexconjugate(I2a1)*complexconjugate(yu(2))*yu(2))/(32.*cmath.pi*abs(MH)**3)',
                                  (P.W__minus__,P.W__plus__):'(((3*ee**4*vev**2)/(4.*sw**4) + (ee**4*MH**4*vev**2)/(16.*MW**4*sw**4) - (ee**4*MH**2*vev**2)/(4.*MW**2*sw**4))*cmath.sqrt(MH**4 - 4*MH**2*MW**2))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.Z,P.Z):'(((9*ee**4*vev**2)/2. + (3*ee**4*MH**4*vev**2)/(8.*MZ**4) - (3*ee**4*MH**2*vev**2)/(2.*MZ**2) + (3*cw**4*ee**4*vev**2)/(4.*sw**4) + (cw**4*ee**4*MH**4*vev**2)/(16.*MZ**4*sw**4) - (cw**4*ee**4*MH**2*vev**2)/(4.*MZ**2*sw**4) + (3*cw**2*ee**4*vev**2)/sw**2 + (cw**2*ee**4*MH**4*vev**2)/(4.*MZ**4*sw**2) - (cw**2*ee**4*MH**2*vev**2)/(MZ**2*sw**2) + (3*ee**4*sw**2*vev**2)/cw**2 + (ee**4*MH**4*sw**2*vev**2)/(4.*cw**2*MZ**4) - (ee**4*MH**2*sw**2*vev**2)/(cw**2*MZ**2) + (3*ee**4*sw**4*vev**2)/(4.*cw**4) + (ee**4*MH**4*sw**4*vev**2)/(16.*cw**4*MZ**4) - (ee**4*MH**2*sw**4*vev**2)/(4.*cw**4*MZ**2))*cmath.sqrt(MH**4 - 4*MH**2*MZ**2))/(32.*cmath.pi*abs(MH)**3)'})

Decay_t = Decay(name = 'Decay_t',
                particle = P.t,
                partial_widths = {(P.H,P.c):'((-MH**2 + MT**2)*((-3*I1a2*I2a3*MH**2*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(yu(2))*yu(2))/2. + (3*I1a2*I2a3*MT**2*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(yu(2))*yu(2))/2.))/(96.*cmath.pi*abs(MT)**3)',
                                  (P.H,P.u):'((-MH**2 + MT**2)*((-3*I1a1*I2a3*MH**2*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(yu(2))*yu(2))/2. + (3*I1a1*I2a3*MT**2*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(yu(2))*yu(2))/2.))/(96.*cmath.pi*abs(MT)**3)',
                                  (P.W__plus__,P.b):'(((3*ee**2*I1a3*I2a3*MB**2*CKM(2)*complexconjugate(I1a3)*complexconjugate(I2a3)*complexconjugate(CKM(2)))/(2.*sw**2) + (3*ee**2*I1a3*I2a3*MT**2*CKM(2)*complexconjugate(I1a3)*complexconjugate(I2a3)*complexconjugate(CKM(2)))/(2.*sw**2) + (3*ee**2*I1a3*I2a3*MB**4*CKM(2)*complexconjugate(I1a3)*complexconjugate(I2a3)*complexconjugate(CKM(2)))/(2.*MW**2*sw**2) - (3*ee**2*I1a3*I2a3*MB**2*MT**2*CKM(2)*complexconjugate(I1a3)*complexconjugate(I2a3)*complexconjugate(CKM(2)))/(MW**2*sw**2) + (3*ee**2*I1a3*I2a3*MT**4*CKM(2)*complexconjugate(I1a3)*complexconjugate(I2a3)*complexconjugate(CKM(2)))/(2.*MW**2*sw**2) - (3*ee**2*I1a3*I2a3*MW**2*CKM(2)*complexconjugate(I1a3)*complexconjugate(I2a3)*complexconjugate(CKM(2)))/sw**2)*cmath.sqrt(MB**4 - 2*MB**2*MT**2 + MT**4 - 2*MB**2*MW**2 - 2*MT**2*MW**2 + MW**4))/(96.*cmath.pi*abs(MT)**3)',
                                  (P.W__plus__,P.d):'((MT**2 - MW**2)*((3*ee**2*I1a1*I2a3*MT**2*CKM(2)*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(CKM(2)))/(2.*sw**2) + (3*ee**2*I1a1*I2a3*MT**4*CKM(2)*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(CKM(2)))/(2.*MW**2*sw**2) - (3*ee**2*I1a1*I2a3*MW**2*CKM(2)*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(CKM(2)))/sw**2))/(96.*cmath.pi*abs(MT)**3)',
                                  (P.W__plus__,P.s):'((MT**2 - MW**2)*((3*ee**2*I1a2*I2a3*MT**2*CKM(2)*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(CKM(2)))/(2.*sw**2) + (3*ee**2*I1a2*I2a3*MT**4*CKM(2)*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(CKM(2)))/(2.*MW**2*sw**2) - (3*ee**2*I1a2*I2a3*MW**2*CKM(2)*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(CKM(2)))/sw**2))/(96.*cmath.pi*abs(MT)**3)'})

Decay_ta__minus__ = Decay(name = 'Decay_ta__minus__',
                          particle = P.ta__minus__,
                          partial_widths = {(P.H,P.e__minus__):'((-MH**2 + MTA**2)*(-0.5*(I1a1*I2a3*MH**2*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(yl(2))*yl(2)) + (I1a1*I2a3*MTA**2*complexconjugate(I1a1)*complexconjugate(I2a3)*complexconjugate(yl(2))*yl(2))/2.))/(32.*cmath.pi*abs(MTA)**3)',
                                            (P.H,P.mu__minus__):'((-MH**2 + MTA**2)*(-0.5*(I1a2*I2a3*MH**2*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(yl(2))*yl(2)) + (I1a2*I2a3*MTA**2*complexconjugate(I1a2)*complexconjugate(I2a3)*complexconjugate(yl(2))*yl(2))/2.))/(32.*cmath.pi*abs(MTA)**3)',
                                            (P.W__minus__,P.vt):'((MTA**2 - MW**2)*((ee**2*MTA**2)/(2.*sw**2) + (ee**2*MTA**4)/(2.*MW**2*sw**2) - (ee**2*MW**2)/sw**2))/(32.*cmath.pi*abs(MTA)**3)'})

Decay_W__plus__ = Decay(name = 'Decay_W__plus__',
                        particle = P.W__plus__,
                        partial_widths = {(P.c,P.s__tilde__):'(ee**2*MW**4)/(16.*cmath.pi*sw**2*abs(MW)**3)',
                                          (P.t,P.b__tilde__):'(((-3*ee**2*MB**2)/(2.*sw**2) - (3*ee**2*MT**2)/(2.*sw**2) - (3*ee**2*MB**4)/(2.*MW**2*sw**2) + (3*ee**2*MB**2*MT**2)/(MW**2*sw**2) - (3*ee**2*MT**4)/(2.*MW**2*sw**2) + (3*ee**2*MW**2)/sw**2)*cmath.sqrt(MB**4 - 2*MB**2*MT**2 + MT**4 - 2*MB**2*MW**2 - 2*MT**2*MW**2 + MW**4))/(48.*cmath.pi*abs(MW)**3)',
                                          (P.u,P.d__tilde__):'(ee**2*MW**4)/(16.*cmath.pi*sw**2*abs(MW)**3)',
                                          (P.ve,P.e__plus__):'(ee**2*MW**4)/(48.*cmath.pi*sw**2*abs(MW)**3)',
                                          (P.vm,P.mu__plus__):'(ee**2*MW**4)/(48.*cmath.pi*sw**2*abs(MW)**3)',
                                          (P.vt,P.ta__plus__):'((-MTA**2 + MW**2)*(-0.5*(ee**2*MTA**2)/sw**2 - (ee**2*MTA**4)/(2.*MW**2*sw**2) + (ee**2*MW**2)/sw**2))/(48.*cmath.pi*abs(MW)**3)'})

Decay_Z = Decay(name = 'Decay_Z',
                particle = P.Z,
                partial_widths = {(P.b,P.b__tilde__):'((-7*ee**2*MB**2 + ee**2*MZ**2 - (3*cw**2*ee**2*MB**2)/(2.*sw**2) + (3*cw**2*ee**2*MZ**2)/(2.*sw**2) - (17*ee**2*MB**2*sw**2)/(6.*cw**2) + (5*ee**2*MZ**2*sw**2)/(6.*cw**2))*cmath.sqrt(-4*MB**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.c,P.c__tilde__):'(MZ**2*(-(ee**2*MZ**2) + (3*cw**2*ee**2*MZ**2)/(2.*sw**2) + (17*ee**2*MZ**2*sw**2)/(6.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.d,P.d__tilde__):'(MZ**2*(ee**2*MZ**2 + (3*cw**2*ee**2*MZ**2)/(2.*sw**2) + (5*ee**2*MZ**2*sw**2)/(6.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.e__minus__,P.e__plus__):'(MZ**2*(-(ee**2*MZ**2) + (cw**2*ee**2*MZ**2)/(2.*sw**2) + (5*ee**2*MZ**2*sw**2)/(2.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.mu__minus__,P.mu__plus__):'(MZ**2*(-(ee**2*MZ**2) + (cw**2*ee**2*MZ**2)/(2.*sw**2) + (5*ee**2*MZ**2*sw**2)/(2.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.s,P.s__tilde__):'(MZ**2*(ee**2*MZ**2 + (3*cw**2*ee**2*MZ**2)/(2.*sw**2) + (5*ee**2*MZ**2*sw**2)/(6.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.t,P.t__tilde__):'((-11*ee**2*MT**2 - ee**2*MZ**2 - (3*cw**2*ee**2*MT**2)/(2.*sw**2) + (3*cw**2*ee**2*MZ**2)/(2.*sw**2) + (7*ee**2*MT**2*sw**2)/(6.*cw**2) + (17*ee**2*MZ**2*sw**2)/(6.*cw**2))*cmath.sqrt(-4*MT**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.ta__minus__,P.ta__plus__):'((-5*ee**2*MTA**2 - ee**2*MZ**2 - (cw**2*ee**2*MTA**2)/(2.*sw**2) + (cw**2*ee**2*MZ**2)/(2.*sw**2) + (7*ee**2*MTA**2*sw**2)/(2.*cw**2) + (5*ee**2*MZ**2*sw**2)/(2.*cw**2))*cmath.sqrt(-4*MTA**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.u,P.u__tilde__):'(MZ**2*(-(ee**2*MZ**2) + (3*cw**2*ee**2*MZ**2)/(2.*sw**2) + (17*ee**2*MZ**2*sw**2)/(6.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.ve,P.ve__tilde__):'(MZ**2*(ee**2*MZ**2 + (cw**2*ee**2*MZ**2)/(2.*sw**2) + (ee**2*MZ**2*sw**2)/(2.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.vm,P.vm__tilde__):'(MZ**2*(ee**2*MZ**2 + (cw**2*ee**2*MZ**2)/(2.*sw**2) + (ee**2*MZ**2*sw**2)/(2.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.vt,P.vt__tilde__):'(MZ**2*(ee**2*MZ**2 + (cw**2*ee**2*MZ**2)/(2.*sw**2) + (ee**2*MZ**2*sw**2)/(2.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.W__minus__,P.W__plus__):'(((-12*cw**2*ee**2*MW**2)/sw**2 - (17*cw**2*ee**2*MZ**2)/sw**2 + (4*cw**2*ee**2*MZ**4)/(MW**2*sw**2) + (cw**2*ee**2*MZ**6)/(4.*MW**4*sw**2))*cmath.sqrt(-4*MW**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)'})

