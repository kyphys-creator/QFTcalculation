# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Fri 16 Oct 2026 22:08:07


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'R2',
               particles = [ P.G0, P.G0, P.G0, P.G0 ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_252_343,(0,0,1):C.R2GC_252_344,(0,0,2):C.R2GC_252_345,(0,0,3):C.R2GC_252_346,(0,0,6):C.R2GC_252_347,(0,0,7):C.R2GC_252_348,(0,0,8):C.R2GC_252_349,(0,0,9):C.R2GC_252_350,(0,0,10):C.R2GC_252_351,(0,0,11):C.R2GC_252_352,(0,0,12):C.R2GC_252_353,(0,0,4):C.R2GC_252_354,(0,0,5):C.R2GC_252_355})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.G0, P.G0, P.G__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
               couplings = {(0,0,20):C.R2GC_248_298,(0,0,22):C.R2GC_248_299,(0,0,0):C.R2GC_248_300,(0,0,2):C.R2GC_163_126,(0,0,3):C.R2GC_248_301,(0,0,4):C.R2GC_248_302,(0,0,5):C.R2GC_248_303,(0,0,6):C.R2GC_248_304,(0,0,8):C.R2GC_248_305,(0,0,12):C.R2GC_248_306,(0,0,14):C.R2GC_248_307,(0,0,15):C.R2GC_248_308,(0,0,17):C.R2GC_248_309,(0,0,18):C.R2GC_248_310,(0,0,19):C.R2GC_248_311,(0,0,21):C.R2GC_248_312,(0,0,1):C.R2GC_248_313,(0,0,7):C.R2GC_248_314,(0,0,9):C.R2GC_248_315,(0,0,11):C.R2GC_248_316,(0,0,13):C.R2GC_248_317,(0,0,16):C.R2GC_248_318,(0,0,10):C.R2GC_248_319})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.G__minus__, P.G__minus__, P.G__plus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.a] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_251_330,(0,0,12):C.R2GC_251_331,(0,0,13):C.R2GC_251_332,(0,0,1):C.R2GC_251_333,(0,0,3):C.R2GC_251_334,(0,0,4):C.R2GC_251_335,(0,0,5):C.R2GC_251_336,(0,0,6):C.R2GC_251_337,(0,0,7):C.R2GC_251_338,(0,0,8):C.R2GC_249_328,(0,0,9):C.R2GC_251_339,(0,0,10):C.R2GC_251_340,(0,0,11):C.R2GC_251_341,(0,0,2):C.R2GC_251_342})

V_4 = CTVertex(name = 'V_4',
               type = 'R2',
               particles = [ P.G0, P.G0, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.Z], [P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_249_320,(0,0,1):C.R2GC_249_321,(0,0,2):C.R2GC_249_322,(0,0,3):C.R2GC_248_304,(0,0,7):C.R2GC_248_310,(0,0,8):C.R2GC_249_323,(0,0,9):C.R2GC_249_324,(0,0,10):C.R2GC_248_311,(0,0,11):C.R2GC_249_325,(0,0,12):C.R2GC_248_298,(0,0,13):C.R2GC_249_326,(0,0,5):C.R2GC_249_327,(0,0,6):C.R2GC_249_328,(0,0,4):C.R2GC_249_329})

V_5 = CTVertex(name = 'V_5',
               type = 'R2',
               particles = [ P.G__minus__, P.G__plus__, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__, P.Z] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
               couplings = {(0,0,20):C.R2GC_248_298,(0,0,22):C.R2GC_248_299,(0,0,0):C.R2GC_248_300,(0,0,2):C.R2GC_163_126,(0,0,3):C.R2GC_248_301,(0,0,4):C.R2GC_248_302,(0,0,5):C.R2GC_248_303,(0,0,6):C.R2GC_248_304,(0,0,10):C.R2GC_248_308,(0,0,12):C.R2GC_248_309,(0,0,14):C.R2GC_248_306,(0,0,16):C.R2GC_248_307,(0,0,17):C.R2GC_248_305,(0,0,18):C.R2GC_248_310,(0,0,19):C.R2GC_248_311,(0,0,21):C.R2GC_248_312,(0,0,1):C.R2GC_248_313,(0,0,7):C.R2GC_248_315,(0,0,9):C.R2GC_248_316,(0,0,11):C.R2GC_248_318,(0,0,13):C.R2GC_248_314,(0,0,15):C.R2GC_248_317,(0,0,8):C.R2GC_248_319})

V_6 = CTVertex(name = 'V_6',
               type = 'R2',
               particles = [ P.H, P.H, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_252_343,(0,0,1):C.R2GC_252_344,(0,0,2):C.R2GC_252_345,(0,0,3):C.R2GC_252_346,(0,0,6):C.R2GC_252_347,(0,0,7):C.R2GC_252_348,(0,0,8):C.R2GC_252_349,(0,0,9):C.R2GC_252_350,(0,0,10):C.R2GC_252_351,(0,0,11):C.R2GC_252_352,(0,0,12):C.R2GC_252_353,(0,0,4):C.R2GC_252_355,(0,0,5):C.R2GC_252_354})

V_7 = CTVertex(name = 'V_7',
               type = 'R2',
               particles = [ P.G0, P.G0, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_360_814,(0,0,1):C.R2GC_360_815,(0,0,2):C.R2GC_360_816,(0,0,3):C.R2GC_360_817,(0,0,7):C.R2GC_360_818,(0,0,8):C.R2GC_360_819,(0,0,9):C.R2GC_360_820,(0,0,10):C.R2GC_360_821,(0,0,11):C.R2GC_360_822,(0,0,12):C.R2GC_360_823,(0,0,13):C.R2GC_360_824,(0,0,5):C.R2GC_360_825,(0,0,6):C.R2GC_360_826,(0,0,4):C.R2GC_360_827})

V_8 = CTVertex(name = 'V_8',
               type = 'R2',
               particles = [ P.G__minus__, P.G__plus__, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
               couplings = {(0,0,15):C.R2GC_360_823,(0,0,17):C.R2GC_361_828,(0,0,0):C.R2GC_361_829,(0,0,2):C.R2GC_164_137,(0,0,3):C.R2GC_361_830,(0,0,4):C.R2GC_361_831,(0,0,5):C.R2GC_361_832,(0,0,6):C.R2GC_360_817,(0,0,7):C.R2GC_361_833,(0,0,11):C.R2GC_361_834,(0,0,12):C.R2GC_361_835,(0,0,13):C.R2GC_360_818,(0,0,14):C.R2GC_360_821,(0,0,16):C.R2GC_361_836,(0,0,1):C.R2GC_361_837,(0,0,8):C.R2GC_361_838,(0,0,9):C.R2GC_361_839,(0,0,10):C.R2GC_361_840})

V_9 = CTVertex(name = 'V_9',
               type = 'R2',
               particles = [ P.H, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_362_841,(0,0,1):C.R2GC_362_842,(0,0,2):C.R2GC_362_843,(0,0,3):C.R2GC_362_844,(0,0,6):C.R2GC_362_845,(0,0,7):C.R2GC_362_846,(0,0,8):C.R2GC_362_847,(0,0,9):C.R2GC_362_848,(0,0,10):C.R2GC_362_849,(0,0,11):C.R2GC_362_850,(0,0,12):C.R2GC_362_851,(0,0,4):C.R2GC_362_852,(0,0,5):C.R2GC_362_853})

V_10 = CTVertex(name = 'V_10',
                type = 'R2',
                particles = [ P.a, P.a, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,9):C.R2GC_163_126,(0,0,0):C.R2GC_322_636,(0,0,1):C.R2GC_322_637,(0,0,2):C.R2GC_322_638,(0,0,3):C.R2GC_322_639,(0,0,4):C.R2GC_322_640,(0,0,5):C.R2GC_322_641,(0,0,6):C.R2GC_322_642,(0,0,7):C.R2GC_322_643,(0,0,8):C.R2GC_322_644})

V_11 = CTVertex(name = 'V_11',
                type = 'R2',
                particles = [ P.a, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,0):C.R2GC_309_614,(0,0,1):C.R2GC_309_615,(0,0,2):C.R2GC_309_616,(0,0,3):C.R2GC_309_617,(0,0,4):C.R2GC_309_618,(0,0,5):C.R2GC_309_619,(0,0,6):C.R2GC_309_620,(0,0,7):C.R2GC_309_621,(0,0,8):C.R2GC_309_622})

V_12 = CTVertex(name = 'V_12',
                type = 'R2',
                particles = [ P.g, P.g, P.g ],
                color = [ 'f(1,2,3)' ],
                lorentz = [ L.VVV7 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
                couplings = {(0,0,0):C.R2GC_221_247,(0,0,1):C.R2GC_221_248})

V_13 = CTVertex(name = 'V_13',
                type = 'R2',
                particles = [ P.g, P.g, P.g, P.g ],
                color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5, L.VVVV8 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
                couplings = {(2,0,0):C.R2GC_130_24,(2,0,1):C.R2GC_130_25,(0,0,0):C.R2GC_130_24,(0,0,1):C.R2GC_130_25,(4,0,0):C.R2GC_125_16,(4,0,1):C.R2GC_125_17,(3,0,0):C.R2GC_125_16,(3,0,1):C.R2GC_125_17,(8,0,0):C.R2GC_127_20,(8,0,1):C.R2GC_127_21,(6,0,0):C.R2GC_133_29,(6,0,1):C.R2GC_133_30,(7,0,0):C.R2GC_131_26,(7,0,1):C.R2GC_131_27,(5,0,0):C.R2GC_125_16,(5,0,1):C.R2GC_125_17,(1,0,0):C.R2GC_125_16,(1,0,1):C.R2GC_125_17,(11,3,0):C.R2GC_126_18,(11,3,1):C.R2GC_126_19,(10,3,0):C.R2GC_126_18,(10,3,1):C.R2GC_126_19,(9,3,1):C.R2GC_111_2,(0,1,0):C.R2GC_130_24,(0,1,1):C.R2GC_130_25,(2,1,0):C.R2GC_130_24,(2,1,1):C.R2GC_130_25,(5,1,0):C.R2GC_125_16,(5,1,1):C.R2GC_125_17,(1,1,0):C.R2GC_125_16,(1,1,1):C.R2GC_125_17,(7,1,0):C.R2GC_131_26,(7,1,1):C.R2GC_132_28,(4,1,0):C.R2GC_125_16,(4,1,1):C.R2GC_125_17,(3,1,0):C.R2GC_125_16,(3,1,1):C.R2GC_125_17,(8,1,0):C.R2GC_127_20,(8,1,1):C.R2GC_128_22,(6,1,0):C.R2GC_135_32,(6,1,1):C.R2GC_135_33,(0,2,0):C.R2GC_130_24,(0,2,1):C.R2GC_130_25,(2,2,0):C.R2GC_130_24,(2,2,1):C.R2GC_130_25,(5,2,0):C.R2GC_125_16,(5,2,1):C.R2GC_125_17,(1,2,0):C.R2GC_125_16,(1,2,1):C.R2GC_125_17,(7,2,0):C.R2GC_136_34,(7,2,1):C.R2GC_130_25,(4,2,0):C.R2GC_125_16,(4,2,1):C.R2GC_125_17,(3,2,0):C.R2GC_125_16,(3,2,1):C.R2GC_125_17,(8,2,0):C.R2GC_127_20,(8,2,1):C.R2GC_129_23,(6,2,0):C.R2GC_133_29,(6,2,1):C.R2GC_134_31})

V_14 = CTVertex(name = 'V_14',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.G0, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_283_549,(0,0,2):C.R2GC_283_550,(0,0,3):C.R2GC_283_551,(0,0,4):C.R2GC_283_552,(0,0,5):C.R2GC_283_553,(0,0,7):C.R2GC_283_554,(0,0,10):C.R2GC_283_555,(0,0,13):C.R2GC_283_556,(0,0,14):C.R2GC_283_557,(0,0,15):C.R2GC_283_558,(0,0,0):C.R2GC_283_559,(0,0,6):C.R2GC_283_560,(0,0,8):C.R2GC_283_561,(0,0,9):C.R2GC_283_562,(0,0,11):C.R2GC_283_563,(0,0,12):C.R2GC_283_564})

V_15 = CTVertex(name = 'V_15',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.G__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_282_542,(0,0,2):C.R2GC_284_565,(0,0,3):C.R2GC_284_566,(0,0,4):C.R2GC_284_567,(0,0,5):C.R2GC_284_568,(0,0,10):C.R2GC_282_539,(0,0,12):C.R2GC_282_538,(0,0,13):C.R2GC_284_569,(0,0,14):C.R2GC_284_570,(0,0,15):C.R2GC_282_533,(0,0,0):C.R2GC_284_571,(0,0,6):C.R2GC_282_547,(0,0,7):C.R2GC_284_572,(0,0,8):C.R2GC_284_573,(0,0,9):C.R2GC_282_544,(0,0,11):C.R2GC_284_574})

V_16 = CTVertex(name = 'V_16',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_365_875,(0,0,2):C.R2GC_365_876,(0,0,3):C.R2GC_365_877,(0,0,4):C.R2GC_365_878,(0,0,6):C.R2GC_365_879,(0,0,7):C.R2GC_365_880,(0,0,0):C.R2GC_365_881,(0,0,5):C.R2GC_365_882})

V_17 = CTVertex(name = 'V_17',
                type = 'R2',
                particles = [ P.W__minus__, P.G0, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_273_490,(0,0,2):C.R2GC_273_491,(0,0,3):C.R2GC_273_492,(0,0,4):C.R2GC_273_493,(0,0,10):C.R2GC_273_494,(0,0,11):C.R2GC_273_495,(0,0,0):C.R2GC_273_496,(0,0,5):C.R2GC_273_497,(0,0,6):C.R2GC_273_498,(0,0,7):C.R2GC_273_499,(0,0,8):C.R2GC_273_500,(0,0,9):C.R2GC_273_501})

