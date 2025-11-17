
import skimage as ski
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.fft as fft
import time

def creaimpares(inicio_inclu,fin_inclu):
    impares=[]
    for i in range(inicio_inclu,fin_inclu+1):
        if(i%2!=0):
            impares.append(i)
    return impares

mask_sizes = creaimpares(3,21)
ts_pruebaEsp=[]
ts_pruebaFrq=[]
ts_Esp=[]
ts_Frq=[]

imagen = ski.io.imread("images/boat.511.tiff")
imagen = ski.util.img_as_float(imagen)



for i in range(len(mask_sizes)):
    # Convolución en el espacio
    for j in range(10):
        

        MASK_SIZE=mask_sizes[i]

        mascara = np.ones((MASK_SIZE, MASK_SIZE))  # Máscara de NxN toda con 1
        mascara /= np.sum(mascara)
        #tiempo ini mask espacio
        t_ini_esp=time.time()
        res_convol = scipy.ndimage.convolve(imagen, mascara, mode="wrap")
        t_fin_esp=time.time()
    
        t_tot_esp=t_fin_esp-t_ini_esp
        ts_pruebaEsp.append(t_tot_esp)
    ts_Esp.append(np.mean(ts_pruebaEsp))
    ts_pruebaEsp=[]

    # Producto pto a pto en la frecuencia
    for k in range(10):
        

        MASK_SIZE=mask_sizes[i]

        mascara = np.ones((MASK_SIZE, MASK_SIZE))  # Máscara de NxN toda con 1
        mascara /= np.sum(mascara)
        
        
        #tiempo ini mask espacio
        t_ini_frq=time.time()
        
        mascara_centrada = np.zeros(imagen.shape)
        fila_i = imagen.shape[0] // 2 - MASK_SIZE // 2
        col_i = imagen.shape[1] // 2 - MASK_SIZE // 2
        mascara_centrada[fila_i:fila_i + MASK_SIZE, col_i:col_i + MASK_SIZE] = mascara
        
        FTimagen = fft.fft2(imagen)
        mascara_en_origen = fft.ifftshift(mascara_centrada)
        FTmascara = fft.fft2(mascara_en_origen)

        FTimagen_filtrada = FTimagen * FTmascara
        
        t_fin_frq=time.time()
    
        t_tot_frq=t_fin_frq-t_ini_frq
        ts_pruebaFrq.append(t_tot_frq)
    ts_Frq.append(np.mean(ts_pruebaFrq))
    ts_pruebaFrq=[]

fig, axs = plt.subplots(1, 2)
axs[0].imshow(imagen, cmap=plt.cm.gray)
axs[0].set_title("Imagen original",fontsize=20)
axs[0].set_axis_off()
axs[1].set_xlabel("Tamaño de máscara")
axs[1].set_ylabel("Tiempo de ejecución")
axs[1].plot(mask_sizes,ts_Esp,label = "tiempos_ejec_espacio",color="red")
axs[1].plot(mask_sizes,ts_Frq,label = "tiempos_ejec_freq",color="blue")
axs[1].legend()

plt.show()

    

