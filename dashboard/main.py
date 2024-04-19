"""A script to generate a dashboard about the LMNH plants."""

from os import environ as ENV

import altair as alt
import pandas as pd
from pymssql import connect
from dotenv import load_dotenv
import streamlit as st
from vega_datasets import data


def connect_to_db(config):
    """Returns a live database connection."""
    return connect(
        server=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASS"],
        database=config["DB_NAME"],
        port=config["DB_PORT"],
        as_dict=True
    )


def get_data_from_db(conn, config, table_name) -> pd.DataFrame:
    '''Returns data as DataFrame from database.'''
    with conn.cursor() as cur:

        cur.execute(f"SELECT * FROM {config['SCHEMA_NAME']}.{table_name};")

        rows = cur.fetchall()

        data_f = pd.DataFrame.from_dict(rows)

    return data_f


def get_origin_data(conn, config) -> pd.DataFrame:
    '''Returns origin data as DataFrame from database.'''
    with conn.cursor() as cur:

        cur.execute(f"""SELECT p.name as Plant, o.location_name as Location, o.long, o.lat
                    FROM {config['SCHEMA_NAME']}.origin AS o
                    JOIN {config['SCHEMA_NAME']}.plant as p
                    ON (p.origin_id=o.origin_id)
                    """)

        rows = cur.fetchall()

        data_f = pd.DataFrame.from_dict(rows)

    return data_f


def get_table_data(conn, config) -> pd.DataFrame:
    '''Returns a recordings as DataFrame from database.'''
    with conn.cursor() as cur:

        cur.execute(f"""SELECT p.name AS 'Plant', r.timestamp AS 'Time', r.temp AS 'Temperature',
                    r.soil_moisture AS 'Soil moisture'
                    FROM {config['SCHEMA_NAME']}.recording AS r
                    JOIN {config['SCHEMA_NAME']}.plant AS p
                    ON (r.plant_id = p.plant_id)
                    WHERE 0 < r.temp
                    AND r.temp < 50
                    AND 0 < r.soil_moisture
                    AND r.soil_moisture < 100;""")

        rows = cur.fetchall()

        data_f = pd.DataFrame.from_dict(rows)

    return data_f


def world_map(origin_data):
    """Generates a world map of where the plants originated from."""
    countries = alt.topo_feature(data.world_110m.url, 'countries')
    background = alt.Chart(countries).mark_geoshape(
        fill='lightgray',
        stroke='white',
        tooltip=None
    ).project('equirectangular').properties(
        width=500,
        height=400
    )
    points = alt.Chart(origin_data).mark_circle(color='red', size=300).encode(
        longitude='lat:Q',
        latitude='long:Q',
        size=alt.value(10),
        tooltip=['Location', 'Plant']
    ).project(
        "equirectangular"
    ).properties(
        width=500,
        height=400
    )
    return alt.layer(background, points).properties(title='Plant origin map')


def get_sidebar(some_data):
    """Set up streamlit sidebar with headers and filters."""
    st.sidebar.title('Filters')
    st.sidebar.subheader('Data analysis of plant conditions')
    sort_ed = st.sidebar.checkbox('Sorted',
                                  False)
    with st.sidebar.expander('Filter by plant'):
        all_options = st.checkbox("Start from all plants", True, True)
        if all_options:
            plants = st.multiselect('Plants',
                                    some_data['Plant'].sort_values().unique(),
                                    default=some_data['Plant'].sort_values(
                                    ).unique())
        else:
            plants = st.multiselect('Plants',
                                    some_data['Plant'].sort_values().unique(),
                                    default=None)
    return plants, sort_ed


if __name__ == "__main__":

    load_dotenv()

    with connect_to_db(ENV) as connection:
        record_data = get_data_from_db(connection, ENV, 'recording')
        basic_stats = get_table_data(connection, ENV)

        # Title
        st.title('LMNH Plants Dashboard')

        # Sidebar
        plant_list, sorted_plants = get_sidebar(basic_stats)

        # World Map
        w_map = world_map(get_origin_data(
            connect_to_db(ENV), ENV))
        st.altair_chart(w_map, use_container_width=True)

        # Average temperatures graph
        average_temps = basic_stats.groupby(
            ['Plant'])['Temperature'].mean().reset_index()

        if sorted_plants:
            X_AVG_TEMP = alt.X('Plant:N').sort('-y')
        else:
            X_AVG_TEMP = alt.X('Plant:N')
        avg_temp = alt.Chart(average_temps[average_temps['Plant'].isin(plant_list)],
                             title='Average Temperatures').mark_bar().encode(
            x=X_AVG_TEMP,
            y='Temperature',
            color='Plant:N',
            tooltip=['Plant', 'Temperature']
        )

        st.altair_chart(avg_temp, use_container_width=True)

        # Temperature over time graph
        temps = alt.Chart(basic_stats[basic_stats['Plant'].isin(plant_list)],
                          title='Temperature over time').mark_line().encode(
            x='hours(Time):O',
            y='mean(Temperature):Q',
            color='Plant:N',
            tooltip='Plant'
        )

        st.altair_chart(temps, use_container_width=True)

        # Soil moisture over time graph

        moist = alt.Chart(basic_stats.loc[basic_stats['Plant'].isin(plant_list)],
                          title='Soil moisture over time').mark_line().encode(
            x='hours(Time):T',
            y='mean(Soil moisture):Q',
            color='Plant:N',
            tooltip=['Plant', 'mean(Soil moisture):Q']
        )

        st.altair_chart(moist, use_container_width=True)

        # All data in last 24 hours table

        st.write(basic_stats[basic_stats['Plant'].isin(
            plant_list)], use_container_width=True)
