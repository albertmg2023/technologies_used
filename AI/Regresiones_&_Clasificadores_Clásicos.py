# ================================
# Notebook 3: Regresiones y Clasificadores Clásicos (Funciones existentes)
# ================================

# ================================
# 1. Importación de librerías
# ================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import fetch_california_housing, load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, f1_score

# ================================
# 2. Regresión Lineal Múltiple y Polinómica (California Housing)
# ================================
housing = fetch_california_housing(as_frame=True)
X_housing = housing.data
y_housing = housing.target

# Holdout
X_train, X_test, y_train, y_test = train_test_split(X_housing, y_housing, test_size=0.3, random_state=42)

# Lineal múltiple
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)

print("Regresión Lineal Múltiple (California Housing)")
print("MSE:", mean_squared_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R²:", r2_score(y_test, y_pred))

# Polinómica (grado 2)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X_housing)
X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(X_poly, y_housing, test_size=0.3, random_state=42)

lr_poly = LinearRegression()
lr_poly.fit(X_train_p, y_train_p)
y_pred_poly = lr_poly.predict(X_test_p)

print("\nRegresión Polinómica (grado 2)")
print("MSE:", mean_squared_error(y_test_p, y_pred_poly))
print("RMSE:", np.sqrt(mean_squared_error(y_test_p, y_pred_poly)))
print("R²:", r2_score(y_test_p, y_pred_poly))

# ================================
# 3. Regresión Logística Multiclase (Iris)
# ================================
iris = load_iris()
X_iris = iris.data
y_iris = iris.target

# Normalizamos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_iris)

# Regresión logística multinomial (default multi_class)
log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X_scaled, y_iris)
y_pred_log = log_reg.predict(X_scaled)

print("\nRegresión Logística Multiclase (Iris)")
print("Accuracy:", accuracy_score(y_iris, y_pred_log))
print("F1-score (macro):", f1_score(y_iris, y_pred_log, average='macro'))

# ================================
# ================================
# 1. Ridge (variando alpha)
# ================================
alphas = [0.1, 1.0, 10.0]
print("Ridge Regression:")
for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train, y_train)
    y_pred = ridge.predict(X_test)
    print(f"alpha={alpha} -> R²: {r2_score(y_test, y_pred):.4f}")

# ================================
# 2. Lasso (variando alpha)
# ================================
print("\nLasso Regression:")
for alpha in alphas:
    lasso = Lasso(alpha=alpha, max_iter=10000)
    lasso.fit(X_train, y_train)
    y_pred = lasso.predict(X_test)
    print(f"alpha={alpha} -> R²: {r2_score(y_test, y_pred):.4f}")

# ================================
# 3. Elastic Net (variando alpha y l1_ratio)
# ================================
l1_ratios = [0.3, 0.5, 0.7]
print("\nElasticNet Regression:")
for alpha in alphas:
    for l1_ratio in l1_ratios:
        elastic = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, max_iter=10000)
        elastic.fit(X_train, y_train)
        y_pred = elastic.predict(X_test)
        print(f"alpha={alpha}, l1_ratio={l1_ratio} -> R²: {r2_score(y_test, y_pred):.4f}")
        
# 5. Árboles de Decisión (Iris) con evaluación correcta
# ================================
from sklearn.model_selection import cross_val_score

# Split train/test
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_iris, y_iris, test_size=0.3, random_state=42)

# Árbol sin poda
tree = DecisionTreeClassifier(random_state=42)
tree.fit(X_train_c, y_train_c)
y_tree_test = tree.predict(X_test_c)
accuracy_tree_test = accuracy_score(y_test_c, y_tree_test)
print("\nÁrbol de Decisión (sin poda) sobre test set")
print("Accuracy test:", accuracy_tree_test)

# Árbol con pre-pruning
tree_pruned = DecisionTreeClassifier(max_depth=3, min_samples_split=5, random_state=42)
tree_pruned.fit(X_train_c, y_train_c)
y_tree_pruned_test = tree_pruned.predict(X_test_c)
accuracy_tree_pruned_test = accuracy_score(y_test_c, y_tree_pruned_test)
print("Árbol de Decisión (pre-pruning) sobre test set")
print("Accuracy test:", accuracy_tree_pruned_test)

# Cross-validation (5 folds) para evaluar generalización
cv_scores = cross_val_score(tree, X_iris, y_iris, cv=5, scoring='accuracy')
print("\nCross-validation Accuracy (sin poda):", cv_scores)
print("Promedio CV Accuracy:", cv_scores.mean())

cv_scores_pruned = cross_val_score(tree_pruned, X_iris, y_iris, cv=5, scoring='accuracy')
print("Cross-validation Accuracy (pre-pruning):", cv_scores_pruned)
print("Promedio CV Accuracy:", cv_scores_pruned.mean())

# ================================
# 6. SVM con kernels (Iris)
# ================================
X_scaled_svm = scaler.fit_transform(X_iris)

svm_linear = SVC(kernel='linear')
svm_linear.fit(X_scaled_svm, y_iris)
print("\nSVM Lineal Accuracy:", accuracy_score(y_iris, svm_linear.predict(X_scaled_svm)))

svm_poly = SVC(kernel='poly', degree=3)
svm_poly.fit(X_scaled_svm, y_iris)
print("SVM Polinomial Accuracy:", accuracy_score(y_iris, svm_poly.predict(X_scaled_svm)))

svm_rbf = SVC(kernel='rbf')
svm_rbf.fit(X_scaled_svm, y_iris)
print("SVM RBF Accuracy:", accuracy_score(y_iris, svm_rbf.predict(X_scaled_svm)))
