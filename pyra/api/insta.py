from fastapi import APIRouter, Request, Response
from datetime import datetime, timedelta

from src.auth import *
from src.constants import *
from src.iracing_api import *

P1_LOGO = "https://media.discordapp.net/attachments/1253731028992917585/1254963577622630532/Default_Compact_White.png?ex=67a408e9&is=67a2b769&hm=7b4f0c6670f2edba30fb1d9d655cd6ba30a9f279a936f845f11ec8116e9ac8f1&=&format=webp&quality=lossless"
IMAGE_URL = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
#IMAGE_URL = "https://media.discordapp.net/attachments/1258787923277643818/1341581295838298216/p1_phoenix_25s2.png?ex=67b68472&is=67b532f2&hm=c90a65e9ed4eb778ab726ff4492c11d933f2c3ccfd11368845a28189be96de27&=&format=webp&quality=lossless"
#IMAGE_URL = "file:///Users/antonio.estrada/Desktop/a.png"

router = APIRouter()

def get_css(theme):
    text_color = "black" if theme == "light" else "white"
    return """
    <style>
    body {
        font-family: 'Industry-DemiItalic';
        color: """ + text_color + """;
        margin: 0;
    }
    .table {
        width: 1080px;
        height: 1350px;
        overflow: hidden;
    }
    .row {
        display: flex;
        font-size: 28px;
    }
    .field {
        padding: 2px 20px;
    }
    .field.pos {
        width: 40px;
    }
    .field.car_num {
        width: 80px;
    }
    .field.name {
        width: 480px;
    }
    .field.interval {
        width: 120px;
    }
    .field.led {
        width: 60px;
    }
    .gain {
        color: limegreen;
    }
    .loss {
        color: red;
    }
    .info_container {
        height: 310px;
    }
    .info {
        position: relative;
    }
    .info > .field {
        position: absolute;
        font-size: 28px;
        padding: 10px 45px;
    }
    .info > .field.season_logo {
        top: 0;
        left: 0;
        padding: 20px;
    }
    .info > .field.p1_logo {
        top: 0;
        right: 0;
        padding: 20px;
    }
    .info > .field.season_logo > img {
        max-height: 140px;
    }
    .info > .field.p1_logo > img {
        max-height: 140px;
    }
    .info > .field.track_name {
        top: 170px;
        left: 0;
    }
    .info > .field.sof {
        top: 170px;
        right: 0;
    }
    .info > .field.total_laps {
        top: 200px;
        left: 0;
    }
    .info > .field.time {
        top: 200px;
        right: 0;
    }
    .info > .field.season_name {
        top: 230px;
        left: 0;
    }
    .info > .field.legend {
        font-size: 24px;
        top: 270px;
        right: 100px;
    }
    .background {
        position: absolute;
        z-index: -1;
        overflow: hidden;
        width: 1080px;
        height: 1350px;
    }
    .background > img {
        filter: grayscale(1);
        width: 1080px;
        height: 1350px;
        object-fit: cover;
        object-position: 50% 50%;
    }
    .background .overlay {
        position: absolute;
        content: ' ';
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        background-color: rgba(28, 22, 48, 0.7);
    }
    .invert {
        filter: invert(1);
    }
    button {
        position: absolute;
        top: 10px;
        right: 10px;
    }
    </style>
    """

def get_js():
    return """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/dom-to-image/2.6.0/dom-to-image.min.js" integrity="sha512-01CJ9/g7e8cUmY0DFTMcUw/ikS799FHiOA0eyHsUWfOetgbx/t6oV4otQ5zXKQyIrQGTHSmRVPIgrgLcZi/WMA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script>
        function downloadImg(url, filename) {
            var a = document.createElement("a");
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
        }

        function printDiv(div) {
            let el = document.querySelector(div);
            domtoimage.toPng(el, { style: { transform: 'scale(2)', transformOrigin: 'top left' }, width: 2160, height: 2700 }).then(function (dataUrl) {
                var img = new Image();
                img.src = dataUrl;
                document.body.appendChild(img);
                downloadImg(dataUrl, 'ir-stats.png');
            });
        }
    </script>
    """

def readable_interval(interval, laps, total_laps):
    if interval == 0:
        return ""
    elif interval == -1:
        return f"-{total_laps - laps}"
    else:
        secs_down = float(interval / 10000)
        return "-{:.2f}".format(secs_down)
    
