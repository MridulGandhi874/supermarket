import streamlit as st
import pandas as pd
import joblib
from pymongo import MongoClient
from fpdf import FPDF
import time
import traceback
import sys



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
    st.session_state.dashboard_page = "overview"
if "employees" not in st.session_state:
    st.session_state.employees = pd.read_csv('datasets/employee_dataset.csv')

# Function to generate PDF bill
def generate_bill_pdf(customer_name, product, quantity, price_per_unit, total_cost):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="SYS MART", ln=1, align='C')
    pdf.cell(200, 10, txt=f"Customer: {customer_name}", ln=1, align='L')
    pdf.cell(200, 10, txt=f"Product: {product}", ln=1, align='L')
    pdf.cell(200, 10, txt=f"Quantity: {quantity}", ln=1, align='L')
    pdf.cell(200, 10, txt=f"Price per Unit: Rs. {price_per_unit:,}", ln=1, align='L')
    pdf.cell(200, 10, txt=f"Total Cost: Rs. {total_cost:,}", ln=1, align='L')
    return pdf.output(dest='S').encode('latin1')

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
            padding: 0 20px;
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
            height: auto;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
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
            margin: 5px 0;
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

    # Navigation Buttons in the Side Panel
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

    # Dashboard Content
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

        with st.form(key="add_stock_form"):
            item = st.selectbox("Select Item", ["Laptops", "Tablets", "Mobiles", "Smartwatches", "Headphones"])
            quantity = st.number_input("Enter Quantity to Add", min_value=1, step=1, value=1)
            submit_button = st.form_submit_button(label="Add Stock")

        if submit_button:
            stock_index = stock[stock['item'] == item].index
            if not stock_index.empty:
                stock.loc[stock_index, 'stock'] += quantity
                stock.to_csv('datasets/item_stock_dataset.csv', index=False)
                globals()[f"{item.lower()}_stock"] = stock.loc[stock['item'] == item, 'stock'].values[0]
                st.success(f"✅ Successfully added {quantity} units to {item} stock.")
            else:
                st.error("Item not found in stock dataset.")
            st.rerun()

    elif st.session_state.dashboard_page == "future_trends":
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

        with st.form(key="future_trends_form"):
            product = st.selectbox("Select Product", ["Headphones", "Laptops", "Smartphones", "Smartwatches", "Tablets"])
            month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12, value=1)
            year = st.number_input("Enter Year", min_value=2025, max_value=2030, value=2025)
            predict_button = st.form_submit_button(label="Predict")

        selected_product = product
        selected_month = month

        if predict_button:
            model_path = f"models/sales/{selected_product.lower()}_model.joblib"
            try:
                model = joblib.load(model_path)
                # Prepare input data with all expected features (value, Year, Month)
                # input_data = pd.DataFrame([[0, year, month]], columns=["value", "Year", "Month"])
                input_data = pd.DataFrame({'Year': [year], 'Month': [month]})
                prediction = model.predict(input_data)[0]
                prediction_html = f"""
                    <div class='stock-container'>
                        <div class='stock-card'>
                            <h3>Prediction Result</h3>
                            <p>Predicted sales for {selected_product} in {selected_month}/{year}: {int(prediction)} units</p>
                        </div>
                    </div>
                """
                st.markdown(prediction_html, unsafe_allow_html=True)
            except Exception as e:
                print("Error type:", type(e).__name__)
                print("Error message:", e)
                tb = sys.exc_info()[2]
                print("Line number:", tb.tb_lineno)
                print("Full traceback:")
                traceback.print_exc()
                prediction_html = f"""
                    <div class='stock-container'>
                        <div class='stock-card'>
                            <h3>Prediction Result</h3>
                            <p>Unable to predict due to an error: {str(e)}</p>
                        </div>
                    </div>
                """
                st.markdown(prediction_html, unsafe_allow_html=True)


    elif st.session_state.dashboard_page == "employees":

        employees = st.session_state.employees.copy()

        html_content = f"""

            <div class='main-content'>

                <h2>👥 Employees</h2>

                <div class='stock-container'>

                    <div class='stock-card'>

                        <h3>Current Employees</h3>

                    </div>

                </div>

            </div>

        """

        st.markdown(html_content, unsafe_allow_html=True)

        employees_with_index = employees.reset_index(drop=True)

        employees_with_index.index = employees_with_index.index + 1

        st.table(employees_with_index)

        with st.form(key="remove_employee_form"):

            remove_name = st.selectbox("Select Employee to Remove", [''] + employees['Name'].tolist(), index=0)

            remove_button = st.form_submit_button(label="Remove Employee")

        if remove_button and remove_name:
            employees = employees[employees['Name'] != remove_name]

            employees.to_csv('datasets/employee_dataset.csv', index=False)

            st.session_state.employees = employees

            st.success(f"✅ Removed {remove_name} from employees.")

            st.rerun()

        with st.form(key="add_employee_form"):

            name = st.text_input("Name")

            email = st.text_input("Email ID")

            years_exp = st.number_input("Years of Experience", min_value=0, step=1, value=0)

            education = st.selectbox("Education Level", ["High School", "Bachelor's", "Master's", "PhD"])

            skill_score = st.number_input("Skill Score (0-100)", min_value=0, max_value=100, step=1, value=50)

            certifications = st.text_input("Certifications (comma-separated)", value="0")

            add_button = st.form_submit_button(label="Add Candidate")

        if add_button and name and email:

            certs = certifications.split(",")[0].strip() if certifications else "0"

            try:

                certs_numeric = int(certs)

            except ValueError:

                certs_numeric = 0

            input_data = pd.DataFrame([[years_exp, education, skill_score, certs_numeric]],

                                      columns=["YearsExperience", "EducationLevel", "SkillScore", "Certifications"])

            try:
                model = joblib.load("models/employeehire/hire_model.joblib")

                prediction = model.predict(input_data)[0]

                st.write(f"Predicted Hire Score: {prediction:.2f}")

                if st.button("Accept Candidate"):
                    print("Accepted Candidate trigger")
                    new_employee = pd.DataFrame({
                        "Name": [name],
                        "EmailID": [email],
                        "YearsExperience": [years_exp],
                        "EducationLevel": [education],
                        "SkillScore": [skill_score],
                        "Certifications": [certs_numeric]
                    })
                    # Debug: Print new_employee to verify data
                    print("New employee data:", new_employee.to_string())
                    # Concatenate and update employees
                    employees = pd.concat([employees, new_employee], ignore_index=True)
                    # Debug: Print updated employees to verify concatenation
                    print("Updated employees:", employees.to_string())
                    # Save to CSV with explicit encoding to avoid issues
                    employees.to_csv('datasets/employee_dataset.csv', index=True)
                    # Verify file write
                    try:
                        loaded_employees = pd.read_csv('datasets/employee_dataset.csv')
                        print("Loaded from CSV:", loaded_employees.to_string())
                        if name in loaded_employees['Name'].values:
                            st.session_state.employees = employees
                            st.success(f"✅ Added {name} to employees. File updated.")
                        else:
                            st.error("Failed to verify employee in CSV after save.")
                    except Exception as e:

                        st.error(f"Error verifying CSV write: {str(e)}")

                    st.rerun()

                if st.button("Reject Candidate"):
                    st.write("Candidate rejected. Displaying current employees.")

            except Exception as e:

                st.error(f"Error loading model or predicting: {str(e)}")

    elif st.session_state.dashboard_page == "generate_bill":
        html_content = f"""
            <div class='main-content'>
                <h2>🧾 Generate Bill</h2>
                <div class='stock-container'>
                    <div class='stock-card'>
                        <h3>Generate Bill</h3>
                    </div>
                </div>
            </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

        with st.form(key="generate_bill_form"):
            customer_name = st.text_input("Customer Name")
            product = st.selectbox("Select Product", ["Smartphones", "Laptops", "Tablets", "Headphones", "Smartwatches"])
            quantity = st.number_input("Quantity", min_value=1, step=1, value=1)
            generate_button = st.form_submit_button(label="Generate Bill")

        if generate_button:
            price_per_unit = {
                "Smartphones": smartphone_cost,
                "Laptops": laptop_cost,
                "Tablets": tablet_cost,
                "Headphones": headphones_cost,
                "Smartwatches": smartwatch_cost
            }.get(product, 0)
            total_cost = price_per_unit * quantity

            bill_html = f"""
                <div class='stock-container'>
                    <div class='stock-card'>
                        <h3>Bill for {customer_name}</h3>
                        <ul class='stock-list'>
                            <li>Product: {product}</li>
                            <li>Quantity: {quantity}</li>
                            <li>Price per Unit: ₹{price_per_unit:,}</li>
                            <li>Total Cost: ₹{total_cost:,}</li>
                        </ul>
                    </div>
                </div>
            """
            st.markdown(bill_html, unsafe_allow_html=True)

            pdf_bytes = generate_bill_pdf(customer_name, product, quantity, price_per_unit, total_cost)
            st.download_button(
                label="Download Bill",
                data=pdf_bytes,
                file_name="bill.pdf",
                mime="application/pdf"
            )

    elif st.session_state.dashboard_page == "vip_customers":
        st.markdown(
            f"""
            <div class='main-content'>
                <h2>💎 VIP Customers</h2>
                <div class='stock-container'>
                    <div class='stock-card'>
                        <h3>Check VIP Status</h3>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form(key="vip_customer_form"):
            total_spend = st.number_input("Total Spend (₹)", min_value=0.0, step=100.0)
            purchase_frequency = st.number_input("Purchase Frequency (per month)", min_value=0.0, step=0.1)
            preferred_product = st.selectbox("Preferred Product", ["Smartphones", "Laptops", "Tablets", "Headphones", "Smartwatches"])
            submit_button = st.form_submit_button(label="Check VIP Status")

        if submit_button:
            # Map preferred product to numerical value
            product_mapping = {
                "Smartphones": 0,
                "Laptops": 1,
                "Tablets": 2,
                "Headphones": 3,
                "Smartwatches": 4
            }
            preferred_product_encoded = product_mapping.get(preferred_product, -1)

            if preferred_product_encoded == -1:
                st.error("Invalid preferred product selected.")
            else:
                # Prepare input data for the model
                # input_data = pd.DataFrame(
                #     [[total_spend, purchase_frequency, preferred_product_encoded]],
                #     columns=["TotalSpend", "PurchaseFrequency", "PreferredProduct"]
                # )
                input_data = pd.DataFrame({
                    'TotalSpend': [total_spend],
                    'PurchaseFrequency': [purchase_frequency],
                    'PreferredProduct': [preferred_product]
                })

                try:
                    model = joblib.load("models/customervipcheck/vip_model.joblib")
                    prediction = model.predict(input_data)[0]

                    # Load existing customer data
                    customer_data = pd.read_csv('datasets/customer_behavior_vip.csv')

                    # Get the last index and CustomerID
                    last_index = customer_data.index[-1]  # Use the last index of the DataFrame
                    last_customer_id = customer_data.iloc[-1]["CustomerID"]

                    # Prepare input_data
                    input_data["IsVIP"] = prediction
                    input_data["CustomerID"] = last_customer_id + 1
                    input_data.index = [last_index + 1]  # Set the index for input_data

                    # Concatenate the data
                    customer_data = pd.concat([customer_data, input_data])

                    # Save to CSV without the index column
                    customer_data.to_csv('datasets/customer_behavior_vip.csv', index=False)

                    if prediction == 1:
                        st.success("This customer should be made a VIP!")
                    else:
                        st.info("This customer does not qualify as a VIP.")
                except Exception as e:
                    st.error(f"Error in prediction: {str(e)}")
                    print("Error type:", type(e).__name__)
                    print("Error message:", e)
                    tb = sys.exc_info()[2]
                    print("Line number:", tb.tb_lineno)
                    print("Full traceback:")
                    traceback.print_exc()

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