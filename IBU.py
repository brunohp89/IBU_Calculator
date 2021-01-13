import math

#-------------------------
# Inputs
#-------------------------

try:
    sg_preboil = float(input("Inserire il SG misurato prima della bollitura (Formato 1.XXX)"))#1.043 #sg misurata prima della bollitura
except:
    print("ATTENZIONE: L'input dev'essere nel formato X.XX")
    sg_preboil = float(input(
        "Inserire il SG misurato prima della bollitura (Formato 1.XXX)"))  # 1.043 #sg misurata prima della bollitura
while sg_preboil > 1.5:
    print("ATTENZIONE: Valore di SG errato")
    float(input(
        "Inserire il SG misurato prima della bollitura (Formato 1.XXX)"))  # 1.043 #sg misurata prima della bollitura

boil_vol = float(input("Inserire il volume del mosto prima della bollitura (Litri)"))#12 #volume prima della bollitura
exp_vol = float(input("Inserire il volume finale nel fermentatore, icluso eventuale rabbocco (Litri)")) #volume finale in fermentatore
while boil_vol < exp_vol:
    print("ATTENZIONE: Il volume prima della bollitura non può essere minore del volume finale")
    boil_vol = float(
        input("Inserire il volume del mosto prima della bollitura (Litri)"))  # 12 #volume prima della bollitura
    exp_vol = float(input(
        "Inserire il volume finale nel fermentatore, icluso eventuale rabbocco (Litri)"))  # volume finale in fermentatore

#-------------------------
# Functions
#-------------------------

def calculate_postboil_sg(sg_preboil,boil_vol,exp_vol):
    brix = 143.254 * sg_preboil**3 - 648.670 * sg_preboil**2 + 1125.805 * sg_preboil - 620.389 #Trasformo SG in brix
    gL = sg_preboil * (brix * 10) #ottengo g di zuccheri disciolti in 1 L g/L
    gL = (gL * boil_vol) / exp_vol #ricacolo la concentrazione nel volume finale
    sg = (0.3781 * gL + 998.521) / 1000 # riconverto in sg
    return sg

#-------------------------
# Calcolo IBU stimata
#-------------------------

g=calculate_postboil_sg(sg_preboil,boil_vol,exp_vol):
print("OG stimata:" + str(round(g,3)))