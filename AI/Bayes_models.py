# ================================================
# Notebook: Regresión Bayesiana con PyMC y análisis de residuos
# ================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymc as pm
import arviz as az

# ================================================
# 1. Carga del dataset
# ================================================
df = pd.read_csv("/home/miningdox/AprendoIA/Mall_Customers.csv")

# Seleccionamos variables numéricas relevantes
X = df[['Age', 'Annual Income (k$)']]
y = df['Spending Score (1-100)'].values  # Target continuo

# Normalizamos features para estabilidad numérica
X_scaled = (X - X.mean()) / X.std()

# ================================================
# 2. Modelo Bayesiano Gaussian
# ================================================
with pm.Model() as model:
    # Priors para coeficientes lineales
    beta = pm.Normal("beta", mu=0, sigma=10, shape=X_scaled.shape[1])
    alpha = pm.Normal("alpha", mu=0, sigma=10)
    sigma = pm.HalfNormal("sigma", sigma=10)

    # Media condicional
    mu = alpha + pm.math.dot(X_scaled.values, beta)

    # Likelihood (y|X)
    y_obs = pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y)

    # Sampling
    trace = pm.sample(2000, tune=1000, chains=2, target_accept=0.95, random_seed=42)

# ================================================
# 3. Predicción usando posterior
# ================================================
with model:
    posterior_predictive = pm.sample_posterior_predictive(trace, random_seed=42)

# Media de predicciones
y_pred = posterior_predictive.posterior_predictive["y_obs"].mean(dim=("chain", "draw")).values

# ================================================
# 4. Análisis de residuos
# ================================================
residuos = y - y_pred

# Histograma
plt.figure(figsize=(6,4))
plt.hist(residuos, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black')
plt.title("Histograma de residuos")
plt.xlabel("Residuo")
plt.ylabel("Densidad")
plt.show()

# Q-Q plot
import scipy.stats as stats
plt.figure(figsize=(6,4))
stats.probplot(residuos, dist="norm", plot=plt)
plt.title("Q-Q Plot de residuos")
plt.show()

# Residuos vs features
for col in X_scaled.columns:
    plt.figure(figsize=(6,4))
    plt.scatter(X_scaled[col], residuos, alpha=0.6)
    plt.axhline(y=0, color='red', linestyle='--')
    plt.xlabel(col)
    plt.ylabel("Residuo")
    plt.title(f"Residuos vs {col}")
    plt.show()

# Estadísticos básicos de residuos
print("Estadísticos básicos de residuos:")
print(pd.Series(residuos).describe())

# ================================================
# 5. Comentarios sobre interpretación
# ================================================
"""
- Si los residuos se distribuyen aproximadamente normales y no muestran patrón con las features,
  el modelo Gaussian Bayesiano es adecuado.
- Si los residuos muestran heterocedasticidad (varianza depende de X) o sesgo,
  el modelo puede necesitar transformaciones o un modelo no-lineal.
"""
