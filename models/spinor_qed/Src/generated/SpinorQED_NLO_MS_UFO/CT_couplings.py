# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 13 Oct 2026 09:20:53


from object_library import all_couplings, Coupling

from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot



R2GC_11_1 = Coupling(name = 'R2GC_11_1',
                     value = '(ee**2*complex(0,1))/(16.*cmath.pi**2)',
                     order = {'QED':2})

R2GC_13_2 = Coupling(name = 'R2GC_13_2',
                     value = '(ee**2*complex(0,1)*MMU)/(8.*cmath.pi**2)',
                     order = {'QED':2})

R2GC_2_3 = Coupling(name = 'R2GC_2_3',
                    value = '(ee**2*complex(0,1))/(24.*cmath.pi**2)',
                    order = {'QED':2})

R2GC_3_4 = Coupling(name = 'R2GC_3_4',
                    value = '(ee**4*complex(0,1))/(12.*cmath.pi**2)',
                    order = {'QED':4})

R2GC_4_5 = Coupling(name = 'R2GC_4_5',
                    value = '-0.25*(ee**2*complex(0,1)*Me**2)/cmath.pi**2',
                    order = {'QED':2})

R2GC_4_6 = Coupling(name = 'R2GC_4_6',
                    value = '-0.25*(ee**2*complex(0,1)*MMU**2)/cmath.pi**2',
                    order = {'QED':2})

R2GC_5_7 = Coupling(name = 'R2GC_5_7',
                    value = '(ee**3*complex(0,1))/(8.*cmath.pi**2)',
                    order = {'QED':3})

R2GC_8_8 = Coupling(name = 'R2GC_8_8',
                    value = '(ee**2*complex(0,1)*Me)/(8.*cmath.pi**2)',
                    order = {'QED':2})

UVGC_10_1 = Coupling(name = 'UVGC_10_1',
                     value = {-1:'( 0 if Me else -(1./24.)*(ee**3*complex(0,1))/cmath.pi**2 )',0:'( -(1./12.)*(ee**3*complex(0,1)*reglog(Me/MU_R))/cmath.pi**2 if Me else 0 )'},
                     order = {'QED':3})

UVGC_10_2 = Coupling(name = 'UVGC_10_2',
                     value = {-1:'( 0 if MMU else -(1./24.)*(ee**3*complex(0,1))/cmath.pi**2 )',0:'( -(1./12.)*(ee**3*complex(0,1)*reglog(MMU/MU_R))/cmath.pi**2 if MMU else 0 )'},
                     order = {'QED':3})

UVGC_10_3 = Coupling(name = 'UVGC_10_3',
                     value = {-1:'( (ee**3*complex(0,1))/(8.*cmath.pi**2) if Me else -0.0625*(ee**3*complex(0,1))/cmath.pi**2 )',0:'( (5*ee**3*complex(0,1))/(16.*cmath.pi**2) - (3*ee**3*complex(0,1)*reglog(Me/MU_R))/(8.*cmath.pi**2) if Me else (ee**3*complex(0,1))/(16.*cmath.pi**2) ) - (ee**3*complex(0,1))/(16.*cmath.pi**2)'},
                     order = {'QED':3})

UVGC_11_4 = Coupling(name = 'UVGC_11_4',
                     value = {-1:'( (ee**2*complex(0,1))/(8.*cmath.pi**2) if MMU else -0.0625*(ee**2*complex(0,1))/cmath.pi**2 ) + (ee**2*complex(0,1))/(16.*cmath.pi**2)',0:'( (5*ee**2*complex(0,1))/(16.*cmath.pi**2) - (3*ee**2*complex(0,1)*reglog(MMU/MU_R))/(8.*cmath.pi**2) if MMU else (ee**2*complex(0,1))/(16.*cmath.pi**2) ) - (ee**2*complex(0,1))/(16.*cmath.pi**2)'},
                     order = {'QED':2})

