
import skimage as ski
import matplotlib.pyplot as plt
import math
import numpy as np

imagen = ski.io.imread("images/borrosa.png")
imagen = ski.transform.rescale(imagen, 0.5, order=5)

# Filtro Gaussiano 
F = []
F = ski.filters.gaussian(imagen, sigma=3)
alpha=1

R=imagen+alpha*(imagen-F)

#R es casi igual que I ya que la difererncia
#entre la inagen filtrada y la imagen original es cercana a cero
#es decir son muy parecidas.


fig, axs = plt.subplots(1, 2)
axs[0].imshow(imagen, cmap=plt.cm.gray)
axs[0].set_title("Imagen I",fontsize=20)
axs[0].set_axis_off()
axs[1].imshow(R, cmap=plt.cm.gray)
axs[1].set_title("Imagen R",fontsize=20)
axs[1].set_axis_off()
plt.show()



