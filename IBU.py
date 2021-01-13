import math

# -------------------------
# Inputs
# -------------------------
ordinali = ['prima', 'seconda', 'terza', 'quarta', 'quinta', 'sesta', 'settima', 'ottava', 'nona', 'decima']
try:
    bugu = float(input("Inserire il rapporto BU:GU desiderato"))  # 0.82 #rapporto bu:gu che si vuole ottenere
except:
    print("ATTENZIONE: L'input dev'essere nel formato X.XX")
    bugu = float(input("Inserire il rapporto BU:GU desiderato"))  # 0.82 #rapporto bu:gu che si vuole ottenere
try:
    sg_preboil = float(input(
        "Inserire il SG misurato prima della bollitura (Formato 1.XXX)"))  # 1.043 #sg misurata prima della bollitura
except:
    print("ATTENZIONE: L'input dev'essere nel formato X.XX")
    sg_preboil = float(input(
        "Inserire il SG misurato prima della bollitura (Formato 1.XXX)"))  # 1.043 #sg misurata prima della bollitura
while sg_preboil > 1.5:
    print("ATTENZIONE: Valore di SG errato")
    float(input(
        "Inserire il SG misurato prima della bollitura (Formato 1.XXX)"))  # 1.043 #sg misurata prima della bollitura

boil_vol = float(
    input("Inserire il volume del mosto prima della bollitura (Litri)"))  # 12 #volume prima della bollitura
exp_vol = float(input(
    "Inserire il volume finale nel fermentatore, icluso eventuale rabbocco (Litri)"))  # volume finale in fermentatore
while boil_vol < exp_vol:
    print("ATTENZIONE: Il volume prima della bollitura non può essere minore del volume finale")
    boil_vol = float(
        input("Inserire il volume del mosto prima della bollitura (Litri)"))  # 12 #volume prima della bollitura
    exp_vol = float(input(
        "Inserire il volume finale nel fermentatore, icluso eventuale rabbocco (Litri)"))  # volume finale in fermentatore
num_gettate = int(input("Numero di gettate"))
if num_gettate > 1:
    diffl = input("La percentuale di alpha acidi è diversa da una gettata all'altra? (S/N)")
    while diffl not in ["S", "s", "N", "n"]:
        print("ATTENZIONE: Risposta invalida")
        diffl = input("La percentuale di alpha acidi è diversa da una gettata all'altra? (S/N)")
    if diffl in ["N", "n", "No", "no", "NO"]:
        aa1 = float(input("Inserire la percentuale di alpha acidi (X.X%)"))
        for i in range(num_gettate):
            i = i + 2
            program = "aa" + str(i) + "=" + "aa1"
            exec(program)
    elif diffl in diffl in ["S", "s", "si", "Sì", "SI"]:
        for k in range(num_gettate):
            k = k + 1
            t = input("Inserire la percentuale di alpha acidi (X.X%) della " + str(k) + "a gettata")
            program = "t" + str(k) + "=" + str(t)
            exec(program)
else:
    aa1 = float(input("Inserire la percentuale di alpha acidi (X.X%)"))

for k in range(num_gettate):
    k = k + 1
    t = input("Inserire il tempo di bollitura della " + str(k) + "a gettata (minuti)")
    program = "t" + str(k) + "=" + str(t)
    exec(program)

for k in range(num_gettate):
    k = k + 1
    t = input("Inserire la quantità di luppolo (grammi) nella " + str(k) + "a gettata")
    program = "w" + str(k) + "=" + str(t)
    exec(program)

unit = "g"


# -------------------------
# Functions
# -------------------------

def tinseth(alphaacid, peso, SG, tempo, volumefinale, unitapeso='g'):
    if unitapeso == 'g':
        peso = peso / 28.35
    elif unitapeso == 'kg':
        peso = (peso * 1000) / 28.35
    elif unitapeso == 'lb':
        peso = peso * 16

    ibu = (75 * (alphaacid * peso) * (1.65) * 0.000125 ** (SG - 1) * ((1 - math.exp(-0.4 * tempo)))) / volumefinale
    return ibu


def calculate_postboil_sg(sg_preboil, boil_vol, exp_vol):
    brix = 143.254 * sg_preboil ** 3 - 648.670 * sg_preboil ** 2 + 1125.805 * sg_preboil - 620.389  # Trasformo SG in brix
    gL = sg_preboil * (brix * 10)  # ottengo g di zuccheri disciolti in 1 L g/L
    gL = (gL * boil_vol) / exp_vol  # ricacolo la concentrazione nel volume finale
    sg = (0.3781 * gL + 998.521) / 1000  # riconverto in sg
    return sg


# -------------------------
# Calcolo IBU stimata
# -------------------------

g = calculate_postboil_sg(sg_preboil, boil_vol, exp_vol)
print("SG stimata: " + str(round(g,3)))
ibu = 0
for k in range(num_gettate):
    k = str(k + 1)
program = "ibu+=tinseth(aa" + k + "," + "w" + k + ",g,t" + k + ",exp_vol,unitapeso=unit)"
exec(program)

if ibu < 0:
    exit("ERRORE: IBU negativo. Chiudere e riaprire il programma e verificare gli input.")

# -------------------------
# Calcolo IBU necessaria per BUGU
# -------------------------

diff = (ibu - bugu * ((g - 1) * 1000)) / ibu
if diff < 1:
    ibu2 = 0
    for k in range(num_gettate):
        k = str(k + 1)
    program = "ibu2+=tinseth(aa" + k + "," + "(w" + k + "-w" + k + "*diff)" + ",g,t" + k + ",exp_vol,unitapeso=unit)"
    exec(program)
    program = "f=str(round(w" + k + "-w" + k + "*diff))"
    exec(program)
    program = "d=w" + k
    exec(program)
    print("Utilizzare " + f + unit + " invece di " + str(d) + unit + " nella prima gettata")
    print("Per un totale di " + str(round(ibu2)) + " IBU con rapporto BU:GU di " + str(round(ibu2 / ((g - 1) * 1000), 2)))
    print("IBU originale: " + str(round(ibu)))
elif diff == 0:
    print("Quantità di luppolo non necessita di correzioni.")
