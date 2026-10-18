# This file was automatically created by FeynRules 2.3.49
# Mathematica version: 14.2.1 for Mac OS X ARM (64-bit) (March 16, 2025)
# Date: Sun 18 Oct 2026 13:10:29


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
               couplings = {(0,0,0):C.R2GC_420_1218,(0,0,1):C.R2GC_420_1219,(0,0,2):C.R2GC_420_1220,(0,0,3):C.R2GC_420_1221,(0,0,6):C.R2GC_420_1222,(0,0,7):C.R2GC_420_1223,(0,0,8):C.R2GC_420_1224,(0,0,9):C.R2GC_420_1225,(0,0,10):C.R2GC_420_1226,(0,0,11):C.R2GC_420_1227,(0,0,12):C.R2GC_420_1228,(0,0,4):C.R2GC_420_1229,(0,0,5):C.R2GC_420_1230})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.G0, P.G0, P.G__minus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
               couplings = {(0,0,26):C.R2GC_416_1097,(0,0,28):C.R2GC_416_1098,(0,0,0):C.R2GC_416_1099,(0,0,2):C.R2GC_416_1100,(0,0,3):C.R2GC_416_1101,(0,0,4):C.R2GC_416_1102,(0,0,5):C.R2GC_416_1103,(0,0,6):C.R2GC_416_1104,(0,0,7):C.R2GC_416_1105,(0,0,8):C.R2GC_416_1106,(0,0,9):C.R2GC_416_1107,(0,0,10):C.R2GC_416_1108,(0,0,12):C.R2GC_416_1109,(0,0,16):C.R2GC_416_1110,(0,0,18):C.R2GC_416_1111,(0,0,19):C.R2GC_416_1112,(0,0,21):C.R2GC_416_1113,(0,0,22):C.R2GC_416_1114,(0,0,23):C.R2GC_416_1115,(0,0,24):C.R2GC_416_1116,(0,0,25):C.R2GC_416_1117,(0,0,27):C.R2GC_416_1118,(0,0,1):C.R2GC_416_1119,(0,0,11):C.R2GC_416_1120,(0,0,13):C.R2GC_416_1121,(0,0,15):C.R2GC_416_1122,(0,0,17):C.R2GC_416_1123,(0,0,20):C.R2GC_416_1124,(0,0,14):C.R2GC_416_1125})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.G__minus__, P.G__minus__, P.G__plus__, P.G__plus__ ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.a] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b, P.c] ], [ [P.b, P.c, P.d] ], [ [P.b, P.c, P.d, P.t] ], [ [P.b, P.c, P.d, P.u] ], [ [P.b, P.c, P.s] ], [ [P.b, P.c, P.s, P.t] ], [ [P.b, P.c, P.s, P.u] ], [ [P.b, P.c, P.t] ], [ [P.b, P.c, P.u] ], [ [P.b, P.d, P.t] ], [ [P.b, P.d, P.t, P.u] ], [ [P.b, P.d, P.u] ], [ [P.b, P.s, P.t] ], [ [P.b, P.s, P.t, P.u] ], [ [P.b, P.s, P.u] ], [ [P.b, P.t] ], [ [P.b, P.t, P.u] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.d, P.s] ], [ [P.c, P.d, P.s, P.t] ], [ [P.c, P.d, P.s, P.u] ], [ [P.c, P.d, P.t] ], [ [P.c, P.d, P.u] ], [ [P.c, P.s] ], [ [P.c, P.s, P.t] ], [ [P.c, P.s, P.u] ], [ [P.d, P.s, P.t] ], [ [P.d, P.s, P.t, P.u] ], [ [P.d, P.s, P.u] ], [ [P.d, P.t] ], [ [P.d, P.t, P.u] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.t, P.u] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_419_1170,(0,0,46):C.R2GC_419_1171,(0,0,47):C.R2GC_419_1172,(0,0,1):C.R2GC_419_1173,(0,0,3):C.R2GC_419_1174,(0,0,4):C.R2GC_419_1175,(0,0,19):C.R2GC_419_1176,(0,0,21):C.R2GC_419_1177,(0,0,22):C.R2GC_419_1178,(0,0,28):C.R2GC_419_1179,(0,0,34):C.R2GC_419_1180,(0,0,36):C.R2GC_419_1181,(0,0,37):C.R2GC_419_1182,(0,0,38):C.R2GC_419_1183,(0,0,39):C.R2GC_419_1184,(0,0,40):C.R2GC_419_1185,(0,0,41):C.R2GC_419_1186,(0,0,42):C.R2GC_419_1187,(0,0,44):C.R2GC_419_1188,(0,0,45):C.R2GC_419_1189,(0,0,2):C.R2GC_419_1190,(0,0,5):C.R2GC_419_1191,(0,0,8):C.R2GC_419_1192,(0,0,11):C.R2GC_419_1193,(0,0,12):C.R2GC_419_1194,(0,0,13):C.R2GC_419_1195,(0,0,15):C.R2GC_419_1196,(0,0,16):C.R2GC_419_1197,(0,0,18):C.R2GC_419_1198,(0,0,20):C.R2GC_419_1199,(0,0,23):C.R2GC_419_1200,(0,0,26):C.R2GC_419_1201,(0,0,27):C.R2GC_419_1202,(0,0,29):C.R2GC_419_1203,(0,0,30):C.R2GC_419_1204,(0,0,31):C.R2GC_419_1205,(0,0,33):C.R2GC_419_1206,(0,0,35):C.R2GC_419_1207,(0,0,43):C.R2GC_419_1208,(0,0,6):C.R2GC_419_1209,(0,0,7):C.R2GC_419_1210,(0,0,9):C.R2GC_419_1211,(0,0,10):C.R2GC_419_1212,(0,0,14):C.R2GC_419_1213,(0,0,17):C.R2GC_419_1214,(0,0,24):C.R2GC_419_1215,(0,0,25):C.R2GC_419_1216,(0,0,32):C.R2GC_419_1217})

V_4 = CTVertex(name = 'V_4',
               type = 'R2',
               particles = [ P.G0, P.G0, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_417_1126,(0,0,1):C.R2GC_417_1127,(0,0,2):C.R2GC_417_1128,(0,0,3):C.R2GC_417_1129,(0,0,8):C.R2GC_417_1130,(0,0,9):C.R2GC_417_1131,(0,0,10):C.R2GC_417_1132,(0,0,11):C.R2GC_417_1133,(0,0,12):C.R2GC_417_1134,(0,0,13):C.R2GC_417_1135,(0,0,14):C.R2GC_417_1136,(0,0,5):C.R2GC_417_1137,(0,0,6):C.R2GC_417_1138,(0,0,7):C.R2GC_417_1139,(0,0,4):C.R2GC_417_1140})

V_5 = CTVertex(name = 'V_5',
               type = 'R2',
               particles = [ P.G__minus__, P.G__plus__, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.W__plus__, P.Z] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
               couplings = {(0,0,26):C.R2GC_418_1141,(0,0,28):C.R2GC_418_1142,(0,0,0):C.R2GC_418_1143,(0,0,2):C.R2GC_418_1144,(0,0,3):C.R2GC_418_1145,(0,0,4):C.R2GC_418_1146,(0,0,5):C.R2GC_418_1147,(0,0,6):C.R2GC_418_1148,(0,0,7):C.R2GC_418_1149,(0,0,8):C.R2GC_418_1150,(0,0,9):C.R2GC_418_1151,(0,0,10):C.R2GC_418_1152,(0,0,14):C.R2GC_418_1153,(0,0,16):C.R2GC_418_1154,(0,0,18):C.R2GC_418_1155,(0,0,20):C.R2GC_418_1156,(0,0,21):C.R2GC_418_1157,(0,0,22):C.R2GC_418_1158,(0,0,23):C.R2GC_418_1159,(0,0,24):C.R2GC_418_1160,(0,0,25):C.R2GC_418_1161,(0,0,27):C.R2GC_418_1162,(0,0,1):C.R2GC_418_1163,(0,0,11):C.R2GC_418_1164,(0,0,13):C.R2GC_418_1165,(0,0,15):C.R2GC_418_1166,(0,0,17):C.R2GC_418_1167,(0,0,19):C.R2GC_418_1168,(0,0,12):C.R2GC_418_1169})

V_6 = CTVertex(name = 'V_6',
               type = 'R2',
               particles = [ P.H, P.H, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_421_1231,(0,0,1):C.R2GC_421_1232,(0,0,2):C.R2GC_421_1233,(0,0,3):C.R2GC_421_1234,(0,0,6):C.R2GC_421_1235,(0,0,7):C.R2GC_421_1236,(0,0,8):C.R2GC_421_1237,(0,0,9):C.R2GC_421_1238,(0,0,10):C.R2GC_421_1239,(0,0,11):C.R2GC_421_1240,(0,0,12):C.R2GC_421_1241,(0,0,4):C.R2GC_421_1242,(0,0,5):C.R2GC_421_1243})

V_7 = CTVertex(name = 'V_7',
               type = 'R2',
               particles = [ P.G0, P.G0, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_559_2263,(0,0,1):C.R2GC_559_2264,(0,0,2):C.R2GC_559_2265,(0,0,3):C.R2GC_559_2266,(0,0,7):C.R2GC_559_2267,(0,0,8):C.R2GC_559_2268,(0,0,9):C.R2GC_559_2269,(0,0,10):C.R2GC_559_2270,(0,0,11):C.R2GC_559_2271,(0,0,12):C.R2GC_559_2272,(0,0,13):C.R2GC_559_2273,(0,0,5):C.R2GC_559_2274,(0,0,6):C.R2GC_559_2275,(0,0,4):C.R2GC_559_2276})

V_8 = CTVertex(name = 'V_8',
               type = 'R2',
               particles = [ P.G__minus__, P.G__plus__, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
               couplings = {(0,0,21):C.R2GC_559_2272,(0,0,23):C.R2GC_560_2277,(0,0,0):C.R2GC_560_2278,(0,0,2):C.R2GC_205_358,(0,0,3):C.R2GC_560_2279,(0,0,4):C.R2GC_560_2280,(0,0,5):C.R2GC_560_2281,(0,0,6):C.R2GC_560_2282,(0,0,7):C.R2GC_560_2283,(0,0,8):C.R2GC_560_2284,(0,0,9):C.R2GC_560_2285,(0,0,10):C.R2GC_559_2266,(0,0,11):C.R2GC_560_2286,(0,0,15):C.R2GC_560_2287,(0,0,16):C.R2GC_560_2288,(0,0,17):C.R2GC_559_2267,(0,0,18):C.R2GC_560_2289,(0,0,19):C.R2GC_560_2290,(0,0,20):C.R2GC_559_2270,(0,0,22):C.R2GC_560_2291,(0,0,1):C.R2GC_560_2292,(0,0,12):C.R2GC_560_2293,(0,0,13):C.R2GC_560_2294,(0,0,14):C.R2GC_560_2295})

V_9 = CTVertex(name = 'V_9',
               type = 'R2',
               particles = [ P.H, P.H, P.H ],
               color = [ '1' ],
               lorentz = [ L.SSS1 ],
               loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
               couplings = {(0,0,0):C.R2GC_561_2296,(0,0,1):C.R2GC_561_2297,(0,0,2):C.R2GC_561_2298,(0,0,3):C.R2GC_561_2299,(0,0,6):C.R2GC_561_2300,(0,0,7):C.R2GC_561_2301,(0,0,8):C.R2GC_561_2302,(0,0,9):C.R2GC_561_2303,(0,0,10):C.R2GC_561_2304,(0,0,11):C.R2GC_561_2305,(0,0,12):C.R2GC_561_2306,(0,0,4):C.R2GC_561_2307,(0,0,5):C.R2GC_561_2308})

V_10 = CTVertex(name = 'V_10',
                type = 'R2',
                particles = [ P.a, P.a, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,16):C.R2GC_520_1977,(0,0,0):C.R2GC_520_1978,(0,0,1):C.R2GC_520_1979,(0,0,2):C.R2GC_520_1980,(0,0,3):C.R2GC_520_1981,(0,0,4):C.R2GC_520_1982,(0,0,5):C.R2GC_520_1983,(0,0,6):C.R2GC_520_1984,(0,0,7):C.R2GC_520_1985,(0,0,8):C.R2GC_520_1986,(0,0,9):C.R2GC_520_1987,(0,0,10):C.R2GC_520_1988,(0,0,11):C.R2GC_520_1989,(0,0,12):C.R2GC_520_1990,(0,0,13):C.R2GC_520_1991,(0,0,14):C.R2GC_520_1992,(0,0,15):C.R2GC_520_1993})

V_11 = CTVertex(name = 'V_11',
                type = 'R2',
                particles = [ P.a, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,0):C.R2GC_507_1942,(0,0,1):C.R2GC_507_1943,(0,0,2):C.R2GC_507_1944,(0,0,3):C.R2GC_507_1945,(0,0,4):C.R2GC_507_1946,(0,0,5):C.R2GC_507_1947,(0,0,6):C.R2GC_507_1948,(0,0,7):C.R2GC_507_1949,(0,0,8):C.R2GC_507_1950,(0,0,9):C.R2GC_507_1951,(0,0,10):C.R2GC_507_1952,(0,0,11):C.R2GC_507_1953,(0,0,12):C.R2GC_507_1954,(0,0,13):C.R2GC_507_1955,(0,0,14):C.R2GC_507_1956})

V_12 = CTVertex(name = 'V_12',
                type = 'R2',
                particles = [ P.g, P.g, P.g ],
                color = [ 'f(1,2,3)' ],
                lorentz = [ L.VVV1 ],
                loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
                couplings = {(0,0,0):C.R2GC_345_934,(0,0,1):C.R2GC_345_935})

V_13 = CTVertex(name = 'V_13',
                type = 'R2',
                particles = [ P.g, P.g, P.g, P.g ],
                color = [ 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.g] ] ],
                couplings = {(2,0,0):C.R2GC_149_1,(1,0,0):C.R2GC_150_2,(0,0,0):C.R2GC_151_3,(2,1,0):C.R2GC_152_4,(1,1,0):C.R2GC_153_5,(0,1,0):C.R2GC_154_6,(2,2,0):C.R2GC_155_7,(1,2,0):C.R2GC_156_8,(0,2,0):C.R2GC_157_9})

V_14 = CTVertex(name = 'V_14',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.G0, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_456_1653,(0,0,2):C.R2GC_456_1654,(0,0,3):C.R2GC_456_1655,(0,0,4):C.R2GC_456_1656,(0,0,5):C.R2GC_456_1657,(0,0,6):C.R2GC_456_1658,(0,0,7):C.R2GC_456_1659,(0,0,8):C.R2GC_456_1660,(0,0,9):C.R2GC_456_1661,(0,0,11):C.R2GC_456_1662,(0,0,14):C.R2GC_456_1663,(0,0,17):C.R2GC_456_1664,(0,0,18):C.R2GC_456_1665,(0,0,19):C.R2GC_456_1666,(0,0,20):C.R2GC_456_1667,(0,0,21):C.R2GC_456_1668,(0,0,0):C.R2GC_456_1669,(0,0,10):C.R2GC_456_1670,(0,0,12):C.R2GC_456_1671,(0,0,13):C.R2GC_456_1672,(0,0,15):C.R2GC_456_1673,(0,0,16):C.R2GC_456_1674})

V_15 = CTVertex(name = 'V_15',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.G__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_458_1697,(0,0,2):C.R2GC_458_1698,(0,0,3):C.R2GC_458_1699,(0,0,4):C.R2GC_458_1700,(0,0,5):C.R2GC_458_1701,(0,0,6):C.R2GC_458_1702,(0,0,7):C.R2GC_458_1703,(0,0,8):C.R2GC_458_1704,(0,0,9):C.R2GC_458_1705,(0,0,14):C.R2GC_458_1706,(0,0,16):C.R2GC_458_1707,(0,0,17):C.R2GC_458_1708,(0,0,18):C.R2GC_458_1709,(0,0,19):C.R2GC_458_1710,(0,0,20):C.R2GC_458_1711,(0,0,21):C.R2GC_458_1712,(0,0,0):C.R2GC_458_1713,(0,0,10):C.R2GC_458_1714,(0,0,11):C.R2GC_458_1715,(0,0,12):C.R2GC_458_1716,(0,0,13):C.R2GC_458_1717,(0,0,15):C.R2GC_458_1718})

V_16 = CTVertex(name = 'V_16',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_564_2342,(0,0,2):C.R2GC_564_2343,(0,0,3):C.R2GC_564_2344,(0,0,4):C.R2GC_564_2345,(0,0,5):C.R2GC_564_2346,(0,0,6):C.R2GC_564_2347,(0,0,7):C.R2GC_564_2348,(0,0,8):C.R2GC_564_2349,(0,0,10):C.R2GC_564_2350,(0,0,11):C.R2GC_564_2351,(0,0,12):C.R2GC_564_2352,(0,0,13):C.R2GC_564_2353,(0,0,0):C.R2GC_564_2354,(0,0,9):C.R2GC_564_2355})

V_17 = CTVertex(name = 'V_17',
                type = 'R2',
                particles = [ P.W__minus__, P.G0, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_439_1509,(0,0,2):C.R2GC_439_1510,(0,0,3):C.R2GC_439_1511,(0,0,4):C.R2GC_439_1512,(0,0,5):C.R2GC_439_1513,(0,0,6):C.R2GC_439_1514,(0,0,7):C.R2GC_439_1515,(0,0,8):C.R2GC_439_1516,(0,0,14):C.R2GC_439_1517,(0,0,15):C.R2GC_439_1518,(0,0,16):C.R2GC_439_1519,(0,0,17):C.R2GC_439_1520,(0,0,0):C.R2GC_439_1521,(0,0,9):C.R2GC_439_1522,(0,0,10):C.R2GC_439_1523,(0,0,11):C.R2GC_439_1524,(0,0,12):C.R2GC_439_1525,(0,0,13):C.R2GC_439_1526})

V_18 = CTVertex(name = 'V_18',
                type = 'R2',
                particles = [ P.W__minus__, P.G__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_441_1543,(0,0,2):C.R2GC_441_1544,(0,0,3):C.R2GC_441_1545,(0,0,4):C.R2GC_441_1546,(0,0,5):C.R2GC_441_1547,(0,0,6):C.R2GC_441_1548,(0,0,7):C.R2GC_441_1549,(0,0,8):C.R2GC_441_1550,(0,0,14):C.R2GC_441_1551,(0,0,15):C.R2GC_441_1552,(0,0,16):C.R2GC_441_1553,(0,0,17):C.R2GC_441_1554,(0,0,0):C.R2GC_441_1555,(0,0,9):C.R2GC_441_1556,(0,0,10):C.R2GC_441_1557,(0,0,11):C.R2GC_441_1558,(0,0,12):C.R2GC_441_1559,(0,0,13):C.R2GC_441_1560})

V_19 = CTVertex(name = 'V_19',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVV1 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_433_1452,(0,0,1):C.R2GC_433_1453,(0,0,2):C.R2GC_433_1454,(0,0,3):C.R2GC_433_1455,(0,0,4):C.R2GC_433_1456,(0,0,5):C.R2GC_433_1457,(0,0,6):C.R2GC_433_1458,(0,0,7):C.R2GC_433_1459,(0,0,8):C.R2GC_433_1460,(0,0,9):C.R2GC_433_1461,(0,0,10):C.R2GC_433_1462,(0,0,11):C.R2GC_433_1463})

V_20 = CTVertex(name = 'V_20',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_457_1675,(0,0,2):C.R2GC_457_1676,(0,0,3):C.R2GC_457_1677,(0,0,4):C.R2GC_457_1678,(0,0,5):C.R2GC_457_1679,(0,0,6):C.R2GC_457_1680,(0,0,7):C.R2GC_457_1681,(0,0,8):C.R2GC_457_1682,(0,0,9):C.R2GC_457_1683,(0,0,11):C.R2GC_457_1684,(0,0,14):C.R2GC_457_1685,(0,0,17):C.R2GC_457_1686,(0,0,18):C.R2GC_457_1687,(0,0,19):C.R2GC_457_1688,(0,0,20):C.R2GC_457_1689,(0,0,21):C.R2GC_457_1690,(0,0,0):C.R2GC_457_1691,(0,0,10):C.R2GC_457_1692,(0,0,12):C.R2GC_457_1693,(0,0,13):C.R2GC_457_1694,(0,0,15):C.R2GC_457_1695,(0,0,16):C.R2GC_457_1696})

V_21 = CTVertex(name = 'V_21',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_455_1631,(0,0,2):C.R2GC_455_1632,(0,0,3):C.R2GC_455_1633,(0,0,4):C.R2GC_455_1634,(0,0,5):C.R2GC_455_1635,(0,0,6):C.R2GC_455_1636,(0,0,7):C.R2GC_455_1637,(0,0,8):C.R2GC_455_1638,(0,0,9):C.R2GC_455_1639,(0,0,14):C.R2GC_455_1640,(0,0,16):C.R2GC_455_1641,(0,0,17):C.R2GC_455_1642,(0,0,18):C.R2GC_455_1643,(0,0,19):C.R2GC_455_1644,(0,0,20):C.R2GC_455_1645,(0,0,21):C.R2GC_455_1646,(0,0,0):C.R2GC_455_1647,(0,0,10):C.R2GC_455_1648,(0,0,11):C.R2GC_455_1649,(0,0,12):C.R2GC_455_1650,(0,0,13):C.R2GC_455_1651,(0,0,15):C.R2GC_455_1652})

V_22 = CTVertex(name = 'V_22',
                type = 'R2',
                particles = [ P.a, P.W__plus__, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_564_2353,(0,0,2):C.R2GC_565_2356,(0,0,3):C.R2GC_565_2357,(0,0,4):C.R2GC_565_2358,(0,0,5):C.R2GC_565_2359,(0,0,6):C.R2GC_565_2360,(0,0,7):C.R2GC_565_2361,(0,0,8):C.R2GC_565_2362,(0,0,10):C.R2GC_565_2363,(0,0,11):C.R2GC_565_2364,(0,0,12):C.R2GC_565_2365,(0,0,13):C.R2GC_564_2342,(0,0,0):C.R2GC_565_2366,(0,0,9):C.R2GC_565_2367})

V_23 = CTVertex(name = 'V_23',
                type = 'R2',
                particles = [ P.W__plus__, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_440_1527,(0,0,2):C.R2GC_440_1528,(0,0,3):C.R2GC_440_1529,(0,0,4):C.R2GC_440_1530,(0,0,5):C.R2GC_440_1531,(0,0,6):C.R2GC_440_1532,(0,0,7):C.R2GC_440_1533,(0,0,8):C.R2GC_440_1534,(0,0,14):C.R2GC_440_1535,(0,0,15):C.R2GC_440_1536,(0,0,16):C.R2GC_440_1537,(0,0,17):C.R2GC_440_1538,(0,0,0):C.R2GC_440_1539,(0,0,9):C.R2GC_439_1523,(0,0,10):C.R2GC_439_1522,(0,0,11):C.R2GC_440_1540,(0,0,12):C.R2GC_440_1541,(0,0,13):C.R2GC_440_1542})

V_24 = CTVertex(name = 'V_24',
                type = 'R2',
                particles = [ P.W__plus__, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS2 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,1):C.R2GC_441_1543,(0,0,2):C.R2GC_441_1544,(0,0,3):C.R2GC_441_1545,(0,0,4):C.R2GC_442_1561,(0,0,5):C.R2GC_441_1547,(0,0,6):C.R2GC_442_1562,(0,0,7):C.R2GC_441_1549,(0,0,8):C.R2GC_441_1550,(0,0,14):C.R2GC_441_1551,(0,0,15):C.R2GC_442_1563,(0,0,16):C.R2GC_441_1553,(0,0,17):C.R2GC_441_1554,(0,0,0):C.R2GC_441_1555,(0,0,9):C.R2GC_441_1556,(0,0,10):C.R2GC_441_1557,(0,0,11):C.R2GC_441_1558,(0,0,12):C.R2GC_441_1559,(0,0,13):C.R2GC_441_1560})

V_25 = CTVertex(name = 'V_25',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.G0, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.H, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,21):C.R2GC_422_1244,(0,0,23):C.R2GC_422_1245,(0,0,1):C.R2GC_422_1246,(0,0,2):C.R2GC_422_1247,(0,0,3):C.R2GC_422_1248,(0,0,4):C.R2GC_422_1249,(0,0,5):C.R2GC_422_1250,(0,0,6):C.R2GC_422_1251,(0,0,7):C.R2GC_422_1252,(0,0,8):C.R2GC_422_1253,(0,0,9):C.R2GC_422_1254,(0,0,13):C.R2GC_422_1255,(0,0,16):C.R2GC_422_1256,(0,0,17):C.R2GC_422_1257,(0,0,18):C.R2GC_422_1258,(0,0,19):C.R2GC_422_1259,(0,0,20):C.R2GC_422_1260,(0,0,22):C.R2GC_422_1261,(0,0,0):C.R2GC_422_1262,(0,0,10):C.R2GC_422_1263,(0,0,11):C.R2GC_422_1264,(0,0,12):C.R2GC_422_1265,(0,0,14):C.R2GC_422_1266,(0,0,15):C.R2GC_422_1267})

V_26 = CTVertex(name = 'V_26',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a] ], [ [P.a, P.G0, P.G__plus__] ], [ [P.a, P.G0, P.W__plus__] ], [ [P.a, P.G__plus__] ], [ [P.a, P.G__plus__, P.H] ], [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.G__plus__, P.W__plus__, P.Z] ], [ [P.a, P.G__plus__, P.Z] ], [ [P.a, P.H, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.a, P.W__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b, P.c] ], [ [P.b, P.c, P.d] ], [ [P.b, P.c, P.d, P.t] ], [ [P.b, P.c, P.d, P.u] ], [ [P.b, P.c, P.s] ], [ [P.b, P.c, P.s, P.t] ], [ [P.b, P.c, P.s, P.u] ], [ [P.b, P.c, P.t] ], [ [P.b, P.c, P.u] ], [ [P.b, P.d, P.t] ], [ [P.b, P.d, P.t, P.u] ], [ [P.b, P.d, P.u] ], [ [P.b, P.s, P.t] ], [ [P.b, P.s, P.t, P.u] ], [ [P.b, P.s, P.u] ], [ [P.b, P.t] ], [ [P.b, P.t, P.u] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.d, P.s] ], [ [P.c, P.d, P.s, P.t] ], [ [P.c, P.d, P.s, P.u] ], [ [P.c, P.d, P.t] ], [ [P.c, P.d, P.u] ], [ [P.c, P.s] ], [ [P.c, P.s, P.t] ], [ [P.c, P.s, P.u] ], [ [P.d, P.s, P.t] ], [ [P.d, P.s, P.t, P.u] ], [ [P.d, P.s, P.u] ], [ [P.d, P.t] ], [ [P.d, P.t, P.u] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.t, P.u] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_423_1268,(0,0,61):C.R2GC_423_1269,(0,0,63):C.R2GC_423_1270,(0,0,3):C.R2GC_423_1271,(0,0,9):C.R2GC_423_1272,(0,0,11):C.R2GC_423_1273,(0,0,12):C.R2GC_423_1274,(0,0,27):C.R2GC_423_1275,(0,0,29):C.R2GC_423_1276,(0,0,30):C.R2GC_423_1277,(0,0,36):C.R2GC_423_1278,(0,0,42):C.R2GC_423_1279,(0,0,44):C.R2GC_423_1280,(0,0,45):C.R2GC_423_1281,(0,0,48):C.R2GC_423_1282,(0,0,53):C.R2GC_423_1283,(0,0,54):C.R2GC_423_1284,(0,0,56):C.R2GC_423_1285,(0,0,57):C.R2GC_423_1286,(0,0,59):C.R2GC_423_1287,(0,0,60):C.R2GC_423_1288,(0,0,62):C.R2GC_423_1289,(0,0,1):C.R2GC_423_1290,(0,0,2):C.R2GC_423_1291,(0,0,4):C.R2GC_423_1292,(0,0,5):C.R2GC_423_1293,(0,0,7):C.R2GC_423_1294,(0,0,8):C.R2GC_423_1295,(0,0,10):C.R2GC_423_1296,(0,0,13):C.R2GC_423_1297,(0,0,16):C.R2GC_423_1298,(0,0,19):C.R2GC_423_1299,(0,0,20):C.R2GC_423_1300,(0,0,21):C.R2GC_423_1301,(0,0,23):C.R2GC_423_1302,(0,0,24):C.R2GC_423_1303,(0,0,26):C.R2GC_423_1304,(0,0,28):C.R2GC_423_1305,(0,0,31):C.R2GC_423_1306,(0,0,34):C.R2GC_423_1307,(0,0,35):C.R2GC_423_1308,(0,0,37):C.R2GC_423_1309,(0,0,38):C.R2GC_423_1310,(0,0,39):C.R2GC_423_1311,(0,0,41):C.R2GC_423_1312,(0,0,43):C.R2GC_423_1313,(0,0,46):C.R2GC_423_1314,(0,0,47):C.R2GC_423_1315,(0,0,49):C.R2GC_423_1316,(0,0,50):C.R2GC_423_1317,(0,0,51):C.R2GC_423_1318,(0,0,52):C.R2GC_423_1319,(0,0,55):C.R2GC_423_1320,(0,0,58):C.R2GC_423_1321,(0,0,6):C.R2GC_423_1322,(0,0,14):C.R2GC_423_1323,(0,0,15):C.R2GC_423_1324,(0,0,17):C.R2GC_423_1325,(0,0,18):C.R2GC_423_1326,(0,0,22):C.R2GC_423_1327,(0,0,25):C.R2GC_423_1328,(0,0,32):C.R2GC_423_1329,(0,0,33):C.R2GC_423_1330,(0,0,40):C.R2GC_423_1331})

