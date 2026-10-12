# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Mon 12 Oct 2026 13:29:08


from object_library import all_couplings, Coupling

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot



R2GC_3_1 = Coupling(name = 'R2GC_3_1',
                    value = '-0.041666666666666664*(complex(0,1)*yps**2)/cmath.pi**2',
                    order = {'YUK':2})

R2GC_4_2 = Coupling(name = 'R2GC_4_2',
                    value = '(5*complex(0,1)*yps**4)/(4.*cmath.pi**2)',
                    order = {'YUK':4})

R2GC_5_3 = Coupling(name = 'R2GC_5_3',
                    value = '(complex(0,1)*Mpsi**2*yps**2)/(4.*cmath.pi**2)',
                    order = {'YUK':2})

R2GC_8_4 = Coupling(name = 'R2GC_8_4',
                    value = 'yps**3/(32.*cmath.pi**2)',
                    order = {'YUK':3})

UVGC_3_1 = Coupling(name = 'UVGC_3_1',
                    value = {-1:'( 0 if mphi else ( (complex(0,1)*yps**2)/(8.*cmath.pi**2) if Mpsi==0 else 0 ) ) - (complex(0,1)*yps**2)/(8.*cmath.pi**2)'},
                    order = {'YUK':2})

UVGC_4_2 = Coupling(name = 'UVGC_4_2',
                    value = {-1:'(-3*complex(0,1)*lamphi**2)/(32.*cmath.pi**2)'},
                    order = {'YUK':4})

UVGC_4_3 = Coupling(name = 'UVGC_4_3',
                    value = {-1:'( 0 if mphi else ( -0.25*(complex(0,1)*lamphi*yps**2)/cmath.pi**2 if Mpsi==0 else 0 ) ) + (3*complex(0,1)*yps**4)/(2.*cmath.pi**2)'},
                    order = {'YUK':4})

UVGC_5_4 = Coupling(name = 'UVGC_5_4',
                    value = {-1:'-0.03125*(complex(0,1)*lamphi*mphi**2)/cmath.pi**2'},
                    order = {'YUK':2})

UVGC_5_5 = Coupling(name = 'UVGC_5_5',
                    value = {-1:'( 0 if mphi else ( -0.125*(complex(0,1)*mphi**2*yps**2)/cmath.pi**2 if Mpsi==0 else 0 ) ) + (complex(0,1)*Mpsi**2*yps**2)/(4.*cmath.pi**2)'},
                    order = {'YUK':2})

UVGC_6_6 = Coupling(name = 'UVGC_6_6',
                    value = {-1:'( 0 if mphi else ( -0.03125*(complex(0,1)*yps**2)/cmath.pi**2 if Mpsi==0 else 0 ) ) + (complex(0,1)*yps**2)/(32.*cmath.pi**2)'},
                    order = {'YUK':2})

UVGC_7_7 = Coupling(name = 'UVGC_7_7',
                    value = {-1:'( 0 if mphi else ( -0.03125*(complex(0,1)*Mpsi*yps**2)/cmath.pi**2 if Mpsi==0 else 0 ) ) + (complex(0,1)*Mpsi*yps**2)/(16.*cmath.pi**2)'},
                    order = {'YUK':2})

UVGC_8_8 = Coupling(name = 'UVGC_8_8',
                    value = {-1:'( 0 if mphi else ( yps**3/(16.*cmath.pi**2) if Mpsi==0 else 0 ) )'},
                    order = {'YUK':3})

UVGC_8_9 = Coupling(name = 'UVGC_8_9',
                    value = {-1:'( 0 if mphi else ( yps**3/(32.*cmath.pi**2) if Mpsi==0 else 0 ) ) + yps**3/(16.*cmath.pi**2)'},
                    order = {'YUK':3})

