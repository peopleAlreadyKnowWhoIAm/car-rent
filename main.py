import json

from flask import Flask

from controller import CarController, ReservationController
from model import db_service
from repository import CarRepository, ReservationRepository
from service import UserReportStrategy
from view import account_view, car_view, reservation_view

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db_service.init_app(app)

app.register_blueprint(account_view.account_blueprint)
app.register_blueprint(car_view.car_blueprint)
app.register_blueprint(reservation_view.reservation_blueprint)

if __name__ == '__main__':
    with app.app_context():
        db_service.create_all()
        user_service = UserReportStrategy()
        car_controller = CarRepository(db_service)
        res_controller = ReservationRepository(db_service)
        data = user_service.create_report(car_controller, res_controller)
        print(data)
    # app.run(port=5000, host='0.0.0.0')
