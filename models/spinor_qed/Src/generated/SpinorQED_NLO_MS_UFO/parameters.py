# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 13 Oct 2026 09:20:53



from object_library import all_parameters, Parameter


from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot

# This is a default parameter object representing 0.
ZERO = Parameter(name = 'ZERO',
                 nature = 'internal',
                 type = 'real',
                 value = '0.0',
                 texname = '0')

# This is a default parameter object representing the renormalization scale (MU_R).
MU_R = Parameter(name = 'MU_R',
                 nature = 'external',
                 type = 'real',
                 value = 91.188,
                 texname = '\\text{\\mu_r}',
                 lhablock = 'LOOP',
                 lhacode = [1])

# User-defined parameters.
ee = Parameter(name = 'ee',
               nature = 'external',
               type = 'real',
               value = 1.,
               texname = '\\text{e}',
               lhablock = 'QEDBLOCK',
               lhacode = [ 1 ])

Me = Parameter(name = 'Me',
               nature = 'external',
               type = 'real',
               value = 1.,
               texname = '\\text{Me}',
               lhablock = 'MASS',
               lhacode = [ 11 ])

MMU = Parameter(name = 'MMU',
                nature = 'external',
                type = 'real',
                value = 1.7,
                texname = '\\text{MMU}',
                lhablock = 'MASS',
                lhacode = [ 13 ])

