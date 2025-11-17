
import skimage as ski
import matplotlib.pyplot as plt
import numpy as np

img_original = ski.io.imread("images/Marilyn_Monroe.jpg")

src = [[0, 0],
       [0, 592],
       [285, 130],  # entrada cabza izquierda
       [395, 130],  #entrada cabza derecha
       [285, 180],          #ceja izquierda
       [395, 180],          #ceja derecha
       [270, 275],  # moflete izq 
       [400, 275],  # moflete der
       [333, 360],  # barbilla
       [657, 0],
       [657, 592]]

dst = src
src = np.array(src)
dst = np.array(dst)

#Marilyn Alien

# alargo cabeza
dst[2] = [260, 80] 
dst[3] = [410, 80]
dst[4] = [230, 180] 
dst[5] = [460, 180]
#alargo barbilla
dst[8]=  [333, 460]
tform = ski.transform.PiecewiseAffineTransform()
tform.estimate(src, dst)
img_t = ski.transform.warp(img_original, inverse_map=tform.inverse)

fig, axs = plt.subplots(1, 2, layout="constrained")
axs[0].imshow(img_original, cmap=plt.cm.gray)
axs[0].set_title("Malla de puntos",fontsize=24)
axs[0].plot(src[:, 0], src[:, 1], '.r')
axs[1].set_title("Marilyn Alien",color="green",fontsize=24)
axs[1].imshow(img_t, cmap=plt.cm.gray)

axs[0].set_axis_off()
axs[1].set_axis_off()
plt.show()
