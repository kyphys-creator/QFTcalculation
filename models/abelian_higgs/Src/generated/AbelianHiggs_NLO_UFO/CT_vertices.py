# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Tue 27 Oct 2026 19:37:02


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'R2',
               particles = [ P.G0, P.G0, P.G0, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.zp] ], [ [P.zp, P.h] ] ],
               couplings = {(0,0,0):C.R2GC_16_8,(0,0,1):C.R2GC_16_9})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.G0, P.G0, P.h, P.h ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.zp] ], [ [P.zp, P.G0, P.h] ], [ [P.zp, P.G0], [P.zp, P.h] ] ],
               couplings = {(0,0,0):C.R2GC_24_14,(0,0,2):C.R2GC_24_15,(0,0,1):C.R2GC_24_16})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.h, P.h, P.h, P.h ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.zp] ], [ [P.zp, P.G0] ] ],
               couplings = {(0,0,0):C.R2GC_16_8,(0,0,1):C.R2GC_16_9})

V_4 = CTVertex(name = 'V_4',
               type = 'R2',
               particles = [ P.G0, P.G0, P.h ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.zp] ], [ [P.zp, P.G0, P.h] ], [ [P.zp, P.h] ] ],
               couplings = {(0,0,0):C.R2GC_26_17,(0,0,2):C.R2GC_26_18,(0,0,1):C.R2GC_26_19})

V_5 = CTVertex(name = 'V_5',
               type = 'R2',
               particles = [ P.h, P.h, P.h ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.zp] ], [ [P.zp, P.G0] ] ],
               couplings = {(0,0,0):C.R2GC_19_10,(0,0,1):C.R2GC_19_11})

