# ================================================
# Notebook: Preprocesamiento Extendido Corregido (con comentarios)
# ================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler, 
    OneHotEncoder, KBinsDiscretizer, 
    PolynomialFeatures, FunctionTransformer
)
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

# ================================================
# 1. Generación de dataset sintético
# --------------------------------
# Aquí creamos un dataset artificial para probar las técnicas:
# - feat_normal: distribución normal.
# - feat_skewed: distribución exponencial (sesgada).
# - feat_outliers: normal con outliers intencionales.
# - feat_cat: variable categórica.
# - target: variable binaria desbalanceada.
# ================================================
np.random.seed(42)
n_samples = 1000

feat_normal = np.random.normal(50, 10, n_samples)
feat_skewed = np.random.exponential(2, n_samples)
feat_outliers = np.random.normal(0, 1, n_samples)
feat_outliers[:20] += np.random.normal(15, 5, 20)  # outliers intencionales
feat_cat = np.random.choice(['A','B','C'], n_samples, p=[0.5,0.3,0.2])
target = np.random.choice([0,1], n_samples, p=[0.7,0.3])

df = pd.DataFrame({
    'feat_normal': feat_normal,
    'feat_skewed': feat_skewed,
    'feat_outliers': feat_outliers,
    'feat_cat': feat_cat,
    'target': target
})

# Introducir valores nulos intencionales para practicar imputación
df.loc[5:10, 'feat_normal'] = np.nan
df.loc[20:25, 'feat_cat'] = np.nan

print("Primeras filas del dataset:")
print(df.head())

# ================================================
# 2. Visualización inicial
# --------------------------------
# Pairplot: permite ver relaciones entre variables
# y distribuciones según la variable objetivo.
# ================================================
sns.pairplot(df.dropna(), hue='target')
plt.suptitle("Distribución inicial de features (sin nulos)", y=1.02)
plt.show()

# ================================================
# 3. Manejo de valores nulos
# --------------------------------
# - Numéricas: imputación con la media.
#   Útil en datasets grandes donde los nulos son pocos.
#   Limitación: puede distorsionar si hay muchos nulos o si la variable es sesgada.
#
# - Categóricas: imputación con la moda.
#   Mantiene consistencia en variables categóricas.
#   Limitación: puede sobre-representar la categoría mayoritaria.
# ================================================
num_cols = df.select_dtypes(include=np.number).columns.tolist()
num_cols.remove('target')
imputer_num = SimpleImputer(strategy='mean')
df[num_cols] = imputer_num.fit_transform(df[num_cols])

cat_cols = df.select_dtypes(include='object').columns.tolist()
imputer_cat = SimpleImputer(strategy='most_frequent')
for col in cat_cols:
    df[col] = imputer_cat.fit_transform(df[[col]]).ravel()

print("\nValores nulos después de imputación:")
print(df.isnull().sum())

# ================================================
# 4. Escalado de variables
# --------------------------------
# - StandardScaler: media=0, varianza=1.
#   Útil en modelos basados en distancia (SVM, KNN, PCA).
#   Limitación: sensible a outliers.
#
# - RobustScaler: usa mediana y rango intercuartílico.
#   Resistente a outliers.
#
# - MinMaxScaler: escala en rango [0,1].
#   Útil en redes neuronales o métodos sensibles a magnitud.
#   Limitación: sensible a valores extremos.
# ================================================
scaler = StandardScaler()
df[['feat_normal','feat_skewed','feat_outliers']] = scaler.fit_transform(df[['feat_normal','feat_skewed','feat_outliers']])

robust_scaler = RobustScaler()
df['feat_outliers_robust'] = robust_scaler.fit_transform(df[['feat_outliers']])

minmax_scaler = MinMaxScaler()
df['feat_skewed_minmax'] = minmax_scaler.fit_transform(df[['feat_skewed']])

df[['feat_normal','feat_skewed','feat_outliers','feat_outliers_robust','feat_skewed_minmax']].hist(figsize=(12,6))
plt.suptitle("Histograma de features escaladas")
plt.show()

