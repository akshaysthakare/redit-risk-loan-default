# credit-risk-loan-default

# Bank Loan Default (Credit Risk) Analysis
Tools: MySQL, Python (Pandas, scikit-learn), Power BI
Data: Kaggle Credit Risk Dataset (32K loans)

## Key findings
- Loans above 30% of income default at 65.6% (vs 11.6% under 10%)
- Income under 30K defaults at 47% (vs 9% for 100K+)
- Logistic Regression: ROC-AUC 0.87, catches 78% of defaulters

## Recommendation
Cap loans at 30% of income and apply stricter checks to loan grades D to G.
