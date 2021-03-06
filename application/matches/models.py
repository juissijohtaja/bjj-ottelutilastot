from application import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import text


matchpoints = db.Table('matchpoints', 
            db.Column('match_id', db.Integer, db.ForeignKey('match.id'), nullable=False),
            db.Column('points_id', db.Integer, db.ForeignKey('points.id'), nullable=False))    

matchfighter = db.Table('matchfighter', 
            db.Column('match_id', db.Integer, db.ForeignKey('match.id'), nullable=False),
            db.Column('fighter_id', db.Integer, db.ForeignKey('fighter.id'), nullable=False))  
       


class Match(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date=db.Column(db.Date, default=db.func.current_date())
    place=db.Column(db.String(144), nullable=False)
    fighter1_id=db.Column(db.Integer, nullable=False )
    fighter2_id=db.Column(db.Integer, nullable=False)
    winner_id=db.Column(db.Integer)
    winning_category= db.Column(db.String(144))
    comment=db.Column(db.String(244))
    creator_id= db.Column(db.Integer, db.ForeignKey('account.id'), nullable= False)

    points=db.relationship('Points', secondary=matchpoints, backref='match')
    fighters=db.relationship('Fighter', secondary=matchfighter, backref='match')
   

    def __init__(self, date, place, winning_category, fighter1_id, fighter2_id, winner_id, comment, creator_id):
        self.date=date
        self.place = place
        self.winning_category= winning_category
        self.winner_id=winner_id
        self.fighter1_id=fighter1_id
        self.fighter2_id=fighter2_id
        self.winner_id=winner_id
        self.comment=comment
        self.creator_id=creator_id


    @staticmethod
    def get_fighters(match_id):
        stmt= text("SELECT id, name FROM Fighter "
                   + "LEFT JOIN matchfighter ON matchfighter.fighter_id = Fighter.id "
                   + "WHERE matchfighter.match_id = :id").params(id=match_id)

        res=db.engine.execute(stmt)

    

    
        response=[]

        for row in res:
            response. append({"id":row[0], "name":row[1]})

        
        if len(response)==0:
            response. append({"id":'<POISTETTU>', "name":'<POISTETTU>'})
            response. append({"id":'<POISTETTU>', "name":'<POISTETTU>'})

        elif len(response)==1:
            response. append({"id":'<POISTETTU>', "name":'<POISTETTU>'})

        return response
       
