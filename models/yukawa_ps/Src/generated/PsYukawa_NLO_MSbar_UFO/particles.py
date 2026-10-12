# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Mon 12 Oct 2026 13:29:08


from __future__ import division
from object_library import all_particles, Particle
import parameters as Param

import propagators as Prop

phi = Particle(pdg_code = 9000001,
               name = 'phi',
               antiname = 'phi',
               spin = 1,
               color = 1,
               mass = Param.mphi,
               width = Param.ZERO,
               texname = 'phi',
               antitexname = 'phi',
               charge = 0)

psi = Particle(pdg_code = 9000002,
               name = 'psi',
               antiname = 'psi~',
               spin = 2,
               color = 1,
               mass = Param.Mpsi,
               width = Param.ZERO,
               texname = 'psi',
               antitexname = 'psi~',
               charge = 0)

psi__tilde__ = psi.anti()