V_18 = CTVertex(name = 'V_18',
                type = 'R2',
                particles = [ P.W__minus__, P.G__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_275_512,(0,0,2):C.R2GC_275_513,(0,0,3):C.R2GC_275_514,(0,0,4):C.R2GC_275_515,(0,0,10):C.R2GC_275_516,(0,0,11):C.R2GC_275_517,(0,0,0):C.R2GC_275_518,(0,0,5):C.R2GC_272_488,(0,0,6):C.R2GC_275_519,(0,0,7):C.R2GC_275_520,(0,0,8):C.R2GC_272_485,(0,0,9):C.R2GC_275_521})

V_19 = CTVertex(name = 'V_19',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVV1, L.VVV2, L.VVV3, L.VVV4, L.VVV5, L.VVV6 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_266_456,(0,0,1):C.R2GC_266_457,(0,0,2):C.R2GC_266_458,(0,0,3):C.R2GC_266_459,(0,1,0):C.R2GC_264_452,(0,1,1):C.R2GC_264_453,(0,1,2):C.R2GC_264_454,(0,1,3):C.R2GC_264_455,(0,2,0):C.R2GC_264_452,(0,2,1):C.R2GC_264_453,(0,2,2):C.R2GC_264_454,(0,2,3):C.R2GC_264_455,(0,3,0):C.R2GC_266_456,(0,3,1):C.R2GC_266_457,(0,3,2):C.R2GC_266_458,(0,3,3):C.R2GC_266_459,(0,4,0):C.R2GC_266_456,(0,4,1):C.R2GC_266_457,(0,4,2):C.R2GC_266_458,(0,4,3):C.R2GC_266_459,(0,5,0):C.R2GC_264_452,(0,5,1):C.R2GC_264_453,(0,5,2):C.R2GC_264_454,(0,5,3):C.R2GC_264_455})

V_20 = CTVertex(name = 'V_20',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_283_549,(0,0,2):C.R2GC_283_550,(0,0,3):C.R2GC_283_551,(0,0,4):C.R2GC_283_552,(0,0,5):C.R2GC_283_553,(0,0,7):C.R2GC_283_554,(0,0,10):C.R2GC_283_555,(0,0,13):C.R2GC_283_556,(0,0,14):C.R2GC_283_557,(0,0,15):C.R2GC_283_558,(0,0,0):C.R2GC_283_559,(0,0,6):C.R2GC_283_560,(0,0,8):C.R2GC_283_561,(0,0,9):C.R2GC_283_562,(0,0,11):C.R2GC_283_563,(0,0,12):C.R2GC_283_564})

V_21 = CTVertex(name = 'V_21',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_282_533,(0,0,2):C.R2GC_282_534,(0,0,3):C.R2GC_282_535,(0,0,4):C.R2GC_282_536,(0,0,5):C.R2GC_282_537,(0,0,10):C.R2GC_282_538,(0,0,12):C.R2GC_282_539,(0,0,13):C.R2GC_282_540,(0,0,14):C.R2GC_282_541,(0,0,15):C.R2GC_282_542,(0,0,0):C.R2GC_282_543,(0,0,6):C.R2GC_282_544,(0,0,7):C.R2GC_282_545,(0,0,8):C.R2GC_282_546,(0,0,9):C.R2GC_282_547,(0,0,11):C.R2GC_282_548})

V_22 = CTVertex(name = 'V_22',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_365_880,(0,0,2):C.R2GC_366_883,(0,0,3):C.R2GC_366_884,(0,0,4):C.R2GC_366_885,(0,0,6):C.R2GC_366_886,(0,0,7):C.R2GC_365_875,(0,0,0):C.R2GC_366_887,(0,0,5):C.R2GC_366_888})

V_23 = CTVertex(name = 'V_23',
                type = 'R2',
                particles = [ P.W__plus__, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS3 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_274_502,(0,0,2):C.R2GC_274_503,(0,0,3):C.R2GC_274_504,(0,0,4):C.R2GC_274_505,(0,0,10):C.R2GC_274_506,(0,0,11):C.R2GC_274_507,(0,0,0):C.R2GC_274_508,(0,0,5):C.R2GC_273_498,(0,0,6):C.R2GC_273_497,(0,0,7):C.R2GC_274_509,(0,0,8):C.R2GC_274_510,(0,0,9):C.R2GC_274_511,(0,1,1):C.R2GC_273_490,(0,1,2):C.R2GC_273_491,(0,1,3):C.R2GC_273_492,(0,1,4):C.R2GC_273_493,(0,1,10):C.R2GC_273_494,(0,1,11):C.R2GC_273_495,(0,1,0):C.R2GC_273_496,(0,1,5):C.R2GC_273_497,(0,1,6):C.R2GC_273_498,(0,1,7):C.R2GC_273_499,(0,1,8):C.R2GC_273_500,(0,1,9):C.R2GC_273_501})

V_24 = CTVertex(name = 'V_24',
                type = 'R2',
                particles = [ P.W__plus__, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS3 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_275_512,(0,0,2):C.R2GC_275_513,(0,0,3):C.R2GC_275_514,(0,0,4):C.R2GC_275_515,(0,0,10):C.R2GC_275_516,(0,0,11):C.R2GC_275_517,(0,0,0):C.R2GC_275_518,(0,0,5):C.R2GC_272_488,(0,0,6):C.R2GC_275_519,(0,0,7):C.R2GC_275_520,(0,0,8):C.R2GC_272_485,(0,0,9):C.R2GC_275_521,(0,1,1):C.R2GC_272_478,(0,1,2):C.R2GC_272_479,(0,1,3):C.R2GC_272_480,(0,1,4):C.R2GC_272_481,(0,1,10):C.R2GC_272_482,(0,1,11):C.R2GC_272_483,(0,1,0):C.R2GC_272_484,(0,1,5):C.R2GC_272_485,(0,1,6):C.R2GC_272_486,(0,1,7):C.R2GC_272_487,(0,1,8):C.R2GC_272_488,(0,1,9):C.R2GC_272_489})

V_25 = CTVertex(name = 'V_25',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.G0, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__], [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,14):C.R2GC_254_356,(0,0,16):C.R2GC_254_357,(0,0,1):C.R2GC_254_358,(0,0,2):C.R2GC_254_359,(0,0,3):C.R2GC_254_360,(0,0,4):C.R2GC_254_361,(0,0,5):C.R2GC_254_362,(0,0,8):C.R2GC_254_363,(0,0,11):C.R2GC_254_364,(0,0,12):C.R2GC_254_365,(0,0,13):C.R2GC_254_366,(0,0,15):C.R2GC_254_367,(0,0,0):C.R2GC_254_368,(0,0,6):C.R2GC_254_369,(0,0,7):C.R2GC_254_370,(0,0,9):C.R2GC_254_371,(0,0,10):C.R2GC_254_372})

V_26 = CTVertex(name = 'V_26',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a] ], [ [P.a, P.G0, P.G__plus__], [P.a, P.G__plus__, P.H] ], [ [P.a, P.G0, P.W__plus__], [P.a, P.H, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.G__plus__, P.W__plus__, P.Z] ], [ [P.a, P.G__plus__, P.Z] ], [ [P.a, P.W__plus__] ], [ [P.a, P.W__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__], [P.G__plus__, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z], [P.G__plus__, P.H, P.Z] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z], [P.H, P.W__plus__, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_255_373,(0,0,22):C.R2GC_254_356,(0,0,24):C.R2GC_255_374,(0,0,3):C.R2GC_255_375,(0,0,7):C.R2GC_255_376,(0,0,9):C.R2GC_255_377,(0,0,10):C.R2GC_254_359,(0,0,11):C.R2GC_254_360,(0,0,12):C.R2GC_254_361,(0,0,13):C.R2GC_254_362,(0,0,16):C.R2GC_255_378,(0,0,19):C.R2GC_255_379,(0,0,20):C.R2GC_254_365,(0,0,21):C.R2GC_254_366,(0,0,23):C.R2GC_255_380,(0,0,1):C.R2GC_248_313,(0,0,2):C.R2GC_255_381,(0,0,4):C.R2GC_255_382,(0,0,6):C.R2GC_255_383,(0,0,8):C.R2GC_255_384,(0,0,14):C.R2GC_254_369,(0,0,15):C.R2GC_255_385,(0,0,17):C.R2GC_255_386,(0,0,18):C.R2GC_255_387,(0,0,5):C.R2GC_255_388})

V_27 = CTVertex(name = 'V_27',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.H, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__], [P.G__plus__, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,14):C.R2GC_254_356,(0,0,16):C.R2GC_254_357,(0,0,1):C.R2GC_254_358,(0,0,2):C.R2GC_254_359,(0,0,3):C.R2GC_254_360,(0,0,4):C.R2GC_254_361,(0,0,5):C.R2GC_254_362,(0,0,9):C.R2GC_254_364,(0,0,10):C.R2GC_254_363,(0,0,12):C.R2GC_254_365,(0,0,13):C.R2GC_254_366,(0,0,15):C.R2GC_254_367,(0,0,0):C.R2GC_254_368,(0,0,6):C.R2GC_254_369,(0,0,7):C.R2GC_254_370,(0,0,8):C.R2GC_254_372,(0,0,11):C.R2GC_254_371})

V_28 = CTVertex(name = 'V_28',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,9):C.R2GC_364_864,(0,0,11):C.R2GC_364_865,(0,0,1):C.R2GC_364_866,(0,0,2):C.R2GC_364_867,(0,0,3):C.R2GC_364_868,(0,0,4):C.R2GC_364_869,(0,0,5):C.R2GC_364_870,(0,0,7):C.R2GC_364_871,(0,0,8):C.R2GC_364_872,(0,0,10):C.R2GC_364_873,(0,0,0):C.R2GC_364_874,(0,0,6):C.R2GC_361_837})

V_29 = CTVertex(name = 'V_29',
                type = 'R2',
                particles = [ P.a, P.a, P.W__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,3):C.R2GC_267_460,(0,0,0):C.R2GC_267_461,(0,0,1):C.R2GC_267_462,(0,0,2):C.R2GC_267_463,(0,0,4):C.R2GC_267_464,(0,1,3):C.R2GC_267_460,(0,1,0):C.R2GC_267_461,(0,1,1):C.R2GC_267_462,(0,1,2):C.R2GC_267_463,(0,1,4):C.R2GC_267_464,(0,2,3):C.R2GC_268_465,(0,2,0):C.R2GC_268_466,(0,2,1):C.R2GC_268_467,(0,2,2):C.R2GC_268_468,(0,2,4):C.R2GC_268_469})

V_30 = CTVertex(name = 'V_30',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVV1, L.VVV2, L.VVV3, L.VVV4, L.VVV5, L.VVV6 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_287_575,(0,0,1):C.R2GC_287_576,(0,0,2):C.R2GC_287_577,(0,0,3):C.R2GC_287_578,(0,1,0):C.R2GC_290_579,(0,1,1):C.R2GC_290_580,(0,1,2):C.R2GC_290_581,(0,1,3):C.R2GC_290_582,(0,2,0):C.R2GC_290_579,(0,2,1):C.R2GC_290_580,(0,2,2):C.R2GC_290_581,(0,2,3):C.R2GC_290_582,(0,3,0):C.R2GC_287_575,(0,3,1):C.R2GC_287_576,(0,3,2):C.R2GC_287_577,(0,3,3):C.R2GC_287_578,(0,4,0):C.R2GC_287_575,(0,4,1):C.R2GC_287_576,(0,4,2):C.R2GC_287_577,(0,4,3):C.R2GC_287_578,(0,5,0):C.R2GC_290_579,(0,5,1):C.R2GC_290_580,(0,5,2):C.R2GC_290_581,(0,5,3):C.R2GC_290_582})

V_31 = CTVertex(name = 'V_31',
                type = 'R2',
                particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.a] ], [ [P.a, P.W__plus__] ], [ [P.a, P.W__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_257_389,(0,0,6):C.R2GC_257_390,(0,0,8):C.R2GC_257_391,(0,0,1):C.R2GC_257_392,(0,0,3):C.R2GC_257_393,(0,0,4):C.R2GC_257_394,(0,0,5):C.R2GC_257_395,(0,0,7):C.R2GC_257_396,(0,0,2):C.R2GC_257_397,(0,1,0):C.R2GC_257_389,(0,1,6):C.R2GC_257_390,(0,1,8):C.R2GC_257_391,(0,1,1):C.R2GC_257_392,(0,1,3):C.R2GC_257_393,(0,1,4):C.R2GC_257_394,(0,1,5):C.R2GC_257_395,(0,1,7):C.R2GC_257_396,(0,1,2):C.R2GC_257_397,(0,2,6):C.R2GC_258_398,(0,2,1):C.R2GC_258_399,(0,2,4):C.R2GC_258_400,(0,2,5):C.R2GC_258_401,(0,2,7):C.R2GC_258_402,(0,2,2):C.R2GC_258_403})

V_32 = CTVertex(name = 'V_32',
                type = 'R2',
                particles = [ P.u__tilde__, P.d, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.d, P.G0, P.u], [P.d, P.H, P.u] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_381_998,(0,0,1):C.R2GC_381_999,(0,0,2):C.R2GC_381_1000,(0,0,6):C.R2GC_381_1001,(0,0,3):C.R2GC_381_1002,(0,0,4):C.R2GC_381_1003,(0,0,5):C.R2GC_381_1004,(0,0,7):C.R2GC_381_1005,(0,0,9):C.R2GC_381_1006,(0,1,0):C.R2GC_404_1115,(0,1,1):C.R2GC_404_1116,(0,1,2):C.R2GC_404_1117,(0,1,6):C.R2GC_404_1118,(0,1,3):C.R2GC_404_1119,(0,1,5):C.R2GC_404_1120,(0,1,7):C.R2GC_404_1121,(0,1,8):C.R2GC_404_1122,(0,1,9):C.R2GC_404_1123})

