import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Define products list
products = ['Smartphones', 'Laptops', 'Headphones', 'Tablets', 'Smartwatches']

# Load the dataset
data = pd.read_csv('../datasets/customer_behavior_vip.csv')

# Step 1: Prepare features and target
X = data[['TotalSpend', 'PurchaseFrequency', 'PreferredProduct']]
y = data['IsVIP']

# Step 2: Create preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), ['PreferredProduct']),
        ('num', 'passthrough', ['TotalSpend', 'PurchaseFrequency'])
    ])

# Step 3: Create and train model pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])
model.fit(X, y)

# Step 4: Calculate accuracy
accuracy = model.score(X, y)

# Step 5: Save the model
model_filename = '../models/customervipcheck/vip_model.joblib'
joblib.dump(model, model_filename)

# Step 6: Print model details
feature_names = (model.named_steps['preprocessor']
                 .named_transformers_['cat']
                 .get_feature_names_out(['PreferredProduct'])
                 .tolist() + ['TotalSpend', 'PurchaseFrequency'])
importances = model.named_steps['classifier'].feature_importances_
print("\nVIP Prediction Model:")
for name, importance in zip(feature_names, importances):
    print(f"Feature Importance: {name} = {importance:.4f}")
print(f"Accuracy: {accuracy:.4f}")
print(f"Model saved as: {model_filename}")


# Step 7: Prediction function
def predict_vip(total_spend, purchase_frequency, preferred_product):
    # Validate inputs
    if not isinstance(total_spend, (int, float)) or total_spend < 0:
        return f"Error: TotalSpend must be a non-negative number, got {total_spend}"
    if not isinstance(purchase_frequency, (int, float)) or purchase_frequency < 0:
        return f"Error: PurchaseFrequency must be a non-negative number, got {purchase_frequency}"
    if preferred_product not in products:
        return f"Error: Invalid product. Choose from {products}"

    # Create input DataFrame
    X_pred = pd.DataFrame({
        'TotalSpend': [total_spend],
        'PurchaseFrequency': [purchase_frequency],
        'PreferredProduct': [preferred_product]
    })

    # Predict
    is_vip = model.predict(X_pred)[0]
    recommendation = "Offer VIP status and exclusive perks." if is_vip else "Do not offer VIP status yet."
    return f"Prediction for customer (Spend=${total_spend:.2f}, Freq={purchase_frequency:.2f}/year, Product={preferred_product}): {'VIP' if is_vip else 'Non-VIP'}. {recommendation}"


# Step 8: Example usage with user input
def get_user_prediction():
    try:
        preferred_product = input("Enter preferred product (Smartphones, Laptops, Headphones, Tablets, Smartwatches): ")
        total_spend = float(input("Enter total spend (USD): "))
        purchase_frequency = float(input("Enter purchase frequency (purchases/year): "))

        result = predict_vip(total_spend, purchase_frequency, preferred_product)
        print(result)
    except ValueError:
        print("Error: Please enter valid numeric values")


# Run example predictions
print("\nRunning example predictions:")
print(predict_vip(4000, 2.0, 'Smartphones'))
print(predict_vip(1000, 0.5, 'Headphones'))
print(predict_vip(3500, 1.8, 'Laptops'))

