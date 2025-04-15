import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Sales Data Calculations
electronic_sales = pd.read_csv('datasets/electronics_sales_updated.csv')

smartphone_cost = 40000
laptop_cost = 75000
tablet_cost = 30000
headphones_cost = 10000
smartwatch_cost = 5000

total_orders = sum(electronic_sales['Sales'])

total_smartphone_sales = electronic_sales[electronic_sales["Product"] == "Smartphones"]["Sales"].sum()
total_laptop_sales = electronic_sales[electronic_sales["Product"] == "Laptops"]["Sales"].sum()
total_tablet_sales = electronic_sales[electronic_sales["Product"] == "Tablets"]["Sales"].sum()
total_headphones_sales = electronic_sales[electronic_sales["Product"] == "Headphones"]["Sales"].sum()
total_smartwatch_sales = electronic_sales[electronic_sales["Product"] == "Smartwatches"]["Sales"].sum() if "Smartwatches" in electronic_sales["Product"].unique() else 0

total_revenue_cpy = (
    total_smartphone_sales * smartphone_cost +
    total_laptop_sales * laptop_cost +
    total_tablet_sales * tablet_cost +
    total_headphones_sales * headphones_cost +
    total_smartwatch_sales * smartwatch_cost
)

total_revenue = total_revenue_cpy // 10000000

# Customer Data
customers = pd.read_csv('datasets/customer_behavior_vip.csv')
num_customers = len(customers)

# Average Order Value
avg_order = round(total_revenue_cpy / num_customers, 2)

# Stock Management
stock = pd.read_csv('datasets/item_stock_dataset.csv')
laptops_stock = stock.loc[stock['item'] == 'Laptops', 'stock'].values[0]
tablets_stock = stock.loc[stock['item'] == 'Tablets', 'stock'].values[0]
mobiles_stock = stock.loc[stock['item'] == 'Mobiles', 'stock'].values[0]
smartwatches_stock = stock.loc[stock['item'] == 'Smartwatches', 'stock'].values[0]
headphones_stock = stock.loc[stock['item'] == 'Headphones', 'stock'].values[0]

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017")
db = client["shop_app"]
users_collection = db["users"]

# Streamlit Page Config
st.set_page_config(layout="wide")

# Session Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"
if "dashboard_page" not in st.session_state:
    st.session_state.dashboard_page = "overview"  # Default to Dashboard Overview

