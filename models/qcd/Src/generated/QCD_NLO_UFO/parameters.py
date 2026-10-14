# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Wed 14 Oct 2026 15:49:25



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
               texname = 'e',
               lhablock = 'QEDBLOCK',
               lhacode = [ 1 ])

aS = Parameter(name = 'aS',
               nature = 'external',
               type = 'real',
               value = 0.0795774715459477,
               texname = '\\alpha _s',
               lhablock = 'SMINPUTS',
               lhacode = [ 3 ])

MT = Parameter(name = 'MT',
               nature = 'external',
               type = 'real',
               value = 1.,
               texname = '\\text{MT}',
               lhablock = 'MASS',
               lhacode = [ 6 ])

G = Parameter(name = 'G',
              nature = 'internal',
              type = 'real',
              value = '2*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)',
              texname = 'G')

