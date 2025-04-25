from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load the dataset
data = pd.read_csv('../datasets/electronics_sales.csv')  # Replace with 'train.csv' if needed

# Step 1: Create separate DataFrames for each product
phones = data[data['Product'] == 'Smartphones'].copy()
laptops = data[data['Product'] == 'Laptops'].copy()
headphones = data[data['Product'] == 'Headphones'].copy()
tablets = data[data['Product'] == 'Tablets'].copy()
smartwatches = data[data['Product'] == 'Smartwatches'].copy()

# Step 2: Train Random Forest models, save them, and store them
dfs = [
    (phones, 'Smartphones'),
    (laptops, 'Laptops'),
    (headphones, 'Headphones'),
    (tablets, 'Tablets'),
    (smartwatches, 'Smartwatches')
]

# Dictionary to store models
models = {}

for df, product_name in dfs:
    # Feature engineering
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    # Prepare features (X) and target (y)
    X = df[['Year', 'Month']]
    y = df['Sales']

    # Train Random Forest model
    # model = RandomForestRegressor(n_estimators=100, random_state=42)
    model = LinearRegression()
    model.fit(X, y)

    # Calculate R² score
    r2_score = model.score(X, y)

    # Save the model to a file
    model_filename = f"{product_name.lower()}_model.joblib"
    joblib.dump(model, model_filename)

    # Store model in dictionary
    models[product_name] = model

    # Print model details
    print(f"\nModel for {product_name}:")
    # print(
    #     f"Feature Importances: Year = {model.feature_importances_[0]:.4f}, Month = {model.feature_importances_[1]:.4f}")
    # print(f"R² Score: {r2_score:.4f}")
    print(f"Model saved as: {model_filename}")


# Step 3: Prediction function
def predict_sales(month, year, product):

    if not isinstance(month, int) or month < 1 or month > 12:
        return f"Error: Month must be an integer between 1 and 12, got {month}"
    if not isinstance(year, int):
        return f"Error: Year must be an integer, got {year}"
    if product not in models:
        return f"Error: Invalid product. Choose from {list(models.keys())}"

    # Get the model for the product
    model = models[product]

    # Predict sales using DataFrame to match training feature names
    X_pred = pd.DataFrame({'Year': [year], 'Month': [month]})
    prediction = model.predict(X_pred)[0]

    return round(prediction, 2)


# Step 4: Example usage with user input
def get_user_prediction():
    try:
        product = input("Enter product (Smartphones, Laptops, Headphones, Tablets, Smartwatches): ")
        month = int(input("Enter month (1-12): "))
        year = int(input("Enter year: "))

        result = predict_sales(month, year, product)
        if isinstance(result, str):  # Error message
            print(result)
        else:
            print(f"Predicted sales for {product} in {year}-{month:02d}: {result} units")
    except ValueError:
        print("Error: Please enter valid numeric values for month and year")


# Run example predictions
print("\nRunning example predictions:")
print(f"Smartphones, Jan 2025: {predict_sales(1, 2025, 'Smartphones')} units")
print(f"Laptops, Dec 2025: {predict_sales(12, 2025, 'Laptops')} units")
print(f"Headphones, Jun 2024: {predict_sales(6, 2024, 'Headphones')} units")
