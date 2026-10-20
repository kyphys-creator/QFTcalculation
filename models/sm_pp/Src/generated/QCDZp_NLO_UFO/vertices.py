# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 20 Oct 2026 14:26:05


from object_library import all_vertices, Vertex
import particles as P
import couplings as C
import lorentz as L


V_1 = Vertex(name = 'V_1',
             particles = [ P.ghG, P.ghG__tilde__, P.g ],
             color = [ 'f(1,2,3)' ],
             lorentz = [ L.UUV1 ],
             couplings = {(0,0):C.GC_1})

V_2 = Vertex(name = 'V_2',
             particles = [ P.g, P.g, P.g ],
             color = [ 'f(1,2,3)' ],
             lorentz = [ L.VVV2 ],
             couplings = {(0,0):C.GC_1})

V_3 = Vertex(name = 'V_3',
             particles = [ P.g, P.g, P.g, P.g ],
             color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
             lorentz = [ L.VVVV2, L.VVVV3, L.VVVV4 ],
             couplings = {(1,0):C.GC_4,(0,0):C.GC_4,(2,1):C.GC_4,(0,1):C.GC_3,(2,2):C.GC_3,(1,2):C.GC_3})

V_4 = Vertex(name = 'V_4',
             particles = [ P.c__tilde__, P.c, P.g ],
             color = [ 'T(3,2,1)' ],
             lorentz = [ L.FFV1 ],
             couplings = {(0,0):C.GC_2})

V_5 = Vertex(name = 'V_5',
             particles = [ P.u__tilde__, P.u, P.g ],
             color = [ 'T(3,2,1)' ],
             lorentz = [ L.FFV1 ],
             couplings = {(0,0):C.GC_2})

V_6 = Vertex(name = 'V_6',
             particles = [ P.d__tilde__, P.d, P.g ],
             color = [ 'T(3,2,1)' ],
             lorentz = [ L.FFV1 ],
             couplings = {(0,0):C.GC_2})

V_7 = Vertex(name = 'V_7',
             particles = [ P.s__tilde__, P.s, P.g ],
             color = [ 'T(3,2,1)' ],
             lorentz = [ L.FFV1 ],
             couplings = {(0,0):C.GC_2})

V_8 = Vertex(name = 'V_8',
             particles = [ P.d__tilde__, P.d, P.Zp ],
             color = [ 'Identity(1,2)' ],
             lorentz = [ L.FFV1, L.FFV2 ],
             couplings = {(0,0):C.GC_7,(0,1):C.GC_5})

V_9 = Vertex(name = 'V_9',
             particles = [ P.s__tilde__, P.s, P.Zp ],
             color = [ 'Identity(1,2)' ],
             lorentz = [ L.FFV1, L.FFV2 ],
             couplings = {(0,0):C.GC_7,(0,1):C.GC_5})

V_10 = Vertex(name = 'V_10',
              particles = [ P.e__plus__, P.e__minus__, P.Zp ],
              color = [ '1' ],
              lorentz = [ L.FFV1, L.FFV2 ],
              couplings = {(0,0):C.GC_9,(0,1):C.GC_5})

V_11 = Vertex(name = 'V_11',
              particles = [ P.c__tilde__, P.c, P.Zp ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFV1, L.FFV2 ],
              couplings = {(0,0):C.GC_8,(0,1):C.GC_6})

V_12 = Vertex(name = 'V_12',
              particles = [ P.u__tilde__, P.u, P.Zp ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFV1, L.FFV2 ],
              couplings = {(0,0):C.GC_8,(0,1):C.GC_6})

