# -*- coding: utf-8 -*-
"""Heart-Disease-Project.ipynb
Original file is located at
    https://colab.research.google.com/drive/1xJ1fuckPv6SSaLms8JQkqkzOHK0P52Dz
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split , cross_val_score
from sklearn.model_selection import RandomizedSearchCV , GridSearchCV
from sklearn.metrics import confusion_matrix , classification_report
from sklearn.metrics import precision_score , recall_score , f1_score
from sklearn.metrics import RocCurveDisplay

df = pd.read_csv("/content/heart-disease (1).csv")
df.shape

df["target"].value_counts()

df["target"].value_counts().plot(kind="bar",color=["salmon","lightblue"]);

df.info()

df.isna().sum()

df.describe()

"""**Heart Diseases Frequency according to Sex**"""

df.sex.value_counts()

pd.crosstab(df.target , df.sex)

pd.crosstab(df.target,df.sex).plot(kind="bar",color=["salmon","lightblue"],
                                   figsize=(10,6))

plt.title("Heart Diseases Frequency for Sex")
plt.xlabel("0 = No Diseases , 1 = Diesases")
plt.ylabel("Amount")
plt.legend(["Female","Male"])
plt.xticks(rotation=0);

"""**Age vs. Max Heart Rate for Heart Disease**"""

plt.figure(figsize=(10,6))

plt.scatter(df.age[df.target==1],df.thalach[df.target==1],color="salmon")

plt.scatter(df.age[df.target==0],df.thalach[df.target==0],color="blue")
plt.title("Heart Disease in function of Age and Max Heart Rate")
plt.xlabel("Age")
plt.ylabel("Max Heart Rate")
plt.legend(["Disease","No Disease"]);

df.age.hist()

"""**Heart Diseases Frequency per Chest Pain Type**"""

pd.crosstab(df.cp,df.target)

pd.crosstab(df.cp,df.target).plot(kind="bar",
                                  figsize=(10,6),
                                  color=["salmon","lightblue"])

plt.title("Heart Diseases Frequency per Chest Pain Type")
plt.xlabel("Chest Pain Type")
plt.ylabel("Amount")
plt.legend(["No Disease","Disease"])
plt.xticks(rotation=0)

df.corr()

corr_metrics = df.corr()
figure , ax = plt.subplots(figsize=(15,12))
ax = sns.heatmap(corr_metrics,
                 annot=True,
                 linewidths=0.5,
                 fmt=".2f",
                 cmap="YlGnBu")

X = df.drop("target", axis=1)
y = df['target']

np.random.seed(42)
X_train,X_test,y_train,y_test = train_test_split(X,y,
                                                 test_size=0.20)

models = {"LogisticRegression": LogisticRegression(),
          "KNN":KNeighborsClassifier(),
          "Random Forest":RandomForestClassifier()}

def fit_and_score(models,X_train,X_test,y_train,y_test):
  np.random.seed(62)
  model_scores = {}
  for name , model in models.items():
    model.fit(X_train,y_train)
    model_scores[name] = model.score(X_test , y_test)
  return model_scores

model_scores = fit_and_score(models=models,
                             X_train=X_train,
                             X_test=X_test,
                             y_train=y_train,
                             y_test=y_test);
model_scores

model_compair = pd.DataFrame(model_scores,index=["accuracy"])
model_compair.T.plot.bar();
plt.xticks(rotation=0)

"""**Hyperparameter Tuning of Model**"""

test_scores = []

neighbors = range(1,21)

knn = KNeighborsClassifier()

for i in neighbors:
  knn.set_params(n_neighbors=i)

  knn.fit(X_train,y_train)

  test_scores.append(knn.score(X_test,y_test))

test_scores

plt.plot(neighbors,test_scores,label="Test Scores")
plt.xticks(np.arange(1,21,1))
plt.xlabel("Number of Neighbors")
plt.ylabel("Model Scores")
plt.legend()

print(f"Maximum KNN score on the test data: {max(test_scores)*100:.2f}%")

"""**Hyperparameter Tuning with RandomizedSearchCV**"""

log_reg_grid = {"C": np.logspace(-4,4,30),
                "solver":["liblinear"]}

rf_grid = {"n_estimators": np.arange(10,1000,50),
           "max_depth": [None,3,5,10],
           "min_samples_split": np.arange(2,20,2),
           "min_samples_leaf": np.arange(1,20,2)}

np.random.seed(42)

rs_log_reg = RandomizedSearchCV(LogisticRegression(),
                           param_distributions=log_reg_grid,
                           cv=5,
                           verbose=True)
rs_log_reg.fit(X_train,y_train)

rs_log_reg.best_params_

rs_log_reg.score(X_test,y_test)

np.random.seed(42)

rs_rf = RandomizedSearchCV(RandomForestClassifier(),
                           param_distributions=rf_grid,
                           cv=5,
                           n_iter=20,
                           verbose=True)
rs_rf.fit(X_train,y_train)

rs_rf.best_params_

rs_rf.score(X_test,y_test)

"""**Hyperparameter Tuning Using GridSearchCV**"""

gs_log_reg = GridSearchCV(LogisticRegression(),
                          param_grid = log_reg_grid,
                          cv=5,
                          verbose=True)
gs_log_reg.fit(X_train,y_train);

gs_log_reg.score(X_test,y_test)

y_preds = gs_log_reg.predict(X_test)

RocCurveDisplay.from_estimator(gs_log_reg,X_test,y_test)

sns.set(font_scale=1.5)
def plot_conf_mat(y_test,y_preds):
  fig ,ax = plt.subplots(figsize=(3,3))
  ax = sns.heatmap(confusion_matrix(y_test,y_preds),
                   annot=True,
                   cbar = False)
  plt.xlabel("True label")
  plt.ylabel("Predicted label")

plot_conf_mat(y_test,y_preds)

print(classification_report(y_test,y_preds))

gs_log_reg.best_params_

clf = LogisticRegression(C=0.23357214690901212,
                         solver='liblinear')

cv_acc = cross_val_score(clf,X,y,cv=5,scoring="accuracy")

cv_acc = cv_acc.mean()
cv_acc

cv_precision = cross_val_score(clf,X,y,cv=5,scoring="precision")
cv_precision = cv_precision.mean()
cv_precision

cv_recall = cross_val_score(clf,X,y,cv=5,scoring="recall")
cv_recall = cv_recall.mean()
cv_recall

cv_f1 = cross_val_score(clf,X,y,cv=5,scoring="f1")
cv_f1 = cv_f1.mean()
cv_f1

cv_metrics = pd.DataFrame({"Accuracy": cv_acc,
                           "Precision": cv_precision,
                           "Recall": cv_recall,
                           "F1": cv_f1},
                          index=[0])

cv_metrics.T.plot.bar(title = "Cross-validation classification metrics",
                      legend = False)

"""**Feature Importance**"""

clf.fit(X_train,y_train)

clf.coef_

feature_dict = dict(zip(df.columns,list(clf.coef_[0])))
feature_dict

feature_df = pd.DataFrame(feature_dict,index=[0])
feature_df.T.plot.bar(title="Feature Importance",legend=False)

!pip install catboost
from catboost import CatBoostClassifier

model = CatBoostClassifier(verbose=0)

model.fit(X_train,y_train)

model.score(X_test,y_test)

!pip install optuna
import optuna

def objective(trial):
    params = {
        "iterations": trial.suggest_int("iterations", 100, 1000),
        "depth": trial.suggest_int("depth", 4, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        "l2_leaf_reg": trial.suggest_int("l2_leaf_reg", 1, 10),
        "verbose": 0
    }

    model = CatBoostClassifier(**params)
    score = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy').mean()
    return score

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

print("Best Params:", study.best_params)

model2 = CatBoostClassifier(iterations= 241, depth= 5, learning_rate= 0.012525868419638625, l2_leaf_reg= 10)

model2.fit(X_train,y_train)

model2.score(X_test,y_test)

import pandas as pd
import numpy as np
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE  # Optional: only if class imbalance

# 🔹 Load your dataset
data = pd.read_csv('/content/heart-disease (1).csv')

# 🔹 Split features and target
X = data.drop('target', axis=1)
y = data['target']

# 🔹 Encode categorical features if needed
cat_cols = X.select_dtypes(include=['object']).columns
for col in cat_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))

# 🔹 Optional: Use SMOTE for imbalanced data
use_smote = True
if use_smote:
    smote = SMOTE(random_state=42)
    X, y = smote.fit_resample(X, y)

# 🔹 Initialize Stratified K-Fold
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 🔹 Store scores
f1_scores = []
acc_scores = []

# 🔹 Training and Evaluation Loop
for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
    print(f"\n📂 Fold {fold+1}")
    X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

    # Train CatBoost
    model = CatBoostClassifier(
        iterations=300,
        learning_rate=0.05,
        depth=6,
        l2_leaf_reg=3,
        eval_metric='F1',
        verbose=0,
        random_seed=42
    )
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_val)

    # Evaluate
    acc = accuracy_score(y_val, y_pred)
    f1 = f1_score(y_val, y_pred, average='weighted')
    print(f"✅ Accuracy: {acc:.4f}, F1-Score: {f1:.4f}")

    f1_scores.append(f1)
    acc_scores.append(acc)

# 🔹 Final Results
print("\n📊 Cross-Validation Results:")
print(f"Mean Accuracy: {np.mean(acc_scores):.4f}")
print(f"Mean F1-Score: {np.mean(f1_scores):.4f}")

# 🔹 Feature Importance
import matplotlib.pyplot as plt

importances = model.get_feature_importance()
features = X.columns

plt.figure(figsize=(10, 6))
plt.barh(features, importances)
plt.xlabel("Feature Importance")
plt.title("CatBoost Feature Importance")
plt.show()

