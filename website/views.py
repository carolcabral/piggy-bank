from flask import Blueprint, render_template, flash, request, redirect
from flask_login import login_required, current_user
from . import db
from .models import Entry, Categories
import json
import datetime
from .reports import *
#from datetime import datetime, timedelta

views = Blueprint('views', __name__)

current_month = datetime.datetime.now().month #or FROM URL
current_year = datetime.datetime.now().year #or FROM URL 

@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    '''Route to home/agenda page'''
    global current_month, current_year
    
    #Query entries by month 
    #(start date: first day of current month, end_date: last day of current_month)
    start_date = datetime.datetime.strptime(f'{current_month}-{current_year}-1', '%m-%Y-%d')
    
    end_date = datetime.datetime.strptime(f'{current_month}-{current_year}-{last_day_of_month(current_month).day}', '%m-%Y-%d')
    
    entries = query_interval(start_date, end_date)
    
    #Calculate montly estimated (all) balance
    balance = total_balance(entries)
    
    ## TODO: Calculate montly real (paid) balance

    ## TODO: Calculate montly upcoming (tocome) balance
     
    if request.method == "POST":
        
        data = json.loads(request.data)
        current_month = data['currentMonth']

        # Changes year if current_month is December or January 
        current_year = data['currentYear'] + 1 if current_month == 13 else data['currentYear'] - 1 if current_month == 0 else data['currentYear']
        print( "Current year", current_year, current_month)

        # Changes month
        current_month = 1 if current_month == 13 else 12 if current_month == 0 else current_month

        return render_template("home.html", current_month=current_month, current_year=current_year, entries=entries, user=current_user, balance=balance)

    return render_template("home.html", current_month=current_month, current_year=current_year, entries=entries, user=current_user, balance=balance )


'''
@views.route('delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
'''

         

@views.route("/new-entry", methods=['POST', 'GET'])
@login_required
def new_entry():
    #Filter groups by parent_ids
    groups = Categories.query.filter_by(parent_id=0).all()
    categories = Categories.query.all() 
    
    if request.method == "POST":
        '''
        print("POST request")
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                print(key,":",value)

        '''
        entry_type = "outcome" if 'type' in request.form.keys() else "income"
        date = request.form['date']
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        value = float(request.form['value']) if entry_type == "income" else -float(request.form['value'])
        
        item = request.form['item']
        group = request.form['group']
        category = request.form['category']

        # Handle new group or categories
        if group == "other":
            parent_id = 0
            name = request.form['newgroup']
            new_group = Categories(name=name, parent_id=parent_id, entry_type=entry_type)
            db.session.add(new_group)
            db.session.commit()
            group = len(categories) + 1
            #print("Created new group with name %s and id %u, with entry_trype %s" % (name, parent_id, entry_type))
            

        if category == "other":
            parent_id =  group if group != "other" else (len(categories))  
            #print ("Group len = ", len(categories), " | ", parent_id)
            name = request.form['newcategory']
            new_category = Categories(name=name, parent_id=parent_id, entry_type=entry_type)
            #print("Created new category with name %s from group %s, with entry_trype %s" % (name, parent_id, entry_type))
            db.session.add(new_category)
            db.session.commit()
      
        frequency = request.form['frequency']        
        
        ## TODO: Handle maping to current_user

        ## TODO: Handle frequency using Frequencies (if everytime, sometime1, sometime2 )

        ## Create new-entry and add to database        
        new_entry = Entry(date=date, value=value, item=item, category=category, frequency=frequency, user_id=current_user.id)
        db.session.add(new_entry)

        try:
            # Commit all changes to database            
            db.session.commit()
            #return render_template('entry.html', categories=categories, groups=groups, user=current_user)
        except Exception as e:
            flash("Error", category='error')
    
        return redirect('/')
        #return render_template('entry.html', categories=categories, groups=groups, user=current_user)
    else:
        return render_template('entry.html', categories=categories, groups=groups,  user=current_user)

'''
@views.route("/config", methods=['POST', 'GET'])
def config():

    if request.method == 'POST':
        print("POST request")
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                print(key,":",value)

        select = request.form.get('parent-select')
        print(str(select))

    return render_template('config.html', user=current_user)
'''