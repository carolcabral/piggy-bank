from time import time
from flask import Blueprint, render_template, flash, request, redirect
from flask_login import login_required, current_user
from . import db
from .models import Usina, Inversor, Dados
import json
import datetime
from .reports import *
import pandas as pd 
#from datetime import datetime, timedelta

views = Blueprint('views', __name__)

current_month = datetime.datetime.now().month  # or FROM URL
current_year = datetime.datetime.now().year  # or FROM URL


@views.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        usina_name = request.form['usina'].lower()
        print("Usina name: ", usina_name)

        if usina_name == "other":
            print("New usina = ", request.form['new_usina'])    
            usina_name = request.form['new_usina']
            db.session.add(Usina(name=usina_name))
            db.session.commit()
        
        
        usina = Usina.query.filter_by(name=usina_name).first() 
        if usina.name == 'rainha':
            read_rainha(file, usina_id=usina.id)
        elif usina.name == 'natuvolts':
            read_natuvolts(file, usina_id=usina.id)
       
        return redirect('/')


@views.route('/', methods=['POST', 'GET'])
def home():
    #return Inversor.query.all() 
    return render_template("home.html", dados=Dados.query.all(), usinas = Usina.query.all(), inverters = Inversor.query.all()  )


@views.route('/report/<usina_id>', methods=['GET', 'POST'])
def get_report(usina_id):
    if request.method == 'POST':
        usina_id = request.form['usina'].lower()

    return render_template("dashboard.html", usina= Usina.query.filter_by(id = usina_id).first(), inverters = Inversor.query.filter_by(usina_id=usina_id).all(), res = get_avg_by_usina(usina_id=usina_id))

from io import StringIO
import csv
from werkzeug.wrappers import Response

@views.route('/downloader/<usina_id>')
def downloader(usina_id):
    res =  get_avg_by_usina(usina_id=usina_id)

    def generate():
        

        data = StringIO()
        w = csv.writer(data)

        # write header

        w.writerow(('Inversor', 'Potência CA', 'Potência CC', 'Energia CA'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each log item
        for item in res:
            # print(item)
            # print(item.id, item.avg_power_ca, item.avg_power_cc, item.avg_energy_ca)
            w.writerow((item.name, item.avg_power_ca, item.avg_power_cc, item.avg_energy_ca))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    # stream the response as the data is generated
    response = Response(generate(), mimetype='text/csv')
    # add a filename
    response.headers.set("Content-Disposition", "attachment", filename="log.csv")
    return response


''' ================================================================== '''
def read_natuvolts(file, usina_id):
    xls = pd.ExcelFile(file)

    columns_to_save = [
            'Data e Hora', 'Potência CA (W)', 'Energia CA (kWh)', 'Potência CC (W)', 'Temperatura (ºC)']
    for name in xls.sheet_names:
        inverter_name = name
        df = xls.parse(name)
        
        for row in df[columns_to_save].iterrows():
            _, values = row

            timestamp, power_ca, energy_ca, power_cc, temperature = values
            timestamp = datetime.datetime.timestamp(
                datetime.datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S"))


            try:
                if Inversor.query.filter_by(name=inverter_name).all() == []:
                    db.session.add( Inversor(name=id, usina_id = usina_id ))
                    db.session.commit()

            except Exception as e :
                print("!!!!!!!!!!!!!!!!! EXCEPTION ON NATUVOLTS" + str(e) )

            inverter = Inversor.query.filter_by(name=inverter_name).first()
            data = Dados(
                id=inverter.id,
                timestamp=datetime.datetime.fromtimestamp(timestamp),
                power_ca=float(power_ca.replace(',', '.')),
                power_cc=float(power_cc.replace(',', '.')),
                energy_ca=float(energy_ca.replace(',', '.')),
                #temperature=float(temperature)
                )
            db.session.add(data)
            db.session.commit()

def read_rainha(file, usina_id):
    xls = pd.ExcelFile(file)
    
    columns_to_save = ['Tempo', 'InversorSN', 'Saída CA Potência Total (Ativa)(W)', 'Geração Total (Ativa)(kWh)']

    for name in xls.sheet_names:
        df = xls.parse(name, skiprows=3)  # Rainha
        
        for row in df[columns_to_save].iterrows():
            _, values = row    
            
            timestamp, inverter_name, power_ca, energy_ca = values
            timestamp = timestamp.timestamp()
            
            try:
                if Inversor.query.filter_by(name=inverter_name).all() == []:
                    db.session.add( Inversor(name=id, usina_id = usina_id ))
                    db.session.commit()

            except Exception as e :
                print("!!!!!!!!!!!!!!!!! EXCEPTION ON NATUVOLTS" + str(e) )

            inverter = Inversor.query.filter_by(name=inverter_name).first()


            data = Dados(
                id=inverter.id,
                timestamp=datetime.datetime.fromtimestamp(timestamp),
                #temperature=float(temperature),
                power_ca=float(power_ca),
                energy_ca=float(energy_ca))

            db.session.add(data)
            db.session.commit()


@views.route('/sandbox/<usina_id>', methods=['POST', 'GET'])
def sandbox(usina_id):
    #return Inversor.query.all() 

    res = get_avg_by_usina(usina_id=usina_id)

       

    print(res)
    return render_template("reporte.html", dados = Dados.query.all(), res = res, usinas = Usina.query.all(), inverters = Inversor.query.all())