V_33 = CTVertex(name = 'V_33',
                type = 'R2',
                particles = [ P.c__tilde__, P.s, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.c, P.s] ], [ [P.a, P.G__plus__, P.s] ], [ [P.c, P.G0, P.s], [P.c, P.H, P.s] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.c, P.g, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_393_1056,(0,0,1):C.R2GC_393_1057,(0,0,2):C.R2GC_393_1058,(0,0,6):C.R2GC_393_1059,(0,0,3):C.R2GC_393_1060,(0,0,5):C.R2GC_393_1061,(0,0,7):C.R2GC_393_1062,(0,0,8):C.R2GC_393_1063,(0,0,9):C.R2GC_393_1064,(0,1,0):C.R2GC_376_963,(0,1,1):C.R2GC_376_964,(0,1,2):C.R2GC_376_965,(0,1,6):C.R2GC_376_966,(0,1,3):C.R2GC_376_967,(0,1,4):C.R2GC_376_968,(0,1,5):C.R2GC_376_969,(0,1,7):C.R2GC_376_970,(0,1,9):C.R2GC_376_971})

V_34 = CTVertex(name = 'V_34',
                type = 'R2',
                particles = [ P.t__tilde__, P.b, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.b, P.G0, P.t], [P.b, P.H, P.t] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_373_946,(0,0,1):C.R2GC_373_947,(0,0,2):C.R2GC_373_948,(0,0,6):C.R2GC_373_949,(0,0,3):C.R2GC_373_950,(0,0,4):C.R2GC_373_951,(0,0,5):C.R2GC_373_952,(0,0,7):C.R2GC_373_953,(0,0,9):C.R2GC_373_954,(0,1,0):C.R2GC_396_1073,(0,1,1):C.R2GC_396_1074,(0,1,2):C.R2GC_396_1075,(0,1,6):C.R2GC_396_1076,(0,1,3):C.R2GC_396_1077,(0,1,5):C.R2GC_396_1078,(0,1,7):C.R2GC_396_1079,(0,1,8):C.R2GC_396_1080,(0,1,9):C.R2GC_396_1081})

V_35 = CTVertex(name = 'V_35',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.H] ], [ [P.d, P.H, P.Z] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_383_1007,(0,0,1):C.R2GC_383_1008,(0,0,2):C.R2GC_383_1009,(0,0,3):C.R2GC_383_1010,(0,0,5):C.R2GC_383_1011,(0,0,6):C.R2GC_383_1012,(0,0,4):C.R2GC_383_1013,(0,0,7):C.R2GC_383_1014})

V_36 = CTVertex(name = 'V_36',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G0, P.s] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.H, P.s, P.Z] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_395_1065,(0,0,1):C.R2GC_395_1066,(0,0,4):C.R2GC_395_1067,(0,0,3):C.R2GC_395_1068,(0,0,5):C.R2GC_395_1069,(0,0,7):C.R2GC_395_1070,(0,0,2):C.R2GC_395_1071,(0,0,6):C.R2GC_395_1072})

V_37 = CTVertex(name = 'V_37',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.H] ], [ [P.b, P.H, P.Z] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_375_955,(0,0,1):C.R2GC_375_956,(0,0,2):C.R2GC_375_957,(0,0,3):C.R2GC_375_958,(0,0,5):C.R2GC_375_959,(0,0,6):C.R2GC_375_960,(0,0,4):C.R2GC_375_961,(0,0,7):C.R2GC_375_962})

V_38 = CTVertex(name = 'V_38',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.G0, P.Z] ], [ [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_176_194,(0,0,1):C.R2GC_176_195,(0,0,2):C.R2GC_176_196,(0,0,4):C.R2GC_176_197,(0,0,5):C.R2GC_176_198,(0,0,6):C.R2GC_176_199,(0,0,3):C.R2GC_176_200,(0,0,7):C.R2GC_176_201})

V_39 = CTVertex(name = 'V_39',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G0, P.s] ], [ [P.G0, P.s, P.Z] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_171_166,(0,0,1):C.R2GC_171_167,(0,0,5):C.R2GC_171_168,(0,0,3):C.R2GC_171_169,(0,0,6):C.R2GC_171_170,(0,0,7):C.R2GC_171_171,(0,0,2):C.R2GC_171_172,(0,0,4):C.R2GC_171_173})

V_40 = CTVertex(name = 'V_40',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.G0, P.Z] ], [ [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_173_176,(0,0,1):C.R2GC_173_177,(0,0,2):C.R2GC_173_178,(0,0,4):C.R2GC_173_179,(0,0,5):C.R2GC_173_180,(0,0,6):C.R2GC_173_181,(0,0,3):C.R2GC_173_182,(0,0,7):C.R2GC_173_183})

V_41 = CTVertex(name = 'V_41',
                type = 'R2',
                particles = [ P.d__tilde__, P.u, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.d, P.G0, P.u], [P.d, P.H, P.u] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_405_1124,(0,0,1):C.R2GC_405_1125,(0,0,2):C.R2GC_405_1126,(0,0,6):C.R2GC_405_1127,(0,0,3):C.R2GC_405_1128,(0,0,5):C.R2GC_405_1129,(0,0,7):C.R2GC_405_1130,(0,0,8):C.R2GC_405_1131,(0,0,9):C.R2GC_405_1132,(0,1,0):C.R2GC_380_989,(0,1,1):C.R2GC_380_990,(0,1,2):C.R2GC_380_991,(0,1,6):C.R2GC_380_992,(0,1,3):C.R2GC_380_993,(0,1,4):C.R2GC_380_994,(0,1,5):C.R2GC_380_995,(0,1,7):C.R2GC_380_996,(0,1,9):C.R2GC_380_997})

V_42 = CTVertex(name = 'V_42',
                type = 'R2',
                particles = [ P.s__tilde__, P.c, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.c, P.s] ], [ [P.a, P.G__plus__, P.s] ], [ [P.c, P.G0, P.s], [P.c, P.H, P.s] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.c, P.g, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_377_972,(0,0,1):C.R2GC_377_973,(0,0,2):C.R2GC_377_974,(0,0,6):C.R2GC_377_975,(0,0,3):C.R2GC_377_976,(0,0,4):C.R2GC_377_977,(0,0,5):C.R2GC_377_978,(0,0,7):C.R2GC_377_979,(0,0,9):C.R2GC_377_980,(0,1,0):C.R2GC_392_1047,(0,1,1):C.R2GC_392_1048,(0,1,2):C.R2GC_392_1049,(0,1,6):C.R2GC_392_1050,(0,1,3):C.R2GC_392_1051,(0,1,5):C.R2GC_392_1052,(0,1,7):C.R2GC_392_1053,(0,1,8):C.R2GC_392_1054,(0,1,9):C.R2GC_392_1055})

V_43 = CTVertex(name = 'V_43',
                type = 'R2',
                particles = [ P.b__tilde__, P.t, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.b, P.G0, P.t], [P.b, P.H, P.t] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_397_1082,(0,0,1):C.R2GC_397_1083,(0,0,2):C.R2GC_397_1084,(0,0,6):C.R2GC_397_1085,(0,0,3):C.R2GC_397_1086,(0,0,5):C.R2GC_397_1087,(0,0,7):C.R2GC_397_1088,(0,0,8):C.R2GC_397_1089,(0,0,9):C.R2GC_397_1090,(0,1,0):C.R2GC_372_937,(0,1,1):C.R2GC_372_938,(0,1,2):C.R2GC_372_939,(0,1,6):C.R2GC_372_940,(0,1,3):C.R2GC_372_941,(0,1,4):C.R2GC_372_942,(0,1,5):C.R2GC_372_943,(0,1,7):C.R2GC_372_944,(0,1,9):C.R2GC_372_945})

V_44 = CTVertex(name = 'V_44',
                type = 'R2',
                particles = [ P.ve__tilde__, P.e__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.G0, P.W__plus__], [P.e__minus__, P.H, P.W__plus__] ], [ [P.e__minus__, P.G__plus__, P.Z] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.G__plus__, P.ve, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_385_1020,(0,0,1):C.R2GC_385_1021,(0,0,2):C.R2GC_385_1022,(0,0,3):C.R2GC_385_1023,(0,0,4):C.R2GC_385_1024})

V_45 = CTVertex(name = 'V_45',
                type = 'R2',
                particles = [ P.vm__tilde__, P.mu__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.W__plus__], [P.H, P.mu__minus__, P.W__plus__] ], [ [P.G__plus__, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.Z] ], [ [P.mu__minus__, P.vm, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_389_1036,(0,0,1):C.R2GC_389_1037,(0,0,2):C.R2GC_389_1038,(0,0,3):C.R2GC_389_1039,(0,0,4):C.R2GC_389_1040})

V_46 = CTVertex(name = 'V_46',
                type = 'R2',
                particles = [ P.vt__tilde__, P.ta__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.W__plus__], [P.H, P.ta__minus__, P.W__plus__] ], [ [P.G__plus__, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.Z] ], [ [P.ta__minus__, P.vt, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_401_1104,(0,0,1):C.R2GC_401_1105,(0,0,2):C.R2GC_401_1106,(0,0,3):C.R2GC_401_1107,(0,0,4):C.R2GC_401_1108})

V_47 = CTVertex(name = 'V_47',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.H, P.Z] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_387_1025,(0,0,1):C.R2GC_387_1026,(0,0,2):C.R2GC_387_1027,(0,0,4):C.R2GC_387_1028,(0,0,3):C.R2GC_387_1029,(0,0,5):C.R2GC_387_1030})

V_48 = CTVertex(name = 'V_48',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.G__plus__, P.vm, P.W__plus__] ], [ [P.H, P.mu__minus__] ], [ [P.H, P.mu__minus__, P.Z] ], [ [P.mu__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_391_1041,(0,0,1):C.R2GC_391_1042,(0,0,3):C.R2GC_391_1043,(0,0,5):C.R2GC_391_1044,(0,0,2):C.R2GC_391_1045,(0,0,4):C.R2GC_391_1046})

V_49 = CTVertex(name = 'V_49',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.G__plus__, P.vt, P.W__plus__] ], [ [P.H, P.ta__minus__] ], [ [P.H, P.ta__minus__, P.Z] ], [ [P.ta__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_403_1109,(0,0,1):C.R2GC_403_1110,(0,0,3):C.R2GC_403_1111,(0,0,5):C.R2GC_403_1112,(0,0,2):C.R2GC_403_1113,(0,0,4):C.R2GC_403_1114})

V_50 = CTVertex(name = 'V_50',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.G0, P.Z] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_178_210,(0,0,1):C.R2GC_178_211,(0,0,3):C.R2GC_178_212,(0,0,4):C.R2GC_178_213,(0,0,2):C.R2GC_178_214,(0,0,5):C.R2GC_178_215})

V_51 = CTVertex(name = 'V_51',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.W__plus__] ], [ [P.H, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_179_216,(0,0,1):C.R2GC_179_217,(0,0,4):C.R2GC_179_218,(0,0,5):C.R2GC_179_219,(0,0,2):C.R2GC_179_220,(0,0,3):C.R2GC_179_221})

V_52 = CTVertex(name = 'V_52',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.W__plus__] ], [ [P.H, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_180_222,(0,0,1):C.R2GC_180_223,(0,0,4):C.R2GC_180_224,(0,0,5):C.R2GC_180_225,(0,0,2):C.R2GC_180_226,(0,0,3):C.R2GC_180_227})

V_53 = CTVertex(name = 'V_53',
                type = 'R2',
                particles = [ P.e__plus__, P.ve, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.G0, P.W__plus__], [P.e__minus__, P.H, P.W__plus__] ], [ [P.e__minus__, P.G__plus__, P.Z] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.G__plus__, P.ve, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_384_1015,(0,0,1):C.R2GC_384_1016,(0,0,2):C.R2GC_384_1017,(0,0,3):C.R2GC_384_1018,(0,0,4):C.R2GC_384_1019})

V_54 = CTVertex(name = 'V_54',
                type = 'R2',
                particles = [ P.mu__plus__, P.vm, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.W__plus__], [P.H, P.mu__minus__, P.W__plus__] ], [ [P.G__plus__, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.Z] ], [ [P.mu__minus__, P.vm, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_388_1031,(0,0,1):C.R2GC_388_1032,(0,0,2):C.R2GC_388_1033,(0,0,3):C.R2GC_388_1034,(0,0,4):C.R2GC_388_1035})

V_55 = CTVertex(name = 'V_55',
                type = 'R2',
                particles = [ P.ta__plus__, P.vt, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.W__plus__], [P.H, P.ta__minus__, P.W__plus__] ], [ [P.G__plus__, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.Z] ], [ [P.ta__minus__, P.vt, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_400_1099,(0,0,1):C.R2GC_400_1100,(0,0,2):C.R2GC_400_1101,(0,0,3):C.R2GC_400_1102,(0,0,4):C.R2GC_400_1103})

V_56 = CTVertex(name = 'V_56',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.u] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.H, P.u, P.Z] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_406_1133,(0,0,1):C.R2GC_406_1134,(0,0,4):C.R2GC_406_1135,(0,0,3):C.R2GC_406_1136,(0,0,5):C.R2GC_406_1137,(0,0,7):C.R2GC_406_1138,(0,0,2):C.R2GC_406_1139,(0,0,6):C.R2GC_406_1140})

V_57 = CTVertex(name = 'V_57',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.H] ], [ [P.c, P.H, P.Z] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_378_981,(0,0,1):C.R2GC_378_982,(0,0,2):C.R2GC_378_983,(0,0,3):C.R2GC_378_984,(0,0,5):C.R2GC_378_985,(0,0,6):C.R2GC_378_986,(0,0,4):C.R2GC_378_987,(0,0,7):C.R2GC_378_988})

V_58 = CTVertex(name = 'V_58',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.G0, P.t] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.H, P.t, P.Z] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_398_1091,(0,0,1):C.R2GC_398_1092,(0,0,4):C.R2GC_398_1093,(0,0,3):C.R2GC_398_1094,(0,0,5):C.R2GC_398_1095,(0,0,7):C.R2GC_398_1096,(0,0,2):C.R2GC_398_1097,(0,0,6):C.R2GC_398_1098})

V_59 = CTVertex(name = 'V_59',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.u] ], [ [P.G0, P.u, P.Z] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_177_202,(0,0,1):C.R2GC_177_203,(0,0,5):C.R2GC_177_204,(0,0,3):C.R2GC_177_205,(0,0,6):C.R2GC_177_206,(0,0,7):C.R2GC_177_207,(0,0,2):C.R2GC_177_208,(0,0,4):C.R2GC_177_209})

