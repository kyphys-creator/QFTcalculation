# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 20 Oct 2026 14:26:05


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'R2',
               particles = [ P.g, P.g, P.g ],
               color = [ 'f(1,2,3)' ],
               lorentz = [ L.VVV2 ],
               loop_particles = [ [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ] ],
               couplings = {(0,0,0):C.R2GC_45_28,(0,0,1):C.R2GC_45_29})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.g, P.g, P.g, P.g ],
               color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
               lorentz = [ L.VVVV2, L.VVVV3, L.VVVV4 ],
               loop_particles = [ [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ] ],
               couplings = {(2,0,0):C.R2GC_40_20,(2,0,1):C.R2GC_40_21,(0,0,0):C.R2GC_40_20,(0,0,1):C.R2GC_40_21,(4,0,0):C.R2GC_38_16,(4,0,1):C.R2GC_38_17,(3,0,0):C.R2GC_38_16,(3,0,1):C.R2GC_38_17,(8,0,0):C.R2GC_39_18,(8,0,1):C.R2GC_39_19,(6,0,0):C.R2GC_47_30,(6,0,1):C.R2GC_50_35,(7,0,0):C.R2GC_48_32,(7,0,1):C.R2GC_49_34,(5,0,0):C.R2GC_38_16,(5,0,1):C.R2GC_38_17,(1,0,0):C.R2GC_38_16,(1,0,1):C.R2GC_38_17,(11,0,0):C.R2GC_42_23,(11,0,1):C.R2GC_42_24,(10,0,0):C.R2GC_42_23,(10,0,1):C.R2GC_42_24,(9,0,1):C.R2GC_41_22,(0,1,0):C.R2GC_40_20,(0,1,1):C.R2GC_40_21,(2,1,0):C.R2GC_40_20,(2,1,1):C.R2GC_40_21,(5,1,0):C.R2GC_38_16,(5,1,1):C.R2GC_38_17,(1,1,0):C.R2GC_38_16,(1,1,1):C.R2GC_38_17,(7,1,0):C.R2GC_48_32,(7,1,1):C.R2GC_48_33,(4,1,0):C.R2GC_38_16,(4,1,1):C.R2GC_38_17,(3,1,0):C.R2GC_38_16,(3,1,1):C.R2GC_38_17,(8,1,0):C.R2GC_39_18,(8,1,1):C.R2GC_52_37,(6,1,0):C.R2GC_43_25,(6,1,1):C.R2GC_43_26,(11,1,0):C.R2GC_42_23,(11,1,1):C.R2GC_42_24,(10,1,0):C.R2GC_42_23,(10,1,1):C.R2GC_42_24,(9,1,1):C.R2GC_41_22,(0,2,0):C.R2GC_40_20,(0,2,1):C.R2GC_40_21,(2,2,0):C.R2GC_40_20,(2,2,1):C.R2GC_40_21,(5,2,0):C.R2GC_38_16,(5,2,1):C.R2GC_38_17,(1,2,0):C.R2GC_38_16,(1,2,1):C.R2GC_38_17,(7,2,0):C.R2GC_44_27,(7,2,1):C.R2GC_40_21,(4,2,0):C.R2GC_38_16,(4,2,1):C.R2GC_38_17,(3,2,0):C.R2GC_38_16,(3,2,1):C.R2GC_38_17,(8,2,0):C.R2GC_39_18,(8,2,1):C.R2GC_51_36,(6,2,0):C.R2GC_47_30,(6,2,1):C.R2GC_47_31,(11,2,0):C.R2GC_42_23,(11,2,1):C.R2GC_42_24,(10,2,0):C.R2GC_42_23,(10,2,1):C.R2GC_42_24,(9,2,1):C.R2GC_41_22})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.c__tilde__, P.c, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.c, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_15_5})

V_4 = CTVertex(name = 'V_4',
               type = 'R2',
               particles = [ P.u__tilde__, P.u, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.g, P.u] ] ],
               couplings = {(0,0,0):C.R2GC_15_5})

V_5 = CTVertex(name = 'V_5',
               type = 'R2',
               particles = [ P.d__tilde__, P.d, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.d, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_15_5})

V_6 = CTVertex(name = 'V_6',
               type = 'R2',
               particles = [ P.s__tilde__, P.s, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.g, P.s] ] ],
               couplings = {(0,0,0):C.R2GC_15_5})

