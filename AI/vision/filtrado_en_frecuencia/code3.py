

import skimage as ski
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.fft as fft

#EJ1

MASK_SIZE = 31
STD_DEV=5
imagen = ski.io.imread("images/boat.511.tiff")
imagen = ski.util.img_as_float(imagen)
imagen=imagen[0:101,0:101]

# Convolución Gaussiana en el espacio
vector = scipy.signal.windows.gaussian(MASK_SIZE, STD_DEV)  # Máscara de NxN toda con 1
vector /= np.sum(vector)  # Máscara normalizada
vectorH = vector.reshape(1, MASK_SIZE)
vectorV = vector.reshape(MASK_SIZE, 1)
matriz = vectorV @ vectorH
res_convolG = scipy.ndimage.convolve(imagen, matriz)

# Ampliamos la máscara Gausiana con ceros para que tenga el mismo tamaño que la imagen
mascara_centradaG1 = np.zeros(imagen.shape)
fila_i = imagen.shape[0] // 2 - MASK_SIZE // 2
col_i = imagen.shape[1] // 2 - MASK_SIZE // 2
mascara_centradaG1[fila_i:fila_i + MASK_SIZE, col_i:col_i + MASK_SIZE] = vector

#EJ2

MASK_SIZE = 5
STD_DEV=5

# Convolución Gaussiana en el espacio
vector = scipy.signal.windows.gaussian(MASK_SIZE, STD_DEV)  # Máscara de NxN toda con 1
vector /= np.sum(vector)  # Máscara normalizada
vectorH = vector.reshape(1, MASK_SIZE)
vectorV = vector.reshape(MASK_SIZE, 1)
matriz = vectorV @ vectorH
res_convolG = scipy.ndimage.convolve(imagen, matriz)

# Ampliamos la máscara Gausiana con ceros para que tenga el mismo tamaño que la imagen
mascara_centradaG2 = np.zeros(imagen.shape)
fila_i = imagen.shape[0] // 2 - MASK_SIZE // 2
col_i = imagen.shape[1] // 2 - MASK_SIZE // 2
mascara_centradaG2[fila_i:fila_i + MASK_SIZE, col_i:col_i + MASK_SIZE] = vector

#COGEMOS LA FILA QUE ESTÁ AL MEDIO DE LAS MÁSCARAS
print(np.shape(mascara_centradaG1),"C_G1")
numfilmedioG1=int((np.shape(mascara_centradaG1)[0])/2)
p_lin_cent_G1=mascara_centradaG1[numfilmedioG1,:]
print(np.shape(mascara_centradaG2),"C_G2")
numfilmedioG2=int((np.shape(mascara_centradaG2)[0])/2)
p_lin_cent_G2=mascara_centradaG2[numfilmedioG2,:]

# Visulización de resultados

fig, axs = plt.subplots(1, 2)
axs[0].imshow(imagen, cmap=plt.cm.gray)
axs[0].set_title("Imagen original",fontsize=20)
axs[0].set_axis_off()
axs[1].set_xlabel("posición")
axs[1].set_ylabel("valor línea central")
axs[1].plot(range(len(p_lin_cent_G1)),p_lin_cent_G1,label = "ej1 31x31 y std=5",color="red")
axs[1].plot(range(len(p_lin_cent_G2)),p_lin_cent_G2,label = "ej2 5x5 y std=5",color="blue")
axs[1].legend()

plt.show()
