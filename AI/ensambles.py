# ================================
# 1. Importación de librerías
# ================================
import numpy as np
from sklearn.datasets import load_digits, fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.ensemble import BaggingRegressor, RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
import matplotlib.pyplot as plt

# ================================
# 2. Cargar datasets
# ================================
# Regresión: California Housing
housing = fetch_california_housing(as_frame=True)
X_reg, y_reg = housing.data, housing.target
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.3, random_state=42)

# Clasificación: Digits
digits = load_digits()
X_clf, y_clf = digits.data, digits.target
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_clf, y_clf, test_size=0.3, random_state=42)

# ================================
# 3. Función de evaluación
# ================================
def evaluar_modelo(modelo, X_train, X_test, y_train, y_test, tipo='regresion'):
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    if tipo == 'regresion':
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        print(f"MSE: {mse:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}")
    else:
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc:.4f}")

# ================================
# 4. Modelos de ensamble (default parameters)
# ================================
print("=== Ensambles - Evaluación inicial ===")

# ---- Regresión ----
print("\nBagging Regressor")
evaluar_modelo(BaggingRegressor(estimator=DecisionTreeRegressor(), n_estimators=50, random_state=42),
               X_train_r, X_test_r, y_train_r, y_test_r, 'regresion')

print("\nRandom Forest Regressor")
evaluar_modelo(RandomForestRegressor(n_estimators=100, random_state=42),
               X_train_r, X_test_r, y_train_r, y_test_r, 'regresion')

print("\nAdaBoost Regressor")
evaluar_modelo(AdaBoostRegressor(n_estimators=100, random_state=42),
               X_train_r, X_test_r, y_train_r, y_test_r, 'regresion')

print("\nGradient Boosting Regressor")
evaluar_modelo(GradientBoostingRegressor(n_estimators=100, random_state=42),
               X_train_r, X_test_r, y_train_r, y_test_r, 'regresion')

# ---- Clasificación ----
print("\nBagging Classifier")
evaluar_modelo(BaggingClassifier(estimator=DecisionTreeClassifier(), n_estimators=50, random_state=42),
               X_train_c, X_test_c, y_train_c, y_test_c, 'clasificacion')

print("\nRandom Forest Classifier")
evaluar_modelo(RandomForestClassifier(n_estimators=100, random_state=42),
               X_train_c, X_test_c, y_train_c, y_test_c, 'clasificacion')

print("\nAdaBoost Classifier")
evaluar_modelo(AdaBoostClassifier(n_estimators=100, random_state=42),
               X_train_c, X_test_c, y_train_c, y_test_c, 'clasificacion')

print("\nGradient Boosting Classifier")
evaluar_modelo(GradientBoostingClassifier(n_estimators=100, random_state=42),
               X_train_c, X_test_c, y_train_c, y_test_c, 'clasificacion')

# ================================
# 5. Comparación visual
# ================================
# Métricas regresión
reg_models = ["Bagging", "Random Forest", "AdaBoost", "Gradient Boosting"]
reg_rmse = []

for modelo in [BaggingRegressor(estimator=DecisionTreeRegressor(), n_estimators=50, random_state=42),
               RandomForestRegressor(n_estimators=100, random_state=42),
               AdaBoostRegressor(n_estimators=100, random_state=42),
               GradientBoostingRegressor(n_estimators=100, random_state=42)]:
    modelo.fit(X_train_r, y_train_r)
    y_pred = modelo.predict(X_test_r)
    reg_rmse.append(np.sqrt(mean_squared_error(y_test_r, y_pred)))

plt.bar(reg_models, reg_rmse, color='skyblue')
plt.ylabel("RMSE")
plt.title("Comparación RMSE Modelos de Ensamble (Regresión)")
plt.show()

# Métricas clasificación
clf_models = ["Bagging", "Random Forest", "AdaBoost", "Gradient Boosting"]
clf_acc = []

for modelo in [BaggingClassifier(estimator=DecisionTreeClassifier(), n_estimators=50, random_state=42),
               RandomForestClassifier(n_estimators=100, random_state=42),
               AdaBoostClassifier(n_estimators=100, random_state=42),
               GradientBoostingClassifier(n_estimators=100, random_state=42)]:
    modelo.fit(X_train_c, y_train_c)
    y_pred = modelo.predict(X_test_c)
    clf_acc.append(accuracy_score(y_test_c, y_pred))

plt.bar(clf_models, clf_acc, color='lightgreen')
plt.ylabel("Accuracy")
plt.title("Comparación Accuracy Modelos de Ensamble (Clasificación)")
plt.show()
