import math

# ==========================================
print("\n--- Aufgabe 1: Impedanz & Phasenwinkel ---")
# ==========================================
Z = 2.5
X = -1.5 
R = math.sqrt(Z**2 - X**2)
phi_rad = math.atan(X / R)

print(f"phi = {phi_rad} Radian")
print(f"R = {R} Ohm")


# ==========================================
print("\n--- Aufgabe 2: Admittanz ---")
# ==========================================
Z2 = 5
R2 = 4
X2 = -math.sqrt(Z2**2 - R2**2)
phi_rad2 = math.atan(X2 / R2)
Z_komplex2 = complex(R2, X2)
Y = 1 / Z_komplex2

print(f"phi = {phi_rad2} Radian")
print(f"X = {X2} Ohm")
print(f"Y = {Y} Siemens")


# ==========================================
print("\n--- Aufgabe 3: Dreiphasen-Leistung ---")
# ==========================================
P_3ph = 240000
U_LL = 2400
cos_phi = 0.8

P = P_3ph / 3
U_strang3 = U_LL / math.sqrt(3)  
phi_rad3 = -math.acos(cos_phi)
S_betrag = P / cos_phi
Q = S_betrag * math.sin(phi_rad3)
S_komplex3 = complex(P, Q)
I_konjugiert3 = S_komplex3 / U_strang3
I_komplex3 = I_konjugiert3.conjugate()
Z_komplex3 = U_strang3 / I_komplex3

print(f"S = {S_komplex3} VA")
print(f"Z = {Z_komplex3} Ohm")
print(f"I = {I_komplex3} A")


# ==========================================
print("\n--- Aufgabe 4: Parallele Lasten ---")
# ==========================================
U_LL4 = 2400 
S1_3ph = 300000
Q1_3ph = 180000
S2_3ph = 240000
P2_3ph = 144000

P1_3ph = math.sqrt(S1_3ph**2 - Q1_3ph**2)
Q2_3ph = -math.sqrt(S2_3ph**2 - P2_3ph**2)
S1_komplex = complex(P1_3ph, Q1_3ph)
S2_komplex = complex(P2_3ph, Q2_3ph)
S_komplex_3ph = S1_komplex + S2_komplex
S_komplex_1ph = S_komplex_3ph / 3
U_strang4 = U_LL4 / math.sqrt(3)
I_konjugiert4 = S_komplex_1ph / U_strang4 
I_komplex4 = I_konjugiert4.conjugate()

print(f"I = {I_komplex4} A")
print(f"S = {S_komplex_1ph} VA")


# ==========================================
print("\n--- Aufgabe 5: pu-Berechnung Trafos & Leitungen ---")
# ==========================================
S_B5 = 100
U_B2_5 = 33  
x_tr1 = 10 / 100
x_tr2 = 12 / 100
x_m = 20 / 100
X_leitung_ohm = 18
Z_B2_5 = (U_B2_5 ** 2) / S_B5
x_l = X_leitung_ohm / Z_B2_5

print(f"x_tr1 = {x_tr1} pu")
print(f"x_l = {x_l} pu")
print(f"x_tr2 = {x_tr2} pu")
print(f"x_m = {x_m} pu")


# ==========================================
print("\n--- Aufgabe 6: Rückwärtsrechnung im Strahlnetz ---")
# ==========================================
S_B6 = 150
U_B2_6 = 230
U_B1_6 = 15

Z_T1_T2_parallel = complex(0, 0.10 / 2)
Z_T3 = complex(0, 0.10)
Z_B2_6 = (U_B2_6**2) / S_B6   
Z_L6 = complex(0, 50 / Z_B2_6)

S1_pu = complex(150, 60) / S_B6
S2_pu = complex(-120, -60) / S_B6

U4 = complex(1.0, 0)
I_L2 = (S2_pu / U4).conjugate()
U3 = U4 + (I_L2 * Z_T3)
U2 = U3 + (I_L2 * Z_L6)
I_L1 = (S1_pu / U2).conjugate()
I_Gesamt = I_L2 + I_L1
U1 = U2 + (I_Gesamt * Z_T1_T2_parallel)
U1_abs_pu = abs(U1)
U1_Volt = U1_abs_pu * U_B1_6 * 1000

print(f"U1 = {U1_Volt} V\n")