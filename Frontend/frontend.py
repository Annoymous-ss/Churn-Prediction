import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime


# Configure page
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# FastAPI backend URL 
FASTAPI_URL = "https://churn-prediction-zb7k.onrender.com"  

# Send wake-up request
try:
    response = requests.get(FASTAPI_URL, timeout=15)
except requests.RequestException:
    pass

# Custom CSS 
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        position: relative;
        z-index: 2;
    }
    
    /* Prediction Card Styles */
    .prediction-card {
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .risk-indicator {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: bold;
        color: white;
        margin: 0 auto 1rem;
        position: relative;
        overflow: hidden;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #4ade80, #22c55e);
        box-shadow: 0 10px 30px rgba(34, 197, 94, 0.3);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);
    }
    
    .risk-high {
        background: linear-gradient(135deg, #f87171, #ef4444);
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.3);
    }
    
    .risk-indicator::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
        transform: rotate(45deg);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0; }
        50% { opacity: 1; }
    }
    
    .probability-text {
        font-size: 1.5rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1rem;
    }
    
    .confidence-text {
        font-size: 1rem;
        color: #6b7280;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #4facfe;
        margin-bottom: 1rem;
    }
    
    /* Input Sections */
    .input-section {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
    }
    
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* Alert Styles */
    .alert-success {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        border: 1px solid #22c55e;
        border-radius: 10px;
        padding: 1rem;
        color: #065f46;
        margin-bottom: 1rem;
    }
    
    .alert-error {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 1rem;
        color: #991b1b;
        margin-bottom: 1rem;
    }
    
    /* Streamlit specific overrides */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e1e8ed;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #4facfe;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e1e8ed;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #4facfe;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(145deg, #f8fafc, #e2e8f0);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state variables correctly
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'churn_probability' not in st.session_state:
    st.session_state.churn_probability = 0.0
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = ""
if 'predictions_count' not in st.session_state:  
    st.session_state.predictions_count = 0
if 'last_churn_probability' not in st.session_state:  
    st.session_state.last_churn_probability = None

# Function to make API call to  backend
def make_prediction_api_call(data):
    """Make API call to backend for prediction"""
    try:
        response = requests.post(f"{FASTAPI_URL}/predict", json=data, timeout=30)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return None, "❌ Connection Error: Unable to connect to the prediction service. Please ensure the FastAPI server is running."
    except requests.exceptions.Timeout:
        return None, "⏱️ Timeout Error: The prediction service is taking too long to respond."
    except Exception as e:
        return None, f"❌ Unexpected Error: {str(e)}"

# Function to validate input data
def validate_inputs(data):
    """Validate input data before sending to API"""
    errors = []
    
    if data['tenure'] < 0 or data['tenure'] > 100:
        errors.append("Tenure must be between 0 and 100 months")
    
    if data['MonthlyCharges'] <= 0 or data['MonthlyCharges'] > 1000:
        errors.append("Monthly charges must be between 0 and 1000")
    
    if data['TotalCharges'] < 0 or data['TotalCharges'] > 100000:
        errors.append("Total charges must be between 0 and 100,000")
    
    # Removed the validation that checked if TotalCharges < MonthlyCharges since it's now auto-calculated
    
    return errors

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 Customer Churn Prediction</h1>
    <p>Advanced ML-powered analytics to predict customer retention probability</p>
