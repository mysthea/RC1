#!/usr/bin/env python
# encoding: utf-8

from math import sin, cos, ceil

from .consts import *

ERRORS = []


def compute_punching(c_class, s_class, dsw, support, sect, b, h, dx, dy, lx,
                     ly, ad, lambda_u, asx, asy, dsit, ved, beta):
    """
    Procedura sprawdzenia nośności na przebicie płyty betonowej wg PN-EN 1992-1
    """
    support_id = support.id

    # -----------------------------------------
    # MATERIAL
    # Beton
    fck = c_tab[c_class.type] * MPa
    # Stal
    fyk = s_tab[s_class.type] * MPa
    alfa_sw = 0.8           # redukcja wytrzymalosci zbr. na ścinanie
    
    # -----------------------------------------
    # GEOMETRIA
    # Element = 'plyta'    # do wyboru: plyta, stopa fundamentowa TODO
    cx = float(b) * cm     # cx = 40 * cm
    cy = float(h) * cm     #cy = 40 * cm
    #D = 40 * cm	       # dla przekroju kolowego TODO
    dsw = dsw.value * mm   # srednica zbrojenia na ścinanie
    dx = float(dx) * cm
    dy = float(dy) * cm
    lx = float(lx) * cm    # odleglosc pola obciazenia do krawedzi plyty w kier. x
    ly = float(ly) * cm    # jw. w kier. y
    ad = float(ad) * cm
    asx = float(asx) * cm2
    asy = float(asy) * cm2    
    lambda_u = lambda_u     # wsp. uwzgledniajacy otwor w poblizu obwodu kontrolnego (%)  # TODO: to przypisanie jest tu bez sensu, ale zrobiłam tak, żeby był ślad po lambda_u
    alfa = pi / 2   # kat miedzy zbrojeniem na ścinanie i plaszczyzna plyty TODO: (zmienic na deg!!!!!!!!!!)

    # -----------------------------------------
    # WARUNKI PRACY
    # TODO wszystko poniżej: musimy trzymać się konwencji pythonowych, nazwy zmiennych małą literą z podkreślnikami, jeśli chcemy coś oddzielić
    design_sit = dsit
    # Faktory
    if design_sit == 'trwała' or design_sit == 'przejściowa':
        gamma_c = 1.4
        gamma_s = 1.15
        alfa_cc = 1.0
    else:   # wyjątkowa
        gamma_c = 1.2
        gamma_s = 1.0
        alfa_cc = 1.0

    # Obciazenia
    beta = beta		# gdzie jest beta?
    ved = 600 * kN	# dodac komentarz, ze nie jest to reakcja, tylko sila tnaca z plyty na slup
                    # dla fundamentow mozna zredukowac sile do VEdred - por. 6.4.4(2)
    # med = 50 * kNm	# TODO do rozwiniecia...

    # ############## OBLICZENIA ##############
    # -----------------------------------------
    # MATERIAL
    fcd = alfa_cc * fck / gamma_c

    fyd = fyk / gamma_s
    fywd = alfa_sw * fyk

    # -----------------------------------------
    # GEOMETRY
    d = (dx + dy) / 2 - ad  # spr. czy sie nie zgrywa z 'D' (srednica kola)

    u00 = compute_u00(support_id, cx, cy, d)
    if u00:
        u0 = (1 - lambda_u / 100) * u00
    else:
        return 0, 0, ERRORS
    u11 = compute_u11(support, cx, cy, d, lx, ly)
    if u11:
        u1 = (1 - lambda_u / 100) * u11
    else:
        return 0, 0, ERRORS

    # -----------------------------------------
    # NAPREZENIA
    # Maksymalne naprezenie przy przebiciu (vEd)
    '''def beta(support):	# okreslic dokladnie wg wzorow !!!!!!!!!!!!!!!!
        if support == 'wewnetrzny':
            return 1.15
        elif support == 'krawedziowy X':
            return 1.4
        elif support == 'krawedziowy Y':
            return 1.4
        elif support == 'narozny':
            return 1.5
        else:
        	return 0
        	ERRORS.append('Błąd w określeniu beta.')   '''
    ved0 = beta * ved * (u0 * d)
    ved1 = beta * ved * (u1 * d)

    # Maksymalna wytrzymalosc na ścinanie przy przebiciu ze wzgledu na sciskane krzyzulce betonowe (vRdmax)
    ni = 0.6 * (1.0 - fck / (250 * MPa))
    vrdmax = 0.4 * ni * fcd

    if vrdmax >= ved0:
        ERRORS.append('Nośność betonu na ścinanie przy przebiciu zachowana (vEd0 <= vRdmax).')
        print('Nośność betonu na ścinanie przy przebiciu zachowana (vEd0 <= vRdmax).')
    else:   # elif vrdmax < ved0:
        ERRORS.append('Nośność betonu na ścinanie przekroczona (vEd0 > vRdmax)!')
        print('Nośność betonu na ścinanie przekroczona (vEd0 > vRdmax)!')

    # Nośność na ścinanie przy przebiciu bez zbrojenia na przebicie (vRdc)
    crdc = 0.18 / gamma_c
    k = min(1.0 + (200 * mm / d)**0.5, 2.0)
    ro_lx = asx / ((cy + 6 * d) * d)
    ro_ly = asy / ((cx + 6 * d) * d)
    ro_l = min((ro_lx * ro_ly)**0.5, 0.02)
    vmin = 0.035 * k**(3/2) * (fck / MPa)**0.5 * MPa
    k1 = 0.1
    sigma_cp = 0.0 * MPa		# rozwinac !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    vrdc = max(crdc * k * (100 * ro_l * fck / MPa)**(1/3) * MPa + k1 * sigma_cp, vmin + k1 * sigma_cp)

    # -----------------------------------------
    # ZBROJENIE

    if vrdc >= ved1:
        ERRORS.append('Nośność na ścinanie przy przebiciu zachowana (vEd1 <= vRdc).')
        print('Nośność na ścinanie przy przebiciu zachowana (vEd1 <= vRdc).')
        asw_req = 0.0   # TODO: nigdzie nie zostało użyte
        nsw_req = 0.0   # TODO: nigdzie nie zostało użyte
    else:   # elif vRdc < vEd1:
        ERRORS.append('Nośność na ścinanie przekroczona (vEd1 > vRdc)!')
        print('Nośność na ścinanie przekroczona (vEd1 > vRdc)!')
        # Obliczenie zbrojenia wymaganego wg Nośnośći na ścinanie przy przebiciu ze zbrojeniem na przebicie (vRdcs)
        sr_max = 0.75 * d 	# promieniowy rozstaw strzemion
        fywd_ef = max((250 + 0.25 * d / mm) * MPa, fywd)
        asw_req = (ved1 - 0.75 * vrdc) * sr_max / (1.5 * d) * u1 * d / (fywd_ef * sin(alfa))
        asw_1bar = pi * dsw**2 / 4
        nsw_req = asw_req / asw_1bar

        # Zbrojenie minimalne
        ro_sw_min = 0.08 * (fck / MPa)**0.5 * MPa / fyk
        st_max = 2.0 * d 	# styczny rozstw strzemion
        asw_min = ro_sw_min * sr_max * st_max / (1.5 * sin(alfa) + cos(alfa))	# czy aby poprawna intepretacja pola jedengo ramienia strzemion??????
        nsw_min = asw_min / asw_1bar

        # Przyjecie zbrojenia
        nsw_prov = ceil(max(nsw_req, nsw_min))
        asw_prov = nsw_prov * asw_1bar

        # Nośność na ścinanie przy przebiciu ze zbrojeniem na przebicie (vRdcs)
        vrdcs = 0.75 * vrdc + 1.5 * d / sr_max * asw_prov * fywd_ef / (u1 * d) * sin(alfa)

        if vrdcs >= ved1:
            ERRORS.append('Nośność na ścinanie przy przebiciu zachowana (vEd1 <= vRdcs).')
            print('Nośność na ścinanie przy przebiciu zachowana (vEd1 <= vRdcs).')
        else:   # elif vrdcs < ved1:
            ERRORS.append('Nośność na ścinanie przekroczona (vEd1 > vRdcs)!')
            print('Nośność na ścinanie przekroczona (vEd1 > vRdcs)!')

        # Rozmieszczenie zbrojenia
            # Co najmniej 2 obwody strzemin
            # Max rozstaw obwodow 0.75d
            # Max rozstaw strzemion w obwodzie 2d (1.5d dla u1)
  
        u_out = beta * ved / (vrdc * d)

        a_out = compute_a_out1(support, u_out, cx, cy, lx, ly) # TODO: nigdzie nie zostało użyte

    # TODO: do zrobienia powyżej, natomiast poniżej do sprawdzenia, czy jest ok
    vrdc = asw_prov / cm / cm
    vrdmax = asx / cm / cm
    return vrdc, vrdmax, ERRORS


