from flask import Blueprint, request


def create_car_blueprint(car_controller):
    car_blueprint = Blueprint("car_blueprint", __name__)

    @car_blueprint.route("/api/cars", methods=["GET"])
    def get_all_cars():
        return car_controller.get_all_entities()

    @car_blueprint.route("/api/cars/<int:car_id>", methods=["GET"])
    def get_car_by_id(car_id):
        return car_controller.get_entity_by_id(entity_id=car_id)

    @car_blueprint.route("/api/cars/add", methods=["POST"])
    def add_car():
        car_data = request.json
        return car_controller.add_entity(**car_data)

    @car_blueprint.route("/api/cars/update/<int:car_id>", methods=["PUT"])
    def update_car(car_id):
        car_data = request.json
        return car_controller.update_entity(entity_id=car_id, **car_data)

    @car_blueprint.route("/api/cars/delete/<int:car_id>", methods=["DELETE"])
    def delete_car(car_id):
        return car_controller.delete_entity(entity_id=car_id)

    return car_blueprint
