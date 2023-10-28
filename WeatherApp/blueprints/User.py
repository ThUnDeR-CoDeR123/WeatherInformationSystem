
from flask import Blueprint,request,render_template,flash
from db.database import db,Complain,Engineer,Instrument
import requests

blueprint_loginas = Blueprint("blueprint_loginas",__name__)
blueprint_loginAdmin = Blueprint("blueprint_loginAdmin",__name__)
blueprint_loginStManager = Blueprint("blueprint_loginStManager",__name__)
blueprint_dashboardAdmin = Blueprint("blueprint_dashboardAdmin",__name__)
blueprint_dashboardStManager = Blueprint("blueprint_dashboardStManager",__name__)
blueprint_assigntask = Blueprint("blueprint_assigntask",__name__)
blueprint_statusview = Blueprint("blueprint_statusview",__name__)
blueprint_generateReport = Blueprint("blueprint_generateReport",__name__)

@blueprint_loginas.route('/loginas')
def loginas():
    return render_template('loginpage.html')

@blueprint_loginAdmin.route('/loginAdmin',methods=['GET', 'POST'])
def loginAdmin():
    return render_template('loginAdmin.html',role="Admin")



@blueprint_loginStManager.route('/loginStManager', methods=['GET', 'POST'])
def loginStManager():
    return render_template('loginStManager.html',role="Admin")

@blueprint_dashboardAdmin.route('/dashboardAdmin',methods=['POST'])
def dashboard():
    if request.method == 'POST':
        # db.create_all()
        #fetch all pending complains
        ComplainList =[i.Id for i in Complain.query.filter(Complain.Resolvedby == None).all() ]
        
        #gets all the list of engineers
        eng = [i.Id for i in Engineer.query.all()]
        ins = [i.Id for i in Instrument.query.all()]
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

@blueprint_dashboardStManager.route('/dashboardStManager',methods=['POST'])
def dashboard():
    
    return render_template('dashboardStManager.html')


@blueprint_assigntask.route('/assigntask',methods=['POST','GET'])
def assigntask():

    #gets the submitted data from the dashboard
    try:
        complain = Complain.query.filter(Complain.Id==request.args.get('Complain')).first()
        engnr = Engineer.query.filter(Engineer.Id==request.args.get('Engineer')).first()

        # print(complain)
        engnr.Assignments.append(complain)
        db.session.commit()
        complain = [i.Id for i in Complain.query.filter(Complain.Resolvedby == None).all() ]
        engnr =  [i.Id for i in Engineer.query.all()]
        ins = [i.Id for i in Instrument.query.all()]
        # flash(f'You have successfully Assigned Task')
        return render_template('/dashboardAdmin.html',tasks = complain,engnr=engnr,inss = ins)
    except Exception as e:
        complain = [i.Id for i in Complain.query.filter(Complain.Resolvedby == None).all() ]
        engnr =  [i.Id for i in Engineer.query.all()]
        ins = [i.Id for i in Instrument.query.all()]
        # flash(f'error assigning')
        return render_template('/dashboardAdmin.html',tasks = complain,engnr=engnr,inss = ins)


@blueprint_statusview.route('/statusview', methods = ['GET'])
def statusview():
    complain = [i.Id for i in Complain.query.filter(Complain.Resolvedby == None).all() ]
    engnr =  [i.Id for i in Engineer.query.all()]
    ins = [i.Id for i in Instrument.query.all()]
    try:
        insId = request.args.get('instrument')
        ComplainId = Complain.query.filter(Complain.instrumentID==insId).first()
        if(ComplainId.is_active==True):
            return render_template('/dashboardAdmin.html',chk=2,tasks = complain,engnr=engnr,inss = ins)
        else:
            return render_template('/dashboardAdmin.html',chk=1,tasks = complain,engnr=engnr,inss = ins)
    except Exception as e:
            return render_template('/dashboardAdmin.html',chk=1,tasks = complain,engnr=engnr,inss = ins)


@blueprint_generateReport.route('/generateReport', methods = ['GET'])
def generateReport():
    print(request.args.get('ID'))
    print([i.Id for i in Instrument.query.all()])
    if int(request.args.get('ID'))  in [i.Id for i in Instrument.query.all()]:
        c = Complain.query.filter(Complain.instrumentID  == request.args.get('ID')).order_by(Complain.date.desc()).all()
        insdata = Instrument.query.filter(Instrument.Id == request.args.get('ID')).first()
        return render_template('report.html',complains = c,instrument_data = insdata)
    return ('<h1>Enter valid field</h1>')