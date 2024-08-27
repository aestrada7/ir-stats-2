import psycopg2
import os
from dotenv import load_dotenv

try:
    load_dotenv()

    conn = psycopg2.connect(
        host = os.environ.get('POSTGRES_HOST'),
        dbname = os.environ.get('POSTGRES_DATABASE'),
        user = os.environ.get('POSTGRES_USER'),
        password = os.environ.get('POSTGRES_PASSWORD'),
        port = os.environ.get('POSTGRES_PORT')
    )
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE users(cust_id INTEGER PRIMARY KEY, email TEXT, encoded_pwd TEXT);''')
    cursor.execute('''CREATE TABLE drivers(cust_id INTEGER PRIMARY KEY, display_name TEXT, club_name TEXT, helm_color1 TEXT, helm_color2 TEXT, helm_color3 TEXT)''')
    cursor.execute('''CREATE TABLE seasons(cust_id INTEGER, series_id INTEGER, car INTEGER, season_year INTEGER, season_quarter INTEGER);''')
    cursor.execute('''CREATE TABLE subsessions(subsession_id INTEGER PRIMARY KEY, start_time TEXT, event_laps_complete INTEGER, series_name TEXT, season_quarter INTEGER,
                                            season_year INTEGER, race_week_num INTEGER, track_id INTEGER, max_weeks INTEGER, series_id INTEGER, caution_laps INTEGER,
                                            winner_id INTEGER, total_laps INTEGER, sof INTEGER)''')
    cursor.execute('''CREATE TABLE raceresults(finishing_position INTEGER, starting_position INTEGER, laps INTEGER, cust_id INTEGER, car_id INTEGER, led INTEGER, dnf BOOLEAN,
                                            champ_points INTEGER, irating INTEGER, irating_change INTEGER, display_name TEXT, subsession_id INTEGER, car_name TEXT,
                                            car_num TEXT, interval INTEGER)''')
    cursor.execute('''CREATE TABLE messages(cust_id INTEGER, season_year INTEGER, season_quarter INTEGER, race_week_num INTEGER, message TEXT, track_id INTEGER, series_id INTEGER)''')
    cursor.execute('''CREATE TABLE driver_subsessions(cust_id INTEGER, subsession_id INTEGER)''')
    conn.commit()
    cursor.close()
    conn.close()

    print('Tables created successfully!')

except psycopg2.Error as error:
    print('Error - ', error)