V_27 = CTVertex(name = 'V_27',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.H, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,21):C.R2GC_424_1332,(0,0,23):C.R2GC_424_1333,(0,0,1):C.R2GC_424_1334,(0,0,2):C.R2GC_424_1335,(0,0,3):C.R2GC_424_1336,(0,0,4):C.R2GC_424_1337,(0,0,5):C.R2GC_424_1338,(0,0,6):C.R2GC_424_1339,(0,0,7):C.R2GC_424_1340,(0,0,8):C.R2GC_424_1341,(0,0,9):C.R2GC_424_1342,(0,0,13):C.R2GC_424_1343,(0,0,15):C.R2GC_424_1344,(0,0,17):C.R2GC_424_1345,(0,0,18):C.R2GC_424_1346,(0,0,19):C.R2GC_424_1347,(0,0,20):C.R2GC_424_1348,(0,0,22):C.R2GC_424_1349,(0,0,0):C.R2GC_424_1350,(0,0,10):C.R2GC_424_1351,(0,0,11):C.R2GC_424_1352,(0,0,12):C.R2GC_424_1353,(0,0,14):C.R2GC_424_1354,(0,0,16):C.R2GC_424_1355})

V_28 = CTVertex(name = 'V_28',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,15):C.R2GC_563_2325,(0,0,17):C.R2GC_563_2326,(0,0,1):C.R2GC_563_2327,(0,0,2):C.R2GC_563_2328,(0,0,3):C.R2GC_563_2329,(0,0,4):C.R2GC_563_2330,(0,0,5):C.R2GC_563_2331,(0,0,6):C.R2GC_563_2332,(0,0,7):C.R2GC_563_2333,(0,0,8):C.R2GC_563_2334,(0,0,9):C.R2GC_563_2335,(0,0,11):C.R2GC_563_2336,(0,0,12):C.R2GC_563_2337,(0,0,13):C.R2GC_563_2338,(0,0,14):C.R2GC_563_2339,(0,0,16):C.R2GC_563_2340,(0,0,0):C.R2GC_563_2341,(0,0,10):C.R2GC_560_2292})

V_29 = CTVertex(name = 'V_29',
                type = 'R2',
                particles = [ P.a, P.a, P.W__minus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,13):C.R2GC_211_413,(0,0,0):C.R2GC_211_414,(0,0,1):C.R2GC_211_415,(0,0,2):C.R2GC_211_416,(0,0,3):C.R2GC_211_417,(0,0,4):C.R2GC_211_418,(0,0,5):C.R2GC_211_419,(0,0,6):C.R2GC_211_420,(0,0,7):C.R2GC_211_421,(0,0,8):C.R2GC_211_422,(0,0,9):C.R2GC_211_423,(0,0,10):C.R2GC_211_424,(0,0,11):C.R2GC_211_425,(0,0,12):C.R2GC_211_426,(0,0,14):C.R2GC_211_427,(0,1,13):C.R2GC_210_398,(0,1,0):C.R2GC_210_399,(0,1,1):C.R2GC_210_400,(0,1,2):C.R2GC_210_401,(0,1,3):C.R2GC_210_402,(0,1,4):C.R2GC_210_403,(0,1,5):C.R2GC_210_404,(0,1,6):C.R2GC_210_405,(0,1,7):C.R2GC_210_406,(0,1,8):C.R2GC_210_407,(0,1,9):C.R2GC_210_408,(0,1,10):C.R2GC_210_409,(0,1,11):C.R2GC_210_410,(0,1,12):C.R2GC_210_411,(0,1,14):C.R2GC_210_412,(0,2,13):C.R2GC_209_383,(0,2,0):C.R2GC_209_384,(0,2,1):C.R2GC_209_385,(0,2,2):C.R2GC_209_386,(0,2,3):C.R2GC_209_387,(0,2,4):C.R2GC_209_388,(0,2,5):C.R2GC_209_389,(0,2,6):C.R2GC_209_390,(0,2,7):C.R2GC_209_391,(0,2,8):C.R2GC_209_392,(0,2,9):C.R2GC_209_393,(0,2,10):C.R2GC_209_394,(0,2,11):C.R2GC_209_395,(0,2,12):C.R2GC_209_396,(0,2,14):C.R2GC_209_397})

V_30 = CTVertex(name = 'V_30',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVV1 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_461_1719,(0,0,1):C.R2GC_461_1720,(0,0,2):C.R2GC_461_1721,(0,0,3):C.R2GC_461_1722,(0,0,4):C.R2GC_461_1723,(0,0,5):C.R2GC_461_1724,(0,0,6):C.R2GC_461_1725,(0,0,7):C.R2GC_461_1726,(0,0,8):C.R2GC_461_1727,(0,0,9):C.R2GC_461_1728,(0,0,10):C.R2GC_461_1729,(0,0,11):C.R2GC_461_1730})

V_31 = CTVertex(name = 'V_31',
                type = 'R2',
                particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.a] ], [ [P.a, P.W__plus__] ], [ [P.a, P.W__plus__, P.Z] ], [ [P.a, P.Z] ], [ [P.b, P.c] ], [ [P.b, P.c, P.d] ], [ [P.b, P.c, P.d, P.t] ], [ [P.b, P.c, P.d, P.u] ], [ [P.b, P.c, P.s] ], [ [P.b, P.c, P.s, P.t] ], [ [P.b, P.c, P.s, P.u] ], [ [P.b, P.c, P.t] ], [ [P.b, P.c, P.u] ], [ [P.b, P.d, P.t] ], [ [P.b, P.d, P.t, P.u] ], [ [P.b, P.d, P.u] ], [ [P.b, P.s, P.t] ], [ [P.b, P.s, P.t, P.u] ], [ [P.b, P.s, P.u] ], [ [P.b, P.t] ], [ [P.b, P.t, P.u] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.d, P.s] ], [ [P.c, P.d, P.s, P.t] ], [ [P.c, P.d, P.s, P.u] ], [ [P.c, P.d, P.t] ], [ [P.c, P.d, P.u] ], [ [P.c, P.s] ], [ [P.c, P.s, P.t] ], [ [P.c, P.s, P.u] ], [ [P.d, P.s, P.t] ], [ [P.d, P.s, P.t, P.u] ], [ [P.d, P.s, P.u] ], [ [P.d, P.t] ], [ [P.d, P.t, P.u] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.t, P.u] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_246_624,(0,0,43):C.R2GC_246_625,(0,0,45):C.R2GC_246_626,(0,0,1):C.R2GC_246_627,(0,0,3):C.R2GC_246_628,(0,0,4):C.R2GC_246_629,(0,0,19):C.R2GC_246_630,(0,0,21):C.R2GC_246_631,(0,0,22):C.R2GC_246_632,(0,0,28):C.R2GC_246_633,(0,0,34):C.R2GC_246_634,(0,0,36):C.R2GC_246_635,(0,0,37):C.R2GC_246_636,(0,0,38):C.R2GC_246_637,(0,0,39):C.R2GC_246_638,(0,0,41):C.R2GC_246_639,(0,0,42):C.R2GC_246_640,(0,0,44):C.R2GC_246_641,(0,0,2):C.R2GC_246_642,(0,0,5):C.R2GC_246_643,(0,0,8):C.R2GC_246_644,(0,0,11):C.R2GC_246_645,(0,0,12):C.R2GC_246_646,(0,0,13):C.R2GC_246_647,(0,0,15):C.R2GC_246_648,(0,0,16):C.R2GC_246_649,(0,0,18):C.R2GC_246_650,(0,0,20):C.R2GC_246_651,(0,0,23):C.R2GC_246_652,(0,0,26):C.R2GC_246_653,(0,0,27):C.R2GC_246_654,(0,0,29):C.R2GC_246_655,(0,0,30):C.R2GC_246_656,(0,0,31):C.R2GC_246_657,(0,0,33):C.R2GC_246_658,(0,0,35):C.R2GC_246_659,(0,0,40):C.R2GC_246_660,(0,0,6):C.R2GC_246_661,(0,0,7):C.R2GC_246_662,(0,0,9):C.R2GC_246_663,(0,0,10):C.R2GC_246_664,(0,0,14):C.R2GC_246_665,(0,0,17):C.R2GC_246_666,(0,0,24):C.R2GC_246_667,(0,0,25):C.R2GC_246_668,(0,0,32):C.R2GC_246_669,(0,1,0):C.R2GC_247_670,(0,1,43):C.R2GC_247_671,(0,1,45):C.R2GC_247_672,(0,1,1):C.R2GC_247_673,(0,1,3):C.R2GC_247_674,(0,1,4):C.R2GC_247_675,(0,1,19):C.R2GC_247_676,(0,1,21):C.R2GC_247_677,(0,1,22):C.R2GC_247_678,(0,1,28):C.R2GC_247_679,(0,1,34):C.R2GC_247_680,(0,1,36):C.R2GC_247_681,(0,1,37):C.R2GC_247_682,(0,1,38):C.R2GC_247_683,(0,1,39):C.R2GC_247_684,(0,1,41):C.R2GC_247_685,(0,1,42):C.R2GC_247_686,(0,1,44):C.R2GC_247_687,(0,1,2):C.R2GC_247_688,(0,1,5):C.R2GC_247_689,(0,1,8):C.R2GC_247_690,(0,1,11):C.R2GC_247_691,(0,1,12):C.R2GC_247_692,(0,1,13):C.R2GC_247_693,(0,1,15):C.R2GC_247_694,(0,1,16):C.R2GC_247_695,(0,1,18):C.R2GC_247_696,(0,1,20):C.R2GC_247_697,(0,1,23):C.R2GC_247_698,(0,1,26):C.R2GC_247_699,(0,1,27):C.R2GC_247_700,(0,1,29):C.R2GC_247_701,(0,1,30):C.R2GC_247_702,(0,1,31):C.R2GC_247_703,(0,1,33):C.R2GC_247_704,(0,1,35):C.R2GC_247_705,(0,1,40):C.R2GC_247_706,(0,1,6):C.R2GC_247_707,(0,1,7):C.R2GC_247_708,(0,1,9):C.R2GC_247_709,(0,1,10):C.R2GC_247_710,(0,1,14):C.R2GC_247_711,(0,1,17):C.R2GC_247_712,(0,1,24):C.R2GC_247_713,(0,1,25):C.R2GC_247_714,(0,1,32):C.R2GC_247_715,(0,2,43):C.R2GC_248_716,(0,2,1):C.R2GC_248_717,(0,2,4):C.R2GC_248_718,(0,2,19):C.R2GC_248_719,(0,2,21):C.R2GC_248_720,(0,2,22):C.R2GC_248_721,(0,2,28):C.R2GC_248_722,(0,2,34):C.R2GC_248_723,(0,2,36):C.R2GC_248_724,(0,2,37):C.R2GC_248_725,(0,2,38):C.R2GC_248_726,(0,2,39):C.R2GC_248_727,(0,2,41):C.R2GC_248_728,(0,2,42):C.R2GC_248_729,(0,2,44):C.R2GC_248_730,(0,2,2):C.R2GC_248_731,(0,2,5):C.R2GC_248_732,(0,2,8):C.R2GC_248_733,(0,2,11):C.R2GC_248_734,(0,2,12):C.R2GC_248_735,(0,2,13):C.R2GC_248_736,(0,2,15):C.R2GC_248_737,(0,2,16):C.R2GC_248_738,(0,2,18):C.R2GC_248_739,(0,2,20):C.R2GC_248_740,(0,2,23):C.R2GC_248_741,(0,2,26):C.R2GC_248_742,(0,2,27):C.R2GC_248_743,(0,2,29):C.R2GC_248_744,(0,2,30):C.R2GC_248_745,(0,2,31):C.R2GC_248_746,(0,2,33):C.R2GC_248_747,(0,2,35):C.R2GC_248_748,(0,2,40):C.R2GC_248_749,(0,2,6):C.R2GC_248_750,(0,2,7):C.R2GC_248_751,(0,2,9):C.R2GC_248_752,(0,2,10):C.R2GC_248_753,(0,2,14):C.R2GC_248_754,(0,2,17):C.R2GC_248_755,(0,2,24):C.R2GC_248_756,(0,2,25):C.R2GC_248_757,(0,2,32):C.R2GC_248_758})

V_32 = CTVertex(name = 'V_32',
                type = 'R2',
                particles = [ P.u__tilde__, P.d, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.d, P.G0, P.u], [P.d, P.H, P.u] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_668_3029,(0,0,1):C.R2GC_668_3030,(0,0,2):C.R2GC_668_3031,(0,0,6):C.R2GC_668_3032,(0,0,3):C.R2GC_668_3033,(0,0,4):C.R2GC_668_3034,(0,0,5):C.R2GC_668_3035,(0,0,7):C.R2GC_668_3036,(0,0,9):C.R2GC_668_3037,(0,1,0):C.R2GC_670_3047,(0,1,1):C.R2GC_670_3048,(0,1,2):C.R2GC_670_3049,(0,1,6):C.R2GC_670_3050,(0,1,3):C.R2GC_670_3051,(0,1,5):C.R2GC_670_3052,(0,1,7):C.R2GC_670_3053,(0,1,8):C.R2GC_670_3054,(0,1,9):C.R2GC_670_3055})

V_33 = CTVertex(name = 'V_33',
                type = 'R2',
                particles = [ P.c__tilde__, P.d, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c, P.d] ], [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.d, P.G__plus__] ], [ [P.c, P.d, P.g] ], [ [P.c, P.d, P.G0], [P.c, P.d, P.H] ], [ [P.c, P.d, P.Z] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_667_3020,(0,0,1):C.R2GC_667_3021,(0,0,2):C.R2GC_667_3022,(0,0,3):C.R2GC_667_3023,(0,0,4):C.R2GC_667_3024,(0,0,5):C.R2GC_667_3025,(0,0,7):C.R2GC_667_3026,(0,0,8):C.R2GC_667_3027,(0,0,9):C.R2GC_667_3028,(0,1,0):C.R2GC_669_3038,(0,1,1):C.R2GC_669_3039,(0,1,2):C.R2GC_669_3040,(0,1,3):C.R2GC_669_3041,(0,1,4):C.R2GC_669_3042,(0,1,5):C.R2GC_669_3043,(0,1,6):C.R2GC_669_3044,(0,1,7):C.R2GC_669_3045,(0,1,9):C.R2GC_669_3046})

V_34 = CTVertex(name = 'V_34',
                type = 'R2',
                particles = [ P.t__tilde__, P.d, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.d, P.G0, P.t], [P.d, P.H, P.t] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.t] ], [ [P.d, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_682_3141,(0,0,1):C.R2GC_682_3142,(0,0,2):C.R2GC_682_3143,(0,0,6):C.R2GC_682_3144,(0,0,3):C.R2GC_682_3145,(0,0,4):C.R2GC_682_3146,(0,0,5):C.R2GC_682_3147,(0,0,7):C.R2GC_682_3148,(0,0,9):C.R2GC_682_3149,(0,1,0):C.R2GC_687_3186,(0,1,1):C.R2GC_687_3187,(0,1,2):C.R2GC_687_3188,(0,1,6):C.R2GC_687_3189,(0,1,3):C.R2GC_687_3190,(0,1,5):C.R2GC_687_3191,(0,1,7):C.R2GC_687_3192,(0,1,8):C.R2GC_687_3193,(0,1,9):C.R2GC_687_3194})

V_35 = CTVertex(name = 'V_35',
                type = 'R2',
                particles = [ P.u__tilde__, P.s, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.s] ], [ [P.a, P.G__plus__, P.u] ], [ [P.a, P.s, P.u] ], [ [P.G0, P.s, P.u], [P.H, P.s, P.u] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ], [ [P.G__plus__, P.u, P.Z] ], [ [P.g, P.s, P.u] ], [ [P.s, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_674_3079,(0,0,1):C.R2GC_674_3080,(0,0,2):C.R2GC_674_3081,(0,0,8):C.R2GC_674_3082,(0,0,3):C.R2GC_674_3083,(0,0,4):C.R2GC_674_3084,(0,0,6):C.R2GC_674_3085,(0,0,7):C.R2GC_674_3086,(0,0,9):C.R2GC_674_3087,(0,1,0):C.R2GC_676_3097,(0,1,1):C.R2GC_676_3098,(0,1,2):C.R2GC_676_3099,(0,1,8):C.R2GC_676_3100,(0,1,3):C.R2GC_676_3101,(0,1,5):C.R2GC_676_3102,(0,1,6):C.R2GC_676_3103,(0,1,7):C.R2GC_676_3104,(0,1,9):C.R2GC_676_3105})

V_36 = CTVertex(name = 'V_36',
                type = 'R2',
                particles = [ P.c__tilde__, P.s, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.c, P.s] ], [ [P.a, P.G__plus__, P.s] ], [ [P.c, P.G0, P.s], [P.c, P.H, P.s] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.c, P.g, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_673_3070,(0,0,1):C.R2GC_673_3071,(0,0,2):C.R2GC_673_3072,(0,0,6):C.R2GC_673_3073,(0,0,3):C.R2GC_673_3074,(0,0,5):C.R2GC_673_3075,(0,0,7):C.R2GC_673_3076,(0,0,8):C.R2GC_673_3077,(0,0,9):C.R2GC_673_3078,(0,1,0):C.R2GC_675_3088,(0,1,1):C.R2GC_675_3089,(0,1,2):C.R2GC_675_3090,(0,1,6):C.R2GC_675_3091,(0,1,3):C.R2GC_675_3092,(0,1,4):C.R2GC_675_3093,(0,1,5):C.R2GC_675_3094,(0,1,7):C.R2GC_675_3095,(0,1,9):C.R2GC_675_3096})

V_37 = CTVertex(name = 'V_37',
                type = 'R2',
                particles = [ P.t__tilde__, P.s, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.s] ], [ [P.a, P.G__plus__, P.t] ], [ [P.a, P.s, P.t] ], [ [P.G0, P.s, P.t], [P.H, P.s, P.t] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ], [ [P.G__plus__, P.t, P.Z] ], [ [P.g, P.s, P.t] ], [ [P.s, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_683_3150,(0,0,1):C.R2GC_683_3151,(0,0,2):C.R2GC_683_3152,(0,0,8):C.R2GC_683_3153,(0,0,3):C.R2GC_683_3154,(0,0,4):C.R2GC_683_3155,(0,0,6):C.R2GC_683_3156,(0,0,7):C.R2GC_683_3157,(0,0,9):C.R2GC_683_3158,(0,1,0):C.R2GC_688_3195,(0,1,1):C.R2GC_688_3196,(0,1,2):C.R2GC_688_3197,(0,1,8):C.R2GC_688_3198,(0,1,3):C.R2GC_688_3199,(0,1,5):C.R2GC_688_3200,(0,1,6):C.R2GC_688_3201,(0,1,7):C.R2GC_688_3202,(0,1,9):C.R2GC_688_3203})

V_38 = CTVertex(name = 'V_38',
                type = 'R2',
                particles = [ P.u__tilde__, P.b, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.b, P.G0, P.u], [P.b, P.H, P.u] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.u] ], [ [P.b, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_685_3168,(0,0,1):C.R2GC_685_3169,(0,0,2):C.R2GC_685_3170,(0,0,6):C.R2GC_685_3171,(0,0,3):C.R2GC_685_3172,(0,0,4):C.R2GC_685_3173,(0,0,5):C.R2GC_685_3174,(0,0,7):C.R2GC_685_3175,(0,0,9):C.R2GC_685_3176,(0,1,0):C.R2GC_690_3213,(0,1,1):C.R2GC_690_3214,(0,1,2):C.R2GC_690_3215,(0,1,6):C.R2GC_690_3216,(0,1,3):C.R2GC_690_3217,(0,1,5):C.R2GC_690_3218,(0,1,7):C.R2GC_690_3219,(0,1,8):C.R2GC_690_3220,(0,1,9):C.R2GC_690_3221})

V_39 = CTVertex(name = 'V_39',
                type = 'R2',
                particles = [ P.c__tilde__, P.b, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.c] ], [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.c, P.G__plus__] ], [ [P.b, P.c, P.g] ], [ [P.b, P.c, P.G0], [P.b, P.c, P.H] ], [ [P.b, P.c, P.Z] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_684_3159,(0,0,1):C.R2GC_684_3160,(0,0,2):C.R2GC_684_3161,(0,0,3):C.R2GC_684_3162,(0,0,4):C.R2GC_684_3163,(0,0,5):C.R2GC_684_3164,(0,0,6):C.R2GC_684_3165,(0,0,7):C.R2GC_684_3166,(0,0,9):C.R2GC_684_3167,(0,1,0):C.R2GC_689_3204,(0,1,1):C.R2GC_689_3205,(0,1,2):C.R2GC_689_3206,(0,1,3):C.R2GC_689_3207,(0,1,4):C.R2GC_689_3208,(0,1,5):C.R2GC_689_3209,(0,1,7):C.R2GC_689_3210,(0,1,8):C.R2GC_689_3211,(0,1,9):C.R2GC_689_3212})

V_40 = CTVertex(name = 'V_40',
                type = 'R2',
                particles = [ P.t__tilde__, P.b, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.b, P.G0, P.t], [P.b, P.H, P.t] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_686_3177,(0,0,1):C.R2GC_686_3178,(0,0,2):C.R2GC_686_3179,(0,0,6):C.R2GC_686_3180,(0,0,3):C.R2GC_686_3181,(0,0,4):C.R2GC_686_3182,(0,0,5):C.R2GC_686_3183,(0,0,7):C.R2GC_686_3184,(0,0,9):C.R2GC_686_3185,(0,1,0):C.R2GC_691_3222,(0,1,1):C.R2GC_691_3223,(0,1,2):C.R2GC_691_3224,(0,1,6):C.R2GC_691_3225,(0,1,3):C.R2GC_691_3226,(0,1,5):C.R2GC_691_3227,(0,1,7):C.R2GC_691_3228,(0,1,8):C.R2GC_691_3229,(0,1,9):C.R2GC_691_3230})

V_41 = CTVertex(name = 'V_41',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.H] ], [ [P.d, P.H, P.Z] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_236_530,(0,0,1):C.R2GC_236_531,(0,0,3):C.R2GC_236_532,(0,0,4):C.R2GC_235_522,(0,0,5):C.R2GC_235_521,(0,0,7):C.R2GC_236_533,(0,0,8):C.R2GC_236_534,(0,0,10):C.R2GC_236_535,(0,0,2):C.R2GC_236_536,(0,0,6):C.R2GC_236_537,(0,0,9):C.R2GC_236_538,(0,0,11):C.R2GC_236_539,(0,1,0):C.R2GC_235_518,(0,1,1):C.R2GC_235_519,(0,1,3):C.R2GC_235_520,(0,1,4):C.R2GC_235_521,(0,1,5):C.R2GC_235_522,(0,1,7):C.R2GC_235_523,(0,1,8):C.R2GC_235_524,(0,1,10):C.R2GC_235_525,(0,1,2):C.R2GC_235_526,(0,1,6):C.R2GC_235_527,(0,1,9):C.R2GC_235_528,(0,1,11):C.R2GC_235_529})

V_42 = CTVertex(name = 'V_42',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G0, P.s] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.H, P.s, P.Z] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_238_552,(0,0,1):C.R2GC_238_553,(0,0,8):C.R2GC_238_554,(0,0,3):C.R2GC_237_546,(0,0,4):C.R2GC_238_555,(0,0,6):C.R2GC_238_556,(0,0,9):C.R2GC_237_543,(0,0,11):C.R2GC_238_557,(0,0,2):C.R2GC_238_558,(0,0,5):C.R2GC_238_559,(0,0,7):C.R2GC_238_560,(0,0,10):C.R2GC_238_561,(0,1,0):C.R2GC_237_540,(0,1,1):C.R2GC_237_541,(0,1,8):C.R2GC_237_542,(0,1,3):C.R2GC_237_543,(0,1,4):C.R2GC_237_544,(0,1,6):C.R2GC_237_545,(0,1,9):C.R2GC_237_546,(0,1,11):C.R2GC_237_547,(0,1,2):C.R2GC_237_548,(0,1,5):C.R2GC_237_549,(0,1,7):C.R2GC_237_550,(0,1,10):C.R2GC_237_551})

V_43 = CTVertex(name = 'V_43',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.H] ], [ [P.b, P.H, P.Z] ], [ [P.b, P.Z] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_572_2428,(0,0,1):C.R2GC_572_2429,(0,0,2):C.R2GC_572_2430,(0,0,3):C.R2GC_572_2431,(0,0,5):C.R2GC_572_2432,(0,0,6):C.R2GC_572_2433,(0,0,8):C.R2GC_572_2434,(0,0,10):C.R2GC_572_2435,(0,0,4):C.R2GC_572_2436,(0,0,7):C.R2GC_572_2437,(0,0,9):C.R2GC_572_2438,(0,0,11):C.R2GC_572_2439})

V_44 = CTVertex(name = 'V_44',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.d, P.g] ], [ [P.d, P.G0] ], [ [P.d, P.G0, P.Z] ], [ [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_584_2501,(0,0,1):C.R2GC_584_2502,(0,0,3):C.R2GC_584_2503,(0,0,4):C.R2GC_584_2504,(0,0,6):C.R2GC_584_2505,(0,0,7):C.R2GC_584_2506,(0,0,8):C.R2GC_584_2507,(0,0,10):C.R2GC_584_2508,(0,0,2):C.R2GC_584_2509,(0,0,5):C.R2GC_584_2510,(0,0,9):C.R2GC_584_2511,(0,0,11):C.R2GC_584_2512,(0,1,0):C.R2GC_584_2501,(0,1,1):C.R2GC_584_2502,(0,1,3):C.R2GC_584_2503,(0,1,4):C.R2GC_584_2504,(0,1,6):C.R2GC_584_2505,(0,1,7):C.R2GC_584_2506,(0,1,8):C.R2GC_584_2507,(0,1,10):C.R2GC_584_2508,(0,1,2):C.R2GC_585_2513,(0,1,5):C.R2GC_584_2510,(0,1,9):C.R2GC_585_2514,(0,1,11):C.R2GC_584_2512})

V_45 = CTVertex(name = 'V_45',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G0, P.s] ], [ [P.G0, P.s, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ], [ [P.g, P.s] ], [ [P.H, P.s] ], [ [P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_617_2697,(0,0,1):C.R2GC_617_2698,(0,0,9):C.R2GC_617_2699,(0,0,3):C.R2GC_617_2700,(0,0,5):C.R2GC_617_2701,(0,0,7):C.R2GC_617_2702,(0,0,10):C.R2GC_617_2703,(0,0,11):C.R2GC_617_2704,(0,0,2):C.R2GC_617_2705,(0,0,4):C.R2GC_617_2706,(0,0,6):C.R2GC_617_2707,(0,0,8):C.R2GC_617_2708,(0,1,0):C.R2GC_617_2697,(0,1,1):C.R2GC_617_2698,(0,1,9):C.R2GC_617_2699,(0,1,3):C.R2GC_617_2700,(0,1,5):C.R2GC_618_2709,(0,1,7):C.R2GC_617_2702,(0,1,10):C.R2GC_617_2703,(0,1,11):C.R2GC_617_2704,(0,1,2):C.R2GC_617_2705,(0,1,4):C.R2GC_617_2706,(0,1,6):C.R2GC_618_2710,(0,1,8):C.R2GC_617_2708})

V_46 = CTVertex(name = 'V_46',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0] ], [ [P.b, P.G0, P.Z] ], [ [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_239_562,(0,0,1):C.R2GC_239_563,(0,0,2):C.R2GC_239_564,(0,0,4):C.R2GC_239_565,(0,0,5):C.R2GC_239_566,(0,0,6):C.R2GC_239_567,(0,0,8):C.R2GC_239_568,(0,0,10):C.R2GC_239_569,(0,0,3):C.R2GC_239_570,(0,0,7):C.R2GC_239_571,(0,0,9):C.R2GC_239_572,(0,0,11):C.R2GC_239_573})

