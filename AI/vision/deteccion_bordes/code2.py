import skimage as ski
import matplotlib.pyplot as plt
import numpy as np

image1 = ski.io.imread("images/cuadros.png")  
image1 = ski.util.img_as_float(image1)
imager1  = ski.util.random_noise(image1, mode="gaussian", var=0.001)


def ajustar_01(imagen):
    maxi = imagen.max()
    mini = imagen.min()
    return (imagen - mini) / (maxi - mini)


def filtrar(image, nombres_filtros):
    images = [image]
    for nf in nombres_filtros:
        if nf == "moravec":
            img = my_moravec(image)
        else:
            if nf == "fast":
                param = ", 9"
            else:
                param = ""
            img = eval("ski.feature.corner_" + nf + "(image" + param + ")")
            if nf == "foerstner":
                img = img[0]
            elif nf == "kitchen_rosenfeld":
                img = np.abs(img)
        images.append(img)
    return images


def detectar_picos(images, umbral):
    resultados = [images[0]]
    for i in range(1, len(images)):
        img = ski.feature.corner_peaks(images[i], indices=False, min_distance=10, threshold_rel=umbral)
        resultados.append(img)
    return resultados


def my_moravec(cimage, window_size=1):
    rows = cimage.shape[0]
    cols = cimage.shape[1]
    out = np.zeros(cimage.shape)
    for r in range(2 * window_size, rows - 2 * window_size):
        for c in range(2 * window_size, cols - 2 * window_size):
            min_msum = 1E100
            for br in range(r - window_size, r + window_size + 1):
                for bc in range(c - window_size, c + window_size + 1):
                    if br != r or bc != c:  #### En scikit-image aquí aparece un AND !!!!
                        msum = 0
                        for mr in range(- window_size, window_size + 1):
                            for mc in range(- window_size, window_size + 1):
                                t = cimage[r + mr, c + mc] - cimage[br + mr, bc + mc]
                                msum += t * t
                        min_msum = min(msum, min_msum)

            out[r, c] = min_msum
    return out


def mostrar(titulo, resultados1, resultados2, nombres):
    fig, ax = plt.subplots(nrows=2, ncols=len(resultados1), layout="constrained")
    fig.suptitle(titulo, fontsize=24)
    for i in range(len(resultados1)):
        ax[0, i].imshow(resultados1[i], cmap='gray')
        ax[0, i].set_title(nombres[i], fontsize=16)
        ax[1, i].imshow(resultados2[i], cmap='gray')
        ax[1, i].set_title(nombres[i], fontsize=16)
    for a in ax.ravel():
        a.set_axis_off()
    plt.show()


filtros = ["kitchen_rosenfeld", "foerstner", "moravec", "harris", "fast"]

imagenesrot=[imager1,ski.transform.rotate(imager1,22.5),ski.transform.rotate(imager1,45),ski.transform.rotate(imager1,67.5),ski.transform.rotate(imager1,90)]

resultfinales=[]
resultcadaangulo=[]
#almaceno los picos de cada detector por cada angulo rotado en una matriz
picosfinales=[]
for i in range(len(imagenesrot)):
    #resultados cada detector
    imageKR = filtrar(imagenesrot[i], [filtros[0]])
    imageFoer= filtrar(imagenesrot[i], [filtros[1]])
    imageM=filtrar(imagenesrot[i], [filtros[2]])
    imageH=filtrar(imagenesrot[i], [filtros[3]])
    imageFast=filtrar(imagenesrot[i], [filtros[4]])
    #picos detectados por cada detector
    picosKR = detectar_picos(imageKR, 0.3)
    picosFoer = detectar_picos(imageFoer, 0.08)
    picosM=detectar_picos(imageM, 0.08)
    picosH=detectar_picos(imageH, 0.01)
    picosFast=detectar_picos(imageFast, 0.1)
    
    resultpicos=[picosKR,picosFoer,picosM,picosH,picosFast]
    resultcadaangulo=[imageKR,imageFoer,imageM,imageH,imageFast]
    
    resultfinales.append(resultcadaangulo)
    picosfinales.append(resultpicos)


fig, ax = plt.subplots(nrows=5, ncols=6, layout="constrained")
titulosangulos=["0 deg","22.5 deg","45 deg","67.5 deg","90 deg"]
for k in range(len(titulosangulos)):
    ax[k,0].imshow(imagenesrot[k], cmap='gray')
    ax[k,0].set_title(titulosangulos[k], fontsize=16)
    for i in range(len(titulosangulos)):
        resultpicos=picosfinales[k]
        for j in range(len(resultpicos[i])):
            ax[k,i+1].imshow(resultpicos[i][j], cmap='gray')
ax[0,1].set_title(filtros[0], fontsize=16)
ax[0,2].set_title(filtros[1], fontsize=16)
ax[0,3].set_title(filtros[2], fontsize=16)
ax[0,4].set_title(filtros[3], fontsize=16)
ax[0,5].set_title(filtros[4], fontsize=16)
for a in ax.ravel():
    a.set_axis_off()
plt.show()



