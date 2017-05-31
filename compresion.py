from scipy.fftpack import fft, ifft   
import numpy as np
from PIL import Image, ImageDraw,ImageFont
import os

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
