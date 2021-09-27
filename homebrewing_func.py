import math


def calculate_postboil_sg(sg_preboil: float, boil_vol: float, exp_vol: float):
    """Estimation of SG in fermentor given a preboil SG, boil volume and desired fermentor volume"""
    brix = 143.254 * sg_preboil ** 3 - 648.670 * sg_preboil ** 2 + 1125.805 * sg_preboil - 620.389  # Turning SG in brix
    gL = sg_preboil * (brix * 10)  # getting total sugar concentration in 1 L (g/L)
    gL = (gL * boil_vol) / exp_vol  # recalculating concentration in final volume
    sg = (0.3781 * gL + 998.521) / 1000  # reconvert in sg
    return sg


def tinseth(alphaacid: float, weigth: float, SG: float, time: int, finalvolume: float, weightunit='g'):
    """Simple calculation of tinseth degrees given the alphaacid content, the weigth, time boiling, finalvolume
    obtained, can be used with grams (g), ounces (lb), or kg"""
    if weightunit == 'g':
        weigth /= 28.35
    elif weightunit == 'kg':
        weigth = (weigth * 1000) / 28.35
    elif weightunit == 'lb':
        weigth *= 16

    ibu = (75 * (alphaacid * weigth) * 1.65 * 0.000125 ** (SG - 1) * (1 - math.exp(-0.4 * time))) / finalvolume
    return ibu


def make_ordinal(n):
    if str(n)[-1] == '1':
        return f'{n}st'
    elif str(n)[-1] == '2':
        return f'{n}nd'
    elif str(n)[-1] == '3':
        return f'{n}rd'
    else:
        return f'{n}th'
