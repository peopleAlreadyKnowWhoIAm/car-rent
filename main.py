import dataclasses
from flask import Flask

from model import db_service, car
from model.reservation import *
from repository import CarRepository
from controller import CarController

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db_service.init_app(app)


@app.route('/')
def db_img_retrieval():
    return '<html><head></head><body><img src="img.jpg"></img></body></html>'


@app.route('/img.jpg')
def img():
    a: car.Car = db_service.get_or_404(car.Car, 1)
    return a.image


@app.route('/json-route')
def mock_json_repr():
    resrs = db_service.session.get(Reservation, 1)
    return resrs.to_dict()


if __name__ == '__main__':
    # with app.app_context():
    #     car_repo = CarRepository(db_manager=db_service)
    #     car_controller = CarController(car_repository=car_repo)
    #     response = car_controller.get_all_entities()
    #     print(f"Response: {response.data}")
    app.run()
