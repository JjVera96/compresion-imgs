from math import cos,sin,pi    #Importamos funciones trigonometricas

'''Scipy es una libreria cientifica de python que saca directamente la Transformada de coseno discreta(DCT): '''
from scipy.fftpack import dct,idct

'''Numpy es una extension de Python que le agrega mayor soporte para vectores y matrices y las operaciones entre ellos:'''
import numpy as np
import random

'''Este modulo se usa para crear nuevas imagenes, retocar imagenes existentes y para generar graficos principalmente en 2D '''
from PIL import Image, ImageDraw,ImageFont
import os
from cdt import *

'''Algoritmo para hacer la compresion de la imagen:
 1. Pasar la imagen original a escala de grises.
 2. Luego dividir la imagen por cuadros de 8 pixeles cada uno (en el documento esta explicada esta parte).
 3. Y finalmente aplicar y obtener la transformada de coseno discreta por cada uno de los bloques: En este proceso se hace:
     3.1. Sacar la matriz.
     3.2. Definir el tipo de DCT que se usara (CDT I, CDT II y CDT III)).
     3.3. Definir la longitud de la transformada en este caso dejamos que la libreria use la estandar.
     3.4. Definir el eje en que se realizara la transformada
     3.5. Hacer la normalizacion.
'''


matriz = [(49,57,34,31,33,28,14,29),
          (20,24,21,20,17,16,18,22),
          (19,20,22,16,12,14,14,35),
          (17,18,16,15,13,22,25,68),
          (47,27,32,26,7,28,46,54),
          (71,46,45,60,24,38,65,37),
          (70,86,37,52,57,53,29,96),
          (66,84,80,44,29,40,93,175)]

#Matriz cuantificada: Se saca para saber que tanta calidad necesitamos reducir a la imagen
Q= [(16,11,10,16,24,40,51,61),
    (12,12,14,19,26,58,60,55),
    (14,13,16,24,40,57,69,56),
    (14,17,22,29,51,87,80,62),
    (18,22,37,56,68,109,103,77),
    (24,35,55,64,81,104,113,92),
    (49,64,78,87,103,121,120,101),
    (72,92,95,98,112,100,103,99)]

qa = np.zeros((8,8))
for i in range(8):
    for j in range(8):
        qa[i][j] = Q[i][j]

#Funcion que crea una matriz temporal
def matrixTemporal(matriz):
    a = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            a[i][j] = matriz[i][j] - 128.0
    return a

#Funcion que saca la TRANSFORMADA DISCRETA DEL COSENO (En este caso la CDT II)
def CDT(a):
    global qa
    b = dct(a,type=2,n=None,axis=-1,norm='ortho',overwrite_x=False) #CDT a la matriz
    c = idct(b, type=2, n=None, axis=-1, norm='ortho', overwrite_x=False) #CDT inversa
    F = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            F[i][j] = b[i][j]/qa[i][j]
    return F

#Funcion que hace LA INVERSA DE LA TRANSFORMADA
def InversaCDT(mat):
    global qa
    new = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            new[i][j] = mat[i][j]*qa[i][j]
    c = idct(new, type=2, n=None, axis=-1, norm='ortho', overwrite_x=False)

    for i in range(8):
        for j in range(8):
            c[i][j] = c[i][j] + 128
    return c
