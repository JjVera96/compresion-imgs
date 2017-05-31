from PIL import Image

image = Image.open("ejemplo.jpg")
ancho, altura = image.size
pixels = image.load()
print(ancho, altura)