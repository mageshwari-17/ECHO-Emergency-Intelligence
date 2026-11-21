import folium
import streamlit as st
from streamlit_folium import st_folium


def show_emergency_map(location, risk_level, incident_type):

    # Demo coordinates for locations
    locations = {
        "chennai": [13.0827, 80.2707],
        "coimbatore": [11.0168, 76.9558],
        "madurai": [9.9252, 78.1198],
        "trichy": [10.7905, 78.7047],
        "salem": [11.6643, 78.1460],
        "vellore": [12.9165, 79.1325],
        "bangalore": [12.9716, 77.5946],
    }

    city = location.strip().lower()

    coordinates = locations.get(city, [11.0168, 76.9558])

    # Map zoom depends on emergency risk
    zoom = 12

    emergency_map = folium.Map(
        location=coordinates,
        zoom_start=zoom,
        tiles="CartoDB positron"
    )

    # Risk color
    colors = {
        "CRITICAL": "red",
        "HIGH": "orange",
        "MEDIUM": "blue",
        "LOW": "green"
    }

    color = colors.get(risk_level, "blue")

    # Emergency location marker
    folium.Marker(
        location=coordinates,
        popup=f"""
        <b>ECHO Emergency Alert</b><br>
        Incident: {incident_type}<br>
        Risk: {risk_level}<br>
        Location: {location}
        """,
        tooltip="Emergency Incident Location",
        icon=folium.Icon(color=color, icon="warning")
    ).add_to(emergency_map)

    # Circle showing affected zone
    folium.Circle(
        location=coordinates,
        radius=1500,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.15,
        popup="Estimated Emergency Zone"
    ).add_to(emergency_map)

    # Display map
    st_folium(
        emergency_map,
        width=None,
        height=450,
        key="echo_emergency_map"
    )

    st.caption(
        "⚠️ Location markers are demo coordinates. "
        "They do not represent verified emergency locations."
    )