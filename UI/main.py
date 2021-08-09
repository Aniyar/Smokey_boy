from flask import Flask, render_template, request
from flask.wrappers import Response
import requests
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/enter_coords', methods=['GET', 'POST'])
def enter_coords():
    if request.method == 'POST':
        fire_coords = (request.form['latitude'], request.form['longtitude'], request.form['radius'])
        query = {'lat':fire_coords[0], 'lon':fire_coords[1], 'appid':'d47b1b3abf26c63fbbf2c2469767c872'}
        response = requests.get('https://api.openweathermap.org/data/2.5/onecall?', params=query)
        cur_weather = response.json()["current"]
        data = (fire_coords[0], fire_coords[1], cur_weather["wind_speed"], cur_weather["wind_deg"], 
                cur_weather["temp"], cur_weather["humidity"])

        return render_template('request.html', item=data)
    
    elif request.method == 'GET':
        return render_template('map.html')




if __name__ == '__main__':
    app.run(debug = True)   