V_47 = CTVertex(name = 'V_47',
                type = 'R2',
                particles = [ P.d__tilde__, P.u, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.d, P.G0, P.u], [P.d, P.H, P.u] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_662_2979,(0,0,1):C.R2GC_662_2980,(0,0,2):C.R2GC_662_2981,(0,0,6):C.R2GC_662_2982,(0,0,3):C.R2GC_662_2983,(0,0,5):C.R2GC_662_2984,(0,0,7):C.R2GC_662_2985,(0,0,8):C.R2GC_662_2986,(0,0,9):C.R2GC_662_2987,(0,1,0):C.R2GC_614_2670,(0,1,1):C.R2GC_614_2671,(0,1,2):C.R2GC_614_2672,(0,1,6):C.R2GC_614_2673,(0,1,3):C.R2GC_614_2674,(0,1,4):C.R2GC_614_2675,(0,1,5):C.R2GC_614_2676,(0,1,7):C.R2GC_614_2677,(0,1,9):C.R2GC_614_2678})

V_48 = CTVertex(name = 'V_48',
                type = 'R2',
                particles = [ P.s__tilde__, P.u, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.s] ], [ [P.a, P.G__plus__, P.u] ], [ [P.a, P.s, P.u] ], [ [P.G0, P.s, P.u], [P.H, P.s, P.u] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ], [ [P.G__plus__, P.u, P.Z] ], [ [P.g, P.s, P.u] ], [ [P.s, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_663_2988,(0,0,1):C.R2GC_663_2989,(0,0,2):C.R2GC_663_2990,(0,0,8):C.R2GC_663_2991,(0,0,3):C.R2GC_663_2992,(0,0,5):C.R2GC_663_2993,(0,0,6):C.R2GC_663_2994,(0,0,7):C.R2GC_663_2995,(0,0,9):C.R2GC_663_2996,(0,1,0):C.R2GC_620_2711,(0,1,1):C.R2GC_620_2712,(0,1,2):C.R2GC_620_2713,(0,1,8):C.R2GC_620_2714,(0,1,3):C.R2GC_620_2715,(0,1,4):C.R2GC_620_2716,(0,1,6):C.R2GC_620_2717,(0,1,7):C.R2GC_620_2718,(0,1,9):C.R2GC_620_2719})

V_49 = CTVertex(name = 'V_49',
                type = 'R2',
                particles = [ P.b__tilde__, P.u, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.u] ], [ [P.a, P.G__plus__, P.u] ], [ [P.b, P.G0, P.u], [P.b, P.H, P.u] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.u] ], [ [P.b, P.u, P.Z] ], [ [P.G0, P.u, P.W__plus__], [P.H, P.u, P.W__plus__] ], [ [P.G__plus__, P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_664_2997,(0,0,1):C.R2GC_664_2998,(0,0,2):C.R2GC_664_2999,(0,0,6):C.R2GC_664_3000,(0,0,3):C.R2GC_664_3001,(0,0,5):C.R2GC_664_3002,(0,0,7):C.R2GC_664_3003,(0,0,8):C.R2GC_664_3004,(0,0,9):C.R2GC_664_3005,(0,1,0):C.R2GC_611_2643,(0,1,1):C.R2GC_611_2644,(0,1,2):C.R2GC_611_2645,(0,1,6):C.R2GC_611_2646,(0,1,3):C.R2GC_611_2647,(0,1,4):C.R2GC_611_2648,(0,1,5):C.R2GC_611_2649,(0,1,7):C.R2GC_611_2650,(0,1,9):C.R2GC_611_2651})

V_50 = CTVertex(name = 'V_50',
                type = 'R2',
                particles = [ P.d__tilde__, P.c, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c, P.d] ], [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.d, P.G__plus__] ], [ [P.c, P.d, P.g] ], [ [P.c, P.d, P.G0], [P.c, P.d, P.H] ], [ [P.c, P.d, P.Z] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_654_2913,(0,0,1):C.R2GC_654_2914,(0,0,2):C.R2GC_654_2915,(0,0,3):C.R2GC_654_2916,(0,0,4):C.R2GC_654_2917,(0,0,5):C.R2GC_654_2918,(0,0,6):C.R2GC_654_2919,(0,0,7):C.R2GC_654_2920,(0,0,9):C.R2GC_654_2921,(0,1,0):C.R2GC_615_2679,(0,1,1):C.R2GC_615_2680,(0,1,2):C.R2GC_615_2681,(0,1,3):C.R2GC_615_2682,(0,1,4):C.R2GC_615_2683,(0,1,5):C.R2GC_615_2684,(0,1,7):C.R2GC_615_2685,(0,1,8):C.R2GC_615_2686,(0,1,9):C.R2GC_615_2687})

V_51 = CTVertex(name = 'V_51',
                type = 'R2',
                particles = [ P.s__tilde__, P.c, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c, P.G__plus__] ], [ [P.a, P.c, P.s] ], [ [P.a, P.G__plus__, P.s] ], [ [P.c, P.G0, P.s], [P.c, P.H, P.s] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ], [ [P.c, P.g, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_655_2922,(0,0,1):C.R2GC_655_2923,(0,0,2):C.R2GC_655_2924,(0,0,6):C.R2GC_655_2925,(0,0,3):C.R2GC_655_2926,(0,0,4):C.R2GC_655_2927,(0,0,5):C.R2GC_655_2928,(0,0,7):C.R2GC_655_2929,(0,0,9):C.R2GC_655_2930,(0,1,0):C.R2GC_621_2720,(0,1,1):C.R2GC_621_2721,(0,1,2):C.R2GC_621_2722,(0,1,6):C.R2GC_621_2723,(0,1,3):C.R2GC_621_2724,(0,1,5):C.R2GC_621_2725,(0,1,7):C.R2GC_621_2726,(0,1,8):C.R2GC_621_2727,(0,1,9):C.R2GC_621_2728})

V_52 = CTVertex(name = 'V_52',
                type = 'R2',
                particles = [ P.b__tilde__, P.c, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.c] ], [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.c, P.G__plus__] ], [ [P.b, P.c, P.g] ], [ [P.b, P.c, P.G0], [P.b, P.c, P.H] ], [ [P.b, P.c, P.Z] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.c, P.G0, P.W__plus__], [P.c, P.H, P.W__plus__] ], [ [P.c, P.G__plus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_656_2931,(0,0,1):C.R2GC_656_2932,(0,0,2):C.R2GC_656_2933,(0,0,3):C.R2GC_656_2934,(0,0,4):C.R2GC_656_2935,(0,0,5):C.R2GC_656_2936,(0,0,7):C.R2GC_656_2937,(0,0,8):C.R2GC_656_2938,(0,0,9):C.R2GC_656_2939,(0,1,0):C.R2GC_612_2652,(0,1,1):C.R2GC_612_2653,(0,1,2):C.R2GC_612_2654,(0,1,3):C.R2GC_612_2655,(0,1,4):C.R2GC_612_2656,(0,1,5):C.R2GC_612_2657,(0,1,6):C.R2GC_612_2658,(0,1,7):C.R2GC_612_2659,(0,1,9):C.R2GC_612_2660})

V_53 = CTVertex(name = 'V_53',
                type = 'R2',
                particles = [ P.d__tilde__, P.t, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.d, P.G__plus__] ], [ [P.a, P.d, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.d, P.G0, P.t], [P.d, P.H, P.t] ], [ [P.d, P.G0, P.W__plus__], [P.d, P.H, P.W__plus__] ], [ [P.d, P.G__plus__, P.Z] ], [ [P.d, P.g, P.t] ], [ [P.d, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_657_2940,(0,0,1):C.R2GC_657_2941,(0,0,2):C.R2GC_657_2942,(0,0,6):C.R2GC_657_2943,(0,0,3):C.R2GC_657_2944,(0,0,5):C.R2GC_657_2945,(0,0,7):C.R2GC_657_2946,(0,0,8):C.R2GC_657_2947,(0,0,9):C.R2GC_657_2948,(0,1,0):C.R2GC_616_2688,(0,1,1):C.R2GC_616_2689,(0,1,2):C.R2GC_616_2690,(0,1,6):C.R2GC_616_2691,(0,1,3):C.R2GC_616_2692,(0,1,4):C.R2GC_616_2693,(0,1,5):C.R2GC_616_2694,(0,1,7):C.R2GC_616_2695,(0,1,9):C.R2GC_616_2696})

V_54 = CTVertex(name = 'V_54',
                type = 'R2',
                particles = [ P.s__tilde__, P.t, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.s] ], [ [P.a, P.G__plus__, P.t] ], [ [P.a, P.s, P.t] ], [ [P.G0, P.s, P.t], [P.H, P.s, P.t] ], [ [P.G0, P.s, P.W__plus__], [P.H, P.s, P.W__plus__] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.s, P.Z] ], [ [P.G__plus__, P.t, P.Z] ], [ [P.g, P.s, P.t] ], [ [P.s, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_658_2949,(0,0,1):C.R2GC_658_2950,(0,0,2):C.R2GC_658_2951,(0,0,8):C.R2GC_658_2952,(0,0,3):C.R2GC_658_2953,(0,0,5):C.R2GC_658_2954,(0,0,6):C.R2GC_658_2955,(0,0,7):C.R2GC_658_2956,(0,0,9):C.R2GC_658_2957,(0,1,0):C.R2GC_622_2729,(0,1,1):C.R2GC_622_2730,(0,1,2):C.R2GC_622_2731,(0,1,8):C.R2GC_622_2732,(0,1,3):C.R2GC_622_2733,(0,1,4):C.R2GC_622_2734,(0,1,6):C.R2GC_622_2735,(0,1,7):C.R2GC_622_2736,(0,1,9):C.R2GC_622_2737})

V_55 = CTVertex(name = 'V_55',
                type = 'R2',
                particles = [ P.b__tilde__, P.t, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.b, P.G__plus__] ], [ [P.a, P.b, P.t] ], [ [P.a, P.G__plus__, P.t] ], [ [P.b, P.G0, P.t], [P.b, P.H, P.t] ], [ [P.b, P.G0, P.W__plus__], [P.b, P.H, P.W__plus__] ], [ [P.b, P.G__plus__, P.Z] ], [ [P.b, P.g, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.G0, P.t, P.W__plus__], [P.H, P.t, P.W__plus__] ], [ [P.G__plus__, P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_659_2958,(0,0,1):C.R2GC_659_2959,(0,0,2):C.R2GC_659_2960,(0,0,6):C.R2GC_659_2961,(0,0,3):C.R2GC_659_2962,(0,0,5):C.R2GC_659_2963,(0,0,7):C.R2GC_659_2964,(0,0,8):C.R2GC_659_2965,(0,0,9):C.R2GC_659_2966,(0,1,0):C.R2GC_613_2661,(0,1,1):C.R2GC_613_2662,(0,1,2):C.R2GC_613_2663,(0,1,6):C.R2GC_613_2664,(0,1,3):C.R2GC_613_2665,(0,1,4):C.R2GC_613_2666,(0,1,5):C.R2GC_613_2667,(0,1,7):C.R2GC_613_2668,(0,1,9):C.R2GC_613_2669})

V_56 = CTVertex(name = 'V_56',
                type = 'R2',
                particles = [ P.ve__tilde__, P.e__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.G0, P.W__plus__], [P.e__minus__, P.H, P.W__plus__] ], [ [P.e__minus__, P.G__plus__, P.Z] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.G__plus__, P.ve, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_588_2520,(0,0,1):C.R2GC_588_2521,(0,0,2):C.R2GC_588_2522,(0,0,3):C.R2GC_588_2523,(0,0,4):C.R2GC_588_2524})

V_57 = CTVertex(name = 'V_57',
                type = 'R2',
                particles = [ P.vm__tilde__, P.mu__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.W__plus__], [P.H, P.mu__minus__, P.W__plus__] ], [ [P.G__plus__, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.Z] ], [ [P.mu__minus__, P.vm, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_592_2536,(0,0,1):C.R2GC_592_2537,(0,0,2):C.R2GC_592_2538,(0,0,3):C.R2GC_592_2539,(0,0,4):C.R2GC_592_2540})

V_58 = CTVertex(name = 'V_58',
                type = 'R2',
                particles = [ P.vt__tilde__, P.ta__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS3 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.W__plus__], [P.H, P.ta__minus__, P.W__plus__] ], [ [P.G__plus__, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.Z] ], [ [P.ta__minus__, P.vt, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_635_2806,(0,0,1):C.R2GC_635_2807,(0,0,2):C.R2GC_635_2808,(0,0,3):C.R2GC_635_2809,(0,0,4):C.R2GC_635_2810})

V_59 = CTVertex(name = 'V_59',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.H, P.Z] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_590_2525,(0,0,1):C.R2GC_590_2526,(0,0,2):C.R2GC_590_2527,(0,0,4):C.R2GC_590_2528,(0,0,3):C.R2GC_590_2529,(0,0,5):C.R2GC_590_2530})

V_60 = CTVertex(name = 'V_60',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.G__plus__, P.vm, P.W__plus__] ], [ [P.H, P.mu__minus__] ], [ [P.H, P.mu__minus__, P.Z] ], [ [P.mu__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_594_2541,(0,0,1):C.R2GC_594_2542,(0,0,3):C.R2GC_594_2543,(0,0,5):C.R2GC_594_2544,(0,0,2):C.R2GC_594_2545,(0,0,4):C.R2GC_594_2546})

V_61 = CTVertex(name = 'V_61',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.G__plus__, P.vt, P.W__plus__] ], [ [P.H, P.ta__minus__] ], [ [P.H, P.ta__minus__, P.Z] ], [ [P.ta__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_637_2811,(0,0,1):C.R2GC_637_2812,(0,0,3):C.R2GC_637_2813,(0,0,5):C.R2GC_637_2814,(0,0,2):C.R2GC_637_2815,(0,0,4):C.R2GC_637_2816})

V_62 = CTVertex(name = 'V_62',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0] ], [ [P.e__minus__, P.G0, P.Z] ], [ [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_241_586,(0,0,1):C.R2GC_241_587,(0,0,3):C.R2GC_241_588,(0,0,4):C.R2GC_241_589,(0,0,2):C.R2GC_241_590,(0,0,5):C.R2GC_241_591})

V_63 = CTVertex(name = 'V_63',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.W__plus__] ], [ [P.H, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_242_592,(0,0,1):C.R2GC_242_593,(0,0,4):C.R2GC_242_594,(0,0,5):C.R2GC_242_595,(0,0,2):C.R2GC_242_596,(0,0,3):C.R2GC_242_597})

V_64 = CTVertex(name = 'V_64',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.W__plus__] ], [ [P.H, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_243_598,(0,0,1):C.R2GC_243_599,(0,0,4):C.R2GC_243_600,(0,0,5):C.R2GC_243_601,(0,0,2):C.R2GC_243_602,(0,0,3):C.R2GC_243_603})

V_65 = CTVertex(name = 'V_65',
                type = 'R2',
                particles = [ P.e__plus__, P.ve, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.a, P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.G0, P.W__plus__], [P.e__minus__, P.H, P.W__plus__] ], [ [P.e__minus__, P.G__plus__, P.Z] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.G__plus__, P.ve, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_587_2515,(0,0,1):C.R2GC_587_2516,(0,0,2):C.R2GC_587_2517,(0,0,3):C.R2GC_587_2518,(0,0,4):C.R2GC_587_2519})

V_66 = CTVertex(name = 'V_66',
                type = 'R2',
                particles = [ P.mu__plus__, P.vm, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.mu__minus__] ], [ [P.G0, P.mu__minus__, P.W__plus__], [P.H, P.mu__minus__, P.W__plus__] ], [ [P.G__plus__, P.mu__minus__, P.Z] ], [ [P.G__plus__, P.vm, P.Z] ], [ [P.mu__minus__, P.vm, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_591_2531,(0,0,1):C.R2GC_591_2532,(0,0,2):C.R2GC_591_2533,(0,0,3):C.R2GC_591_2534,(0,0,4):C.R2GC_591_2535})

V_67 = CTVertex(name = 'V_67',
                type = 'R2',
                particles = [ P.ta__plus__, P.vt, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.FFS4 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.ta__minus__] ], [ [P.G0, P.ta__minus__, P.W__plus__], [P.H, P.ta__minus__, P.W__plus__] ], [ [P.G__plus__, P.ta__minus__, P.Z] ], [ [P.G__plus__, P.vt, P.Z] ], [ [P.ta__minus__, P.vt, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_634_2801,(0,0,1):C.R2GC_634_2802,(0,0,2):C.R2GC_634_2803,(0,0,3):C.R2GC_634_2804,(0,0,4):C.R2GC_634_2805})

V_68 = CTVertex(name = 'V_68',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.u] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.H, P.u, P.Z] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_660_2967,(0,0,1):C.R2GC_660_2968,(0,0,3):C.R2GC_660_2969,(0,0,8):C.R2GC_660_2970,(0,0,5):C.R2GC_660_2971,(0,0,6):C.R2GC_660_2972,(0,0,9):C.R2GC_660_2973,(0,0,11):C.R2GC_660_2974,(0,0,2):C.R2GC_660_2975,(0,0,4):C.R2GC_660_2976,(0,0,7):C.R2GC_660_2977,(0,0,10):C.R2GC_660_2978})

V_69 = CTVertex(name = 'V_69',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.H] ], [ [P.c, P.H, P.Z] ], [ [P.c, P.Z] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_220_462,(0,0,1):C.R2GC_220_463,(0,0,3):C.R2GC_220_464,(0,0,4):C.R2GC_219_454,(0,0,5):C.R2GC_219_453,(0,0,7):C.R2GC_220_465,(0,0,8):C.R2GC_220_466,(0,0,10):C.R2GC_220_467,(0,0,2):C.R2GC_220_468,(0,0,6):C.R2GC_220_469,(0,0,9):C.R2GC_220_470,(0,0,11):C.R2GC_220_471,(0,1,0):C.R2GC_219_450,(0,1,1):C.R2GC_219_451,(0,1,3):C.R2GC_219_452,(0,1,4):C.R2GC_219_453,(0,1,5):C.R2GC_219_454,(0,1,7):C.R2GC_219_455,(0,1,8):C.R2GC_219_456,(0,1,10):C.R2GC_219_457,(0,1,2):C.R2GC_219_458,(0,1,6):C.R2GC_219_459,(0,1,9):C.R2GC_219_460,(0,1,11):C.R2GC_219_461})

V_70 = CTVertex(name = 'V_70',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.t] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.H, P.t, P.Z] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_227_484,(0,0,1):C.R2GC_227_485,(0,0,3):C.R2GC_227_486,(0,0,8):C.R2GC_227_487,(0,0,5):C.R2GC_227_488,(0,0,6):C.R2GC_227_489,(0,0,9):C.R2GC_227_490,(0,0,11):C.R2GC_227_491,(0,0,2):C.R2GC_227_492,(0,0,4):C.R2GC_227_493,(0,0,7):C.R2GC_227_494,(0,0,10):C.R2GC_227_495,(0,1,0):C.R2GC_228_496,(0,1,1):C.R2GC_228_497,(0,1,3):C.R2GC_228_498,(0,1,8):C.R2GC_228_499,(0,1,5):C.R2GC_227_490,(0,1,6):C.R2GC_228_500,(0,1,9):C.R2GC_227_488,(0,1,11):C.R2GC_228_501,(0,1,2):C.R2GC_228_502,(0,1,4):C.R2GC_228_503,(0,1,7):C.R2GC_228_504,(0,1,10):C.R2GC_228_505})

V_71 = CTVertex(name = 'V_71',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.u] ], [ [P.G0, P.u, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ], [ [P.g, P.u] ], [ [P.H, P.u] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_240_574,(0,0,1):C.R2GC_240_575,(0,0,3):C.R2GC_240_576,(0,0,9):C.R2GC_240_577,(0,0,5):C.R2GC_240_578,(0,0,7):C.R2GC_240_579,(0,0,10):C.R2GC_240_580,(0,0,11):C.R2GC_240_581,(0,0,2):C.R2GC_240_582,(0,0,4):C.R2GC_240_583,(0,0,6):C.R2GC_240_584,(0,0,8):C.R2GC_240_585})

V_72 = CTVertex(name = 'V_72',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.c, P.g] ], [ [P.c, P.G0] ], [ [P.c, P.G0, P.Z] ], [ [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_574_2440,(0,0,1):C.R2GC_574_2441,(0,0,3):C.R2GC_574_2442,(0,0,4):C.R2GC_574_2443,(0,0,6):C.R2GC_574_2444,(0,0,7):C.R2GC_574_2445,(0,0,8):C.R2GC_574_2446,(0,0,10):C.R2GC_574_2447,(0,0,2):C.R2GC_574_2448,(0,0,5):C.R2GC_574_2449,(0,0,9):C.R2GC_575_2452,(0,0,11):C.R2GC_574_2451,(0,1,0):C.R2GC_574_2440,(0,1,1):C.R2GC_574_2441,(0,1,3):C.R2GC_574_2442,(0,1,4):C.R2GC_574_2443,(0,1,6):C.R2GC_574_2444,(0,1,7):C.R2GC_574_2445,(0,1,8):C.R2GC_574_2446,(0,1,10):C.R2GC_574_2447,(0,1,2):C.R2GC_574_2448,(0,1,5):C.R2GC_574_2449,(0,1,9):C.R2GC_574_2450,(0,1,11):C.R2GC_574_2451})

V_73 = CTVertex(name = 'V_73',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS4 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G0, P.t] ], [ [P.G0, P.t, P.Z] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ], [ [P.g, P.t] ], [ [P.H, P.t] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_632_2786,(0,0,1):C.R2GC_632_2787,(0,0,3):C.R2GC_632_2788,(0,0,9):C.R2GC_632_2789,(0,0,5):C.R2GC_632_2790,(0,0,7):C.R2GC_633_2798,(0,0,10):C.R2GC_632_2792,(0,0,11):C.R2GC_632_2793,(0,0,2):C.R2GC_632_2794,(0,0,4):C.R2GC_633_2799,(0,0,6):C.R2GC_632_2796,(0,0,8):C.R2GC_633_2800,(0,1,0):C.R2GC_632_2786,(0,1,1):C.R2GC_632_2787,(0,1,3):C.R2GC_632_2788,(0,1,9):C.R2GC_632_2789,(0,1,5):C.R2GC_632_2790,(0,1,7):C.R2GC_632_2791,(0,1,10):C.R2GC_632_2792,(0,1,11):C.R2GC_632_2793,(0,1,2):C.R2GC_632_2794,(0,1,4):C.R2GC_632_2795,(0,1,6):C.R2GC_632_2796,(0,1,8):C.R2GC_632_2797})

V_74 = CTVertex(name = 'V_74',
                type = 'R2',
                particles = [ P.a, P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,16):C.R2GC_552_2167,(0,0,0):C.R2GC_552_2168,(0,0,1):C.R2GC_552_2169,(0,0,2):C.R2GC_552_2170,(0,0,3):C.R2GC_552_2171,(0,0,4):C.R2GC_552_2172,(0,0,5):C.R2GC_552_2173,(0,0,6):C.R2GC_552_2174,(0,0,7):C.R2GC_552_2175,(0,0,8):C.R2GC_552_2176,(0,0,9):C.R2GC_552_2177,(0,0,10):C.R2GC_552_2178,(0,0,11):C.R2GC_552_2179,(0,0,12):C.R2GC_552_2180,(0,0,13):C.R2GC_552_2181,(0,0,14):C.R2GC_552_2182,(0,0,15):C.R2GC_552_2183})

V_75 = CTVertex(name = 'V_75',
                type = 'R2',
                particles = [ P.Z, P.G0, P.H ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS3 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_522_1994,(0,0,1):C.R2GC_522_1995,(0,0,2):C.R2GC_522_1996,(0,0,3):C.R2GC_522_1997,(0,0,6):C.R2GC_522_1998,(0,0,7):C.R2GC_522_1999,(0,0,8):C.R2GC_522_2000,(0,0,9):C.R2GC_522_2001,(0,0,10):C.R2GC_522_2002,(0,0,5):C.R2GC_522_2003,(0,0,4):C.R2GC_522_2004,(0,1,0):C.R2GC_546_2134,(0,1,1):C.R2GC_546_2135,(0,1,2):C.R2GC_546_2136,(0,1,3):C.R2GC_546_2137,(0,1,6):C.R2GC_546_2138,(0,1,7):C.R2GC_546_2139,(0,1,8):C.R2GC_546_2140,(0,1,9):C.R2GC_546_2141,(0,1,10):C.R2GC_546_2142,(0,1,5):C.R2GC_546_2143,(0,1,4):C.R2GC_546_2144})

V_76 = CTVertex(name = 'V_76',
                type = 'R2',
                particles = [ P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VSS1, L.VSS3 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ] ],
                couplings = {(0,0,0):C.R2GC_533_2084,(0,0,1):C.R2GC_533_2085,(0,0,2):C.R2GC_533_2086,(0,0,3):C.R2GC_533_2087,(0,0,4):C.R2GC_533_2088,(0,0,5):C.R2GC_533_2089,(0,0,6):C.R2GC_533_2090,(0,0,7):C.R2GC_533_2091,(0,0,8):C.R2GC_533_2092,(0,0,10):C.R2GC_533_2093,(0,0,11):C.R2GC_533_2094,(0,0,12):C.R2GC_533_2095,(0,0,13):C.R2GC_533_2096,(0,0,14):C.R2GC_533_2097,(0,0,15):C.R2GC_533_2098,(0,0,9):C.R2GC_533_2099,(0,1,0):C.R2GC_532_2068,(0,1,1):C.R2GC_532_2069,(0,1,2):C.R2GC_532_2070,(0,1,3):C.R2GC_532_2071,(0,1,4):C.R2GC_532_2072,(0,1,5):C.R2GC_532_2073,(0,1,6):C.R2GC_532_2074,(0,1,7):C.R2GC_532_2075,(0,1,8):C.R2GC_532_2076,(0,1,10):C.R2GC_532_2077,(0,1,11):C.R2GC_532_2078,(0,1,12):C.R2GC_532_2079,(0,1,13):C.R2GC_532_2080,(0,1,14):C.R2GC_532_2081,(0,1,15):C.R2GC_532_2082,(0,1,9):C.R2GC_532_2083})

V_77 = CTVertex(name = 'V_77',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G0, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_428_1380,(0,0,2):C.R2GC_428_1381,(0,0,3):C.R2GC_428_1382,(0,0,4):C.R2GC_428_1383,(0,0,5):C.R2GC_428_1384,(0,0,6):C.R2GC_428_1385,(0,0,7):C.R2GC_428_1386,(0,0,8):C.R2GC_428_1387,(0,0,9):C.R2GC_428_1388,(0,0,12):C.R2GC_428_1389,(0,0,16):C.R2GC_428_1390,(0,0,19):C.R2GC_428_1391,(0,0,20):C.R2GC_428_1392,(0,0,21):C.R2GC_428_1393,(0,0,22):C.R2GC_428_1394,(0,0,23):C.R2GC_428_1395,(0,0,0):C.R2GC_428_1396,(0,0,11):C.R2GC_428_1397,(0,0,13):C.R2GC_428_1398,(0,0,14):C.R2GC_428_1399,(0,0,15):C.R2GC_428_1400,(0,0,17):C.R2GC_428_1401,(0,0,18):C.R2GC_428_1402,(0,0,10):C.R2GC_428_1403})

V_78 = CTVertex(name = 'V_78',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G__plus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_427_1356,(0,0,2):C.R2GC_427_1357,(0,0,3):C.R2GC_427_1358,(0,0,4):C.R2GC_427_1359,(0,0,5):C.R2GC_427_1360,(0,0,6):C.R2GC_427_1361,(0,0,7):C.R2GC_427_1362,(0,0,8):C.R2GC_427_1363,(0,0,9):C.R2GC_427_1364,(0,0,15):C.R2GC_427_1365,(0,0,17):C.R2GC_427_1366,(0,0,19):C.R2GC_427_1367,(0,0,20):C.R2GC_427_1368,(0,0,21):C.R2GC_427_1369,(0,0,22):C.R2GC_427_1370,(0,0,23):C.R2GC_427_1371,(0,0,0):C.R2GC_427_1372,(0,0,11):C.R2GC_427_1373,(0,0,12):C.R2GC_427_1374,(0,0,13):C.R2GC_427_1375,(0,0,14):C.R2GC_427_1376,(0,0,16):C.R2GC_427_1377,(0,0,18):C.R2GC_427_1378,(0,0,10):C.R2GC_427_1379})

V_79 = CTVertex(name = 'V_79',
                type = 'R2',
                particles = [ P.W__minus__, P.Z, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_566_2379,(0,0,2):C.R2GC_567_2383,(0,0,3):C.R2GC_567_2384,(0,0,4):C.R2GC_567_2385,(0,0,5):C.R2GC_567_2386,(0,0,6):C.R2GC_567_2387,(0,0,7):C.R2GC_567_2388,(0,0,8):C.R2GC_567_2389,(0,0,10):C.R2GC_567_2390,(0,0,12):C.R2GC_567_2391,(0,0,13):C.R2GC_567_2392,(0,0,14):C.R2GC_566_2368,(0,0,0):C.R2GC_567_2393,(0,0,9):C.R2GC_567_2394,(0,0,11):C.R2GC_567_2395})

