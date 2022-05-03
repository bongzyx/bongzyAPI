import stat
from dotenv import dotenv_values
from datetime import datetime
from flask import Blueprint, jsonify, request
from app import app
import json
import requests

radio = Blueprint("radio", __name__, url_prefix="/radio")

config_values = dotenv_values(".env")


@radio.get("/mediacorp")
def get_mediacorp_station():
    args = request.args
    stationName = args.get("stationName")
    count = args.get("count", 1)
    station_list = [
        "INDIEGO_S01AAC",
        "CLASS95AAC",
        "GOLD905AAC",
        "987FMAAC",
        "938NOWAAC",
        "SYMPHONY924AAC",
        "YES933AAC",
        "LOVE972FMAAC",
        "CAPITAL958FMAAC",
        "WARNA942FMAAC",
        "RIA897FMAAC",
        "OLI968FMAAC",
    ]
    if stationName in station_list:
        r = requests.get(
            f"https://www.melisten.sg/api/streaminfo/public/nowplaying?mountName={stationName}&numberToFetch={count}&eventType=track"
        )
        single_station_info = json.loads(r.content)
        return jsonify(single_station_info)
    else:
        all_stations_data = []
        for s in station_list:
            r = requests.get(
                f"https://www.melisten.sg/api/streaminfo/public/nowplaying?mountName={s}&numberToFetch={count}&eventType=track"
            )
            clean_data = json.loads(r.content)
            all_stations_data.append(
                {
                    "stationName": s,
                    "data": clean_data[0] if len(clean_data) != 0 else clean_data,
                }
            )
        return jsonify(all_stations_data)
