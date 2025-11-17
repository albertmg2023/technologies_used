# Objetivo:
# -Convolve (en 1D y en 2D)

import skimage as ski
import matplotlib.pyplot as plt
import numpy as np
import scipy
import time

def creaimpares(inicio_inclu,fin_inclu):
    impares=[]
    for i in range(inicio_inclu,fin_inclu+1):
        if(i%2!=0):
            impares.append(i)
    return impares
        

imagen = ski.io.imread("images/boat.512.tiff")
imagen = ski.util.img_as_float(imagen)


# Tiempos finales Media 2d
tiempos2D=[]

# Tiempos finales Media 1d

tiempos1D=[]

#PARA ALMACENAR 10 Tiempos y hacer la media de ellos
ts2D_prueba=[]
ts1D_prueba=[]

mean_sizes = creaimpares(3,21)
for i in range(len(mean_sizes)):

    tam=(mean_sizes[i],mean_sizes[i])
    vector=np.ones(tam)
    matriz=(1/((mean_sizes[i]*mean_sizes[i]))*vector)
    vectorH = (1/(mean_sizes[i]))*np.ones((1,mean_sizes[i]))
    vectorV = (1/(mean_sizes[i]))*np.ones((mean_sizes[i],1))
    """print(matriz,"vector entero")
    print(vectorH,"vectorH")
    print(vectorV,"vectorV")
    print(vectorV @ vectorH)"""

    #ConVolución 2d
    for j in range(10):
        inicio2D=time.time()

        res_convol2D = scipy.ndimage.convolve(imagen, matriz)

        fin2D=time.time()
        total2D=fin2D-inicio2D
        ts2D_prueba.append(total2D)
    
    tiempos2D.append(np.mean(ts2D_prueba))
    ts2D_prueba=[]
    #ConVolución 1d
    for j in range(10):

        inicio1D=time.time()
        resH = scipy.ndimage.convolve(imagen, vectorH)
        res1D = scipy.ndimage.convolve(resH, vectorV)
        fin1D=time.time()
        
        total1D=fin1D-inicio1D
        ts1D_prueba.append(total1D)
    
    tiempos1D.append(np.mean(ts1D_prueba))
    ts1D_prueba=[]



fig, axs = plt.subplots(1, 2)
axs[0].imshow(imagen, cmap=plt.cm.gray)
axs[0].set_title("Imagen original",fontsize=20)
axs[0].set_axis_off()
axs[1].set_xlabel("Tamaño de máscara")
axs[1].set_ylabel("Tiempo de ejecución")
axs[1].plot(mean_sizes,tiempos2D,label = "tiempos_conv_2D")
axs[1].plot(mean_sizes,tiempos1D,label = "tiempos_conv_1D")
axs[1].legend()

plt.show()
