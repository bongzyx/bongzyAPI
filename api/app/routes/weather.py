from dotenv import dotenv_values
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, send_file, Response
from app import app
import json
import urllib
import math
import io
import requests
from PIL import Image, ImageDraw, ImageFont

weather = Blueprint("weather", __name__, url_prefix="/weather")

config_values = dotenv_values(".env")


@weather.get("/getAll2Hours")
def get_all_2_hours():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/2-hour-weather-forecast?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}'
    )
    data = json.loads(r.content)
    return data


@weather.get("/getAll24Hours")
def get_all_24_hours():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/24-hour-weather-forecast?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}'
    )
    data = json.loads(r.content)
    return data


@weather.get("/getAll4Days")
def get_all_4_days():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/4-day-weather-forecast?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}'
    )
    data = json.loads(r.content)
    return data


@weather.get("/pm25")
def get_pm25():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/pm25?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}'
    )
    data = json.loads(r.content)
    return data


@weather.get("/psi")
def get_psi():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/psi?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}'
    )
    data = json.loads(r.content)
    return data


@weather.get("/uvi")
def get_uvi():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/uv-index?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}'
    )
    data = json.loads(r.content)
    return data


@weather.get("/humidity")
def get_humidity():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/relative-humidity?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}'
    )
    data = json.loads(r.content)
    return data


@weather.get("/rainingAreas")
def get_raining_areas():
    a, img = get_latest_picture()
    file_object = io.BytesIO()
    img.save(file_object, "PNG")

    return Response(file_object.getvalue(), mimetype="image/png")


def get_latest_picture():
    current_time = datetime.now()
    rounded_time = current_time.replace(
        minute=(5 * math.floor(current_time.minute / 5))
    )

    for i in range(0, 10):
        loop_time = rounded_time - timedelta(minutes=5 * i)
        str_time = loop_time.strftime("%Y%m%d%H%M")
        print(str_time)
        url = f"http://www.weather.gov.sg/files/rainarea/50km/v2/dpsri_70km_{str_time}0000dBR.dpsri.png"
        image = requests.get(url)
        if image.status_code == 200:
            img = io.BytesIO(image.content)
            background = Image.open(f"{app.root_path}/assets/base-853.png").convert(
                "RGBA"
            )
            foreground = Image.open(img).resize(
                (background.size[0], background.size[1]), resample=Image.NEAREST
            )

            foreground2 = foreground.copy()
            foreground2.putalpha(120)
            foreground.paste(foreground2, foreground)
            background.paste(foreground, mask=foreground)

            draw = ImageDraw.Draw(background)
            font = ImageFont.truetype(f"{app.root_path}/assets/Rubik-Bold.ttf", 22)
            draw.text(
                (background.size[0] - 255, background.size[1] - 70),
                loop_time.strftime("%H:%M   %d-%m-%Y"),
                fill=(69, 171, 214),
                font=font,
            )

            return loop_time, background
