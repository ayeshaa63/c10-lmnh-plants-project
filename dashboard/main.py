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
    '''Returns a transactions as DataFrame from database.'''
    with conn.cursor() as cur:

        cur.execute(f"SELECT * FROM {config['SCHEMA_NAME']}.{table_name};")

        rows = cur.fetchall()

        df = pd.DataFrame.from_dict(rows)

    return df


def get_table_data(conn, config) -> pd.DataFrame:
    '''Returns a transactions as DataFrame from database.'''
    with conn.cursor() as cur:

        cur.execute(f"""SELECT p.name as 'Plant', r.timestamp as 'Time', r.temp as 'Temperature', r.soil_moisture as 'Soil moisture' 
                    FROM {config['SCHEMA_NAME']}.recording as r
                    JOIN {config['SCHEMA_NAME']}.plant as p
                    ON (r.plant_id = p.plant_id)
                    WHERE 0 < r.temp
                    AND r.temp < 40
                    AND 0 < r.soil_moisture
                    AND r.soil_moisture < 50;""")

        rows = cur.fetchall()

        df = pd.DataFrame.from_dict(rows)

    return df


def world_map(origin_data):

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
        tooltip='location_name'
    ).project(
        "equirectangular"
    ).properties(
        width=500,
        height=400
    )
    return background + points


def get_sidebar(some_data):
    """Set up streamlit sidebar with headers and filters."""
    st.sidebar.title('Filters')
    st.sidebar.subheader('Data analysis of plant conditions')
    sorted = st.sidebar.checkbox('Sorted',
                                 False)
    with st.sidebar.expander('Filter by plant'):
        plants = st.multiselect('Plants',
                                some_data['Plant'].sort_values().unique(),
                                default=some_data['Plant'].sort_values().unique())

    return plants, sorted


if __name__ == "__main__":

    load_dotenv()

    with connect_to_db(ENV) as conn:
        record_data = get_data_from_db(conn, ENV, 'recording')
        basic_stats = get_table_data(conn, ENV)

        # Title
        st.title('LMNH Plants Dashboard')

        # Sidebar
        plant_list, sorted = get_sidebar(basic_stats)

        # World Map
        w_map = world_map(get_data_from_db(
            connect_to_db(ENV), ENV, 'origin'))
        st.altair_chart(w_map, use_container_width=True)

        # Average temperatures graph
        average_temps = basic_stats.groupby(
            ['Plant'])['Temperature'].mean().reset_index()

        if sorted:
            x_avg_temp = alt.X('Plant:N').sort('-y')
        else:
            x_avg_temp = alt.X('Plant:N')
        avg_temp = alt.Chart(average_temps[average_temps['Plant'].isin(plant_list)], title='Average Temperatures').mark_bar().encode(
            x=x_avg_temp,
            y='Temperature',
            color='Plant:N'
        )

        st.altair_chart(avg_temp, use_container_width=True)

        # Temperature over time graph

        temps = alt.Chart(basic_stats[basic_stats['Plant'].isin(plant_list)], title='Temperature over time').mark_line().encode(
            x='hours(Time):T',
            y='mean(Temperature):Q',
            color='Plant:N'
        )

        st.altair_chart(temps, use_container_width=True)

        # Soil moisture over time graph

        moist = alt.Chart(basic_stats.loc[basic_stats['Plant'].isin(plant_list)], title='Soil moisture over time').mark_line().encode(
            x='hours(Time):T',
            y='mean(Soil moisture):Q',
            color='Plant:N'
        )

        st.altair_chart(moist, use_container_width=True)

        # All data in last 24 hours table

        st.write(basic_stats[basic_stats['Plant'].isin(
            plant_list)], use_container_width=True)

        # left, right = st.columns(2)
        # with left:

        # with right:
