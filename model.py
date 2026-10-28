import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

pw = quote_plus("YOUR_PASSWORD")
engine = create_engine(f"mysql+pymysql://root:{pw}@localhost/credit_risk")
df = pd.read_sql("SELECT * FROM loans_clean", engine)

X = df.drop(columns="loan_status")
y = df["loan_status"]

num_cols = X.select_dtypes("number").columns
cat_cols = X.select_dtypes("object").columns

prep = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(drop="first"), cat_cols)
])

model = Pipeline([
    ("prep", prep),
    ("lr", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

model.fit(X_train, y_train)
pred = model.predict(X_test)
prob = model.predict_proba(X_test)[:, 1]

print("Accuracy:", round(accuracy_score(y_test, pred), 3))
print("ROC-AUC:", round(roc_auc_score(y_test, prob), 3))
print(classification_report(y_test, pred))

# Top risk factors
names = model.named_steps["prep"].get_feature_names_out()
coef = pd.Series(model.named_steps["lr"].coef_[0], index=names).sort_values()
print(coef.tail(8))
print(coef.head(5))

coef.plot(kind="barh", figsize=(8, 8), title="Risk factors (positive = more default)")
plt.tight_layout()
plt.savefig("P:/credit card default/risk_factors.png")

# Save results for Power BI
df["default_probability"] = model.predict_proba(X)[:, 1]
df.to_csv("P:/credit card default/loans_scored.csv", index=False)
coef.rename("coefficient").to_csv("P:/credit card default/risk_factors.csv")