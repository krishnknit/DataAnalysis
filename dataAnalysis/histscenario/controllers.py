from flask import render_template, Blueprint, request, make_response
from dataAnalysis.histscenario.forms import HistScenarioForm
from dataAnalysis import app
import pymssql

##############################################################################
histscenario = Blueprint('histscenario', __name__, url_prefix='/histscenario')
##############################################################################


@histscenario.route('/create', methods=['GET', 'POST'])
def create():
	form = HistScenarioForm()
	title = "create Historical scenario Data"
	choices = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5, 'tenth': 10}

	if request.method == 'POST' and form.validate_on_submit():
		bus_dt = form.start_date.data
		liq_period = choices.get(request.form.get('liquidation_period'), 0)
		look_back_period = choices.get(request.form.get('lock_back_period'), 0)

		cur = getConnection()
		#cur.execute("select * from yld_crv_hist_v")
		#cur.execute("EXEC s_SGD_CPA_raw_data_R @bus_dt = '1990-01-10', @liq_period = 10, @look_back_period = 5")
		cur.execute("EXEC s_SGD_CPA_raw_data_R @bus_dt = '{}', @liq_period = {}, @look_back_period = {}".format(bus_dt, liq_period, look_back_period))

		rows = cur.fetchall();

		# print app.config['USERNAME']
		# print app.config['PASSWORD']
		print rows
		return render_template("histscenario/list.html",rows = rows)

	return (render_template('histscenario/form.html', form=form, title=title))

@histscenario.route('/add', methods=['GET', 'POST'])
def add():
	form = HistScenarioForm(request.form)
	title = "Add Historical Scenario data"

	if request.method == 'POST' and form.validate_on_submit():
		return "Under construction"
	return (make_response(render_template('histscenario/form.html', form=form, title=title)))


@histscenario.route('/import', methods=['GET', 'POST'])
def histImport():
	return "This page is under construction....."
	#return render_template('histscenario/import.html')

@histscenario.route('/addRemove', methods=['GET', 'POST'])
def addRemove():
	return "This page is under construction....."
	#return render_template('histscenario/addRemove.html')

def getConnection():
	con = pymssql.connect(  app.config['HOSTNAME'],
								app.config['USERNAME'],
								app.config['PASSWORD'],
								app.config['DBNAME'],
								app.config['PORT'])

	cursor = con.cursor()

	return cursor