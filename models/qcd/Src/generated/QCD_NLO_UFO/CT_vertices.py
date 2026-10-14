# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Wed 14 Oct 2026 15:49:25


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'R2',
               particles = [ P.g, P.g, P.g ],
               color = [ 'f(1,2,3)' ],
               lorentz = [ L.VVV2 ],
               loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
               couplings = {(0,0,0):C.R2GC_56_23,(0,0,1):C.R2GC_56_24})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.g, P.g, P.g, P.g ],
               color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
               lorentz = [ L.VVVV1, L.VVVV2, L.VVVV4, L.VVVV7 ],
               loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
               couplings = {(2,0,0):C.R2GC_41_13,(2,0,1):C.R2GC_41_14,(0,0,0):C.R2GC_41_13,(0,0,1):C.R2GC_41_14,(4,0,0):C.R2GC_39_9,(4,0,1):C.R2GC_39_10,(3,0,0):C.R2GC_39_9,(3,0,1):C.R2GC_39_10,(8,0,0):C.R2GC_40_11,(8,0,1):C.R2GC_40_12,(6,0,0):C.R2GC_45_18,(6,0,1):C.R2GC_61_30,(7,0,0):C.R2GC_46_20,(7,0,1):C.R2GC_60_29,(5,0,0):C.R2GC_39_9,(5,0,1):C.R2GC_39_10,(1,0,0):C.R2GC_39_9,(1,0,1):C.R2GC_39_10,(11,3,0):C.R2GC_43_16,(11,3,1):C.R2GC_43_17,(10,3,0):C.R2GC_43_16,(10,3,1):C.R2GC_43_17,(9,3,1):C.R2GC_42_15,(0,1,0):C.R2GC_41_13,(0,1,1):C.R2GC_41_14,(2,1,0):C.R2GC_41_13,(2,1,1):C.R2GC_41_14,(5,1,0):C.R2GC_39_9,(5,1,1):C.R2GC_39_10,(1,1,0):C.R2GC_39_9,(1,1,1):C.R2GC_39_10,(7,1,0):C.R2GC_46_20,(7,1,1):C.R2GC_46_21,(4,1,0):C.R2GC_39_9,(4,1,1):C.R2GC_39_10,(3,1,0):C.R2GC_39_9,(3,1,1):C.R2GC_39_10,(8,1,0):C.R2GC_40_11,(8,1,1):C.R2GC_62_31,(6,1,0):C.R2GC_57_25,(6,1,1):C.R2GC_57_26,(0,2,0):C.R2GC_41_13,(0,2,1):C.R2GC_41_14,(2,2,0):C.R2GC_41_13,(2,2,1):C.R2GC_41_14,(5,2,0):C.R2GC_39_9,(5,2,1):C.R2GC_39_10,(1,2,0):C.R2GC_39_9,(1,2,1):C.R2GC_39_10,(7,2,0):C.R2GC_58_27,(7,2,1):C.R2GC_41_14,(4,2,0):C.R2GC_39_9,(4,2,1):C.R2GC_39_10,(3,2,0):C.R2GC_39_9,(3,2,1):C.R2GC_39_10,(8,2,0):C.R2GC_40_11,(8,2,1):C.R2GC_59_28,(6,2,0):C.R2GC_45_18,(6,2,1):C.R2GC_45_19})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.b__tilde__, P.b, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.b, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_10_1})

V_4 = CTVertex(name = 'V_4',
               type = 'R2',
               particles = [ P.d__tilde__, P.d, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.d, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_10_1})

V_5 = CTVertex(name = 'V_5',
               type = 'R2',
               particles = [ P.s__tilde__, P.s, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.g, P.s] ] ],
               couplings = {(0,0,0):C.R2GC_10_1})

V_6 = CTVertex(name = 'V_6',
               type = 'R2',
               particles = [ P.t__tilde__, P.t, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.g, P.t] ] ],
               couplings = {(0,0,0):C.R2GC_47_22})

