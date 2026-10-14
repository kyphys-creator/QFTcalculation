# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Wed 14 Oct 2026 15:49:25


from object_library import all_vertices, Vertex
import particles as P
import couplings as C
import lorentz as L


V_1 = Vertex(name = 'V_1',
             particles = [ P.ghG, P.ghG__tilde__, P.g ],
             color = [ 'f(1,2,3)' ],
             lorentz = [ L.UUV1 ],
             couplings = {(0,0):C.GC_4})

V_2 = Vertex(name = 'V_2',
             particles = [ P.g, P.g, P.g ],
             color = [ 'f(1,2,3)' ],
             lorentz = [ L.VVV2 ],
             couplings = {(0,0):C.GC_4})

V_3 = Vertex(name = 'V_3',
             particles = [ P.g, P.g, P.g, P.g ],
             color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
             lorentz = [ L.VVVV3, L.VVVV5, L.VVVV6 ],
             couplings = {(1,1):C.GC_6,(0,0):C.GC_6,(2,2):C.GC_6})

V_4 = Vertex(name = 'V_4',
             particles = [ P.b__tilde__, P.b, P.a ],
             color = [ 'Identity(1,2)' ],
             lorentz = [ L.FFV1 ],
             couplings = {(0,0):C.GC_1})

V_5 = Vertex(name = 'V_5',
             particles = [ P.d__tilde__, P.d, P.a ],
             color = [ 'Identity(1,2)' ],
             lorentz = [ L.FFV1 ],
             couplings = {(0,0):C.GC_1})

V_6 = Vertex(name = 'V_6',
             particles = [ P.s__tilde__, P.s, P.a ],
             color = [ 'Identity(1,2)' ],
             lorentz = [ L.FFV1 ],
             couplings = {(0,0):C.GC_1})

V_7 = Vertex(name = 'V_7',
             particles = [ P.e__plus__, P.e__minus__, P.a ],
             color = [ '1' ],
             lorentz = [ L.FFV1 ],
             couplings = {(0,0):C.GC_3})

V_8 = Vertex(name = 'V_8',
             particles = [ P.t__tilde__, P.t, P.a ],
             color = [ 'Identity(1,2)' ],
             lorentz = [ L.FFV1 ],
             couplings = {(0,0):C.GC_2})

V_9 = Vertex(name = 'V_9',
             particles = [ P.c__tilde__, P.c, P.a ],
             color = [ 'Identity(1,2)' ],
             lorentz = [ L.FFV1 ],
             couplings = {(0,0):C.GC_2})

V_10 = Vertex(name = 'V_10',
              particles = [ P.u__tilde__, P.u, P.a ],
              color = [ 'Identity(1,2)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_2})

V_11 = Vertex(name = 'V_11',
              particles = [ P.c__tilde__, P.c, P.g ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_5})

V_12 = Vertex(name = 'V_12',
              particles = [ P.u__tilde__, P.u, P.g ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_5})

V_13 = Vertex(name = 'V_13',
              particles = [ P.b__tilde__, P.b, P.g ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_5})

V_14 = Vertex(name = 'V_14',
              particles = [ P.d__tilde__, P.d, P.g ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_5})

V_15 = Vertex(name = 'V_15',
              particles = [ P.s__tilde__, P.s, P.g ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_5})

V_16 = Vertex(name = 'V_16',
              particles = [ P.t__tilde__, P.t, P.g ],
              color = [ 'T(3,2,1)' ],
              lorentz = [ L.FFV1 ],
              couplings = {(0,0):C.GC_5})

