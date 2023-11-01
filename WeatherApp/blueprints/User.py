
from flask import Blueprint,request,render_template,flash,redirect
from db.database import db,Complain,Engineer,Instrument,Admin,StManager
import requests

blueprint_loginas = Blueprint("blueprint_loginas",__name__)
blueprint_loginAdmin = Blueprint("blueprint_loginAdmin",__name__)
blueprint_loginStManager = Blueprint("blueprint_loginStManager",__name__)
blueprint_dashboardAdmin = Blueprint("blueprint_dashboardAdmin",__name__)
blueprint_dashboardStManager = Blueprint("blueprint_dashboardStManager",__name__)
blueprint_adminloginpage = Blueprint("blueprint_adminloginpage",__name__)
blueprint_StManagerloginpage = Blueprint("blueprint_StManagerloginpage",__name__)
blueprint_engineerloginpage = Blueprint("blueprint_engineerloginpage",__name__)
blueprint_loginEngineer = Blueprint("blueprint_loginEngineer",__name__)
blueprint_dashboardEngineer = Blueprint("blueprint_dashboardEngineer",__name__)

@blueprint_loginas.route('/loginas')
def loginas():
    return render_template('loginpage.html')
@blueprint_adminloginpage.route('/AdminLoginPage')
def AdminLoginPage():
    return render_template('loginAdmin.html',role="Admin")
@blueprint_engineerloginpage.route('/LoginEngineerPage')
def LoginEngineerPage():
    return render_template('loginEngineer.html',role="Engineer")
@blueprint_StManagerloginpage.route('/loginStManagerPage')
def loginStManagerPage():
    return render_template('loginStManager.html',role="StManager")

@blueprint_loginAdmin.route('/loginAdmin',methods=['POST'])
def loginAdmin():
    error = 'Invalid credentials'
    admin = Admin.query.filter(Admin.email == request.form['user']).first()
    if admin and admin.password == request.form['pass']:
        flash('Successfully logged in')
        return redirect("/dashboardAdmin")
    flash('Invalid credentials')
    return render_template('loginAdmin.html',role="Admin",error=error)
    



@blueprint_loginStManager.route('/loginStManager', methods=['GET', 'POST'])
def loginStManager():
    error = 'Invalid credentials'
    manager = StManager.query.filter(StManager.email == request.form['user']).first()
    if manager and manager.password == request.form['pass']:
        flash('Successfully logged in')
        return redirect("/dashboardStManager")

    flash('Invalid credentials')
    return render_template('loginStManager.html',role="StManager",error=error)


@blueprint_loginEngineer.route('/loginEngineer', methods=['GET', 'POST'])
def loginStManager():
    error = 'Invalid credentials'
    manager = Engineer.query.filter(Engineer.email == request.form['user']).first()
    if manager and manager.password == request.form['pass']:
        flash('Successfully logged in')
        return redirect("/dashboardEngineer")

    flash('Invalid credentials')
    return render_template('loginEngineer.html',role="Engineer",error=error)

@blueprint_dashboardAdmin.route('/dashboardAdmin',methods=['POST', 'GET'])
def dashboard():
    ComplainList =[i.Id for i in Complain.query.filter(Complain.Resolvedby == None).all() ]
        
    #gets all the list of engineers
    eng = [i.Id for i in Engineer.query.all()]
    ins = [i.Id for i in Complain.query.all()]
    if request.method == 'POST':
        # db.create_all()
        #fetch all pending complains
        
        # return str(ComplainList)
        city_name = request.form.get('city')
        inputtsk= request.form.get('inputTasks')
        inputeng= request.form.get('inputEngnr')
        if inputtsk and inputeng :
            c = Complain.query.filter(Complain.Id)

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

            return render_template('dashboardAdmin.html',tasks = ComplainList,inss=ins,engnr=eng,temperature=temperature,pressure=pressure,humidity=humidity,city_name=city_name,condition=condition,wind=wind,desc=desc)
        except Exception as e:
            # flash('Enter only City Name')
            return render_template('dashboardAdmin.html',tasks = ComplainList,engnr=eng,inss=ins)
    else:
        return render_template('dashboardAdmin.html',tasks = ComplainList,engnr=eng,inss=ins)


@blueprint_dashboardStManager.route('/dashboardStManager',methods=['POST', 'GET'])
def dashboard():


    complain_list = [i.Id for i in Complain.query.all() ]
    Instrument_list = [i.Id for i in Instrument.query.all()]

    
    if request.method == 'POST':
        # db.create_all()
        #fetch all pending complains
        
        # return str(ComplainList)
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

            return render_template('/dashboardStManager.html',cmpln=complain_list,insid=Instrument_list,temperature=temperature,pressure=pressure,humidity=humidity,city_name=city_name,condition=condition,wind=wind,desc=desc)
        except Exception as e:
            # flash('Enter only City Name')
            return render_template('/dashboardStManager.html',cmpln=complain_list,insid=Instrument_list)
    return render_template('/dashboardStManager.html',cmpln=complain_list,insid=Instrument_list)
    



@blueprint_dashboardEngineer.route('/dashboardEngineer',methods=['POST', 'GET'])
def dashboard():
    complainlist = [i.Id for i in Complain.query.filter(Complain.is_active==True).all()]
 
    if request.method == 'POST':
        # db.create_all()
        #fetch all pending complains
        
        # return str(ComplainList)
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

            return render_template('/dashboardEngineer.html',comp =complainlist,temperature=temperature,pressure=pressure,humidity=humidity,city_name=city_name,condition=condition,wind=wind,desc=desc)
        except Exception as e:
            # flash('Enter only City Name')
            return render_template('/dashboardEngineer.html',comp =complainlist)
    return render_template('dashboardEngineer.html',comp =complainlist)
