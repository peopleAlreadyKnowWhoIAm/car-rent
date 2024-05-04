import dataclasses
from flask import Flask

from model import db, car
from model.account import *
from model.reservation import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db.init_app(app)

@app.route('/')
def db_img_retrieval():
        return '<html><head></head><body><img src="img.jpg"></img></body></html>'

@app.route('/img.jpg')
def img():
    a:car.Car = db.get_or_404(car.Car, 1)
    return a.image

@app.route('/json-route')
def mock_json_repr():
    resrs = db.session.get(Reservation, 1)
    return resrs.to_dict()

if __name__ == '__main__':
        app.run()
