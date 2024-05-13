import dataclasses
from flask import Flask, request, jsonify

from model import db_service, car
from model.reservation import *
from repository import AccountRepository, CarRepository, ReservationRepository

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db_service.init_app(app)

car_repo = CarRepository(db_manager=db_service)
account_repo = AccountRepository(db_manager=db_service)
reservation_repo = ReservationRepository(db_manager=db_service)


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


# Routes for cars
@app.route('/cars', methods=['GET'])
def get_cars():
    cars = car_repo.get_all_entities()
    return jsonify([car.to_dict() for car in cars])


@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    car_data = car_repo.get_entity_by_id(car_id)
    if car_data:
        return jsonify(car_data.to_dict())
    else:
        return jsonify({'error': 'Car not found'}), 404


@app.route('/cars', methods=['POST'])
def add_car():
    data = request.json
    car_repo.add_entity(**data)
    return jsonify({'message': 'Car added successfully'}), 201


@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.json
    car_repo.update_entity(car_id, **data)
    return jsonify({'message': 'Car updated successfully'})


@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car_repo.delete_entity(car_id)
    return jsonify({'message': 'Car deleted successfully'})


# Routes for accounts
@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = account_repo.get_all_entities()
    return jsonify([account.to_dict() for account in accounts])


@app.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account_data = account_repo.get_entity_by_id(account_id)
    if account_data:
        return jsonify(account_data.to_dict())
    else:
        return jsonify({'error': 'Account not found'}), 404


@app.route('/accounts', methods=['POST'])
def add_account():
    data = request.json
    account_repo.add_entity(**data)
    return jsonify({'message': 'Account added successfully'}), 201


@app.route('/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    data = request.json
    account_repo.update_entity(account_id, **data)
    return jsonify({'message': 'Account updated successfully'})


@app.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account_repo.delete_entity(account_id)
    return jsonify({'message': 'Account deleted successfully'})


# Routes for reservations
@app.route('/reservations', methods=['GET'])
def get_reservations():
    reservations = reservation_repo.get_all_entities()
    return jsonify([reservation.to_dict() for reservation in reservations])


@app.route('/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    reservation_data = reservation_repo.get_entity_by_id(reservation_id)
    if reservation_data:
        return jsonify(reservation_data.to_dict())
    else:
        return jsonify({'error': 'Reservation not found'}), 404


@app.route('/reservations', methods=['POST'])
def add_reservation():
    data = request.json
    reservation_repo.add_entity(**data)
    return jsonify({'message': 'Reservation added successfully'}), 201


@app.route('/reservations/<int:reservation_id>', methods=['PUT'])
def update_reservation(reservation_id):
    data = request.json
    reservation_repo.update_entity(reservation_id, **data)
    return jsonify({'message': 'Reservation updated successfully'})


@app.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    reservation_repo.delete_entity(reservation_id)
    return jsonify({'message': 'Reservation deleted successfully'})


if __name__ == '__main__':
    # with app.app_context():
    #     car_repo = CarRepository(db_manager=db_service)
    #     kwargs = {
    #         "model": "Enzo",
    #         "brand": "Ferrari",
    #         "year": 2015,
    #         "price": 3e5,
    #         "image": b"0xFF",
    #         "status": car.CarStatus.RESERVED,
    #         "mode": car.CarMode.BUSINESS,
    #     }
    #     car_repo.delete_entity(7)
    app.run()
