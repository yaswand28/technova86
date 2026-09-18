
import streamlit as st
from utils.aerodynamics import calculate_aerodynamics
import plotly.graph_objects as go


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

# =========================
# SIDEBAR INPUTS
# =========================

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

# =========================
# CALCULATIONS
# =========================

damaged = calculate_aerodynamics(
    air_speed,
    angle_of_attack,
    crack_length,
    crack_depth,
    air_density
)

healthy = calculate_aerodynamics(
    air_speed,
    angle_of_attack,
    0.0,
    0.0,
    air_density
)

# Percentage changes
if healthy["lift"] != 0:
    lift_change = (
        (damaged["lift"] - healthy["lift"])
        / healthy["lift"]
    ) * 100
else:
    lift_change = 0

if healthy["drag"] != 0:
    drag_change = (
        (damaged["drag"] - healthy["drag"])
        / healthy["drag"]
    ) * 100
else:
    drag_change = 0

# =========================
# MAIN OUTPUT
# =========================

st.header("Aerodynamic Analysis")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Lift Coefficient (Cl)",
        f"{damaged['cl']:.3f}"
    )

with col2:
    st.metric(
        "Drag Coefficient (Cd)",
        f"{damaged['cd']:.3f}"
    )

with col3:
    st.metric(
        "Lift Force",
        f"{damaged['lift']:,.0f} N"
    )

with col4:
    st.metric(
        "Drag Force",
        f"{damaged['drag']:,.0f} N"
    )

st.markdown("---")

# =========================
# HEALTHY VS DAMAGED
# =========================

st.header("Healthy Wing vs Micro-Fractured Wing")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Healthy Wing")

    st.metric(
        "Lift",
        f"{healthy['lift']:,.0f} N"
    )

    st.metric(
        "Drag",
        f"{healthy['drag']:,.0f} N"
    )

with col2:
    st.subheader("Micro-Fractured Wing")

    st.metric(
        "Lift",
        f"{damaged['lift']:,.0f} N"
    )

    st.metric(
        "Drag",
        f"{damaged['drag']:,.0f} N"
    )

# =========================
# PERFORMANCE CHANGE
# =========================

st.markdown("---")

st.header("Performance Change")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Lift Change",
        f"{lift_change:.2f}%"
    )

with col2:
    st.metric(
        "Drag Change",
        f"{drag_change:.2f}%"
    )

# =========================
# DAMAGE SEVERITY
# =========================

st.markdown("---")

st.header("Micro-Fracture Assessment")

damage_score = (
    crack_length / 5.0 +
    crack_depth / 2.0
) / 2

if damage_score == 0:
    severity = "No Damage"
elif damage_score < 0.25:
    severity = "Low"
elif damage_score < 0.60:
    severity = "Moderate"
else:
    severity = "High"

st.metric(
    "Prototype Damage Severity",
    severity
)

st.caption(
    "Severity is a transparent Phase 1 prototype indicator "
    "based on crack length and depth. It is not an AI diagnosis."
)

# =========================
# INPUT SUMMARY
# =========================

st.markdown("---")

st.header("Analysis Parameters")

st.write(f"**Air Speed:** {air_speed:.1f} m/s")
st.write(f"**Angle of Attack:** {angle_of_attack:.1f}°")
st.write(f"**Crack Length:** {crack_length:.1f} mm")
st.write(f"**Crack Depth:** {crack_depth:.1f} mm")
st.write(f"**Air Density:** {air_density:.3f} kg/m³")
st.write(
    f"**Dynamic Pressure:** "
    f"{damaged['dynamic_pressure']:,.2f} Pa"
)

# =========================
# INTERACTIVE AERODYNAMIC CHARTS
# =========================

st.markdown("---")

st.header("Aerodynamic Performance Curves")

angle_values = [
    -5, -4, -3, -2, -1,
     0,  1,  2,  3,  4,
     5,  6,  7,  8,  9,
    10, 11, 12, 13, 14, 15
]

healthy_cl_values = []
damaged_cl_values = []
healthy_cd_values = []
damaged_cd_values = []

for angle in angle_values:

    healthy_result = calculate_aerodynamics(
        air_speed,
        angle,
        0.0,
        0.0,
        air_density
    )

    damaged_result = calculate_aerodynamics(
        air_speed,
        angle,
        crack_length,
        crack_depth,
        air_density
    )

    healthy_cl_values.append(healthy_result["cl"])
    damaged_cl_values.append(damaged_result["cl"])

    healthy_cd_values.append(healthy_result["cd"])
    damaged_cd_values.append(damaged_result["cd"])


# Lift coefficient chart
fig_lift = go.Figure()

fig_lift.add_trace(
    go.Scatter(
        x=angle_values,
        y=healthy_cl_values,
        mode="lines+markers",
        name="Healthy Wing"
    )
)

fig_lift.add_trace(
    go.Scatter(
        x=angle_values,
        y=damaged_cl_values,
        mode="lines+markers",
        name="Micro-Fractured Wing"
    )
)

fig_lift.update_layout(
    title="Lift Coefficient vs Angle of Attack",
    xaxis_title="Angle of Attack (°)",
    yaxis_title="Lift Coefficient (Cl)",
    hovermode="x unified"
)

st.plotly_chart(
    fig_lift,
    use_container_width=True
)


# Drag coefficient chart
fig_drag = go.Figure()

fig_drag.add_trace(
    go.Scatter(
        x=angle_values,
        y=healthy_cd_values,
        mode="lines+markers",
        name="Healthy Wing"
    )
)

fig_drag.add_trace(
    go.Scatter(
        x=angle_values,
        y=damaged_cd_values,
        mode="lines+markers",
        name="Micro-Fractured Wing"
    )
)

fig_drag.update_layout(
    title="Drag Coefficient vs Angle of Attack",
    xaxis_title="Angle of Attack (°)",
    yaxis_title="Drag Coefficient (Cd)",
    hovermode="x unified"
)

st.plotly_chart(
    fig_drag,
    use_container_width=True
)
# =========================
# PHASE 1 DISCLAIMER
# =========================

st.markdown("---")

st.info(
    "Phase 1 Prototype: Results are generated using a "
    "physics-based prototype model. The trained Physics-Informed "
    "Neural Network (PINN) will be integrated in later phases "
    "after dataset preparation and model training."
)

st.success(
    "Quantum-Aero aerodynamic analysis completed successfully."
)