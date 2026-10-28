# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 27 Oct 2026 17:53:40


from __future__ import division
from object_library import all_particles, Particle
import parameters as Param

import propagators as Prop

zp = Particle(pdg_code = 32,
              name = 'zp',
              antiname = 'zp',
              spin = 3,
              color = 1,
              mass = Param.MA,
              width = Param.WA,
              texname = 'zp',
              antitexname = 'zp',
              charge = 0,
              GhostNumber = 0,
              QX = 0)

ghA = Particle(pdg_code = 9000001,
               name = 'ghA',
               antiname = 'ghA~',
               spin = -1,
               color = 1,
               mass = Param.MA,
               width = Param.WA,
               texname = 'ghA',
               antitexname = 'ghA~',
               charge = 0,
               GhostNumber = 1,
               QX = 0)

ghA__tilde__ = ghA.anti()

h = Particle(pdg_code = 25,
             name = 'h',
             antiname = 'h',
             spin = 1,
             color = 1,
             mass = Param.MH,
             width = Param.WH,
             texname = 'h',
             antitexname = 'h',
             charge = 0,
             GhostNumber = 0,
             QX = 0)

G0 = Particle(pdg_code = 250,
              name = 'G0',
              antiname = 'G0',
              spin = 1,
              color = 1,
              mass = Param.MA,
              width = Param.WA,
              texname = 'G0',
              antitexname = 'G0',
              goldstone = True,
              charge = 0,
              GhostNumber = 0,
              QX = 0)

