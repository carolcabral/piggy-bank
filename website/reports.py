from .models import Entry, Categories

import datetime 

''' ==================================''' 
def last_day_of_month(month):
    current_year = datetime.datetime.now().year
    fist_day =  datetime.datetime.strptime(f'{month}-{current_year}-1', '%m-%Y-%d')

    # Guaranteed to get the next month. Force any_date to 28th and then add 4 days.
    next_month = fist_day.replace(day=28) + datetime.timedelta(days=4)
    
    # Subtract all days that are over since the start of the month.
    return next_month - datetime.timedelta(days=next_month.day)

def query_interval(start_date, end_date):
    return Entry.query.filter(Entry.date > start_date).filter(Entry.date < end_date).all()

def total_balance(query):
    if query:
        balance = 0
        for entry in query:
            balance += entry.value
        return balance
    else: 
        return 0
''' ============================================== '''

def filterCategories(Categories, parent_id):
    return Categories.query.filter_by(parent_id=parent_id).order_by(Categories.id).all()

def printbyId(Categories, database):
    for item in Categories.query.all():
        print("[ %u | %u ] - %s " % (item.id, item.parent_id, item.name))

def printbyParent(Categories):
    for item in Categories.query.order_by(Categories.parent_id).all():
        print("[ %u | %u ] - %s " % (item.parent_id, item.id, item.name))


''' *****************************''' 

def total_expense(entries):
    entries.query.filter(Entry.value < 0).all()
    #somar 
def total_recipe(entries):
    entries.query.filter(Entry.value > 0).all()
    #somar

def filter_category(entries, category):
    return entries.query.filter(Entry.category == category)


'''reports:
1) Flask + plotly
2) Despesas fixas (entries.query.filter(Entry.frequency == everytime)) vs receita (total_recipe)

3) Pie chart de categorias
    entries.query.filter()
'''