def compute_u00(support_id, cx, cy, d):
    # TODO: zrobić coś z tymi komentarzami, w bazie dodatkowo:
    # TODO: ściana - naroże (3) i ściana - koniec (4)
    if support_id == 0:
        return 2 * (cx + cy)
    elif support_id == 1:   # Poprawic, poki co jest roboczo !!!
        return min(2 * cx + cy, cy + 3 * d)
    #elif support_id == 'słup krawędziowy X':
    #    return min(2 * cx + cy, cy + 3 * d)
    #elif support_id == 'słup krawędziowy Y':
    #    return min(cx + 2 * cy, cx + 3 * d)
    elif support_id == 2:
        return min(cx + cy, 3 * d)
    else:
        ERRORS.append('Błąd w określeniu położenia słupa.')
        return None


def compute_u11(support_id, cx, cy, d, lx, ly):
    # TODO: jak wyżej
    if support_id == 0:
        return 2 * cx + 2 * cy + 4 * pi * d
    if support_id == 1:   # Poprawic, poki co jest roboczo !!!
        return 2 * cx + 1 * cy + 2 * pi * d + 2 * lx
    # elif support_id == 'słup krawędziowy X':
    #     return 2 * cx + 1 * cy + 2 * pi * d + 2 * lx
    # elif support_id == 'słup krawędziowy Y':
    #     return 1 * cx + 2 * cy + 2 * pi * d + 2 * ly
    elif support_id == 2:
        return 1 * cx + 1 * cy + 1 * pi * d + lx + ly
    else:
        ERRORS.append('Błąd w określeniu położenia słupa.')
        return None


def compute_a_out1(support, u_out, cx, cy, lx, ly):
    if support == 0:
        return (u_out - (2 * cx + 2 * cy)) / (2 * pi)
    elif support == 1:
    # Poprawic, poki co jest roboczo !!!
        return (u_out - (2 * cx + 1 * cy + 2 * lx)) / pi
    elif support == 2:
        return (u_out - (1 * cx + 1 * cy + lx + ly)) / (0.5 * pi)
    else:
        ERRORS.append('Błąd w określeniu umax.')
        return None
