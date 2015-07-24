#!/usr/bin/env python
# encoding: utf-8

import math
# sin = lambda x: math.sin(x)   # uzyte w asw_req

from .consts import *

c_tab = {'C12/15': 12, 'C16/20': 16, 'C20/25': 20, 'C25/30': 25, 'C30/37': 30,
         'C35/45': 35, 'C40/50': 40, 'C45/55': 45, 'C50/60': 50, 'C55/67': 55,
         'C60/75': 60, 'C70/85': 70, 'C80/95': 80, 'C90/105': 90}

s_tab = {'35G2Y': 410, '34GS': 410, 'RB400': 400, 'RB400W': 400,
         '20G2VY-b': 490, 'RB500': 500, 'RB500W': 500, 'B500SP': 500,
         'BSt420': 420, 'BSt500': 500}


def compute_punching(c_class, s_class, dsw, support, sect, b, h, dx, dy, lx,
                     ly, ad, lambda_u, asx, asy, dsit, ved, beta):
    """
    Procedura sprawdzenia nosnosci na przebicie plyty betonowej wg PN-EN 1992-1
    """
    errors = []

    # -----------------------------------------
    # MATERIAL
    # Beton
    fck = c_tab[c_class.type] * MPa
    # Stal
    fyk = s_tab[s_class.type] * MPa
    alfa_sw = 0.8           # redukcja wytrzymalosci zbr. na scinanie TODO
    
    # -----------------------------------------
    # GEOMETRIA
    # Element = 'plyta'    # do wyboru: plyta, stopa fundamentowa TODO
    support = support      # Bez sensu, ale poki co dla porzadku #'Słup wewnetrzny'	# Slup wewnetrzny, krawedziowy X / Y, narozny TODO  # cbColPos.index TODO
    sect = sect            # jw. # 'prostokatny'	# Przekroj prostokatny, kolowy TODO
    cx = float(b) * cm     # cx = 40 * cm    # TODO
    cy = float(h) * cm     #cy = 40 * cm    # TODO
    #D = 40 * cm	       # dla przekroju kolowego TODO
    dsw = dsw.value * mm   # srednica zbrojenia na scinanie
    dx = float(dx) * cm
    dy = float(dy) * cm
    lx = float(lx) * cm    # odleglosc pola obciazenia do krawedzi plyty w kier. x
    ly = float(ly) * cm    # jw. w kier. y
    ad = float(ad) * cm
    asx = float(asx) * cm2
    asy = float(asy) * cm2    
    lambda_u = lambda_u     # wsp. uwzgledniajacy otwor w poblizu obwodu kontrolnego (%)  # TODO: to przypisanie jest tu bez sensu, ale zrobiłam tak, żeby był ślad po lambda_u 
    alfa = pi / 2 # kat miedzy zbrojeniem na scinanie i plaszczyzna plyty (zmienic na deg!!!!!!!!!!)    # TODO

    # -----------------------------------------
    # WARUNKI PRACY
    # TODO wszystko poniżej: musimy trzymać się konwencji pythonowych, nazwy zmiennych małą literą z podkreślnikami, jeśli chcemy coś oddzielić
    # Faktory
    if desit == 'trwała' or desit == 'przejściowa':
        gamma_c = 1.4
        gamma_s = 1.15
        alfa_cc = 1.0
    else:   # wyjątkowa
        gamma_c = 1.2
        gamma_s = 1.0
        alfa_cc = 1.0

    # Obciazenia
    ved = 600 * kN	# dodac komentarz, ze nie jest to reakcja, tylko sila tnaca z plyty na slup
                    # dla fundamentow mozna zredukowac sile do VEdred - por. 6.4.4(2)
    # med = 50 * kNm


    # ############## OBLICZENIA ##############
    # -----------------------------------------
    # MATERIAL
    fcd = alfa_cc * fck / gamma_c

    fyd = fyk / gamma_s
    fywd = alfa_sw * fyk


    # -----------------------------------------
    # GEOMETRIA
    d = (dx + dy) / 2 - ad	# spr. czy sie nie zgrywa z 'D' (srednica kola)

    # -> u0
    def u00(support):
        if support == 'słup wewnetrzny':
        # zrobic to na indeksach obiektow (1, 2, 3), zeby nie wpisywac w nieskonczonosc: wew., kraw. etc. (ryzyko pomylki)
            return 2 * (cx + cy)
        elif support == 'słup krawędziowy':   # Poprawic, poki co jest roboczo !!!
            return min(2 * cx + cy, cy + 3 * d)
        #elif support == 'słup krawędziowy X':
        #    return min(2 * cx + cy, cy + 3 * d)
        #elif support == 'słup krawędziowy Y':
        #    return min(cx + 2 * cy, cx + 3 * d) 
        elif support == 'słup narożny':
            return min(cx + cy, 3 * d)
        else:
            errors.append('Blad w okresleniu polozenia slupa.')

    '''if ColPos == 'wewnetrzny':			# uzyc 'case'
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
        print('Blad w okresleniu polozenia slupa.') '''

    u0 = lambda_u * u00(support)

    # -> u1
    def u11(support):
        if support == 'słup wewnętrzny':
        # zrobic to na indeksach obiektow (1, 2, 3), zeby nie wpisywac w nieskonczonosc: wew., kraw. etc. (ryzyko pomylki)
            return 2 * cx + 2 * cy + 4 * pi * d
        if support == 'słup krawędziowy':   # Poprawic, poki co jest roboczo !!!
            return 2 * cx + 1 * cy + 2 * pi * d + 2 * lx
        # elif support == 'słup krawędziowy X':
        #     return 2 * cx + 1 * cy + 2 * pi * d + 2 * lx
        # elif ColPos == 'słup krawędziowy Y':
        #     return 1 * cx + 2 * cy + 2 * pi * d + 2 * ly 
        elif support == 'słup narożny':
            return 1 * cx + 1 * cy + 1 * pi * d + lx + ly
        else:
            errors.append('Blad w okresleniu polozenia slupa.')   
    '''if ColPos == 'wewnetrzny':
    # zrobic to na indeksach obiektow (1, 2, 3), zeby nie wpisywac w nieskonczonosc: wew., kraw. etc. (ryzyko pomylki)
        u1 = 2 * cx + 2 * cy + 4 * pi * d
    if ColPos == 'krawedziowy X':
        u1 = 2 * cx + 1 * cy + 2 * pi * d + 2 * lx
    if ColPos == 'krawedziowy Y':
        u1 = 1 * cx + 2 * cy + 2 * pi * d + 2 * ly
    if ColPos == 'narozny':
        u1 = 1 * cx + 1 * cy + 1 * pi * d + lx + ly '''

    u1 = lambda_u * u11(support)


    # -----------------------------------------
    # NAPREZENIA
    # Maksymalne naprezenie przy przebiciu (vEd)
    '''if ColPos == 'wewnetrzny':
        beta = 1.15
    if ColPos == 'krawedziowy X':
        beta = 1.4
    if ColPos == 'krawedziowy Y':
        beta = 1.4
    if ColPos == 'narozny':
        beta = 1.5 '''
    '''def beta(ColPos):	# okreslic dokladnie wg wzorow !!!!!!!!!!!!!!!!
        if ColPos == 'wewnetrzny':
            return 1.15
        if ColPos == 'krawedziowy X':
            return 1.4
        if ColPos == 'krawedziowy Y':
            return 1.4
        if ColPos == 'narozny':
            return 1.5	'''
    ved0 = beta * ved * (u0 * d)
    ved1 = beta * ved * (u1 * d)

    # Maksymalna wytrzymalosc na scinanie przy przebiciu ze wzgledu na sciskane krzyzulce betonowe (vRdmax)
    ni = 0.6 * ( 1.0 - fck / (250 * MPa) )
    vrdmax = 0.4 * ni * fcd

    if vrdmax >= ved0:
        errors.append('Nosnosc betonu na scinanie przy przebiciu zachowana (vEd0 <= vRdmax).')
        print('Nosnosc betonu na scinanie przy przebiciu zachowana (vEd0 <= vRdmax).')
    else:   # elif vrdmax < ved0:
        errors.append('Nosnosc betonu na scinanie przekroczona (vEd0 > vRdmax)!')
        print('Nosnosc betonu na scinanie przekroczona (vEd0 > vRdmax)!')

    # Nosnosc na scinanie przy przebiciu bez zbrojenia na przebicie (vRdc)
    crdc = 0.18 / gamma_c
    k = min( 1.0 + (200 * mm / d)**0.5, 2.0 )
    ro_lx = asx / ( (cy + 6 * d) * d )
    ro_ly = asy / ( (cx + 6 * d) * d )
    ro_l = min( (ro_lx * ro_ly)**0.5, 0.02 )
    vmin = 0.035 * k**(3/2) * (fck / MPa)**0.5 * MPa
    k1 = 0.1
    sigma_cp = 0.0 * MPa		# rozwinac !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    vrdc = max( crdc * k * (100 * ro_l * fck / MPa)**(1/3) * MPa + k1 * sigma_cp, vmin + k1 * sigma_cp )


    # -----------------------------------------
    # ZBROJENIE

    if vrdc >= ved1:
        errors.append('Nosnosc na scinanie przy przebiciu zachowana (vEd1 <= vRdc).')
        print('Nosnosc na scinanie przy przebiciu zachowana (vEd1 <= vRdc).')
        asw_req = 0.0
        nsw_req = 0.0
    else:   # elif vRdc < vEd1:
        errors.append('Nosnosc na scinanie przekroczona (vEd1 > vRdc)!')
        print('Nosnosc na scinanie przekroczona (vEd1 > vRdc)!')
        # Obliczenie zbrojenia wymaganego wg Nosnosci na scinanie przy przebiciu ze zbrojeniem na przebicie (vRdcs)
        sr_max = 0.75 * d 	# promieniowy rozstaw strzemion
        fywd_ef = max( (250 + 0.25 * d / mm) * MPa, fywd )
        asw_req = (ved1 - 0.75 * vrdc) * sr_max / (1.5 * d) * u1 * d / ( fywd_ef * math.sin(alfa) )
        asw_1bar = pi * dsw**2 / 4
        nsw_req = asw_req / asw_1bar

        # Zbrojenie minimalne
        ro_sw_min = 0.08 * (fck / MPa)**0.5 * MPa / fyk
        st_max = 2.0 * d 	# styczny rozstw strzemion
        asw_min = ro_sw_min * sr_max * st_max / ( 1.5 * math.sin(alfa) + math.cos(alfa) )	# czy aby poprawna intepretacja pola jedengo ramienia strzemion??????
        nsw_min = asw_min / asw_1bar

        # Przyjecie zbrojenia
        nsw_prov = math.ceil( max(nsw_req, nsw_min) )
        asw_prov = nsw_prov * asw_1bar

        # Nosnosc na scinanie przy przebiciu ze zbrojeniem na przebicie (vRdcs)
        vrdcs = 0.75 * vrdc + 1.5 * d / sr_max * asw_prov * fywd_ef / (u1 * d) * math.sin(alfa)

        if vrdcs >= ved1:
            errors.append('Nosnosc na scinanie przy przebiciu zachowana (vEd1 <= vRdcs).')
            print('Nosnosc na scinanie przy przebiciu zachowana (vEd1 <= vRdcs).')
        else:   # elif vrdcs < ved1:
            errors.append('Nosnosc na scinanie przekroczona (vEd1 > vRdcs)!')
            print('Nosnosc na scinanie przekroczona (vEd1 > vRdcs)!')

        # Rozmieszczenie zbrojenia
            # Co najmniej 2 obwody strzemin
            # Max rozstaw obwodow 0.75d
            # Max rozstaw strzemion w obwodzie 2d (1.5d dla u1)
  
        u_out = beta * ved / (vrdc * d)

        # -> rout
    def a_out1(support):
        if support == 'słup wewnętrzny':
            return ( u_out - (2 * cx + 2 * cy) ) / (2 * pi)
        elif support == 'słup krawędziowy':
        # Poprawic, poki co jest roboczo !!!
            return ( u_out - (2 * cx + 1 * cy + 2 * lx) ) / (pi)
        elif support == 'słup narożny':
            return ( u_out - (1 * cx + 1 * cy + lx + ly) ) / (0.5 * pi)
        else:
            errors.append('Blad w okresleniu umax.') 

        '''if support == 'słup wewnętrzny':
            a_out = ( u_out - (2 * cx + 2 * cy) ) / (2 * pi)
        if support == 'słup krawędziowy':                           # Popawic !!!
            a_out = ( u_out - (2 * cx + 1 * cy + 2 * lx) ) / (pi)
        if support == 'krawedziowy X':
            a_out = ( u_out - (2 * cx + 1 * cy + 2 * lx) ) / (pi)
        if support == 'krawedziowy Y':
            a_out = ( u_out - (1 * cx + 2 * cy + 2 * ly) ) / (pi)
        if support == 'narozny':
            a_out = ( u_out - (1 * cx + 1 * cy + lx + ly) ) / (0.5 * pi) '''
    a_out = a_out1(support)

    # TODO: do zrobienia powyżej, natomiast poniżej do sprawdzenia, czy jest ok
    vrdc = asw_prov / cm / cm
    vrdmax = asx / cm / cm
    return vrdc, vrdmax, errors