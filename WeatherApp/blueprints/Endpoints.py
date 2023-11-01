from db.database import Complain,Engineer,Instrument
from flask import Blueprint,request,redirect,render_template
from db.singleton import db

blueprint_statusView = Blueprint("blueprint_statusView",__name__)
blueprint_issuetask = Blueprint("blueprint_issuetask",__name__)
blueprint_statusupdate = Blueprint("blueprint_statusupdate",__name__)
blueprint_assigntask = Blueprint("blueprint_assigntask",__name__)
blueprint_statusview = Blueprint("blueprint_statusview",__name__)
blueprint_generateReport = Blueprint("blueprint_generateReport",__name__)




@blueprint_generateReport.route('/generateReport', methods = ['GET'])
def generateReport():
    print(request.args.get('ID'))
    print([i.Id for i in Instrument.query.all()])
    if int(request.args.get('ID'))  in [i.Id for i in Instrument.query.all()]:
        c = Complain.query.filter(Complain.instrumentID  == request.args.get('ID')).order_by(Complain.date.desc()).all()
        insdata = Instrument.query.filter(Instrument.Id == request.args.get('ID')).first()
        return render_template('report.html',complains = c,instrument_data = insdata)
    return ('<h1>Enter valid field</h1>')



@blueprint_issuetask.route('/issue_task',methods=['POST'])
def issue_data():
    if request.method == 'POST':
        try:

            complain = Complain(instrumentID=request.form['instrumentID'],
                                details=request.form['Complain_Details'])
            db.session.add(complain)
            db.session.commit()
        except Exception as e:
            pass
    return redirect('/dashboardStManager')
    



@blueprint_statusupdate.route('/status_update', methods=['POST','GET'])
def status_view():
    print("trigerred",request)
    complain = Complain.query.filter(Complain.Id == request.args.get('complain_id')).first()
    complain.is_active = False
    db.session.commit()

    return redirect('/dashboardEngineer')




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
        ins = [i.Id for i in Complain.query.all()]
        # flash(f'You have successfully Assigned Task')
        return render_template('/dashboardAdmin.html',tasks = complain,engnr=engnr,inss = ins)
    except Exception as e:
        complain = [i.Id for i in Complain.query.filter(Complain.Resolvedby == None).all() ]
        engnr =  [i.Id for i in Engineer.query.all()]
        ins = [i.Id for i in Complain.query.all()]
        # flash(f'error assigning')
        return render_template('/dashboardAdmin.html',tasks = complain,engnr=engnr,inss = ins)


@blueprint_statusview.route('/statusview', methods = ['GET'])
def statusview():
    complain = [i.Id for i in Complain.query.filter(Complain.Resolvedby == None).all() ]
    engnr =  [i.Id for i in Engineer.query.all()]
    ins = [i.Id for i in Complain.query.all()]
    try:
        CmplnId = request.args.get('instrument')
        ComplainId = Complain.query.filter(Complain.Id==CmplnId).first()
        if(ComplainId.is_active==True):
            return render_template('/dashboardStManager.html',chk=1,tasks = complain,engnr=engnr,cmpln = ins)
        else:
            return render_template('/dashboardStManager.html',chk=2,tasks = complain,engnr=engnr,cmpln = ins)
    except Exception as e:
            return render_template('/dashboardStManager.html',tasks = complain,engnr=engnr,cmpln = ins)


@blueprint_statusView.route('/status_view', methods=['POST','GET'])
def status_view():
    complain_list = [i.Id for i in Complain.query.all() ]
    Instrument_list = [i.Id for i in Instrument.query.all()]
   
    try:

        CmplnId = request.args.get('instrument')
        ComplainId = Complain.query.filter(Complain.Id==CmplnId).first()
        if(ComplainId.is_active==True):
            print("triggerred", ComplainId.is_active)
            return render_template('/dashboardStManager.html',chk=1,cmpln=complain_list,insid=Instrument_list)
        else:
            print("triggerred", ComplainId.is_active)
            return render_template('/dashboardStManager.html',chk=2,cmpln=complain_list,insid=Instrument_list)
    except Exception as e:
            return render_template('/dashboardStManager.html',cmpln=complain_list,insid=Instrument_list)
    