V_60 = CTVertex(name = 'V_60',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0, P.Z] ], [ [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_170_158,(0,0,1):C.R2GC_170_159,(0,0,2):C.R2GC_170_160,(0,0,4):C.R2GC_170_161,(0,0,5):C.R2GC_170_162,(0,0,6):C.R2GC_170_163,(0,0,3):C.R2GC_170_164,(0,0,7):C.R2GC_170_165})

V_61 = CTVertex(name = 'V_61',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.G0, P.t] ], [ [P.G0, P.t, P.Z] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_174_184,(0,0,1):C.R2GC_174_185,(0,0,5):C.R2GC_174_186,(0,0,3):C.R2GC_174_187,(0,0,6):C.R2GC_174_188,(0,0,7):C.R2GC_174_189,(0,0,2):C.R2GC_174_190,(0,0,4):C.R2GC_174_191})

V_62 = CTVertex(name = 'V_62',
                type = 'R2',
                particles = [ P.a, P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,9):C.R2GC_352_753,(0,0,0):C.R2GC_353_755,(0,0,1):C.R2GC_353_756,(0,0,2):C.R2GC_353_757,(0,0,3):C.R2GC_353_758,(0,0,4):C.R2GC_353_759,(0,0,5):C.R2GC_353_760,(0,0,6):C.R2GC_353_761,(0,0,7):C.R2GC_353_762,(0,0,8):C.R2GC_353_763})

V_63 = CTVertex(name = 'V_63',
                type = 'R2',
                particles = [ P.Z, P.G0, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS3 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_324_645,(0,0,1):C.R2GC_324_646,(0,0,2):C.R2GC_324_647,(0,0,3):C.R2GC_324_648,(0,0,6):C.R2GC_324_649,(0,0,7):C.R2GC_324_650,(0,0,8):C.R2GC_324_651,(0,0,9):C.R2GC_324_652,(0,0,10):C.R2GC_324_653,(0,0,5):C.R2GC_324_654,(0,0,4):C.R2GC_324_655,(0,1,0):C.R2GC_348_733,(0,1,1):C.R2GC_348_734,(0,1,2):C.R2GC_348_735,(0,1,3):C.R2GC_348_736,(0,1,6):C.R2GC_348_737,(0,1,7):C.R2GC_348_738,(0,1,8):C.R2GC_348_739,(0,1,9):C.R2GC_348_740,(0,1,10):C.R2GC_348_741,(0,1,5):C.R2GC_348_742,(0,1,4):C.R2GC_348_743})

V_64 = CTVertex(name = 'V_64',
                type = 'R2',
                particles = [ P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS3 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,0):C.R2GC_335_695,(0,0,1):C.R2GC_335_696,(0,0,2):C.R2GC_335_697,(0,0,3):C.R2GC_335_698,(0,0,4):C.R2GC_335_699,(0,0,6):C.R2GC_335_700,(0,0,7):C.R2GC_335_701,(0,0,8):C.R2GC_335_702,(0,0,9):C.R2GC_335_703,(0,0,5):C.R2GC_335_704,(0,1,0):C.R2GC_334_685,(0,1,1):C.R2GC_334_686,(0,1,2):C.R2GC_334_687,(0,1,3):C.R2GC_334_688,(0,1,4):C.R2GC_334_689,(0,1,6):C.R2GC_334_690,(0,1,7):C.R2GC_334_691,(0,1,8):C.R2GC_334_692,(0,1,9):C.R2GC_334_693,(0,1,5):C.R2GC_334_694})

V_65 = CTVertex(name = 'V_65',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G0, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_261_422,(0,0,2):C.R2GC_261_423,(0,0,3):C.R2GC_261_424,(0,0,4):C.R2GC_261_425,(0,0,5):C.R2GC_261_426,(0,0,8):C.R2GC_261_427,(0,0,12):C.R2GC_261_428,(0,0,15):C.R2GC_261_429,(0,0,16):C.R2GC_261_430,(0,0,17):C.R2GC_261_431,(0,0,0):C.R2GC_261_432,(0,0,7):C.R2GC_261_433,(0,0,9):C.R2GC_261_434,(0,0,10):C.R2GC_261_435,(0,0,11):C.R2GC_261_436,(0,0,13):C.R2GC_261_437,(0,0,14):C.R2GC_261_438,(0,0,6):C.R2GC_261_439})

V_66 = CTVertex(name = 'V_66',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_260_404,(0,0,2):C.R2GC_260_405,(0,0,3):C.R2GC_260_406,(0,0,4):C.R2GC_260_407,(0,0,5):C.R2GC_260_408,(0,0,11):C.R2GC_260_409,(0,0,13):C.R2GC_260_410,(0,0,15):C.R2GC_260_411,(0,0,16):C.R2GC_260_412,(0,0,17):C.R2GC_260_413,(0,0,0):C.R2GC_260_414,(0,0,7):C.R2GC_260_415,(0,0,8):C.R2GC_260_416,(0,0,9):C.R2GC_260_417,(0,0,10):C.R2GC_260_418,(0,0,12):C.R2GC_260_419,(0,0,14):C.R2GC_260_420,(0,0,6):C.R2GC_260_421})

V_67 = CTVertex(name = 'V_67',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_367_894,(0,0,2):C.R2GC_368_898,(0,0,3):C.R2GC_368_899,(0,0,4):C.R2GC_368_900,(0,0,6):C.R2GC_368_901,(0,0,8):C.R2GC_367_889,(0,0,0):C.R2GC_368_902,(0,0,5):C.R2GC_368_903,(0,0,7):C.R2GC_368_904})

V_68 = CTVertex(name = 'V_68',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_261_422,(0,0,2):C.R2GC_261_423,(0,0,3):C.R2GC_261_424,(0,0,4):C.R2GC_261_425,(0,0,5):C.R2GC_261_426,(0,0,8):C.R2GC_261_427,(0,0,12):C.R2GC_261_428,(0,0,15):C.R2GC_261_429,(0,0,16):C.R2GC_261_430,(0,0,17):C.R2GC_261_431,(0,0,0):C.R2GC_261_432,(0,0,7):C.R2GC_261_433,(0,0,9):C.R2GC_261_434,(0,0,10):C.R2GC_261_435,(0,0,11):C.R2GC_261_436,(0,0,13):C.R2GC_261_437,(0,0,14):C.R2GC_261_438,(0,0,6):C.R2GC_261_439})

V_69 = CTVertex(name = 'V_69',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_260_413,(0,0,2):C.R2GC_262_440,(0,0,3):C.R2GC_262_441,(0,0,4):C.R2GC_262_442,(0,0,5):C.R2GC_262_443,(0,0,11):C.R2GC_260_410,(0,0,13):C.R2GC_260_409,(0,0,15):C.R2GC_262_444,(0,0,16):C.R2GC_262_445,(0,0,17):C.R2GC_260_404,(0,0,0):C.R2GC_262_446,(0,0,7):C.R2GC_260_418,(0,0,8):C.R2GC_262_447,(0,0,9):C.R2GC_262_448,(0,0,10):C.R2GC_260_415,(0,0,12):C.R2GC_262_449,(0,0,14):C.R2GC_262_450,(0,0,6):C.R2GC_262_451})

V_70 = CTVertex(name = 'V_70',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_367_889,(0,0,2):C.R2GC_367_890,(0,0,3):C.R2GC_367_891,(0,0,4):C.R2GC_367_892,(0,0,6):C.R2GC_367_893,(0,0,8):C.R2GC_367_894,(0,0,0):C.R2GC_367_895,(0,0,5):C.R2GC_367_896,(0,0,7):C.R2GC_367_897})

V_71 = CTVertex(name = 'V_71',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.W__plus__, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVVV1, L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,1,3):C.R2GC_292_588,(0,1,0):C.R2GC_292_589,(0,1,1):C.R2GC_292_590,(0,1,2):C.R2GC_292_591,(0,1,4):C.R2GC_292_592,(0,2,3):C.R2GC_291_583,(0,2,0):C.R2GC_291_584,(0,2,1):C.R2GC_291_585,(0,2,2):C.R2GC_291_586,(0,2,4):C.R2GC_291_587,(0,3,3):C.R2GC_291_583,(0,3,0):C.R2GC_291_584,(0,3,1):C.R2GC_291_585,(0,3,2):C.R2GC_291_586,(0,3,4):C.R2GC_291_587,(0,0,1):C.R2GC_162_115,(0,0,2):C.R2GC_162_116})

V_72 = CTVertex(name = 'V_72',
                type = 'R2',
                particles = [ P.Z, P.Z, P.G0, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_354_764,(0,0,1):C.R2GC_354_765,(0,0,2):C.R2GC_354_766,(0,0,3):C.R2GC_354_767,(0,0,7):C.R2GC_354_768,(0,0,8):C.R2GC_354_769,(0,0,9):C.R2GC_354_770,(0,0,10):C.R2GC_354_771,(0,0,11):C.R2GC_354_772,(0,0,12):C.R2GC_354_773,(0,0,5):C.R2GC_354_774,(0,0,6):C.R2GC_354_775,(0,0,4):C.R2GC_148_85})

V_73 = CTVertex(name = 'V_73',
                type = 'R2',
                particles = [ P.Z, P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,10):C.R2GC_354_773,(0,0,0):C.R2GC_322_642,(0,0,1):C.R2GC_355_776,(0,0,2):C.R2GC_355_777,(0,0,3):C.R2GC_355_778,(0,0,4):C.R2GC_355_779,(0,0,6):C.R2GC_355_780,(0,0,7):C.R2GC_355_781,(0,0,8):C.R2GC_355_782,(0,0,9):C.R2GC_355_783,(0,0,5):C.R2GC_355_784})

V_74 = CTVertex(name = 'V_74',
                type = 'R2',
                particles = [ P.Z, P.Z, P.H, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_354_764,(0,0,1):C.R2GC_354_765,(0,0,2):C.R2GC_354_766,(0,0,3):C.R2GC_354_767,(0,0,7):C.R2GC_354_768,(0,0,8):C.R2GC_354_769,(0,0,9):C.R2GC_354_770,(0,0,10):C.R2GC_354_771,(0,0,11):C.R2GC_354_772,(0,0,12):C.R2GC_354_773,(0,0,5):C.R2GC_354_775,(0,0,6):C.R2GC_354_774,(0,0,4):C.R2GC_148_85})

V_75 = CTVertex(name = 'V_75',
                type = 'R2',
                particles = [ P.Z, P.Z, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_371_926,(0,0,1):C.R2GC_371_927,(0,0,2):C.R2GC_371_928,(0,0,3):C.R2GC_371_929,(0,0,5):C.R2GC_371_930,(0,0,6):C.R2GC_371_931,(0,0,7):C.R2GC_371_932,(0,0,8):C.R2GC_371_933,(0,0,9):C.R2GC_371_934,(0,0,10):C.R2GC_371_935,(0,0,4):C.R2GC_371_936})

V_76 = CTVertex(name = 'V_76',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,3):C.R2GC_270_470,(0,0,0):C.R2GC_267_464,(0,0,1):C.R2GC_270_471,(0,0,2):C.R2GC_270_472,(0,0,4):C.R2GC_270_473,(0,1,3):C.R2GC_270_470,(0,1,0):C.R2GC_267_464,(0,1,1):C.R2GC_270_471,(0,1,2):C.R2GC_270_472,(0,1,4):C.R2GC_270_473,(0,2,3):C.R2GC_271_474,(0,2,0):C.R2GC_268_469,(0,2,1):C.R2GC_271_475,(0,2,2):C.R2GC_271_476,(0,2,4):C.R2GC_271_477})

V_77 = CTVertex(name = 'V_77',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0], [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_310_623,(0,0,1):C.R2GC_310_624,(0,0,2):C.R2GC_310_625,(0,0,3):C.R2GC_264_453,(0,1,0):C.R2GC_310_623,(0,1,1):C.R2GC_310_624,(0,1,2):C.R2GC_319_635})

V_78 = CTVertex(name = 'V_78',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__], [P.H, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_310_623,(0,0,1):C.R2GC_311_626,(0,0,2):C.R2GC_310_625,(0,0,3):C.R2GC_264_453,(0,1,0):C.R2GC_310_623,(0,1,1):C.R2GC_311_626,(0,1,2):C.R2GC_319_635})

V_79 = CTVertex(name = 'V_79',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__], [P.H, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_310_623,(0,0,1):C.R2GC_312_627,(0,0,2):C.R2GC_310_625,(0,0,3):C.R2GC_264_453,(0,1,0):C.R2GC_310_623,(0,1,1):C.R2GC_312_627,(0,1,2):C.R2GC_319_635})

V_80 = CTVertex(name = 'V_80',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.g, P.u] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,3):C.R2GC_159_111,(0,1,0):C.R2GC_303_603,(0,1,1):C.R2GC_305_609,(0,1,2):C.R2GC_303_607,(0,1,4):C.R2GC_303_604,(0,1,5):C.R2GC_303_605,(0,2,0):C.R2GC_303_603,(0,2,1):C.R2GC_318_634,(0,2,4):C.R2GC_303_604,(0,2,5):C.R2GC_316_631})

V_81 = CTVertex(name = 'V_81',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                couplings = {(0,0,2):C.R2GC_153_101,(0,1,0):C.R2GC_303_603,(0,1,1):C.R2GC_303_604,(0,1,3):C.R2GC_303_605,(0,1,4):C.R2GC_303_606,(0,1,5):C.R2GC_303_607,(0,2,0):C.R2GC_303_603,(0,2,1):C.R2GC_303_604,(0,2,3):C.R2GC_316_631,(0,2,4):C.R2GC_316_632})

V_82 = CTVertex(name = 'V_82',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.g, P.t] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,3):C.R2GC_155_105,(0,1,0):C.R2GC_303_603,(0,1,1):C.R2GC_304_608,(0,1,2):C.R2GC_303_607,(0,1,4):C.R2GC_303_604,(0,1,5):C.R2GC_303_605,(0,2,0):C.R2GC_303_603,(0,2,1):C.R2GC_317_633,(0,2,4):C.R2GC_303_604,(0,2,5):C.R2GC_316_631})

