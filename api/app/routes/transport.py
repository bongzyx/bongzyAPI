from dotenv import dotenv_values
from datetime import datetime
from flask import Blueprint, jsonify, request, send_file, make_response
from app import app
import json
import urllib
import requests
import io
import re
from PIL import Image, ImageDraw, ImageFont


transport = Blueprint('transport', __name__, url_prefix='/transport')

lta_env = dotenv_values("lta.env")


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
    c_timestamp = ''
    if location:
        if location == "wdls_bridge":
            for c in data['items'][0]['cameras']:
                if c['camera_id'] == '2701':
                    data = requests.get(c['image']).content
                    c_timestamp = c['timestamp']

        if location == "wdls_checkpoint":
            for c in data['items'][0]['cameras']:
                if c['camera_id'] == '2702':
                    data = requests.get(c['image']).content
                    c_timestamp = c['timestamp']

        img = Image.open(io.BytesIO(data))
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype(r'./assets/Rubik-Bold.ttf', 72)
        draw.text((100, 100), datetime.fromisoformat(c_timestamp).strftime("%H:%M   %d-%m-%Y"), fill=(
            255, 255, 255), font=font)

        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format='PNG')
        img = imgByteArr.getvalue()
        response = make_response(img)
        response.headers.set('Content-Type', 'image/png')
        return response
    return data


@transport.get('/bus')
def get_bus():
    args = request.args
    code = args.get('code')

    now = datetime.now()
    if re.match(r"\b\d{5}\b", str(code)):
        r = requests.get(
            f'http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode={code}',
            headers={"AccountKey": lta_env.get("AccountKey")})
        data = json.loads(r.content)
        if data["Services"]:
            all_bus_services = []
            for index, service in enumerate(data["Services"]):
                single_bus_info = {}
                single_bus_info['busNumber'] = service.get(
                    "ServiceNo")
                single_bus_info['busOperator'] = service.get(
                    "Operator")

                single_bus_info['timings'] = []

                if service["NextBus"]["EstimatedArrival"]:
                    next_dict = service["NextBus"]
                    next_dict['duration'] = str(
                        calcTime(service["NextBus"]["EstimatedArrival"]))
                    single_bus_info['timings'].append(next_dict)
                if service["NextBus2"]["EstimatedArrival"]:
                    next_dict2 = service["NextBus"]
                    next_dict2['duration'] = str(
                        calcTime(service["NextBus2"]["EstimatedArrival"]))
                    single_bus_info['timings'].append(next_dict2)
                if service["NextBus3"]["EstimatedArrival"]:
                    next_dict3 = service["NextBus"]
                    next_dict3['duration'] = str(
                        calcTime(service["NextBus3"]["EstimatedArrival"]))
                    single_bus_info['timings'].append(next_dict3)

                all_bus_services.append(single_bus_info)
            return jsonify(all_bus_services)

        return data
    return "invalid bus stop code"


def calcTime(time):
    currentTime = datetime.now()

    nextTiming = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z").replace(
        tzinfo=None
    )

    timeDiff = nextTiming - currentTime
    timeDiff = round(timeDiff.total_seconds() / 60)

    if timeDiff <= 1:
        return "Arr"
    elif timeDiff >= 1:
        return timeDiff
    else:
        return None
