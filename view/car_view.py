import json
from http import HTTPStatus

from flask import Blueprint, request, Response

from model.account import AccountPrivilege
from service import ReportContext, UserReportStrategy, ManagerReportStrategy

report_context = ReportContext()
user_report_strategy = UserReportStrategy()
manager_report_strategy = ManagerReportStrategy()


def create_car_blueprint(car_controller, account_controller, car_repository, reservation_repository):
    car_blueprint = Blueprint("car_blueprint", __name__)

    @car_blueprint.route("/api/cars", methods=["GET"])
    def get_all_cars():
        return car_controller.get_all_entities()

    @car_blueprint.route("/api/cars/<int:car_id>", methods=["GET"])
    def get_car_by_id(car_id):
        return car_controller.get_entity_by_id(entity_id=car_id)

    @car_blueprint.route('/api/cars/image/<int:car_id>', methods=['GET'])
    def get_car_image_by_id(car_id):
        return car_controller.get_entity_image_by_id(entity_id=car_id)

    @car_blueprint.route('/api/cars/add', methods=['POST'])
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

    @car_blueprint.route('/api/cars/report', methods=['GET'])
    def get_cars_report():
        account_creds = request.json
        if 'email' not in account_creds or 'password' not in account_creds:
            return Response(status=HTTPStatus.BAD_REQUEST, response="Incorrect request body.")
        account_check = account_controller.check_entity(email=account_creds['email'],
                                                        password=account_creds['password'])
        if account_check.status == HTTPStatus.OK:
            account = json.loads(account_check.json)
            if account.privilege_level == AccountPrivilege.COMMON:
                report_context.set_strategy(user_report_strategy)
            elif account.privilege_level == AccountPrivilege.PRIVILEDGED:
                report_context.set_strategy(manager_report_strategy)
            else:
                return Response(response="No such privilege level.", status=HTTPStatus.NOT_FOUND)
            data = report_context.create_report(
                car_repository=car_repository,
                reservation_repository=reservation_repository,
            )
            return Response(response=json.dumps(data), status=HTTPStatus.OK)
        else:
            return account_check

    @car_blueprint.route('/api/cars/filtered', methods=['GET'])
    def get_filtered_cars():
        filters = request.args.to_dict()
        return car_controller.get_filtered_entities(**filters)

    return car_blueprint
