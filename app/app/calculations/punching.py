#!/usr/bin/env python
# encoding: utf-8

from math import pi, sin, cos, ceil

from .consts import *


ERRORS = []     # lista bledow
INFO = []       # lista sprawdzenia warunkow nosnosci


def compute_design_situation(design_situation_id):
    if design_situation_id in [0, 1]: # 'trwała' (0) lub 'przejściowa' (1)
        gamma_c = 1.4
        gamma_s = 1.15
        alfa_cc = 1.0
    elif design_situation_id == 2:    # 'wyjątkowa'
        gamma_c = 1.2
        gamma_s = 1.0
        alfa_cc = 1.0
    else:
        gamma_c = 0.0
        gamma_s = 0.0
        alfa_cc = 0.0
        ERRORS.append('Błąd w określeniu sytuacji obliczeniowej.')
    return gamma_c, gamma_s, alfa_cc


def compute_u0(support_id, cx, cy, d):
    # TODO(LZ): Dodac warunek na section i powiazac support
    # TODO: ściana - naroże (3) i ściana - koniec (4)
    if support_id == 0:     # słup wewnętrzny
        u00 = 2 * (cx + cy)
    elif support_id == 1:   # słup krawędziowy X
        u00 = min(2 * cx + cy, cy + 3 * d)
    elif support_id == 2:   # słup krawędziowy Y
        u00 = min(cx + 2 * cy, cx + 3 * d)
    elif support_id == 3:   # słup narożny
        u00 = min(cx + cy, 3 * d)
    elif support_id == 4:   # ściana - naroże
        u00 = 100           # TODO(LZ): poprawic!
        ERRORS.append("Podpora 'ściana-naroże' niedostępna.")
    elif support_id == 5:   # ściana - koniec
        u00 = 200           # TODO(LZ): poprawic!
        ERRORS.append("Podpora 'ściana-koniec' niedostępna.")
    else:
        # TODO(LZ): dodac sciany (naroznik, koniec)
        u00 = 0.0
        ERRORS.append('Błąd w określeniu położenia podpory (u0).')
    return u00


def compute_u1(support_id, cx, cy, d, lx, ly):
    a1 = 2*d
    if support_id == 0:     # slup wewnetrzny
        u11 = 2 * cx + 2 * cy + 2 * pi * a1
    elif support_id == 1:   # słup krawędziowy X
        u11 = 2 * cx + 1 * cy + 1 * pi * a1 + 2 * lx
    elif support_id == 2:   # słup krawędziowy Y
        u11 = 1 * cx + 2 * cy + 1 * pi * a1 + 2 * ly
    elif support_id == 3:   # słup narożny
        u11 = 1 * cx + 1 * cy + 0.5 * pi * a1 + lx + ly
    elif support_id == 4:   # ściana - naroże
        u11 = 100           # TODO(LZ): poprawic!
        ERRORS.append("Podpora 'ściana-naroże' niedostępna.")
    elif support_id == 5:   # ściana - koniec
        u11 = 200           # TODO(LZ): poprawic!
        ERRORS.append("Podpora 'ściana-koniec' niedostępna.")
    else:
        u11 = 0.0
        ERRORS.append('Błąd w określeniu położenia podpory (u1).')
    return u11


def compute_a_out(support_id, cx, cy, lx, ly, u_out):
    if support_id == 0:     # slup wewnetrzny
        a_out = (u_out - (2 * cx + 2 * cy)) / (2 * pi)
    elif support_id == 1:   # słup krawędziowy X
    # TODO(LZ): Poprawic dla innych przekrojow; poki co jest roboczo !!!
        a_out = (u_out - (2 * cx + 1 * cy + 2 * lx)) / pi
    elif support_id == 2:   # słup krawędziowy Y
        a_out = (u_out - (1 * cx + 2 * cy + 2 * ly)) / pi
    elif support_id == 3:   # słup narożny
        a_out = (u_out - (1 * cx + 1 * cy + lx + ly)) / (0.5 * pi)
    elif support_id == 4:   # ściana - naroże
        a_out = 100         # TODO(LZ): poprawic!
        ERRORS.append("Podpora 'ściana-naroże' niedostępna.")
    elif support_id == 5:   # ściana - koniec
        a_out = 200         # TODO(LZ): poprawic!
        ERRORS.append("Podpora 'ściana-koniec' niedostępna.")
    else:
        ERRORS.append('Błąd w określeniu odległości a.out.')
        a_out = 0.0
    return a_out

