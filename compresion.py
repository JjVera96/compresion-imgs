from scipy.fftpack import fft, ifft, dct, idct
import numpy as np
from PIL import Image, ImageDraw,ImageFont
from time import time
import os

def matrixTemporal(matriz):
    a = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            a[i][j] = matriz[i][j] - 130.0
    return a

def tamImage(imagen):
    tam = os.stat(imagen)
    return tam.st_size

def cargarImage(imagen):
    try:
        image = Image.open(imagen)
        ancho, altura = image.size
        pixels = image.load()
        return ancho,altura,pixels,image
    except IOError:
        return None

def comprimirFFT(imagen):
    print("Inicia FFT")
    ti = time()
    ancho,altura,pixels,image = cargarImage(imagen) 
    arreglo = []
    i = 0
    j = 0
    while i < altura: 
        while j < ancho:
            if ancho - j >= 8 and altura - i >= 8:
                mat = []
                for k in range(8):
                    mat.append([])
                    for l in range(8):
                        mat[k].append(pixels[l+j,k+i][0])
                mat = matrixTemporal(mat) 
                mat = fft(mat) 
                conts = 0
                array = []
                for k in range(8):
                    for l in range(8):
                        if mat[k][l] != 0 and abs(mat[k][l]) < 1: 
                            mat[k][l]  = 0.0
                            array.append(pixels[j+l,i+k][0])
                            conts += 1
                finaly = ifft(mat) 
                for k in range(8): 
                    for l in range(8):
                        pixels[j+l,i+k] = (int(np.real(finaly[k][l])),int(np.real(finaly[k][l])),int(np.real(finaly[k][l])))
                j = j + 8
            else:
                j = j + 1
        i = i + 8
        j = 0
    nameimg, ext = imagen.split(".")
    nameimg = nameimg+"compressFFT.jpg"
    image.save(nameimg) 
    tf = time()
    print("Fin FFT\nTiempo Ejeucion", tf-ti, "segundos")
    return nameimg

def comprimirDCT(imagen):
    print("Inicia DCT")
    ti = time()
    ancho,altura,pixels,image = cargarImage(imagen)
    arreglo = []
    i = 0
    j = 0
    while i < altura: 
        while j < ancho:
            if ancho - j >= 8 and altura - i >= 8:
                mat = []
                for k in range(8): 
                    mat.append([])
                    for l in range(8):
                        mat[k].append(pixels[l+j,k+i][0]) 
                mat = matrixTemporal(mat) 
                mat = dct(mat) 
                conts = 0
                array = []
                for k in range(8):
                    for l in range(8):
                        if mat[k][l] != 0 and abs(mat[k][l]) < 1: 
                            mat[k][l]  = 0.0
                            array.append(pixels[j+l,i+k][0])
                            conts += 1
                finaly = idct(mat) 
                for k in range(8): 
                    for l in range(8):
                        pixels[j+l,i+k] = (int(finaly[k][l]),int(finaly[k][l]),int(finaly[k][l]))
                j = j + 8
            else:
                j = j + 1
        i = i + 8
        j = 0
    nameimg = imagen.split(".")
    nameimg = nameimg[0]+"compressCDT.jpg"
    image.save(nameimg)  
    tf = time()
    print("Fin DCT\nTiempo Ejeucion", tf-ti, "segundos")
    return nameimg

def main():
    imagen = input("Nombre Imagen(Salir, salir, SALIR para finalizar): ")
    while imagen != "Salir" and imagen != "salir" and imagen != "SALIR":        
        if cargarImage(imagen) != None:
            imgFFT = comprimirFFT(imagen)
            imgDCT = comprimirDCT(imagen)
            original = tamImage(imagen)
            nuevaFFT = tamImage(imgFFT)
            nuevaDCT = tamImage(imgDCT)
            print("Original : ", original, " bytes \nImagenFFT : ", nuevaFFT, "bytes\nImagenDCT : ", nuevaDCT, "bytes")
            print("Porcentaje Compresion FFT :",100.0 - (float(nuevaFFT)*100.0)/float(original),"%")
            print("Porcentaje Compresion DCT :",100.0 - (float(nuevaDCT)*100.0)/float(original),"%")
            print("-------------------------------------------------\n")
        else:
            print("No existe Imagen")
            print("-------------------------------------------------\n")
        imagen = input("Nombre Imagen: ")

if __name__ == '__main__':
    main()