V_6 = CTVertex(name = 'V_6',
               type = 'R2',
               particles = [ P.zp, P.zp, P.G0, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               loop_particles = [ [ [P.zp, P.G0, P.h] ], [ [P.zp, P.h] ] ],
               couplings = {(0,0,1):C.R2GC_15_6,(0,0,0):C.R2GC_15_7})

V_7 = CTVertex(name = 'V_7',
               type = 'R2',
               particles = [ P.zp, P.zp, P.h, P.h ],
               color = [ '1' ],
               lorentz = [ L.VVSS1 ],
               loop_particles = [ [ [P.zp, P.G0] ], [ [P.zp, P.G0, P.h] ] ],
               couplings = {(0,0,0):C.R2GC_15_6,(0,0,1):C.R2GC_15_7})

V_8 = CTVertex(name = 'V_8',
               type = 'R2',
               particles = [ P.zp, P.G0, P.h ],
               color = [ '1' ],
               lorentz = [ L.VSS1, L.VSS2 ],
               loop_particles = [ [ [P.zp, P.G0, P.h] ] ],
               couplings = {(0,0,0):C.R2GC_22_13,(0,1,0):C.R2GC_21_12})

V_9 = CTVertex(name = 'V_9',
               type = 'R2',
               particles = [ P.h, P.h ],
               color = [ '1' ],
               lorentz = [ L.SS1, L.SS2 ],
               loop_particles = [ [ [P.zp] ], [ [P.zp, P.G0] ] ],
               couplings = {(0,0,0):C.R2GC_13_4,(0,0,1):C.R2GC_13_5,(0,1,1):C.R2GC_12_3})

V_10 = CTVertex(name = 'V_10',
                type = 'R2',
                particles = [ P.G0, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.SS1, L.SS2 ],
                loop_particles = [ [ [P.zp] ], [ [P.zp, P.h] ] ],
                couplings = {(0,0,0):C.R2GC_11_1,(0,0,1):C.R2GC_11_2,(0,1,1):C.R2GC_12_3})

V_11 = CTVertex(name = 'V_11',
                type = 'UV',
                particles = [ P.G0, P.G0, P.G0, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.SSSS1 ],
                loop_particles = [ [ [P.G0] ], [ [P.G0, P.h] ], [ [P.ghA] ], [ [P.h] ], [ [P.zp] ], [ [P.zp, P.G0] ], [ [P.zp, P.h] ] ],
                couplings = {(0,0,4):C.UVGC_25_84,(0,0,0):C.UVGC_25_85,(0,0,2):C.UVGC_25_86,(0,0,3):C.UVGC_25_87,(0,0,5):C.UVGC_25_88,(0,0,6):C.UVGC_25_89,(0,0,1):C.UVGC_25_90})

V_12 = CTVertex(name = 'V_12',
                type = 'UV',
                particles = [ P.G0, P.G0, P.h, P.h ],
                color = [ '1' ],
                lorentz = [ L.SSSS1 ],
                loop_particles = [ [ [P.G0] ], [ [P.G0, P.h] ], [ [P.ghA] ], [ [P.h] ], [ [P.zp] ], [ [P.zp, P.G0] ], [ [P.zp, P.G0, P.h] ], [ [P.zp, P.h] ] ],
                couplings = {(0,0,4):C.UVGC_24_76,(0,0,0):C.UVGC_24_77,(0,0,2):C.UVGC_24_78,(0,0,3):C.UVGC_24_79,(0,0,5):C.UVGC_24_80,(0,0,7):C.UVGC_24_81,(0,0,1):C.UVGC_24_82,(0,0,6):C.UVGC_24_83})

V_13 = CTVertex(name = 'V_13',
                type = 'UV',
                particles = [ P.h, P.h, P.h, P.h ],
                color = [ '1' ],
                lorentz = [ L.SSSS1 ],
                loop_particles = [ [ [P.G0] ], [ [P.G0, P.h] ], [ [P.ghA] ], [ [P.h] ], [ [P.zp] ], [ [P.zp, P.G0] ], [ [P.zp, P.h] ] ],
                couplings = {(0,0,4):C.UVGC_16_27,(0,0,0):C.UVGC_16_28,(0,0,2):C.UVGC_16_29,(0,0,3):C.UVGC_16_30,(0,0,5):C.UVGC_16_31,(0,0,6):C.UVGC_16_32,(0,0,1):C.UVGC_16_33})

V_14 = CTVertex(name = 'V_14',
                type = 'UV',
                particles = [ P.G0, P.G0, P.h ],
                color = [ '1' ],
                lorentz = [ L.SSS1 ],
                loop_particles = [ [ [P.G0] ], [ [P.G0, P.h] ], [ [P.ghA] ], [ [P.h] ], [ [P.zp] ], [ [P.zp, P.G0] ], [ [P.zp, P.G0, P.h] ], [ [P.zp, P.h] ] ],
                couplings = {(0,0,4):C.UVGC_26_91,(0,0,0):C.UVGC_26_92,(0,0,2):C.UVGC_26_93,(0,0,3):C.UVGC_26_94,(0,0,5):C.UVGC_26_95,(0,0,7):C.UVGC_26_96,(0,0,1):C.UVGC_26_97,(0,0,6):C.UVGC_26_98})

V_15 = CTVertex(name = 'V_15',
                type = 'UV',
                particles = [ P.h, P.h, P.h ],
                color = [ '1' ],
                lorentz = [ L.SSS1 ],
                loop_particles = [ [ [P.G0] ], [ [P.G0, P.h] ], [ [P.ghA] ], [ [P.h] ], [ [P.zp] ], [ [P.zp, P.G0] ], [ [P.zp, P.h] ] ],
                couplings = {(0,0,4):C.UVGC_19_46,(0,0,0):C.UVGC_19_47,(0,0,2):C.UVGC_19_48,(0,0,3):C.UVGC_19_49,(0,0,5):C.UVGC_19_50,(0,0,6):C.UVGC_19_51,(0,0,1):C.UVGC_19_52})

V_16 = CTVertex(name = 'V_16',
                type = 'UV',
                particles = [ P.zp, P.zp, P.G0, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.G0] ], [ [P.G0, P.h] ], [ [P.h] ], [ [P.zp, P.G0] ], [ [P.zp, P.G0, P.h] ], [ [P.zp, P.h] ] ],
                couplings = {(0,0,0):C.UVGC_23_71,(0,0,2):C.UVGC_23_72,(0,0,3):C.UVGC_23_73,(0,0,5):C.UVGC_23_74,(0,0,1):C.UVGC_23_75,(0,0,4):C.UVGC_10_1})

V_17 = CTVertex(name = 'V_17',
                type = 'UV',
                particles = [ P.zp, P.zp, P.h, P.h ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.G0] ], [ [P.G0, P.h] ], [ [P.ghA] ], [ [P.h] ], [ [P.zp] ], [ [P.zp, P.G0] ], [ [P.zp, P.G0, P.h] ], [ [P.zp, P.h] ] ],
                couplings = {(0,0,4):C.UVGC_15_20,(0,0,0):C.UVGC_15_21,(0,0,2):C.UVGC_15_22,(0,0,3):C.UVGC_15_23,(0,0,5):C.UVGC_15_24,(0,0,7):C.UVGC_15_25,(0,0,1):C.UVGC_15_26,(0,0,6):C.UVGC_10_1})