V_7 = CTVertex(name = 'V_7',
               type = 'R2',
               particles = [ P.c__tilde__, P.c, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.c, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_47_22})

V_8 = CTVertex(name = 'V_8',
               type = 'R2',
               particles = [ P.u__tilde__, P.u, P.a ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.g, P.u] ] ],
               couplings = {(0,0,0):C.R2GC_47_22})

V_9 = CTVertex(name = 'V_9',
               type = 'R2',
               particles = [ P.c__tilde__, P.c, P.g ],
               color = [ 'T(3,2,1)' ],
               lorentz = [ L.FFV1 ],
               loop_particles = [ [ [P.c, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_11_2})

V_10 = CTVertex(name = 'V_10',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_11 = CTVertex(name = 'V_11',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_12 = CTVertex(name = 'V_12',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_13 = CTVertex(name = 'V_13',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_14 = CTVertex(name = 'V_14',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_11_2})

V_15 = CTVertex(name = 'V_15',
                type = 'R2',
                particles = [ P.u__tilde__, P.u ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_12_3})

V_16 = CTVertex(name = 'V_16',
                type = 'R2',
                particles = [ P.c__tilde__, P.c ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_12_3})

V_17 = CTVertex(name = 'V_17',
                type = 'R2',
                particles = [ P.d__tilde__, P.d ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_12_3})

V_18 = CTVertex(name = 'V_18',
                type = 'R2',
                particles = [ P.s__tilde__, P.s ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_12_3})

V_19 = CTVertex(name = 'V_19',
                type = 'R2',
                particles = [ P.b__tilde__, P.b ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_12_3})

V_20 = CTVertex(name = 'V_20',
                type = 'R2',
                particles = [ P.t__tilde__, P.t ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2, L.FF3 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_66_32,(0,1,0):C.R2GC_12_3})

V_21 = CTVertex(name = 'V_21',
                type = 'R2',
                particles = [ P.g, P.g ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VV2, L.VV3, L.VV4 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ], [ [P.t] ] ],
                couplings = {(0,2,1):C.R2GC_7_33,(0,0,2):C.R2GC_8_34,(0,1,0):C.R2GC_20_4})

V_22 = CTVertex(name = 'V_22',
                type = 'R2',
                particles = [ P.a, P.a, P.g, P.g ],
                color = [ 'Identity(3,4)' ],
                lorentz = [ L.VVVV7 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_21_5,(0,0,1):C.R2GC_21_6})

V_23 = CTVertex(name = 'V_23',
                type = 'R2',
                particles = [ P.a, P.g, P.g, P.g ],
                color = [ 'd(2,3,4)' ],
                lorentz = [ L.VVVV7 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_22_7,(0,0,1):C.R2GC_22_8})

V_24 = CTVertex(name = 'V_24',
                type = 'UV',
                particles = [ P.g, P.g, P.g ],
                color = [ 'f(1,2,3)' ],
                lorentz = [ L.VVV1, L.VVV2, L.VVV3 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,1,0):C.UVGC_56_28,(0,1,3):C.UVGC_56_29,(0,2,1):C.UVGC_23_1,(0,0,2):C.UVGC_24_2})

V_25 = CTVertex(name = 'V_25',
                type = 'UV',
                particles = [ P.g, P.g, P.g, P.g ],
                color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
                lorentz = [ L.VVVV1, L.VVVV2, L.VVVV4, L.VVVV7 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(2,0,2):C.UVGC_40_12,(2,0,3):C.UVGC_40_11,(0,0,2):C.UVGC_40_12,(0,0,3):C.UVGC_40_11,(4,0,2):C.UVGC_39_9,(4,0,3):C.UVGC_39_10,(3,0,2):C.UVGC_39_9,(3,0,3):C.UVGC_39_10,(8,0,2):C.UVGC_40_11,(8,0,3):C.UVGC_40_12,(6,0,1):C.UVGC_60_39,(6,0,2):C.UVGC_61_43,(6,0,3):C.UVGC_61_44,(6,0,4):C.UVGC_60_42,(7,0,1):C.UVGC_60_39,(7,0,2):C.UVGC_60_40,(7,0,3):C.UVGC_60_41,(7,0,4):C.UVGC_60_42,(5,0,2):C.UVGC_39_9,(5,0,3):C.UVGC_39_10,(1,0,2):C.UVGC_39_9,(1,0,3):C.UVGC_39_10,(11,3,2):C.UVGC_43_15,(11,3,3):C.UVGC_43_16,(10,3,2):C.UVGC_43_15,(10,3,3):C.UVGC_43_16,(9,3,2):C.UVGC_42_13,(9,3,3):C.UVGC_42_14,(0,1,2):C.UVGC_40_12,(0,1,3):C.UVGC_40_11,(2,1,2):C.UVGC_40_12,(2,1,3):C.UVGC_40_11,(5,1,2):C.UVGC_39_9,(5,1,3):C.UVGC_39_10,(1,1,2):C.UVGC_39_9,(1,1,3):C.UVGC_39_10,(7,1,0):C.UVGC_45_21,(7,1,2):C.UVGC_46_23,(7,1,3):C.UVGC_46_24,(4,1,2):C.UVGC_39_9,(4,1,3):C.UVGC_39_10,(3,1,2):C.UVGC_39_9,(3,1,3):C.UVGC_39_10,(8,1,1):C.UVGC_62_45,(8,1,2):C.UVGC_62_46,(8,1,3):C.UVGC_62_47,(8,1,4):C.UVGC_62_48,(6,1,2):C.UVGC_57_30,(6,1,3):C.UVGC_57_31,(6,1,4):C.UVGC_57_32,(0,2,2):C.UVGC_40_12,(0,2,3):C.UVGC_40_11,(2,2,2):C.UVGC_40_12,(2,2,3):C.UVGC_40_11,(5,2,2):C.UVGC_39_9,(5,2,3):C.UVGC_39_10,(1,2,2):C.UVGC_39_9,(1,2,3):C.UVGC_39_10,(7,2,2):C.UVGC_58_33,(7,2,3):C.UVGC_58_34,(7,2,4):C.UVGC_57_32,(4,2,2):C.UVGC_39_9,(4,2,3):C.UVGC_39_10,(3,2,2):C.UVGC_39_9,(3,2,3):C.UVGC_39_10,(8,2,1):C.UVGC_59_35,(8,2,2):C.UVGC_59_36,(8,2,3):C.UVGC_59_37,(8,2,4):C.UVGC_59_38,(6,2,0):C.UVGC_45_21,(6,2,2):C.UVGC_45_22,(6,2,3):C.UVGC_42_13})

V_26 = CTVertex(name = 'V_26',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV4 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_26_4})

V_27 = CTVertex(name = 'V_27',
                type = 'UV',
                particles = [ P.d__tilde__, P.d, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV4 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_26_4})

V_28 = CTVertex(name = 'V_28',
                type = 'UV',
                particles = [ P.s__tilde__, P.s, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV4 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_26_4})

V_29 = CTVertex(name = 'V_29',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV6 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_47_25,(0,1,0):C.UVGC_64_50})

V_30 = CTVertex(name = 'V_30',
                type = 'UV',
                particles = [ P.c__tilde__, P.c, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_47_25,(0,1,0):C.UVGC_29_6,(0,2,0):C.UVGC_29_6})

V_31 = CTVertex(name = 'V_31',
                type = 'UV',
                particles = [ P.u__tilde__, P.u, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_47_25,(0,1,0):C.UVGC_29_6,(0,2,0):C.UVGC_29_6})

V_32 = CTVertex(name = 'V_32',
                type = 'UV',
                particles = [ P.c__tilde__, P.c, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.c, P.g] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,0,1):C.UVGC_27_5,(0,1,0):C.UVGC_44_17,(0,1,2):C.UVGC_44_18,(0,1,3):C.UVGC_44_19,(0,1,4):C.UVGC_44_20,(0,1,1):C.UVGC_48_26,(0,2,0):C.UVGC_44_17,(0,2,2):C.UVGC_44_18,(0,2,3):C.UVGC_44_19,(0,2,4):C.UVGC_44_20,(0,2,1):C.UVGC_48_26})

