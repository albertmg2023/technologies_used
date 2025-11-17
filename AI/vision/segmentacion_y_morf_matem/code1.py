import numpy as np
import skimage as ski
import matplotlib.pyplot as plt
from math import pi

img1 = ski.io.imread("images/monedas1.png")
img2 = ski.io.imread("images/monedas2.png")
img3 = ski.io.imread("images/monedas3.png")



umbral_otsu1 = ski.filters.threshold_otsu(img1)
img_umbralizada1 = img1 < umbral_otsu1 
umbral_otsu2 = ski.filters.threshold_otsu(img2)
img_umbralizada2 = img2 < umbral_otsu2
umbral_otsu3 = ski.filters.threshold_otsu(img3)
img_umbralizada3 = img3 < umbral_otsu3

print(f"Umbral saleccionado (local1): {umbral_otsu1}")
print(f"Umbral saleccionado (local2): {umbral_otsu2}")
print(f"Umbral saleccionado (local3): {umbral_otsu3}")




rad_1eur=int(((23*50)/25.4)/2)
rad_10cent=int(((19.5*50)/25.4)/2)
A_1eur=pi*rad_1eur*rad_1eur
A_10cent=pi*rad_10cent*rad_10cent
print("Area de 1 euro: ",A_1eur,"  Area de 10 centimos: ",A_10cent)


st_elem = ski.morphology.disk(2)
eros1=ski.morphology.erosion(img_umbralizada1,footprint=st_elem)
eros2=ski.morphology.erosion(img_umbralizada2,footprint=st_elem)
eros3=ski.morphology.erosion(img_umbralizada3,footprint=st_elem)
st_elem = ski.morphology.disk(5)
dilat1=ski.morphology.dilation(eros1, footprint=st_elem)
dilat2=ski.morphology.dilation(eros2, footprint=st_elem)
dilat3=ski.morphology.dilation(eros3, footprint=st_elem)

dilat1=ski.morphology.dilation(dilat1, footprint=st_elem)
dilat2=ski.morphology.dilation(dilat2, footprint=st_elem)
dilat3=ski.morphology.dilation(dilat3, footprint=st_elem)
"""quitapeque1=ski.morphology.remove_small_objects(eros1, min_size=3)
quitapeque2=ski.morphology.remove_small_objects(eros2, min_size=3)
quitapeque3=ski.morphology.remove_small_objects(eros3, min_size=3)
"""

st_elem = ski.morphology.disk(5)
#
img_opening1 = ski.morphology.diameter_opening(dilat1, diameter_threshold=3)
img_opening2 = ski.morphology.diameter_opening(dilat2, diameter_threshold=3)
img_opening3 = ski.morphology.diameter_opening(dilat3, diameter_threshold=3)

"""img_cierre1=ski.morphology.remove_small_holes(img_cierre1, area_threshold=64)
img_cierre2=ski.morphology.remove_small_holes( img_cierre1,area_threshold=64)
img_cierre3=ski.morphology.remove_small_holes(img_cierre3, area_threshold=64)
"""
##################

img_etiquetada1 = ski.morphology.label(img_opening1,background=1)
img_etiquetada2 = ski.morphology.label(img_opening2,background=1)
img_etiquetada3 = ski.morphology.label(img_opening3,background=1)
props1 = ski.measure.regionprops(img_etiquetada1)
props2 = ski.measure.regionprops(img_etiquetada2)
props3 = ski.measure.regionprops(img_etiquetada3)
print("imagen 1")
for p in props1:
    print(f"Etiqueta: {p.label} Área: {p.area} Excentricidad: {p.eccentricity:.2f}")
img_monedas1 = np.zeros(img1.shape)
contador_monedas1 = 0
for p in props1:
    if p.eccentricity < 0.50:
        if(500<p.area<700):
            img_monedas1[img_etiquetada1 == p.label] = 1
            print("Moneda de 1 Euro")
        elif(350<p.area<450):
            img_monedas1[img_etiquetada1 == p.label] = 2
            print("Moneda de 10 cents")
        contador_monedas1 += 1
print(f"Detectadas {contador_monedas1} monedas")
print("imagen 2")
img_monedas2 = np.zeros(img2.shape)
contador_monedas2 = 0
for p in props2:
    print(f"Etiqueta: {p.label} Área: {p.area} Excentricidad: {p.eccentricity:.2f}")
for p in props2:
    if p.eccentricity < 0.50:
        if(500<p.area<700):
            img_monedas2[img_etiquetada2 == p.label] = 1
            print("Moneda de 1 Euro")
        elif(350<p.area<450):
            img_monedas2[img_etiquetada2 == p.label] = 2
            print("Moneda de 10 cents")
        contador_monedas2 += 1
print(f"Detectadas {contador_monedas2} monedas")
print("Imagen 3")
img_monedas3 = np.zeros(img3.shape)
contador_monedas3 = 0
for p in props3:
    print(f"Etiqueta: {p.label} Área: {p.area} Excentricidad: {p.eccentricity:.2f}")
for p in props3:
    if p.eccentricity < 0.50:
         if(500<p.area<700):
            img_monedas3[img_etiquetada3 == p.label] = 1
            print("Moneda de 1 Euro")
         elif(350<p.area<450):
            img_monedas3[img_etiquetada3 == p.label] = 2
            print("Moneda de 10 cents")
         contador_monedas3 += 1
print(f"Detectadas {contador_monedas3} monedas")



# Visualizar resultados
fig, axs = plt.subplots(3, 6, layout="constrained")
for ax in axs.ravel():
    ax.set_axis_off()
fig.suptitle("Segmentación por umbralización", fontsize=24)

axs[0, 0].set_title("Originales", fontsize=16)
axs[0, 0].imshow(img1, cmap="gray")
axs[1, 0].imshow(img2, cmap="gray")
axs[2, 0].imshow(img3, cmap="gray")

axs[0 ,1].set_title("Umbralizada", fontsize=16)
axs[0, 1].imshow(img_umbralizada1, cmap="gray")
axs[1, 1].imshow(img_umbralizada2, cmap="gray")
axs[2, 1].imshow(img_umbralizada3, cmap="gray")

axs[0, 2].set_title("erosionadas", fontsize=16)

axs[0, 2].imshow(eros1, cmap="gray")
axs[1, 2].imshow(eros2, cmap="gray")
axs[2, 2].imshow(eros3, cmap="gray")

axs[0, 3].set_title("dilatadas", fontsize=16)

axs[0, 3].imshow(dilat1, cmap="gray")
axs[1, 3].imshow(dilat2, cmap="gray")
axs[2, 3].imshow(dilat3, cmap="gray")


axs[0, 3].set_title("Opening", fontsize=16)

axs[0, 3].imshow(img_opening1, cmap="gray")
axs[1, 3].imshow(img_opening2, cmap="gray")
axs[2, 3].imshow(img_opening3, cmap="gray")


axs[0, 4].imshow(img_monedas1, interpolation="None", cmap="jet")
axs[1, 4].imshow(img_monedas2, interpolation="None", cmap="jet")
axs[2, 4].imshow(img_monedas3, interpolation="None", cmap="jet")
axs[0, 4].set_title("Monedas", fontsize=16)

plt.show()
