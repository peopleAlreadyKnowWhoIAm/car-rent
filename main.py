from flask import Flask

from model import db_service
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
    app.run()
