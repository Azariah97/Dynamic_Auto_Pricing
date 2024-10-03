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

# Function to calculate the premium
def calculate_premium(age, vehicle_use, town, vehicle_value, body_type, mileage):
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
    
    # Mileage-based premium adjustments (for mileage above 50,000)
    if mileage > 50000:
        rate += 0.01  # Add 1% for mileage over 50,000

    # Calculate the premium
    premium = vehicle_value * rate
    
    # Town-based adjustment
    premium *= town_adjustments.get(town, 1.0)  # Defaults to no adjustment if town not listed
    
    # Body type-based adjustment
    premium *= body_risk_adjustments.get(body_type, 1.0)  # Defaults to no adjustment if body type not listed
    
    # Add 5% premium income tax
    premium *= 1.05
    
    return f"{premium:.2f} ZMW"

# Streamlit Web App
st.markdown("<h1 style='color: #007BFF;'>MGen Insurance Premium Calculator</h1>", unsafe_allow_html=True)

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

# Button to calculate premium
if st.button("Calculate Premium"):
    premium = calculate_premium(age, vehicle_use, town, vehicle_value, body_type, mileage)
    
    if "Error" in premium:
        st.error(premium)  # Display the error if any
    else:
        st.markdown(f"<h3 style='color: #007BFF;'>The calculated premium for your vehicle is: {premium} </h3>", unsafe_allow_html=True)