V_7 = CTVertex(name = 'V_7',
               type = 'R2',
               particles = [ P.d__tilde__, P.d, P.Zp ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2, L.FFV3 ],
               loop_particles = [ [ [P.d, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_28_15,(0,1,0):C.R2GC_16_6})

V_8 = CTVertex(name = 'V_8',
               type = 'R2',
               particles = [ P.s__tilde__, P.s, P.Zp ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2, L.FFV5 ],
               loop_particles = [ [ [P.g, P.s] ] ],
               couplings = {(0,0,0):C.R2GC_18_7,(0,1,0):C.R2GC_16_6})

V_9 = CTVertex(name = 'V_9',
               type = 'R2',
               particles = [ P.c__tilde__, P.c, P.Zp ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV2, L.FFV5 ],
               loop_particles = [ [ [P.c, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_12_3,(0,1,0):C.R2GC_13_4})

V_10 = CTVertex(name = 'V_10',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.Zp ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV5 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_12_3,(0,1,0):C.R2GC_13_4})

V_11 = CTVertex(name = 'V_11',
                type = 'R2',
                particles = [ P.u__tilde__, P.u ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_12 = CTVertex(name = 'V_12',
                type = 'R2',
                particles = [ P.c__tilde__, P.c ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_13 = CTVertex(name = 'V_13',
                type = 'R2',
                particles = [ P.d__tilde__, P.d ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_14 = CTVertex(name = 'V_14',
                type = 'R2',
                particles = [ P.s__tilde__, P.s ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_15 = CTVertex(name = 'V_15',
                type = 'R2',
                particles = [ P.g, P.g ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VV2, L.VV3 ],
                loop_particles = [ [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ] ],
                couplings = {(0,1,1):C.R2GC_10_1,(0,0,0):C.R2GC_24_8})

V_16 = CTVertex(name = 'V_16',
                type = 'R2',
                particles = [ P.g, P.g, P.Zp, P.Zp ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVVV5 ],
                loop_particles = [ [ [P.c], [P.u] ], [ [P.d], [P.s] ] ],
                couplings = {(0,0,0):C.R2GC_27_13,(0,0,1):C.R2GC_27_14})

V_17 = CTVertex(name = 'V_17',
                type = 'R2',
                particles = [ P.g, P.g, P.g, P.Zp ],
                color = [ 'd(1,2,3)', 'f(1,2,3)' ],
                lorentz = [ L.VVVV1, L.VVVV5 ],
                loop_particles = [ [ [P.c], [P.u] ], [ [P.d], [P.s] ] ],
                couplings = {(1,0,0):C.R2GC_25_9,(1,0,1):C.R2GC_25_10,(0,1,0):C.R2GC_26_11,(0,1,1):C.R2GC_26_12})

V_18 = CTVertex(name = 'V_18',
                type = 'UV',
                particles = [ P.g, P.g, P.g ],
                color = [ 'f(1,2,3)' ],
                lorentz = [ L.VVV1, L.VVV2, L.VVV3 ],
                loop_particles = [ [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(0,1,0):C.UVGC_45_19,(0,2,1):C.UVGC_29_1,(0,0,2):C.UVGC_30_2})

V_19 = CTVertex(name = 'V_19',
                type = 'UV',
                particles = [ P.g, P.g, P.g, P.g ],
                color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV4 ],
                loop_particles = [ [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(2,0,1):C.UVGC_39_10,(2,0,2):C.UVGC_39_9,(0,0,1):C.UVGC_39_10,(0,0,2):C.UVGC_39_9,(4,0,1):C.UVGC_38_7,(4,0,2):C.UVGC_38_8,(3,0,1):C.UVGC_38_7,(3,0,2):C.UVGC_38_8,(8,0,1):C.UVGC_39_9,(8,0,2):C.UVGC_39_10,(6,0,0):C.UVGC_49_27,(6,0,1):C.UVGC_50_30,(6,0,2):C.UVGC_50_31,(7,0,0):C.UVGC_49_27,(7,0,1):C.UVGC_49_28,(7,0,2):C.UVGC_49_29,(5,0,1):C.UVGC_38_7,(5,0,2):C.UVGC_38_8,(1,0,1):C.UVGC_38_7,(1,0,2):C.UVGC_38_8,(11,0,1):C.UVGC_42_13,(11,0,2):C.UVGC_42_14,(10,0,1):C.UVGC_42_13,(10,0,2):C.UVGC_42_14,(9,0,1):C.UVGC_41_11,(9,0,2):C.UVGC_41_12,(0,1,1):C.UVGC_39_10,(0,1,2):C.UVGC_39_9,(2,1,1):C.UVGC_39_10,(2,1,2):C.UVGC_39_9,(5,1,1):C.UVGC_38_7,(5,1,2):C.UVGC_38_8,(1,1,1):C.UVGC_38_7,(1,1,2):C.UVGC_38_8,(7,1,0):C.UVGC_47_23,(7,1,1):C.UVGC_48_25,(7,1,2):C.UVGC_48_26,(4,1,1):C.UVGC_38_7,(4,1,2):C.UVGC_38_8,(3,1,1):C.UVGC_38_7,(3,1,2):C.UVGC_38_8,(8,1,0):C.UVGC_52_35,(8,1,1):C.UVGC_52_36,(8,1,2):C.UVGC_52_37,(6,1,1):C.UVGC_43_15,(6,1,2):C.UVGC_43_16,(11,1,1):C.UVGC_42_13,(11,1,2):C.UVGC_42_14,(10,1,1):C.UVGC_42_13,(10,1,2):C.UVGC_42_14,(9,1,1):C.UVGC_41_11,(9,1,2):C.UVGC_41_12,(0,2,1):C.UVGC_39_10,(0,2,2):C.UVGC_39_9,(2,2,1):C.UVGC_39_10,(2,2,2):C.UVGC_39_9,(5,2,1):C.UVGC_38_7,(5,2,2):C.UVGC_38_8,(1,2,1):C.UVGC_38_7,(1,2,2):C.UVGC_38_8,(7,2,1):C.UVGC_44_17,(7,2,2):C.UVGC_44_18,(4,2,1):C.UVGC_38_7,(4,2,2):C.UVGC_38_8,(3,2,1):C.UVGC_38_7,(3,2,2):C.UVGC_38_8,(8,2,0):C.UVGC_51_32,(8,2,1):C.UVGC_51_33,(8,2,2):C.UVGC_51_34,(6,2,0):C.UVGC_47_23,(6,2,1):C.UVGC_47_24,(6,2,2):C.UVGC_41_11,(11,2,1):C.UVGC_42_13,(11,2,2):C.UVGC_42_14,(10,2,1):C.UVGC_42_13,(10,2,2):C.UVGC_42_14,(9,2,1):C.UVGC_41_11,(9,2,2):C.UVGC_41_12})

V_20 = CTVertex(name = 'V_20',
                type = 'UV',
                particles = [ P.c__tilde__, P.c, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.c], [P.d], [P.s], [P.u] ], [ [P.c, P.g] ], [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(0,0,1):C.UVGC_33_4,(0,1,0):C.UVGC_46_20,(0,1,2):C.UVGC_46_21,(0,1,3):C.UVGC_46_22,(0,1,1):C.UVGC_53_38,(0,2,0):C.UVGC_46_20,(0,2,2):C.UVGC_46_21,(0,2,3):C.UVGC_46_22,(0,2,1):C.UVGC_53_38})

V_21 = CTVertex(name = 'V_21',
                type = 'UV',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV4, L.FFV5 ],
                loop_particles = [ [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.u] ] ],
                couplings = {(0,0,3):C.UVGC_33_4,(0,1,0):C.UVGC_46_20,(0,1,1):C.UVGC_46_21,(0,1,2):C.UVGC_46_22})

V_22 = CTVertex(name = 'V_22',
                type = 'UV',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV4, L.FFV5 ],
                loop_particles = [ [ [P.c], [P.d], [P.s], [P.u] ], [ [P.d, P.g] ], [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(0,0,1):C.UVGC_33_4,(0,1,0):C.UVGC_46_20,(0,1,2):C.UVGC_46_21,(0,1,3):C.UVGC_46_22})

V_23 = CTVertex(name = 'V_23',
                type = 'UV',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.s] ] ],
                couplings = {(0,0,3):C.UVGC_33_4,(0,1,0):C.UVGC_46_20,(0,1,1):C.UVGC_46_21,(0,1,2):C.UVGC_46_22,(0,1,3):C.UVGC_53_38,(0,2,0):C.UVGC_46_20,(0,2,1):C.UVGC_46_21,(0,2,2):C.UVGC_46_22,(0,2,3):C.UVGC_53_38})

V_24 = CTVertex(name = 'V_24',
                type = 'UV',
                particles = [ P.u__tilde__, P.u ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_31_3})

V_25 = CTVertex(name = 'V_25',
                type = 'UV',
                particles = [ P.c__tilde__, P.c ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_31_3})

V_26 = CTVertex(name = 'V_26',
                type = 'UV',
                particles = [ P.d__tilde__, P.d ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_31_3})

V_27 = CTVertex(name = 'V_27',
                type = 'UV',
                particles = [ P.s__tilde__, P.s ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_31_3})

V_28 = CTVertex(name = 'V_28',
                type = 'UV',
                particles = [ P.g, P.g ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VV1 ],
                loop_particles = [ [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(0,0,0):C.UVGC_37_5,(0,0,1):C.UVGC_37_6})