V_80 = CTVertex(name = 'V_80',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G0, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_429_1404,(0,0,2):C.R2GC_429_1405,(0,0,3):C.R2GC_429_1406,(0,0,4):C.R2GC_429_1407,(0,0,5):C.R2GC_429_1408,(0,0,6):C.R2GC_429_1409,(0,0,7):C.R2GC_429_1410,(0,0,8):C.R2GC_429_1411,(0,0,9):C.R2GC_429_1412,(0,0,12):C.R2GC_429_1413,(0,0,16):C.R2GC_429_1414,(0,0,19):C.R2GC_429_1415,(0,0,20):C.R2GC_429_1416,(0,0,21):C.R2GC_429_1417,(0,0,22):C.R2GC_429_1418,(0,0,23):C.R2GC_429_1419,(0,0,0):C.R2GC_429_1420,(0,0,11):C.R2GC_429_1421,(0,0,13):C.R2GC_429_1422,(0,0,14):C.R2GC_429_1423,(0,0,15):C.R2GC_429_1424,(0,0,17):C.R2GC_429_1425,(0,0,18):C.R2GC_429_1426,(0,0,10):C.R2GC_429_1427})

V_81 = CTVertex(name = 'V_81',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G__minus__, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.G__plus__, P.H, P.Z] ], [ [P.G0, P.G__plus__, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.W__plus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_430_1428,(0,0,2):C.R2GC_430_1429,(0,0,3):C.R2GC_430_1430,(0,0,4):C.R2GC_430_1431,(0,0,5):C.R2GC_430_1432,(0,0,6):C.R2GC_430_1433,(0,0,7):C.R2GC_430_1434,(0,0,8):C.R2GC_430_1435,(0,0,9):C.R2GC_430_1436,(0,0,15):C.R2GC_430_1437,(0,0,17):C.R2GC_430_1438,(0,0,19):C.R2GC_430_1439,(0,0,20):C.R2GC_430_1440,(0,0,21):C.R2GC_430_1441,(0,0,22):C.R2GC_430_1442,(0,0,23):C.R2GC_430_1443,(0,0,0):C.R2GC_430_1444,(0,0,11):C.R2GC_430_1445,(0,0,12):C.R2GC_430_1446,(0,0,13):C.R2GC_430_1447,(0,0,14):C.R2GC_430_1448,(0,0,16):C.R2GC_430_1449,(0,0,18):C.R2GC_430_1450,(0,0,10):C.R2GC_430_1451})

V_82 = CTVertex(name = 'V_82',
                type = 'R2',
                particles = [ P.W__plus__, P.Z, P.G__minus__ ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.a, P.G__plus__, P.W__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.G__plus__, P.W__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,1):C.R2GC_566_2368,(0,0,2):C.R2GC_566_2369,(0,0,3):C.R2GC_566_2370,(0,0,4):C.R2GC_566_2371,(0,0,5):C.R2GC_566_2372,(0,0,6):C.R2GC_566_2373,(0,0,7):C.R2GC_566_2374,(0,0,8):C.R2GC_566_2375,(0,0,10):C.R2GC_566_2376,(0,0,12):C.R2GC_566_2377,(0,0,13):C.R2GC_566_2378,(0,0,14):C.R2GC_566_2379,(0,0,0):C.R2GC_566_2380,(0,0,9):C.R2GC_566_2381,(0,0,11):C.R2GC_566_2382})

V_83 = CTVertex(name = 'V_83',
                type = 'R2',
                particles = [ P.a, P.W__minus__, P.W__plus__, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVVV1, L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,1,13):C.R2GC_466_1761,(0,1,0):C.R2GC_466_1762,(0,1,1):C.R2GC_466_1763,(0,1,2):C.R2GC_466_1764,(0,1,3):C.R2GC_466_1765,(0,1,4):C.R2GC_466_1766,(0,1,5):C.R2GC_466_1767,(0,1,6):C.R2GC_466_1768,(0,1,7):C.R2GC_466_1769,(0,1,8):C.R2GC_466_1770,(0,1,9):C.R2GC_466_1771,(0,1,10):C.R2GC_466_1772,(0,1,11):C.R2GC_466_1773,(0,1,12):C.R2GC_466_1774,(0,1,14):C.R2GC_466_1775,(0,2,13):C.R2GC_465_1746,(0,2,0):C.R2GC_465_1747,(0,2,1):C.R2GC_465_1748,(0,2,2):C.R2GC_465_1749,(0,2,3):C.R2GC_465_1750,(0,2,4):C.R2GC_465_1751,(0,2,5):C.R2GC_465_1752,(0,2,6):C.R2GC_465_1753,(0,2,7):C.R2GC_465_1754,(0,2,8):C.R2GC_465_1755,(0,2,9):C.R2GC_465_1756,(0,2,10):C.R2GC_465_1757,(0,2,11):C.R2GC_465_1758,(0,2,12):C.R2GC_465_1759,(0,2,14):C.R2GC_465_1760,(0,3,13):C.R2GC_464_1731,(0,3,0):C.R2GC_464_1732,(0,3,1):C.R2GC_464_1733,(0,3,2):C.R2GC_464_1734,(0,3,3):C.R2GC_464_1735,(0,3,4):C.R2GC_464_1736,(0,3,5):C.R2GC_464_1737,(0,3,6):C.R2GC_464_1738,(0,3,7):C.R2GC_464_1739,(0,3,8):C.R2GC_464_1740,(0,3,9):C.R2GC_464_1741,(0,3,10):C.R2GC_464_1742,(0,3,11):C.R2GC_464_1743,(0,3,12):C.R2GC_464_1744,(0,3,14):C.R2GC_464_1745,(0,0,1):C.R2GC_202_315,(0,0,2):C.R2GC_202_316,(0,0,3):C.R2GC_202_317,(0,0,4):C.R2GC_202_318,(0,0,5):C.R2GC_202_319,(0,0,6):C.R2GC_202_320,(0,0,7):C.R2GC_202_321,(0,0,8):C.R2GC_202_322,(0,0,9):C.R2GC_202_323,(0,0,10):C.R2GC_202_324,(0,0,11):C.R2GC_202_325,(0,0,12):C.R2GC_202_326})

V_84 = CTVertex(name = 'V_84',
                type = 'R2',
                particles = [ P.Z, P.Z, P.G0, P.G0 ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_553_2184,(0,0,1):C.R2GC_553_2185,(0,0,2):C.R2GC_553_2186,(0,0,3):C.R2GC_553_2187,(0,0,7):C.R2GC_553_2188,(0,0,8):C.R2GC_553_2189,(0,0,9):C.R2GC_553_2190,(0,0,10):C.R2GC_553_2191,(0,0,11):C.R2GC_553_2192,(0,0,12):C.R2GC_553_2193,(0,0,5):C.R2GC_553_2194,(0,0,6):C.R2GC_553_2195,(0,0,4):C.R2GC_553_2196})

V_85 = CTVertex(name = 'V_85',
                type = 'R2',
                particles = [ P.Z, P.Z, P.G__minus__, P.G__plus__ ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.H, P.W__plus__] ], [ [P.G0, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,17):C.R2GC_554_2197,(0,0,0):C.R2GC_554_2198,(0,0,1):C.R2GC_554_2199,(0,0,2):C.R2GC_554_2200,(0,0,3):C.R2GC_554_2201,(0,0,4):C.R2GC_554_2202,(0,0,5):C.R2GC_554_2203,(0,0,6):C.R2GC_554_2204,(0,0,7):C.R2GC_554_2205,(0,0,8):C.R2GC_554_2206,(0,0,10):C.R2GC_554_2207,(0,0,11):C.R2GC_554_2208,(0,0,12):C.R2GC_554_2209,(0,0,13):C.R2GC_554_2210,(0,0,14):C.R2GC_554_2211,(0,0,15):C.R2GC_554_2212,(0,0,16):C.R2GC_554_2213,(0,0,9):C.R2GC_554_2214})

V_86 = CTVertex(name = 'V_86',
                type = 'R2',
                particles = [ P.Z, P.Z, P.H, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.H, P.Z] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_555_2215,(0,0,1):C.R2GC_555_2216,(0,0,2):C.R2GC_555_2217,(0,0,3):C.R2GC_555_2218,(0,0,7):C.R2GC_555_2219,(0,0,8):C.R2GC_555_2220,(0,0,9):C.R2GC_555_2221,(0,0,10):C.R2GC_555_2222,(0,0,11):C.R2GC_555_2223,(0,0,12):C.R2GC_555_2224,(0,0,5):C.R2GC_555_2225,(0,0,6):C.R2GC_555_2226,(0,0,4):C.R2GC_555_2227})

V_87 = CTVertex(name = 'V_87',
                type = 'R2',
                particles = [ P.Z, P.Z, P.H ],
                color = [ '1' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_570_2417,(0,0,1):C.R2GC_570_2418,(0,0,2):C.R2GC_570_2419,(0,0,3):C.R2GC_570_2420,(0,0,5):C.R2GC_570_2421,(0,0,6):C.R2GC_570_2422,(0,0,7):C.R2GC_570_2423,(0,0,8):C.R2GC_570_2424,(0,0,9):C.R2GC_570_2425,(0,0,10):C.R2GC_570_2426,(0,0,4):C.R2GC_570_2427})

V_88 = CTVertex(name = 'V_88',
                type = 'R2',
                particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
                color = [ '1' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ] ],
                couplings = {(0,0,13):C.R2GC_437_1479,(0,0,0):C.R2GC_437_1480,(0,0,1):C.R2GC_437_1481,(0,0,2):C.R2GC_437_1482,(0,0,3):C.R2GC_437_1483,(0,0,4):C.R2GC_437_1484,(0,0,5):C.R2GC_437_1485,(0,0,6):C.R2GC_437_1486,(0,0,7):C.R2GC_437_1487,(0,0,8):C.R2GC_437_1488,(0,0,9):C.R2GC_437_1489,(0,0,10):C.R2GC_437_1490,(0,0,11):C.R2GC_437_1491,(0,0,12):C.R2GC_437_1492,(0,0,14):C.R2GC_437_1493,(0,1,13):C.R2GC_436_1464,(0,1,0):C.R2GC_436_1465,(0,1,1):C.R2GC_436_1466,(0,1,2):C.R2GC_436_1467,(0,1,3):C.R2GC_436_1468,(0,1,4):C.R2GC_436_1469,(0,1,5):C.R2GC_436_1470,(0,1,6):C.R2GC_436_1471,(0,1,7):C.R2GC_436_1472,(0,1,8):C.R2GC_436_1473,(0,1,9):C.R2GC_436_1474,(0,1,10):C.R2GC_436_1475,(0,1,11):C.R2GC_436_1476,(0,1,12):C.R2GC_436_1477,(0,1,14):C.R2GC_436_1478,(0,2,13):C.R2GC_438_1494,(0,2,0):C.R2GC_438_1495,(0,2,1):C.R2GC_438_1496,(0,2,2):C.R2GC_438_1497,(0,2,3):C.R2GC_438_1498,(0,2,4):C.R2GC_438_1499,(0,2,5):C.R2GC_438_1500,(0,2,6):C.R2GC_438_1501,(0,2,7):C.R2GC_438_1502,(0,2,8):C.R2GC_438_1503,(0,2,9):C.R2GC_438_1504,(0,2,10):C.R2GC_438_1505,(0,2,11):C.R2GC_438_1506,(0,2,12):C.R2GC_438_1507,(0,2,14):C.R2GC_438_1508})

V_89 = CTVertex(name = 'V_89',
                type = 'R2',
                particles = [ P.e__plus__, P.e__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0], [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.ve, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_508_1957,(0,0,1):C.R2GC_508_1958,(0,0,2):C.R2GC_508_1959,(0,0,3):C.R2GC_508_1960,(0,1,0):C.R2GC_508_1957,(0,1,1):C.R2GC_508_1958,(0,1,2):C.R2GC_517_1976})

V_90 = CTVertex(name = 'V_90',
                type = 'R2',
                particles = [ P.mu__plus__, P.mu__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__], [P.H, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_508_1957,(0,0,1):C.R2GC_509_1961,(0,0,2):C.R2GC_508_1959,(0,0,3):C.R2GC_508_1960,(0,1,0):C.R2GC_508_1957,(0,1,1):C.R2GC_509_1961,(0,1,2):C.R2GC_517_1976})

V_91 = CTVertex(name = 'V_91',
                type = 'R2',
                particles = [ P.ta__plus__, P.ta__minus__, P.a ],
                color = [ '1' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__], [P.H, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_508_1957,(0,0,1):C.R2GC_510_1962,(0,0,2):C.R2GC_508_1959,(0,0,3):C.R2GC_508_1960,(0,1,0):C.R2GC_508_1957,(0,1,1):C.R2GC_510_1962,(0,1,2):C.R2GC_517_1976})

V_92 = CTVertex(name = 'V_92',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.G__plus__, P.s] ], [ [P.g, P.u] ], [ [P.s, P.W__plus__] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,5):C.R2GC_196_275,(0,1,0):C.R2GC_501_1909,(0,1,1):C.R2GC_503_1926,(0,1,2):C.R2GC_503_1927,(0,1,3):C.R2GC_503_1928,(0,1,4):C.R2GC_503_1929,(0,1,7):C.R2GC_501_1912,(0,1,6):C.R2GC_503_1930,(0,1,8):C.R2GC_503_1931,(0,1,9):C.R2GC_501_1914,(0,2,0):C.R2GC_501_1909,(0,2,1):C.R2GC_516_1973,(0,2,3):C.R2GC_516_1974,(0,2,7):C.R2GC_501_1912,(0,2,6):C.R2GC_516_1975,(0,2,9):C.R2GC_514_1967})

V_93 = CTVertex(name = 'V_93',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_501_1909,(0,0,1):C.R2GC_501_1910,(0,0,2):C.R2GC_501_1911,(0,0,3):C.R2GC_501_1912,(0,0,4):C.R2GC_501_1913,(0,0,5):C.R2GC_501_1914,(0,0,6):C.R2GC_501_1915,(0,0,7):C.R2GC_501_1916,(0,0,8):C.R2GC_501_1917,(0,0,9):C.R2GC_501_1918,(0,1,0):C.R2GC_501_1909,(0,1,1):C.R2GC_514_1966,(0,1,3):C.R2GC_501_1912,(0,1,4):C.R2GC_501_1913,(0,1,5):C.R2GC_514_1967,(0,1,6):C.R2GC_514_1968,(0,1,8):C.R2GC_514_1969})

V_94 = CTVertex(name = 'V_94',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.G__plus__, P.s] ], [ [P.g, P.t] ], [ [P.s, P.W__plus__] ], [ [P.t, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_501_1909,(0,0,1):C.R2GC_502_1919,(0,0,2):C.R2GC_502_1920,(0,0,3):C.R2GC_502_1921,(0,0,4):C.R2GC_502_1922,(0,0,7):C.R2GC_501_1912,(0,0,5):C.R2GC_502_1923,(0,0,6):C.R2GC_502_1924,(0,0,8):C.R2GC_502_1925,(0,0,9):C.R2GC_501_1914,(0,1,0):C.R2GC_501_1909,(0,1,1):C.R2GC_515_1970,(0,1,3):C.R2GC_515_1971,(0,1,7):C.R2GC_501_1912,(0,1,5):C.R2GC_502_1923,(0,1,6):C.R2GC_515_1972,(0,1,9):C.R2GC_514_1967})

V_95 = CTVertex(name = 'V_95',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.d] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_498_1885,(0,0,1):C.R2GC_499_1895,(0,0,2):C.R2GC_499_1896,(0,0,3):C.R2GC_498_1886,(0,0,4):C.R2GC_499_1897,(0,0,5):C.R2GC_498_1888,(0,0,6):C.R2GC_499_1898,(0,0,7):C.R2GC_499_1899,(0,0,8):C.R2GC_499_1900,(0,0,9):C.R2GC_499_1901,(0,1,0):C.R2GC_498_1885,(0,1,1):C.R2GC_505_1936,(0,1,3):C.R2GC_498_1886,(0,1,4):C.R2GC_499_1897,(0,1,5):C.R2GC_504_1932,(0,1,6):C.R2GC_505_1937,(0,1,7):C.R2GC_505_1938})

V_96 = CTVertex(name = 'V_96',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.g, P.s] ], [ [P.s, P.Z] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_498_1885,(0,0,1):C.R2GC_500_1902,(0,0,2):C.R2GC_500_1903,(0,0,6):C.R2GC_498_1886,(0,0,3):C.R2GC_500_1904,(0,0,4):C.R2GC_500_1905,(0,0,5):C.R2GC_500_1906,(0,0,7):C.R2GC_498_1888,(0,0,8):C.R2GC_500_1907,(0,0,9):C.R2GC_500_1908,(0,1,0):C.R2GC_498_1885,(0,1,1):C.R2GC_506_1939,(0,1,6):C.R2GC_498_1886,(0,1,3):C.R2GC_500_1904,(0,1,4):C.R2GC_506_1940,(0,1,5):C.R2GC_506_1941,(0,1,7):C.R2GC_504_1932})

V_97 = CTVertex(name = 'V_97',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_498_1885,(0,0,1):C.R2GC_498_1886,(0,0,2):C.R2GC_498_1887,(0,0,3):C.R2GC_498_1888,(0,0,4):C.R2GC_498_1889,(0,0,5):C.R2GC_498_1890,(0,0,6):C.R2GC_498_1891,(0,0,7):C.R2GC_498_1892,(0,0,8):C.R2GC_498_1893,(0,0,9):C.R2GC_498_1894,(0,1,0):C.R2GC_498_1885,(0,1,1):C.R2GC_498_1886,(0,1,2):C.R2GC_498_1887,(0,1,3):C.R2GC_504_1932,(0,1,4):C.R2GC_504_1933,(0,1,6):C.R2GC_504_1934,(0,1,7):C.R2GC_504_1935})

V_98 = CTVertex(name = 'V_98',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.u] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.G__plus__, P.s] ], [ [P.g, P.u] ], [ [P.s, P.W__plus__] ], [ [P.u, P.Z] ] ],
                couplings = {(0,0,0):C.R2GC_197_276,(0,0,7):C.R2GC_197_277,(0,0,5):C.R2GC_197_278,(0,1,1):C.R2GC_348_948,(0,1,2):C.R2GC_347_944,(0,1,3):C.R2GC_352_964,(0,1,4):C.R2GC_351_962,(0,1,6):C.R2GC_362_1007,(0,1,8):C.R2GC_361_1005,(0,1,9):C.R2GC_349_950,(0,2,1):C.R2GC_347_942,(0,2,3):C.R2GC_351_960,(0,2,6):C.R2GC_361_1003,(0,2,9):C.R2GC_350_955})

V_99 = CTVertex(name = 'V_99',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV2, L.FFV3 ],
                loop_particles = [ [ [P.a, P.c] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                couplings = {(0,0,0):C.R2GC_197_276,(0,0,1):C.R2GC_348_946,(0,0,2):C.R2GC_347_940,(0,0,3):C.R2GC_197_277,(0,0,4):C.R2GC_349_949,(0,0,5):C.R2GC_349_950,(0,0,6):C.R2GC_349_951,(0,0,7):C.R2GC_349_952,(0,0,8):C.R2GC_349_953,(0,0,9):C.R2GC_349_954,(0,1,0):C.R2GC_197_276,(0,1,1):C.R2GC_347_939,(0,1,3):C.R2GC_197_277,(0,1,4):C.R2GC_349_949,(0,1,5):C.R2GC_350_955,(0,1,6):C.R2GC_350_956,(0,1,8):C.R2GC_350_957})

V_100 = CTVertex(name = 'V_100',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.G__plus__, P.s] ], [ [P.g, P.t] ], [ [P.s, P.W__plus__] ], [ [P.t, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_197_276,(0,0,1):C.R2GC_348_947,(0,0,2):C.R2GC_347_943,(0,0,3):C.R2GC_352_963,(0,0,4):C.R2GC_351_961,(0,0,7):C.R2GC_197_277,(0,0,5):C.R2GC_367_1026,(0,0,6):C.R2GC_362_1006,(0,0,8):C.R2GC_361_1004,(0,0,9):C.R2GC_349_950,(0,1,0):C.R2GC_197_276,(0,1,1):C.R2GC_347_941,(0,1,3):C.R2GC_351_959,(0,1,7):C.R2GC_197_277,(0,1,5):C.R2GC_367_1026,(0,1,6):C.R2GC_361_1002,(0,1,9):C.R2GC_350_955})

V_101 = CTVertex(name = 'V_101',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_347_936,(0,0,1):C.R2GC_350_956,(0,0,2):C.R2GC_349_952,(0,0,3):C.R2GC_197_277,(0,0,4):C.R2GC_351_958,(0,0,5):C.R2GC_347_938,(0,0,6):C.R2GC_351_959,(0,0,7):C.R2GC_351_960,(0,0,8):C.R2GC_351_961,(0,0,9):C.R2GC_351_962,(0,1,0):C.R2GC_347_936,(0,1,1):C.R2GC_349_951,(0,1,3):C.R2GC_197_277,(0,1,4):C.R2GC_351_958,(0,1,5):C.R2GC_348_945,(0,1,6):C.R2GC_352_963,(0,1,7):C.R2GC_352_964})

V_102 = CTVertex(name = 'V_102',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.g, P.s] ], [ [P.s, P.Z] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_347_936,(0,0,1):C.R2GC_350_957,(0,0,2):C.R2GC_349_954,(0,0,6):C.R2GC_197_277,(0,0,3):C.R2GC_361_1001,(0,0,4):C.R2GC_361_1002,(0,0,5):C.R2GC_361_1003,(0,0,7):C.R2GC_347_938,(0,0,8):C.R2GC_361_1004,(0,0,9):C.R2GC_361_1005,(0,1,0):C.R2GC_347_936,(0,1,1):C.R2GC_349_953,(0,1,6):C.R2GC_197_277,(0,1,3):C.R2GC_361_1001,(0,1,4):C.R2GC_362_1006,(0,1,5):C.R2GC_362_1007,(0,1,7):C.R2GC_348_945})

V_103 = CTVertex(name = 'V_103',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_347_936,(0,0,1):C.R2GC_197_277,(0,0,2):C.R2GC_347_937,(0,0,3):C.R2GC_347_938,(0,0,4):C.R2GC_347_939,(0,0,5):C.R2GC_347_940,(0,0,6):C.R2GC_347_941,(0,0,7):C.R2GC_347_942,(0,0,8):C.R2GC_347_943,(0,0,9):C.R2GC_347_944,(0,1,0):C.R2GC_347_936,(0,1,1):C.R2GC_197_277,(0,1,2):C.R2GC_347_937,(0,1,3):C.R2GC_348_945,(0,1,4):C.R2GC_348_946,(0,1,6):C.R2GC_348_947,(0,1,7):C.R2GC_348_948})

V_104 = CTVertex(name = 'V_104',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.d, P.u] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.d, P.G0, P.u] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_446_1568,(0,0,1):C.R2GC_446_1569,(0,0,2):C.R2GC_446_1570,(0,0,4):C.R2GC_446_1571,(0,0,6):C.R2GC_446_1572,(0,0,7):C.R2GC_446_1573,(0,0,8):C.R2GC_446_1574,(0,1,3):C.R2GC_231_510,(0,1,5):C.R2GC_231_511})

V_105 = CTVertex(name = 'V_105',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.u, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.s, P.u] ], [ [P.a, P.s, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.G0, P.s, P.u] ], [ [P.g, P.s, P.u] ], [ [P.H, P.s, P.u] ], [ [P.s, P.u, P.Z] ], [ [P.s, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_447_1575,(0,0,1):C.R2GC_447_1576,(0,0,2):C.R2GC_447_1577,(0,0,4):C.R2GC_447_1578,(0,0,6):C.R2GC_447_1579,(0,0,7):C.R2GC_447_1580,(0,0,8):C.R2GC_447_1581,(0,1,3):C.R2GC_233_514,(0,1,5):C.R2GC_233_515})

V_106 = CTVertex(name = 'V_106',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.u, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.b, P.u] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.b, P.G0, P.u] ], [ [P.b, P.g, P.u] ], [ [P.b, P.H, P.u] ], [ [P.b, P.u, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_448_1582,(0,0,1):C.R2GC_448_1583,(0,0,2):C.R2GC_448_1584,(0,0,4):C.R2GC_448_1585,(0,0,6):C.R2GC_448_1586,(0,0,7):C.R2GC_448_1587,(0,0,8):C.R2GC_448_1588,(0,1,3):C.R2GC_229_506,(0,1,5):C.R2GC_229_507})

V_107 = CTVertex(name = 'V_107',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.c, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.c, P.d] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.d, P.W__plus__] ], [ [P.c, P.d, P.g] ], [ [P.c, P.d, P.G0] ], [ [P.c, P.d, P.H] ], [ [P.c, P.d, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.d, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_449_1589,(0,0,1):C.R2GC_449_1590,(0,0,2):C.R2GC_449_1591,(0,0,3):C.R2GC_449_1592,(0,0,6):C.R2GC_449_1593,(0,0,7):C.R2GC_449_1594,(0,0,8):C.R2GC_449_1595,(0,1,4):C.R2GC_215_442,(0,1,5):C.R2GC_215_443})

V_108 = CTVertex(name = 'V_108',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.c, P.s] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.s, P.W__plus__] ], [ [P.c, P.G0, P.s] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.s, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_450_1596,(0,0,1):C.R2GC_450_1597,(0,0,2):C.R2GC_450_1598,(0,0,4):C.R2GC_450_1599,(0,0,6):C.R2GC_450_1600,(0,0,7):C.R2GC_450_1601,(0,0,8):C.R2GC_450_1602,(0,1,3):C.R2GC_217_446,(0,1,5):C.R2GC_217_447})

V_109 = CTVertex(name = 'V_109',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.c, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.b, P.c] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.c, P.W__plus__] ], [ [P.b, P.c, P.g] ], [ [P.b, P.c, P.G0] ], [ [P.b, P.c, P.H] ], [ [P.b, P.c, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.c, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_451_1603,(0,0,1):C.R2GC_451_1604,(0,0,2):C.R2GC_451_1605,(0,0,3):C.R2GC_451_1606,(0,0,6):C.R2GC_451_1607,(0,0,7):C.R2GC_451_1608,(0,0,8):C.R2GC_451_1609,(0,1,4):C.R2GC_213_438,(0,1,5):C.R2GC_213_439})

V_110 = CTVertex(name = 'V_110',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.t, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.d, P.t] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.d, P.G0, P.t] ], [ [P.d, P.g, P.t] ], [ [P.d, P.H, P.t] ], [ [P.d, P.t, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_452_1610,(0,0,1):C.R2GC_452_1611,(0,0,2):C.R2GC_452_1612,(0,0,4):C.R2GC_452_1613,(0,0,6):C.R2GC_452_1614,(0,0,7):C.R2GC_452_1615,(0,0,8):C.R2GC_452_1616,(0,1,3):C.R2GC_223_476,(0,1,5):C.R2GC_223_477})

V_111 = CTVertex(name = 'V_111',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.t, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.s, P.t] ], [ [P.a, P.s, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.G0, P.s, P.t] ], [ [P.g, P.s, P.t] ], [ [P.H, P.s, P.t] ], [ [P.s, P.t, P.Z] ], [ [P.s, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_453_1617,(0,0,1):C.R2GC_453_1618,(0,0,2):C.R2GC_453_1619,(0,0,4):C.R2GC_453_1620,(0,0,6):C.R2GC_453_1621,(0,0,7):C.R2GC_453_1622,(0,0,8):C.R2GC_453_1623,(0,1,3):C.R2GC_225_480,(0,1,5):C.R2GC_225_481})

V_112 = CTVertex(name = 'V_112',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.b, P.t] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.b, P.G0, P.t] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_454_1624,(0,0,1):C.R2GC_454_1625,(0,0,2):C.R2GC_454_1626,(0,0,4):C.R2GC_454_1627,(0,0,6):C.R2GC_454_1628,(0,0,7):C.R2GC_454_1629,(0,0,8):C.R2GC_454_1630,(0,1,3):C.R2GC_221_472,(0,1,5):C.R2GC_221_473})

V_113 = CTVertex(name = 'V_113',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.d, P.u] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.d, P.G0, P.u] ], [ [P.d, P.g, P.u] ], [ [P.d, P.H, P.u] ], [ [P.d, P.u, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_666_3013,(0,0,1):C.R2GC_666_3014,(0,0,2):C.R2GC_666_3015,(0,0,4):C.R2GC_666_3016,(0,0,6):C.R2GC_666_3017,(0,0,7):C.R2GC_666_3018,(0,0,8):C.R2GC_666_3019,(0,1,3):C.R2GC_232_512,(0,1,5):C.R2GC_232_513})

V_114 = CTVertex(name = 'V_114',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.d, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.c, P.d] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.d, P.W__plus__] ], [ [P.c, P.d, P.g] ], [ [P.c, P.d, P.G0] ], [ [P.c, P.d, P.H] ], [ [P.c, P.d, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.d, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_665_3006,(0,0,1):C.R2GC_665_3007,(0,0,2):C.R2GC_665_3008,(0,0,3):C.R2GC_665_3009,(0,0,6):C.R2GC_665_3010,(0,0,7):C.R2GC_665_3011,(0,0,8):C.R2GC_665_3012,(0,1,4):C.R2GC_216_444,(0,1,5):C.R2GC_216_445})

