# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 20 Oct 2026 12:21:32


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'R2',
               particles = [ P.g, P.g, P.h ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.VVS2 ],
               loop_particles = [ [ [P.g] ] ],
               couplings = {(0,0,0):C.R2GC_8_25})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.g, P.g, P.g ],
               color = [ 'f(1,2,3)' ],
               lorentz = [ L.VVV1, L.VVV2 ],
               loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ] ],
               couplings = {(0,0,0):C.R2GC_41_19,(0,1,1):C.R2GC_7_24})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.g, P.g, P.g, P.g ],
               color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
               lorentz = [ L.VVVV1, L.VVVV2, L.VVVV4, L.VVVV7 ],
               loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ] ],
               couplings = {(2,0,0):C.R2GC_36_10,(2,0,1):C.R2GC_36_11,(0,0,0):C.R2GC_36_10,(0,0,1):C.R2GC_36_11,(4,0,0):C.R2GC_34_6,(4,0,1):C.R2GC_34_7,(3,0,0):C.R2GC_34_6,(3,0,1):C.R2GC_34_7,(8,0,0):C.R2GC_35_8,(8,0,1):C.R2GC_35_9,(6,0,0):C.R2GC_43_20,(6,0,1):C.R2GC_46_23,(7,0,0):C.R2GC_44_21,(7,0,1):C.R2GC_45_22,(5,0,0):C.R2GC_34_6,(5,0,1):C.R2GC_34_7,(1,0,0):C.R2GC_34_6,(1,0,1):C.R2GC_34_7,(11,3,0):C.R2GC_38_13,(11,3,1):C.R2GC_38_14,(10,3,0):C.R2GC_38_13,(10,3,1):C.R2GC_38_14,(9,3,1):C.R2GC_37_12,(0,1,0):C.R2GC_36_10,(0,1,1):C.R2GC_36_11,(2,1,0):C.R2GC_36_10,(2,1,1):C.R2GC_36_11,(5,1,0):C.R2GC_34_6,(5,1,1):C.R2GC_34_7,(1,1,0):C.R2GC_34_6,(1,1,1):C.R2GC_34_7,(7,1,0):C.R2GC_44_21,(7,1,1):C.R2GC_35_9,(4,1,0):C.R2GC_34_6,(4,1,1):C.R2GC_34_7,(3,1,0):C.R2GC_34_6,(3,1,1):C.R2GC_34_7,(8,1,0):C.R2GC_35_8,(8,1,1):C.R2GC_45_22,(6,1,0):C.R2GC_39_15,(6,1,1):C.R2GC_39_16,(0,2,0):C.R2GC_36_10,(0,2,1):C.R2GC_36_11,(2,2,0):C.R2GC_36_10,(2,2,1):C.R2GC_36_11,(5,2,0):C.R2GC_34_6,(5,2,1):C.R2GC_34_7,(1,2,0):C.R2GC_34_6,(1,2,1):C.R2GC_34_7,(7,2,0):C.R2GC_40_17,(7,2,1):C.R2GC_40_18,(4,2,0):C.R2GC_34_6,(4,2,1):C.R2GC_34_7,(3,2,0):C.R2GC_34_6,(3,2,1):C.R2GC_34_7,(8,2,0):C.R2GC_35_8,(8,2,1):C.R2GC_40_18,(6,2,0):C.R2GC_43_20})

V_4 = CTVertex(name = 'V_4',
               type = 'R2',
               particles = [ P.c__tilde__, P.c, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.c, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_10_1})

V_5 = CTVertex(name = 'V_5',
               type = 'R2',
               particles = [ P.u__tilde__, P.u, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.g, P.u] ] ],
               couplings = {(0,0,0):C.R2GC_10_1})

V_6 = CTVertex(name = 'V_6',
               type = 'R2',
               particles = [ P.b__tilde__, P.b, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.b, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_10_1})

V_7 = CTVertex(name = 'V_7',
               type = 'R2',
               particles = [ P.d__tilde__, P.d, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.d, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_10_1})

V_8 = CTVertex(name = 'V_8',
               type = 'R2',
               particles = [ P.s__tilde__, P.s, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.g, P.s] ] ],
               couplings = {(0,0,0):C.R2GC_10_1})

V_9 = CTVertex(name = 'V_9',
               type = 'R2',
               particles = [ P.u__tilde__, P.u ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FF1 ],
               loop_particles = [ [ [P.g, P.u] ] ],
               couplings = {(0,0,0):C.R2GC_11_2})

