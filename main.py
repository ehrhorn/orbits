import streamlit as st

st.set_page_config(layout="wide")
from modules import plot_satellite_orbit_plotly

eccentricity = st.sidebar.number_input(
    "Eccentricity", min_value=0.0, max_value=1.0, value=0.00155, format="%f"
)
orbital_period = st.sidebar.number_input(
    "Orbital period (minutes)", min_value=0.0, value=717.966, format="%f"
)
inclination = st.sidebar.number_input(
    "Inclination (degrees)", min_value=0.0, max_value=180.0, value=56.396, format="%f"
)
RAAN = st.sidebar.number_input(
    "RA ascending node (hours)", min_value=0.0, value=23.263, format="%f"
)
argument_of_perigee = st.sidebar.number_input(
    "Argument of perigee (degrees)", min_value=0.0, value=125.549, format="%f"
)

fig = plot_satellite_orbit_plotly(
    eccentricity, orbital_period, inclination, RAAN, argument_of_perigee
)

st.plotly_chart(fig, use_container_width=True)
