import pickle

import numpy as np
import plotly.graph_objects as go
from PyAstronomy import pyasl


def calculate_semi_major_axis(orbital_period, standard_gravitational_parameter):
    semi_major_axis = (
        orbital_period ** (2 / 3)
        * np.cbrt(standard_gravitational_parameter)
        / (2 * np.pi) ** (2 / 3)
    )
    return semi_major_axis


def create_globe():
    with open("surface.pickle", "rb") as f:
        surface = pickle.load(f)
    surface = go.Surface(
        x=surface["xs"],
        y=surface["ys"],
        z=surface["zs"],
        colorscale=surface["Ctopo"],
        surfacecolor=surface["topo"],
        cmin=surface["cmin"],
        cmax=surface["cmax"],
        showscale=False,
    )
    return surface


def set_layout():
    noaxis = dict(
        showbackground=False,
        showgrid=False,
        showline=False,
        showticklabels=False,
        ticks="",
        title="",
        zeroline=False,
    )
    titlecolor = "white"
    bgcolor = "white"
    layout = go.Layout(
        autosize=True,
        width=1200,
        height=800,
        titlefont=dict(family="Courier New", color=titlecolor),
        showlegend=True,
        scene=dict(
            xaxis=noaxis,
            yaxis=noaxis,
            zaxis=noaxis,
        ),
        paper_bgcolor=bgcolor,
        plot_bgcolor=bgcolor,
    )
    return layout


def set_camera():
    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=1.25, y=1.25, z=1.25),
    )
    return camera


def plot_satellite_orbit_plotly(
    eccentricity, orbital_period, inclination, RAAN, argument_of_perigee, number
):

    standard_gravitational_parameter = 3.986004418e14
    orbital_period = int(orbital_period * 60)
    semi_major_axis = calculate_semi_major_axis(
        orbital_period, standard_gravitational_parameter
    )
    earth_radius = 6.371009e6
    semi_major_axis = semi_major_axis / earth_radius

    ke = pyasl.KeplerEllipse(
        semi_major_axis,
        orbital_period,
        e=eccentricity,
        Omega=RAAN,
        i=inclination,
        w=argument_of_perigee,
    )
    t = np.linspace(0, orbital_period, 200)
    cis_vector = ke.xyzPos(t)
    ascn, descn = ke.xyzNodes_LOSZ()

    orbit = go.Scatter3d(
        x=cis_vector[:, 0],
        y=cis_vector[:, 1],
        z=cis_vector[:, 2],
        mode="lines",
        name=f"Orbit {number}",
    )
    ascending_node = go.Scatter3d(
        x=[ascn[0]],
        y=[ascn[1]],
        z=[ascn[2]],
        mode="markers",
        name=f"Ascending node {number}",
    )
    descending_node = go.Scatter3d(
        x=[descn[0]],
        y=[descn[1]],
        z=[descn[2]],
        mode="markers",
        name=f"Descending node {number}",
    )
    periapsis = go.Scatter3d(
        x=[cis_vector[0, 0]],
        y=[cis_vector[0, 1]],
        z=[cis_vector[0, 2]],
        mode="markers",
        name=f"Periapsis {number}",
    )
    return [orbit, ascending_node, descending_node, periapsis]
