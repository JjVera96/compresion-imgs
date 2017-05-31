from math import cos,sin,pi
from scipy.fftpack import dct,idct, fft, ifft   
import numpy as np
import random
from PIL import Image, ImageDraw,ImageFont
import os
from cdt import *


#Tamano de la imagen: Funcion que determina el tamano de la imagen original
def tamImage(imagen):
    tam = os.stat(imagen)
    return tam.st_size

#Funcion de carga la imagen desde el archivo
def cargarImage(imagen):
    image = Image.open(imagen)
    ancho, altura = image.size
    pixels = image.load()
    return ancho,altura,pixels,image

#Inicia el proceso de compreseion
def comprimir(imagen):
    ancho,altura,pixels,image = cargarImage(imagen) #Cargamos la imagen a gris
    i = 0
    j = 0
    print("Altura de la imagen: ", altura) #Nos da el alto de la imagen
    arreglo = []
    i = 0
    j = 0
    while i < altura: #Recorre la imagen (los bloques de 8 pixeles)
        while j < ancho:
            if ancho - j >= 8 and altura - i >= 8:
                mat = []
                for k in range(8): #Bloques de ocho pixeles
                    mat.append([])
                    for l in range(8):
                        mat[k].append(pixels[l+j,k+i][0]) #Guarda la matriz con lo nuevos valores
                mat = matrixTemporal(mat) #Llevamos la nueva matriz a la extension NUMPY para operar correctamente con ella
                mat = fft(mat) #Aplicamos la transformada a la matriz y le hacemos la cuantificacion
                conts = 0
                array = []
                for k in range(8):
                    for l in range(8):
                        if mat[k][l] != 0 and abs(mat[k][l]) < 1: #Se da un valor maximo y se modifica la matriz cuantificada
                            mat[k][l]  = 0.0
                            array.append(pixels[j+l,i+k][0])
                            conts += 1
                finaly = ifft(mat) #Se aplica LA INVERSA DELA TRANSFORMADA DEL DISCRETA DEL COSENO (DCT III)
                for k in range(8): #Dibujamos nuevamente la imagen
                    for l in range(8):
                        pixels[j+l,i+k] = (int(finaly[k][l]),int(finaly[k][l]),int(finaly[k][l]))
                j = j + 8
            else:
                j = j + 1
        i = i + 8
        j = 0
    nameimg, ext = imagen.split(".")
    nameimg = nameimg+"compresion.jpg"
    image.save(nameimg)  #RESULTADO FINAL DE LA COMPRESION
    return nameimg

#Menu para pedir la imagen que se desea comprimir
def main():
    imagen = input("Escriba el nombre de la imagen que desea comprimir (ejemplo: imagen.jpg): ")
    imgcompre =comprimir(imagen)
    original = tamImage(imagen)
    nueva = tamImage(imgcompre)
    print("Tamano de la imagen original : ", original, " bytes \nTamano de la imagen nueva : ", nueva, "bytes")
    print("Porcentaje de compresion de la imagen :",100.0 - (float(nueva)*100.0)/float(original),"%")
main()
