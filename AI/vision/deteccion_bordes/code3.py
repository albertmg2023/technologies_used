import skimage as ski
import matplotlib.pyplot as plt
import numpy as np

image1 = ski.io.imread("images/monedas1.png")
image2 = ski.io.imread("images/monedas2.png")
image3 = ski.io.imread("images/monedas3.png")# Probar también con sintética
image1 = ski.util.img_as_float(image1)
image2 = ski.util.img_as_float(image2)
image3 = ski.util.img_as_float(image3)
#aplico el mismo filtro gaussiano a todas para eliminar ruido
filtrada1=ski.filters.gaussian(image1, sigma=1)
filtrada2=ski.filters.gaussian(image2, sigma=1)
filtrada3=ski.filters.gaussian(image3, sigma=1)
#aplico detector de bordes Sobel

detbord1=ski.filters.sobel(filtrada1)
detbord2=ski.filters.sobel(filtrada2)
detbord3=ski.filters.sobel(filtrada3)

#resultados del refinamiento de bordes
res_refinbord=[]
resultados0=[detbord1,detbord2,detbord3]
for i in range(len(resultados0)):
    maximo = resultados0[i].max()
    low = maximo * 0.2
    high = maximo * 0.5
    mapa_bordes = ski.filters.apply_hysteresis_threshold(resultados0[i], low, high)
    mapa_bordes = ski.morphology.thin(mapa_bordes)
    res_refinbord.append(mapa_bordes)


#radios a pixeles
rad_1eur=int(((23*50)/25.4)/2)
rad_10cent=int(((19.5*50)/25.4)/2)
print("pixeles rad 1 eur=:",rad_1eur)
print("pixeles rad 10 cent=:",rad_10cent)
resultfinales=[]
# Transformada de Hough para círculos
for i in range(3):
    radios_posibles = np.array([rad_10cent,rad_1eur])  
    hough_res = ski.transform.hough_circle(res_refinbord[i], radios_posibles)
    accums, cx, cy, radii = ski.transform.hough_circle_peaks(hough_res, radios_posibles, min_xdistance=5, min_ydistance=5)
    resultado = np.zeros(res_refinbord[i].shape)
    #dibujar circulos si son de 10cent son Blancos y si son de 1 euro son grises
    for fila, col, radio in zip(cy, cx, radii):
            circy, circx = ski.draw.circle_perimeter(fila, col, radio, shape=res_refinbord[i].shape)
            # Dibuja un círculo
            if radio==rad_1eur:
                resultado[circy, circx] = 1
            else:
                resultado[circy, circx] = 2

    resultfinales.append(resultado)
    resultado=[]


fig, ax = plt.subplots(nrows=3, ncols=5, layout="constrained")
ax[0,0].set_title("Originales", size=16)
ax[0, 0].imshow(image1, cmap='gray')
ax[1, 0].imshow(image2, cmap='gray')
ax[2, 0].imshow(image3, cmap='gray')
ax[0,1].set_title("Filtro G con sigm=1", size=16)
ax[0, 1].imshow(filtrada1, cmap='gray')
ax[1, 1].imshow(filtrada2, cmap='gray')
ax[2, 1].imshow(filtrada3, cmap='gray')
ax[0,2].set_title("Detección de bordes", size=16)
ax[0, 2].imshow(detbord1, cmap='gray')
ax[1, 2].imshow(detbord2, cmap='gray')
ax[2, 2].imshow(detbord3, cmap='gray')
ax[0,3].set_title("Mejora de bordes", size=16)
ax[0, 3].imshow(res_refinbord[0], cmap='gray')
ax[1, 3].imshow(res_refinbord[1], cmap='gray')
ax[2, 3].imshow(res_refinbord[2], cmap='gray')
ax[0,4].set_title("Detección de monedas", size=16)
ax[0, 4].imshow(resultfinales[0], cmap='gray')
ax[1, 4].imshow(resultfinales[1], cmap='gray')
ax[2, 4].imshow(resultfinales[2], cmap='gray')

for a in ax.ravel():
    a.set_axis_off()
plt.show()