V_83 = CTVertex(name = 'V_83',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_300_594,(0,0,1):C.R2GC_300_595,(0,0,2):C.R2GC_301_599,(0,0,3):C.R2GC_300_597,(0,0,4):C.R2GC_301_600,(0,0,5):C.R2GC_264_454,(0,1,0):C.R2GC_300_594,(0,1,1):C.R2GC_300_595,(0,1,2):C.R2GC_301_599,(0,1,3):C.R2GC_306_610,(0,1,4):C.R2GC_307_612})

V_84 = CTVertex(name = 'V_84',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.g, P.s] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_300_594,(0,0,1):C.R2GC_302_601,(0,0,2):C.R2GC_264_454,(0,0,4):C.R2GC_300_595,(0,0,3):C.R2GC_302_602,(0,0,5):C.R2GC_300_597,(0,1,0):C.R2GC_300_594,(0,1,1):C.R2GC_308_613,(0,1,4):C.R2GC_300_595,(0,1,3):C.R2GC_302_602,(0,1,5):C.R2GC_306_610})

V_85 = CTVertex(name = 'V_85',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.t, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_300_594,(0,0,1):C.R2GC_300_595,(0,0,2):C.R2GC_300_596,(0,0,3):C.R2GC_300_597,(0,0,4):C.R2GC_300_598,(0,0,5):C.R2GC_264_454,(0,1,0):C.R2GC_300_594,(0,1,1):C.R2GC_300_595,(0,1,2):C.R2GC_300_596,(0,1,3):C.R2GC_306_610,(0,1,4):C.R2GC_306_611})

V_86 = CTVertex(name = 'V_86',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.g, P.u] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_154_102,(0,0,4):C.R2GC_154_103,(0,0,3):C.R2GC_160_112,(0,1,1):C.R2GC_228_262,(0,1,2):C.R2GC_223_253,(0,1,5):C.R2GC_225_256,(0,2,1):C.R2GC_227_261,(0,2,5):C.R2GC_226_258})

V_87 = CTVertex(name = 'V_87',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_154_102,(0,0,1):C.R2GC_154_103,(0,0,2):C.R2GC_154_104,(0,1,3):C.R2GC_225_256,(0,1,4):C.R2GC_225_257,(0,1,5):C.R2GC_223_253,(0,2,3):C.R2GC_226_258,(0,2,4):C.R2GC_226_259})

V_88 = CTVertex(name = 'V_88',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.g, P.t] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_154_102,(0,0,4):C.R2GC_154_103,(0,0,3):C.R2GC_156_106,(0,1,1):C.R2GC_224_255,(0,1,2):C.R2GC_223_253,(0,1,5):C.R2GC_225_256,(0,2,1):C.R2GC_223_252,(0,2,5):C.R2GC_226_258})

V_89 = CTVertex(name = 'V_89',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_223_249,(0,0,1):C.R2GC_154_103,(0,0,2):C.R2GC_227_260,(0,0,3):C.R2GC_223_251,(0,0,4):C.R2GC_227_261,(0,0,5):C.R2GC_223_253,(0,1,0):C.R2GC_223_249,(0,1,1):C.R2GC_154_103,(0,1,2):C.R2GC_227_260,(0,1,3):C.R2GC_224_254,(0,1,4):C.R2GC_228_262})

V_90 = CTVertex(name = 'V_90',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.g, P.s] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_223_249,(0,0,1):C.R2GC_226_259,(0,0,2):C.R2GC_223_253,(0,0,4):C.R2GC_154_103,(0,0,3):C.R2GC_229_263,(0,0,5):C.R2GC_223_251,(0,1,0):C.R2GC_223_249,(0,1,1):C.R2GC_225_257,(0,1,4):C.R2GC_154_103,(0,1,3):C.R2GC_229_263,(0,1,5):C.R2GC_224_254})

V_91 = CTVertex(name = 'V_91',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.t, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_223_249,(0,0,1):C.R2GC_154_103,(0,0,2):C.R2GC_223_250,(0,0,3):C.R2GC_223_251,(0,0,4):C.R2GC_223_252,(0,0,5):C.R2GC_223_253,(0,1,0):C.R2GC_223_249,(0,1,1):C.R2GC_154_103,(0,1,2):C.R2GC_223_250,(0,1,3):C.R2GC_224_254,(0,1,4):C.R2GC_224_255})

V_92 = CTVertex(name = 'V_92',
                type = 'R2',
                particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d, P.u] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.d, P.G0, P.u] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_276_522,(0,0,1):C.R2GC_276_524,(0,0,2):C.R2GC_276_523,(0,0,4):C.R2GC_276_525,(0,0,6):C.R2GC_276_526,(0,0,7):C.R2GC_276_528,(0,0,8):C.R2GC_276_527,(0,1,3):C.R2GC_175_192,(0,1,5):C.R2GC_175_193})

V_93 = CTVertex(name = 'V_93',
                type = 'R2',
                particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c, P.s] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.s, P.W__plus__] ], [ [P.c, P.G0, P.s] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.s, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_276_522,(0,0,1):C.R2GC_276_523,(0,0,2):C.R2GC_276_524,(0,0,4):C.R2GC_276_525,(0,0,6):C.R2GC_276_526,(0,0,7):C.R2GC_276_527,(0,0,8):C.R2GC_276_528,(0,1,3):C.R2GC_169_156,(0,1,5):C.R2GC_169_157})

V_94 = CTVertex(name = 'V_94',
                type = 'R2',
                particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b, P.t] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.b, P.G0, P.t] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_276_522,(0,0,1):C.R2GC_276_524,(0,0,2):C.R2GC_276_523,(0,0,4):C.R2GC_276_525,(0,0,6):C.R2GC_276_526,(0,0,7):C.R2GC_276_528,(0,0,8):C.R2GC_276_527,(0,1,3):C.R2GC_172_174,(0,1,5):C.R2GC_172_175})

V_95 = CTVertex(name = 'V_95',
                type = 'R2',
                particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d, P.u] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.d, P.G0, P.u] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_276_522,(0,0,1):C.R2GC_276_524,(0,0,2):C.R2GC_276_523,(0,0,4):C.R2GC_276_525,(0,0,6):C.R2GC_276_526,(0,0,7):C.R2GC_276_528,(0,0,8):C.R2GC_276_527,(0,1,3):C.R2GC_175_192,(0,1,5):C.R2GC_175_193})

V_96 = CTVertex(name = 'V_96',
                type = 'R2',
                particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c, P.s] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.s, P.W__plus__] ], [ [P.c, P.G0, P.s] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.s, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_276_522,(0,0,1):C.R2GC_276_523,(0,0,2):C.R2GC_276_524,(0,0,4):C.R2GC_276_525,(0,0,6):C.R2GC_276_526,(0,0,7):C.R2GC_276_527,(0,0,8):C.R2GC_276_528,(0,1,3):C.R2GC_169_156,(0,1,5):C.R2GC_169_157})

V_97 = CTVertex(name = 'V_97',
                type = 'R2',
                particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b, P.t] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.b, P.G0, P.t] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_276_522,(0,0,1):C.R2GC_276_524,(0,0,2):C.R2GC_276_523,(0,0,4):C.R2GC_276_525,(0,0,6):C.R2GC_276_526,(0,0,7):C.R2GC_276_528,(0,0,8):C.R2GC_276_527,(0,1,3):C.R2GC_172_174,(0,1,5):C.R2GC_172_175})

V_98 = CTVertex(name = 'V_98',
                type = 'R2',
                particles = [ P.e__plus__, P.ve, P.W__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__, P.Z] ], [ [P.ve, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_279_529,(0,0,1):C.R2GC_279_530,(0,0,2):C.R2GC_279_531,(0,0,3):C.R2GC_279_532})

V_99 = CTVertex(name = 'V_99',
                type = 'R2',
                particles = [ P.mu__plus__, P.vm, P.W__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFV2 ],
                loop_particles = [ [ [P.a, P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__, P.Z] ], [ [P.vm, P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_279_529,(0,0,1):C.R2GC_279_530,(0,0,2):C.R2GC_279_531,(0,0,3):C.R2GC_279_532})

V_100 = CTVertex(name = 'V_100',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.vt, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__, P.Z] ], [ [P.vt, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_279_529,(0,0,1):C.R2GC_279_530,(0,0,2):C.R2GC_279_531,(0,0,3):C.R2GC_279_532})

V_101 = CTVertex(name = 'V_101',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__, P.Z] ], [ [P.ve, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_279_529,(0,0,1):C.R2GC_279_530,(0,0,2):C.R2GC_279_531,(0,0,3):C.R2GC_279_532})

V_102 = CTVertex(name = 'V_102',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.mu__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__, P.Z] ], [ [P.vm, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_279_529,(0,0,1):C.R2GC_279_530,(0,0,2):C.R2GC_279_531,(0,0,3):C.R2GC_279_532})

V_103 = CTVertex(name = 'V_103',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.ta__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__, P.Z] ], [ [P.vt, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_279_529,(0,0,1):C.R2GC_279_530,(0,0,2):C.R2GC_279_531,(0,0,3):C.R2GC_279_532})

V_104 = CTVertex(name = 'V_104',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.g, P.u] ], [ [P.u, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_326_662,(0,0,1):C.R2GC_330_674,(0,0,2):C.R2GC_326_667,(0,0,4):C.R2GC_326_663,(0,0,3):C.R2GC_330_675,(0,0,5):C.R2GC_326_665,(0,1,0):C.R2GC_342_716,(0,1,1):C.R2GC_344_723,(0,1,4):C.R2GC_342_717,(0,1,3):C.R2GC_344_724,(0,1,5):C.R2GC_342_719})

V_105 = CTVertex(name = 'V_105',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_326_662,(0,0,1):C.R2GC_326_663,(0,0,2):C.R2GC_326_664,(0,0,3):C.R2GC_326_665,(0,0,4):C.R2GC_326_666,(0,0,5):C.R2GC_326_667,(0,1,0):C.R2GC_342_716,(0,1,1):C.R2GC_342_717,(0,1,2):C.R2GC_342_718,(0,1,3):C.R2GC_342_719,(0,1,4):C.R2GC_342_720})

V_106 = CTVertex(name = 'V_106',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.g, P.t] ], [ [P.t, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_326_662,(0,0,1):C.R2GC_329_672,(0,0,2):C.R2GC_326_667,(0,0,4):C.R2GC_326_663,(0,0,3):C.R2GC_329_673,(0,0,5):C.R2GC_326_665,(0,1,0):C.R2GC_342_716,(0,1,1):C.R2GC_343_721,(0,1,4):C.R2GC_342_717,(0,1,3):C.R2GC_343_722,(0,1,5):C.R2GC_342_719})

V_107 = CTVertex(name = 'V_107',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.u] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_325_656,(0,0,1):C.R2GC_325_657,(0,0,2):C.R2GC_327_668,(0,0,3):C.R2GC_325_659,(0,0,4):C.R2GC_327_669,(0,0,5):C.R2GC_325_661,(0,1,0):C.R2GC_331_676,(0,1,1):C.R2GC_331_677,(0,1,2):C.R2GC_332_681,(0,1,3):C.R2GC_331_679,(0,1,4):C.R2GC_332_682})

V_108 = CTVertex(name = 'V_108',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.g, P.s] ], [ [P.s, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_325_656,(0,0,1):C.R2GC_328_670,(0,0,2):C.R2GC_325_661,(0,0,4):C.R2GC_325_657,(0,0,3):C.R2GC_328_671,(0,0,5):C.R2GC_325_659,(0,1,0):C.R2GC_331_676,(0,1,1):C.R2GC_333_683,(0,1,4):C.R2GC_331_677,(0,1,3):C.R2GC_333_684,(0,1,5):C.R2GC_331_679})

V_109 = CTVertex(name = 'V_109',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.t, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_325_656,(0,0,1):C.R2GC_325_657,(0,0,2):C.R2GC_325_658,(0,0,3):C.R2GC_325_659,(0,0,4):C.R2GC_325_660,(0,0,5):C.R2GC_325_661,(0,1,0):C.R2GC_331_676,(0,1,1):C.R2GC_331_677,(0,1,2):C.R2GC_331_678,(0,1,3):C.R2GC_331_679,(0,1,4):C.R2GC_331_680})

V_110 = CTVertex(name = 'V_110',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.W__plus__] ], [ [P.ve, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_339_711,(0,0,1):C.R2GC_339_712,(0,0,2):C.R2GC_339_713})

V_111 = CTVertex(name = 'V_111',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.mu__minus__] ], [ [P.mu__minus__, P.W__plus__] ], [ [P.vm, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_340_714,(0,0,1):C.R2GC_339_712,(0,0,2):C.R2GC_339_713})

V_112 = CTVertex(name = 'V_112',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.ta__minus__] ], [ [P.ta__minus__, P.W__plus__] ], [ [P.vt, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_341_715,(0,0,1):C.R2GC_339_712,(0,0,2):C.R2GC_339_713})

V_113 = CTVertex(name = 'V_113',
                 type = 'R2',
                 particles = [ P.e__plus__, P.e__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0], [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve] ], [ [P.ve, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_336_705,(0,0,1):C.R2GC_336_706,(0,0,2):C.R2GC_336_707,(0,0,4):C.R2GC_336_708,(0,1,0):C.R2GC_345_725,(0,1,1):C.R2GC_345_726,(0,1,2):C.R2GC_345_727,(0,1,3):C.R2GC_345_728})

V_114 = CTVertex(name = 'V_114',
                 type = 'R2',
                 particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__], [P.H, P.mu__minus__] ], [ [P.G__plus__, P.vm] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_336_705,(0,0,1):C.R2GC_337_709,(0,0,3):C.R2GC_336_707,(0,0,4):C.R2GC_336_708,(0,1,0):C.R2GC_345_725,(0,1,1):C.R2GC_346_729,(0,1,2):C.R2GC_346_730,(0,1,3):C.R2GC_345_727})