# ================================================
# 5. Transformaciones de features
# --------------------------------
# - Log-transform:
#   Reduce sesgo en distribuciones con cola larga.
#   Limitación: no aplica a valores <= 0.
#
# - PolynomialFeatures:
#   Crea combinaciones no lineales de variables.
#   Útil para modelos lineales que quieran capturar relaciones más complejas.
#   Limitación: aumenta dimensionalidad muy rápido.
# ================================================
log_transformer = FunctionTransformer(np.log1p)
df['feat_skewed_log'] = log_transformer.fit_transform(df[['feat_skewed']])

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(df[['feat_normal','feat_skewed']])
poly_feature_names = poly.get_feature_names_out(['feat_normal','feat_skewed'])
df_poly = pd.DataFrame(X_poly, columns=poly_feature_names)
df = pd.concat([df, df_poly], axis=1)

# ================================================
# 6. Codificación de variables categóricas
# --------------------------------
# OneHotEncoder:
#   Convierte categorías en variables binarias.
#   "drop='first'" evita multicolinealidad.
#   Limitación: aumenta el número de columnas si hay muchas categorías.
# ================================================
encoder = OneHotEncoder(sparse_output=False, drop='first')
cat_encoded = encoder.fit_transform(df[['feat_cat']])
cat_encoded_df = pd.DataFrame(cat_encoded, columns=encoder.get_feature_names_out(['feat_cat']))
df = pd.concat([df.drop(columns='feat_cat'), cat_encoded_df], axis=1)

# ================================================
# 7. Detección de outliers con Z-Score
# --------------------------------
# Z-score mide cuántas desviaciones estándar se aleja un valor de la media.
# Umbral típico: > 3 o < -3 se considera outlier.
# Limitación: asume distribución normal.
# ================================================
z_scores = np.abs(zscore(df[['feat_normal','feat_skewed','feat_outliers']]))
outliers_detected = (z_scores > 3).any(axis=1)
print(f"Número de outliers detectados: {outliers_detected.sum()}")

# ================================================
# 8. Discretización de variables (Binning)
# --------------------------------
# KBinsDiscretizer:
#   Divide una variable continua en intervalos (bins).
#   - strategy='quantile': asegura bins con igual cantidad de datos.
#   Útil para transformar variables continuas en categóricas.
#   Limitación: puede perder información precisa.
# ================================================
kbins = KBinsDiscretizer(
    n_bins=5, 
    encode='ordinal', 
    strategy='quantile',
    dtype=np.float64,
    quantile_method='averaged_inverted_cdf'
)

feat_normal_binned = kbins.fit_transform(df[['feat_normal']])
df['feat_normal_binned'] = feat_normal_binned[:, 0]

plt.figure(figsize=(6,4))
sns.countplot(x='feat_normal_binned', data=df)
plt.title("Distribución de feat_normal después de discretización")
plt.show()

# ================================================
# 9. Balanceo de clases
# --------------------------------
# - SMOTE (oversampling):
#   Genera ejemplos sintéticos de la clase minoritaria.
#   Útil en datasets desbalanceados.
#   Limitación: puede generar ruido si la clase minoritaria es muy dispersa.
#
# - RandomUnderSampler:
#   Elimina ejemplos de la clase mayoritaria.
#   Útil para reducir desbalance sin generar datos artificiales.
#   Limitación: puede perder información valiosa.
# ================================================
X = df.drop(columns='target')
y = df['target']

print("Número de NaN antes de SMOTE:", df.isna().sum().sum())
df = df.fillna(df.mean(numeric_only=True))  # Aseguramos que no queden NaN

X = df.drop(columns='target')
y = df['target']

smote = SMOTE(random_state=42)
X_smote, y_smote = smote.fit_resample(X, y)
print("\nDistribución tras SMOTE:")
print(pd.Series(y_smote).value_counts())

plt.figure(figsize=(6,4))
sns.countplot(x=y_smote)
plt.title("Distribución de clases tras SMOTE")
plt.show()

rus = RandomUnderSampler(random_state=42)
X_rus, y_rus = rus.fit_resample(X, y)
print("\nDistribución tras undersampling:")
print(pd.Series(y_rus).value_counts())

plt.figure(figsize=(6,4))
sns.countplot(x=y_rus)
plt.title("Distribución de clases tras undersampling")
plt.show()
