from flask import Flask

from controller import AccountController, CarController, ReservationController
from model import db_service
from repository import AccountRepository, CarRepository, ReservationRepository
from view import create_account_blueprint, create_car_blueprint, create_reservation_blueprint

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db_service.init_app(app)

account_repository = AccountRepository(db_manager=db_service)
account_controller = AccountController(account_repository=account_repository)

car_repository = CarRepository(db_manager=db_service)
car_controller = CarController(car_repository=car_repository)

reservation_repository = ReservationRepository(db_manager=db_service)
reservation_controller = ReservationController(reservation_repository=reservation_repository)

account_blueprint = create_account_blueprint(account_controller)
car_blueprint = create_car_blueprint(car_controller, account_controller, car_repository, reservation_repository)
reservation_blueprint = create_reservation_blueprint(reservation_controller)

app.register_blueprint(account_blueprint)
app.register_blueprint(car_blueprint)
app.register_blueprint(reservation_blueprint)

if __name__ == '__main__':
    with app.app_context():
        db_service.create_all()
    app.run(port=5000, host='0.0.0.0')