def gain_loss(start, finish):
    res = start - finish
    if res > 0:
        return f"<span class='gain'>+{res}</span>"
    elif res < 0:
        return f"<span class='loss'>{res}</span>"
    else:
        return f"{res}"
    
def format_car_number(car_num, car_color1, car_color2, car_num_color1, car_num_color2):
    invert = ""
    if car_color1 == car_num_color1:
        invert = "class='invert'"

    car_format = f"<div style='text-align: center; color: #{car_num_color1}; background-color: #{car_color1}; -webkit-text-stroke-width: 1px; -webkit-text-stroke-color: #{car_num_color2}'><span {invert}>{car_num}</span></div>"
    return car_format

def format_date(start_date):
    formatted_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ") - timedelta(hours=5)
    formatted_date = f"{formatted_date.year}/{formatted_date.month}/{formatted_date.day}"
    return formatted_date

@router.get("/insta")
def index(request: Request, id: int, usr: str, pwd: str, bg: str, theme):
    css = get_css(theme)
    js = get_js()
    session = auth_nodb(usr, pwd)
    RACE_SESSION = 6
    IRACING_SUBSESSION_DATA_URL = f"{Constants.IRACING_SUBSESSION_URL}?subsession_id={id}"
    data_cache = session.get(IRACING_SUBSESSION_DATA_URL)
    race_results = session.get(data_cache.json()['link']).json()

    total_laps = race_results['race_summary']['laps_complete']
    sof = race_results['event_strength_of_field']
    season_name = race_results['season_name']
    season_short_name = race_results['season_short_name']
    series_logo = f"{Constants.IRACING_IMAGE_BASE_URL}{race_results['series_logo']}"
    track_name = race_results['track']['track_name']
    start_time = race_results['start_time']

    data_table = ""

    for subsession_results in race_results['session_results']:
        if subsession_results['simsession_type'] == RACE_SESSION:
            results = subsession_results['results']
            for result in results:
                finishing_position = result['finish_position'] + 1
                starting_position = result['starting_position'] + 1
                laps = result['laps_complete']
                led = result['laps_lead']
                champ_points = result['champ_points']
                irating = result['newi_rating']
                display_name = result['display_name']
                car_name = result['car_name']
                car_num = result['livery']['car_number']
                car_color1 = result['livery']['color1']
                car_color2 = result['livery']['color2']
                car_color3 = result['livery']['color3']
                car_num_color1 = result['livery']['number_color1']
                car_num_color2 = result['livery']['number_color2']
                car_num_color3 = result['livery']['number_color3']
                interval = result['interval']

                club_name = result['club_name']
                data_table += f"""<div class='row'>
                    <div class='field pos'>{finishing_position}</div>
                    <div class='field car_num'>{format_car_number(car_num, car_color1, car_color2, car_num_color1, car_num_color2)}</div>
                    <div class='field name'>{display_name}</div>
                    <div class='field interval'>{readable_interval(interval, laps, total_laps)}</div>
                    <div class='field led'>{led}</div>
                    <div class='field gain_loss'>{gain_loss(starting_position, finishing_position)}</div>
                </div>"""
    
    session_info = f"""
        <div class='info_container'>
            <div class='info'>
                <div class='field season_logo'><img src='{series_logo}' /></div>
                <div class='field p1_logo'><img src='{P1_LOGO}' /></div>
                <div class='field track_name'>{track_name}</div>
                <div class='field season_name'>{season_short_name}</div>
                <div class='field total_laps'>{total_laps} laps</div>
                <div class='field sof'>SOF: {sof}</div>
                <div class='field time'>{format_date(start_time)}</div>
                <div class='field legend'>Interval&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Led</div>
            </div>
        </div>
    """

    background = ""
    if(IMAGE_URL):
        background = f"<div class='background'><img src='{IMAGE_URL}' /><div class='overlay'></div></div>"
    if(bg != ""):
        background = f"<div class='background'><img src='{bg}' /><div class='overlay'></div></div>"

    output = f"<html><head><title>Subsession</title>{css}{js}</head><body><div class='table'>{background}{session_info}{data_table}</div><button class='print' onclick='printDiv(\".table\")'>Print</button></body></html>"
    return Response(content=output, media_type='text/html; charset=utf-8')