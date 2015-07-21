#!/usr/bin/env python
# encoding: utf-8

import math

from .consts import *

C_tab = {'C12/15': 12, 'C16/20': 16, 'C20/25': 20, 'C25/30': 25, 'C30/37': 30,
         'C35/45': 35, 'C40/50': 40, 'C45/55': 45, 'C50/60': 50, 'C55/67': 55,
         'C60/75': 60, 'C70/85': 70, 'C80/95': 80, 'C90/105': 90}

S_tab = {'35G2Y': 410, '34GS': 410, 'RB400': 400, 'RB400W': 400,
         '20G2VY-b': 490, 'RB500': 500, 'RB500W': 500, 'B500SP': 500,
         'BSt420': 420, 'BSt500': 500}


def compute_punching(c_class, s_class, dsw, support, sect, b, h, dx, dy, lx,
                     ly, ad, lambda_u, asx, asy, dsit, ved, beta):
    """
    Procedura sprawdzenia nosnosci na przebicie plyty betonowej wg PN-EN 1992-1
    """
    errors = []

    # MATERIAL
    # Beton
    fck = C_tab[c_class.type] * MPa
    # Stal
    fyk = S_tab[s_class.type] * MPa
    alfaSw = 0.8    # redukcja wytrzymalosci zbr. na scinanie TODO

    # GEOMETRIA

    Element = 'plyta'	# do wyboru: plyta, stopa fundamentowa TODO
    ColPos = 'wewnetrzny'	# Slup wewnetrzny, krawedziowy X / Y, narozny TODO
    # cbColPos.index TODO
    Section = 'prostokatny'	# Przekroj prostokatny, kolowy TODO
    cx = 40 * cm    # TODO
    cy = 40 * cm    # TODO
    #D = 40 * cm	# dla przekroju kolowego TODO
    dsw = dsw.value * mm  # srednica zbrojenia na scinanie
    dx = float(dx) * cm
    dy = float(dy) * cm
    lx = float(lx) * cm    # odleglosc pola obciazenia do krawedzi plyty w kier. x
    ly = float(ly) * cm    # jw. w kier. y
    asx = float(asx) * cm2
    asy = float(asy) * cm2
    alfa = pi / 2 # kat miedzy zbrojeniem na scinanie i plaszczyzna plyty (zmienic na deg!!!!!!!!!!)    # TODO
    lambda_u = lambda_u   # wsp. uwzgledniajacy otwor w poblizu obwodu kontrolnego (%)  # TODO: to przypisanie jest tu bez sensu, ale zrobiłam tak, żeby był ślad po lambda_u

    # -----------------------------------------
    # SYTUCJA OBLICZENIOWA

    # TODO wszystko poniżej: musimy trzymać się konwencji pythonowych, nazwy zmiennych małą literą z podkreślnikami, jeśli chcemy coś oddzielić
    # Faktory
    gammaC = 1.4	# dac jako syt. obl.: trwala, przejsciowa, wyjatkowa
    gammaS = 1.15
    alfaCC = 1.0

    # Obciazenia
    VEd = 600 * kN	# dodac komenarz, ze nie jest to reakcja, tylko sila tnaca z plyty na slup
                    # dla fundamentow mozna zredukowac sile do VEdred - por. 6.4.4(2)
    # MEd = 50 * kNm


    # ############## OBLICZENIA ##############
    # -----------------------------------------
    # MATERIAL
    fcd = alfaCC * fck / gammaC

    fyd = fyk / gammaS
    fywd = alfaSw * fyk

    # -----------------------------------------
    # GEOMETRIA
    d = (dx + dy) / 2	# spr. czy sie nie zgrywa z 'D' (srednica kola)

    # -> u0
    if ColPos == 'wewnetrzny':			# uzyc 'case'
    # zrobic to na indeksach obiektow (1, 2, 3), zeby nie wpisywac w nieskonczonosc: wew., kraw. etc. (ryzyko pomylki)
        u0 = 2 * (cx + cy)
    elif ColPos == 'krawedziowy X':
        u0 = min(2 * cx + 1 * cy, cy + 3 * d)
    elif ColPos == 'krawedziowy Y':
        u0 = min(1 * cx + 2 * cy, cx + 3 * d)
    elif ColPos == 'narozny':
        u0 = min(cx + cy, 3 * d)
    else:
        errors.append('Blad w okresleniu polozenia slupa.')
        print('Blad w okresleniu polozenia slupa.')
    '''def u00(ColPos):
        if ColPos == 'wewnetrzny':
        # zrobic to na indeksach obiektow (1, 2, 3), zeby nie wpisywac w nieskonczonosc: wew., kraw. etc. (ryzyko pomylki)
            return 2 * (cx + cy)
        if ColPos == 'krawedziowy X':
            return min(2 * cx + cy, cy + 3 * d)
        if ColPos == 'krawedziowy Y':
            return min(cx + 2 * cy, cx + 3 * d)
        if ColPos == 'narozny':
            return min(cx + cy, 3 * d)
    u0 = u00(ColPos)	'''

    # -> u1
    if ColPos == 'wewnetrzny':
    # zrobic to na indeksach obiektow (1, 2, 3), zeby nie wpisywac w nieskonczonosc: wew., kraw. etc. (ryzyko pomylki)
        u1 = 2 * cx + 2 * cy + 4 * pi * d
    if ColPos == 'krawedziowy X':
        u1 = 2 * cx + 1 * cy + 2 * pi * d + 2 * lx
    if ColPos == 'krawedziowy Y':
        u1 = 1 * cx + 2 * cy + 2 * pi * d + 2 * ly
    if ColPos == 'narozny':
        u1 = 1 * cx + 1 * cy + 1 * pi * d + lx + ly
    '''def u11(ColPos):
        if ColPos == 'wewnetrzny':
        # zrobic to na indeksach obiektow (1, 2, 3), zeby nie wpisywac w nieskonczonosc: wew., kraw. etc. (ryzyko pomylki)
            return 2 * cx + 2 * cy + 4 * pi * d
        if ColPos == 'krawedziowy X':
            return 2 * cx + 1 * cy + 2 * pi * d + 2 * lx
        if ColPos == 'krawedziowy Y':
            return 1 * cx + 2 * cy + 2 * pi * d + 2 * ly
        if ColPos == 'narozny':
            return 1 * cx + 1 * cy + 1 * pi * d + lx + ly	'''
    u1 = lambda_u * u1

    # -----------------------------------------
    # NAPREZENIA

    # Maksymalne naprezenie przy przebiciu (vEd)
    if ColPos == 'wewnetrzny':
        beta = 1.15
    if ColPos == 'krawedziowy X':
        beta = 1.4
    if ColPos == 'krawedziowy Y':
        beta = 1.4
    if ColPos == 'narozny':
        beta = 1.5
    '''def beta(ColPos):	# okreslic dokladnie wg wzorow !!!!!!!!!!!!!!!!
        if ColPos == 'wewnetrzny':
            return 1.15
        if ColPos == 'krawedziowy X':
            return 1.4
        if ColPos == 'krawedziowy Y':
            return 1.4
        if ColPos == 'narozny':
            return 1.5	'''
    vEd0 = beta * VEd * (u0 * d)
    vEd1 = beta * VEd * (u1 * d)

    # Maksymalna wytrzymalosc na scinanie przy przebiciu ze wzgledu na sciskane krzyzulce betonowe (vRdmax)
    ni = 0.6 * ( 1.0 - fck / (250 * MPa) )
    vRdmax = 0.4 * ni * fcd

    if vRdmax >= vEd0:
        errors.append('Nosnosc betonu na scinanie przy przebiciu zachowana (vEd0 <= vRdmax).')
        print('Nosnosc betonu na scinanie przy przebiciu zachowana (vEd0 <= vRdmax).')
    elif vRdmax < vEd0:
        errors.append('Nosnosc betonu na scinanie przekroczona (vEd0 > vRdmax)!')
        print('Nosnosc betonu na scinanie przekroczona (vEd0 > vRdmax)!')

    # Nosnosc na scinanie przy przebiciu bez zbrojenia na przebicie (vRdc)
    CRdc = 0.18 / gammaC
    k = min( 1.0 + (200 * mm / d)**0.5, 2.0 )
    roLx = asx / ( (cy + 6 * d) * d )
    roLy = asy / ( (cx + 6 * d) * d )
    roL = min( (roLx * roLy)**0.5, 0.02 )
    vmin = 0.035 * k**(3/2) * (fck / MPa)**0.5 * MPa
    k1 = 0.1
    sigmaCp = 0.0 * MPa		# rozwinac !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    vRdc = max( CRdc * k * (100 * roL * fck / MPa)**(1/3) * MPa + k1 * sigmaCp, vmin + k1 * sigmaCp )

    # -----------------------------------------
    # ZBROJENIE

    if vRdc >= vEd1:
        errors.append('Nosnosc na scinanie przy przebiciu zachowana (vEd1 <= vRdc).')
        print('Nosnosc na scinanie przy przebiciu zachowana (vEd1 <= vRdc).')
        Asw_req = 0.0
        nsw_req = 0.0
    elif vRdc < vEd1:
        errors.append('Nosnosc na scinanie przekroczona (vEd1 > vRdc)!')
        print('Nosnosc na scinanie przekroczona (vEd1 > vRdc)!')
        # Obliczenie zbrojenia wymaganego wg Nosnosci na scinanie przy przebiciu ze zbrojeniem na przebicie (vRdcs)
        sr_max = 0.75 * d 	# promieniowy rozstaw strzemion
        fywd_ef = max( (250 + 0.25 * d / mm) * MPa, fywd )
        Asw_req = (vEd1 - 0.75 * vRdc) * sr_max / (1.5 * d) * u1 * d / ( fywd_ef * math.sin(alfa) )
        Asw_1bar = pi * dsw**2 / 4
        nsw_req = Asw_req / Asw_1bar

        # Zbrojenie minimalne
        roSw_min = 0.08 * (fck / MPa)**0.5 * MPa / fyk
        st_max = 2 * d 	# styczny rozstw strzemion
        Asw_min = roSw_min * sr_max * st_max / ( 1.5 * math.sin(alfa) + math.cos(alfa) )	# czy aby poprawna intepretacja pola jedengo ramienia strzemion??????
        nsw_min = Asw_min / Asw_1bar

        # Przyjecie zbrojenia
        nsw_prov = math.ceil( max(nsw_req, nsw_min) )
        Asw_prov = nsw_prov * Asw_1bar

        # Nosnosc na scinanie przy przebiciu ze zbrojeniem na przebicie (vRdcs)
        vRdcs = 0.75 * vRdc + 1.5 * d / sr_max * Asw_prov * fywd_ef / (u1 * d) * math.sin(alfa)

        if vRdcs >= vEd1:
            errors.append('Nosnosc na scinanie przy przebiciu zachowana (vEd1 <= vRdcs).')
            print('Nosnosc na scinanie przy przebiciu zachowana (vEd1 <= vRdcs).')
        elif vRdcs < vEd1:
            errors.append('Nosnosc na scinanie przekroczona (vEd1 > vRdcs)!')
            print('Nosnosc na scinanie przekroczona (vEd1 > vRdcs)!')

        # Rozmieszczenie zbrojenia
            # Co najmniej 2 obwody strzemin
            # Max rozstaw obwodow 0.75d
            # Max rozstaw strzemion w obwodzie 2d (1.5d dla u1)

        uout = beta * VEd / (vRdc * d)
        # -> rout
        if ColPos == 'wewnetrzny':
            rout = ( uout - (2 * cx + 2 * cy) ) / (2 * pi)
        if ColPos == 'krawedziowy X':
            rout = ( uout - (2 * cx + 1 * cy + 2 * lx) ) / (pi)
        if ColPos == 'krawedziowy Y':
            rout = ( uout - (1 * cx + 2 * cy + 2 * ly) ) / (pi)
        if ColPos == 'narozny':
            rout = ( uout - (1 * cx + 1 * cy + lx + ly) ) / (0.5 * pi)

    # TODO: do zrobienia powyżej, natomiast poniżej do sprawdzenia, czy jest ok
    vrdc = Asw_prov / cm / cm
    vrdmax = asx / cm / cm
    return vrdc, vrdmax, errors





