# Heart_Diseases_Prediction_Model


---

### 📁 `heart_disease_project` – [README.md]

```markdown

This project aims to **predict the presence of heart disease** in a patient using machine learning classification algorithms on structured health data.

## 🧠 Problem Statement

Given patient medical attributes, predict whether or not they are at risk of heart disease.

## 📂 Dataset

Dataset: `heart-disease.csv`

Features include:
- Age
- Sex
- Chest pain type
- Blood pressure
- Cholesterol levels
- Heart rate
- Exercise-induced angina
- and more...

## 🧪 Models Used

- Logistic Regression
- K-Nearest Neighbors (KNN)
- Random Forest Classifier
- CatBoost Classifier
- Hyperparameter tuning with:
  - GridSearchCV
  - RandomizedSearchCV
  - Optuna

## 🔍 Key Techniques

- Exploratory Data Analysis
- Data Visualization using Seaborn & Matplotlib
- Feature Engineering
- SMOTE for class imbalance
- Cross-validation
- ROC Curve, Confusion Matrix, Precision, Recall, F1-score

## 🔥 Advanced Techniques

- **CatBoostClassifier**: for handling categorical data effectively
- **Optuna**: for efficient hyperparameter tuning
- **StratifiedKFold**: for better model evaluation

## 📊 Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

## 📈 Visualizations

- Age vs. Max Heart Rate
- Heart Disease Frequency by Sex
- Chest Pain vs. Disease Presence
- Correlation Heatmaps

## 📁 Output

- Classification reports
- Feature importances
- Trained models

## 🚀 How to Run

```bash
# Install dependencies
pip install pandas numpy seaborn scikit-learn catboost optuna imbalanced-learn

# Run the script
python heart_disease_project.py