</div>
""", unsafe_allow_html=True)

# API Status Check
with st.sidebar:
    st.markdown("## 🔗 API Connection Status")
    
    if st.button("🔍 Test API Connection"):
        with st.spinner("Testing connection..."):
            try:
                response = requests.get(f"{FASTAPI_URL}/docs", timeout=5)
                if response.status_code == 200:
                    st.success("✅ FastAPI server is running!")
                else:
                    st.error("❌ FastAPI server responded with error")
            except:
                st.error("❌ Cannot connect to FastAPI server")
                st.info(f"Make sure your FastAPI server is running at: {FASTAPI_URL}")

# Create columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    # Demographics Section
    st.markdown("""
    <div class="input-section">
        <div class="section-header">👤 Customer Demographics</div>
    </div>
    """, unsafe_allow_html=True)
    
    demo_col1, demo_col2 = st.columns(2)
    with demo_col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        partner = st.selectbox("Has Partner", ["Yes", "No"])
    
    with demo_col2:
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        dependents = st.selectbox("Has Dependents", ["Yes", "No"])
    
    # Account Information
    st.markdown("""
    <div class="input-section">
        <div class="section-header">📊 Account Information</div>
    </div>
    """, unsafe_allow_html=True)
    
    account_col1, account_col2 = st.columns(2)
    with account_col1:
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    
    with account_col2:
        payment_method = st.selectbox("Payment Method", 
                                    ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
    
    # Services Section
    st.markdown("""
    <div class="input-section">
        <div class="section-header">🔧 Services</div>
    </div>
    """, unsafe_allow_html=True)
    
    service_col1, service_col2 = st.columns(2)
    with service_col1:
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    
    with service_col2:
        online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
        device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
        streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    
    streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
    
    # Charges Section
    st.markdown("""
    <div class="input-section">
        <div class="section-header">💰 Billing Information</div>
    </div>
    """, unsafe_allow_html=True)
    
    charge_col1, charge_col2 = st.columns(2)
    with charge_col1:
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=1000.0, value=50.0, step=0.1)
    
    with charge_col2:
        # Auto-calculate total charges 
        total_charges = monthly_charges * tenure
        st.metric("Total Charges (Auto-calculated)", f"${total_charges:.2f}")
        st.caption(f"Monthly Charges × Tenure = ${monthly_charges:.2f} × {tenure} months")

with col2:
    # Prediction Section
    st.markdown("""
    <div class="prediction-card">
        <h3 style="margin-bottom: 1rem; color: #374151;">🔮 Churn Prediction</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Predict button
    if st.button("🎯 Predict Churn Risk", key="predict_btn"):
        # data for API call 
        api_data = {
            "gender": gender,
            "SeniorCitizen": 1 if senior_citizen == "Yes" else 0,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": int(tenure),
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless_billing,
            "PaymentMethod": payment_method,
            "MonthlyCharges": float(monthly_charges),
            "TotalCharges": float(total_charges)  
        }
        
        # Validate inputs
        validation_errors = validate_inputs(api_data)
        
        if validation_errors:
            st.markdown(f"""
            <div class="alert-error">
                <strong>⚠️ Input Validation Errors:</strong><br>
                {'<br>'.join([f"• {error}" for error in validation_errors])}
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("🔄 Analyzing customer data..."):
                # Make API call
                result, error = make_prediction_api_call(api_data)
                
                if error:
                    st.markdown(f"""
                    <div class="alert-error">
                        <strong>{error}</strong><br>
                        Please check if your FastAPI server is running at: <code>{FASTAPI_URL}</code>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Storing results in session state and increment counter
                    st.session_state.churn_probability = result['probability']
                    st.session_state.prediction_result = result['prediction']
                    st.session_state.last_churn_probability = result['probability']
                    st.session_state.prediction_made = True
                    
                    # Incrementing predictions count only when a new prediction is made
                    st.session_state.predictions_count += 1
                    
                    # Success message
                    st.markdown(f"""
                    <div class="alert-success">
                        <strong>✅ Prediction Complete!</strong><br>
                        Model prediction: <strong>{result['prediction']}</strong>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Display prediction results
    if st.session_state.prediction_made:
        prob = st.session_state.churn_probability
        prediction = st.session_state.prediction_result
        
        # Determining risk level based on probability
        if prob < 0.3:
            risk_level = "Low"
            risk_class = "risk-low"
            risk_emoji = "✅"
            risk_color = "#22c55e"
        elif prob < 0.7:
            risk_level = "Medium"
            risk_class = "risk-medium"
            risk_emoji = "⚠️"
            risk_color = "#f59e0b"
        else:
            risk_level = "High"
            risk_class = "risk-high"
            risk_emoji = "🚨"
            risk_color = "#ef4444"
        
        # Display risk indicator
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <div class="risk-indicator {risk_class}">
                <span>{risk_emoji}</span>
            </div>
            <div class="probability-text">
                {prob:.1%} Churn Risk
            </div>
            <div class="confidence-text">
                Risk Level: <strong>{risk_level}</strong><br>
                Prediction: <strong>{prediction}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Probability gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = prob * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Churn Probability (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': risk_color},
                'steps': [
                    {'range': [0, 30], 'color': "#dcfcdc"},
                    {'range': [30, 70], 'color': "#fef3c7"},
                    {'range': [70, 100], 'color': "#fecaca"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    # Customer Summary
    st.markdown("""
    <div class="metric-card">
        <h4 style="color: #374151; margin-bottom: 1rem;">📋 Customer Summary</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col_metric1, col_metric2 = st.columns(2)
    with col_metric1:
        st.metric("Tenure", f"{tenure} months")
        st.metric("Contract", contract)
    
    with col_metric2:
        st.metric("Monthly Charges", f"${monthly_charges:.2f}")
        st.metric("Total Charges", f"${total_charges:.2f}")
    
    # Risk factors analysis (based on common churn indicators)
    if st.session_state.prediction_made:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #374151; margin-bottom: 1rem;">⚡ Key Risk Indicators</h4>
        </div>
        """, unsafe_allow_html=True)
        
        risk_factors = []
        
        if senior_citizen == "Yes":
            risk_factors.append("👴 Senior citizen")
        if partner == "No":
            risk_factors.append("💔 No partner")
        if dependents == "No":
            risk_factors.append("👥 No dependents")
        if tenure < 12:
            risk_factors.append("⏰ Short tenure")
        if contract == "Month-to-month":
            risk_factors.append("📄 Month-to-month contract")
        if payment_method == "Electronic check":
            risk_factors.append("💳 Electronic check payment")
        if monthly_charges > 80:
            risk_factors.append("💰 High monthly charges")
        if internet_service == "Fiber optic" and online_security == "No":
            risk_factors.append("🔒 No online security with fiber")
        if paperless_billing == "Yes":
            risk_factors.append("📧 Paperless billing")
        
        if risk_factors:
            for factor in risk_factors[:6]:  # Shows top 6 risk factors
                st.markdown(f"• {factor}")
        else:
            st.markdown("• ✅ No major risk factors identified")

# Footer with additional information
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    <p>🤖 Powered by Advanced Machine Learning • Real-time Predictions • FastAPI Backend</p>
    <p><small>API Endpoint: <code>{FASTAPI_URL}</code> • Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</small></p>
</div>
""", unsafe_allow_html=True)

# Sidebar with API information and controls
with st.sidebar:
    st.markdown("## 🎛️ Advanced Controls")
    
    # API Configuration
    with st.expander("🔧 API Configuration"):
        new_api_url = st.text_input("FastAPI Server URL", value=FASTAPI_URL)
        if st.button("Update API URL"):
            FASTAPI_URL = new_api_url
            st.success("API URL updated!")
    
    # Model Information
    with st.expander("🧠 Model Information"):
        st.info("""
        **Model Type:** Random Forest Classifier
        
        **Features Used:**
        - Demographics (Age, Gender, etc.)
        - Account Info (Tenure, Contract)
        - Services (Internet, Phone, etc.)
        - Billing (Charges, Payment method)
        
        **Output:**
        - Churn Prediction (Yes/No)
        - Probability Score (0-100%)
        """)
    
    # Data export
    with st.expander("📊 Data Export"):
        if st.session_state.prediction_made:
            if st.button("Export Prediction Results"):
                # Detailed prediction data for export
                prediction_data = {
                    'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    'Gender': [gender],
                    'SeniorCitizen': [senior_citizen],
                    'Partner': [partner],
                    'Dependents': [dependents],
                    'Tenure_Months': [tenure],
                    'Contract': [contract],
                    'PaymentMethod': [payment_method],
                    'MonthlyCharges': [monthly_charges],
                    'TotalCharges': [total_charges],
                    'Churn_Prediction': [st.session_state.prediction_result],
                    'Churn_Probability': [f"{st.session_state.churn_probability:.4f}"],
                    'Risk_Level': ['High' if st.session_state.churn_probability > 0.7 else 'Medium' if st.session_state.churn_probability > 0.3 else 'Low']
                }
                df = pd.DataFrame(prediction_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results (CSV)",
                    data=csv,
                    file_name=f"churn_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("Make a prediction first to export results")
    
    # API Health Check
    st.markdown("## 🏥 System Health")
    
    if st.button("🔍 Run Health Check"):
        with st.spinner("Checking system health..."):
            try:
                # Test basic connection
                response = requests.get(f"{FASTAPI_URL}/docs", timeout=5)
                if response.status_code == 200:
                    st.success("✅ FastAPI server is healthy")
                    
                    # Test prediction endpoint with sample data
                    sample_data = {
                        "gender": "Male",
                        "SeniorCitizen": 0,
                        "Partner": "Yes",
                        "Dependents": "No",
                        "tenure": 12,
                        "PhoneService": "Yes",
                        "MultipleLines": "No",
                        "InternetService": "DSL",
                        "OnlineSecurity": "Yes",
                        "OnlineBackup": "Yes",
                        "DeviceProtection": "No",
                        "TechSupport": "No",
                        "StreamingTV": "No",
                        "StreamingMovies": "No",
                        "Contract": "One year",
                        "PaperlessBilling": "No",
                        "PaymentMethod": "Credit card (automatic)",
                        "MonthlyCharges": 45.0,
                        "TotalCharges": 540.0
                    }
                    
                    test_response = requests.post(f"{FASTAPI_URL}/predict", json=sample_data, timeout=10)
                    if test_response.status_code == 200:
                        st.success("✅ Prediction endpoint working")
                        result = test_response.json()
                        st.info(f"Sample prediction: {result['prediction']} ({result['probability']:.3f})")
                    else:
                        st.warning("⚠️ Prediction endpoint has issues")
                else:
                    st.error("❌ FastAPI server not responding correctly")
            except Exception as e:
                st.error(f"❌ Health check failed: {str(e)}")
    
    # Session Stats 
    st.markdown("## 📈 Session Stats")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Predictions Made", st.session_state.predictions_count)
    
    with col2:
        if st.session_state.last_churn_probability is not None:
            accuracy_display = f"{st.session_state.last_churn_probability:.1%}"
        else:
            accuracy_display = "N/A"
        st.metric("Last Probability", accuracy_display)