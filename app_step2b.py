
import streamlit as st
from utils.aerodynamics import calculate_aerodynamics


st.set_page_config(
    page_title="Quantum-Aero",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Quantum-Aero")
st.subheader(
    "Physics-Informed Neural Network for Real-Time Wing Micro-Fracture Aerodynamics"
)

st.markdown("---")

# Sidebar
st.sidebar.header("Flight & Wing Parameters")

air_speed = st.sidebar.slider(
    "Air Speed (m/s)",
    50.0, 250.0, 150.0, 1.0
)

angle_of_attack = st.sidebar.slider(
    "Angle of Attack (°)",
    -5.0, 15.0, 5.0, 0.5
)

crack_length = st.sidebar.slider(
    "Crack Length (mm)",
    0.0, 5.0, 0.0, 0.1
)

crack_depth = st.sidebar.slider(
    "Crack Depth (mm)",
    0.0, 2.0, 0.0, 0.1
)

air_density = st.sidebar.number_input(
    "Air Density (kg/m³)",
    0.1, 2.0, 1.225, 0.01
)

# Calculate
results = calculate_aerodynamics(
    air_speed,
    angle_of_attack,
    crack_length,
    crack_depth,
    air_density
)

# Output cards
st.header("Aerodynamic Analysis")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Lift Coefficient (Cl)", f"{results['cl']:.3f}")

with col2:
    st.metric("Drag Coefficient (Cd)", f"{results['cd']:.3f}")

with col3:
    st.metric("Lift Force", f"{results['lift']:,.0f} N")

with col4:
    st.metric("Drag Force", f"{results['drag']:,.0f} N")

st.markdown("---")

st.header("Analysis Summary")

st.write(f"**Air Speed:** {air_speed:.1f} m/s")
st.write(f"**Angle of Attack:** {angle_of_attack:.1f}°")
st.write(f"**Crack Length:** {crack_length:.1f} mm")
st.write(f"**Crack Depth:** {crack_depth:.1f} mm")
st.write(f"**Dynamic Pressure:** {results['dynamic_pressure']:,.2f} Pa")

st.info(
    "Phase 1 Prototype: These results are generated using a "
    "physics-based prototype model. The trained PINN will be "
    "integrated in later phases."
)

st.success("Aerodynamic calculation engine connected successfully.")