V_33 = CTVertex(name = 'V_33',
                type = 'UV',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.u] ], [ [P.t] ] ],
                couplings = {(0,0,3):C.UVGC_27_5,(0,1,0):C.UVGC_44_17,(0,1,1):C.UVGC_44_18,(0,1,2):C.UVGC_44_19,(0,1,4):C.UVGC_44_20,(0,1,3):C.UVGC_48_26,(0,2,0):C.UVGC_44_17,(0,2,1):C.UVGC_44_18,(0,2,2):C.UVGC_44_19,(0,2,4):C.UVGC_44_20,(0,2,3):C.UVGC_48_26})

V_34 = CTVertex(name = 'V_34',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.b, P.g] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,0,1):C.UVGC_27_5,(0,1,0):C.UVGC_44_17,(0,1,2):C.UVGC_44_18,(0,1,3):C.UVGC_44_19,(0,1,4):C.UVGC_44_20})

V_35 = CTVertex(name = 'V_35',
                type = 'UV',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.d, P.g] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,0,1):C.UVGC_27_5,(0,1,0):C.UVGC_44_17,(0,1,2):C.UVGC_44_18,(0,1,3):C.UVGC_44_19,(0,1,4):C.UVGC_44_20})

V_36 = CTVertex(name = 'V_36',
                type = 'UV',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV5, L.FFV6 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.s] ], [ [P.t] ] ],
                couplings = {(0,0,3):C.UVGC_27_5,(0,1,0):C.UVGC_44_17,(0,1,1):C.UVGC_44_18,(0,1,2):C.UVGC_44_19,(0,1,4):C.UVGC_44_20})

