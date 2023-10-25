#make a virtual envirnment and install all the module 
#import the flask module
from flask import Flask,render_template,request,flash
import requests
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
# app.config['SECRECT_KEY']  = 'secret_key'
# db=SQLAlchemy(app)
#make a route and render all the html templates in this route
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

@app.route('/loginas')
def loginas():
    return render_template('loginpage.html')

@app.route('/login/<int:Id>',methods=['GET', 'POST'])
def login(Id):
    if request.method == 'POST':
        a=request.form['user']
        return a

    else:

        if Id==1:
            return render_template('login.html',role="Admin")
        elif Id==2:
            return render_template('login.html',role="Regional Station Manager")
        return render_template('login.html',role="Engineer")       



@app.route('/dashboard',methods=['POST'])
def dashboard():
    return request.form.get('user')

if __name__ == '__main__':
    app.run(debug=True)
