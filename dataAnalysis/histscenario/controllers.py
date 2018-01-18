from flask import render_template, Blueprint, request, make_response
from dataAnalysis.histscenario.forms import HistScenarioForm, RunAnalysisForm
from dataAnalysis import app
import pandas as pd
import pymssql
import os


##############################################################################
histscenario = Blueprint('histscenario', __name__, url_prefix='/histscenario')
##############################################################################


@histscenario.route('/runanalysis', methods=['GET', 'POST'])
def run_analysis():
	form = RunAnalysisForm()
	title = "Run Comparision Analysis"

	if request.method == 'POST' and form.validate_on_submit():
		curPcdfFile = form.currentPcdfFile.data
		prePcdfFile = form.previousPcdfFile.data
		curIdxFile = form.currentIdxFile.data
		preIdxFile = form.previousIdxFile.data

		path = os.getcwd() + '/dataAnalysis/static/compfiles'
		preMonPCDF = pd.read_excel(os.path.join(path, prePcdfFile), sheetname = "Sheet1")
		newMonPCDF = pd.read_excel(os.path.join(path, curPcdfFile), sheetname = "Sheet1")
		preMonIdxDF = pd.read_excel(os.path.join(path, preIdxFile), sheetname = "Sheet1")
		newMonIdxDF = pd.read_excel(os.path.join(path, curIdxFile), sheetname = "Sheet1")

		preMonPCDF.reset_index(inplace = True)
		newMonPCDF.reset_index(inplace = True)
		preMonIdxDF.reset_index(inplace = True)
		newMonIdxDF.reset_index(inplace = True)
		preMonPCDF.rename(columns = {"index": "Date"}, inplace = True)
		newMonPCDF.rename(columns = {"index": "Date"}, inplace = True)
		preMonIdxDF.rename(columns = {"index": "Date"}, inplace = True)
		newMonIdxDF.rename(columns = {"index": "Date"}, inplace = True)

		missDF = preMonPCDF[~preMonPCDF.Date.isin(newMonPCDF.Date.values)]
		newDF = newMonPCDF[~newMonPCDF.Date.isin(preMonPCDF.Date.values)]

		#rows = []
		newRows = []
		missRows = []
		if not newDF.empty:
		    newRows = makeAnalysisData(newDF, newMonIdxDF, 'new')
		if not missDF.empty:
		    missRows = makeAnalysisData(missDF, preMonIdxDF, 'miss')

		if newRows and missRows:
			rows = newRows + missRows
		elif newRows:
			rows = newRows
		elif missRows:
			rows = missRows


		return render_template("histscenario/disp_analysis.html",rows = rows)

	return (render_template('histscenario/run_analysis.html', form=form, title=title))


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
		return render_template("histscenario/disp_create.html",rows = rows)

	return (render_template('histscenario/create.html', form=form, title=title))


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

def makeAnalysisData(newmissdf, idxDF, sln):
	data = []
	for index, row in newmissdf.iterrows():
		date = row['Date']
		driver = row['driver']
		idxDF.sort_values(by=[str(driver)], ascending = True, inplace = True)
		dfLength = len(idxDF.index)

		#print date
		# get rank
		rtext = getRank(idxDF, driver, date, dfLength)

		data.append((str(sln),
					str(date),
					str(row['y1']),
					str(row['y2']),
					str(row['y3']),
					str(row['y5']),
					str(row['y7']),
					str(row['y10']),
					str(row['y20']),
					str(row['y30']),
					str(rtext)))
	return data

def getRank(df, driver, date, dfLength):
    rank = ''
    for idx, r in df.iterrows():
        rr = r['Date']
        if str(date) == str(rr):
            if idx > dfLength / 2:
                rank = dfLength - idx
                rank = '-' + str(rank)
            else:
                rank = idx

    rtext = driver + " Relative ranking (" + rank + ")"
    return rtext