# def compute _ui(u0, u1):  # TODO(LZ): rozwinac w funckje obl. poszczegolne obowdy kontrolne (u.i)
#     ui = []
    # while ui <= u_out:
    #     pass
    #     ui.append()
    # podobnie ai - odl. poszczegolnych obwodow


def compute_punching(c_class, s_class, dsw, support, section, b, h, dx, dy, lx,
                     ly, ad, lambda_u, asx, asy, design_situation, ved, beta):
    """
    Procedura sprawdzenia nośności na przebicie płyty betonowej wg PN-EN 1992-1

    :param c_class:     # TODO(LZ): opisac def parametrow wejsciowych i co otrzymujemy na wyniku 
    :param s_class:
    :param dsw:
    :param support:
    :param section:
    :param b:
    :param h:
    :param dx:
    :param dy:
    :param lx:
    :param ly:
    :param ad:
    :param lambda_u:
    :param asx:
    :param asy:
    :param design_situation:
    :param ved:
    :param beta:
    :return:
    
    """

    # -----------------------------------------
    # MATERIAL
    # Beton
    fck = c_tab[c_class.type] * MPa
    # Stal
    fyk = s_tab[s_class.type] * MPa
    alfa_sw = 0.8   # TODO(LZ): redukcja wytrzymalosci zbr. na ścinanie, do namyslu jak to ustalac
    
    # -----------------------------------------
    # GEOMETRIA
    # Element = 'plyta'   # do wyboru: plyta, stopa fundamentowa TODO
    cx = float(b) *cm     # cx = 40.0 * cm
    cy = float(h) *cm     # cy = 40.0 * cm
    #cxy = 40.0 * cm	  # TODO(LZ): dla przekroju kolowego
    dsw = dsw.value *mm   # srednica zbrojenia na ścinanie
    dx = float(dx) *cm
    dy = float(dy) *cm
    lx = float(lx) *cm    # odleglosc pola obciazenia do krawedzi plyty w kier. x
    ly = float(ly) *cm    # jw. w kier. y
    ad = float(ad) *cm
    asx = float(asx) *cm2
    asy = float(asy) *cm2    
    alfa = pi / 2     # = 90deg, kat miedzy zbrojeniem na ścinanie i plaszczyzna plyty

    # -----------------------------------------
    # WARUNKI PRACY
    # Faktory
    gamma_c, gamma_s, alfa_cc = compute_design_situation(design_situation.id)

    # Obciazenia
    beta = float(beta)
    ved = float(ved) *kN  # 600.0 *kN	# sila tnaca oddzialywujaca z plyty na slup, NIE jest to reakcja na slup!!!
                    # dla fundamentow mozna zredukowac sile do VEdred - por. 6.4.4(2)

    # ############## OBLICZENIA ##############
    # -----------------------------------------
    # MATERIAL
    fcd = alfa_cc * fck / gamma_c
    fyd = fyk / gamma_s
    fywd = alfa_sw * fyd

    # -----------------------------------------
    # GEOMETRY
    d = (dx + dy) / 2 - ad  # spr. czy sie nie koliduje z 'D' (srednica kola)

    u00 = compute_u0(support.id, cx, cy, d)
    u11 = compute_u1(support.id, cx, cy, d, lx, ly)
    u0 = (1.0 - lambda_u / 100) * u00
    u1 = (1.0 - lambda_u / 100) * u11

    # -----------------------------------------
    # NAPREZENIA
    # Maksymalne naprezenie przy przebiciu (vEd)
    ved0 = beta * ved * (u0 * d)
    ved1 = beta * ved * (u1 * d)

    # Maksymalna wytrzymalosc na ścinanie przy przebiciu ze wzgledu na sciskane krzyzulce betonowe (vRdmax)
    ni = 0.6 * (1.0 - fck / (250 * MPa))
    vrdmax = 0.4 * ni * fcd

    if vrdmax >= ved0:
        INFO.append('Nośność betonu na ścinanie przy przebiciu zachowana '
                    '(vEd0 <= vRdmax).')
    else:   # elif vrdmax < ved0:
        ERRORS.append('Nośność betonu na ścinanie przekroczona '
                      '(vEd0 > vRdmax)!')

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
    # Zbrojenie minimalne
    ro_sw_min = 0.08 * (fck / MPa)**0.5 * MPa / fyk
    sr_max = 0.75 * d   # promieniowy rozstaw strzemion
    st_max = 2.0 * d    # styczny rozstaw strzemion
    st1_max = 1.5 * d   # TODO(LZ): do opracowanie pozniej dla obwodu u1
    asw_min = ro_sw_min * sr_max * st_max / (1.5 * sin(alfa) + cos(alfa))   # czy aby poprawna intepretacja pola jedengo ramienia strzemion??????
    asw_1bar = pi * dsw**2 / 4
    # ZBROJENIE wymagane (req)
    if vrdc >= ved1:
        INFO.append('Nośność na ścinanie przy przebiciu zachowana '
                    '(vEd1 <= vRdc).')
        asw_req = vrdcs = 0.0
        asw_prov = ceil(max(asw_req, asw_min) / asw_1bar)
    else:   # elif vRdc < vEd1:
        ERRORS.append('Nośność na ścinanie przekroczona (vEd1 > vRdc)!')
        # Obliczenie zbrojenia wymaganego wg Nośności na ścinanie przy przebiciu ze zbrojeniem na przebicie (vRdcs)
        sr_max = 0.75 * d 	# promieniowy rozstaw strzemion
        fywd_ef = max((250 + 0.25 * d / mm) * MPa, fywd)
        asw_req = (ved1 - 0.75 * vrdc) * sr_max / (1.5 * d) * u1 * d / \
                  (fywd_ef * sin(alfa))

        # Rozmieszczenie zbrojenia (prov)

        nsw_prov = ceil(max(asw_req, asw_min) / asw_1bar)
        asw_prov = nsw_prov * asw_1bar
        ssw = 0.0  # TODO(LZ): rozstaw zbr. na obwodach, do opracowania

        # Nośność na ścinanie przy przebiciu ze zbrojeniem na przebicie (vRdcs)
        vrdcs = 0.75 * vrdc + 1.5 * d / sr_max * asw_prov * fywd_ef / \
                              (u1 * d) * sin(alfa)
        if vrdcs >= ved1:
            INFO.append('Nośność na ścinanie przy przebiciu zachowana '
                        '(vEd1 <= vRdcs).')
        else:   # elif vrdcs < ved1:
            ERRORS.append('Nośność na ścinanie przekroczona (vEd1 > vRdcs)!')



            # Co najmniej 2 obwody strzemin
            # Max rozstaw obwodow 0.75d
            # Max rozstaw strzemion w obwodzie 2d (1.5d dla u1)
  
    u_out = beta * ved / (vrdc * d)
    a_out = compute_a_out(support.id, cx, cy, lx, ly, u_out)
    # TODO(LZ): rozstaw strzemion - rozstaw obwodow i strzemion na obwodach

    return (vrdc, vrdmax, vrdcs, ERRORS, INFO)
        # TODO(LZ): poprawic wyniki na ui, ai etc.,
        # dodac wyniki u1, a_out, vrdc, vrdmax, vrdcs, asw_req, asw_min, ssw_prov, nsw_prov


