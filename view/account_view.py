from http import HTTPStatus
from flask import Blueprint, Response, request


def create_account_blueprint(account_controller):
    account_blueprint = Blueprint('account_blueprint', __name__)

    @account_blueprint.route('/api/accounts', methods=['GET'])
    def get_all_accounts():
        return account_controller.get_all_entities()

    @account_blueprint.route('/api/accounts/<int:account_id>', methods=['GET'])
    def get_account_by_id(account_id):
        return account_controller.get_entity_by_id(entity_id=account_id)

    @account_blueprint.route('/api/accounts/add', methods=['POST'])
    def add_account():
        account_data = request.json
        try:
            return account_controller.add_entity(first_name=account_data['first_name'], last_name=account_data['last_name'], password=account_data['password'], email=account_data['email'])
        except Exception as e:
            return Response(status=HTTPStatus.BAD_REQUEST, response='Wrong parameters')

    @account_blueprint.route('/api/accounts/update/<int:account_id>', methods=['PUT'])
    def update_account(account_id):
        account_data = request.json
        return account_controller.update_entity(entity_id=account_id, **account_data)

    @account_blueprint.route('/api/accounts/delete/<int:account_id>', methods=['DELETE'])
    def delete_account(account_id):
        return account_controller.delete_entity(entity_id=account_id)

    @account_blueprint.put('/api/accounts/login')
    def login_account():
        account_creds = request.json
        if 'email' not in account_creds or 'password' not in account_creds:
            return Response(status=HTTPStatus.BAD_REQUEST, response="You must provide email and password for login")
        return account_controller.check_entity(email=account_creds['email'], password=account_creds['password'])

    return account_blueprint
