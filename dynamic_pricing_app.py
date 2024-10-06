import streamlit as st

# Dictionary for town-based adjustments
town_adjustments = {
    "Lusaka": 1.20,   # 20% increase
    "Kitwe": 1.15,    # 15% increase
    "Ndola": 1.10,    # 10% increase
    "Livingstone": 1.07, # 7% increase
    "Solwezi": 1.05,   # 5% increase
    "Kabwe": 1.03     # 3% increase
}

# Dictionary for body type risk factors
body_risk_adjustments = {
    "Sedan": 1.00,     # No adjustment (low risk)
    "Hatchback": 1.00, # No adjustment (low risk)
    "Wagon": 1.05,     # 5% increase (medium risk)
    "SUV": 1.10,       # 10% increase (medium-high risk)
    "TRU (Truck)": 1.15, # 15% increase (high risk)
    "Trailer": 1.20,   # 20% increase (high risk)
    "Tanker": 1.25,    # 25% increase (very high risk)
    "Minibus": 1.15,   # 15% increase (high risk)
    "Van": 1.10,       # 10% increase (medium risk)
    "Pick Up": 1.10,   # 10% increase (medium-high risk)
    "Double Cab": 1.12, # 12% increase (medium-high risk)
    "Convertible": 1.20, # 20% increase (high risk)
    "Primemover": 1.25, # 25% increase (very high risk)
    "Motorcycle": 1.20, # 20% increase (high risk)
    "Tricycle": 1.05,  # 5% increase (medium risk)
    "Coupe": 1.07      # 7% increase (medium risk)
}

# Dictionary for vehicle model risk factors
model_risk_adjustments = {
    "Toyota Corolla": 1.00,  # Low risk
    "Honda Civic": 1.00,     # Low risk
    "Ford Ranger": 1.10,     # Medium risk
    "Toyota Hilux": 1.12,    # Medium-high risk
    "Nissan Navara": 1.12,   # Medium-high risk
    "Mercedes-Benz C-Class": 1.15,  # High risk
    "BMW 3 Series": 1.15,    # High risk
    "Toyota Land Cruiser": 1.20,   # High risk
    "Jeep Wrangler": 1.20,   # High risk
    "Volkswagen Golf": 1.07  # Medium risk
}

# Function to calculate the premium
def calculate_premium(age, vehicle_use, town, vehicle_value, body_type, mileage, vehicle_model, long_term_discount, vehicle_QTY):
    # Check for minimum vehicle value (ZMW 35,000, except for Motorcycles)
    min_value = 35000 if body_type != "Motorcycle" else 15000
    if vehicle_value < min_value:
        return f"Error: Vehicle value cannot be less than {min_value:.2f} ZMW"
    
    # Apply base rate of 4%
    rate = 0.04
    
    # Adjust rate for vehicle use
    if vehicle_use == "Commercial":
        rate += 0.03  # Additional 3% for commercial use
    
    # Age-based premium adjustments
    if age < 25:
        rate += 0.02  # Additional 2% for age below 25
    elif age > 60:
        rate += 0.02  # Additional 2% for age above 60
    
    # Mileage-based premium adjustments
    if mileage > 50000 and mileage <= 100000:
        rate += 0.002  # 0.2% increase for mileage between 50,000 and 100,000
    elif mileage > 100000 and mileage <= 150000:
        rate += 0.0025  # 0.25% increase for mileage between 100,000 and 150,000
    elif mileage > 150000 and mileage <= 200000:
        rate += 0.0029  # 0.29% increase for mileage between 150,000 and 200,000
    elif mileage > 200000:
        rate += 0.005  # 0.5% increase for mileage above 200,000

    # Calculate the premium
    premium = vehicle_value * rate
    
    # Town-based adjustment
    premium *= town_adjustments.get(town, 1.0)  # Defaults to no adjustment if town not listed
    
    # Body type-based adjustment
    premium *= body_risk_adjustments.get(body_type, 1.0)  # Defaults to no adjustment if body type not listed
    
    # Model-based adjustment
    premium *= model_risk_adjustments.get(vehicle_model, 1.0)  # Defaults to no adjustment if model not listed
    
    # Add 5% premium income tax
    premium *= 1.05
    
    # Apply long-term discount, max capped at 30%
    discount = min(long_term_discount, 30)  # Cap discount at 30%
    premium -= (premium * discount / 100)
    
    # Multiply by vehicle quantity
    premium *= vehicle_QTY
    
    return f"{premium:.2f}"

# Streamlit Web App
st.markdown("<h1 style='color: #007BFF;'> MOTOR INSURANCE PREMIUM INTERFACE </h1>", unsafe_allow_html=True)

# Collecting inputs
age = st.number_input("Enter your age", min_value=18, max_value=100, value=30)
vehicle_use = st.selectbox("Select vehicle use", ["Private", "Commercial"])
town = st.selectbox("Select your town", ["Lusaka", "Kitwe", "Ndola", "Livingstone", "Solwezi", "Kabwe"])
vehicle_value = st.number_input("Enter the vehicle value (ZMW)", min_value=15000.00, value=35000.00)
body_type = st.selectbox("Select vehicle body type", [
    "Sedan", "Hatchback", "Wagon", "SUV", "TRU (Truck)", "Trailer", "Tanker", "Minibus", 
    "Van", "Pick Up", "Double Cab", "Convertible", "Primemover", "Motorcycle", "Tricycle", "Coupe"
])
mileage = st.number_input("Enter the vehicle mileage", min_value=0, value=50000)
vehicle_model = st.selectbox("Select vehicle model", [
    "Toyota Corolla", "Honda Civic", "Ford Ranger", "Toyota Hilux", "Nissan Navara",
    "Mercedes-Benz C-Class", "BMW 3 Series", "Toyota Land Cruiser", "Jeep Wrangler", "Volkswagen Golf"
])
long_term_discount = st.slider("Select long-term discount (%)", min_value=0, max_value=30, value=0)
vehicle_QTY = st.number_input("Enter Number of Vehicles", min_value=1, max_value=100, value=1)

# Button to calculate premium
if st.button("Calculate Premium"):
    premium = calculate_premium(age, vehicle_use, town, vehicle_value, body_type, mileage, vehicle_model, long_term_discount, vehicle_QTY)
    
    if "Error" in premium:
        st.error(premium)  # Display the error if any
    else:
        st.markdown(f"<h3 style='color: #007BFF;'>The calculated premium for your vehicle(s) is: ZMW {premium} </h3>", unsafe_allow_html=True)
