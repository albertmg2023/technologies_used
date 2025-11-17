

import skimage as ski
import matplotlib.pyplot as plt
import numpy as np

img_original = ski.io.imread("images/lena256.pgm")
N=90
#rotación sin rotate
transf_despl = ski.transform.EuclideanTransform(translation=(0, 0))
tranf_rot=ski.transform.EuclideanTransform(rotation=np.radians(N))
print(img_original.size())
transf_desplfin = ski.transform.EuclideanTransform(translation=(255,0))

mtot=transf_desplfin.params @ tranf_rot.params @ transf_despl.params

transf_tot=ski.transform.EuclideanTransform(mtot)

img_fin = ski.transform.warp(img_original,transf_tot)

#ROTACIÓN CON FUNCION ROTATE
N=90
img_girada = ski.transform.rotate(img_original, N)



print("Matriz total ")
print(transf_desplfin.params @ tranf_rot.params @ transf_despl.params )
print()

fig, axs = plt.subplots(1, 3, layout="constrained")
axs[0].set_axis_off()
axs[0].set_title('ORIGINAL')
axs[0].imshow(img_original, cmap=plt.cm.gray)
axs[1].set_title('Rotate')
axs[1].imshow(img_girada, cmap=plt.cm.gray)
axs[2].set_title('Euclidean Transform')
axs[2].imshow(img_fin, cmap=plt.cm.gray)

plt.show()
