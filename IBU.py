from homebrewing_func import tinseth, calculate_postboil_sg, make_ordinal
import re

# -------------------------
# Inputs
# -------------------------
ordinali = ['prima', 'seconda', 'terza', 'quarta', 'quinta', 'sesta', 'settima', 'ottava', 'nona', 'decima']

bugu = input("Insert BU:GU ratio you desire to obtain")  # example 0.82
while not re.match('^[0-1].[0-9]{2}$', bugu):
    print("ERROR: The input has to be in the format X.XX")
    bugu = input("Insert BU:GU ratio you desire to obtain")
bugu = float(bugu)

sg_preboil = input("Insert measured SG before boiling (Format 1.XXX)")  # example 1.043
while not re.match('^1.[0-5][0-9]{2}$', sg_preboil):
    print("ERROR: The input has to be in the OG format X.XXX and smaller than 1.5")
    sg_preboil = input("Insert measured SG before boiling (Format 1.XXX)")
sg_preboil = float(sg_preboil)

boil_vol = float(
    input("Insert volume before boiling (Liters)"))  # example 12 --> the volume before boiling
exp_vol = float(input(
    "Inserire final fermentor volume including top-ups (Liters)"))  # example 9 --> # final volume in fermentor
while boil_vol < exp_vol:
    print("ERROR: The pre-boil volume cannot be smallert than final volume")
    boil_vol = float(
        input("Insert volume before boiling (Liters)"))
    exp_vol = float(input(
        "Inserire final fermentor volume including top-ups (Liters)"))

num_gettate = int(input("Insert the number of hops addition"))  # How many times during boil you add hops
if num_gettate > 1:
    diffl = input("Is the AA% different from one addition to the other? (Y/N)")
    while diffl not in ["Y", "y", "N", "n"]:
        print("ERROR: Invalid answer")
        diffl = input("Is the AA% different from one addition to the other? (Y/N)")
    if diffl in ["N", "n"]:
        aa1 = float(input("Insert the AA% (X.X%)"))
        for i in range(num_gettate):
            i = i + 2
            program = "aa" + str(i) + "=" + "aa1"
            exec(program)
    elif diffl in diffl in ["Y", "y"]:
        for k in range(num_gettate):
            k = k + 1
            t = input(f'Insert the AA%  of the {make_ordinal(k)} addition (X.X%)')
            program = "t" + str(k) + "=" + str(t)
            exec(program)
else:
    aa1 = float(input("Insert the AA% (X.X%)"))

for k in range(num_gettate):
    k = k + 1
    t = input(f'Insert boiling time of the {make_ordinal(k)} addition (minutes)')
    program = "t" + str(k) + "=" + str(t)
    exec(program)

for k in range(num_gettate):
    k = k + 1
    t = input(f'Insert weight in grams of the {make_ordinal(k)} addition (grams)')
    program = "w" + str(k) + "=" + str(t)
    exec(program)

# -------------------------
# Estimate IBU calculation
# -------------------------

g = calculate_postboil_sg(sg_preboil, boil_vol, exp_vol)
print("Estimated SG in fermentor will be :" + str(round(g, 3)))
ibu = 0
for k in range(num_gettate):
    k = str(k + 1)
    program = f'ibu+=tinseth(aa{k},w{k},g,t{k},exp_vol)'
    exec(program)

if ibu < 0:
    exit("ERRORE: IBU cannot be negative, please close the program and start again being careful to "
         "input correct data.")

# -------------------------
# Calcolo IBU necessaria per BUGU
# -------------------------

diff = (ibu - bugu * ((g - 1) * 1000)) / ibu
if diff < 1:
    ibu2 = 0
    for k in range(num_gettate):
        k = str(k + 1)
    program = f'ibu2+=tinseth(aa{k},w{k},g,t{k},exp_vol)'
    exec(program)
    program = f'f=str(round(w{k}-w{k}*diff))'
    exec(program)
    program = "d=w" + k
    exec(program)
    print(f"Use {f} {unit} instead of {d} {unit} in the first addition")
    print(
        "For a total of " + str(round(ibu2)) + " IBU with BU:GU ratio of " + str(round(ibu2 / ((g - 1) * 1000), 2)))
    print("Original IBU : " + str(round(ibu)))
elif diff == 0:
    print("No need for corrections in the hops additions")
