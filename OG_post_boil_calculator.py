import re
from homebrewing_func import calculate_postboil_sg

# -------------------------
# Inputs
# -------------------------

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


g = calculate_postboil_sg(sg_preboil, boil_vol, exp_vol)
print("Estimated SG in fermentor will be :" + str(round(g, 3)))
