import streamlit as st
from prediction_helper import predict

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Health Insurance Cost Predictor", page_icon="💰", layout="centered")

# -------------------------
# Session State Initialization
# -------------------------
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

st.title("💡 Health Insurance Cost Predictor")
st.write("Fill in your details below to get an estimate of your insurance cost.")

# -------------------------
# Categorical options
# -------------------------
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer', ''],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# -------------------------
# Input Form
# -------------------------
with st.form("prediction_form", clear_on_submit=True):
    st.subheader("📝 Enter Your Details")

    user_name = st.text_input("👤 Enter your Name")

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input('Age', min_value=18, step=1, max_value=100)
    with col2:
        number_of_dependants = st.number_input('Dependants', min_value=0, step=1, max_value=20)
    with col3:
        income_lakhs = st.number_input('Income (Lakhs)', step=1, min_value=0, max_value=200)

    col4, col5, col6 = st.columns(3)
    with col4:
        genetical_risk = st.number_input('Genetical Risk (0-5)', step=1, min_value=0, max_value=5)
    with col5:
        insurance_plan = st.selectbox('Insurance Plan', categorical_options['Insurance Plan'])
    with col6:
        employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'])

    col7, col8, col9 = st.columns(3)
    with col7:
        gender = st.selectbox('Gender', categorical_options['Gender'])
    with col8:
        marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'])
    with col9:
        bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'])

    col10, col11, col12 = st.columns(3)
    with col10:
        smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'])
    with col11:
        region = st.selectbox('Region', categorical_options['Region'])
    with col12:
        medical_history = st.selectbox('Medical History', categorical_options['Medical History'])

    # Submit Button
    submitted = st.form_submit_button("🔮 Predict Cost")

# -------------------------
# Prediction Logic
# -------------------------
if submitted:
    input_dict = {
        'Age': age,
        'Number of Dependants': number_of_dependants,
        'Income in Lakhs': income_lakhs,
        'Genetical Risk': genetical_risk,
        'Insurance Plan': insurance_plan,
        'Employment Status': employment_status,
        'Gender': gender,
        'Marital Status': marital_status,
        'BMI Category': bmi_category,
        'Smoking Status': smoking_status,
        'Region': region,
        'Medical History': medical_history
    }

    st.session_state.prediction = predict(input_dict)
    st.session_state.user_name = user_name.strip()
    st.session_state.show_popup = True
    st.rerun()

# -------------------------
# Prediction Popup
# -------------------------
if st.session_state.show_popup and st.session_state.prediction is not None:
    st.markdown("---")
    with st.container():
        st.markdown(
            f"""
            <div style="
                background-color: #ffffff;
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                font-size: 20px;
                font-weight: 600;
                color: #2c3e50;
                box-shadow: 0 6px 20px rgba(0,0,0,0.25);
            ">
                🎉 Hello <b>{st.session_state.user_name or "User"}</b>! <br><br>
                Your predicted insurance cost is <br>
                <span style="color:#27ae60; font-size:26px;">₹ {st.session_state.prediction}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("❌ Close Result"):
            st.session_state.show_popup = False
            st.session_state.prediction = None
            st.rerun()