V_115 = CTVertex(name = 'V_115',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.d, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.d, P.t] ], [ [P.a, P.d, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.d, P.G0, P.t] ], [ [P.d, P.g, P.t] ], [ [P.d, P.H, P.t] ], [ [P.d, P.t, P.Z] ], [ [P.d, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_677_3106,(0,0,1):C.R2GC_677_3107,(0,0,2):C.R2GC_677_3108,(0,0,4):C.R2GC_677_3109,(0,0,6):C.R2GC_677_3110,(0,0,7):C.R2GC_677_3111,(0,0,8):C.R2GC_677_3112,(0,1,3):C.R2GC_224_478,(0,1,5):C.R2GC_224_479})

V_116 = CTVertex(name = 'V_116',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.s, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.s, P.u] ], [ [P.a, P.s, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.G0, P.s, P.u] ], [ [P.g, P.s, P.u] ], [ [P.H, P.s, P.u] ], [ [P.s, P.u, P.Z] ], [ [P.s, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_672_3063,(0,0,1):C.R2GC_672_3064,(0,0,2):C.R2GC_672_3065,(0,0,4):C.R2GC_672_3066,(0,0,6):C.R2GC_672_3067,(0,0,7):C.R2GC_672_3068,(0,0,8):C.R2GC_672_3069,(0,1,3):C.R2GC_234_516,(0,1,5):C.R2GC_234_517})

V_117 = CTVertex(name = 'V_117',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.c, P.s] ], [ [P.a, P.c, P.W__plus__] ], [ [P.a, P.s, P.W__plus__] ], [ [P.c, P.G0, P.s] ], [ [P.c, P.g, P.s] ], [ [P.c, P.H, P.s] ], [ [P.c, P.s, P.Z] ], [ [P.c, P.W__plus__, P.Z] ], [ [P.s, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_671_3056,(0,0,1):C.R2GC_671_3057,(0,0,2):C.R2GC_671_3058,(0,0,4):C.R2GC_671_3059,(0,0,6):C.R2GC_671_3060,(0,0,7):C.R2GC_671_3061,(0,0,8):C.R2GC_671_3062,(0,1,3):C.R2GC_218_448,(0,1,5):C.R2GC_218_449})

V_118 = CTVertex(name = 'V_118',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.s, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.s, P.t] ], [ [P.a, P.s, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.G0, P.s, P.t] ], [ [P.g, P.s, P.t] ], [ [P.H, P.s, P.t] ], [ [P.s, P.t, P.Z] ], [ [P.s, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_678_3113,(0,0,1):C.R2GC_678_3114,(0,0,2):C.R2GC_678_3115,(0,0,4):C.R2GC_678_3116,(0,0,6):C.R2GC_678_3117,(0,0,7):C.R2GC_678_3118,(0,0,8):C.R2GC_678_3119,(0,1,3):C.R2GC_226_482,(0,1,5):C.R2GC_226_483})

V_119 = CTVertex(name = 'V_119',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.b, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.b, P.u] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.u, P.W__plus__] ], [ [P.b, P.G0, P.u] ], [ [P.b, P.g, P.u] ], [ [P.b, P.H, P.u] ], [ [P.b, P.u, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.u, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_680_3127,(0,0,1):C.R2GC_680_3128,(0,0,2):C.R2GC_680_3129,(0,0,4):C.R2GC_680_3130,(0,0,6):C.R2GC_680_3131,(0,0,7):C.R2GC_680_3132,(0,0,8):C.R2GC_680_3133,(0,1,3):C.R2GC_230_508,(0,1,5):C.R2GC_230_509})

V_120 = CTVertex(name = 'V_120',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.b, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.b, P.c] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.c, P.W__plus__] ], [ [P.b, P.c, P.g] ], [ [P.b, P.c, P.G0] ], [ [P.b, P.c, P.H] ], [ [P.b, P.c, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.c, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_679_3120,(0,0,1):C.R2GC_679_3121,(0,0,2):C.R2GC_679_3122,(0,0,3):C.R2GC_679_3123,(0,0,6):C.R2GC_679_3124,(0,0,7):C.R2GC_679_3125,(0,0,8):C.R2GC_679_3126,(0,1,4):C.R2GC_214_440,(0,1,5):C.R2GC_214_441})

V_121 = CTVertex(name = 'V_121',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.b, P.t] ], [ [P.a, P.b, P.W__plus__] ], [ [P.a, P.t, P.W__plus__] ], [ [P.b, P.G0, P.t] ], [ [P.b, P.g, P.t] ], [ [P.b, P.H, P.t] ], [ [P.b, P.t, P.Z] ], [ [P.b, P.W__plus__, P.Z] ], [ [P.t, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_681_3134,(0,0,1):C.R2GC_681_3135,(0,0,2):C.R2GC_681_3136,(0,0,4):C.R2GC_681_3137,(0,0,6):C.R2GC_681_3138,(0,0,7):C.R2GC_681_3139,(0,0,8):C.R2GC_681_3140,(0,1,3):C.R2GC_222_474,(0,1,5):C.R2GC_222_475})

V_122 = CTVertex(name = 'V_122',
                 type = 'R2',
                 particles = [ P.e__plus__, P.ve, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__, P.Z] ], [ [P.ve, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_443_1564,(0,0,1):C.R2GC_443_1565,(0,0,2):C.R2GC_443_1566,(0,0,3):C.R2GC_443_1567})

V_123 = CTVertex(name = 'V_123',
                 type = 'R2',
                 particles = [ P.mu__plus__, P.vm, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__, P.Z] ], [ [P.vm, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_443_1564,(0,0,1):C.R2GC_443_1565,(0,0,2):C.R2GC_443_1566,(0,0,3):C.R2GC_443_1567})

V_124 = CTVertex(name = 'V_124',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.vt, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__, P.Z] ], [ [P.vt, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_443_1564,(0,0,1):C.R2GC_443_1565,(0,0,2):C.R2GC_443_1566,(0,0,3):C.R2GC_443_1567})

V_125 = CTVertex(name = 'V_125',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.e__minus__, P.W__plus__] ], [ [P.e__minus__, P.ve, P.Z] ], [ [P.e__minus__, P.W__plus__, P.Z] ], [ [P.ve, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_443_1564,(0,0,1):C.R2GC_443_1565,(0,0,2):C.R2GC_443_1566,(0,0,3):C.R2GC_443_1567})

V_126 = CTVertex(name = 'V_126',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.mu__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.mu__minus__, P.W__plus__] ], [ [P.mu__minus__, P.vm, P.Z] ], [ [P.mu__minus__, P.W__plus__, P.Z] ], [ [P.vm, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_443_1564,(0,0,1):C.R2GC_443_1565,(0,0,2):C.R2GC_443_1566,(0,0,3):C.R2GC_443_1567})

V_127 = CTVertex(name = 'V_127',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.ta__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.a, P.ta__minus__, P.W__plus__] ], [ [P.ta__minus__, P.vt, P.Z] ], [ [P.ta__minus__, P.W__plus__, P.Z] ], [ [P.vt, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_443_1564,(0,0,1):C.R2GC_443_1565,(0,0,2):C.R2GC_443_1566,(0,0,3):C.R2GC_443_1567})

V_128 = CTVertex(name = 'V_128',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.u] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.u], [P.H, P.u] ], [ [P.G__plus__, P.s] ], [ [P.g, P.u] ], [ [P.s, P.W__plus__] ], [ [P.u, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_524_2015,(0,0,1):C.R2GC_528_2046,(0,0,2):C.R2GC_528_2047,(0,0,3):C.R2GC_528_2048,(0,0,4):C.R2GC_528_2049,(0,0,7):C.R2GC_524_2018,(0,0,5):C.R2GC_528_2050,(0,0,6):C.R2GC_528_2051,(0,0,8):C.R2GC_528_2052,(0,0,9):C.R2GC_524_2020,(0,1,0):C.R2GC_540_2111,(0,1,1):C.R2GC_542_2122,(0,1,3):C.R2GC_542_2123,(0,1,7):C.R2GC_540_2113,(0,1,5):C.R2GC_542_2124,(0,1,6):C.R2GC_542_2125,(0,1,9):C.R2GC_540_2115})

V_129 = CTVertex(name = 'V_129',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.c, P.g] ], [ [P.c, P.G0], [P.c, P.H] ], [ [P.c, P.Z] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_524_2015,(0,0,1):C.R2GC_524_2016,(0,0,2):C.R2GC_524_2017,(0,0,3):C.R2GC_524_2018,(0,0,4):C.R2GC_524_2019,(0,0,5):C.R2GC_524_2020,(0,0,6):C.R2GC_524_2021,(0,0,7):C.R2GC_524_2022,(0,0,8):C.R2GC_524_2023,(0,0,9):C.R2GC_524_2024,(0,1,0):C.R2GC_540_2111,(0,1,1):C.R2GC_540_2112,(0,1,3):C.R2GC_540_2113,(0,1,4):C.R2GC_540_2114,(0,1,5):C.R2GC_540_2115,(0,1,6):C.R2GC_540_2116,(0,1,8):C.R2GC_540_2117})

V_130 = CTVertex(name = 'V_130',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G0, P.t], [P.H, P.t] ], [ [P.G__plus__, P.s] ], [ [P.g, P.t] ], [ [P.s, P.W__plus__] ], [ [P.t, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_524_2015,(0,0,1):C.R2GC_527_2039,(0,0,2):C.R2GC_527_2040,(0,0,3):C.R2GC_527_2041,(0,0,4):C.R2GC_527_2042,(0,0,7):C.R2GC_524_2018,(0,0,5):C.R2GC_527_2043,(0,0,6):C.R2GC_527_2044,(0,0,8):C.R2GC_527_2045,(0,0,9):C.R2GC_524_2020,(0,1,0):C.R2GC_540_2111,(0,1,1):C.R2GC_541_2118,(0,1,3):C.R2GC_541_2119,(0,1,7):C.R2GC_540_2113,(0,1,5):C.R2GC_541_2120,(0,1,6):C.R2GC_541_2121,(0,1,9):C.R2GC_540_2115})

V_131 = CTVertex(name = 'V_131',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.d, P.g] ], [ [P.d, P.G0], [P.d, P.H] ], [ [P.d, P.Z] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_523_2005,(0,0,1):C.R2GC_525_2025,(0,0,2):C.R2GC_525_2026,(0,0,3):C.R2GC_523_2006,(0,0,4):C.R2GC_525_2027,(0,0,5):C.R2GC_523_2008,(0,0,6):C.R2GC_525_2028,(0,0,7):C.R2GC_525_2029,(0,0,8):C.R2GC_525_2030,(0,0,9):C.R2GC_525_2031,(0,1,0):C.R2GC_529_2053,(0,1,1):C.R2GC_530_2060,(0,1,3):C.R2GC_529_2054,(0,1,4):C.R2GC_530_2061,(0,1,5):C.R2GC_529_2056,(0,1,6):C.R2GC_530_2062,(0,1,7):C.R2GC_530_2063})

V_132 = CTVertex(name = 'V_132',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G0, P.s], [P.H, P.s] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.g, P.s] ], [ [P.s, P.Z] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_523_2005,(0,0,1):C.R2GC_526_2032,(0,0,2):C.R2GC_526_2033,(0,0,6):C.R2GC_523_2006,(0,0,3):C.R2GC_526_2034,(0,0,4):C.R2GC_526_2035,(0,0,5):C.R2GC_526_2036,(0,0,7):C.R2GC_523_2008,(0,0,8):C.R2GC_526_2037,(0,0,9):C.R2GC_526_2038,(0,1,0):C.R2GC_529_2053,(0,1,1):C.R2GC_531_2064,(0,1,6):C.R2GC_529_2054,(0,1,3):C.R2GC_531_2065,(0,1,4):C.R2GC_531_2066,(0,1,5):C.R2GC_531_2067,(0,1,7):C.R2GC_529_2056})

V_133 = CTVertex(name = 'V_133',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.G0], [P.b, P.H] ], [ [P.b, P.Z] ], [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_523_2005,(0,0,1):C.R2GC_523_2006,(0,0,2):C.R2GC_523_2007,(0,0,3):C.R2GC_523_2008,(0,0,4):C.R2GC_523_2009,(0,0,5):C.R2GC_523_2010,(0,0,6):C.R2GC_523_2011,(0,0,7):C.R2GC_523_2012,(0,0,8):C.R2GC_523_2013,(0,0,9):C.R2GC_523_2014,(0,1,0):C.R2GC_529_2053,(0,1,1):C.R2GC_529_2054,(0,1,2):C.R2GC_529_2055,(0,1,3):C.R2GC_529_2056,(0,1,4):C.R2GC_529_2057,(0,1,6):C.R2GC_529_2058,(0,1,7):C.R2GC_529_2059})

V_134 = CTVertex(name = 'V_134',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.e__minus__, P.G__plus__] ], [ [P.e__minus__, P.W__plus__] ], [ [P.ve, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_537_2106,(0,0,1):C.R2GC_537_2107,(0,0,2):C.R2GC_537_2108})

V_135 = CTVertex(name = 'V_135',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.mu__minus__] ], [ [P.mu__minus__, P.W__plus__] ], [ [P.vm, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_538_2109,(0,0,1):C.R2GC_537_2107,(0,0,2):C.R2GC_537_2108})

V_136 = CTVertex(name = 'V_136',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.ta__minus__] ], [ [P.ta__minus__, P.W__plus__] ], [ [P.vt, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_539_2110,(0,0,1):C.R2GC_537_2107,(0,0,2):C.R2GC_537_2108})

V_137 = CTVertex(name = 'V_137',
                 type = 'R2',
                 particles = [ P.e__plus__, P.e__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.G0], [P.e__minus__, P.H] ], [ [P.e__minus__, P.Z] ], [ [P.G__plus__, P.ve] ], [ [P.ve, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_534_2100,(0,0,1):C.R2GC_534_2101,(0,0,2):C.R2GC_534_2102,(0,0,4):C.R2GC_534_2103,(0,1,0):C.R2GC_543_2126,(0,1,1):C.R2GC_543_2127,(0,1,2):C.R2GC_543_2128,(0,1,3):C.R2GC_543_2129})

V_138 = CTVertex(name = 'V_138',
                 type = 'R2',
                 particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.G0, P.mu__minus__], [P.H, P.mu__minus__] ], [ [P.G__plus__, P.vm] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_534_2100,(0,0,1):C.R2GC_535_2104,(0,0,3):C.R2GC_534_2102,(0,0,4):C.R2GC_534_2103,(0,1,0):C.R2GC_543_2126,(0,1,1):C.R2GC_544_2130,(0,1,2):C.R2GC_544_2131,(0,1,3):C.R2GC_543_2128})

V_139 = CTVertex(name = 'V_139',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.G0, P.ta__minus__], [P.H, P.ta__minus__] ], [ [P.G__plus__, P.vt] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_534_2100,(0,0,1):C.R2GC_536_2105,(0,0,3):C.R2GC_534_2102,(0,0,4):C.R2GC_534_2103,(0,1,0):C.R2GC_543_2126,(0,1,1):C.R2GC_545_2132,(0,1,2):C.R2GC_545_2133,(0,1,3):C.R2GC_543_2128})

V_140 = CTVertex(name = 'V_140',
                 type = 'R2',
                 particles = [ P.H ],
                 color = [ '1' ],
                 lorentz = [ L.S1 ],
                 loop_particles = [ [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_195_273,(0,0,1):C.R2GC_195_274})

V_141 = CTVertex(name = 'V_141',
                 type = 'R2',
                 particles = [ P.e__plus__, P.e__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.e__minus__] ], [ [P.e__minus__, P.Z] ], [ [P.ve, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_387_1072,(0,1,1):C.R2GC_387_1073,(0,3,0):C.R2GC_387_1072,(0,3,1):C.R2GC_387_1073,(0,2,1):C.R2GC_279_789,(0,2,2):C.R2GC_279_790,(0,4,1):C.R2GC_280_791,(0,0,0):C.R2GC_159_11})

V_142 = CTVertex(name = 'V_142',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.e__minus__, P.W__plus__] ], [ [P.ve, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_279_790,(0,0,1):C.R2GC_332_913})

V_143 = CTVertex(name = 'V_143',
                 type = 'R2',
                 particles = [ P.mu__plus__, P.mu__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.mu__minus__] ], [ [P.mu__minus__, P.Z] ], [ [P.vm, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_388_1074,(0,1,1):C.R2GC_388_1075,(0,3,0):C.R2GC_388_1074,(0,3,1):C.R2GC_388_1075,(0,2,1):C.R2GC_279_789,(0,2,2):C.R2GC_279_790,(0,4,1):C.R2GC_280_791,(0,0,0):C.R2GC_159_11})

V_144 = CTVertex(name = 'V_144',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.mu__minus__, P.W__plus__] ], [ [P.vm, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_279_790,(0,0,1):C.R2GC_332_913})

V_145 = CTVertex(name = 'V_145',
                 type = 'R2',
                 particles = [ P.ta__plus__, P.ta__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.ta__minus__] ], [ [P.ta__minus__, P.Z] ], [ [P.vt, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_403_1082,(0,1,1):C.R2GC_403_1083,(0,3,0):C.R2GC_403_1082,(0,3,1):C.R2GC_403_1083,(0,2,1):C.R2GC_279_789,(0,2,2):C.R2GC_279_790,(0,4,1):C.R2GC_280_791,(0,0,0):C.R2GC_159_11})

V_146 = CTVertex(name = 'V_146',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.ta__minus__, P.W__plus__] ], [ [P.vt, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_279_790,(0,0,1):C.R2GC_332_913})

V_147 = CTVertex(name = 'V_147',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.u] ], [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.g, P.u] ], [ [P.s, P.W__plus__] ], [ [P.u, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_412_1084,(0,0,3):C.R2GC_412_1085,(0,0,5):C.R2GC_412_1086,(0,2,0):C.R2GC_412_1084,(0,2,3):C.R2GC_412_1085,(0,2,5):C.R2GC_412_1086,(0,1,0):C.R2GC_267_762,(0,1,1):C.R2GC_212_430,(0,1,2):C.R2GC_212_434,(0,1,3):C.R2GC_265_759,(0,1,4):C.R2GC_212_437,(0,1,5):C.R2GC_267_763,(0,3,0):C.R2GC_267_762,(0,3,3):C.R2GC_265_759,(0,3,5):C.R2GC_268_764})

V_148 = CTVertex(name = 'V_148',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.d] ], [ [P.c, P.W__plus__] ], [ [P.d, P.g] ], [ [P.d, P.Z] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_386_1069,(0,0,2):C.R2GC_386_1070,(0,0,3):C.R2GC_386_1071,(0,2,0):C.R2GC_386_1069,(0,2,2):C.R2GC_386_1070,(0,2,3):C.R2GC_386_1071,(0,1,0):C.R2GC_158_10,(0,1,1):C.R2GC_212_431,(0,1,2):C.R2GC_265_759,(0,1,3):C.R2GC_265_760,(0,1,4):C.R2GC_212_433,(0,1,5):C.R2GC_212_434,(0,3,0):C.R2GC_158_10,(0,3,2):C.R2GC_265_759,(0,3,3):C.R2GC_266_761})

V_149 = CTVertex(name = 'V_149',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_293_820,(0,0,1):C.R2GC_293_821,(0,0,2):C.R2GC_293_822})

V_150 = CTVertex(name = 'V_150',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_269_765,(0,0,1):C.R2GC_269_766,(0,0,2):C.R2GC_269_767})

V_151 = CTVertex(name = 'V_151',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_292_817,(0,0,1):C.R2GC_292_818,(0,0,2):C.R2GC_292_819})

V_152 = CTVertex(name = 'V_152',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.s] ], [ [P.c, P.W__plus__] ], [ [P.g, P.s] ], [ [P.s, P.Z] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_397_1076,(0,0,2):C.R2GC_397_1077,(0,0,3):C.R2GC_397_1078,(0,2,0):C.R2GC_397_1076,(0,2,2):C.R2GC_397_1077,(0,2,3):C.R2GC_397_1078,(0,1,0):C.R2GC_158_10,(0,1,1):C.R2GC_212_432,(0,1,2):C.R2GC_265_759,(0,1,3):C.R2GC_265_760,(0,1,4):C.R2GC_212_436,(0,1,5):C.R2GC_212_437,(0,3,0):C.R2GC_158_10,(0,3,2):C.R2GC_265_759,(0,3,3):C.R2GC_266_761})

V_153 = CTVertex(name = 'V_153',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_284_793,(0,0,1):C.R2GC_284_794,(0,0,2):C.R2GC_284_795})

V_154 = CTVertex(name = 'V_154',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_270_768,(0,0,1):C.R2GC_270_769,(0,0,2):C.R2GC_270_770})

V_155 = CTVertex(name = 'V_155',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_285_796,(0,0,1):C.R2GC_285_797,(0,0,2):C.R2GC_285_798})

V_156 = CTVertex(name = 'V_156',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF1, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.b] ], [ [P.b, P.g] ], [ [P.b, P.Z] ], [ [P.c, P.W__plus__] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,1,0):C.R2GC_380_1063,(0,1,1):C.R2GC_380_1064,(0,1,2):C.R2GC_380_1065,(0,3,0):C.R2GC_380_1063,(0,3,1):C.R2GC_380_1064,(0,3,2):C.R2GC_380_1065,(0,2,1):C.R2GC_265_759,(0,2,2):C.R2GC_265_760,(0,2,3):C.R2GC_212_428,(0,2,4):C.R2GC_212_429,(0,2,5):C.R2GC_212_430,(0,4,1):C.R2GC_265_759,(0,4,2):C.R2GC_266_761,(0,0,0):C.R2GC_158_10})

V_157 = CTVertex(name = 'V_157',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.c] ], [ [P.b, P.W__plus__] ], [ [P.c, P.g] ], [ [P.c, P.Z] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_381_1066,(0,0,2):C.R2GC_381_1067,(0,0,3):C.R2GC_381_1068,(0,2,0):C.R2GC_381_1066,(0,2,2):C.R2GC_381_1067,(0,2,3):C.R2GC_381_1068,(0,1,0):C.R2GC_267_762,(0,1,1):C.R2GC_212_428,(0,1,2):C.R2GC_265_759,(0,1,3):C.R2GC_267_763,(0,1,4):C.R2GC_212_431,(0,1,5):C.R2GC_212_432,(0,3,0):C.R2GC_267_762,(0,3,2):C.R2GC_265_759,(0,3,3):C.R2GC_268_764})

V_158 = CTVertex(name = 'V_158',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [P.a, P.t] ], [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.g, P.t] ], [ [P.s, P.W__plus__] ], [ [P.t, P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_402_1079,(0,0,3):C.R2GC_402_1080,(0,0,5):C.R2GC_402_1081,(0,2,0):C.R2GC_402_1079,(0,2,3):C.R2GC_402_1080,(0,2,5):C.R2GC_402_1081,(0,1,0):C.R2GC_267_762,(0,1,1):C.R2GC_212_429,(0,1,2):C.R2GC_212_433,(0,1,3):C.R2GC_265_759,(0,1,4):C.R2GC_212_436,(0,1,5):C.R2GC_267_763,(0,3,0):C.R2GC_267_762,(0,3,3):C.R2GC_265_759,(0,3,5):C.R2GC_268_764})

V_159 = CTVertex(name = 'V_159',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_314_865,(0,0,1):C.R2GC_314_866,(0,0,2):C.R2GC_314_867})

V_160 = CTVertex(name = 'V_160',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_322_889,(0,0,1):C.R2GC_322_890,(0,0,2):C.R2GC_322_891})

V_161 = CTVertex(name = 'V_161',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_315_868,(0,0,1):C.R2GC_315_869,(0,0,2):C.R2GC_315_870})

V_162 = CTVertex(name = 'V_162',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_305_844,(0,0,1):C.R2GC_305_845,(0,0,2):C.R2GC_305_846})

V_163 = CTVertex(name = 'V_163',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_323_892,(0,0,1):C.R2GC_323_893,(0,0,2):C.R2GC_323_894})

V_164 = CTVertex(name = 'V_164',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.b, P.W__plus__] ], [ [P.d, P.W__plus__] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_304_841,(0,0,1):C.R2GC_304_842,(0,0,2):C.R2GC_304_843})

V_165 = CTVertex(name = 'V_165',
                 type = 'R2',
                 particles = [ P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G0, P.Z] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_556_2228,(0,0,1):C.R2GC_556_2229,(0,0,2):C.R2GC_556_2230,(0,0,3):C.R2GC_556_2231,(0,0,6):C.R2GC_556_2232,(0,0,7):C.R2GC_556_2233,(0,0,8):C.R2GC_556_2234,(0,0,9):C.R2GC_556_2235,(0,0,10):C.R2GC_556_2236,(0,0,11):C.R2GC_558_2260,(0,0,12):C.R2GC_558_2261,(0,0,4):C.R2GC_558_2262,(0,0,5):C.R2GC_556_2239,(0,1,0):C.R2GC_206_360,(0,1,1):C.R2GC_206_361,(0,1,2):C.R2GC_206_362,(0,1,3):C.R2GC_206_363,(0,1,6):C.R2GC_206_364,(0,1,7):C.R2GC_206_365,(0,1,8):C.R2GC_206_366,(0,1,9):C.R2GC_206_367,(0,1,10):C.R2GC_206_368,(0,1,4):C.R2GC_206_369,(0,1,5):C.R2GC_206_370})

V_166 = CTVertex(name = 'V_166',
                 type = 'R2',
                 particles = [ P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS4 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.H, P.Z] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_556_2228,(0,0,1):C.R2GC_556_2229,(0,0,2):C.R2GC_556_2230,(0,0,3):C.R2GC_556_2231,(0,0,6):C.R2GC_556_2232,(0,0,7):C.R2GC_556_2233,(0,0,8):C.R2GC_556_2234,(0,0,9):C.R2GC_556_2235,(0,0,10):C.R2GC_556_2236,(0,0,11):C.R2GC_556_2237,(0,0,12):C.R2GC_556_2238,(0,0,4):C.R2GC_556_2239,(0,0,5):C.R2GC_556_2240,(0,1,0):C.R2GC_206_360,(0,1,1):C.R2GC_206_361,(0,1,2):C.R2GC_206_362,(0,1,3):C.R2GC_206_363,(0,1,6):C.R2GC_206_364,(0,1,7):C.R2GC_206_365,(0,1,8):C.R2GC_206_366,(0,1,9):C.R2GC_206_367,(0,1,10):C.R2GC_206_368,(0,1,4):C.R2GC_206_370,(0,1,5):C.R2GC_206_369})

V_167 = CTVertex(name = 'V_167',
                 type = 'R2',
                 particles = [ P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS2 ],
                 loop_particles = [ [ [P.a, P.G__plus__] ], [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__], [P.H, P.W__plus__] ], [ [P.G__plus__, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,18):C.R2GC_556_2237,(0,0,20):C.R2GC_557_2241,(0,0,0):C.R2GC_557_2242,(0,0,1):C.R2GC_557_2243,(0,0,2):C.R2GC_557_2244,(0,0,3):C.R2GC_557_2245,(0,0,4):C.R2GC_557_2246,(0,0,5):C.R2GC_557_2247,(0,0,6):C.R2GC_557_2248,(0,0,7):C.R2GC_557_2249,(0,0,8):C.R2GC_557_2250,(0,0,9):C.R2GC_557_2251,(0,0,10):C.R2GC_557_2252,(0,0,12):C.R2GC_557_2253,(0,0,13):C.R2GC_557_2254,(0,0,14):C.R2GC_557_2255,(0,0,15):C.R2GC_557_2256,(0,0,16):C.R2GC_557_2257,(0,0,17):C.R2GC_557_2258,(0,0,19):C.R2GC_557_2259,(0,1,0):C.R2GC_207_371,(0,1,2):C.R2GC_207_372,(0,1,3):C.R2GC_207_373,(0,1,4):C.R2GC_207_374,(0,1,5):C.R2GC_207_375,(0,1,6):C.R2GC_207_376,(0,1,7):C.R2GC_207_377,(0,1,8):C.R2GC_207_378,(0,1,9):C.R2GC_206_363,(0,1,11):C.R2GC_207_379,(0,1,12):C.R2GC_207_380,(0,1,14):C.R2GC_206_364,(0,1,15):C.R2GC_207_381,(0,1,16):C.R2GC_207_382,(0,1,17):C.R2GC_206_367})

V_168 = CTVertex(name = 'V_168',
                 type = 'R2',
                 particles = [ P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,12):C.R2GC_191_253,(0,1,0):C.R2GC_192_254,(0,1,2):C.R2GC_192_255,(0,1,4):C.R2GC_192_256,(0,1,5):C.R2GC_192_257,(0,1,7):C.R2GC_192_258,(0,1,8):C.R2GC_192_259,(0,1,9):C.R2GC_192_260,(0,1,10):C.R2GC_192_261,(0,1,11):C.R2GC_192_262,(0,1,12):C.R2GC_192_263,(0,2,1):C.R2GC_191_251,(0,2,3):C.R2GC_191_252,(0,2,6):C.R2GC_191_253,(0,2,12):C.R2GC_159_11})

