from app import db,Complain,Engineer
from flask import Blueprint,request

issue_data = Blueprint("issue_data",__name__)
search_data = Blueprint("search_data",__name__)
assign_task = Blueprint("assign_task",__name__)
status_view = Blueprint("status_view",__name__)

@issue_data.route('/issue_data',methods=['POST'])
def issue_data(request):
    if request.method == 'POST':
        try:

            complain = Complain(instrumentID=request.form['instrument_id'],
                                details=request.form['details'])
            db.session.add(complain)
            db.session.commit()
        except Exception as e:
            return "Error creating : Please check the details"
    
@assign_task.route('/assign_task',methods=['POST'])
def assign_task(request):
    engineer = Engineer.query.filter(Engineer.name==request.form['engineer_name']).first()
    complain = Complain.query.filter(Complain.Id==request.form['complain_id']).first()
    complain.Resolvedby.append(engineer)
    db.session.commit()
    return "Success"

@status_view.route('status_view', methods=['POST'])
def status_view(request):
    complain = Complain.query.filter(Complain.Id == request.form['complain_id']).first()
    return complain.is_active
