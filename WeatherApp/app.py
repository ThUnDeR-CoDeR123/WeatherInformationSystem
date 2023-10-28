#make a virtual envirnment and install all the module 
#import the flask module
from flask import Flask,render_template,request,blueprints
from db.singleton import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from blueprints.User import blueprint_generateReport,blueprint_statusview,blueprint_assigntask,blueprint_dashboardAdmin,blueprint_dashboardStManager,blueprint_loginAdmin,blueprint_loginas,blueprint_loginStManager
import requests

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///db.sqlite3"
app.config['SECRECT_KEY']  = 'secret_key'
db.init_app(app)
#make a route and render all the html templates in this route

#________________________________________________________________REGISTER ALL BLUEPRINTS________________________________________________________________

app.register_blueprint(blueprint_dashboardAdmin)
app.register_blueprint(blueprint_assigntask)
app.register_blueprint(blueprint_dashboardStManager)
app.register_blueprint(blueprint_loginAdmin)
app.register_blueprint(blueprint_loginas)
app.register_blueprint(blueprint_loginStManager)
app.register_blueprint(blueprint_statusview)
app.register_blueprint(blueprint_generateReport)



    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form.get('city')

        try:
            #take a variable to show the json data
            r = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+city_name+'&appid=cbf1b9f6f3127d65b15aa57c0cd3d28a')

            #read the json object
            json_object = r.json()

            #take some attributes like temperature,humidity,pressure of this 
            temperature = int(json_object['main']['temp']-273.15) #this temparetuure in kelvin
            humidity = int(json_object['main']['humidity'])
            pressure = int(json_object['main']['pressure'])
            wind = int(json_object['wind']['speed'])

            #atlast just pass the variables
            condition = json_object['weather'][0]['main']
            desc = json_object['weather'][0]['description']
            return render_template('home.html',temperature=temperature,pressure=pressure,humidity=humidity,city_name=city_name,condition=condition,wind=wind,desc=desc)
        except:
            # flash('Enter only City Name')
            return render_template('home.html')
    else:
        return render_template('home.html') 
    

if __name__ == '__main__':
    app.config['SECRECT_KEY']  = 'secret_key'
    app.app_context().push()
    db.create_all()
    app.run(debug=True)