V_10 = CTVertex(name = 'V_10',
                type = 'R2',
                particles = [ P.c__tilde__, P.c ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_11 = CTVertex(name = 'V_11',
                type = 'R2',
                particles = [ P.d__tilde__, P.d ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_12 = CTVertex(name = 'V_12',
                type = 'R2',
                particles = [ P.s__tilde__, P.s ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_13 = CTVertex(name = 'V_13',
                type = 'R2',
                particles = [ P.b__tilde__, P.b ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_14 = CTVertex(name = 'V_14',
                type = 'R2',
                particles = [ P.g, P.g ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VV1, L.VV2 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ] ],
                couplings = {(0,0,1):C.R2GC_33_5,(0,1,0):C.R2GC_19_3,(0,1,1):C.R2GC_19_4})

V_15 = CTVertex(name = 'V_15',
                type = 'UV',
                particles = [ P.g, P.g, P.h ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.g] ] ],
                couplings = {(0,0,0):C.UVGC_21_2})

V_16 = CTVertex(name = 'V_16',
                type = 'UV',
                particles = [ P.g, P.g, P.g ],
                color = [ 'f(1,2,3)' ],
                lorentz = [ L.VVV1, L.VVV3, L.VVV4 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(0,0,0):C.UVGC_41_20,(0,1,1):C.UVGC_20_1,(0,2,2):C.UVGC_22_3})

V_17 = CTVertex(name = 'V_17',
                type = 'UV',
                particles = [ P.g, P.g, P.g, P.g ],
                color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
                lorentz = [ L.VVVV1, L.VVVV2, L.VVVV4, L.VVVV7 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(2,0,1):C.UVGC_35_11,(2,0,2):C.UVGC_35_10,(0,0,1):C.UVGC_35_11,(0,0,2):C.UVGC_35_10,(4,0,1):C.UVGC_34_8,(4,0,2):C.UVGC_34_9,(3,0,1):C.UVGC_34_8,(3,0,2):C.UVGC_34_9,(8,0,1):C.UVGC_35_10,(8,0,2):C.UVGC_35_11,(6,0,0):C.UVGC_45_26,(6,0,1):C.UVGC_46_29,(6,0,2):C.UVGC_46_30,(7,0,0):C.UVGC_45_26,(7,0,1):C.UVGC_45_27,(7,0,2):C.UVGC_45_28,(5,0,1):C.UVGC_34_8,(5,0,2):C.UVGC_34_9,(1,0,1):C.UVGC_34_8,(1,0,2):C.UVGC_34_9,(11,3,1):C.UVGC_38_14,(11,3,2):C.UVGC_38_15,(10,3,1):C.UVGC_38_14,(10,3,2):C.UVGC_38_15,(9,3,1):C.UVGC_37_12,(9,3,2):C.UVGC_37_13,(0,1,1):C.UVGC_35_11,(0,1,2):C.UVGC_35_10,(2,1,1):C.UVGC_35_11,(2,1,2):C.UVGC_35_10,(5,1,1):C.UVGC_34_8,(5,1,2):C.UVGC_34_9,(1,1,1):C.UVGC_34_8,(1,1,2):C.UVGC_34_9,(7,1,0):C.UVGC_43_24,(7,1,1):C.UVGC_35_10,(7,1,2):C.UVGC_44_25,(4,1,1):C.UVGC_34_8,(4,1,2):C.UVGC_34_9,(3,1,1):C.UVGC_34_8,(3,1,2):C.UVGC_34_9,(8,1,0):C.UVGC_48_33,(8,1,1):C.UVGC_45_27,(8,1,2):C.UVGC_48_34,(6,1,1):C.UVGC_39_16,(6,1,2):C.UVGC_39_17,(0,2,1):C.UVGC_35_11,(0,2,2):C.UVGC_35_10,(2,2,1):C.UVGC_35_11,(2,2,2):C.UVGC_35_10,(5,2,1):C.UVGC_34_8,(5,2,2):C.UVGC_34_9,(1,2,1):C.UVGC_34_8,(1,2,2):C.UVGC_34_9,(7,2,1):C.UVGC_40_18,(7,2,2):C.UVGC_40_19,(4,2,1):C.UVGC_34_8,(4,2,2):C.UVGC_34_9,(3,2,1):C.UVGC_34_8,(3,2,2):C.UVGC_34_9,(8,2,0):C.UVGC_47_31,(8,2,1):C.UVGC_40_18,(8,2,2):C.UVGC_47_32,(6,2,0):C.UVGC_43_24,(6,2,2):C.UVGC_37_12})

V_18 = CTVertex(name = 'V_18',
                type = 'UV',
                particles = [ P.c__tilde__, P.c, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.c, P.g] ], [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(0,0,1):C.UVGC_24_5,(0,1,0):C.UVGC_42_21,(0,1,2):C.UVGC_42_22,(0,1,3):C.UVGC_42_23})

V_19 = CTVertex(name = 'V_19',
                type = 'UV',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.u] ] ],
                couplings = {(0,0,3):C.UVGC_24_5,(0,1,0):C.UVGC_42_21,(0,1,1):C.UVGC_42_22,(0,1,2):C.UVGC_42_23})

V_20 = CTVertex(name = 'V_20',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.b, P.g] ], [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(0,0,1):C.UVGC_24_5,(0,1,0):C.UVGC_42_21,(0,1,2):C.UVGC_42_22,(0,1,3):C.UVGC_42_23})

V_21 = CTVertex(name = 'V_21',
                type = 'UV',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.d, P.g] ], [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(0,0,1):C.UVGC_24_5,(0,1,0):C.UVGC_42_21,(0,1,2):C.UVGC_42_22,(0,1,3):C.UVGC_42_23})

V_22 = CTVertex(name = 'V_22',
                type = 'UV',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.s] ] ],
                couplings = {(0,0,3):C.UVGC_24_5,(0,1,0):C.UVGC_42_21,(0,1,1):C.UVGC_42_22,(0,1,2):C.UVGC_42_23})

V_23 = CTVertex(name = 'V_23',
                type = 'UV',
                particles = [ P.u__tilde__, P.u ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_23_4})

V_24 = CTVertex(name = 'V_24',
                type = 'UV',
                particles = [ P.c__tilde__, P.c ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_23_4})

V_25 = CTVertex(name = 'V_25',
                type = 'UV',
                particles = [ P.d__tilde__, P.d ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_23_4})

V_26 = CTVertex(name = 'V_26',
                type = 'UV',
                particles = [ P.s__tilde__, P.s ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_23_4})

V_27 = CTVertex(name = 'V_27',
                type = 'UV',
                particles = [ P.b__tilde__, P.b ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_23_4})

V_28 = CTVertex(name = 'V_28',
                type = 'UV',
                particles = [ P.g, P.g ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VV1 ],
                loop_particles = [ [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(0,0,0):C.UVGC_33_6,(0,0,1):C.UVGC_33_7})

