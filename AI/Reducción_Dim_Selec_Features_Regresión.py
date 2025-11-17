# ================================
# Notebook: Reducción, selección de features y regresión (compatible con regresión continua)
# ================================

# ================================
# 1. Librerías
# ================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_diabetes
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_regression, RFE
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ================================
# 2. Dataset
# ================================
diabetes = load_diabetes()
X = diabetes.data
y = diabetes.target
feature_names = diabetes.feature_names

df = pd.DataFrame(X, columns=feature_names)
df['target'] = y
print("Primeras filas del dataset de diabetes:")
print(df.head())

# ================================
# 3. Estandarización
# ================================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ================================
# 4. Reducción de dimensionalidad
# ================================

# ---- a) PCA (Principal Component Analysis) ----
n_components = 5
pca = PCA(n_components=n_components)
X_pca = pca.fit_transform(X_scaled)

explained_variance = pca.explained_variance_ratio_
print("\nVarianza explicada por cada componente PCA:", explained_variance)
print("Varianza acumulada:", np.cumsum(explained_variance))

plt.figure(figsize=(8,4))
plt.bar(range(1, n_components+1), explained_variance, alpha=0.7, label='Individual')
plt.plot(range(1, n_components+1), np.cumsum(explained_variance), marker='o', color='red', label='Acumulada')
plt.xlabel("Componente")
plt.ylabel("Varianza explicada")
plt.title("Varianza explicada por PCA")
plt.legend()
plt.show()

# ---- Nota sobre LDA ----
# LDA es supervisado y requiere clases, por lo que no es adecuado para regresión continua.
# Se puede usar solo ilustrativamente si binarizamos el target:
# y_binary = (y > np.median(y)).astype(int)
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
# lda = LDA(n_components=1)
# X_lda = lda.fit_transform(X_scaled, y_binary)
# plt.scatter(X_lda, y_binary)

# ================================
# 5. Selección de features
# ================================


# SelectKBest es un método rápido que selecciona las K mejores features según un test estadístico individual,
# sin considerar el modelo ni las interacciones entre features.
# RFE (Recursive Feature Elimination) usa un modelo base para eliminar iterativamente las features menos importantes,
# teniendo en cuenta cómo interactúan entre sí, por lo que suele ser más preciso pero más costoso.

# ---- SelectKBest (Filter method) ----
# Para regresión usamos f_regression en vez de f_classif
kbest = SelectKBest(score_func=f_regression, k=5)
X_kbest = kbest.fit_transform(X_scaled, y)
selected_features = np.array(feature_names)[kbest.get_support()]
print("\nSelectKBest seleccionó:", selected_features)

# ---- RFE (Wrapper method) ----
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rfe = RFE(estimator=rf, n_features_to_select=5)
rfe.fit(X_scaled, y)
rfe_features = np.array(feature_names)[rfe.support_]
print("RFE seleccionó:", rfe_features)

# ---- Importancia RF (Embedded method) ----
rf.fit(X_scaled, y)
importances = rf.feature_importances_
for name, imp in zip(feature_names, importances):
    print(f"{name}: importancia RF = {imp:.4f}")

plt.figure(figsize=(10,5))
plt.bar(feature_names, importances)
plt.xticks(rotation=45)
plt.ylabel("Importancia")
plt.title("Feature Importances con Random Forest")
plt.show()

# ================================
# 6. Regresión usando PCA
# ================================
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.3, random_state=42)
reg_pca = LinearRegression()
reg_pca.fit(X_train, y_train)
y_pred_pca = reg_pca.predict(X_test)

mse_pca = mean_squared_error(y_test, y_pred_pca)
rmse_pca = np.sqrt(mse_pca)
r2_pca = r2_score(y_test, y_pred_pca)

print("\nRegresión con componentes PCA")
print("MSE:", mse_pca, "RMSE:", rmse_pca, "R²:", r2_pca)

# ================================
# 7. Contribución aproximada de features originales
# ================================
pca_loadings = pca.components_.T
reg_coef = reg_pca.coef_
feature_contrib = np.dot(pca_loadings, reg_coef)

for name, contrib in zip(feature_names, feature_contrib):
    print(f"{name}: contribución aproximada = {contrib:.4f}")

plt.figure(figsize=(10,5))
plt.bar(feature_names, feature_contrib)
plt.xticks(rotation=45)
plt.ylabel("Contribución aproximada")
plt.title("Contribución aproximada de features originales (PCA + regresión)")
plt.show()

# ================================
# 8. Comparación con regresión original
# ================================
X_train_orig, X_test_orig, y_train_orig, y_test_orig = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
reg_orig = LinearRegression()
reg_orig.fit(X_train_orig, y_train_orig)
y_pred_orig = reg_orig.predict(X_test_orig)

mse_orig = mean_squared_error(y_test_orig, y_pred_orig)
rmse_orig = np.sqrt(mse_orig)
r2_orig = r2_score(y_test_orig, y_pred_orig)

print("\nRegresión con features originales")
print("MSE:", mse_orig, "RMSE:", rmse_orig, "R²:", r2_orig)

"""
Comentarios finales:

- PCA reduce dimensionalidad y ruido; contribución aproximada permite entender impacto de features.
- Selección de features con SelectKBest, RFE o Random Forest mantiene interpretabilidad y puede mejorar rendimiento.
- LDA no se usa directamente en regresión continua, solo ilustrativo con target binarizado.
- Comparación R² y RMSE indica si la reducción de dimensionalidad preserva suficiente información.
"""
