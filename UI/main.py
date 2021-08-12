from flask import Flask, render_template, request, redirect
from flask.wrappers import Response
import requests
from models.InventoryModel import InventoryModel
from db import DB


db = DB()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/enter_coords', methods=['GET', 'POST'])
def enter_coords():
    if request.method == 'POST':
        fire_rad = request.form["radius"]
        fire_coords = request.form["LngLat"].split(', ')
        query = {'lat':fire_coords[0], 'lon':fire_coords[1], 'appid':'d47b1b3abf26c63fbbf2c2469767c872'}
        response = requests.get('https://api.openweathermap.org/data/2.5/onecall?', params=query)
        cur_weather = response.json()["current"]
        data = (fire_coords[0], fire_coords[1], cur_weather["wind_speed"], cur_weather["wind_deg"], 
                cur_weather["temp"], cur_weather["humidity"])

        return render_template('request.html', item=data)
    
    elif request.method == 'GET':
        return render_template('main.html')


@app.route('/map', methods=['GET'])
def map():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    im = InventoryModel(db.get_connection())
    im.init_table()
    if request.method == 'GET':
        return render_template('inventory.html', inventory=im.get_all())
    elif request.method == 'POST':
        name, rclass, availability, location, description = request.form["name"], request.form["classselect"], request.form["availabilityselect"], request.form["location"], request.form["description"]
        im.insert(name, rclass, availability, location, description)


@app.route('/delete_item/<int:item_id>', methods=['GET'])
def delete_news(item_id):
    im = InventoryModel(db.get_connection())
    im.delete(item_id)
    return redirect("/inventory")


@app.route('/plan', methods=['GET'])
def plan():
    if request.method == 'GET':
        return render_template('map_interventions.html')


if __name__ == '__main__':
    app.run(debug = True)   