V_18 = CTVertex(name = 'V_18',
                type = 'UV',
                particles = [ P.zp, P.zp, P.h ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.G0] ], [ [P.G0, P.h] ], [ [P.ghA] ], [ [P.h] ], [ [P.zp] ], [ [P.zp, P.G0] ], [ [P.zp, P.G0, P.h] ], [ [P.zp, P.h] ] ],
                couplings = {(0,0,4):C.UVGC_18_38,(0,0,0):C.UVGC_18_39,(0,0,2):C.UVGC_18_40,(0,0,3):C.UVGC_18_41,(0,0,5):C.UVGC_18_42,(0,0,7):C.UVGC_18_43,(0,0,1):C.UVGC_18_44,(0,0,6):C.UVGC_18_45})

V_19 = CTVertex(name = 'V_19',
                type = 'UV',
                particles = [ P.zp, P.G0, P.h ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS2 ],
                loop_particles = [ [ [P.G0] ], [ [P.G0, P.h] ], [ [P.ghA] ], [ [P.h] ], [ [P.zp] ], [ [P.zp, P.G0] ], [ [P.zp, P.G0, P.h] ], [ [P.zp, P.h] ] ],
                couplings = {(0,0,4):C.UVGC_22_63,(0,0,0):C.UVGC_22_64,(0,0,2):C.UVGC_22_65,(0,0,3):C.UVGC_22_66,(0,0,5):C.UVGC_22_67,(0,0,7):C.UVGC_22_68,(0,0,1):C.UVGC_22_69,(0,0,6):C.UVGC_22_70,(0,1,4):C.UVGC_21_55,(0,1,0):C.UVGC_21_56,(0,1,2):C.UVGC_21_57,(0,1,3):C.UVGC_21_58,(0,1,5):C.UVGC_21_59,(0,1,7):C.UVGC_21_60,(0,1,1):C.UVGC_21_61,(0,1,6):C.UVGC_21_62})

V_20 = CTVertex(name = 'V_20',
                type = 'UV',
                particles = [ P.h, P.h ],
                color = [ '1' ],
                lorentz = [ L.SS1, L.SS2 ],
                loop_particles = [ [ [P.G0] ], [ [P.ghA] ], [ [P.h] ], [ [P.zp] ], [ [P.zp, P.G0] ] ],
                couplings = {(0,0,3):C.UVGC_13_13,(0,0,0):C.UVGC_13_14,(0,0,1):C.UVGC_13_15,(0,0,2):C.UVGC_13_16,(0,0,4):C.UVGC_13_17,(0,1,3):C.UVGC_12_8,(0,1,0):C.UVGC_12_9,(0,1,1):C.UVGC_12_10,(0,1,2):C.UVGC_12_11,(0,1,4):C.UVGC_12_12})

V_21 = CTVertex(name = 'V_21',
                type = 'UV',
                particles = [ P.G0, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.SS1, L.SS2 ],
                loop_particles = [ [ [P.G0] ], [ [P.G0, P.h] ], [ [P.h] ], [ [P.zp] ], [ [P.zp, P.h] ] ],
                couplings = {(0,0,3):C.UVGC_11_3,(0,0,0):C.UVGC_11_4,(0,0,2):C.UVGC_11_5,(0,0,4):C.UVGC_11_6,(0,0,1):C.UVGC_11_7,(0,1,4):C.UVGC_20_53,(0,1,1):C.UVGC_20_54})

V_22 = CTVertex(name = 'V_22',
                type = 'UV',
                particles = [ P.zp, P.zp ],
                color = [ '1' ],
                lorentz = [ L.VV1, L.VV2 ],
                loop_particles = [ [ [P.G0] ], [ [P.G0, P.h] ], [ [P.h] ], [ [P.zp, P.h] ] ],
                couplings = {(0,1,3):C.UVGC_14_18,(0,1,1):C.UVGC_14_19,(0,0,0):C.UVGC_17_34,(0,0,2):C.UVGC_17_35,(0,0,3):C.UVGC_17_36,(0,0,1):C.UVGC_17_37})

V_23 = CTVertex(name = 'V_23',
                type = 'UV',
                particles = [ P.zp, P.zp, P.zp, P.zp ],
                color = [ '1' ],
                lorentz = [ L.VVVV1 ],
                loop_particles = [ [ [P.G0], [P.h] ], [ [P.G0, P.h] ] ],
                couplings = {(0,0,0):C.UVGC_10_1,(0,0,1):C.UVGC_10_2})

