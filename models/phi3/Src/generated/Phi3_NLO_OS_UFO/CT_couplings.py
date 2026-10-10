# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Sat 10 Oct 2026 06:16:34


from object_library import all_couplings, Coupling

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot



UVGC_2_1 = Coupling(name = 'UVGC_2_1',
                    value = {0:'( (complex(0,1)*gphi**2)/(32.*cmath.pi**2*m**2) - (complex(0,1)*gphi**2)/(48.*cmath.pi*m**2*cmath.sqrt(3)) if m else 0 )'},
                    order = {'PHI':2})

UVGC_3_2 = Coupling(name = 'UVGC_3_2',
                    value = {0:'( (-3*complex(0,1)*gphi**3)/(64.*cmath.pi**2*m**2) + (complex(0,1)*gphi**3)/(32.*cmath.pi*m**2*cmath.sqrt(3)) if m else 0 )'},
                    order = {'PHI':3})

UVGC_4_3 = Coupling(name = 'UVGC_4_3',
                    value = {-1:'-0.03125*(complex(0,1)*gphi**2)/cmath.pi**2',0:'( (-3*complex(0,1)*gphi**2)/(32.*cmath.pi**2) + (5*complex(0,1)*gphi**2)/(96.*cmath.pi*cmath.sqrt(3)) + (complex(0,1)*gphi**2*reglog(m/MU_R))/(16.*cmath.pi**2) if m else 0 )'},
                    order = {'PHI':2})

