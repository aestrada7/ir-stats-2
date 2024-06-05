import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_database():
    """
    Connects to a PostgreSQL database using the provided environment variables for the host, database name, user, password, and port.

    Returns:
        conn (psycopg2.extensions.connection): A connection object to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        host = os.environ.get('POSTGRES_HOST'),
        dbname = os.environ.get('POSTGRES_DATABASE'),
        user = os.environ.get('POSTGRES_USER'),
        password = os.environ.get('POSTGRES_PASSWORD'),
        port = os.environ.get('POSTGRES_PORT')
    )
    return conn

def close_database(conn):
    """
    Closes a connection to a PostgreSQL database.

    Args:
        conn (psycopg2.extensions.connection): A connection object to the PostgreSQL database.

    Returns:
        None
    """
    conn.close()

def upsert_user(db, email, cust_id, encoded_pwd):
    try:
        conn = db
        cursor = conn.cursor()
        insert_sql = '''
            INSERT INTO users(cust_id, email, encoded_pwd)
            VALUES(%s, %s, %s) ON CONFLICT(cust_id) DO UPDATE
            SET (cust_id, email) = (EXCLUDED.cust_id, EXCLUDED.email)
        '''
        cursor.execute(insert_sql, (cust_id, email, encoded_pwd))
        conn.commit()
        cursor.close()
        print('session ok')

    except psycopg2.Error as error:
        print('Error - ', error)

def insert_driver(db, cust_id, display_name, club_name, helm_color1, helm_color2, helm_color3):
    try:
        conn = db
        cursor = conn.cursor()

        select_sql = '''
            SELECT cust_id FROM drivers WHERE cust_id = %s
        '''
        cursor.execute(select_sql, (cust_id,))
        result = cursor.fetchone()
        if result:
            print(f'driver {cust_id} already exists')
            cursor.close()
            return

        insert_sql = '''
            INSERT INTO drivers(cust_id, display_name, club_name, helm_color1, helm_color2, helm_color3)
            VALUES(%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_sql, (cust_id, display_name, club_name, helm_color1, helm_color2, helm_color3))
        conn.commit()
        cursor.close()

    except psycopg2.Error as error:
        print('Error - ', error)

def insert_race_result(db, finishing_position, starting_position, laps, cust_id, car_id, led, dnf, champ_points, irating, irating_change, display_name, 
                       subsession_id, car_name, car_num, interval):
    try:
        conn = db
        cursor = conn.cursor()
        insert_sql = '''
            INSERT INTO raceresults(finishing_position, starting_position, laps, cust_id, car_id, led, dnf, champ_points, irating, irating_change, display_name, 
                                    subsession_id, car_name, car_num, interval)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_sql, (finishing_position, starting_position, laps, cust_id, car_id, led, dnf, champ_points, irating, irating_change, display_name, subsession_id, car_name, car_num, interval))
        conn.commit()
        cursor.close()

    except psycopg2.Error as error:
        print('Error - ', error)

'''
Inserts subsession into the db
'''
def insert_subsession(db, subsession_id, start_time, event_laps_complete, series_name, season_quarter, season_year, race_week_num, track_id, max_weeks, series_id, caution_laps, winner_id, total_laps, sof):
    try:
        conn = db
        cursor = conn.cursor()
        select_sql = '''
            SELECT subsession_id FROM subsessions WHERE subsession_id = %s
        '''
        cursor.execute(select_sql, (subsession_id,))
        row = cursor.fetchone()
        if row:
            print(f'subsesh {subsession_id} already exists')
            return False

        insert_sql = '''
            INSERT INTO subsessions(subsession_id, start_time, event_laps_complete, series_name, season_quarter, season_year, race_week_num, track_id, max_weeks, series_id, 
                                    caution_laps, winner_id, total_laps, sof)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_sql, (subsession_id, start_time, event_laps_complete, series_name, season_quarter, season_year, race_week_num, track_id, max_weeks, series_id, caution_laps, winner_id, total_laps, sof))
        conn.commit()
        cursor.close()

        print(f'subsesh {subsession_id} written ok!')
        return True

    except psycopg2.Error as error:
        print('Error - ', error)

'''
Adds info to the subsesh
'''
def update_subsession(db, subsession_id, total_laps, max_weeks, sof):
    try:
        conn = db
        cursor = conn.cursor()
        update_sql = '''
            UPDATE subsessions SET total_laps = %s, max_weeks = %s, sof = %s WHERE subsession_id = %s
        '''
        cursor.execute(update_sql, (total_laps, max_weeks, sof, subsession_id))
        conn.commit()
        cursor.close()
        print(f'subsesh {subsession_id} updated correctly with sof {sof}!')

    except psycopg2.Error as error:
        print('Error - ', error)