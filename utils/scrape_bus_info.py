import requests
import json
import datetime
import re
from dotenv import dotenv_values


lta_env = dotenv_values("lta.env")
api_key = lta_env.get("AccountKey")


def get_bus_services():
    all_bus_services = []
    bus_services_count = 0
    while True:
        r = requests.get(
            url=f"http://datamall2.mytransport.sg/ltaodataservice/BusServices?$skip={bus_services_count}",
            headers={"AccountKey": api_key},
        )
        data = json.loads(r.content)
        if not data["value"]:
            break
        else:
            bus_services_count += 500
            all_bus_services += data["value"]
    print(len(all_bus_services))

    bus_services_json = {
        "timestamp": datetime.datetime.now().isoformat(),
        "data": all_bus_services,
    }
    f = open("BusServices.json", "w")
    f.write(json.dumps(bus_services_json))
    f.close()


def get_bus_routes():
    all_bus_routes = []
    bus_routes_count = 0
    while True:
        r = requests.get(
            url=f"http://datamall2.mytransport.sg/ltaodataservice/BusRoutes?$skip={bus_routes_count}",
            headers={"AccountKey": api_key},
        )
        data = json.loads(r.content)
        if not data["value"]:
            break
        else:
            bus_routes_count += 500
            all_bus_routes += data["value"]
    print(len(all_bus_routes))

    bus_routes_json = {
        "timestamp": datetime.datetime.now().isoformat(),
        "data": all_bus_routes,
    }
    f = open("BusRoutes.json", "w")
    f.write(json.dumps(bus_routes_json))
    f.close()


def get_bus_stops():
    all_bus_stops = []
    bus_stops_count = 0
    while True:
        r = requests.get(
            url=f"http://datamall2.mytransport.sg/ltaodataservice/BusStops?$skip={bus_stops_count}",
            headers={"AccountKey": api_key},
        )
        data = json.loads(r.content)
        if not data["value"]:
            break
        else:
            bus_stops_count += 500
            all_bus_stops += data["value"]
    print(len(all_bus_stops))

    bus_stops_json = {
        "timestamp": datetime.datetime.now().isoformat(),
        "data": all_bus_stops,
    }
    f = open("BusStops.json", "w")
    f.write(json.dumps(bus_stops_json))
    f.close()


# get_bus_routes()
# get_bus_services()
# get_bus_stops()

# read json
f = open("BusStops.json")
data = json.load(f)["data"]

print(list(filter(lambda x: x["BusStopCode"] == "47491", data)))
