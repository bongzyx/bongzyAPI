from flask import Blueprint, jsonify

from app import app
from ..utils.nea_weather import SongReader

from dotenv import dotenv_values

config = dotenv_values(".env")
print(config)


weather = Blueprint('weather', __name__, url_prefix='/weather')


@weather.get('/startScan')
def startScan():

    return jsonify("hi")
