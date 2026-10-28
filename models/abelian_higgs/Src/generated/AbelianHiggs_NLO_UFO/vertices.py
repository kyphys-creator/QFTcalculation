# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 27 Oct 2026 19:37:01


from object_library import all_vertices, Vertex
import particles as P
import couplings as C
import lorentz as L


V_1 = Vertex(name = 'V_1',
             particles = [ P.G0, P.G0, P.G0, P.G0 ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_5})

V_2 = Vertex(name = 'V_2',
             particles = [ P.G0, P.G0, P.h, P.h ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_4})

V_3 = Vertex(name = 'V_3',
             particles = [ P.h, P.h, P.h, P.h ],
             color = [ '1' ],
             lorentz = [ L.SSSS1 ],
             couplings = {(0,0):C.GC_5})

V_4 = Vertex(name = 'V_4',
             particles = [ P.G0, P.G0, P.h ],
             color = [ '1' ],
             lorentz = [ L.SSS1 ],
             couplings = {(0,0):C.GC_7})

V_5 = Vertex(name = 'V_5',
             particles = [ P.h, P.h, P.h ],
             color = [ '1' ],
             lorentz = [ L.SSS1 ],
             couplings = {(0,0):C.GC_8})

V_6 = Vertex(name = 'V_6',
             particles = [ P.zp, P.zp, P.G0, P.G0 ],
             color = [ '1' ],
             lorentz = [ L.VVSS1 ],
             couplings = {(0,0):C.GC_3})

V_7 = Vertex(name = 'V_7',
             particles = [ P.zp, P.zp, P.h, P.h ],
             color = [ '1' ],
             lorentz = [ L.VVSS1 ],
             couplings = {(0,0):C.GC_3})

V_8 = Vertex(name = 'V_8',
             particles = [ P.zp, P.zp, P.h ],
             color = [ '1' ],
             lorentz = [ L.VVS1 ],
             couplings = {(0,0):C.GC_6})

V_9 = Vertex(name = 'V_9',
             particles = [ P.zp, P.G0, P.h ],
             color = [ '1' ],
             lorentz = [ L.VSS1, L.VSS2 ],
             couplings = {(0,0):C.GC_2,(0,1):C.GC_1})

V_10 = Vertex(name = 'V_10',
              particles = [ P.ghA, P.ghA__tilde__, P.h ],
              color = [ '1' ],
              lorentz = [ L.UUS1 ],
              couplings = {(0,0):C.GC_9})

