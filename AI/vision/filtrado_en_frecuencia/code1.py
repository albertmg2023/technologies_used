

import skimage as ski
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.fft as fft

MASK_SIZE = 31
STD_DEV=5
imagen = ski.io.imread("images/boat.511.tiff")
imagen = ski.util.img_as_float(imagen)

# Convolución Gaussiana en el espacio
vector = scipy.signal.windows.gaussian(MASK_SIZE, STD_DEV)  # Máscara de NxN toda con 1
vector /= np.sum(vector)  # Máscara normalizada
vectorH = vector.reshape(1, MASK_SIZE)
vectorV = vector.reshape(MASK_SIZE, 1)
matriz = vectorV @ vectorH
res_convolG = scipy.ndimage.convolve(imagen, matriz)

# Ampliamos la máscara Gausiana con ceros para que tenga el mismo tamaño que la imagen
mascara_centradaG = np.zeros(imagen.shape)
fila_i = imagen.shape[0] // 2 - MASK_SIZE // 2
col_i = imagen.shape[1] // 2 - MASK_SIZE // 2
mascara_centradaG[fila_i:fila_i + MASK_SIZE, col_i:col_i + MASK_SIZE] = vector

# Convolución Media en el espacio
mascara = np.ones((MASK_SIZE, MASK_SIZE))  # Máscara de NxN toda con 1
mascara /= np.sum(mascara)  # Máscara normalizada
res_convolM = scipy.ndimage.convolve(imagen, mascara, mode="wrap")

# Ampliamos la máscara Media con ceros para que tenga el mismo tamaño que la imagen
mascara_centradaM = np.zeros(imagen.shape)
fila_i = imagen.shape[0] // 2 - MASK_SIZE // 2
col_i = imagen.shape[1] // 2 - MASK_SIZE // 2
mascara_centradaM[fila_i:fila_i + MASK_SIZE, col_i:col_i + MASK_SIZE] = mascara


# Pasamos imagen y máscaras a las frecuencias
FTimagen = fft.fft2(imagen)

mascara_en_origenG = fft.ifftshift(mascara_centradaG)
FTmascaraG = fft.fft2(mascara_en_origenG)

mascara_en_origenM = fft.ifftshift(mascara_centradaM)
FTmascaraM = fft.fft2(mascara_en_origenM)

# Convolución Gausiana en la frecuancia
FTimagen_filtradaG = FTimagen * FTmascaraG  # Producto punto a punto
FTimagen_filtradaM = FTimagen * FTmascaraM

# Recuperamos resultado en el espacio

#DEL FILTRO GAUSSIANO

res_filtro_FTG = fft.ifft2(FTimagen_filtradaG)
res_filtro_realG = np.real(res_filtro_FTG)
res_filtro_imagG = np.imag(res_filtro_FTG)

#DEL FILTRO MEDIA

res_filtro_FTM = fft.ifft2(FTimagen_filtradaM)
res_filtro_realM = np.real(res_filtro_FTM)
res_filtro_imagM = np.imag(res_filtro_FTM)



#MAGNITUDES DE LAS TRANSFORMADAS DEL FILTRO GAUSSIANO
magnitud_imagen = fft.fftshift(np.log(np.absolute(FTimagen) + 1))
magnitud_mascaraG = fft.fftshift(np.log(np.absolute(FTmascaraG) + 1))
magnitud_productoG = fft.fftshift(np.log(np.absolute(FTimagen_filtradaG) + 1))

#MAGNITUDES DE LAS TRANSFORMADAS DEL FILTRO MEDIA

magnitud_mascaraM = fft.fftshift(np.log(np.absolute(FTmascaraM) + 1))
magnitud_productoM = fft.fftshift(np.log(np.absolute(FTimagen_filtradaM) + 1))

# Visulización de resultados

fig, axs = plt.subplots(3, 5, layout="constrained")

axs[0, 0].set_title("imagen original")
axs[0, 1].set_title("Máscara Gausiana en espacio")
axs[0, 2].set_title("Result filtro Gausiano")
axs[0, 3].set_title("Máscara Media en espacio")
axs[0, 4].set_title("Result filtro Media")

axs[1, 0].set_title("Magnitud imagen ")
axs[1, 1].set_title("Máscara Gausiana en frecuencia")
axs[1, 2].set_title("Magnitud imagen filtrada")
axs[1, 3].set_title("Máscara Media en frecuencia")
axs[1, 4].set_title("Magnitud imagen filtrada")

axs[0, 0].imshow(imagen, cmap=plt.cm.gray)
axs[0, 1].imshow(mascara_centradaG, cmap=plt.cm.gray)
axs[0, 2].imshow(res_filtro_realG, cmap=plt.cm.gray)
axs[0, 3].imshow(mascara_centradaM, cmap=plt.cm.gray)
axs[0, 4].imshow(res_filtro_realG, cmap=plt.cm.gray)


axs[1, 0].imshow(magnitud_imagen, cmap=plt.cm.gray)
axs[1, 1].imshow(magnitud_mascaraG, cmap=plt.cm.gray)
axs[1, 2].imshow(magnitud_productoG, cmap=plt.cm.gray)
axs[1, 3].imshow(magnitud_mascaraM, cmap=plt.cm.gray)
axs[1, 4].imshow(magnitud_productoM, cmap=plt.cm.gray)



for a in axs.ravel():
    a.set_axis_off()
plt.show()


#conclusión entre ejer 1y 2: A menor sea el tamaño de la máscara,
#el filtro gausiano y el filtro media tienen una magnitud más similar.
#En cambio cuando aumenta este tamaño,
#las magnitudes de ambos filtros no presentan tanta similitud.