V_37 = CTVertex(name = 'V_37',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV6 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.t] ], [ [P.t] ] ],
                couplings = {(0,0,3):C.UVGC_27_5,(0,1,0):C.UVGC_44_17,(0,1,1):C.UVGC_44_18,(0,1,2):C.UVGC_44_19,(0,1,4):C.UVGC_44_20,(0,1,3):C.UVGC_65_51})

V_38 = CTVertex(name = 'V_38',
                type = 'UV',
                particles = [ P.u__tilde__, P.u ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF4 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_25_3})

V_39 = CTVertex(name = 'V_39',
                type = 'UV',
                particles = [ P.c__tilde__, P.c ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF4 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_25_3})

V_40 = CTVertex(name = 'V_40',
                type = 'UV',
                particles = [ P.d__tilde__, P.d ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF4 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_25_3})

V_41 = CTVertex(name = 'V_41',
                type = 'UV',
                particles = [ P.s__tilde__, P.s ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF4 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_25_3})

V_42 = CTVertex(name = 'V_42',
                type = 'UV',
                particles = [ P.b__tilde__, P.b ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF4 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_25_3})

V_43 = CTVertex(name = 'V_43',
                type = 'UV',
                particles = [ P.t__tilde__, P.t ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2, L.FF3 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_66_52,(0,1,0):C.UVGC_63_49})

V_44 = CTVertex(name = 'V_44',
                type = 'UV',
                particles = [ P.g, P.g ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VV1, L.VV5 ],
                loop_particles = [ [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,0,0):C.UVGC_38_7,(0,0,1):C.UVGC_38_8,(0,1,2):C.UVGC_55_27})