V_115 = CTVertex(name = 'V_115',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__], [P.H, P.ta__minus__] ], [ [P.G__plus__, P.vt] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_336_705,(0,0,1):C.R2GC_338_710,(0,0,3):C.R2GC_336_707,(0,0,4):C.R2GC_336_708,(0,1,0):C.R2GC_345_725,(0,1,1):C.R2GC_347_731,(0,1,2):C.R2GC_347_732,(0,1,3):C.R2GC_345_727})

V_116 = CTVertex(name = 'V_116',
                 type = 'R2',
                 particles = [ P.H ],
                 color = [ '1' ],
                 lorentz = [ L.S1 ],
                 loop_particles = [ [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_152_99,(0,0,1):C.R2GC_152_100})

V_117 = CTVertex(name = 'V_117',
                 type = 'R2',
                 particles = [ P.e__plus__, P.e__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.Z] ], [ [P.ve, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_239_273,(0,1,1):C.R2GC_239_274,(0,3,0):C.R2GC_239_273,(0,3,1):C.R2GC_239_274,(0,2,1):C.R2GC_203_244,(0,2,2):C.R2GC_161_113,(0,4,1):C.R2GC_204_245,(0,0,0):C.R2GC_117_7})

V_118 = CTVertex(name = 'V_118',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.e__minus__, P.W__plus__] ], [ [P.ve, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_161_113,(0,0,1):C.R2GC_215_246})

V_119 = CTVertex(name = 'V_119',
                 type = 'R2',
                 particles = [ P.mu__plus__, P.mu__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_240_275,(0,1,1):C.R2GC_240_276,(0,3,0):C.R2GC_240_275,(0,3,1):C.R2GC_240_276,(0,2,1):C.R2GC_203_244,(0,2,2):C.R2GC_161_113,(0,4,1):C.R2GC_204_245,(0,0,0):C.R2GC_117_7})

V_120 = CTVertex(name = 'V_120',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.mu__minus__, P.W__plus__] ], [ [P.vm, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_161_113,(0,0,1):C.R2GC_215_246})

V_121 = CTVertex(name = 'V_121',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.ta__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_243_283,(0,1,1):C.R2GC_243_284,(0,3,0):C.R2GC_243_283,(0,3,1):C.R2GC_243_284,(0,2,1):C.R2GC_203_244,(0,2,2):C.R2GC_161_113,(0,4,1):C.R2GC_204_245,(0,0,0):C.R2GC_117_7})

V_122 = CTVertex(name = 'V_122',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.ta__minus__, P.W__plus__] ], [ [P.vt, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_161_113,(0,0,1):C.R2GC_215_246})

V_123 = CTVertex(name = 'V_123',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.u] ], [ [P.d, P.W__plus__] ], [ [P.g, P.u] ], [ [P.u, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_244_285,(0,0,2):C.R2GC_244_286,(0,0,3):C.R2GC_244_287,(0,2,0):C.R2GC_244_285,(0,2,2):C.R2GC_244_286,(0,2,3):C.R2GC_244_287,(0,1,0):C.R2GC_199_241,(0,1,1):C.R2GC_161_113,(0,1,2):C.R2GC_197_238,(0,1,3):C.R2GC_199_242,(0,3,0):C.R2GC_199_241,(0,3,2):C.R2GC_197_238,(0,3,3):C.R2GC_200_243})

V_124 = CTVertex(name = 'V_124',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.d, P.g] ], [ [P.d, P.Z] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_238_270,(0,1,1):C.R2GC_238_271,(0,1,2):C.R2GC_238_272,(0,3,0):C.R2GC_238_270,(0,3,1):C.R2GC_238_271,(0,3,2):C.R2GC_238_272,(0,2,1):C.R2GC_197_238,(0,2,2):C.R2GC_197_239,(0,2,3):C.R2GC_161_113,(0,4,1):C.R2GC_197_238,(0,4,2):C.R2GC_198_240,(0,0,0):C.R2GC_115_6})

V_125 = CTVertex(name = 'V_125',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.c, P.g] ], [ [P.c, P.Z] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_237_267,(0,0,1):C.R2GC_237_268,(0,0,2):C.R2GC_237_269,(0,2,0):C.R2GC_237_267,(0,2,1):C.R2GC_237_268,(0,2,2):C.R2GC_237_269,(0,1,0):C.R2GC_199_241,(0,1,1):C.R2GC_197_238,(0,1,2):C.R2GC_199_242,(0,1,3):C.R2GC_161_113,(0,3,0):C.R2GC_199_241,(0,3,1):C.R2GC_197_238,(0,3,2):C.R2GC_200_243})

V_126 = CTVertex(name = 'V_126',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.W__plus__] ], [ [P.g, P.s] ], [ [P.s, P.Z] ] ],
                 couplings = {(0,1,0):C.R2GC_241_277,(0,1,2):C.R2GC_241_278,(0,1,3):C.R2GC_241_279,(0,3,0):C.R2GC_241_277,(0,3,2):C.R2GC_241_278,(0,3,3):C.R2GC_241_279,(0,2,1):C.R2GC_161_113,(0,2,2):C.R2GC_197_238,(0,2,3):C.R2GC_197_239,(0,4,2):C.R2GC_197_238,(0,4,3):C.R2GC_198_240,(0,0,0):C.R2GC_115_6})

V_127 = CTVertex(name = 'V_127',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.W__plus__] ], [ [P.g, P.t] ], [ [P.t, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_242_280,(0,0,2):C.R2GC_242_281,(0,0,3):C.R2GC_242_282,(0,2,0):C.R2GC_242_280,(0,2,2):C.R2GC_242_281,(0,2,3):C.R2GC_242_282,(0,1,0):C.R2GC_199_241,(0,1,1):C.R2GC_161_113,(0,1,2):C.R2GC_197_238,(0,1,3):C.R2GC_199_242,(0,3,0):C.R2GC_199_241,(0,3,2):C.R2GC_197_238,(0,3,3):C.R2GC_200_243})

V_128 = CTVertex(name = 'V_128',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.Z] ], [ [P.t, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_236_264,(0,1,1):C.R2GC_236_265,(0,1,2):C.R2GC_236_266,(0,3,0):C.R2GC_236_264,(0,3,1):C.R2GC_236_265,(0,3,2):C.R2GC_236_266,(0,2,1):C.R2GC_197_238,(0,2,2):C.R2GC_197_239,(0,2,3):C.R2GC_161_113,(0,4,1):C.R2GC_197_238,(0,4,2):C.R2GC_198_240,(0,0,0):C.R2GC_115_6})

V_129 = CTVertex(name = 'V_129',
                 type = 'R2',
                 particles = [ P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_357_785,(0,0,1):C.R2GC_357_786,(0,0,2):C.R2GC_357_787,(0,0,3):C.R2GC_357_788,(0,0,6):C.R2GC_357_789,(0,0,7):C.R2GC_357_790,(0,0,8):C.R2GC_357_791,(0,0,9):C.R2GC_357_792,(0,0,10):C.R2GC_357_793,(0,0,11):C.R2GC_359_811,(0,0,12):C.R2GC_359_812,(0,0,4):C.R2GC_359_813,(0,0,5):C.R2GC_357_796,(0,1,0):C.R2GC_165_139,(0,1,1):C.R2GC_165_140,(0,1,2):C.R2GC_165_141,(0,1,3):C.R2GC_165_142,(0,1,6):C.R2GC_165_143,(0,1,7):C.R2GC_165_144,(0,1,8):C.R2GC_165_145,(0,1,9):C.R2GC_165_146,(0,1,10):C.R2GC_165_147,(0,1,4):C.R2GC_165_148,(0,1,5):C.R2GC_165_149})

V_130 = CTVertex(name = 'V_130',
                 type = 'R2',
                 particles = [ P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_357_785,(0,0,1):C.R2GC_357_786,(0,0,2):C.R2GC_357_787,(0,0,3):C.R2GC_357_788,(0,0,6):C.R2GC_357_789,(0,0,7):C.R2GC_357_790,(0,0,8):C.R2GC_357_791,(0,0,9):C.R2GC_357_792,(0,0,10):C.R2GC_357_793,(0,0,11):C.R2GC_357_794,(0,0,12):C.R2GC_357_795,(0,0,4):C.R2GC_357_796,(0,0,5):C.R2GC_357_797,(0,1,0):C.R2GC_165_139,(0,1,1):C.R2GC_165_140,(0,1,2):C.R2GC_165_141,(0,1,3):C.R2GC_165_142,(0,1,6):C.R2GC_165_143,(0,1,7):C.R2GC_165_144,(0,1,8):C.R2GC_165_145,(0,1,9):C.R2GC_165_146,(0,1,10):C.R2GC_165_147,(0,1,4):C.R2GC_165_149,(0,1,5):C.R2GC_165_148})

V_131 = CTVertex(name = 'V_131',
                 type = 'R2',
                 particles = [ P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,12):C.R2GC_357_794,(0,0,14):C.R2GC_358_798,(0,0,0):C.R2GC_358_799,(0,0,1):C.R2GC_358_800,(0,0,2):C.R2GC_358_801,(0,0,3):C.R2GC_358_802,(0,0,4):C.R2GC_358_803,(0,0,5):C.R2GC_358_804,(0,0,6):C.R2GC_358_805,(0,0,8):C.R2GC_358_806,(0,0,9):C.R2GC_358_807,(0,0,10):C.R2GC_358_808,(0,0,11):C.R2GC_358_809,(0,0,13):C.R2GC_358_810,(0,1,0):C.R2GC_166_150,(0,1,2):C.R2GC_166_151,(0,1,3):C.R2GC_166_152,(0,1,4):C.R2GC_166_153,(0,1,5):C.R2GC_165_142,(0,1,7):C.R2GC_166_154,(0,1,8):C.R2GC_166_155,(0,1,10):C.R2GC_165_143,(0,1,11):C.R2GC_165_146})

V_132 = CTVertex(name = 'V_132',
                 type = 'R2',
                 particles = [ P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV3, L.VV6 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,2,12):C.R2GC_112_3,(0,0,0):C.R2GC_147_72,(0,0,2):C.R2GC_147_73,(0,0,4):C.R2GC_147_74,(0,0,5):C.R2GC_147_75,(0,0,7):C.R2GC_147_76,(0,0,8):C.R2GC_147_77,(0,0,9):C.R2GC_147_78,(0,0,10):C.R2GC_147_79,(0,0,11):C.R2GC_147_80,(0,0,12):C.R2GC_147_81,(0,1,1):C.R2GC_121_8,(0,1,3):C.R2GC_121_9,(0,1,6):C.R2GC_121_10})

V_133 = CTVertex(name = 'V_133',
                 type = 'R2',
                 particles = [ P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV3, L.VV6 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,2,12):C.R2GC_114_5,(0,0,0):C.R2GC_247_288,(0,0,2):C.R2GC_247_289,(0,0,4):C.R2GC_247_290,(0,0,5):C.R2GC_247_291,(0,0,7):C.R2GC_247_292,(0,0,8):C.R2GC_247_293,(0,0,9):C.R2GC_247_294,(0,0,10):C.R2GC_247_295,(0,0,11):C.R2GC_247_296,(0,0,12):C.R2GC_247_297,(0,1,1):C.R2GC_138_41,(0,1,3):C.R2GC_138_42,(0,1,6):C.R2GC_138_43})

V_134 = CTVertex(name = 'V_134',
                 type = 'R2',
                 particles = [ P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV3, L.VV6 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ] ],
                 couplings = {(0,2,13):C.R2GC_113_4,(0,0,0):C.R2GC_369_905,(0,0,2):C.R2GC_369_906,(0,0,4):C.R2GC_369_907,(0,0,5):C.R2GC_369_908,(0,0,7):C.R2GC_369_909,(0,0,8):C.R2GC_369_910,(0,0,9):C.R2GC_369_911,(0,0,10):C.R2GC_369_912,(0,0,11):C.R2GC_369_913,(0,0,13):C.R2GC_369_914,(0,1,1):C.R2GC_145_64,(0,1,3):C.R2GC_145_65,(0,1,6):C.R2GC_145_66,(0,1,12):C.R2GC_145_67})

V_135 = CTVertex(name = 'V_135',
                 type = 'R2',
                 particles = [ P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV4 ],
                 loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.t] ], [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ], [ [P.c, P.s] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.mu__minus__, P.vm] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,2,0):C.R2GC_112_3,(0,2,10):C.R2GC_113_4,(0,0,9):C.R2GC_363_854,(0,0,11):C.R2GC_363_855,(0,0,0):C.R2GC_363_856,(0,0,1):C.R2GC_363_857,(0,0,3):C.R2GC_363_858,(0,0,4):C.R2GC_363_859,(0,0,5):C.R2GC_363_860,(0,0,7):C.R2GC_363_861,(0,0,8):C.R2GC_363_862,(0,0,10):C.R2GC_363_863,(0,1,2):C.R2GC_161_113,(0,1,6):C.R2GC_161_114})

V_136 = CTVertex(name = 'V_136',
                 type = 'R2',
                 particles = [ P.g, P.g ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VV1, L.VV3, L.VV6 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.c] ], [ [P.d] ], [ [P.g] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,2,4):C.R2GC_110_1,(0,0,0):C.R2GC_137_35,(0,0,2):C.R2GC_137_36,(0,0,3):C.R2GC_137_37,(0,0,5):C.R2GC_137_38,(0,0,6):C.R2GC_137_39,(0,0,7):C.R2GC_137_40,(0,1,1):C.R2GC_122_11})

V_137 = CTVertex(name = 'V_137',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.e__minus__, P.G__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_313_628})

V_138 = CTVertex(name = 'V_138',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.mu__minus__] ] ],
                 couplings = {(0,0,0):C.R2GC_314_629})

V_139 = CTVertex(name = 'V_139',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.ta__minus__] ] ],
                 couplings = {(0,0,0):C.R2GC_315_630})

V_140 = CTVertex(name = 'V_140',
                 type = 'R2',
                 particles = [ P.a, P.a, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_164_128,(0,0,1):C.R2GC_164_129,(0,0,2):C.R2GC_164_130,(0,0,3):C.R2GC_164_131,(0,0,5):C.R2GC_164_132,(0,0,6):C.R2GC_164_133,(0,0,7):C.R2GC_164_134,(0,0,8):C.R2GC_164_135,(0,0,9):C.R2GC_164_136,(0,0,10):C.R2GC_164_137,(0,0,4):C.R2GC_164_138})