V_169 = CTVertex(name = 'V_169',
                 type = 'R2',
                 particles = [ P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,12):C.R2GC_338_915,(0,1,0):C.R2GC_415_1087,(0,1,2):C.R2GC_415_1088,(0,1,4):C.R2GC_415_1089,(0,1,5):C.R2GC_415_1090,(0,1,7):C.R2GC_415_1091,(0,1,8):C.R2GC_415_1092,(0,1,9):C.R2GC_415_1093,(0,1,10):C.R2GC_415_1094,(0,1,11):C.R2GC_415_1095,(0,1,12):C.R2GC_415_1096,(0,2,1):C.R2GC_194_269,(0,2,3):C.R2GC_194_270,(0,2,6):C.R2GC_194_271,(0,2,12):C.R2GC_194_272})

V_170 = CTVertex(name = 'V_170',
                 type = 'R2',
                 particles = [ P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.d], [P.s] ], [ [P.c] ], [ [P.c], [P.t], [P.u] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.e__minus__], [P.mu__minus__], [P.ta__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.ve], [P.vm], [P.vt] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,13):C.R2GC_335_914,(0,1,0):C.R2GC_568_2396,(0,1,2):C.R2GC_568_2397,(0,1,4):C.R2GC_568_2398,(0,1,5):C.R2GC_568_2399,(0,1,7):C.R2GC_568_2400,(0,1,8):C.R2GC_568_2401,(0,1,9):C.R2GC_568_2402,(0,1,10):C.R2GC_568_2403,(0,1,11):C.R2GC_568_2404,(0,1,13):C.R2GC_568_2405,(0,2,1):C.R2GC_193_264,(0,2,3):C.R2GC_193_265,(0,2,6):C.R2GC_193_266,(0,2,12):C.R2GC_193_267,(0,2,13):C.R2GC_193_268})

V_171 = CTVertex(name = 'V_171',
                 type = 'R2',
                 particles = [ P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV3 ],
                 loop_particles = [ [ [P.a, P.W__plus__] ], [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.e__minus__, P.ve] ], [ [P.e__minus__, P.ve], [P.mu__minus__, P.vm], [P.ta__minus__, P.vt] ], [ [P.mu__minus__, P.vm] ], [ [P.s, P.t] ], [ [P.s, P.u] ], [ [P.ta__minus__, P.vt] ], [ [P.W__plus__] ], [ [P.W__plus__, P.Z] ], [ [P.Z] ] ],
                 couplings = {(0,0,0):C.R2GC_191_253,(0,0,15):C.R2GC_335_914,(0,1,14):C.R2GC_562_2309,(0,1,16):C.R2GC_562_2310,(0,1,0):C.R2GC_562_2311,(0,1,1):C.R2GC_562_2312,(0,1,2):C.R2GC_562_2313,(0,1,3):C.R2GC_562_2314,(0,1,4):C.R2GC_562_2315,(0,1,5):C.R2GC_562_2316,(0,1,6):C.R2GC_562_2317,(0,1,7):C.R2GC_562_2318,(0,1,8):C.R2GC_562_2319,(0,1,10):C.R2GC_562_2320,(0,1,11):C.R2GC_562_2321,(0,1,12):C.R2GC_562_2322,(0,1,13):C.R2GC_562_2323,(0,1,15):C.R2GC_562_2324,(0,2,0):C.R2GC_159_11,(0,2,1):C.R2GC_212_428,(0,2,2):C.R2GC_212_429,(0,2,3):C.R2GC_212_430,(0,2,4):C.R2GC_212_431,(0,2,5):C.R2GC_212_432,(0,2,6):C.R2GC_212_433,(0,2,7):C.R2GC_212_434,(0,2,9):C.R2GC_212_435,(0,2,11):C.R2GC_212_436,(0,2,12):C.R2GC_212_437,(0,2,15):C.R2GC_193_268})

V_172 = CTVertex(name = 'V_172',
                 type = 'R2',
                 particles = [ P.g, P.g ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VV1, L.VV2, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.c] ], [ [P.d] ], [ [P.g] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,4):C.R2GC_281_792,(0,1,0):C.R2GC_174_80,(0,1,2):C.R2GC_174_81,(0,1,3):C.R2GC_174_82,(0,1,5):C.R2GC_174_83,(0,1,6):C.R2GC_174_84,(0,1,7):C.R2GC_174_85,(0,2,1):C.R2GC_173_78,(0,2,4):C.R2GC_173_79})

V_173 = CTVertex(name = 'V_173',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.d, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_608_2625,(0,0,2):C.R2GC_608_2626,(0,0,4):C.R2GC_608_2627,(0,0,1):C.R2GC_608_2628,(0,0,3):C.R2GC_608_2629,(0,0,5):C.R2GC_608_2630,(0,1,0):C.R2GC_604_2601,(0,1,2):C.R2GC_604_2602,(0,1,4):C.R2GC_604_2603,(0,1,1):C.R2GC_604_2604,(0,1,3):C.R2GC_604_2605,(0,1,5):C.R2GC_604_2606})

V_174 = CTVertex(name = 'V_174',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.d, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_578_2465,(0,0,2):C.R2GC_578_2466,(0,0,4):C.R2GC_578_2467,(0,0,1):C.R2GC_578_2468,(0,0,3):C.R2GC_578_2469,(0,0,5):C.R2GC_578_2470,(0,1,0):C.R2GC_582_2489,(0,1,2):C.R2GC_582_2490,(0,1,4):C.R2GC_582_2491,(0,1,1):C.R2GC_582_2492,(0,1,3):C.R2GC_582_2493,(0,1,5):C.R2GC_582_2494})

V_175 = CTVertex(name = 'V_175',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.s, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_605_2607,(0,0,2):C.R2GC_605_2608,(0,0,4):C.R2GC_605_2609,(0,0,1):C.R2GC_605_2610,(0,0,3):C.R2GC_605_2611,(0,0,5):C.R2GC_605_2612,(0,1,0):C.R2GC_609_2631,(0,1,2):C.R2GC_609_2632,(0,1,4):C.R2GC_609_2633,(0,1,1):C.R2GC_609_2634,(0,1,3):C.R2GC_609_2635,(0,1,5):C.R2GC_609_2636})

V_176 = CTVertex(name = 'V_176',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.s, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_597_2559,(0,0,2):C.R2GC_597_2560,(0,0,4):C.R2GC_597_2561,(0,0,1):C.R2GC_597_2562,(0,0,3):C.R2GC_597_2563,(0,0,5):C.R2GC_597_2564,(0,1,0):C.R2GC_601_2583,(0,1,2):C.R2GC_601_2584,(0,1,4):C.R2GC_601_2585,(0,1,1):C.R2GC_601_2586,(0,1,3):C.R2GC_601_2587,(0,1,5):C.R2GC_601_2588})

V_177 = CTVertex(name = 'V_177',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.b, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_581_2483,(0,0,2):C.R2GC_581_2484,(0,0,4):C.R2GC_581_2485,(0,0,1):C.R2GC_581_2486,(0,0,3):C.R2GC_581_2487,(0,0,5):C.R2GC_581_2488,(0,1,0):C.R2GC_577_2459,(0,1,2):C.R2GC_577_2460,(0,1,4):C.R2GC_577_2461,(0,1,1):C.R2GC_577_2462,(0,1,3):C.R2GC_577_2463,(0,1,5):C.R2GC_577_2464})

V_178 = CTVertex(name = 'V_178',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.b, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_600_2577,(0,0,2):C.R2GC_600_2578,(0,0,4):C.R2GC_600_2579,(0,0,1):C.R2GC_600_2580,(0,0,3):C.R2GC_600_2581,(0,0,5):C.R2GC_600_2582,(0,1,0):C.R2GC_596_2553,(0,1,2):C.R2GC_596_2554,(0,1,4):C.R2GC_596_2555,(0,1,1):C.R2GC_596_2556,(0,1,3):C.R2GC_596_2557,(0,1,5):C.R2GC_596_2558})

V_179 = CTVertex(name = 'V_179',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.u, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_640_2829,(0,0,2):C.R2GC_640_2830,(0,0,4):C.R2GC_640_2831,(0,0,1):C.R2GC_640_2832,(0,0,3):C.R2GC_640_2833,(0,0,5):C.R2GC_640_2834,(0,1,0):C.R2GC_644_2853,(0,1,2):C.R2GC_644_2854,(0,1,4):C.R2GC_644_2855,(0,1,1):C.R2GC_644_2856,(0,1,3):C.R2GC_644_2857,(0,1,5):C.R2GC_644_2858})

V_180 = CTVertex(name = 'V_180',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.u, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_648_2877,(0,0,2):C.R2GC_648_2878,(0,0,4):C.R2GC_648_2879,(0,0,1):C.R2GC_648_2880,(0,0,3):C.R2GC_648_2881,(0,0,5):C.R2GC_648_2882,(0,1,0):C.R2GC_652_2901,(0,1,2):C.R2GC_652_2902,(0,1,4):C.R2GC_652_2903,(0,1,1):C.R2GC_652_2904,(0,1,3):C.R2GC_652_2905,(0,1,5):C.R2GC_652_2906})

V_181 = CTVertex(name = 'V_181',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.c, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_643_2847,(0,0,2):C.R2GC_643_2848,(0,0,4):C.R2GC_643_2849,(0,0,1):C.R2GC_643_2850,(0,0,3):C.R2GC_643_2851,(0,0,5):C.R2GC_643_2852,(0,1,0):C.R2GC_639_2823,(0,1,2):C.R2GC_639_2824,(0,1,4):C.R2GC_639_2825,(0,1,1):C.R2GC_639_2826,(0,1,3):C.R2GC_639_2827,(0,1,5):C.R2GC_639_2828})

V_182 = CTVertex(name = 'V_182',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.c, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_628_2768,(0,0,2):C.R2GC_628_2769,(0,0,4):C.R2GC_628_2770,(0,0,1):C.R2GC_628_2771,(0,0,3):C.R2GC_628_2772,(0,0,5):C.R2GC_628_2773,(0,1,0):C.R2GC_624_2744,(0,1,2):C.R2GC_624_2745,(0,1,4):C.R2GC_624_2746,(0,1,1):C.R2GC_624_2747,(0,1,3):C.R2GC_624_2748,(0,1,5):C.R2GC_624_2749})

V_183 = CTVertex(name = 'V_183',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.t, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_651_2895,(0,0,2):C.R2GC_651_2896,(0,0,4):C.R2GC_651_2897,(0,0,1):C.R2GC_651_2898,(0,0,3):C.R2GC_651_2899,(0,0,5):C.R2GC_651_2900,(0,1,0):C.R2GC_647_2871,(0,1,2):C.R2GC_647_2872,(0,1,4):C.R2GC_647_2873,(0,1,1):C.R2GC_647_2874,(0,1,3):C.R2GC_647_2875,(0,1,5):C.R2GC_647_2876})

V_184 = CTVertex(name = 'V_184',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.t, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_625_2750,(0,0,2):C.R2GC_625_2751,(0,0,4):C.R2GC_625_2752,(0,0,1):C.R2GC_625_2753,(0,0,3):C.R2GC_625_2754,(0,0,5):C.R2GC_625_2755,(0,1,0):C.R2GC_629_2774,(0,1,2):C.R2GC_629_2775,(0,1,4):C.R2GC_629_2776,(0,1,1):C.R2GC_629_2777,(0,1,3):C.R2GC_629_2778,(0,1,5):C.R2GC_629_2779})

V_185 = CTVertex(name = 'V_185',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.d, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_607_2619,(0,0,2):C.R2GC_607_2620,(0,0,4):C.R2GC_607_2621,(0,0,1):C.R2GC_607_2622,(0,0,3):C.R2GC_607_2623,(0,0,5):C.R2GC_607_2624,(0,1,0):C.R2GC_606_2613,(0,1,2):C.R2GC_606_2614,(0,1,4):C.R2GC_606_2615,(0,1,1):C.R2GC_606_2616,(0,1,3):C.R2GC_606_2617,(0,1,5):C.R2GC_606_2618})

V_186 = CTVertex(name = 'V_186',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.d, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_576_2453,(0,0,2):C.R2GC_576_2454,(0,0,4):C.R2GC_576_2455,(0,0,1):C.R2GC_576_2456,(0,0,3):C.R2GC_576_2457,(0,0,5):C.R2GC_576_2458,(0,1,0):C.R2GC_583_2495,(0,1,2):C.R2GC_583_2496,(0,1,4):C.R2GC_583_2497,(0,1,1):C.R2GC_583_2498,(0,1,3):C.R2GC_583_2499,(0,1,5):C.R2GC_583_2500})

V_187 = CTVertex(name = 'V_187',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.s, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_603_2595,(0,0,2):C.R2GC_603_2596,(0,0,4):C.R2GC_603_2597,(0,0,1):C.R2GC_603_2598,(0,0,3):C.R2GC_603_2599,(0,0,5):C.R2GC_603_2600,(0,1,0):C.R2GC_610_2637,(0,1,2):C.R2GC_610_2638,(0,1,4):C.R2GC_610_2639,(0,1,1):C.R2GC_610_2640,(0,1,3):C.R2GC_610_2641,(0,1,5):C.R2GC_610_2642})

V_188 = CTVertex(name = 'V_188',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.s, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_595_2547,(0,0,2):C.R2GC_595_2548,(0,0,4):C.R2GC_595_2549,(0,0,1):C.R2GC_595_2550,(0,0,3):C.R2GC_595_2551,(0,0,5):C.R2GC_595_2552,(0,1,0):C.R2GC_602_2589,(0,1,2):C.R2GC_602_2590,(0,1,4):C.R2GC_602_2591,(0,1,1):C.R2GC_602_2592,(0,1,3):C.R2GC_602_2593,(0,1,5):C.R2GC_602_2594})

V_189 = CTVertex(name = 'V_189',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.b, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_580_2477,(0,0,2):C.R2GC_580_2478,(0,0,4):C.R2GC_580_2479,(0,0,1):C.R2GC_580_2480,(0,0,3):C.R2GC_580_2481,(0,0,5):C.R2GC_580_2482,(0,1,0):C.R2GC_579_2471,(0,1,2):C.R2GC_579_2472,(0,1,4):C.R2GC_579_2473,(0,1,1):C.R2GC_579_2474,(0,1,3):C.R2GC_579_2475,(0,1,5):C.R2GC_579_2476})

V_190 = CTVertex(name = 'V_190',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.b, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.t, P.W__plus__] ], [ [P.G__plus__, P.u] ], [ [P.G__plus__, P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_599_2571,(0,0,2):C.R2GC_599_2572,(0,0,4):C.R2GC_599_2573,(0,0,1):C.R2GC_599_2574,(0,0,3):C.R2GC_599_2575,(0,0,5):C.R2GC_599_2576,(0,1,0):C.R2GC_598_2565,(0,1,2):C.R2GC_598_2566,(0,1,4):C.R2GC_598_2567,(0,1,1):C.R2GC_598_2568,(0,1,3):C.R2GC_598_2569,(0,1,5):C.R2GC_598_2570})

V_191 = CTVertex(name = 'V_191',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.u, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_641_2835,(0,0,2):C.R2GC_641_2836,(0,0,4):C.R2GC_641_2837,(0,0,1):C.R2GC_641_2838,(0,0,3):C.R2GC_641_2839,(0,0,5):C.R2GC_641_2840,(0,1,0):C.R2GC_642_2841,(0,1,2):C.R2GC_642_2842,(0,1,4):C.R2GC_642_2843,(0,1,1):C.R2GC_642_2844,(0,1,3):C.R2GC_642_2845,(0,1,5):C.R2GC_642_2846})

V_192 = CTVertex(name = 'V_192',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.u, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_649_2883,(0,0,2):C.R2GC_649_2884,(0,0,4):C.R2GC_649_2885,(0,0,1):C.R2GC_649_2886,(0,0,3):C.R2GC_649_2887,(0,0,5):C.R2GC_649_2888,(0,1,0):C.R2GC_650_2889,(0,1,2):C.R2GC_650_2890,(0,1,4):C.R2GC_650_2891,(0,1,1):C.R2GC_650_2892,(0,1,3):C.R2GC_650_2893,(0,1,5):C.R2GC_650_2894})

V_193 = CTVertex(name = 'V_193',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.c, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_645_2859,(0,0,2):C.R2GC_645_2860,(0,0,4):C.R2GC_645_2861,(0,0,1):C.R2GC_645_2862,(0,0,3):C.R2GC_645_2863,(0,0,5):C.R2GC_645_2864,(0,1,0):C.R2GC_638_2817,(0,1,2):C.R2GC_638_2818,(0,1,4):C.R2GC_638_2819,(0,1,1):C.R2GC_638_2820,(0,1,3):C.R2GC_638_2821,(0,1,5):C.R2GC_638_2822})

V_194 = CTVertex(name = 'V_194',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.c, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_630_2780,(0,0,2):C.R2GC_630_2781,(0,0,4):C.R2GC_630_2782,(0,0,1):C.R2GC_630_2783,(0,0,3):C.R2GC_630_2784,(0,0,5):C.R2GC_630_2785,(0,1,0):C.R2GC_623_2738,(0,1,2):C.R2GC_623_2739,(0,1,4):C.R2GC_623_2740,(0,1,1):C.R2GC_623_2741,(0,1,3):C.R2GC_623_2742,(0,1,5):C.R2GC_623_2743})

V_195 = CTVertex(name = 'V_195',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.t, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_653_2907,(0,0,2):C.R2GC_653_2908,(0,0,4):C.R2GC_653_2909,(0,0,1):C.R2GC_653_2910,(0,0,3):C.R2GC_653_2911,(0,0,5):C.R2GC_653_2912,(0,1,0):C.R2GC_646_2865,(0,1,2):C.R2GC_646_2866,(0,1,4):C.R2GC_646_2867,(0,1,1):C.R2GC_646_2868,(0,1,3):C.R2GC_646_2869,(0,1,5):C.R2GC_646_2870})

V_196 = CTVertex(name = 'V_196',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.t, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.G__plus__, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.G__plus__, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.G__plus__, P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_626_2756,(0,0,2):C.R2GC_626_2757,(0,0,4):C.R2GC_626_2758,(0,0,1):C.R2GC_626_2759,(0,0,3):C.R2GC_626_2760,(0,0,5):C.R2GC_626_2761,(0,1,0):C.R2GC_627_2762,(0,1,2):C.R2GC_627_2763,(0,1,4):C.R2GC_627_2764,(0,1,1):C.R2GC_627_2765,(0,1,3):C.R2GC_627_2766,(0,1,5):C.R2GC_627_2767})

V_197 = CTVertex(name = 'V_197',
                 type = 'R2',
                 particles = [ P.ve__tilde__, P.ve, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.e__minus__, P.G__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_511_1963})

V_198 = CTVertex(name = 'V_198',
                 type = 'R2',
                 particles = [ P.vm__tilde__, P.vm, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.mu__minus__] ] ],
                 couplings = {(0,0,0):C.R2GC_512_1964})

V_199 = CTVertex(name = 'V_199',
                 type = 'R2',
                 particles = [ P.vt__tilde__, P.vt, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [P.G__plus__, P.ta__minus__] ] ],
                 couplings = {(0,0,0):C.R2GC_513_1965})

V_200 = CTVertex(name = 'V_200',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.d, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_294_823,(0,0,1):C.R2GC_294_824,(0,0,2):C.R2GC_294_825,(0,0,3):C.R2GC_294_826,(0,0,4):C.R2GC_294_827,(0,0,5):C.R2GC_294_828,(0,1,0):C.R2GC_298_835,(0,1,2):C.R2GC_298_836,(0,1,3):C.R2GC_298_837})

V_201 = CTVertex(name = 'V_201',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.d, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_272_777,(0,0,1):C.R2GC_272_778,(0,0,2):C.R2GC_272_779,(0,0,3):C.R2GC_272_780,(0,0,4):C.R2GC_272_781,(0,0,5):C.R2GC_272_782,(0,1,0):C.R2GC_276_786,(0,1,2):C.R2GC_276_787,(0,1,3):C.R2GC_276_788})

V_202 = CTVertex(name = 'V_202',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.s, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_295_829,(0,0,1):C.R2GC_295_830,(0,0,2):C.R2GC_295_831,(0,0,3):C.R2GC_295_832,(0,0,4):C.R2GC_295_833,(0,0,5):C.R2GC_295_834,(0,1,0):C.R2GC_299_838,(0,1,2):C.R2GC_299_839,(0,1,3):C.R2GC_299_840})

V_203 = CTVertex(name = 'V_203',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.b, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_271_771,(0,0,1):C.R2GC_271_772,(0,0,2):C.R2GC_271_773,(0,0,3):C.R2GC_271_774,(0,0,4):C.R2GC_271_775,(0,0,5):C.R2GC_271_776,(0,1,0):C.R2GC_275_783,(0,1,2):C.R2GC_275_784,(0,1,3):C.R2GC_275_785})

V_204 = CTVertex(name = 'V_204',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.s, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_287_805,(0,0,1):C.R2GC_287_806,(0,0,2):C.R2GC_287_807,(0,0,3):C.R2GC_287_808,(0,0,4):C.R2GC_287_809,(0,0,5):C.R2GC_287_810,(0,1,0):C.R2GC_291_814,(0,1,2):C.R2GC_291_815,(0,1,3):C.R2GC_291_816})

V_205 = CTVertex(name = 'V_205',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.b, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_286_799,(0,0,1):C.R2GC_286_800,(0,0,2):C.R2GC_286_801,(0,0,3):C.R2GC_286_802,(0,0,4):C.R2GC_286_803,(0,0,5):C.R2GC_286_804,(0,1,0):C.R2GC_290_811,(0,1,2):C.R2GC_290_812,(0,1,3):C.R2GC_290_813})

V_206 = CTVertex(name = 'V_206',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.u, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_316_871,(0,0,1):C.R2GC_316_872,(0,0,2):C.R2GC_316_873,(0,0,3):C.R2GC_316_874,(0,0,4):C.R2GC_316_875,(0,0,5):C.R2GC_316_876,(0,1,0):C.R2GC_320_883,(0,1,2):C.R2GC_320_884,(0,1,4):C.R2GC_320_885})

V_207 = CTVertex(name = 'V_207',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.u, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_324_895,(0,0,1):C.R2GC_324_896,(0,0,2):C.R2GC_324_897,(0,0,3):C.R2GC_324_898,(0,0,4):C.R2GC_324_899,(0,0,5):C.R2GC_324_900,(0,1,0):C.R2GC_328_907,(0,1,2):C.R2GC_328_908,(0,1,4):C.R2GC_328_909})

V_208 = CTVertex(name = 'V_208',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.c, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_317_877,(0,0,1):C.R2GC_317_878,(0,0,2):C.R2GC_317_879,(0,0,3):C.R2GC_317_880,(0,0,4):C.R2GC_317_881,(0,0,5):C.R2GC_317_882,(0,1,0):C.R2GC_321_886,(0,1,2):C.R2GC_321_887,(0,1,4):C.R2GC_321_888})

V_209 = CTVertex(name = 'V_209',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.t, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_325_901,(0,0,1):C.R2GC_325_902,(0,0,2):C.R2GC_325_903,(0,0,3):C.R2GC_325_904,(0,0,4):C.R2GC_325_905,(0,0,5):C.R2GC_325_906,(0,1,0):C.R2GC_329_910,(0,1,2):C.R2GC_329_911,(0,1,4):C.R2GC_329_912})

V_210 = CTVertex(name = 'V_210',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.c, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_307_853,(0,0,1):C.R2GC_307_854,(0,0,2):C.R2GC_307_855,(0,0,3):C.R2GC_307_856,(0,0,4):C.R2GC_307_857,(0,0,5):C.R2GC_307_858,(0,1,0):C.R2GC_311_862,(0,1,2):C.R2GC_311_863,(0,1,4):C.R2GC_311_864})

V_211 = CTVertex(name = 'V_211',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.t, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_306_847,(0,0,1):C.R2GC_306_848,(0,0,2):C.R2GC_306_849,(0,0,3):C.R2GC_306_850,(0,0,4):C.R2GC_306_851,(0,0,5):C.R2GC_306_852,(0,1,0):C.R2GC_310_859,(0,1,2):C.R2GC_310_860,(0,1,4):C.R2GC_310_861})

V_212 = CTVertex(name = 'V_212',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_481_1812,(0,0,1):C.R2GC_481_1813,(0,0,2):C.R2GC_481_1814,(0,0,3):C.R2GC_481_1815,(0,0,4):C.R2GC_481_1816,(0,0,5):C.R2GC_481_1817,(0,1,0):C.R2GC_484_1827,(0,1,2):C.R2GC_484_1828,(0,1,3):C.R2GC_484_1829})

V_213 = CTVertex(name = 'V_213',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_474_1782,(0,0,1):C.R2GC_474_1783,(0,0,2):C.R2GC_474_1784,(0,0,3):C.R2GC_474_1785,(0,0,4):C.R2GC_474_1786,(0,0,5):C.R2GC_474_1787,(0,1,0):C.R2GC_475_1788,(0,1,2):C.R2GC_475_1789,(0,1,3):C.R2GC_475_1790})

V_214 = CTVertex(name = 'V_214',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_482_1818,(0,0,1):C.R2GC_482_1819,(0,0,2):C.R2GC_482_1820,(0,0,3):C.R2GC_482_1821,(0,0,4):C.R2GC_482_1822,(0,0,5):C.R2GC_482_1823,(0,1,0):C.R2GC_483_1824,(0,1,2):C.R2GC_483_1825,(0,1,3):C.R2GC_483_1826})

V_215 = CTVertex(name = 'V_215',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_473_1776,(0,0,1):C.R2GC_473_1777,(0,0,2):C.R2GC_473_1778,(0,0,3):C.R2GC_473_1779,(0,0,4):C.R2GC_473_1780,(0,0,5):C.R2GC_473_1781,(0,1,0):C.R2GC_476_1791,(0,1,2):C.R2GC_476_1792,(0,1,3):C.R2GC_476_1793})

V_216 = CTVertex(name = 'V_216',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_478_1800,(0,0,1):C.R2GC_478_1801,(0,0,2):C.R2GC_478_1802,(0,0,3):C.R2GC_478_1803,(0,0,4):C.R2GC_478_1804,(0,0,5):C.R2GC_478_1805,(0,1,0):C.R2GC_479_1806,(0,1,2):C.R2GC_479_1807,(0,1,3):C.R2GC_479_1808})

V_217 = CTVertex(name = 'V_217',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_477_1794,(0,0,1):C.R2GC_477_1795,(0,0,2):C.R2GC_477_1796,(0,0,3):C.R2GC_477_1797,(0,0,4):C.R2GC_477_1798,(0,0,5):C.R2GC_477_1799,(0,1,0):C.R2GC_480_1809,(0,1,2):C.R2GC_480_1810,(0,1,3):C.R2GC_480_1811})

V_218 = CTVertex(name = 'V_218',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_490_1854,(0,0,1):C.R2GC_490_1855,(0,0,2):C.R2GC_490_1856,(0,0,3):C.R2GC_490_1857,(0,0,4):C.R2GC_490_1858,(0,0,5):C.R2GC_490_1859,(0,1,0):C.R2GC_492_1863,(0,1,2):C.R2GC_492_1864,(0,1,4):C.R2GC_492_1865})

V_219 = CTVertex(name = 'V_219',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_494_1872,(0,0,1):C.R2GC_494_1873,(0,0,2):C.R2GC_494_1874,(0,0,3):C.R2GC_494_1875,(0,0,4):C.R2GC_494_1876,(0,0,5):C.R2GC_494_1877,(0,1,0):C.R2GC_496_1881,(0,1,2):C.R2GC_496_1882,(0,1,4):C.R2GC_496_1883})

V_220 = CTVertex(name = 'V_220',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_489_1848,(0,0,1):C.R2GC_489_1849,(0,0,2):C.R2GC_489_1850,(0,0,3):C.R2GC_489_1851,(0,0,4):C.R2GC_489_1852,(0,0,5):C.R2GC_489_1853,(0,1,0):C.R2GC_491_1860,(0,1,2):C.R2GC_491_1861,(0,1,4):C.R2GC_491_1862})

V_221 = CTVertex(name = 'V_221',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_493_1866,(0,0,1):C.R2GC_493_1867,(0,0,2):C.R2GC_493_1868,(0,0,3):C.R2GC_493_1869,(0,0,4):C.R2GC_493_1870,(0,0,5):C.R2GC_493_1871,(0,1,0):C.R2GC_495_1878,(0,1,2):C.R2GC_495_1879,(0,1,4):C.R2GC_495_1880})

V_222 = CTVertex(name = 'V_222',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_485_1830,(0,0,1):C.R2GC_485_1831,(0,0,2):C.R2GC_485_1832,(0,0,3):C.R2GC_485_1833,(0,0,4):C.R2GC_485_1834,(0,0,5):C.R2GC_485_1835,(0,1,0):C.R2GC_487_1842,(0,1,2):C.R2GC_487_1843,(0,1,4):C.R2GC_487_1844})

