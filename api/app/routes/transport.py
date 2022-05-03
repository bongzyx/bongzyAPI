from dotenv import dotenv_values
from datetime import datetime
from flask import Blueprint, jsonify, request, send_file, make_response
from app import app
import json
import urllib
import requests
import io
from PIL import Image

transport = Blueprint('transport', __name__, url_prefix='/transport')

config_values = dotenv_values(".env")


@transport.get('/carparkLots')
def get_carpark_lots():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/transport/carpark-availability?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}')
    data = json.loads(r.content)
    return data['items'][0]


@transport.get('/taxi')
def get_taxi_availability():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/transport/taxi-availability?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}')
    data = json.loads(r.content)
    return data


@transport.get('/camera')
def get_camera():
    args = request.args
    location = args.get('location')

    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/transport/traffic-images?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}')
    data = json.loads(r.content)
    if location:
        if location == "wdls_bridge":
            for c in data['items'][0]['cameras']:
                if c['camera_id'] == '2701':
                    data = requests.get(c['image']).content
                    img = Image.open(io.BytesIO(data))
                    imgByteArr = io.BytesIO()
                    img.save(imgByteArr, format='PNG')
                    img = imgByteArr.getvalue()
                    response = make_response(img)
                    response.headers.set('Content-Type', 'image/png')
                    return response
        if location == "wdls_checkpoint":
            for c in data['items'][0]['cameras']:
                if c['camera_id'] == '2702':
                    data = requests.get(c['image']).content
                    img = Image.open(io.BytesIO(data))
                    imgByteArr = io.BytesIO()
                    img.save(imgByteArr, format='PNG')
                    img = imgByteArr.getvalue()
                    response = make_response(img)
                    response.headers.set('Content-Type', 'image/png')
                    return response
    return data