V_141 = CTVertex(name = 'V_141',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_370_915,(0,0,1):C.R2GC_370_916,(0,0,2):C.R2GC_370_917,(0,0,3):C.R2GC_370_918,(0,0,5):C.R2GC_370_919,(0,0,6):C.R2GC_370_920,(0,0,7):C.R2GC_370_921,(0,0,8):C.R2GC_370_922,(0,0,9):C.R2GC_370_923,(0,0,10):C.R2GC_370_924,(0,0,4):C.R2GC_370_925})

V_142 = CTVertex(name = 'V_142',
                 type = 'R2',
                 particles = [ P.g, P.g, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_143_52,(0,0,1):C.R2GC_143_53,(0,0,2):C.R2GC_143_54,(0,0,3):C.R2GC_143_55,(0,0,4):C.R2GC_143_56,(0,0,5):C.R2GC_143_57})

V_143 = CTVertex(name = 'V_143',
                 type = 'R2',
                 particles = [ P.a, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [P.G__plus__, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_299_593})

V_144 = CTVertex(name = 'V_144',
                 type = 'R2',
                 particles = [ P.a, P.a, P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_146_68,(0,0,1):C.R2GC_146_69,(0,0,2):C.R2GC_146_70,(0,0,3):C.R2GC_146_71})

V_145 = CTVertex(name = 'V_145',
                 type = 'R2',
                 particles = [ P.a, P.a, P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_151_95,(0,0,1):C.R2GC_151_96,(0,0,2):C.R2GC_151_97,(0,0,3):C.R2GC_151_98})

V_146 = CTVertex(name = 'V_146',
                 type = 'R2',
                 particles = [ P.a, P.a, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_150_91,(0,0,1):C.R2GC_150_92,(0,0,2):C.R2GC_150_93,(0,0,3):C.R2GC_150_94})

V_147 = CTVertex(name = 'V_147',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_149_87,(0,0,1):C.R2GC_149_88,(0,0,2):C.R2GC_149_89,(0,0,3):C.R2GC_149_90})

V_148 = CTVertex(name = 'V_148',
                 type = 'R2',
                 particles = [ P.Z, P.Z, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_148_82,(0,0,1):C.R2GC_148_83,(0,0,2):C.R2GC_148_84,(0,0,3):C.R2GC_148_85,(0,0,4):C.R2GC_148_86})

V_149 = CTVertex(name = 'V_149',
                 type = 'R2',
                 particles = [ P.a, P.a, P.g, P.g ],
                 color = [ 'Identity(3,4)' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_123_12,(0,0,1):C.R2GC_123_13})

V_150 = CTVertex(name = 'V_150',
                 type = 'R2',
                 particles = [ P.g, P.g, P.W__minus__, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_157_107})

V_151 = CTVertex(name = 'V_151',
                 type = 'R2',
                 particles = [ P.a, P.g, P.g, P.Z ],
                 color = [ 'Identity(2,3)' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_139_44,(0,0,1):C.R2GC_139_45})

V_152 = CTVertex(name = 'V_152',
                 type = 'R2',
                 particles = [ P.g, P.g, P.Z, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_142_50,(0,0,1):C.R2GC_142_51})

V_153 = CTVertex(name = 'V_153',
                 type = 'R2',
                 particles = [ P.a, P.g, P.g, P.g ],
                 color = [ 'd(2,3,4)' ],
                 lorentz = [ L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_124_14,(0,0,1):C.R2GC_124_15})

V_154 = CTVertex(name = 'V_154',
                 type = 'R2',
                 particles = [ P.g, P.g, P.g, P.Z ],
                 color = [ 'd(1,2,3)', 'f(1,2,3)' ],
                 lorentz = [ L.VVVV1, L.VVVV8 ],
                 loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                 couplings = {(1,0,0):C.R2GC_141_48,(1,0,1):C.R2GC_141_49,(0,1,0):C.R2GC_140_46,(0,1,1):C.R2GC_140_47})

V_155 = CTVertex(name = 'V_155',
                 type = 'R2',
                 particles = [ P.a, P.a, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_163_117,(0,0,1):C.R2GC_163_118,(0,0,2):C.R2GC_163_119,(0,0,3):C.R2GC_163_120,(0,0,5):C.R2GC_163_121,(0,0,6):C.R2GC_163_122,(0,0,7):C.R2GC_163_123,(0,0,8):C.R2GC_163_124,(0,0,9):C.R2GC_163_125,(0,0,10):C.R2GC_163_126,(0,0,4):C.R2GC_163_127})

V_156 = CTVertex(name = 'V_156',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_352_744,(0,0,1):C.R2GC_352_745,(0,0,2):C.R2GC_352_746,(0,0,3):C.R2GC_352_747,(0,0,5):C.R2GC_352_748,(0,0,6):C.R2GC_352_749,(0,0,7):C.R2GC_352_750,(0,0,8):C.R2GC_352_751,(0,0,9):C.R2GC_352_752,(0,0,10):C.R2GC_352_753,(0,0,4):C.R2GC_352_754})

V_157 = CTVertex(name = 'V_157',
                 type = 'R2',
                 particles = [ P.g, P.g, P.H, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_144_58,(0,0,1):C.R2GC_144_59,(0,0,2):C.R2GC_144_60,(0,0,3):C.R2GC_144_61,(0,0,4):C.R2GC_144_62,(0,0,5):C.R2GC_144_63})

V_158 = CTVertex(name = 'V_158',
                 type = 'R2',
                 particles = [ P.a, P.a, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_163_117,(0,0,1):C.R2GC_163_118,(0,0,2):C.R2GC_163_119,(0,0,3):C.R2GC_163_120,(0,0,5):C.R2GC_163_121,(0,0,6):C.R2GC_163_122,(0,0,7):C.R2GC_163_123,(0,0,8):C.R2GC_163_124,(0,0,9):C.R2GC_163_125,(0,0,10):C.R2GC_163_126,(0,0,4):C.R2GC_163_127})

V_159 = CTVertex(name = 'V_159',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_352_744,(0,0,1):C.R2GC_352_745,(0,0,2):C.R2GC_352_746,(0,0,3):C.R2GC_352_747,(0,0,5):C.R2GC_352_748,(0,0,6):C.R2GC_352_749,(0,0,7):C.R2GC_352_750,(0,0,8):C.R2GC_352_751,(0,0,9):C.R2GC_352_752,(0,0,10):C.R2GC_352_753,(0,0,4):C.R2GC_352_754})

V_160 = CTVertex(name = 'V_160',
                 type = 'R2',
                 particles = [ P.g, P.g, P.G0, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_144_58,(0,0,1):C.R2GC_144_59,(0,0,2):C.R2GC_144_60,(0,0,3):C.R2GC_144_61,(0,0,4):C.R2GC_144_62,(0,0,5):C.R2GC_144_63})

V_161 = CTVertex(name = 'V_161',
                 type = 'R2',
                 particles = [ P.W__minus__, P.W__minus__, P.G__plus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.a, P.G0, P.G__plus__] ], [ [P.a, P.G0, P.W__plus__] ], [ [P.a, P.G__plus__, P.H] ], [ [P.a, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,5):C.R2GC_181_228,(0,0,8):C.R2GC_181_229,(0,0,0):C.R2GC_181_230,(0,0,1):C.R2GC_181_231,(0,0,2):C.R2GC_181_232,(0,0,3):C.R2GC_181_233,(0,0,4):C.R2GC_181_234,(0,0,6):C.R2GC_181_235,(0,0,7):C.R2GC_181_236,(0,0,9):C.R2GC_181_237})

V_162 = CTVertex(name = 'V_162',
                 type = 'R2',
                 particles = [ P.g, P.g, P.G__minus__, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b, P.t] ], [ [P.c, P.s] ], [ [P.d, P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_158_108,(0,0,1):C.R2GC_158_109,(0,0,2):C.R2GC_158_110})

V_163 = CTVertex(name = 'V_163',
                 type = 'R2',
                 particles = [ P.W__plus__, P.W__plus__, P.G__minus__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.a, P.G0, P.G__plus__] ], [ [P.a, P.G0, P.W__plus__] ], [ [P.a, P.G__plus__, P.H] ], [ [P.a, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,5):C.R2GC_181_228,(0,0,8):C.R2GC_181_229,(0,0,0):C.R2GC_181_230,(0,0,1):C.R2GC_181_231,(0,0,2):C.R2GC_181_232,(0,0,3):C.R2GC_181_233,(0,0,4):C.R2GC_181_234,(0,0,6):C.R2GC_181_235,(0,0,7):C.R2GC_181_236,(0,0,9):C.R2GC_181_237})

V_164 = CTVertex(name = 'V_164',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_252_70})

V_165 = CTVertex(name = 'V_165',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_248_67})

V_166 = CTVertex(name = 'V_166',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__minus__, P.G__plus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_251_69})

V_167 = CTVertex(name = 'V_167',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_249_68})

V_168 = CTVertex(name = 'V_168',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__plus__, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_249_68})

V_169 = CTVertex(name = 'V_169',
                 type = 'UV',
                 particles = [ P.H, P.H, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_253_71})

V_170 = CTVertex(name = 'V_170',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_360_174})

V_171 = CTVertex(name = 'V_171',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_360_174})

V_172 = CTVertex(name = 'V_172',
                 type = 'UV',
                 particles = [ P.H, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_362_175})

V_173 = CTVertex(name = 'V_173',
                 type = 'UV',
                 particles = [ P.a, P.a, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_322_137})

V_174 = CTVertex(name = 'V_174',
                 type = 'UV',
                 particles = [ P.a, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_309_126})

V_175 = CTVertex(name = 'V_175',
                 type = 'UV',
                 particles = [ P.ghA, P.ghWm__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_218_37})

V_176 = CTVertex(name = 'V_176',
                 type = 'UV',
                 particles = [ P.ghA, P.ghWp__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_219_38})

V_177 = CTVertex(name = 'V_177',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghA__tilde__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_246_65})

V_178 = CTVertex(name = 'V_178',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghA__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_218_37})

V_179 = CTVertex(name = 'V_179',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_294_111})

V_180 = CTVertex(name = 'V_180',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_295_112})

V_181 = CTVertex(name = 'V_181',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_265_82})

V_182 = CTVertex(name = 'V_182',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_286_103})

V_183 = CTVertex(name = 'V_183',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghZ__tilde__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_350_165})

V_184 = CTVertex(name = 'V_184',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghZ__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_288_105})

V_185 = CTVertex(name = 'V_185',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghA__tilde__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_245_64})

V_186 = CTVertex(name = 'V_186',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghA__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_219_38})

V_187 = CTVertex(name = 'V_187',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_293_110})

V_188 = CTVertex(name = 'V_188',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_295_112})

V_189 = CTVertex(name = 'V_189',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_263_80})

V_190 = CTVertex(name = 'V_190',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_289_106})

V_191 = CTVertex(name = 'V_191',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghZ__tilde__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_349_164})

V_192 = CTVertex(name = 'V_192',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghZ__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_285_102})

V_193 = CTVertex(name = 'V_193',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWm__tilde__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_297_114})

V_194 = CTVertex(name = 'V_194',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWm__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_288_105})

V_195 = CTVertex(name = 'V_195',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWp__tilde__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_296_113})

V_196 = CTVertex(name = 'V_196',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWp__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_285_102})

V_197 = CTVertex(name = 'V_197',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghZ__tilde__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_351_166})

V_198 = CTVertex(name = 'V_198',
                 type = 'UV',
                 particles = [ P.ghG, P.ghG__tilde__, P.g ],
                 color = [ 'f(1,2,3)' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_222_41})

V_199 = CTVertex(name = 'V_199',
                 type = 'UV',
                 particles = [ P.g, P.g, P.g ],
                 color = [ 'f(1,2,3)' ],
                 lorentz = [ L.VVV7 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_221_40})

V_200 = CTVertex(name = 'V_200',
                 type = 'UV',
                 particles = [ P.g, P.g, P.g, P.g ],
                 color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
                 lorentz = [ L.VVVV4, L.VVVV6, L.VVVV7 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(1,1,0):C.UVGC_235_54,(0,0,0):C.UVGC_235_54,(2,2,0):C.UVGC_235_54})

V_201 = CTVertex(name = 'V_201',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.G0, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_283_100})

V_202 = CTVertex(name = 'V_202',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_284_101})

V_203 = CTVertex(name = 'V_203',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_365_178})

V_204 = CTVertex(name = 'V_204',
                 type = 'UV',
                 particles = [ P.W__minus__, P.G0, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_273_90})

V_205 = CTVertex(name = 'V_205',
                 type = 'UV',
                 particles = [ P.W__minus__, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_275_92})

V_206 = CTVertex(name = 'V_206',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVV1, L.VVV2, L.VVV3, L.VVV4, L.VVV5, L.VVV6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_266_83,(0,1,0):C.UVGC_264_81,(0,2,0):C.UVGC_264_81,(0,3,0):C.UVGC_266_83,(0,4,0):C.UVGC_266_83,(0,5,0):C.UVGC_264_81})

V_207 = CTVertex(name = 'V_207',
                 type = 'UV',
                 particles = [ P.a, P.W__plus__, P.G0, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_283_100})

V_208 = CTVertex(name = 'V_208',
                 type = 'UV',
                 particles = [ P.a, P.W__plus__, P.G__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_282_99})

V_209 = CTVertex(name = 'V_209',
                 type = 'UV',
                 particles = [ P.a, P.W__plus__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_366_179})

V_210 = CTVertex(name = 'V_210',
                 type = 'UV',
                 particles = [ P.W__plus__, P.G0, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS1, L.VSS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_274_91,(0,1,0):C.UVGC_273_90})

V_211 = CTVertex(name = 'V_211',
                 type = 'UV',
                 particles = [ P.W__plus__, P.G__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS1, L.VSS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_275_92,(0,1,0):C.UVGC_272_89})

V_212 = CTVertex(name = 'V_212',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_254_72})

V_213 = CTVertex(name = 'V_213',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_254_72})

