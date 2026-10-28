import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.parse import quote_plus
from sqlalchemy import create_engine

pw = quote_plus("YOUR_PASSWORD")
engine = create_engine(f"mysql+pymysql://root:{pw}@localhost/credit_risk")
df = pd.read_sql("SELECT * FROM loans_clean", engine)
print(df.shape)

# Which numbers move with default?
num = df.select_dtypes("number")
corr = num.corr()["loan_status"].drop("loan_status").sort_values()
print(corr)

# Chart 1: correlation with default
corr.plot(kind="barh", title="Correlation with default")
plt.tight_layout()
plt.savefig("P:/credit card default/corr.png")
plt.close()

# Chart 2: default rate by home ownership
df.groupby("person_home_ownership")["loan_status"].mean().mul(100).plot(
    kind="bar", title="Default rate % by home ownership")
plt.tight_layout()
plt.savefig("P:/credit card default/home.png")

# Past default on file
print(df.groupby("cb_person_default_on_file")["loan_status"].mean() * 100)