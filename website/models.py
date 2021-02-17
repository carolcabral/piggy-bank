from . import db
from flask_login import UserMixin
from enum import Enum


class Categories(db.Model):
    ''' Categories database

        - Groups [ ID: 1 | Parent_id: 0 ]
            - Categories [ ID: 2 | Parent_id: 1]
            - Categories [ ID: 3 | Parent_id: 1]
        - Groups [ ID: 4 | Parent_id: 0 ]
            - Categories [ ID: 5 | Parent_id: 4]
            - Categories [ ID: 6 | Parent_id: 4]
            
    
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    parent_id = db.Column(db.Integer, default=0)
    entry_type = db.Column(db.String(10), default="outcome") #Income or outcome

    def __repr__(self):
        #return '<%r [ ID: %u | Parent_id: %u] \t Type: %r>' % (self.name, self.id, self.parent_id, self.entry_type)
        if self.parent_id == 0:
            return ("[ %u ] Group: %s " % (self.id, self.name))
        else:
            return "\t [ %u | %u ] - %s " % (self.parent_id, self.id, self.name)

'''
class Frequency(Enum):
    ONETIME = 1
    EVERYTIME = 2
    SOMETIME_1 = 3  # X parcelas iguais de R$ (entry.value)
    SOMETIME_2 = 4  # R$/X parcelas iguais (x - do form)
'''

Frequencies = Enum('Frequencies', 'onetime everytime sometime1 sometime2')
# Frequencies['onetime']


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    value = value = db.Column(db.Float, default=0)
    item = db.Column(db.String(200), nullable=False)

    category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    #category = db.Column(db.String(20), nullable=False)

    frequency = db.Column(db.Integer)  # mapear para Frequency
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        #return '<Entry [%u] - %r \t R$ %f \t %u | %r >' % (self.id, self.item, self.value, self.category, self.frequency)
        #self.category = other
        return '<Entry [%u]: %r \t R$ %f \t %u \n >' % (self.id, self.item, self.value, self.frequency)

class User(db.Model, UserMixin):
    '''Defines User database '''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))

    # One (user) to many (entries) relationship
    entry = db.relationship('Entry')

    def __repr__(self):
        return '<User %r>' % self.username
