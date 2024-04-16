"""Take the Dataframe returned from transform.py and
upload it to a Microsoft SQL Server database."""

from dotenv import load_dotenv
from os import environ as ENV
import pandas as pd
from pymssql import connect, Connection


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


def get_botanist_ids(df: pd.DataFrame, conn: Connection, config) -> pd.DataFrame:
    """Look through botanist data in database:
     - If botanist doesn't exist, add them to database and get id,
     - If botanist does already exist, get their id as appear in table.
     Replace botanist columns in DataFrame to a column of ids."""
    botanists = df[['name', 'phone', 'email']].drop_duplicates()
    with conn.cursor() as cur:
        for _, botanist in botanists.iterrows():
            cur.execute(
                f"""SELECT * from {config['SCHEMA_NAME']}.botanist
                    WHERE name='{botanist.iloc[0]}'
                    AND phone='{botanist.iloc[1]}'
                    AND email='{botanist.iloc[2]}'""")
            botanist_info = cur.fetchall()
            if not botanist_info:
                cur.execute(
                    f"""INSERT INTO {config['SCHEMA_NAME']}.botanist
                        (name, phone, email) VALUES
                        ('{botanist.iloc[0]}', '{botanist.iloc[1]}', '{botanist.iloc[2]}')""")
                conn.commit()


def upload_watering_data(df: pd.DataFrame, conn: Connection):
    """Upload new watering data to database."""
    # Not sure if to_sql will work yet, use INSERT INTO if not.
    df['timestamp', 'plant_id'].to_sql(
        'watering', con=conn, index=False, schema=ENV['SCHEMA_NAME'], if_exists='append')
    conn.commit()


def upload_recordings_data(df: pd.DataFrame, conn: Connection):
    """Uploads transaction data to the database."""
    # Not sure if to_sql will work yet, use INSERT INTO if not.
    df['timestamp', 'temp', 'soil_moisture', 'botanist_id', 'plant_id'].to_sql('recordings', con=conn, index=False,
                                                                               schema=ENV['SCHEMA_NAME'], if_exists='append')
    conn.commit()


def load(df: pd.DataFrame) -> None:
    """main load function"""
    with connect_to_db(ENV) as conn:
        df = get_botanist_ids(df, conn, ENV)
        upload_watering_data(df, conn)
        upload_recordings_data(df, conn)


if __name__ == "__main__":
    load_dotenv()
    load(pd.DataFrame({'name': ['mickey', 'mickey', 'mouse'], 'phone': [
         '839429', '839429', '4872682'], 'email': ['mickeymouse@clubhouse.com', 'mickeymouse@clubhouse.com', 'anemail@email.com']}))
