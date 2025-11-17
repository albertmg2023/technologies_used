import skimage as ski
import matplotlib.pyplot as plt
import numpy as np

image = ski.io.imread("images/cuadros.png")  # Probar también con cuadros
imager1  = ski.util.random_noise(image, mode="gaussian", var=0.001)
imager2 = ski.util.random_noise(image, mode="gaussian", var=0.0015)
imager3 =img_noise = ski.util.random_noise(image, mode="gaussian", var=0.0025)

iniciales=[image,imager1,imager2,imager3]

#SOBEL
#obtener el gradiente con sobel
image1=ski.filters.sobel(image)
#imagen ruido 1 resultado 1 significa imager11 
imager11=ski.filters.sobel(imager1)
imager21=ski.filters.sobel(imager2)
imager31=ski.filters.sobel(imager3)

#Refinamiento de bordes Resultado1
resultados1=[]
resultados0=[image1,imager11,imager21,imager31]
for i in range(len(resultados0)):
    maximo = resultados0[i].max()
    low = maximo * 0.1
    high = maximo * 0.2
    mapa_bordes = ski.filters.apply_hysteresis_threshold(resultados0[i], low, high)
    mapa_bordes = ski.morphology.thin(mapa_bordes)
    resultados1.append(mapa_bordes)

#obtener los contornos Hough
resultados2=[]
for j in range (len(resultados1)):
    segmentos = ski.transform.probabilistic_hough_line(resultados1[j], threshold=10, line_length=5, line_gap=3)
    resultados2.append(segmentos)
    
#CANNY

#contronos con canny->result3
sigma=2
resultados3=[]
for k in range(len(iniciales)):
    img = ski.feature.canny(iniciales[k], sigma=sigma)
    resultados3.append(img)
    
    
#result 4
resultados4=[]
for j in range (len(resultados3)):
    segmentos = ski.transform.probabilistic_hough_line(resultados3[j], threshold=10, line_length=5, line_gap=3)
    resultados4.append(segmentos)

    



fig, ax = plt.subplots(nrows=4, ncols=5, layout="constrained")
ax[0, 0].imshow(image, cmap='gray')
ax[0, 0].set_title("Original", fontsize=16)
ax[1, 0].imshow(imager1, cmap='gray')
ax[1, 0].set_title("var=0.001", fontsize=16)
ax[2, 0].imshow(imager2, cmap='gray')
ax[2, 0].set_title("var=0.0015", fontsize=16)
ax[3, 0].imshow(imager3, cmap='gray')
ax[3, 0].set_title("var=0.0025", fontsize=16)
    
#resultados
ax[0, 1].set_title("Resultado1", fontsize=16)
ax[0, 1].imshow(resultados1[0], cmap='gray')
ax[1, 1].imshow(resultados1[1], cmap='gray')
ax[2, 1].imshow(resultados1[2], cmap='gray')
ax[3, 1].imshow(resultados1[3], cmap='gray')

ax[0, 2].set_title("Resultado2", fontsize=16)
ax[0, 2].imshow(np.zeros(image.shape), cmap='gray')
for segmento in resultados2[0]:
    p0, p1 = segmento
    ax[0, 2].plot((p0[0], p1[0]), (p0[1], p1[1]), color='r')  # Dibujar segmento
ax[1, 2].imshow(np.zeros(image.shape), cmap='gray')
for segmento in resultados2[1]:
    p0, p1 = segmento
    ax[1, 2].plot((p0[0], p1[0]), (p0[1], p1[1]), color='r')
ax[2, 2].imshow(np.zeros(image.shape), cmap='gray')
for segmento in resultados2[2]:
    p0, p1 = segmento
    ax[2, 2].plot((p0[0], p1[0]), (p0[1], p1[1]), color='r')
ax[3, 2].imshow(np.zeros(image.shape), cmap='gray')
for segmento in resultados2[3]:
    p0, p1 = segmento
    ax[3, 2].plot((p0[0], p1[0]), (p0[1], p1[1]), color='r')
    
ax[0, 3].set_title("Resultado3", fontsize=16)
ax[0, 3].imshow(resultados3[0], cmap='gray')
ax[1, 3].imshow(resultados3[1], cmap='gray')
ax[2, 3].imshow(resultados3[2], cmap='gray')
ax[3, 3].imshow(resultados3[3], cmap='gray')

ax[0, 4].set_title("Resultado4", fontsize=16)
ax[0, 4].imshow(np.zeros(image.shape), cmap='gray')
for segmento in resultados4[0]:
    p0, p1 = segmento
    ax[0, 4].plot((p0[0], p1[0]), (p0[1], p1[1]), color='r')  # Dibujar segmento
ax[1, 4].imshow(np.zeros(image.shape), cmap='gray')
for segmento in resultados4[1]:
    p0, p1 = segmento
    ax[1, 4].plot((p0[0], p1[0]), (p0[1], p1[1]), color='r')
ax[2, 4].imshow(np.zeros(image.shape), cmap='gray')
for segmento in resultados4[2]:
    p0, p1 = segmento
    ax[2, 4].plot((p0[0], p1[0]), (p0[1], p1[1]), color='r')
ax[3, 4].imshow(np.zeros(image.shape), cmap='gray')
for segmento in resultados4[3]:
    p0, p1 = segmento
    ax[3, 4].plot((p0[0], p1[0]), (p0[1], p1[1]), color='r')


for a in ax.ravel():
    a.set_axis_off()
plt.show()



def filtrar(image, nombre_filtro):
    if nombre_filtro == "roberts":
        dir1 = "_neg_diag"
        dir2 = "_pos_diag"
    else:
        dir1 = "_h"
        dir2 = "_v"
    img1 = eval("ski.filters." + nombre_filtro + dir1 + "(image)")
    img2 = eval("ski.filters." + nombre_filtro + dir2 + "(image)")
    img3 = eval("ski.filters." + nombre_filtro + "(image)")
    maximo = img3.max()
    low = maximo * 0.1  # Probar otros valores
    high = maximo * 0.2
    img4 = ski.filters.apply_hysteresis_threshold(img3, low, high)
    return [image, img1, img2, img3, img4]

    







def canny(image, sigmas, *args, **kwargs):
    images = [image]
    for sigma in sigmas:
        img = ski.feature.canny(image, sigma=sigma, *args, **kwargs)
        images.append(img)
    return images





