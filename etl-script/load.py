"""Take the Dataframe returned from transform.py and 
upload it to a Microsoft SQL Server database."""

from dotenv import load_dotenv
from os import environ as ENV
import pandas as pd
from pymssql import connect, Connection


def connect_to_db(config) -> Connection:
    """Return a connection to redshift database using environment variables."""
    return connect(
        server=config['DB_HOST'],
        database=config['DB_NAME'],
        user=config['DB_USER'],
        password=config['DB_PASS'],
        port=config['DB_PORT'],
        as_dict=True
    )


def get_botanist_ids(df: pd.DataFrame, conn: Connection) -> pd.DataFrame:
    """Look through botanist data in database:
     - If botanist doesn't exist, add them to database and get id,
     - If botanist does already exist, get their id as appear in table.
     Replace botanist columns in DataFrame to a column of ids."""
    botanists = df[['name', 'phone', 'email']].unique()

    with conn.cursor as cur:
        for botanist in botanists:
            cur.execute(
                f"""SELECT * from botanists 
                WHERE name={botanist['name']} 
                AND phone={botanist['phone']} 
                AND email={botanist['email']}""")
            info = cur.fetchall()
            conn.commit()
            print(info)


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


def load(df=pd.DataFrame) -> None:
    """main load function"""
    with connect_to_db(ENV) as conn:
        df = get_botanist_ids(df, conn)
        upload_watering_data(df, conn)
        upload_recordings_data(df, conn)


if __name__ == "__main__":
    load_dotenv()
    load()