V_223 = CTVertex(name = 'V_223',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_486_1836,(0,0,1):C.R2GC_486_1837,(0,0,2):C.R2GC_486_1838,(0,0,3):C.R2GC_486_1839,(0,0,4):C.R2GC_486_1840,(0,0,5):C.R2GC_486_1841,(0,1,0):C.R2GC_488_1845,(0,1,2):C.R2GC_488_1846,(0,1,4):C.R2GC_488_1847})

V_224 = CTVertex(name = 'V_224',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_358_989,(0,0,1):C.R2GC_358_990,(0,0,2):C.R2GC_358_991,(0,0,3):C.R2GC_358_992,(0,0,4):C.R2GC_358_993,(0,0,5):C.R2GC_358_994,(0,1,0):C.R2GC_360_998,(0,1,2):C.R2GC_360_999,(0,1,3):C.R2GC_360_1000})

V_225 = CTVertex(name = 'V_225',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_341_916,(0,0,1):C.R2GC_341_917,(0,0,2):C.R2GC_341_918,(0,0,3):C.R2GC_341_919,(0,0,4):C.R2GC_341_920,(0,0,5):C.R2GC_341_921,(0,1,0):C.R2GC_343_928,(0,1,2):C.R2GC_343_929,(0,1,3):C.R2GC_343_930})

V_226 = CTVertex(name = 'V_226',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_357_983,(0,0,1):C.R2GC_357_984,(0,0,2):C.R2GC_357_985,(0,0,3):C.R2GC_357_986,(0,0,4):C.R2GC_357_987,(0,0,5):C.R2GC_357_988,(0,1,0):C.R2GC_359_995,(0,1,2):C.R2GC_359_996,(0,1,3):C.R2GC_359_997})

V_227 = CTVertex(name = 'V_227',
                 type = 'R2',
                 particles = [ P.b__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_353_965,(0,0,1):C.R2GC_353_966,(0,0,2):C.R2GC_353_967,(0,0,3):C.R2GC_353_968,(0,0,4):C.R2GC_353_969,(0,0,5):C.R2GC_353_970,(0,1,0):C.R2GC_355_977,(0,1,2):C.R2GC_355_978,(0,1,3):C.R2GC_355_979})

V_228 = CTVertex(name = 'V_228',
                 type = 'R2',
                 particles = [ P.d__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_342_922,(0,0,1):C.R2GC_342_923,(0,0,2):C.R2GC_342_924,(0,0,3):C.R2GC_342_925,(0,0,4):C.R2GC_342_926,(0,0,5):C.R2GC_342_927,(0,1,0):C.R2GC_344_931,(0,1,2):C.R2GC_344_932,(0,1,3):C.R2GC_344_933})

V_229 = CTVertex(name = 'V_229',
                 type = 'R2',
                 particles = [ P.s__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.c, P.G__plus__] ], [ [P.c, P.W__plus__] ], [ [P.G__plus__, P.t] ], [ [P.G__plus__, P.u] ], [ [P.t, P.W__plus__] ], [ [P.u, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_354_971,(0,0,1):C.R2GC_354_972,(0,0,2):C.R2GC_354_973,(0,0,3):C.R2GC_354_974,(0,0,4):C.R2GC_354_975,(0,0,5):C.R2GC_354_976,(0,1,0):C.R2GC_356_980,(0,1,2):C.R2GC_356_981,(0,1,3):C.R2GC_356_982})

V_230 = CTVertex(name = 'V_230',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.u, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_369_1027,(0,0,1):C.R2GC_369_1028,(0,0,2):C.R2GC_369_1029,(0,0,3):C.R2GC_369_1030,(0,0,4):C.R2GC_369_1031,(0,0,5):C.R2GC_369_1032,(0,1,0):C.R2GC_371_1039,(0,1,2):C.R2GC_371_1040,(0,1,4):C.R2GC_371_1041})

V_231 = CTVertex(name = 'V_231',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.u, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_373_1045,(0,0,1):C.R2GC_373_1046,(0,0,2):C.R2GC_373_1047,(0,0,3):C.R2GC_373_1048,(0,0,4):C.R2GC_373_1049,(0,0,5):C.R2GC_373_1050,(0,1,0):C.R2GC_375_1057,(0,1,2):C.R2GC_375_1058,(0,1,4):C.R2GC_375_1059})

V_232 = CTVertex(name = 'V_232',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.c, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_370_1033,(0,0,1):C.R2GC_370_1034,(0,0,2):C.R2GC_370_1035,(0,0,3):C.R2GC_370_1036,(0,0,4):C.R2GC_370_1037,(0,0,5):C.R2GC_370_1038,(0,1,0):C.R2GC_372_1042,(0,1,2):C.R2GC_372_1043,(0,1,4):C.R2GC_372_1044})

V_233 = CTVertex(name = 'V_233',
                 type = 'R2',
                 particles = [ P.t__tilde__, P.c, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_364_1014,(0,0,1):C.R2GC_364_1015,(0,0,2):C.R2GC_364_1016,(0,0,3):C.R2GC_364_1017,(0,0,4):C.R2GC_364_1018,(0,0,5):C.R2GC_364_1019,(0,1,0):C.R2GC_366_1023,(0,1,2):C.R2GC_366_1024,(0,1,4):C.R2GC_366_1025})

V_234 = CTVertex(name = 'V_234',
                 type = 'R2',
                 particles = [ P.u__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_374_1051,(0,0,1):C.R2GC_374_1052,(0,0,2):C.R2GC_374_1053,(0,0,3):C.R2GC_374_1054,(0,0,4):C.R2GC_374_1055,(0,0,5):C.R2GC_374_1056,(0,1,0):C.R2GC_376_1060,(0,1,2):C.R2GC_376_1061,(0,1,4):C.R2GC_376_1062})

V_235 = CTVertex(name = 'V_235',
                 type = 'R2',
                 particles = [ P.c__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [P.b, P.G__plus__] ], [ [P.b, P.W__plus__] ], [ [P.d, P.G__plus__] ], [ [P.d, P.W__plus__] ], [ [P.G__plus__, P.s] ], [ [P.s, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_363_1008,(0,0,1):C.R2GC_363_1009,(0,0,2):C.R2GC_363_1010,(0,0,3):C.R2GC_363_1011,(0,0,4):C.R2GC_363_1012,(0,0,5):C.R2GC_363_1013,(0,1,0):C.R2GC_365_1020,(0,1,2):C.R2GC_365_1021,(0,1,4):C.R2GC_365_1022})

V_236 = CTVertex(name = 'V_236',
                 type = 'R2',
                 particles = [ P.a, P.a, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_205_349,(0,0,1):C.R2GC_205_350,(0,0,2):C.R2GC_205_351,(0,0,3):C.R2GC_205_352,(0,0,5):C.R2GC_205_353,(0,0,6):C.R2GC_205_354,(0,0,7):C.R2GC_205_355,(0,0,8):C.R2GC_205_356,(0,0,9):C.R2GC_205_357,(0,0,10):C.R2GC_205_358,(0,0,4):C.R2GC_205_359})

V_237 = CTVertex(name = 'V_237',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_569_2406,(0,0,1):C.R2GC_569_2407,(0,0,2):C.R2GC_569_2408,(0,0,3):C.R2GC_569_2409,(0,0,5):C.R2GC_569_2410,(0,0,6):C.R2GC_569_2411,(0,0,7):C.R2GC_569_2412,(0,0,8):C.R2GC_569_2413,(0,0,9):C.R2GC_569_2414,(0,0,10):C.R2GC_569_2415,(0,0,4):C.R2GC_569_2416})

V_238 = CTVertex(name = 'V_238',
                 type = 'R2',
                 particles = [ P.g, P.g, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_175_86,(0,0,1):C.R2GC_175_87,(0,0,2):C.R2GC_175_88,(0,0,3):C.R2GC_175_89,(0,0,4):C.R2GC_175_90,(0,0,5):C.R2GC_175_91})

V_239 = CTVertex(name = 'V_239',
                 type = 'R2',
                 particles = [ P.a, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [P.G__plus__, P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_497_1884})

V_240 = CTVertex(name = 'V_240',
                 type = 'R2',
                 particles = [ P.a, P.a, P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_176_92,(0,0,1):C.R2GC_176_93,(0,0,2):C.R2GC_176_94,(0,0,3):C.R2GC_176_95,(0,0,4):C.R2GC_176_96,(0,0,5):C.R2GC_176_97,(0,0,6):C.R2GC_176_98,(0,0,7):C.R2GC_176_99,(0,0,8):C.R2GC_176_100,(0,0,9):C.R2GC_176_101,(0,1,0):C.R2GC_183_171,(0,1,1):C.R2GC_183_172,(0,1,2):C.R2GC_183_173,(0,1,3):C.R2GC_183_174,(0,1,4):C.R2GC_183_175,(0,1,5):C.R2GC_183_176,(0,1,6):C.R2GC_183_177,(0,1,7):C.R2GC_183_178,(0,1,8):C.R2GC_183_179,(0,1,9):C.R2GC_183_180,(0,2,0):C.R2GC_184_181,(0,2,1):C.R2GC_184_182,(0,2,2):C.R2GC_184_183,(0,2,3):C.R2GC_184_184,(0,2,4):C.R2GC_184_185,(0,2,5):C.R2GC_184_186,(0,2,6):C.R2GC_184_187,(0,2,7):C.R2GC_184_188,(0,2,8):C.R2GC_184_189,(0,2,9):C.R2GC_184_190})

V_241 = CTVertex(name = 'V_241',
                 type = 'R2',
                 particles = [ P.a, P.a, P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_185_191,(0,0,1):C.R2GC_185_192,(0,0,2):C.R2GC_185_193,(0,0,3):C.R2GC_185_194,(0,0,4):C.R2GC_185_195,(0,0,5):C.R2GC_185_196,(0,0,6):C.R2GC_185_197,(0,0,7):C.R2GC_185_198,(0,0,8):C.R2GC_185_199,(0,0,9):C.R2GC_185_200,(0,1,0):C.R2GC_186_201,(0,1,1):C.R2GC_186_202,(0,1,2):C.R2GC_186_203,(0,1,3):C.R2GC_186_204,(0,1,4):C.R2GC_186_205,(0,1,5):C.R2GC_186_206,(0,1,6):C.R2GC_186_207,(0,1,7):C.R2GC_186_208,(0,1,8):C.R2GC_186_209,(0,1,9):C.R2GC_186_210,(0,2,0):C.R2GC_187_211,(0,2,1):C.R2GC_187_212,(0,2,2):C.R2GC_187_213,(0,2,3):C.R2GC_187_214,(0,2,4):C.R2GC_187_215,(0,2,5):C.R2GC_187_216,(0,2,6):C.R2GC_187_217,(0,2,7):C.R2GC_187_218,(0,2,8):C.R2GC_187_219,(0,2,9):C.R2GC_187_220})

V_242 = CTVertex(name = 'V_242',
                 type = 'R2',
                 particles = [ P.a, P.a, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_188_221,(0,0,1):C.R2GC_188_222,(0,0,2):C.R2GC_188_223,(0,0,3):C.R2GC_188_224,(0,0,4):C.R2GC_188_225,(0,0,5):C.R2GC_188_226,(0,0,6):C.R2GC_188_227,(0,0,7):C.R2GC_188_228,(0,0,8):C.R2GC_188_229,(0,0,9):C.R2GC_188_230,(0,1,0):C.R2GC_189_231,(0,1,1):C.R2GC_189_232,(0,1,2):C.R2GC_189_233,(0,1,3):C.R2GC_189_234,(0,1,4):C.R2GC_189_235,(0,1,5):C.R2GC_189_236,(0,1,6):C.R2GC_189_237,(0,1,7):C.R2GC_189_238,(0,1,8):C.R2GC_189_239,(0,1,9):C.R2GC_189_240,(0,2,0):C.R2GC_190_241,(0,2,1):C.R2GC_190_242,(0,2,2):C.R2GC_190_243,(0,2,3):C.R2GC_190_244,(0,2,4):C.R2GC_190_245,(0,2,5):C.R2GC_190_246,(0,2,6):C.R2GC_190_247,(0,2,7):C.R2GC_190_248,(0,2,8):C.R2GC_190_249,(0,2,9):C.R2GC_190_250})

V_243 = CTVertex(name = 'V_243',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_177_102,(0,0,1):C.R2GC_177_103,(0,0,2):C.R2GC_177_104,(0,0,3):C.R2GC_177_105,(0,0,4):C.R2GC_177_106,(0,0,5):C.R2GC_177_107,(0,0,6):C.R2GC_177_108,(0,0,7):C.R2GC_177_109,(0,0,8):C.R2GC_177_110,(0,0,9):C.R2GC_177_111,(0,1,0):C.R2GC_178_112,(0,1,1):C.R2GC_178_113,(0,1,2):C.R2GC_178_114,(0,1,3):C.R2GC_178_115,(0,1,4):C.R2GC_178_116,(0,1,5):C.R2GC_178_117,(0,1,6):C.R2GC_178_118,(0,1,7):C.R2GC_178_119,(0,1,8):C.R2GC_178_120,(0,1,9):C.R2GC_178_121,(0,2,0):C.R2GC_179_122,(0,2,1):C.R2GC_179_123,(0,2,2):C.R2GC_179_124,(0,2,3):C.R2GC_179_125,(0,2,4):C.R2GC_179_126,(0,2,5):C.R2GC_179_127,(0,2,6):C.R2GC_179_128,(0,2,7):C.R2GC_179_129,(0,2,8):C.R2GC_179_130,(0,2,9):C.R2GC_179_131})

V_244 = CTVertex(name = 'V_244',
                 type = 'R2',
                 particles = [ P.Z, P.Z, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.ve] ], [ [P.vm] ], [ [P.vt] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_180_132,(0,0,1):C.R2GC_180_133,(0,0,2):C.R2GC_180_134,(0,0,3):C.R2GC_180_135,(0,0,4):C.R2GC_180_136,(0,0,5):C.R2GC_180_137,(0,0,6):C.R2GC_180_138,(0,0,7):C.R2GC_180_139,(0,0,8):C.R2GC_180_140,(0,0,9):C.R2GC_180_141,(0,0,10):C.R2GC_180_142,(0,0,11):C.R2GC_180_143,(0,0,12):C.R2GC_180_144,(0,1,0):C.R2GC_181_145,(0,1,1):C.R2GC_181_146,(0,1,2):C.R2GC_181_147,(0,1,3):C.R2GC_181_148,(0,1,4):C.R2GC_181_149,(0,1,5):C.R2GC_181_150,(0,1,6):C.R2GC_181_151,(0,1,7):C.R2GC_181_152,(0,1,8):C.R2GC_181_153,(0,1,9):C.R2GC_181_154,(0,1,10):C.R2GC_181_155,(0,1,11):C.R2GC_181_156,(0,1,12):C.R2GC_181_157,(0,2,0):C.R2GC_182_158,(0,2,1):C.R2GC_182_159,(0,2,2):C.R2GC_182_160,(0,2,3):C.R2GC_182_161,(0,2,4):C.R2GC_182_162,(0,2,5):C.R2GC_182_163,(0,2,6):C.R2GC_182_164,(0,2,7):C.R2GC_182_165,(0,2,8):C.R2GC_182_166,(0,2,9):C.R2GC_182_167,(0,2,10):C.R2GC_182_168,(0,2,11):C.R2GC_182_169,(0,2,12):C.R2GC_182_170})

V_245 = CTVertex(name = 'V_245',
                 type = 'R2',
                 particles = [ P.a, P.a, P.g, P.g ],
                 color = [ 'Identity(3,4)' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_162_12,(0,0,1):C.R2GC_162_13,(0,0,2):C.R2GC_162_14,(0,0,3):C.R2GC_162_15,(0,0,4):C.R2GC_162_16,(0,0,5):C.R2GC_162_17,(0,1,0):C.R2GC_163_18,(0,1,1):C.R2GC_163_19,(0,1,2):C.R2GC_163_20,(0,1,3):C.R2GC_163_21,(0,1,4):C.R2GC_163_22,(0,1,5):C.R2GC_163_23,(0,2,0):C.R2GC_164_24,(0,2,1):C.R2GC_164_25,(0,2,2):C.R2GC_164_26,(0,2,3):C.R2GC_164_27,(0,2,4):C.R2GC_164_28,(0,2,5):C.R2GC_164_29})

V_246 = CTVertex(name = 'V_246',
                 type = 'R2',
                 particles = [ P.g, P.g, P.W__minus__, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.s, P.t] ], [ [P.s, P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_199_288,(0,0,1):C.R2GC_199_289,(0,0,2):C.R2GC_199_290,(0,0,3):C.R2GC_199_291,(0,0,4):C.R2GC_199_292,(0,0,5):C.R2GC_199_293,(0,0,6):C.R2GC_199_294,(0,0,7):C.R2GC_199_295,(0,0,8):C.R2GC_199_296,(0,1,0):C.R2GC_198_279,(0,1,1):C.R2GC_198_280,(0,1,2):C.R2GC_198_281,(0,1,3):C.R2GC_198_282,(0,1,4):C.R2GC_198_283,(0,1,5):C.R2GC_198_284,(0,1,6):C.R2GC_198_285,(0,1,7):C.R2GC_198_286,(0,1,8):C.R2GC_198_287,(0,2,0):C.R2GC_200_297,(0,2,1):C.R2GC_200_298,(0,2,2):C.R2GC_200_299,(0,2,3):C.R2GC_200_300,(0,2,4):C.R2GC_200_301,(0,2,5):C.R2GC_200_302,(0,2,6):C.R2GC_200_303,(0,2,7):C.R2GC_200_304,(0,2,8):C.R2GC_200_305})

V_247 = CTVertex(name = 'V_247',
                 type = 'R2',
                 particles = [ P.a, P.g, P.g, P.Z ],
                 color = [ 'Identity(2,3)' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_167_42,(0,0,1):C.R2GC_167_43,(0,0,2):C.R2GC_167_44,(0,0,3):C.R2GC_167_45,(0,0,4):C.R2GC_167_46,(0,0,5):C.R2GC_167_47,(0,1,0):C.R2GC_165_30,(0,1,1):C.R2GC_165_31,(0,1,2):C.R2GC_165_32,(0,1,3):C.R2GC_165_33,(0,1,4):C.R2GC_165_34,(0,1,5):C.R2GC_165_35,(0,2,0):C.R2GC_166_36,(0,2,1):C.R2GC_166_37,(0,2,2):C.R2GC_166_38,(0,2,3):C.R2GC_166_39,(0,2,4):C.R2GC_166_40,(0,2,5):C.R2GC_166_41})

V_248 = CTVertex(name = 'V_248',
                 type = 'R2',
                 particles = [ P.g, P.g, P.Z, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_168_48,(0,0,1):C.R2GC_168_49,(0,0,2):C.R2GC_168_50,(0,0,3):C.R2GC_168_51,(0,0,4):C.R2GC_168_52,(0,0,5):C.R2GC_168_53,(0,1,0):C.R2GC_169_54,(0,1,1):C.R2GC_169_55,(0,1,2):C.R2GC_169_56,(0,1,3):C.R2GC_169_57,(0,1,4):C.R2GC_169_58,(0,1,5):C.R2GC_169_59,(0,2,0):C.R2GC_170_60,(0,2,1):C.R2GC_170_61,(0,2,2):C.R2GC_170_62,(0,2,3):C.R2GC_170_63,(0,2,4):C.R2GC_170_64,(0,2,5):C.R2GC_170_65})

V_249 = CTVertex(name = 'V_249',
                 type = 'R2',
                 particles = [ P.a, P.a, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_203_327,(0,0,1):C.R2GC_203_328,(0,0,2):C.R2GC_203_329,(0,0,3):C.R2GC_203_330,(0,0,5):C.R2GC_203_331,(0,0,6):C.R2GC_203_332,(0,0,7):C.R2GC_203_333,(0,0,8):C.R2GC_203_334,(0,0,9):C.R2GC_203_335,(0,0,10):C.R2GC_203_336,(0,0,4):C.R2GC_203_337})

V_250 = CTVertex(name = 'V_250',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_550_2145,(0,0,1):C.R2GC_550_2146,(0,0,2):C.R2GC_550_2147,(0,0,3):C.R2GC_550_2148,(0,0,5):C.R2GC_550_2149,(0,0,6):C.R2GC_550_2150,(0,0,7):C.R2GC_550_2151,(0,0,8):C.R2GC_550_2152,(0,0,9):C.R2GC_550_2153,(0,0,10):C.R2GC_550_2154,(0,0,4):C.R2GC_550_2155})

V_251 = CTVertex(name = 'V_251',
                 type = 'R2',
                 particles = [ P.g, P.g, P.H, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_171_66,(0,0,1):C.R2GC_171_67,(0,0,2):C.R2GC_171_68,(0,0,3):C.R2GC_171_69,(0,0,4):C.R2GC_171_70,(0,0,5):C.R2GC_171_71})

V_252 = CTVertex(name = 'V_252',
                 type = 'R2',
                 particles = [ P.a, P.a, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_204_338,(0,0,1):C.R2GC_204_339,(0,0,2):C.R2GC_204_340,(0,0,3):C.R2GC_204_341,(0,0,5):C.R2GC_204_342,(0,0,6):C.R2GC_204_343,(0,0,7):C.R2GC_204_344,(0,0,8):C.R2GC_204_345,(0,0,9):C.R2GC_204_346,(0,0,10):C.R2GC_204_347,(0,0,4):C.R2GC_204_348})

V_253 = CTVertex(name = 'V_253',
                 type = 'R2',
                 particles = [ P.a, P.Z, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.e__minus__] ], [ [P.G__plus__, P.W__plus__] ], [ [P.mu__minus__] ], [ [P.s] ], [ [P.t] ], [ [P.ta__minus__] ], [ [P.u] ], [ [P.W__plus__] ] ],
                 couplings = {(0,0,0):C.R2GC_551_2156,(0,0,1):C.R2GC_551_2157,(0,0,2):C.R2GC_551_2158,(0,0,3):C.R2GC_551_2159,(0,0,5):C.R2GC_551_2160,(0,0,6):C.R2GC_551_2161,(0,0,7):C.R2GC_551_2162,(0,0,8):C.R2GC_551_2163,(0,0,9):C.R2GC_551_2164,(0,0,10):C.R2GC_551_2165,(0,0,4):C.R2GC_551_2166})

V_254 = CTVertex(name = 'V_254',
                 type = 'R2',
                 particles = [ P.g, P.g, P.G0, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_172_72,(0,0,1):C.R2GC_172_73,(0,0,2):C.R2GC_172_74,(0,0,3):C.R2GC_172_75,(0,0,4):C.R2GC_172_76,(0,0,5):C.R2GC_172_77})

V_255 = CTVertex(name = 'V_255',
                 type = 'R2',
                 particles = [ P.W__minus__, P.W__minus__, P.G__plus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.a, P.G0, P.G__plus__] ], [ [P.a, P.G0, P.W__plus__] ], [ [P.a, P.G__plus__, P.H] ], [ [P.a, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,5):C.R2GC_244_604,(0,0,8):C.R2GC_244_605,(0,0,0):C.R2GC_244_606,(0,0,1):C.R2GC_244_607,(0,0,2):C.R2GC_244_608,(0,0,3):C.R2GC_244_609,(0,0,4):C.R2GC_244_610,(0,0,6):C.R2GC_244_611,(0,0,7):C.R2GC_244_612,(0,0,9):C.R2GC_244_613})

V_256 = CTVertex(name = 'V_256',
                 type = 'R2',
                 particles = [ P.g, P.g, P.G__minus__, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.b, P.c] ], [ [P.b, P.t] ], [ [P.b, P.u] ], [ [P.c, P.d] ], [ [P.c, P.s] ], [ [P.d, P.t] ], [ [P.d, P.u] ], [ [P.s, P.t] ], [ [P.s, P.u] ] ],
                 couplings = {(0,0,0):C.R2GC_201_306,(0,0,1):C.R2GC_201_307,(0,0,2):C.R2GC_201_308,(0,0,3):C.R2GC_201_309,(0,0,4):C.R2GC_201_310,(0,0,5):C.R2GC_201_311,(0,0,6):C.R2GC_201_312,(0,0,7):C.R2GC_201_313,(0,0,8):C.R2GC_201_314})

V_257 = CTVertex(name = 'V_257',
                 type = 'R2',
                 particles = [ P.W__plus__, P.W__plus__, P.G__minus__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [P.a, P.G0, P.G__plus__] ], [ [P.a, P.G0, P.W__plus__] ], [ [P.a, P.G__plus__, P.H] ], [ [P.a, P.H, P.W__plus__] ], [ [P.G0, P.G__plus__, P.Z] ], [ [P.G0, P.W__plus__] ], [ [P.G0, P.W__plus__, P.Z] ], [ [P.G__plus__, P.H, P.Z] ], [ [P.H, P.W__plus__] ], [ [P.H, P.W__plus__, P.Z] ] ],
                 couplings = {(0,0,5):C.R2GC_245_614,(0,0,8):C.R2GC_245_615,(0,0,0):C.R2GC_245_616,(0,0,1):C.R2GC_245_617,(0,0,2):C.R2GC_245_618,(0,0,3):C.R2GC_245_619,(0,0,4):C.R2GC_245_620,(0,0,6):C.R2GC_245_621,(0,0,7):C.R2GC_245_622,(0,0,9):C.R2GC_245_623})

V_258 = CTVertex(name = 'V_258',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_420_171})

V_259 = CTVertex(name = 'V_259',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_416_168})

V_260 = CTVertex(name = 'V_260',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__minus__, P.G__plus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_419_170})

V_261 = CTVertex(name = 'V_261',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_417_169})

V_262 = CTVertex(name = 'V_262',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__plus__, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_417_169})

V_263 = CTVertex(name = 'V_263',
                 type = 'UV',
                 particles = [ P.H, P.H, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_421_172})

V_264 = CTVertex(name = 'V_264',
                 type = 'UV',
                 particles = [ P.G0, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_559_300})

V_265 = CTVertex(name = 'V_265',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_559_300})

V_266 = CTVertex(name = 'V_266',
                 type = 'UV',
                 particles = [ P.H, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_561_301})

V_267 = CTVertex(name = 'V_267',
                 type = 'UV',
                 particles = [ P.a, P.a, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_520_263})

V_268 = CTVertex(name = 'V_268',
                 type = 'UV',
                 particles = [ P.a, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_507_252})

V_269 = CTVertex(name = 'V_269',
                 type = 'UV',
                 particles = [ P.ghA, P.ghWm__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_336_88})

V_270 = CTVertex(name = 'V_270',
                 type = 'UV',
                 particles = [ P.ghA, P.ghWp__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_337_89})

V_271 = CTVertex(name = 'V_271',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghA__tilde__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_414_166})

V_272 = CTVertex(name = 'V_272',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghA__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_336_88})

V_273 = CTVertex(name = 'V_273',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_468_213})

V_274 = CTVertex(name = 'V_274',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_469_214})

V_275 = CTVertex(name = 'V_275',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_432_181})

V_276 = CTVertex(name = 'V_276',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_460_206})

V_277 = CTVertex(name = 'V_277',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghZ__tilde__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_548_291})

V_278 = CTVertex(name = 'V_278',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghZ__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_462_208})

V_279 = CTVertex(name = 'V_279',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghA__tilde__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_413_165})

V_280 = CTVertex(name = 'V_280',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghA__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_337_89})

V_281 = CTVertex(name = 'V_281',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_467_212})

V_282 = CTVertex(name = 'V_282',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_469_214})

V_283 = CTVertex(name = 'V_283',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_431_180})

V_284 = CTVertex(name = 'V_284',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_463_209})

V_285 = CTVertex(name = 'V_285',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghZ__tilde__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_547_290})

V_286 = CTVertex(name = 'V_286',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghZ__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_459_205})

V_287 = CTVertex(name = 'V_287',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWm__tilde__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_471_216})

V_288 = CTVertex(name = 'V_288',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWm__tilde__, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_462_208})

V_289 = CTVertex(name = 'V_289',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWp__tilde__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_470_215})

V_290 = CTVertex(name = 'V_290',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghWp__tilde__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_459_205})

V_291 = CTVertex(name = 'V_291',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghZ__tilde__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.UUS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_549_292})

V_292 = CTVertex(name = 'V_292',
                 type = 'UV',
                 particles = [ P.ghG, P.ghG__tilde__, P.g ],
                 color = [ 'f(1,2,3)' ],
                 lorentz = [ L.UUV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_346_98})

V_293 = CTVertex(name = 'V_293',
                 type = 'UV',
                 particles = [ P.g, P.g, P.g ],
                 color = [ 'f(1,2,3)' ],
                 lorentz = [ L.VVV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_345_97})

