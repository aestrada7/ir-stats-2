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
        print('Session ok')

    except psycopg2.Error as error:
        print('Error - ', error)

def insert_season(db, cust_id, season_year, season_quarter, series_id):
    try:
        conn = db
        cursor = conn.cursor()

        select_sql = '''
            SELECT cust_id FROM seasons WHERE cust_id = %s AND season_year = %s AND season_quarter = %s AND series_id = %s
        '''
        cursor.execute(select_sql, (cust_id, season_year, season_quarter, series_id))
        result = cursor.fetchone()
        if result:
            print(f'Season {season_year}/{season_quarter} already exists')
            cursor.close()
            return

        insert_sql = '''
            INSERT INTO seasons(cust_id, season_year, season_quarter, series_id)
            VALUES(%s, %s, %s, %s)
        '''
        cursor.execute(insert_sql, (cust_id, season_year, season_quarter, series_id))
        conn.commit()
        cursor.close()
        print(f'Season {season_year}/{season_quarter} added correctly.')

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
            print(f'Driver {cust_id} already exists')
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

def get_drivers(db, params, is_id, maxItems):
    try:
        conn = db
        cursor = conn.cursor()
        select_sql = '''
            SELECT cust_id, display_name, club_name, helm_color1, helm_color2, helm_color3 FROM drivers 
        '''
        if is_id:
            select_sql += 'WHERE cust_id = %s'
            cursor.execute(select_sql, (params['custid'],))
        else:
            select_sql += 'WHERE display_name ILIKE %s LIMIT %s'
            cursor.execute(select_sql, ('%' + params['displayname'] + '%', maxItems))
        result = cursor.fetchall()
        cursor.close()
        return result

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
            print(f'Subsession {subsession_id} already exists, skipping.')
            return False

        insert_sql = '''
            INSERT INTO subsessions(subsession_id, start_time, event_laps_complete, series_name, season_quarter, season_year, race_week_num, track_id, max_weeks, series_id, 
                                    caution_laps, winner_id, total_laps, sof)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_sql, (subsession_id, start_time, event_laps_complete, series_name, season_quarter, season_year, race_week_num, track_id, max_weeks, series_id, caution_laps, winner_id, total_laps, sof))
        conn.commit()
        cursor.close()

        print(f'Subsession {subsession_id} created.')
        return True

    except psycopg2.Error as error:
        print('Error - ', error)

'''
Adds info to the subsession
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
        print(f'Subsession {subsession_id} updated correctly with sof: {sof}')

    except psycopg2.Error as error:
        print('Error - ', error)

def get_messages(db, cust_id, season_year, season_quarter, race_week_num, series_id):
    try:
        conn = db
        cursor = conn.cursor()
        select_sql = '''
            SELECT * FROM messages WHERE cust_id = %s AND season_year = %s AND season_quarter = %s AND race_week_num = %s AND series_id = %s
        '''
        cursor.execute(select_sql, (cust_id, season_year, season_quarter, race_week_num, series_id))
        result = cursor.fetchall()
        cursor.close()
        return result

    except psycopg2.Error as error:
        print('Error - ', error)

def get_messages_by_track(db, cust_id, track_id, series_id):
    try:
        conn = db
        cursor = conn.cursor()
        select_sql = '''
            SELECT * FROM messages WHERE cust_id = %s AND track_id = %s AND series_id = %s
        '''
        cursor.execute(select_sql, (cust_id, track_id, series_id))
        result = cursor.fetchall()
        cursor.close()
        return result

    except psycopg2.Error as error:
        print('Error - ', error)

def upsert_message(db, cust_id, season_year, season_quarter, race_week_num, message, track_id, series_id):
    try:
        conn = db
        cursor = conn.cursor()
        select_sql = '''
            SELECT * FROM messages WHERE cust_id = %s AND season_year = %s AND season_quarter = %s AND race_week_num = %s AND series_id = %s
        '''
        cursor.execute(select_sql, (cust_id, season_year, season_quarter, race_week_num, series_id))
        row = cursor.fetchone()
        if row:
            update_sql = '''
                UPDATE messages SET message = %s WHERE cust_id = %s AND season_year = %s AND season_quarter = %s AND race_week_num = %s AND series_id = %s
            '''
            cursor.execute(update_sql, (message, cust_id, season_year, season_quarter, race_week_num, series_id))
            conn.commit()
            cursor.close()
            print(f'Message updated correctly for cust_id {cust_id}, season_year {season_year}, season_quarter {season_quarter}, race_week_num {race_week_num}, series_id {series_id}')
            return
        
        insert_sql = '''
            INSERT INTO messages(cust_id, season_year, season_quarter, race_week_num, message, track_id, series_id)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_sql, (cust_id, season_year, season_quarter, race_week_num, message, track_id, series_id))
        conn.commit()
        cursor.close()
        print(f'Message created correctly for cust_id {cust_id}, season_year {season_year}, season_quarter {season_quarter}, race_week_num {race_week_num}, series_id {series_id}')

    except psycopg2.Error as error: 
        print('Error - ', error)