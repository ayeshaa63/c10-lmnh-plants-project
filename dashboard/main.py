from os import environ as ENV

import altair as alt
import pandas as pd
from pymssql import connect
from dotenv import load_dotenv
import streamlit as st


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


def get_data_from_db(conn, config) -> pd.DataFrame:
    '''Returns a transactions as DataFrame from database.'''
    with conn.cursor() as cur:

        cur.execute(f"SELECT * FROM {config['SCHEMA_NAME']}.recording;")

        rows = cur.fetchall()

        df = pd.DataFrame.from_dict(rows)

    return df


if __name__ == "__main__":

    load_dotenv()

    conn = connect_to_db(ENV)
    data = get_data_from_db(conn, ENV)

    st.title('LMNH Plants Dashboard')

    st.write(data)

    average_temps = data.groupby(['plant_id'])['temp'].mean().reset_index()

    avg_rev = alt.Chart(average_temps, title='Average Temperatures').mark_bar().encode(
        x='plant_id:N',
        y='temp'
    )

    st.altair_chart(avg_rev)

    temps = alt.Chart(data, title='Temperature over time').mark_line().encode(
        x='timestamp:T',
        y='temp:Q',
        color='plant_id:N'
    )

    st.altair_chart(temps)
