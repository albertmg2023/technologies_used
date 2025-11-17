# ================================
# Notebook 2: Validación y Evaluación de Modelos (Diabetes dataset)
# ================================

# ================================
# 1. Importación de librerías
# ================================
import numpy as np
import pandas as pd
from math import sqrt
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split, KFold, LeaveOneOut, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.utils import resample
from sklearn.metrics import mean_squared_error, r2_score, make_scorer

# ================================
# 2. Carga del dataset Diabetes
# ================================
diabetes = load_diabetes()
X, y = diabetes.data, diabetes.target

# Convertimos a DataFrame
df = pd.DataFrame(X, columns=diabetes.feature_names)
df['target'] = y

# ================================
# 2b. Visualización opcional de correlación
# ================================
corr_matrix = df.corr()
plt.figure(figsize=(12,10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Matriz de correlación completa")
plt.show()

# ================================
# 3. Holdout Validation
# ================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
reg = LinearRegression()
reg.fit(X_train, y_train)
y_pred = reg.predict(X_test)

mse_holdout = mean_squared_error(y_test, y_pred)
rmse_holdout = sqrt(mse_holdout)

print("Holdout Validation")
print("MSE:", mse_holdout)
print("RMSE:", rmse_holdout)
print("R²:", r2_score(y_test, y_pred))

# ================================
# 4. K-Fold Cross Validation con MSE y RMSE
# ================================
kf = KFold(n_splits=5, shuffle=True, random_state=42)
mse_scorer = make_scorer(mean_squared_error, greater_is_better=False)
scores = cross_val_score(reg, X, y, cv=kf, scoring=mse_scorer)
mse_kfold = -scores
rmse_kfold = np.sqrt(mse_kfold)

print("\nK-Fold Cross Validation (k=5)")
print("MSE en cada fold:", mse_kfold)
print("RMSE en cada fold:", rmse_kfold)
print("MSE promedio:", mse_kfold.mean())
print("RMSE promedio:", sqrt(mse_kfold.mean()))

# ================================
# 5. Leave-One-Out Cross Validation con MSE y RMSE
# ================================
loo = LeaveOneOut()
mse_scores_loo = []

for train_index, test_index in loo.split(X):
    X_train_loo, X_test_loo = X[train_index], X[test_index]
    y_train_loo, y_test_loo = y[train_index], y[test_index]
    reg.fit(X_train_loo, y_train_loo)
    y_pred_loo = reg.predict(X_test_loo)
    mse_scores_loo.append(mean_squared_error(y_test_loo, y_pred_loo))

rmse_loo = sqrt(np.mean(mse_scores_loo))
print("\nLeave-One-Out Cross Validation")
print("MSE promedio:", np.mean(mse_scores_loo))
print("RMSE promedio:", rmse_loo)

# ================================
# 6. Nested Cross Validation (tuning de hiperparámetros) con R²
# ================================
param_grid = {'fit_intercept': [True, False]}
inner_cv = KFold(n_splits=3, shuffle=True, random_state=42)
outer_cv = KFold(n_splits=5, shuffle=True, random_state=42)

reg_nested = GridSearchCV(LinearRegression(), param_grid, cv=inner_cv, scoring='r2')
scores_nested = cross_val_score(reg_nested, X, y, cv=outer_cv, scoring='r2')
print("\nNested Cross Validation")
print("R² promedio:", scores_nested.mean())

# ================================
# 7. Bootstrapping con MSE y RMSE
# ================================
n_iterations = 100
mse_scores_boot = []

for i in range(n_iterations):
    X_resampled, y_resampled = resample(X_train, y_train, random_state=i)
    reg.fit(X_resampled, y_resampled)
    y_pred_boot = reg.predict(X_test)
    mse_scores_boot.append(mean_squared_error(y_test, y_pred_boot))

rmse_boot = sqrt(np.mean(mse_scores_boot))
print("\nBootstrapping")
print("MSE promedio:", np.mean(mse_scores_boot))
print("RMSE promedio:", rmse_boot)
