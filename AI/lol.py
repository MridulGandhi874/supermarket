import pandas as pd

data = pd.read_csv('../datasets/electronics_sales.csv')
print(data.head())
data["Sales"] = (data["Sales"]/10).astype(int)
data.to_csv('../datasets/electronics_sales_updated.csv', index=False)
