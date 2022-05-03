from cmath import sin
import stat
from dotenv import dotenv_values
from datetime import datetime
from flask import Blueprint, jsonify, request
from app import app
import json
import requests
import xmltodict

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
            f"https://np.tritondigital.com/public/nowplaying?mountName={stationName}&numberToFetch={count}&eventType=track"
        )
        single_station_info = xmltodict.parse(r.content)
        if single_station_info["nowplaying-info-list"]:
            return jsonify(
                {
                    "stationName": stationName,
                    "timestamp": single_station_info["nowplaying-info-list"][
                        "nowplaying-info"
                    ]["@timestamp"],
                    "artist": single_station_info["nowplaying-info-list"][
                        "nowplaying-info"
                    ]["property"][3]["#text"],
                    "title": single_station_info["nowplaying-info-list"][
                        "nowplaying-info"
                    ]["property"][2]["#text"],
                    "cueTimeStart": single_station_info["nowplaying-info-list"][
                        "nowplaying-info"
                    ]["property"][1]["#text"],
                    "cueTimeDuration": single_station_info["nowplaying-info-list"][
                        "nowplaying-info"
                    ]["property"][0]["#text"],
                    "mergedName": single_station_info["nowplaying-info-list"][
                        "nowplaying-info"
                    ]["property"][3]["#text"]
                    + " - "
                    + single_station_info["nowplaying-info-list"]["nowplaying-info"][
                        "property"
                    ][2]["#text"],
                }
            )
        return jsonify([])
    else:
        all_stations_data = []
        for s in station_list:
            r = requests.get(
                f"https://np.tritondigital.com/public/nowplaying?mountName={s}&numberToFetch={count}&eventType=track"
            )
            single_station_info = xmltodict.parse(r.content)
            if single_station_info["nowplaying-info-list"]:
                clean_data = {
                    "stationName": s,
                    "timestamp": single_station_info["nowplaying-info-list"][
                        "nowplaying-info"
                    ]["@timestamp"],
                    "artist": single_station_info["nowplaying-info-list"][
                        "nowplaying-info"
                    ]["property"][3]["#text"],
                    "title": single_station_info["nowplaying-info-list"][
                        "nowplaying-info"
                    ]["property"][2]["#text"],
                    "cueTimeStart": single_station_info["nowplaying-info-list"][
                        "nowplaying-info"
                    ]["property"][1]["#text"],
                    "cueTimeDuration": single_station_info["nowplaying-info-list"][
                        "nowplaying-info"
                    ]["property"][0]["#text"],
                    "mergedName": single_station_info["nowplaying-info-list"][
                        "nowplaying-info"
                    ]["property"][3]["#text"]
                    + " - "
                    + single_station_info["nowplaying-info-list"]["nowplaying-info"][
                        "property"
                    ][2]["#text"],
                }
                all_stations_data.append(clean_data)
        return jsonify(all_stations_data)