UVGC_12_5 = Coupling(name = 'UVGC_12_5',
                     value = {-1:'( (ee**3*complex(0,1))/(8.*cmath.pi**2) if MMU else -0.0625*(ee**3*complex(0,1))/cmath.pi**2 )',0:'( (5*ee**3*complex(0,1))/(16.*cmath.pi**2) - (3*ee**3*complex(0,1)*reglog(MMU/MU_R))/(8.*cmath.pi**2) if MMU else (ee**3*complex(0,1))/(16.*cmath.pi**2) ) - (ee**3*complex(0,1))/(16.*cmath.pi**2)'},
                     order = {'QED':3})

UVGC_13_6 = Coupling(name = 'UVGC_13_6',
                     value = {-1:'( (ee**2*complex(0,1)*MMU)/(8.*cmath.pi**2) if MMU else -0.0625*(ee**2*complex(0,1)*MMU)/cmath.pi**2 ) + (ee**2*complex(0,1)*MMU)/(4.*cmath.pi**2)',0:'( (9*ee**2*complex(0,1)*MMU)/(16.*cmath.pi**2) - (3*ee**2*complex(0,1)*MMU*reglog(MMU/MU_R))/(4.*cmath.pi**2) if MMU else (ee**2*complex(0,1)*MMU)/(16.*cmath.pi**2) ) - (ee**2*complex(0,1)*MMU)/(16.*cmath.pi**2)'},
                     order = {'QED':2})

UVGC_5_7 = Coupling(name = 'UVGC_5_7',
                    value = {-1:'(ee**3*complex(0,1))/(16.*cmath.pi**2)'},
                    order = {'QED':3})

UVGC_7_8 = Coupling(name = 'UVGC_7_8',
                    value = {-1:'( (ee**2*complex(0,1))/(8.*cmath.pi**2) if Me else -0.0625*(ee**2*complex(0,1))/cmath.pi**2 ) + (ee**2*complex(0,1))/(16.*cmath.pi**2)',0:'( (5*ee**2*complex(0,1))/(16.*cmath.pi**2) - (3*ee**2*complex(0,1)*reglog(Me/MU_R))/(8.*cmath.pi**2) if Me else (ee**2*complex(0,1))/(16.*cmath.pi**2) ) - (ee**2*complex(0,1))/(16.*cmath.pi**2)'},
                    order = {'QED':2})

UVGC_8_9 = Coupling(name = 'UVGC_8_9',
                    value = {-1:'( (ee**2*complex(0,1)*Me)/(8.*cmath.pi**2) if Me else -0.0625*(ee**2*complex(0,1)*Me)/cmath.pi**2 ) + (ee**2*complex(0,1)*Me)/(4.*cmath.pi**2)',0:'( (9*ee**2*complex(0,1)*Me)/(16.*cmath.pi**2) - (3*ee**2*complex(0,1)*Me*reglog(Me/MU_R))/(4.*cmath.pi**2) if Me else (ee**2*complex(0,1)*Me)/(16.*cmath.pi**2) ) - (ee**2*complex(0,1)*Me)/(16.*cmath.pi**2)'},
                    order = {'QED':2})

UVGC_9_10 = Coupling(name = 'UVGC_9_10',
                     value = {-1:'( 0 if Me else (ee**2*complex(0,1))/(12.*cmath.pi**2) ) - (ee**2*complex(0,1))/(12.*cmath.pi**2)',0:'( (ee**2*complex(0,1)*reglog(Me/MU_R))/(6.*cmath.pi**2) if Me else 0 )'},
                     order = {'QED':2})

UVGC_9_11 = Coupling(name = 'UVGC_9_11',
                     value = {-1:'( 0 if MMU else (ee**2*complex(0,1))/(12.*cmath.pi**2) ) - (ee**2*complex(0,1))/(12.*cmath.pi**2)',0:'( (ee**2*complex(0,1)*reglog(MMU/MU_R))/(6.*cmath.pi**2) if MMU else 0 )'},
                     order = {'QED':2})