V_294 = CTVertex(name = 'V_294',
                 type = 'UV',
                 particles = [ P.g, P.g, P.g, P.g ],
                 color = [ 'f(-1,1,2)*f(3,4,-1)', 'f(-1,1,3)*f(2,4,-1)', 'f(-1,1,4)*f(2,3,-1)' ],
                 lorentz = [ L.VVVV4, L.VVVV7, L.VVVV8 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(1,1,0):C.UVGC_379_131,(0,0,0):C.UVGC_379_131,(2,2,0):C.UVGC_379_131})

V_295 = CTVertex(name = 'V_295',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.G0, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_456_203})

V_296 = CTVertex(name = 'V_296',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_458_204})

V_297 = CTVertex(name = 'V_297',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_564_304})

V_298 = CTVertex(name = 'V_298',
                 type = 'UV',
                 particles = [ P.W__minus__, P.G0, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_439_187})

V_299 = CTVertex(name = 'V_299',
                 type = 'UV',
                 particles = [ P.W__minus__, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_441_189})

V_300 = CTVertex(name = 'V_300',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_433_182})

V_301 = CTVertex(name = 'V_301',
                 type = 'UV',
                 particles = [ P.a, P.W__plus__, P.G0, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_456_203})

V_302 = CTVertex(name = 'V_302',
                 type = 'UV',
                 particles = [ P.a, P.W__plus__, P.G__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_455_202})

V_303 = CTVertex(name = 'V_303',
                 type = 'UV',
                 particles = [ P.a, P.W__plus__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_565_305})

V_304 = CTVertex(name = 'V_304',
                 type = 'UV',
                 particles = [ P.W__plus__, P.G0, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_440_188})

V_305 = CTVertex(name = 'V_305',
                 type = 'UV',
                 particles = [ P.W__plus__, P.G__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_441_189})

V_306 = CTVertex(name = 'V_306',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_422_173})

V_307 = CTVertex(name = 'V_307',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_422_173})

V_308 = CTVertex(name = 'V_308',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_424_174})

V_309 = CTVertex(name = 'V_309',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_563_303})

V_310 = CTVertex(name = 'V_310',
                 type = 'UV',
                 particles = [ P.a, P.a, P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_434_183})

V_311 = CTVertex(name = 'V_311',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVV1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_461_207})

V_312 = CTVertex(name = 'V_312',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__minus__, P.W__plus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_425_175})

V_313 = CTVertex(name = 'V_313',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.d, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_668_404,(0,1,0):C.UVGC_670_406})

V_314 = CTVertex(name = 'V_314',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.d, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_667_403,(0,1,0):C.UVGC_669_405})

V_315 = CTVertex(name = 'V_315',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.d, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_682_418,(0,1,0):C.UVGC_687_423})

V_316 = CTVertex(name = 'V_316',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.s, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_674_410,(0,1,0):C.UVGC_676_412})

V_317 = CTVertex(name = 'V_317',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.s, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_673_409,(0,1,0):C.UVGC_675_411})

V_318 = CTVertex(name = 'V_318',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.s, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_683_419,(0,1,0):C.UVGC_688_424})

V_319 = CTVertex(name = 'V_319',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.b, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_685_421,(0,1,0):C.UVGC_690_426})

V_320 = CTVertex(name = 'V_320',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.b, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_684_420,(0,1,0):C.UVGC_689_425})

V_321 = CTVertex(name = 'V_321',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.b, P.G__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_686_422,(0,1,0):C.UVGC_691_427})

V_322 = CTVertex(name = 'V_322',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_586_324})

V_323 = CTVertex(name = 'V_323',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_619_356})

V_324 = CTVertex(name = 'V_324',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_572_312})

V_325 = CTVertex(name = 'V_325',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_584_323,(0,1,0):C.UVGC_584_323})

V_326 = CTVertex(name = 'V_326',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_617_355,(0,1,0):C.UVGC_617_355})

V_327 = CTVertex(name = 'V_327',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_571_311,(0,1,0):C.UVGC_571_311})

V_328 = CTVertex(name = 'V_328',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.u, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_662_398,(0,1,0):C.UVGC_614_352})

V_329 = CTVertex(name = 'V_329',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.u, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_663_399,(0,1,0):C.UVGC_620_357})

V_330 = CTVertex(name = 'V_330',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.u, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_664_400,(0,1,0):C.UVGC_611_349})

V_331 = CTVertex(name = 'V_331',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.c, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_654_390,(0,1,0):C.UVGC_615_353})

V_332 = CTVertex(name = 'V_332',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.c, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_655_391,(0,1,0):C.UVGC_621_358})

V_333 = CTVertex(name = 'V_333',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.c, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_656_392,(0,1,0):C.UVGC_612_350})

V_334 = CTVertex(name = 'V_334',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.t, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_657_393,(0,1,0):C.UVGC_616_354})

V_335 = CTVertex(name = 'V_335',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.t, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_658_394,(0,1,0):C.UVGC_622_359})

V_336 = CTVertex(name = 'V_336',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.t, P.G__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_659_395,(0,1,0):C.UVGC_613_351})

V_337 = CTVertex(name = 'V_337',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.e__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_588_326})

V_338 = CTVertex(name = 'V_338',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.mu__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_592_330})

V_339 = CTVertex(name = 'V_339',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.ta__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_635_371})

V_340 = CTVertex(name = 'V_340',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_590_328})

V_341 = CTVertex(name = 'V_341',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_594_332})

V_342 = CTVertex(name = 'V_342',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_637_373})

V_343 = CTVertex(name = 'V_343',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_589_327,(0,1,0):C.UVGC_589_327})

V_344 = CTVertex(name = 'V_344',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_593_331,(0,1,0):C.UVGC_593_331})

V_345 = CTVertex(name = 'V_345',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_636_372,(0,1,0):C.UVGC_636_372})

V_346 = CTVertex(name = 'V_346',
                 type = 'UV',
                 particles = [ P.e__plus__, P.ve, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_587_325})

V_347 = CTVertex(name = 'V_347',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.vm, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_591_329})

V_348 = CTVertex(name = 'V_348',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.vt, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_634_370})

V_349 = CTVertex(name = 'V_349',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_660_396})

V_350 = CTVertex(name = 'V_350',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_573_313})

V_351 = CTVertex(name = 'V_351',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_631_368})

V_352 = CTVertex(name = 'V_352',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_661_397,(0,1,0):C.UVGC_661_397})

V_353 = CTVertex(name = 'V_353',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_574_314,(0,1,0):C.UVGC_574_314})

V_354 = CTVertex(name = 'V_354',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_632_369,(0,1,0):C.UVGC_632_369})

V_355 = CTVertex(name = 'V_355',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_552_294})

V_356 = CTVertex(name = 'V_356',
                 type = 'UV',
                 particles = [ P.Z, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS1, L.VSS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_522_265,(0,1,0):C.UVGC_546_289})

V_357 = CTVertex(name = 'V_357',
                 type = 'UV',
                 particles = [ P.Z, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VSS1, L.VSS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_533_276,(0,1,0):C.UVGC_532_275})

V_358 = CTVertex(name = 'V_358',
                 type = 'UV',
                 particles = [ P.W__minus__, P.Z, P.G0, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_428_178})

V_359 = CTVertex(name = 'V_359',
                 type = 'UV',
                 particles = [ P.W__minus__, P.Z, P.G__plus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_427_177})

V_360 = CTVertex(name = 'V_360',
                 type = 'UV',
                 particles = [ P.W__minus__, P.Z, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_567_307})

V_361 = CTVertex(name = 'V_361',
                 type = 'UV',
                 particles = [ P.W__plus__, P.Z, P.G0, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_428_178})

V_362 = CTVertex(name = 'V_362',
                 type = 'UV',
                 particles = [ P.W__plus__, P.Z, P.G__minus__, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_430_179})

V_363 = CTVertex(name = 'V_363',
                 type = 'UV',
                 particles = [ P.W__plus__, P.Z, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_566_306})

V_364 = CTVertex(name = 'V_364',
                 type = 'UV',
                 particles = [ P.a, P.W__minus__, P.W__plus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_466_211,(0,1,0):C.UVGC_464_210,(0,2,0):C.UVGC_464_210})

V_365 = CTVertex(name = 'V_365',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_553_295})

V_366 = CTVertex(name = 'V_366',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_554_296})

V_367 = CTVertex(name = 'V_367',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_555_297})

V_368 = CTVertex(name = 'V_368',
                 type = 'UV',
                 particles = [ P.Z, P.Z, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_570_310})

V_369 = CTVertex(name = 'V_369',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__, P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VVVV2, L.VVVV3, L.VVVV5 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_436_185,(0,1,0):C.UVGC_436_185,(0,2,0):C.UVGC_438_186})

V_370 = CTVertex(name = 'V_370',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_508_253,(0,1,0):C.UVGC_517_260})

V_371 = CTVertex(name = 'V_371',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_509_254,(0,1,0):C.UVGC_518_261})

V_372 = CTVertex(name = 'V_372',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_510_255,(0,1,0):C.UVGC_519_262})

V_373 = CTVertex(name = 'V_373',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_503_248,(0,1,0):C.UVGC_516_259})

V_374 = CTVertex(name = 'V_374',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_501_246,(0,1,0):C.UVGC_514_257})

V_375 = CTVertex(name = 'V_375',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_502_247,(0,1,0):C.UVGC_515_258})

V_376 = CTVertex(name = 'V_376',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_499_244,(0,1,0):C.UVGC_505_250})

V_377 = CTVertex(name = 'V_377',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_500_245,(0,1,0):C.UVGC_506_251})

V_378 = CTVertex(name = 'V_378',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_498_243,(0,1,0):C.UVGC_504_249})

V_379 = CTVertex(name = 'V_379',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_377_129,(0,1,0):C.UVGC_378_130})

V_380 = CTVertex(name = 'V_380',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_349_101,(0,1,0):C.UVGC_350_102})

V_381 = CTVertex(name = 'V_381',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_367_119,(0,1,0):C.UVGC_368_120})

V_382 = CTVertex(name = 'V_382',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_351_103,(0,1,0):C.UVGC_352_104})

V_383 = CTVertex(name = 'V_383',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_361_113,(0,1,0):C.UVGC_362_114})

V_384 = CTVertex(name = 'V_384',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_347_99,(0,1,0):C.UVGC_348_100})

V_385 = CTVertex(name = 'V_385',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_446_193})

V_386 = CTVertex(name = 'V_386',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.u, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_447_194})

V_387 = CTVertex(name = 'V_387',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.u, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_448_195})

V_388 = CTVertex(name = 'V_388',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.c, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_449_196})

V_389 = CTVertex(name = 'V_389',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_450_197})

V_390 = CTVertex(name = 'V_390',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.c, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_451_198})

V_391 = CTVertex(name = 'V_391',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.t, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_452_199})

V_392 = CTVertex(name = 'V_392',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.t, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_453_200})

V_393 = CTVertex(name = 'V_393',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_454_201})

V_394 = CTVertex(name = 'V_394',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_666_402})

V_395 = CTVertex(name = 'V_395',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.d, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_665_401})

V_396 = CTVertex(name = 'V_396',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.d, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_677_413})

V_397 = CTVertex(name = 'V_397',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.s, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_672_408})

V_398 = CTVertex(name = 'V_398',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_671_407})

V_399 = CTVertex(name = 'V_399',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.s, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_678_414})

V_400 = CTVertex(name = 'V_400',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.b, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_680_416})

V_401 = CTVertex(name = 'V_401',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.b, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_679_415})

V_402 = CTVertex(name = 'V_402',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_681_417})

V_403 = CTVertex(name = 'V_403',
                 type = 'UV',
                 particles = [ P.e__plus__, P.ve, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_443_190})

V_404 = CTVertex(name = 'V_404',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.vm, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_444_191})

V_405 = CTVertex(name = 'V_405',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.vt, P.W__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_445_192})

V_406 = CTVertex(name = 'V_406',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.e__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_443_190})

V_407 = CTVertex(name = 'V_407',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.mu__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_444_191})

V_408 = CTVertex(name = 'V_408',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.ta__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_445_192})

V_409 = CTVertex(name = 'V_409',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_528_271,(0,1,0):C.UVGC_542_285})

V_410 = CTVertex(name = 'V_410',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_524_267,(0,1,0):C.UVGC_540_283})

V_411 = CTVertex(name = 'V_411',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_527_270,(0,1,0):C.UVGC_541_284})

V_412 = CTVertex(name = 'V_412',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_525_268,(0,1,0):C.UVGC_530_273})

V_413 = CTVertex(name = 'V_413',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_526_269,(0,1,0):C.UVGC_531_274})

V_414 = CTVertex(name = 'V_414',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_523_266,(0,1,0):C.UVGC_529_272})

V_415 = CTVertex(name = 'V_415',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.ve, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_537_280})

V_416 = CTVertex(name = 'V_416',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.vm, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_538_281})

V_417 = CTVertex(name = 'V_417',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.vt, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_539_282})

V_418 = CTVertex(name = 'V_418',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_534_277,(0,1,0):C.UVGC_543_286})

V_419 = CTVertex(name = 'V_419',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_535_278,(0,1,0):C.UVGC_544_287})

V_420 = CTVertex(name = 'V_420',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_536_279,(0,1,0):C.UVGC_545_288})

V_421 = CTVertex(name = 'V_421',
                 type = 'UV',
                 particles = [ P.e__plus__, P.e__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_387_139,(0,3,0):C.UVGC_387_139,(0,2,0):C.UVGC_279_31,(0,4,0):C.UVGC_280_32,(0,0,0):C.UVGC_258_10})

V_422 = CTVertex(name = 'V_422',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.ve ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_332_84})

V_423 = CTVertex(name = 'V_423',
                 type = 'UV',
                 particles = [ P.mu__plus__, P.mu__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_388_140,(0,3,0):C.UVGC_388_140,(0,2,0):C.UVGC_282_34,(0,4,0):C.UVGC_283_35,(0,0,0):C.UVGC_259_11})

V_424 = CTVertex(name = 'V_424',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.vm ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_333_85})

V_425 = CTVertex(name = 'V_425',
                 type = 'UV',
                 particles = [ P.ta__plus__, P.ta__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_403_155,(0,3,0):C.UVGC_403_155,(0,2,0):C.UVGC_302_54,(0,4,0):C.UVGC_303_55,(0,0,0):C.UVGC_262_14})

V_426 = CTVertex(name = 'V_426',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.vt ],
                 color = [ '1' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_334_86})

V_427 = CTVertex(name = 'V_427',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_412_164,(0,3,0):C.UVGC_412_164,(0,2,0):C.UVGC_330_82,(0,4,0):C.UVGC_331_83,(0,0,0):C.UVGC_263_15})

V_428 = CTVertex(name = 'V_428',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_386_138,(0,3,0):C.UVGC_386_138,(0,2,0):C.UVGC_277_29,(0,4,0):C.UVGC_278_30,(0,0,0):C.UVGC_257_9})

V_429 = CTVertex(name = 'V_429',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_293_45,(0,0,0):C.UVGC_394_146,(0,2,0):C.UVGC_396_148,(0,3,0):C.UVGC_297_49})

V_430 = CTVertex(name = 'V_430',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_269_21,(0,0,0):C.UVGC_384_136,(0,2,0):C.UVGC_382_134,(0,3,0):C.UVGC_273_25})

V_431 = CTVertex(name = 'V_431',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_292_44,(0,0,0):C.UVGC_395_147,(0,2,0):C.UVGC_393_145,(0,3,0):C.UVGC_296_48})

V_432 = CTVertex(name = 'V_432',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_397_149,(0,3,0):C.UVGC_397_149,(0,2,0):C.UVGC_300_52,(0,4,0):C.UVGC_301_53,(0,0,0):C.UVGC_260_12})

V_433 = CTVertex(name = 'V_433',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_284_36,(0,0,0):C.UVGC_391_143,(0,2,0):C.UVGC_389_141,(0,3,0):C.UVGC_288_40})

V_434 = CTVertex(name = 'V_434',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_270_22,(0,0,0):C.UVGC_383_135,(0,2,0):C.UVGC_385_137,(0,3,0):C.UVGC_274_26})

V_435 = CTVertex(name = 'V_435',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_285_37,(0,0,0):C.UVGC_390_142,(0,2,0):C.UVGC_392_144,(0,3,0):C.UVGC_289_41})

V_436 = CTVertex(name = 'V_436',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_380_132,(0,3,0):C.UVGC_380_132,(0,2,0):C.UVGC_265_17,(0,4,0):C.UVGC_266_18,(0,0,0):C.UVGC_255_7})

V_437 = CTVertex(name = 'V_437',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_381_133,(0,3,0):C.UVGC_381_133,(0,2,0):C.UVGC_267_19,(0,4,0):C.UVGC_268_20,(0,0,0):C.UVGC_256_8})

V_438 = CTVertex(name = 'V_438',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_402_154,(0,3,0):C.UVGC_402_154,(0,2,0):C.UVGC_312_64,(0,4,0):C.UVGC_313_65,(0,0,0):C.UVGC_261_13})

V_439 = CTVertex(name = 'V_439',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_314_66,(0,0,0):C.UVGC_406_158,(0,2,0):C.UVGC_404_156,(0,3,0):C.UVGC_318_70})

V_440 = CTVertex(name = 'V_440',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_322_74,(0,0,0):C.UVGC_410_162,(0,2,0):C.UVGC_408_160,(0,3,0):C.UVGC_326_78})

V_441 = CTVertex(name = 'V_441',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_315_67,(0,0,0):C.UVGC_405_157,(0,2,0):C.UVGC_407_159,(0,3,0):C.UVGC_319_71})

V_442 = CTVertex(name = 'V_442',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_305_57,(0,0,0):C.UVGC_399_151,(0,2,0):C.UVGC_401_153,(0,3,0):C.UVGC_309_61})

V_443 = CTVertex(name = 'V_443',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_323_75,(0,0,0):C.UVGC_409_161,(0,2,0):C.UVGC_411_163,(0,3,0):C.UVGC_327_79})

V_444 = CTVertex(name = 'V_444',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF3, L.FF4, L.FF5, L.FF6 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,1,0):C.UVGC_304_56,(0,0,0):C.UVGC_400_152,(0,2,0):C.UVGC_398_150,(0,3,0):C.UVGC_308_60})

V_445 = CTVertex(name = 'V_445',
                 type = 'UV',
                 particles = [ P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.SS1, L.SS3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_558_299,(0,1,0):C.UVGC_251_3})

V_446 = CTVertex(name = 'V_446',
                 type = 'UV',
                 particles = [ P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.SS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_556_298})

V_447 = CTVertex(name = 'V_447',
                 type = 'UV',
                 particles = [ P.G__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.SS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_556_298})

V_448 = CTVertex(name = 'V_448',
                 type = 'UV',
                 particles = [ P.a, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_264_16,(0,1,0):C.UVGC_249_1})

V_449 = CTVertex(name = 'V_449',
                 type = 'UV',
                 particles = [ P.a, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_338_90,(0,1,0):C.UVGC_415_167,(0,2,0):C.UVGC_339_91})

V_450 = CTVertex(name = 'V_450',
                 type = 'UV',
                 particles = [ P.Z, P.Z ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_340_92,(0,1,0):C.UVGC_568_308,(0,2,0):C.UVGC_253_5})

V_451 = CTVertex(name = 'V_451',
                 type = 'UV',
                 particles = [ P.W__minus__, P.W__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VV1, L.VV2, L.VV4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_335_87,(0,1,0):C.UVGC_562_302,(0,2,0):C.UVGC_252_4})

V_452 = CTVertex(name = 'V_452',
                 type = 'UV',
                 particles = [ P.g, P.g ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VV1, L.VV4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_281_33,(0,1,0):C.UVGC_250_2})

V_453 = CTVertex(name = 'V_453',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.d, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_608_346,(0,1,0):C.UVGC_604_342})

V_454 = CTVertex(name = 'V_454',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.d, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_578_317,(0,1,0):C.UVGC_582_321})

V_455 = CTVertex(name = 'V_455',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.s, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_605_343,(0,1,0):C.UVGC_609_347})

V_456 = CTVertex(name = 'V_456',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.s, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_597_335,(0,1,0):C.UVGC_601_339})

V_457 = CTVertex(name = 'V_457',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.b, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_581_320,(0,1,0):C.UVGC_577_316})

V_458 = CTVertex(name = 'V_458',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.b, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_600_338,(0,1,0):C.UVGC_596_334})

V_459 = CTVertex(name = 'V_459',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.u, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_640_376,(0,1,0):C.UVGC_644_380})

V_460 = CTVertex(name = 'V_460',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.u, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_648_384,(0,1,0):C.UVGC_652_388})

V_461 = CTVertex(name = 'V_461',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.c, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_643_379,(0,1,0):C.UVGC_639_375})

V_462 = CTVertex(name = 'V_462',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.c, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_628_365,(0,1,0):C.UVGC_624_361})

V_463 = CTVertex(name = 'V_463',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.t, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_651_387,(0,1,0):C.UVGC_647_383})

V_464 = CTVertex(name = 'V_464',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.t, P.H ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_625_362,(0,1,0):C.UVGC_629_366})

V_465 = CTVertex(name = 'V_465',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.d, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_607_345,(0,1,0):C.UVGC_606_344})

V_466 = CTVertex(name = 'V_466',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.d, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_576_315,(0,1,0):C.UVGC_583_322})

V_467 = CTVertex(name = 'V_467',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.s, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_603_341,(0,1,0):C.UVGC_610_348})

V_468 = CTVertex(name = 'V_468',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.s, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_595_333,(0,1,0):C.UVGC_602_340})

V_469 = CTVertex(name = 'V_469',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.b, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_580_319,(0,1,0):C.UVGC_579_318})

V_470 = CTVertex(name = 'V_470',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.b, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_599_337,(0,1,0):C.UVGC_598_336})

V_471 = CTVertex(name = 'V_471',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.u, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_641_377,(0,1,0):C.UVGC_642_378})

V_472 = CTVertex(name = 'V_472',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.u, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_649_385,(0,1,0):C.UVGC_650_386})

V_473 = CTVertex(name = 'V_473',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.c, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_645_381,(0,1,0):C.UVGC_638_374})

V_474 = CTVertex(name = 'V_474',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.c, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_630_367,(0,1,0):C.UVGC_623_360})

V_475 = CTVertex(name = 'V_475',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.t, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_653_389,(0,1,0):C.UVGC_646_382})

V_476 = CTVertex(name = 'V_476',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.t, P.G0 ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFS3, L.FFS4 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_626_363,(0,1,0):C.UVGC_627_364})

V_477 = CTVertex(name = 'V_477',
                 type = 'UV',
                 particles = [ P.ve__tilde__, P.ve, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_511_256})

V_478 = CTVertex(name = 'V_478',
                 type = 'UV',
                 particles = [ P.vm__tilde__, P.vm, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_511_256})

V_479 = CTVertex(name = 'V_479',
                 type = 'UV',
                 particles = [ P.vt__tilde__, P.vt, P.a ],
                 color = [ '1' ],
                 lorentz = [ L.FFV2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_511_256})

V_480 = CTVertex(name = 'V_480',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.d, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_294_46,(0,1,0):C.UVGC_298_50})

V_481 = CTVertex(name = 'V_481',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.d, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_272_24,(0,1,0):C.UVGC_276_28})

V_482 = CTVertex(name = 'V_482',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.s, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_295_47,(0,1,0):C.UVGC_299_51})

V_483 = CTVertex(name = 'V_483',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.b, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_271_23,(0,1,0):C.UVGC_275_27})

V_484 = CTVertex(name = 'V_484',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.s, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_287_39,(0,1,0):C.UVGC_291_43})

V_485 = CTVertex(name = 'V_485',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.b, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_286_38,(0,1,0):C.UVGC_290_42})

V_486 = CTVertex(name = 'V_486',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.u, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_316_68,(0,1,0):C.UVGC_320_72})

V_487 = CTVertex(name = 'V_487',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.u, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_324_76,(0,1,0):C.UVGC_328_80})

V_488 = CTVertex(name = 'V_488',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.c, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_317_69,(0,1,0):C.UVGC_321_73})

V_489 = CTVertex(name = 'V_489',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.t, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_325_77,(0,1,0):C.UVGC_329_81})

V_490 = CTVertex(name = 'V_490',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.c, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_307_59,(0,1,0):C.UVGC_311_63})

V_491 = CTVertex(name = 'V_491',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.t, P.a ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_306_58,(0,1,0):C.UVGC_310_62})

V_492 = CTVertex(name = 'V_492',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_481_226,(0,1,0):C.UVGC_484_229})

V_493 = CTVertex(name = 'V_493',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.d, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_474_219,(0,1,0):C.UVGC_475_220})

V_494 = CTVertex(name = 'V_494',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_482_227,(0,1,0):C.UVGC_483_228})

V_495 = CTVertex(name = 'V_495',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_473_218,(0,1,0):C.UVGC_476_221})

V_496 = CTVertex(name = 'V_496',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.s, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_478_223,(0,1,0):C.UVGC_479_224})

V_497 = CTVertex(name = 'V_497',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.b, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_477_222,(0,1,0):C.UVGC_480_225})

V_498 = CTVertex(name = 'V_498',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_490_235,(0,1,0):C.UVGC_492_237})

V_499 = CTVertex(name = 'V_499',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.u, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_494_239,(0,1,0):C.UVGC_496_241})

V_500 = CTVertex(name = 'V_500',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_489_234,(0,1,0):C.UVGC_491_236})

V_501 = CTVertex(name = 'V_501',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_493_238,(0,1,0):C.UVGC_495_240})

V_502 = CTVertex(name = 'V_502',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.c, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_485_230,(0,1,0):C.UVGC_487_232})

V_503 = CTVertex(name = 'V_503',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.t, P.Z ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_486_231,(0,1,0):C.UVGC_488_233})

V_504 = CTVertex(name = 'V_504',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_358_110,(0,1,0):C.UVGC_360_112})

V_505 = CTVertex(name = 'V_505',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.d, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_341_93,(0,1,0):C.UVGC_343_95})

V_506 = CTVertex(name = 'V_506',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_357_109,(0,1,0):C.UVGC_359_111})

V_507 = CTVertex(name = 'V_507',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.s, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_353_105,(0,1,0):C.UVGC_355_107})

V_508 = CTVertex(name = 'V_508',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_342_94,(0,1,0):C.UVGC_344_96})

V_509 = CTVertex(name = 'V_509',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.b, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_354_106,(0,1,0):C.UVGC_356_108})

V_510 = CTVertex(name = 'V_510',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.u, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_369_121,(0,1,0):C.UVGC_371_123})

V_511 = CTVertex(name = 'V_511',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.u, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_373_125,(0,1,0):C.UVGC_375_127})

V_512 = CTVertex(name = 'V_512',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.c, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_370_122,(0,1,0):C.UVGC_372_124})

V_513 = CTVertex(name = 'V_513',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.c, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_364_116,(0,1,0):C.UVGC_366_118})

V_514 = CTVertex(name = 'V_514',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_374_126,(0,1,0):C.UVGC_376_128})

V_515 = CTVertex(name = 'V_515',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.t, P.g ],
                 color = [ 'T(3,2,1)' ],
                 lorentz = [ L.FFV2, L.FFV3 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_363_115,(0,1,0):C.UVGC_365_117})

V_516 = CTVertex(name = 'V_516',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_569_309})

V_517 = CTVertex(name = 'V_517',
                 type = 'UV',
                 particles = [ P.a, P.G0, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VSS2 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_497_242})

V_518 = CTVertex(name = 'V_518',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.H, P.H ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_550_293})

V_519 = CTVertex(name = 'V_519',
                 type = 'UV',
                 particles = [ P.a, P.Z, P.G0, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VVSS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_550_293})

V_520 = CTVertex(name = 'V_520',
                 type = 'UV',
                 particles = [ P.ghWm, P.ghWm__tilde__ ],
                 color = [ '1' ],
                 lorentz = [ L.UU1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_435_184})

V_521 = CTVertex(name = 'V_521',
                 type = 'UV',
                 particles = [ P.ghWp, P.ghWp__tilde__ ],
                 color = [ '1' ],
                 lorentz = [ L.UU1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_435_184})

V_522 = CTVertex(name = 'V_522',
                 type = 'UV',
                 particles = [ P.ghZ, P.ghZ__tilde__ ],
                 color = [ '1' ],
                 lorentz = [ L.UU1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_521_264})

V_523 = CTVertex(name = 'V_523',
                 type = 'UV',
                 particles = [ P.a, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_254_6})

V_524 = CTVertex(name = 'V_524',
                 type = 'UV',
                 particles = [ P.W__minus__, P.G__plus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_426_176})

V_525 = CTVertex(name = 'V_525',
                 type = 'UV',
                 particles = [ P.W__plus__, P.G__minus__ ],
                 color = [ '1' ],
                 lorentz = [ L.VS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_426_176})

V_526 = CTVertex(name = 'V_526',
                 type = 'UV',
                 particles = [ P.Z, P.G0 ],
                 color = [ '1' ],
                 lorentz = [ L.VS1 ],
                 loop_particles = [ [ [] ] ],
                 couplings = {(0,0,0):C.UVGC_472_217})
