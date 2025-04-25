import pandas as pd
import numpy as np

from AI.customertraining import accuracy

# Settings
np.random.seed(42)
products = ['Smartphones', 'Laptops', 'Headphones', 'Tablets', 'Smartwatches']
num_customers = 10000
years = list(range(2005, 2025))
base_prices = {'Smartphones': 400, 'Laptops': 1000, 'Headphones': 100, 'Tablets': 500, 'Smartwatches': 250}
price_ranges = {'Smartphones': (200, 1000), 'Laptops': (500, 2000), 'Headphones': (50, 300),
                'Tablets': (300, 800), 'Smartwatches': (150, 500)}
product_weights = {'Smartphones': 0.4, 'Laptops': 0.2, 'Headphones': 0.25, 'Tablets': 0.1, 'Smartwatches': 0.05}

data = []

for customer_id in range(1, num_customers + 1):
    num_purchases = np.random.randint(1, 21)
    purchase_years = np.random.choice(years, size=num_purchases, replace=True)
    purchase_years.sort()
    first_year = min(purchase_years)
    active_years = max(purchase_years) - first_year + 1 if purchase_years.size > 0 else 1

    total_spend = 0
    product_counts = {p: 0 for p in products}
    for year in purchase_years:
        product = np.random.choice(products, p=[product_weights[p] for p in products])
        if product == 'Tablets' and year < 2010:
            product = np.random.choice(['Smartphones', 'Laptops', 'Headphones'])
        if product == 'Smartwatches' and year < 2015:
            product = np.random.choice(['Smartphones', 'Laptops', 'Headphones'])
        base_price = np.random.uniform(price_ranges[product][0], price_ranges[product][1])
        price = base_price * (1 + 0.02) ** (year - 2005)
        total_spend += price
        product_counts[product] += 1

    total_spend = round(total_spend, 2)
    purchase_frequency = round(num_purchases / active_years, 2)
    preferred_product = max(product_counts, key=product_counts.get)

    is_vip = 1 if total_spend > 3000 or purchase_frequency > 1.5 else 0
    if np.random.random() < 0.1:
        is_vip = 1 - is_vip

    data.append([customer_id, total_spend, purchase_frequency, preferred_product, is_vip])

# Save dataset
df = pd.DataFrame(data, columns=['CustomerID', 'TotalSpend', 'PurchaseFrequency', 'PreferredProduct', 'IsVIP'])
df.to_csv('customer_behavior_vip.csv', index=False)
print("Dataset saved as customer_behavior_vip.csv")