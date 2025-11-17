# ================================
# 1. Librerías
# ================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
# ================================
# 2. Cargar dataset
# ================================
df = pd.read_csv("/home/miningdox/AprendoIA/Mall_Customers.csv")
print(df.head())
print(df.info())

# Seleccionamos características para clustering
X = df[['Annual Income (k$)', 'Spending Score (1-100)']].values

# Estandarización
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ================================
# 3. Elección del número de clusters: Método del Codo
# ================================
inertia = []
K_range = range(1,11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8,5))
plt.plot(K_range, inertia, 'bo-', markersize=8)
plt.xlabel("Número de clusters (k)")
plt.ylabel("Inertia (Suma de distancias al cuadrado)")
plt.title("Método del codo para KMeans")
plt.show()

print("""
Interpretación: Busca el 'codo' donde la reducción de inertia empieza a decrecer lentamente. 
Ese punto indica el número óptimo de clusters.
""")

# ================================
# 4. Elección del número de clusters: Silhouette Score
# ================================
silhouette_scores = []
for k in range(2,11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    silhouette_scores.append(score)

plt.figure(figsize=(8,5))
plt.plot(range(2,11), silhouette_scores, 'ro-', markersize=8)
plt.xlabel("Número de clusters (k)")
plt.ylabel("Silhouette Score")
plt.title("Silhouette Score para KMeans")
plt.show()

print("""
Interpretación: El valor más alto del Silhouette Score indica un clustering más definido y separado.
Combina con el método del codo para elegir k óptimo.
""")

# ================================
# 5. KMeans con número de clusters elegido
# ================================
optimal_k = 5  # por ejemplo según el análisis previo
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
kmeans_labels = kmeans.fit_predict(X_scaled)

plt.figure(figsize=(8,5))
plt.scatter(X_scaled[:,0], X_scaled[:,1], c=kmeans_labels, cmap='viridis', s=50)
plt.xlabel("Annual Income (scaled)")
plt.ylabel("Spending Score (scaled)")
plt.title(f"KMeans Clustering con k={optimal_k}")
plt.show()

# ================================
# 6. DBSCAN: búsqueda de parámetros
# ================================
# Estandarización
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ================================
# 1. Gráfico k-distance para elegir eps
# ================================
min_samples_default = 7
neighbors = NearestNeighbors(n_neighbors=min_samples_default)
neighbors_fit = neighbors.fit(X_scaled)
distances, indices = neighbors_fit.kneighbors(X_scaled)

# Distancia al 7º vecino más cercano
distances_k = np.sort(distances[:, min_samples_default-1])
plt.figure(figsize=(8,5))
plt.plot(distances_k)
plt.title(f"Distancia al {min_samples_default}º vecino más cercano")
plt.xlabel("Puntos ordenados")
plt.ylabel("Distancia")
plt.show()

print("""
Interpretación: El 'codo' en este gráfico indica un valor adecuado de eps.
Los puntos donde la distancia aumenta bruscamente son los límites entre clusters.
""")

# ================================
# 2. Exploración de varios eps y min_samples
# ================================
eps_values = [0.3, 0.35,0.37,0.4, 0.5, 0.6, 0.7]
min_samples_values = [2,3,4,5, 7, 10]

best_score = -1
best_params = {}

for eps in eps_values:
    for min_samples in min_samples_values:
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(X_scaled)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        # Solo evaluamos si hay al menos 2 clusters
        if n_clusters >= 2:
            score = silhouette_score(X_scaled, labels)
            if score > best_score:
                best_score = score
                best_params = {'eps': eps, 'min_samples': min_samples, 'n_clusters': n_clusters}

print("Mejores parámetros DBSCAN según Silhouette Score:")
print(best_params)
print("Silhouette Score:", best_score)

# ================================
# 3. Entrenar DBSCAN con parámetros óptimos
# ================================
dbscan = DBSCAN(eps=best_params['eps'], min_samples=best_params['min_samples'])
dbscan_labels = dbscan.fit_predict(X_scaled)

# ================================
# 4. Visualización de clusters
# ================================
plt.figure(figsize=(8,5))
plt.scatter(X_scaled[:,0], X_scaled[:,1], c=dbscan_labels, cmap='plasma', s=50)
plt.xlabel("Annual Income (scaled)")
plt.ylabel("Spending Score (scaled)")
plt.title(f"DBSCAN Clustering (eps={best_params['eps']}, min_samples={best_params['min_samples']})")
plt.show()
print("""
Interpretación:
- Los puntos etiquetados como -1 son considerados outliers por DBSCAN.
- Ajustando 'eps' y 'min_samples' podemos controlar densidad mínima para formar clusters.
""")