V_214 = CTVertex(name = 'V_214',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_256_73})

V_215 = CTVertex(name = 'V_215',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_364_177})

V_216 = CTVertex(name = 'V_216',
                 type = 'UV',
                 particles = [ P.a, P.a, P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_267_84,(0,1,0):C.UVGC_267_84,(0,2,0):C.UVGC_268_85})

V_217 = CTVertex(name = 'V_217',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVV1, L.VVV2, L.VVV3, L.VVV4, L.VVV5, L.VVV6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_287_104,(0,1,0):C.UVGC_290_107,(0,2,0):C.UVGC_290_107,(0,3,0):C.UVGC_287_104,(0,4,0):C.UVGC_287_104,(0,5,0):C.UVGC_290_107})

V_218 = CTVertex(name = 'V_218',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_257_74,(0,1,0):C.UVGC_257_74,(0,2,0):C.UVGC_258_75})

V_219 = CTVertex(name = 'V_219',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.d, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_381_194,(0,1,0):C.UVGC_404_217})

V_220 = CTVertex(name = 'V_220',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.s, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_393_206,(0,1,0):C.UVGC_376_189})

V_221 = CTVertex(name = 'V_221',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.b, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_373_186,(0,1,0):C.UVGC_396_209})

V_222 = CTVertex(name = 'V_222',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_383_196})

V_223 = CTVertex(name = 'V_223',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_395_208})

V_224 = CTVertex(name = 'V_224',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_375_188})

V_225 = CTVertex(name = 'V_225',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_382_195,(0,1,0):C.UVGC_382_195})

V_226 = CTVertex(name = 'V_226',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_394_207,(0,1,0):C.UVGC_394_207})

V_227 = CTVertex(name = 'V_227',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_374_187,(0,1,0):C.UVGC_374_187})

V_228 = CTVertex(name = 'V_228',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.u, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_405_218,(0,1,0):C.UVGC_380_193})

V_229 = CTVertex(name = 'V_229',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.c, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_377_190,(0,1,0):C.UVGC_392_205})

V_230 = CTVertex(name = 'V_230',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.t, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_397_210,(0,1,0):C.UVGC_372_185})

V_231 = CTVertex(name = 'V_231',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.e__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_385_198})

V_232 = CTVertex(name = 'V_232',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.mu__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_389_202})

V_233 = CTVertex(name = 'V_233',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.ta__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_401_214})

V_234 = CTVertex(name = 'V_234',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_387_200})

V_235 = CTVertex(name = 'V_235',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_391_204})

V_236 = CTVertex(name = 'V_236',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_403_216})

V_237 = CTVertex(name = 'V_237',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_386_199,(0,1,0):C.UVGC_386_199})

V_238 = CTVertex(name = 'V_238',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_390_203,(0,1,0):C.UVGC_390_203})

V_239 = CTVertex(name = 'V_239',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_402_215,(0,1,0):C.UVGC_402_215})

V_240 = CTVertex(name = 'V_240',
                 type = 'UV',
                 particles = [ P.e__plus__, P.ve, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_384_197})

V_241 = CTVertex(name = 'V_241',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.vm, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_388_201})

V_242 = CTVertex(name = 'V_242',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.vt, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_400_213})

V_243 = CTVertex(name = 'V_243',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_406_219})

V_244 = CTVertex(name = 'V_244',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_378_191})

V_245 = CTVertex(name = 'V_245',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_398_211})

V_246 = CTVertex(name = 'V_246',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_407_220,(0,1,0):C.UVGC_407_220})

V_247 = CTVertex(name = 'V_247',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_379_192,(0,1,0):C.UVGC_379_192})

V_248 = CTVertex(name = 'V_248',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_399_212,(0,1,0):C.UVGC_399_212})

V_249 = CTVertex(name = 'V_249',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_353_168})

V_250 = CTVertex(name = 'V_250',
                 type = 'UV',
                 particles = [ P.Z, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS1, L.VSS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_324_139,(0,1,0):C.UVGC_348_163})

V_251 = CTVertex(name = 'V_251',
                 type = 'UV',
                 particles = [ P.Z, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS1, L.VSS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_335_150,(0,1,0):C.UVGC_334_149})

V_252 = CTVertex(name = 'V_252',
                 type = 'UV',
                 particles = [ P.W__minus__, P.Z, P.G0, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_261_78})

V_253 = CTVertex(name = 'V_253',
                 type = 'UV',
                 particles = [ P.W__minus__, P.Z, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_260_77})

V_254 = CTVertex(name = 'V_254',
                 type = 'UV',
                 particles = [ P.W__minus__, P.Z, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_368_181})

V_255 = CTVertex(name = 'V_255',
                 type = 'UV',
                 particles = [ P.W__plus__, P.Z, P.G0, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_261_78})

V_256 = CTVertex(name = 'V_256',
                 type = 'UV',
                 particles = [ P.W__plus__, P.Z, P.G__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_262_79})

V_257 = CTVertex(name = 'V_257',
                 type = 'UV',
                 particles = [ P.W__plus__, P.Z, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_367_180})

V_258 = CTVertex(name = 'V_258',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.W__plus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_292_109,(0,1,0):C.UVGC_291_108,(0,2,0):C.UVGC_291_108})

V_259 = CTVertex(name = 'V_259',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_354_169})

V_260 = CTVertex(name = 'V_260',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_355_170})

V_261 = CTVertex(name = 'V_261',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_356_171})

V_262 = CTVertex(name = 'V_262',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_371_184})

V_263 = CTVertex(name = 'V_263',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_270_87,(0,1,0):C.UVGC_270_87,(0,2,0):C.UVGC_271_88})

V_264 = CTVertex(name = 'V_264',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_310_127,(0,1,0):C.UVGC_319_134})

V_265 = CTVertex(name = 'V_265',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_311_128,(0,1,0):C.UVGC_320_135})

V_266 = CTVertex(name = 'V_266',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_312_129,(0,1,0):C.UVGC_321_136})

V_267 = CTVertex(name = 'V_267',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_305_122,(0,1,0):C.UVGC_318_133})

V_268 = CTVertex(name = 'V_268',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_303_120,(0,1,0):C.UVGC_316_131})

V_269 = CTVertex(name = 'V_269',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_304_121,(0,1,0):C.UVGC_317_132})

V_270 = CTVertex(name = 'V_270',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_301_118,(0,1,0):C.UVGC_307_124})

V_271 = CTVertex(name = 'V_271',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_302_119,(0,1,0):C.UVGC_308_125})

V_272 = CTVertex(name = 'V_272',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_300_117,(0,1,0):C.UVGC_306_123})

V_273 = CTVertex(name = 'V_273',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_233_52,(0,1,0):C.UVGC_234_53})

V_274 = CTVertex(name = 'V_274',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_225_44,(0,1,0):C.UVGC_226_45})

V_275 = CTVertex(name = 'V_275',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_231_50,(0,1,0):C.UVGC_232_51})

V_276 = CTVertex(name = 'V_276',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_227_46,(0,1,0):C.UVGC_228_47})

V_277 = CTVertex(name = 'V_277',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_229_48,(0,1,0):C.UVGC_230_49})

V_278 = CTVertex(name = 'V_278',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_223_42,(0,1,0):C.UVGC_224_43})

V_279 = CTVertex(name = 'V_279',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_278_95})

V_280 = CTVertex(name = 'V_280',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_276_93})

V_281 = CTVertex(name = 'V_281',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_277_94})

V_282 = CTVertex(name = 'V_282',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_278_95})

V_283 = CTVertex(name = 'V_283',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_276_93})

V_284 = CTVertex(name = 'V_284',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_277_94})

V_285 = CTVertex(name = 'V_285',
                 type = 'UV',
                 particles = [ P.e__plus__, P.ve, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_279_96})

V_286 = CTVertex(name = 'V_286',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.vm, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_280_97})

V_287 = CTVertex(name = 'V_287',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.vt, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_281_98})

V_288 = CTVertex(name = 'V_288',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_279_96})

V_289 = CTVertex(name = 'V_289',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.mu__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_280_97})

V_290 = CTVertex(name = 'V_290',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.ta__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_281_98})

V_291 = CTVertex(name = 'V_291',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_330_145,(0,1,0):C.UVGC_344_159})

V_292 = CTVertex(name = 'V_292',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_326_141,(0,1,0):C.UVGC_342_157})

V_293 = CTVertex(name = 'V_293',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_329_144,(0,1,0):C.UVGC_343_158})

V_294 = CTVertex(name = 'V_294',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_327_142,(0,1,0):C.UVGC_332_147})

V_295 = CTVertex(name = 'V_295',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_328_143,(0,1,0):C.UVGC_333_148})

V_296 = CTVertex(name = 'V_296',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_325_140,(0,1,0):C.UVGC_331_146})

V_297 = CTVertex(name = 'V_297',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.ve, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_339_154})

V_298 = CTVertex(name = 'V_298',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.vm, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_340_155})

V_299 = CTVertex(name = 'V_299',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.vt, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_341_156})

V_300 = CTVertex(name = 'V_300',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_336_151,(0,1,0):C.UVGC_345_160})

V_301 = CTVertex(name = 'V_301',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_337_152,(0,1,0):C.UVGC_346_161})

V_302 = CTVertex(name = 'V_302',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_338_153,(0,1,0):C.UVGC_347_162})

V_303 = CTVertex(name = 'V_303',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_239_58,(0,3,0):C.UVGC_239_58,(0,2,0):C.UVGC_203_22,(0,4,0):C.UVGC_204_23,(0,0,0):C.UVGC_191_10})

V_304 = CTVertex(name = 'V_304',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.ve ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_215_34})

V_305 = CTVertex(name = 'V_305',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_240_59,(0,3,0):C.UVGC_240_59,(0,2,0):C.UVGC_205_24,(0,4,0):C.UVGC_206_25,(0,0,0):C.UVGC_192_11})

V_306 = CTVertex(name = 'V_306',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.vm ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_216_35})

V_307 = CTVertex(name = 'V_307',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_243_62,(0,3,0):C.UVGC_243_62,(0,2,0):C.UVGC_209_28,(0,4,0):C.UVGC_210_29,(0,0,0):C.UVGC_195_14})

V_308 = CTVertex(name = 'V_308',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.vt ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_217_36})

V_309 = CTVertex(name = 'V_309',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_244_63,(0,3,0):C.UVGC_244_63,(0,2,0):C.UVGC_213_32,(0,4,0):C.UVGC_214_33,(0,0,0):C.UVGC_196_15})

V_310 = CTVertex(name = 'V_310',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_238_57,(0,3,0):C.UVGC_238_57,(0,2,0):C.UVGC_201_20,(0,4,0):C.UVGC_202_21,(0,0,0):C.UVGC_190_9})

V_311 = CTVertex(name = 'V_311',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_237_56,(0,3,0):C.UVGC_237_56,(0,2,0):C.UVGC_199_18,(0,4,0):C.UVGC_200_19,(0,0,0):C.UVGC_189_8})

V_312 = CTVertex(name = 'V_312',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_241_60,(0,3,0):C.UVGC_241_60,(0,2,0):C.UVGC_207_26,(0,4,0):C.UVGC_208_27,(0,0,0):C.UVGC_193_12})

V_313 = CTVertex(name = 'V_313',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_242_61,(0,3,0):C.UVGC_242_61,(0,2,0):C.UVGC_211_30,(0,4,0):C.UVGC_212_31,(0,0,0):C.UVGC_194_13})

V_314 = CTVertex(name = 'V_314',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_236_55,(0,3,0):C.UVGC_236_55,(0,2,0):C.UVGC_197_16,(0,4,0):C.UVGC_198_17,(0,0,0):C.UVGC_188_7})

V_315 = CTVertex(name = 'V_315',
                 type = 'UV',
                 particles = [ P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_359_173,(0,1,0):C.UVGC_184_3})

V_316 = CTVertex(name = 'V_316',
                 type = 'UV',
                 particles = [ P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_357_172})

V_317 = CTVertex(name = 'V_317',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_357_172})

V_318 = CTVertex(name = 'V_318',
                 type = 'UV',
                 particles = [ P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_182_1})

V_319 = CTVertex(name = 'V_319',
                 type = 'UV',
                 particles = [ P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_247_66,(0,1,0):C.UVGC_220_39})

V_320 = CTVertex(name = 'V_320',
                 type = 'UV',
                 particles = [ P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_369_182,(0,1,0):C.UVGC_186_5})

V_321 = CTVertex(name = 'V_321',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_363_176,(0,1,0):C.UVGC_185_4})

V_322 = CTVertex(name = 'V_322',
                 type = 'UV',
                 particles = [ P.g, P.g ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_183_2})

V_323 = CTVertex(name = 'V_323',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.ve, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_313_130})

V_324 = CTVertex(name = 'V_324',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.vm, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_313_130})

V_325 = CTVertex(name = 'V_325',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.vt, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_313_130})

V_326 = CTVertex(name = 'V_326',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_370_183})

V_327 = CTVertex(name = 'V_327',
                 type = 'UV',
                 particles = [ P.a, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_299_116})

V_328 = CTVertex(name = 'V_328',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_352_167})

V_329 = CTVertex(name = 'V_329',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_352_167})

V_330 = CTVertex(name = 'V_330',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__ ],
                 color = [ '1' ],
                 lorentz = [ L.UU1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_269_86})

V_331 = CTVertex(name = 'V_331',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__ ],
                 color = [ '1' ],
                 lorentz = [ L.UU1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_269_86})

V_332 = CTVertex(name = 'V_332',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghZ__tilde__ ],
                 color = [ '1' ],
                 lorentz = [ L.UU1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_323_138})

V_333 = CTVertex(name = 'V_333',
                 type = 'UV',
                 particles = [ P.a, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_187_6})

V_334 = CTVertex(name = 'V_334',
                 type = 'UV',
                 particles = [ P.W__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_259_76})

V_335 = CTVertex(name = 'V_335',
                 type = 'UV',
                 particles = [ P.W__plus__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_259_76})

V_336 = CTVertex(name = 'V_336',
                 type = 'UV',
                 particles = [ P.Z, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_298_115})
