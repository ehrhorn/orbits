import plotly.graph_objects as go
import streamlit as st
from numpy.random import random

st.set_page_config(layout="wide")
from modules import create_globe, plot_satellite_orbit_plotly, set_camera, set_layout


def input_options(i):
    out_dict = {}
    out_dict["eccentricity"] = st.sidebar.number_input(
        f"Eccentricity {i}",
        min_value=0.0,
        max_value=1.0,
        value=round(0.3 * random() + 0.1, 2),
        step=0.1,
        format="%f",
    )
    out_dict["orbital_period"] = st.sidebar.number_input(
        f"Orbital period (minutes) {i}",
        min_value=0.0,
        value=round(2000 * random() + 200, 2),
        step=100.0,
        format="%f",
    )
    out_dict["inclination"] = st.sidebar.number_input(
        f"Inclination (degrees) {i}",
        min_value=0.0,
        max_value=180.0,
        value=round(150 * random() + 1, 2),
        step=1.0,
        format="%f",
    )
    out_dict["RAAN"] = st.sidebar.number_input(
        f"RA ascending node (hours) {i}",
        min_value=0.0,
        max_value=24.0,
        value=round(20 * random() + 1, 2),
        step=1.0,
        format="%f",
    )
    out_dict["argument_of_perigee"] = st.sidebar.number_input(
        f"Argument of perigee (degrees) {i}",
        min_value=0.0,
        max_value=180.0,
        value=round(80 * random() + 50, 2),
        step=1.0,
        format="%f",
    )
    return out_dict


no_orbits = st.sidebar.select_slider(label="No. of orbits", options=[1, 2, 3], value=3)

coordinate_list = []
for number in range(no_orbits):
    coordinate_list.append(input_options(number + 1))

if st.button("Create random orbit(s)"):
    coordinate_list = []
    for number in range(no_orbits):
        coordinate_list.append(input_options(number + 1))

surface = create_globe()
layout = set_layout()
camera = set_camera()

plot_data = [surface]
for number, coordinate_set in enumerate(coordinate_list):
    plot_data.extend(
        plot_satellite_orbit_plotly(
            coordinate_set["eccentricity"],
            coordinate_set["orbital_period"],
            coordinate_set["inclination"],
            coordinate_set["RAAN"],
            coordinate_set["argument_of_perigee"],
            number + 1,
        )
    )

fig = go.Figure(data=plot_data, layout=layout)
fig.update_layout(scene_camera=camera)
st.plotly_chart(fig, use_container_width=True)
