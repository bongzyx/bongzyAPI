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


transport = Blueprint("transport", __name__, url_prefix="/transport")

lta_env = dotenv_values("lta.env")

f_camera_locations = open(f"{app.root_path}/assets/camera_location.json")
camera_locations = json.load(f_camera_locations)["data"]


@transport.get("/carparkLots")
def get_carpark_lots():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/transport/carpark-availability?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}'
    )
    data = json.loads(r.content)
    return data["items"][0]


@transport.get("/taxi")
def get_taxi_availability():
    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/transport/taxi-availability?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}'
    )
    data = json.loads(r.content)
    return data


@transport.get("/camera")
def get_camera():
    args = request.args
    location = args.get("location")

    now = datetime.now()
    r = requests.get(
        f'https://api.data.gov.sg/v1/transport/traffic-images?date_time={now.strftime("%Y-%m-%dT%H:%M:%S")}'
    )
    res_data = json.loads(r.content)

    if location:
        c_timestamp = ""
        if location == "wdls_bridge":
            for c in res_data["items"][0]["cameras"]:
                if c["camera_id"] == "2701":
                    res_data = requests.get(c["image"]).content
                    c_timestamp = c["timestamp"]

        if location == "wdls_checkpoint":
            for c in res_data["items"][0]["cameras"]:
                if c["camera_id"] == "2702":
                    res_data = requests.get(c["image"]).content
                    c_timestamp = c["timestamp"]

        img = Image.open(io.BytesIO(res_data))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(f"{app.root_path}/assets/Rubik-Bold.ttf", 72)
        draw.text(
            (100, 100),
            datetime.fromisoformat(c_timestamp).strftime("%H:%M   %d-%m-%Y"),
            fill=(255, 255, 255),
            font=font,
        )

        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format="PNG")
        img = imgByteArr.getvalue()
        response = make_response(img)
        response.headers.set("Content-Type", "image/png")
        return response

    for cam_group in camera_locations:
        for area_cam in cam_group["cameras"]:
            for c in res_data["items"][0]["cameras"]:
                if c["camera_id"] == area_cam["cameraId"]:
                    area_cam["imageUrl"] = c["image"]
                    area_cam["imageMetadata"] = c["image_metadata"]
                    area_cam["timestamp"] = c["timestamp"]

    return jsonify(camera_locations)


@transport.get("/busArrival")
def get_bus_arrival():
    args = request.args
    code = args.get("code")

    if re.match(r"\b\d{5}\b", str(code)):
        r = requests.get(
            f"http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode={code}",
            headers={"AccountKey": lta_env.get("AccountKey")},
        )
        data = json.loads(r.content)

        f = open(f"{app.root_path}/assets/BusStops.json")
        bus_stops_data = json.load(f)["data"]

        if data["Services"]:
            all_bus_services = []
            for service in data["Services"]:
                single_bus_info = {}
                single_bus_info["busNumber"] = service.get("ServiceNo")
                single_bus_info["busOperator"] = service.get("Operator")

                single_bus_info["timings"] = []

                if service["NextBus"]["EstimatedArrival"]:
                    next_dict = service["NextBus"]
                    next_dict["RelativeDuration"] = str(
                        calc_relative_time(service["NextBus"]["EstimatedArrival"])
                    )
                    single_bus_info["timings"].append(next_dict)
                if service["NextBus2"]["EstimatedArrival"]:
                    next_dict2 = service["NextBus2"]
                    next_dict2["RelativeDuration"] = str(
                        calc_relative_time(service["NextBus2"]["EstimatedArrival"])
                    )
                    single_bus_info["timings"].append(next_dict2)
                if service["NextBus3"]["EstimatedArrival"]:
                    next_dict3 = service["NextBus3"]
                    next_dict3["RelativeDuration"] = str(
                        calc_relative_time(service["NextBus3"]["EstimatedArrival"])
                    )
                    single_bus_info["timings"].append(next_dict3)
                print(next_dict)
                all_bus_services.append(single_bus_info)
            return jsonify(
                {
                    "info": list(
                        filter(lambda x: x["BusStopCode"] == str(code), bus_stops_data)
                    ),
                    "data": all_bus_services,
                }
            )
        return data
    return "invalid bus stop code"


def calc_relative_time(time):
    current_time = datetime.now()
    next_timing = datetime.fromisoformat(time).replace(tzinfo=None)
    time_diff = round((next_timing - current_time).total_seconds() / 60)
    return "Arr" if time_diff <= 1 else time_diff


@transport.get("/busInfo")
def get_bus_info():
    args = request.args
    bus_code = args.get("bus")

    bus_routes_file = open(f"{app.root_path}/assets/BusRoutes.json")
    bus_routes_data = json.load(bus_routes_file)["data"]

    bus_stops_file = open(f"{app.root_path}/assets/BusStops.json")
    bus_stops_data = json.load(bus_stops_file)["data"]

    result_list = list(
        filter(lambda x: x["ServiceNo"] == str(bus_code), bus_routes_data)
    )

    def get_sequence(val):
        return float(val.get("StopSequence"))

    result_list.sort(key=get_sequence)
    if len(result_list) != 0:
        for bus_stop in result_list:
            filter_result = list(
                filter(
                    lambda x: x["BusStopCode"] == str(bus_stop["BusStopCode"]),
                    bus_stops_data,
                )
            )
            bus_stop["Location"] = filter_result[0]

    return jsonify(
        {
            "info": result_list,
        }
    )
    # return "invalid bus stop code"
