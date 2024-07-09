from src.constants import *
from src.db import *

def process_subsession(db, session, subsession_id):
    RACE_SESSION = 6
    IRACING_SUBSESSION_DATA_URL = f"{Constants.IRACING_SUBSESSION_URL}?subsession_id={subsession_id}"
    data_cache = session.get(IRACING_SUBSESSION_DATA_URL)
    race_results = session.get(data_cache.json()['link']).json()

    total_laps = race_results['race_summary']['laps_complete']
    max_weeks = race_results['max_weeks']
    sof = race_results['event_strength_of_field']
    update_subsession(db, subsession_id, total_laps, max_weeks, sof)

    for subsession_results in race_results['session_results']:
        if subsession_results['simsession_type'] == RACE_SESSION:
            results = subsession_results['results']
            for result in results:
                finishing_position = result['finish_position'] + 1
                starting_position = result['starting_position'] + 1
                laps = result['laps_complete']
                cust_id = result['cust_id']
                car_id = result['car_id']
                led = result['laps_lead']
                dnf = result['reason_out_id'] != 0
                champ_points = result['champ_points']
                irating = result['newi_rating']
                irating_change = result['newi_rating'] - result['oldi_rating']
                display_name = result['display_name']
                car_name = result['car_name']
                car_num = result['livery']['car_number']
                interval = result['interval']

                club_name = result['club_name']
                helm_color1 = result['helmet']['color1']
                helm_color2 = result['helmet']['color2']
                helm_color3 = result['helmet']['color3']

                insert_driver(db, cust_id, display_name,club_name, helm_color1, helm_color2, helm_color3)
                insert_race_result(db, finishing_position, starting_position, laps, cust_id, car_id, led, dnf, champ_points, irating, irating_change, display_name, 
                                   subsession_id, car_name, car_num, interval)
    print(f"Subsession {subsession_id} PROCESSED ok")

'''
Retrieve results from a series in a season.
'''
def get_results(db, session, cust_id, series_id, season_year, season_quarter, category):
    IRACING_RESULTS_DATA_URL = f"{Constants.IRACING_RESULTS_URL}?season_year={season_year}&season_quarter={season_quarter}&cust_id={cust_id}&series_id={series_id}&official_only=true&event_types={Constants.EVENT_TYPE_RACE}"
    results = session.get(IRACING_RESULTS_DATA_URL)

    chunk_info = results.json()['data']['chunk_info']

    if chunk_info['num_chunks'] != 0:
        insert_season(db, cust_id, season_year, season_quarter, series_id)

    for item in chunk_info['chunk_file_names']:
        chunk_url = chunk_info['base_download_url'] + item
        subsessions = session.get(chunk_url)

        for subsession in subsessions.json():
            subsession_id = subsession['subsession_id']
            start_time = subsession['start_time']
            event_laps_complete = subsession['event_laps_complete']
            series_name = subsession['series_name']
            race_week_num = subsession['race_week_num']
            track_id = subsession['track']['track_id']
            max_weeks = 0
            caution_laps = subsession['num_caution_laps']
            winner_id = subsession['winner_group_id']
            total_laps = 0
            sof = 0

            subsession_inserted = insert_subsession(db, subsession_id, start_time, event_laps_complete, series_name, season_quarter, season_year, race_week_num, track_id, max_weeks, series_id, caution_laps, winner_id, total_laps, sof)
            if subsession_inserted:
                process_subsession(db, session, subsession_id)

    print('Process Finished')
