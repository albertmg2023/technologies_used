# Objetivos:
# - Rotar una imagen (parámetros centro, resize e interpolación)
# - Crear, manejar y aplicar transformaciones afines (también podrían se euclídeas o de similitud)

import skimage as ski
import matplotlib.pyplot as plt
import numpy as np

img_original = ski.io.imread("images/lena256.pgm")





ta_esc = ski.transform.AffineTransform(scale=[0.5,0.75])
mscalado = ta_esc.params

i_escalada=ski.transform.warp(img_original, ta_esc.inverse, output_shape=(512, 512))
print(f"Matriz de escalado con factor [0.5,0.75]")
print(mscalado)
print()

DISTANCIA_TRASLACION = (64, 0)
ta_desp = ski.transform.AffineTransform(translation=DISTANCIA_TRASLACION)
mtranslacion = ta_desp.params
i_desp=ski.transform.warp(i_escalada, ta_desp.inverse, output_shape=(512, 512))
print(f"Matriz de traslación con distancia {DISTANCIA_TRASLACION}")
print(mtranslacion)
print()

ANGULO_ROTACION_EN_GRADOS =15
ta_rot = ski.transform.AffineTransform(rotation=np.radians(ANGULO_ROTACION_EN_GRADOS))
mrotacion = ta_rot.params
i_rot=ski.transform.warp(i_desp, ta_rot.inverse, output_shape=(512, 512))
print(f"Matriz de rotación con ángulo {ANGULO_ROTACION_EN_GRADOS}")
print(mrotacion)
print()

ANGULOS_INCLINACION_EN_GRADOS = [-10,-10]
ta_inc = ski.transform.AffineTransform(shear=np.radians(ANGULOS_INCLINACION_EN_GRADOS))
mshear = ta_inc.params
i_inc=ski.transform.warp(i_rot, ta_inc.inverse, output_shape=(512, 512))
print(f"Matriz de inclinación con ángulo de {ANGULOS_INCLINACION_EN_GRADOS} grados")
print(mshear)
print()

#5

ta = ski.transform.AffineTransform(scale=[0.5,0.75],translation=DISTANCIA_TRASLACION,rotation=np.radians(ANGULO_ROTACION_EN_GRADOS),shear=np.radians(ANGULOS_INCLINACION_EN_GRADOS))
print(f"Matriz de transformación generada con todos los paŕametros")
print(ta.params)
print()

#6

matriz_total_calculada = mshear @ mrotacion @ mtranslacion @ mscalado


print(f"Matriz de transformación total calculada: 1. Escalado 2. Traslación 3. Rotación 4. Inclinación")
print(matriz_total_calculada)
print()

mita = ski.transform.AffineTransform(matriz_total_calculada)
mi_img_tras = ski.transform.warp(img_original, mita.inverse, output_shape=(512, 512))



img_tras = ski.transform.warp(img_original, ta.inverse, output_shape=(512, 512))

fig, axs = plt.subplots(2, 4, layout="constrained")
axs[0, 0].set_title("Original")
axs[0, 0].imshow(img_original, cmap=plt.cm.gray)
axs[0, 1].imshow(i_escalada, cmap=plt.cm.gray)
axs[0, 2].imshow(i_desp, cmap=plt.cm.gray)
axs[0, 0].set_title("Original")
axs[0, 1].set_title("1-Escalada")
axs[0, 2].set_title("2-Desplazada")
axs[1, 0].set_title("3-Rotada")
axs[1, 1].set_title("4-Inclinada")
axs[1, 2].set_title("5-Todas_simultáneas")
axs[1, 3].set_title("6-Mult_matrices")
axs[1, 0].imshow(i_rot, cmap=plt.cm.gray)
axs[1, 1].imshow(i_inc, cmap=plt.cm.gray)
axs[1, 2].imshow(img_tras, cmap=plt.cm.gray)
axs[1, 3].imshow(mi_img_tras, cmap=plt.cm.gray)

axs[0, 0].set_axis_off()
axs[0, 3].set_axis_off()
axs[1, 0].set_axis_off()
plt.show()
