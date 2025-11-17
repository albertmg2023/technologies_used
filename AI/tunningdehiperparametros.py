# ================================
# 1. Importación de librerías
# ================================
import numpy as np
from sklearn.datasets import fetch_california_housing, load_digits
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score

# ================================
# 2. Cargar datasets grandes
# ================================
# Regresión: California Housing (~20k muestras)
housing = fetch_california_housing(as_frame=True)
X_reg, y_reg = housing.data, housing.target
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.3, random_state=42)

# Clasificación: Digits (~1,797 muestras, 64 features)
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
# 4. Evaluación inicial (default parameters)
# ================================
print("=== Evaluación inicial ===")

# ---- Regresión ----
print("\nRidge Regression (default)")
evaluar_modelo(make_pipeline(StandardScaler(), Ridge()), X_train_r, X_test_r, y_train_r, y_test_r, 'regresion')

print("\nLasso Regression (default)")
evaluar_modelo(make_pipeline(StandardScaler(), Lasso(max_iter=5000)), X_train_r, X_test_r, y_train_r, y_test_r, 'regresion')

print("\nElasticNet Regression (default)")
evaluar_modelo(make_pipeline(StandardScaler(), ElasticNet(max_iter=5000)), X_train_r, X_test_r, y_train_r, y_test_r, 'regresion')

print("\nRegresión Polinómica (grado 2, LinearRegression)")
poly_model = Pipeline([
    ('poly', PolynomialFeatures(degree=2)),
    ('scaler', StandardScaler()),
    ('linreg', LinearRegression())
])
evaluar_modelo(poly_model, X_train_r, X_test_r, y_train_r, y_test_r, 'regresion')

# ---- Clasificación ----
print("\nLogistic Regression Multinomial (default)")
evaluar_modelo(make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000, multi_class='multinomial', solver='lbfgs')), 
               X_train_c, X_test_c, y_train_c, y_test_c, 'clasificacion')

print("\nSVM (default)")
evaluar_modelo(make_pipeline(StandardScaler(), SVC()), X_train_c, X_test_c, y_train_c, y_test_c, 'clasificacion')

print("\nDecision Tree (default)")
evaluar_modelo(DecisionTreeClassifier(random_state=42), X_train_c, X_test_c, y_train_c, y_test_c, 'clasificacion')

print("\nRandom Forest (default)")
evaluar_modelo(RandomForestClassifier(random_state=42), X_train_c, X_test_c, y_train_c, y_test_c, 'clasificacion')

# ================================
# 5. GridSearchCV para tuning
# ================================
# ---- Regresión ----
param_ridge = {'ridge__alpha':[0.01,0.1,1,10,100]}
grid_ridge = GridSearchCV(make_pipeline(StandardScaler(), Ridge()), param_ridge, cv=5, scoring='r2')
grid_ridge.fit(X_train_r, y_train_r)

param_lasso = {'lasso__alpha':[0.001,0.01,0.1,1,10]}
grid_lasso = GridSearchCV(make_pipeline(StandardScaler(), Lasso(max_iter=5000)), param_lasso, cv=5, scoring='r2')
grid_lasso.fit(X_train_r, y_train_r)

param_elastic = {'elasticnet__alpha':[0.01,0.1,1,10], 'elasticnet__l1_ratio':[0.2,0.5,0.7]}
grid_elastic = GridSearchCV(make_pipeline(StandardScaler(), ElasticNet(max_iter=5000)), param_elastic, cv=5, scoring='r2')
grid_elastic.fit(X_train_r, y_train_r)

# ---- Clasificación ----
param_log = {'logisticregression__C':[0.01,0.1,1,10], 'logisticregression__solver':['lbfgs','saga']}
grid_log = GridSearchCV(make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000, multi_class='multinomial')), param_log, cv=5, scoring='accuracy')
grid_log.fit(X_train_c, y_train_c)

param_svc = {'svc__C':[0.1,1,10], 'svc__kernel':['linear','rbf','poly'], 'svc__gamma':['scale','auto']}
grid_svc = GridSearchCV(make_pipeline(StandardScaler(), SVC()), param_svc, cv=5, scoring='accuracy')
grid_svc.fit(X_train_c, y_train_c)

param_tree = {'max_depth':[2,3,4,5,None], 'min_samples_split':[2,5,10], 'min_samples_leaf':[1,2,4]}
grid_tree = GridSearchCV(DecisionTreeClassifier(random_state=42), param_tree, cv=5, scoring='accuracy')
grid_tree.fit(X_train_c, y_train_c)

param_rf = {'n_estimators':[50,100,200], 'max_depth':[3,5,7,None]}
grid_rf = GridSearchCV(RandomForestClassifier(random_state=42), param_rf, cv=5, scoring='accuracy')
grid_rf.fit(X_train_c, y_train_c)

# ================================
# 6. Evaluación después del tuning
# ================================
print("\n=== Evaluación después del tuning ===")

# ---- Regresión ----
print("\nRidge Regression")
print("Mejor alpha:", grid_ridge.best_params_)
evaluar_modelo(grid_ridge.best_estimator_, X_train_r, X_test_r, y_train_r, y_test_r, 'regresion')

print("\nLasso Regression")
print("Mejor alpha:", grid_lasso.best_params_)
evaluar_modelo(grid_lasso.best_estimator_, X_train_r, X_test_r, y_train_r, y_test_r, 'regresion')

print("\nElasticNet Regression")
print("Mejor combinación:", grid_elastic.best_params_)
evaluar_modelo(grid_elastic.best_estimator_, X_train_r, X_test_r, y_train_r, y_test_r, 'regresion')

# Polinómica se puede usar tuning similar, agregando Ridge/Lasso dentro del pipeline si se desea
print("\nRegresión Polinómica (grado 2)")
evaluar_modelo(poly_model, X_train_r, X_test_r, y_train_r, y_test_r, 'regresion')

# ---- Clasificación ----
print("\nLogistic Regression Multinomial")
print("Mejor combinación:", grid_log.best_params_)
evaluar_modelo(grid_log.best_estimator_, X_train_c, X_test_c, y_train_c, y_test_c, 'clasificacion')

print("\nSVM")
print("Mejor combinación:", grid_svc.best_params_)
evaluar_modelo(grid_svc.best_estimator_, X_train_c, X_test_c, y_train_c, y_test_c, 'clasificacion')

print("\nDecision Tree")
print("Mejor combinación:", grid_tree.best_params_)
evaluar_modelo(grid_tree.best_estimator_, X_train_c, X_test_c, y_train_c, y_test_c, 'clasificacion')

print("\nRandom Forest")
print("Mejor combinación:", grid_rf.best_params_)
evaluar_modelo(grid_rf.best_estimator_, X_train_c, X_test_c, y_train_c, y_test_c, 'clasificacion')
