from flask import render_template
from flask import current_app as app
from application.models import *
from flask_security import current_user
from application import tasks
from main import cache




@app.route("/")
def home():
    return render_template("home.html")


@app.route('/analysis')
@cache.cached(timeout= 20)
def send_analysis_report():
    tasks.create_admin_report.apply_async()
    return {'message': 'Analysis report will be mailed shortly.'}



@app.get('/create_csv/<int:category_id>')
@cache.cached(timeout=10)
def StoreManagerCsv(category_id):
    recipient_email = current_user.email_address
    task = tasks.generate_report.apply_async(args=[category_id, recipient_email])
    return {"message" : "Category details will be mailed shortly."}


@app.get('/user_requested_report/<int:user_id>')
@cache.cached(timeout=20)
def user_report(user_id):
    task = tasks.user_requested_report.apply_async([user_id])
    return {"message" : "Mail will be sent shortly!"}
