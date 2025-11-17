# Notebook 1: Introducción a Machine Learning con Iris

# ================================
# 1. Importación de librerías
# ================================
import numpy as np                # Librería para operaciones matemáticas
import pandas as pd               # Manejo de datos en formato tabla (DataFrames)
import matplotlib.pyplot as plt   # Visualización
import seaborn as sns             # Visualización avanzada

from sklearn.datasets import load_iris                # Dataset Iris
from sklearn.model_selection import train_test_split  # División en train/test
from sklearn.linear_model import LinearRegression     # Regresión lineal
from sklearn.neighbors import KNeighborsClassifier    # KNN (clasificación)
from sklearn.preprocessing import StandardScaler      # Normalización de datos
from sklearn.cluster import KMeans                   # Clustering KMeans

# ================================
# 2. Carga y exploración del dataset
# ================================
iris = load_iris()

# iris.data -> variables (4 características por flor)
# iris.target -> etiquetas (0 = setosa, 1 = versicolor, 2 = virginica)

X = iris.data
y = iris.target

# Convertimos a DataFrame para visualizar mejor
df = pd.DataFrame(X, columns=iris.feature_names)
df['species'] = y
df.head()

# ================================
# 3. Regresión Lineal (supervisado)
# ================================
# Objetivo: predecir la longitud del pétalo a partir de la longitud del sépalo

X_reg = df[['sepal length (cm)']]   # variable independiente
y_reg = df['petal length (cm)']     # variable dependiente

# División en train/test (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

# Modelo de regresión lineal
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)  # Entrenamiento del modelo

# Predicciones
y_pred = lin_reg.predict(X_test)

# Visualización de la regresión
plt.scatter(X_test, y_test, color='blue', label='Datos reales')
plt.plot(X_test, y_pred, color='red', label='Recta ajustada')
plt.xlabel('Longitud del sépalo (cm)')
plt.ylabel('Longitud del pétalo (cm)')
plt.title('Regresión Lineal en Iris')
plt.legend()
plt.show()

# ================================
# 4. Clasificación con KNN (supervisado)
# ================================
# Objetivo: clasificar la especie de iris según sus características

X_clf = X
y_clf = y

# Normalización de datos -> muy importante en KNN porque usa distancias
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_clf)

# División train/test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_clf, test_size=0.2, random_state=42)

# Modelo KNN
# Parámetro n_neighbors = número de vecinos que se consideran
knn = KNeighborsClassifier(n_neighbors=10)
knn.fit(X_train, y_train)

# Precisión en test
accuracy = knn.score(X_test, y_test)
print(f"Precisión de KNN con 5 vecinos: {accuracy:.2f}")

# ================================
# 5. Clustering con KMeans (no supervisado)
# ================================
# Objetivo: agrupar las flores en 3 clusters (sin usar etiquetas reales)

kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

# Agregamos los clusters al DataFrame
df['cluster'] = clusters

# Visualización: usamos solo dos dimensiones para graficar (longitud y ancho del pétalo)
sns.scatterplot(x=df['petal length (cm)'], y=df['petal width (cm)'], hue=df['cluster'], palette='deep')
plt.title('Clustering KMeans en Iris (3 clusters)')
plt.show()

# Nota: en clustering no usamos las etiquetas verdaderas, pero podemos comparar
de_comparación = pd.crosstab(df['species'], df['cluster'])
print("\nComparación entre etiquetas reales y clusters encontrados:")
print(de_comparación)
