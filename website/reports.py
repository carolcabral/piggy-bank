# from .models import Usina, Inversor, Dados

import datetime
from . import db

from website.models import Dados, Inversor

def query_interval(start_date, end_date):
    return Dados.query.filter(Dados.timestamp > start_date).filter(Dados.timestamp < end_date).all()

def query_by_id(id):
    return Dados.query.filter_by(id = id).all()

# def get_avg_by_usina(usina_id):

#     inverters = Inversor.query.all()


#     # print("Dados", Dados.query.all())
#     return db.session.execute(f'''SELECT id, AVG(power_ca) as avg_power_ca, 
#     AVG(power_ca) as avg_power_ca,
#     AVG(power_cc) as avg_power_cc,
#     AVG(energy_ca) as avg_energy_ca 
#     FROM dados GROUP BY id''').all()

def get_avg_by_usina(usina_id):
    return db.session.execute(f'''SELECT id, name, AVG(power_ca) as avg_power_ca, 
    AVG(power_ca) as avg_power_ca,
    AVG(power_cc) as avg_power_cc,
    AVG(energy_ca) as avg_energy_ca FROM (SELECT *
    FROM dados INNER JOIN inversor on dados.id = inversor.id) WHERE usina_id = {usina_id} GROUP BY id''').all()


   
    # print(Dados.query.filter_by(id=usina_id).all())
    # res = db.select([db.func.avg(Dados.power_ca)]).label('avg_power_ca').filter_by(id=usina_id).all()
    # return res
    #return Dados.query.(func.avg(Inversor.).label('avg_agg'),func.stddev(Foo.foo_id).label('stddev_agg'),func.stddev_samp(Foo.foo_id).label('stddev_samp_agg')

# def query_by_(Dados):
#     for item in Categories.query.order_by(Categories.parent_id).all():
#         print("[ %u | %u ] - %s " % (item.parent_id, item.id, item.name))

# ''' =================================='''


# def last_day_of_month(month):
#     current_year = datetime.datetime.now().year
#     fist_day = datetime.datetime.strptime(
#         f'{month}-{current_year}-1', '%m-%Y-%d')

#     # Guaranteed to get the next month. Force any_date to 28th and then add 4 days.
#     next_month = fist_day.replace(day=28) + datetime.timedelta(days=4)

#     # Subtract all days that are over since the start of the month.
#     return next_month - datetime.timedelta(days=next_month.day)


# def query_interval(start_date, end_date):
#     return Entry.query.filter(Entry.date > start_date).filter(Entry.date < end_date).all()


# def total_balance(query):
#     if query:
#         balance = 0
#         for entry in query:
#             balance += entry.value
#         return balance
#     else:
#         return 0


# ''' ============================================== '''


# def filterCategories(Categories, parent_id):
#     return Categories.query.filter_by(parent_id=parent_id).order_by(Categories.id).all()


# def printbyId(Categories, database):
#     for item in Categories.query.all():
#         print("[ %u | %u ] - %s " % (item.id, item.parent_id, item.name))


# def printbyParent(Categories):
#     for item in Categories.query.order_by(Categories.parent_id).all():
#         print("[ %u | %u ] - %s " % (item.parent_id, item.id, item.name))


# ''' *****************************'''


# def total_expense(entries):
#     entries.query.filter(Entry.value < 0).all()
#     # somar


# def total_recipe(entries):
#     entries.query.filter(Entry.value > 0).all()
#     # somar


# def filter_category(entries, category):
#     return entries.query.filter(Entry.category == category)


# '''reports:
# 1) Flask + plotly
# 2) Despesas fixas (entries.query.filter(Entry.frequency == everytime)) vs receita (total_recipe)

# 3) Pie chart de categorias
#     entries.query.filter()
# '''


#import pandas as pd

#dir_path = "/home/carol/resources/solarbot"


# case NATUVOLTS
#file = f"{dir_path}/Inversor - SJ2ES170L3U600-2022-09-20-1663695240769 - Rainha Alimentos.xlsx"


# def read_file():
#     xls = pd.ExcelFile(file)

#     columns_to_save = ['Tempo', 'InversorSN', 'Saída CA Potência Total (Ativa)(W)', 'Total AC Reactive Power(Var)',
#                        'Geração Total (Ativa)(kWh)', 'Temperatura do Inversor(℃)']

#     # ['Data e Hora', 'Potência CA (W)', 'Energia CA (kWh)', 'Potência CC (W)', 'Temperatura (ºC)']

#     for name in xls.sheet_names:
#         df = xls.parse(name, skiprows=3)
#         print(df.columns.to_list())
#         for row in df[columns_to_save].iterrows():
#             _, values = row

#             # print(x.to_list())  # .split())
#             timestamp, id, power_ca, _, energy_ca, temperature = values
#             print(type(timestamp))
#             print(timestamp.timestamp())
#             print(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
#             print(datetime.datetime.timestamp(
#                 datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")))
#             input()

# df = pd.read_excel(file)
# print(df)



# read_file()
