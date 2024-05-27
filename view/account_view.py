import json
from http import HTTPStatus
from flask import Blueprint, Response, request

from controller import AccountController


def create_account_blueprint(account_controller: AccountController):
    account_blueprint = Blueprint('account_blueprint', __name__)

    @account_blueprint.route('/api/accounts', methods=['GET'])
    def get_all_accounts():
        result = account_controller.get_all_entities()
        if result["status"] == 404:
            return Response(response=result["response"], status=HTTPStatus(result["status"]))
        return Response(response=json.dumps([entity.to_dict() for entity in result["response"]]),
                        status=HTTPStatus(result["status"]))

    @account_blueprint.route("/api/accounts/add", methods=["POST"])
    def add_account():
        account_data = request.json
        result = account_controller.add_entity(
            first_name=account_data["first_name"],
            last_name=account_data["last_name"],
            password=account_data["password"],
            email=account_data["email"],
            city=account_data["city"],
            phone_number=account_data["phone_number"],
        )
        if result["status"] == 201:
            return Response(response=json.dumps(result["response"].to_dict()), status=HTTPStatus(result["status"]))
        return Response(status=HTTPStatus(result["status"]))

    @account_blueprint.route('/api/accounts/<int:account_id>', methods=['GET'])
    def get_account_by_id(account_id):
        result = account_controller.get_entity_by_id(entity_id=account_id)
        if result["status"] == 404:
            return Response(response=result["response"], status=HTTPStatus(result["status"]))
        return Response(response=json.dumps(result["response"].to_dict()),
                        status=HTTPStatus(result["status"]))

    @account_blueprint.route('/api/accounts/update/<int:account_id>', methods=['PUT'])
    def update_account(account_id):
        account_data = request.json
        result = account_controller.update_entity(entity_id=account_id, **account_data)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @account_blueprint.route('/api/accounts/delete/<int:account_id>', methods=['DELETE'])
    def delete_account(account_id):
        result = account_controller.delete_entity(entity_id=account_id)
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    @account_blueprint.put('/api/accounts/login')
    def login_account():
        account_creds = request.json
        if 'email' not in account_creds or 'password' not in account_creds:
            return Response(status=HTTPStatus.BAD_REQUEST, response="You must provide email and password for login")
        result = account_controller.check_entity(email=account_creds['email'], password=account_creds['password'])
        if result["status"] == 200:
            return Response(response=json.dumps(result["response"].to_dict()), status=HTTPStatus(result["status"]))
        return Response(response=result["response"], status=HTTPStatus(result["status"]))

    return account_blueprint
