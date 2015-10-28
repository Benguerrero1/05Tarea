# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 19:41:28 2015
Este programa calcula el potencial dentro de una caja de 10x15
que contiene la letra "B" que tiene una carga de 1[C],
usando la ecuación de Poisson.
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import pdb

L_x = 10
L_y = 15
h = 0.2

def crear_caja(x, y, h):
    '''Recibe las dimensiones de la caja  y el tamaño del reticulado
     y la inicia en ceros '''
    ancho_efectivo = x / h + 1
    largo_efectivo = y / h + 1
    caja = np.zeros((ancho_efectivo, largo_efectivo))

    return caja

def poner_condiciones_borde(caja):
    '''Conecta a tierra el perímetro de la caja, la segunda iteración
    (bordes laterales) se itera desde borde+1, hasta borde para evitar pasar
    2 veces por las esquinas'''
    borde_inferior = np.array([np.array([-5, -7.5]), np.array([5, -7.5])])
    borde_superior = np.array([np.array([-5, 7.5]), np.array([5, 7.5])])
    borde_inferior[0] = transformar(borde_inferior[0])
    borde_inferior[1] = transformar(borde_inferior[1])
    borde_superior[0] = transformar(borde_superior[0])
    borde_superior[1] = transformar(borde_superior[1])
    for i in range(int(borde_inferior[0][0]), int(borde_inferior[1][0]) + 1):
        caja[i, borde_inferior[0][1]] = 0
        caja[i, borde_superior[0][1]] = 0
    for i in range(int(borde_inferior[0][1])+1, int(borde_superior[0][1])):
        caja[borde_inferior[0][0], i] = 0
        caja[borde_superior[1][0], i] = 0
    return caja
    
def transformar(coordenada):
    ''' Recibe coordenadas considerando 0,0 como el centro y
    las dimensiones originales en centímetros, a las unidades de la grilla
     (Notar que se utiliza Ancho+1 porque el arreglo se define desde 0)'''

    x, y = coordenada[0], coordenada[1]
    x_tran = int((x + (L_x)/2)/h)
    y_tran = int((y + (L_y)/2)/h)
    return x_tran, y_tran
    
def es_horizontal(ini, fin):
        '''Retorna true si el trazo es horizontal, false si es vertical'''
        return (ini[1] == fin[1])


def trazo(ini, fin, ancho):
    '''Recibe la coordenada de inicio del trazo, el final y el ancho del
    trazo, devuelve un arreglo con las coordenadas de los puntos que lo
    conformman. Sólo funciona para trazos rectos.
    (recibe los puntos más izquierdos, o más  abajo del trazo)'''
    ancho = int(ancho)+1
    actual = ini
    if es_horizontal(ini, fin):
        paso = np.array([1, 0])
        ancho_1 = np.array([0, 1])
        rango = int(np.fabs(fin[0]-ini[0]))+1
    else:
        paso = np.array([0, 1])
        ancho_1 = np.array([1, 0])
        rango = int(np.fabs(fin[1]-ini[1]))

    trazo = np.zeros([(rango)*(ancho), 2])
    for a in range(ancho):
        for i in range(rango):
            trazo[i+(rango)*a] = np.array([actual])
            actual += paso
        actual = ini
        actual += (a+1)*ancho_1
    
    return trazo


def dentro_letra_B(x, y):
    '''Devuelve True si la coordenada está dentro del bloque que contiene
    la letra'''
    if (2.5 / h <= x and x <= 7.5 / h):
        if(4 / h <= y and y <= 11 / h):
            return True
    return False
    
def armar_letra_B():
    '''Devuelve el arreglo de coordenaas que conforman la letra B, las coordenadas
     ini y fin se dan considerando 0,0 en el centro y
     las dimensiones en centímetros'''
    ancho = 1
    ini = np.array([-2.5, -3.5])
    fin = np.array([-2.5, 3.5])
    ini2 = np.array([-1.5, 2.5])
    fin2 = np.array([1.5, 2.5])
    ini3 = np.array([-1.5, -0.5])
    fin3 = np.array([1.5, -0.5])
    ini4 = np.array([-1.5, -3.5])
    fin4 = np.array([1.5, -3.5])
    ini5 = np.array([1.5, 0.5])
    fin5 = np.array([1.5, 2.5])
    ini6 = np.array([1.5, -2.5])
    fin6 = np.array([1.5, -0.5])

    ancho_transf = ancho / h
    ini, fin = transformar(ini), transformar(fin)
    ini2, fin2 = transformar(ini2), transformar(fin2)
    ini3, fin3 = transformar(ini3), transformar(fin3)
    ini4, fin4 = transformar(ini4), transformar(fin4)
    ini5, fin5 = transformar(ini5), transformar(fin5)
    ini6, fin6 = transformar(ini6), transformar(fin6)

    trazo_1 = trazo(ini, fin, ancho_transf)
    trazo_2 = trazo(ini2, fin2, ancho_transf)
    trazo_3 = trazo(ini3, fin3, ancho_transf)
    trazo_4 = trazo(ini4, fin4, ancho_transf)
    trazo_5 = trazo(ini5, fin5, ancho_transf)
    trazo_6 = trazo(ini6, fin6, ancho_transf)
    letra = np.append(trazo_1, trazo_2, axis=0)
    letra = np.append(letra, trazo_3, axis=0)
    letra = np.append(letra, trazo_4, axis=0)
    letra = np.append(letra, trazo_5, axis=0)
    letra = np.append(letra, trazo_6, axis=0)
    return letra


def Iteracion(V, V_next, N_pasos_x, N_pasos_y, h, w):
    for i in range(1, N_pasos_x-1):
        for j in range (1, N_pasos_y-1):
            V_next[i, j] = ((1 - w) * V[i, j] +
                            w / 4 * (V[i+1, j] + V[i-1, j]
                                    + V[i, j+1] + V[i, j-1] + 
                                    h**2 * rho(i, j, h)))

def no_converge(V, V_next, tolerancia=1e-7):
    ''' Devuelve True si es que la iteracion converge'''
    not_zero = (V_next != 0)
    diff_relativa = (V - V_next)[not_zero] / V_next[not_zero]
    max_diff = np.max(np.fabs(diff_relativa))
    if max_diff > tolerancia:
        return True
    else:
        return False

#Main

#Inicializacion

N_pasos_x = (L_x / h) + 1
N_pasos_y = (L_y / h) + 1

V = np.zeros((N_pasos_x, N_pasos_y))
V_next = np.zeros((N_pasos_x, N_pasos_y))

#Iteracion

Iteracion(V, V_next, N_pasos_x, N_pasos_y, h, w)
contador = 1
while contador < 900 or no_converge(V, V_next, tolerancia=1e-7):
    V = V_next.copy()
    Iteracion(V, V_next, N_pasos_x, N_pasos_y, h, w)
    contador += 1
    
