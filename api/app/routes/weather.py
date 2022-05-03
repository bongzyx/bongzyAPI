from dotenv import dotenv_values
from datetime import datetime
from flask import Blueprint, jsonify
from app import app
import json
import urllib
import requests

weather = Blueprint('weather', __name__, url_prefix='/weather')

config_values = dotenv_values(".env")


@weather.get('/getAll2Hours')
def get_all_2_hours():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/2-hour-weather-forecast?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}')
    data = json.loads(r.content)
    return data


@weather.get('/getAll24Hours')
def get_all_24_hours():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/24-hour-weather-forecast?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}')
    data = json.loads(r.content)
    return data


@weather.get('/getAll4Days')
def get_all_4_days():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/4-day-weather-forecast?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}')
    data = json.loads(r.content)
    return data


@weather.get('/pm25')
def get_pm25():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/pm25?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}')
    data = json.loads(r.content)
    return data


@weather.get('/psi')
def get_psi():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/psi?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}')
    data = json.loads(r.content)
    return data


@weather.get('/uvi')
def get_uvi():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/uv-index?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}')
    data = json.loads(r.content)
    return data


@weather.get('/humidity')
def get_humidity():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/environment/relative-humidity?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}')
    data = json.loads(r.content)
    return data