# Home Dashboard
def show_home():
    # Custom CSS Styling
    st.markdown(
        """
        <style>
        html, body {
            overflow: hidden !important;
            margin: 0;
            padding: 0;
            height: 100vh;
        }
        .stApp {
            background-color: #000000;
            color: #ffffff;
            height: 100vh;
            overflow: hidden;
        }
        .container {
            display: flex;
            flex-direction: row;
            height: 100%;
            overflow: hidden;
        }
        .side-panel {
            width: 250px;
            background-color: #1a1a1a;
            padding: 0 20px; /* Adjusted padding to remove top space */
            color: white;
            box-shadow: 2px 0 5px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            height: 100%;
            overflow: hidden;
        }
        .menu-item {
            margin: 15px 0;
            color: #bbb;
            font-size: 1rem;
            cursor: pointer;
            background: none;
            border: none;
            padding: 0;
            text-align: left;
            width: 100%;
        }
        .menu-item:hover {
            color: #fff;
        }
        .main-content {
            flex: 1;
            padding: 20px;
            color: white;
            background-color: black;
            height: 100%;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        .stats-container {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 10px;
            flex: 1;
        }
        .stock-container {
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
            margin-top: 20px;
            flex: 1;
        }
        .stat-card, .stock-card {
            background-color: #222;
            padding: 15px;
            border-radius: 10px;
            min-width: 200px;
            height: 120px; /* Adjusted to fit stats without overflow */
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
        }
        .stock-card {
            height: 300px; /* Adjusted to fit stock list */
        }
        .stat-card h3, .stock-card h3 {
            margin-bottom: 5px;
            font-size: 1rem;
            color: #ddd;
        }
        .stat-card p, .stock-card p {
            font-size: 1.1rem; /* Reduced to fit content */
            font-weight: bold;
            margin: 0;
            color: #fff;
        }
        .stock-card .stock-list {
            list-style-type: none;
            padding: 0;
            margin-top: 10px;
            text-align: left;
            font-size: 0.9rem;
            color: #fff;
            overflow: hidden;
        }
        .stock-card .stock-list li {
            margin: 5px 0; /* Reduced margin to fit all items */
        }
        h2 {
            text-align: center;
            font-size: 1.5rem;
            margin-bottom: 10px;
        }
        .stock-container h2::before {
            content: "📦 ";
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Navigation Buttons in the Side Panel (using Streamlit buttons)
    with st.sidebar:
        st.markdown("<div class='side-panel'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; font-size: 1.2rem; margin: 0;'>SYS MART</h3>", unsafe_allow_html=True)
        st.markdown("<div style='color: #bbb; font-size: 1.5rem; font-weight: bold; font-family: \"Segoe UI\", sans-serif; margin: 0 0 20px 0;'>COMBINES SYSTEM AND MART</div>", unsafe_allow_html=True)
        if st.button("📊 Dashboard", key="btn_overview"):
            st.session_state.dashboard_page = "overview"
            st.rerun()
        if st.button("🛒 Stock", key="btn_stock"):
            st.session_state.dashboard_page = "stock"
            st.rerun()
        if st.button("🛍️ Future Trends", key="btn_future_trends"):
            st.session_state.dashboard_page = "future_trends"
            st.rerun()
        if st.button("👥 Employees", key="btn_employees"):
            st.session_state.dashboard_page = "employees"
            st.rerun()
        if st.button("🧾 Generate Bill", key="btn_generate_bill"):
            st.session_state.dashboard_page = "generate_bill"
            st.rerun()
        if st.button("💎 VIP Customers", key="btn_vip_customers"):
            st.session_state.dashboard_page = "vip_customers"
            st.rerun()
        if st.button("⚙️ Settings", key="btn_settings"):
            st.session_state.dashboard_page = "settings"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Dashboard Content based on selected page
    if st.session_state.dashboard_page == "overview":
        html_content = f"""
            <div class='main-content'>
                <h2>📊 Dashboard Overview</h2>
                <div class='stats-container'>
                    <div class='stat-card'>
                        <h3>Total Revenue</h3>
                        <p>₹{total_revenue} crores</p>
                    </div>
                    <div class='stat-card'>
                        <h3>Total Orders</h3>
                        <p>{total_orders}</p>
                    </div>
                    <div class='stat-card'>
                        <h3>Total Unique Customers</h3>
                        <p>{num_customers}</p>
                    </div>
                    <div class='stat-card'>
                        <h3>Avg. Order Value</h3>
                        <p>₹{avg_order}</p>
                    </div>
                </div>
                <h2>Stocks Overview</h2>
                <div class='stock-container'>
                    <div class='stock-card'>
                        <h3>Total Stocks Available</h3>
                        <ul class='stock-list'>
                            <li>Laptops: {laptops_stock}</li>
                            <li>Tablets: {tablets_stock}</li>
                            <li>Mobiles: {mobiles_stock}</li>
                            <li>Smartwatches: {smartwatches_stock}</li>
                            <li>Headphones: {headphones_stock}</li>
                        </ul>
                    </div>
                </div>
            </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
    elif st.session_state.dashboard_page == "stock":
        html_content = f"""
            <div class='main-content'>
                <h2>🛒 Stock</h2>
                <div class='stock-container'>
                    <div class='stock-card'>
                        <h3>Current Stock Levels</h3>
                        <ul class='stock-list'>
                            <li>Laptops: {laptops_stock}</li>
                            <li>Tablets: {tablets_stock}</li>
                            <li>Mobiles: {mobiles_stock}</li>
                            <li>Smartwatches: {smartwatches_stock}</li>
                            <li>Headphones: {headphones_stock}</li>
                        </ul>
                    </div>
                </div>
            </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

        # Add Stock Form using Streamlit
        with st.form(key="add_stock_form"):
            item = st.selectbox("Select Item", ["Laptops", "Tablets", "Mobiles", "Smartwatches", "Headphones"])
            quantity = st.number_input("Enter Quantity to Add", min_value=1, step=1, value=1)
            submit_button = st.form_submit_button(label="Add Stock")

        # Handle form submission
        if submit_button:
            stock_index = stock[stock['item'] == item].index
            if not stock_index.empty:
                stock.loc[stock_index, 'stock'] += quantity
                stock.to_csv('datasets/item_stock_dataset.csv', index=False)
                # Update local variables
                globals()[f"{item.lower()}_stock"] = stock.loc[stock['item'] == item, 'stock'].values[0]
                st.success(f"✅ Successfully added {quantity} units to {item} stock.")
            else:
                st.error("Item not found in stock dataset.")
            st.rerun()

    elif st.session_state.dashboard_page == "future_trends":
        import joblib
        # HTML content for the page
        html_content = f"""
            <div class='main-content'>
                <h2>🛍️ Future Trends</h2>
                <div class='stock-container'>
                    <div class='stock-card'>
                        <h3>Future Sales Prediction</h3>
                    </div>
                </div>
            </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

        # User input for prediction
        with st.form(key="future_trends_form"):
            product = st.selectbox("Select Product", ["Headphones", "Laptops", "Smartphones", "Smartwatches", "Tablets"])
            month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12, value=1)
            year = st.number_input("Enter Year", min_value=2025, max_value=2030, value=2025)
            predict_button = st.form_submit_button(label="Predict")

        # Load the appropriate model and predict on button click
        if predict_button:
            model_path = f"models/sales/{product.lower()}_model.joblib"
            model = joblib.load(model_path)
            # prediction = model.predict(year=year, month=month)
            prediction = model.predict([[month, year]])
            # Display prediction in styled HTML
            prediction_html = f"""
                                <div class='stock-container'>
                                    <div class='stock-card'>
                                        <h3>Prediction Result</h3>
                                        <p>Future Sales: {round(prediction[0])} units</p>
                                    </div>
                                </div>
                            """
            st.markdown(prediction_html, unsafe_allow_html=True)

    elif st.session_state.dashboard_page == "employees":
        html_content = f"""
            <div class='main-content'>
                <h2>👥 Employees</h2>
                <div class='stock-container'>
                    <div class='stock-card'>
                        <h3>Employee Details</h3>
                        <p>Employee management content here.</p>
                    </div>
                </div>
            </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
    elif st.session_state.dashboard_page == "generate_bill":
        html_content = f"""
            <div class='main-content'>
                <h2>🧾 Generate Bill</h2>
                <div class='stock-container'>
                    <div class='stock-card'>
                        <h3>Bill Generation</h3>
                        <p>Bill generation content here.</p>
                    </div>
                </div>
            </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
    elif st.session_state.dashboard_page == "vip_customers":
        html_content = f"""
            <div class='main-content'>
                <h2>💎 VIP Customers</h2>
                <div class='stock-container'>
                    <div class='stock-card'>
                        <h3>VIP Customers</h3>
                        <p>VIP customer content here.</p>
                    </div>
                </div>
            </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
    elif st.session_state.dashboard_page == "settings":
        html_content = f"""
            <div class='main-content'>
                <h2>⚙️ Settings</h2>
                <div class='stock-container'>
                    <div class='stock-card'>
                        <h3>Settings</h3>
                        <p>Settings content here.</p>
                    </div>
                </div>
            </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

# Registration Page
def register_page():
    st.title("🔐 Register")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if users_collection.find_one({"email": email}):
            st.warning("Email already registered.")
        else:
            users_collection.insert_one({"name": name, "email": email, "password": password})
            st.success("Registration successful! Please login.")
            st.session_state.page = "login"
    if st.button("Back to Login"):
        st.session_state.page = "login"

# Login Page
def login_page():
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = users_collection.find_one({"email": email, "password": password})
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success(f"Welcome, {user['name']}!")
            st.rerun()
        else:
            st.error("Invalid email or password.")
    if st.button("Go to Register"):
        st.session_state.page = "register"

# Page Routing
if st.session_state.logged_in:
    show_home()
elif st.session_state.page == "register":
    register_page()
else:
    login_page()