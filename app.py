import os
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from streamlit.components.v1 import iframe

# Ensure the workspace root is on the import path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from auth_utils import authenticate_user, register_user
from location_prices import get_average_price_per_area, get_location_map_data, get_location_prices

st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "Home"

st.markdown(
    """
    <style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1728721529009-bfaab6fcc8e6?fm=jpg&q=60&w=3000&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGhvdXNlJTIwaW1hZ2VzfGVufDB8fDB8fHww');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(3px);
        z-index: -1;
    }
    .main {
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.97);
        border-radius: 12px;
        margin: 10px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        
    }
    .stMetric {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 10px;
        border-left: 4px solid #2980b9;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        color: #000000 !important;
    }
    .stMetric label {
        color: #000000 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #000000 !important;
    }
    .market-data {
        color: #000000 !important;
    }
    .market-data h3 {
        color: #000000 !important;
    }
    .stButton > button {
        background-color: #27ae60 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    try:
        with open(ROOT_DIR / "price_model.pkl", "rb") as handle:
            return pickle.load(handle)
    except Exception:
        st.error("⚠️ Model not found. Please train the model first by running: python train_model.py")
        return None


def save_prediction(area, location, price):
    prediction_data = {
        "timestamp": pd.Timestamp.now(),
        "area": area,
        "location": location,
        "predicted_price": price,
    }

    predictions_file = ROOT_DIR / "data" / "predictions_history.csv"
    predictions_file.parent.mkdir(parents=True, exist_ok=True)

    if predictions_file.exists():
        df = pd.read_csv(predictions_file)
        df = pd.concat([df, pd.DataFrame([prediction_data])], ignore_index=True)
    else:
        df = pd.DataFrame([prediction_data])

    df.to_csv(predictions_file, index=False)
    st.success("✅ Prediction saved!")


with st.sidebar:
    st.header("🧭 Navigation")
    page = st.radio(
        "Choose a page",
        ["Home", "About Us", "Login / Register", "Dashboard", "Feedback"],
        index=["Home", "About Us", "Login / Register", "Dashboard", "Feedback"].index(st.session_state.page),
        label_visibility="collapsed",
    )
    st.session_state.page = page

    if st.session_state.authenticated:
        st.markdown("---")
        st.write(f"Welcome, {st.session_state.user['full_name']}")
        if st.button("Log out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.page = "Home"
            st.rerun()

    st.markdown("---")
    st.info(
        "This app predicts house prices using a trained ML model and shows pricing information for selected locations."
    )


def save_feedback(feedback_data):
    feedback_file = ROOT_DIR / "data" / "feedback.csv"
    feedback_file.parent.mkdir(parents=True, exist_ok=True)

    if feedback_file.exists():
        df = pd.read_csv(feedback_file)
        df = pd.concat([df, pd.DataFrame([feedback_data])], ignore_index=True)
    else:
        df = pd.DataFrame([feedback_data])

    df.to_csv(feedback_file, index=False)


def render_home_page():
    st.title("🏠 House Price Prediction System")
    st.markdown("---")
    st.markdown(
        """
        Welcome to the smart real estate platform where you can explore market trends,
        register as a user, log in, and predict property prices instantly.
        """
    )

    st.markdown("### Why Choose Our Platform?")
    st.write("- AI-powered house price prediction with high accuracy")
    st.write("- Interactive Google Maps for location-based insights.")
    st.write("- Fast, responsive, and user-friendly interface.")
    st.write("- Secure user registration and login system.")

    if not st.session_state.authenticated:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go to Login", use_container_width=True):
                st.session_state.page = "Login / Register"
                st.rerun()
        with col2:
            if st.button("Create an account", use_container_width=True):
                st.session_state.page = "Login / Register"
                st.rerun()


def render_about_page():
    st.title("ℹ️ About Us")
    st.markdown("---")
    st.markdown(
        """
        This App is a house price prediction system designed to help users estimate the value of a property
        using the plot area, the selected location, and historical market data.

        The application combines machine learning with location intelligence so that the prediction feels more practical
        and useful for property planning and research.
        """
    )
    st.success("Built for modern real estate analysis and fast property price estimation.")


def render_auth_page():
    st.title("🔐 User Access")
    st.markdown("---")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", use_container_width=True):
            user = authenticate_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.session_state.page = "Dashboard"
                st.success(f"Welcome back, {user['full_name']}")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with register_tab:
        full_name = st.text_input("Full name", key="register_full_name")
        username = st.text_input("Choose username", key="register_username")
        password = st.text_input("Create password", type="password", key="register_password")
        if st.button("Register", use_container_width=True):
            success, message = register_user(username, password, full_name)
            if success:
                st.success(message)
                st.session_state.page = "Login / Register"
            else:
                st.error(message)


def render_feedback_page():
    st.title("📝 Feedback")
    st.markdown("---")
    st.markdown(
        "We would love to hear from you. Please share your feedback, rating, and any questions you have about the app."
    )

    name_default = st.session_state.user["full_name"] if st.session_state.authenticated else ""
    with st.form(key="feedback_form"):
        name = st.text_input("Name", value=name_default, max_chars=100)
        phone = st.text_input("Phone Number", max_chars=20, help="Enter your contact phone number.")
        rating = st.radio(
            "Rating",
            ["⭐☆☆☆☆", "⭐⭐☆☆☆", "⭐⭐⭐☆☆", "⭐⭐⭐⭐☆", "⭐⭐⭐⭐⭐"],
            index=4,
            horizontal=True,
        )
        Review = st.text_area(
            "Your Review or Feedback",
            help="Share your review, comment, or suggestion.",
            height=140,
        )
        submit_feedback = st.form_submit_button("Submit Feedback")

    if submit_feedback:
        if not name.strip():
            st.error("Please enter your name.")
        elif not phone.strip():
            st.error("Please enter your phone number.")
        else:
            feedback_record = {
                "timestamp": pd.Timestamp.now(),
                "name": name.strip(),
                "phone": phone.strip(),
                "rating": rating,
                "review": Review.strip(),
                "user": st.session_state.user["username"] if st.session_state.authenticated else "anonymous",
            }
            save_feedback(feedback_record)
            st.success("✅ Thank you! Your feedback has been recorded.")


def render_dashboard():
    st.title("📊 Welcome to the House Price Prediction System")
    st.markdown("---")
    st.markdown("Predict house prices and review the market data for your selected location.")

    location_prices = get_location_prices()
    available_locations = list(location_prices.keys())
    location_price_per_sqft = get_average_price_per_area()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Enter Property Details")
        area = st.number_input(
            "Plot Area (in sq. ft.)",
            min_value=100,
            max_value=50000,
            value=1000,
            step=100,
            help="Enter the total plot area in square feet",
        )
        location = st.selectbox(
            "Select Location/Place",
            available_locations,
            help="Choose the location where the property is situated",
        )

    with col2:
        st.markdown('<div class="market-data">', unsafe_allow_html=True)
        st.subheader("📊 Location Market Data")
        if location in location_prices:
            avg_price = location_prices[location]["avg_price"]
            price_range = location_prices[location]["price_range"]
            st.metric("Average Price (per sq. ft.)", f"₹{avg_price:,.0f}")
            st.metric("Price Range", f"₹{price_range[0]:,.0f} - ₹{price_range[1]:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💰 Price Prediction")

    model = load_model()
    if model is not None and st.button("🔮 Predict Price", use_container_width=True):
        try:
            location_encoded = available_locations.index(location)
            features = np.array([[area, location_encoded]])
            predicted_price = model.predict(features)[0]

            location_avg_price_per_sqft = location_prices[location]["avg_price"]
            market_based_price = area * location_avg_price_per_sqft

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Predicted Price",
                    f"₹{predicted_price:,.0f}",
                    delta=f"{((predicted_price / market_based_price - 1) * 100):.1f}% vs Market",
                )
            with col2:
                st.metric("Market Based Price", f"₹{market_based_price:,.0f}")
            with col3:
                price_per_sqft = predicted_price / area
                st.metric("Price per Sq. ft.", f"₹{price_per_sqft:,.0f}")

            st.markdown("---")
            st.subheader("📈 Insights")
            insight_col1, insight_col2 = st.columns(2)
            with insight_col1:
                st.write(
                    f"""
                    **Property Details:**
                    - Plot Area: {area:,} sq. ft.
                    - Location: {location}
                    - Predicted Price: ₹{predicted_price:,.0f}
                    """
                )
            with insight_col2:
                if predicted_price > market_based_price:
                    st.warning(
                        f"💡 Price is **{((predicted_price / market_based_price - 1) * 100):.1f}%** above market average for this location"
                    )
                else:
                    st.success(
                        f"✅ Price is **{((1 - predicted_price / market_based_price) * 100):.1f}%** below market average - Good deal!"
                    )

            st.markdown("---")
            if st.checkbox("Save this prediction?"):
                save_prediction(area, location, predicted_price)
        except Exception as exc:
            st.error(f"❌ Error during prediction: {str(exc)}")

    st.markdown("---")
    st.subheader("🗺️ Google Map View")
    map_data = get_location_map_data()
    if location in map_data:
        coords = map_data[location]
        iframe_url = f"https://www.google.com/maps?q={coords['lat']},{coords['lng']}&z=13&output=embed"
        iframe(iframe_url, height=320)
        st.caption(f"Showing {location} on Google Maps")


if st.session_state.page == "Dashboard" and not st.session_state.authenticated:
    st.session_state.page = "Login / Register"

if st.session_state.page == "Home":
    render_home_page()
elif st.session_state.page == "About Us":
    render_about_page()
elif st.session_state.page == "Login / Register":
    render_auth_page()
elif st.session_state.page == "Feedback":
    render_feedback_page()
else:
    render_dashboard()

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: white;'>
        <p>House Price Predictor v1.0 | Data Science Project</p>
        <p>Predictions are estimates based on ML model training</p>
    </div>
    """,
    unsafe_allow_html=True,
)
